# coding: utf8

from src.Agent import *


class Problem(object):

    def __init__(self, name, agents, items):
        assert (len(items) % len(agents) == 0), "Number of items must be a multiple of the number of agents"

        self.name = name
        self.agents = dict()
        self.items = items

        for name in agents:
            self.agents[name] = Agent(name, self)

    def __str__(self):
        s = "|-=-=-=-=-=-=-=-=-= [ Problem ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|\n"
        s += "| Name : " + self.name + "\n"
        s += "| [" + str(len(self.agents.values())) + "] Agents :\n"
        for counter, agent in enumerate(self.agents.values()):
            s += "|" + str(counter+1) + " : " + str(agent) + "\n"
        s += "|\n"
        s += "| [" + str(len(self.items)) + "] Items :\n"
        s += "|\n"
        for counter, item in enumerate(self.items):
            s += "|" + str(counter+1) + " : " + str(item) + "\n"
        s += "|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n\n"
        return s

    "======================================"
    "=============== Agents ==============="
    "======================================"

    """
    Donne l'item spécifié à l'agent spécifié
    """
    def allocate(self, item, agent):
        return

    "====================================="
    "=============== Items ==============="
    "====================================="

    """
    Retourne les items qui ont été alloués
    """
    def get_allocated_items(self):
        allocated_items = set()

        for agent in self.agents:
            for item in agent.items:
                allocated_items.add(item)

        return allocated_items

    """
    Retourne les items qui n'ont pas été alloués
    """
    def get_unallocated_items(self):
        return self.items - self.get_allocated_items()

    "=========================================="
    "=============== Efficiency ==============="
    "=========================================="

    """
    Retourne vrai si la propriété de complétude est vérifié
    """
    def check_completeness(self):
        return len(self.get_unallocated_items()) == 0

    """
    Retourne vrai si la propriété de front de pareto optimal est vérifié
    """
    def check_pareto_optimality(self):
        # TODO - Implement
        return NotImplementedError
