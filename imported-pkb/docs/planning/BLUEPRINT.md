# Personal Knowledge Base - Blueprint

*Draft v0.2 - January 2026*
*Derived from Phase 1 planning session. Updated to reflect Graphiti/FalkorDB pivot (Jan 20).*

---

## Overview

This blueprint organizes all requirements, principles, and use cases from the Phase 1 planning document into a structured format to prepare for execution.

---

## 1. Core Principles

These apply to the entire system:

| Principle | Description |
|-----------|-------------|
| **LLM-Controlled** | Access is almost always through LLMs, not manual browsing/editing. Manual only for debugging or automation. |
| **Temporal Primacy** | When information was stored/learned is critical context. Two modes: recent cluster (order matters) vs extended timespan (age matters significantly). |
| **Entity-Centric** | Knowledge is organized around entities (projects, people, ideas, topics) and their relationships. Projects are a first-class entity type with dedicated workflows, but not all memories require a project. |
| **Cross-Tool** | Must work across Claude Code, Gemini CLI, and all tooling via MCP server. |

---

## 2. Phase Structure

| Phase | Scope | Status |
|-------|-------|--------|
| **Phase 0** | Planning - enumerate requirements, decide what to nail down vs defer | COMPLETE |
| **Phase 1** | Run Graphiti MCP server locally with FalkorDB. Verify MCP tools work. Test from Claude Code. | NEXT |
| **Phase 2** | Deploy to coldane-infra for central access. Refine workflows (session continuity, cross-referencing). | FUTURE |
| **Phase 3+** | Expand prompting rigor to all globals, then all projects. | FUTURE |

**Technology decisions (Phase 0 outcome):** Graphiti temporal knowledge graph, FalkorDB backend, official Graphiti MCP server. LLM: Minimax 2.1 (via OpenAI-compatible API). Embeddings: OpenRouter (qwen3-embedding-8b). API keys via BWS. See [JOURNAL.md](../implementation/JOURNAL.md) for decision rationale.

---

## 3. Repository Relationship

```
┌─────────────────────────────────────┐
│         coldane-infra               │
│  - Deployment information           │
│  - Hosting details                  │
│  - Infrastructure setup             │
│  - Syncs/deploys to all machines    │
└─────────────────┬───────────────────┘
                  │
                  │ references for infra answers
                  ▼
┌─────────────────────────────────────┐
│   PersonalKnowledgeBase (this repo) │
│  - Memory system implementation     │
│  - Can embed secrets as needed      │
│  - Prototype prompt patterns here   │
└─────────────────────────────────────┘
                  │
                  │ future
                  ▼
┌─────────────────────────────────────┐
│   Shared Git Submodule (future)     │
│  - Canonical global prompts         │
│  - Prompt documentation pattern     │
│  - Consumed by both repos           │
└─────────────────────────────────────┘
```

---

## 4. Hard Requirements

1. **Session continuity** - Enable "What did we do last session?" queries for projects and other contexts
2. **Entity relationships** - Memories connect to entities (projects, people, ideas, topics) and can be cross-referenced. Projects are a primary workflow but not the only organizing principle.
3. **Cross-tool access** - MCP server works across all LLM tooling (Claude Code, Gemini CLI, etc.)
4. **Accessible everywhere** - Quick notes/memories must be reachable from any context, with or without project association

---

## 5. Problems to Solve (Use Cases)

| # | Problem | Memory System Solution |
|---|---------|----------------------|
| 1 | LLMs have stale training data (~2024 cutoff), hallucinate outdated info | Store research/learnings; LLMs can query for up-to-date context |
| 2 | Trouble putting down projects - unsure what was done last | Per-project session continuity queries |
| 3 | Important info buried in verbose documentation | North Star concept - short bulleted requirements per project (in flux) |
| 4 | Quick notes get lost without central place | Notes go into memory system, searchable, temporally aware |
| 5 | Article ideas scattered and unfindable | Central findable storage for ideas |
| 6 | LLM conversation summaries lost across many places | Dump summaries into memory, tagged and separately searchable |

---

## 6. Mental Model for Retrieval

Not a rigid implementation spec, but the system must support queries aligned with this thinking:

1. **Single project** - Retrieve memories for one specific project
2. **Cross-context** - Retrieve across multiple projects/contexts
3. **General** - Retrieve memories not tied to any project

---

## 7. Temporal Weighting (Needs Research)

Two fundamentally different scenarios:

| Scenario | Condition | What Matters |
|----------|-----------|--------------|
| **Recent cluster** | Entries within days of each other | ORDER only - what came before what |
| **Extended timespan** | Entries spanning months/years | AGE significantly - changes interpretation entirely |

**First idea (off-the-cuff, NOT best practice, needs research):** Sub-agent evaluates temporal relationships according to a rubric. Main agent provides context, sub-agent handles weighting. *Preserving this idea for potential revisit.*

**Documentation requirement:** README or first-class doc describing CURRENT approach to temporal handling. Preserve ALL history of attempts and decisions.

---

## 8. LLM Prompting Documentation System

### Immediate (Phase 1 prep):
- Documentation folder for LLM prompts in this repo
- Progressive disclosure: tool-specific prompts only when invoking tools

### Near-term:
- Apply rigorous documentation to memory-related portion of global prompts

### Future:
- Shared git submodule (does not exist yet)
- Expand to ALL global prompts
- Then expand to all projects (if pattern succeeds)

### Documentation Structure for Each Prompt:
- The prompt itself (markdown with headers/sections)
- For each section: WHY included, research basis, what we're trying to do, why we like it
- Last reviewed date
- Requires personal sign-off
- Version controlled/protected (super ultra important)

---

## 9. Future Capabilities (Preserve for Later Phases)

These are documented to preserve intent. Not in scope for Phase 1, but should inform later work.

### Source-Agnostic Ingestion
- Ingest from "pretty much everywhere" — any device, all connected coding tools
- Automated dumping scripts (e.g., Obsidian plugin) to push raw thoughts to central store
- Prevent clutter in source apps by moving data to the memory system

### Organization & Tagging
- One unified repository regardless of origin (product, project, device)
- Contextual tagging: tag items with projects/contexts after ingestion
- Priority flagging: ability to mark ideas as "Super Important" for quick retrieval

### Immutability & Frozen State
- "Decided items" pile: items that have been completely decided
- Freeze functionality: review a document and freeze it as immutable (the original requirement)
- Serves as anchor for requirements, independent of product versions
- Maps to existing `IMMUTABLEBACKUPS/` pattern but more formalized

### Versioning Workflow
- Future versions of frozen items must explain why the change was made
- All versions remain anchored to the original frozen requirements
- Prevents drift from original intent

---

## 10. Explicitly Deferred

| Item | Notes |
|------|-------|
| Hierarchical memory | Valued, no time to engineer/test now |
| Emotional memory | Valued, no time to engineer/test now |
| Shodan, MIRIX, other frameworks | Mentioned for reference |
| ScreenPipe-like tool | Separate project, mentioned for future integration |
| Pattern expansion to all projects | Far future, if pattern succeeds |

---

## 11. Phase 1 Checklist

### Phase 1 Success Criteria
Phase 1 is complete when the Graphiti MCP server runs locally, MCP tools work from Claude Code, and basic add/search/retrieve operations are verified.

### Local Setup:
- [ ] Clone graphiti repo, run `docker compose up` (FalkorDB + MCP server)
- [ ] Configure Minimax API key (from BWS) for extraction LLM
- [ ] Configure OpenRouter API key (from BWS) for embeddings
- [ ] Connect Claude Code to `http://localhost:8000/mcp/`
- [ ] Test `add_episode`, `search_nodes`, `search_facts`, `get_episodes`
- [ ] Verify entity extraction works (auto-extracts from natural language)

### Documentation:
- [x] Create initial documentation folder structure for prompts
- [ ] Document actual setup experience (update SETUP.md with findings)

### Decided (no longer open):
- [x] Memory system: Graphiti (evaluated Jan 18)
- [x] Database: FalkorDB (not PostgreSQL — graph DB needed for knowledge graph)
- [x] MCP server: Official Graphiti server (not custom code)
- [x] Entity model: Entity-centric (not project-centric)

---

## 12. Open Questions

1. ~~What exactly are "basic memory capabilities" for Phase 1?~~ **Resolved:** Run Graphiti locally, verify MCP tools work.
2. ~~Schema design - Phase 1 or Phase 2?~~ **Resolved:** Graphiti handles schema (entity extraction, knowledge graph). No custom schema needed.
3. ~~Graffiti evaluation - when does this happen?~~ **Resolved:** Evaluated Jan 18, chosen. See [evaluation report](../research/2026-01-18-memory-system-evaluation.md).
4. Temporal weighting approach - needs dedicated research session *(still open)*
5. ~~Embedding provider~~ **Resolved:** Minimax 2.1 for extraction (via OpenAI-compatible API), OpenRouter for embeddings (qwen3-embedding-8b)
6. Central deployment approach for coldane-infra *(Phase 2, not blocking)*

---

*This blueprint is a living document. Update as decisions are made.*
