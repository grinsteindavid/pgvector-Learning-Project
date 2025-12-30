import json
import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from src.agents.state import AgentState
from src.retrievers.base import BaseRetriever
from src.logger import get_logger

logger = get_logger(__name__)


ORG_MATCHER_PROMPT = """You are a healthcare organizations specialist helping find relevant case studies and implementations.

Based on the retrieved healthcare organizations below, provide insights about how similar organizations are using AI.

Retrieved Organizations:
{orgs}

Provide a concise summary of relevant implementations and lessons learned.

At the end of your response, add a confidence assessment as JSON on a new line:
{{"response_confidence": 0.0-1.0}}

Confidence reflects how well the retrieved organizations match the query:
- 0.9-1.0: Excellent matches, comprehensive answer
- 0.7-0.9: Good matches, solid answer
- 0.5-0.7: Partial matches, some gaps
- Below 0.5: Poor matches, limited answer"""


class OrgMatcherAgent:
    """Finds relevant healthcare organizations with AI implementations."""
    
    def __init__(self, retriever: BaseRetriever, llm: BaseChatModel):
        self.retriever = retriever
        self.llm = llm
    
    def run(self, state: AgentState) -> AgentState:
        """Search for organizations and generate response."""
        logger.info(f"OrgMatcher processing: '{state.query[:50]}...'")
        results = self.retriever.search(state.query, limit=5)
        state.orgs_results = results
        logger.info(f"Retrieved {len(results)} organizations")
        
        state.confidence["retrieval"] = self._calc_retrieval_confidence(results)
        
        orgs_text = self._format_results(results)
        
        messages = [
            SystemMessage(content=ORG_MATCHER_PROMPT.format(orgs=orgs_text)),
            HumanMessage(content=state.query)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content
        
        state.response, response_conf = self._parse_response(content)
        state.confidence["response"] = response_conf
        
        return state
    
    def _calc_retrieval_confidence(self, results: list[dict]) -> float:
        """Calculate confidence from similarity scores."""
        if not results:
            return 0.0
        similarities = [r.get("similarity", 0) for r in results]
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
    
    def _format_results(self, results: list[dict]) -> str:
        """Format search results for the prompt."""
        if not results:
            return "No organizations found."
        
        lines = []
        for r in results:
            lines.append(f"- **{r['name']}** ({r['specialty']})")
            lines.append(f"  Type: {r['org_type']} | Location: {r['city']}, {r['state']}")
            lines.append(f"  AI Use Cases: {', '.join(r['ai_use_cases'])}")
            lines.append(f"  Similarity: {r['similarity']:.2f}")
            lines.append("")
        return "\n".join(lines)
