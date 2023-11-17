# =================================================================================================
# Contributing Authors:	    Alexander Wise, Ruby Harris and Michaela Winfree
# Email Addresses:          Alex.Wise@uky.edu,
# Date:                     11/16/2023
# Purpose:                  This is the server file for the game of pong. It creates a server and 
#                               updates client game instances through sockets and threads.
# Misc:                     To test this program on a single machine:
#                               1. Open an instance of VS Code and open pongServer.py in it.
#                               2. Open another instance of VS Code and open the PongProject folder
#                                       in it.
#                               3. Open the pongClient.py from the Explorer in the instance of VS 
#                                       Code from step 2.
#                               4. Click the run button for the pongServer.py file.
#                               5. Click the run button for the pongClient.py file.
#                               6. Open a new terminal in the instance of VS Code from step 2.
#                               7. Copy and paste the run command from the Python terminal
#                                       generated by step 5 to the terminal from step 6.
#                               8. Finally, use the values given by HOST and PORT below
#                                       for the Server IP and Server Port, and enjoy. - Alex 
# =================================================================================================


#1.1.0- You can try running this (still untested)... It might work... maybe...
import socket
import threading
# used to encode to strings for the sending to and from server
import json
from socket_wrapper import sock_wrapper
# Constants
# IP of the host of the server. 
# Ensure that the IP is the same as the pongClient.py.
HOST = "localhost"
# Port # of the server. Set > 1023 for non-priveleged ports. 
# Ensure that the # is the same as the pointClient.py.
PORT = 5000

# Use this file to write your server logic
# You will need to support at least two clients
# Game Information
class gameSave:
    def __init__(self):
        self.ball_lock = threading.Lock()
        self.ballx = 0 # X, Y
        self.bally = 0
        self.score_lock = threading.Lock()
        self.score = [0,0] # lScore, rScore

        self.rPaddle_lock = threading.Lock()
        self.rPaddlex = 0 # X, Y, Moving
        self.rPaddley = 0
        self.rPaddlemov = ''

        self.lPaddle_lock = threading.Lock()
        self.lPaddlex = 0 # X, Y, Moving
        self.lPaddley = 0
        self.lPaddlemov = ''

        self.sync_lock = threading.Lock()
        self.sync = 0 # The current sync between the two clients

        self.lReady_lock = threading.Lock()
        self.lReady = False # Is the left player ready to start?

        self.rReady_lock = threading.Lock()
        self.rReady = False # is the right player ready to start?


def clientControl(shutDown, game, clientSocket, clientNumber):
    Connection = sock_wrapper(clientSocket)

    while not shutDown.is_set() and not Connection.closed:
        # Receive data from the client
        _ , newMessage = Connection.recv()

        if newMessage is None:
            break

        if newMessage['type'] == 'start':
            if clientNumber == 0:
                with game.lReady_lock:
                    game.lReady = True
                newMessage['playerpaddle'] = 'left'

            elif clientNumber == 1:
                with game.rReady_lock:
                    game.rReady = True
                newMessage['playerpaddle'] = 'right'

            with game.lReady_lock, game.rReady_lock:
                if game.lReady and game.rReady:
                    newMessage['data'] = True
                else:
                    newMessage['data'] = False
                Connection.send(newMessage)
            continue

        if newMessage['type'] == 'gimme':
            if clientNumber == 0:
                with game.sync_lock:
                    newMessage['data']['seq'] = game.sync
                with game.ball_lock:
                    newMessage['data']['ballx'] = game.ballx
                    newMessage['data']['bally'] = game.bally
                with game.score_lock:
                    newMessage['data']['score'] = game.score
                with game.rPaddle_lock:
                    newMessage['data']['opponentpaddlex'] = game.rPaddlex
                    newMessage['data']['opponentpaddley'] = game.rPaddley
                    Connection.send(newMessage)
                    print("sent update")
            elif clientNumber == 1:
                with game.sync_lock:
                    newMessage['data']['seq'] = game.sync
                with game.ball_lock:
                    newMessage['data']['ballx'] = game.ballx
                    newMessage['data']['bally'] = game.bally
                with game.score_lock:
                    newMessage['data']['score'] = game.score
                with game.lPaddle_lock:
                    newMessage['data']['opponentpaddlex'] = game.lPaddlex
                    newMessage['data']['opponentpaddley'] = game.lPaddley
                Connection.send(newMessage)
                print("sent update")
            continue

        if newMessage['type'] == 'update':
            with game.sync_lock:
                if clientNumber == 0 and game.sync >= newMessage['data']['seq']:
                    with game.lPaddle_lock:
                        game.lPaddlex = newMessage['data']['playerpaddlex']
                        game.lPaddley = newMessage['data']['playerpaddley']
                        game.lPaddlemov = newMessage['data']['playermov']
                        print("update recvd")
                    continue
                elif clientNumber == 1 and game.sync >= newMessage['data']['seq']:
                    with game.rPaddle_lock:
                        game.rPaddlex = newMessage['data']['playerpaddlex']
                        game.rPaddley = newMessage['data']['playerpaddley']
                        game.rPaddlemov = newMessage['data']['playermov']
                        print("update recvd")
                    continue
            with game.sync_lock:
                game.sync = newMessage['data']['seq']
            with game.ball_lock:
                game.ballx = newMessage['data']['ballx']
                game.bally = newMessage['data']['bally']
            with game.score_lock:
                game.score = newMessage['data']['score']
                
            if clientNumber == 0:
                with game.lPaddle_lock:
                    game.lPaddlex = newMessage['data']['playerpaddlex']
                    game.lPaddley = newMessage['data']['playerpaddley']
                    game.lPaddlemov = newMessage['data']['playermov']
            elif clientNumber == 1:
                with game.rPaddle_lock:
                    game.rPaddlex = newMessage['data']['playerpaddlex']
                    game.rPaddley = newMessage['data']['playerpaddley']
                    game.rPaddlemov = newMessage['data']['playermov']

            print("update recvd")
            continue
        else:
            print(f"Unknown message type: {newMessage['type']}")




def main():
    print('Server Online')

    # Create our server type 1 socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server socket to the HOST and PORT
    server.bind((HOST, PORT))

    # List of client threads
    clientThreads = []

    # Event to shutdown the server
    endServer = threading.Event()

    server.listen()

    gameState = gameSave()

    clientNum = 0
    maxClient = 2

    while not endServer.is_set() and clientNum < maxClient:
        # Accept a connection from a client
        newClient, retAddress = server.accept()
        print('Client ' + str(retAddress) + ' connected.')

        # Create a new thread for each client
        newThread = threading.Thread(target=clientControl, args=(endServer, gameState, newClient, clientNum))
        newThread.start()
        clientThreads.append(newThread)  # Store the thread reference in the list
        clientNum += 1

    server.close()

    # Join all client threads for proper termination
    for client in clientThreads:
        client.join()


  
    print('Server Closing')

if __name__ == "__main__": 
    main()