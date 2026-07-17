import json
from pathlib import Path

from forward_deployed_ai_lab.evaluation.evidence import canonical_json_sha256, dataset_label


def test_canonical_json_hash_ignores_formatting_and_newlines() -> None:
    compact = json.loads('[{"name":"example","value":1}]')
    formatted = json.loads('[\r\n  {"value": 1, "name": "example"}\r\n]')
    assert canonical_json_sha256(compact) == canonical_json_sha256(formatted)


def test_dataset_label_is_stable_for_packaged_or_checkout_path() -> None:
    assert dataset_label(Path("repo/data/eval/golden_set.json")) == (
        "data/eval/golden_set.json"
    )
    assert dataset_label(Path("golden_set.json")) == "golden_set.json"
