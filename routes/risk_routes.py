from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from database.postgres import SessionLocal
from models.transaction import TraceRecord

router = APIRouter(prefix="/risk", tags=["risk"])

@router.get("/{trace_id}/receivers")
def ranked_receivers(trace_id: str):
    with SessionLocal() as db:
        record = db.scalar(select(TraceRecord).where(TraceRecord.trace_id == trace_id))
        if not record:
            raise HTTPException(404, "Trace not found")
        return {"trace_id": trace_id, "receivers": record.result_json["analysis"]["ranked_receivers"]}
