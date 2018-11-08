# -*- coding: utf-8 -*-
# from __future__ import division
#########################################################################################################################################################################
### Date : 21 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains every Physic Logic for the game. 																									#
#########################################################################################################################################################################
from commonclasses import *
from Player import *
import RendererEngine
import PhysicEngine
import pygame
from pygame.locals import *
##########################################################IMPORTS########################################################################################################
class InputEngine:
    """All I/O element should be found in this class"""

    #Default Constructor
    def __init__(self):
        self.player: Player
        self.currentGameState = "MENU"
        self.mainMenuOptionsSelections = [1, 0]

    #Initialization
    def initialization(self):
        pygame.key.set_repeat(50,100)

    #Set dependencies
    def setDependencies(self, Player):
        self.player = Player

    #Loop through pygame event
    def getPygameEvents(self):
        """Get the events caught by Pygame"""
        if self.currentGameState == "MENU":
            self.handleMenuEvents()
        elif self.currentGameState == "GAME":
            self.handleGameEvents()
    
    #Handle events for the menu
    def handleMenuEvents(self):
        """Handle any related events when in the main menu of the game"""
        #Loop on each event which has been sent by PyGame :
        for evt in pygame.event.get():
            #If the player selected the quit button (cross right-sided of the window)
            if evt.type == QUIT:
                self.currentGameState = "QUIT"
            
            elif evt.type == KEYDOWN:
                if evt.key == K_DOWN:
                    if self.mainMenuOptionsSelections == [1,0]:
                        self.mainMenuOptionsSelections = [0,1]
                    elif self.mainMenuOptionsSelections == [0,1]:
                        self.mainMenuOptionsSelections = [1,0]
                
                if evt.key == K_UP:
                    if self.mainMenuOptionsSelections == [1,0]:
                        self.mainMenuOptionsSelections = [0,1]
                    elif self.mainMenuOptionsSelections == [0,1]:
                        self.mainMenuOptionsSelections = [1,0]

                if evt.key == K_RETURN or evt.key == K_KP_ENTER:
                    if self.mainMenuOptionsSelections == [1,0]:
                        self.currentGameState = "GAME"
                    elif self.mainMenuOptionsSelections == [0,1]:
                        self.currentGameState = "QUIT"
    
    #Handle events for the game
    def handleGameEvents(self):
        """Handle any related events when actually playing the game"""
        #Loop on all the event sent by pygame :
        for evt in pygame.event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_DOWN:
                    self.player.dy = 2
                elif evt.key == K_UP:
                    self.player.dy = -2
                elif evt.key == K_LEFT:
                    self.player.dx = -2
                elif evt.key == K_RIGHT:
                    self.player.dx = 2
                elif evt.key == K_SPACE:
                    self.player.fireShot()
                elif evt.key == K_LCTRL:
                    if self.player.timeBeforeShieldIsDeactivated == 0 and self.player.nbTimesShieldAllowed > 0:
                        self.player.timeBeforeShieldIsDeactivated = 500
                        self.player.nbTimesShieldAllowed -= 1
                elif evt.key == K_F1:
                    self.player.currentWeapon = "fire1"
                elif evt.key == K_F2:
                    self.player.currentWeapon = "fire2"
                elif evt.key == K_F3:
                    self.player.currentWeapon = "fire3"

            elif evt.type == KEYUP:
                if evt.key == K_LEFT or evt.key == K_RIGHT:
                    self.player.dx = 0
                elif evt.key == K_DOWN or evt.key == K_UP:
                    self.player.dy = 0
                """elif evt.key == K_SPACE:
                    self.player.fireShot()
                elif evt.key == K_LCTRL:
                    if self.player.timeBeforeShieldIsDeactivated == 0 and self.player.nbTimesShieldAllowed > 0:
                        self.player.timeBeforeShieldIsDeactivated = 500
                        self.player.nbTimesShieldAllowed -= 1
                elif evt.key == K_F1:
                    self.player.currentWeapon = "fire1"
                elif evt.key == K_F2:
                    self.player.currentWeapon = "fire2"
                elif evt.key == K_F3:
                    self.player.currentWeapon = "fire3"""
            
            elif evt.type == JOYBUTTONDOWN:
                if evt.button == 0:
                    self.player.fireShot()
                elif evt.button == 1:
                    if self.player.currentWeapon == "fire1":
                        self.player.currentWeapon = "fire2"
                    elif self.player.currentWeapon == "fire2":
                        self.player.currentWeapon = "fire3"
                    elif self.player.currentWeapon == "fire3":
                        self.player.currentWeapon = "fire1"
                elif evt.button == 2:
                    if self.player.timeBeforeShieldIsDeactivated == 0 and self.player.nbTimesShieldAllowed > 0:
                        self.player.timeBeforeShieldIsDeactivated = 500
                        self.player.nbTimesShieldAllowed -= 1
            
            elif evt.type == JOYAXISMOTION:
                if evt.axis == 0:
                    if evt.value < -0.25:
                        self.player.dx = -2
                    elif evt.value > 0.25:
                        self.player.dx = 2
                    else:
                        self.player.dx = 0
                elif evt.axis == 1:
                    if evt.value < -0.25:
                        self.player.dy = -2
                    elif evt.value > 0.25:
                        self.player.dy = 2
                    else:
                        self.player.dy = 0

    #TODO: Faire quelque chose avec ce truc ...
    """def joystick(self):
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
            print("Hats :", joystick_player.get_numhats())"""

    #Process Player Inputs (Awesome comments here !)
    def processPlayerInput(self, playerInputs):
        """Process the player inputs"""
        for input in playerInputs:
            if input == "left":
                self.player.dx = 2
            elif input == "right":
                self.player.dx = 2
            elif input == "up":
                self.player.dy = -2
            elif input == "down":
                self.player.dy = 2
            elif input == "space":
                self.player.fireShot()
            elif input == "ctrl":
                if self.player.timeBeforeShieldIsDeactivated == 0 and self.player.nbTimesShieldAllowed > 0:
                        self.player.timeBeforeShieldIsDeactivated = 500
                        self.player.nbTimesShieldAllowed -= 1
            elif input == "f1":
                self.player.currentWeapon = "fire1"
            elif input == "f2":
                self.player.currentWeapon = "fire2"
            elif input == "f3":
                self.player.currentWeapon = "fire3"
            else:
                print('error with inputs of player #' + str(self.player.playerID))
    