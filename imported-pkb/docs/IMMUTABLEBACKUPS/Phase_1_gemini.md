# Phase 0: Knowledge Base Refinement (Gemini)
*Synthesized from Phase 1 Raw Notes - January 16, 2026*

## Chunk 1: Infrastructure & Initial Phases

### Verbatim Source
> Phase one, this is January 16th, 2026. And phase one is going to be connecting to using my coldane_infra repo I'm connecting to and setting up my PostgreSQL server with very basic memory capabilities. This, and then phase two is going to be trying to implement some sort of database or like management of those memories.

### Refined Intent
- **Phase 1 (Infrastructure & Quick Start):** Focus on deploying a basic, "out-of-the-box" memory solution (likely an existing open-source project) that utilizes a PostgreSQL backend.
    - *Mechanism:* Use the `coldaine-infra` repository for infrastructure orchestration.
    - *Requirement:* Prioritize immediate, low-configuration deployment.
- **Phase 2 (Management Layer):** Establish a more sophisticated database or management system for those memories on top of the initial foundation.

---

## Chunk 2: Memory Organization & Retrieval Capabilities

### Verbatim Source
> I think we're just going to go ahead and try to implement Graffiti and then make sure we have the tools for, to search and create and reference memories they need to be organized by project. So it's easy to drill down and just get the memories that we need. And we probably need to go ahead and follow up and research this. We probably need a couple of little separate MCP commands.
> 
> One should be like retrieved single projects memory. And then another one should be retrieve across context. And then there should probably be like another like retrieve memory in general when you're not like specific to a product project.

### Refined Intent
- **Management Framework:** Implement **Graffiti**.
- **Indexing & Organization:** 
    - **Project:** A first-class index, specifically tying memories to GitHub code repositories.
    - **Domain:** Higher-level groupings (broader than a single project).
    - **Metadata:** Tracking origin (e.g., LLM-generated vs. User-written).
    - **Personal/Musings:** A separate category for general thoughts and personal notes.
- **Retrieval Capabilities:** The system must provide methods (likely MCP) to:
    1.  Retrieve memories for a **single project**.
    2.  Retrieve memories **across contexts**.
    3.  Retrieve **general/global** memories.
- **Next Step:** Research and define the specific implementation of these retrieval tools.

---

## Chunk 3: Unified Context & Temporal Knowledge

### Verbatim Source
> My requirements here in my use cases let me work you walk through you the key one. So number one is when I'm working on a so I do a lot of work in Claude code in the CLI do a lot of work in Gemini in the CLI but I think it's and I think it's all specified somewhere but basically I need to work across Claude code in all my tooling. So it'll be some sort of MCP server that connects to, you know, hopefully PostgreSQL or with and graph of graffiti, I think the thing that we're grabbing from graffiti is the temporal knowledge like that's the key missing piece is that the knowledge temporally is important.

### Refined Intent
- **Primary Requirement (Unified Tooling):** The system must bridge the context gap across **all** tooling (e.g., Claude Code CLI, Gemini CLI, etc.), ensuring a shared memory state regardless of the specific interface.
- **Infrastructure Bridge:** Use an MCP server as the primary interface connecting these tools to the PostgreSQL/Graffiti backend.
- **The "Key Missing Piece":** The vital feature being extracted from the Graffiti framework is **temporal knowledge**—understanding the timing and sequence of information is critical.

---

## Chunk 4: Memory Hierarchy & Scope Constraints

### Verbatim Source
> We've also considered and we need to add this in the long term to do planning that we've considered other more complicated memory frameworks with emotional memory, you know, various types of memory moving them up and down the hierarchy. I'm a big fan of that plan. In fact, I think hierarchical hierarchical memory is important and useful. I just don't have time to engineer and try and test all these solutions. Here's just a list of some partial ones at Shodan, Mierix, et cetera.

### Refined Intent
- **Hierarchical & Emotional Memory (Philosophy):** Strong alignment with the concept of hierarchical memory models (where memories move up/down layers) and emotional memory attributes. References partial solutions like **Shodan** and **MIRIX**.
- **Scope Decision (Constraint):** While conceptually sound, these complex features are explicitly **deferred** to the long-term roadmap.
- **Reasoning:** To avoid engineering overhead and testing complexity ("time to engineer"), the immediate focus remains on the simpler, practical implementation outlined in Phase 1 & 2.

---