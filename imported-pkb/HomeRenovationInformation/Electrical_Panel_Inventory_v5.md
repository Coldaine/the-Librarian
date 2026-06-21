# Electrical Panel Inventory

*Document Created: February 8, 2026 | Based on physical walkthrough and outdoor inspection*

---

## Service Overview

- **Total Service:** 400A (two independent 200A mains)
- **Configuration:** Standard US residential split-phase 120/240V
- **Utility:** Cumberland Electric Membership Corporation (CEMC) — TVA cooperative
- **Meter:** Landis+Gyr Focus AXR — Gridstream RF Enhanced Integrated
  - Form 2SE, CL320, 240V, 3W, 60Hz, TA=50
  - ZigBee certified (HAN port present but locked down by CEMC — utility provisioning required, not available to consumers)
  - FCC ID: R7PEG1R1S2
- **Usage Portal:** SmartHub® — https://cemc.smarthub.coop (daily usage data only)

---

## Panel Topology

```
Utility Meter (400A service, CL320)
│
├── MAIN PANEL 1 — "Distribution / HVAC" (200A)
│   ├── 100A feeder → Outdoor HVAC Sub-Panel
│   │   ├── 60A — Trane XL15c (Zone 1)
│   │   └── 40A — Silver Series condenser (Zone 3 cooling)
│   ├── 100A feeder → Sub-Panel (Laundry Room)
│   ├── 80A — Pool Equipment (pump + electric heater, believed)
│   ├── 15A — Irrigation
│   └── (remaining slots empty)
│
├── MAIN PANEL 2 — "Heavy Loads / Appliances" (200A)
│   ├── 60A — AC Bonus Handler (Zone 2 air handler — heat source unknown)
│   ├── 60A — Hot Tub Rear Porch
│   ├── 20A 2-pole — AC Bonus Compressor (Silver Series condenser, Zone 2)
│   ├── 30A — Hot Water Backup
│   ├── 30A — Hot Water Main
│   ├── 40A — Oven/Microwave
│   ├── 30A — Single Oven
│   ├── 30A — Dryer
│   ├── 30A — Hot Water Porch
│   ├── 20A — AC Upstairs Handler (Zone 3 blower/furnace controls)
│   ├── 20A — AC Upstairs Handler (second breaker, same label)
│   ├── 15A — Garage Plug
│   ├── 15A — Garage Light
│   └── (remaining slots empty)
│
├── OUTDOOR HVAC SUB-PANEL (fed by 100A from Panel 1)
│   ├── 60A — Trane XL15c (Zone 1)
│   └── 40A — Silver Series condenser (Zone 3)
│
└── SUB-PANEL — Laundry Room (fed by 100A from Panel 1)
    └── 30× 15A/20A single-pole circuits (lighting, receptacles, kitchen, bedrooms)
    └── (remaining slots empty)

OUTDOOR HVAC UNITS (3 confirmed):
  1. Trane XL15c — Zone 1 (Main Floor) — packaged dual fuel
     Fed by 60A in outdoor HVAC sub-panel
  2. Silver Series condenser — Zone 2 (Bonus Room) — standalone
     Fed by 20A "AC Bonus Compressor" in Panel 2
  3. Silver Series condenser — Zone 3 (Upstairs) — in outdoor sub-panel
     Fed by 40A in outdoor HVAC sub-panel

INDOOR HVAC UNITS:
  - Propane furnace — Zone 3 (Upstairs closet) — confirmed
```

**Note:** All panels are standard residential sizes. Any slot not listed above is empty/blank. There is significant spare capacity in all panels.

---

## Panel 1 — Distribution / HVAC (at Meter)

**Main Breaker:** 200A disconnect

| Side | Slots | Amps | Poles | Label | Notes |
|------|-------|------|-------|-------|-------|
| Left | 1–2 | **100A** | 2-pole | AC Main Floor | Feeds outdoor HVAC sub-panel: 60A (Trane XL15c) + 40A (Silver Series condenser) |
| Left | 3–4 | **100A** | 2-pole | Sub Panel Laundry | Feeder to Laundry Room sub-panel (30 circuits) |
| Right | 1 | 15A | single | Outdoor Irrigation | |
| Right | 2–3 | **80A** | 2-pole | Pool Equipment | Believed to be pump + electric heater (unconfirmed). Pool closed for winter. |

All remaining slots are empty.

**Breaker Summary — Panel 1:**
- 2× 100A 2-pole
- 1× 80A 2-pole
- 1× 15A single
- **Total: 4 branch circuits**

---

## Panel 2 — Heavy Loads / Appliances (at Meter)

**Main Breaker:** 200A disconnect

### Left Side

| Slots | Amps | Poles | Label | Notes |
|-------|------|-------|-------|-------|
| — | **60A** | 2-pole | AC Bonus Handler | Zone 2 indoor air handler. Heat source unknown — thermostat shows no emergency/aux mode. 60A breaker suggests possible electric heat strips but unconfirmed. |
| — | **60A** | 2-pole | Hot Tub Rear Porch | |
| — | 20A | 2-pole | AC Bonus Compressor | Zone 2 cooling — Silver Series condenser (standalone, direct connection) |
| — | 30A | 2-pole | Hot Water Backup | A.O. Smith 50gal 4,500W |
| — | 30A | 2-pole | Hot Water Main | A.O. Smith 50gal 4,500W |

### Right Side

| Slots | Amps | Poles | Label | Notes |
|-------|------|-------|-------|-------|
| — | **40A** | 2-pole | Oven Microwave | |
| — | 30A | 2-pole | Single Oven | |
| — | 30A | 2-pole | Dryer | |
| — | 30A | 2-pole | Hot Water Porch | A.O. Smith 50gal 4,500W |
| — | 20A | individual | AC Upstairs Handler | Zone 3 blower + propane furnace controls. Configuration of the two breakers unknown (two separate 120V circuits, or other arrangement). |
| — | 20A | individual | AC Upstairs Handler | (second breaker, same label) |
| — | 15A | individual | Garage Plug | |
| — | 15A | individual | Garage Light | |

All remaining slots are empty.

**Breaker Summary — Panel 2:**
- 2× 60A 2-pole
- 1× 40A 2-pole
- 1× 20A 2-pole (AC Bonus Compressor)
- 5× 30A 2-pole (3 water heaters, single oven, dryer)
- 2× 20A individual (AC Upstairs Handler)
- 2× 15A individual (garage)
- **Total: 13 branch circuits**

---

## Sub-Panel — Laundry Room (General Circuits)

**Fed by:** 100A 2-pole breaker from Panel 1

All circuits are single-pole 15A or 20A — standard lighting and receptacles.

### Left Side

| Amps | Label |
|------|-------|
| 20A | Bath GFCI |
| 20A | Disposal |
| 20A | Kitchen Plugs |
| 20A | Refrigerator |
| 20A | Dishwasher |
| 15A | Breakfast Plug |
| 15A | Hall Light |
| 15A | Hood |
| 15A | Kit Lights |
| 15A | Powder Rm & Hall |
| 15A | Dining Play Light |
| 20A | Back Room |
| 15A | Upstairs Hall |
| 15A | Bonus, Bath & Stair Lights |
| 15A | Front Door Hall |

### Right Side

| Amps | Label | Notes |
|------|-------|-------|
| 20A | Laundry Rm | |
| 20A | Washer | |
| 20A | MB Tub (jetted) | |
| 20A | HW Pumps (recirc) | Recirculation pump for water heaters |
| 20A | Central VAC | |
| 20A | Dining Room | |
| 15A | Wine Cooler / Butler / Bath Floor | AFCI |
| 15A | Living Rm | |
| 15A | Up Rear West Bdr | AFCI |
| 15A | Up Front Bdr | AFCI |
| 15A | Up Rear East / Smoke D | AFCI |
| 15A | Master Sit | AFCI |
| 15A | Master Bdr | AFCI |
| 15A | Guest Bdr | AFCI |
| 15A | Master Bath Lights / Bonus Rm Plug | |

All remaining slots are empty.

**Breaker Summary — Sub-Panel:**
- 12× 20A single-pole
- 18× 15A single-pole
- **Total: 30 branch circuits**

---

## Grand Total — All Panels

| Breaker Size | Panel 1 | Panel 2 | Sub-Panel | Total |
|-------------|---------|---------|-----------|-------|
| 100A 2-pole | 2 | — | — | **2** |
| 80A 2-pole | 1 | — | — | **1** |
| 60A 2-pole | — | 2 | — | **2** |
| 40A 2-pole | — | 1 | — | **1** |
| 30A 2-pole | — | 5 | — | **5** |
| 20A 2-pole | — | 1 | — | **1** |
| 20A single | — | 2 | 12 | **14** |
| 15A single | 1 | 2 | 18 | **21** |
| **TOTAL** | **4** | **13** | **30** | **47** |

*Note: Outdoor HVAC sub-panel (60A + 40A) is downstream of Panel 1's 100A "AC Main Floor" breaker and not counted separately in grand total.*

---

## HVAC System — Three Zones, Three Outdoor Units

### Zone Map

| Zone | Area | Heating | Cooling | Outdoor Unit | Breaker(s) |
|------|------|---------|---------|--------------|------------|
| **1** | Main Floor | Trane XL15c heat pump + propane backup | Trane XL15c (same unit) | Trane XL15c | 60A in outdoor HVAC sub-panel ← 100A "AC Main Floor" in Panel 1 |
| **2** | Bonus Room | Unknown — thermostat shows no emergency/aux mode | Silver Series condenser | Silver Series (standalone) | 60A "AC Bonus Handler" + 20A "AC Bonus Compressor" in Panel 2 |
| **3** | Upstairs | Propane furnace (upstairs closet) | Silver Series condenser | Silver Series (in outdoor sub-panel) | 40A in outdoor HVAC sub-panel ← 100A Panel 1; 2× 20A "AC Upstairs Handler" in Panel 2 |

### Outdoor Units

1. **Trane XL15c** — Zone 1 (Main Floor)
   - Model: 4DCZ6060C1115A (5-ton, 115,000 BTU heating)
   - Type: Heat Pump + Propane backup, 81% AFUE
   - Electrical: 208/230V, single-phase, 60A circuit spec
   - Compressor RLA: 27.1A | LRA: 152.9A
   - Fed by 60A breaker in outdoor HVAC sub-panel
2. **Silver Series Condenser** — Zone 2 (Bonus Room)
   - Model: 4A6H4036D1000AA (2014), 3-ton, 14 SEER, ~25–35A at 240V
   - Fed by 20A "AC Bonus Compressor" in Panel 2 (direct connection)
3. **Silver Series Condenser** — Zone 3 (Upstairs)
   - Same model as #2
   - Fed by 40A breaker in outdoor HVAC sub-panel

### Outdoor HVAC Sub-Panel

- **Location:** Outside, near outdoor units
- **Fed by:** 100A "AC Main Floor" breaker in Panel 1
- **Contains:**
  - 60A breaker → Trane XL15c (Zone 1)
  - 40A breaker → Silver Series condenser (Zone 3)

### Indoor Units

- **Propane Furnace** (Zone 3) — conventional gas furnace in upstairs closet. Blower and controls powered by the 2× 20A "AC Upstairs Handler" breakers in Panel 2.

---

## Water Heater System

**Model:** A.O. Smith ENS 50100 (ProLine series)
- **Quantity:** 3 units
- **Tank Size:** 50 gallons each (150 gallons total storage)
- **First Hour Rating:** 62 gallons
- **Power:** 4,500W each at 240V (~18.75A per unit)
- **Combined worst-case draw:** 13,500W / ~56A
- **Locations:** Main, Backup, Porch (serves rear porch/hot tub area)
- **Recirculation:** HW Pumps circuit in sub-panel indicates recirc system

---

## Open Questions

| # | Question | Notes |
|---|----------|-------|
| 1 | Zone 2 bonus room — heat source unknown. 60A handler breaker suggests possible electric heat strips, but thermostat shows no emergency/aux mode. | Would need to open air handler to inspect, or find model number on handler. |
| 2 | Pool equipment (80A) — believed to be pump + electric heater, but unconfirmed. | Pool closed for winter. Electric heater could draw 50A+ sustained when operational. |
| 3 | AC Upstairs Handler — two individual 20A breakers with the same label. Unknown whether these are two separate 120V circuits or some other configuration. | Low priority — both breakers serve Zone 3 blower/furnace regardless. |
