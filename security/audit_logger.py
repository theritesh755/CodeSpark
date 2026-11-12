import hashlib, json
from pathlib import Path
from datetime import datetime, timezone
from threading import Lock

LOG_PATH = Path("logs/audit_log.jsonl")
_lock = Lock()

def append_audit(event: dict):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        previous = "0" * 64
        if LOG_PATH.exists():
            lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
            if lines:
                previous = json.loads(lines[-1])["hash"]
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), "previous_hash": previous, "event": event}
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
        record["hash"] = hashlib.sha256(canonical.encode()).hexdigest()
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
        return record

def verify_audit_chain():
    previous = "0" * 64
    if not LOG_PATH.exists():
        return {"valid": True, "records": 0}
    for index, line in enumerate(LOG_PATH.read_text(encoding="utf-8").splitlines()):
        record = json.loads(line)
        claimed = record.pop("hash")
        if record.get("previous_hash") != previous:
            return {"valid": False, "failed_record": index}
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
        actual = hashlib.sha256(canonical.encode()).hexdigest()
        if actual != claimed:
            return {"valid": False, "failed_record": index}
        previous = claimed
    return {"valid": True, "records": index + 1 if 'index' in locals() else 0}
