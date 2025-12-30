# Clinical Decision Support Multi-Agent System

A LangGraph multi-agent system for clinical decision support, leveraging pgvector for semantic search over healthcare data.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://github.com/langchain-ai/langgraph)
[![PostgreSQL 16](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://www.postgresql.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-red.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://react.dev/)

<img width="877" height="749" alt="image" src="https://github.com/user-attachments/assets/e132526a-de05-49ef-8b2f-9d40c5144439" />


---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Database Schema](#database-schema)
- [Development](#development)

---

## Overview

This system provides intelligent clinical decision support through a multi-agent architecture:

| Agent | Responsibility |
|-------|----------------|
| **Supervisor** | Routes queries to specialist agents |
| **Tool Finder** | Searches clinical tools and software |
| **Org Matcher** | Finds healthcare organizations with AI implementations |
| **Workflow Advisor** | Synthesizes comprehensive recommendations |

### Key Features

- **Semantic Search** - pgvector-powered similarity search over clinical data
- **Multi-Agent Routing** - Intelligent query classification and delegation
- **Streaming API** - Real-time Server-Sent Events (SSE) for progressive responses
- **React Chat UI** - Modern streaming chat interface with thread persistence
- **LangGraph Checkpoints** - PostgreSQL-backed conversation state persistence
- **Docker Ready** - Separate dev/prod configurations

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React UI      │     │   Flask API     │     │   PostgreSQL    │
│   (Vite/nginx)  │────▶│   (gunicorn)    │────▶│   (pgvector)    │
│   Port 3000     │ SSE │   Port 5000     │     │   Port 5432     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     LangGraph       │
                    │   Multi-Agent       │
                    │                     │
                    │  ┌───────────────┐  │
                    │  │  Supervisor   │  │
                    │  └───────┬───────┘  │
                    │          │          │
                    │  ┌───────┴───────┐  │
                    │  ▼       ▼       ▼  │
                    │ Tool   Org   Workflow│
                    │ Finder Matcher Advisor│
                    └─────────────────────┘
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key

### 1. Clone and Configure

```bash
git clone https://github.com/grinsteindavid/pgvector-Learning-Project.git
cd pgvector-Learning-Project

cp .env.example .env
# Edit .env with your OpenAI API key
```

### 2. Start Development Environment

```bash
make dev
```

This starts all services with hot-reload:
- **UI**: http://localhost:3000
- **API**: http://localhost:5000
- **PostgreSQL**: localhost:5432

### 3. Seed Database (optional)

```bash
make init-db
make seed-db
```

### Available Commands

```bash
make dev       # Start development environment (hot-reload)
make prod      # Start production environment
make down      # Stop all containers
make logs      # View container logs
make test      # Run test suite
make clean     # Remove containers, volumes, and cache
```

---

## API Reference

### Health Check

```
GET /health
```

### Standard Query

```
POST /api/query
Content-Type: application/json

{"query": "How can we reduce documentation burden?"}
```

**Response:**
```json
{
  "route": "tool_finder",
  "response": "Based on your query...",
  "tools_results": [...],
  "orgs_results": [...]
}
```

### Streaming Query (SSE)

```
POST /api/query/stream
Content-Type: application/json

{"query": "What tools help with drug interactions?"}
```

**Response:** Server-Sent Events stream
```
data: {"node": "supervisor", "data": {"route": "tool_finder"}}
data: {"node": "tool_finder", "data": {"response": "..."}}
data: [DONE]
```

See [API Documentation](docs/api.md) for complete reference.

---

## Project Structure

```
pgvectors/
├── .env.example                 # Environment template
├── Makefile                     # Dev/prod commands
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Dev/test dependencies
├── pytest.ini                   # Test configuration
│
├── compose/                     # Docker Compose configs
│   ├── docker-compose.yml       # Base services
│   ├── docker-compose.dev.yml   # Dev overrides (hot-reload)
│   └── docker-compose.prod.yml  # Prod overrides (optimized)
│
├── docker/                      # Dockerfiles
│   ├── api/
│   │   ├── Dockerfile           # Production API
│   │   └── Dockerfile.dev       # Development API
│   └── ui/
│       ├── Dockerfile           # Production UI (nginx)
│       ├── Dockerfile.dev       # Development UI (vite)
│       └── nginx.conf           # Production nginx config
│
├── docs/                        # Documentation
│   ├── api.md                   # API reference
│   └── architecture.md          # System design
│
├── scripts/                     # CLI utilities
│   ├── init_db.py               # Initialize schema
│   ├── seed_db.py               # Seed database
│   ├── run_agent.py             # CLI agent
│   └── query_examples.py        # Example queries
│
├── src/                         # Python application
│   ├── config.py                # Configuration
│   ├── logger.py                # Logging setup
│   ├── api/                     # Flask REST API
│   │   ├── app.py               # App factory
│   │   └── routes/
│   │       ├── health.py        # Health endpoint
│   │       ├── agent.py         # Query endpoints
│   │       └── threads.py       # Thread management
│   ├── agents/                  # LangGraph agents
│   │   ├── state.py             # State definition
│   │   ├── graph.py             # Workflow graph
│   │   ├── supervisor.py        # Router agent
│   │   ├── tool_finder.py       # Tools agent
│   │   ├── org_matcher.py       # Orgs agent
│   │   └── workflow_advisor.py  # Synthesis agent
│   ├── db/                      # Database layer
│   │   ├── connection.py        # Connection pool
│   │   ├── schema.py            # Schema init
│   │   ├── checkpointer.py      # LangGraph checkpoints
│   │   └── threads.py           # Thread persistence
│   ├── retrievers/              # pgvector search
│   │   ├── base.py              # Abstract retriever
│   │   ├── tools_retriever.py   # Tools search
│   │   └── orgs_retriever.py    # Orgs search
│   └── embeddings/
│       └── openai_embed.py      # OpenAI embeddings
│
├── tests/                       # Test suite
│   ├── conftest.py              # Fixtures
│   ├── mocks/                   # Mock implementations
│   ├── unit/                    # Unit tests
│   └── integration/             # E2E tests
│
├── ui/                          # React frontend
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx
│       ├── components/
│       │   ├── Chat.tsx         # Chat interface
│       │   └── Sidebar.tsx      # Thread list
│       ├── hooks/
│       │   └── useThreads.ts    # Thread state
│       └── types/
│           └── thread.ts        # TypeScript types
│
└── logs/                        # Log files (gitignored)
```

---

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-proj-...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/vectordb` |

### Logging

Logs are written to `logs/agent_run_YYYYMMDD_HHMMSS.log` and console.

```python
from src.logger import get_logger
logger = get_logger(__name__)
logger.info("Processing query...")
```

---

## Testing

### Unit Tests (No Network)

```bash
pytest tests/unit -v
```

### Integration Tests (Requires DB + API Key)

```bash
RUN_INTEGRATION_TESTS=1 pytest tests/integration -v
```

### Test Coverage

- 29 unit tests with mocked embeddings and database
- 3 integration tests for end-to-end flow
- Live log output during test execution

---

## Docker Deployment

### Development (Hot-Reload)

```bash
make dev
# Or manually:
docker compose -f compose/docker-compose.yml -f compose/docker-compose.dev.yml up
```

Features:
- Source code mounted as volumes
- Flask debug mode with auto-reload
- Vite dev server with HMR
- Logs visible in terminal

### Production (Optimized)

```bash
make prod
# Or manually:
docker compose -f compose/docker-compose.yml -f compose/docker-compose.prod.yml up -d
```

Features:
- Multi-stage builds (smaller images)
- gunicorn with 4 workers
- nginx serving static assets
- Health checks enabled

### Access

| Service | Dev | Prod |
|---------|-----|------|
| UI | http://localhost:3000 | http://localhost:3000 |
| API | http://localhost:5000 | http://localhost:5000 |
| PostgreSQL | localhost:5432 | localhost:5432 |

---

## Database Schema

### clinical_organizations

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(255) | Organization name |
| org_type | VARCHAR(50) | health_system, academic_medical_center |
| specialty | VARCHAR(100) | Primary specialty focus |
| description | TEXT | Detailed description (embedded) |
| city, state | VARCHAR | Location |
| services | JSONB | Service capabilities |
| ai_use_cases | TEXT[] | AI applications in use |
| embedding | vector(1536) | OpenAI text-embedding-3-small |

### clinical_tools

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(255) | Tool name |
| category | VARCHAR(100) | CDS, Documentation, Analytics |
| description | TEXT | Full description (embedded) |
| target_users | TEXT[] | Intended user roles |
| problem_solved | TEXT | Problem addressed |
| embedding | vector(1536) | OpenAI text-embedding-3-small |

### chat_threads

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| title | VARCHAR(255) | Thread title |
| created_at | TIMESTAMPTZ | Creation timestamp |
| updated_at | TIMESTAMPTZ | Last update |

### chat_messages

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| thread_id | UUID | Foreign key to chat_threads |
| role | VARCHAR(20) | 'user' or 'assistant' |
| content | TEXT | Message content |
| route | VARCHAR(50) | Agent route used |
| created_at | TIMESTAMPTZ | Creation timestamp |

### HNSW Indexes

```sql
CREATE INDEX idx_org_embedding ON clinical_organizations 
    USING hnsw (embedding vector_cosine_ops);

CREATE INDEX idx_tool_embedding ON clinical_tools 
    USING hnsw (embedding vector_cosine_ops);
```

---

## Development

### Dev vs Prod

| Aspect | Development | Production |
|--------|-------------|------------|
| API Server | Flask debug (reload) | gunicorn (4 workers) |
| UI Server | Vite dev server | nginx + static |
| Code | Volume mounts | Built into image |
| Debugging | Enabled | Disabled |

### Adding New Agents

1. Create agent file in `src/agents/`
2. Define agent class with `run(state: AgentState)` method
3. Register in `src/agents/graph.py`
4. Add routing logic in `src/agents/supervisor.py`

### Adding New Retrievers

1. Create retriever in `src/retrievers/`
2. Extend `BaseRetriever` abstract class
3. Implement `search(query, limit)` method
4. Add to `src/retrievers/__init__.py`

### Code Style

- Functions and files should be short and focused
- One concept per file
- Descriptive naming based on responsibility
- Logging for all significant operations

---

## License

MIT License

---

## Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - Multi-agent framework
- [pgvector](https://github.com/pgvector/pgvector) - Vector similarity for PostgreSQL
- [OpenAI](https://openai.com) - Embeddings and LLM
- Healthcare domain context inspired by Wolters Kluwer Health
