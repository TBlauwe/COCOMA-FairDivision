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
a3_r2_pb = Problem("a3_r2",
             db.get_random_agents_names(nbAgents),
             db.get_random_items_names(nbItems))


# Resolve a pb with an algorithm
#trump_algo = TrumpAlgorithm(a3_r2_pb)
#trump_algo.compute(Sequence.generate(trump_algo.problem, SequenceType.ROUND_ROBIN, True), False)
#print(trump_algo)

#trump_algo = TrumpAlgorithm(a6_r2_pb)
#trump_algo.compute(Sequence.generate(trump_algo.problem, SequenceType.ROUND_ROBIN, True), False)
#print(trump_algo)

bottom_up_algo = BottomUpAlgorithm(a3_r2_pb)
bottom_up_algo.compute(Sequence.generate(bottom_up_algo.problem, SequenceType.ROUND_ROBIN, True), False)


# Define a problem
nbAgents = 3
nbItems = nbAgents * 2
initial_pb = Problem("test",
                           db.get_random_agents_names(nbAgents),
                           db.get_random_items_names(nbItems))

pb_set = ProblemSet(initial_pb, 720)

seq = Sequence.generate(initial_pb, SequenceType.ROUND_ROBIN, True)
for index, problem in enumerate(pb_set.problems):
    print("========== Round " + str(index) + "==========")
    bottom_up_algo = BottomUpAlgorithm(problem)
    bottom_up_algo.compute(seq, False)
