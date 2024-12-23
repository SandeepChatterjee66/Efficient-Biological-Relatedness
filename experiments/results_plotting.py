
# src/visualization/results_plotter.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List, Tuple

class ResultsPlotter:
    """Visualizes experimental results and performance metrics."""
    
    def plot_aspl_distribution(
        self,
        pathway_results: Dict[str, Dict],
        save_path: str = None
    ) -> None:
        """Plots ASPL distribution for different pathways."""
        data = []
        for pathway, results in pathway_results.items():
            distances = [d for _, _, d in results['distances']]
            data.extend([(pathway, d) for d in distances])
            
        df = pd.DataFrame(data, columns=['Pathway', 'ASPL'])
        
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='Pathway', y='ASPL', data=df)
        plt.xticks(rotation=45)
        plt.title('ASPL Distribution by Pathway')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        
    def plot_performance_comparison(
        self,
        performance_metrics: List[Dict[str, float]],
        method_names: List[str],
        save_path: str = None
    ) -> None:
        """Plots performance comparison between methods."""
        metrics = ['precision', 'recall', 'f1_score']
        
        data = []
        for method, perf in zip(method_names, performance_metrics):
            for metric in metrics:
                data.append((method, metric, perf[metric]))
                
        df = pd.DataFrame(data, columns=['Method', 'Metric', 'Value'])
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Method', y='Value', hue='Metric', data=df)
        plt.xticks(rotation=45)
        plt.title('Performance Comparison')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        plt.close()

