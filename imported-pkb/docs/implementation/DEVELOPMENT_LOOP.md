# Development Loop

*How we iterate toward requirements alignment*

---

## TDD Cycle (Per Feature)

```
┌─────────────────────────────────────────────────────────────┐
│  1. READ REQUIREMENT                                        │
│     └── Check docs/requirements/*.md                        │
│     └── Identify acceptance criteria                        │
│                                                             │
│  2. WRITE FAILING TEST                                      │
│     └── Test encodes the requirement                        │
│     └── Use real objects, not mocks                         │
│     └── Integration tests preferred over unit tests         │
│                                                             │
│  3. IMPLEMENT MINIMUM CODE                                  │
│     └── Make test pass                                      │
│     └── No over-engineering                                 │
│                                                             │
│  4. REFACTOR                                                │
│     └── Clean up while tests stay green                     │
│     └── Extract value objects, protocols as needed          │
│                                                             │
│  5. VERIFY                                                  │
│     └── Check against GAPS.md for known issues              │
│     └── Document any deviations                             │
│                                                             │
│  6. COMMIT                                                  │
│     └── Atomic commits per feature                          │
│     └── Reference requirement in commit message             │
└─────────────────────────────────────────────────────────────┘
```

---

## Requirements Alignment Loop (Periodic)

```
┌─────────────────────────────────────────────────────────────┐
│  1. REVIEW REQUIREMENTS                                     │
│     └── Check hard-requirements.md against current state    │
│                                                             │
│  2. IDENTIFY GAPS                                           │
│     └── Which hard requirements are not met?                │
│     └── Update GAPS.md                                      │
│                                                             │
│  3. PRIORITIZE                                              │
│     └── Hard requirements > Core principles > Use cases     │
│     └── Gaps that block requirements first                  │
│                                                             │
│  4. PLAN NEXT ITERATION                                     │
│     └── Pick 1-3 gaps to close                              │
│     └── Write tests first                                   │
│                                                             │
│  5. EXECUTE TDD CYCLE                                       │
│     └── Per feature above                                   │
│                                                             │
│  6. MEASURE                                                 │
│     └── Run all tests                                       │
│     └── Update GAPS.md                                      │
│     └── Compare to baseline                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Testing Philosophy

### Hierarchy (Most → Least Preferred)

1. **Integration tests** - Real databases via testcontainers
2. **Contract tests** - MCP protocol compliance
3. **Property-based tests** - Hypothesis for edge cases
4. **Unit tests with fakes** - In-memory implementations
5. **Unit tests with mocks** - AVOID unless absolutely necessary

### Why No Mocks?

Mocks test implementation, not behavior. They verify that code CALLS a dependency, not that the behavior is correct. Prefer fakes or real integrations.

---

## Documentation Structure

```
docs/
├── requirements/           # WHAT we need (from planning)
│   ├── hard-requirements.md
│   ├── core-principles.md
│   ├── use-cases.md
│   └── deferred.md
│
├── planning/               # WHY we're building this
│   └── BLUEPRINT.md
│
├── research/               # WHAT options exist
│   └── 2026-01-18-memory-system-evaluation.md
│
├── implementation/         # HOW we're building it
│   ├── SETUP.md            # Graphiti MCP server setup
│   ├── GAPS.md             # Outstanding gaps
│   ├── TODO.md             # Task tracking
│   ├── JOURNAL.md          # Decision log
│   └── DEVELOPMENT_LOOP.md # This file
│
└── IMMUTABLEBACKUPS/       # Historical - DO NOT MODIFY
```

---

## Commit Message Format

```
feat: <short description>

Implements requirement: <requirement name from hard-requirements.md>

- <what was done>
- <what was done>
```

---

*This document defines HOW we work, not WHAT we build.*
