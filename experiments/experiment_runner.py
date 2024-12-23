
# src/experiments/experiment_runner.py
from typing import Dict, Any
import yaml
import logging
from pathlib import Path
from ..data.loader import BioGridLoader
from ..algorithms.landmark_sampler import LandmarkSampler
from ..algorithms.neighborhood_sampler import NeighborhoodSampler
from ..algorithms.distance_oracle import DistanceOracle
from ..analysis.aspl_calculator import ASPLCalculator
from ..analysis.relatedness_classifier import RelatednessClassifier

class ExperimentRunner:
    """Runs the complete experimental pipeline."""
    
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.logger = logging.getLogger(__name__)
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads experiment configuration."""
        with open(config_path) as f:
            return yaml.safe_load(f)
            
    def run_experiment(self) -> Dict[str, Any]:
        """Executes the complete experimental pipeline."""
        results = {}
        
        # Load and process data
        loader = BioGridLoader(self.config['data_path'])
        network, gene_pathways = loader.process_data()
        self.logger.info(f"Loaded network with {network.number_of_nodes()} nodes")
        
        # Sample landmarks
        landmark_sampler = LandmarkSampler(network)
        landmarks = landmark_sampler.sample_landmarks()
        landmark_distances = landmark_sampler.compute_landmark_distances()
        self.logger.info(f"Sampled {len(landmarks)} landmarks")
        
        # Sample neighborhoods
        neighborhood_sampler = NeighborhoodSampler(
            network, landmarks, landmark_distances
        )
        neighborhood_vertices = neighborhood_sampler.sample_neighborhood_vertices()
        balls = neighborhood_sampler.compute_balls(neighborhood_vertices)
        self.logger.info(f"Created {len(balls)} neighborhood balls")
        
        # Build distance oracle
        oracle = DistanceOracle(
            network, landmarks, balls, landmark_distances
        )
        
        # Calculate ASPLs
        calculator = ASPLCalculator(oracle, gene_pathways)
        classifier = RelatednessClassifier()
        
        # Run pathway analysis
        pathway_results = {}
        for pathway in self.config['pathways_to_analyze']:
            avg_aspl, distances = calculator.calculate_pathway_aspl(pathway)
            pathway_results[pathway] = {
                'avg_aspl': avg_aspl,
                'distances': distances
            }
            
        results['pathway_results'] = pathway_results
        
        # Evaluate classification performance
        if 'known_relations' in self.config:
            known_related = [
                (g1, g2, calculator.calculate_gene_pair_aspl(g1, g2))
                for g1, g2 in self.config['known_relations']['related']
            ]
            known_unrelated = [
                (g1, g2, calculator.calculate_gene_pair_aspl(g1, g2))
                for g1, g2 in self.config['known_relations']['unrelated']
            ]
            
            classifier.fit_threshold(known_related, known_unrelated)
            
            # Evaluate on test set
            test_pairs = [
                (g1, g2, calculator.calculate_gene_pair_aspl(g1, g2))
                for g1, g2 in self.config['known_relations']['test']
            ]
            true_labels = self.config['known_relations']['test_labels']
            predicted_labels = classifier.predict_relatedness(test_pairs)
            
            performance = classifier.evaluate_performance(
                true_labels, predicted_labels
            )
            results['classification_performance'] = performance
            
        return results
