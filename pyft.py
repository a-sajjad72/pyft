import socket
from _thread import *
import threading
import os, zipfile
import json
from pip._vendor.rich import filesize
from pip._vendor.rich.console import Console
from pip._vendor.rich.progress import (
    Progress,
    Task,
    TextColumn,
    BarColumn,
    TransferSpeedColumn,
    DownloadColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from pip._vendor.rich.table import Column
from pip._vendor.rich.text import Text  # for progress bar


class FileTransfer:
    """
    A class for handling file transfer between client and server.

    Args:
        conn : Socket for the connection to send/receive data.
        bufferSize (int, optional): The buffer size for sending/receiving data. Defaults to 4096 B (4 KiB)
    """

    def __init__(self, conn, bufferSize: int = 4096):
        self.conn = conn
        self.bufferSize = bufferSize

    def recv_file(self, path: str = os.getcwd()) -> str:
        """
        Receives the file from the initialized connection.

        Args: path (str, optional): The path of the directory to store received file. Defaults to current working directory.

        Returns:
            str: Name of the received file.
        """

        try:
            file_details = self.recv_msg()
            file_details = json.loads(file_details)
            filename, filesize = file_details["filename"], file_details["filesize"]
            console = Console()
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                MyDownloadColumn(binary_units=True, precision=2),
                TextColumn("at"),
                TransferSpeedColumn(),
                TextColumn("in"),
                TimeElapsedColumn(),
                transient=True,
            ) as progress:
                console.print(filename, style="bold")
                recv_task = progress.add_task("Receiving", total=filesize)
                bytes_received = 0
                with open(os.path.join(path, filename), "wb") as f:
                    while bytes_received < filesize:
                        data = self.conn.recv(
                            min(self.bufferSize, filesize - bytes_received)
                        )
                        if not data:
                            break
                        elif data:
                            bytes_received += f.write(data)
                        progress.update(recv_task, completed=bytes_received)
            self.send_msg(str(bytes_received))
            result = bool(self.recv_msg())
            if result:
                console.print(f"{filename} successfully received", style="bold green")
            return filename

        except Exception as e:
            return f"ERROR while receiving: {e}"

    def send_file(self, filePath: str) -> None:
        """
        Sends the file to the initialized connection.

        Args:
            filePath (str): path/name of the file to send.
        """

        try:
            filename = os.path.basename(
                filePath.rstrip("\\" if os.name == "nt" else "/")
            )
            filesize = os.path.getsize(filePath)
            self.send_msg(json.dumps({"filename": filename, "filesize": filesize}))
            console = Console()
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                MyDownloadColumn(binary_units=True, precision=2),
                TextColumn("at"),
                TransferSpeedColumn(),
                TextColumn("in"),
                TimeElapsedColumn(),
                transient=True,
            ) as progress:
                console.print(filename, style="bold")
                send_task = progress.add_task("Sending", total=filesize)
                bytes_sent = 0
                with open(filePath, "rb") as f:
                    while True:
                        data = f.read(self.bufferSize)
                        if not data:
                            break
                        bytes_sent += self.conn.send(data)
                        progress.update(send_task, completed=bytes_sent)
            bytes_received = int(self.recv_msg())
            result = bytes_received == bytes_sent
            self.send_msg(str(result))
            if result:
                console.print(f"{filename} successfully sent", style="bold green")

        except Exception as e:
            return f"ERROR while sending: {e}"

    def send_msg(self, msg: str) -> None:
        """
        Sends a message to the initialized connection.

        Args:
            msg: The message to send.
        """

        message_length = len(msg.encode())
        self.conn.send(message_length.to_bytes(4, byteorder="big"))
        self.conn.send(msg.encode())

    def recv_msg(self) -> str:
        """
        Receives a message from the initialized connection.

        Returns:
            str: The received message.
        """

        msg_length_bytes = self.conn.recv(4)
        msg_length = int.from_bytes(msg_length_bytes, byteorder="big")
        del msg_length_bytes
        msg = ""
        while len(msg) < msg_length:
            data = self.conn.recv(msg_length - len(msg)).decode()
            if not data:
                break  # end of stream
            msg += data

        return msg

    def archive(self, name: str, items: list) -> None:
        """
        A method that creates Zipfile to archive files and directories.

        Args:
            name (str): to name the archived zip. may also contains path alongwith the filename to store it on different path. if not provided the archived file is created in the current working directory.
            items (list): the paths of the files, directories to archive.
        """

        with zipfile.ZipFile(f"{name}", "w", zipfile.ZIP_DEFLATED) as zf:
            for item in items:
                if os.path.isdir(item):
                    self.zipDir(item, zf)
                elif os.path.isfile(item):
                    self.zipFile(item, zf)

    def zipFile(self, path: str, ziph) -> None:
        """
        write the file to the Zipfile.
        Args:
            path (str): path of file to be archive
            ziph: Zipfile to write the file
        """

        ziph.write(
            path, os.path.basename(path.rstrip("\\" if os.name == "nt" else "/"))
        )

    def zipDir(self, path: str, ziph) -> None:
        """
        write the directory to the Zipfile.
        Args:
            path (str): path of directory to be archive
            ziph: Zipfile to write the directory
        """

        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), os.path.join(path, "..")),
                )

    def extract(src: str, dest: str = os.getcwd()) -> None:
        """extract the Zipfile file to the dest directory.
        Args:
            src (str): path of the archive to extract
            dest: path to extract the archive. Defaults to current working directory
        """

        with zipfile.ZipFile(src) as ziph:
            ziph.extractall(dest)


# ------------------------------------------------------------------------------#


class Client:
    """
    A class that implements the client side of file transfer.

    Args:
        serverHost (str): The IP address or hostname of the server.
        serverPort (int): The port number of the server.
    """

    def __init__(self, serverHost: str, serverPort: int):
        self.serverHost = serverHost
        self.serverPort = serverPort

    def start_client(self) -> None:
        """
        Starts the client.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            clientSocket.connect((self.serverHost, self.serverPort))
            print(f"Connected to [{self.serverHost}:{self.serverPort}]")

            self.response_server(clientSocket)

            print("Connection closed")

    def response_server(self, conn) -> None:
        """
        Handles the response from the server and respond to the server to perform necessary actions.

        Args:
        conn: Socket for the connection to the server.
        """

        # Initiates FileTransfer class to make communication between client and server
        fileTransfer = FileTransfer(conn, 4096)

        # Recieve Welcome message from the server
        server_msg = fileTransfer.recv_msg()

        # Print the received message
        print(f"[SERVER] {server_msg}")


# ------------------------------------------------------------------------------#


class Server:
    """
    A class for handling the server side of the file transfer.

    Args:
        host (str, optional): The IP address or hostname of the server. Defaults to loacl ip address.
        port (int, optional): The port number of the server. Defaults to 9999.
        maxClients (int, optional): The maximum number of clients that can be connected to the server. Defaults to 8.
    """

    def __init__(self, host=None, port: int = 9999, maxClients: int = 8):
        if not host:
            self.host = self.get_ip()
        else:
            self.host = host
        self.port = port
        self.maxClients = maxClients

    def start_server(self) -> None:
        """
        Starts the server and accepts connections from clients.
        """
        # Create a server socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the server socket to the given host and port
        self.serverSocket.bind((self.host, self.port))

        # Start listening for client connections
        self.serverSocket.listen(self.maxClients)

        print(f"Server started on {self.host}:{self.port}")

        # Accept connections from clients
        self.accept_connections()

    def accept_connections(self) -> None:
        """
        Accepts connections from the clients.
        """
        while True:
            # Accept a client connection
            conn, addr = self.serverSocket.accept()

            # Handle the client connection in a separate thread

            threading.Thread(target=self.client_handler, args=(conn, addr)).start()

    def client_handler(self, conn, addr: tuple) -> None:
        """
        Handles connected clients to the server.

        Args:
            conn: Socket representing the connection to the client.
            addr (tuple): A tuple containing the IP address and port number of the client.
        """

        print(f"New client connected: {addr[0]}:{addr[1]}")

        # while True:
        fileTransfer = FileTransfer(conn)

        # Sends message to the client
        fileTransfer.send_msg("Welcome to Our Server")

        # Close the connection to the client
        print(f"Closing connection to client {addr[0]}:{addr[1]}")
        conn.close()

    def accept_connections(self) -> None:
        """
        Accepts incoming connections.
        """

        while True:
            # Accept a client connection
            conn, addr = self.serverSocket.accept()

            # Handle the client connection in a separate thread
            start_new_thread(self.client_handler, (conn, addr))

            print(f"New client connected: {addr[0]}:{addr[1]}")

    def get_ip(self) -> str:
        """
        returns the local ip address
        """

        hostname = socket.getfqdn()
        return socket.gethostbyname_ex(hostname)[2][-1]


class MyDownloadColumn(DownloadColumn):
    def __init__(
        self,
        binary_units: bool = False,
        precision: int = 1,
        table_column: Column | None = None,
    ) -> None:
        self.precision = precision
        super().__init__(binary_units, table_column)

    def render(self, task: Task) -> Text:
        """Calculate common unit for completed and total."""
        completed = int(task.completed)

        unit_and_suffix_calculation_base = (
            int(task.total) if task.total is not None else completed
        )
        if self.binary_units:
            unit, suffix = filesize.pick_unit_and_suffix(
                unit_and_suffix_calculation_base,
                ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"],
                1024,
            )
        else:
            unit, suffix = filesize.pick_unit_and_suffix(
                unit_and_suffix_calculation_base,
                ["bytes", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"],
                1000,
            )
        precision = 0 if unit == 1 else self.precision

        completed_ratio = completed / unit
        completed_str = f"{completed_ratio:,.{precision}f}"

        if task.total is not None:
            total = int(task.total)
            total_ratio = total / unit
            total_str = f"{total_ratio:,.{precision}f}"
        else:
            total_str = "?"

        download_status = f"{completed_str}/{total_str} {suffix}"
        download_text = Text(download_status, style="progress.download")
        return download_text
