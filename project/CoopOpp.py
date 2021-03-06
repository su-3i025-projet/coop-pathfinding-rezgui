#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.strategies import OpportunisticStrat
from utils.engine import Engine

#board_name = "match"
board_name = "test2"

strategy = OpportunisticStrat(3)
engine = Engine(board_name)
#engine.setGoals([(16,10), (2,10)])
#engine.setGoals([(18,7), (1,11)])
engine.setGoals([(18,9), (1,9)])
engine.play(strategy)
