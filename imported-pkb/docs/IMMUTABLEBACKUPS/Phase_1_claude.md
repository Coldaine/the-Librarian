# Phase One - Reframed Document

*Working document created January 16th, 2026*

---

## Chunk 1: Phase Structure & Command Architecture

**VERBATIM:**
> "Phase one, this is January 16th, 2026. And phase one is going to be connecting to using my coldane_infra repo I'm connecting to and setting up my PostgreSQL server with very basic memory capabilities. This, and then phase two is going to be trying to implement some sort of database or like management of those memories. I think we're just going to go ahead and try to implement Graffiti and then make sure we have the tools for, to search and create and reference memories they need to be organized by project. So it's easy to drill down and just get the memories that we need. And we probably need to go ahead and follow up and research this. We probably need a couple of little separate MCP commands.
>
> One should be like retrieved single projects memory. And then another one should be retrieve across context. And then there should probably be like another like retrieve memory in general when you're not like specific to a product project."

**SUMMARY:**
Phase 1 is standing up PostgreSQL connection (infrastructure lives in coldane-infra). Phase 2 is implementing memory management (likely Graffiti). The three retrieval types (single project, cross-context, general) are a mental model for how memories should be queryable - not a rigid implementation spec. Hard requirement: memories must be organized by project. The finer distinctions (project vs general vs other) will be fleshed out later.

**REWORDED:**
> Phase 1 (dated January 16th, 2026): Connect to and stand up PostgreSQL server via the coldane-infra repo. This phase is limited to basic memory persistence - infrastructure only.
>
> Phase 2: Implement memory management, likely using Graffiti. This includes tooling to search, create, and reference memories.
>
> Mental model for retrieval (not a rigid spec): (1) retrieve a single project's memories, (2) retrieve across contexts/projects, (3) retrieve general memories not tied to a project. The actual implementation may differ, but the system must support queries that align with this thinking.
>
> Hard requirement: Memories must be organized by project. Further organization details (project vs general vs other) to be defined later.

---

## Chunk 2: Primary Use Case & Temporal Knowledge

**VERBATIM:**
> "My requirements here in my use cases let me work you walk through you the key one. So number one is when I'm working on a so I do a lot of work in Claude code in the CLI do a lot of work in Gemini in the CLI but I think it's and I think it's all specified somewhere but basically I need to work across Claude code in all my tooling. So it'll be some sort of MCP server that connects to, you know, hopefully PostgreSQL or with and graph of graffiti, I think the thing that we're grabbing from graffiti is the temporal knowledge like that's the key missing piece is that the knowledge temporally is important. We've also considered and we need to add this in the long term to do planning that we've considered other more complicated memory frameworks with emotional memory, you know, various types of memory moving them up and down the hierarchy. I'm a big fan of that plan. In fact, I think hierarchical hierarchical memory is important and useful. I just don't have time to engineer and try and test all these solutions. Here's just a list of some partial ones at Shodan, Mierix, et cetera."

**SUMMARY:**
Primary requirement: An MCP server connecting to PostgreSQL (with Graffiti) that works across all tooling - Claude Code, Gemini CLI, etc. The key value from Graffiti is temporal knowledge - when something was learned/stored matters. Hierarchical memory, emotional memory, and other frameworks (Shodan, MIRIX, etc.) are ideas you value but are explicitly deferring due to time constraints.

**REWORDED:**
> Key use case: Work seamlessly across Claude Code, Gemini CLI, and all tooling. This requires an MCP server connecting to PostgreSQL (with Graffiti).
>
> The critical feature from Graffiti: Temporal knowledge. When information was stored/learned is important context that most memory systems lack.
>
> Deferred (valued but not now): More sophisticated memory frameworks - hierarchical memory, emotional memory, moving knowledge up/down hierarchies. Specific tools considered: Shodan, MIRIX, and others. These are good ideas worth revisiting, but engineering and testing them is out of scope for now.

---

## Chunk 3: Long-term Vision & Core Principle

**VERBATIM:**
> "And then other things to put on long term to-do list related to this is eventually there's gonna be where I was going for fork. Not fork but at this point I wanted to remake screenpipe and basically take screenshots and or accessibility tree grabs depending you know which depends on if your windows are on Linux and then periodically index them for knowledge very similar to Microsoft recall but a personal version. And again all this tooling it's the number one priority for all this kind of stuff is large language model controlled. It's for the it large language models to both understand what it is that they did recently for me to understand what it is that they did recently to preserve that knowledge to preserve domains of knowledge that we created one time so here let me get back to some explicit examples."

**SUMMARY:**
*Aside:* ScreenPipe-like tool is a separate future project, mentioned only for potential integration. *Core principle for this personal knowledge/memory project:* LLM-controlled access - user interacts through LLMs, not manually (except debugging/automation). Two LLM use cases: direct retrieval at user's request, and contextual reference while working. Goals include (not exhaustive): both LLMs and user understand what was done recently; preserve domains of knowledge.

**REWORDED:**
> *Aside (separate project, future integration potential):* A personal ScreenPipe/Microsoft Recall equivalent - screenshots on Windows, accessibility tree grabs on Linux/Wayland, periodically indexed. Deferred; mentioned only for future integration possibility.
>
> *Core principle for this personal knowledge/memory project:* This memory system is LLM-controlled. Access is almost always through LLMs, not manual browsing/editing. Manual interaction only for debugging or automation.
>
> LLM use cases:
> 1. Direct retrieval at user's request
> 2. Contextual reference while working on projects (ensuring up-to-date context)
>
> Goals include (not exhaustive): LLMs and the user both understand what was done recently. Preserve domains of knowledge created during work.

---

## Chunk 4: Example 1 - Outdated LLM Knowledge

**VERBATIM:**
> "Some explicit examples here. Example one: I almost always have to ask agents to re-remember all the time that it's 2026 and then particularly for things like LangGraph or other dependencies where their knowledge in that like where things have changed very much in the last two years since they're cut off of their training data in 2024. Google Gemini is a big very guilty of this frequently hallucinating model versions that are ancient and declaring newer models don't exist. Claude is also guilty this as well so number that's one requirement and use case they can use this to solve"

**SUMMARY:**
Problem: LLMs have stale training data (~2024 cutoff), hallucinate outdated info about fast-moving dependencies (LangGraph, model versions, etc.). User constantly has to remind them it's 2026. Gemini and Claude both guilty. Memory system intent: User does research and updates; when LLMs learn new things, it goes into memory (project-specific or general). LLMs may be able to search research notes, etc. Exact form TBD.

**REWORDED:**
> Example 1 - Outdated LLM knowledge:
>
> Problem: LLMs have stale training data (cutoff ~2024). They hallucinate outdated information, especially for fast-moving dependencies like LangGraph or model versions. Google Gemini and Claude are both guilty of this. User constantly has to remind them it's 2026.
>
> Memory system intent: When research is done and new things are learned, it gets stored in memory (project-specific or general). LLMs may be able to search through research notes and updated information. Exact implementation form is TBD.

---

## Chunk 5: Example 2 - Session Continuity & North Star

**VERBATIM:**
> "another requirement too and speculative workflow so when I work on a project I'm having a lot of trouble putting it down because I'm not sure exactly what was the last thing I did so the initial memory part of this the large language model part of this on the per project scope at the very least you know if everything is good get if we are able to make the memory work then um You know I'll be able to say hey, what did we do last session or hey? You know what have we done recently and then it'll pull? The memory applicable to that and know in addition to that explicit very important things often get lost in the documentation what we do like I like verbose copious documentation, but the problem is It's hard to have a universally referenceable like short list that you know these are the most vital things to remember other project for For one in every single project we need to commit as soon as we finalize Basically commit what's in the North star which is you know? A number of bullets You know it could be two it could be ten but in bulleted form the absolute like requirements that are unambiguous that everything else is going to flow from this can be any and as a reminder here those are very high level like speech-to-text Local focused Windows and Linux, you know with Wayland compatible Keyboard shortcut control plus super or control win enables it Initial workflow will be it is intended to be hold control windows I speak it injects At my cursor and Then eventual future targets are Having context awareness and having large language models Intervene and edit so that would be an example You know converted to bullets Of the sort of thing that would need to be in the permanent project memory and available"

**SUMMARY:**
Problem 1 (first-class requirement): Trouble putting down a project because unsure what was done last. Memory should enable "what did we do last session?" queries per project. Problem 2: Important things get lost in verbose documentation. Proposed solution: A "North Star" - short bulleted list of absolute unambiguous requirements per project, stored in permanent project memory. (North Star concept is in flux.) The speech-to-text example is explicitly what a northstar.md might look like - an illustrative example, not a requirement for this system.

**REWORDED:**
> Example 2 - Session continuity & project requirements:
>
> Problem 1 (first-class requirement): Difficulty putting down a project because unsure what was done last. Memory system must enable per-project queries like "what did we do last session?" or "what have we done recently?"
>
> Problem 2: Important information gets lost in verbose documentation. Hard to maintain a universally referenceable short list of vital project requirements.
>
> Proposed solution (in flux): A "North Star" per project - a short bulleted list (2-10 items) of absolute, unambiguous requirements that everything else flows from. Stored in permanent project memory.
>
> Example of what a North Star might look like (from a speech-to-text project):
> - Local-focused, Windows and Linux (Wayland compatible)
> - Keyboard shortcut: Ctrl+Win to enable
> - Initial workflow: Hold Ctrl+Win, speak, text injects at cursor
> - Future targets: Context awareness, LLM intervention/editing

---

## Chunk 6: Example 3 - Quick Notes Accessible Everywhere

**VERBATIM:**
> "Use example three: sometimes I just need to get something jotted down, like a general memory or like a general note. And it needs to be accessible from everywhere because otherwise I will lose it. For example, right now, these thoughts right now are just getting dumped into this markdown document. In the future they're going to be jumped, they're going to be put somewhere in this memory so that they can be searched for. And also when we have temporal awareness. We can say okay when it was happening? What does it look like I was working on? Etc. And we can back into my workflow. I mean sometimes we can tell what I was doing based on the source of notes I was making. So that's another requirement."

**SUMMARY:**
Problem: Quick thoughts/notes need a place accessible from everywhere, or they get lost. Currently dumped into markdown documents. Future state: Notes go into memory system - searchable, with temporal awareness (when captured, what was being worked on). Advantage: Can infer workflow context from timing and author (user vs LLM) of notes/memories.

**REWORDED:**
> Example 3 - Quick notes accessible everywhere:
>
> Problem: Sometimes need to quickly jot down a general note or memory. Must be accessible from everywhere, or it gets lost. Currently these get dumped into markdown documents.
>
> Future state: Notes go into the memory system where they can be searched. Temporal awareness enables: when was it captured? What was being worked on at the time?
>
> Advantage: Can infer workflow context from the timing and author (user vs LLM) of the notes/memories themselves.

---

## Chunk 7: Requirement 4 - Repository Relationship

**VERBATIM:**
> "This is similar to requirement three or sorry requirement four. Requirement four is it needs to we're going to make this accessible multiple places. I think and we need we're going to stand some of this up I think as its own repository its own project but it's very closely tied to coldaine underscore infra repo and so we need to kind of carefully manage between the two. coldaine-infra is going to contain all the information about deploying the infrastructure where is it going to get hosted where do we store the secrets etc. coldaine info will give us some of that stays here but the reference and you know we need to remember to reach out to that repo for any of those answers involving like what where and secrets. There can be some documentation locally but the definitive is in coldaine Infra."

**SUMMARY:**
This memory system will be its own repository, closely tied to coldane-infra. Careful boundary management needed. coldane-infra is the definitive source for: deployment, hosting, where things live. This repo CAN and SHOULD have secrets embedded as needed - the anti-pattern to avoid is assuming all secrets must live only in coldane-infra.

**REWORDED:**
> Requirement 4 - Repository relationship:
>
> This memory system will be its own separate repository/project, but closely tied to coldane-infra. Careful management of the boundary between them is required.
>
> coldane-infra is the definitive source for:
> - Deployment information
> - Hosting details (where things live)
>
> This repo can have local documentation and should reference coldane-infra for infrastructure answers. Secrets CAN be embedded in this project as needed - the anti-pattern to avoid is assuming all secrets must only live in coldane-infra.

---

## Chunk 8: Example 5 - Article Ideas & Conversation Summaries

**VERBATIM:**
> "Use example/use requirement number five. I often have ideas about what would make a good article, and now unfortunately I've got dozens of these but I haven't actually written any of the articles because I can't find or figure out where I put all of those articles, or all of those ideas. Not only that, many of the conversations I have with our language models, I need to be able to summarize and just dump a summary of what was learned there so that needs to be like, I don't know, we might have to do front matter or anything but like there'll be huge dumps of summaries of when I like had a conversation with a large language model and those should be like tagged and separably searchable somehow. Like you should we should be able to explicitly look for those and I think we're doing some sort of like semantics search so those will be serviceable. Then the reason I mentioned the conversation with large language models is often, well we've done exhaustive research and we'll have some great ideas, great technologies, great things but now they're all lost and scattered across so many different places that I can't find them or make use of them."

**SUMMARY:**
Problem A: Article ideas - dozens exist but can't be found, so none get written. Need a findable place. Problem B: LLM conversation summaries - exhaustive research produces great findings but they're lost and scattered. Need to dump summaries into memory, tagged and separately searchable. Implementation (in flux): May involve front matter, tagging, semantic search - exact form TBD but must be explicitly searchable as a category.

**REWORDED:**
> Example 5 - Article ideas & conversation summaries:
>
> Problem A: Have dozens of article ideas but can't find them, so none get written. Need a findable, central place for these.
>
> Problem B: LLM conversations produce exhaustive research, great ideas, technologies, findings - but they're lost and scattered across many places. Need to dump summaries of what was learned into memory.
>
> Requirement: These summaries must be tagged and separately searchable - should be able to explicitly look for "LLM conversation summaries" as a category.
>
> Implementation (in flux): May involve front matter, tagging, semantic search. Exact form TBD.

---

## Chunk 9: Temporal Primacy & Weighting

**VERBATIM:**
> "Also we need to emphasize the primacy here of temporal tooling because I might have had a great conversation about something new in large language models but it was eight months ago and that means that it's likely outdated and we'll need to weigh that when when retrieving any information. And again so that's another part of this tooling is we need to at some point explicitly, and I'd like to explicitly make this like a markdown document, explain the part how we're handling and understanding large language model agents like how we're having them weigh the temporal part of the memory."

**SUMMARY:**
Temporal tooling has primacy - example: a great LLM conversation from 8 months ago is likely outdated, must weigh that during retrieval. Need a markdown document explaining how LLM agents weigh the temporal aspect of memories.

*[Vital tangent appended - user elaborated extensively:]*

Key insight: Two fundamentally different temporal scenarios exist:
- **Scenario A (recent cluster):** Entries within days - age doesn't matter, only ORDER matters
- **Scenario B (extended timespan):** Entries spanning months/years - AGE matters significantly, changes interpretation entirely

These are different evaluation modes, not a sliding scale.

**First idea (off-the-cuff, NOT best practice, needs research before considering implementation):** Sub-agent approach - main agent provides context, sub-agent evaluates temporal relationships according to a rubric. *Preserving this idea in case we try something else and need to revisit.*

**Research & documentation requirements:** Ongoing area of research. Must plan systematically. Preserve ALL history of attempts/decisions in detail. First-class documentation (possibly README) describing CURRENT approach.

**REWORDED:**
> Temporal Primacy & Weighting:
>
> Temporal tooling has primacy. Example: A great conversation about something new in LLMs from eight months ago is likely outdated - must weigh that when retrieving information.
>
> Documentation requirement: A markdown document explicitly explaining how LLM agents weigh the temporal aspect of memories.

---

## Chunk 10: LLM Prompting Documentation System

**VERBATIM:**
> "I think this is, and here's another stream of consciousness idea that makes your needs get recorded. Each part of the large like we need our own documentation folder here just for the prompts for the large language models for any like pieces. We need to basically have a whole bunch of markdown documents one of them's gonna say this is the sec, like this is the section that goes into every single Cloud MD like global Cloud MD and global Gemini MD and agents MD on every single computer. This is the part of it that's gonna be like yeah you know appended or you know included in there that helps it understand how and when to use the memories. And then we're gonna have a bunch of other markdown documents that say you know here are the like we're gonna obey progressive disclosure and then you know when they connect to some of these tools they won't need the other prompts or the other information on how that took like the tools work specifically or you know specific workflows until they invoke those tools so progressive disclosure etcetera etcetera. And again we need to like it's a that's a first-class vital part of this like LLM prompting is vital and I keep losing all of it we need to specifically basically have you know a flowchart saying how all that lives how they'll you know how they all you know relate to each other that is version controlled and deployed by the code coldane in for reef reef respect infrastructure but again we need not just the prompt but any prompt needs to require and I mean like a fairly detailed dive like this is why we included these sections like this is like there needs to be separate markdown file it says you know here is the tooling or like here is the markdown file that contains just the prompt here are sections of headers that you know these are the pieces of the prompt and then for each section. And we're going to write you know little sections as why did we include it and then what research to be based on what is it we're trying to do and why we like it so much and then we will have a changed like last reviewed and then will require my personal sign off for that. I will need some way to version protect each of these like this is super ultra important like. The versioning of those prompt documents and their detailed analysis we need to basically we need to convert into a process and we'll figure it all out."

**SUMMARY:**
Need a documentation folder for LLM prompts - markdown documents with sections that go into CLAUDE.md, Gemini MD, agents MD on every computer, explaining how/when to use memories. Progressive disclosure: LLMs get tool-specific prompts only when invoking those tools, not upfront. LLM prompting is vital and keeps getting lost. Need version control, a flowchart showing how prompts relate, and a formal process.

*[User elaborated extensively - scope expansion beyond this repo:]*

This chunk speaks to something BROADER than just this memory repo (PersonalKnowledgeBase). It spans into coldane-infra and represents a cross-cutting concern.

**Core mechanism (proposed):** A shared git submodule that both coldane-infra and this memory repo can consume. Does not exist yet - creating it is part of future work. Contains:
- Canonical global prompts (first-class citizens)
- Specific tooling sections like memory (also first-class citizens)
- The "pattern" for rigorous prompt organization

**Relationship between pieces:**
```
Shared Git Submodule (canonical prompts + pattern)
                │
    ┌───────────┴───────────┐
    ▼                       ▼
Memory Repo              coldane-infra
(PersonalKnowledgeBase)  (deploys/syncs to
(prototype pattern here) all machines)
```

**"Globals are first-class citizens" means:** Global/shared instruction content is the primary, canonical source - not scattered copies. Global prompts maintained in one authoritative location. Project-specific instructions reference or extend these, not duplicate them.

**MCP tool integration:** Tool descriptions and associated prompts/context must be included in this system - not just instruction files. All of it ties together.

**Phased rollout:**
1. **Now:** Apply rigorous approach to the portion of global prompts pertaining to memory management only
2. **Soon after:** Expand to cover ALL global prompts regardless of topic
3. **Future (if pattern succeeds):** Adopt for all projects

**Deployment:** Pattern gets injected into all global LLM context files, deployed and synced through coldane-infra.

**Documentation structure for each prompt:**
- The prompt itself (markdown with headers/sections)
- For each section: WHY it was included, what research it's based on, what we're trying to do, why we like it
- Last reviewed date
- Requires user's personal sign-off
- Version controlled/protected - this is super ultra important

**REWORDED:**
> LLM Prompting Documentation System:
>
> Need a documentation folder for LLM prompts - markdown documents with sections that go into CLAUDE.md, Gemini MD, agents MD on every computer. These explain how/when to use memories.
>
> Progressive disclosure: LLMs don't get all prompt info upfront - tool-specific prompts only when invoking those tools.
>
> LLM prompting is vital and keeps getting lost. Need version control, a flowchart showing how prompts relate, and a formal process. Versioning of prompt documents is super ultra important - must convert into a process.

---

