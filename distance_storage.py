# src/algorithms/distance_storage.py
from typing import Dict, Set, Tuple, Optional
import networkx as nx

class DistanceStorage:
    """Main distance storage implementation."""
    
    def __init__(
        self,
        network: nx.Graph,
        landmarks: Set[str],
        balls: Dict[str, Set[str]],
        landmark_distances: Dict[str, Dict[str, int]]
    ):
        self.network = network
        self.landmarks = landmarks
        self.balls = balls
        self.landmark_distances = landmark_distances
        self.exact_distances = {}
        self.build_exact_distances()
        
    def build_exact_distances(self) -> None:
        """Precomputes exact distances for vertices in same/intersecting balls."""
        for center1, ball1 in self.balls.items():
            for center2, ball2 in self.balls.items():
                if center1 >= center2:
                    continue
                    
                # Compute distances for intersecting balls
                intersection = ball1.intersection(ball2)
                if intersection:
                    for v1 in ball1:
                        for v2 in ball2:
                            dist = nx.shortest_path_length(
                                self.network, v1, v2
                            )
                            self.exact_distances[(v1, v2)] = dist
                            self.exact_distances[(v2, v1)] = dist
                            
    def query_distance(self, s: str, t: str) -> int:
        """Queries distance between two vertices."""
        # Check if exact distance is available
        if (s, t) in self.exact_distances:
            return self.exact_distances[(s, t)]
            
        # Find nearest landmarks
        s_landmark = min(
            self.landmarks,
            key=lambda l: self.landmark_distances[l].get(s, float('inf'))
        )
        t_landmark = min(
            self.landmarks,
            key=lambda l: self.landmark_distances[l].get(t, float('inf'))
        )
        
        # Approximate distance using landmarks
        return (
            self.landmark_distances[s_landmark].get(s, 0) +
            nx.shortest_path_length(self.network, s_landmark, t_landmark) +
            self.landmark_distances[t_landmark].get(t, 0)
        )