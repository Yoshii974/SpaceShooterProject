# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 24 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains the Network Logic for the game. 																									#
#########################################################################################################################################################################
import threading
import pickle
import socket
import os, sys
sys.path.insert(0, os.path.abspath(".."))
from Player import *
from Ennemies import *
from commonclasses import *
# import io

# Since a packet is usually 1518 bytes and since we're using TCP, we'd rather make sure our buffer will fullfill the payload of each frame/packet to its maximum size
BUFFER_SIZE = 2048

# Macro which defines the repeat time (every 16 ms means 60FPS)
THREADING_REPEAT_TIME = 0.016

class NetworkEngine:
    """Any of Networking element should be found in this class. """

    # Default Constructor
    def __init__(self):
        self.port: int
        self.address: str
        self.bufferSize: int
        self.socket: socket.socket
    
    # The Server is gonna talk to each Client via TCP Protocol
    def initialization(self):
        #self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bufferSize = BUFFER_SIZE

    # Set the dependencies
    def setDependencies(self,port, address, socket):
        self.port = port
        self.address = address
        self.socket = socket

    # Serialize data
    def encodeData(self, data):
        # print('Les donnees serializer : {!r}'.format(pickle.dumps(data)))
        # Put into a Stream, the binary representation of our data
        dataStream = pickle.dumps(data)

        # Send the data to the socket
        totalsent = 0

        # While the whole message has not been sent
        while totalsent < len(dataStream):
            sent = self.socket.send(dataStream[totalsent:])
            # If nothing has been sent, it means that the connection has broken
            if (sent == 0):
                print("Error : NetworkEngine --> Impossible to send data into self.socket. Connection broken ")
                break
            # Else, it means that we still need to send the data
            else:
                totalsent = totalsent + sent
    
    # De-Serialize data
    def decodeData(self):
        # The data Stream container to received the chunks of data
        dataStream = b""

        # Read until the last chunk is of size lower than self.bufferSize
        while True:
            receivedData = self.socket.recv(self.bufferSize)

            # If receivedData is null, then an error has occurred
            if len(receivedData) == 0:
                print("Error : NetworkEngine --> Impossible to receive data from self.socket. Connection broken ")
                break
            # If the "" null string has been returned, then it has finished to receive
            elif receivedData == b"":
                break
            # The last receivedData has been found
            elif len(receivedData) < self.bufferSize:
                dataStream += bytes(receivedData)
                break
            # Otherwise, keep receiving data (here, receivedData should always be as big as self.bufferSize)
            else:
                dataStream += bytes(receivedData)

        # Recreate the original object from the received data
        data = pickle.loads(dataStream)

        # Return the object received
        return data

class ServerNetworkingThread (threading.Thread):
    """This class is instantiate any time a new connection to the main server socket is accepted."""
    # Voir : https://www.tutorialspoint.com/python/python_multithreading.htm
    
    # Default Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadID: int
        self.clientSocket: socket
        self.clientPort: int
        self.clientIpAddress: str
        self.clientID: int
        self.currentGameState: str
        self.inputCommands = ServerNetworkingInput()
        self.outputCommands = ServerNetworkingOutput()
        self.networkEngine: NetworkEngine
        #self.timer: threading.Timer
        self.threadingRepeatTime: float
    
    # Initialize the thread
    def initialization(self):
        # self.GAME_STATUS = "START"

        # Create the network engine and set dependencies
        self.networkEngine = NetworkEngine()
        self.networkEngine.setDependencies(self.clientPort, self.clientIpAddress, self.clientSocket)
        self.networkEngine.initialization()

        # Create the timer: every 16 ms means 60FPS
        # self.timer = threading.Timer(0.016, self.threadMain())
        self.threadingRepeatTime = THREADING_REPEAT_TIME
    
    # Set the dependencies
    def setDependencies(self, threadID, clientSocket, clientPort, clientIpAddress, clientID):
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.clientPort = clientPort
        self.clientIpAddress = clientIpAddress
        self.clientID = clientID
        #self.inputCommands = inputCommands
        #self.outputCommands = outputCommands

    # Get the timer
    #def getTimer(self):
    #    return self.timer

    # Start timer
    #def startTimer(self):
    #    self.timer.start()

    # Stop timer
    #def stopTimer(self):
    #    self.timer.cancel()

    # Override the "run" function (due to Interface)
    def run(self):
        print("Starting communication with : " + str(self.clientID))
        # self.startTimer()
        self.threadMain()

    # Main Thread Function
    def threadMain(self):
        # Allows to repeat n times this thread main function
        threading.Timer(self.threadingRepeatTime, self.threadMain).start()

        # Decode data from the client
        recvData = self.networkEngine.decodeData()

        # Create a struct/tuple and add it to the input Command dict
        self.inputCommands = recvData

        # Create local data to send to the client
        sendData = self.outputCommands

        # Send data to the client
        self.networkEngine.encodeData(sendData)

class ClientNetworkingThread(threading.Thread):
    """This class is instantiate once per client. It allows the client to receive and send data from/to a remote server asynchronously"""

    # Default Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.serverAddress: str
        self.serverPort: str
        self.serverSocket: socket
        self.networkEngine: NetworkEngine
        self.inputCommands: ServerNetworkingOutput
        self.outputCommands: ServerNetworkingInput
        self.timer: threading.Timer
    
    # Initialize the thread
    def initialization(self):
        #Create the local socket to connect to the server
        self.serverSocket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)

        #Connect to remote server
        self.serverSocket.connect((self.serverAddress, int(self.serverPort)))

        # Create the network engine and set dependencies
        self.networkEngine = NetworkEngine()
        self.networkEngine.setDependencies(self.serverPort, self.serverAddress, self.serverSocket)
        self.networkEngine.initialization()

        # Create the timer: every 16 ms means 60FPS
        # self.timer = threading.Timer(0.016, self.threadMain())

    # Set the dependencies
    def setDependencies(self, ServerPort, ServerAddress):
        self.serverPort = ServerPort
        self.serverAddress = ServerAddress
    
    # Get the timer
    def getTimer(self):
        return self.timer

    # Start timer
    def startTimer(self):
        self.timer.start()

    # Stop timer
    def stopTimer(self):
        self.timer.cancel()

    # Override the "run" function (due to Interface)
    def run(self):
        print("Starting communication with server at : " + str(self.serverAddress))
        self.startTimer()
    
    # Main Thread Function
    def threadMain(self):
        # Decode data from the server
        recvData = self.networkEngine.decodeData()

        # Create a struct/tuple and add it to the input Command dict
        self.inputCommands = recvData

        # Create local data to send to the server
        sendData = self.outputCommands

        # Send data to the server
        self.networkEngine.encodeData(sendData)

class ServerNetworkingInput:
    """This class represent every input received from a remote client"""

    # Default Constructor
    def __init__(self):
        self.clientInput: [] # list of Client string commands

class ServerNetworkingOutput:
    """This class represent every output processed by the server to be sent to a remote client"""

    # Default Constructor
    def __init__(self):
        self.ennemies: Ennemies
        self.player: Player
        self.otherPlayers: [] # list of Player object
        self.listOfExplosions: [] # list of Explosions to be drawn by the clients
        #self.ennemies: [] # list of Ennemy_group object
    
    # Set Dependencies
    def setDependencies(self, Ennemies, Player, OtherPlayers, ListOfExplosions):
        self.ennemies = Ennemies
        self.player = Player
        self.otherPlayers = OtherPlayers
        self.listOfExplosions = ListOfExplosions