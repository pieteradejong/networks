import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import random


def create_initial_network(n):
    return nx.erdos_renyi_graph(n, 0.1)


def visualize_network(G):
    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True, colorscale="YlGnBu", size=10, colorbar=dict(thickness=15)
        ),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False, hovermode="closest", margin=dict(b=0, l=0, r=0, t=0)
        ),
    )
    fig.show()


def adapt_network(G):
    # Simple preferential attachment mechanism
    new_node = max(G.nodes()) + 1
    G.add_node(new_node)

    # Connect to existing nodes with probability proportional to their degree
    for node in G.nodes():
        if node != new_node:
            if random.random() < G.degree(node) / (2 * G.number_of_edges()):
                G.add_edge(new_node, node)

    return G


def calculate_degree_distribution(G):
    degrees = [G.degree(node) for node in G.nodes()]
    return np.unique(degrees, return_counts=True)


def plot_degree_distribution(G):
    degrees, counts = calculate_degree_distribution(G)
    plt.figure(figsize=(8, 6))
    plt.loglog(degrees, counts, "b.")
    plt.xlabel("Degree")
    plt.ylabel("Count")
    plt.title("Degree Distribution")
    plt.show()


class NetworkSimulation:
    def __init__(self, initial_size=30, initial_probability=0.1):
        self.G = nx.erdos_renyi_graph(initial_size, initial_probability)
        self.history = []

    def step(self):
        self.G = adapt_network(self.G)
        self.history.append(self.calculate_metrics())

    def run(self, steps):
        for _ in range(steps):
            self.step()

    def calculate_metrics(self):
        return {
            "nodes": self.G.number_of_nodes(),
            "edges": self.G.number_of_edges(),
            "avg_degree": np.mean([d for _, d in self.G.degree()]),
        }

    def plot_metrics(self):
        metrics = list(
            zip(*[(d["nodes"], d["edges"], d["avg_degree"]) for d in self.history])
        )
        plt.figure(figsize=(12, 4))
        plt.subplot(131)
        plt.plot(metrics[0])
        plt.title("Number of Nodes")
        plt.subplot(132)
        plt.plot(metrics[1])
        plt.title("Number of Edges")
        plt.subplot(133)
        plt.plot(metrics[2])
        plt.title("Average Degree")
        plt.tight_layout()
        plt.show()


# Run a simulation
if __name__ == "__main__":
    sim = NetworkSimulation()
    sim.run(100)
    sim.plot_metrics()
    visualize_network(sim.G)
    plot_degree_distribution(sim.G)
