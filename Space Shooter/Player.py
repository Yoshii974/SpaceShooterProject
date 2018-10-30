# -*- coding: utf-8 -*-

#########################################################################################################################################################################
### Date : 9 Août 2015																																					#
### Author : Yoshii_974																																					#
### Description : Ce fichier correspond à la classe "Player" contenant toutes les informations relatives aux données liées au joueur.									#
###	Contient, les animations du vaisseau, la position du vaisseau, le calcul de la physique des collisions avec le vaisseau, le score du joueur etc.					#
#########################################################################################################################################################################
import pathfile
from commonclasses import *
import pygame

########################################GLOBAL VARIABLES################################################################################################################
GAME_ELEMENT_PLAYER_SIZE = 50
GAME_ELEMENT_SIZE = 32
MAIN_WINDOW_SIZE = 512
SHOT_ID = 0
########################################################################################################################################################################
class Player:
	"""This class contains all the required information about the player, such as its position, the collision detection etc."""

	#Default constructor :
	def __init__(self):
		self.x = 0
		self.y = 0
		self.dx = 0
		self.dy = 0
		self.SpriteKey = ""
		self.SoundKey = ""
		self.ListofFireShot = {}
		self.SpriteManager = ""
		self.MusicAndSoundManager = ""
		self.touchedCounter = 0
		self.health = 100
		self.maxHealth = 100
		self.activateShield = 0
		self.currentWeapon = "fire1"
		self.nbTimesShieldAllowed = 3

	#Parametric Constructor :
	def __init__(self,X,Y):
		self.x = X
		self.y = Y
		self.dx = 0
		self.dy = 0	
		self.SpriteKey = ""
		self.SoundKey = ""
		self.ListofFireShot = {}
		self.SpriteManager = ""
		self.MusicAndSoundManager = ""
		self.touchedCounter = 0
		self.health = 100
		self.maxHealth = 100
		self.activateShield = 0
		self.currentWeapon = "fire1"
		self.nbTimesShieldAllowed = 3

	#Initialization :
	def initialization(self):
		"""This function initialize every part of the player object such as the loading of the image (convert to Surface), loading player sounds etc."""
	
	#Animates the player surface/sprite and also the fireshots :
	def animate(self):
		"""This function calculates the new position of the player. Also, indicates which sprite to be used for the next move of the player object."""
		#Move the player object to the new position:
		if self.x + self.dx >= 0 and self.x + self.dx <= MAIN_WINDOW_SIZE - GAME_ELEMENT_PLAYER_SIZE:
			self.x = self.x + self.dx
		if self.y + self.dy >= 0 and self.y + self.dy <= MAIN_WINDOW_SIZE - GAME_ELEMENT_PLAYER_SIZE:
			self.y = self.y + self.dy
		
		#Pick up the right sprite to be showned:
		if self.dx > 0:
			self.SpriteKey = "right"
		elif self.dx < 0:
			self.SpriteKey = "left"
		elif self.dx == 0:
			self.SpriteKey = "idle"

		#Move the fireshots if any :
		for shot_id, shot in self.ListofFireShot.items():
			shot.y = shot.y - 4

	#Set up and animate a fire shot :
	def fireShot(self):
		"""This function blablabla"""
		global SHOT_ID
		
		#Create a fire shot tuple :
		fireShot = FireShot(self.x,self.y,self.currentWeapon,SHOT_ID,"ennemy",0)

		#Insert the fire shot into the list of fire shot tuple :
		self.ListofFireShot[SHOT_ID] = fireShot

		#Increase the counter of fire shots:
		SHOT_ID = SHOT_ID + 1

	def destroyFireShots(self):
		""""""
		listofFireShotToBeRemoved = []
		
		for shot_id,shot in self.ListofFireShot.items():
			if shot.lifespan > 0:
				shot.lifespan -= 1
			else:
				listofFireShotToBeRemoved.append(shot_id)

		for shot_id in listofFireShotToBeRemoved:
			del self.ListofFireShot[shot_id]
