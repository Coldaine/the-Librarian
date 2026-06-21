# Foundational "Immutable" Architectural Principles

**Generated**: 2026-01-28
**Purpose**: Catalog the core, foundational architectural principles that guide the entire Recall Pipeline project

---

## What You Were Looking For

You documented your vision for this system with **foundational principles** - the "above all else, these are the requirements" that define what the project IS and guide all technical decisions. I found these across multiple branches, particularly:

- **`docs-hybrid-architecture`** branch
- **`hybrid-architecture-candle-inference`** branches

---

## 1. Core Purpose (The "Why")

**Location**: `docs/architecture/unified-vision.md`, `docs/architecture/overview.md`

### The Mission Statement

> **Total digital recall + perfect AI context.** Capture everything across all machines, summarize intelligently at multiple levels, make it searchable and usable as context for LLMs.

### Operating Model (Non-Negotiable)

> **Single-user, multi-deployment.** One person, multiple machines (laptop, desktop, work PC). Data flows from deployments to a central server. **No multi-user tenancy.**

---

## 2. Foundational Architectural Decisions (ADRs)

**Location**: `docs/DECISIONS.md` on `docs-hybrid-architecture` branch

### 9 Architecture Decision Records

These are your "immutable agreements" - formal decisions that guide everything:

#### **ADR-003: PostgreSQL Over Lightweight Embedded Database** ✓ ACTIVE
- **Above all else**: No SQLite. Postgres only.
- **Reason**: SQLite died from write contention. Never again.
- **Non-negotiable**: Single source of truth in PostgreSQL

#### **ADR-009: Pure Rust End-to-End Stack** ✓ ACTIVE (Supersedes ADR-002)
- **Above all else**: Rust for everything production. Python is reference only.
- **Reason**: No IPC overhead, single toolchain, one deployment artifact
- **Non-negotiable**: No Python in production runtime

#### **ADR-005: MIRIX Multi-Agent System as Intelligence Layer** ✓ ACTIVE
- **Above all else**: 6 specialized memory agent types
- **Types**: Core, Episodic, Semantic, Procedural, Resource, Knowledge Vault
- **Non-negotiable**: Memory categorization, not just storage

#### **ADR-006: Windows 11 First, Multi-Platform Later** ✓ ACTIVE
- **Above all else**: Ship MVP fast on one platform
- **Later**: macOS/Linux when needed

---

## 3. Anti-Patterns to NEVER Use

**Location**: `docs/HYBRID_ARCHITECTURE.md` on `docs-hybrid-architecture` branch

### The "Never Do This" List

These are your **immutable constraints** - things you decided NEVER to do:

❌ **Python in the hot path** - Would slow down capture
❌ **Rust for LLM orchestration** - Immature ecosystem, hard to iterate *(Note: Superseded by ADR-009)*
❌ **Tight IPC coupling** - Complex, brittle, debugging nightmare
❌ **Subprocess calls** - Error-prone, hard to manage
❌ **Shared memory** - Race conditions, complexity
❌ **Multi-user tenancy** - Single-user only, forever
❌ **Real-time processing on capture device** - Lazy processing only
❌ **SQLite or local-first architecture** - Postgres server-first

---

## 4. Performance Requirements (Immutable Targets)

**Location**: `docs/HYBRID_ARCHITECTURE.md`

### Hot Path Performance Targets

These are your **non-negotiable performance requirements**:

- **Frame ingestion**: <50ms
- **Deduplication (phash)**: <10ms
- **OCR**: <300ms/frame
- **No blocking operations** in main capture loop

### Data Volume Expectations

- 12-18 hours capture/day
- ~2-5 GB/day raw
- Terabytes available — not a constraint

---

## 5. Key Concepts (The "How It Works")

**Location**: `docs/architecture/overview.md`, `docs/architecture/unified-vision.md`

### Immutable Conceptual Model

| Concept | Immutable Definition |
|---------|---------------------|
| **`deployment_id`** | Which machine captured this (laptop, desktop, etc.) - MUST be on every table |
| **Lazy review** | OCR/LLM processing is async, batched, configurable - NEVER real-time on capture |
| **Hierarchical summaries** | Drill down: Day → Project → Activity → Frame - MUST support all levels |
| **Secret vault** | Detected secrets redacted from search, stored encrypted (FIDO2) - MUST protect |
| **Memory agents** | MIRIX system for automatic LLM context - 6 types, categorized storage |

---

## 6. Non-Goals (What This System Is NOT)

**Location**: `docs/architecture/overview.md`

### The "We Will Never Do This" List

- Multi-user tenancy
- Real-time processing on capture device
- SQLite or local-first architecture
- Audio capture (for now)
- Mobile capture

---

## 7. Hierarchical Summarization (Core UX)

**Location**: `docs/architecture/overview.md`

### The Immutable User Experience

> The core user experience: drill down from high-level to raw captures.

```
"What did I do Thursday?"
  └── Day Summary
        └── Project Summaries ("recall-pipeline", "client-work")
              └── Activity Summaries ("working on database layer")
                    └── Frame Clusters (10-minute windows)
                          └── Individual Frames (raw screenshots)
```

**Requirements**:
- Start at ANY level and drill down
- Ask "what was I working on?" and get progressively more detail
- Search across ANY level (day, project, activity, or full-text frame content)

---

## 8. Data Flow Architecture (The "North Star")

**Location**: `docs/architecture/overview.md`

### Immutable Data Flow Pattern

```
DEPLOYMENTS (your machines)              SERVER (your capable remote)
┌────────────────────────┐              ┌─────────────────────────────┐
│ Laptop / Desktop       │              │                             │
│                        │              │  Postgres + pgvector        │
│  Rust Capture          │    HTTP      │    - frames                 │
│  (screenshots, phash)  │ ──────────▶  │    - activities             │
│                        │    POST      │    - projects               │
│  No local database     │              │    - day_summaries          │
│  Just buffer + retry   │              │    - secrets                │
│                        │              │                             │
└────────────────────────┘              │  Python Workers (lazy)      │
                                        │    - OCR                    │
                                        │    - Vision summarization   │
                                        │    - Embeddings             │
                                        │                             │
                                        │  Memory Agents (Phase 4)    │
                                        │    - MIRIX system           │
                                        └─────────────────────────────┘
```

**Key Decision**: Server-First, Postgres Only

> **Why not SQLite/local-first?** Screenpipe's SQLite backend died from write contention after minutes of capture. Multiple concurrent writes locked the database and it never recovered.

> **Solution:** Push frames directly to Postgres on a capable server. No local database complexity. If network blips, buffer in memory and retry.

---

## 9. Storage Model (Immutable Schema Principles)

**Location**: `docs/domains/storage.md`, `docs/plans/schema-unification-plan.md`

### The Five Schema Commandments

1. **`deployment_id` on everything** - Identifies which machine captured the data
2. **No `user_id` or `organization_id`** - Single-user system, no multi-tenancy
3. **Hierarchical summaries** - frames → activities → projects → day_summaries
4. **Secret vault with FIDO2** - Hardware key required to decrypt sensitive data
5. **Status codes** - 0=pending, 1=done, 2=error, 3=skipped

### Status Codes (Immutable Convention)

| Code | Meaning |
|------|---------|
| 0 | Pending |
| 1 | Done |
| 2 | Error |
| 3 | Skipped |

---

## 10. The "Hybrid Model Server" Vision (Historical)

**Location**: `docs/architecture/unified-vision.md` on `hybrid-architecture-candle-inference` branches

**Note**: This describes the hybrid Rust+Python architecture. Per ADR-009, this is now **superseded** by pure Rust, but the principles remain valuable.

### Division of Responsibilities (Historical)

**Rust (The "Muscle")**:
- Capture, Dedup, Storage (Postgres), and Inference
- Local LLMs (Phi-3, Llama-3-Quantized) on the metal (CUDA/Metal)
- Exposes OpenAI-compatible API (`POST /v1/chat/completions`)
- High-throughput embedding generation

**Python (The "Brain")** - *Now deprecated per ADR-009*:
- Orchestration, Logic, Memory, High-Level Reasoning
- Consumes inference API from Rust
- Manages Memory Agents (MIRIX)
- Recursive summarization hierarchies

**Why this won** (Historical rationale):
- **Speed**: Inference in Rust (fastest possible)
- **Ease**: Logic in Python (easiest possible)
- **Privacy**: Everything local
- **Stability**: Rust binary is stable appliance; Python scripts change daily

**Why it was superseded**:
- IPC complexity and latency
- Two-stack maintenance burden
- Deployment complexity

---

## 11. Benefits of Architecture (Why These Principles)

**Location**: `docs/HYBRID_ARCHITECTURE.md`

### ✅ Performance
- Rust hot path never waits for anything
- Capture runs at full speed regardless of processing
- No IPC overhead (after ADR-009)

### ✅ Reliability
- Components can crash without affecting capture
- Independent restart and scaling
- Failure isolation

### ✅ Flexibility
- Iterate quickly on high-level logic
- Add new LLM providers easily
- Can disable processing entirely if needed

### ✅ Simplicity
- No complex IPC (per ADR-009)
- PostgreSQL provides natural boundary
- Each system does what it's good at

### ✅ Scalability
- Capture scales with CPU cores
- Processing scales horizontally
- Database is the only shared resource

---

## 12. Implementation Philosophy

**Location**: ADR-008 in `docs/DECISIONS.md`

### Gradual Extraction Over Big-Bang Rewrite

**Order of extraction**:
1. PostgreSQL schemas and migrations (foundation)
2. Core Memory Agent (simplest agent)
3. Rust capture engine (performance critical)
4. Remaining 5 agents (one by one)
5. Integration layer (ties it together)
6. Cleanup and optimization

**Rationale**:
- Safety > speed for architectural refactor
- Can deliver value incrementally
- Reduces risk of wasted effort

---

## Summary: The "Above All Else" Requirements

### 1. **Single-User, Multi-Deployment**
   - No multi-tenancy, ever
   - `deployment_id` on every table

### 2. **PostgreSQL Only**
   - No SQLite in production
   - Server-first architecture

### 3. **Pure Rust Stack** (ADR-009)
   - No Python in production runtime
   - Single toolchain, single binary

### 4. **Lazy Processing**
   - Never block capture for OCR/LLM
   - Async, batched, configurable

### 5. **Hierarchical Summaries**
   - Day → Project → Activity → Frame
   - Drill down from any level

### 6. **Performance Targets**
   - Frame ingestion <50ms
   - Deduplication <10ms
   - No blocking in capture loop

### 7. **6 Memory Types** (MIRIX)
   - Episodic, Semantic, Procedural, Resource, Knowledge Vault, Core
   - Categorized memory, not just storage

### 8. **Anti-Patterns Never Allowed**
   - No Python in hot path
   - No tight IPC coupling
   - No subprocess calls
   - No SQLite
   - No real-time processing on device

---

## Where to Find These Documents

### Primary Sources (Branches to Preserve)

1. **`docs-hybrid-architecture`** branch:
   - `docs/DECISIONS.md` - 9 ADRs (foundational decisions)
   - `docs/HYBRID_ARCHITECTURE.md` - Complete architecture spec with anti-patterns

2. **`hybrid-architecture-candle-inference-v2`** branch:
   - `docs/architecture/unified-vision.md` - Core purpose and vision
   - `docs/architecture/overview.md` - Operating model and key concepts
   - `docs/domains/storage.md` - Storage principles and schema commandments
   - `docs/plans/schema-unification-plan.md` - Migration details and decisions

3. **Current `main`/`claude/find-architectural-docs-JaSNO`** branch:
   - Has some of these, but missing the comprehensive DECISIONS.md and HYBRID_ARCHITECTURE.md

---

## Recommended Action

These documents contain your **foundational vision** for the project. I recommend:

1. **Preserve `docs/DECISIONS.md`** from `docs-hybrid-architecture` branch
   - This contains the 9 ADRs that are your "immutable" architectural agreements

2. **Preserve the "Anti-Patterns" section** from `HYBRID_ARCHITECTURE.md`
   - This is your "never do this" list

3. **Preserve the "Non-Goals" section** from `overview.md`
   - Defines what the system will NEVER be

4. **Create a new `docs/PRINCIPLES.md`** that consolidates:
   - Core purpose and mission
   - Operating model (single-user, multi-deployment)
   - The 8 anti-patterns
   - The 5 non-goals
   - Performance targets
   - The 5 schema commandments

This would give you a single, canonical "Above All Else" document that guides all development decisions.

Would you like me to create this consolidated `PRINCIPLES.md` document by extracting the key foundational principles from all the branches I found?

