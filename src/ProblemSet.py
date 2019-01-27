import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from src.Problem import *
from src.Sequence import *


class ProblemSet(object):
    """
    Permet de générér plusieurs instances d'un problème avec les mêmes paramètrs (nombre d'agents et d'items), mais avec
    des changements au niveau des préférences des agents. Au plus N! instances possibles (N = nombre d'items)
    """

    def __init__(self, initial_problem, algorithms, limit=math.inf, path="./"):
        self.initial_problem = initial_problem
        self.problems = list()  # Set of problems to test
        self.algorithms = algorithms
        self.results = dict()
        self.sequence = None
        self.path = path

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
        n = self.initial_problem.number_of_items()
        print("... number of possible permutations for preferences :", math.factorial(n))
        print("... generating permutations")
        all_rankings = [list(x) for x in itertools.islice(itertools.permutations(self.initial_problem.items, n), limit)]

        print("... generating instances")

        rankings_per_agent = dict()
        # La préférence du premier agent n'est pas importante
        agents_name = list(self.initial_problem.get_agents_name())
        rankings_per_agent[agents_name.pop()] = all_rankings[0]
        self.recursive_generate_instances(all_rankings, rankings_per_agent, agents_name, limit)

        return

    def recursive_generate_instances(self, all_rankings, current_rankings, remaining_agents, limit):
        agent_name = remaining_agents.pop()
        for ranking in all_rankings:
            if len(self.problems) >= limit:
                return

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
                problem = Problem(self.initial_problem.get_agents_name(),
                                  self.initial_problem.items,
                                  False)
                problem.force_agents(agents)
                self.problems.append(problem)

    def run(self, sequence):
        self.sequence = sequence
        print("|-=-=-=-=-=-= [ STARTING BENCHMARK ] =-=-=-=-=-=-=|")
        print(self.get_summary())
        print("|-=-=-=-=-=-=-=-=- [ BEGIN ] -=-=-=-=-=-=-=-=-=-=-|")
        for algorithm in self.algorithms:
            print("\n---------- Testing : " + algorithm.__name__)
            nb_pb = len(self.problems)
            step = nb_pb / 51
            checkpoint = step
            print("In progress ", end="")
            for index, problem in enumerate(self.problems):
                if index >= checkpoint:
                    print(".", end="")
                    checkpoint += step
                algo = algorithm(problem)
                algo.compute(sequence, False)
                self.add_result(algorithm, algo)
            print(" Done !")

        print("\n|-=-=-=-=-=-=-=-=-= [ END ] =-=-=-=-=-=-=-=-=-=-=-|")

    def add_result(self, algorithm, instance):
        """
        :param algorithm: Classe de l'algorithme testé
        :param instance: Instance de l'algorithme testé
        """
        for borda_property in BordaProperty:
            self.results[algorithm][borda_property].append(instance.problem.borda_properties[borda_property][0])

    def get_name(self):
        name = "Set_"
        name += self.initial_problem.name + "_"
        name += self.sequence.get_type_name()
        return name

    def get_summary(self):
        s = str(self.initial_problem)
        s += "|-=-=-=-=-=-=-=-=-= [ SUMMARY ]-=-=-=-=-=-=-=-=-=|\n"
        s += "|\n"
        s += "| Problem         : " + self.initial_problem.name + "\n"
        s += "| Algorithms      : " + str([x.__name__ for x in self.algorithms]) + "\n"
        s += "| Sequence        : " + str(self.sequence) + "\n"
        s += "| Nb of instances : " + str(len(self.problems)) + "\n"
        s += "| Nb of agents    : " + str(self.initial_problem.number_of_agents()) + "\n"
        s += "| Nb of items     : " + str(self.initial_problem.number_of_items()) + "\n"
        s += "|\n"
        s += "|-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|"
        return s

    def show_results(self, save_only=False):
        fig = plt.figure()
        plt.style.use('ggplot')

        plt.suptitle(self.get_name().replace("_", " "), fontsize=14, fontweight='bold')
        plt.title("Nombre d'instances : " + str(len(self.problems)))
        plt.yticks(range(0,101,10))
        plt.ylim([0,100])
        plt.ylabel("% d'allocs vérifiant la propriété")

        X = np.arange(len(BordaProperty.values()))
        gap = .5 / len(self.algorithms)

        labels = [x.replace(" ", "\n") for x in BordaProperty.values()]
        plt.xticks(X + gap, labels)

        for i, algorithm in enumerate(self.algorithms):
            y = list()
            for borda_property in BordaProperty:
                values = self.results[algorithm][borda_property]
                y.append(sum(values) / len(values) * 100)
            plt.bar(X + i * gap, y, width=gap, label=algorithm.__name__)

        plt.legend(loc="best")
        if not save_only:
            plt.show()
        plt.savefig(self.path + "out/" + str(self.get_name()) + ".png")
