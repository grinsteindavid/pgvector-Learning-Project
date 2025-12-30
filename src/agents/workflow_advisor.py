import json
import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from src.agents.state import AgentState
from src.retrievers.base import BaseRetriever
from src.logger import get_logger

logger = get_logger(__name__)


WORKFLOW_ADVISOR_PROMPT = """You are a clinical workflow advisor synthesizing recommendations from tools and organizational insights.

Based on the retrieved clinical tools and healthcare organizations below, provide comprehensive workflow recommendations.

Retrieved Tools:
{tools}

Retrieved Organizations:
{orgs}

Provide actionable recommendations that combine tool capabilities with real-world implementation insights.

At the end of your response, add a confidence assessment as JSON on a new line:
{{"response_confidence": 0.0-1.0}}

Confidence reflects how well you could synthesize a comprehensive answer:
- 0.9-1.0: Excellent data from both sources, comprehensive answer
- 0.7-0.9: Good data, solid answer
- 0.5-0.7: Limited data, partial answer
- Below 0.5: Insufficient data, speculative answer"""


class WorkflowAdvisorAgent:
    """Synthesizes recommendations from both tools and organizations."""
    
    def __init__(
        self, 
        tools_retriever: BaseRetriever, 
        orgs_retriever: BaseRetriever, 
        llm: BaseChatModel
    ):
        self.tools_retriever = tools_retriever
        self.orgs_retriever = orgs_retriever
        self.llm = llm
    
    def run(self, state: AgentState) -> AgentState:
        """Search both tables and generate comprehensive response."""
        logger.info(f"WorkflowAdvisor processing: '{state.query[:50]}...'")
        tools_results = self.tools_retriever.search(state.query, limit=3)
        orgs_results = self.orgs_retriever.search(state.query, limit=3)
        
        state.tools_results = tools_results
        state.orgs_results = orgs_results
        logger.info(f"Retrieved {len(tools_results)} tools, {len(orgs_results)} orgs")
        
        state.confidence["retrieval"] = self._calc_retrieval_confidence(
            tools_results, orgs_results
        )
        
        tools_text = self._format_tools(tools_results)
        orgs_text = self._format_orgs(orgs_results)
        
        messages = [
            SystemMessage(content=WORKFLOW_ADVISOR_PROMPT.format(
                tools=tools_text, 
                orgs=orgs_text
            )),
            HumanMessage(content=state.query)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content
        
        state.response, response_conf = self._parse_response(content)
        state.confidence["response"] = response_conf
        
        return state
    
    def _calc_retrieval_confidence(
        self, tools: list[dict], orgs: list[dict]
    ) -> float:
        """Calculate combined retrieval confidence."""
        all_results = tools + orgs
        if not all_results:
            return 0.0
        similarities = [r.get("similarity", 0) for r in all_results]
        return sum(similarities) / len(similarities)
    
    def _parse_response(self, content: str) -> tuple[str, float]:
        """Extract response text and confidence."""
        try:
            match = re.search(r'\{[^}]*"response_confidence"[^}]*\}', content)
            if match:
                data = json.loads(match.group())
                confidence = float(data.get("response_confidence", 0.5))
                text = content[:match.start()].strip()
                return text, min(max(confidence, 0.0), 1.0)
        except (json.JSONDecodeError, ValueError):
            pass
        return content.strip(), 0.5
    
    def _format_tools(self, results: list[dict]) -> str:
        """Format tool results for the prompt."""
        if not results:
            return "No tools found."
        
        lines = []
        for r in results:
            lines.append(f"- **{r['name']}**: {r['problem_solved']}")
        return "\n".join(lines)
    
    def _format_orgs(self, results: list[dict]) -> str:
        """Format org results for the prompt."""
        if not results:
            return "No organizations found."
        
        lines = []
        for r in results:
            lines.append(f"- **{r['name']}** ({r['specialty']}): {', '.join(r['ai_use_cases'])}")
        return "\n".join(lines)
