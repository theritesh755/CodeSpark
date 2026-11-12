import re
from fastapi import HTTPException

EVM_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
BTC_RE = re.compile(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{20,90}$")
TX_RE = re.compile(r"^(0x[a-fA-F0-9]{64}|[a-fA-F0-9]{64})$")

def validate_subject(subject: str, chain: str):
    if chain == "bitcoin":
        if not (BTC_RE.match(subject) or TX_RE.match(subject)):
            raise HTTPException(422, "Invalid Bitcoin address or transaction hash format")
    elif not (EVM_RE.match(subject) or TX_RE.match(subject)):
        raise HTTPException(422, f"Invalid {chain} address or transaction hash format")
    return subject
