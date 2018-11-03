# -*- coding: utf-8 -*-

#########################################################################################################################################################################
### Date : 13 Août 2015																																					#
### Author : Yoshii_974																																					#
### Description : This file contains common used classes. Every classes here may be called by each other python files included in the space shooter game.				#
#########################################################################################################################################################################
##########################################IMPORTS########################################################################################################################
import pathfile
import pygame
##########################################GLOBAL VARIABLES###############################################################################################################
GAME_ELEMENT_SIZE = 32
GAME_ELEMENT_PLAYER_SIZE = 50
##########################################CLASSES########################################################################################################################
class SpriteManager():
	"""This class handle every sprite part of the game..."""

	#Default Constructor:
	def __init__(self):
		"""This is the default constructor."""
		self.ListofPlayerSurface = {}
		self.ListofEnnemiesSurface = {}
		self.ListofFireShotSurface = {}
		self.ListofExplosionSurface = {}
		self.ListofEnnemiesSurfaceKeys = []
		self.ListofSysFonts = {}
		self.HealthBar = ""
		self.Boss = ""

	#loads Sprites:
	def initialization(self):
		""""""
		self.loadMainGameBackGrounds()
		self.loadPlayerSprites()
		self.loadEnnemiesSprites()
		self.loadFireShotSprites()
		self.loadExplosionSprites()
		self.loadHealthBarSprites()
		self.loadBossSprites()
		self.loadSysFonts()

	#Main Game BackGround
	def loadMainGameBackGrounds(self):
		"""This function loads the main game backgrounds."""
		#The background of the game :
		self.backGround1 = pygame.image.load(pathfile.mainGameBackGround1)
		self.backGround1Copy = pygame.image.load(pathfile.mainGameBackGround1)
		self.backGround2 = pygame.image.load(pathfile.mainGameBackGround2)
		self.backGround2Copy = pygame.image.load(pathfile.mainGameBackGround2)

	#Player's Sprites:
	#Initialization of all animations of the player's space shuttle :
	def loadPlayerSprites(self):
		"""This function loads the differents sprites used by the player."""
		#Fullfill the list of player's Surfaces
		player_left_surface = pygame.image.load(pathfile.mainGameShuttlesPlayerLeft).convert_alpha()
		player_right_surface = pygame.image.load(pathfile.mainGameShuttlesPlayerRight).convert_alpha()
	
		tmpSurfaceListLeft = []
		tmpSurfaceListRight = []
		for i in range(0,3):
			tmpSurfaceLeft = player_left_surface.subsurface(i*GAME_ELEMENT_PLAYER_SIZE,0,GAME_ELEMENT_PLAYER_SIZE-1,GAME_ELEMENT_PLAYER_SIZE-1)
			tmpSurfaceListLeft.append(tmpSurfaceLeft)

		for j in range(1,3):
			tmpSurfaceRight = player_right_surface.subsurface(j*GAME_ELEMENT_PLAYER_SIZE,0,GAME_ELEMENT_PLAYER_SIZE-1,GAME_ELEMENT_PLAYER_SIZE-1)
			tmpSurfaceListRight.append(tmpSurfaceRight)

		#Insert the previous surfaces into the dictionnary :
		self.ListofPlayerSurface["left"] = tmpSurfaceListLeft[0]
		self.ListofPlayerSurface["idle"] = tmpSurfaceListLeft[2]
		self.ListofPlayerSurface["right"] = tmpSurfaceListRight[1]	
		
	
	#Ennemies's Sprites:
	def loadEnnemiesSprites(self):
		"""This function loads every part of the ennemies animation. It also provides loading of the sprite used in the game."""	
		#Load the sprites that contains every ennemy spaceshuttle of the game :
		ennemies_surface = pygame.image.load(pathfile.mainGameShuttlesEnnemies).convert_alpha()

		#Each sprites is taken as a picture and put in the list of sprites
		for j in range(0,7):
			for i in range(0,8):
				#The dictionnary key of the current sprite :
				key = "surface_" + str(j+1) + str(i+1)
				ennemySurface = ennemies_surface.subsurface((i*GAME_ELEMENT_SIZE,j*GAME_ELEMENT_SIZE),(GAME_ELEMENT_SIZE-1,GAME_ELEMENT_SIZE-1))
				#Rotate the sprite to 90 degres :
				ennemySurface = self.rot_center(ennemySurface,90)
				
				#Add the sprite to the dictionnary :
				self.ListofEnnemiesSurfaceKeys.append(key)
				self.ListofEnnemiesSurface[key] = ennemySurface	
	
	#FireShot's Sprites:
	def loadFireShotSprites(self):
		#Load the fires sprites:
		fire_shot_surface = pygame.image.load(pathfile.mainGameFire).convert_alpha()
		
		#Insert fire into dictionnary of Surface
		for i in range(0,3):
			key = "fire" + str(i+1)
			tmpSurfaceFire = fire_shot_surface.subsurface(i*GAME_ELEMENT_SIZE,0,GAME_ELEMENT_SIZE-1,GAME_ELEMENT_SIZE-1)
			tmpSurfaceFireRotate = self.rot_center(tmpSurfaceFire,-90)
			self.ListofFireShotSurface[key] = tmpSurfaceFireRotate


	#Explosion's Sprites:
	def loadExplosionSprites(self):
		#Load the explosions sprites:
		explosion_surface = pygame.image.load(pathfile.mainGameExplosions).convert_alpha()
		shield_surface = pygame.image.load(pathfile.mainGameShield).convert_alpha()
		
		#This one is for the animation showned when player collide with bonus:
		self.ListofExplosionSurface["bonusCircle"] = shield_surface#explosion_surface.subsurface(0,0,GAME_ELEMENT_SIZE-1,GAME_ELEMENT_SIZE-1)

		#Insert explosions into dictionnary of Surface
		for i in range(1,3):
			key = "explosion" + str(i)
			tmpSurfaceExplosion = explosion_surface.subsurface(i*GAME_ELEMENT_SIZE,0,GAME_ELEMENT_SIZE-1,GAME_ELEMENT_SIZE-1)
			self.ListofExplosionSurface[key] = tmpSurfaceExplosion

	#Health Bar's Sprites:
	def loadHealthBarSprites(self):
		"""Load the health bar of the game used by the player."""
		#The special rect for the surface of the health bar:
		self.HealthBar = pygame.image.load(pathfile.mainGameHealthBar).convert_alpha()
	
	#Load the system fonts to be used by the game :
	def loadSysFonts(self):
		"""Load every useful system fonts to be used in the game This way, all this fonts are load only once and not each time the game loop begin again."""
		self.ListofSysFonts["Times New Roman"] = pygame.font.SysFont("Times New Roman",16)
		self.ListofSysFonts["Arial"] = pygame.font.SysFont("Arial",12)
		
	#The Boss's Sprite :
	def loadBossSprites(self):
		"""Load the sprite of the Boss."""
		key = "boss"
		self.ListofEnnemiesSurface[key] = pygame.image.load(pathfile.mainGameBoss).convert_alpha()

	#Source of this code [http://www.pygame.org/wiki/RotateCenter]
	def rot_center(self,image,angle):
		"""rotate an image while keeping its center and size"""
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image


class MusicAndSoundManager():
	"""This class gives everything you need to manage all music and sound used in the game."""
	
	#Init
	def __init__(self):
		self.ListofFireShotSound = {}
		self.ListofExplosionSound = {}
		self.ListofMusic = {}
	
	#Initialization :
	def initialization(self):
		"""Load every music and sounds used in the game."""
		self.loadExplosionSounds()
		self.loadMusic()	
	
	#Load the Sounds of shoots of explosions :
	def loadExplosionSounds(self):
		"""This function loads sounds related to explosions."""
		self.ListofExplosionSound["explosion1"] = pygame.mixer.Sound(pathfile.mainGameExplosion1)
	
	#Load the musics to be played during the game :
	def loadMusic(self):
		"""This function loads all musics file used in the game."""
		self.ListofMusic["mainMenu"] = pygame.mixer.Sound(pathfile.mainWindowMusic)
		self.ListofMusic["start"] = pygame.mixer.Sound(pathfile.mainGameMusicStart)
		self.ListofMusic["level1"] = pygame.mixer.Sound(pathfile.mainGameMusicLevel1)
	
	#Here you can play whatever music you want as long as it's contained in the available music list :
	def playMusic(self,music):
		pygame.mixer.stop()
		self.ListofMusic[music].play(-1)
	
	
	#Here you stop any music which was previously playing :
	def stopMusic(self,music):
		#Stop the music given as argument :
		self.ListofMusic[music].stop()




class FireShot:
	"""This class describe a fire shot element."""
	#Default Constructor:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.type = ""
		self.id = 0
		self.target = ""
		self.lifespan = 200
		self.orientation = 4

	#Parametric Constructor:
	def __init__(self,X,Y,Type,Id,Target,Orientation):
		self.x = X
		self.y = Y
		self.type = Type
		self.id = Id
		self.target = Target
		self.lifespan = 200
		self.orientation = Orientation



class Explosion:
	"""This class describes an explosion."""
	#Default Constructor:
	def __init__(self,X,Y):
		self.x = X
		self.y = Y
		self.lifespan1 = 10
		self.lifespan2 = 30
		self.hasSoundBeenPlayed = 0



class Score:
	"""This class describes everything related to the score of the player."""
	
	#Init:
	def __init__(self):
		self.playerScore = 0
		self.ListofTranslation = {}
