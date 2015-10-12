# -*- coding: utf-8 -*-

#########################################################################################################################################################################
### Date : 11 Août 2015																																					#
### Author : Yoshii_974																																					#
### Description : This file contains the logic for the behaviour of every ennemies included in the space shooter game.													#
#########################################################################################################################################################################
##########################################################GLOBAL VARIABLES###############################################################################################
MAIN_WINDOW_SIZE = 512
GAME_ELEMENT_ENNEMY_SIZE = 32
ENNEMY_GROUP_ID = 0
FIRE_RATE = 50
##########################################################IMPORTS########################################################################################################
import pathfile
import random
from commonclasses import *
import pygame
from pygame.locals import *
#########################################################################################################################################################################
class Ennemies:
	"""This class describes every ennemy used in the space shooter game."""
	
	#Default Constructor :
	def __init__(self):
		self.ListofEnnemies = {}
		self.ListofEnnemiesWave = {}
		self.currentGroupNumber = 0
		self.currentEnnemyNumber = 0
		self.currentEnnemyWave = 1
		self.SpriteManager = ""
		self.MusicAndSoundManager = ""
	
	#Initialize the ennemy class:
	def initialization(self):
		"""This function initialize each part of the class."""
		self.createEnnemyWave()
	
	#animate:
	def animate(self):
		"""This function animate each ennemy group inside the ListofEnnemies dictionary."""
		#TEST:
		for eg_id in self.ListofEnnemiesWave[self.currentEnnemyWave]:
			eg = self.ListofEnnemies[eg_id]
			if eg.endStartMove:
				eg.animate()
			else:
				eg.animateStart()

	#animate the fireshots:
	def animateFireShots(self):
		"""This function calls the animateFireShots() method of each group of ennmies."""
		for eg_id,eg in self.ListofEnnemies.items():
			eg.animateFireShots(4)
	
	#Triggers fireshots from the ennemy
	def fire(self):
		"""This function triggers fireshots from each ennemy group."""
		#loop on each ennemy group:
		for eg_id in self.ListofEnnemiesWave[self.currentEnnemyWave]:
			eg = self.ListofEnnemies[eg_id]
			if eg.endStartMove:
				eg.fire()
		
	#Destroy all fireshots from every group of ennemy:
	def destroyFireShots(self):
		"""This function calls the destroyFireShot() method of all group of ennemy."""
		for eg_id,eg in self.ListofEnnemies.items():
			eg.destroyFireShots()
	
	#Destroy all group of ennemies which contains no ennemy :
	def destroyGroupofEnnemy(self):
		"""This function is used to check which group of ennemy should be removed from the dictionary of ennemies."""
		ListofegToBeRemoved = []
		for eg_id,eg in self.ListofEnnemies.items():
			if eg.currentNumber == 0:
				ListofegToBeRemoved.append(eg_id)

		for eg_id in ListofegToBeRemoved:
			del self.ListofEnnemies[eg_id]
	
	#Create a wave of ennemy :
	def createEnnemyWave(self):
		"""This method create a group of ennemy and put it in a wave ennemy list."""
		#Wave 1:
		EnnemyWave1 = []
		EnnemyWave1.append(self.createEnnemyGroup(1,70,100))
		EnnemyWave1.append(self.createEnnemyGroup(2,140,200))
		self.ListofEnnemiesWave[1] = EnnemyWave1
		
		#Wave 2:
		EnnemyWave2 = []
		EnnemyWave2.append(self.createEnnemyGroup(2,100,200))
		EnnemyWave2.append(self.createEnnemyGroup(2,150,250))
		EnnemyWave2.append(self.createEnnemyGroup(2,200,300))
		self.ListofEnnemiesWave[2] = EnnemyWave2

		#Wave 3:
		EnnemyWave3 = []
		EnnemyWave3.append(self.createEnnemyGroup(2,70,40))
		EnnemyWave3.append(self.createEnnemyGroup(2,220,75))
		EnnemyWave3.append(self.createEnnemyGroup(2,160,105))
		EnnemyWave3.append(self.createEnnemyGroup(2,340,140))
		EnnemyWave3.append(self.createEnnemyGroup(2,20,175))
		self.ListofEnnemiesWave[3] = EnnemyWave3

		#Wave 4:
		EnnemyWave4 = []
		EnnemyWave4.append(self.createEnnemyGroup(1,40,70))
		EnnemyWave4.append(self.createEnnemyGroup(1,75,220))
		EnnemyWave4.append(self.createEnnemyGroup(1,105,160))
		EnnemyWave4.append(self.createEnnemyGroup(1,140,340))
		EnnemyWave4.append(self.createEnnemyGroup(1,175,20))
		self.ListofEnnemiesWave[4] = EnnemyWave4

	
	#Create ennemy group:
	def createEnnemyGroup(self,num,center_X,center_Y):
		"""This method creates a group of ennemy."""
		global ENNEMY_GROUP_ID
		
		#Create a specific group of ennemy :
		if num == 1:
			ennemy_group = Ennemy_Group_1(center_X,center_Y)
		elif num == 2:
			ennemy_group = Ennemy_Group_2(center_X,center_Y)
		
		#Set the attributes of the ennemy group:
		ennemy_group.surface_id = random.choice(self.SpriteManager.ListofEnnemiesSurfaceKeys)
		ennemy_group.center_x = center_X
		ennemy_group.center_y = center_Y
		ENNEMY_GROUP_ID += 1
		self.ListofEnnemies[ENNEMY_GROUP_ID] = ennemy_group
		self.currentGroupNumber += 1
		self.currentEnnemyNumber += ennemy_group.currentEnnemyNumber
		
		#Return this group of ennemy:
		return ENNEMY_GROUP_ID

	def updateEnnemiesWave(self):
		"""Update the current ennemy wave."""
		wave = self.ListofEnnemiesWave[self.currentEnnemyWave]
		e_sum = 0
		for eg_id in wave:
			eg = self.ListofEnnemies[eg_id]
			e_sum += eg.currentEnnemyNumber
		if e_sum == 0:
			self.currentEnnemyWave += 1


class Ennemy_Group:
	"""This class is the abstract class which defines anything a group of ennemies should have. This should not be instantiate !"""
	#Init
	#ListofPosition contains --->[['ennemy_id',ennemy_x,ennemy_y]]
	def __init__(self):
		self.ListofPositions = []
		self.ListofFireShot = {}
		self.center_x = 0
		self.center_y = 0
		self.center_dx = 0
		self.center_dy = 0
		self.currentEnnemyNumber = 0
		self.surface_id = ""
		self.fire_rate = FIRE_RATE
		self.shot_id = 0
		self.endStartMove = False

	#Initialization
	def initialization(self):
		"""Initialize everything."""
	
	
	#Animate
	def animate(self):
		""""""
	
	#Animate the fire shots if any
	def animateFireShots(self,direction):
		"""Move all fireshots from this ennemy group. The direction is used to define in which direction the fireshot are moving. Here is the diagramm:
		0
	7		1
6				2
	5		3
		4
"""
		
		#Move the fire shots :
		for shot_id,shot in self.ListofFireShot.items():
			if direction == 0:
				shot.y -= 4
			elif direction == 1:
				shot.x += 4
				shot.y -= 4
			elif direction == 2:
				shot.x += 4
			elif direction == 3:
				shot.x += 4
				shot.y += 4
			elif direction == 4:
				shot.y += 4
			elif direction == 5:
				shot.x -= 4
				shot.y += 4
			elif direction == 6:
				shot.x -= 4
			elif direction == 7:
				shot.x -= 4
				shot.y -= 4
	
	
	#Shoots laser
	def fire(self):
		"""This function triggers fire shots from each ennemy included in this group."""
		if self.fire_rate == 0:
			for e in self.ListofPositions:
				shot = FireShot(e[1],e[2],"fire1",self.shot_id,"player")
				self.ListofFireShot[self.shot_id] = shot
				self.shot_id += 1
			self.fire_rate = FIRE_RATE
		else:
			self.fire_rate -= 1
	
	#Destroy all fire shot which lifespan is equal to 0:
	def destroyFireShots(self):
		""""""
		listofFireShotToBeRemoved = []

		for shot_id,shot in self.ListofFireShot.items():
			if shot.lifespan == 0:
				listofFireShotToBeRemoved.append(shot_id)
			else:
				shot.lifespan -= 1

		for shot_id in listofFireShotToBeRemoved:
			del self.ListofFireShot[shot_id]



class Ennemy_Group_1(Ennemy_Group):
	"""This class describes the first group of ennemies."""
	
	#Init
	def __init__(self,center_X,center_Y):
		"""This group of ennemy consist of a single line of 3 verticaly aligned ennemies."""
		self.center_x = center_X
		self.center_y = center_Y
		self.center_dx = 0
		self.center_dy = 1
		self.ListofPositions = [['ennemy_1',self.center_x,-MAIN_WINDOW_SIZE],
					['ennemy_2',self.center_x,-MAIN_WINDOW_SIZE + GAME_ELEMENT_ENNEMY_SIZE + 3],
					['ennemy_3',self.center_x,-MAIN_WINDOW_SIZE + 2*GAME_ELEMENT_ENNEMY_SIZE + 3]]
		self.currentEnnemyNumber = 3
		self.ListofFireShot = {}
		self.fire_rate = FIRE_RATE * 3
		self.shot_id = 0
		self.endStartMove = False

	#Move the group of ennemy in a start wat :
	def animateStart(self):
		"""This method moves the group of ennemy for the beginning of the game."""
		for i,e in enumerate(self.ListofPositions):
			e[2] += 2
		if self.ListofPositions[0][2] == self.center_y:
			self.endStartMove = True
	
	#Move the group of ennemy in the usual way :
	def animate(self):
		""""""
		#set x and y of center group :
		self.center_y = self.center_y + self.center_dy

		#update each ennemy's position :
		for i,e in enumerate(self.ListofPositions):
			e_current_index = int(e[0][-1])
			e[2] = self.center_y + e_current_index*GAME_ELEMENT_ENNEMY_SIZE + 3
		
		#Once the y position reach a certain edge, we change the direction of the movement :
		if self.center_y == 350:
			self.center_dy = -1
		elif self.center_y == 50:
			self.center_dy = 1




class Ennemy_Group_2(Ennemy_Group):
	"""This class describes the second group of ennemies."""
	
	#Init
	def __init__(self,center_X,center_Y):
		"""This group of ennemy consist of a single line of 4 horizontally aligned ennemies."""
		self.center_x = center_X
		self.center_y = center_Y
		self.center_dx = 1
		self.center_dy = 0
		self.ListofPositions = [['ennemy_1',MAIN_WINDOW_SIZE,self.center_y],
					['ennemy_2',MAIN_WINDOW_SIZE + GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y],
					['ennemy_3',MAIN_WINDOW_SIZE + 2*GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y],
					['ennemy_4',MAIN_WINDOW_SIZE + 3*GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y]]
		self.currentEnnemyNumber = 4
		self.ListofFireShot = {}
		self.fire_rate = FIRE_RATE * 4
		self.shot_id = 0
		self.endStartMove = False
	
	#Move the group of ennemy in a specific way :
	def animateStart(self):
		"""This moves the group of ennemy for their arrival in the display screen."""
		for i,e in enumerate(self.ListofPositions):
			e[1] -= 2
		if self.ListofPositions[0][1] == self.center_x:
			self.endStartMove = True
	
	#Move the group the usual way:
	def animate(self):
		""""""
		#set x and y of center group :
		self.center_x = self.center_x + self.center_dx

		#update each ennemy's position :
		for i,e in enumerate(self.ListofPositions):
			e_current_index = int(e[0][-1])
			e[1] = self.center_x + e_current_index*GAME_ELEMENT_ENNEMY_SIZE + 3
			e[2] = self.center_y
		
		#Once the y position reach a certain edge, we change the direction of the movement :
		if self.center_x == 410:
			self.center_dx = -1
		elif self.center_x == 50:
			self.center_dx = 1
