# PyFT (Python File Transfer)

The PyFT is a Python-based file transfer framework that enables file transfer between computers over a TCP/IP connection. It provides classes and methods for handling file transfer operations between a client and a server.

## Features

- Send and receive files between client and server.
- Progress bar display during file transfer.
- Archive files and directories into a zip file.
- Extract files from a zip archive.

## Prerequisites

- Python 3.7 or above.

## Installation

-  Clone the repository from the below code or download the source code from [here](https://github.com/a-sajjad72/pyft/releases/).
```
git clone https://github.com/a-sajjad72/pyft.git
```
**NOTE:** You must have installed [git](https://git-scm.com/) before using the above command.

## Usage
### Client
The Client class is used to implement the client side of the file transfer. It connects to the server and initiates the file transfer process.

```py
from pyft import Client

# Create a client instance
client = Client(serverHost, serverPort)

# Start the client
client.start_client()
```

- `serverHost` (str): The IP address or hostname of the server.
- `serverPort` (int): The port number of the server.

#### Write your own Client code
You can write your own client code by overiding the `server_response` method by inheriting the Client class. Example shown below
```py
from pyft import Client, FileTransfer

class MyClient(Client):
    def __init__(self, serverHost: str, serverPort: int):
        super().__init__(serverHost, serverPort)
        self.start_client()

    def response_server(self, conn) -> None:
        ft = FileTransfer(conn)
        ft.send_file(file)

if __name__ == "__main__":
    client = MyClient('127.0.0.1',9999)
```
### Server
The Server class handles the server side of the file transfer. It listens for client connections and handles file transfer operations.

```py
from pyft import Server

# Create a server instance
server = Server(host, port, maxClients)

# Start the server
server.start_server()
```
- `host` (str, optional): The IP address or hostname of the server. If not provided, it will use the local IP address.
- `port` (int, optional): The port number of the server. Defaults to 9999.
- `maxClients` (int, optional): The maximum number of clients that can be connected to the server. Defaults to 8.

#### Write your own Server code
Like Client class you can also write your own server code by overiding `client_handler` method of Server class. Example shown below.
```py
from pyft import Server, FileTransfer
class MyServer(Server):
    def __init__(self, host=None, port: int = 9999, maxClients: int = 8):
        super().__init__(host, port, maxClients)
    
    def client_handler(self, conn, addr) -> None:
        ft = FileTransfer(conn)
        ft.recv_file()

if __name__ == "__main__":
    server = MyServer('127.0.0.1')
```
### FileTransfer
The FileTransfer class provides methods for sending and receiving files between the client and server. It also provide methods to archive files and directories before sending.

#### Receiving Files
To receive a file from the server, create an instance of the FileTransfer class and call the recv_file method. 
```py
# initialized server/client connection

...

ft = FileTransfer(connection)

# Receive a file
ft.recv_file(path)
```
- `connection`: Socket for the connection to send/receive data.
- `path` (str, optional): The path of the directory to store the received file. Defaults to the current working directory.

Also see example [here](#write-your-own-server-code)

#### Sending Files
To send a file to the server, create an instance of the FileTransfer class and call the send_file method.

```py
# initialized server/client connection

...

ft = FileTransfer(connection)

# Send a file
ft.send_file(filePath)
```

 - `connection`: Socket for the connection to send/receive data.
 - `filePath` (str): Path/name of the file to send.

Also see example [here](#write-your-own-client-code)

#### Archiving Files
The FileTransfer class also provides methods to archive files and directories into a zip file.

```py
# initialized server/client connection

...

ft = FileTransfer(connection)

# Archive files and directories
ft.archive(name, items)
```

- `name` (str): Path/name to name the archived zip file.
- `items` (list): List of paths of the files or directories to archive.

#### Extracting Files
You can also extract files from a zip archive using the `extract` method.

```py
# initialized server/client connection

...

FileTransfer.extract(src, dest)
```

- `src` (str): Path of the archive to extract.
- `dest` (str, optional): Path to extract the archive. Defaults to the current working directory.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
Feel free to contribute to the project by reporting [issues](https://github.com/a-sajjad72/pyft/issues), submitting [pull requests](https://github.com/a-sajjad72/pyft/pulls) or improving [documenataion](https://github.com/a-sajjad72/pyft/blob/master/documentation.md). You know the documentation is not so well that's why improvement in documentation is also greatly appreciated.

**NOTE:** Please make sure you forked the repository before making any contributions.