from security.audit_logger import append_audit, verify_audit_chain

def test_audit_hash_chain(tmp_path, monkeypatch):
    import security.audit_logger as audit
    monkeypatch.setattr(audit, "LOG_PATH", tmp_path / "audit.jsonl")
    audit.append_audit({"action": "test"})
    audit.append_audit({"action": "test2"})
    assert audit.verify_audit_chain()["valid"] is True
    assert audit.verify_audit_chain()["records"] == 2
