import json, uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.postgres import get_db
from models.transaction import TraceRecord
from schemas.trace_schema import TraceRequest
from services.data_validator import validate_subject
from services.bitcoin_service import BitcoinService
from services.ethereum_service import EthereumService
from engine.graph_builder import build_graph, serialize_graph
from engine.risk_engine import analyze_graph
from security.audit_logger import append_audit
from security.input_validator import reject_suspicious_input
from security.address_spoof_detector import detect_lookalikes
from security.graph_poisoning_detector import detect_graph_anomalies
from security.dusting_detector import detect_dust_edges
from datasets.sample_data import load_sample

router = APIRouter(prefix="/traces", tags=["tracing"])

@router.post("")
async def create_trace(request: TraceRequest, db: Session = Depends(get_db)):
    try:
        subject = reject_suspicious_input(request.subject)
        validate_subject(subject, request.chain)
        if request.use_sample or request.chain != "bitcoin" and not request.subject.startswith("0x"):
            transactions = load_sample()
            source_mode = "sample"
        elif request.chain == "bitcoin":
            service = BitcoinService()
            if len(subject) == 64:
                transactions = [await service.fetch_transaction(subject)]
            else:
                transactions = await service.fetch_address(subject, request.limit)
            source_mode = "blockstream"
        else:
            tx = EthereumService().get_transaction(request.chain, subject)
            transactions = [tx]
            source_mode = "evm-rpc"
        graph = build_graph(transactions, request.chain)
        analysis = analyze_graph(graph, transactions)
        serialized = serialize_graph(graph)
        security = {
            "dust_edges": detect_dust_edges(serialized["edges"]),
            "lookalikes": detect_lookalikes([n["id"] for n in serialized["nodes"]]),
            "graph_anomalies": detect_graph_anomalies(graph),
        }
        trace_id = str(uuid.uuid4())
        result = {
            "trace_id": trace_id, "subject": subject, "chain": request.chain,
            "source_mode": source_mode, "hops_requested": request.max_hops,
            "graph": serialized, "analysis": analysis, "security": security,
            "limitations": ["A trace only includes transactions returned by the selected provider or sample dataset.",
                "Heuristic scores are investigative leads, not identity attribution or proof of wrongdoing.",
                "Cross-chain bridge correlation and entity labels require trusted, curated datasets."]
        }
        db.add(TraceRecord(trace_id=trace_id, subject=subject, chain=request.chain, result_json=result))
        db.commit()
        append_audit({"action": "trace_created", "trace_id": trace_id, "subject": subject, "chain": request.chain, "source_mode": source_mode})
        return result
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=502, detail=f"Trace failed: {str(exc)}")
