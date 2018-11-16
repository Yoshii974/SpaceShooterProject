# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 21 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains every Rendering Logic for the game. 																							    #
#########################################################################################################################################################################
import pygame
import PhysicEngine
import pathfile
from commonclasses import *
from Player import *
from Ennemies import *
from pygame.locals import *
from Server import NetworkEngine
##########################################################IMPORTS########################################################################################################
#Size in pixels of the main menu's window :
MAIN_WINDOW_SIZE = 512

class RendererEngine:
	"""Any of Rendering element should be found in this class. """

	# Default Constructor:
	def __init__(self):
		self.ennemies: Ennemies
		self.players: [] # list of Players
		self.spriteManager: SpriteManager
		self.soundManager: MusicAndSoundManager
		self.physicEngine: PhysicEngine
		self.clientNetworkingThread: NetworkEngine.ClientNetworkingThread
		self.mainMenuOptionsSelections = [1, 0]
		self.currentGameState = "MENU"
		self.backGroundPos1 = 0

	# Initialization
	def initialization(self):
		# Initialization of pygame :
		pygame.init()
		# Set window to be size of 512 pixels
		self.mainWindow = pygame.display.set_mode((MAIN_WINDOW_SIZE, MAIN_WINDOW_SIZE))
		# Set pygame timer to tick every 16.67 ms <=> 60 FPS
		pygame.time.Clock().tick(60)

		#Load main menu back ground sprite
		self.mainMenuBG = pygame.image.load(pathfile.mainWindowBackGround).convert()
		self.mainMenuLogo = pygame.image.load(pathfile.mainWindowLogo).convert_alpha()

	# Set the Dependencies to the Renderer Engine
	def setDependencies(self, SpriteManager, SoundManager, PhysicEngine, Ennemies, Players):
		self.spriteManager = SpriteManager
		self.soundManager = SoundManager
		self.physicEngine = PhysicEngine
		self.ennemies = Ennemies
		self.players = Players
    
	# Set the current game state
	def setCurrentGameState(self, state):
		self.currentGameState = state

	# Render every game element present at the screen
	def renderAll(self):
		"""This function provides animation for each elements drawn on the screen. This function is typically called by the game loop."""
		#print("rendering game elements")

		if self.currentGameState == "MENU":
			self.drawMainMenu()
		
		elif self.currentGameState == "GAME_OVER":
			#Display a game over message :
			print("We are in game over mode.")
			#Change the music :
			#musicAndSoundManager.play("game_over")
			
		elif self.currentGameState == "SINGLE_PLAYER":
			#Animate the background :
			self.drawBackGround()

			#Update game state
			self.physicEngine.updateCurrentGameState()
			
			#By default, enable collision detection
			enablePhysicdetection = True

			#If first ennemies animation in not finished
			for eg_id in self.ennemies.ListofEnnemiesWave[self.ennemies.currentEnnemyWave]:
				eg = self.ennemies.ListofEnnemies[eg_id]
				if eg.endStartMove == False:
					enablePhysicdetection = False
			
			#Call the physic engine
			if enablePhysicdetection:
				self.physicEngine.simulateAllCollisions()

			#Check the game over status
			if self.players[0].health <= 0:
				self.currentGameState = "GAME_OVER"

			#Draw the player
			self.mainWindow.blit(self.spriteManager.ListofPlayerSurface[self.players[0].SpriteKey], (self.players[0].x, self.players[0].y))
			
			#For each ennemy group
			for eg_id,eg in self.ennemies.ListofEnnemies.items():
				for e in eg.ListofPositions:
					draw_ennemy = self.spriteManager.ListofEnnemiesSurface[eg.surface_id]
					
					#Convert orientation to degrees
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
				
					#Apply rotation before the final draw call
					if not angle == 0:
						draw_ennemy = self.spriteManager.rot_center(draw_ennemy,angle)
					
					#The Final draw call
					self.mainWindow.blit(draw_ennemy,(e[1],e[2]))
			
			#Draw the shots after drawing the ennemies. This way, the shots are overwritting the ennemies sprites/surface and lets the player knows what happen to the shot :
			for shot_id,shot in self.players[0].ListofFireShot.items():
				#Final draw call
				self.mainWindow.blit(self.spriteManager.ListofFireShotSurface[shot.type], (shot.x, shot.y))
			
			#Draw each ennemy with a rotation which is the same as the shot angle
			for eg_id,eg in self.ennemies.ListofEnnemies.items():
				for shot_id,shot in eg.ListofFireShot.items():
					draw_shot = self.spriteManager.ListofFireShotSurface[shot.type]
					
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
					draw_shot = self.spriteManager.rot_center(draw_shot,angle)
					
					#The final draw call :
					self.mainWindow.blit(draw_shot, (shot.x, shot.y))
			
			#Draw the explosions :
			self.makingExplosions()

			#Draw the health bar :
			self.updateHealthBarStatus()

			#Update the player score :
			self.updatePlayerScore()
			
			#Update the number of remaining shields :
			self.updatePlayerShield()

			#Draw player shield:
			self.drawPlayersShield()
		
		elif self.currentGameState == "MULTI_PLAYER":
			#First, get data from the client networking thread
			handleDataRcvdFromServer()

			#Animate the background
			self.drawBackGround()

			#Draw each player
			for player in self.players:
				self.mainWindow.blit(self.spriteManager.ListofPlayerSurface[player.SpriteKey], (player.x, player.y))

			#Draw the explosions :
			self.makingExplosions()

			"""#Draw the health bar :
			self.updateHealthBarStatus()

			#Update the player score :
			self.updatePlayerScore()
			
			#Update the number of remaining shields :
			self.updatePlayerShield()"""

			#Draw player shield:
			self.drawPlayersShield()
			
		#Finally, refresh the screen unless the cpu gets here before 16.67 ms has passed, then it'll not refresh the screen
		pygame.display.flip()

    # Handle data from server
	def handleDataRcvdFromServer(self):
		"""Process data received from a remote server """
		
		self.players[0] = self.clientNetworkingThread.inputCommands.player
		self.ennemies = self.clientNetworkingThread.inputCommands.ennemies
		self.physicEngine.listofExplosions = self.clientNetworkingThread.inputCommands.listOfExplosions

		for i in range (1, len(self.clientNetworkingThread.otherPlayers)):
			self.players[i] = self.clientNetworkingThread.inputCommands.otherPlayers[i]


	# Render Background
	def drawBackGround(self):
		"""Main background animation. It allows the background to be scrolled each time this function it's called."""

		#This is used to make the background scroll :
		#current_background_position_1 = 0
		current_background_position_2 = [0,0]
		backgroundPattern = random.choice([0,2,4,6])

		if self.ennemies.GAME_STATUS == "NORMAL":
			#The current position of the main game background and the position of the duplicate :
			self.backGroundPos1 += 2

			#Get the rect from the background in order to know and use the height :
			background_rect_1 = self.spriteManager.backGround1.get_rect()
			background_height_1 = background_rect_1.height
			
			#Scroll the background by 2 pixels:
			self.mainWindow.blit(self.spriteManager.backGround1,(0, self.backGroundPos1))
			self.mainWindow.blit(self.spriteManager.backGround1Copy,(0, self.backGroundPos1 - background_height_1))
			
			#If the background y position has reached the size of the screen, we reset the position :
			if self.backGroundPos1 == background_height_1:
				self.backGroundPos1 = 0
			
		elif self.ennemies.GAME_STATUS == "BOSS":
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
				
				self.mainWindow.blit(self.spriteManager.backGround2,(0,current_background_position_2[1]))
				self.mainWindow.blit(self.spriteManager.backGround2Copy,(0,MAIN_WINDOW_SIZE + current_background_position_2[1]))
			
				if current_background_position_2[1] == -MAIN_WINDOW_SIZE:
					current_background_position_2[1] = 0
				
			#elif backgroundPattern == 1:
			#	current_background_position_2[0] += 1
			#	current_background_position_2[1] -= 1
			elif backgroundPattern == 2:
				current_background_position_2[0] += 1
				current_background_position_2[1] += 0
				
				self.mainWindow.blit(self.spriteManager.backGround2,(current_background_position_2[0],0))
				self.mainWindow.blit(self.spriteManager.backGround2Copy,(-MAIN_WINDOW_SIZE + current_background_position_2[0],0))
			
				if current_background_position_2[0] == MAIN_WINDOW_SIZE:
					current_background_position_2[0] = 0
			
			#elif backgroundPattern == 3:
			#	current_background_position_2[0] += 1
			#	current_background_position_2[1] += 1
			
			elif backgroundPattern == 4:
				current_background_position_2[0] += 0
				current_background_position_2[1] += 1
				
				self.mainWindow.blit(self.spriteManager.backGround2,(0,current_background_position_2[1]))
				self.mainWindow.blit(self.spriteManager.backGround2Copy,(0,-MAIN_WINDOW_SIZE + current_background_position_2[1]))
			
				if current_background_position_2[1] == MAIN_WINDOW_SIZE:
					current_background_position_2[1] = 0
			
			#elif backgroundPattern == 5:
			#	current_background_position_2[0] -= 1
			#	current_background_position_2[1] += 1
			
			
			elif backgroundPattern == 6:
				current_background_position_2[0] -= 1
				current_background_position_2[1] += 0
				
				self.mainWindow.blit(self.spriteManager.backGround2,(current_background_position_2[0],0))
				self.mainWindow.blit(self.spriteManager.backGround2Copy,(MAIN_WINDOW_SIZE + current_background_position_2[0],0))
			
				if current_background_position_2[0] == -MAIN_WINDOW_SIZE:
					current_background_position_2[0] = 0
			
			#elif backgroundPattern == 7:
			#	current_background_position_2[0] -= 1
			#	current_background_position_2[1] -= 1

	# Update and Render the health bar
	def updateHealthBarStatus(self):
		"""Update the health bar status and draw it at the screen."""

		#First, draw the rect which is updated depending on the current player's health.
		x_health = (self.players[0].health/self.players[0].maxHealth) * 115
		if x_health < 0:
			x_health = 0
		health_bar_surface = pygame.Surface((int(x_health), 10))
		
		#Fill the surface partially depending on the player's health :
		health_bar_surface.fill((0,255,0))
		
		#Finaly, draw the health bar :
		self.mainWindow.blit(health_bar_surface, (512-130,20))
		self.mainWindow.blit(self.spriteManager.HealthBar, (512-150,15))

	# Update and Render the player score
	def updatePlayerScore(self):
		"""Update the player score."""

		#Draw the score :
		policeFont = self.spriteManager.ListofSysFonts["Times New Roman"]
		scoreSentence = "THE SCORE : " + str(self.players[0].score.playerScore)
		scoreSurface = policeFont.render(scoreSentence, 0, (0,255,0))
		self.mainWindow.blit(scoreSurface, (20,20))

	# Update and Render the player shield
	def updatePlayerShield(self):
		"""Update the number of shield which remain for the player"""
		
		#Draw the number of remaining shields
		policeFont = self.spriteManager.ListofSysFonts["Times New Roman"]
		shieldSentence = "REMAINING SHIELDS : " + str(self.players[0].nbTimesShieldAllowed)
		shieldSurface = policeFont.render(shieldSentence, 0, (0,255,0))
		self.mainWindow.blit(shieldSurface, (20,40))

	# Update and Render the player shield
	def drawPlayersShield(self):
		"""Draw the shield around the player."""
		shieldSurface = self.spriteManager.ListofExplosionSurface["bonusCircle"]

		for player in self.players:
			if player.timeBeforeShieldIsDeactivated > 0:
				#Draw the shield :
				self.mainWindow.blit(shieldSurface, (player.x - 16, player.y - 16))
	
	# Draw Main Menu
	def drawMainMenu(self):
		"""This function draw the main menu of the game"""
		self.mainWindow.blit(self.mainMenuBG, (0,0))
		self.mainWindow.blit(self.mainMenuLogo, (25,-10))
		self.drawMainMenuOptions()
		#self.drawMainMenuShip

	# Useless...
	def drawMainMenuLogo(self):
		"""This function provides animation of the main Logo displayed on the main window"""
		print("TODO Wtf is this function doing ??")

	# Draw the main menu options
	def drawMainMenuOptions(self):
		"""This function create each elements from the main window"""
		
		#Here we create the differents options :
		policeFont = self.spriteManager.ListofSysFonts["Times New Roman"]

		#Play game button :
		if self.mainMenuOptionsSelections == [1,0]:
			playGame = policeFont.render("Play Game",0,(255,0,0))
		elif self.mainMenuOptionsSelections == [0,1]:
			playGame = policeFont.render("Play Game",0,(255,255,255))
		self.mainWindow.blit(playGame,(70,200))

		#Exit game button :
		if self.mainMenuOptionsSelections == [1,0]:
			exitGame = policeFont.render("Exit Game",0,(255,255,255))
		elif self.mainMenuOptionsSelections == [0,1]:
			exitGame = policeFont.render("Exit Game",0,(255,0,0))
		self.mainWindow.blit(exitGame,(70,230))

		#Credits :
		creditsFont = self.spriteManager.ListofSysFonts["Arial"]
		creditsFont.set_italic(True)
		creditsText = "Space Shooter, v1.0.5, author : Yoshii_974, all right reserved.TM"
		creditsImg = creditsFont.render(creditsText,1,(255,255,0))
		self.mainWindow.blit(creditsImg,(200,495))

	# TODO: Cette fonction ne marche pas car elle redefinie a chaque boucle, un nouveau sprite et rect pour le ship !
	# Draw the main menu ship
	def drawMainMenuShip(self):
		"""The ship from the main menu"""
		
		#Choose randomly a ship to be showed
		randomKey = random.choice(self.spriteManager.ListofEnnemiesSurfaceKeys)
		shipSurface = self.spriteManager.ListofEnnemiesSurface[randomKey]
		shipRect = shipSurface.get_rect()

		#Define the position of the ship
		shipRect.x = 475
		shipRect.y = 350

		#ship = pygame.Surface((0,0))
		if (shipRect.x > 0):
			shipRect.x -= 4
		
		#Draw ship
		self.mainWindow.blit(shipSurface, shipRect)

	# Draw explosions
	def makingExplosions(self):
		"""This function is only useful for drawing and producing explosions objects at the right place, at the right time..."""
		
		#Loop on each explosions :
		for exp in self.physicEngine.listofExplosions:
			if exp.lifespan1 > 0:
				self.mainWindow.blit(self.spriteManager.ListofExplosionSurface["explosion1"],(exp.x,exp.y))
				#if exp.hasSoundBeenPlayed == 0:
				#self.soundManager.ListofExplosionSound["explosion1"].play()
					#exp.hasSoundBeenPlayed = 1
				#exp.lifespan1 -= 1
			elif exp.lifespan2 > 0:
				self.mainWindow.blit(self.spriteManager.ListofExplosionSurface["explosion2"],(exp.x,exp.y))
				#exp.lifespan2 -= 1