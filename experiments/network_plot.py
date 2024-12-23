# src/visualization/network_plotter.py
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Set
import seaborn as sns

class NetworkPlotter:
    """Visualizes network properties and analysis results."""
    
    def __init__(self, network: nx.Graph):
        self.network = network
        plt.style.use('seaborn')
        
    def plot_degree_distribution(self, save_path: str = None) -> None:
        """Plots the degree distribution of the network."""
        degrees = [d for _, d in self.network.degree()]
        
        plt.figure(figsize=(10, 6))
        plt.hist(degrees, bins=50, alpha=0.75)
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('Network Degree Distribution')
        plt.yscale('log')
        
        if save_path:
            plt.savefig(save_path)
        plt.close()
        
    def plot_landmark_coverage(
        self,
        landmarks: Set[str],
        save_path: str = None
    ) -> None:
        """Visualizes landmark distribution in network."""
        pos = nx.spring_layout(self.network)
        
        plt.figure(figsize=(12, 8))
        # Plot regular nodes
        nx.draw_networkx_nodes(
            self.network,
            pos,
            node_color='lightblue',
            node_size=100,
            alpha=0.6
        )
        # Highlight landmarks
        nx.draw_networkx_nodes(
            self.network,
            pos,
            nodelist=list(landmarks),
            node_color='red',
            node_size=200,
            alpha=0.8
        )
        nx.draw_networkx_edges(
            self.network,
            pos,
            alpha=0.2
        )
        
        plt.title('Network with Landmark Nodes')
        if save_path:
            plt.savefig(save_path)
        plt.close()
