# Implementation Gaps

*Outstanding work and decisions for the PKB memory system*

**Status**: OPEN - Post-pivot review
**Last Updated**: January 20, 2026

---

## Summary

After architectural pivot to use the **official Graphiti MCP server**, most previous gaps are resolved. Remaining work is configuration and deployment.

| Gap | Severity | Status | Notes |
|-----|----------|--------|-------|
| [GAP-1: Local Testing](#gap-1-local-testing-not-done) | HIGH | Open | Need to actually run and test |
| [GAP-2: Anthropic Configuration](#gap-2-anthropic-configuration) | MEDIUM | Open | Configure instead of OpenAI |
| [GAP-3: Central Deployment](#gap-3-central-deployment) | HIGH | Open | Deploy to coldane-infra |

---

## Resolved Gaps (from pivot)

| Former Gap | Resolution |
|------------|------------|
| MCP tools not integrated | Using official Graphiti MCP server (already integrated) |
| PostgreSQL not used | Accepted: FalkorDB is appropriate for knowledge graph |
| OpenAI dependency | Configurable: Graphiti supports Anthropic |
| Custom code complexity | Removed: No custom code needed |
| Entity model mismatch | Resolved: Graphiti is entity-centric (what we need) |

---

## GAP-1: Local Testing Not Done

### Current State

- Official Graphiti MCP server exists
- We have setup instructions in [SETUP.md](./SETUP.md)
- **Not yet run locally**

### What's Needed

1. Run `docker compose up` in graphiti/mcp_server
2. Configure Anthropic API key
3. Connect Claude Code to `http://localhost:8000/mcp/`
4. Test the MCP tools work as expected
5. Verify entity extraction and search

### Tasks

- [ ] Clone graphiti repo (done: C:\Development\graphiti)
- [ ] Create .env with ANTHROPIC_API_KEY
- [ ] Run docker compose
- [ ] Test from Claude Code
- [ ] Document any issues

---

## GAP-2: Anthropic Configuration

### Current State

Graphiti defaults to OpenAI. We want Anthropic.

### What's Needed

Edit `config.yaml`:
```yaml
llm:
  provider: "anthropic"
  model: "claude-sonnet-4-20250514"
```

### Tasks

- [ ] Verify Anthropic provider works with Graphiti
- [ ] Test entity extraction quality with Claude
- [ ] Document any differences from OpenAI

---

## GAP-3: Central Deployment

### Requirement

From BLUEPRINT.md: "Accessible everywhere - no friction"

### Current State

- Local Docker setup ready
- Not deployed to coldane-infra

### What's Needed

1. Deploy FalkorDB to coldane-infra
2. Deploy Graphiti MCP server
3. Configure networking/secrets
4. Update MCP client configs to point to central URL

### Tasks

- [ ] Define coldane-infra deployment approach
- [ ] Create Kubernetes/Docker manifests
- [ ] Configure secrets management
- [ ] Test remote MCP connectivity

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-20 | Use official Graphiti MCP server | We don't need custom code; Graphiti provides everything |
| 2026-01-20 | Entity-centric model | Projects are entities, not mandatory containers |
| 2026-01-20 | Remove custom src/pkb code | Over-engineered; never tested against real Graphiti |
| 2026-01-18 | Choose Graphiti over alternatives | Best temporal awareness, active development |
| 2026-01-18 | Choose FalkorDB over Neo4j | 500x faster p99, lightweight |

---

## References

- [SETUP.md](./SETUP.md) - Setup instructions
- [JOURNAL.md](./JOURNAL.md) - Decision journal
- [TODO.md](./TODO.md) - Task tracking
- [BLUEPRINT.md](../planning/BLUEPRINT.md) - Requirements

---

*This document tracks remaining gaps after the Jan 20 architectural pivot.*
