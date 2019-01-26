# coding: utf8

import math
import random

from src.Utility import *


class SequenceType(AutoNumber):
    ROUND_ROBIN = ()
    BALANCED = ()


class Sequence(object):

    def __init__(self, value, _type):
        self.type = _type
        self.value = value

    def __str__(self):
        return "(" + str(self.get_type_name()) + ") - " + str(self.value)

    def get_type_name(self):
        return self.type.name

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
            return Sequence(p * repeat, mode)
        elif mode == SequenceType.BALANCED:
            return Sequence((p + p_inv) * math.floor(repeat / 2), mode)
