# Direct Quotes and Clear Statements from Patrick

**Generated**: 2026-01-28
**Purpose**: Catalog direct quotes and unambiguous statements about the project vision and requirements

---

## Your Own Words: The 8 Conceptual Questions

**Source**: `docs/architecture/unified-vision.md` (version 1.1.0)

### 1. What problem are you solving for yourself?

> "Both of those issues, I want to both recall, and give perfect context. **The scope of this is large.**"

### 2. What are your "deployments"?

> "Different machines, **eventually we will aggregate across all of them.**"

### 3. When you imagine using this successfully, what does that interaction look like?

> "Yes, I want to be able to **visualize in dashboards what I was doing at each part of the day**, with intelligent summarization, and having LLM review that intelligently sees what I was doing and **aggregates that into multiple levels that I can drill down into or up from** eg: working on personal projects → working on screenpipe → working on the database layer.
>
> I also want it to **capture things like secrets, and redact and store them** (securely, eventually we will get into specifics, but **I have a FIDO2 key that I want all sensitive information to be encrypted with**).
>
> Additionally, I want the **MIRIX memory component to explore and research it**, to see how useful it is in providing context to my LLMs automatically."

### 4. Where should the data live?

> "Ultimately a hierarchy: Local caching/storage gets uploaded, reviewed, etc... or stored wholesale on my remote aggregation server. **Key to this vision is the "lazy review"** where we are going to do both OCR and LLM vision review of the (de-duplicated) screen content, but **certainly not realtime** (or perhaps configurable for OCR - for example **my laptop probably can't spare the power to do that in realtime, my desktop probably can**)."

### 5. Memory types - necessary or over-engineered?

> "**This is for experimentation**, and already should exist here, **this should be mostly done**."

### 6. What's your relationship with the captured data over time?

> "For testing purposes we're just going to retain, **90 day retention is about right, but we're going to configure this over time.**"

### 7. How much should this system "think" vs just "store"?

> "**Yes, automatically.** But we need to flesh this out over time."

### 8. Is this purely for you, or do you imagine sharing context with AI assistants?

> "**Absolutely, needs to be a catch all storage.**"

---

## Core Purpose Statement

**Source**: `docs/architecture/overview.md`, `docs/architecture/unified-vision.md`

> "**Total digital recall + perfect AI context.** Capture everything across all machines, summarize intelligently at multiple levels, make it searchable and usable as context for LLMs."

---

## Operating Model (Non-Negotiable)

**Source**: `docs/architecture/overview.md`

> "**Single-user, multi-deployment.** One person, multiple machines (laptop, desktop, work PC). Data flows from deployments to a central server. **No multi-user tenancy.**"

---

## The "Never Again" Decision: PostgreSQL Only

**Source**: `docs/architecture/overview.md`, `docs/domains/storage.md`

> "**Why not SQLite/local-first?** Screenpipe's SQLite backend **died from write contention** after minutes of capture. Multiple concurrent writes locked the database and **it never recovered.**"

> "**Solution:** Push frames directly to Postgres on a capable server. **No local database complexity.** If network blips, buffer in memory and retry."

---

## Key Design Principles

**Source**: `docs/ARCHITECTURE.md` on `docs-hybrid-architecture` branch

### Design Principles List

1. **Performance First**: Rust for hot path, Python for intelligence
2. **Agentic by Default**: LLM-powered understanding, not just storage
3. **Production Grade**: PostgreSQL, proper error handling, observability
4. **Developer-Friendly**: Clear separation of concerns, good docs
5. **Incremental Migration**: Cherry-pick, don't rewrite from scratch

---

## The Vision Statement

**Source**: `docs/ARCHITECTURE.md` on `docs-hybrid-architecture` branch

> "Build a Rust-based screen capture pipeline that feeds into MIRIX's multi-agent memory system, creating an **intelligent, agentic screen activity tracking and recall system**."

---

## Performance Requirements (Clear Targets)

**Source**: `docs/HYBRID_ARCHITECTURE.md` on `docs-hybrid-architecture` branch

### Hot Path Performance Targets

- **Frame ingestion**: <50ms
- **Deduplication**: <10ms
- **OCR**: <300ms/frame
- **No blocking operations in main loop**

---

## The "Why This Wins" Statement

**Source**: `docs/architecture/unified-vision.md` (version 1.2.0, hybrid-architecture branch)

> "**Why this wins:**
> - **Speed:** Inference happens in Rust (fastest possible).
> - **Ease:** Logic happens in Python (easiest possible).
> - **Privacy:** Everything is local.
> - **Stability:** The Rust binary is a stable appliance; Python scripts can change daily without recompiling the heavy inference engine."

**Note**: This was for the hybrid architecture, which was later superseded by ADR-009 (pure Rust).

---

## Anti-Patterns You Explicitly Rejected

**Source**: `docs/HYBRID_ARCHITECTURE.md` on `docs-hybrid-architecture` branch

### The "We Avoided" List

❌ **Python in the hot path** - Would slow down capture
❌ **Rust for LLM orchestration** - Immature ecosystem, hard to iterate *(superseded by ADR-009)*
❌ **Tight IPC coupling** - Complex, brittle, debugging nightmare
❌ **Subprocess calls** - Error-prone, hard to manage
❌ **Shared memory** - Race conditions, complexity

---

## Non-Goals (What This Will Never Be)

**Source**: `docs/architecture/overview.md`

- Multi-user tenancy
- Real-time processing on capture device
- SQLite or local-first architecture
- Audio capture (for now)
- Mobile capture

---

## The Hierarchical Summarization UX

**Source**: `docs/architecture/overview.md`

> "The core user experience: **drill down from high-level to raw captures.**"

```
"What did I do Thursday?"
  └── Day Summary
        └── Project Summaries ("recall-pipeline", "client-work")
              └── Activity Summaries ("working on database layer")
                    └── Frame Clusters (10-minute windows)
                          └── Individual Frames (raw screenshots)
```

> "Users can:
> - **Start at any level and drill down**
> - Ask "what was I working on?" and get progressively more detail
> - **Search across any level** (day, project, activity, or full-text frame content)"

---

## Architecture Decision Rationales (From ADRs)

**Source**: `docs/DECISIONS.md` on `docs-hybrid-architecture` branch

### ADR-003: PostgreSQL Over Lightweight Embedded Database

**Positive Consequences:**
- Single source of truth
- ACID transactions across Rust and Python
- **Concurrent writes without locking**
- BM25 full-text search + vector similarity in one system
- Production-ready (MIRIX already uses PostgreSQL)
- Complex temporal queries supported

**Trade-offs Accepted:**
- Docker Compose makes deployment easy
- Resource usage acceptable for agentic features
- MIRIX already designed for PostgreSQL

### ADR-005: MIRIX Multi-Agent System as Intelligence Layer

**Rationale:**
> "MIRIX agents solve exactly our problem (memory consolidation). **Building custom agents would take months.** Can always refactor later if needed."

### ADR-006: Windows 11 First, Multi-Platform Later

**Decision:**
> "**Phase 1 (MVP)**: Windows 11 only"

**Positive:**
- **Faster MVP delivery**
- Can leverage Windows-specific optimizations
- Most users on Windows anyway
- screenpipe already Windows-first

### ADR-008: Gradual Extraction Over Big-Bang Rewrite

**Rationale:**
> "**Safety > speed for architectural refactor**. Can deliver value incrementally. Reduces risk of wasted effort."

**Order of extraction:**
1. PostgreSQL schemas and migrations (foundation)
2. Core Memory Agent (simplest agent)
3. Rust capture engine (performance critical)
4. Remaining 5 agents (one by one)
5. Integration layer (ties it together)
6. Cleanup and optimization

### ADR-009: Pure Rust End-to-End Stack (Supersedes ADR-002)

**Positive Consequences:**
- **Single toolchain and deployment artifact** (Cargo workspace → one binary/installer)
- **No IPC boundary**; easier to enforce workload budgets (vision cooldowns, LLM spend caps) inside one runtime
- Reuse of existing Rust crates accelerates delivery
- Aligns with the "pure Rust migration" roadmap and simplifies contributor onboarding

**Negative Consequences:**
- All MIRIX functionality must be reimplemented in Rust before we can delete the reference folder
- Rust-based LLM integrations require more boilerplate than Python SDKs
- Contributors familiar only with Python must ramp up on Rust/Tokio

---

## Implementation Philosophy

**Source**: `docs/plans/implementation-roadmap.md`

### Phase 1 Goal

> "**Goal:** Reliable capture that doesn't die"

### Phase Structure

- **Phase 1**: Raw capture → Postgres (**Current priority**)
- **Phase 2**: Local Inference Infrastructure (Rust + Candle) (**Completed**)
- **Phase 3**: Lazy OCR + vision workers (Python consumers) (Next Up)
- **Phase 4**: Hierarchical summaries (activity → project → day) (Future)
- **Phase 5**: Memory agents (MIRIX), secret encryption (**Deprioritized**)

---

## Data Volume Expectations

**Source**: `docs/domains/storage.md`

- 12-18 hours capture/day
- ~2-5 GB/day raw
- **Terabytes available — not a constraint**

---

## "Why Server-First?" Statement

**Source**: `docs/architecture/unified-vision.md` (current branch)

> "**Why server-first?** SQLite write contention killed the original screenpipe local-first approach. **Single Postgres instance is simpler and more reliable.**"

---

## Schema Commandments (The Five Rules)

**Source**: `docs/plans/schema-unification-plan.md`

1. **`deployment_id` on everything** - Identifies which machine captured the data
2. **No `user_id` or `organization_id`** - Single-user system, no multi-tenancy
3. **Hierarchical summaries** - frames → activities → projects → day_summaries
4. **Secret vault with FIDO2** - Hardware key required to decrypt sensitive data
5. **Status codes** - 0=pending, 1=done, 2=error, 3=skipped

---

## The "Lazy Review" Concept (Your Key Innovation)

**Source**: Multiple documents

### From unified-vision.md Q&A:
> "**Key to this vision is the "lazy review"** where we are going to do both OCR and LLM vision review of the (de-duplicated) screen content, but **certainly not realtime**"

### From Key Concepts:
> "**Lazy review:** OCR/LLM processing is async, batched, configurable per deployment"

### Design Decision:
- Not real-time on capture device
- Configurable per deployment
- Laptop: probably can't do real-time
- Desktop: probably can

---

## Benefits of Architecture (Why These Decisions)

**Source**: `docs/HYBRID_ARCHITECTURE.md`

### ✅ Performance
- Rust hot path never waits for Python
- Capture runs at full speed regardless of agent processing
- No tight coupling, no IPC overhead

### ✅ Reliability
- Python can crash without affecting capture
- Independent restart and scaling
- Failure isolation

### ✅ Flexibility
- Iterate on agents without touching Rust
- Add new LLM providers easily
- Prompt engineering in Python (fast iteration)
- Can disable agent processing entirely if needed

### ✅ Simplicity
- No complex IPC (no gRPC, no subprocess management)
- PostgreSQL provides natural boundary
- Each system does what it's good at

### ✅ Scalability
- Rust capture scales with CPU cores
- Python agents scale horizontally (multiple workers)
- Database is the only shared resource

---

## Deployment Vision

**Source**: `docs/HYBRID_ARCHITECTURE.md`

### Option 3: Cloud Split (Long-term Vision)
- **Rust capture**: Runs on user's machine (local)
- **PostgreSQL**: Managed database (AWS RDS, etc.)
- **Python agents**: Cloud workers (EC2, Lambda, etc.)

---

## Memory Agent Types (The Six Categories)

**Source**: Multiple documents

1. **Core Memory**: Key facts, user preferences, context
2. **Episodic Memory**: "What happened when" - temporal events
3. **Semantic Memory**: Concepts, relationships, knowledge
4. **Procedural Memory**: How-to's, workflows, processes
5. **Resource Memory**: Files, URLs, external resources
6. **Knowledge Vault**: Long-term knowledge storage

---

## Secret Handling Requirements

**Source**: `docs/architecture/unified-vision.md` Q&A

> "I also want it to **capture things like secrets, and redact and store them** (securely, eventually we will get into specifics, but **I have a FIDO2 key that I want all sensitive information to be encrypted with**)."

---

## The "Agentic Screen Capture" Vision

**Source**: `docs/ARCHITECTURE.md`

> "**Not just OCR**: Intelligent understanding of screen content"
> - Memory Consolidation: Agents process raw captures into structured memories
> - **Multi-modal**: Text, images, metadata combined
> - **Temporal Queries**: "What was I doing Tuesday afternoon?"

---

## Clear Technical Decisions

### Database Choice
> "Use **PostgreSQL 16+** as the single database for:
> - Raw screen captures
> - OCR text and metadata
> - Memory consolidations
> - Vector embeddings
> - Full-text search"

### Extensions Required
> "**Extensions Required**:
> - pgvector for embeddings
> - pg_search or ParadeDB for BM25 full-text search"

### Image Storage (Phase 1 Decision)
**Source**: `docs/domains/storage.md`

> "Options (decide based on what's easiest):
> - **Filesystem:** Save images to disk, store path in `image_ref`
> - **S3/R2:** Upload to object storage, store URL in `image_ref`
> - **Postgres BYTEA:** Store directly in DB (simpler, but larger DB)
>
> **For Phase 1, filesystem is fine. Just get it working.**"

---

## Status Code Convention (Immutable Standard)

**Source**: `docs/domains/storage.md`, `docs/plans/schema-unification-plan.md`

| Code | Meaning |
|------|---------|
| 0 | Pending |
| 1 | Done |
| 2 | Error |
| 3 | Skipped |

---

## Document Authorship Attribution

**Source**: `docs/DECISIONS.md`, `docs/ARCHITECTURE.md`

> "**Author**: Coldaine (with Claude Code)"

---

## Summary: Your Clearest Statements

1. **"The scope of this is large."** - You're not building a small tool
2. **"Certainly not realtime"** - Lazy processing is fundamental
3. **"I have a FIDO2 key that I want all sensitive information to be encrypted with"** - Security requirement
4. **"Eventually we will aggregate across all of them"** - Multi-machine vision
5. **"Needs to be a catch all storage"** - Everything gets captured
6. **"SQLite backend died from write contention"** - Never SQLite again
7. **"Safety > speed for architectural refactor"** - Methodology statement
8. **"Building custom agents would take months"** - Pragmatic reuse
9. **"Just get it working"** - Phase 1 pragmatism
10. **"This should be mostly done"** - MIRIX should already exist

---

These are your words, your vision, and your technical requirements as documented across all the branches.

