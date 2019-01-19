# coding: utf8

from src.Database import *
from src.Problem import *
from src.Sequence import *
from src.Utility import *


# ==========================================
# =============== PARAMETERS ===============
# ==========================================
NUMBER_OF_AGENTS = 3
NUMBER_OF_ITEMS = NUMBER_OF_AGENTS * 2

# ==============================================
# =============== INITIALIZATION ===============
# ==============================================

# Load database
db = Database()

# Define a problem
pb = Problem("Test",
             db.get_random_agents_names(NUMBER_OF_AGENTS),
             db.get_random_items_names(NUMBER_OF_ITEMS))

# Visualize data
print(pb)

# Sequence data
seq = Sequence.generate_sequence(pb.agents, pb.items, SequenceType.ROUND_ROBIN)
print(seq)

seq = Sequence.generate_sequence(pb.agents, pb.items, SequenceType.BALANCED)
print(seq)
