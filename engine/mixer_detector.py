def detect_mixer_patterns(graph):
    findings = []
    for node in graph.nodes:
        indeg, outdeg = graph.in_degree(node), graph.out_degree(node)
        if indeg >= 3 and outdeg >= 3:
            findings.append({"address": node, "tag": "possible_mixer_fan_in_fan_out", "confidence": 0.55, "in_degree": indeg, "out_degree": outdeg})
    return findings
