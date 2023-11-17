# =================================================================================================
# Contributing Authors:	    Alexander Wise, Ruby Harris and Michaela Winfree
# Email Addresses:          Alex.Wise@uky.edu, Ruby.Harris@uky.edu, Michaela.Winfree@uky.edu
# Date:                     11/17/2023
# Purpose:                  Runs the game on each client computer
# =================================================================================================

import pygame
import tkinter as tk
import sys
import socket


from socket_wrapper import sock_wrapper

# Constants

from assets.code.helperCode import *

# This is the main game loop.  For the most part, you will not need to modify this.  The sections
# where you should add to the code are marked.  Feel free to change any part of this project
# to suit your needs.
def playGame(screenWidth:int, screenHeight:int, playerPaddle:str, client:sock_wrapper) -> None:
    
    # Pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    # Constants
    WHITE = (255,255,255)
    clock = pygame.time.Clock()
    scoreFont = pygame.font.Font("./assets/fonts/pong-score.ttf", 32)
    winFont = pygame.font.Font("./assets/fonts/visitor.ttf", 48)
    pointSound = pygame.mixer.Sound("./assets/sounds/point.wav")
    bounceSound = pygame.mixer.Sound("./assets/sounds/bounce.wav")

    # Display objects
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    winMessage = pygame.Rect(0,0,0,0)
    topWall = pygame.Rect(-10,0,screenWidth+20, 10)
    bottomWall = pygame.Rect(-10, screenHeight-10, screenWidth+20, 10)
    centerLine = []
    for i in range(0, screenHeight, 10):
        centerLine.append(pygame.Rect((screenWidth/2)-5,i,5,5))

    # Paddle properties and init
    paddleHeight = 50
    paddleWidth = 10
    paddleStartPosY = (screenHeight/2)-(paddleHeight/2)
    leftPaddle = Paddle(pygame.Rect(10,paddleStartPosY, paddleWidth, paddleHeight))
    rightPaddle = Paddle(pygame.Rect(screenWidth-20, paddleStartPosY, paddleWidth, paddleHeight))

    ball = Ball(pygame.Rect(screenWidth/2, screenHeight/2, 5, 5), -5, 0)

    if playerPaddle == "left":
        opponentPaddleObj = rightPaddle
        playerPaddleObj = leftPaddle
    else:
        opponentPaddleObj = leftPaddle
        playerPaddleObj = rightPaddle

    lScore = 0
    rScore = 0
    sync = 0
    last_update_time = 0
    update_interval = 10 
    last_play_time = 0
    play_interval = 10
    while True:
        # Wiping the screen
        screen.fill((0,0,0))

        # Getting keypress events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    playerPaddleObj.moving = "down"

                elif event.key == pygame.K_UP:
                    playerPaddleObj.moving = "up"

            elif event.type == pygame.KEYUP:
                playerPaddleObj.moving = ""

        # Send the update to the server.
        # =========================================================================================
        # Your code here to send an update to the server on your paddle's information,
        # where the ball is and the current score.
        # Feel free to change when the score is updated to suit your needs/requirements
        # Dictonary to send the client's game data to the server
        dataFrame = {

            # Essentially the seq # for the frame
            'seq': sync,
            'playerpaddlex': playerPaddleObj.rect.x,
            'playerpaddley': playerPaddleObj.rect.y,
            'playermov' : playerPaddleObj.moving,

            # Player Paddle's x and y position
            # these are server use only
            #didnt see the point of making a server df, so...
            # Ball's x and y positions
            'ballx': ball.rect.x,
            'bally': ball.rect.y,

            # Scores
            'score': [lScore,rScore]
        }
        mess = {
            'type': 'update',
            'data': dataFrame
        }


   
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > update_interval:
        # Your code to send updates to the server
        # ...
            client.send(mess)
        last_update_time = current_time
        # Send the update to the server.
        
  
        # WIP: Do we need to grab and set whether opponent paddle is moving according to the for loop below?
        # Send the update to the server.

        # =========================================================================================

        # Update the player paddle and opponent paddle's location on the screen
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            if paddle.moving == "down":
                if paddle.rect.bottomleft[1] < screenHeight-10:
                    paddle.rect.y += paddle.speed
            elif paddle.moving == "up":
                if paddle.rect.topleft[1] > 10:
                    paddle.rect.y -= paddle.speed

        # If the game is over, display the win message
        if lScore > 4 or rScore > 4:
            winText = "Player 1 Wins! " if lScore > 4 else "Player 2 Wins! "
            textSurface = winFont.render(winText, False, WHITE, (0,0,0))
            textRect = textSurface.get_rect()
            textRect.center = ((screenWidth/2), screenHeight/2)
            winMessage = screen.blit(textSurface, textRect)
        else:

            # ==== Ball Logic =====================================================================
            ball.updatePos()

            # If the ball makes it past the edge of the screen, update score, etc.
            if ball.rect.x > screenWidth:
                lScore += 1
                pointSound.play()
                ball.reset(nowGoing="left")
            elif ball.rect.x < 0:
                rScore += 1
                pointSound.play()
                ball.reset(nowGoing="right")
                
            # If the ball hits a paddle
            if ball.rect.colliderect(playerPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(playerPaddleObj.rect.center[1])
            elif ball.rect.colliderect(opponentPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(opponentPaddleObj.rect.center[1])
                
            # If the ball hits a wall
            if ball.rect.colliderect(topWall) or ball.rect.colliderect(bottomWall):
                bounceSound.play()
                ball.hitWall()
            
            pygame.draw.rect(screen, WHITE, ball)
            # ==== End Ball Logic =================================================================

        # Drawing the dotted line in the center
        for i in centerLine:
            pygame.draw.rect(screen, WHITE, i)
        
        # Drawing the player's new location
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            pygame.draw.rect(screen, WHITE, paddle)

        pygame.draw.rect(screen, WHITE, topWall)
        pygame.draw.rect(screen, WHITE, bottomWall)
        scoreRect = updateScore(lScore, rScore, screen, WHITE, scoreFont)
        pygame.display.update()
        clock.tick(60)
        
        # This number should be synchronized between you and your opponent.  If your number is larger
        # then you are ahead of them in time, if theirs is larger, they are ahead of you, and you need to
        # catch up (use their info)
        sync += 1

        # =========================================================================================
        # Send your server update here at the end of the game loop to sync your game with your
        # opponent's game
        mess = {
            'type': 'gimme',
            'seq': sync
        }

        # Send a request for client update.
        latestGame = handshake(client, mess)
        # Receive the latest copy of game data from the server
        # WIP: Make sure what's received is a game data frame....
        if latestGame != None:
            # Update game params based on the latestGame data
            #this should either get the highest sync or just grab the opponent's data
            if (sync < latestGame['seq']):
                lScore = latestGame['score'][0]
                rScore = latestGame['score'][1]
                ball.rect.x = latestGame['ballx']
                ball.rect.y = latestGame['bally']
                ball.updatePos()
                if playerPaddle == 'left':
                    playerPaddleObj.rect.x = latestGame['lPaddlex']
                    playerPaddleObj.rect.y = latestGame['lPaddley']
                    playerPaddleObj.moving = latestGame['lPaddlemov']
                elif playerPaddle == 'right':
                    playerPaddleObj.rect.x = latestGame['rPaddlex']
                    playerPaddleObj.rect.y = latestGame['rPaddley']
                    playerPaddleObj.moving = latestGame['rPaddlemov']
            if playerPaddle == 'left':
                opponentPaddleObj.rect.x = latestGame['rPaddlex']
                opponentPaddleObj.rect.y = latestGame['rPaddley']
                opponentPaddleObj.moving = latestGame['rPaddlemov']
            elif playerPaddle == 'right':
                opponentPaddleObj.rect.x = latestGame['lPaddlex']
                opponentPaddleObj.rect.y = latestGame['lPaddley']
                opponentPaddleObj.moving = latestGame['lPaddlemov']

            
        # =========================================================================================




# This is where you will connect to the server to get the info required to call the game loop.  Mainly
# the screen width, height and player paddle (either "left" or "right")
# If you want to hard code the screen's dimensions into the code, that's fine, but you will need to know
# which client is which
def joinServer(ip:str, port:str, errorLabel:tk.Label, app:tk.Tk) -> None:
    # Purpose:      This method is fired when the join button is clicked
    # Arguments:
    # ip            A string holding the IP address of the server
    # port          A string holding the port the server is using
    # errorLabel    A tk label widget, modify it's text to display messages to the user (example below)
    # app           The tk window object, needed to kill the window
    # Create a socket and connect to the server
    # You don't have to use SOCK_STREAM, use what you think is best
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #Connect to server with specified host ip
        client.connect(('localhost', 6000))
    except (ConnectionRefusedError, socket.error) as e:
        print(f"Connection error: {e}")
        errorLabel.config(text="Connection error. Please check the server.")
        errorLabel.update()
        return

    

    # Wrap the client for send/receive handling
    wClient = sock_wrapper(client)
    initRequest = {
        'type': 'start',
        'data': False,
        'playerpaddle': ''
    }
    while initRequest['data'] != True: 
        initRequest = handshake(wClient, initRequest)


    # If you have messages you'd like to show the user use the errorLabel widget like so
    errorLabel.config(text=f"Some update text. You input: IP: {ip}, Port: {port}")
    errorLabel.update()     

    # Close this window and start the game with the info passed to you from the server
    app.withdraw()     # Hides the window (we'll kill it later)
    playGame(480, 640, initRequest['playerpaddle'], wClient)  # User will be either left or right paddle
    app.quit()         # Kills the window


# This displays the opening screen, you don't need to edit this (but may if you like)
def startScreen():
    app = tk.Tk()
    app.title("Server Info")

    image = tk.PhotoImage(file="./assets/images/logo.png")

    titleLabel = tk.Label(image=image)
    titleLabel.grid(column=0, row=0, columnspan=2)

    ipLabel = tk.Label(text="Server IP:")
    ipLabel.grid(column=0, row=1, sticky="W", padx=8)

    ipEntry = tk.Entry(app)
    ipEntry.grid(column=1, row=1)

    portLabel = tk.Label(text="Server Port:")
    portLabel.grid(column=0, row=2, sticky="W", padx=8)

    portEntry = tk.Entry(app)
    portEntry.grid(column=1, row=2)

    errorLabel = tk.Label(text="")
    errorLabel.grid(column=0, row=4, columnspan=2)

    joinButton = tk.Button(text="Join", command=lambda: joinServer(ipEntry.get(), portEntry.get(), errorLabel, app))
    joinButton.grid(column=0, row=3, columnspan=2)

    app.mainloop()


# Author:        Alexander Wise
# Purpose:       Handles the receiving of tuples of encoded json dictionaries from the server.
# Pre:           This method expects a wrapped client socket to be connected to a server that is sending/receiving data.
# Post:          The method sends a request in the form of a dictionary, and waits for a valid dictionary tuple to return.
def handshake(wSock:sock_wrapper, request:dict) -> dict:
    wSock.send(request)
    received , data = wSock.recv()
    while not received or data == None:
        wSock.send(request)
        received , data = wSock.recv()
    return data

if __name__ == "__main__":
    startScreen()
    
    # Uncomment the line below if you want to play the game without a server to see how it should work
    # the startScreen() function should call playGame with the arguments given to it by the server this is
    # here for demo purposes only
    #playGame(640, 480,"left",socket.socket(socket.AF_INET, socket.SOCK_STREAM))