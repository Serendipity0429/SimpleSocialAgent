# src/visualization.py
import networkx as nx
import matplotlib.pyplot as plt
from typing import Optional

class NetworkVisualizer:
    def __init__(self, social_network):
        self.social_network = social_network
        self.pos = None

    def plot_network(self, figure_size: tuple = (10, 10),
                    with_labels: bool = True,
                    node_size: int = 500,
                    save_path: Optional[str] = None):
        plt.figure(figsize=figure_size)
        
        # Get the graph
        G = self.social_network.graph
        
        # Calculate layout if not already calculated
        if self.pos is None:
            self.pos = nx.spring_layout(G)
        
        # Get edge weights for width and color
        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
        
        # Draw the network
        nx.draw_networkx_edges(G, self.pos, edge_color=edge_weights,
                             edge_cmap=plt.cm.Blues, width=2)
        nx.draw_networkx_nodes(G, self.pos, node_color='lightblue',
                             node_size=node_size)
        
        if with_labels:
            nx.draw_networkx_labels(G, self.pos)
        
        plt.title("Social Network Visualization")
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        
        plt.close()

    def plot_network_evolution(self, metrics_history: dict,
                             save_path: Optional[str] = None):
        plt.figure(figsize=(12, 6))
        
        for metric, values in metrics_history.items():
            plt.plot(values, label=metric)
        
        plt.xlabel("Time Steps")
        plt.ylabel("Metric Value")
        plt.title("Network Evolution")
        plt.legend()
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        
        plt.close()
