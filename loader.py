

# src/data/loader.py
import pandas as pd
import networkx as nx
from pathlib import Path
from typing import Tuple, Dict, Set

class BioGridLoader:
    """Loads and processes BioGRID interaction data."""
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.validate_path()
        
    def validate_path(self) -> None:
        """Validates that the data path exists."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data path not found: {self.data_path}")
            
    def load_interactions(self) -> pd.DataFrame:
        """Loads raw interaction data from BioGRID."""
        df = pd.read_csv(self.data_path, sep='\t')
        required_cols = ['Gene1', 'Gene2', 'Interaction_Type']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")
        return df
        
    def filter_direct_interactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filters for direct physical interactions."""
        direct_types = {'physical', 'direct interaction'}
        return df[df['Interaction_Type'].str.lower().isin(direct_types)]
        
    def build_network(self, df: pd.DataFrame) -> nx.Graph:
        """Constructs NetworkX graph from interaction data."""
        G = nx.Graph()
        for _, row in df.iterrows():
            G.add_edge(row['Gene1'], row['Gene2'])
        return G
        
    def process_data(self) -> Tuple[nx.Graph, Dict[str, Set[str]]]:
        """Main processing pipeline for BioGRID data."""
        df = self.load_interactions()
        df = self.filter_direct_interactions(df)
        
        # Create gene-pathway mappings
        gene_pathways = {}
        for gene in set(df['Gene1']).union(set(df['Gene2'])):
            # In practice, you'd load this from KEGG/Reactome
            gene_pathways[gene] = set()
            
        network = self.build_network(df)
        return network, gene_pathways