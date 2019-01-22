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
        s = "Agent " + self.name + "\t| Items " + str(self.items) + "\t| Utility " + str(self.utility()) + "\t| Rankings : "
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
    Retourne le rank d'un item.
    1 préféré
    N le moins préféré
    """
    def rank(self, item):
        for index, _item in enumerate(self.rankings.keys()):
            if _item == item:
                return index

    """
    Retourne tous les items qui ont un rang meilleur ou égal à celui donné
    """
    def get_items_under_rank(self, items, rank):
        _items = set()
        for item in items:
            if self.rank(item) <= rank:
                _items.add(item)
        return _items

    """
    Retourne l'utilité actuelle de l'agent
    """
    def utility(self):
        return self.evaluate_bundle(self.items)

    """
    Retourne l'utilité d'un agent envers un bien
    """
    def evaluate(self, item):
        return self.rankings[item]

    """
    Retourne l'utilité d'un agent envers un lot (ou le score de borda d'un bundle)
    """
    def evaluate_bundle(self, bundle):
        evaluation = 0
        for item in bundle:
            evaluation += self.evaluate(item)
        return evaluation

    """
    Retourne le "value" meilleur item d'un lot
    """
    def top(self, items, value=0):
        lot = OrderedDict()
        for item in items:
            lot[item] = self.evaluate(item)
        sorted_lot = list(sorted(lot.items(), key=lambda x: x[1], reverse=True))
        return sorted_lot[value][0]

    """
    Retourne le "value" moins bon item d'un lot
    """
    def bottom(self, items, value=0):
        lot = dict()
        for item in items:
            lot[item] = self.evaluate(item)
        sorted_lot = list(sorted(lot.items(), key=lambda x: x[1], reverse=False))
        return sorted_lot[value][0]

    """
    Compare l'allocation actuelle avec l'allocation passé en paramètre
    - 1 :   Moins bonne
    0 :     Indécis
    1 :     Meilleure
    """
    def compare_bundle(self, bundle):
        return self.utility() - self.evaluate_bundle(bundle)

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
