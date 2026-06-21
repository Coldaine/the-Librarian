# Use Cases (Problems to Solve)

*Extracted from [BLUEPRINT.md](../planning/BLUEPRINT.md) - Section 5*

---

## Overview

These are the concrete problems the Personal Knowledge Base system is designed to solve. Each problem has a corresponding solution approach within the memory system.

---

## Problems and Solutions

| # | Problem | Memory System Solution |
|---|---------|----------------------|
| 1 | LLMs have stale training data (~2024 cutoff), hallucinate outdated info | Store research/learnings; LLMs can query for up-to-date context |
| 2 | Trouble putting down projects - unsure what was done last | Per-project session continuity queries |
| 3 | Important info buried in verbose documentation | North Star concept - short bulleted requirements per project (in flux) |
| 4 | Quick notes get lost without central place | Notes go into memory system, searchable, temporally aware |
| 5 | Article ideas scattered and unfindable | Central findable storage for ideas |
| 6 | LLM conversation summaries lost across many places | Dump summaries into memory, tagged and separately searchable |

---

## Use Case Details

### Use Case 1: Stale LLM Knowledge

**Problem:** LLMs are trained on data with a cutoff date (approximately 2024). When asked about recent developments, APIs, or best practices, they may hallucinate outdated or incorrect information.

**Solution:** Store research findings and learnings in the knowledge base. When working on tasks, LLMs can query the knowledge base for up-to-date context before providing answers.

### Use Case 2: Project Continuity

**Problem:** After stepping away from a project for days, weeks, or months, it's difficult to remember where things left off. This creates friction when returning to work.

**Solution:** Per-project session continuity queries allow asking "What did we do last session?" and getting meaningful context to resume work efficiently.

### Use Case 3: Documentation Overload

**Problem:** Important requirements and decisions get buried in verbose documentation, making them hard to find and reference.

**Solution:** The "North Star" concept - maintain short, bulleted requirements per project. This is still in flux but aims to provide quick access to what matters most.

### Use Case 4: Lost Quick Notes

**Problem:** Quick notes, ideas, and reminders get lost because there's no central, searchable place for them.

**Solution:** All notes go into the memory system, making them searchable and temporally aware. Nothing gets lost.

### Use Case 5: Scattered Ideas

**Problem:** Article ideas, project concepts, and inspirations are scattered across different places and become unfindable.

**Solution:** Central, searchable storage for all ideas ensures nothing valuable slips through the cracks.

### Use Case 6: Lost Conversation Summaries

**Problem:** Valuable summaries from LLM conversations are scattered across many different places and difficult to retrieve.

**Solution:** Dump conversation summaries into the memory system with appropriate tags. They become separately searchable and contribute to project context.

---

*These use cases drive feature prioritization and success metrics for the system.*
