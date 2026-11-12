from collections import defaultdict

def common_input_clusters(transactions):
    # Bitcoin common-input heuristic only. Never apply to account-based EVM chains.
    groups = defaultdict(set)
    for tx in transactions:
        inputs = [x.get("address") for x in tx.get("inputs", []) if x.get("address")]
        if len(inputs) > 1:
            for address in inputs:
                groups[tuple(sorted(inputs))].add(address)
    return [{"heuristic": "common_input_ownership", "addresses": sorted(v)} for v in groups.values() if len(v) > 1]
