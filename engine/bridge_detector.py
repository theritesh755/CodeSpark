def detect_bridge_correlations(transactions):
    # Correlation requires indexed events from both chains. This safe starter flags
    # bridge-labelled metadata only; it does not infer cross-chain identity from timing alone.
    return [{"txid": tx["txid"], "tag": "bridge_reference_present", "confidence": 0.4}
            for tx in transactions if tx.get("bridge_reference")]
