# src/network.py
import networkx as nx
from typing import List, Dict, Optional
import random

class SocialNetwork:
    def __init__(self, num_agents: int = 0):
        self.agents = []
        self.graph = nx.Graph()
        self.network_stats = {}

    def add_agent(self, agent):
        self.agents.append(agent)
        self.graph.add_node(agent.id)

    def remove_agent(self, agent):
        self.agents.remove(agent)
        self.graph.remove_node(agent.id)

    def update_edge(self, agent_a, agent_b, weight: float):
        self.graph.add_edge(agent_a.id, agent_b.id, weight=weight)

    def get_network_stats(self) -> Dict:
        self.network_stats = {
            "density": nx.density(self.graph),
            "average_clustering": nx.average_clustering(self.graph),
            "triadic_closure": self.analyze_triadic_closure(),
        }
        return self.network_stats

    def analyze_triadic_closure(self) -> float:
        triads = 0
        closed_triads = 0
        
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    triads += 1
                    if self.graph.has_edge(neighbors[i], neighbors[j]):
                        closed_triads += 1
        
        return closed_triads / triads if triads > 0 else 0.0

    def select_random_pairs(self, num_pairs: int) -> List[tuple]:
        all_possible_pairs = [
            (a, b) for i, a in enumerate(self.agents)
            for b in self.agents[i+1:]
        ]
        return random.sample(all_possible_pairs, 
                           min(num_pairs, len(all_possible_pairs)))
