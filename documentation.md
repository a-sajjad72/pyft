<a id="pyft"></a>

# pyft

<a id="pyft.FileTransfer"></a>

## FileTransfer Objects

```python
class FileTransfer()
```

A class for handling file transfer between client and server.

**Arguments**:

  conn : Socket for the connection to send/receive data.
- `bufferSize` _int, optional_ - The buffer size for sending/receiving data. Defaults to 4096 B (4 KiB)

<a id="pyft.FileTransfer.recv_file"></a>

#### recv\_file

```python
def recv_file(path: str = os.getcwd()) -> str
```

Receives the file from the initialized connection.

Args: path (str, optional): The path of the directory to store received file. Defaults to current working directory.

**Returns**:

- `str` - Name of the received file.

<a id="pyft.FileTransfer.send_file"></a>

#### send\_file

```python
def send_file(filePath: str) -> None
```

Sends the file to the initialized connection.

**Arguments**:

- `filePath` _str_ - path/name of the file to send.

<a id="pyft.FileTransfer.send_msg"></a>

#### send\_msg

```python
def send_msg(msg: str) -> None
```

Sends a message to the initialized connection.

**Arguments**:

- `msg` - The message to send.

<a id="pyft.FileTransfer.recv_msg"></a>

#### recv\_msg

```python
def recv_msg() -> str
```

Receives a message from the initialized connection.

**Returns**:

- `str` - The received message.

<a id="pyft.FileTransfer.archive"></a>

#### archive

```python
def archive(name: str, items: list) -> None
```

A method that creates Zipfile to archive files and directories.

**Arguments**:

- `name` _str_ - to name the archived zip. may also contains path alongwith the filename to store it on different path. if not provided the archived file is created in the current working directory.
- `items` _list_ - the paths of the files, directories to archive.

<a id="pyft.FileTransfer.zipFile"></a>

#### zipFile

```python
def zipFile(path: str, ziph) -> None
```

write the file to the Zipfile.

**Arguments**:

- `path` _str_ - path of file to be archive
- `ziph` - Zipfile to write the file

<a id="pyft.FileTransfer.zipDir"></a>

#### zipDir

```python
def zipDir(path: str, ziph) -> None
```

write the directory to the Zipfile.

**Arguments**:

- `path` _str_ - path of directory to be archive
- `ziph` - Zipfile to write the directory

<a id="pyft.FileTransfer.extract"></a>

#### extract

```python
def extract(src: str, dest: str = os.getcwd()) -> None
```

extract the Zipfile file to the dest directory.

**Arguments**:

- `src` _str_ - path of the archive to extract
- `dest` - path to extract the archive. Defaults to current working directory

<a id="pyft.Client"></a>

## Client Objects

```python
class Client()
```

A class that implements the client side of file transfer.

**Arguments**:

- `serverHost` _str_ - The IP address or hostname of the server.
- `serverPort` _int_ - The port number of the server.

<a id="pyft.Client.start_client"></a>

#### start\_client

```python
def start_client() -> None
```

Starts the client.

<a id="pyft.Client.response_server"></a>

#### response\_server

```python
def response_server(conn) -> None
```

Handles the response from the server and respond to the server to perform necessary actions.

**Arguments**:

- `conn` - Socket for the connection to the server.

<a id="pyft.Server"></a>

## Server Objects

```python
class Server()
```

A class for handling the server side of the file transfer.

**Arguments**:

- `host` _str_ - The IP address or hostname of the server. Defaults to loacl ip address.
- `port` _int, optional_ - The port number of the server. Defaults to 9999.
- `maxClients` _int, optional_ - The maximum number of clients that can be connected to the server. Defaults to 8.

<a id="pyft.Server.start_server"></a>

#### start\_server

```python
def start_server() -> None
```

Starts the server and accepts connections from clients.

<a id="pyft.Server.accept_connections"></a>

#### accept\_connections

```python
def accept_connections() -> None
```

Accepts connections from the clients.

<a id="pyft.Server.client_handler"></a>

#### client\_handler

```python
def client_handler(conn, addr: tuple) -> None
```

Handles connected clients to the server.

**Arguments**:

- `conn` - Socket representing the connection to the client.
- `addr` _tuple_ - A tuple containing the IP address and port number of the client.

<a id="pyft.Server.accept_connections"></a>

#### accept\_connections

```python
def accept_connections() -> None
```

Accepts incoming connections.

<a id="pyft.Server.get_ip"></a>

#### get\_ip

```python
def get_ip() -> str
```

returns the local ip address

