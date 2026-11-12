def detect_lookalikes(addresses):
    # Flags near-identical strings for analyst review; it does not assert common ownership.
    results = []
    normalized = [(a, a.lower()) for a in set(addresses)]
    for i, (a, na) in enumerate(normalized):
        for b, nb in normalized[i+1:]:
            if len(na) == len(nb) and sum(x != y for x, y in zip(na, nb)) == 1:
                results.append({"address_a": a, "address_b": b, "tag": "possible_lookalike_address", "confidence": 0.5})
    return results
