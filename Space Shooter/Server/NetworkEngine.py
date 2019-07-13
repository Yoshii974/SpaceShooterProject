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
import time
import os, sys
sys.path.insert(0, os.path.abspath(".."))
from Player import *
from Ennemies import *
from commonclasses import *
# import io

# Since a packet is usually 1518 bytes and since we're using TCP, we'd rather make sure our buffer will fullfill the payload of each frame/packet to its maximum size
BUFFER_SIZE = 1024

# Macro which defines the header length. In this application protocol, it has been decided to use a 4-bytes header which explains
# how long the payload is.
HEADER_LENGTH = 10

# Macro which defines the repeat time (every 32 ms means about 30 Hz)
THREADING_REPEAT_TIME = 0.032

class NetworkEngine:
    """Any of Networking element should be found in this class. """

    # Default Constructor
    def __init__(self):
        self.port: int
        self.address: str
        self.bufferSize: int
        self.headerLength: int
        self.socket: socket.socket
        self.lastDataReceived: object
        self.LOSCounter: int
        self.messageID: int
        self.listOfReceivedFragments: []
    
    # The Server is gonna talk to each Client via TCP Protocol
    def initialization(self):
        #self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bufferSize = BUFFER_SIZE
        self.headerLength = HEADER_LENGTH
        self.lastDataReceived = None
        self.LOSCounter = 0
        self.messageID = 0
        self.listOfReceivedFragments = []

    # Set the dependencies
    def setDependencies(self, port, address, socket):
        self.port = port
        self.address = address
        self.socket = socket

    # Create fragments for the data
    def createFragments(self, data):
        listOfFragments = []

        # Insert header which contains the length of the payload

        # Converts the size of the data stream onto 4 bytes (with default reading is "big endian")

        # The final message is as follow : MSG = [ [Message_ID (4 bytes)] [Current_Fragment_Index (CFI, 2 bytes)] [Maximum_Fragment_Index (MFI, 2 bytes)] [Fragment_Payload_Length (2 bytes)] [Fragment_Payload (variables length)] ]

        # print('Les donnees serializer : {!r}'.format(pickle.dumps(data)))
        # Put into a Stream, the binary representation of our data
        dataStream = pickle.dumps(data)
        dataStreamLength = len(dataStream)
        
        numberOfBytesToReadFromDataStream = self.bufferSize - self.headerLength
        maximumFragmentIndex = dataStreamLength / numberOfBytesToReadFromDataStream
        currentFragmentIndex = 0
        offset = 0
        fragment = b""

        if maximumFragmentIndex == 0:
            fragmentPayload = dataStream[:numberOfBytesToReadFromDataStream]

            msgID = self.messageID.to_bytes(4, 'big')
            fragment += msgID

            fragment += int(0).to_bytes(2, 'big')
            fragment += int(0).to_bytes(2, 'big')

            fragmentPayloadLength = len(fragmentPayload)
            fragment += fragmentPayloadLength.to_bytes(2, 'big')

            fragment += fragmentPayload

            # Add the fragment to the list of fragments
            listOfFragments.append(fragment)
        else:
            for i in range(0, maximumFragmentIndex):
                fragmentPayload = dataStream[offset:offset + numberOfBytesToReadFromDataStream]

                msgID = self.messageID.to_bytes(4, 'big')
                fragment += msgID
                
                fragment += currentFragmentIndex.to_bytes(2, 'big')
                fragment += maximumFragmentIndex.to_bytes(2, 'big')

                fragmentPayloadLength = len(fragmentPayload)
                fragment += fragmentPayloadLength.to_bytes(2, 'big')

                fragment += fragmentPayload

                # Add the fragment to the list of fragments
                listOfFragments.append(fragment)

                # Do all increments
                currentFragmentIndex += 1
                offset += numberOfBytesToReadFromDataStream

        # Increment the message ID counter
        self.messageID += 1

        return listOfFragments

    # Serialize data
    def encodeData(self, data):
        listOfFragments = self.createFragments(data)

        for fragment in listOfFragments:
            # Send the data to the socket
            totalsent = 0

            # While the whole message has not been sent
            while totalsent < len(fragment):
                try:
                    sent = self.socket.sendto(fragment[totalsent:], (self.address, self.port))
                except socket.timeout:
                #print ("Quantite information sent : " + str(sent))
                # If nothing has been sent, it means that the connection has broken
                #if sent == 0:
                    print("Error : NetworkEngine --> encodeData(), First While, Sending Data. The socket was not ready to send any data. ")
                    return False
                except socket.error:
                    return False
                # Else, it means that we still need to send the data
                else:
                    totalsent = totalsent + sent
        
        # Everything went well
        return True
    
    # Retrieve the original message from all the fragments 
    def retrieveMessage(self):
        message = b""
        listOfFragmentInfo = []

        currentMessageID = -1
        currentFragmentIndex = 0
        maximumFragmentIndex = 0

        msgIdLength = 4
        currentFragmentIndexLength = 2
        maximumFragmentIndexLength = 2
        fragmentPayloadLengthSize = 2

        # Step 1 : Process all Fragments received
        for fragment in self.listOfReceivedFragments:
            offset = 0

            messageID = int.from_bytes(fragment[offset:offset + msgIdLength], 'big')
            offset += msgIdLength

            if currentMessageID == -1:
                currentMessageID = messageID

            currentFragmentIndex = int.from_bytes(fragment[offset:offset + currentFragmentIndexLength], 'big')
            offset += currentFragmentIndexLength

            maximumFragmentIndex = int.from_bytes(fragment[offset:offset + maximumFragmentIndexLength], 'big')
            offset += maximumFragmentIndexLength

            fragmentPayloadLength = int.from_bytes(fragment[offset:offset + fragmentPayloadLengthSize], 'big')
            offset += fragmentPayloadLengthSize

            fragmentPayload = int.from_bytes(fragment[offset:offset + fragmentPayloadLength], 'big')

            fragmentInfo = (messageID, currentFragmentIndex, maximumFragmentIndex, fragmentPayload)
            listOfFragmentInfo.append(fragmentInfo)

        # Step 2 : re-ordering the fragments and make sure none of them is missing
        listOfFragmentInfo.sort(key = lambda fragmentInfo : fragmentInfo[1])
        
        currentFragmentIndex = 0

        for fragmentInfo in listOfFragmentInfo:
            if fragmentInfo[0] != currentMessageID:
                return []
            
            if fragmentInfo[1] != currentFragmentIndex:
                return []
            
            #if fragmentInfo[2] == maximumFragmentIndex and currentFragmentIndex != maximumFragmentIndex:
            #    return False

            currentFragmentIndex += 1
            message += fragmentInfo[3]

        return message

    # De-Serialize data
    def decodeData(self):
        # First, we need to receive the header of the message (which is always a 4-bytes size header),
        # Then, we receive the payload
        header = b""

        while len(header) < self.headerLength:
            try:
                receivedHeader = self.socket.recvfrom(self.headerLength)
            #print("Le header recu : " + str(receivedHeader))
            except socket.timeout:

            # If receivedHeader is null, then an error has occurred
            #if len(receivedHeader) == 0:
                #print("Error : NetworkEngine --> Impossible to receive data from self.socket. Connection broken ")
                # If no Header has been retrieved, then it is useless to keep checking for any other incoming bytes
                # And, we increment the LOS counter
                self.LOSCounter += 1
                return False
            except socket.error:
                return False
            else:
                self.LOSCounter = 0
                header += receivedHeader
        
        # Once the header has been retrieved, we now therefor know how long the payload is
        dataStreamLength = int.from_bytes(header, 'big')
        #print('Taille du data Stream (base sur linterpretation du header) : ' + str(dataStreamLength))

        # The data Stream container to received the chunks of data
        dataStream = b""

        while len(dataStream) < dataStreamLength:
            try:
                receivedData = self.socket.recvfrom(dataStreamLength)
            #print ("Information dataStream recv : " + str(receivedData))

            # If receivedData is null, then an error has occurred
            #if len(receivedData) == 0:
            except socket.timeout:
                print("Error : NetworkEngine --> decodeData(), Second While(). receivedData = 0 after having received a header ")
                return False
            except socket.error:
                return False
            else:
                dataStream += bytes(receivedData)

        # Recreate the original object from the received data
        data = pickle.loads(dataStream)

        # Store the received data
        self.lastDataReceived = data

        # Everything went well
        return True

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
        self.inputCommands: ServerNetworkingInput
        self.outputCommands: ServerNetworkingOutput
        self.networkEngine: NetworkEngine
        #self.timer: threading.Timer
        self.threadingRepeatTime: float
        self.threadStop = False
    
    # Initialize the thread
    def initialization(self):
        # Set socket to non-blocking mode
        self.clientSocket.setblocking(0)

        # self.GAME_STATUS = "START"
        self.inputCommands = ServerNetworkingInput()
        self.outputCommands = ServerNetworkingOutput()

        self.inputCommands.reset()
        self.outputCommands.reset()

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
        print("Starting communication with client : " + str(self.clientID))
        # self.startTimer()
        self.threadMain()

    # Main Thread Function
    def threadMain(self):
        # Allows to repeat n times this thread main function
        # t = threading.Timer(self.threadingRepeatTime, self.threadMain).start()
        while self.threadStop == False:
            # Wait for 0.016s = 16ms = 60 FPS
            time.sleep(self.threadingRepeatTime)

            # Decode data from the client
            if self.networkEngine.decodeData() == False:
                # print ("Probleme lors de la reception de donnee en provenance du client : " + str(self.clientID) + " dans le thread no : " + str(self.threadID))
                pass
            else:
                # TODO: Verifier que dans le message recu, il n'y ait pas une demande fermeture de la connection.
                self.inputCommands = self.networkEngine.lastDataReceived
            # No particular data has been retrieved. The server will just process and simulate with the latest values he received.
            # Also, increment the LOS Counter
            
            # Check if any data was retrieved and if not, the increment the LOS Counter
            #if recvData == 0:
            #    self.networkEngine.LOSCounter += 1
            # Otherwise, reset the counter
            #else:
            #    self.networkEngine.LOSCounter = 0

            #if len(recvData) != 0:
                # Create a struct/tuple and add it to the input Command dict
            #    clientInput = ServerNetworkingInput()
            #    clientInput.clientInput = recvData
            #    self.inputCommands = clientInput.clientInput

            # Create local data to send to the client
            sendData = self.outputCommands

            # Send data to the client
            if self.networkEngine.encodeData(sendData) == False:
                # print ("Probleme lors de l'envoie de donnee aux Clients.")
                pass
        
            # A problem occurred during networking process, then we stop the thread
            #    print ("An error occurred during networking process in the Server Networking thread. The exception was raised in thread :  " + str(self.threadID) + ". Network connection has been shut down with client : " + str(self.clientID))
            #    self.threadStop = True
        
        # Close socket connection
        self.clientSocket.close()

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
        # self.timer: threading.Timer
        self.threadingRepeatTime: float
        self.threadStop = False
    
    # Initialize the thread
    def initialization(self):
        self.inputCommands = ServerNetworkingOutput()
        self.outputCommands = ServerNetworkingInput()

        self.inputCommands.reset()
        self.outputCommands.reset()

        # Create the local socket to connect to the server
        self.serverSocket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)

        # Connect to remote server
        self.serverSocket.connect((self.serverAddress, int(self.serverPort)))

        # Set socket to non-blocking mode
        self.serverSocket.setblocking(0)

        # Create the network engine and set dependencies
        self.networkEngine = NetworkEngine()
        self.networkEngine.setDependencies(self.serverPort, self.serverAddress, self.serverSocket)
        self.networkEngine.initialization()

        # Create the timer: every 16 ms means 60FPS
        # self.timer = threading.Timer(0.016, self.threadMain())
        self.threadingRepeatTime = THREADING_REPEAT_TIME

    # Set the dependencies
    def setDependencies(self, ServerPort, ServerAddress):
        self.serverPort = ServerPort
        self.serverAddress = ServerAddress
    
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
        print("Starting communication with server at : " + str(self.serverAddress))
        #self.startTimer()
        self.threadMain()
    
    # Main Thread Function
    def threadMain(self):
        while self.threadStop == False:
            #try:
            # Wait for 0.016s = 16ms = 60 FPS
            time.sleep(self.threadingRepeatTime)

            #try:
            # Decode data from the server
            if self.networkEngine.decodeData() == False:
                # print ("Probleme lors de la reception de donnee en provenance du Serveur.")
                pass
            else:
                self.inputCommands = self.networkEngine.lastDataReceived
    #        except:
    #            pass
            
            # Check if any data was retrieved and if not, the increment the LOS Counter
            #if recvData == 0:
            #    self.networkEngine.LOSCounter += 1
            # Otherwise, reset the counter
            #else:
            #    self.networkEngine.LOSCounter = 0

            #if recvData != 0:
                # Create a struct/tuple and add it to the input Command dict
            #    self.inputCommands = recvData

            # Create local data to send to the server
            sendData = self.outputCommands

            # Send data to the server
            if self.networkEngine.encodeData(sendData) == False:
                # print ("Probleme lors de l'envoie des donnees au Serveur.")
                pass
        #except:
                # A problem occurred during networking process, then we stop the thread
        #        print ("An error occurred during networking process in the Client Networking thread. Network connection has been shut down. ")
        #        self.threadStop = True
        
        # Close socket connection
        self.serverSocket.close()

class ServerNetworkingInput:
    """This class represent every input received from a remote client"""

    # Default Constructor
    def __init__(self):
        self.clientInput = [] # list of Client string commands

    # Reset the Object
    def reset(self):
        self.clientInput = []

class ServerNetworkingOutput:
    """This class represent every output processed by the server to be sent to a remote client"""

    # Default Constructor
    def __init__(self):
        self.ennemies: Ennemies
        self.player: Player
        self.otherPlayers = [] # list of Player object
        self.listOfExplosions = [] # list of Explosions to be drawn by the clients
        #self.ennemies: [] # list of Ennemy_group object
    
    # Set Dependencies
    def setDependencies(self, Ennemies, Player, OtherPlayers, ListOfExplosions):
        self.ennemies = Ennemies
        self.player = Player
        self.otherPlayers = OtherPlayers
        self.listOfExplosions = ListOfExplosions

    # Reset the Object
    def reset(self):
        self.ennemies = None
        self.player = None
        self.listOfExplosions = []
        self.otherPlayers = []