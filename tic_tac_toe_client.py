#########################################
# Aishwarya Manicka Ravichandran
# CS372 - Introduction to Computer Networks
# Summer 2020
# Program: client.py
#References: https://pythonprogramming.net/client-chatroom-sockets-tutorial-python-3/
#           https://docs.python.org/3/library/socket.html
#           https://www.youtube.com/watch?v=WM1z8soch0Q
#           https://www.youtube.com/watch?v=Lbfe3-v7yE0
#           https://www.tutorialspoint.com/simple-chat-room-using-python
#           https://realpython.com/python-sockets/
#           https://techwithtim.net/tutorials/python-programming/tic-tac-toe-tutorial/
#           https://stackoverflow.com/questions/53658969/tic-tac-toe-client-server-interaction
##########################################
import socket
import sys 
import re

#function to initialize the game board
def init_game(client_socket):
    board = [' ' for x in range(10)]
    print("Server will start the game")
    print_board(board)
    #start the game
    start_game(client_socket, board)

#function to start the game
def start_game(client_socket, board):
    
    while True:
        
        #get the server's move
        server_move = client_socket.recv(1024).decode('utf-8')

        #if the server's move is either a server's winning msg or draw msg
        if(re.search("Server Won", server_move) or re.search("Game Draw", server_move)):
            final_move = client_socket.recv(1024).decode('utf-8')
            board[int(final_move)] = 'X'
            print("Server's move: ", str(final_move))
            print_board(board)
            print(server_move)
            break
        
        #if the server's move is quitting the game
        elif(re.search("quit the game", server_move)):
            print(server_move)
            break

        #if the server's move is client's winning message
        elif(re.search("You Won", server_move)):
            print(server_move)
            break
        #if the server's move is an actual move in the game board
        else:
            server_move = int(server_move)
            #update board
            print("Server's Move: ", server_move)
            board[server_move] = 'X'
            #print board
            print_board(board)

            #get the move from client
            print("Your turn")
            client_move = input("Enter your position in the grid (1-9) \n > ")
            
            #check if the client's msg is a quit msg
            if(str(client_move) == '/q'):
                client_quit = "Client has quit the game..Byee"
                print("Thanks for playing")
                client_socket.send(bytes(client_quit, 'utf-8'))
                break
            
            else:
                #convert the client_move's type to int
                client_move = int(client_move)
                #check if the client's move is valid
                while (client_move < 1 or client_move > 9 or board[client_move] != ' '):
                    client_move = int(input("Invalid!!Enter your position in the grid \n > "))

                #if valid, update the board and print it
                board[client_move] = 'O'
                print_board(board)
                #send the client's move to server
                client_socket.send(bytes(str(client_move), 'utf-8'))
                print("Wait for the server to play...")


#function to print the game board
def print_board(board):
    print('******************')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('******************')

#function which handles the server client chat in the client side of the project
def server_chat(client_socket):
    
    msg_recv = client_socket.recv(1024).decode('utf-8')
    print(msg_recv)
    #prompt for the message to be sent to the server 
    msg_to_send = input(">")
    
    #send the message by converting into bytes to the server
    client_socket.send(bytes(msg_to_send, 'utf-8'))

    #if the client wants to continue, intiate the game
    if(re.search("yes", msg_to_send)):
        print("Type /q when you want to quit")
        init_game(client_socket)
    #if the client doesnt want to continue, send quit msg
    else:
        msg_recv = client_socket.recv(1024).decode('utf-8')
        print(msg_recv)
        return
        

#main function       
def main():

    #host and port for connecting the socket
    host = socket.gethostbyname("localhost")
    port = 7777

    #set up a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect the socket with the host and port
    client_socket.connect((host, port))
    print("Connected to: ", host, "on port:", port)

    #start the chat with the server
    server_chat(client_socket)
    #After chatting is exited, close the socket
    client_socket.close()

#call for main function
if __name__ == '__main__':
    main()
