# Core Principles

*Extracted from [BLUEPRINT.md](../planning/BLUEPRINT.md) - Section 1*
*Updated January 2026 to reflect entity-centric pivot (see [JOURNAL.md](../implementation/JOURNAL.md))*

---

## Overview

These foundational principles apply to the entire Personal Knowledge Base system. All design decisions, implementations, and tooling must align with these principles.

---

## Principles

### LLM-Controlled

Access to the knowledge base is almost always through LLMs, not manual browsing or editing. Manual access is reserved only for:
- Debugging issues
- Building automation
- Emergency recovery

This means the system must be designed with LLM interaction as the primary interface, not as an afterthought.

### Temporal Primacy

**When** information was stored or learned is critical context. The system must support two distinct temporal modes:

| Mode | Condition | What Matters |
|------|-----------|--------------|
| **Recent cluster** | Entries within days of each other | Order only - what came before what |
| **Extended timespan** | Entries spanning months/years | Age significantly - changes interpretation entirely |

Temporal context fundamentally changes how information should be interpreted and weighted.

### Entity-Centric

Knowledge is organized around entities (projects, people, ideas, topics) and their relationships. Projects are a first-class entity type with dedicated workflows, but **not all memories require a project.** This enables:
- Per-project session continuity (via `group_id` scoping)
- Focused context retrieval within or across entities
- Cross-referencing between projects, people, ideas, and topics
- General-purpose notes that don't need project association

### Cross-Tool

The system must work seamlessly across all LLM tooling:
- Claude Code
- Gemini CLI
- Any other tools via MCP server

This is achieved through an MCP server backed by a Graphiti temporal knowledge graph (FalkorDB), ensuring consistent access regardless of which tool is being used.

---

*These principles were established during Phase 0 planning and refined during the January 2026 architectural pivot.*
