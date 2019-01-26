# coding: utf8

"""
Exemple de fichier permettant de lancer résoudre un problème avec un algorithme donnée
"""

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
pb = Problem(db.get_random_agents_names(nbAgents), db.get_random_items_names(nbItems))

# Define an algorithm
trump_algo = TrumpAlgorithm(pb)

# Solve the problem according to a specific sequence
seq = Sequence.generate(pb, SequenceType.ROUND_ROBIN, True)
trump_algo.compute(seq)
