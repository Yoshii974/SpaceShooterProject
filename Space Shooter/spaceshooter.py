# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 5 Août 2015																																					#
### Author : Yoshii_974																																					#
### Description : This is the main file of the space shooter program. 																									#
### This file contain the game logic such as : the use of pygame for the 2D drawcall, the main game loop.																#
#########################################################################################################################################################################

##########################################################IMPORTS########################################################################################################
import random
import pathfile
import PhysicEngine
import RendererEngine
import InputEngine
import pygame
from Server import NetworkEngine
from pygame.locals import *
from commonclasses import *
from Player import *
from Ennemies import *
##########################################################GLOBAL VARIABLES###############################################################################################
#Size in pixels of the main menu's window :
MAIN_WINDOW_SIZE = 512

#Size in pixels of a game elements :
GAME_ELEMENT_SIZE = 32

#Size in pixels of the player element :
GAME_ELEMENT_PLAYER_SIZE = 50

#The main character :
player = Player(256,452)
player.playerID = 0

#List of players :
listOfPlayers = []
listOfPlayers.append(player)

#The ennemies of the game :
ennemies = Ennemies()
ennemies.PlayerObject = player

#Joysticks ID :
JOYSTICK_ID = 0

#The Sprite Manager :
spriteManager = SpriteManager()

#The Music and Sound Manager :
musicAndSoundManager = MusicAndSoundManager()

#The Physic Engine :
physicEngine = PhysicEngine.PhysicEngine()

#The Renderer Engine :
rendererEngine = RendererEngine.RendererEngine()

#The Input Engine :
inputEngine = InputEngine.InputEngine()

#The Client Networking Thread :
clientNetworkingThread = NetworkEngine.ClientNetworkingThread()

#This is used to make the background scroll :
current_background_position_1 = 0
current_background_position_2 = [0,0]

#List of selected option from the main menu :
ListSelectedOptions = [1,0]

#MENU --> You can go back to the main menu
#OPTIONS --> Used in the main menu to configure the game options
#GAME --> Lets you enter into the game
#QUIT --> Quit the game

##########################################################FUNCTIONS##############################################################################################
#Multiplayer Initialization function :
def multiplayerInitialization():
	global isMultiplayerInitialized
	
	serverAddress = input('Plz, enter server address : ')
	serverPort = input('Plz, enter server port : ')

	#Set client networking dependencies
	clientNetworkingThread.serverIpAddress = serverAddress
	clientNetworkingThread.serverPort = int(serverPort)
	clientNetworkingThread.initialization()

	#Set dependencies to the client network
	rendererEngine.clientNetworkingThread = clientNetworkingThread
	inputEngine.clientNetworkingThread = clientNetworkingThread
	physicEngine.clientNetworkingThread = clientNetworkingThread

	clientNetworkingThread.inputCommands.ennemies = ennemies
	clientNetworkingThread.inputCommands.player = player
	clientNetworkingThread.inputCommands.otherPlayers = []
	clientNetworkingThread.inputCommands.listOfExplosions = physicEngine.listofExplosions

	#Start the network thread
	clientNetworkingThread.start()
	#clientNetworkingThread.join()

	#player2 = Player(256,452)
	#player2.playerID = 1
	#player2.initialization()
	#physicEngine.players.append(player2)
	#rendererEngine.players.append(player2)

	#No need to get into this part of the code once the multiplayer mode has been already initialized
	isMultiplayerInitialized = True


###########################################################MAIN##########################################################################################################
#Set the ennemies and player references to the sprite and sound managers :
physicEngine.setDependencies(ennemies,
							 listOfPlayers)
physicEngine.inputEngine = inputEngine

rendererEngine.setDependencies(spriteManager,
							   musicAndSoundManager,
							   physicEngine,
							   ennemies,
							   listOfPlayers)

#Set input engine dependencies :
inputEngine.setDependencies(player)

#Set ennemies dependencies :
ennemies.SpriteManager = spriteManager
ennemies.MusicAndSoundManager = musicAndSoundManager

#Initialize the renderer engine :
rendererEngine.initialization()

#Initialize the input engine :
inputEngine.initialization()

#Initialize the sprite manager :
spriteManager.initialization()

#Initialize the music and sound manager :
musicAndSoundManager.initialization()

#Initialize the ennemies :
ennemies.initialization()

#Initialize the player :
player.initialization()

#Multiplayer initialization control :
isMultiplayerInitialized = False

#Main Game loop :
while True:
	#The renderer engine state
	state = rendererEngine.currentGameState

	if state == "QUIT" or state == "GAME_OVER":
		break
	
	#Call the input engine
	inputEngine.getPygameEvents()

	#Synchronise the state of the renderer engine with the state of the input engine
	if state == "MENU":
		rendererEngine.mainMenuOptionsSelections = inputEngine.mainMenuOptionsSelections
		rendererEngine.setCurrentGameState(inputEngine.currentGameState)
		state = rendererEngine.currentGameState
	
	if state == "MULTI_PLAYER" and isMultiplayerInitialized == False:
		multiplayerInitialization()
	
	#Here is the end of the main menu loop. So every needs in animation is done at this place
	rendererEngine.renderAll()

###END of the Game###
print("See you next time !")
pygame.quit()