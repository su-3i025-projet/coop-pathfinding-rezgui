#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections


def manhatthan_distance(initial_state, target_state):
    return sum([abs(a - b) for a, b in zip(initial_state, target_state)])




def get_path(initial_state, goal_state, came_from):
    current_state = goal_state
    path = [] 

    while current_state[0] != initial_state[0] or current_state[1] != initial_state[1]:
        path.append(current_state)
        current_state = came_from[current_state]

    path.reverse()
    return path




class SingleStrat:
    def __init__(self, heuristic = "manhatthan"):
        if heuristic == "manhatthan":
            self.heuristic = manhatthan_distance


    def setMap(self, game_map):
        self.game_map = game_map


    def find_path(self, initial_state, goal_state):
        frontier = collections.OrderedDict({})
        came_from = {}
        cost_so_far = {}
        
        frontier[initial_state] = 0
        came_from[initial_state] = None
        cost_so_far[initial_state] = 0

        while frontier:
            current_state = min(frontier.keys(), key=(lambda k: frontier[k]))
            del frontier[current_state]

            if current_state == goal_state:
                break;
            
            steps = [(0,1), (0,-1), (1,0), (-1,0)]
            
            for step in steps:
                next_state = tuple(a + b for a, b in zip(current_state, step))

                if self.game_map.isValid(next_state):
                    new_cost = cost_so_far[current_state] + 1

                    if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                        cost_so_far[next_state] = new_cost    
                        priority = new_cost + self.heuristic(next_state, goal_state)
                        frontier[next_state] = priority
                        came_from[next_state] = current_state
        return get_path(initial_state, goal_state, came_from)


    def solve_collision(self, player_path, player_state, player_goal_state):
        pass




class OpportunisticStrat:
    def __init__(self, M, heuristic = "manhatthan"):
        self.M = M
        if heuristic == "manhatthan":
            self.heuristic = manhatthan_distance


    def setMap(self, game_map):
        self.game_map = game_map


    def find_path(self, initial_state, goal_state, collision_state = None):
        frontier = collections.OrderedDict({})
        came_from = {}
        cost_so_far = {}
        
        frontier[initial_state] = 0
        came_from[initial_state] = None
        cost_so_far[initial_state] = 0

        while frontier:
            current_state = min(frontier.keys(), key=(lambda k: frontier[k]))
            del frontier[current_state]

            if current_state == goal_state:
                break;
            
            steps = [(0,1), (0,-1), (1,0), (-1,0)]
            
            for step in steps:
                next_state = tuple(a + b for a, b in zip(current_state, step))

                if self.game_map.isValid(next_state) and next_state !=  collision_state:
                    new_cost = cost_so_far[current_state] + 1

                    if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                        cost_so_far[next_state] = new_cost    
                        priority = new_cost + self.heuristic(next_state, goal_state)
                        frontier[next_state] = priority
                        came_from[next_state] = current_state
        return get_path(initial_state, goal_state, came_from)


    def solve_collision(self, player_path, player_state, player_goal_state):
        collision_state = player_path[0]
        if self.M < len(player_path):
            goal_state = player_path[self.M]
            new_path = self.find_path(player_state, goal_state, collision_state)
            return new_path + player_path[self.M + 1:]
        else:
            new_path = self.find_path(player_state, goal_state, collision_state)
            return new_path




class BaseStrat:
    def __init__(self, heuristic = "manhatthan"):
        self.groups = {}
        self.max_group_length = []
        if heuristic == "manhatthan":
            self.heuristic = manhatthan_distance


    def setMap(self, game_map):
        self.game_map = game_map


    def find_path(self, initial_state, goal_state):
        frontier = collections.OrderedDict({})
        came_from = {}
        cost_so_far = {}
        
        frontier[initial_state] = 0
        came_from[initial_state] = None
        cost_so_far[initial_state] = 0

        while frontier:
            current_state = min(frontier.keys(), key=(lambda k: frontier[k]))
            del frontier[current_state]

            if current_state == goal_state:
                break;
            
            steps = [(0,1), (0,-1), (1,0), (-1,0)]
            
            for step in steps:
                next_state = tuple(a + b for a, b in zip(current_state, step))

                if self.game_map.isValid(next_state) and next_state not in self.game_map.getPosPlayers():
                    new_cost = cost_so_far[current_state] + 1

                    if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                        cost_so_far[next_state] = new_cost    
                        priority = new_cost + self.heuristic(next_state, goal_state)
                        frontier[next_state] = priority
                        came_from[next_state] = current_state

        path = get_path(initial_state, goal_state, came_from)
        grp_id = self.__find_group(path)
        path = self.__set_waiting(initial_state, path, grp_id)
        return path


    def __find_group(self, path):
        grp_id = 0

        while True:
            if grp_id in self.groups:
                for state in path:
                    if state in self.groups[grp_id]:
                        grp_id += 1
                        break 
                    self.groups[grp_id] += path
                    self.max_group_length[grp_id] = max(self.max_group_length, len(path))
                    return grp_id
            else:
                self.groups[grp_id] = path
                self.max_group_length.append(len(path))
                return grp_id

    def __set_waiting(self, initial_state, path, grp_id):
        if grp_id == 0:
            return path

        wait = [initial_state] * self.max_group_length[grp_id - 1]
        return wait + path




class AdvancedStrat:
    def __init__(self, iterations = 100, heuristic = "manhatthan"):
        self.iterations = iterations
        self.reserved = {}
        if heuristic == "manhatthan":
            self.heuristic = manhatthan_distance


    def setMap(self, game_map):
        self.game_map = game_map


    def find_path(self, initial_state, goal_state):
        initial_state += (0,)
        goal_state += (self.iterations,)

        frontier = collections.OrderedDict({})
        came_from = {}
        cost_so_far = {}
        
        frontier[initial_state] = 0
        came_from[initial_state] = None
        cost_so_far[initial_state] = 0

        while frontier:
            current_state = min(frontier.keys(), key=(lambda k: frontier[k]))
            del frontier[current_state]

            if current_state == goal_state:
                break;
            
            steps = [(0,1,1), (0,-1,1), (1,0,1), (-1,0,1), (0,0,1)]
            
            for step in steps:
                next_state = tuple(a + b for a, b in zip(current_state, step))

                if self.game_map.isValid(next_state) and next_state not in self.reserved:
                    new_cost = cost_so_far[current_state] + 1

                    if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                        cost_so_far[next_state] = new_cost    
                        priority = new_cost + self.heuristic(next_state, goal_state)
                        frontier[next_state] = priority
                        came_from[next_state] = current_state
        path = get_path(initial_state, goal_state, came_from)
        self.__reserve(path)   
        return path


    def __reserve(self, path):
        for state in path:
            self.reserved[state] = 1
            #second_reserve = tuple(a + b for a, b in zip(state, (0,0,1)))
            #self.reserved[second_reserve] = 1
            third_state= tuple(a + b for a, b in zip(state, (0,0,-1)))
            self.reserved[third_state] = 1
