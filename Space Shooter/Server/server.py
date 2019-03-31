# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 24 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains the Server Logic for the game. 																									#
#########################################################################################################################################################################
import NetworkEngine
import threading
import socket
import time
import os, sys
#import pygame
sys.path.insert(0, os.path.abspath(".."))
from Player import *
from Ennemies import *
from PhysicEngine import *
from InputEngine import *
from commonclasses import *
#from pygame.locals import *
##########################################################FUNCTIONS##############################################################################################
# Do Physics stuff here ...
# No Rendering plz !
def mainServerFunction():
    # 0 - Get data from clients
    # Already there in the clients Threads !

    # 1 - Process players inputs
    for index in range(0, len(clientsThreads)):
        inputEngines[index].processPlayerInput(clientsThreads[index].inputCommands)

    # 2 - Do the Physics Processing
    physicEngine.simulateGameState()
    physicEngine.simulateAllCollisions()
    physicEngine.updateCurrentGameState()

    # 3 - Send to the clients the current Game State
    for index in range(0, len(clientsThreads)):
        sendData = NetworkEngine.ServerNetworkingOutput()
        sendData.ennemies = ennemies
        sendData.player = players[index]
        sendData.otherPlayers = [p for p in players if p != players[index]]

        clientsThreads[index].outputCommands = sendData


##############################################GLOBAL VARIABLES#######################################################################################
TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Port = 5890
clientsThreads = []
players = []
inputEngines = []
threadID = 0
NB_MIN_PLAYER = 1

# TODO : C'est de la merde, parce que 0.016 signifie executer la fonction juste apres l'appel Threading.Timer
# TODO : Ne veut pas dire "repeter" tous les 0.016 secondes
#timer = threading.Timer(0.016, mainServerFunction)

# Ok, This is not the good way of doing it but whatever ...
# So I'm not really using pygame here. It is just used to load the sprites into the SpriteManager which is not even used !
#pygame.init()
#pygame.display.set_mode((512, 512))

# This is just done to have the server not pissing me off !
#spriteManager = SpriteManager()
#spriteManager.isServer = True

#musicAndSoundManager = MusicAndSoundManager()
#musicAndSoundManager.isServer = True

# Main Server Function
print ("Launching  Game Server ...")

# Bind socket and listen to port
print ("hostname : " + socket.gethostname())
TCPSocket.bind(("localhost", Port))

# Max 4 players at the same time
TCPSocket.listen(4)

# Main Accept loop
while True:
    # Receiving connection
    (clientSocket, clientInfo) = TCPSocket.accept()

    # Create a thread to interact with the client
    clientThread = NetworkEngine.ServerNetworkingThread()
    print("New Connected Client. The client infos are : ")
    print(clientInfo)
    # TEST:
    clientThread.setDependencies(threadID, 
                                 clientSocket, 
                                 clientInfo[1], 
                                 clientInfo[0], 
                                 None)

    # Initialize thread
    clientThread.initialization()

    # Add the client to the list of clients
    clientsThreads.append(clientThread)

    # Increment thread count
    threadID += 1

    # If the number of players have reached the desired number, then the multiplayer game starts
    if (len(clientsThreads) >= NB_MIN_PLAYER):
        print("Game Starting ...")
        
        # Stop receiving connection
        break

# Here, create server objects
initialPos = 50
index = 0

# For each client thread create a corresponding Player and Input Engine
for cT in clientsThreads:
    # Create one Player object for each player
    player = Player(initialPos + index*80, 452)
    player.initialization() # Does nothing ...
    players.append(player)

    # Create one Input Engine for each player and set dependencies
    inputEngine = InputEngine()
    inputEngine.playerID = index
    inputEngine.setDependencies(player)
    inputEngines.append(inputEngine)

    index += 1

# Set Dependencies to the Ennemies
ennemies = Ennemies()
ennemies.PlayerObject = players[0]
#ennemies.SpriteManager = spriteManager
#ennemies.MusicAndSoundManager = musicAndSoundManager
#spriteManager.initialization()
#musicAndSoundManager.initialization()
ennemies.initialization()

# Set Dependencies to the Physic Engine
physicEngine = PhysicEngine.PhysicEngine()
physicEngine.setDependencies(ennemies, players)

# Initialization of all the outputCommands for each client thread
for index in range(0, len(players)):
    # Give dependencies to the list of clients Thread outputs commands
    clientsThreads[index].outputCommands.ennemies = ennemies
    clientsThreads[index].outputCommands.listOfExplosions = physicEngine.listofExplosions
    clientsThreads[index].outputCommands.player = players[index]
    clientsThreads[index].outputCommands.otherPlayers = [p for p in players if p != players[index]]

# Starts all the clients Threads
for cT in clientsThreads:
    cT.currentGameState = "RUNNING"
    cT.start()
    cT.join()

# Main Game loop
#timer.start()
physicEngine.currentGameState = "RUNNING"
while True:
    if physicEngine.currentGameState == "STOP":
        for cT in clientsThreads:
            cT.threadStop = True
        break
    time.sleep(0.016)
    mainServerFunction()
print ("That was nice Server, deh ? o_O")