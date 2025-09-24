
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Load data
data = pd.read_csv('csv/grouped.csv', index_col=0)  # Set the first column as the index

# Initialize an empty graph
G = nx.Graph()

# Loop through the DataFrame to add edges
for skill1 in data.columns:
    for skill2 in data.columns:
        weight = data.loc[skill1, skill2]
        if weight > 0:  # Only add edges with non-zero weights
            G.add_edge(skill1, skill2, weight=weight)

# Generate positions for each node
pos = nx.spring_layout(G, k=0.15, seed=42)  # Seed for reproducibility

# Prepare data for Plotly scatter plot
edge_x = []
edge_y = []
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

# Create node traces
node_x = []
node_y = []
node_text = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)


from networkx.algorithms.community import girvan_newman

# Community Detection
communities = list(girvan_newman(G))

# Save Communities
communities_df = pd.DataFrame(communities, columns=['community'])
communities_df.to_csv('communities.csv', index=False)

degree_centrality = nx.degree_centrality(G)
degree_df = pd.DataFrame(degree_centrality.items(), columns=['skill', 'degree_centrality'])

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
betweenness_df = pd.DataFrame(betweenness_centrality.items(), columns=['skill', 'betweenness_centrality'])

# Merge Centrality Measures
centrality_df = pd.merge(degree_df, betweenness_df, on='skill')
centrality_df.to_csv('centrality_measures.csv', index=False)

import matplotlib.pyplot as plt

# Visualization
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
plt.savefig('graph_visualization.png')


pagerank = nx.pagerank(G)
pagerank_df = pd.DataFrame(pagerank.items(), columns=['skill', 'pagerank'])

# Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G)
eigenvector_df = pd.DataFrame(eigenvector_centrality.items(), columns=['skill', 'eigenvector_centrality'])

# Merge Skill Importance Measures
importance_df = pd.merge(pagerank_df, eigenvector_df, on='skill')
importance_df.to_csv('skill_importance.csv', index=False)

skill_gaps = df[df['count'] < df['count'].mean()].sort_values(by='count', ascending=False)
skill_gaps.to_csv('skill_gaps.csv', index=False)

"""node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    text=node_text,
    textposition="top center",
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
    )
)

# Build figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Skill Co-occurrence Network Graph',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()
"""