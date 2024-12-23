# src/algorithms/neighborhood_sampler.py
from typing import Dict, Set
import random
import networkx as nx

class NeighborhoodSampler:
    """Implements second-level neighborhood sampling strategy."""
    
    def __init__(
        self, 
        network: nx.Graph,
        landmarks: Set[str],
        landmark_distances: Dict[str, Dict[str, int]]
    ):
        self.network = network
        self.landmarks = landmarks
        self.landmark_distances = landmark_distances
        self.n = network.number_of_nodes()
        
    def sample_neighborhood_vertices(self) -> Set[str]:
        """Samples vertices with probability n^(-2/3)."""
        p2 = self.n ** (-2/3)
        return {
            node for node in self.network.nodes()
            if random.random() < p2
        }
        
    def compute_balls(
        self, 
        sampled_vertices: Set[str]
    ) -> Dict[str, Set[str]]:
        """Computes neighborhood balls for sampled vertices."""
        balls = {}
        for vertex in sampled_vertices:
            nearest_landmark_dist = min(
                self.landmark_distances[l].get(vertex, float('inf'))
                for l in self.landmarks
            )
            
            # Collect vertices closer than nearest landmark
            ball = {
                v for v in self.network.nodes()
                if nx.shortest_path_length(
                    self.network, vertex, v
                ) < nearest_landmark_dist
            }
            balls[vertex] = ball
            
        return balls
