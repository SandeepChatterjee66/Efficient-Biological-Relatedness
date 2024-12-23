# src/analysis/aspl_calculator.py
from typing import List, Tuple, Dict
import networkx as nx
import numpy as np
from ..algorithms.distance_oracle import DistanceStorage

class ASPLCalculator:
    """Calculates Average Shortest Path Length metrics."""
    
    def __init__(
        self,
        oracle: DistanceOracle,
        gene_pathways: Dict[str, Set[str]]
    ):
        self.oracle = oracle
        self.gene_pathways = gene_pathways
        
    def calculate_gene_pair_aspl(
        self,
        gene1: str,
        gene2: str
    ) -> float:
        """Calculates ASPL between two genes."""
        return self.oracle.query_distance(gene1, gene2)
        
    def calculate_pathway_aspl(
        self,
        pathway: str
    ) -> Tuple[float, List[Tuple[str, str, float]]]:
        """Calculates average ASPL for genes in a pathway."""
        pathway_genes = {
            gene for gene, pathways in self.gene_pathways.items()
            if pathway in pathways
        }
        
        distances = []
        for g1 in pathway_genes:
            for g2 in pathway_genes:
                if g1 >= g2:
                    continue
                dist = self.calculate_gene_pair_aspl(g1, g2)
                distances.append((g1, g2, dist))
                
        avg_aspl = np.mean([d for _, _, d in distances])
        return avg_aspl, distances
