from fastapi.testclient import TestClient

from forward_deployed_ai_lab.app import create_app


def test_health_and_assist(settings):
    client = TestClient(create_app(settings))
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    payload = health.json()
    assert payload["status"] == "ok"
    assert payload["model_provider"] == "deterministic-grounded-demo"
    assert payload["integrations"]["salesforce_mode"] == "synthetic"
    assert payload["integrations"]["audit_chain"][0] is True

    result = client.post(
        "/api/v1/assist",
        json={"query": "What is the P1 response target?", "requested_action": "read"},
    )
    assert result.status_code == 200
    body = result.json()
    assert body["policy"]["decision"] == "allow"
    assert body["citations"]
    assert body["evaluation"]["passed_release_gate"] is True
    assert any(
        step["detail"].get("prompt_version") == "deterministic-grounded-v1"
        for step in body["trace"]
        if step["stage"] == "response"
    )


def test_approval_endpoint_executes_only_after_decision(settings):
    client = TestClient(create_app(settings))
    result = client.post(
        "/api/v1/assist",
        json={
            "query": "Close this case after resolution.",
            "case_id": "500000000000001",
            "requested_action": "close_case",
        },
    ).json()
    approval_id = result["approval_id"]
    pending = client.get(f"/api/v1/approvals/{approval_id}")
    assert pending.status_code == 200
    assert pending.json()["status"] == "pending"

    decided = client.post(
        f"/api/v1/approvals/{approval_id}/decision",
        json={"approved": True, "decided_by": "Unit Test Reviewer"},
    )
    assert decided.status_code == 200
    body = decided.json()
    assert body["approval"]["status"] == "approved"
    assert body["execution"]["success"] is True
    assert body["execution"]["updated_fields"]["Status"] == "Closed"

    replay = client.post(
        f"/api/v1/approvals/{approval_id}/decision",
        json={"approved": True, "decided_by": "Unit Test Reviewer"},
    )
    assert replay.status_code == 200
    assert replay.json()["approval"]["decision_replayed"] is True
    assert replay.json()["execution"]["replayed"] is True
    current = client.get(f"/api/v1/approvals/{approval_id}").json()
    assert current["execution_attempts"] == 1
    assert current["execution_status"] == "succeeded"

    conflicting = client.post(
        f"/api/v1/approvals/{approval_id}/decision",
        json={"approved": True, "decided_by": "Another Reviewer"},
    )
    assert conflicting.status_code == 409


def test_rejected_approval_never_executes(settings):
    client = TestClient(create_app(settings))
    result = client.post(
        "/api/v1/assist",
        json={
            "query": "Escalate this case to the incident lead.",
            "case_id": "500000000000002",
            "requested_action": "escalate",
        },
    ).json()
    approval_id = result["approval_id"]

    decided = client.post(
        f"/api/v1/approvals/{approval_id}/decision",
        json={
            "approved": False,
            "decided_by": "Security Reviewer",
            "comment": "Insufficient evidence for escalation.",
        },
    )
    assert decided.status_code == 200
    body = decided.json()
    assert body["approval"]["status"] == "rejected"
    assert body["execution"] is None


def test_unknown_approval_returns_404(settings):
    client = TestClient(create_app(settings))
    assert client.get("/api/v1/approvals/apr_missing").status_code == 404
    response = client.post(
        "/api/v1/approvals/apr_missing/decision",
        json={"approved": True, "decided_by": "Unit Test Reviewer"},
    )
    assert response.status_code == 404


def test_capability_and_evaluation_endpoints(settings):
    client = TestClient(create_app(settings))

    capabilities = client.get("/api/v1/architecture/capabilities")
    assert capabilities.status_code == 200
    body = capabilities.json()
    assert {agent["name"] for agent in body["agents"]} >= {
        "intake",
        "retrieval",
        "policy",
        "response",
        "evaluation",
    }
    assert any(item["name"] == "Salesforce REST API" for item in body["integrations"])

    benchmark = client.post("/api/v1/evaluations/benchmark")
    assert benchmark.status_code == 200
    assert benchmark.json()["release_gate"]["passed"] is True

    red_team = client.post("/api/v1/evaluations/red-team")
    assert red_team.status_code == 200
    assert red_team.json()["metrics"]["pass_rate"] == 1.0
