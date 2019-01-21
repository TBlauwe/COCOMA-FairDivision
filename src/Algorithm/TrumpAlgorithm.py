from src.Algorithm.AbstractAlgorithm import AbstractAlgorithm

"""
This algorithm was developed by Pruhs and Woeginger (2012). It also considers
players sequentially and thus generates up to two allocations when each of the
two players is considered first.

Variante : Lorsque plus de deux joueurs sont considéres, l'item le moins préféré de tous les autres agents
mais le plus préféré par l'agent considéré lui est donné
"""


class TrumpAlgorithm(AbstractAlgorithm):

    def _compute(self, sequence):
        # On considère chaque agent en suivant la séquence
        counter = 1
        for rank in range(1, self.problem.number_of_items()+1, self.problem.number_of_agents()):
            self.trace.append("... Considering rank " + str(rank))

            for agent_name in sequence:
                self.trace.append("----- Round " + str(counter) + " -----")
                self.trace.append("Remaining sequence " + str(sequence[counter:]))

                # Récupération de l'agent
                agent = self.problem.agents[agent_name]
                self.trace.append("... Considering agent : " + str(agent))

                # Récupération des items non alloués
                unallocated_items = self.problem.get_unallocated_items()
                self.trace.append("... Unallocated items " + str(unallocated_items))

                # Récupération des items possibles
                h = agent.get_items_under_rank(unallocated_items, rank)

                if not h:
                    self.trace.append("!!! ABORT !!!  No envy free allocation")
                    self.status = self.Status.FAILED
                    self.reason = "No envy free allocation"
                    return

                # Récupération des autres agents
                other_agents_name = self.problem.get_other_agents(set(agent_name))

                # Récupération des items les moins valué par les autres agents
                least_valued_items = set()
                for other_agent_name in other_agents_name:
                    other_agent = self.problem.agents[other_agent_name]
                    least_valued_items.add(other_agent.bottom(self.problem.get_unallocated_items()))
                self.trace.append("... Least valued items by other agents : " + str(least_valued_items))

                # Récupération de l'item le plus valué par l'agent considéré
                most_valued_item = agent.top(least_valued_items)
                self.trace.append("... Most valued item : " + str(most_valued_item))

                # Allocation de l'item
                self.problem.allocate(most_valued_item, agent_name)
                self.trace.append("... Giving item " + str(most_valued_item) + " to " + str(agent_name))

                counter += 1

        self.status = self.Status.SUCCEEDED
