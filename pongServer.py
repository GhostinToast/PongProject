# =================================================================================================
# Contributing Authors:	    Alexander Wise, Ruby Harris and Michaela Winfree
# Email Addresses:          Alex.Wise@uky.edu,
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
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
PORT = 4000

# Use this file to write your server logic
# You will need to support at least two clients
# Game Information
class gameSave:
    def __init__(self):
        self.ball_lock = threading.Lock()
        self.ball = [0,0] # X, Y

        self.score_lock = threading.Lock()
        self.score = [0,0] # lScore, rScore

        self.rPaddle_lock = threading.Lock()
        self.rPaddle = [0,0,''] # X, Y, Moving

        self.lPaddle_lock = threading.Lock()
        self.lPaddle = [0,0,''] # X, Y, Moving

        self.sync_lock = threading.Lock()
        self.sync = 0 # The current sync between the two clients

        self.lReady_lock = threading.Lock()
        self.lReady = False # Is the left player ready to start?

        self.rReady_lock = threading.Lock()
        self.rReady = False # is the right player ready to start?


def clientControl(self, shutDown, game, clientSocket, clientNumber):
    
    Connection = sock_wrapper(clientSocket)

    while not shutDown.is_set() and not Connection.closed:
        
        # Receive data from the client
        _ , newMessage = Connection.recv()

        if newMessage is None:
            break
        if newMessage['type'] == 'start':
            
            if clientNumber == 0:
                game.lReady_lock.acquire()
                game.lReady = True
                game.lReady_lock.release()
                newMessage['playerpaddle'] = 'left'
                
            elif clientNumber == 1:
                game.rReady_lock.acquire()
                game.rReady = True
                game.rReady_lock.release()
                newMessage['playerpaddle'] = 'left'

            game.rReady_lock.acquire()
            game.lReady_lock.acquire()    
            if game.lReady and game.rReady:
                newMessage['data'] = 'True'
                Connection.send(newMessage)
                game.rReady_lock.release()
                game.lReady_lock.release() 
                continue

            else:
                newMessage['data'] = 'False'
                Connection.send(newMessage)
                game.rReady_lock.release()
                game.lReady_lock.release()
                continue

        #check if right side is connected
        #check if left side is connected
        #if so, send "yes", else "no"
        if newMessage['type'] == 'gimme':
            if clientNumber == 0: #left side is connected
                    game.sync_lock.acquire()
                    newMessage['data']['seq'] = game.sync
                    game.sync_lock.release()
                    game.ball_lock.aquire()
                    newMessage['data']['ball'] = game.ball
                    game.ball_lock.release()
                    game.score_lock.aquire()
                    newMessage['data']['score'] = game.score # lScore, rScore
                    game.score_lock.release()
                    game.rPaddle_lock.aquire()
                    newMessage['data']['opponentpaddlex'] = game.rPaddle[0]
                    newMessage['data']['opponentpaddley'] = game.rPaddle[1]# X, Y, Moving
                    game.rPaddle_lock.release()

        
            if clientNumber == 1: #left side is connected
                game.sync_lock.acquire()
                if game.sync > newMessage['data']['seq']:
                    newMessage['data']['seq'] = game.sync
                    game.sync_lock.release()
                    game.ball_lock.aquire()
                    newMessage['data']['ball'] = game.ball
                    game.ball_lock.release()
                    game.score_lock.aquire()
                    newMessage['data']['score'] = game.score # lScore, rScore
                    game.score_lock.release()
                    game.lPaddle_lock.aquire()
                    newMessage['data']['opponentpaddlex'] = game.lPaddle[0]
                    newMessage['data']['opponentpaddley'] = game.lPaddle[1]# X, Y, Moving
                    game.lPaddle_lock.release()
            Connection.send(newMessage)
            continue


               
        if newMessage['type'] == 'update':
            if clientNumber == 0: #left side is connected
                game.sync_lock.acquire()
                if game.sync > newMessage['data']['seq']:
                    game.sync_lock.release()
                    game.lPaddle_lock.acquire()
                    game.lPaddle = newMessage['data']['playerpaddlex'], newMessage['data']['playerpaddley'], newMessage['data']['playermov']
                    game.lPaddle_lock.release()
                    continue
                game.sync = newMessage['data']['seq']
                game.sync_lock.release()
                game.lPaddle_lock.acquire()
                game.lPaddle = newMessage['data']['playerpaddlex'], newMessage['data']['playerpaddley'], newMessage['data']['playermov']
                game.lPaddle_lock.release()
                game.ball_lock.aquire()
                game.ball = newMessage['data']['ball']
                game.ball_lock.release()
                game.score_lock.aquire()
                game.score = newMessage['data']['score'] # lScore, rScore
                game.score_lock.release()
                game.rPaddle_lock.aquire()
                game.rPaddle[0] = newMessage['data']['opponentpaddlex']
                game.rPaddle[1] = newMessage['data']['opponentpaddley'] # X, Y, Moving
                game.rPaddle_lock.release()
            if clientNumber == 1: #right side is connected:
                game.sync_lock.acquire()
                if game.sync > newMessage['data']['seq']:
                    game.sync_lock.release()
                    game.rPaddle_lock.acquire()
                    game.rPaddle = newMessage['data']['playerpaddlex'], newMessage['data']['playerpaddley'], newMessage['data']['playermov']
                    game.rPaddle_lock.release()
                    continue
                game.sync = newMessage['data']['seq']
                game.sync_lock.release()
                game.rPaddle_lock.acquire()
                game.rPaddle = newMessage['data']['playerpaddlex'], newMessage['data']['playerpaddley'], newMessage['data']['playermov']
                game.rPaddle_lock.release()
                game.ball_lock.aquire()
                game.ball = newMessage['data']['ball']
                game.ball_lock.release()
                game.score_lock.aquire()
                game.score = newMessage['data']['score'] # lScore, rScore
                game.score_lock.release()
                game.lPaddle_lock.aquire()
                game.lPaddle[0] = newMessage['data']['opponentpaddlex']
                game.lPaddle[1] = newMessage['data']['opponentpaddley'] # X, Y, Moving
                game.lPaddle_lock.release()

            Connection.send(newMessage)
            continue



def main():
    print('Server Online')

    # Create our server type 1 socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server socket to the HOST and PORT
    server.bind((HOST, PORT))

    # List of client threads
    clientThreads = []

    # Event to shutdown the server
    shutDown = threading.Event()

    server.listen()

    game = gameSave()

    clientNumber = 0
    maxClient = 2

    while not shutDown.is_set() and clientNumber < maxClient:
        # Accept a connection from a client
        newClient, _ = server.accept()

        # Create a new thread for each client
        newThread = threading.Thread(target=clientControl, args=(shutDown, game, newClient, clientNumber))
        newThread.start()

        clientNumber += 1

    server.close()

    for client in clientThreads:
        client.join()

    print('Server Closing')

if __name__ == "__main__": 
    main()