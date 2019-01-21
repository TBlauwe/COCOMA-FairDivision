from src.Algorithm.AbstractAlgorithm import AbstractAlgorithm

"""
This algorithm was introduced by Brams and Taylor (1996). In contrast to
the algorithms discussed so far, it considers players sequentially. Therefore, it
will generate at most two allocations, depending on which player is considered
first. The algorithm is extremely simple: when considering player m, it allocates
item lastm(U) to m’s opponent m. Despite its simplicity, this algorithm always
generates allocations that are max-min.

Variants : For working with more than 2 agents, we allocate item lastm(U) to 
the agent who appreciate the most this item and to even allocation (All agents must have the same number of items)
"""


class BottomUpAlgorithm(AbstractAlgorithm):

    def _compute(self, sequence):
        # On considère chaque agent en suivant la séquence
        counter = 1
        for agent_name in sequence:
            self.trace.append(print("----- Round " + str(counter) + "-----"))
            self.trace.append(print("Remaining sequence " + str(sequence[counter:])))

            # Récupération de l'agent
            agent = self.problem.agents[agent_name]
            self.trace.append(print("... Considering agent : " + agent))

            # Récupération de l'item le moins valué du lot par cet agent
            least_valued_item = agent.bottom(self.problem.get_unallocated_items())
            self.trace.append(print("... Least valued item : " + str(least_valued_item)))

            # Récupération des agents qui peuvent recevoir un item (tous le monde doit avoir le même nb d'items)
            eligible_agents = self.problem.get_eligible_agents()

            # Récupération de l'agent qui value le plus cet item
            receiver = self.problem.max_utility_from(least_valued_item, eligible_agents)
            self.trace.append(print("... Agent valuing this item the most : " + str(receiver)))

            # Allocation de l'item
            self.problem.allocate(least_valued_item, receiver)
            self.trace.append("... Giving item " + str(least_valued_item) + " to " + str(agent_name))

            counter += 1
        self.status = self.Status.SUCCEEDED
