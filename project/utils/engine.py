#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

from lib.gameclass import Game
from lib.spritebuilder import SpriteBuilder
from lib.ontology import Ontology
from .map import Map
from .player import Player
import pygame

class Engine:
    def __init__(self, board_name):
        self.board_name = board_name
        self.game = Game()
        self.game = Game('Cartes/' + board_name + '.json', SpriteBuilder)
        self.game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
        self.game.populate_sprite_names(self.game.O)
        self.game.fps = 5  # frames per second
        self.game.mainiteration()
        self.game.allow_overlaping_players = True

        # on initialise tous les joueurs
        self.players = [o for o in self.game.layers['joueur']]

        # on localise tous les etats initiaux (loc du joueur)
        self.initStates = [o.get_rowcol() for o in self.game.layers['joueur']]
        
        # on localise tous les objets ramassables
        self.goalStates = [o.get_rowcol() for o in self.game.layers['ramassable']]
            
        # on localise tous les murs
        wallStates = [w.get_rowcol() for w in self.game.layers['obstacle']]

        # creation de la carte
        self.game_map = Map((self.game.spriteBuilder.rowsize, self.game.spriteBuilder.colsize), wallStates, self.initStates)                     



    def play(self, strategy, iterations = 100):
        print("Init states:", self.initStates)
        print("Goal states:", self.goalStates)

        # on donne la carte a utiliser dans la strategie
        strategy.setMap(self.game_map)

        # creation des joueurs
        custom_players = [Player(self.initStates[i], self.goalStates[i], strategy) for i in range(len(self.players))]

        # position de chacun des joueurs
        posPlayers = self.initStates

        # objectifs atteints
        goals_reached = [False] * len(self.goalStates)


        for i in range(iterations):
            for j in range(len(self.players)):   
                next_step = custom_players[j].next_step()    

                if next_step in posPlayers and posPlayers.index(next_step) != j:
                    custom_players[j].solve_collision()

                
                posPlayers[j] = custom_players[j].move()
                self.game_map.setPosPlayer(j, posPlayers[j])
                self.players[j].set_rowcol(posPlayers[j][0], posPlayers[j][1])

                self.game.mainiteration()

                if custom_players[j].reached_goal() and not goals_reached[j]:
                    goals_reached[j] = True
                    print("[Player" + str(j) + "]: Reached Goal " + str((next_step[0], next_step[1])) + " in " + str(i) + " iterations")
            
            if False not in goals_reached:
                print("All players reached their goals in " + str(i) + " iterations")
                pygame.quit()
                return

        pygame.quit()


    def setGoals(self, goalStates):
        self.goalStates = goalStates
