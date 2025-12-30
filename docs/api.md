# Clinical Decision Support API

Flask-based REST API for the Clinical Decision Support Multi-Agent system.

## Endpoints

### Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "clinical-ai-agent"
}
```

---

### Standard Query

```
POST /api/query
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "How can we reduce documentation burden for physicians?"
}
```

**Response:**
```json
{
  "route": "tool_finder",
  "response": "Based on your query, I recommend...",
  "tools_results": [...],
  "orgs_results": []
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "reduce documentation burden"}'
```

---

### Streaming Query (SSE)

```
POST /api/query/stream
Content-Type: application/json
```

Streams events as Server-Sent Events (SSE).

**Response:** `text/event-stream`
```
data: {"node": "supervisor", "data": {"route": "tool_finder"}}
data: {"node": "tool_finder", "data": {"tools_results": [...], "response": "..."}}
data: [DONE]
```

---

### Thread Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/threads` | List all threads |
| POST | `/api/threads` | Create new thread |
| GET | `/api/threads/:id` | Get thread with messages |
| DELETE | `/api/threads/:id` | Delete thread |
| POST | `/api/threads/:id/query` | Query with thread context |
| POST | `/api/threads/:id/query/stream` | Streaming with thread |

---

## Routing Logic

| Route | Triggered By |
|-------|--------------|
| `tool_finder` | Questions about clinical tools, software, documentation |
| `org_matcher` | Questions about hospitals, health systems, case studies |
| `workflow_advisor` | Complex questions requiring both tools and org context |

---

## Error Handling

**400 Bad Request:**
```json
{"error": "Missing 'query' field"}
```

**500 Internal Server Error:**
```json
{"error": "Error message details"}
```
