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

class NetworkEngine:
    """Any of Networking element should be found in this class. """

    # Default Constructor
    def __init__(self):
        self.port: int
        self.address: str
        self.bufferSize: int
        self.socket: socket
    
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
        # DEBUG Code
        # Create an empty byte buffer
        # writeStream = bytearray(self.bufferSize)
        # Serialize data
        print('Les donnees serializer : {!r}'.format(pickle.dumps(data)))
        #pickle.dump(data, writeStream)

        # Real code here --
        # Put into string, the binary representation of our data
        dataString = pickle.dumps(data)
        
        # Get the size of the message to explain the Receiver how big the message is
        # msgSize = len(dataString)

        # Add the End Marker
        dataString = dataString + "@"

        # Create the final message : format -> [Size Separator Msg]
        #finalDataString = str(msgSize) + "@" + dataString
        print('Voici ce que contient data String : ' + dataString)

        # Send the data to the socket
        totalsent = 0

        # As long as all the message has not been sent
        while totalsent < len(dataString):
            sent = self.socket.send(dataString[totalsent:])

            # If nothing has been sent, it means the connection has broken
            if (sent == 0):
                print("Connection broken ")

            totalsent = totalsent + sent
    
    # De-Serialize data
    def decodeData(self):
        # Read data from the socket
        chunks = []

        # Read until the End Marker is found
        while True:
            chunk = self.socket.recv(self.bufferSize)

            # If chunk is null, then an error has occured
            if len(chunk) == 0:
                print("Connection broken ")
                break

            # The End Marker has been found. The message received is now complete
            if "@" in chunk:
                # Get rid of the Marker
                chunk = chunk[:-1]
                # Add the latest chunk before breaking
                chunks.append(chunk)
                break
            
            # Add the latest chunk of data to the previous received data
            chunks.append(chunk)
        
        # Recreate the original message
        rcvdData = ''.join(chunks)

        # Recreate the original object from the received data
        data = pickle.loads(rcvdData)

        # Return the object received
        return data

        # Create a stream which can be read
        # readStream = io.BytesIO(writeStream.get_value())

        # Get data from the encoded stream
        # data = pickle.load(readStream)

        # Return data
        # return data

class ServerNetworkingThread (threading.Thread):
    """This class is instantiate any time a new connection to the main server socket is accepted."""
    # Voir : https://www.tutorialspoint.com/python/python_multithreading.htm
    
    # Default Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadID: int
        self.clientSocket: socket
        self.clientPort: int
        self.clientIpAddress: int
        self.clientID: int
        self.currentGameState: str
        self.inputCommands: {} # dict of Clients inputs
        self.outputCommands: {} # dict of Client outputs
        self.networkEngine: NetworkEngine
        self.timer: threading.Timer
    
    # Initialize the thread
    def initialization(self):
        # self.GAME_STATUS = "START"

        # Create the network engine and set dependencies
        self.networkEngine = NetworkEngine()
        self.networkEngine.setDependencies(self.clientPort, self.clientIpAddress, self.clientSocket)
        self.networkEngine.initialization()

        # Create the timer: every 16 ms means 60FPS
        self.timer = threading.Timer(0.016, self.threadMain())
    
    # Set the dependencies
    def setDependencies(self, threadID, clientSocket, clientPort, clientIpAddress, clientID, inputCommands, outputCommands):
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.clientPort = clientPort
        self.clientIpAddress = clientIpAddress
        self.clientID = clientID
        self.inputCommands = inputCommands
        self.outputCommands = outputCommands

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
        print("Starting communication with : " + str(self.clientID))
        self.startTimer()

    # Main Thread Function
    def threadMain(self):
        # Decode data from the client
        recvData = self.networkEngine.decodeData()

        # Create a struct/tuple and add it to the input Command dict
        self.inputCommands[self.clientID] = recvData

        # Create local data to send to the client
        sendData = self.outputCommands[self.clientID]

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
        self.serverSocket.connect((self.serverAddress, self.serverPort))

        # Create the network engine and set dependencies
        self.networkEngine = NetworkEngine()
        self.networkEngine.setDependencies(self.serverPort, self.serverAddress, self.serverSocket)
        self.networkEngine.initialization()

        # Create the timer: every 16 ms means 60FPS
        self.timer = threading.Timer(0.016, self.threadMain())

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