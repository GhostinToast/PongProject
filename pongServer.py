# =================================================================================================
# Contributing Authors:	    Alexander Wise,
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


# MFW's notes 
#   gameSave is a universal dictionary. It will be updated a bunch
#   each client gets a copy of gamesave, with the playerpaddle changed
#   to reflect the player. the sync number will be updated on each, and
#   each cycle we replace the outdated version (whether it be on a client
#   or in the )

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


def clientControl(self, clientSocket, clientNumber):
    
    Connection = sock_wrapper(clientSocket)

    while not self.shutDown.is_set() and not Connection.closed:
        
        # Receive data from the client
        _ , newMessage = Connection.recv()
        if newMessage is None:
            break
        if newMessage['type'] == 'start':
        #check if right side is connected
        #check if left side is connected
        #if so, send "yes", else "no"
            continue
        if newMessage['type'] == 'gimme':
        #send it the data from other client using the game save
        #send type:gimme return:dictionary
        #send type:update return:dictionary
            continue
        if newMessage['type'] == 'update':
        #using dict passed in,
        #check the sync number
        #if its a lil fucky wucky, 
        #use game save to update client dict.
        #else
        #update game save using dict passed in


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

    while not self.shutDown.is_set() and self.clientNumber < self.maxClient:
        # Accept a connection from a client
        newClient, _ = server.accept()

        # Create a new thread for each client
        newThread = threading.Thread(target=self.clientControl, args=(newClient, self.clientNumber))
        newThread.start()

        clientNumber += 1

    server.close()

    for client in clientThreads:
        client.join()

    print('Server Closing')

if __name__ == "__main__":
    main()