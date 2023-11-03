# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

#1.1- loose n rough, modifying nescesary(untested) (you proably shouldnt run this)
import socket
import threading
#used to encode to binary for the sending to and from server
import json

# Use this file to write your server logic
# You will need to support at least two clients
class gameSave:
    # You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
    # for each player and where the ball is, and relay that to each client
    leftlock = threading.Lock()
    rightlock = threading.Lock()
    #bools that show if the left and right servers are on
    lefton = False
    righton = False

    rpadlock = threading.Lock()
    #x and y coordinates of the right paddle
    rpad = [0,0]
    lpadlock = threading.Lock()
    #x and y coordinates of the left paddle
    lpad = [0,0]
    ballock = threading.Lock()
    # x and y coordinates of the ball
    ball = [0,0]
    scorelock = threading.Lock()
    #right and left hand side scores
    score = [0,0]

    namelock = threading.Lock()
    #player name, 1 or 2 (0 is the null)
    name = 0
    # I suggest you use the sync variable in pongClient.py to determine how out of sync your two
    # clients are and take actions to resync the games
    synclock = threading.Lock()
    sync = 0
def client(socket, name):
    if name == 1: #left hand side stuff
        #check rhs sync
        #if rhssync > lhssync
            #wu oh
            #replace lhs stuff with rhs stuff
            #pass back to the lhs client
        #else
            #update score with lhs things
    else:
        #do right hand side stuff: just opposite of above
def main():
    #uhhh idk how most of this works, is mostly the theory
    #before both are in, a loop will ask server if both are online
    #i think that client mayyyy turn the bool to on?


    #check if both servers are in fact online
    if left_on and right_on:
        #then continue
        #starting the server updates
    #while either socket not error:
        socket, address = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading = threading.Thread(target=client, args=(socket, name))
