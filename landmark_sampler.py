# src/algorithms/landmark_sampler.py
from typing import Set, List
import random
import networkx as nx
import numpy as np

class LandmarkSampler:
    """Implements first-level landmark sampling strategy."""
    
    def __init__(self, network: nx.Graph):
        self.network = network
        self.n = network.number_of_nodes()
        self.landmarks: Set[str] = set()
        
    def sample_landmarks(self) -> Set[str]:
        """Samples landmarks with probability n^(-1/3)."""
        p1 = self.n ** (-1/3)
        self.landmarks = {
            node for node in self.network.nodes()
            if random.random() < p1
        }
        return self.landmarks
        
    def compute_landmark_distances(self) -> Dict[str, Dict[str, int]]:
        """Computes shortest paths from landmarks to all nodes."""
        distances = {}
        for landmark in self.landmarks:
            distances[landmark] = nx.single_source_shortest_path_length(
                self.network, landmark
            )
        return distances