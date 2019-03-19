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
		self.ListofEnnemiesSurfaceKeys = []
		self.PlayerObject = ""
		self.GAME_STATUS = "NORMAL"
	
	#Initialize the ennemy class:
	def initialization(self):
		"""This function initialize each part of the class."""
		
		for j in range(0,7):
			for i in range(0,8):
				#The dictionnary key of the current sprite :
				key = "surface_" + str(j+1) + str(i+1)
				self.ListofEnnemiesSurfaceKeys.append(key)
		
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
			eg.animateFireShots()
	
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
		EnnemyWave1.append(self.createEnnemyGroup(1,140,200))
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

		#Wave 5:
		EnnemyWave5 = []
		EnnemyWave5.append(self.createEnnemyGroup(3,50,70))
		self.ListofEnnemiesWave[5] = EnnemyWave5
		
		#Final Wave :
		EnnemyWave6 = []
		EnnemyWave6.append(self.createBoss(120,180)) #240,126
		self.ListofEnnemiesWave[6] = EnnemyWave6
		
	#Create ennemy group:
	def createEnnemyGroup(self,num,center_X,center_Y):
		"""This method creates a group of ennemy."""
		global ENNEMY_GROUP_ID
		
		#Create a specific group of ennemy :
		if num == 1:
			ennemy_group = Ennemy_Group_1(center_X,center_Y)
		elif num == 2:
			ennemy_group = Ennemy_Group_2(center_X,center_Y)
		elif num == 3:
			ennemy_group = Ennemy_Group_3(center_X,center_Y)
		
		#Set the attributes of the ennemy group:
		ennemy_group.surface_id = random.choice(self.ListofEnnemiesSurfaceKeys)
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
			
			#Check if we are at the end of the game :
			if eg.TYPE == "BOSS":
				self.GAME_STATUS = "BOSS"
			
			e_sum += eg.currentEnnemyNumber
			
		if e_sum == 0:
			self.currentEnnemyWave += 1
		
	def createBoss(self,center_X,center_Y):
		"""Create the Boss of the game."""
		global ENNEMY_GROUP_ID
		
		#Create the Boss :
		boss = Boss(center_X,center_Y)
		boss.PlayerObject = self.PlayerObject
		
		#Set the attributes of the Boss :
		boss.surface_id = "boss"
		ENNEMY_GROUP_ID += 1
		self.ListofEnnemies[ENNEMY_GROUP_ID] = boss
		self.currentGroupNumber += 1
		self.currentEnnemyNumber += 1
		
		#Return the ID of the Boss :
		return ENNEMY_GROUP_ID



class Ennemy_Group:
	"""This class is the abstract class which defines anything a group of ennemies should have. This should not be instantiate !"""
	#Init
	#ListofPosition contains --->[['ennemy_id',ennemy_x,ennemy_y],ennemy_orientation]
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
		self.fire_rate_group = FIRE_RATE
		self.shot_id = 0
		self.endStartMove = False
		self.TYPE = "ENNEMY_WAVE"

	#Initialization
	def initialization(self):
		"""Initialize everything."""
	
	
	#Animate
	def animate(self):
		""""""
	
	#Animate the fire shots if any
	def animateFireShots(self):
		"""Move all fireshots from this ennemy group. The direction is used to define in which direction the fireshots are moving. Here is the diagramm:
		0
	7		1
6				2
	5		3
		4
"""
		
		#Move the fire shots :
		for shot_id,shot in self.ListofFireShot.items():
			if shot.orientation == 0:
				shot.y -= 2
			elif shot.orientation == 1:
				shot.x += 2
				shot.y -= 2
			elif shot.orientation == 2:
				shot.x += 2
			elif shot.orientation == 3:
				shot.x += 2
				shot.y += 2
			elif shot.orientation == 4:
				shot.y += 2
			elif shot.orientation == 5:
				shot.x -= 2
				shot.y += 2
			elif shot.orientation == 6:
				shot.x -= 2
			elif shot.orientation == 7:
				shot.x -= 2
				shot.y -= 2
	
	
	#Shoots laser
	def fire(self):
		"""This function triggers fire shots from each ennemy included in this group."""
		if self.fire_rate == 0:
			for e in self.ListofPositions:
				shot = FireShot(e[1],e[2],"fire1",self.shot_id,"player",4)
				self.ListofFireShot[self.shot_id] = shot
				self.shot_id += 1
			self.fire_rate = self.fire_rate_group
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
		self.ListofPositions = [['ennemy_1',self.center_x,-MAIN_WINDOW_SIZE,0],
					['ennemy_2',self.center_x,-MAIN_WINDOW_SIZE + GAME_ELEMENT_ENNEMY_SIZE + 3,0],
					['ennemy_3',self.center_x,-MAIN_WINDOW_SIZE + 2*GAME_ELEMENT_ENNEMY_SIZE + 3,0]]
		self.currentEnnemyNumber = 3
		self.ListofFireShot = {}
		self.fire_rate = FIRE_RATE
		self.fire_rate_group = FIRE_RATE * 3
		self.shot_id = 0
		self.endStartMove = False
		self.TYPE = "ENNEMY_WAVE"

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
		self.ListofPositions = [['ennemy_1',MAIN_WINDOW_SIZE,self.center_y,0],
					['ennemy_2',MAIN_WINDOW_SIZE + GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y,0],
					['ennemy_3',MAIN_WINDOW_SIZE + 2*GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y,0],
					['ennemy_4',MAIN_WINDOW_SIZE + 3*GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y,0]]
		self.currentEnnemyNumber = 4
		self.ListofFireShot = {}
		self.fire_rate = FIRE_RATE
		self.fire_rate_group = FIRE_RATE * 4
		self.shot_id = 0
		self.endStartMove = False
		self.TYPE = "ENNEMY_WAVE"
	
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
			#e[2] = self.center_y
		
		#Once the y position reach a certain edge, we change the direction of the movement :
		if self.center_x == 410:
			self.center_dx = -1
		elif self.center_x == 50:
			self.center_dx = 1

			
			
			
class Ennemy_Group_3(Ennemy_Group):
	"""This ennemy group contains ennemies which are able to shoots with a predefine rotation."""
	
	#Init
	def __init__(self,center_X,center_Y):
		"""This group of ennemy consist of a 4 ennemies. The first one is on the left, the second one is at the top, the third one is on the right and the last one is at the bottom."""
		self.center_x = center_X
		self.center_y = center_Y
		self.center_dx = 1
		self.center_dy = 0
		self.ListofPositions = [['ennemy_1',MAIN_WINDOW_SIZE,self.center_y,0],
					['ennemy_2',MAIN_WINDOW_SIZE + GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y + GAME_ELEMENT_ENNEMY_SIZE + 3,1],
					['ennemy_3',MAIN_WINDOW_SIZE + 2*GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y,2],
					['ennemy_4',MAIN_WINDOW_SIZE + GAME_ELEMENT_ENNEMY_SIZE + 3,self.center_y - GAME_ELEMENT_ENNEMY_SIZE + 3,3]]
		self.currentEnnemyNumber = 4
		self.ListofFireShot = {}
		self.fire_rate = FIRE_RATE
		self.fire_rate_group = FIRE_RATE * 8
		self.shot_id = 0
		self.endStartMove = False
		self.orientation_counter_ennemy_1 = 0
		self.orientation_counter_ennemy_2 = 1
		self.orientation_counter_ennemy_3 = 2
		self.orientation_counter_ennemy_4 = 3
		self.TYPE = "ENNEMY_WAVE"
	
	#Move the group of ennemy in a specific way :
	def animateStart(self):
		"""This moves the group of ennemy for their arrival in the display screen."""
		for i,e in enumerate(self.ListofPositions):
			e[1] -= 2
		if self.ListofPositions[0][1] == self.center_x:
			self.endStartMove = True
	
	#Move the group the usual way:
	#def animate(self):
	#	""""""
	#	#set x and y of center group :
	#	self.center_x = self.center_x + self.center_dx

	#	#update each ennemy's position :
	#	for i,e in enumerate(self.ListofPositions):
	#		e_current_index = int(e[0][-1])
	#		if i == 3:
	#			e[1] = self.center_x + 2*GAME_ELEMENT_ENNEMY_SIZE + 3
	#		else:
	#			e[1] = self.center_x + e_current_index*GAME_ELEMENT_ENNEMY_SIZE + 3
			
		
	#	#Once the y position reach a certain edge, we change the direction of the movement :
	#	if self.center_x == 410:
	#		self.center_dx = -1
	#	elif self.center_x == 50:
	#		self.center_dx = 1
	
	#Shoots laser
	def fire(self):
		"""This function triggers fire shots from each ennemy included in this group."""
		if self.fire_rate == 0:
			for e in self.ListofPositions:
				e_current_index = int(e[0][-1])
				
				if e_current_index == 1:
					#Convert orientation to angle :
					e[3] = self.orientation_counter_ennemy_1%8
					shot = FireShot(e[1],e[2],"fire2",self.shot_id,"player",e[3])
					self.orientation_counter_ennemy_1 += 1
				elif e_current_index == 2:
					#Convert orientation to angle :
					e[3] = self.orientation_counter_ennemy_2%8
					shot = FireShot(e[1],e[2],"fire2",self.shot_id,"player",e[3])
					self.orientation_counter_ennemy_2 += 1
				elif e_current_index == 3:
					#Convert orientation to angle :
					e[3] = self.orientation_counter_ennemy_3%8
					shot = FireShot(e[1],e[2],"fire2",self.shot_id,"player",e[3])
					self.orientation_counter_ennemy_3 += 1
				elif e_current_index == 4:
					#Convert orientation to angle :
					e[3] = self.orientation_counter_ennemy_4%8
					shot = FireShot(e[1],e[2],"fire2",self.shot_id,"player",e[3])
					self.orientation_counter_ennemy_4 += 1
				
				self.ListofFireShot[self.shot_id] = shot
				self.shot_id += 1
			
			self.fire_rate = self.fire_rate_group
		
		else:
			self.fire_rate -= 1
			
			
			
class Boss(Ennemy_Group):
	"""This class describe the Boss of the game."""
	#Default Constructor:
	def __init__(self,center_X,center_Y):
		self.center_x = center_X
		self.center_y = center_Y
		self.center_dx = 0
		self.center_dy = 0
		self.ListofPositions = [['ennemy_1',self.center_x,-MAIN_WINDOW_SIZE,0]]
		self.currentEnnemyNumber = 1
		self.ListofFireShot = {}
		self.fire_rate = FIRE_RATE
		self.fire_rate_group = FIRE_RATE * 3
		self.shot_id = 0
		self.endStartMove = False
		self.mouvementCountDown = 0
		self.mouvementPattern = "SQUARE"
		self.firePattern = 0
		self.fireCountDown = 0
		self.PlayerObject = ""
		self.SQUARECountDown = 0
		self.TYPE = "BOSS"
	
	#Move the boss in a specific way :
	def animateStart(self):
		"""This moves the boss for its arrival in the display screen."""
		for i,e in enumerate(self.ListofPositions):
			e[2] += 2 #The boss come from the top
		if self.ListofPositions[0][2] == self.center_y:
			self.endStartMove = True
	
	def animate(self):
		"""Here is defined the movement of the Boss"""
		#Mouvment pattern of the boss : SQUARE
		if self.mouvementPattern == "SQUARE":
			if self.SQUARECountDown >= 0 and self.SQUARECountDown < 100:
				self.center_dx = 1
				self.center_dy = 0
				self.SQUARECountDown += 1
			elif self.SQUARECountDown >= 100 and self.SQUARECountDown < 200:
				self.center_dx = 0
				self.center_dy = -1
				self.SQUARECountDown += 1
			elif self.SQUARECountDown >= 200 and self.SQUARECountDown < 300:
				self.center_dx = -1
				self.center_dy = 0
				self.SQUARECountDown += 1
			elif self.SQUARECountDown >= 300 and self.SQUARECountDown < 400:
				self.center_dx = 0
				self.center_dy = 1
				self.SQUARECountDown += 1
				if self.SQUARECountDown == 400:
					self.SQUARECountDown = 0
				
			#Increase the Pattern Countdown :
			self.mouvementCountDown += 1
			
			#If the countdown has reached its maximum :
			if self.mouvementCountDown == 4000:#40
				self.mouvementPattern = "PLAYER_RUSH"
				self.mouvementCountDown = 0
		
		#Mouvement pattern of the boss : RUSHING TO THE PLAYER
		elif self.mouvementPattern == "PLAYER_RUSH":
			#Knows the current player's positions, mark a point at these coordinates and then go straight to that point :
			#Change dx and dy depending on player's positions :
			if self.center_x > self.PlayerObject.x:
				self.center_dx = -2
			if self.center_x <= self.PlayerObject.x:
				self.center_dx = +2
			if self.center_y > self.PlayerObject.y:
				self.center_dy = -2
			if self.center_y <= self.PlayerObject.y:
				self.center_dy = +2
			
			#Increase the countdown :
			self.mouvementCountDown += 1
			
			#If the countdown has reached its maximum :
			if self.mouvementCountDown == 150:
				self.mouvementPattern = "SQUARE"
				self.mouvementCountDown = 0
				
				#The Boss reappears at a random position :
				self.center_x = random.randrange(20,130)#120
				self.center_y = random.randrange(60,200)#180
				

		#Set the center X :
		self.center_x = self.center_x + self.center_dx
		self.center_y = self.center_y + self.center_dy
		
		#update the boss position :
		for i,e in enumerate(self.ListofPositions):
			e_current_index = int(e[0][-1])
			e[1] = self.center_x
			e[2] = self.center_y
			
	#Shoots laser
	def fire(self):
		"""This function triggers fire shots from each ennemy included in this group."""
		if self.fire_rate == 0 and self.firePattern == 0:
			#This mode allows the boss to shoot 4 lasers in different directions and with different angle :
			shot1 = FireShot(self.center_x,self.center_y,"fire2",self.shot_id,"player",4)
			shot2 = FireShot(self.center_x,self.center_y + 132,"fire3",self.shot_id,"player",5)
			shot3 = FireShot(self.center_x + 113,self.center_y + 132,"fire3",self.shot_id,"player",3)
			shot4 = FireShot(self.center_x + 113,self.center_y,"fire2",self.shot_id,"player",4)
			
			#Adds the shots to the FireShot List :
			self.ListofFireShot[self.shot_id] = shot1
			self.shot_id += 1
			self.ListofFireShot[self.shot_id] = shot2
			self.shot_id += 1
			self.ListofFireShot[self.shot_id] = shot3
			self.shot_id += 1
			self.ListofFireShot[self.shot_id] = shot4
			self.shot_id += 1
			
			#Reset the Fire rate :
			self.fire_rate = self.fire_rate_group
			self.fireCountDown += 1
			
			#This lets us know when it should change its fire mode :
			if self.fireCountDown == 15:
				self.firePattern = 1
				self.fireCountDown = 0
		
		elif self.fire_rate == 0 and self.firePattern == 1:
			#In this mode, the boss shoots many laser really fast and in a single direction :
			shot1 = FireShot(self.center_x + 90,self.center_y + 15,"fire3",self.shot_id,"player",4)
			
			#Adds the shots to the FireShot List :
			self.ListofFireShot[self.shot_id] = shot1
			self.shot_id += 1
			
			#Reset the Fire rate :
			self.fire_rate = 12#self.fire_rate_group / 6
			self.fireCountDown += 1
			
			#Reset countdown :
			if self.fireCountDown == 60:
				self.firePattern = 0
				self.fireCountDown = 0
			
		else:
			self.fire_rate -= 1