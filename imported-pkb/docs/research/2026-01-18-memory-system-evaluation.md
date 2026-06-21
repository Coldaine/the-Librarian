# Memory System Evaluation Report

*Date: January 18, 2026*
*Status: Research Complete*

---

## Objective

Evaluate pre-built memory systems that could meet the PersonalKnowledgeBase requirements with minimal customization, focusing on systems that can be centrally deployed and accessed via MCP.

---

## Requirements Summary

| Requirement | Priority | Description |
|-------------|----------|-------------|
| **LLM-Controlled** | Hard | Access through LLMs, not manual browsing/editing |
| **Temporal Primacy** | Hard | When information was stored is critical context |
| **Project-Organized** | Hard | Memories MUST be organized by project |
| **Cross-Tool via MCP** | Hard | Must work across Claude Code, Gemini CLI, and all tooling |
| **Session Continuity** | Hard | Enable "What did we do last session?" queries per project |
| **Central Deployment** | Hard | Accessible from any context/machine |
| **PostgreSQL Compatible** | Soft | Preference for PostgreSQL backend |

---

## Systems Evaluated

### 1. LLM Memory MCP Server

**Repository:** https://lobehub.com/mcp/andreahaku-llm_memory_mcp

**Overview:** A persistent knowledge base MCP server supporting project-specific and global storage with dual-scope architecture.

| Requirement | Status | Notes |
|-------------|--------|-------|
| LLM-Controlled | Yes | MCP native |
| Temporal Primacy | No | No explicit temporal weighting |
| Project-Organized | Yes | Dual scope: global + project-specific |
| Cross-Tool MCP | Yes | Claude Code, Cursor, Codex CLI compatible |
| Session Continuity | Partial | Searchable by project, not session-aware |
| Central Deployment | No | Local storage only (JSON files) |
| PostgreSQL | No | Local file-based |

**Verdict:** Best out-of-box project organization, but local-only and lacks temporal awareness.

---

### 2. Zep / Graphiti

**Website:** https://www.getzep.com/
**Repository:** https://github.com/getzep/graphiti
**Research Paper:** arXiv:2501.13956

**Overview:** Temporal knowledge graph architecture for agent memory. Graphiti is the open-source engine; Zep is the commercial platform built on it.

| Requirement | Status | Notes |
|-------------|--------|-------|
| LLM-Controlled | Yes | API and MCP access |
| Temporal Primacy | Yes | Bi-temporal KG (best in class) |
| Project-Organized | No | Entity/user-centric design |
| Cross-Tool MCP | Yes | Graphiti MCP server (20k+ GitHub stars) |
| Session Continuity | Yes | Episodic memory explicitly supported |
| Central Deployment | Partial | SaaS "not ready"; self-host requires Neo4j |
| PostgreSQL | Partial | Neo4j primary, PostgreSQL for metadata |

**Key Strengths:**
- Superior temporal handling with bi-temporal data model
- Real-time incremental updates without batch recomputation
- Hybrid retrieval: semantic embeddings + BM25 + graph traversal
- 94.8% accuracy on Deep Memory Retrieval benchmark (vs 93.4% MemGPT)
- 90% latency reduction vs baseline implementations

**Verdict:** Strongest temporal handling. Would need to model "projects" as first-class graph entities.

---

### 3. Mem0

**Website:** https://mem0.ai/
**Repository:** https://github.com/mem0ai/mem0
**Research Paper:** arXiv:2504.19413

**Overview:** Production-ready memory layer for AI agents with hybrid datastore architecture (vector + key-value + graph).

| Requirement | Status | Notes |
|-------------|--------|-------|
| LLM-Controlled | Yes | API and MCP access |
| Temporal Primacy | Partial | Timestamps exist, not bi-temporal |
| Project-Organized | No | User/personalization-centric |
| Cross-Tool MCP | Yes | mem0 MCP server available |
| Session Continuity | Partial | Remembers across sessions, not session-structured |
| Central Deployment | Yes | Cloud SaaS or self-host |
| PostgreSQL | Yes | pgvector supported |

**Key Strengths:**
- Most production-ready (Fortune 500 adoption, AWS SDK integration)
- 26% accuracy boost in benchmarks
- 91% lower p95 latency
- 90% token savings
- $24M Series A funding (Oct 2025)
- 41k GitHub stars, 14M downloads

**Verdict:** Easiest deployment path. User-centric design doesn't match project-centric requirements.

---

### 4. MCP Memory Service

**Repository:** https://github.com/doobidoo/mcp-memory-service

**Overview:** Automatic context memory that captures project context, architecture decisions, and code patterns.

| Requirement | Status | Notes |
|-------------|--------|-------|
| LLM-Controlled | Yes | MCP native |
| Temporal Primacy | No | No explicit temporal handling |
| Project-Organized | Yes | Project context aware |
| Cross-Tool MCP | Yes | 13+ AI tools supported |
| Session Continuity | Yes | "Never re-explain your project" |
| Central Deployment | No | Local only |
| PostgreSQL | No | Local storage |

**Verdict:** Good session continuity UX, but local-only deployment.

---

### 5. Basic Memory

**Repository:** https://github.com/basicmachines-co/basic-memory

**Overview:** Markdown-based knowledge persistence through MCP.

| Requirement | Status | Notes |
|-------------|--------|-------|
| LLM-Controlled | Yes | MCP native |
| Temporal Primacy | No | Manual organization |
| Project-Organized | Partial | File-based organization |
| Cross-Tool MCP | Yes | MCP compatible |
| Session Continuity | No | Not structured for this |
| Central Deployment | No | Local markdown files |
| PostgreSQL | No | File-based |

**Verdict:** Too simple for requirements.

---

### 6. Anthropic Knowledge Graph Memory (Official)

**Repository:** https://github.com/modelcontextprotocol/servers

**Overview:** Reference MCP server implementing knowledge graph memory.

| Requirement | Status | Notes |
|-------------|--------|-------|
| LLM-Controlled | Yes | MCP native |
| Temporal Primacy | No | Basic implementation |
| Project-Organized | No | General-purpose |
| Cross-Tool MCP | Yes | Reference implementation |
| Session Continuity | No | Not structured for this |
| Central Deployment | No | Local |
| PostgreSQL | No | In-memory/file |

**Verdict:** Reference implementation, not production-ready for these requirements.

---

## Comparative Summary

| System | Project Org | Temporal | Central Deploy | MCP | Production Ready |
|--------|-------------|----------|----------------|-----|------------------|
| LLM Memory MCP | **Yes** | No | No | Yes | Moderate |
| Zep/Graphiti | No | **Yes** | Partial | Yes | Moderate |
| Mem0 | No | Partial | **Yes** | Yes | **Yes** |
| MCP Memory Service | Yes | No | No | Yes | Moderate |
| Basic Memory | Partial | No | No | Yes | Low |
| Anthropic KG | No | No | No | Yes | Reference only |

---

## Gap Analysis

**No pre-built system fully satisfies all requirements.** The fundamental tension:

- Systems optimized for **temporal awareness** (Zep/Graphiti) are entity-centric, not project-centric
- Systems with **project organization** (LLM Memory MCP) lack central deployment and temporal handling
- Systems with **central deployment** (Mem0) are user-centric, not project-centric

---

## Recommendations

### Option A: Adapt Graphiti (Recommended)

**Approach:**
1. Fork the Graphiti MCP server
2. Model "projects" as first-class entity nodes in the temporal knowledge graph
3. Deploy centrally with Neo4j (graph) + PostgreSQL (metadata)
4. Add project-scoping to all queries

**Pros:**
- Best-in-class temporal awareness (your hard requirement)
- Active development (20k+ stars)
- Research-backed architecture

**Cons:**
- Requires customization work
- Neo4j adds operational complexity

**Estimated Effort:** Medium-High

---

### Option B: Extend Mem0 with Project Metadata

**Approach:**
1. Deploy Mem0 self-hosted with pgvector/PostgreSQL
2. Add project ID as required metadata on all memories
3. Implement project-scoped query filters
4. Accept weaker temporal handling

**Pros:**
- Most production-ready baseline
- PostgreSQL native
- Easiest to deploy

**Cons:**
- Temporal handling less sophisticated than Zep
- Fighting against user-centric design

**Estimated Effort:** Medium

---

### Option C: Extend LLM Memory MCP with Central Backend

**Approach:**
1. Fork LLM Memory MCP server
2. Replace local JSON storage with PostgreSQL backend
3. Add temporal metadata and weighting logic
4. Deploy database centrally

**Pros:**
- Already has project organization model
- Cleanest alignment with requirements

**Cons:**
- Most development work required
- Building temporal logic from scratch

**Estimated Effort:** High

---

## Decision

**Pending.** This evaluation provides the foundation for an informed decision. Next steps:

1. Review this evaluation
2. Decide on acceptable trade-offs
3. Prototype the chosen approach in Phase 2

---

## References

- [Graphiti Knowledge Graph Memory - Neo4j Blog](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/)
- [Mem0 Official](https://mem0.ai/)
- [Zep Platform](https://www.getzep.com/)
- [LLM Memory MCP](https://lobehub.com/mcp/andreahaku-llm_memory_mcp)
- [MCP Memory Service](https://github.com/doobidoo/mcp-memory-service)
- [AI Memory Tools Evaluation - Cognee](https://www.cognee.ai/blog/deep-dives/ai-memory-tools-evaluation)
- [Memory Framework Comparison](https://medium.com/asymptotic-spaghetti-integration/from-beta-to-battle-tested-picking-between-letta-mem0-zep-for-ai-memory-6850ca8703d1)
- [Zep Research Paper (arXiv:2501.13956)](https://arxiv.org/abs/2501.13956)
- [Mem0 Research Paper (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413)
