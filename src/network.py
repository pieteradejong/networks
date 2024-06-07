import networkx as nx
import plotly.graph_objs as go


def run_analysis():
    # Create a graph
    G = nx.Graph()
    G.add_edge(1, 2)

    # Extract edge and node positions
    pos = nx.spring_layout(G)
    edges = list(G.edges())
    nodes = list(G.nodes())

    # Create edge trace
    edge_trace = go.Scatter(
        x=[], y=[], line=dict(width=2, color="gray"), hoverinfo="none", mode="lines"
    )

    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace["x"] += (x0, x1, None)
        edge_trace["y"] += (y0, y1, None)

    # Create node trace
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers+text",
        hoverinfo="text",
        marker=dict(color="lightblue", size=30, line=dict(width=2)),
    )

    for node in nodes:
        x, y = pos[node]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        node_trace["text"] += (str(node),)

    # Create figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="Simple Graph Visualization",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
        ),
    )

    fig.show()
