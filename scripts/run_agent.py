#!/usr/bin/env python3
"""CLI to run the clinical decision support multi-agent."""

import sys
sys.path.insert(0, ".")

from src.logger import setup_app_logger

logger = setup_app_logger("clinical_ai")

from src.agents.graph import create_clinical_graph


def main():
    logger.info("=" * 60)
    logger.info("Clinical Decision Support Multi-Agent")
    logger.info("=" * 60)
    logger.info("Initializing graph...")
    
    try:
        graph = create_clinical_graph()
        logger.info("Graph initialized successfully")
    except Exception as e:
        logger.exception(f"Failed to initialize graph: {e}")
        return
    
    logger.info("Ready! Type your query (or 'quit' to exit)")
    
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ("quit", "exit", "q"):
                logger.info("User requested exit")
                logger.info("Goodbye!")
                break
            
            logger.info(f"User query: {query}")
            
            result = graph.invoke({
                "query": query,
                "route": None,
                "tools_results": [],
                "orgs_results": [],
                "response": "",
                "error": None
            })
            
            route = result.get('route', 'unknown')
            response = result.get('response', 'No response')
            
            logger.info(f"Routed to: {route}")
            logger.info(f"Response length: {len(response)} chars")
            
            print(f"\n[Route: {route}]")
            print(f"\nAssistant: {response}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            logger.info("Application stopped by user (Ctrl+C)")
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.exception(f"Error processing query: {e}")


if __name__ == "__main__":
    main()
