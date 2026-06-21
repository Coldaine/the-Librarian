---
title: Logging
created: 2026-01-28
last_updated: 2026-01-28
---

# Logging

## Philosophy

### Structured Logging

Prefer structured logs (JSON) over plain text for machine parseability.

### Log Levels

- **ERROR**: Something failed that shouldn't have
- **WARN**: Something unexpected but recoverable
- **INFO**: Normal operations worth noting
- **DEBUG**: Detailed diagnostic information

### What to Log

- MCP tool invocations and results
- Entity extraction outcomes
- Search queries and result counts
- Errors and their context

### What Not to Log

- Sensitive content (API keys, personal data in full)
- High-frequency operations at INFO level

## Implementation Status

No custom code currently exists. Using official Graphiti MCP server.

Graphiti server logging is configured via environment variables. See [SETUP.md](../implementation/SETUP.md).
