import json
import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from src.agents.state import AgentState
from src.logger import get_logger

logger = get_logger(__name__)


ROUTING_PROMPT = """You are a routing agent for a clinical decision support system.

Analyze the user query and decide which specialist agent should handle it:

- **tool_finder**: Questions about clinical tools, software, documentation systems, drug references, decision support tools
- **org_matcher**: Questions about healthcare organizations, hospitals, health systems, case studies, implementations
- **workflow_advisor**: Complex questions requiring both tools AND organizational context, workflow optimization, comprehensive recommendations

Respond with JSON only: {"route": "tool_finder|org_matcher|workflow_advisor", "confidence": 0.0-1.0}

Confidence reflects how clearly the query matches your chosen route:
- 0.9-1.0: Very clear match to one category
- 0.7-0.9: Good match with minor ambiguity
- 0.5-0.7: Moderate match, could fit multiple categories
- Below 0.5: Unclear, defaulting to best guess"""


class SupervisorAgent:
    """Routes queries to appropriate specialist agents."""
    
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
    
    def route(self, state: AgentState) -> AgentState:
        """Determine which agent should handle the query."""
        logger.info(f"Routing query: '{state.query[:50]}...'")
        messages = [
            SystemMessage(content=ROUTING_PROMPT),
            HumanMessage(content=state.query)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content.strip()
        
        route, confidence = self._parse_response(content)
        
        logger.info(f"Routed to: {route} (confidence: {confidence:.2f})")
        state.route = route
        state.confidence["routing"] = confidence
        return state
    
    def _parse_response(self, content: str) -> tuple[str, float]:
        """Parse JSON response with route and confidence."""
        try:
            match = re.search(r'\{[^}]+\}', content)
            if match:
                data = json.loads(match.group())
                route = data.get("route", "").lower()
                confidence = float(data.get("confidence", 0.5))
            else:
                route = content.lower()
                confidence = 0.5
        except (json.JSONDecodeError, ValueError):
            route = content.split()[0].lower() if content else "workflow_advisor"
            confidence = 0.5
        
        if route not in ("tool_finder", "org_matcher", "workflow_advisor"):
            logger.warning(f"Invalid route '{route}', defaulting to workflow_advisor")
            route = "workflow_advisor"
            confidence = 0.3
        
        return route, min(max(confidence, 0.0), 1.0)
