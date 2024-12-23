# README.md
# Biological Relatedness Analysis

This repository contains the implementation of an efficient data structure and algorithms for analyzing biological relatedness in protein-protein interaction networks. The implementation is based on a two-level sampling approach that enables scalable computation of shortest path distances.

Problem with earlier approax approaches is that they provide 3x approximation not suitable for classification
Problem with a

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.experiments.experiment_runner import ExperimentRunner

# Run complete experimental pipeline
runner = ExperimentRunner('config/config.yaml')
results = runner.run_experiment()
```

## Structure

- `/`: Source code Root
  - `data/`: Data loading and preprocessing
  - `algorithms/`: Core algorithmic implementations
  - `analysis/`: Analysis tools
 
  - `experiments/`: Experiment runners
         - `visualization/`: Plotting utilities
  - `utils/`: Utility functions
- `tests/`: Unit tests
- `config/`: Configuration files

## Citation

If you use this code in your research, please cite this github repo

```
https://github.com/SandeepChatterjee66/Efficient-Biological-Relatedness
```