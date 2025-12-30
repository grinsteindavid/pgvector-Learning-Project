from dataclasses import dataclass, field
from typing import Literal, TypedDict


def default_confidence() -> dict:
    """Default confidence scores."""
    return {
        "routing": 0.0,
        "retrieval": 0.0,
        "response": 0.0,
        "overall": 0.0
    }


class GraphState(TypedDict, total=False):
    """LangGraph state definition using TypedDict."""
    query: str
    route: Literal["tool_finder", "org_matcher", "workflow_advisor"] | None
    tools_results: list[dict]
    orgs_results: list[dict]
    response: str
    error: str | None
    confidence: dict


@dataclass
class AgentState:
    """Dataclass for agent internal processing."""
    query: str
    route: Literal["tool_finder", "org_matcher", "workflow_advisor"] | None = None
    tools_results: list[dict] = field(default_factory=list)
    orgs_results: list[dict] = field(default_factory=list)
    response: str = ""
    error: str | None = None
    confidence: dict = field(default_factory=default_confidence)
    
    @classmethod
    def from_graph_state(cls, state: dict) -> "AgentState":
        """Create AgentState from LangGraph state dict."""
        return cls(
            query=state.get("query", ""),
            route=state.get("route"),
            tools_results=state.get("tools_results", []),
            orgs_results=state.get("orgs_results", []),
            response=state.get("response", ""),
            error=state.get("error"),
            confidence=state.get("confidence", default_confidence())
        )
