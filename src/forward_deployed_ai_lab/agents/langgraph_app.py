"""LangGraph deployment entry point for the optional agents extra.

This module is imported only by LangGraph tooling. The credential-free FastAPI
runtime does not require LangGraph.
"""

from __future__ import annotations

from ..app import build_container
from .langgraph_adapter import build_langgraph

_container = build_container()
graph = build_langgraph(_container.orchestrator)
