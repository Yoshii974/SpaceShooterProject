# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 21 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains every Rendering Logic for the game. 																							    #
#########################################################################################################################################################################
from commonclasses import *
from Player import *
from Ennemies import *
import pygame
from pygame.locals import *
##########################################################IMPORTS########################################################################################################
#Size in pixels of the main menu's window :
MAIN_WINDOW_SIZE = 512



class RendererEngine:
	"""Any of Rendering element should be found in this class. """

	#Default Constructor:
	def __init__(self):
		self.ennemies: Ennemies
		self.player: Player
		self.score: Score
		self.listofExplosions: []
		self.gameMode: str
		self.spriteManager: SpriteManager
		self.mainWindow = pygame.display.set_mode((MAIN_WINDOW_SIZE, MAIN_WINDOW_SIZE))

	# Set the Dependencies to the Renderer Engine
	def setDependencies(self, SpriteManager, Ennemies, Player, Score, ListofExplosions):
		self.spriteManager = SpriteManager
		self.ennemies = Ennemies
		self.player = Player
		self.score = Score
		self.listofExplosions = ListofExplosions
    
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
			background_rect_1 = self.backGround1.get_rect()
			background_height_1 = background_rect_1.height
			
			#Scroll the background by 2 pixels:
			self.mainWindow.blit(self.backGround1,(0,current_background_position_1))
			self.mainWindow.blit(self.backGround1Copy,(0,current_background_position_1 - background_height_1))
			
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
				
				self.mainWindow.blit(self.backGround2,(0,current_background_position_2[1]))
				self.mainWindow.blit(self.backGround2Copy,(0,MAIN_WINDOW_SIZE + current_background_position_2[1]))
			
				if current_background_position_2[1] == -MAIN_WINDOW_SIZE:
					current_background_position_2[1] = 0
				
			#elif backgroundPattern == 1:
			#	current_background_position_2[0] += 1
			#	current_background_position_2[1] -= 1
			elif backgroundPattern == 2:
				current_background_position_2[0] += 1
				current_background_position_2[1] += 0
				
				self.mainWindow.blit(self.backGround2,(current_background_position_2[0],0))
				self.mainWindow.blit(self.backGround2Copy,(-MAIN_WINDOW_SIZE + current_background_position_2[0],0))
			
				if current_background_position_2[0] == MAIN_WINDOW_SIZE:
					current_background_position_2[0] = 0
			
			#elif backgroundPattern == 3:
			#	current_background_position_2[0] += 1
			#	current_background_position_2[1] += 1
			
			elif backgroundPattern == 4:
				current_background_position_2[0] += 0
				current_background_position_2[1] += 1
				
				self.mainWindow.blit(self.backGround2,(0,current_background_position_2[1]))
				self.mainWindow.blit(self.backGround2Copy,(0,-MAIN_WINDOW_SIZE + current_background_position_2[1]))
			
				if current_background_position_2[1] == MAIN_WINDOW_SIZE:
					current_background_position_2[1] = 0
			
			#elif backgroundPattern == 5:
			#	current_background_position_2[0] -= 1
			#	current_background_position_2[1] += 1
			
			
			elif backgroundPattern == 6:
				current_background_position_2[0] -= 1
				current_background_position_2[1] += 0
				
				self.mainWindow.blit(self.backGround2,(current_background_position_2[0],0))
				self.mainWindow.blit(self.backGround2Copy,(MAIN_WINDOW_SIZE + current_background_position_2[0],0))
			
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