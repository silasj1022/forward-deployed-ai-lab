"""Salesforce REST adapter with a safe synthetic fallback.

The connector supports read/query operations and approval-controlled Case updates.
Live writes are disabled unless both live integration and write flags are enabled.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, cast
from urllib.parse import quote

import httpx

from ..config import Settings
from ..models.domain import ActionKind, ProposedAction
from ..utils.ids import new_id

SALESFORCE_ID_RE = re.compile(r"^[A-Za-z0-9]{15}(?:[A-Za-z0-9]{3})?$")

SYNTHETIC_FIELD_MAP = {
    "Status": "status",
    "Priority": "priority",
    "Refund_Requested__c": "refund_requested",
}


def _validated_salesforce_id(value: str) -> str:
    if not SALESFORCE_ID_RE.fullmatch(value):
        raise ValueError("Salesforce record IDs must be 15 or 18 alphanumeric characters")
    return value


class SalesforceClient:
    def __init__(self, settings: Settings, synthetic_cases_path: Path) -> None:
        self.settings = settings
        self.synthetic_cases_path = synthetic_cases_path
        self._cases = {
            item["case_id"]: item
            for item in json.loads(synthetic_cases_path.read_text(encoding="utf-8"))
        }

    @property
    def live(self) -> bool:
        return bool(
            self.settings.live_integrations_enabled
            and self.settings.salesforce_instance_url
            and self.settings.salesforce_access_token
        )

    def _base_url(self) -> str:
        value = self.settings.salesforce_instance_url
        if not value:
            raise RuntimeError("Salesforce instance URL is not configured")
        return value.rstrip("/")

    def _headers(self) -> dict[str, str]:
        if not self.settings.salesforce_access_token:
            raise RuntimeError("Salesforce access token is not configured")
        return {
            "Authorization": f"Bearer {self.settings.salesforce_access_token}",
            "Content-Type": "application/json",
        }

    def query(self, soql: str) -> dict[str, Any]:
        if not self.live:
            normalized = soql.lower()
            records = list(self._cases.values())
            if "where id" in normalized:
                for case_id, record in self._cases.items():
                    if case_id.lower() in normalized:
                        records = [record]
                        break
            return {"totalSize": len(records), "done": True, "records": deepcopy(records)}

        base = self._base_url()
        endpoint = (
            f"{base}/services/data/{self.settings.salesforce_api_version}/query?q={quote(soql)}"
        )
        response = httpx.get(endpoint, headers=self._headers(), timeout=20.0)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())

    def get_case(self, case_id: str) -> dict[str, Any] | None:
        case_id = _validated_salesforce_id(case_id)
        if not self.live:
            record = self._cases.get(case_id)
            return deepcopy(record) if record else None
        soql = (
            "SELECT Id, CaseNumber, Subject, Status, Priority, Owner.Name, Account.Name "
            f"FROM Case WHERE Id = '{case_id}' LIMIT 1"
        )
        records = self.query(soql).get("records", [])
        return records[0] if records else None

    def propose_case_update(
        self, *, case_id: str, fields: dict[str, Any], rationale: str, kind: ActionKind
    ) -> ProposedAction:
        case_id = _validated_salesforce_id(case_id)
        return ProposedAction(
            action_id=new_id("act"),
            kind=kind,
            target=f"Case/{case_id}",
            payload={"case_id": case_id, "fields": fields},
            rationale=rationale,
        )

    def execute_case_update(self, action: ProposedAction, *, approved: bool) -> dict[str, Any]:
        if not approved:
            raise PermissionError("A named human approval is required before a Salesforce write")
        case_id = _validated_salesforce_id(str(action.payload["case_id"]))
        fields = dict(action.payload["fields"])

        if not self.live:
            if case_id not in self._cases:
                raise KeyError(case_id)
            persisted_fields = {
                SYNTHETIC_FIELD_MAP.get(key, key): value for key, value in fields.items()
            }
            self._cases[case_id].update(persisted_fields)
            return {
                "mode": "synthetic",
                "success": True,
                "case_id": case_id,
                "updated_fields": fields,
                "persisted_fields": persisted_fields,
            }

        if not self.settings.allow_salesforce_writes:
            raise PermissionError("FDAI_ALLOW_SALESFORCE_WRITES is false")
        base = self._base_url()
        endpoint = (
            f"{base}/services/data/{self.settings.salesforce_api_version}/sobjects/Case/{case_id}"
        )
        response = httpx.patch(endpoint, headers=self._headers(), json=fields, timeout=20.0)
        response.raise_for_status()
        return {"mode": "live", "success": True, "case_id": case_id, "updated_fields": fields}
