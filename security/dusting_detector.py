def detect_dust_edges(edges, threshold=546):
    return [{"source": e["source"], "target": e["target"], "txid": e["txid"], "tag": "dust_candidate"}
            for e in edges if 0 < int(e.get("value", 0)) <= threshold]
