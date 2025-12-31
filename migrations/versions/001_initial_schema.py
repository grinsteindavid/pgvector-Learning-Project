"""Initial schema with all tables

Revision ID: 001
Revises: 
Create Date: 2024-12-30
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from pgvector.sqlalchemy import Vector

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    op.create_table(
        'clinical_organizations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('org_type', sa.String(50), nullable=False),
        sa.Column('specialty', sa.String(100)),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('city', sa.String(100)),
        sa.Column('state', sa.String(50)),
        sa.Column('services', JSON, default={}),
        sa.Column('ai_use_cases', ARRAY(sa.Text)),
        sa.Column('embedding', Vector(1536)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    
    op.create_table(
        'clinical_tools',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('target_users', ARRAY(sa.Text)),
        sa.Column('problem_solved', sa.Text()),
        sa.Column('embedding', Vector(1536)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    
    op.create_table(
        'chat_threads',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(255), server_default='New Chat'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )
    
    op.create_table(
        'chat_messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('thread_id', UUID(as_uuid=True), sa.ForeignKey('chat_threads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('route', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    
    op.create_table(
        'langgraph_checkpoints',
        sa.Column('thread_id', UUID(as_uuid=True), sa.ForeignKey('chat_threads.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('checkpoint_id', sa.String(255), primary_key=True),
        sa.Column('parent_checkpoint_id', sa.String(255)),
        sa.Column('state', JSON, nullable=False),
        sa.Column('metadata', JSON),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    
    op.create_index('idx_org_embedding', 'clinical_organizations', ['embedding'], postgresql_using='hnsw', postgresql_ops={'embedding': 'vector_cosine_ops'})
    op.create_index('idx_tool_embedding', 'clinical_tools', ['embedding'], postgresql_using='hnsw', postgresql_ops={'embedding': 'vector_cosine_ops'})
    op.create_index('idx_messages_thread', 'chat_messages', ['thread_id', 'created_at'])


def downgrade() -> None:
    op.drop_index('idx_messages_thread')
    op.drop_index('idx_tool_embedding')
    op.drop_index('idx_org_embedding')
    op.drop_table('langgraph_checkpoints')
    op.drop_table('chat_messages')
    op.drop_table('chat_threads')
    op.drop_table('clinical_tools')
    op.drop_table('clinical_organizations')
