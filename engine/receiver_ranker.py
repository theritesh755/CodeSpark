def rank_receivers(graph, findings):
    flagged = {}
    for finding in findings:
        addr = finding.get("address") or finding.get("continuation")
        if addr:
            flagged[addr] = max(flagged.get(addr, 0), float(finding.get("confidence", 0)))
    candidates = []
    for node in graph.nodes:
        if graph.out_degree(node) == 0 and graph.in_degree(node) > 0:
            exposure = flagged.get(node, 0)
            risk = min(100, round(20 + graph.in_degree(node) * 8 + exposure * 35))
            confidence = min(0.99, round(0.35 + graph.in_degree(node) * 0.12 + exposure * 0.2, 2))
            candidates.append({
                "address": node, "confidence": confidence, "risk_score": risk,
                "risk_level": "high" if risk >= 70 else "medium" if risk >= 40 else "low",
                "reasoning": ["terminal node in observed trace", "heuristic score; requires analyst review"],
            })
    return sorted(candidates, key=lambda x: (x["confidence"], x["risk_score"]), reverse=True)
