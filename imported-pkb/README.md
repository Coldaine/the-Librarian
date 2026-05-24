# PersonalKnowledgeBase

A personal knowledge and memory system designed for LLM access, using the **Graphiti temporal knowledge graph**.

## Overview

This repository contains documentation and configuration for a personal knowledge/memory system accessed by LLMs (Claude Code, Gemini CLI, etc.) via MCP.

**Approach**: Use the official [Graphiti MCP Server](https://github.com/getzep/graphiti/tree/main/mcp_server) - no custom code needed.

## Quick Start

See [docs/implementation/SETUP.md](docs/implementation/SETUP.md) for full instructions.

```bash
# Clone Graphiti
git clone https://github.com/getzep/graphiti.git
cd graphiti/mcp_server

# Configure
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Run
docker compose up

# Connect Claude Code to http://localhost:8000/mcp/
```

## Key Concepts

### Entity-Centric Model

Knowledge is organized around **entities** (projects, people, ideas, topics) and their **relationships**:

- Projects are ONE type of entity (first-class workflow)
- Personal notes, ideas, research findings are also entities
- Cross-referencing between entities is natural
- Not everything needs a project - some memories are general

### Temporal Awareness

Graphiti provides bi-temporal knowledge graph:
- When information was stored matters
- Recent cluster vs extended timespan handling
- Session continuity via `get_episodes`

### Optional Scoping

Use `group_id` for project isolation when helpful:
```
add_episode(content="...", group_id="my-project")  # Scoped
add_episode(content="...")                          # General
```

## Documentation

See [docs/INDEX.md](docs/INDEX.md) for full documentation index.

| Document | Description |
|----------|-------------|
| [ROADMAP.md](docs/ROADMAP.md) | Vision, phases, outcomes |
| [SETUP.md](docs/implementation/SETUP.md) | How to run Graphiti MCP server |
| [BLUEPRINT.md](docs/planning/BLUEPRINT.md) | Requirements |
| [CHANGELOG.md](docs/CHANGELOG.md) | Change log |

## Repository Structure

```
PersonalKnowledgeBase/
├── docs/
│   ├── planning/           # Requirements (BLUEPRINT.md)
│   ├── implementation/     # Setup, gaps, journal, todo
│   ├── research/           # Evaluation reports
│   └── IMMUTABLEBACKUPS/   # Historical (don't modify)
├── pyproject.toml          # Minimal project config
└── README.md
```

## Related

- [getzep/graphiti](https://github.com/getzep/graphiti) - The Graphiti framework
- **coldane-infra** - Deployment target for central access
