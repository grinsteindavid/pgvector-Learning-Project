"""PostgreSQL checkpointer for LangGraph state persistence using SQLAlchemy."""

import json
from typing import Optional, Iterator

from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata
from langgraph.checkpoint.base import CheckpointTuple
from sqlalchemy import text

from src.db.models.base import engine
from src.logger import get_logger

logger = get_logger(__name__)


class PostgresCheckpointer(BaseCheckpointSaver):
    """Persist LangGraph checkpoints to PostgreSQL using SQLAlchemy."""
    
    def put(
        self,
        config: dict,
        checkpoint: Checkpoint,
        metadata: CheckpointMetadata,
        new_versions: dict
    ) -> dict:
        """Save a checkpoint to the database."""
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_id = checkpoint.get("id")
        parent_id = config.get("configurable", {}).get("checkpoint_id")
        
        if not thread_id:
            raise ValueError("thread_id is required in config")
        
        logger.info(f"Saving checkpoint {checkpoint_id} for thread {thread_id}")
        
        try:
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO langgraph_checkpoints 
                    (thread_id, checkpoint_id, parent_checkpoint_id, state, metadata)
                    VALUES (:thread_id, :checkpoint_id, :parent_id, :state, :metadata)
                    ON CONFLICT (thread_id, checkpoint_id) 
                    DO UPDATE SET state = EXCLUDED.state, metadata = EXCLUDED.metadata
                """), {
                    "thread_id": thread_id,
                    "checkpoint_id": checkpoint_id,
                    "parent_id": parent_id,
                    "state": json.dumps(checkpoint),
                    "metadata": json.dumps(metadata) if metadata else None
                })
                conn.commit()
            
            return {
                "configurable": {
                    "thread_id": thread_id,
                    "checkpoint_id": checkpoint_id
                }
            }
        except Exception as e:
            logger.exception(f"Failed to save checkpoint: {e}")
            raise
    
    def put_writes(
        self,
        config: dict,
        writes: list,
        task_id: str
    ) -> None:
        """Save intermediate writes (no-op for simple implementation)."""
        pass
    
    def get_tuple(self, config: dict) -> Optional[CheckpointTuple]:
        """Get the latest checkpoint for a thread."""
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_id = config.get("configurable", {}).get("checkpoint_id")
        
        if not thread_id:
            return None
        
        try:
            with engine.connect() as conn:
                if checkpoint_id:
                    result = conn.execute(text("""
                        SELECT checkpoint_id, parent_checkpoint_id, state, metadata
                        FROM langgraph_checkpoints
                        WHERE thread_id = :thread_id AND checkpoint_id = :checkpoint_id
                    """), {"thread_id": thread_id, "checkpoint_id": checkpoint_id})
                else:
                    result = conn.execute(text("""
                        SELECT checkpoint_id, parent_checkpoint_id, state, metadata
                        FROM langgraph_checkpoints
                        WHERE thread_id = :thread_id
                        ORDER BY created_at DESC
                        LIMIT 1
                    """), {"thread_id": thread_id})
                
                row = result.fetchone()
                
                if not row:
                    logger.debug(f"No checkpoint found for thread {thread_id}")
                    return None
                
                row_dict = row._mapping
                checkpoint_data = row_dict["state"]
                metadata_data = row_dict["metadata"] or {}
                
                logger.debug(f"Retrieved checkpoint {row_dict['checkpoint_id']} for thread {thread_id}")
                
                return CheckpointTuple(
                    config={
                        "configurable": {
                            "thread_id": thread_id,
                            "checkpoint_id": row_dict["checkpoint_id"]
                        }
                    },
                    checkpoint=checkpoint_data,
                    metadata=metadata_data,
                    parent_config={
                        "configurable": {
                            "thread_id": thread_id,
                            "checkpoint_id": row_dict["parent_checkpoint_id"]
                        }
                    } if row_dict["parent_checkpoint_id"] else None
                )
        except Exception as e:
            logger.exception(f"Failed to get checkpoint: {e}")
            return None
    
    def list(
        self,
        config: Optional[dict],
        *,
        filter: Optional[dict] = None,
        before: Optional[dict] = None,
        limit: Optional[int] = None
    ) -> Iterator[CheckpointTuple]:
        """List checkpoints for a thread."""
        if not config:
            return
        
        thread_id = config.get("configurable", {}).get("thread_id")
        if not thread_id:
            return
        
        try:
            with engine.connect() as conn:
                query = """
                    SELECT checkpoint_id, parent_checkpoint_id, state, metadata
                    FROM langgraph_checkpoints
                    WHERE thread_id = :thread_id
                    ORDER BY created_at DESC
                """
                params = {"thread_id": thread_id}
                
                if limit:
                    query += " LIMIT :limit"
                    params["limit"] = limit
                
                result = conn.execute(text(query), params)
                
                for row in result:
                    row_dict = row._mapping
                    yield CheckpointTuple(
                        config={
                            "configurable": {
                                "thread_id": thread_id,
                                "checkpoint_id": row_dict["checkpoint_id"]
                            }
                        },
                        checkpoint=row_dict["state"],
                        metadata=row_dict["metadata"] or {},
                        parent_config={
                            "configurable": {
                                "thread_id": thread_id,
                                "checkpoint_id": row_dict["parent_checkpoint_id"]
                            }
                        } if row_dict["parent_checkpoint_id"] else None
                    )
        except Exception as e:
            logger.exception(f"Failed to list checkpoints: {e}")
            return
