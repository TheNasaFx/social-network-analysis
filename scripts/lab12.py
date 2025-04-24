# Step 1: Install and Import Required Libraries
# - dynetx: For dynamic network modeling.
# - networkx: For generating synthetic static graphs.
# - random: For random graph generation.
# - No need for Google Drive since we're generating data synthetically.


import dynetx as dn
import networkx as nx
import random
import dynetx.algorithms as al

# Step 2: Generate Synthetic Dynamic Network Data
# - Instead of reading from CSV files, we generate synthetic graphs using NetworkX.
# - For each timestamp (1 to 8), we create an Erdos-Renyi random graph with 100 nodes and a probability of edge creation (p=0.05).
# - These graphs simulate the evolution of a network over time.

g = dn.DynGraph()  # Create an empty dynamic graph

for t in range(1, 9):
    # Generate a random Erdos-Renyi graph with 100 nodes and edge probability 0.05
    er = nx.erdos_renyi_graph(n=100, p=0.05, seed=t)  # Use timestamp as seed for reproducibility
    # Add the edges as interactions at timestamp t
    g.add_interactions_from(er.edges, t=t)

# Step 3: Analyze Snapshots
# - List all snapshot timestamps.
# - Access a specific snapshot (e.g., at t=1) and check its properties.
# - Create a time window (e.g., from t=0 to t=3) and analyze its properties.

print("Snapshot IDs:", g.temporal_snapshots_ids())  # List all snapshot timestamps

g1 = g.time_slice(1)  # Get the snapshot at t=1
print("Snapshot at t=1:", type(g1), g1.number_of_nodes(), g1.number_of_edges())

g0_3 = g.time_slice(0, 3)  # Get a time window from t=0 to t=3
print("Time window (0-3):", type(g0_3), g0_3.number_of_nodes(), g0_3.number_of_edges(), g0_3.interactions_per_snapshots())

# Convert a snapshot to a static NetworkX graph for further analysis
g1_flat = nx.Graph(g1.edges())
print("Flattened snapshot at t=1:", type(g1_flat), g1_flat.number_of_nodes(), g1_flat.number_of_edges())

# Step 4: Dynamic Network Metrics
# - Inter Event Time (Global): Distribution of time between new interactions.
# - Inter Event Time (Node): Time between interactions for a specific node (e.g., node "0").
# - Inter Event Time (Edge): Time between interactions for a specific edge (e.g., between nodes "0" and "1").

# Global inter event time
r = g.inter_event_time_distribution()
print("Global inter event time:", r)

# Node-specific inter event time for node 0
r = g.inter_event_time_distribution(0)
print("Node (0) inter event time:", r)

# Edge-specific inter event time between nodes 0 and 1
u, v = 0, 1
if g.has_edge(u, v):
    r = g.inter_event_time_distribution(u, v)
    print(f"Edge ({u}, {v}) inter event time:", r)
else:
    print(f"Edge ({u}, {v}) does not exist in the graph")
    # Find the first connected edge in the graph
    for edge in g.edges():
        u, v = edge
        r = g.inter_event_time_distribution(u, v)
        print(f"Using connected edge ({u}, {v}) inter event time:", r)
        break

# Step 5: Additional Metrics
# - Degree: Check the degree of a node at a specific timestamp.
# - Coverage: Ratio of existing nodes to possible nodes.
# - Node Contribution: Contribution of a specific node.
# - Edge Contribution: Contribution of a specific edge.
# - Node Pair Uniformity: Overlap of presence times between two nodes.
# - Density: Overall temporal network density.
# - Node Density: Density for a specific node.
# - Pair Density: Density for a specific pair of nodes.
# - Snapshot Density: Density at each timestamp.
# - Path Analysis: Find time-respecting paths between two nodes.

# Degree of a node at a specific time
print("Degree of node 0 at t=2:", g.degree(t=2).get("0", 0))

# Coverage
print("Coverage:", g.coverage())

# Node contribution
print("Node contribution of node 0:", g.node_contribution(0))

# Edge contribution
if g.has_edge(u, v):
    print(f"Edge contribution ({u}, {v}):", g.edge_contribution(u, v))
else:
    print(f"Edge ({u}, {v}) does not exist, cannot calculate contribution")

# Node pair uniformity
if g.has_edge(u, v):
    print(f"Node pair uniformity ({u}, {v}):", g.node_pair_uniformity(u, v))
else:
    print(f"Edge ({u}, {v}) does not exist, cannot calculate uniformity")

# Density
print("Overall density:", g.density())

# Node density
print(f"Node density ({u}):", g.node_density(u))

# Pair density
if g.has_edge(u, v):
    print(f"Pair density ({u}, {v}):", g.pair_density(u, v))
else:
    print(f"Edge ({u}, {v}) does not exist, cannot calculate pair density")

# Snapshot density for each timestamp
for t in g.temporal_snapshots_ids():
    print(f"Snapshot density at t={t}: {g.snapshot_density(t)}")

# Path analysis between two nodes
if g.has_edge(u, v):
    paths = al.time_respecting_paths(g, u, v, start=1, end=5)
    print("Time-respecting paths:", paths[0] if paths else "No paths found")
else:
    print(f"Edge ({u}, {v}) does not exist, cannot find paths")