# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 24 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains the Server Logic for the game. 																									#
#########################################################################################################################################################################
import threading
import socket
from NetworkEngine import *

##############################################GLOBAL VARIABLES#######################################################################################
TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Port = 5890
inputCommands = []
outputCommands = []
clientsThreads = []
threadID = 0
NB_MIN_PLAYER = 2

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
    clientThread = NetworkingThread()
    clientThread.setDependencies(threadID, 
                                 clientSocket, 
                                 clientInfo.clientPort, 
                                 clientInfo.clientIpAddress, 
                                 clientInfo.clientID, 
                                 inputCommands, 
                                 outputCommands)

    # Initialize thread
    clientThread.initialization()

    # Add the client to the list of clients
    clientsThreads.append(clientThread)

    # Increment thread count
    threadID += 1

    # If the number of players have reached the desired number, then the multiplayer game starts
    if (len(clientsThreads) >= NB_MIN_PLAYER):
        print("Game Starting ...")

        for clientThread in clientsThreads:
            clientThread.GAME_STATUS = "RUNNING"
            clientThread.starts()
        
        # Stop receiving connection
        break
    
# Main Game loop
print ("Thats was nice Server, deh ? o_O")
# Do Physics stuff here ...
# No Rendering plz !
