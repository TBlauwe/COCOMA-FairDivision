# coding: utf8

"""
Multi run Benchmark
"""

from src.Database import *
from src.Problem import *
from src.ProblemSet import *
from src.Sequence import *
from src.Algorithm import *

limit = 10000
minNbAgent = 2
maxNbAgent = 4
minNbItems = 2
maxNbItems = 4

# Load database
db = Database()

for i in range(minNbAgent, maxNbAgent + 1):
    for j in range(minNbItems, maxNbItems + 1):
        # Define a problem
        nbAgents = i
        nbItems = nbAgents * j
        initial_pb = Problem(db.get_random_agents_names(nbAgents), db.get_random_items_names(nbItems))

        # Create a set of different instances of a problem
        algorithms = [BottomUpAlgorithm, TrumpAlgorithm]
        pb_set = ProblemSet(initial_pb, algorithms, limit, "../../")

        # Test with a specific sequence
        seq = Sequence.generate(initial_pb, SequenceType.BALANCED)
        pb_set.run(seq)
        pb_set.show_results(True)
