from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from database.postgres import SessionLocal
from models.transaction import TraceRecord

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/{trace_id}")
def report(trace_id: str):
    with SessionLocal() as db:
        record = db.scalar(select(TraceRecord).where(TraceRecord.trace_id == trace_id))
        if not record:
            raise HTTPException(404, "Trace not found")
        result = record.result_json
        return {"trace_id": trace_id, "subject": record.subject, "chain": record.chain,
                "findings": result["analysis"]["findings"],
                "ranked_receivers": result["analysis"]["ranked_receivers"],
                "security": result["security"], "limitations": result["limitations"]}
