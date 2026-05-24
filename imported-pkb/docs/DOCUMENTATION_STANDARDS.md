---
title: Documentation Standards
created: 2026-01-28
last_updated: 2026-01-28
---

# Documentation Standards

## Required Front Matter

All documentation files must include front matter with:

```yaml
---
title: [Document Title]
created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
---
```

## Required Files

| File | Location | Purpose |
|------|----------|---------|
| README.md | Root | Project overview, quick start |
| CLAUDE.md | Root | LLM instructions, documentation index |
| INDEX.md | /docs | Master documentation index |
| DOCUMENTATION_STANDARDS.md | /docs | This file |
| ROADMAP.md | /docs | Vision, phases, outcomes |
| CHANGELOG.md | /docs | Change log |
| LOGGING.md | /docs/dev | Logging philosophy and implementation |
| TESTING.md | /docs/dev | Testing philosophy and implementation |

## Protected Files

Files in `/docs/IMMUTABLEBACKUPS/` are enshrined and must not be modified.
