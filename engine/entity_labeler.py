# Labels must be populated from a trusted, reviewed dataset. No label is bundled as a claim.
KNOWN_LABELS = {}

def label_address(address):
    return KNOWN_LABELS.get(address, {"entity": "unknown", "source": None, "verified": False})
