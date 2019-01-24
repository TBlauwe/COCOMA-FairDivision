import random
import math
import numpy as np
import matplotlib.pyplot as plt
from src.Problem import *
from src.Sequence import *


class ProblemSet(object):
    """
    Permet de générér plusieurs instances d'un problème avec les mêmes paramètrs (nombre d'agents et d'items), mais avec
    des changements au niveau des préférences des agents. Au plus N! instances possibles (N = nombre d'items)
    """

    def __init__(self, initial_problem, algorithms, limit=math.inf):
        self.initial_problem = initial_problem
        self.problems = list()  # Set of problems to test
        self.algorithms = algorithms
        self.results = dict()

        # Create a container to store all borda properties per algorithm
        for algorithm in algorithms:
            borda_properties = dict()
            for borda_property in BordaProperty:
                borda_properties[borda_property] = list()
            self.results[algorithm] = borda_properties

        self.generate_instances(limit)

    def generate_instances(self, limit):
        """
        :param number: Par défaut, génére le nombre maximal d'instances possibles, sinon la valeur spécifiée
        """
        all_rankings = [list(x) for x in itertools.permutations(self.initial_problem.items)]
        rankings_per_agent = dict()

        # La préférence du premier agent n'est pas importante
        agents_name = list(self.initial_problem.get_agents_name())
        rankings_per_agent[agents_name.pop()] = all_rankings[0]
        self.recursive_generate_instances(all_rankings, rankings_per_agent, agents_name, limit)

        return

    def recursive_generate_instances(self, all_rankings, current_rankings, remaining_agents, limit):
        if len(self.problems) >= limit:
            return

        agent_name = remaining_agents.pop()
        for ranking in all_rankings:
            _current_rankings = dict(current_rankings)
            _current_rankings[agent_name] = ranking
            if remaining_agents:
                self.recursive_generate_instances(all_rankings, _current_rankings, remaining_agents[:], limit)
            else:
                agents = dict()
                for name, rankings in _current_rankings.items():
                    agent = Agent(name, self.initial_problem)
                    agent.set_borda_ranks(rankings)
                    agents[name] = agent
                problem = Problem(self.initial_problem.name + "_" + str(len(self.problems) + 1),
                                  self.initial_problem.get_agents_name(),
                                  self.initial_problem.items,
                                  False)
                problem.force_agents(agents)
                self.problems.append(problem)

    def run(self, sequence):
        print("===================================================")
        print("=============== LAUNCHING BENCHMARK ===============")
        print("===================================================")

        for algorithm in self.algorithms:
            print("---------- Testing : " + algorithm.__name__)
            for index, problem in enumerate(self.problems):
                print("... round " + str(index))
                algo = algorithm(problem)
                algo.compute(sequence, False)
                self.add_result(algorithm, algo)

        print("==================================================")
        print("=============== STOPPING BENCHMARK ===============")
        print("==================================================")

    def add_result(self, algorithm, instance):
        """
        :param algorithm: Classe de l'algorithme testé
        :param instance: Instance de l'algorithme testé
        """
        for borda_property in BordaProperty:
            self.results[algorithm][borda_property].append(instance.problem.borda_properties[borda_property][0])

    def show_results(self):
        fig = plt.figure()
        plt.style.use('ggplot')

        plt.title(self.initial_problem.name)
        plt.yticks(range(0,101,10))
        plt.ylim([0,100])

        gap = .8 / len(self.algorithms)

        for i, algorithm in enumerate(self.algorithms):
            y = list()
            X = np.arange(len(BordaProperty.values()))
            for borda_property in BordaProperty:
                values = self.results[algorithm][borda_property]
                y.append(sum(values) / len(values) * 100)
            plt.bar(X + i * gap, y, width=gap, label=algorithm.__name__)

        plt.legend(loc="best")
        plt.show()
