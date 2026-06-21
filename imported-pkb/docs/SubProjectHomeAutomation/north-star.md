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

**PostgreSQL holds hard data about things that exist**: inventory of real devices, real network gear, physical spaces, cabling. Facts. This is what gets queried.

**Obsidian holds narrative and planning**: deployment plans, status reports, analysis sessions, brainstorming, ideas, backlog. These are documents that tell a story, capture reasoning, or track future possibilities.

**The boundary is existence.** If it's a real thing you own or a real space in your house, it goes in PostgreSQL. If it's an idea, a plan, a thought, or a "someday maybe"—it lives in Obsidian as a note with tags.

**Example lifecycle**:
```
Obsidian idea note: "Backyard Cameras" (tagged: smart_home, low_priority, waiting_for_pricing)
    ↓
  [you actually buy them]
    ↓
PostgreSQL device records: real cameras with model, location, status
```

**The narrative links to the data for context.**

Example: We do an analysis session comparing thermostats—evaluating Ecobee vs Honeywell vs Meross, weighing protocols, pricing, integration quality. That session is captured as a note in Obsidian. But the actual thermostat records (what we own, what's installed where, what we decided) live in PostgreSQL as hard data. The note references that data.

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

## What's In Scope (PostgreSQL)

Hard data about things that exist:
- Smart home devices (locks, sensors, thermostats, cameras, switches)
- Network infrastructure (routers, switches, APs, NAS, cabling)
- Physical spaces (rooms)
- Decisions log (choices made with rationale)
- Meta: table of tables with domain classification

## What Lives in Obsidian (Not PostgreSQL)

Narrative and planning:
- Ideas / backlog / "someday maybe"
- Deployment plans
- Status reports
- Analysis sessions and brainstorming
- Any document that tells a story or captures reasoning

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

---

## Example Workflow: Ideas → Classification → Action

This illustrates the intended end-state for how ideas and notes flow through the system. The exact UI and mechanisms are future work—this is the vision.

**1. Capture (unstructured)**

An idea gets captured somehow—voice note, quick text, forwarded link, whatever. It ends up in Obsidian as a note. Maybe I forget to tag it properly. It's just a standalone thought sitting there.

```
# Backyard cameras

Should probably get some cameras for the backyard. Night vision. 
Maybe two to cover the whole area. Wait for good pricing.
```

**2. LLM-assisted review (periodic)**

Eventually, something surfaces this note for review. An LLM process (we don't know exactly how yet—scheduled job, manual trigger, inbox review, whatever) looks at recently added or unclassified notes and proposes:

> "Here's a note snippet you entered on January 15th. It looks like a standalone thought related to the **Smart Home** domain, specifically **cameras/security**. It seems like a future/backlog item, not something immediate.
>
> I propose:
> - Tags: `smart_home`, `cameras`, `backlog`
> - Priority: `low` (you mentioned waiting for pricing)
> - Waiting for: `pricing`
>
> Does this look right?"

**3. User confirms or adjusts**

I say "yeah, that's right" or "actually make it medium priority." The note gets properly tagged and classified.

**4. Lifecycle continues**

The idea lives in Obsidian as a tagged note. When I eventually buy the cameras, a device record gets created in PostgreSQL. The idea note might get archived or linked to the new records.

---

**Key points:**
- The capture step should be frictionless—don't force tagging at entry time
- LLM does the heavy lifting of classification and surfacing
- Human confirms/adjusts rather than doing the work from scratch
- We don't know the exact interface yet—that's translation layer / tooling work

---

## To-Do List

### Schema & Data

- [ ] **Enumerate all rooms** — Complete list with floor, zone, sq footage, ethernet/coax
  - Pseudo-rooms: `pending` (uninstalled), `exterior` (outdoor devices, outside of entry doors)
  - Floor 1: master_bedroom, master_closet_patrick, master_closet_sarah, master_bathroom, downstairs_hall, entryway, entryway_bathroom, living_room, kitchen, dining_room, butlers_pantry, office, office_bathroom
  - Garage: garage
  - Floor 2: guest_room (Blue Room), guest_bathroom, pink_room (Sarah's Office), pink_bathroom, upstairs_hall (Upstairs Entryway), entryway_attic, white_room, white_bathroom, white_closet, white_closet_attic
  - Validate with 2D floor plan scan

- [ ] **Enumerate all doors** — Use floor plan to extract all entrances/exits
  - Entry doors (front, back, garage exterior, etc.)
  - Interior doors between rooms
  - Closet doors (especially those that might get sensors)
  - Note which will have smart hardware
  - *Candidate for LLM-assisted extraction from floor plan image*

- [ ] **Write real PostgreSQL DDL** — Convert pseudo-SQL to actual DDL with proper types, constraints, indexes

- [ ] **Seed rooms data** — Populate rooms table with real data
  - Use floor plan for square footage
  - Mark ethernet/coax based on cabling knowledge

- [ ] **Seed doors data** — Populate doors table
  - Mark door types
  - Link rooms appropriately

- [ ] **Seed devices data** — Current inventory of smart home devices

- [ ] **Seed network_devices data** — Current inventory of network equipment

- [ ] **Seed cable_runs data** — Document existing cabling

- [ ] **Seed decisions data** — Capture decisions already made (Matter strategy, etc.)

### Future Work (Not Blocking)

- [ ] **Home Assistant entity mapping** — Convention or column for correlating devices to HA entity IDs
- [ ] **Translation layers** — Sync to Obsidian, LLM query interfaces
- [ ] **Obsidian idea workflow** — The LLM-assisted classification/review system

---

## Open Questions (Deferred Until Implementation)

These are design questions we explicitly chose not to resolve now. We'll cross these bridges when we encounter them in practice:

- **Multiple identical devices naming** — Convention for 5 window sensors in one room. Positional? Indexed? By what they monitor? Decide when we actually deploy bulk sensors.

- **Cable runs key convention** — Verbose derived (`utility_to_office_cat6_1`) vs short editorial (`office_eth_1`). Will become clear when we map actual network topology.

- **Network topology / VLANs** — Whole separate session. Will inform cable_runs and network_devices structure.

---

## Deployment & Infrastructure

All infrastructure questions—where PostgreSQL runs, secrets management, backup strategy, what runs where—are answered by the **coldane-info repo**. That repo is the source of truth for deployment configuration. This schema document doesn't need to duplicate that.

---

## Philosophy: What This Schema Is (and Isn't)

**This is a reference index**, not a live state system.

The LLM will live next to Home Assistant and can query live data directly—device status, firmware versions, last seen timestamps, configuration state. We don't need to duplicate anything that can be fetched live.

This schema captures:
- **What exists** — Inventory of devices, rooms, doors, cabling
- **Where things are** — Physical topology
- **Why decisions were made** — Rationale for future reference
- **Relationships** — What connects to what

This schema does NOT need to capture:
- Live device state (HA knows this)
- Configuration details (HA knows this)
- Warranty/service tracking (out of scope)
- Detailed cost analysis (separate concern)
- Anything the LLM can investigate live and report back

If we encounter a gap where we need information we don't have, we can spin up an agent to investigate and augment the schema then. No need to over-engineer upfront.
