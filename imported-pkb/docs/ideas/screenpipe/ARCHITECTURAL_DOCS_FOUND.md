# Architectural Documentation Discovery Report

**Generated**: 2026-01-26
**Task**: Search all branches for architectural documents to preserve

## Executive Summary

I've searched through 20+ branches in your repository and found extensive architectural documentation that should be preserved. The most valuable documents are located in the **hybrid-architecture** branches, particularly:
- `hybrid-architecture-candle-inference`
- `hybrid-architecture-candle-inference-v2`
- `docs-hybrid-architecture`

These branches contain comprehensive specifications about interface agreements, error handling patterns, and architectural decisions.

---

## Critical Documents Found

### 1. Interface/IPC Specifications ("Innuptial Error Agreements")

**Location**: `docs/architecture/ffi-bridge.md`
**Branches**: `hybrid-architecture-candle-inference`, `hybrid-architecture-candle-inference-v2`

This document defines:
- **FFI/IPC Interface Specifications** between Rust and Python
- **Error Handling Agreements** with standard error codes
- **Data Serialization Protocols** (Bincode, Protobuf, JSON)
- **IPC Mechanisms** (PostgreSQL LISTEN/NOTIFY, Unix sockets, gRPC)

**Key Error Codes Defined**:
```
- RATE_LIMIT_EXCEEDED
- AUTHENTICATION_FAILED
- MALFORMED_DATA
- NETWORK_ERROR
- RESOURCE_EXHAUSTED
```

**Status**: Reference specification for future FFI/IPC patterns

---

### 2. Architecture Decision Records (ADRs)

**Location**: `docs/DECISIONS.md`
**Branch**: `docs-hybrid-architecture`

Contains 9 formal ADRs documenting:
- **ADR-001**: Monorepo architecture with reference folders
- **ADR-002**: Rust for capture, Python for intelligence (SUPERSEDED)
- **ADR-003**: PostgreSQL over lightweight embedded database
- **ADR-004**: Branch protection for historical archive
- **ADR-005**: MIRIX multi-agent system as intelligence layer
- **ADR-006**: Windows 11 first, multi-platform later
- **ADR-007**: Temporary reference folders (not submodules)
- **ADR-008**: Gradual extraction over big-bang rewrite
- **ADR-009**: Pure Rust end-to-end stack (SUPERSEDES ADR-002)

**Critical**: Documents the evolution from hybrid Rust+Python to pure Rust architecture

---

### 3. Error Handling Patterns

**Location**: `docs/rust/error-handling-patterns.md`
**Branch**: `docs-hybrid-architecture`

Rust-specific error handling conventions:
- Context chaining with `anyhow::Context`
- Custom error types with `thiserror`
- Error conversion at API boundaries
- Logging best practices with `tracing`
- Testing error conditions

---

### 4. Hybrid Architecture Specification

**Location**: `docs/HYBRID_ARCHITECTURE.md`
**Branch**: `docs-hybrid-architecture`

Comprehensive 330-line document describing:
- **Hot Path (Rust)**: Performance-critical capture and storage
- **Cold Path (Python)**: LLM-powered intelligence and analysis
- **Database Schema**: Shared state layer (PostgreSQL)
- **Communication Patterns**: How Rust and Python interact via Postgres
- **Deployment Options**: Single machine, separate services, cloud split
- **Performance Targets**: Frame ingestion <50ms, deduplication <10ms

**Status**: Superseded by ADR-009 (pure Rust), but valuable reference

---

### 5. Unified Vision Document

**Location**: `docs/architecture/unified-vision.md`
**Branches**: `hybrid-architecture-candle-inference`, `hybrid-architecture-candle-inference-v2`

Describes the "Hybrid Model Server" architecture:
- Rust handles capture, dedup, storage, and **local LLM inference**
- Python handles orchestration, memory, and high-level reasoning
- Rust exposes OpenAI-compatible API (`/v1/chat/completions`)
- Python consumes this API for summarization and memory agents

**Key Concepts**:
- `deployment_id` - Which machine captured data
- Lazy review - Async OCR/LLM processing
- Hierarchical summaries - Day → Project → Task → Frame
- Secret vault with FIDO2 encryption

---

### 6. Schema Unification Plan

**Location**: `docs/plans/schema-unification-plan.md`
**Branches**: `hybrid-architecture-candle-inference`, `hybrid-architecture-candle-inference-v2`

Comprehensive 475-line plan documenting:
- **Track A**: Rust schema normalization (`device_name` → `deployment_id`)
- **Track B**: Python schema simplification (multi-tenant → single-user)
- **Track C**: Hierarchy tables (activities, projects, day_summaries)
- **Track D**: Secrets infrastructure
- **Track E**: CI pipeline implementation

**Migration Safety**:
- Pre-migration requirements
- Rollback procedures
- Known limitations

---

### 7. Implementation Roadmap

**Location**: `docs/plans/implementation-roadmap.md`
**Branches**: `hybrid-architecture-candle-inference`, `hybrid-architecture-candle-inference-v2`

5-phase implementation plan:
- **Phase 1**: Raw capture → Postgres (Current priority)
- **Phase 2**: Local inference infrastructure with Candle (Completed)
- **Phase 3**: Lazy OCR + vision workers (Next up)
- **Phase 4**: Hierarchical summaries
- **Phase 5**: Memory agents + secrets (Deprioritized)

---

### 8. Master Documentation Playbook

**Location**: `docs/MasterDocumentationPlaybook.md`
**Branches**: `docs-frontmatter-compliance`, `docs-playbook-compliance`, multiple others

Organization-wide documentation standards:
- Canonical docs structure (`/docs` layout)
- Required metadata headers (YAML frontmatter)
- Placement and naming rules
- Lifecycle and retention policies
- CI enforcement rules
- Domain short codes and naming conventions

**Version**: 1.0.1
**Status**: Draft

---

### 9. Consolidation History

**Location**: `docs/plans/consolidation-2025-11.md`
**Branches**: `hybrid-architecture-candle-inference`, `hybrid-architecture-candle-inference-v2`

Historical record of November 2025 cleanup:
- What got removed (legacy Python capture, Tauri app, pipes)
- What got renamed (`screenpipe/` → `capture/`)
- Context for the refactor

---

### 10. Code Inventory

**Location**: `docs/architecture/code-inventory.md`
**Branches**: `hybrid-architecture-candle-inference`, `hybrid-architecture-candle-inference-v2`

Audit of existing code and its status (not fully read, but exists)

---

### 11. Screenpipe Crate Audit

**Location**: `docs/architecture/screenpipe-crate-audit.md`
**Branches**: `hybrid-architecture-candle-inference`, `hybrid-architecture-candle-inference-v2`

Full audit of all 10 screenpipe crates with decisions (referenced in worklog)

---

## Branch Recommendations

### Branches with Most Complete Documentation

1. **`hybrid-architecture-candle-inference-v2`** - Most recent, includes all key docs
2. **`hybrid-architecture-candle-inference`** - Similar to v2, slightly older
3. **`docs-hybrid-architecture`** - Contains comprehensive HYBRID_ARCHITECTURE.md and DECISIONS.md
4. **`docs-frontmatter-compliance`** - Master Documentation Playbook
5. **`claude/consolidate-project-01VK7y9qPdzzieM8riE1QpKu`** - Consolidated state

### Recommended Preservation Strategy

1. **Create a `docs/archive/historical-architecture/` directory**
2. **Copy these documents from the hybrid-architecture branches**:
   - `ffi-bridge.md` - Interface/IPC specifications
   - `DECISIONS.md` - All 9 ADRs
   - `HYBRID_ARCHITECTURE.md` - Hybrid Rust+Python architecture
   - `unified-vision.md` - Hybrid model server vision
   - `schema-unification-plan.md` - Complete migration plan
   - `implementation-roadmap.md` - 5-phase roadmap
   - `consolidation-2025-11.md` - Consolidation history
   - `rust/error-handling-patterns.md` - Error handling conventions

3. **Add a README in the archive explaining**:
   - These documents represent architectural explorations
   - Some decisions were superseded (ADR-002 → ADR-009)
   - They provide valuable context for understanding the project evolution
   - Current architecture is in `docs/architecture/overview.md`

---

## Search Results by Branch

### `docs-hybrid-architecture`
- ✅ **DECISIONS.md** (9 ADRs)
- ✅ **HYBRID_ARCHITECTURE.md** (330 lines)
- ✅ **rust/error-handling-patterns.md**
- ARCHITECTURE.md
- IMPLEMENTATION_PLAN.md
- DEVELOPMENT.md
- DEPLOYMENT.md
- OPERATIONS.md
- HYBRID_WORKFLOW.md

### `hybrid-architecture-candle-inference` & `-v2`
- ✅ **ffi-bridge.md** (IPC/Error specifications)
- ✅ **unified-vision.md** (Hybrid model server)
- ✅ **schema-unification-plan.md** (475 lines)
- ✅ **implementation-roadmap.md**
- ✅ **consolidation-2025-11.md**
- code-inventory.md
- screenpipe-crate-audit.md
- multi-agent-review.md

### `docs-frontmatter-compliance` & `docs-playbook-compliance`
- ✅ **MasterDocumentationPlaybook.md** (344 lines)
- standards.md
- Domain-specific docs (capture, storage, routing, orchestration)

### `feat/hybrid-architecture-integration`
- architecture/database_schema.md
- Similar structure to main branch

### `archive-old-main`
- MIGRATE_MILVUS.md
- REPOMIX.md
- IMPLEMENTATION_PLAN.md
- (Minimal documentation)

---

## Answering Your Question: "Innuptial Error Agreements"

Based on my search, I believe you were referring to one or more of these:

1. **`ffi-bridge.md`** - "FFI/IPC Interface Specifications"
   - Defines error handling agreements between Rust and Python
   - Standard error codes and formats
   - Interface contracts for cross-language communication

2. **`error-handling-patterns.md`** - Rust error handling conventions
   - How errors should be handled in the codebase
   - Context chaining, custom error types

3. **ADRs in `DECISIONS.md`** - Architectural "agreements"
   - Formal decisions about how components interact
   - Especially ADR-002 (hybrid) and ADR-009 (pure Rust)

All three documents focus on **agreements** between different parts of the system about how to handle **errors** and **interfaces**.

---

## Next Steps

1. **Decide which documents to preserve**
   - All of them? (Recommended - they're valuable history)
   - Only the "superseded" ones? (To show evolution)
   - Create an archive with clear status labels

2. **Choose preservation location**
   - `docs/archive/historical-architecture/`
   - `docs/architecture/superseded/`
   - Separate `docs/history/` directory

3. **Add context**
   - Create an index/README explaining the documents
   - Note which decisions are still active vs superseded
   - Link to current architecture documents

4. **Commit and document**
   - Create a commit preserving these docs
   - Update worklog with preservation decision
   - Reference in main docs/README.md

Would you like me to proceed with copying these documents to an archive directory in your current branch?

