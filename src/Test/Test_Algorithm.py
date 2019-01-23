# coding: utf8

from src.Database import *
from src.Problem import *
from src.ProblemSet import *
from src.Sequence import *
from src.Algorithm import *

# Load database
db = Database()

# Define a problem
nbAgents = 3
nbItems = nbAgents * 2
initial_pb = Problem("test",
                           db.get_random_agents_names(nbAgents),
                           db.get_random_items_names(nbItems))

pb_set = ProblemSet(initial_pb, 720)

seq = Sequence.generate(initial_pb, SequenceType.ROUND_ROBIN, True)

for index, problem in enumerate(pb_set.problems):
    bottom_up_algo = BottomUpAlgorithm(problem)
    bottom_up_algo.compute(seq, False)
    pb_set.add_results(bottom_up_algo)

pb_set.show_results()
