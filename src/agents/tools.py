from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.embeddings.openai_embed import get_embedding
from src.retrievers import ToolsRetriever, OrgsRetriever
from src.logger import get_logger

logger = get_logger(__name__)


class ToolSearchInput(BaseModel):
    """Input schema for searching clinical tools."""
    query: str = Field(description="Search query for finding clinical decision support tools")
    limit: int = Field(default=5, description="Maximum number of results to return")


class OrgSearchInput(BaseModel):
    """Input schema for searching healthcare organizations."""
    query: str = Field(description="Search query for finding healthcare organizations with AI implementations")
    limit: int = Field(default=5, description="Maximum number of results to return")


class CombinedSearchInput(BaseModel):
    """Input schema for searching both tools and organizations."""
    query: str = Field(description="Search query for comprehensive clinical workflow recommendations")
    tools_limit: int = Field(default=3, description="Maximum number of tools to return")
    orgs_limit: int = Field(default=3, description="Maximum number of organizations to return")


@tool(args_schema=ToolSearchInput)
def search_clinical_tools(query: str, limit: int = 5) -> list[dict]:
    """
    Search for clinical decision support tools by semantic similarity.
    
    Use this tool when the user asks about:
    - Clinical software and tools
    - Documentation systems
    - Drug reference databases
    - Decision support systems
    - Healthcare IT solutions
    """
    logger.info(f"Tool 'search_clinical_tools' called: query='{query[:50]}...', limit={limit}")
    
    retriever = ToolsRetriever(embed_fn=get_embedding)
    results = retriever.search(query, limit=limit)
    return [
        {
            "name": r["name"],
            "category": r["category"],
            "description": r["description"],
            "problem_solved": r["problem_solved"],
            "target_users": r["target_users"],
            "similarity": round(r["similarity"], 3)
        }
        for r in results
    ]


@tool(args_schema=OrgSearchInput)
def search_healthcare_orgs(query: str, limit: int = 5) -> list[dict]:
    """
    Search for healthcare organizations with AI implementations by semantic similarity.
    
    Use this tool when the user asks about:
    - Hospitals and health systems
    - AI implementation case studies
    - Healthcare organizations using specific technologies
    - Real-world examples of clinical AI
    """
    logger.info(f"Tool 'search_healthcare_orgs' called: query='{query[:50]}...', limit={limit}")
    retriever = OrgsRetriever(embed_fn=get_embedding)
    results = retriever.search(query, limit=limit)
    return [
        {
            "name": r["name"],
            "org_type": r["org_type"],
            "specialty": r["specialty"],
            "city": r["city"],
            "state": r["state"],
            "ai_use_cases": r["ai_use_cases"],
            "similarity": round(r["similarity"], 3)
        }
        for r in results
    ]


@tool(args_schema=CombinedSearchInput)
def search_clinical_workflow(query: str, tools_limit: int = 3, orgs_limit: int = 3) -> dict:
    """
    Search both clinical tools and healthcare organizations for comprehensive workflow recommendations.
    
    Use this tool when the user asks about:
    - Workflow optimization strategies
    - Comprehensive implementation recommendations
    - Combining tools with organizational insights
    - End-to-end clinical AI solutions
    """
    logger.info(f"Tool 'search_clinical_workflow' called: query='{query[:50]}...'")
    tools_retriever = ToolsRetriever(embed_fn=get_embedding)
    orgs_retriever = OrgsRetriever(embed_fn=get_embedding)
    
    tools_results = tools_retriever.search(query, limit=tools_limit)
    orgs_results = orgs_retriever.search(query, limit=orgs_limit)
    
    return {
        "tools": [
            {
                "name": r["name"],
                "category": r["category"],
                "problem_solved": r["problem_solved"],
                "similarity": round(r["similarity"], 3)
            }
            for r in tools_results
        ],
        "organizations": [
            {
                "name": r["name"],
                "specialty": r["specialty"],
                "ai_use_cases": r["ai_use_cases"],
                "similarity": round(r["similarity"], 3)
            }
            for r in orgs_results
        ]
    }


CLINICAL_TOOLS = [search_clinical_tools, search_healthcare_orgs, search_clinical_workflow]
