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
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        return s

    "======================================"
    "=============== Agents ==============="
    "======================================"

    """
    Donne l'item spécifié à l'agent spécifié
    """
    def allocate(self, item, agent_name):
        agent = self.agents[agent_name]
        agent.give_item(item)
        print("... Giving item", item, "to", agent_name)
        return

    """
    Enlève l'item spécifié à l'agent spécifié
    """
    def unallocate(self, item, agent_name):
        agent = self.agents[agent_name]
        agent.drop_item(item)
        print("... Removing item", item, "from", agent_name)
        return

    """
    Transfère l'item spécifié de l'agent donneur vers l'agent receveur
    """
    def transfer(self, agent_name_giver, item, agent_name_receiver):
        agent_giver = self.agents[agent_name_giver]
        agent_receiver = self.agents[agent_name_receiver]
        agent_giver.drop_item(item)
        agent_receiver.give_item(item)
        print("... Transfering item", item, "from", agent_name_giver, "to", agent_name_receiver)
        return

    """
    Retourne l'agent, appartenant aux agents eligibles, qui value le plus cet item
    """
    def max_utility_from(self, item, agents_name_set):
        agents_evaluation = dict()
        for name, agent in self.agents.items():
            if name in agents_name_set:
                agents_evaluation[name] = agent.evaluate(item)
        sorted_agents = list(sorted(agents_evaluation.items(), key=lambda x: x[1], reverse=True))
        return sorted_agents[0][0]

    """
    Retourne l'agent, appartenant aux agents eligibles, qui value le moins cet item
    """
    def least_utility_from(self, item, agents_name_set):
        agents_evaluation = dict()
        for name, agent in self.agents.items():
            if name in agents_name_set:
                agents_evaluation[name] = agent.evaluate(item)
        sorted_agents = list(sorted(agents_evaluation.items(), key=lambda x: x[1], reverse=False))
        return sorted_agents[0][0]

    """
    Retourne la taille de l'allocation la plus grande
    """
    def get_max_alloc_size(self):
        max_size = 0
        for name, agent in self.agents.items():
            if len(agent.items) > max_size:
                max_size = len(agent.items)
        return max_size

    """
    Retourne les agents qui peuvent recevoir des items
    """
    def get_eligible_agents(self):
        eligible_agents = set()
        max_size = self.get_max_alloc_size()
        for name, agent in self.agents.items():
            if len(agent.items) < max_size:
                eligible_agents.add(name)

        # They all have the same number of items
        if len(eligible_agents) == 0:
            eligible_agents = self.agents.keys()

        return eligible_agents

    """
    Retourne les agents qui ne peuvent pas recevoir des items
    """
    def get_uneligible_agents(self):
        return self.agents.keys() - self.get_eligible_agents()

    "====================================="
    "=============== Items ==============="
    "====================================="

    """
    Retourne les items qui ont été alloués
    """
    def get_allocated_items(self):
        allocated_items = set()

        for agent in self.agents.values():
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
