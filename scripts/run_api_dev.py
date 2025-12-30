#!/usr/bin/env python
"""Development API server with auto-reload and schema init."""

import sys
sys.path.insert(0, '/app')

from src.db.schema import init_schema
from src.api import create_app

if __name__ == '__main__':
    init_schema()
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
