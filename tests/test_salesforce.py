from pathlib import Path

import httpx
import pytest

from forward_deployed_ai_lab.config import Settings
from forward_deployed_ai_lab.models.domain import ActionKind
from forward_deployed_ai_lab.tools.approvals import ApprovalStore
from forward_deployed_ai_lab.tools.salesforce import SalesforceClient


def live_client(
    project_root: Path,
    handler: httpx.MockTransport,
    *,
    retries: int = 2,
) -> SalesforceClient:
    settings = Settings(
        environment="test",
        data_dir=project_root / "data",
        live_integrations_enabled=True,
        allow_salesforce_writes=True,
        salesforce_instance_url="https://example.my.salesforce.com",
        salesforce_access_token="test-token",
        salesforce_max_retries=retries,
        salesforce_retry_backoff_seconds=0,
    )
    return SalesforceClient(
        settings,
        project_root / "data/salesforce_cases.json",
        http_client=httpx.Client(transport=handler),
    )


def test_synthetic_salesforce_read(container):
    record = container.salesforce.get_case("500000000000001")
    assert record is not None
    assert record["case_number"] == "C-1001"


def test_salesforce_write_requires_approval(container):
    action = container.salesforce.propose_case_update(
        case_id="500000000000001",
        fields={"Status": "Closed"},
        rationale="test",
        kind=ActionKind.CLOSE_CASE,
    )
    try:
        container.salesforce.execute_case_update(action, approved=False)
    except PermissionError:
        pass
    else:
        raise AssertionError("write executed without approval")

    result = container.salesforce.execute_case_update(action, approved=True)
    assert result["success"] is True
    assert container.salesforce.get_case("500000000000001")["status"] == "Closed"


def test_salesforce_id_validation(container):
    try:
        container.salesforce.get_case("500000000000001 OR 1=1")
    except ValueError as exc:
        assert "15 or 18" in str(exc)
    else:
        raise AssertionError("invalid Salesforce ID was accepted")


def test_live_salesforce_query_success() -> None:
    project_root = Path(__file__).resolve().parents[1]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-token"
        assert request.method == "GET"
        return httpx.Response(200, json={"totalSize": 1, "records": [{"Id": "500000000000001"}]})

    client = live_client(project_root, httpx.MockTransport(handler))
    assert client.query("SELECT Id FROM Case")["totalSize"] == 1


def test_live_salesforce_update_success() -> None:
    project_root = Path(__file__).resolve().parents[1]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        assert request.url.path.endswith("/sobjects/Case/500000000000001")
        assert request.content == b'{"Status":"Closed"}'
        return httpx.Response(204, request=request)

    client = live_client(project_root, httpx.MockTransport(handler))
    action = client.propose_case_update(
        case_id="500000000000001",
        fields={"Status": "Closed"},
        rationale="approved test",
        kind=ActionKind.CLOSE_CASE,
    )
    result = client.execute_case_update(action, approved=True)
    assert result == {
        "mode": "live",
        "success": True,
        "case_id": "500000000000001",
        "updated_fields": {"Status": "Closed"},
    }


def test_live_salesforce_auth_failure_is_not_retried() -> None:
    project_root = Path(__file__).resolve().parents[1]
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(401, request=request, json={"error": "invalid_session"})

    client = live_client(project_root, httpx.MockTransport(handler))
    with pytest.raises(httpx.HTTPStatusError):
        client.query("SELECT Id FROM Case")
    assert calls == 1


def test_live_salesforce_timeout_retries_then_succeeds() -> None:
    project_root = Path(__file__).resolve().parents[1]
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise httpx.ReadTimeout("synthetic timeout", request=request)
        return httpx.Response(200, request=request, json={"totalSize": 0, "records": []})

    client = live_client(project_root, httpx.MockTransport(handler))
    assert client.query("SELECT Id FROM Case")["totalSize"] == 0
    assert calls == 3


def test_live_salesforce_rate_limit_uses_bounded_retry() -> None:
    project_root = Path(__file__).resolve().parents[1]
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, request=request, headers={"Retry-After": "0"})
        return httpx.Response(200, request=request, json={"totalSize": 0, "records": []})

    client = live_client(project_root, httpx.MockTransport(handler))
    client.query("SELECT Id FROM Case")
    assert calls == 2


def test_live_salesforce_retry_exhaustion_raises() -> None:
    project_root = Path(__file__).resolve().parents[1]
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, request=request)

    client = live_client(project_root, httpx.MockTransport(handler), retries=1)
    with pytest.raises(httpx.HTTPStatusError):
        client.query("SELECT Id FROM Case")
    assert calls == 2


def test_approval_binds_action_and_replays_success(container) -> None:
    approvals = ApprovalStore()
    action = container.salesforce.propose_case_update(
        case_id="500000000000001",
        fields={"Status": "Closed"},
        rationale="test",
        kind=ActionKind.CLOSE_CASE,
    )
    approval_id = approvals.create(action, trace_id="trace_test")
    approvals.decide(approval_id, approved=True, decided_by="Reviewer")
    claimed, _, key = approvals.claim_execution(approval_id, action)
    assert claimed is True
    result = {"success": True, "idempotency_key": key}
    approvals.complete_execution(approval_id, result)

    claimed_again, prior, same_key = approvals.claim_execution(approval_id, action)
    assert claimed_again is False
    assert prior == result
    assert same_key == key

    tampered = action.model_copy(deep=True)
    tampered.payload["fields"] = {"Status": "Escalated"}
    with pytest.raises(PermissionError, match="no longer matches"):
        approvals.claim_execution(approval_id, tampered)
