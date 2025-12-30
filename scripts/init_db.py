#!/usr/bin/env python3
"""Initialize database schema with pgvector extension."""

import sys
sys.path.insert(0, ".")

from src.db.schema import init_schema

if __name__ == "__main__":
    print("Initializing database schema...")
    init_schema()
