# coding: utf8


class Agent(object):

    def __init__(self, name):
        self.name = name
        self.items = set()

    def __str__(self):
        s = "Agent " + self.name + " | Items ["
        for index, item in enumerate(self.items):
            s += item
            if not len(self.items) - index == 1:
                s += ","
        s += "]"
        return s

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
        return 0
