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

#Used to remember where to draw explosions :
ListofExplosions = []

#player score :
score = Score()

#The Physic Engine :
physicEngine = PhysicEngine.PhysicEngine()

#The Renderer Engine :
rendererEngine = RendererEngine.RendererEngine()

#The Input Engine :
inputEngine = InputEngine.InputEngine()

#player number of shield left :
nb_player_shield = 3

#The space shuttle and its position as global variables :
#animatedSpaceShuttle = pygame.Surface((0,0)) 
#animatedSpaceShuttleRect = animatedSpaceShuttle.get_rect()

#The background of the game :
#animatedMainGameBackGround1 = pygame.image.load(pathfile.mainGameBackGround1)
#animatedMainGameBackGround1Compensation = pygame.image.load(pathfile.mainGameBackGround1)
#animatedMainGameBackGround2 = pygame.image.load(pathfile.mainGameBackGround2)
#animatedMainGameBackGround2Compensation1 = pygame.image.load(pathfile.mainGameBackGround2)
# animatedMainGameBackGround2Compensation2 = pygame.image.load(pathfile.mainGameBackGround2)

#This is used to make the background scroll :
current_background_position_1 = 0
current_background_position_2 = [0,0]

#The countdown for the background :
#backgroundCountDown = 0
#The background Pattern :
backgroundPattern = random.choice([0,2,4,6])#0

#List of selected option from the main menu :
ListSelectedOptions = [1,0]

#List of available game state :
#ListAvailableGameState = ["MENU","OPTIONS","GAME"]
#MENU --> You can go back to the main menu
#OPTIONS --> Used in the main menu to configure the game options
#GAME --> Lets you enter into the game
#QUIT --> Quit the game
#Current Game State :
CURRENT_GAME_STATE = "MENU"

##########################################################FUNCTIONS##############################################################################################
def mainWindowLogoAnimation():
	"""This function provides animation of the main Logo displayed on the main window"""
	print("TODO")

def mainWindowOptionsRenderer():
	"""This function create each elements from the main window"""
	global spriteManager
	
	#Here we create the differents options :
	policeFont = spriteManager.ListofSysFonts["Times New Roman"]

	#Play game button :
	if ListSelectedOptions == [1,0]:
		playGameButtonImg = policeFont.render("Play Game",0,(255,0,0))
	elif ListSelectedOptions == [0,1]:
		playGameButtonImg = policeFont.render("Play Game",0,(255,255,255))
	mainWindow.blit(playGameButtonImg,(70,200))

	#Exit game button :
	if ListSelectedOptions == [1,0]:
		exitGameButtonImg = policeFont.render("Exit Game",0,(255,255,255))
	elif ListSelectedOptions == [0,1]:
		exitGameButtonImg = policeFont.render("Exit Game",0,(255,0,0))
	mainWindow.blit(exitGameButtonImg,(70,230))

	#Credits :
	creditsFont = spriteManager.ListofSysFonts["Arial"]
	creditsFont.set_italic(True)
	creditsText = "Space Shooter, v1.0.2, author : Yoshii_974, all right reserved.TM"
	creditsImg = creditsFont.render(creditsText,1,(255,255,0))
	mainWindow.blit(creditsImg,(200,495))

def mainWindowSpaceShuttle():
	"""This function provides a spacecraft to be animated from time to time. This function does not deal with the animation of the spaceshuttle. It only gives which one to choose in the list of all spaceshuttle available."""
	global animatedSpaceShuttle
	global animatedSpaceShuttleRect
	global spriteManager

	#Choose randomly a ship to be showed
	randomKey = random.choice(spriteManager.ListofEnnemiesSurfaceKeys)
	animatedSpaceShuttle = spriteManager.ListofEnnemiesSurface[randomKey]

	#Define the position of the ship
	animatedSpaceShuttleRect.x = 475
	animatedSpaceShuttleRect.y = 350

def mainWindowSpaceShuttleAnimation():
	"""Calculate the new position of the animated ship. Return True if the position is still positif, false otherwise"""
	global animatedSpaceShuttleRect

	#Move the ship per 4 pixels throught the window
	if animatedSpaceShuttleRect.x > 0:
		animatedSpaceShuttleRect = animatedSpaceShuttleRect.move(-4,0)
		return True
	else:
		return False

###THE BIG FUNCTION###
def mainGameAnimationRendererManager():
	"""This function provides animation for each elements drawned on the screen. This function is typically called by the game loop."""
	global animatedSpaceShuttle
	global animatedSpaceShuttleRect
	global player
	global ennemies
	global spriteManager
	global musicAndSoundManager

	if CURRENT_GAME_STATE == "MENU":
		#The main background
		mainWindow.blit(mainWindowBG,(0,0))
		#The logo
		mainWindow.blit(mainWindowLogo,(25,-10))
		#The credits
		mainWindowOptionsRenderer()
	
		#Add this shuttle to the main menu window and refresh the screen
		if (mainWindowSpaceShuttleAnimation()):
			mainWindow.blit(animatedSpaceShuttle,animatedSpaceShuttleRect)
	
	elif CURRENT_GAME_STATE == "GAME_OVER":
		#Display a game over message :
		print("We are in game over mode.")
		#Change the music :
		#musicAndSoundManager.play("game_over")
		
	elif CURRENT_GAME_STATE == "GAME":

		#Animate the background :
		mainGameBackGroundAnimationRenderer(ennemies.GAME_STATUS)
		
		#Destroy the player's fireshot which lifespan has been reached:
		player.destroyFireShots()
		
		#Check for the animation of the player :
		player.animate()
		
		#Update the wave of ennemies :
		ennemies.updateEnnemiesWave()
		
		#Destroy all previous ennemy shots :
		ennemies.destroyFireShots()
		
		#Make ennemies to trigger fire shots :
		ennemies.fire()
		ennemies.animateFireShots()
		
		#Animate the ennemies groups :
		ennemies.animate()
		
		#Call the physic collision detector :
		enablePhysicdetection = True
		for eg_id in ennemies.ListofEnnemiesWave[ennemies.currentEnnemyWave]:
			eg = ennemies.ListofEnnemies[eg_id]
			if eg.endStartMove == False:
				enablePhysicdetection = False
		
		if enablePhysicdetection:
			#physicCollisionManager()
			physicEngine.simulateAllCollisions()

		#Check the game over status :
		checkGameOverStatus()

		#Draw everything which has to be drawned :
		mainWindow.blit(spriteManager.ListofPlayerSurface[player.SpriteKey],(player.x,player.y))
		
		#For each ennemy group :
		for eg_id,eg in ennemies.ListofEnnemies.items():
			for e in eg.ListofPositions:
				draw_ennemy = spriteManager.ListofEnnemiesSurface[eg.surface_id]
				
				#Convert orientation to degrees :
				if e[3] == 0:
					angle = 0
				elif e[3] == 1:
					angle = -45
				elif e[3] == 2:
					angle = -90
				elif e[3] == 3:
					angle = -135
				elif e[3] == 4:
					angle = -180
				elif e[3] == 5:
					angle = -225
				elif e[3] == 6:
					angle = -270
				elif e[3] == 7:
					angle = -315
				elif e[3] == 8:
					angle = -360
			
				#Apply rotation before the final draw call :
				if not angle == 0:
					draw_ennemy = spriteManager.rot_center(draw_ennemy,angle)
				
				#The Final draw call:
				mainWindow.blit(draw_ennemy,(e[1],e[2]))
		
		#Draw the shots after drawing the ennemies. This way, the shots are overwritting the ennemies sprites/surface and lets the player knows what happen to the shot :
		for shot_id,shot in player.ListofFireShot.items():
			#Final draw call
			mainWindow.blit(spriteManager.ListofFireShotSurface[shot.type],(shot.x,shot.y))
		
		#Draw each ennemy with a rotation which is the same as the shot angle :
		for eg_id,eg in ennemies.ListofEnnemies.items():
			for shot_id,shot in eg.ListofFireShot.items():
				draw_shot = spriteManager.ListofFireShotSurface[shot.type]
				
				#Convert orientation to degrees :
				if shot.orientation == 0:
					angle = 0
				elif shot.orientation == 1:
					angle = -45
				elif shot.orientation == 2:
					angle = -90
				elif shot.orientation == 3:
					angle = -135
				elif shot.orientation == 4:
					angle = -180
				elif shot.orientation == 5:
					angle = -225
				elif shot.orientation == 6:
					angle = -270
				elif shot.orientation == 7:
					angle = -315
				elif shot.orientation == 8:
					angle = -360
			
				#Apply rotation before the final draw call :
				draw_shot = spriteManager.rot_center(draw_shot,angle)
				
				#The final draw call :
				mainWindow.blit(draw_shot,(shot.x,shot.y))
		
		#Draw the explosions :
		makingExplosions()

		#Draw the health bar :
		updateHealthBarStatus()

		#Update the player score :
		updatePlayerScore()
		
		#Update the number of remaining shields :
		updatePlayerShield()

		#TEST:
		if player.activateShield > 0:
			activatePlayerShield()
	
	#Finally, refresh the screen
	pygame.display.flip()



def mainGameBackGroundAnimationRenderer(mode):
	"""This function animates the background. It allows the background to be scrolled each time this function it's called."""
	global animatedMainGameBackGround1
	global animatedMainGameBackGround1Compensation
	global animatedMainGameBackGround2
	global animatedMainGameBackGround2Compensation1
	# global animatedMainGameBackGround2Compensation2
	global current_background_position_1
	global current_background_position_2
	global backgroundCountDown
	global backgroundPattern
	
	if mode == "NORMAL":
		#The current position of the main game background and the position of the duplicate :
		current_background_position_1 += 2

		#Get the rect from the background in order to know and use the height :
		background_rect_1 = animatedMainGameBackGround1.get_rect()
		background_height_1 = background_rect_1.height
		
		#Scroll the background by 2 pixels:
		mainWindow.blit(animatedMainGameBackGround1,(0,current_background_position_1))
		mainWindow.blit(animatedMainGameBackGround1Compensation,(0,current_background_position_1 - background_height_1))
		
		#If the background y position has reached the size of the screen, we reset the position :
		if current_background_position_1 == background_height_1:
			current_background_position_1 = 0
		
	elif mode == "BOSS":
		#The current position of the main game background and the position of the duplicate :
		#backgroundCountDown += 1
		
		#Increase the countdown :
		#if backgroundCountDown == 800:
		#	backgroundPattern += 2
		#	backgroundCountDown = 0
		
		#Check current value of backgroundPattern :
		#if backgroundPattern == 8:
		#	backgroundPattern = 0
		
		#Change the scroll x and y, of the background :
		if backgroundPattern == 0:
			current_background_position_2[0] += 0
			current_background_position_2[1] -= 1
			
			mainWindow.blit(animatedMainGameBackGround2,(0,current_background_position_2[1]))
			mainWindow.blit(animatedMainGameBackGround2Compensation1,(0,MAIN_WINDOW_SIZE + current_background_position_2[1]))
		
			if current_background_position_2[1] == -MAIN_WINDOW_SIZE:
				current_background_position_2[1] = 0
			
		#elif backgroundPattern == 1:
		#	current_background_position_2[0] += 1
		#	current_background_position_2[1] -= 1
		elif backgroundPattern == 2:
			current_background_position_2[0] += 1
			current_background_position_2[1] += 0
			
			mainWindow.blit(animatedMainGameBackGround2,(current_background_position_2[0],0))
			mainWindow.blit(animatedMainGameBackGround2Compensation1,(-MAIN_WINDOW_SIZE + current_background_position_2[0],0))
		
			if current_background_position_2[0] == MAIN_WINDOW_SIZE:
				current_background_position_2[0] = 0
		
		#elif backgroundPattern == 3:
		#	current_background_position_2[0] += 1
		#	current_background_position_2[1] += 1
		
		elif backgroundPattern == 4:
			current_background_position_2[0] += 0
			current_background_position_2[1] += 1
			
			mainWindow.blit(animatedMainGameBackGround2,(0,current_background_position_2[1]))
			mainWindow.blit(animatedMainGameBackGround2Compensation1,(0,-MAIN_WINDOW_SIZE + current_background_position_2[1]))
		
			if current_background_position_2[1] == MAIN_WINDOW_SIZE:
				current_background_position_2[1] = 0
		
		#elif backgroundPattern == 5:
		#	current_background_position_2[0] -= 1
		#	current_background_position_2[1] += 1
		
		
		elif backgroundPattern == 6:
			current_background_position_2[0] -= 1
			current_background_position_2[1] += 0
			
			mainWindow.blit(animatedMainGameBackGround2,(current_background_position_2[0],0))
			mainWindow.blit(animatedMainGameBackGround2Compensation1,(MAIN_WINDOW_SIZE + current_background_position_2[0],0))
		
			if current_background_position_2[0] == -MAIN_WINDOW_SIZE:
				current_background_position_2[0] = 0
		
		#elif backgroundPattern == 7:
		#	current_background_position_2[0] -= 1
		#	current_background_position_2[1] -= 1

def makingExplosions():
	"""This function is only useful for drawing and producing explosions objects at the right place, at the right time..."""
	global ListofExplosions
	global spriteManager
	global musicAndSoundManager

	#Contains each explosions which has their lifespan 1 and 2 equals to 0 it's time to remove this explosion object :
	listofExplosionsToBeRemoved = []
	
	#Loop on each explosions :
	for exp in ListofExplosions:
		if exp.lifespan1 > 0:
			mainWindow.blit(spriteManager.ListofExplosionSurface["explosion1"],(exp.x,exp.y))
			if exp.hasSoundBeenPlayed == 0:
				musicAndSoundManager.ListofExplosionSound["explosion1"].play()
				exp.hasSoundBeenPlayed = 1
			exp.lifespan1 -= 1
		elif exp.lifespan2 > 0:
			mainWindow.blit(spriteManager.ListofExplosionSurface["explosion2"],(exp.x,exp.y))
			exp.lifespan2 -= 1
		else:
			listofExplosionsToBeRemoved.append(exp)

	#We delete every explosions which has no longer any reason to stay alive:
	for exp in listofExplosionsToBeRemoved:
		ListofExplosions.remove(exp)



def checkGameOverStatus():
	"""Check if the player is still able to play the game. This means that if the player's health is equal to 0, the game is over."""
	global player
	global CURRENT_GAME_STATE
	
	#Check the player's health :
	if player.health <= 0:
		CURRENT_GAME_STATE = "GAME_OVER"





def updateHealthBarStatus():
	"""Update the health bar status and draw it at the screen."""
	global player
	global spriteManager

	#First, draw the rect which is updated depending on the current player's health.
	x_health = (player.health/player.maxHealth) * 115
	if x_health < 0:
		x_health = 0
	health_bar_surface = pygame.Surface((int(x_health),10))
	
	#Fill the surface partially depending on the player's health :
	health_bar_surface.fill((0,255,0))
	
	#Finaly, draw the health bar :
	mainWindow.blit(health_bar_surface,(512-130,20))
	mainWindow.blit(spriteManager.HealthBar,(512-150,15))



def updatePlayerScore():
	"""Update the player score."""
	global score
	global spriteManager
	
	#Draw the score :
	policeFont = spriteManager.ListofSysFonts["Times New Roman"]
	score_sentence = "THE SCORE : " + str(score.playerScore)
	ScoreSurface = policeFont.render(score_sentence,0,(0,255,0))
	mainWindow.blit(ScoreSurface,(20,20))

	
def updatePlayerShield():
	"""Update the number of shield which remain for the player"""
	global nb_player_shield
	global spriteManager
	
	#Draw the number of remaining shields
	policeFont = spriteManager.ListofSysFonts["Times New Roman"]
	shield_sentence = "REMAINING SHIELDS : " + str(nb_player_shield)
	ShieldSurface = policeFont.render(shield_sentence,0,(0,255,0));
	mainWindow.blit(ShieldSurface,(20,40))

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