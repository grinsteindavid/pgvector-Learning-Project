# pgvector Learning Project

Hands-on PostgreSQL + pgvector learning with clinical healthcare data.  
**Context:** Case study at Wolters Kluwer Health.

## Quick Start

```bash
# 1. Start PostgreSQL with pgvector
docker-compose up -d

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize schema
python scripts/init_db.py

# 5. Seed data (creates embeddings via OpenAI)
python scripts/seed_db.py

# 6. Run example queries
python scripts/query_examples.py
```

## Study Plan

### Phase 1: PostgreSQL Setup & Basics
- [ ] Run PostgreSQL + pgvector via Docker
- [ ] Connect with DBeaver (localhost:5432, user: pguser, pass: pgpass, db: clinical_ai)
- [ ] Review psql basics: `\dt`, `\d table_name`, `\x`
- [ ] Practice: JSONB, arrays, basic indexing

### Phase 2: pgvector Fundamentals
- [ ] Understand `vector(1536)` data type (matches OpenAI embedding dimension)
- [ ] Learn distance operators:
  - `<->` L2 distance (Euclidean)
  - `<#>` Inner product (negative)
  - `<=>` Cosine distance
- [ ] Create and compare index types:
  - `USING ivfflat` - faster build, good for millions of rows
  - `USING hnsw` - slower build, better recall (recommended)
- [ ] Analyze queries with `EXPLAIN ANALYZE`

### Phase 3: Python Integration
- [ ] Create embeddings with OpenAI `text-embedding-3-small`
- [ ] Insert vectors using psycopg3
- [ ] Implement semantic search queries
- [ ] Batch processing for efficiency

### Phase 4: LangGraph Integration
- [ ] Use vectorstore as retriever in LangGraph nodes
- [ ] Implement agent memory patterns
- [ ] Cross-agent knowledge sharing

---

## Database Schema

### clinical_organizations
Healthcare systems and facilities with AI use cases relevant to Wolters Kluwer Health's market.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR | Organization name |
| org_type | VARCHAR | health_system, academic_medical_center, etc. |
| specialty | VARCHAR | Primary specialty focus |
| description | TEXT | Detailed description (embedded) |
| city, state | VARCHAR | Location |
| services | JSONB | Service capabilities |
| ai_use_cases | TEXT[] | AI applications in use |
| embedding | vector(1536) | OpenAI embedding |

### clinical_tools
Clinical decision support and healthcare IT tools (aligned with WK Health products).

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR | Tool name |
| category | VARCHAR | CDS, Documentation, Analytics, etc. |
| description | TEXT | Full description (embedded) |
| target_users | TEXT[] | Intended user roles |
| problem_solved | TEXT | Problem addressed |
| embedding | vector(1536) | OpenAI embedding |

---

## Key SQL Patterns

### Create pgvector extension
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Create table with vector column
```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)
);
```

### Create HNSW index (recommended)
```sql
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);
```

### Semantic search (cosine similarity)
```sql
SELECT name, description,
       1 - (embedding <=> $1::vector) AS similarity
FROM clinical_organizations
ORDER BY embedding <=> $1::vector
LIMIT 5;
```

### Filter + semantic search
```sql
SELECT * FROM clinical_organizations
WHERE org_type = 'health_system'
ORDER BY embedding <=> $1::vector
LIMIT 5;
```

### Analyze query plan
```sql
EXPLAIN ANALYZE
SELECT * FROM clinical_organizations
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 5;
```

---

## Distance Operators Reference

| Operator | Function | Use Case |
|----------|----------|----------|
| `<->` | L2 distance | General similarity |
| `<=>` | Cosine distance | **Recommended for text embeddings** |
| `<#>` | Negative inner product | When vectors are normalized |

**Note:** Lower distance = more similar. For cosine, `1 - distance = similarity score`.

---

## Project Structure

```
pgvectors/
├── docker-compose.yml      # PostgreSQL 16 + pgvector
├── requirements.txt        # Python dependencies
├── .env                    # API keys (gitignored)
├── src/
│   ├── config.py           # Configuration
│   ├── db/
│   │   ├── connection.py   # Database connection
│   │   └── schema.py       # Schema initialization
│   ├── embeddings/
│   │   └── openai_embed.py # OpenAI embedding helper
│   ├── seed/
│   │   ├── clinical_data.py # Sample healthcare data
│   │   └── run_seed.py     # Seeding script
│   └── queries/
│       └── similarity.py   # Semantic search functions
└── scripts/
    ├── init_db.py          # Initialize schema
    ├── seed_db.py          # Run seeding
    └── query_examples.py   # Test queries
```

---

## DBeaver Connection

| Setting | Value |
|---------|-------|
| Host | localhost |
| Port | 5432 |
| Database | clinical_ai |
| Username | pguser |
| Password | pgpass |

---

## Wolters Kluwer Health Context

This project simulates data relevant to WK Health's focus areas:

- **Clinical Decision Support** - UpToDate, Lexicomp
- **Clinician Burnout Reduction** - Documentation AI, workflow automation
- **Staffing Shortages** - Predictive scheduling, resource optimization
- **Drug Safety** - Interaction checking, alerts
- **Evidence-Based Care** - Clinical pathways, quality analytics

Semantic search enables finding relevant organizations and tools based on natural language queries about clinical challenges.
