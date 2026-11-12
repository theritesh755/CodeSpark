from fastapi import APIRouter
from security.audit_logger import verify_audit_chain

router = APIRouter(prefix="/security", tags=["security"])

@router.get("/audit/verify")
def verify_audit():
    return verify_audit_chain()

@router.get("/capabilities")
def capabilities():
    return {"controls": ["input-format-validation", "provider-response-shape-validation",
        "lookalike-address-flagging", "dust-output-flagging", "graph-anomaly-checks",
        "sha256-hash-chained-audit-log"], "warning": "These controls reduce common risks but do not make external provider data inherently trustworthy."}
