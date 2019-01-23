import random
import math
import matplotlib.pyplot as plt
from src.Problem import *


class ProblemSet(object):
    """
    Permet de générér plusieurs instances d'un problème avec les mêmes paramètrs (nombre d'agents et d'items), mais avec
    des changements au niveau des préférences des agents. Au plus N! instances possibles (N = nombre d'items)
    """

    def __init__(self, initial_problem, number=math.inf):
        self.initial_problem = initial_problem
        self.problems = list()
        self.results = dict()
        self.borda_properties_matrix = dict()

        for borda_property in BordaProperty:
            self.borda_properties_matrix[borda_property] = list()

        all_rankings = [list(x) for x in itertools.permutations(self.initial_problem.items)]

        rankings_per_agent = dict()
        for name in self.initial_problem.get_agents_name():
            random_rankings = all_rankings[:]
            random.shuffle(random_rankings)
            rankings_per_agent[name] = random_rankings

        for i in range(min(len(all_rankings), number)):
            agents = dict()
            for name in self.initial_problem.get_agents_name():
                agent = Agent(name, self.initial_problem)
                agent.set_borda_ranks(rankings_per_agent[name].pop())
                agents[name] = agent
            problem = Problem(self.initial_problem.name,
                              self.initial_problem.get_agents_name(),
                              self.initial_problem.items,
                              False)
            problem.force_agents(agents)
            self.problems.append(problem)

        return

    def add_results(self, algorithm):
        for borda_property in BordaProperty:
            self.borda_properties_matrix[borda_property].append(algorithm.problem.borda_properties[borda_property][0])

    def show_results(self):
        fig = plt.figure()
        plt.style.use('ggplot')
        plt.title(self.initial_problem.name)
        plt.yticks(range(0,101,10))
        ax = plt.subplot(111)
        ax.set_ylim([0, 100])

        y = list()
        for borda_property in BordaProperty:
            values = self.borda_properties_matrix[borda_property]
            y.append(sum(values) / len(values) * 100)

        ax.bar(BordaProperty.values(), y)
        plt.show()
