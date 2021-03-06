# -*- coding: utf-8 -*-
from __future__ import division
#########################################################################################################################################################################
### Date : 21 Octobre 2018																																			    #
### Author : Yoshii_974																																					#
### Description : This file contains every Physic Logic for the game. 																									#
#########################################################################################################################################################################
from commonclasses import *
from Player import *
from Ennemies import *
import pygame
from pygame.locals import *
##########################################################IMPORTS########################################################################################################
class PhysicEngine:
    """Any of Physic element should be found in this class. """

    # Default Constructor
    def __init__(self):
        self.ennemies: Ennemies
        self.players: [] # list of Players
        self.listofExplosions = []

    # Set the Dependencies to the Physic Engine
    def setDependencies(self, Ennemies, Players):
        self.ennemies = Ennemies
        self.players = Players
    
    # Update current game State
    def updateCurrentGameState(self):
        """Update the state of the different elements of the game """
        for player in self.players:

            # Destroy the player's fireshot which lifespan has been reached :
            player.destroyFireShots()
        
            # Check for the animation of the player :
            player.animate()

        # Update the wave of ennemies :
        self.ennemies.updateEnnemiesWave()

        # Destroy all previous ennemy shots :
        self.ennemies.destroyFireShots()

        # Make ennemies to trigger fire shots :
        self.ennemies.fire()
        self.ennemies.animateFireShots()

        # Animate the ennemies groups :
        self.ennemies.animate()

    # Detect all Collisions
    def simulateAllCollisions(self):
        #print("all collisions")
        self.simulateEnnemiesCollisions()
        self.simulatePlayersCollisions()
        self.updateExplosionsStates()

    # Detect Collisions for the Ennemies
    def simulateEnnemiesCollisions(self):
        # print("ennemies collisions")
        # Loop on each ennemy group and check if there's any collision
        ListofEnnemiesCollisions = []
        
        # For each player in the current physic engine list of players
        for player in self.players:
            # For each fireshot in this player's list of fireshot
            for fire_id,fireshot in player.ListofFireShot.items():
                # Create a fireshot rect
                fireshot_rect = pygame.Rect(fireshot.x,fireshot.y,GAME_ELEMENT_SIZE,GAME_ELEMENT_SIZE)
                # Allows us not to keep looping when a collision has already been found.
                # Checking this value twice is needed since we are in a 3-way nested loop checking !
                collisionFound = False
                
                # For each ennemy in each ennemy_group
                for eg_id,eg in self.ennemies.ListofEnnemies.items():
                    # If it has been detected a collision for the current fire shot, no need to keep loopking on ennemy group
                    if collisionFound == True:
                        break
                    
                    # For each ennemy in this current group
                    for e in eg.ListofPositions:
                        # If it has been detected a collision for the current fire shot, no need to keep loopking on each ennemy inside this ennemy group
                        if collisionFound == True:
                            break
                        
                        # Create a rect of a game size element to check for a collision
                        e_rect = pygame.Rect(e[1],e[2],GAME_ELEMENT_SIZE,GAME_ELEMENT_SIZE)
                        
                        # If there is a collision between the current fireshot and the current ennemy, then we create a collision and we go to the next fireshot checking :
                        if fireshot_rect.colliderect(e_rect):
                            # Create a collision containing the ennemy group, the ennemy id and the fire shot id
                            collision = [eg_id, e[0], fire_id, player.playerID]
                            # Add to the list of collisions
                            ListofEnnemiesCollisions.append(collision)
                            # Stop checking for a collision between this fire shot and anything else
                            collisionFound = True

        # Now, it is time to destroy every elements which collided with something else:
        for col in ListofEnnemiesCollisions:
            print(col)
            # First, get the ennemy group
            eg = self.ennemies.ListofEnnemies[col[0]]

            # For each ennemy in the current ennemy group
            for e in eg.ListofPositions:
                # If this ennemy collide with a fire shot
                if e[0] == col[1]:
                    # add it to the list of ennemy to be removed
                    # ennemyToBeRemoved = e
                    # Create an explosions at the ennemy position
                    exp = Explosion(e[1],e[2])
                    # Add this explosions to the list of explosions to be drawn by the Renderer Engine later
                    self.listofExplosions.append(exp)
                    # Increase the current player score
                    self.players[col[3]].score.playerScore += 50
                    # Remove 1 ennemy from the ennemy group
                    eg.currentEnnemyNumber -= 1
                    # Remove the fire shot from the current player list
                    del self.players[col[3]].ListofFireShot[col[2]]
                    # Remove the collided ennemy
                    eg.ListofPositions.remove(e)
                    # I usually don't like to remove an item from a list on which I am currently looping 
                    # but in this case, since it doesn't keep looping after removing the item, 
                    # then everything should works fine 
                    # ( so here the break is quiet important ... 
                    # or maybe not, if python deals nicely with these kind of situations )
                    break

    # Detect Collisions for the Player
    def simulatePlayersCollisions(self):
        """ Checking if any of the ennemies shots collide with the player. In this case, the player health is decreased. """
        # print("player collisions")
        # For each player 
        for player in self.players:
            # Create the list containing the collisions with the player
            ListofPlayerCollisions = []
            # Create a rect of a game size element to check for a collision
            player_rect = pygame.Rect(player.x, player.y, GAME_ELEMENT_PLAYER_SIZE, GAME_ELEMENT_PLAYER_SIZE)

            # For each ennemy group
            for eg_id,eg in self.ennemies.ListofEnnemies.items():
                # For each fire shots in this ennemy group
                for shot_id,shot in eg.ListofFireShot.items():
                    # Create a rect of a game size element to check for a collision
                    shot_rect = pygame.Rect(shot.x, shot.y, GAME_ELEMENT_SIZE, GAME_ELEMENT_SIZE)
                    # If a collision was detected
                    if (shot_rect.colliderect(player_rect)):
                        # Create a collision containing the ennemy group id and the fire shot id
                        collision = [eg_id,shot_id]
                        # Add to the list of collisions
                        ListofPlayerCollisions.append(collision)

            # For each collisions
            for col in ListofPlayerCollisions:
                # Get the ennemy group ID
                eg = self.ennemies.ListofEnnemies[col[0]]
                # Remove the shot from the list of ennemy fire shots
                del eg.ListofFireShot[col[1]]
                # If the player hasn't activated its shield
                if player.timeBeforeShieldIsDeactivated == 0:
                    # print(self.player.health)
                    # Remove health
                    player.health -= 0
    
    # Loop through explosions and delete these which lifespan has reach 0
    def updateExplosionsStates(self):
        """Loop through explosions and delete these which lifespan has reach 0 """

        #Contains each explosions which has their lifespan 1 and 2 equals to 0, it's time to remove this explosion object :
        listofExplosionsToBeRemoved = []

        # Loop through explosions
        for exp in self.listofExplosions:
            if exp.lifespan1 > 0:
                exp.lifespan1 -= 1
            elif exp.lifespan2 > 0:
                exp.lifespan2 -=1
            else:
                listofExplosionsToBeRemoved.append(exp)
        
        #We delete every explosions which has no longer any reason to stay alive:
        for exp in listofExplosionsToBeRemoved:
            self.listofExplosions.remove(exp)