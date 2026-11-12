def transaction_to_edges(tx, chain):
    edges = []
    inputs = [x for x in tx.get("inputs", []) if x.get("address")]
    outputs = [x for x in tx.get("outputs", []) if x.get("address")]
    for source in inputs:
        for target in outputs:
            if source["address"] != target["address"]:
                edges.append({
                    "source": source["address"], "target": target["address"],
                    "value": min(int(source.get("value", 0)), int(target.get("value", 0))),
                    "txid": tx["txid"], "timestamp": tx.get("timestamp"),
                    "chain": chain, "confirmed": tx.get("confirmed", False),
                })
    return edges
