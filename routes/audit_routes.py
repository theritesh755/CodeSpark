from fastapi import APIRouter
from pathlib import Path
import json
from security.audit_logger import verify_audit_chain, LOG_PATH

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("")
def audit_records():
    rows = []
    if LOG_PATH.exists():
        rows = [json.loads(line) for line in LOG_PATH.read_text(encoding="utf-8").splitlines()]
    return {"verification": verify_audit_chain(), "records": rows[-100:]}
