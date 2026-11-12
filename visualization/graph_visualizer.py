from pyvis.network import Network
from pathlib import Path

def render_graph(graph, output="reports/trace_graph.html"):
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    net = Network(height="720px", width="100%", directed=True, bgcolor="#111827", font_color="white")
    for node, attrs in graph.nodes(data=True):
        net.add_node(node, label=node[:18], title=str(attrs), color="#60a5fa")
    for source, target, attrs in graph.edges(data=True):
        net.add_edge(source, target, title=f"value={attrs.get('value')} tx={attrs.get('txid')}", arrows="to")
    net.write_html(output)
    return output
