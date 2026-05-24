# Graphiti MCP Server Setup

*Instructions for running the official Graphiti MCP server for PKB*

---

## Overview

We use the **official Graphiti MCP server** from [getzep/graphiti](https://github.com/getzep/graphiti). This provides:

- Temporal knowledge graph for memory storage
- Entity extraction from natural language
- Semantic + hybrid search
- Optional `group_id` scoping for projects
- Built-in entity types (Preference, Requirement, Topic, etc.)

---

## Prerequisites

- Docker and Docker Compose
- Minimax API key (for entity extraction LLM) — stored in BWS
- OpenRouter API key (for embeddings) — stored in BWS

---

## Quick Start

### 1. Clone Graphiti

```bash
git clone https://github.com/getzep/graphiti.git
cd graphiti/mcp_server
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```bash
# Minimax for entity extraction LLM
MINIMAX_API_KEY=<from BWS>

# OpenRouter for embeddings
OPENROUTER_API_KEY=<from BWS>

# Optional: disable telemetry
GRAPHITI_TELEMETRY_ENABLED=false
```

### 3. Configure LLM and Embeddings

Graphiti uses OpenAI-compatible APIs. Configure with custom endpoints:

```python
import os
from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig

# LLM for entity extraction - Minimax 2.1
llm_client = OpenAIGenericClient(config=LLMConfig(
    api_key=os.environ["MINIMAX_API_KEY"],
    model="MiniMax-M2.1",
    base_url="https://api.minimax.io/v1",
))

# Embeddings - OpenRouter
embedder = OpenAIEmbedder(config=OpenAIEmbedderConfig(
    api_key=os.environ["OPENROUTER_API_KEY"],
    embedding_model="qwen/qwen3-embedding-8b",
    base_url="https://openrouter.ai/api/v1",
))
```

**Note:** Both API keys are managed via BWS (Bitwarden Secrets Manager). See global CLAUDE.md for secrets management.

### 4. Start the Server

```bash
docker compose up
```

This starts:
- FalkorDB on `localhost:6379`
- MCP server on `http://localhost:8000/mcp/`
- FalkorDB web UI on `http://localhost:3000`

---

## Connect Claude Code

Add to Claude Code MCP configuration:

### Option A: HTTP Transport (Cursor, VS Code)

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

### Option B: stdio Transport (Claude Desktop)

Claude Desktop doesn't support HTTP natively. Use `mcp-remote`:

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8000/mcp/"]
    }
  }
}
```

---

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `add_episode` | Store a memory (auto-extracts entities) |
| `search_nodes` | Find entity summaries |
| `search_facts` | Find relationships between entities |
| `get_episodes` | Get recent episodes (session continuity) |
| `delete_episode` | Remove a memory |
| `get_status` | Check server health |

---

## Using group_id for Projects

The `group_id` parameter provides optional scoping. Use it for project organization:

```
# Store memory scoped to a project
add_episode(
  name="PKB decision",
  episode_body="Decided to use entity-centric model instead of project-centric",
  group_id="pkb-project"
)

# Store general memory (no project)
add_episode(
  name="Quick note",
  episode_body="Dentist Tuesday 3pm"
)

# Search within project scope
search_facts(
  query="architecture decisions",
  group_ids=["pkb-project"]
)

# Search across everything
search_facts(
  query="what do I know about graph databases"
)
```

---

## Entity Types

Graphiti auto-extracts these entity types from your memories:

- **Preference** - choices, opinions
- **Requirement** - needs, features
- **Procedure** - instructions, workflows
- **Location** - places
- **Event** - activities, occurrences
- **Organization** - companies, groups
- **Document** - articles, reports
- **Topic** - subjects, domains
- **Object** - items, tools

---

## Session Continuity

To implement "What did we do last session?":

```
# Get recent episodes for a project
get_episodes(
  group_id="pkb-project",
  limit=20
)
```

This returns recent memories scoped to that project, enabling session continuity queries.

---

## Deployment to coldane-infra

For central deployment (accessible everywhere):

1. Deploy FalkorDB to coldane-infra
2. Deploy Graphiti MCP server pointing to that FalkorDB
3. Configure MCP clients to point to deployed URL

*TODO: Document coldane-infra deployment steps*

---

## References

- [Graphiti MCP Server README](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md)
- [Graphiti Documentation](https://help.getzep.com/graphiti/getting-started/welcome)
- [FalkorDB Documentation](https://docs.falkordb.com/)
