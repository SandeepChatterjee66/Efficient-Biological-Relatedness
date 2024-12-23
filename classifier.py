# src/analysis/relatedness_classifier.py
from typing import List, Tuple, Dict
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

class RelatednessClassifier:
    """Classifies gene pairs as related/unrelated based on ASPL."""
    
    def __init__(self, threshold: float = None):
        self.threshold = threshold
        
    def fit_threshold(
        self,
        known_related: List[Tuple[str, str, float]],
        known_unrelated: List[Tuple[str, str, float]]
    ) -> None:
        """Fits optimal threshold using known relations."""
        related_aspls = [d for _, _, d in known_related]
        unrelated_aspls = [d for _, _, d in known_unrelated]
        
        # Simple threshold as mean between averages
        self.threshold = (
            np.mean(related_aspls) + np.mean(unrelated_aspls)
        ) / 2
        
    def predict_relatedness(
        self,
        gene_pairs: List[Tuple[str, str, float]]
    ) -> List[bool]:
        """Predicts if gene pairs are related based on ASPL."""
        if self.threshold is None:
            raise ValueError("Threshold not set. Call fit_threshold first.")
            
        return [
            dist <= self.threshold
            for _, _, dist in gene_pairs
        ]
        
    def evaluate_performance(
        self,
        true_labels: List[bool],
        predicted_labels: List[bool]
    ) -> Dict[str, float]:
        """Evaluates classification performance."""
        precision, recall, f1, _ = precision_recall_fscore_support(
            true_labels,
            predicted_labels,
            average='binary'
        )
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
