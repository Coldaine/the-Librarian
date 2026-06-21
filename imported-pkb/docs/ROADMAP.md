---
title: Roadmap
created: 2026-01-28
last_updated: 2026-01-28
---

# Roadmap

## Vision

A personal knowledge and memory system accessed by LLMs via MCP. Store notes, research, ideas, and project context. Retrieve them naturally through conversation. Answer questions like "What did we do last session?" and "What do I know about X?"

## Phases

### Phase 0: Planning
**Status:** Complete

**Outcome:** Requirements defined, technology chosen.

- Evaluated memory systems, chose Graphiti
- Defined core principles (entity-centric, temporal, cross-tool)
- Documented requirements and use cases

---

### Phase 1: Local Verification
**Status:** Next

**Outcome:** Graphiti MCP server runs locally. You can store and retrieve memories from Claude Code.

**Tasks:**
- Run official Graphiti MCP server with FalkorDB (Docker)
- Configure Minimax API (extraction) and OpenRouter API (embeddings) from BWS
- Connect Claude Code to the MCP server
- Verify basic operations: add episode, search, retrieve

**Exit criteria:** Store a memory, retrieve it later, confirm it works.

---

### Phase 2: Central Deployment
**Status:** Future

**Outcome:** Memory system accessible from any machine via coldane-infra.

**Tasks:**
- Deploy FalkorDB to coldane-infra
- Deploy Graphiti MCP server
- Configure networking and secrets
- Update MCP client configs to point to central URL

**Exit criteria:** Access memories from multiple machines.

---

### Phase 3+: Workflow Refinement
**Status:** Future

**Outcome:** Refined workflows for session continuity, cross-referencing, prompt documentation.

**Tasks:**
- Define session boundary detection approach
- Document common query patterns
- Expand prompt documentation system

---

## Out of Scope

- Hierarchical memory
- Emotional memory
- ScreenPipe integration
- Custom code (using official Graphiti server)

See [deferred.md](requirements/deferred.md) for details.

## Open Questions

1. **Session boundaries** — How do we define "last session"? Time gap? Explicit markers?
2. **Deployment specifics** — Kubernetes vs Docker Compose for coldane-infra

## Technical Decisions

| Component | Choice | Endpoint |
|-----------|--------|----------|
| Extraction LLM | Minimax 2.1 | `https://api.minimax.io/v1` |
| Embeddings | qwen3-embedding-8b via OpenRouter | `https://openrouter.ai/api/v1` |

API keys managed via BWS (Bitwarden Secrets Manager).
