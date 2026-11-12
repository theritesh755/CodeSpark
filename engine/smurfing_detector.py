def detect_smurfing(graph, dust_threshold=546):
    findings = []
    for source in graph.nodes:
        tiny = [(target, data.get("value", 0)) for _, target, data in graph.out_edges(source, data=True)
                if 0 < data.get("value", 0) <= dust_threshold]
        if len(tiny) >= 2:
            findings.append({"address": source, "tag": "possible_dusting_or_structuring", "count": len(tiny), "confidence": 0.6})
    return findings
