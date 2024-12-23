# src/experiments/benchmark_runner.py
import time
import psutil
import pandas as pd
from typing import Dict, Any, List
import networkx as nx
from ..algorithms.distance_oracle import DistanceOracle

class BenchmarkRunner:
    """Runs performance benchmarks on the implementation."""
    
    def __init__(self, network: nx.Graph, oracle: DistanceOracle):
        self.network = network
        self.oracle = oracle
        self.results: Dict[str, List[float]] = {
            'query_time': [],
            'memory_usage': []
        }
        
    def measure_query_time(
        self,
        num_queries: int = 1000
    ) -> Dict[str, float]:
        """Measures average query time."""
        nodes = list(self.network.nodes())
        pairs = [
            (nodes[i], nodes[j])
            for i in range(num_queries)
            for j in range(i + 1, min(i + 2, len(nodes)))
        ]
        
        start_time = time.time()
        for s, t in pairs:
            self.oracle.query_distance(s, t)
        end_time = time.time()
        
        avg_query_time = (end_time - start_time) / len(pairs)
        self.results['query_time'].append(avg_query_time)
        
        return {
            'avg_query_time': avg_query_time,
            'num_queries': len(pairs)
        }
        
    def measure_memory_usage(self) -> Dict[str, float]:
        """Measures memory usage of the oracle."""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        memory_usage = memory_info.rss / 1024 / 1024  # Convert to MB
        self.results['memory_usage'].append(memory_usage)
        
        return {
            'memory_usage_mb': memory_usage
        }
        
    def run_scalability_test(
        self,
        network_sizes: List[int]
    ) -> pd.DataFrame:
        """Tests scalability with different network sizes."""
        results = []
        
        for size in network_sizes:
            # Create subgraph of specified size
            nodes = list(self.network.nodes())[:size]
            subgraph = self.network.subgraph(nodes)
            
            # Initialize oracle for subgraph
            from ..algorithms.landmark_sampler import LandmarkSampler
            from ..algorithms.neighborhood_sampler import NeighborhoodSampler
            
            landmark_sampler = LandmarkSampler(subgraph)
            landmarks = landmark_sampler.sample_landmarks()
            landmark_distances = landmark_sampler.compute_landmark_distances()
            
            neighborhood_sampler = NeighborhoodSampler(
                subgraph, landmarks, landmark_distances
            )
            neighborhood_vertices = (
                neighborhood_sampler.sample_neighborhood_vertices()
            )
            balls = neighborhood_sampler.compute_balls(neighborhood_vertices)
            
            subgraph_oracle = DistanceOracle(
                subgraph, landmarks, balls, landmark_distances
            )
            
            # Measure performance
            query_time = self.measure_query_time()['avg_query_time']
            memory_usage = self.measure_memory_usage()['memory_usage_mb']
            
            results.append({
                'network_size': size,
                'query_time': query_time,
                'memory_usage': memory_usage,
                'num_landmarks': len(landmarks),
                'num_balls': len(balls)
            })
            
        return pd.DataFrame(results)
