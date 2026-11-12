def detect_peel_chains(graph):
    findings = []
    for node in graph.nodes:
        successors = list(graph.successors(node))
        if len(successors) < 2:
            continue
        weighted = sorted([(s, graph[node][s].get("value", 0)) for s in successors], key=lambda x: x[1], reverse=True)
        if len(weighted) >= 2 and weighted[0][1] > weighted[1][1] * 1.5:
            next_node = weighted[0][0]
            if graph.out_degree(next_node) >= 1:
                findings.append({"address": node, "continuation": next_node, "tag": "possible_peel_chain", "confidence": 0.65})
    return findings
