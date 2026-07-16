"""Provider factory and optional cloud/LLM adapters.

Only the deterministic provider is required for the public demo. Networked
providers are imported lazily and require explicit credentials.
"""

from __future__ import annotations

from typing import Any

from ..config import Settings
from ..prompts.system import GROUNDED_ENTERPRISE_SYSTEM_PROMPT, SYSTEM_PROMPT_VERSION
from .base import ModelProvider
from .deterministic import DeterministicGroundedModel
from .domain import KnowledgeDocument


def _approved_context(documents: list[KnowledgeDocument]) -> str:
    return "\n\n".join(
        f"[{document.document_id}] {document.title}\n{document.content}" for document in documents
    )


class OpenAIProvider:
    """Optional OpenAI Responses API provider."""

    name = "openai"
    prompt_version = SYSTEM_PROMPT_VERSION

    def __init__(self, api_key: str, model_name: str) -> None:
        from openai import OpenAI  # type: ignore[import-not-found]

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def generate(
        self,
        *,
        query: str,
        documents: list[KnowledgeDocument],
        case_context: dict[str, object] | None = None,
    ) -> str:
        del case_context
        context = _approved_context(documents)
        response = self.client.responses.create(
            model=self.model_name,
            instructions=GROUNDED_ENTERPRISE_SYSTEM_PROMPT,
            input=f"REQUEST:\n{query}\n\nAPPROVED CONTEXT:\n{context}",
        )
        return str(response.output_text)


class AnthropicProvider:
    """Optional Anthropic Messages API provider."""

    name = "anthropic"
    prompt_version = SYSTEM_PROMPT_VERSION

    def __init__(self, api_key: str, model_name: str) -> None:
        import anthropic  # type: ignore[import-not-found]

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_name = model_name

    def generate(
        self,
        *,
        query: str,
        documents: list[KnowledgeDocument],
        case_context: dict[str, object] | None = None,
    ) -> str:
        del case_context
        context = _approved_context(documents)
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=700,
            system=GROUNDED_ENTERPRISE_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"{query}\n\nApproved context:\n{context}",
                }
            ],
        )
        return "".join(block.text for block in message.content if hasattr(block, "text"))


def build_model_provider(settings: Settings) -> ModelProvider:
    provider = settings.model_provider
    if provider == "deterministic":
        return DeterministicGroundedModel()
    if provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("FDAI_OPENAI_API_KEY is required for the OpenAI provider")
        return OpenAIProvider(settings.openai_api_key, settings.model_name)
    if provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("FDAI_ANTHROPIC_API_KEY is required for the Anthropic provider")
        return AnthropicProvider(settings.anthropic_api_key, settings.model_name)
    raise NotImplementedError(
        f"Provider '{provider}' is documented as a production extension point but is not enabled "
        "in the credential-free reference runtime."
    )


def provider_capabilities() -> list[dict[str, Any]]:
    return [
        {"provider": "deterministic", "status": "implemented", "credentials": False},
        {"provider": "openai", "status": "implemented-optional", "credentials": True},
        {"provider": "anthropic", "status": "implemented-optional", "credentials": True},
        {"provider": "azure", "status": "extension-point", "credentials": True},
        {"provider": "bedrock", "status": "extension-point", "credentials": True},
        {"provider": "vertex", "status": "extension-point", "credentials": True},
    ]
