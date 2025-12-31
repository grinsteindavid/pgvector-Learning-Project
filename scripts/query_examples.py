#!/usr/bin/env python3
"""Example semantic search queries for clinical data."""

import sys
sys.path.insert(0, ".")

from src.retrievers.tools_retriever import ToolsRetriever
from src.retrievers.orgs_retriever import OrgsRetriever
from src.embeddings.openai_embed import get_embedding


def print_org_results(results: list[dict], query: str):
    """Pretty print organization results."""
    print(f"\n{'='*60}")
    print(f"ORGANIZATIONS matching: '{query}'")
    print("="*60)
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['name']} ({r.get('specialty', 'N/A')})")
        print(f"   Type: {r['org_type']} | Location: {r.get('city', 'N/A')}, {r.get('state', 'N/A')}")
        print(f"   AI Use Cases: {', '.join(r.get('ai_use_cases', []))}")
        print(f"   Similarity: {r['similarity']:.4f}")


def print_tool_results(results: list[dict], query: str):
    """Pretty print tool results."""
    print(f"\n{'='*60}")
    print(f"CLINICAL TOOLS matching: '{query}'")
    print("="*60)
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['name']}")
        print(f"   Category: {r['category']}")
        print(f"   Target Users: {', '.join(r.get('target_users', []))}")
        problem = r.get('problem_solved', '')[:80] if r.get('problem_solved') else 'N/A'
        print(f"   Problem Solved: {problem}...")
        print(f"   Similarity: {r['similarity']:.4f}")


def run_examples():
    """Run example semantic searches."""
    
    tools_retriever = ToolsRetriever(embed_fn=get_embedding)
    orgs_retriever = OrgsRetriever(embed_fn=get_embedding)
    
    print("\n" + "="*60)
    print("PGVECTOR SEMANTIC SEARCH EXAMPLES")
    print("="*60)
    
    org_queries = [
        "hospitals using AI to reduce physician burnout",
        "cancer treatment and oncology research",
        "rural healthcare and telemedicine",
        "heart disease and cardiology AI"
    ]
    
    tool_queries = [
        "reduce documentation time for doctors",
        "drug interaction checking and medication safety",
        "clinical trial patient matching",
        "staffing shortages and workforce management"
    ]
    
    print("\n--- ORGANIZATION SEARCHES ---")
    for query in org_queries:
        results = orgs_retriever.search(query, limit=3)
        print_org_results(results, query)
    
    print("\n\n--- CLINICAL TOOL SEARCHES ---")
    for query in tool_queries:
        results = tools_retriever.search(query, limit=3)
        print_tool_results(results, query)
    
    print("\n\n--- COMBINED SEARCH ---")
    query = "AI solutions for clinician burnout and documentation"
    org_results = orgs_retriever.search(query, limit=3)
    tool_results = tools_retriever.search(query, limit=3)
    print_org_results(org_results, "AI for burnout (combined)")
    print_tool_results(tool_results, "AI for burnout (combined)")


if __name__ == "__main__":
    run_examples()
