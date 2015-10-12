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
from commonclasses import *
from Player import *
from Ennemies import *
import pygame
from pygame.locals import *
##########################################################GLOBAL VARIABLES###############################################################################################
#Size in pixels of the main menu's window :
MAIN_WINDOW_SIZE = 512

#Size in pixels of a game elements :
GAME_ELEMENT_SIZE = 32

#Size in pixels of the player element :
GAME_ELEMENT_PLAYER_SIZE = 50

#These lists contains respectively the ennemies and the differents weapons available for the player :
ennemies = Ennemies()

#Player's space shuttle :
player = Player(256,452)

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

#The space shuttle and its position as global variables :
animatedSpaceShuttle = pygame.Surface((0,0)) 
animatedSpaceShuttleRect = animatedSpaceShuttle.get_rect()

#The background of the game :
animatedMainGameBackGround1 = pygame.image.load(pathfile.mainGameBackGround1)
animatedMainGameBackGround1Compensation = pygame.image.load(pathfile.mainGameBackGround1)
animatedMainGameBackGround2 = pygame.image.load(pathfile.mainGameBackGround2)
animatedMainGameBackGround2Compensation = pygame.image.load(pathfile.mainGameBackGround2)

#This is used to make the background scroll :
current_background_position = 0

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
	creditsText = "Space Shooter, v1.0.1, author : Yoshii_974, all right reserved.TM"
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



#Physics engine for the ennemy and the player collisions :
def physicCollisionManager():
	"""This function deals with every physics component related to ennemies."""
	global ennemies
	global player
	global ListofExplosions
	global score

	#Loop on each ennemy group and check if there's any collision :
	ListofEnnemiesCollisions = []
	
	for fire_id,fireshot in player.ListofFireShot.items():
		#Create a fireshot rect:
		fireshot_rect = pygame.Rect(fireshot.x,fireshot.y,GAME_ELEMENT_SIZE,GAME_ELEMENT_SIZE)
		collisionFound = False
		#for each ennemy in each ennemy_group:
		for eg_id,eg in ennemies.ListofEnnemies.items():
			if collisionFound == False:
				for e in eg.ListofPositions:
					if collisionFound == False:
						e_rect = pygame.Rect(e[1],e[2],GAME_ELEMENT_SIZE,GAME_ELEMENT_SIZE)
						#If there is a collision between the current fireshot and the current ennemy, then we create a collision and we go to the next fireshot checking :
						if fireshot_rect.colliderect(e_rect):
							collision = [eg_id,e[0],fire_id]
							ListofEnnemiesCollisions.append(collision)
							collisionFound = True

	#Now, it is time to destroy every elements which collided with something else:
	for col in ListofEnnemiesCollisions:
		print(col)
		eg = ennemies.ListofEnnemies[col[0]]
		for e in eg.ListofPositions:
			if e[0] == col[1]:
				ennemyToBeRemoved = e
				exp = Explosion(e[1],e[2])
				ListofExplosions.append(exp)
				score.playerScore += 50
				eg.currentEnnemyNumber -= 1
				break
		if eg.ListofPositions.count(ennemyToBeRemoved) != 0:
			eg.ListofPositions.remove(ennemyToBeRemoved)
		del player.ListofFireShot[col[2]]

	#Checking if any of the ennemies shots collide with the player. In this case, the player health is decreased :
	ListofPlayerCollisions = []
	player_rect = pygame.Rect(player.x,player.y,GAME_ELEMENT_PLAYER_SIZE,GAME_ELEMENT_PLAYER_SIZE)

	for eg_id,eg in ennemies.ListofEnnemies.items():
		for shot_id,shot in eg.ListofFireShot.items():
			shot_rect = pygame.Rect(shot.x,shot.y,GAME_ELEMENT_SIZE,GAME_ELEMENT_SIZE)
			if (shot_rect.colliderect(player_rect)):
				collision = [eg_id,shot_id]
				ListofPlayerCollisions.append(collision)

	for col in ListofPlayerCollisions:
		eg = ennemies.ListofEnnemies[col[0]]
		del eg.ListofFireShot[col[1]]
		if player.activateShield == 0:
			print(player.health)
			player.health -= 10


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
		mainGameBackGroundAnimationRenderer("NORMAL")
		
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
			physicCollisionManager()

		#Check the game over status :
		checkGameOverStatus()

		#Draw everything which has to be drawned :
		mainWindow.blit(spriteManager.ListofPlayerSurface[player.SpriteKey],(player.x,player.y))
		
		#For each ennemy group :
		for eg_id,eg in ennemies.ListofEnnemies.items():
			for e in eg.ListofPositions:
				mainWindow.blit(spriteManager.ListofEnnemiesSurface[eg.surface_id],(e[1],e[2]))
		
		#Draw the shots after drawing the ennemies. This way, the shots are overwritting the ennemies sprites/surface and lets the player knows what happen to the shot :
		for shot_id,shot in player.ListofFireShot.items():
			mainWindow.blit(spriteManager.ListofFireShotSurface[shot.type],(shot.x,shot.y))

		for eg_id,eg in ennemies.ListofEnnemies.items():
			for shot_id,shot in eg.ListofFireShot.items():
				mainWindow.blit(spriteManager.ListofFireShotSurface[shot.type],(shot.x,shot.y))
		
		#Draw the explosions :
		makingExplosions()

		#Draw the health bar :
		updateHealthBarStatus()

		#Update the player score :
		updatePlayerScore()

		#TEST:
		if player.activateShield > 0:
			activatePlayerShield()
	
	#Finally, refresh the screen
	pygame.display.flip()



def mainGameBackGroundAnimationRenderer(mode):
	"""This function animates the background. It allows the background to be scrolled each timew this funciton it's called."""
	global animatedMainGameBackGround1
	global animatedMainGameBackGround1Compensation
	global current_background_position

	#The current position of the main game background and the position of the duplicate :
	current_background_position = current_background_position + 2

	#Get the rect from the background in order to know and use the height :
	background_rect = animatedMainGameBackGround1.get_rect()
	background_height = background_rect.height

	if mode == "NORMAL":
		#Scroll the background by 2 pixels:
		mainWindow.blit(animatedMainGameBackGround1,(0,current_background_position))
		mainWindow.blit(animatedMainGameBackGround1Compensation,(0,current_background_position - background_height))
	elif mode == "BOSS":
		#TODO: Find out an algorithm to have the background moving in each directions during fight against the boss :
		animatedMainGameBackGround1.scroll(0,2)
	
	#If the background y position has reached the size of the screen, we reset the position :
	if current_background_position == background_height:
		current_background_position = 0


def mainGameInitialization():
	"""Initialise the display window for receiving the differents elements of the game and initialize the game elements itselfs"""
	global player
	global ennemies
	global spriteManager
	global musicAndSoundManager
	global animatedMainGameBackGround1
	global JOYSTICK_ID

	#Set the key repeat mode :
	pygame.key.set_repeat(50,100)

	#Set the level1 music :
	musicAndSoundManager.playMusic("level1")

	#Set the ennemies and player references to the sprite and sound managers :
	player.SpriteManager = spriteManager
	player.MusicAndSoundManager = musicAndSoundManager
	ennemies.SpriteManager = spriteManager
	ennemies.MusicAndSoundManager = musicAndSoundManager

	#Initialize the ennemies :
	ennemies.initialization()

	#Initialize the player :
	player.initialization()

	#TEST JOYSTICK :
	nb_joysticks = pygame.joystick.get_count()
	print("Il y a " + str(nb_joysticks) + " joysticks connecté au PC")

	#Check if there's any Joystick connected to the PC:
	if nb_joysticks > 0:
		joystick_player = pygame.joystick.Joystick(JOYSTICK_ID)
		JOYSTICK_ID += 1
		joystick_player.init()
		print("Joystick name : " + joystick_player.get_name())
		print("Axes :", joystick_player.get_numaxes())
		print("Boutons :", joystick_player.get_numbuttons())
		print("Trackballs :", joystick_player.get_numballs())
		print("Hats :", joystick_player.get_numhats())

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




def activatePlayerShield():
	"""Activate the shield around the player."""
	global player
	global spriteManager
	
	#Draw the shield :
	shield_surface = spriteManager.ListofExplosionSurface["bonusCircle"]
	mainWindow.blit(shield_surface,(player.x - 16,player.y - 16))
	player.activateShield -= 1

###########################################################MAIN##########################################################################################################
# Initialization of pygame :
pygame.init()

### Main menu ###
# Using pygame to create the main menu window :
mainWindow = pygame.display.set_mode((MAIN_WINDOW_SIZE, MAIN_WINDOW_SIZE))

#Initialize the sprite manager :
spriteManager.initialization()

#Initialize the music and sound manager :
musicAndSoundManager.initialization()

#Add a font to the background of the main window menu :
mainWindowBG = pygame.image.load(pathfile.mainWindowBackGround).convert()
mainWindow.blit(mainWindowBG,(0,0))

#Add the logo of the game :
mainWindowLogo = pygame.image.load(pathfile.mainWindowLogo).convert_alpha()
mainWindow.blit(mainWindowLogo,(25,-10))

#Call the animation of the main menu :
mainWindowSpaceShuttle()

#Call the music manager :
musicAndSoundManager.playMusic("mainMenu")

#Main window loop :
while CURRENT_GAME_STATE == "MENU":
	
	#Limitation of the loop to only 30 fps :
	pygame.time.Clock().tick(30)
	
	#Here is the end of the main menu loop. So every needs in animation is done at this place
	mainGameAnimationRendererManager()
	
	#Loop on each event which has been sent by PyGame :	
	for evt in pygame.event.get():
		
		#If the player selected the quit button (cross right-sided of the window)
		if evt.type == QUIT:
			CURRENT_GAME_STATE = "QUIT"
		
		elif evt.type == KEYDOWN:
			if evt.key == K_DOWN:
				if ListSelectedOptions == [1,0]:
					ListSelectedOptions = [0,1]
				elif ListSelectedOptions == [0,1]:
					ListSelectedOptions = [1,0]
			
			if evt.key == K_UP:
				if ListSelectedOptions == [1,0]:
					ListSelectedOptions = [0,1]
				elif ListSelectedOptions == [0,1]:
					ListSelectedOptions = [1,0]

			if evt.key == K_RETURN or evt.key == K_KP_ENTER:
				if ListSelectedOptions == [1,0]:
					CURRENT_GAME_STATE = "GAME"
				elif ListSelectedOptions == [0,1]:
					CURRENT_GAME_STATE = "QUIT"



###Main Game###
#Initializing the game objects :
mainGameInitialization()

#The main game loop :
while CURRENT_GAME_STATE == "GAME":
	
	#Loop on all the event sent by pygame :
	for evt in pygame.event.get():
		if evt.type == KEYDOWN:
			if evt.key == K_DOWN:
				player.dy = 2
			elif evt.key == K_UP:
				player.dy = -2
			elif evt.key == K_LEFT:
				player.dx = -2
			elif evt.key == K_RIGHT:
				player.dx = 2
			elif evt.key == K_SPACE:
				player.fireShot()
			elif evt.key == K_LCTRL:
				if player.activateShield == 0:
					player.activateShield = 500
			elif evt.key == K_F1:
				player.currentWeapon = "fire1"
			elif evt.key == K_F2:
				player.currentWeapon = "fire2"
			elif evt.key == K_F3:
				player.currentWeapon = "fire3"

		elif evt.type == KEYUP:
			if evt.key == K_LEFT or evt.key == K_RIGHT:
				player.dx = 0
			elif evt.key == K_DOWN or evt.key == K_UP:
				player.dy = 0
			elif evt.key == K_SPACE:
				player.fireShot()
			elif evt.key == K_LCTRL:
				if player.activateShield == 0:
					player.activateShield = 500
			elif evt.key == K_F1:
				player.currentWeapon = "fire1"
			elif evt.key == K_F2:
				player.currentWeapon = "fire2"
			elif evt.key == K_F3:
				player.currentWeapon = "fire3"
		
		elif evt.type == JOYBUTTONDOWN:
			if evt.button == 0:
				player.fireShot()
			elif evt.button == 1:
				if player.currentWeapon == "fire1":
					player.currentWeapon = "fire2"
				elif player.currentWeapon == "fire2":
					player.currentWeapon = "fire3"
				elif player.currentWeapon == "fire3":
					player.currentWeapon = "fire1"
			elif evt.button == 2:
				if player.activateShield == 0:
					player.activateShield = 500
		
		elif evt.type == JOYAXISMOTION:
			if evt.axis == 0:
				if evt.value < -0.25:
					player.dx = -2
				elif evt.value > 0.25:
					player.dx = 2
				else:
					player.dx = 0
			elif evt.axis == 1:
				if evt.value < -0.25:
					player.dy = -2
				elif evt.value > 0.25:
					player.dy = 2
				else:
					player.dy = 0
			
	#Call the Animation Manager :
	mainGameAnimationRendererManager()

###END of the Game###
print("See you next time !")
pygame.quit()