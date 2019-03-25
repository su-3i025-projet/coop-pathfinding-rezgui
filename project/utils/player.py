#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Player:
    def __init__(self, initial_state, goal_state, strategy):
        self.current_state = initial_state
        self.goal_state = goal_state
        self.strategy = strategy
        self.path = strategy.find_path(initial_state, goal_state)

    def move(self):
        if self.path:
            self.current_state = self.path.pop(0)

        return self.current_state

    def next_step(self):
        if self.path:
            return self.path[0]
        else:
            return self.current_state

    def state(self):
        return self.current_state

    def setGoal(self, goal_state):
        self.goal_state = goal_state

    def reached_goal(self):
        return self.current_state[0] == self.goal_state[0] and self.current_state[1] == self.goal_state[1]

    def solve_collision(self):
        self.path = self.strategy.solve_collision(self.path, self.current_state, self.goal_state)

