# coding: utf8

from src.Database import *
from src.Problem import *
from src.Sequence import *
from src.Algorithm.BottomUpAlgorithm import BottomUpAlgorithm

# Load database
db = Database()

# Define a problem
nbAgents = 3
nbItems = nbAgents * 2
a3_r2_pb = Problem("a3_r2",
             db.get_random_agents_names(nbAgents),
             db.get_random_items_names(nbItems))

# Resolve a pb with an algorithm
bottom_up_algo = BottomUpAlgorithm(a3_r2_pb)
bottom_up_algo.compute(Sequence.generate(bottom_up_algo.problem, SequenceType.ROUND_ROBIN))
