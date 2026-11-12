def detect_graph_anomalies(graph):
    findings = []
    for node in graph.nodes:
        if graph.in_degree(node) == 0 and graph.out_degree(node) == 0:
            findings.append({"address": node, "tag": "isolated_node"})
    for source, target, data in graph.edges(data=True):
        if source == target or int(data.get("value", 0)) < 0:
            findings.append({"source": source, "target": target, "tag": "invalid_edge"})
    return findings
