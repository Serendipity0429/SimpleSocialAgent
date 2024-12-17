# src/simulation.py
from typing import Dict, List, Optional, Union
import time
import glob
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

    def initialize_network(self, initial_weight: float = 0.2):
        from .agent import Agent
        for i in range(self.config.num_agents):
            agent = Agent(str(i), self.config.personality_generator)
            self.network.add_agent(agent)
        self.network.initialize_edges(initial_weight)

    def run(self, steps: int):
        for step in range(steps):
            print(f"Running simulation step {step + 1}/{steps}")
            
            # Select random pairs for interaction
            pairs = self.network.select_random_pairs(
                self.config.interactions_per_step)
            
            # Simulate interactions
            for agent_a, agent_b in pairs:
                score = agent_a.interact_with(agent_b, self.config.llm_client)
                score = 0 if score < self.config.threshold else score # Thresholding
                self.network.update_edge(agent_a, agent_b, score)
            
            # Calculate and store network metrics
            stats = self.network.get_network_stats()
            for metric, value in stats.items():
                if metric in self.metrics_history:
                    self.metrics_history[metric].append(value)
                    
            # Print network statistics
            print("Network Statistics:", end=" ")
            for metric, value in stats.items():
                print(f"{metric}: {value:.3f}", end=", ")
            print()
            
            # Visualize network state if configured
            if step % self.config.visualization_interval == 0:
                self.visualize_network(step + 1)
        # Plot final network state
        self.visualize_network(step + 1, final=True)

    def visualize_network(self, step: Union[str, int], final: bool = False):
        if final:
            self.visualizer.plot_network(
                save_path=f"{self.config.output_dir}/final_network.png"
            )
        else:
            self.visualizer.plot_network(
            save_path=f"{self.config.output_dir}/network_step_{step}.png"
        )
        
        
    def get_final_analysis(self) -> Dict:
        return {
            "final_stats": self.network.get_network_stats(),
            "metrics_history": self.metrics_history
        }

    def save_results(self, animation: bool = True) -> Dict:
        results = self.get_final_analysis()
        
        all_plots = sorted(glob.glob(f"{self.config.output_dir}/network_step_*.png")) if animation else None
        
        # Save metrics history plot
        self.visualizer.plot_network_evolution(
            self.metrics_history,
            save_dir=self.config.output_dir,
            all_plots=all_plots
        )
        return results