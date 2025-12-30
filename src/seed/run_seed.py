import json
from src.db.connection import get_connection
from src.embeddings.openai_embed import get_embeddings_batch
from src.seed.clinical_data import CLINICAL_ORGANIZATIONS, CLINICAL_TOOLS
from src.logger import get_logger

logger = get_logger(__name__)


def create_embedding_text_org(org: dict) -> str:
    """Create text representation for embedding."""
    return f"{org['name']} - {org['org_type']} - {org['specialty']}. {org['description']}"


def create_embedding_text_tool(tool: dict) -> str:
    """Create text representation for embedding."""
    return f"{tool['name']} - {tool['category']}. {tool['description']} {tool['problem_solved']}"


def seed_organizations():
    """Seed clinical organizations with embeddings."""
    logger.info("Generating embeddings for organizations...")
    texts = [create_embedding_text_org(org) for org in CLINICAL_ORGANIZATIONS]
    
    try:
        embeddings = get_embeddings_batch(texts)
    except Exception as e:
        logger.exception(f"Failed to generate organization embeddings: {e}")
        raise
    
    logger.info(f"Inserting {len(CLINICAL_ORGANIZATIONS)} organizations...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for org, embedding in zip(CLINICAL_ORGANIZATIONS, embeddings):
                    cur.execute("""
                        INSERT INTO clinical_organizations 
                        (name, org_type, specialty, description, city, state, services, ai_use_cases, embedding)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        org["name"],
                        org["org_type"],
                        org["specialty"],
                        org["description"],
                        org["city"],
                        org["state"],
                        json.dumps(org["services"]),
                        org["ai_use_cases"],
                        embedding
                    ))
                conn.commit()
        logger.info("Organizations seeded successfully.")
    except Exception as e:
        logger.exception(f"Failed to insert organizations: {e}")
        raise


def seed_tools():
    """Seed clinical tools with embeddings."""
    logger.info("Generating embeddings for clinical tools...")
    texts = [create_embedding_text_tool(tool) for tool in CLINICAL_TOOLS]
    
    try:
        embeddings = get_embeddings_batch(texts)
    except Exception as e:
        logger.exception(f"Failed to generate tool embeddings: {e}")
        raise
    
    logger.info(f"Inserting {len(CLINICAL_TOOLS)} clinical tools...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for tool, embedding in zip(CLINICAL_TOOLS, embeddings):
                    cur.execute("""
                        INSERT INTO clinical_tools 
                        (name, category, description, target_users, problem_solved, embedding)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        tool["name"],
                        tool["category"],
                        tool["description"],
                        tool["target_users"],
                        tool["problem_solved"],
                        embedding
                    ))
                conn.commit()
        logger.info("Clinical tools seeded successfully.")
    except Exception as e:
        logger.exception(f"Failed to insert clinical tools: {e}")
        raise


def run_seed():
    """Run full seeding process."""
    logger.info("Starting seed process...")
    seed_organizations()
    seed_tools()
    logger.info("Seeding complete!")


if __name__ == "__main__":
    run_seed()
