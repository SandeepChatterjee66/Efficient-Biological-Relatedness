# src/utils/validators.py
from typing import Any, Dict, Set
import networkx as nx

def validate_network(network: nx.Graph) -> None:
    """Validates network properties."""
    if not isinstance(network, nx.Graph):
        raise TypeError("Network must be a NetworkX Graph")
        
    if not nx.is_connected(network):
        raise ValueError("Network must be connected")
        
def validate_landmarks(
    landmarks: Set[str],
    network: nx.Graph
) -> None:
    """Validates landmark properties."""
    if not landmarks.issubset(network.nodes()):
        raise ValueError("Landmarks must be nodes in the network")
        
def validate_config(config: Dict[str, Any]) -> None:
    """Validates configuration parameters."""
    required_keys = {'data_path', 'pathways_to_analyze'}
    if not all(key in config for key in required_keys):
        raise ValueError(f"Missing required config keys: {required_keys}")
        
    if not isinstance(config['pathways_to_analyze'], list):
        raise TypeError("pathways_to_analyze must be a list")