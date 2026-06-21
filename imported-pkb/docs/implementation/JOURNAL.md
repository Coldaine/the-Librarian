# Memory System Implementation - Journal

*Decision log and progress notes for the PKB memory system*

**Branch:** `feature/graphiti-memory-system`

---

## 2026-01-20: Architectural Pivot - Use Official Graphiti MCP Server

### What Happened

Realized we over-engineered. Built custom domain entities, services, and MCP tools that wrap Graphiti, but:

1. **Never actually ran Graphiti** - code was written based on assumptions
2. **MCP tools were stubs** - returned hardcoded fake data
3. **Misunderstood requirements** - enforced `project_id` as REQUIRED when it should be optional
4. **Graphiti already has an MCP server** - we didn't need to build one

### The Misunderstanding

**What we thought:** "All memories MUST be organized by project" (project-centric)

**What was actually meant:** Entity-centric model where:
- Projects are ONE type of entity (first-class workflow)
- Personal notes, ideas, people, topics are also entities
- Cross-referencing between entities is key
- Not everything needs a project

### Decision

**Scrap custom code. Use official Graphiti MCP server.**

The official server provides:
- `add_episode` - store memories (auto-extracts entities)
- `search_nodes` - find entity summaries
- `search_facts` - find relationships
- `get_episodes` - session continuity via recent episodes
- `group_id` - optional scoping (use for projects when needed)
- Built-in entity types: Preference, Requirement, Procedure, Location, Event, Organization, Document, Topic, Object
- FalkorDB support (default)
- Anthropic LLM support

### What We're Keeping

- `docs/planning/BLUEPRINT.md` - requirements (updated to clarify entity-centric)
- `docs/implementation/GAPS.md` - gap tracking
- `docs/research/2026-01-18-memory-system-evaluation.md` - evaluation report

### What We're Removing

- `src/pkb/` - all custom domain code
- `tests/` - tests for code we're removing

### Next Steps

1. Run official Graphiti MCP server with Docker
2. Configure Anthropic for LLM/embeddings
3. Test from Claude Code
4. Document setup

---

## 2026-01-18: Initial Implementation Attempt

### What We Did

- Created `feature/graphiti-memory-system` branch
- Set up uv project with pyproject.toml
- Built domain layer: Memory, Project, Session entities
- Built value objects: ProjectId, TemporalSpan, MemoryQuery
- Built services: MemoryService, TemporalWeightingService
- Built GraphitiAdapter (never tested against real DB)
- Built MCP server with FastMCP (stub implementations)
- 81 unit tests passing

### What Went Wrong

- Enforced `project_id` as required (wrong)
- Never ran against real Graphiti/FalkorDB
- MCP tools returned hardcoded stubs
- Built abstractions without understanding Graphiti's actual model
- Didn't check if Graphiti already had an MCP server (it does)

### Lesson Learned

**Understand the tool before building on top of it.** Clone repo, read docs, run examples FIRST.

---

## 2026-01-18: Memory System Evaluation

### Decision

Chose **Graphiti** over alternatives (Mem0, LLM Memory MCP, etc.)

### Reasoning

- Best-in-class temporal awareness (bi-temporal knowledge graph)
- 94.8% accuracy on memory retrieval benchmarks
- Hybrid search: semantic + BM25 + graph traversal
- FalkorDB support (500x faster than Neo4j)
- Active development (21k+ GitHub stars)

See [evaluation report](../research/2026-01-18-memory-system-evaluation.md) for full analysis.

---

*This journal documents what we did, what we learned, and why we made decisions.*
