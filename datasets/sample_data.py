import json
from pathlib import Path

def load_sample():
    path = Path(__file__).with_name("sample_transactions.json")
    return json.loads(path.read_text(encoding="utf-8"))["transactions"]
