#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.strategies import SingleStrat
from utils.engine import Engine

board_name = "pathfindingWorld3"

strategy = SingleStrat()
engine = Engine(board_name)
engine.play(strategy)
