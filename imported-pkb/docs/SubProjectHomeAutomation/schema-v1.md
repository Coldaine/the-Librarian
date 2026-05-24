# Schema Design v1

This is the first pass at the PostgreSQL schema for the personal knowledge base.

Pseudo-SQL for readability. Not yet optimized or validated.

---

## Design Boundary

**PostgreSQL holds hard data about things that exist.** Real devices, real network gear, real physical spaces, real cabling, real decisions made.

**Obsidian holds narrative and planning.** Ideas, backlog, "someday maybe," deployment plans, analysis sessions. These are notes with tags, not database records.

**The boundary is existence.** When you buy something, it becomes a record. Before that, it's an Obsidian note.

---

## Tables Overview

| Table | Domain L1 | Domain L2 | Purpose | Key Strategy |
|-------|-----------|-----------|---------|--------------|
| `tables` | Meta | Core | Table of tables with domain classification | Literal table name: `rooms`, `devices` |
| `rooms` | Infrastructure | Core | Physical spaces in the house | Slugified name: `office`, `guest_room` |
| `doors` | Infrastructure | Core | Entrances/exits between spaces | Editorial: `front_door`, `office_to_hall` |
| `devices` | Infrastructure | Smart Home | Smart home devices | Editorial descriptive: `front_door_lock` |
| `network_devices` | Infrastructure | Network | Network infrastructure | Editorial descriptive: `udm_pro_max` |
| `cable_runs` | Infrastructure | Network | Physical cabling between rooms | Derived: `utility_to_office_cat6` |
| `decisions` | Meta | Planning | Log of choices with rationale | Date + topic slug: `2024_12_matter_strategy` |

---

## Value Sets (Not Tables)

These are small, static sets. Use TEXT with conventions or ENUM, not lookup tables.

```
floor:      "First Floor" | "Second Floor" | "Garage" | "Attic" | "Basement"
zone:       "Interior" | "Exterior" | "Garage Area"
protocol:   "Matter/Thread" | "WiFi" | "Zigbee" | "Z-Wave" | "HomeKit" | "Ethernet"
device_type: "Lock" | "Sensor" | "Thermostat" | "Camera" | "Switch" | "Doorbell" | "Other"
network_device_type: "Router" | "Switch" | "AP" | "NAS" | "Workstation" | "Camera" | "Other"
door_type:  "Entry" | "Interior" | "Closet" | "Garage"
cable_type: "Cat6" | "Cat6A" | "Cat5e" | "Coax" | "Fiber"
decision_category: "Protocol" | "Device" | "Architecture" | "Rejected"
decision_status: "Active" | "Superseded" | "Under Review"
domain_l1:  "Infrastructure" | "Meta"
domain_l2:  "Core" | "Smart Home" | "Network" | "Planning"
```

**Note on device lifecycle:** There is no status field. The `room_id` serves as a proxy:
- `room_id = "pending"` → Purchased, not yet installed
- `room_id = "exterior"` → Installed outside (cameras, outdoor sensors, etc.)
- `room_id = <real room>` → Installed in that room

Use `notes` for nuance (e.g., "needs configuration", "having issues").

---

## Table: `tables` (Meta)

Table of tables. Provides domain classification for organizing and querying.

**Key strategy**: Literal table name.

```sql
tables (
    table_id        TEXT PRIMARY KEY,   -- "rooms", "devices", "network_devices"
    display_name    TEXT NOT NULL,
    domain_l1       TEXT NOT NULL,      -- "Infrastructure", "Meta"
    domain_l2       TEXT NOT NULL,      -- "Core", "Smart Home", "Network", "Planning"
    description     TEXT
)
```

**Seed data**:
```
table_id        | display_name    | domain_l1      | domain_l2   | description
----------------|-----------------|----------------|-------------|---------------------------------------------
tables          | Tables          | Meta           | Core        | This table. Meta-schema.
rooms           | Rooms           | Infrastructure | Core        | Physical spaces, referenced by everything
doors           | Doors           | Infrastructure | Core        | Entrances/exits, some with smart hardware
devices         | Devices         | Infrastructure | Smart Home  | Locks, sensors, thermostats, cameras, etc.
network_devices | Network Devices | Infrastructure | Network     | Routers, switches, APs, NAS
cable_runs      | Cable Runs      | Infrastructure | Network     | Physical cabling between rooms
decisions       | Decisions       | Meta           | Planning    | Choices made with rationale
```

---

## Table: `rooms`

Physical spaces. Referenced by devices, network devices, cable runs, doors.

**Key strategy**: Room names are unique within a house. Slugify the name.

**Natural uniqueness**: `name`

```sql
rooms (
    room_id         TEXT PRIMARY KEY,   -- e.g., "office", "guest_room", "utility_closet"
    name            TEXT NOT NULL,      -- e.g., "Patrick's Office", "Guest Room"
    alternate_name  TEXT,               -- Common alternate (e.g., "Blue Room" for guest room)
    floor           TEXT,               -- "First Floor", "Second Floor", "Garage", "Attic"
    zone            TEXT,               -- "Interior", "Exterior", "Garage Area"
    square_footage  INTEGER,
    has_ethernet    BOOLEAN DEFAULT FALSE,
    has_coax        BOOLEAN DEFAULT FALSE,
    notes           TEXT
)
```

**Example rows**:
```
room_id          | name             | alternate_name   | floor        | zone         | sq_ft | ethernet | coax
-----------------|------------------|------------------|--------------|--------------|-------|----------|------
pending          | Pending          | null             | null         | null         | null  | false    | false
exterior         | Exterior         | null             | null         | Exterior     | null  | false    | false
office           | Patrick's Office | null             | First Floor  | Interior     | null  | true     | false
guest_room       | Guest Room       | Blue Room        | Second Floor | Interior     | null  | false    | false
pink_room        | Pink Room        | Sarah's Office   | Second Floor | Interior     | null  | false    | false
upstairs_hall    | Upstairs Hall    | Upstairs Entryway| Second Floor | Interior     | null  | false    | false
garage           | Garage           | null             | Garage       | Garage Area  | null  | false    | false
```

**Special pseudo-rooms**:
- `pending` — Purchased-but-not-installed devices
- `exterior` — Outdoor devices (cameras, motion sensors, etc.) and the "outside" side of entry doors

---

## Table: `devices`

Smart home devices: locks, sensors, thermostats, cameras, switches, etc.

**Key strategy**: Devices don't have natural uniqueness (could have two identical sensors). Use editorial descriptive keys that indicate what/where.

**Natural uniqueness**: None reliable. `manufacturer` + `model` + `location` could collide.

```sql
devices (
    device_id       TEXT PRIMARY KEY,   -- e.g., "front_door_lock", "garage_door_sensor"
    name            TEXT NOT NULL,      -- Human display name
    device_type     TEXT NOT NULL,      -- "Lock", "Sensor", "Thermostat", etc.
    protocol        TEXT NOT NULL,      -- "Matter/Thread", "WiFi", etc.
    manufacturer    TEXT,
    model           TEXT,
    room_id         TEXT NOT NULL REFERENCES rooms(room_id),  -- "pending" if not yet installed
    door_id         TEXT REFERENCES doors(door_id),           -- For locks/door sensors
    purchase_date   DATE,
    purchase_price  DECIMAL(10,2),
    notes           TEXT
)
```

**Example rows**:
```
device_id              | name                    | type       | protocol      | manufacturer | model              | room_id      | door_id
-----------------------|-------------------------|------------|---------------|--------------|--------------------|--------------|-----------------
front_door_lock        | Front Door Lock         | Lock       | WiFi          | Ultraloq     | Bolt               | entryway     | front_door
garage_interior_lock   | Garage Interior Lock    | Lock       | Matter/Thread | Aqara        | U300               | pending      | null
back_door_lock         | Back Door Lock          | Lock       | Matter/Thread | Ultraloq     | Bolt Fingerprint   | pending      | null
garage_door_sensor     | Garage Door Sensor      | Sensor     | Matter/Thread | Aqara        | P2                 | pending      | null
```

---

## Table: `network_devices`

Network infrastructure: routers, switches, APs, NAS, etc.

**Key strategy**: Similar to devices. Editorial descriptive keys.

**Natural uniqueness**: None reliable.

```sql
network_devices (
    network_device_id   TEXT PRIMARY KEY,   -- e.g., "udm_pro_max", "switch_pro_xg8", "ap_office"
    name                TEXT NOT NULL,
    device_type         TEXT NOT NULL,      -- "Router", "Switch", "AP", etc.
    manufacturer        TEXT,
    model               TEXT,
    room_id             TEXT NOT NULL REFERENCES rooms(room_id),  -- "pending" if not yet installed
    ip_address          TEXT,               -- Could use INET type in real PG
    vlan                TEXT,               -- Or INTEGER if you prefer VLAN IDs
    port_count          INTEGER,
    poe_budget_watts    INTEGER,
    purchase_date       DATE,
    purchase_price      DECIMAL(10,2),
    notes               TEXT
)
```

**Example rows**:
```
network_device_id | name                  | type   | manufacturer | model              | room_id
------------------|-----------------------|--------|--------------|--------------------|--------------
udm_pro_max       | Dream Machine Pro Max | Router | Ubiquiti     | UDM Pro Max        | utility_closet
switch_pro_xg8    | Switch Pro XG 8 PoE   | Switch | Ubiquiti     | USW-Pro-XG-8-PoE   | utility_closet
switch_flex_2g    | Switch Flex 2.5G PoE  | Switch | Ubiquiti     | USW-Flex-2.5G-PoE  | pending
ap_office         | Office AP             | AP     | Ubiquiti     | U7 Pro XGS         | pending
ap_bonus_room     | Bonus Room AP         | AP     | Ubiquiti     | U7 Pro XGS         | pending
```

---

## Table: `cable_runs`

Physical network cabling between locations.

**Key strategy**: Natural composite is `from_room` + `to_room` + `cable_type`, but could have multiple runs of same type between same rooms. Add index suffix if needed.

**Natural uniqueness**: `from_room` + `to_room` + `cable_type` + `run_index`

```sql
cable_runs (
    cable_run_id        TEXT PRIMARY KEY,   -- e.g., "utility_to_office_cat6_1"
    from_room_id        TEXT NOT NULL REFERENCES rooms(room_id),
    to_room_id          TEXT NOT NULL REFERENCES rooms(room_id),
    cable_type          TEXT NOT NULL,      -- "Cat6", "Cat6A", etc.
    run_index           INTEGER DEFAULT 1,  -- For multiple runs of same type
    length_ft           INTEGER,
    terminated          BOOLEAN DEFAULT FALSE,
    tested_speed_gbps   DECIMAL(4,1),
    notes               TEXT
)
```

**Example rows**:
```
cable_run_id             | from           | to         | type | idx | length | terminated | speed | notes
-------------------------|----------------|------------|------|-----|--------|------------|-------|---------------------------
utility_to_office_cat6_1 | utility_closet | office     | Cat6 | 1   | 50     | true       | 10.0  | Spec was Cat6A, got Cat6
utility_to_bonus_cat6_1  | utility_closet | bonus_room | Cat6 | 1   | 80     | true       | null  | Not yet tested
```

---

## Table: `doors`

Physical doors/entrances between spaces. Some will have smart hardware (locks, sensors).

**Key strategy**: Editorial descriptive. Entry doors get simple names, interior doors describe the connection.

**Natural uniqueness**: None reliable (could have multiple doors between same rooms).

```sql
doors (
    door_id         TEXT PRIMARY KEY,   -- e.g., "front_door", "office_to_hall", "garage_entry"
    name            TEXT NOT NULL,
    room_a_id       TEXT NOT NULL REFERENCES rooms(room_id),  -- One side
    room_b_id       TEXT NOT NULL REFERENCES rooms(room_id),  -- Other side (use "exterior" for outside)
    door_type       TEXT,               -- "Entry", "Interior", "Closet", "Garage"
    notes           TEXT
)
```

**Example rows**:
```
door_id              | name                    | room_a_id      | room_b_id       | door_type | notes
---------------------|-------------------------|----------------|-----------------|-----------|------------------
front_door           | Front Door              | entryway       | exterior        | Entry     | Main entry
garage_entry         | Garage Entry Door       | garage         | exterior        | Garage    | Side door to exterior
garage_to_house      | Garage to House         | garage         | kitchen         | Interior  | Connects garage to house
office_to_hall       | Office Door             | office         | downstairs_hall | Interior  | 
master_closet_patrick| Patrick's Closet Door   | master_bedroom | master_closet_patrick | Closet |
```

**Note**: Entry doors connect a room to `exterior`. No nulls needed—both sides always reference a room.

---

## Table: `decisions`

Log of choices made with rationale. **Rich context field**: `rationale` is for LLM consumption.

**Key strategy**: Date + topic slug. Decisions are temporal and topical.

**Natural uniqueness**: `date_made` + `title` (unlikely to make two decisions on same topic same day)

```sql
decisions (
    decision_id     TEXT PRIMARY KEY,   -- e.g., "2024_12_matter_strategy"
    title           TEXT NOT NULL,
    rationale       TEXT NOT NULL,      -- RICH: natural language, full reasoning
    category        TEXT NOT NULL,      -- "Protocol", "Device", "Architecture", "Rejected"
    date_made       DATE NOT NULL,
    status          TEXT NOT NULL,      -- "Active", "Superseded", "Under Review"
    revisitable     BOOLEAN DEFAULT TRUE,
    notes           TEXT
)
```

**Example row**:
```sql
INSERT INTO decisions VALUES (
    '2024_12_matter_strategy',
    'Matter/Thread as preferred protocol',
    'We decided to prefer Matter/Thread for new smart home purchases. Rationale:
    
    1. Local control without cloud dependency
    2. Vendor-neutral standard backed by Apple, Google, Amazon
    3. Thread mesh networking improves reliability and range
    4. Future-proofing as ecosystem matures
    
    We''re willing to pay up to ~25% cost premium for Matter/Thread over alternatives.
    
    Exceptions: WiFi acceptable for powered interior devices. Zigbee acceptable
    for bulk sensor deployments where cost savings exceed 25%.
    
    This does NOT mean we reject all non-Matter devices—just that Matter is
    the default preference when available and reasonably priced.',
    'Protocol',
    '2024-12-17',
    'Active',
    TRUE,
    NULL
);
```

---

## Relationships Diagram

```
┌─────────────────┐
│     tables      │  (Meta: domain classification for all tables)
│─────────────────│
│ table_id (PK)   │
│ domain_l1       │
│ domain_l2       │
└─────────────────┘


                    ┌─────────────────┐
                    │     rooms       │
                    │─────────────────│
                    │ room_id (PK)    │
                    │ name            │
                    │ alternate_name  │
                    │ floor           │
                    │ zone            │
                    │ square_footage  │
                    │ has_ethernet    │
                    │ has_coax        │
                    └────────┬────────┘
                             │
       ┌─────────────────────┼─────────────────────┬──────────────────┐
       │                     │                     │                  │
       ▼                     ▼                     ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│     doors       │ │    devices      │ │ network_devices │ │   cable_runs    │
│─────────────────│ │─────────────────│ │─────────────────│ │─────────────────│
│ door_id (PK)    │ │ device_id (PK)  │ │ net_dev_id (PK) │ │ cable_run_id(PK)│
│ room_a_id (FK)  │ │ room_id (FK)    │ │ room_id (FK)    │ │ from_room_id(FK)│
│ room_b_id (FK)  │ │ door_id (FK) ───┼─│ ...             │ │ to_room_id (FK) │
│ door_type       │ │ ...             │ │                 │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
     (Core)            (Smart Home)         (Network)            (Network)
        ▲                   │
        └───────────────────┘
        devices.door_id → doors


┌─────────────────┐
│   decisions     │  (Meta: choices with rationale)
│─────────────────│
│ decision_id(PK) │
│ title           │
│ rationale       │  ← Rich context for LLM consumption
│ category        │
│ date_made       │
│ status          │
└─────────────────┘
```

**Domain organization via `tables` meta-table:**
- LLM can query "what tables are in the Smart Home domain?" → `devices`
- LLM can query "what tables are in the Network domain?" → `network_devices`, `cable_runs`
- LLM can query "what tables are in Core?" → `rooms`, `doors`
- Decisions relate to domains implicitly via their category and content

---

## Open Questions

See **north-star.md** for deferred design questions. Key ones:
- Multiple identical devices naming convention
- Cable runs key convention  
- Network topology / VLANs

---

## Next Steps

1. Review this schema against actual inventory
2. Enumerate real rooms
3. Decide on open questions above
4. Write actual PostgreSQL DDL
5. Seed with real data
