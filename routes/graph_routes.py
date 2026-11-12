from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from database.postgres import SessionLocal
from models.transaction import TraceRecord
from visualization.graph_visualizer import render_graph
from engine.graph_builder import build_graph

router = APIRouter(prefix="/graphs", tags=["graphs"])

@router.get("/{trace_id}")
def get_graph(trace_id: str):
    with SessionLocal() as db:
        record = db.scalar(select(TraceRecord).where(TraceRecord.trace_id == trace_id))
        if not record:
            raise HTTPException(404, "Trace not found")
        return record.result_json["graph"]

@router.post("/{trace_id}/visualize")
def visualize(trace_id: str):
    with SessionLocal() as db:
        record = db.scalar(select(TraceRecord).where(TraceRecord.trace_id == trace_id))
        if not record:
            raise HTTPException(404, "Trace not found")
        txs = __import__("datasets.sample_data", fromlist=["load_sample"]).load_sample()
        graph = build_graph(txs, record.chain)
        path = render_graph(graph, f"reports/{trace_id}.html")
        return {"file": path, "note": "Open this local HTML file in a browser."}
