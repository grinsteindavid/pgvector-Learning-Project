"""PostgreSQL checkpointer for LangGraph state persistence."""

import json
from typing import Any, Optional, Iterator
from datetime import datetime

from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointMetadata
from langgraph.checkpoint.base import CheckpointTuple

from src.db.connection import get_connection
from src.logger import get_logger

logger = get_logger(__name__)


class PostgresCheckpointer(BaseCheckpointSaver):
    """Persist LangGraph checkpoints to PostgreSQL."""
    
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
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO langgraph_checkpoints 
                        (thread_id, checkpoint_id, parent_checkpoint_id, state, metadata)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (thread_id, checkpoint_id) 
                        DO UPDATE SET state = EXCLUDED.state, metadata = EXCLUDED.metadata
                    """, (
                        thread_id,
                        checkpoint_id,
                        parent_id,
                        json.dumps(checkpoint),
                        json.dumps(metadata) if metadata else None
                    ))
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
            with get_connection() as conn:
                with conn.cursor() as cur:
                    if checkpoint_id:
                        cur.execute("""
                            SELECT checkpoint_id, parent_checkpoint_id, state, metadata
                            FROM langgraph_checkpoints
                            WHERE thread_id = %s AND checkpoint_id = %s
                        """, (thread_id, checkpoint_id))
                    else:
                        cur.execute("""
                            SELECT checkpoint_id, parent_checkpoint_id, state, metadata
                            FROM langgraph_checkpoints
                            WHERE thread_id = %s
                            ORDER BY created_at DESC
                            LIMIT 1
                        """, (thread_id,))
                    
                    row = cur.fetchone()
                    
                    if not row:
                        logger.debug(f"No checkpoint found for thread {thread_id}")
                        return None
                    
                    checkpoint_data = row["state"]
                    metadata_data = row["metadata"] or {}
                    
                    logger.debug(f"Retrieved checkpoint {row['checkpoint_id']} for thread {thread_id}")
                    
                    return CheckpointTuple(
                        config={
                            "configurable": {
                                "thread_id": thread_id,
                                "checkpoint_id": row["checkpoint_id"]
                            }
                        },
                        checkpoint=checkpoint_data,
                        metadata=metadata_data,
                        parent_config={
                            "configurable": {
                                "thread_id": thread_id,
                                "checkpoint_id": row["parent_checkpoint_id"]
                            }
                        } if row["parent_checkpoint_id"] else None
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
            with get_connection() as conn:
                with conn.cursor() as cur:
                    query = """
                        SELECT checkpoint_id, parent_checkpoint_id, state, metadata
                        FROM langgraph_checkpoints
                        WHERE thread_id = %s
                        ORDER BY created_at DESC
                    """
                    params = [thread_id]
                    
                    if limit:
                        query += " LIMIT %s"
                        params.append(limit)
                    
                    cur.execute(query, params)
                    
                    for row in cur.fetchall():
                        yield CheckpointTuple(
                            config={
                                "configurable": {
                                    "thread_id": thread_id,
                                    "checkpoint_id": row["checkpoint_id"]
                                }
                            },
                            checkpoint=row["state"],
                            metadata=row["metadata"] or {},
                            parent_config={
                                "configurable": {
                                    "thread_id": thread_id,
                                    "checkpoint_id": row["parent_checkpoint_id"]
                                }
                            } if row["parent_checkpoint_id"] else None
                        )
        except Exception as e:
            logger.exception(f"Failed to list checkpoints: {e}")
            return
