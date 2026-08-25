# network-distributed-computing
# Network Distributed Computing

A **JSON-RPC-based peer-to-peer remote management system** developed as part of a university assignment for the Network Distributed Computing module.

The project consists of a client and multiple interconnected servers. The client can issue remote system-management commands to a server, while servers can communicate with one another to discover peers, exchange messages, and coordinate server availability.

## Project Overview

The system was designed to provide remote management functionality without implementing a low-level socket protocol directly. Instead, **JSON-RPC** is used for communication between the client and servers.

Each server operates on its own port and maintains a list of other servers it knows about ("friends"). Servers can notify one another when they come online or go offline, perform heartbeat checks, and forward messages between servers.

The client is capable of communicating with multiple servers and issuing commands sequentially.

## Features

### Remote Management

The client can request servers to perform several management tasks, including:

* Create and delete folders
* Search for files in the server's current directory
* Retrieve the server's identity and port
* Retrieve the server's Python version
* Ping a server and receive a `pong` response
* Start and shut down additional servers

### Peer-to-Peer Server Communication

Servers can communicate with other servers to maintain an awareness of the network:

* **`list_friends`** — list known server ports
* **`online`** — notify other servers that a server has joined the network
* **`offline`** — notify other servers that a server has left the network
* **`heartbeat`** — ping known server peers and return their responses
* **`pass`** — forward a message through the server network until it reaches the specified server

### Testing

The project includes Python unit tests covering the server functionality and implemented commands.

## Technologies

* **Python**
* **JSON-RPC**
* **Python unit testing**
* Client-server architecture
* Peer-to-peer server communication

## Project Structure

```text
network-distributed-computing/
├── src/
│   ├── c.py
│   ├── s.py
│   ├── test_server.py
│   └── run_server.bat
│
├── docs/
│   └── Assignment1_Report.pdf
│
└── README.md
```

## Commands

The server implements the following commands:

| Command               | Description                                      |
| --------------------- | ------------------------------------------------ |
| `make_folder XXXXX`   | Creates a folder on the server                   |
| `delete_folder XXXXX` | Deletes a folder on the server                   |
| `whoareyou`           | Returns the server number and port               |
| `get_version`         | Returns the server's Python version              |
| `ping`                | Returns `pong`                                   |
| `search XXXXX`        | Searches for a filename in the current directory |
| `startup X`           | Starts another server on port `500X`             |
| `shutdown X`          | Shuts down a server running on port `500X`       |
| `list_friends`        | Returns the server's known peers                 |
| `online X`            | Notifies peers that a server has come online     |
| `offline X`           | Notifies peers that a server has gone offline    |
| `heartbeat`           | Checks the availability of known server peers    |
| `pass msg x`          | Forwards a message to the specified server       |

## Running the Project

The server can be started using the provided batch script:

```text
src\run_server.bat
```

The client can be started using:

```text
python src\c.py
```

The unit tests can be run using:

```text
python src\test_server.py
```

The exact runtime configuration and server ports used by the application are documented in the accompanying assignment report.

## Documentation

The original assignment report, including the project code, testing results, and system diagrams, is available in the [`docs`](docs/) directory.

## University Project

This project was developed as **Assignment 1** for the **Network Distributed Computing** module.

The assignment focused on developing a distributed remote-management system using JSON-RPC, with support for multiple interconnected servers and client-to-server communication.

