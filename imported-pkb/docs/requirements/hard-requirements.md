# Hard Requirements

*Extracted from [BLUEPRINT.md](../planning/BLUEPRINT.md) - Section 4*
*Updated January 2026 to reflect entity-centric pivot (see [JOURNAL.md](../implementation/JOURNAL.md))*

---

## Overview

These are non-negotiable requirements for the Personal Knowledge Base system. They represent the minimum viable functionality that must be achieved for the system to be considered successful.

---

## Requirements

### 1. Session Continuity

**Enable "What did we do last session?" queries for projects and other contexts.**

This is a first-class requirement. Users must be able to:
- Pick up where they left off on any project
- Understand the context of previous work
- Quickly get back into flow after time away from a project

This directly addresses Problem #2 from the use cases: "Trouble putting down projects - unsure what was done last."

### 2. Entity Relationships

**Memories connect to entities (projects, people, ideas, topics) and can be cross-referenced.**

Projects are a first-class entity type with dedicated workflows, but not the only organizing principle. The system must support:
- Project-scoped memories (via `group_id`)
- General memories not tied to any project
- Cross-referencing between different entity types
- Scalable organization as the knowledge base grows

### 3. Cross-Tool Access

**MCP server backed by Graphiti (FalkorDB), works across all LLM tooling.**

The system must be accessible from:
- Claude Code
- Gemini CLI
- Any future LLM tooling

A single source of truth accessed through a standardized protocol (MCP) ensures consistency and prevents fragmentation of knowledge across different tools.

### 4. Accessible Everywhere

**Quick notes and memories must be reachable from any context, with or without project association.**

This means:
- No friction to store new information
- No friction to retrieve stored information
- Works regardless of current project or environment

If the system isn't easily accessible, it won't be used, and unused systems provide no value.

---

## Success Criteria

A requirement is met when:
1. The functionality exists
2. It works reliably
3. It aligns with the core principles

---

*These requirements drive the implementation roadmap.*
