---
title: Testing
created: 2026-01-28
last_updated: 2026-01-28
---

# Testing

## Philosophy

### Avoid Mocks

Mocks test implementation, not behavior. They verify that code *calls* a dependency, not that the behavior is correct.

**Prefer (in order):**
1. Integration tests with real dependencies (testcontainers)
2. Contract tests for protocol compliance
3. Fakes (in-memory implementations with real behavior)
4. Mocks (only when no alternative)

### Test Behavior, Not Implementation

Tests should verify what the system does, not how it does it. Refactoring should not break tests unless behavior changes.

### Integration Over Unit

When practical, prefer integration tests that exercise real paths through the system.

## Implementation Status

No custom code currently exists. Using official Graphiti MCP server.

Testing will focus on:
- Verifying MCP tools work as expected
- Integration tests against real FalkorDB (via Docker)
