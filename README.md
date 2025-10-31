# Logistics Route Optimizer

This module models inter-city delivery routes across India and determines the most efficient path between major hubs using Dijkstra’s algorithm.

## Data
Synthetic dataset of 20 Indian cities with realistic road distances (km).

## Functions
- Builds weighted graph from CSV.
- Computes central hubs using degree centrality.
- Calculates shortest paths for chosen city pairs.
- Visualizes the national route network with NetworkX.

## Requirements
pandas  
networkx  
matplotlib

## Run
```bash
python logistics_optimizer.py
