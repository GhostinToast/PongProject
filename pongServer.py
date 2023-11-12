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

class ServerControl:
    def __init__(self):
        print('Server Online')

        # Create our server type 1 socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the server socket to the HOST and PORT
        self.server.bind((HOST, PORT))

        # List of client threads
        self.clientThreads = []

        # Event to shutdown the server
        self.shutDown = threading.Event()

        self.server.listen()

        self.game = gameSave()

        self.clientNumber = 0
        self.maxClient = 2

        while not self.shutDown.is_set() and self.clientNumber < self.maxClient:
            # Accept a connection from a client
            newClient, _ = self.server.accept()

            # Create a new thread for each client
            newThread = threading.Thread(target=self.clientControl, args=(newClient, self.clientNumber))
            newThread.start()

            self.clientNumber += 1


        self.server.close()

        for client in self.clientThreads:
            client.join()

        print('Server Closing')

    def clientControl(self, clientSocket, clientNumber):
        
        Connection = ClientWrapper(clientSocket)

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

def clientupdate(socket, playerPaddle):
    # WIP: Any reading/writing of gameSave probably needs some mutexes/semaphores, but that's for another day
    while (True):
        # Retrieve the (hopefully) latest game frame as encoded data from the client
        byteStream = socket.recv(1024)
        # Decode bytestream into json data and convert it to dictionary
        frameData = json.loads(byteStream.decode)
        # Check against sync
        if frameData['seq'] < gameSave['sync']:
            # Client needs the latest game data
            # Encode the game data as a json string
            jsonGame = json.dumps(gameSave)
            # Encode the string and finally send it to client
            socket.sendall(jsonGame.encode)
        else:
            # Edit server data instead
            if playerPaddle == 'left': 
                gameSave['lpad'][0] = frameData['playerpaddlex']
                gameSave['lpad'][1] = frameData['playerpaddley']
                gameSave['score'][0] = frameData['playerScore']
                gameSave['score'][1] = frameData['opponentScore']
            else:
                gameSave['rpad'][0] = frameData['playerpaddlex']
                gameSave['rpad'][1] = frameData['playerpaddley']
                gameSave['score'][1] = frameData['playerScore']
                gameSave['score'][0] = frameData['opponentScore']
            gameSave['sync'] = frameData['seq']



def main():
    #uhhh idk how most of this works, is mostly the theory
    #before both are in, a loop will ask server if both are online
    #i think that client mayyyy turn the bool to on?
   

    # create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set up the IP port we're listening to
    # we're probably going to change this from localhost
    server.bind((HOST, PORT))
    # this loop connects the clients (2 clients) and
    # sends them copies of gamesave with appropriate
    # paddles and boolean connection values
    server.listen(5)
    for i in range(1):
        # clientSocket, a is the address
        clientSocket, a = server.accept()
        # then once we got the connection,
        rawConn = gameSave
        # make a new dict and cnange its 'playerpaddle'
        # left is 1, right is 2.
        rawConn['name'] = i+1
        # then update the connection boolean values
        if i+1 == 1:
            # ^^ left side
            rawConn['lefton'] = True
            rawConn['playerpaddle'] = 'left'
        if i+1 == 2:
            # ^^ right side
            rawConn['righton'] = True
            rawConn['lefton'] = True
            rawConn['playerpaddle'] = 'right'

        # json encode the rawConn
        jsonConn = json.dumps(rawConn)
        # send the encoded newConn to the client:
        clientSocket.sendall(jsonConn.encode())
        # perhaps have the clients respond with confirmations?
        
    # current issues (FIXED): the first client won't think client 2 is connected 


    # while either socket not error:
        clientSocket, clientAddress = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading = threading.Thread(target=clientupdate, args=(clientSocket, playerpaddle))
