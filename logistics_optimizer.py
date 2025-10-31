import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean

data = pd.read_csv("routes.csv")
G = nx.Graph()

for _, r in data.iterrows():
    G.add_edge(r.Source, r.Destination, weight=r.Distance)

sources = data["Source"].unique()
targets = data["Destination"].unique()
all_nodes = sorted(set(sources) | set(targets))

centrality = nx.degree_centrality(G)
average_distance = mean([r.Distance for _, r in data.iterrows()])

print("Nodes in network:", len(all_nodes))
print("Average route distance:", round(average_distance, 2))

hub = max(centrality, key=centrality.get)
print("Primary hub:", hub)

pairs = [
    ("Bangalore", "Chennai"),
    ("Mumbai", "Hyderabad"),
    ("Delhi", "Jaipur"),
    ("Ahmedabad", "Pune")
]

for s, t in pairs:
    if nx.has_path(G, s, t):
        path = nx.shortest_path(G, s, t, weight="weight")
        distance = nx.shortest_path_length(G, s, t, weight="weight")
        print(f"{s} → {t}: {path} ({distance} km)")

pos = nx.spring_layout(G, seed=7)
nx.draw(G, pos, with_labels=True, node_color="#8cbdf9", node_size=1700, font_size=9)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"))
plt.title("Folkslogic Logistics Route Network – India")
plt.show()
