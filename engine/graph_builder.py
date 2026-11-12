import networkx as nx
from services.transaction_parser import transaction_to_edges

def build_graph(transactions, chain):
    graph = nx.DiGraph()
    for tx in transactions:
        for edge in transaction_to_edges(tx, chain):
            graph.add_node(edge["source"], chain=chain)
            graph.add_node(edge["target"], chain=chain)
            graph.add_edge(edge["source"], edge["target"], **edge)
    return graph

def serialize_graph(graph):
    return {
        "nodes": [{"id": n, **data} for n, data in graph.nodes(data=True)],
        "edges": [dict(data) for _, _, data in graph.edges(data=True)],
    }
