# TicTacToeWithSocketProgramming
Tic tac toe game between server and client using socket programming

To run the program, open a terminal and run the server using the following command
```
python3 tic_tac_toe_server.py
```
Server will start running and will be waiting for the client to connect

To start a client, open another termina and run using the following command
```
python3 tic_tac_toe_client.py
```
Client gets connected to the server.

The server prompts the client, whether it is willing to start the game. 
If yes, server starts playing the game. 
If no, the server gets disconnected and the sockets close.
