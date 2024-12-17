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
        
    def initialize_edges(self, initial_weight: float = 0.2):
        num_pairs = len(self.agents) * (len(self.agents) - 1) // 2
        num_pairs = int(num_pairs * initial_weight)
        pairs = self.select_random_pairs(num_pairs)
        for agent_a, agent_b in pairs:
            random_weight = random.random()
            self.update_edge(agent_a, agent_b, random.random())
            agent_a.update_relationship(agent_b, random_weight)
            agent_b.update_relationship(agent_a, random_weight)
        # Ensure all agents have at least one connection
        for agent in self.agents:
            if not list(self.graph.neighbors(agent.id)):
                other_agent = random.choice(self.agents)
                random_weight = random.random()
                self.update_edge(agent, other_agent, random_weight)
                agent.update_relationship(other_agent, random_weight)
                other_agent.update_relationship(agent, random_weight)

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
            (a, b) for a in range(len(self.agents)) 
            for b in range(a+1, len(self.agents))
        ]
        results = random.sample(all_possible_pairs, 
                           min(num_pairs, len(all_possible_pairs)))
        results = [(self.agents[a], self.agents[b]) for a, b in results]
        return results