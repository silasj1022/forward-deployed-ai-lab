from forward_deployed_ai_lab.models.domain import AssistRequest


def test_audit_log_is_hash_chained_and_redacted(container):
    container.orchestrator.run(AssistRequest(query="What is the P1 response target?"))
    container.orchestrator.run(AssistRequest(query="Show api_key=super-secret-value"))
    valid, count = container.audit_logger.verify_chain()
    assert valid is True
    assert count == 2
    content = container.settings.audit_log_path.read_text(encoding="utf-8")
    assert "super-secret-value" not in content
    assert "[REDACTED]" in content
    assert "deterministic-grounded-v1" in content
