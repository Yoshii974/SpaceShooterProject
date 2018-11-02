# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 21 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains every Rendering Logic for the game. 																							    #
#########################################################################################################################################################################
import pygame
import PhysicEngine
from commonclasses import *
from Player import *
from Ennemies import *
from pygame.locals import *
##########################################################IMPORTS########################################################################################################
#Size in pixels of the main menu's window :
MAIN_WINDOW_SIZE = 512

class RendererEngine:
	"""Any of Rendering element should be found in this class. """

	# Default Constructor:
	def __init__(self):
		self.ennemies: Ennemies
		self.player: Player
		self.score: Score
		self.gameMode: str
		self.spriteManager: SpriteManager
		self.soundManager: MusicAndSoundManager
		self.physicEngine: PhysicEngine
		self.mainMenuOptionsSelections = [1, 0]
		self.mainWindow = pygame.display.set_mode((MAIN_WINDOW_SIZE, MAIN_WINDOW_SIZE))

	# Set the Dependencies to the Renderer Engine
	def setDependencies(self, SpriteManager, SoundManager, PhysicEngine, Ennemies, Player, Score):
		self.spriteManager = SpriteManager
		self.soundManager = SoundManager
		self.physicEngine = PhysicEngine
		self.ennemies = Ennemies
		self.player = Player
		self.score = Score
    
	# Render every game element present at the screen
	def renderAllGameElement(self):
		print("rendering game elements")
    
	# Render Background
	def mainGameBackGroundAnimationRenderer(self):
		"""Main background animation. It allows the background to be scrolled each time this function it's called."""

		#This is used to make the background scroll :
		current_background_position_1 = 0
		current_background_position_2 = [0,0]
		backgroundPattern = random.choice([0,2,4,6])

		if self.ennemies.GAME_STATUS == "NORMAL":
			#The current position of the main game background and the position of the duplicate :
			current_background_position_1 += 2

			#Get the rect from the background in order to know and use the height :
			background_rect_1 = self.spriteManager.backGround1.get_rect()
			background_height_1 = background_rect_1.height
			
			#Scroll the background by 2 pixels:
			self.mainWindow.blit(self.spriteManager.backGround1,(0,current_background_position_1))
			self.mainWindow.blit(self.spriteManager.backGround1Copy,(0,current_background_position_1 - background_height_1))
			
			#If the background y position has reached the size of the screen, we reset the position :
			if current_background_position_1 == background_height_1:
				current_background_position_1 = 0
			
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
		x_health = (self.player.health/self.player.maxHealth) * 115
		if x_health < 0:
			x_health = 0
		health_bar_surface = pygame.Surface((int(x_health),10))
		
		#Fill the surface partially depending on the player's health :
		health_bar_surface.fill((0,255,0))
		
		#Finaly, draw the health bar :
		self.mainWindow.blit(health_bar_surface,(512-130,20))
		self.mainWindow.blit(self.spriteManager.HealthBar,(512-150,15))

	# Update and Render the player score
	def updatePlayerScore(self):
		"""Update the player score."""

		#Draw the score :
		policeFont = self.spriteManager.ListofSysFonts["Times New Roman"]
		scoreSentence = "THE SCORE : " + str(self.score.playerScore)
		scoreSurface = policeFont.render(scoreSentence,0,(0,255,0))
		self.mainWindow.blit(scoreSurface,(20,20))

	# Update and Render the player shield
	def updatePlayerShield(self):
		"""Update the number of shield which remain for the player"""
		
		#Draw the number of remaining shields
		policeFont = self.spriteManager.ListofSysFonts["Times New Roman"]
		shieldSentence = "REMAINING SHIELDS : " + str(self.player.nbTimesShieldAllowed)
		shieldSurface = policeFont.render(shieldSentence,0,(0,255,0))
		self.mainWindow.blit(shieldSurface,(20,40))

	# Update and Render the player shield
	def drawPlayerShield(self):
		"""Draw the shield around the player."""
		
		#Draw the shield :
		shieldSurface = self.spriteManager.ListofExplosionSurface["bonusCircle"]
		self.mainWindow.blit(shieldSurface,(self.player.x - 16, self.player.y - 16))
		self.player.activateShield -= 1
	
	# Useless...
	def mainWindowLogoAnimation(self):
		"""This function provides animation of the main Logo displayed on the main window"""
		print("TODO Wtf is this function doing ??")

	# Draw the main menu options
	def mainWindowOptionsRenderer(self):
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

	# TODO: A Revoir !
	#Animate and Draw a randow ennemy space shuttle at the main menu
	def mainWindowSpaceShuttle(self):
		"""This function provides a spacecraft to be animated from time to time. This function does not deal with the animation of the spaceshuttle. It only gives which one to choose in the list of all spaceshuttle available."""
		global animatedSpaceShuttle
		global animatedSpaceShuttleRect
		global spriteManager

		#Choose randomly a ship to be showed
		randomKey = random.choice(self.spriteManager.ListofEnnemiesSurfaceKeys)
		animatedSpaceShuttle = self.spriteManager.ListofEnnemiesSurface[randomKey]

		#Define the position of the ship
		animatedSpaceShuttleRect.x = 475
		animatedSpaceShuttleRect.y = 350

	# TODO: A Revoir !
	def mainWindowSpaceShuttleAnimation(self):
		"""Calculate the new position of the animated ship. Return True if the position is still positif, false otherwise"""
		global animatedSpaceShuttleRect

		#Move the ship per 4 pixels throught the window
		if animatedSpaceShuttleRect.x > 0:
			animatedSpaceShuttleRect = animatedSpaceShuttleRect.move(-4,0)
			return True
		else:
			return False
	
	# Draw explosions
	def makingExplosions(self):
		"""This function is only useful for drawing and producing explosions objects at the right place, at the right time..."""

		#Contains each explosions which has their lifespan 1 and 2 equals to 0, it's time to remove this explosion object :
		listofExplosionsToBeRemoved = []
		
		#Loop on each explosions :
		for exp in self.physicEngine.listofExplosions:
			if exp.lifespan1 > 0:
				self.mainWindow.blit(self.spriteManager.ListofExplosionSurface["explosion1"],(exp.x,exp.y))
				if exp.hasSoundBeenPlayed == 0:
					self.soundManager.ListofExplosionSound["explosion1"].play()
					exp.hasSoundBeenPlayed = 1
				exp.lifespan1 -= 1
			elif exp.lifespan2 > 0:
				self.mainWindow.blit(self.spriteManager.ListofExplosionSurface["explosion2"],(exp.x,exp.y))
				exp.lifespan2 -= 1
			else:
				listofExplosionsToBeRemoved.append(exp)

		#We delete every explosions which has no longer any reason to stay alive:
		for exp in listofExplosionsToBeRemoved:
			self.physicEngine.listofExplosions.remove(exp)