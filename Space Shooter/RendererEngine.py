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
		self.mainWindow = pygame.display.set_mode((MAIN_WINDOW_SIZE, MAIN_WINDOW_SIZE))
		#The background of the game :
		self.backGround1 = pygame.image.load(pathfile.mainGameBackGround1)
		self.backGround1Copy = pygame.image.load(pathfile.mainGameBackGround1)
		self.backGround2 = pygame.image.load(pathfile.mainGameBackGround2)
		self.backGround2Copy = pygame.image.load(pathfile.mainGameBackGround2)

	# Set the Dependencies to the Renderer Engine
	def setDependencies(self, Ennemies, Player, Score, ListofExplosions):
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