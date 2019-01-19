# coding: utf8

import math

from src.Utility import *


class SequenceType(AutoNumber):
    ROUND_ROBIN = ()
    BALANCED = ()


class Sequence(object):

    @staticmethod
    def generate_sequence(agents, resources, mode=SequenceType.ROUND_ROBIN):
        repeat = math.floor(len(resources) / len(agents))
        p = list(agents)
        p_inv = p.copy()
        p_inv.reverse()

        if mode == SequenceType.ROUND_ROBIN:
            return p * repeat
        elif mode == SequenceType.BALANCED:
            return (p + p_inv) * math.floor(repeat / 2)
