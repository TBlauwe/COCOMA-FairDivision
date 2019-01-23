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
        s = "Agent " + self.name + \
            "\t| Items " + str(self.items) + "\t| Utility " + str(self.utility()) + "\t| Rankings : "
        for index, item in enumerate(self.rankings):
            s += item
            if not len(self.rankings) - index == 1:
                s += " > "
        s += ""
        return s

    "==========================================="
    "=============== Preferences ==============="
    "==========================================="

    def set_borda_ranks(self, rankings):
        for index, item in enumerate(rankings):
            self.rankings[item] = len(rankings) - index

    def generate_borda_rankings(self, items):
        """
        Génère les préférences de Borda de l'agent de manière aléatoire
        """
        items = list(items)
        random.shuffle(items)
        for index, item in enumerate(items):
            self.rankings[item] = len(items) - index

    def rank(self, item):
        """
        Retourne le rank d'un item.
        1 préféré
        N le moins préféré
        """
        for index, _item in enumerate(self.rankings.keys()):
            if _item == item:
                return index

    def get_items_under_rank(self, items, rank):
        """
        Retourne tous les items qui ont un rang meilleur ou égal à celui donné
        """
        _items = set()
        for item in items:
            if self.rank(item) <= rank:
                _items.add(item)
        return _items

    def utility(self):
        """
        Retourne l'utilité actuelle de l'agent
        """
        return self.evaluate_bundle(self.items)

    def evaluate(self, item):
        """
        Retourne l'utilité d'un agent envers un bien
        """
        return self.rankings[item]

    def evaluate_bundle(self, bundle):
        """
        Retourne l'utilité d'un agent envers un lot (ou le score de borda d'un bundle)
        """
        evaluation = 0
        for item in bundle:
            evaluation += self.evaluate(item)
        return evaluation

    def top(self, items, value=0):
        """
        Retourne le "value" meilleur item d'un lot
        """
        lot = OrderedDict()
        for item in items:
            lot[item] = self.evaluate(item)
        sorted_lot = list(sorted(lot.items(), key=lambda x: x[1], reverse=True))
        return sorted_lot[value][0]

    def bottom(self, items, value=0):
        """
        Retourne le "value" moins bon item d'un lot
        """
        lot = dict()
        for item in items:
            lot[item] = self.evaluate(item)
        sorted_lot = list(sorted(lot.items(), key=lambda x: x[1], reverse=False))
        return sorted_lot[value][0]

    def compare_bundle(self, bundle):
        """
        Compare l'allocation actuelle avec l'allocation passé en paramètre
        - 1 :   Moins bonne
        0 :     Indécis
        1 :     Meilleure
        """
        return self.utility() - self.evaluate_bundle(bundle)

    "====================================="
    "=============== Items ==============="
    "====================================="

    def give_item(self, item):
        """
        Donne l'item spécifié à cet agent
        """
        self.items.add(item)
        return

    def drop_item(self, item):
        """
        Enlève l'item spécifié d
        """
        self.items.remove(item)
        return
