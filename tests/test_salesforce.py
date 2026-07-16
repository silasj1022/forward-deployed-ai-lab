from forward_deployed_ai_lab.models.domain import ActionKind


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
