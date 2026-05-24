# PersonalKnowledgeBase - LLM Instructions

## Documentation

**Start here:** [docs/INDEX.md](docs/INDEX.md)

At the start of a session, read the documentation relevant to your task:
- Planning/requirements: `docs/planning/BLUEPRINT.md`, `docs/requirements/`
- Implementation: `docs/implementation/SETUP.md`, `docs/implementation/GAPS.md`
- Development guidance: `docs/dev/TESTING.md`, `docs/dev/LOGGING.md`

## Key Guidelines

### Testing
- **Avoid mocks.** Prefer fakes or real integrations. See [docs/dev/TESTING.md](docs/dev/TESTING.md).

### Protected Files
- **Do NOT modify files in `docs/IMMUTABLEBACKUPS/`** — these are enshrined historical records.
- Only reference them when tracing original intent or resolving ambiguity.

### Documentation
- All docs require front matter (title, created, last_updated). See [docs/DOCUMENTATION_STANDARDS.md](docs/DOCUMENTATION_STANDARDS.md).

## Current Phase

| Phase | Status |
|-------|--------|
| Phase 0 (Planning) | COMPLETE |
| Phase 1 (Run Graphiti locally, verify MCP tools) | NEXT |

See [docs/ROADMAP.md](docs/ROADMAP.md) for full roadmap.

## Related Repositories

- **coldane-infra**: Infrastructure, deployment, secrets
