# Constraints, Anti-Patterns, and Lessons Learned

This document catalogs the technical decisions regarding what to **avoid**, based on historical failures and architectural constraints identified during the Screenpipe discovery process.

## 1. The "Never Again" List (Technical Failures)
*   **No SQLite/Local-First**: The original screenpipe SQLite backend died from write contention. **PostgreSQL server-first is the only path forward.**
*   **No Python in Hot Path**: Python is for reference or "cold path" intelligence only. It must never handle the high-speed capture loop.
*   **No Multi-User Tenancy**: The system is strictly single-user, multi-deployment.

## 2. Structural Anti-Patterns
*   **Tight IPC Coupling**: Avoid complex, brittle IPC; use the database (Postgres) as the shared state layer.
*   **Subprocess Calls**: Avoid these for core operations due to management and error-handling complexity.
*   **Shared Memory**: Avoid due to race conditions and implementation complexity.

## 3. Operational Constraints
*   **No Real-time Processing on Capture Device**: Prioritize stable capture. OCR and LLM analysis should not block the main loop or drain battery in real-time.
*   **Incremental Migration**: Avoid "big-bang" rewrites; cherry-pick and move code from reference to production gradually.
