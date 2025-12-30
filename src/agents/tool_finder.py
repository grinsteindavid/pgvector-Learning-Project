import json
import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from src.agents.state import AgentState
from src.retrievers.base import BaseRetriever
from src.logger import get_logger

logger = get_logger(__name__)


TOOL_FINDER_PROMPT = """You are a clinical tools specialist helping healthcare organizations find the right solutions.

Based on the retrieved clinical tools below, provide a helpful response to the user's query.
Focus on how each tool addresses their specific needs.

Retrieved Tools:
{tools}

Provide a concise, actionable recommendation.

At the end of your response, add a confidence assessment as JSON on a new line:
{{"response_confidence": 0.0-1.0}}

Confidence reflects how well the retrieved tools match the query:
- 0.9-1.0: Excellent matches, comprehensive answer
- 0.7-0.9: Good matches, solid answer
- 0.5-0.7: Partial matches, some gaps
- Below 0.5: Poor matches, limited answer"""


class ToolFinderAgent:
    """Finds relevant clinical decision support tools."""
    
    def __init__(self, retriever: BaseRetriever, llm: BaseChatModel):
        self.retriever = retriever
        self.llm = llm
    
    def run(self, state: AgentState) -> AgentState:
        """Search for tools and generate response."""
        logger.info(f"ToolFinder processing: '{state.query[:50]}...'")
        results = self.retriever.search(state.query, limit=5)
        state.tools_results = results
        logger.info(f"Retrieved {len(results)} tools")
        
        state.confidence["retrieval"] = self._calc_retrieval_confidence(results)
        
        tools_text = self._format_results(results)
        
        messages = [
            SystemMessage(content=TOOL_FINDER_PROMPT.format(tools=tools_text)),
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
            return "No tools found."
        
        lines = []
        for r in results:
            lines.append(f"- **{r['name']}** ({r['category']})")
            lines.append(f"  Description: {r['description']}")
            lines.append(f"  Problem Solved: {r['problem_solved']}")
            lines.append(f"  Similarity: {r['similarity']:.2f}")
            lines.append("")
        return "\n".join(lines)
