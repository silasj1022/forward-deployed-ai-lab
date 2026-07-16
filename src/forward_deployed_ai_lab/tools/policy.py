"""Deterministic policy, prompt-injection, and approval routing controls."""

from __future__ import annotations

import re

from ..models.domain import ActionKind, Decision, PolicyDecision, RiskLevel


class PolicyEngine:
    """Evaluate requests before any model or enterprise write is trusted."""

    injection_patterns = (
        re.compile(r"(?i)ignore (all|any|the) (previous|prior|system) (instructions|rules|prompt)"),
        re.compile(
            r"(?i)(reveal|show|print|dump).*(system prompt|hidden prompt|developer message)"
        ),
        re.compile(r"(?i)(bypass|disable|override).*(guardrail|policy|approval|security)"),
        re.compile(r"(?i)act as .* unrestricted"),
    )
    secret_patterns = (
        re.compile(r"(?i)(api key|access token|password|client secret|private key)"),
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    )
    destructive_patterns = (
        re.compile(r"(?i)delete (all|every|the).*(data|record|account|case)"),
        re.compile(r"(?i)drop (table|database)"),
        re.compile(r"(?i)purge"),
    )
    write_patterns: tuple[tuple[re.Pattern[str], ActionKind], ...] = (
        (re.compile(r"(?i)close (the )?(case|ticket)"), ActionKind.CLOSE_CASE),
        (re.compile(r"(?i)(update|change|edit).*(case|ticket|account)"), ActionKind.UPDATE_CASE),
        (re.compile(r"(?i)(refund|credit|reimburse)"), ActionKind.CREATE_REFUND),
        (
            re.compile(r"(?i)(escalate|page|notify).*(manager|engineer|incident)"),
            ActionKind.ESCALATE,
        ),
    )

    def detect_action(self, query: str, requested_action: ActionKind) -> ActionKind:
        if requested_action != ActionKind.NONE:
            return requested_action
        for pattern, action in self.write_patterns:
            if pattern.search(query):
                return action
        if any(pattern.search(query) for pattern in self.destructive_patterns):
            return ActionKind.DELETE_DATA
        return ActionKind.READ

    def evaluate(
        self,
        *,
        query: str,
        requested_action: ActionKind = ActionKind.NONE,
        retrieval_confidence: float = 1.0,
    ) -> PolicyDecision:
        action = self.detect_action(query, requested_action)
        reasons: list[str] = []
        controls = ["NIST-AI-RMF-GOVERN", "NIST-AI-RMF-MEASURE"]

        if any(pattern.search(query) for pattern in self.injection_patterns):
            return PolicyDecision(
                decision=Decision.BLOCK,
                risk_level=RiskLevel.CRITICAL,
                reasons=["Prompt-injection or instruction-override pattern detected."],
                controls=[*controls, "OWASP-LLM01-PROMPT-INJECTION"],
                requires_human_approval=False,
                detected_action=action,
            )

        if any(pattern.search(query) for pattern in self.secret_patterns):
            return PolicyDecision(
                decision=Decision.BLOCK,
                risk_level=RiskLevel.CRITICAL,
                reasons=["Request seeks credentials, secrets, or restricted personal data."],
                controls=[*controls, "DATA-MINIMIZATION", "SECRETS-NONDISCLOSURE"],
                requires_human_approval=False,
                detected_action=action,
            )

        if action == ActionKind.DELETE_DATA or any(
            pattern.search(query) for pattern in self.destructive_patterns
        ):
            return PolicyDecision(
                decision=Decision.BLOCK,
                risk_level=RiskLevel.CRITICAL,
                reasons=[
                    "Bulk or destructive action is outside the autonomous authority boundary."
                ],
                controls=[*controls, "ZERO-TRUST-LEAST-PRIVILEGE", "DESTRUCTIVE-ACTION-BLOCK"],
                requires_human_approval=False,
                detected_action=ActionKind.DELETE_DATA,
            )

        if action in {
            ActionKind.UPDATE_CASE,
            ActionKind.CLOSE_CASE,
            ActionKind.CREATE_REFUND,
            ActionKind.ESCALATE,
        }:
            reasons.append("Consequential enterprise write requires named human approval.")
            if retrieval_confidence < 0.25:
                reasons.append("Supporting knowledge confidence is low.")
            return PolicyDecision(
                decision=Decision.REVIEW,
                risk_level=RiskLevel.HIGH,
                reasons=reasons,
                controls=[*controls, "HUMAN-IN-THE-LOOP", "MAKER-CHECKER"],
                requires_human_approval=True,
                detected_action=action,
            )

        if retrieval_confidence < 0.10:
            return PolicyDecision(
                decision=Decision.REVIEW,
                risk_level=RiskLevel.MEDIUM,
                reasons=["No sufficiently relevant approved knowledge was found."],
                controls=[*controls, "INSUFFICIENT-EVIDENCE-ESCALATION"],
                requires_human_approval=True,
                detected_action=action,
            )

        return PolicyDecision(
            decision=Decision.ALLOW,
            risk_level=RiskLevel.LOW,
            reasons=["Read-only request is supported by approved knowledge."],
            controls=controls,
            requires_human_approval=False,
            detected_action=action,
        )
