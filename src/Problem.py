# coding: utf8

from src.Agent import *
import itertools
import math


class Problem(object):

    def __init__(self, name, agents_name, items, initialize_agents=True):
        assert (len(items) % len(agents_name) == 0), "Number of items must be a multiple of the number of agents"

        self.name = name
        self.agents = dict()
        self.items = items

        if initialize_agents:
            for name in agents_name:
                self.agents[name] = Agent(name, self)
        else:
            for name in agents_name:
                self.agents[name] = None

    def __str__(self):
        s = "|-=-=-=-=-=-=-=-=-= [ Problem ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|\n"
        s += "| Name : " + self.name + "\n"
        s += "|\n"
        s += "| [" + str(len(self.agents.values())) + "] Agents :\n"
        for counter, agent in enumerate(self.agents.values()):
            s += "|\t" + str(counter+1) + " : " + str(agent) + "\n"
        s += "|\n"
        s += "| [" + str(len(self.items)) + "] Items :\n"
        for counter, item in enumerate(self.items):
            s += "|\t" + str(counter+1) + " : " + str(item) + "\n"
        s += "|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|\n"
        return s

    def number_of_items(self):
        return len(self.items)

    def number_of_agents(self):
        return len(self.agents)

    "======================================"
    "=============== Agents ==============="
    "======================================"

    def force_agents(self, agents):
        self.agents = agents

    def allocate(self, item, agent_name):
        """
        Donne l'item spécifié à l'agent spécifié
        """
        agent = self.agents[agent_name]
        agent.give_item(item)
        return

    def unallocate(self, item, agent_name):
        """
        Enlève l'item spécifié à l'agent spécifié
        """
        agent = self.agents[agent_name]
        agent.drop_item(item)
        print("... Removing item", item, "from", agent_name)
        return

    def transfer(self, agent_name_giver, item, agent_name_receiver):
        """
        Transfère l'item spécifié de l'agent donneur vers l'agent receveur
        """
        agent_giver = self.agents[agent_name_giver]
        agent_receiver = self.agents[agent_name_receiver]
        agent_giver.drop_item(item)
        agent_receiver.give_item(item)
        print("... Transfering item", item, "from", agent_name_giver, "to", agent_name_receiver)
        return

    def max_utility_from(self, item, agents_name_set):
        """
        Retourne l'agent, appartenant aux agents eligibles, qui value le plus cet item
        """
        agents_evaluation = dict()
        for name, agent in self.agents.items():
            if name in agents_name_set:
                agents_evaluation[name] = agent.evaluate(item)
        sorted_agents = list(sorted(agents_evaluation.items(), key=lambda x: x[1], reverse=True))
        return sorted_agents[0][0]

    def least_utility_from(self, item, agents_name_set):
        """
        Retourne l'agent, appartenant aux agents eligibles, qui value le moins cet item
        """
        agents_evaluation = dict()
        for name, agent in self.agents.items():
            if name in agents_name_set:
                agents_evaluation[name] = agent.evaluate(item)
        sorted_agents = list(sorted(agents_evaluation.items(), key=lambda x: x[1], reverse=False))
        return sorted_agents[0][0]

    def get_max_alloc_size(self):
        """
        Retourne la taille de l'allocation la plus grande
        """
        max_size = 0
        for name, agent in self.agents.items():
            if len(agent.items) > max_size:
                max_size = len(agent.items)
        return max_size

    def get_eligible_agents(self):
        """
        Retourne les agents qui peuvent recevoir des items
        """
        eligible_agents = set()
        max_size = self.get_max_alloc_size()
        for name, agent in self.agents.items():
            if len(agent.items) < max_size:
                eligible_agents.add(name)

        # They all have the same number of items
        if len(eligible_agents) == 0:
            eligible_agents = self.agents.keys()

        return eligible_agents

    def get_uneligible_agents(self):
        """
        Retourne les agents qui ne peuvent pas recevoir des items
        """
        return self.agents.keys() - self.get_eligible_agents()

    def get_other_agents(self, agents):
        """
        Retourne les agents autre que ceux passés en argument
        """
        return self.agents.keys() - agents

    def get_agents_name(self):
        """
        Retourne les agents qui ne peuvent pas recevoir des items
        """
        return set(self.agents.keys())

    "====================================="
    "=============== Items ==============="
    "====================================="

    def get_allocated_items(self):
        """
        Retourne les items qui ont été alloués
        """
        allocated_items = set()

        for agent in self.agents.values():
            for item in agent.items:
                allocated_items.add(item)

        return allocated_items

    def get_unallocated_items(self):
        """
        Retourne les items qui n'ont pas été alloués
        """
        return self.items - self.get_allocated_items()

    def get_items_per_agent(self):
        return math.floor(len(self.items) / len(self.agents))

    @staticmethod
    def get_other_items(ref, items):
        return set(ref) - set(items)

    "=========================================="
    "=============== Efficiency ==============="
    "=========================================="

    def check_completeness(self):
        """
        Retourne vrai si la propriété de complétude est vérifié
        """
        return len(self.get_unallocated_items()) == 0

    "================================================"
    "=============== Borda properties ==============="
    "================================================"

    def is_borda_optimal(self):
        """
        Retourne vrai si chaque allocation de chaque agent est meilleure ou égale
        que si chacun possédait les autres allocations des autres agents.
        De plus, un agent doit évaluer que son allocation est strictment meilleure
        que celle d'un autre au moins une fois
        """
        at_least_one_greater = False
        for name, agent in self.agents.items():
            other_agents = self.get_other_agents(set(name))
            for other_name in other_agents:
                other_agent = self.agents[other_name]
                u = agent.utility()
                o_u = agent.evaluate_bundle(other_agent.items)
                diff = u - o_u
                if diff < 0:
                    return False, \
                           name + " prefers " + other_name + "'s allocation : " + str(other_agent.items) + " | " \
                           + str(u) + " vs " + str(o_u)
                elif diff > 0:
                    at_least_one_greater = True
        if at_least_one_greater:
            return True, \
                   "For each agent, his allocation is greater or equal to other agent's allocations"
        else:
            return False, \
                   "For each agent, his allocation is equal to other agent's allocations"

    def is_maximum_borda_sum(self):
        """
        Retourne vrai si la somme des scores de Borda des agents actuels
        est égale au max de la sum des scores de Borda des agents selon toutes les allocations possibles
        """
        # I./ Compute current sum
        current_sum = 0
        for name, agent in self.agents.items():
            current_sum += agent.utility()

        # II./ Get all possible allocations
        sum_list = list()
        self.recursive_borda_sum(sum_list,
                                 0,
                                 list(self.items),
                                 list(self.agents.keys()))
        max_sum = max(sum_list)
        return current_sum == max_sum, "Current sum (" + str(current_sum) + ") | Max sum (" + str(max_sum) + ")"

    def recursive_borda_sum(self, sum_list, current_sum, items, remaining_agents):
        all_alloc = [list(x) for x in itertools.combinations(items, self.get_items_per_agent())]
        agent_name = remaining_agents.pop()
        agent = self.agents[agent_name]
        for alloc in all_alloc:
            remaining_items = self.get_other_items(items, alloc)
            if remaining_agents:
                self.recursive_borda_sum(sum_list,
                                         current_sum + agent.evaluate_bundle(alloc),
                                         remaining_items,
                                         remaining_agents[:])
            else:
                sum_list.append(current_sum + agent.evaluate_bundle(alloc))
        return

    def is_borda_proportional(self):
        """
        Retourne vrai si chaque agent a un score de Borda au moins égal à tous les autres agents
        """
        for name, agent in self.agents.items():
            other_agents = self.get_other_agents(set(name))
            for other_name in other_agents:
                other_agent = self.agents[other_name]
                u = agent.utility()
                o_u = agent.evaluate_bundle(other_agent.items)
                if u - o_u < 0:
                    return False, \
                           name + " prefers " + other_name + "'s allocation : " + str(other_agent.items) + " | " \
                           + str(u) + " vs " + str(o_u)
        return True, "For each agent, his allocation is at least equal to other agent's allocations"

    def is_borda_max_min(self):
        """
        itertools.combinaison()
        Retourne vrai si le min des scores de borda est égal au max min des scores de Borda
        des agents selon toutes les allocations possibles
        """

        # I./ Compute current minimum
        min_score = None
        for name, agent in self.agents.items():
            value = agent.utility()
            if not min_score or value < min_score:
                min_score = value

        # II./ Compute current minimum
        score_list = list()
        self.recursive_borda_max_min(score_list,
                                     list(),
                                     list(self.items),
                                     list(self.agents.keys()))

        # III./ Compute min for each possible allocations
        min_score_list = list()
        for round_score in score_list:
            min_score_list.append(min(round_score))

        max_min_score = max(min_score_list)
        return min_score == max(min_score_list), \
               "Minimum score (" + str(min_score) + ") | Max min score (" + str(max_min_score) + ")"

    def recursive_borda_max_min(self, score_list, current_score, items, remaining_agents):
        all_alloc = [list(x) for x in itertools.combinations(items, self.get_items_per_agent())]
        agent_name = remaining_agents.pop()
        agent = self.agents[agent_name]
        for alloc in all_alloc:
            remaining_items = self.get_other_items(items, alloc)
            if remaining_agents:
                _current_score = current_score[:]
                _current_score.append(agent.evaluate_bundle(alloc))
                self.recursive_borda_max_min(score_list,
                                             _current_score,
                                             remaining_items,
                                             remaining_agents[:])
            else:
                _current_score = current_score[:]
                _current_score.append(agent.evaluate_bundle(alloc))
                score_list.append(_current_score)
        return
