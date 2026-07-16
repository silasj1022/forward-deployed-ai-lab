def test_bm25_retrieves_p1_policy(container):
    results = container.knowledge_base.retrieve("Priority 1 incident response target", top_k=3)
    assert results
    assert results[0].document_id == "KB-002"
    assert results[0].score > 0


def test_role_filter_hides_manager_only_record(container):
    results = container.knowledge_base.retrieve(
        "bulk data deletion retention",
        top_k=5,
        user_role="agent",
    )
    assert "KB-005" not in {item.document_id for item in results}
