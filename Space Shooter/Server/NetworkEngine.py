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

# Macro which defines the number of bytes to encode the message length
MESSAGE_LENGTH = 4

# Macro which defines the number of bytes to encore the current fragment index
CURRENT_FRAGMENT_INDEX_LENGTH = 2

# Macro which defines the number of bytes to encode the maximum fragment index
MAXIMUM_FRAGMENT_INDEX_LENGTH = 2

# Macro which defines the number of bytes to encode the payload length
FRAGMENT_PAYLOAD_LENGTH = 2

# Macro which defines the repeat time (every 32 ms means about 30 Hz)
THREADING_REPEAT_TIME = 2#0.032

class NetworkEngine:
    """Any of Networking element should be found in this class. """

    # Default Constructor
    def __init__(self):
        self.localAddress: str
        self.localPort: int
        self.remoteAddress: str
        self.remotePort: int
        self.bufferSize: int
        self.headerLength: int
        self.socket: socket.socket
        self.lastDataReceived: object
        self.LOSCounter: int
        self.messageID: int
        self.messageIDLength: int
        self.currentFragmentIndexLength: int
        self.maximumFragmentIndexLength: int
        self.fragmentPayloadLength: int
        self.lastReceivedFromAddress: object
    
    # The Server is gonna talk to each Client via UDP Protocol
    def initialization(self):
        #self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.bufferSize = BUFFER_SIZE
        self.headerLength = HEADER_LENGTH
        self.lastDataReceived = None
        self.LOSCounter = 0
        self.messageID = 0
        self.messageIDLength = MESSAGE_LENGTH
        self.currentFragmentIndexLength = CURRENT_FRAGMENT_INDEX_LENGTH
        self.maximumFragmentIndexLength = MAXIMUM_FRAGMENT_INDEX_LENGTH
        self.fragmentPayloadLength = FRAGMENT_PAYLOAD_LENGTH

    # Set the dependencies
    def setDependencies(self, socket, localAddress, localPort, remoteAddress, remotePort):
        self.socket = socket
        self.localAddress = localAddress
        self.localPort = localPort
        self.remoteAddress = remoteAddress
        self.remotePort = remotePort

    # Create fragments for the data
    # The final message is as follow : 
    # MSG = [ [Message_ID (4 bytes)] [Current_Fragment_Index (CFI, 2 bytes)] [Maximum_Fragment_Index (MFI, 2 bytes)] [Fragment_Payload_Length (2 bytes)] [Fragment_Payload (variables length)] ]
    def createFragments(self, data):
        listOfFragments = []

        # print('Les donnees serializer : {!r}'.format(pickle.dumps(data)))

        # Put into a Stream, the binary representation of our data
        dataStream = pickle.dumps(data)
        dataStreamSize = len(dataStream)
        
        payloadAvailableSize = self.bufferSize - self.headerLength
        maximumFragmentIndex = (dataStreamSize // payloadAvailableSize) + 1
        currentFragmentIndex = 0
        offset = 0

        for i in range(0, maximumFragmentIndex):
            fragment = b""
            fragmentPayload = dataStream[offset:offset + payloadAvailableSize]

            msgID = self.messageID.to_bytes(self.messageIDLength, 'big')
            fragment += msgID
            
            fragment += currentFragmentIndex.to_bytes(self.currentFragmentIndexLength, 'big')
            fragment += maximumFragmentIndex.to_bytes(self.maximumFragmentIndexLength, 'big')

            # Converts the size of the data stream onto 4 bytes (with default reading is "big endian")
            fragmentPayloadSize = len(fragmentPayload)
            fragment += fragmentPayloadSize.to_bytes(self.fragmentPayloadLength, 'big')

            fragment += fragmentPayload

            # Add the fragment to the list of fragments
            listOfFragments.append(fragment)

            # Do all increments
            currentFragmentIndex += 1
            offset += payloadAvailableSize

        # Increment the message ID counter
        self.messageID += 1

        return listOfFragments

    # Serialize data
    def encodeData(self, data):
        listOfFragments = self.createFragments(data)

        ind = 0
        for fragment in listOfFragments:
            # Send the data to the socket
            #totalsent = 0

            # While the whole message has not been sent
            #while totalsent < len(fragment):
            #    try:
            #        sent = self.socket.sendto(fragment[totalsent:], (self.address, self.port))
            #    except socket.timeout:
                #print ("Quantite information sent : " + str(sent))
                # If nothing has been sent, it means that the connection has broken
                #if sent == 0:
            #        print("Error : NetworkEngine --> encodeData(), First While, Sending Data. The socket was not ready to send any data. ")
            #        return False
            #    except socket.error:
            #        return False
                # Else, it means that we still need to send the data
            #    else:
            #        totalsent = totalsent + sent
            # print (fragment)
            # self.socket.sendto(fragment, (self.address, self.port))
            ind += 1
            self.writeSocket(fragment)
        
        # Everything went well
        return True
    
    # Retrieve the original message from all the fragments 
    def retrieveMessage(self, listOfFragments):
        message = b""

        messageId = listOfFragments[0][0][0]

        for fragment in listOfFragments:
            if fragment[0][0] != messageId:
                message = b""
                return message

            message += fragment[1]

        return message

    def processFragment(self, fragment):
        # self.processFragmentHeader

        # fragmentPayload = int.from_bytes(fragment[offset:offset + fragmentPayloadLength], 'big')
        # fragmentInfo = (messageID, currentFragmentIndex, maximumFragmentIndex, fragmentPayload)

        # return fragmentInfo
        pass

    def processFragmentHeader(self, header):
        offset = 0

        messageID = int.from_bytes(header[offset:offset + self.messageIDLength], 'big')
        offset += self.messageIDLength

        currentFragmentIndex = int.from_bytes(header[offset:offset + self.currentFragmentIndexLength], 'big')
        offset += self.currentFragmentIndexLength

        maximumFragmentIndex = int.from_bytes(header[offset:offset + self.maximumFragmentIndexLength], 'big')
        offset += self.maximumFragmentIndexLength

        fragmentPayloadSize = int.from_bytes(header[offset:offset + self.fragmentPayloadLength], 'big')
        offset += self.fragmentPayloadLength

        return (messageID, currentFragmentIndex, maximumFragmentIndex, fragmentPayloadSize)

    # De-Serialize data
    def decodeData(self):
        # First, we need to receive the header of the message (which is always a 4-bytes size header),
        # Then, we receive the payload
        firstFragmentPayload = b""
        # fragmentLength = self.headerLength + self.bufferSize
        currentFragmentIndex = -1

        while currentFragmentIndex != 0:
            # TCP implements a stream ptrocol then you ask for how much bytes you want to process.
            # UDP implements a message protocol. Thus, you ask for enough bytes to cover the message or it'll be dropped.
            # See : https://stackoverflow.com/questions/36115971/recv-and-recvfrom-socket-programming-using-python
            firstFragment = self.readSocket(self.bufferSize)

            if firstFragment != b"":
                firstFragmentInfo = self.processFragmentHeader(firstFragment[:self.headerLength])
                firstFragmentPayload = firstFragment[self.headerLength:]
            
                if firstFragmentInfo[1] == 0:
                    currentFragmentIndex = 0
            else:
                return False
        
        firstFragment = (firstFragmentInfo, firstFragmentPayload)

        maximumFragmentIndex = firstFragment[0][2]

        listOfFragments = []
        listOfFragments.append(firstFragment)

        for i in range (1, maximumFragmentIndex):
            fragment = self.readSocket(self.bufferSize)

            if fragment != b"":
                fragmentInfo = self.processFragmentHeader(fragment[:self.headerLength])

                fragmentPayload = fragment[self.headerLength:]
            else:
                return False
            
            fragment = (fragmentInfo, fragmentPayload)
            listOfFragments.append(fragment)

        # Step 0 : check if none of the fragment is missing
        if len(listOfFragments) != maximumFragmentIndex:
            listOfFragments.clear()
            return False

        # Step 1 : re-ordering the fragments
        listOfFragments.sort(key = lambda fragment : fragment[0][1])

        # Step 2 : retrieving the original message
        message = self.retrieveMessage(listOfFragments)
        
        # Recreate the original object from the received data
        if message != b"":
            data = pickle.loads(message)
        else:
            return False

        # Store the received data
        self.lastDataReceived = data

        # Everything went well
        return True

    # Read the socket pipe with the desired length
    # In case of problems, increase the LOS Counter and returns the empty message buffer
    def readSocket(self, length):
        try:
            bytesRead, address = self.socket.recvfrom(length)
            self.lastReceivedFromAddress = address
            print (len(bytesRead))
            self.LOSCounter = 0

        except socket.error:
            self.LOSCounter += 1
            bytesRead = b""
        
        return bytesRead

    # Write to the socket pipe with the desired message
    # In case of problems, increase the LOS Counter and returns -1:
    def writeSocket(self, data):
        try:
            sent = self.socket.sendto(data, (self.remoteAddress, self.remotePort))
            self.LOSCounter = 0
        
        except socket.error:
            self.LOSCounter += 1
            sent = -1
        
        return sent


class ServerNetworkingThread (threading.Thread):
    """This class is instantiate any time a new connection to the main server socket is accepted."""
    # Voir : https://www.tutorialspoint.com/python/python_multithreading.htm
    
    # Default Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.threadID: int
        self.serverSocket: socket
        self.serverIpAddress: str
        self.serverPort : int
        self.clientIpAddress: str
        self.clientPort: int
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
        self.serverSocket.setblocking(0)

        # self.GAME_STATUS = "START"
        self.inputCommands = ServerNetworkingInput()
        self.outputCommands = ServerNetworkingOutput()

        self.inputCommands.reset()
        self.outputCommands.reset()

        # Create the network engine and set dependencies
        self.networkEngine = NetworkEngine()
        self.networkEngine.setDependencies(self.serverSocket, self.serverIpAddress, self.serverPort, self.clientIpAddress, self.clientPort)
        self.networkEngine.initialization()

        # Create the timer: every 16 ms means 60FPS
        # self.timer = threading.Timer(0.016, self.threadMain())
        self.threadingRepeatTime = THREADING_REPEAT_TIME

        # Send to the Client which configuration to use to communicate with the server
        self.networkEngine.encodeData((self.serverIpAddress, self.serverPort))
    
    # Set the dependencies
    def setDependencies(self, threadID, serverSocket, serverIpAddress, serverPort, clientIpAddress, clientPort, clientID):
        self.threadID = threadID
        self.serverSocket = serverSocket
        self.serverIpAddress = serverIpAddress
        self.serverPort = serverPort
        self.clientIpAddress = clientIpAddress
        self.clientPort = clientPort
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
        self.serverSocket.close()

class ClientNetworkingThread(threading.Thread):
    """This class is instantiate once per client. It allows the client to receive and send data from/to a remote server asynchronously"""

    # Default Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.clientSocket: socket
        self.clientIpAddress: str
        self.clientPort: int
        self.serverIpAddress: str
        self.serverPort: int
        self.listOfAvailablePorts: []
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

        self.listOfAvailablePorts = [49300, 49301, 49302, 49303]

        # Create the local socket to connect to the server
        self.clientSocket = socket.socket(socket.AF_INET,
                                          socket.SOCK_DGRAM)

        #self.clientIpAddress = socket.gethostbyname(socket.gethostname())
        self.clientIpAddress = "localhost"
        self.clientPort = self.listOfAvailablePorts[0]
        self.clientSocket.bind((self.clientIpAddress, self.clientPort))
        # Connect to remote server
        #self.serverSocket.connect((self.serverAddress, int(self.serverPort)))

        # Set socket to non-blocking mode
        self.clientSocket.setblocking(0)

        # Create the network engine and set dependencies
        self.networkEngine = NetworkEngine()
        self.networkEngine.setDependencies(self.clientSocket, self.clientIpAddress, self.clientPort, self.serverIpAddress, self.serverPort)
        self.networkEngine.initialization()

        # Create the timer: every 16 ms means 60FPS
        # self.timer = threading.Timer(0.016, self.threadMain())
        self.threadingRepeatTime = THREADING_REPEAT_TIME

        self.networkEngine.encodeData("GAME_SESSION_JOIN")

        # Fill-up the server's infos
        while True:
            if self.networkEngine.decodeData() == True:
                self.serverIpAddress = self.networkEngine.lastReceivedFromAddress[0]
                self.serverPort = self.networkEngine.lastReceivedFromAddress[1]

                self.networkEngine.setDependencies(self.clientSocket, self.clientIpAddress, self.clientPort, self.serverIpAddress, self.serverPort)
                break

    # Set the dependencies
    def setDependencies(self, clientSocket, clientIpAddress, clientPort, serverIpAddress, serverPort):
        self.clientSocket = clientSocket
        self.clientIpAddress = clientIpAddress
        self.clientPort = clientPort
        self.serverIpAddress = serverIpAddress
        self.serverPort = serverPort
    
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
        print("Starting communication with server at : " + str(self.serverIpAddress))
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
        self.clientSocket.close()

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