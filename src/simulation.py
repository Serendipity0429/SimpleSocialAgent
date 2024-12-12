# src/simulation.py
from typing import Dict, List, Optional
import time
from .network import SocialNetwork
from .visualization import NetworkVisualizer

class Simulation:
    def __init__(self, config):
        self.config = config
        self.network = SocialNetwork()
        self.visualizer = NetworkVisualizer(self.network)
        self.metrics_history = {
            "density": [],
            "clustering": [],
            "triadic_closure": []
        }

    def initialize_network(self):
        from .agent import Agent
        for i in range(self.config.num_agents):
            agent = Agent(str(i), self.config.personality_generator)
            self.network.add_agent(agent)

    def run(self, steps: int):
        for step in range(steps):
            print(f"Running simulation step {step + 1}/{steps}")
            
            # Select random pairs for interaction
            pairs = self.network.select_random_pairs(
                self.config.interactions_per_step)
            
            # Simulate interactions
            for agent_a, agent_b in pairs:
                score = agent_a.interact_with(agent_b, self.config.llm_client)
                self.network.update_edge(agent_a, agent_b, score)
            
            # Calculate and store network metrics
            stats = self.network.get_network_stats()
            for metric, value in stats.items():
                if metric in self.metrics_history:
                    self.metrics_history[metric].append(value)
            
            # Visualize network state if configured
            if step % self.config.visualization_interval == 0:
                self.visualize_network(step)

    def visualize_network(self, step: int):
        self.visualizer.plot_network(
            save_path=f"{self.config.output_dir}/network_step_{step}.png"
        )
        
    def get_final_analysis(self) -> Dict:
        return {
            "final_stats": self.network.get_network_stats(),
            "metrics_history": self.metrics_history
        }

    def save_results(self):
        results = self.get_final_analysis()
        # Save metrics history plot
        self.visualizer.plot_network_evolution(
            self.metrics_history,
            save_path=f"{self.config.output_dir}/metrics_evolution.png"
        )
        return results
