#!/usr/bin/env python3
"""Seed database with clinical healthcare data."""

import sys
sys.path.insert(0, ".")

from src.seed.run_seed import run_seed

if __name__ == "__main__":
    run_seed()
