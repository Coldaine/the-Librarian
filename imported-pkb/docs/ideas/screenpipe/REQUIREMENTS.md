# Screenpipe Recall Pipeline: Core Requirements

This document outlines the primary goals and vision for the Screenpipe recall system. **Above all else, these are the requirements that define what the project IS.**

## 1. The Vision: Total Digital Recall
> "Capture everything across all machines, summarize intelligently at multiple levels, make it searchable and usable as context for LLMs."

*   **Catch-all Storage**: Needs to be a universal repository for all digital activity.
*   **Multi-Machine Aggregation**: Data flows from multiple deployments (laptop, desktop, work PC) to a central aggregation server.
*   **Agentic Recall**: The system doesn't just store data; it "thinks" and provides context to AI assistants automatically.

## 2. Interaction & UX Goals
*   **Hierarchical Summarization**: Aggregate activity into multiple levels for "drill down/up" capability (e.g., Personal Projects -> Screenpipe -> Database Layer).
*   **Visual Dashboards**: Ability to visualize parts of the day with intelligent, LLM-powered reviews.
*   **Perfect AI Context**: The primary consumer is the LLM, enabling it to understand exactly what was done recently and preserve complex domains of knowledge.

## 3. Technical & Security Mandates
*   **Pure Rust Stack**: Use Rust for the entire production pipeline to ensure performance, stability, and a single deployment artifact.
*   **FIDO2 Encryption**: All sensitive information captured (including secrets) must be encrypted using a FIDO2 hardware key.
*   **Lazy Review**: Perform OCR and LLM vision review asynchronously ("lazy") to preserve power on mobile devices.
*   **90-Day Retention**: Standard retention target, configurable over time.
*   **MIRIX Intelligence**: Integrate with the 6 specialized memory agent types (Core, Episodic, Semantic, Procedural, Resource, Knowledge Vault).

## 4. Platform Strategy
*   **Windows 11 First**: MVP development targets Windows for speed.
*   **Multi-Platform Later**: macOS and Linux (accessibility tree grabs for Wayland) planned for subsequent phases.
