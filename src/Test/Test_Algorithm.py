# coding: utf8

from src.Database import *
from src.Problem import *
from src.Sequence import *
from src.Algorithm.TestAlgorithm import TestAlgorithm


# ==============================================
# =============== INITIALIZATION ===============
# ==============================================

# Load database
db = Database()

# Define a problem
nbAgents = 3
nbItems = nbAgents * 2
test_pb = Problem("Test",
             db.get_random_agents_names(nbAgents),
             db.get_random_items_names(nbItems))

# Resolve a pb with an algorithm
test_algo = TestAlgorithm(test_pb)

# ==============================================
# =============== COMPUTATION ===============
# ==============================================

test_algo.compute()

# =======================================
# =============== TESTING ===============
# =======================================

print("|-=-=-=-=-=-=-=-=-= Testing -=-=-=-=-=-=-=-=-=-=|")

print(" --- SEQUENCES ---");

# Sequence data
seq = Sequence.generate_sequence(test_pb.agents, test_pb.items, SequenceType.ROUND_ROBIN)
print("RoundRobin", seq)

seq = Sequence.generate_sequence(test_pb.agents, test_pb.items, SequenceType.BALANCED)
print("Balanced", seq)

