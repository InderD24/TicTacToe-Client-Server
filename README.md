# TicTacToe Client-Server

This project implements a simple network Tic Tac Toe game using Python sockets and Tkinter.
One machine runs `host.py` to act as the server while another runs `client.py` to connect as a player.

## Getting Started

1. **Find the Host IP**
   ```bash
   python3 IP.py
   ```
   Use the printed address when the client is prompted for the host IP.

2. **Run the Host**
   ```bash
   python3 host.py
   ```
   The host waits for a single connection and displays a GUI to play the game.

3. **Run the Client**
   ```bash
   python3 client.py
   ```
   When prompted, enter the host IP and port (default `5050`).

Both applications must be able to reach each other over the network.

## Files

- `host.py` – server application and GUI for player one.
- `client.py` – client application and GUI for player two.
- `gameboard.py` – board state and win logic.
- `IP.py` – helper script to print the host machine's IP address.

## Requirements

- Python 3
- Tkinter (usually included with standard Python distributions)

The game windows provide buttons to make moves and communicate between host and client. After a game ends you can choose to play again or close the connection.
