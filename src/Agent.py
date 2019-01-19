# coding: utf8

import random

from collections import OrderedDict



class Agent(object):

    def __init__(self, name, problem):
        self.name = name
        self.items = set()
        self.rankings = OrderedDict()

        self.generate_borda_rankings(problem.items)

    def __str__(self):
        s = "Agent " + self.name + " | Items " + str(self.items) + " | Rankings "
        for index, item in enumerate(self.rankings):
            s += item
            if not len(self.rankings) - index == 1:
                s += " > "
        s += ""
        return s

    "==========================================="
    "=============== Preferences ==============="
    "==========================================="

    """
    Génère les préférences de Borda de l'agent de manière aléatoire
    """
    def generate_borda_rankings(self, items):
        items = list(items)
        random.shuffle(items)
        for index, item in enumerate(items):
            self.rankings[item] = len(items) - index

    """
    Retourne l'utilité actuelle de l'agent
    """
    def utility(self):
        utility = 0
        for item in self.items:
            utility += self.evaluate(item)

        return utility

    """
    Retourne l'utilité d'un agent envers un bien
    """
    def evaluate(self, item):
        return self.rankings[item]

    """
    Retourne le "value" meilleur item d'un lot
    """
    def top(self, items, value=0):
        lot = OrderedDict()
        for item in items:
            lot[item] = self.evaluate(item)
        sorted_lot = list(sorted(lot.items(), key=lambda x: x[1], reverse=False))
        return sorted_lot[value][0]

    """
    Retourne le "value" moins bon item d'un lot
    """
    def bottom(self, items, value=0):
        lot = dict()
        for item in items:
            lot[item] = self.evaluate(item)
        sorted_lot = list(sorted(lot.items(), key=lambda x: x[1], reverse=True))
        return sorted_lot[value][0]

    "====================================="
    "=============== Items ==============="
    "====================================="

    """
    Donne l'item spécifié à cet agent
    """
    def give_item(self, item):
        self.items.add(item)
        return

    """
    Enlève l'item spécifié d 
    """
    def drop_item(self, item):
        self.items.remove(item)
        return

