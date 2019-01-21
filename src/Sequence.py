# coding: utf8

import math
import random

from src.Utility import *


class SequenceType(AutoNumber):
    ROUND_ROBIN = ()
    BALANCED = ()


class Sequence(object):

    @staticmethod
    def generate(problem, mode=SequenceType.ROUND_ROBIN, randomize=False):
        agents = list(problem.agents.keys())
        if randomize:
            random.shuffle(agents)
        resources = problem.items

        repeat = math.floor(len(resources) / len(agents))
        p = agents[:]
        p_inv = p.copy()
        p_inv.reverse()

        if mode == SequenceType.ROUND_ROBIN:
            return p * repeat
        elif mode == SequenceType.BALANCED:
            return (p + p_inv) * math.floor(repeat / 2)
