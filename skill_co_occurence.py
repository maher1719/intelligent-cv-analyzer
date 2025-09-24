import pandas as pd
import networkx as nx
from networkx.algorithms import community
from cdlib import algorithms
import matplotlib.pyplot as plt

# Load the skill co-occurrence data
df = pd.read_csv("csv/grouped3.csv", index_col=0)  # Assuming "grouped3.csv" has co-occurrence weights

# Initialize an undirected graph
G = nx.Graph()

# Add nodes and edges with weights based on co-occurrence data
for skill1 in df.columns:
    for skill2 in df.index:
        weight = df.at[skill2, skill1]
        if weight > 0:  # Only add edges with positive weights
            G.add_edge(skill1, skill2, weight=weight)
print("step 1 ended")
# Calculate threshold for top 40% of edge weights
threshold = df.stack().quantile(0.60)

# Remove edges with weights below the threshold
for u, v, data in list(G.edges(data=True)):
    if data['weight'] < threshold:
        G.remove_edge(u, v)
print("step 2 ended")
# Detect communities using Louvain method
communities = algorithms.louvain(G)

# Create a dictionary mapping each node to its cluster ID
community_dict = {}
for i, community in enumerate(communities.communities):
    for skill in community:
        community_dict[skill] = i

# Save cluster memberships to CSV
community_df = pd.DataFrame(list(community_dict.items()), columns=["Skill", "Cluster_ID"])
community_df.to_csv("skill_clusters.csv", index=False)

print("step 3 ended")

# Weighted Degree Centrality
degree_centrality = nx.degree_centrality(G)

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')

# Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G, weight='weight')

# Save centrality measures to CSV
centrality_df = pd.DataFrame({
    "Skill": list(G.nodes),
    "Degree Centrality": [degree_centrality[node] for node in G.nodes],
    "Betweenness Centrality": [betweenness_centrality[node] for node in G.nodes],
    "Eigenvector Centrality": [eigenvector_centrality[node] for node in G.nodes]
})
centrality_df.to_csv("centrality_measures.csv", index=False)


print("step 4 ended")

import matplotlib.cm as cm

# Position nodes using Fruchterman-Reingold force-directed algorithm
pos = nx.spring_layout(G, k=0.15, iterations=20)

# Define colors for each community
colors = [community_dict[node] for node in G.nodes]
cmap = cm.get_cmap('viridis', max(colors) + 1)

# Draw the network
plt.figure(figsize=(12, 12))
nx.draw_networkx_nodes(G, pos, node_size=50, node_color=colors, cmap=cmap)
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
plt.title("Skill Co-Occurrence Network with Cluster Coloring")
plt.show()


print("step 5 ended")

# Calculate total occurrences for each skill
total_occurrences = df.sum(axis=1)

# Initialize lists to hold the skill pairs and their ratios
skill1_list, skill2_list, ratio_by_row, ratio_by_column = [], [], [], []

for skill1 in df.columns:
    for skill2 in df.index:
        if skill1 != skill2:
            co_occurrence = df.at[skill2, skill1]
            ratio_row = co_occurrence / total_occurrences[skill2] if total_occurrences[skill2] > 0 else 0
            ratio_column = co_occurrence / total_occurrences[skill1] if total_occurrences[skill1] > 0 else 0
            
            skill1_list.append(skill1)
            skill2_list.append(skill2)
            ratio_by_row.append(ratio_row)
            ratio_by_column.append(ratio_column)

# Save the pairwise ratios to CSV
pair_ratios_df = pd.DataFrame({
    "Skill1": skill1_list,
    "Skill2": skill2_list,
    "Ratio_by_Row": ratio_by_row,
    "Ratio_by_Column": ratio_by_column
})
pair_ratios_df.to_csv("pairwise_skill_ratios.csv", index=False)


