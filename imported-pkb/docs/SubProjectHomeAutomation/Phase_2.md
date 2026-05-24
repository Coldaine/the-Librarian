

The reason that this is phase two is that phase one needs to be stood up in a hurry and it's just going to be a basic place to save all of our thoughts into Notion MCP. Or not. I'm sorry. Into that Postgres SQL that is currently deployed on my Raspberry Pi. 


# North Star: Personal Knowledge Base

## What This Is

A personal knowledge base covering smart home automation, homelab infrastructure, and related decision-making. Small scale: hundreds of records, single user.

## The Problem We're Solving

Notion databases sprawl. Columns multiply. Filtering becomes painful. The more you add, the harder it gets to find and reason about your data.

We want clean relational design—not to replicate Notion's sprawl, but to escape it. A well-normalized schema with clear relationships is easier to query, easier to understand, and easier for an LLM to reason about.

## Why

This is the backend for a personal knowledge management system that LLMs help serve. It needs to be:
- Queryable by humans and LLMs alike
- Rich enough in context (descriptions, rationale) for an LLM to reason about
- Clean enough in structure for reliable querying

---

## How Structured Data and Narrative Work Together

**PostgreSQL holds the hard data**: inventory, facts, relationships, status. This is what gets queried.

**Obsidian (or similar) holds the narrative**: deployment plans, status reports, analysis sessions, brainstorming. These are documents that tell a story or capture reasoning.

**The narrative links to the data for context.**

Example: We do an analysis session comparing thermostats—evaluating Ecobee vs Honeywell vs Meross, weighing protocols, pricing, integration quality. That session is captured as a note. But the actual thermostat records (what we own, what's installed where, what we decided) live in PostgreSQL as hard data. The note references that data.

Another example: There's a "Deployment Plan" note that outlines what we're doing with home automation. It doesn't contain the full inventory—it links to it. There's a separate "Current Status" note that gets updated. Keeping these as separate documents (not one monolithic file) helps track progress without sprawl.

**The LLM can use both**: query the structured data for facts, read the narrative for context and rationale.

---

## Rich Context Fields

Not every table needs extensive "why" fields. But key tables—especially **Decisions** and **Ideas**—need rich rationale.

An LLM reasoning about "should we add Zigbee sensors?" needs to understand:
- What we decided before and why
- What constraints or preferences shaped that decision
- What's changed since then

This means:
- `rationale` fields should be written in natural language, not terse notes
- They should capture the reasoning, not just the conclusion
- They're for LLM consumption as much as human consumption

---

## Core Architecture

**PostgreSQL is the source of truth.**

Design a clean relational schema. Don't optimize for any downstream platform.

**Notion and Obsidian are optional interfaces.**

They may be used for data entry or viewing. Translation layers (built later) will handle platform-specific idioms. Those translation layers can be LLM-assisted—we're in 2026, and smart tooling can solve format conversion problems.

**Sync model**: Eventually consistent. No real-time requirements. Conflict resolution can be simple for now.

---

## Guiding Principles

### 1. Human-Readable Keys (Preference, Not Dogma)

Primary keys should be meaningful to humans when practical.

**Prefer:**
```
room_id: "office"
room_id: "bonus_room"
```

**Avoid when possible:**
```
room_id: 1
room_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

**Rationale**: When you see a foreign key value in *any* context—a SQL query result, a JSON export, an Obsidian frontmatter field, a log message, anywhere—you should immediately know what it refers to without needing a lookup. `room_id: "office"` is self-documenting. `room_id: 7` or `room_id: "a1b2c3d4..."` requires you to go find out what that means.

**Key design is a per-table decision.** For each table, we will:

1. **Identify natural uniqueness**: What combination of columns would make a row unique? (e.g., for Cable Runs: `from_room` + `to_room` + `cable_type`?)
2. **Assess length/complexity**: Is that combination short enough to use directly as a key?
3. **Watch for collisions**: Could two things reasonably share that key? (e.g., two Cat6 runs between the same rooms)
4. **Decide**: Use the natural composite, derive a slug, or editorially assign a readable surrogate

This process happens during schema design for each table. There's no single answer.

---

### 2. Right-Sized Normalization

**Intrinsic properties live on the entity.**

In plain terms: things that are *unambiguous and tie directly to that object* belong on its table. A room's square footage is a fact about the room—it belongs in the Rooms table. A room's name, its floor, whether it has ethernet—these are intrinsic.

**Extrinsic relationships are references.**

A device's location is a relationship to a room, not a property of the device itself. The device could move. Store `room_id`, not duplicated room data.

**Don't over-normalize.**

Small, static value sets (3-5 items like floors or priorities) probably don't need their own table. A text field or enum is fine.

**Do normalize when:**
- The entity is referenced by multiple other tables
- The entity has intrinsic properties worth tracking
- The list of values is dynamic or might grow

---

### 3. Personal Scale, Not Enterprise

This is NOT:
- Multi-user
- High-volume
- Mission-critical
- Audit-required

Therefore, skip:
- UUIDs everywhere
- `created_at` / `updated_at` / `created_by` on every table
- Trigger-based history tracking
- Materialized views
- Over-constrained CHECK constraints

Include only what serves the actual use case.

---

### 4. Platform Concerns Are Downstream

**Do not prematurely optimize for Notion or Obsidian.**

The schema should be clean relational design. How that maps to:
- Notion relations and selects
- Obsidian frontmatter and wikilinks
- Datacore queries
- Bases views

...is a translation layer problem, not a schema design problem.

**Translation layers can be smart.** We're in 2026. LLM-assisted tooling can:
- Convert `room_id: "office"` to `location: "[[Rooms/Office]]"` for Obsidian
- Generate display names, enrich references, handle format quirks
- Parse structured data into platform-native representations
- Handle edge cases that would have required brittle custom code

This is a solved problem. Don't contort the schema to fit platform idioms.

---

## What's In Scope

- Smart home devices (locks, sensors, thermostats, cameras, switches)
- Network infrastructure (routers, switches, APs, NAS, cabling)
- Physical spaces (rooms, floors)
- Decisions log (choices made with rationale)
- Ideas/backlog (future possibilities)

## What's Out of Scope (for now)

- Threadripper workstation build (separate project, may reference)
- General notes/PKM (this is specifically the smart home/homelab domain)

---

## Open Questions

1. **Key design**: For each table, what columns define uniqueness? Is that short enough to use directly, or do we need a surrogate?
2. **Lookup table threshold**: When does a value set deserve its own table vs. just being a constrained field?
3. **Translation layer architecture**: To be designed later. LLM-assisted is assumed.

---

## Next Steps

1. ✅ Establish vision and principles (this document)
2. ⬜ Design the core schema (tables, columns, keys, relationships)
3. ⬜ Enumerate actual data (rooms, existing devices, network gear)
4. ⬜ Implement in PostgreSQL
5. ⬜ Build translation layers (Notion, Obsidian) — future work
6. ⬜ Seed with real data

---

## TEMPORARY: Domain Principles (Smart Home / Homelab)

> **Note**: This section is an example of domain-level overview knowledge. It will be moved to its own location once this north star document moves into a proper repository. This demonstrates the kind of contextual knowledge the system should store.

### Requirements (Non-Negotiable)

- Home Assistant is the control plane
- Voice/LLM is primary interface, dashboards secondary
- Locks must have fingerprint + keypad + physical key backup

### Protocol Preferences

- Matter/Thread is preferred for new purchases
- Worth up to **~25% cost premium** for Matter/Thread over alternatives
- Minimize cloud dependencies where practical
- Avoid vendor hub sprawl

### Flexibility Notes

- Cloud dependency is acceptable where it doesn't impede goals
- WiFi is acceptable for powered interior devices
- Zigbee is acceptable for bulk sensor deployments where cost savings exceed 25%
- These preferences inform decisions but shouldn't block practical progress

### Decision Framework

When evaluating a device or approach:
1. Does it meet non-negotiable requirements?
2. Does it align with protocol preferences?
3. If not, is there a compelling reason (cost, availability, unique capability)?
4. Log the decision with rationale