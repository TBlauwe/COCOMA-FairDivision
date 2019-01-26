# coding: utf8

"""
Exemple de fichier permettant de lancer un benchmark sur un jeu de données générées avec les algorithmes spécifiés
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
initial_pb = Problem(db.get_random_agents_names(nbAgents), db.get_random_items_names(nbItems))

# Create a set of different instances of a problem
algorithms = [BottomUpAlgorithm, TrumpAlgorithm]
limit = 100
pb_set = ProblemSet(initial_pb, algorithms, limit, "../../")

# Test with a specific sequence
seq = Sequence.generate(initial_pb, SequenceType.ROUND_ROBIN, True)
pb_set.run(seq)
pb_set.show_results()

trump_algo = TrumpAlgorithm(initial_pb)
seq = Sequence.generate(initial_pb, SequenceType.ROUND_ROBIN, True)
trump_algo.compute(seq)
