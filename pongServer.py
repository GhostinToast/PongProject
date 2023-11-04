# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================



#1.0.1- loose n rough, modifying nescesary(untested) (you proably shouldnt run this)
import socket
import threading
# used to encode to strings for the sending to and from server
import json


# MFW's notes 
#   gameSave is a universal dictionary. It will be updated a bunch
#   each client gets a copy of gamesave, with the playerpaddle changed
#   to reflect the player. the sync number will be updated on each, and
#   each cycle we replace the outdated version (whether it be on a client
#   or in the )

# Use this file to write your server logic
# You will need to support at least two clients

gameSave = {
    # You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
    # for each player and where the ball is, and relay that to each client

    #bools that show if the left and right servers are on
    'lefton' : False,
    'righton' : False,


    #x and y coordinates of the right paddle
    'rpad': [0,0],
    #x and y coordinates of the left paddle
    'lpad' : [0,0],

    # x and y coordinates of the ball
    'ball': [0,0],

    #right and left hand side scores
    'score': [0,0],

    #player side, left or right
    'playerpaddle' : 'null',

    # I suggest you use the sync variable in pongClient.py to determine how out of sync your two
    # clients are and take actions to resync the games
    'sync' : 0
}

def clientupdate(socket, playerpaddle):
    
    if playerpaddle == 'left': #left hand side stuff
        #check rhs sync
        #if rhssync > lhssync
            #wu oh
            #replace lhs stuff with rhs stuff
            #pass back to the lhs client
        #else
            #update score with lhs things
    if playerpaddle == 'right':
        #do right hand side stuff: just opposite of above


def main():
    #uhhh idk how most of this works, is mostly the theory
    #before both are in, a loop will ask server if both are online
    #i think that client mayyyy turn the bool to on?
   

    # create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set up the IP port we're listening to
    # we're probably going to change this from localhost
    server.bind(("localhost", 5000))
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
        clientSocket.send(jsonConn.encode())
        # perhaps have the clients respond with confirmations?
    # current issues (FIXED): the first client won't think client 2 is connected 


    # while either socket not error:
        socket, address = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading = threading.Thread(target=clientupdate, args=(socket, playerpaddle))
