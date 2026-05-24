# Memory System Implementation - TODO

*Project-specific task tracking for the PKB memory system*

**Branch:** `feature/graphiti-memory-system`
**Last Updated:** January 20, 2026

---

## Current Focus

Use the official Graphiti MCP server instead of custom code.

---

## Active Tasks

- [ ] Run official Graphiti MCP server locally with FalkorDB
- [ ] Configure for Anthropic embeddings
- [ ] Test MCP tools from Claude Code
- [ ] Document setup instructions

---

## Completed

- [x] Evaluate memory systems (chose Graphiti) - Jan 18
- [x] Understand entity-centric model (not project-centric) - Jan 20
- [x] Update BLUEPRINT.md to clarify entity-centric approach - Jan 20
- [x] Prune unnecessary custom code - Jan 20
- [x] Document architectural pivot in JOURNAL.md - Jan 20

---

## Blocked / Waiting

- [ ] Deploy to coldane-infra (waiting: local testing first)

---

## Backlog

- [ ] Define custom entity types if needed beyond Graphiti defaults
- [ ] Session continuity workflow (use `get_episodes` with group_id)
- [ ] Cross-referencing workflow documentation

---

## Out of Scope (Deferred)

- Hierarchical memory
- Emotional memory
- ScreenPipe integration

---

*See [JOURNAL.md](./JOURNAL.md) for decision log and progress notes.*
