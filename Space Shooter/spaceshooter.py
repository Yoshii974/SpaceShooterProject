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

#Player's space shuttle :
player = Player(256,452)

#These lists contains respectively the ennemies and the differents weapons available for the player :
ennemies = Ennemies()
ennemies.PlayerObject = player

#Joysticks ID :
JOYSTICK_ID = 0

#The Sprite Manager :
spriteManager = SpriteManager()

#The Music and Sound Manager :
musicAndSoundManager = MusicAndSoundManager()

#player score :
score = Score()

#The Physic Engine :
physicEngine = PhysicEngine.PhysicEngine()

#The Renderer Engine :
rendererEngine = RendererEngine.RendererEngine()

#The Input Engine :
inputEngine = InputEngine.InputEngine()

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



###########################################################MAIN##########################################################################################################
#Set the ennemies and player references to the sprite and sound managers :
physicEngine.setDependencies(ennemies,
							 player,
							 score)

rendererEngine.setDependencies(spriteManager,
							   musicAndSoundManager,
							   physicEngine,
							   ennemies,
							   player,
							   score)

inputEngine.setDependencies(player)

#Initialize the renderer engine :
rendererEngine.initialization()

#Initialize the input engine :
inputEngine.initialization()

#Initialize the sprite manager :
spriteManager.initialization()

#Initialize the music and sound manager :
musicAndSoundManager.initialization()

player.SpriteManager = spriteManager
player.MusicAndSoundManager = musicAndSoundManager
ennemies.SpriteManager = spriteManager
ennemies.MusicAndSoundManager = musicAndSoundManager

#Initialize the ennemies :
ennemies.initialization()

#Initialize the player :
player.initialization()

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
		rendererEngine.setCurrentGameState(inputEngine.currentGameState)
		rendererEngine.mainMenuOptionsSelections = inputEngine.mainMenuOptionsSelections
	
	#Here is the end of the main menu loop. So every needs in animation is done at this place
	rendererEngine.renderAll()

###END of the Game###
print("See you next time !")
pygame.quit()