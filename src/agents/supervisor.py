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

Respond with ONLY one of: tool_finder, org_matcher, workflow_advisor"""


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
        route = response.content.strip().lower()
        
        if route not in ("tool_finder", "org_matcher", "workflow_advisor"):
            logger.warning(f"Invalid route '{route}', defaulting to workflow_advisor")
            route = "workflow_advisor"
        
        logger.info(f"Routed to: {route}")
        state.route = route
        return state
