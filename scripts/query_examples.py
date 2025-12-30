#!/usr/bin/env python3
"""Example semantic search queries for clinical data."""

import sys
sys.path.insert(0, ".")

from src.queries.similarity import search_organizations, search_tools, search_all


def print_org_results(results: list[dict], query: str):
    """Pretty print organization results."""
    print(f"\n{'='*60}")
    print(f"ORGANIZATIONS matching: '{query}'")
    print("="*60)
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['name']} ({r['specialty']})")
        print(f"   Type: {r['org_type']} | Location: {r['city']}, {r['state']}")
        print(f"   AI Use Cases: {', '.join(r['ai_use_cases'])}")
        print(f"   Similarity: {r['similarity']:.4f}")


def print_tool_results(results: list[dict], query: str):
    """Pretty print tool results."""
    print(f"\n{'='*60}")
    print(f"CLINICAL TOOLS matching: '{query}'")
    print("="*60)
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['name']}")
        print(f"   Category: {r['category']}")
        print(f"   Target Users: {', '.join(r['target_users'])}")
        print(f"   Problem Solved: {r['problem_solved'][:80]}...")
        print(f"   Similarity: {r['similarity']:.4f}")


def run_examples():
    """Run example semantic searches."""
    
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
        results = search_organizations(query, limit=3)
        print_org_results(results, query)
    
    print("\n\n--- CLINICAL TOOL SEARCHES ---")
    for query in tool_queries:
        results = search_tools(query, limit=3)
        print_tool_results(results, query)
    
    print("\n\n--- COMBINED SEARCH ---")
    combined = search_all("AI solutions for clinician burnout and documentation", limit=3)
    print_org_results(combined["organizations"], "AI for burnout (combined)")
    print_tool_results(combined["tools"], "AI for burnout (combined)")


if __name__ == "__main__":
    run_examples()
