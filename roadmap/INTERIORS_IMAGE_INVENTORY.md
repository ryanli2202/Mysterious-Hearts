# Interiors room and image inventory

**Status:** Generation paused on 2026-11-11. Batches 01 and 02 artwork remain complete, retaining 48 and 41 accepted files respectively. Batch 03 is unfinished, with one accepted file and three staged drafts; 47 images are not started. See the manifests for outputs and provenance. No runtime mappings changed.
**Source:** All three interiors plan documents plus current location assets and selected campaign sources.

**Production grouping:** [Ten generation batches](INTERIORS_GENERATION_BATCHES.md), with per-image Markdown and JSON manifests. Production metadata now exists: revise inventory and batch manifests explicitly together. Initial planning generators refuse to overwrite production records.

## Totals

| Scope | Views | Reuse candidates | New images | Layout decisions |
| --- | ---: | ---: | ---: | ---: |
| Interior | 508 | 87 | 421 | 0 |
| Outdoor | 20 | 3 | 17 | 0 |
| Conditional | 2 | 0 | 0 | 2 |

**90 building/group entries.** Each listed room/view has one image slot. Outdoor views and unresolved dorm bathrooms are separated from the firm interior count.

**Production review note:** Counts above retain the original allocation. Of its 90 reuse candidates, Garrett’s living-room candidate was rejected at full size because it depicts an exterior estate facade/courtyard. It may guide architectural styling but cannot cover an indoor living room. A replacement must be added through an explicit inventory/batch revision before release. The [batch 01 review](interiors-generation-batches/interiors-01-production/PRODUCTION_REVIEW.md) records the 48 accepted new images and checks; it does not claim final approval of reused rooms.

The [batch 02 review](interiors-generation-batches/interiors-02-production/PRODUCTION_REVIEW.md) records another 41 accepted images and all seven original references unchanged. Lena's and Naomi's original living-room images depict open sleeping areas, whereas the planned layouts have private bedrooms. Reconcile original-art reuse and room/privacy routing before runtime integration; this production operation does not change the approved allocation or silently add replacement images.

Reuse means a visually matching candidate identified in the contact-sheet audit, not a final in-game approval. Every candidate has a real path, dimensions and SHA-256 in the JSON companion; none is assigned to two views or has identical bytes to another selected candidate. Full-resolution detail, art continuity, door positions and character framing still need final review. Budget new artwork for every New row; replacement of a rejected candidate would increase that budget.

## Scope and counting decisions

- This is the complete enumerated production baseline for the currently specified layouts, including the integration review's missing JobSeek staff rooms. It is not proof that every future campaign scene has been implemented or that no later design change can add rooms.
- Each semicolon-separated space in the authored data is a separate image/view. Explicit navigable alcoves, counters and seating views receive their own image even when they share a physical room. Ordinary clickable hotspots (a chair, sink or desk) do not get extra images. Open zones retain shared witnesses.
- Named entrances and stairways are budgeted as separate views unless the plan explicitly makes them a doorway action (Mavis and the dorm thresholds). Outdoor frontages already used for travel remain separate assets, not new indoor lobbies.
- One restroom scene per public/working building is budgeted to close the plans' general bathroom requirement. Private/public boundaries must remain separate. Leader bases include a visitor restroom and private bathroom. These are proposed service-layout details; extra cubicles are not individually navigable.
- Dorm bathrooms remain conditional. Generic labels such as shop units resolve to one JobSeek tenant and its support rooms for this baseline, not an unlimited mall. Generic residential areas at six gang bases are expanded into bounded proposed rooms below.
- Existing home images often show adjoining open-plan areas. Reuse is allocated to one primary room only; new views must preserve visual continuity. A reused image may show a doorway but cannot act as the image for every room behind it.
- One guard post does not require one background: guards overlay their assigned room/view. Neither NPCs nor automatic outfits are baked into the art. New enclosed guardrooms require new inventory entries.
- Historical flashbacks, unspecified new venues and future campaign-specific spaces are not silently invented or assigned arbitrary room counts; see the coverage notes below.

## Building summary

| Building | Interior | Outdoor | Conditional | Reuse candidates |
| --- | ---: | ---: | ---: | ---: |
| [Rei and Yuriko's penthouse](#rei-home) | 9 | 0 | 0 | 1 |
| [Emily's garden apartment](#emily-home) | 7 | 1 | 0 | 1 |
| [Sophie's trackside loft](#sophie-home) | 6 | 1 | 0 | 1 |
| [Amy's dorm](#amy-home) | 1 | 0 | 1 | 1 |
| [Amy and Minsu's shared building access](#nest-dorm-corridor) | 1 | 0 | 0 | 0 |
| [Minsu's dorm](#minsu-home) | 1 | 0 | 1 | 1 |
| [Samantha's garage flat](#samantha-home) | 7 | 0 | 0 | 1 |
| [April's observatory townhouse](#april-home) | 10 | 1 | 0 | 1 |
| [Garrett's hillside estate](#garrett-home) | 10 | 1 | 0 | 1 |
| [Yeuns' Ferry Signal House](#valentina-home) | 10 | 0 | 0 | 1 |
| [Neo and Alyssa's station apartment](#neo-home) | 6 | 1 | 0 | 1 |
| [Tyler's East Ward duplex](#tyler-home) | 6 | 1 | 0 | 1 |
| [Lena's clocktower flat](#lena-home) | 7 | 0 | 0 | 1 |
| [Naomi's riverside maisonette](#naomi-home) | 7 | 1 | 0 | 1 |
| [Celeste's blue-door cottage](#celeste-home) | 6 | 0 | 0 | 1 |
| [Dev's station studio](#dev-home) | 3 | 0 | 0 | 1 |
| [Rosa's market terrace](#rosa-home) | 8 | 1 | 0 | 1 |
| [Elliot's willow cabin](#elliot-home) | 4 | 1 | 0 | 1 |
| [Daniel's flat above the Bijou](#daniel-home) | 6 | 0 | 0 | 1 |
| [Fox's Blackhaven hideout](#fox-home) | 7 | 0 | 0 | 1 |
| [Gordon's Civic Court apartment](#gordon-home) | 6 | 0 | 0 | 1 |
| [Sylvanis's shuttered flat](#sylvanis-home) | 6 | 0 | 0 | 1 |
| [Martos's apartment](#martos-home) | 7 | 0 | 0 | 1 |
| [Elias's penthouse](#elias-home) | 7 | 0 | 0 | 1 |
| [Mavis's private room](#mavis-home) | 1 | 0 | 0 | 1 |
| [Camila's apartment](#camila-home) | 7 | 0 | 0 | 1 |
| [Downtown apartment](#vacant-downtown-home) | 5 | 0 | 0 | 1 |
| [Suburban house](#vacant-suburbs-home) | 7 | 1 | 0 | 1 |
| [Beach cottage](#vacant-beach-home) | 6 | 1 | 0 | 1 |
| [University apartment](#vacant-university-home) | 4 | 0 | 0 | 1 |
| [Campus café](#cafe) | 7 | 0 | 0 | 1 |
| [Golden Dragon](#noodle-shop) | 6 | 0 | 0 | 1 |
| [Mario's Pizza](#marios-pizza) | 4 | 0 | 0 | 1 |
| [Chess café](#chess) | 5 | 0 | 0 | 1 |
| [Petal & Stem](#flowers) | 5 | 0 | 0 | 1 |
| [Gift boutique](#boutique) | 4 | 0 | 0 | 1 |
| [Winterfield Galleria and JobSeek tenant](#shopping-mall) | 8 | 0 | 0 | 0 |
| [Winterfield University](#campus) | 8 | 0 | 0 | 0 |
| [University track pavilion](#track) | 4 | 0 | 0 | 0 |
| [Downtown modelling and recording studio](#studio) | 8 | 0 | 0 | 1 |
| [Arena lounge and training](#arena) | 6 | 0 | 0 | 1 |
| [East Ward Boxing Club](#boxing-club) | 6 | 0 | 0 | 1 |
| [Iron Circle](#iron-circle) | 6 | 0 | 0 | 1 |
| [Public library](#library) | 7 | 0 | 0 | 0 |
| [Old town archive](#archive) | 5 | 0 | 0 | 1 |
| [Station makerspace](#makerspace) | 5 | 0 | 0 | 1 |
| [Riverside cycle workshop](#cycle-shop) | 4 | 0 | 0 | 1 |
| [Hilltop planetarium](#planetarium) | 5 | 0 | 0 | 1 |
| [Bijou cinema](#cinema) | 6 | 0 | 0 | 1 |
| [Municipal boathouse](#sailing-club) | 4 | 1 | 0 | 1 |
| [Lantern community market](#market) | 3 | 1 | 0 | 1 |
| [Winterfield Lanes](#bowling-alley) | 4 | 0 | 0 | 0 |
| [Pixel Pier](#arcade) | 7 | 0 | 0 | 0 |
| [Afterglow](#nightclub) | 6 | 0 | 0 | 0 |
| [Copper Lantern](#bar) | 5 | 0 | 0 | 0 |
| [Commons gardener pavilion](#public-park-pavilion) | 3 | 0 | 0 | 0 |
| [Silver Sands beach](#beach) | 0 | 1 | 0 | 0 |
| [Hillside Tea Room](#hill-tea-room) | 4 | 0 | 0 | 1 |
| [Westbrook farm shop](#farm-shop) | 4 | 0 | 0 | 1 |
| [Old Mill pottery studio](#pottery-studio) | 4 | 0 | 0 | 1 |
| [Marine discovery centre](#marine-centre) | 5 | 0 | 0 | 1 |
| [South Harbour covered market](#harbour-market) | 2 | 3 | 0 | 1 |
| [Railway museum](#railway-museum) | 4 | 0 | 0 | 1 |
| [Riverside diner](#southbank-diner) | 4 | 0 | 0 | 1 |
| [Waterfront executive offices](#syndicate-office) | 4 | 0 | 0 | 1 |
| [Syndicate underground HQ](#syndicate-hq) | 7 | 0 | 0 | 1 |
| [Red Dragons lounge](#syndicate) | 6 | 0 | 0 | 1 |
| [Kestrel Operations Centre](#site-01) | 6 | 0 | 0 | 2 |
| [Pacific Relay Depot](#site-02) | 6 | 0 | 0 | 2 |
| [Stillwater Research Annex](#site-03) | 6 | 0 | 0 | 2 |
| [Breakwater Security Depot](#site-04) | 6 | 0 | 0 | 2 |
| [Aster Media House](#site-05) | 6 | 0 | 0 | 2 |
| [Meridian Capital Offices](#site-06) | 6 | 0 | 0 | 2 |
| [Oculus Winterfield Campus](#site-07) | 8 | 0 | 0 | 2 |
| [Greyglass Service House](#site-08) | 6 | 0 | 0 | 2 |
| [Glasshouse](#glasshouse-lab) | 7 | 0 | 0 | 1 |
| [Interpol Regional HQ](#interpol-hq) | 7 | 0 | 0 | 4 |
| [Blackstone Headquarters](#blackstone-hq) | 6 | 1 | 0 | 5 |
| [Lantern House](#lantern-house) | 9 | 0 | 0 | 1 |
| [Saints Rail Depot](#saints-depot) | 7 | 0 | 0 | 1 |
| [Purple Skulls clubhouse](#purple-clubhouse) | 10 | 0 | 0 | 1 |
| [Kurose House](#hamayashi-house) | 8 | 1 | 0 | 1 |
| [Los Rojos base](#rojos-courtyard) | 9 | 1 | 0 | 1 |
| [Waterfront Consortium House](#consortium-house) | 9 | 0 | 0 | 1 |
| [Hamayashi riverside annex](#hamayashi-annex) | 3 | 0 | 0 | 1 |
| [Hamayashi supply house](#hamayashi-store) | 4 | 0 | 0 | 1 |
| [West workshop](#crew-lot-west) | 4 | 0 | 0 | 0 |
| [Dock warehouse](#crew-lot-docks) | 4 | 0 | 0 | 0 |
| [Northern offices](#crew-lot-north) | 4 | 0 | 0 | 0 |
| [South garage](#crew-lot-south) | 4 | 0 | 0 | 0 |

## Homes

### rei-home

**Rei and Yuriko's penthouse** — planning key `rei_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/rei_home/entrance.png` |
| Living space | interior | Reuse candidate | [rei_home.png](../assets/ui/locations/rei_home.png) |
| Kitchen and dining | interior | New | `assets/ui/locations/interiors/rei_home/kitchen_and_dining.png` |
| Library | interior | New | `assets/ui/locations/interiors/rei_home/library.png` |
| Art space | interior | New | `assets/ui/locations/interiors/rei_home/art_space.png` |
| Hallway | interior | New | `assets/ui/locations/interiors/rei_home/hallway.png` |
| Rei bedroom | interior | New | `assets/ui/locations/interiors/rei_home/rei_bedroom.png` |
| Yuriko bedroom | interior | New | `assets/ui/locations/interiors/rei_home/yuriko_bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/rei_home/bathroom.png` |

### emily-home

**Emily's garden apartment** — planning key `emily_home`.

Existing image shows a bed, so allocate it to the bedroom, not the proposed separate living room.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/emily_home/entrance.png` |
| Living room | interior | New | `assets/ui/locations/interiors/emily_home/living_room.png` |
| Kitchen | interior | New | `assets/ui/locations/interiors/emily_home/kitchen.png` |
| LEGO workroom | interior | New | `assets/ui/locations/interiors/emily_home/lego_workroom.png` |
| Hall | interior | New | `assets/ui/locations/interiors/emily_home/hall.png` |
| Bedroom | interior | Reuse candidate | [emily_home.png](../assets/ui/locations/emily_home.png) |
| Bathroom | interior | New | `assets/ui/locations/interiors/emily_home/bathroom.png` |
| Flower balcony | outdoor | New | `assets/ui/locations/interiors/emily_home/flower_balcony.png` |

### sophie-home

**Sophie's trackside loft** — planning key `sophie_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/sophie_home/entrance.png` |
| Open living kitchen | interior | Reuse candidate | [sophie_home.png](../assets/ui/locations/sophie_home.png) |
| Stretching zone view | interior | New | `assets/ui/locations/interiors/sophie_home/stretching_zone_view.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/sophie_home/stairway.png` |
| Sleeping loft | interior | New | `assets/ui/locations/interiors/sophie_home/sleeping_loft.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/sophie_home/bathroom.png` |
| Balcony | outdoor | New | `assets/ui/locations/interiors/sophie_home/balcony.png` |

### amy-home

**Amy's dorm** — planning key `amy_home`.

Bathroom configuration is unresolved; do not generate bathroom art until the dorm layout is settled.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Dorm room | interior | Reuse candidate | [amy_home.png](../assets/ui/locations/amy_home.png) |
| Bathroom | conditional | Hold: layout decision | `assets/ui/locations/interiors/amy_home/bathroom.png` |

### nest-dorm-corridor

**Amy and Minsu's shared building access** — planning key `nest_dorm_corridor`.

Proposed planning-only building/view key; not a current runtime location. Keep separate dorm entry gates.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Public dorm corridor | interior | New | `assets/ui/locations/interiors/nest_dorm_corridor/public_dorm_corridor.png` |

### minsu-home

**Minsu's dorm** — planning key `minsu_home`.

Bathroom configuration is unresolved; do not generate bathroom art until the dorm layout is settled.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Dorm room | interior | Reuse candidate | [minsu_home.png](../assets/ui/locations/minsu_home.png) |
| Bathroom | conditional | Hold: layout decision | `assets/ui/locations/interiors/minsu_home/bathroom.png` |

### samantha-home

**Samantha's garage flat** — planning key `samantha_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Street-entry vestibule | interior | New | `assets/ui/locations/interiors/samantha_home/street_entry_vestibule.png` |
| Garage workbench | interior | New | `assets/ui/locations/interiors/samantha_home/garage_workbench.png` |
| Heavy-bag zone view | interior | New | `assets/ui/locations/interiors/samantha_home/heavy_bag_zone_view.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/samantha_home/stairway.png` |
| Living kitchen | interior | Reuse candidate | [samantha_home.png](../assets/ui/locations/samantha_home.png) |
| Bedroom | interior | New | `assets/ui/locations/interiors/samantha_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/samantha_home/bathroom.png` |

### april-home

**April's observatory townhouse** — planning key `april_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/april_home/entrance.png` |
| Sitting chess room | interior | Reuse candidate | [april_home.png](../assets/ui/locations/april_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/april_home/kitchen.png` |
| Hall | interior | New | `assets/ui/locations/interiors/april_home/hall.png` |
| Study lab desk | interior | New | `assets/ui/locations/interiors/april_home/study_lab_desk.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/april_home/bathroom.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/april_home/stairway.png` |
| Upper landing | interior | New | `assets/ui/locations/interiors/april_home/upper_landing.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/april_home/bedroom.png` |
| Roof access | interior | New | `assets/ui/locations/interiors/april_home/roof_access.png` |
| Telescope terrace | outdoor | New | `assets/ui/locations/interiors/april_home/telescope_terrace.png` |

### garrett-home

**Garrett's hillside estate** — planning key `garrett_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Foyer | interior | New | `assets/ui/locations/interiors/garrett_home/foyer.png` |
| Living room | interior | Reuse candidate | [garrett_home.png](../assets/ui/locations/garrett_home.png) |
| Dining room | interior | New | `assets/ui/locations/interiors/garrett_home/dining_room.png` |
| Noodle kitchen | interior | New | `assets/ui/locations/interiors/garrett_home/noodle_kitchen.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/garrett_home/stairway.png` |
| Landing | interior | New | `assets/ui/locations/interiors/garrett_home/landing.png` |
| Garage passage | interior | New | `assets/ui/locations/interiors/garrett_home/garage_passage.png` |
| Garage | interior | New | `assets/ui/locations/interiors/garrett_home/garage.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/garrett_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/garrett_home/bathroom.png` |
| Terrace | outdoor | New | `assets/ui/locations/interiors/garrett_home/terrace.png` |

### valentina-home

**Yeuns' Ferry Signal House** — planning key `valentina_home`.

Use the current shared signal-house art. Legacy ivan_home.png depicts the older home and is not a second room of this building.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/valentina_home/entrance.png` |
| Harbour living room | interior | Reuse candidate | [valentina_home.png](../assets/ui/locations/valentina_home.png) |
| Kitchen dining | interior | New | `assets/ui/locations/interiors/valentina_home/kitchen_dining.png` |
| Piano alcove view | interior | New | `assets/ui/locations/interiors/valentina_home/piano_alcove_view.png` |
| Sail workroom | interior | New | `assets/ui/locations/interiors/valentina_home/sail_workroom.png` |
| Mezzanine stairway | interior | New | `assets/ui/locations/interiors/valentina_home/mezzanine_stairway.png` |
| Reading mezzanine | interior | New | `assets/ui/locations/interiors/valentina_home/reading_mezzanine.png` |
| Ivan bedroom | interior | New | `assets/ui/locations/interiors/valentina_home/ivan_bedroom.png` |
| Valentina bedroom | interior | New | `assets/ui/locations/interiors/valentina_home/valentina_bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/valentina_home/bathroom.png` |

### neo-home

**Neo and Alyssa's station apartment** — planning key `neo_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/neo_home/entrance.png` |
| Living room | interior | Reuse candidate | [neo_home.png](../assets/ui/locations/neo_home.png) |
| Kitchen dining | interior | New | `assets/ui/locations/interiors/neo_home/kitchen_dining.png` |
| Hall | interior | New | `assets/ui/locations/interiors/neo_home/hall.png` |
| Shared bedroom | interior | New | `assets/ui/locations/interiors/neo_home/shared_bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/neo_home/bathroom.png` |
| Herb balcony | outdoor | New | `assets/ui/locations/interiors/neo_home/herb_balcony.png` |

### tyler-home

**Tyler's East Ward duplex** — planning key `tyler_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entry living room | interior | Reuse candidate | [tyler_home.png](../assets/ui/locations/tyler_home.png) |
| Kitchen dining | interior | New | `assets/ui/locations/interiors/tyler_home/kitchen_dining.png` |
| Level hall | interior | New | `assets/ui/locations/interiors/tyler_home/level_hall.png` |
| Tyler bedroom | interior | New | `assets/ui/locations/interiors/tyler_home/tyler_bedroom.png` |
| Father bedroom | interior | New | `assets/ui/locations/interiors/tyler_home/father_bedroom.png` |
| Accessible bathroom | interior | New | `assets/ui/locations/interiors/tyler_home/accessible_bathroom.png` |
| Accessible porch | outdoor | New | `assets/ui/locations/interiors/tyler_home/accessible_porch.png` |

### lena-home

**Lena's clocktower flat** — planning key `lena_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/lena_home/entrance.png` |
| Living record room | interior | Reuse candidate | [lena_home.png](../assets/ui/locations/lena_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/lena_home/kitchen.png` |
| Photo workroom | interior | New | `assets/ui/locations/interiors/lena_home/photo_workroom.png` |
| Hall | interior | New | `assets/ui/locations/interiors/lena_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/lena_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/lena_home/bathroom.png` |

### naomi-home

**Naomi's riverside maisonette** — planning key `naomi_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/naomi_home/entrance.png` |
| Living room | interior | Reuse candidate | [naomi_home.png](../assets/ui/locations/naomi_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/naomi_home/kitchen.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/naomi_home/stairway.png` |
| Landing | interior | New | `assets/ui/locations/interiors/naomi_home/landing.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/naomi_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/naomi_home/bathroom.png` |
| Balcony | outdoor | New | `assets/ui/locations/interiors/naomi_home/balcony.png` |

### celeste-home

**Celeste's blue-door cottage** — planning key `celeste_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/celeste_home/entrance.png` |
| Piano sitting room | interior | Reuse candidate | [celeste_home.png](../assets/ui/locations/celeste_home.png) |
| Kitchen dining | interior | New | `assets/ui/locations/interiors/celeste_home/kitchen_dining.png` |
| Hall | interior | New | `assets/ui/locations/interiors/celeste_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/celeste_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/celeste_home/bathroom.png` |

### dev-home

**Dev's station studio** — planning key `dev_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/dev_home/entrance.png` |
| Studio room | interior | Reuse candidate | [dev_home.png](../assets/ui/locations/dev_home.png) |
| Bathroom | interior | New | `assets/ui/locations/interiors/dev_home/bathroom.png` |

### rosa-home

**Rosa's market terrace** — planning key `rosa_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/rosa_home/entrance.png` |
| Sitting room | interior | New | `assets/ui/locations/interiors/rosa_home/sitting_room.png` |
| Communal dining room | interior | Reuse candidate | [rosa_home.png](../assets/ui/locations/rosa_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/rosa_home/kitchen.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/rosa_home/stairway.png` |
| Landing | interior | New | `assets/ui/locations/interiors/rosa_home/landing.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/rosa_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/rosa_home/bathroom.png` |
| Shared courtyard | outdoor | New | `assets/ui/locations/interiors/rosa_home/shared_courtyard.png` |

### elliot-home

**Elliot's willow cabin** — planning key `elliot_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Living workroom | interior | Reuse candidate | [elliot_home.png](../assets/ui/locations/elliot_home.png) |
| Kitchenette | interior | New | `assets/ui/locations/interiors/elliot_home/kitchenette.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/elliot_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/elliot_home/bathroom.png` |
| Covered porch | outdoor | New | `assets/ui/locations/interiors/elliot_home/covered_porch.png` |

### daniel-home

**Daniel's flat above the Bijou** — planning key `daniel_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Stair entrance | interior | New | `assets/ui/locations/interiors/daniel_home/stair_entrance.png` |
| Poster hall | interior | Reuse candidate | [daniel_home.png](../assets/ui/locations/daniel_home.png) |
| Living drawing room | interior | New | `assets/ui/locations/interiors/daniel_home/living_drawing_room.png` |
| Kitchen | interior | New | `assets/ui/locations/interiors/daniel_home/kitchen.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/daniel_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/daniel_home/bathroom.png` |

### fox-home

**Fox's Blackhaven hideout** — planning key `fox_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/fox_home/entrance.png` |
| Living kettle room | interior | New | `assets/ui/locations/interiors/fox_home/living_kettle_room.png` |
| Equipment workshop | interior | Reuse candidate | [fox_home.png](../assets/ui/locations/fox_home.png) |
| Private evidence room | interior | New | `assets/ui/locations/interiors/fox_home/private_evidence_room.png` |
| Hall | interior | New | `assets/ui/locations/interiors/fox_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/fox_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/fox_home/bathroom.png` |

### gordon-home

**Gordon's Civic Court apartment** — planning key `gordon_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance uniform locker | interior | New | `assets/ui/locations/interiors/gordon_home/entrance_uniform_locker.png` |
| Living reading room | interior | Reuse candidate | [gordon_home.png](../assets/ui/locations/gordon_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/gordon_home/kitchen.png` |
| Hall | interior | New | `assets/ui/locations/interiors/gordon_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/gordon_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/gordon_home/bathroom.png` |

### sylvanis-home

**Sylvanis's shuttered flat** — planning key `sylvanis_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Bell entrance | interior | New | `assets/ui/locations/interiors/sylvanis_home/bell_entrance.png` |
| Bare sitting room | interior | Reuse candidate | [sylvanis_home.png](../assets/ui/locations/sylvanis_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/sylvanis_home/kitchen.png` |
| Private notes room | interior | New | `assets/ui/locations/interiors/sylvanis_home/private_notes_room.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/sylvanis_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/sylvanis_home/bathroom.png` |

### martos-home

**Martos's apartment** — planning key `martos_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/martos_home/entrance.png` |
| Living room | interior | Reuse candidate | [martos_home.png](../assets/ui/locations/martos_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/martos_home/kitchen.png` |
| Watch workroom | interior | New | `assets/ui/locations/interiors/martos_home/watch_workroom.png` |
| Hall | interior | New | `assets/ui/locations/interiors/martos_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/martos_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/martos_home/bathroom.png` |

### elias-home

**Elias's penthouse** — planning key `elias_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/elias_home/entrance.png` |
| Sitting rehearsal room | interior | Reuse candidate | [elias_home.png](../assets/ui/locations/elias_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/elias_home/kitchen.png` |
| Script study | interior | New | `assets/ui/locations/interiors/elias_home/script_study.png` |
| Hall | interior | New | `assets/ui/locations/interiors/elias_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/elias_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/elias_home/bathroom.png` |

### mavis-home

**Mavis's private room** — planning key `mavis_home`.

Threshold is a doorway action within this single-room view, not an invented lobby. No address or additional private rooms are established.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Private room | interior | Reuse candidate | [mavis_home.png](../assets/ui/locations/mavis_home.png) |

### camila-home

**Camila's apartment** — planning key `camila_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/camila_home/entrance.png` |
| Living chess room | interior | Reuse candidate | [camila_home.png](../assets/ui/locations/camila_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/camila_home/kitchen.png` |
| Private study | interior | New | `assets/ui/locations/interiors/camila_home/private_study.png` |
| Hall | interior | New | `assets/ui/locations/interiors/camila_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/camila_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/camila_home/bathroom.png` |

## Custom homes

### vacant-downtown-home

**Downtown apartment** — planning key `vacant_downtown_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/vacant_downtown_home/entrance.png` |
| Open living kitchen | interior | Reuse candidate | [vacant_downtown_home.png](../assets/ui/locations/vacant_downtown_home.png) |
| Hall | interior | New | `assets/ui/locations/interiors/vacant_downtown_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/vacant_downtown_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/vacant_downtown_home/bathroom.png` |

### vacant-suburbs-home

**Suburban house** — planning key `vacant_suburbs_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/vacant_suburbs_home/entrance.png` |
| Living room | interior | Reuse candidate | [vacant_suburbs_home.png](../assets/ui/locations/vacant_suburbs_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/vacant_suburbs_home/kitchen.png` |
| Hall | interior | New | `assets/ui/locations/interiors/vacant_suburbs_home/hall.png` |
| Bedroom 1 | interior | New | `assets/ui/locations/interiors/vacant_suburbs_home/bedroom_1.png` |
| Bedroom 2 | interior | New | `assets/ui/locations/interiors/vacant_suburbs_home/bedroom_2.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/vacant_suburbs_home/bathroom.png` |
| Garden | outdoor | New | `assets/ui/locations/interiors/vacant_suburbs_home/garden.png` |

### vacant-beach-home

**Beach cottage** — planning key `vacant_beach_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/vacant_beach_home/entrance.png` |
| Living room | interior | Reuse candidate | [vacant_beach_home.png](../assets/ui/locations/vacant_beach_home.png) |
| Kitchen | interior | New | `assets/ui/locations/interiors/vacant_beach_home/kitchen.png` |
| Hall | interior | New | `assets/ui/locations/interiors/vacant_beach_home/hall.png` |
| Bedroom | interior | New | `assets/ui/locations/interiors/vacant_beach_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/vacant_beach_home/bathroom.png` |
| Dune deck | outdoor | New | `assets/ui/locations/interiors/vacant_beach_home/dune_deck.png` |

### vacant-university-home

**University apartment** — planning key `vacant_university_home`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/vacant_university_home/entrance.png` |
| Living study kitchenette | interior | Reuse candidate | [vacant_university_home.png](../assets/ui/locations/vacant_university_home.png) |
| Bedroom | interior | New | `assets/ui/locations/interiors/vacant_university_home/bedroom.png` |
| Bathroom | interior | New | `assets/ui/locations/interiors/vacant_university_home/bathroom.png` |

## Public and work

### cafe

**Campus café** — planning key `cafe`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/cafe/entrance.png` |
| Counter seating room | interior | Reuse candidate | [cafe-evening.png](../assets/ui/cafe-evening.png) |
| Quiet study room | interior | New | `assets/ui/locations/interiors/cafe/quiet_study_room.png` |
| Staff kitchen | interior | New | `assets/ui/locations/interiors/cafe/staff_kitchen.png` |
| Staff office | interior | New | `assets/ui/locations/interiors/cafe/staff_office.png` |
| Service corridor | interior | New | `assets/ui/locations/interiors/cafe/service_corridor.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/cafe/restroom.png` |

### noodle-shop

**Golden Dragon** — planning key `noodle_shop`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/noodle_shop/entrance.png` |
| Dining room | interior | Reuse candidate | [noodle_shop.png](../assets/ui/locations/noodle_shop.png) |
| Service counter view | interior | New | `assets/ui/locations/interiors/noodle_shop/service_counter_view.png` |
| Kitchen | interior | New | `assets/ui/locations/interiors/noodle_shop/kitchen.png` |
| Staff office store | interior | New | `assets/ui/locations/interiors/noodle_shop/staff_office_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/noodle_shop/restroom.png` |

### marios-pizza

**Mario's Pizza** — planning key `marios_pizza`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/marios_pizza/entrance.png` |
| Dining counter room | interior | Reuse candidate | [marios_pizza.png](../assets/ui/locations/marios_pizza.png) |
| Staff kitchen store | interior | New | `assets/ui/locations/interiors/marios_pizza/staff_kitchen_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/marios_pizza/restroom.png` |

### chess

**Chess café** — planning key `chess`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/chess/entrance.png` |
| Café room | interior | New | `assets/ui/locations/interiors/chess/caf_room.png` |
| Playing room | interior | Reuse candidate | [chess.png](../assets/ui/locations/chess.png) |
| Lesson alcove view | interior | New | `assets/ui/locations/interiors/chess/lesson_alcove_view.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/chess/restroom.png` |

### flowers

**Petal & Stem** — planning key `flowers`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/flowers/entrance.png` |
| Shop floor | interior | Reuse candidate | [flowers.png](../assets/ui/locations/flowers.png) |
| Arrangement workroom | interior | New | `assets/ui/locations/interiors/flowers/arrangement_workroom.png` |
| Stockroom | interior | New | `assets/ui/locations/interiors/flowers/stockroom.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/flowers/restroom.png` |

### boutique

**Gift boutique** — planning key `boutique`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/boutique/entrance.png` |
| Display counter room | interior | Reuse candidate | [boutique.png](../assets/ui/locations/boutique.png) |
| Staff store | interior | New | `assets/ui/locations/interiors/boutique/staff_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/boutique/restroom.png` |

### shopping-mall

**Winterfield Galleria and JobSeek tenant** — planning key `shopping_mall`.

Existing shopping_mall.png is flat placeholder art. One JobSeek tenant is budgeted; additional named tenant units require additional rows if enabled.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Concourse | interior | New | `assets/ui/locations/interiors/shopping_mall/concourse.png` |
| Food seating view | interior | New | `assets/ui/locations/interiors/shopping_mall/food_seating_view.png` |
| Customer service room | interior | New | `assets/ui/locations/interiors/shopping_mall/customer_service_room.png` |
| JobSeek tenant shop floor | interior | New | `assets/ui/locations/interiors/shopping_mall/jobseek_tenant_shop_floor.png` |
| Tenant receiving room | interior | New | `assets/ui/locations/interiors/shopping_mall/tenant_receiving_room.png` |
| Tenant staff office | interior | New | `assets/ui/locations/interiors/shopping_mall/tenant_staff_office.png` |
| Tenant store | interior | New | `assets/ui/locations/interiors/shopping_mall/tenant_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/shopping_mall/restroom.png` |

### campus

**Winterfield University** — planning key `campus`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Main lobby | interior | New | `assets/ui/locations/interiors/campus/main_lobby.png` |
| Teaching corridor | interior | New | `assets/ui/locations/interiors/campus/teaching_corridor.png` |
| Lecture room | interior | New | `assets/ui/locations/interiors/campus/lecture_room.png` |
| Seminar room | interior | New | `assets/ui/locations/interiors/campus/seminar_room.png` |
| Study room | interior | New | `assets/ui/locations/interiors/campus/study_room.png` |
| Theatre workshop | interior | New | `assets/ui/locations/interiors/campus/theatre_workshop.png` |
| Rehearsal room | interior | New | `assets/ui/locations/interiors/campus/rehearsal_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/campus/restroom.png` |

### track

**University track pavilion** — planning key `track`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Pavilion lobby | interior | New | `assets/ui/locations/interiors/track/pavilion_lobby.png` |
| Changing room | interior | New | `assets/ui/locations/interiors/track/changing_room.png` |
| Coaching room | interior | New | `assets/ui/locations/interiors/track/coaching_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/track/restroom.png` |

### studio

**Downtown modelling and recording studio** — planning key `studio`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | New | `assets/ui/locations/interiors/studio/reception.png` |
| Corridor | interior | New | `assets/ui/locations/interiors/studio/corridor.png` |
| Photo studio | interior | Reuse candidate | [studio.png](../assets/ui/locations/studio.png) |
| Dressing fitting room | interior | New | `assets/ui/locations/interiors/studio/dressing_fitting_room.png` |
| Recording booth | interior | New | `assets/ui/locations/interiors/studio/recording_booth.png` |
| Choreography room | interior | New | `assets/ui/locations/interiors/studio/choreography_room.png` |
| Review room | interior | New | `assets/ui/locations/interiors/studio/review_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/studio/restroom.png` |

### arena

**Arena lounge and training** — planning key `arena`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/arena/entrance.png` |
| Lounge | interior | Reuse candidate | [arena.png](../assets/ui/locations/arena.png) |
| Training hall | interior | New | `assets/ui/locations/interiors/arena/training_hall.png` |
| Coach review room | interior | New | `assets/ui/locations/interiors/arena/coach_review_room.png` |
| Changing room | interior | New | `assets/ui/locations/interiors/arena/changing_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/arena/restroom.png` |

### boxing-club

**East Ward Boxing Club** — planning key `boxing_club`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/boxing_club/entrance.png` |
| Reception lounge | interior | New | `assets/ui/locations/interiors/boxing_club/reception_lounge.png` |
| Training hall | interior | Reuse candidate | [boxing_club.png](../assets/ui/locations/boxing_club.png) |
| Equipment room | interior | New | `assets/ui/locations/interiors/boxing_club/equipment_room.png` |
| Changing room | interior | New | `assets/ui/locations/interiors/boxing_club/changing_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/boxing_club/restroom.png` |

### iron-circle

**Iron Circle** — planning key `iron_circle`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Controlled entrance | interior | New | `assets/ui/locations/interiors/iron_circle/controlled_entrance.png` |
| Spectator lounge | interior | New | `assets/ui/locations/interiors/iron_circle/spectator_lounge.png` |
| Ring hall | interior | Reuse candidate | [iron_circle.png](../assets/ui/locations/iron_circle.png) |
| Fighter preparation room | interior | New | `assets/ui/locations/interiors/iron_circle/fighter_preparation_room.png` |
| Recovery room | interior | New | `assets/ui/locations/interiors/iron_circle/recovery_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/iron_circle/restroom.png` |

### library

**Public library** — planning key `library`.

Existing base image is simple flat placeholder art; replace with new finished room-specific artwork.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Lobby desk | interior | New | `assets/ui/locations/interiors/library/lobby_desk.png` |
| Reading room | interior | New | `assets/ui/locations/interiors/library/reading_room.png` |
| Stacks | interior | New | `assets/ui/locations/interiors/library/stacks.png` |
| Reservable study room | interior | New | `assets/ui/locations/interiors/library/reservable_study_room.png` |
| Staff catalogue office | interior | New | `assets/ui/locations/interiors/library/staff_catalogue_office.png` |
| Desk corridor | interior | New | `assets/ui/locations/interiors/library/desk_corridor.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/library/restroom.png` |

### archive

**Old town archive** — planning key `archive`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Public desk | interior | New | `assets/ui/locations/interiors/archive/public_desk.png` |
| Reading records room | interior | Reuse candidate | [archive.png](../assets/ui/locations/archive.png) |
| Conservation workshop | interior | New | `assets/ui/locations/interiors/archive/conservation_workshop.png` |
| Restricted storage | interior | New | `assets/ui/locations/interiors/archive/restricted_storage.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/archive/restroom.png` |

### makerspace

**Station makerspace** — planning key `makerspace`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Welcome room | interior | New | `assets/ui/locations/interiors/makerspace/welcome_room.png` |
| Shared workshop | interior | Reuse candidate | [makerspace.png](../assets/ui/locations/makerspace.png) |
| Electronics room | interior | New | `assets/ui/locations/interiors/makerspace/electronics_room.png` |
| Tool store | interior | New | `assets/ui/locations/interiors/makerspace/tool_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/makerspace/restroom.png` |

### cycle-shop

**Riverside cycle workshop** — planning key `cycle_shop`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Customer counter room | interior | Reuse candidate | [cycle_shop.png](../assets/ui/locations/cycle_shop.png) |
| Repair room | interior | New | `assets/ui/locations/interiors/cycle_shop/repair_room.png` |
| Parts store | interior | New | `assets/ui/locations/interiors/cycle_shop/parts_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/cycle_shop/restroom.png` |

### planetarium

**Hilltop planetarium** — planning key `planetarium`.

Existing artwork reads as the exhibit lobby/entrance to the dome, not the auditorium itself.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Lobby exhibits | interior | Reuse candidate | [planetarium.png](../assets/ui/locations/planetarium.png) |
| Dome theatre | interior | New | `assets/ui/locations/interiors/planetarium/dome_theatre.png` |
| Staff corridor | interior | New | `assets/ui/locations/interiors/planetarium/staff_corridor.png` |
| Preparation room | interior | New | `assets/ui/locations/interiors/planetarium/preparation_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/planetarium/restroom.png` |

### cinema

**Bijou cinema** — planning key `cinema`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Ticket foyer | interior | Reuse candidate | [cinema.png](../assets/ui/locations/cinema.png) |
| Auditorium | interior | New | `assets/ui/locations/interiors/cinema/auditorium.png` |
| Staff corridor | interior | New | `assets/ui/locations/interiors/cinema/staff_corridor.png` |
| Projection room | interior | New | `assets/ui/locations/interiors/cinema/projection_room.png` |
| Staff office | interior | New | `assets/ui/locations/interiors/cinema/staff_office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/cinema/restroom.png` |

### sailing-club

**Municipal boathouse** — planning key `sailing_club`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [sailing_club.png](../assets/ui/locations/sailing_club.png) |
| Rigging workshop | interior | New | `assets/ui/locations/interiors/sailing_club/rigging_workshop.png` |
| Equipment store | interior | New | `assets/ui/locations/interiors/sailing_club/equipment_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/sailing_club/restroom.png` |
| Launch | outdoor | New | `assets/ui/locations/interiors/sailing_club/launch.png` |

### market

**Lantern community market** — planning key `market`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Community dining room | interior | New | `assets/ui/locations/interiors/market/community_dining_room.png` |
| Staff kitchen store | interior | New | `assets/ui/locations/interiors/market/staff_kitchen_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/market/restroom.png` |
| Public stalls | outdoor | Reuse candidate | [market.png](../assets/ui/locations/market.png) |

### bowling-alley

**Winterfield Lanes** — planning key `bowling_alley`.

Existing base image is simple flat placeholder art; replace with new finished room-specific artwork.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | New | `assets/ui/locations/interiors/bowling_alley/reception.png` |
| Lane hall | interior | New | `assets/ui/locations/interiors/bowling_alley/lane_hall.png` |
| Lounge | interior | New | `assets/ui/locations/interiors/bowling_alley/lounge.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/bowling_alley/restroom.png` |

### arcade

**Pixel Pier** — planning key `arcade`.

Existing base image is simple flat placeholder art; replace with new finished room-specific artwork.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Counter room | interior | New | `assets/ui/locations/interiors/arcade/counter_room.png` |
| Cabinet floor | interior | New | `assets/ui/locations/interiors/arcade/cabinet_floor.png` |
| Seating view | interior | New | `assets/ui/locations/interiors/arcade/seating_view.png` |
| Staff repair room | interior | New | `assets/ui/locations/interiors/arcade/staff_repair_room.png` |
| Staff office | interior | New | `assets/ui/locations/interiors/arcade/staff_office.png` |
| Service corridor | interior | New | `assets/ui/locations/interiors/arcade/service_corridor.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/arcade/restroom.png` |

### nightclub

**Afterglow** — planning key `nightclub`.

Existing base image is simple flat placeholder art; replace with new finished room-specific artwork.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/nightclub/entrance.png` |
| Dance hall | interior | New | `assets/ui/locations/interiors/nightclub/dance_hall.png` |
| Lounge | interior | New | `assets/ui/locations/interiors/nightclub/lounge.png` |
| Service room | interior | New | `assets/ui/locations/interiors/nightclub/service_room.png` |
| Staff corridor | interior | New | `assets/ui/locations/interiors/nightclub/staff_corridor.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/nightclub/restroom.png` |

### bar

**Copper Lantern** — planning key `bar`.

Existing base image is simple flat placeholder art; replace with new finished room-specific artwork.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/bar/entrance.png` |
| Bar seating room | interior | New | `assets/ui/locations/interiors/bar/bar_seating_room.png` |
| Service room | interior | New | `assets/ui/locations/interiors/bar/service_room.png` |
| Staff office | interior | New | `assets/ui/locations/interiors/bar/staff_office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/bar/restroom.png` |

### public-park-pavilion

**Commons gardener pavilion** — planning key `public_park_pavilion`.

Proposed support building for the existing gardener job; not an established runtime building ID.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Tool store | interior | New | `assets/ui/locations/interiors/public_park_pavilion/tool_store.png` |
| Supervisor office | interior | New | `assets/ui/locations/interiors/public_park_pavilion/supervisor_office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/public_park_pavilion/restroom.png` |

## Outdoor placeholder replacement

### beach

**Silver Sands beach** — planning key `beach`.

Replace assets/ui/locations/beach.png: current simple geometric placeholder. Keep the beach outdoors and preserve weather, travel and beach-outfit context. This is one additional image, not an interior room.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Shoreline beach scene | outdoor | New | `assets/ui/locations/interiors/beach/shoreline_beach_scene.png` |

## Outskirts

### hill-tea-room

**Hillside Tea Room** — planning key `hill_tea_room`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance counter view | interior | New | `assets/ui/locations/interiors/hill_tea_room/entrance_counter_view.png` |
| Tea room | interior | Reuse candidate | [hill_tea_room.png](../assets/ui/locations/hill_tea_room.png) |
| Staff kitchen | interior | New | `assets/ui/locations/interiors/hill_tea_room/staff_kitchen.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/hill_tea_room/restroom.png` |

### farm-shop

**Westbrook farm shop** — planning key `farm_shop`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/farm_shop/entrance.png` |
| Produce counter hall | interior | Reuse candidate | [farm_shop.png](../assets/ui/locations/farm_shop.png) |
| Staff store | interior | New | `assets/ui/locations/interiors/farm_shop/staff_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/farm_shop/restroom.png` |

### pottery-studio

**Old Mill pottery studio** — planning key `pottery_studio`.

Existing art contains worktables and ceramics equipment; allocate it to the workshop, not both display room and workshop.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance display room | interior | New | `assets/ui/locations/interiors/pottery_studio/entrance_display_room.png` |
| Pottery workshop | interior | Reuse candidate | [pottery_studio.png](../assets/ui/locations/pottery_studio.png) |
| Kiln room | interior | New | `assets/ui/locations/interiors/pottery_studio/kiln_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/pottery_studio/restroom.png` |

### marine-centre

**Marine discovery centre** — planning key `marine_centre`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Lobby | interior | New | `assets/ui/locations/interiors/marine_centre/lobby.png` |
| Exhibit hall | interior | Reuse candidate | [marine_centre.png](../assets/ui/locations/marine_centre.png) |
| Education room | interior | New | `assets/ui/locations/interiors/marine_centre/education_room.png` |
| Staff service room | interior | New | `assets/ui/locations/interiors/marine_centre/staff_service_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/marine_centre/restroom.png` |

### harbour-market

**South Harbour covered market** — planning key `harbour_market`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Vendor storage | interior | New | `assets/ui/locations/interiors/harbour_market/vendor_storage.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/harbour_market/restroom.png` |
| Sheltered entrance | outdoor | New | `assets/ui/locations/interiors/harbour_market/sheltered_entrance.png` |
| Stall aisles | outdoor | Reuse candidate | [harbour_market.png](../assets/ui/locations/harbour_market.png) |
| Public seating | outdoor | New | `assets/ui/locations/interiors/harbour_market/public_seating.png` |

### railway-museum

**Railway museum** — planning key `railway_museum`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Ticket lobby | interior | New | `assets/ui/locations/interiors/railway_museum/ticket_lobby.png` |
| Collection hall | interior | Reuse candidate | [railway_museum.png](../assets/ui/locations/railway_museum.png) |
| Archive education room | interior | New | `assets/ui/locations/interiors/railway_museum/archive_education_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/railway_museum/restroom.png` |

### southbank-diner

**Riverside diner** — planning key `southbank_diner`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/southbank_diner/entrance.png` |
| Dining counter room | interior | Reuse candidate | [southbank_diner.png](../assets/ui/locations/southbank_diner.png) |
| Staff kitchen | interior | New | `assets/ui/locations/interiors/southbank_diner/staff_kitchen.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/southbank_diner/restroom.png` |

## Headquarters

### syndicate-office

**Waterfront executive offices** — planning key `syndicate_office`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Public lobby | interior | New | `assets/ui/locations/interiors/syndicate_office/public_lobby.png` |
| Appointment room | interior | Reuse candidate | [syndicate_office.png](../assets/ui/locations/syndicate_office.png) |
| Guarded access passage | interior | New | `assets/ui/locations/interiors/syndicate_office/guarded_access_passage.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/syndicate_office/restroom.png` |

### syndicate-hq

**Syndicate underground HQ** — planning key `syndicate_hq`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Security foyer | interior | New | `assets/ui/locations/interiors/syndicate_hq/security_foyer.png` |
| Internal corridor | interior | New | `assets/ui/locations/interiors/syndicate_hq/internal_corridor.png` |
| Council chamber | interior | Reuse candidate | [syndicate_hq.png](../assets/ui/locations/syndicate_hq.png) |
| Executive meeting room | interior | New | `assets/ui/locations/interiors/syndicate_hq/executive_meeting_room.png` |
| Cross-branch operations room | interior | New | `assets/ui/locations/interiors/syndicate_hq/cross_branch_operations_room.png` |
| Members lounge | interior | New | `assets/ui/locations/interiors/syndicate_hq/members_lounge.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/syndicate_hq/restroom.png` |

### syndicate

**Red Dragons lounge** — planning key `syndicate`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/syndicate/entrance.png` |
| Members lounge | interior | Reuse candidate | [syndicate.png](../assets/ui/locations/syndicate.png) |
| Council meeting room | interior | New | `assets/ui/locations/interiors/syndicate/council_meeting_room.png` |
| Community liaison room | interior | New | `assets/ui/locations/interiors/syndicate/community_liaison_room.png` |
| Office | interior | New | `assets/ui/locations/interiors/syndicate/office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/syndicate/restroom.png` |

### site-01

**Kestrel Operations Centre** — planning key `site_01`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [site_01_reception.png](../assets/ui/locations/site_01_reception.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/site_01/secure_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_01_briefing.png](../assets/ui/locations/site_01_briefing.png) |
| Operations office | interior | New | `assets/ui/locations/interiors/site_01/operations_office.png` |
| Guarded service room | interior | New | `assets/ui/locations/interiors/site_01/guarded_service_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_01/restroom.png` |

### site-02

**Pacific Relay Depot** — planning key `site_02`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [site_02_reception.png](../assets/ui/locations/site_02_reception.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/site_02/secure_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_02_briefing.png](../assets/ui/locations/site_02_briefing.png) |
| Dispatch room | interior | New | `assets/ui/locations/interiors/site_02/dispatch_room.png` |
| Warehouse | interior | New | `assets/ui/locations/interiors/site_02/warehouse.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_02/restroom.png` |

### site-03

**Stillwater Research Annex** — planning key `site_03`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [site_03_reception.png](../assets/ui/locations/site_03_reception.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/site_03/secure_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_03_briefing.png](../assets/ui/locations/site_03_briefing.png) |
| Research office | interior | New | `assets/ui/locations/interiors/site_03/research_office.png` |
| Restricted laboratory | interior | New | `assets/ui/locations/interiors/site_03/restricted_laboratory.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_03/restroom.png` |

### site-04

**Breakwater Security Depot** — planning key `site_04`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [site_04_reception.png](../assets/ui/locations/site_04_reception.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/site_04/secure_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_04_briefing.png](../assets/ui/locations/site_04_briefing.png) |
| Equipment room | interior | New | `assets/ui/locations/interiors/site_04/equipment_room.png` |
| Maintenance bay | interior | New | `assets/ui/locations/interiors/site_04/maintenance_bay.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_04/restroom.png` |

### site-05

**Aster Media House** — planning key `site_05`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [site_05_reception.png](../assets/ui/locations/site_05_reception.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/site_05/secure_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_05_briefing.png](../assets/ui/locations/site_05_briefing.png) |
| Production room | interior | New | `assets/ui/locations/interiors/site_05/production_room.png` |
| Editing room | interior | New | `assets/ui/locations/interiors/site_05/editing_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_05/restroom.png` |

### site-06

**Meridian Capital Offices** — planning key `site_06`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [site_06_reception.png](../assets/ui/locations/site_06_reception.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/site_06/secure_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_06_briefing.png](../assets/ui/locations/site_06_briefing.png) |
| Accounts office | interior | New | `assets/ui/locations/interiors/site_06/accounts_office.png` |
| Restricted records room | interior | New | `assets/ui/locations/interiors/site_06/restricted_records_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_06/restroom.png` |

### site-07

**Oculus Winterfield Campus** — planning key `site_07`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception public displays | interior | Reuse candidate | [site_07_reception.png](../assets/ui/locations/site_07_reception.png) |
| Controlled corridor | interior | New | `assets/ui/locations/interiors/site_07/controlled_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_07_briefing.png](../assets/ui/locations/site_07_briefing.png) |
| Corporate office | interior | New | `assets/ui/locations/interiors/site_07/corporate_office.png` |
| Data wing | interior | New | `assets/ui/locations/interiors/site_07/data_wing.png` |
| Security room | interior | New | `assets/ui/locations/interiors/site_07/security_room.png` |
| Public-service supervisor room | interior | New | `assets/ui/locations/interiors/site_07/public_service_supervisor_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_07/restroom.png` |

### site-08

**Greyglass Service House** — planning key `site_08`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | Reuse candidate | [site_08_reception.png](../assets/ui/locations/site_08_reception.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/site_08/secure_corridor.png` |
| Briefing room | interior | Reuse candidate | [site_08_briefing.png](../assets/ui/locations/site_08_briefing.png) |
| Equipment workshop | interior | New | `assets/ui/locations/interiors/site_08/equipment_workshop.png` |
| Restricted store | interior | New | `assets/ui/locations/interiors/site_08/restricted_store.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/site_08/restroom.png` |

### glasshouse-lab

**Glasshouse** — planning key `glasshouse_lab`.

Private review/reunion room is one reservable room used at different times; no simultaneous incompatible private scenes.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Cleared entrance | interior | New | `assets/ui/locations/interiors/glasshouse_lab/cleared_entrance.png` |
| Internal corridor | interior | New | `assets/ui/locations/interiors/glasshouse_lab/internal_corridor.png` |
| Laboratory workroom | interior | Reuse candidate | [glasshouse_lab.png](../assets/ui/locations/glasshouse_lab.png) |
| Private review reunion room | interior | New | `assets/ui/locations/interiors/glasshouse_lab/private_review_reunion_room.png` |
| Records room | interior | New | `assets/ui/locations/interiors/glasshouse_lab/records_room.png` |
| Rest room | interior | New | `assets/ui/locations/interiors/glasshouse_lab/rest_room.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/glasshouse_lab/restroom.png` |

### interpol-hq

**Interpol Regional HQ** — planning key `interpol_hq`.

Containment wing is one initial scene. If subdivided into interview rooms or cells, each new navigable room needs another image.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Public lobby verification desk | interior | Reuse candidate | [interpol_hq.png](../assets/ui/locations/interpol_hq.png) |
| Secure corridor | interior | New | `assets/ui/locations/interiors/interpol_hq/secure_corridor.png` |
| Awakened Operations briefing room | interior | Reuse candidate | [interpol_briefing.png](../assets/ui/locations/interpol_briefing.png) |
| Controlled training hall | interior | Reuse candidate | [interpol_training.png](../assets/ui/locations/interpol_training.png) |
| Interview containment wing | interior | Reuse candidate | [interpol_containment.png](../assets/ui/locations/interpol_containment.png) |
| Case office | interior | New | `assets/ui/locations/interiors/interpol_hq/case_office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/interpol_hq/restroom.png` |

### blackstone-hq

**Blackstone Headquarters** — planning key `blackstone_hq`.

Loading compound is an existing exterior view, not an indoor room. Keep its authored campaign location outdoors.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception security | interior | Reuse candidate | [blackstone_hq.png](../assets/ui/locations/blackstone_hq.png) |
| Controlled corridor | interior | New | `assets/ui/locations/interiors/blackstone_hq/controlled_corridor.png` |
| Research records | interior | Reuse candidate | [blackstone_records.png](../assets/ui/locations/blackstone_records.png) |
| Experimental wing | interior | Reuse candidate | [blackstone_lab.png](../assets/ui/locations/blackstone_lab.png) |
| Executive command | interior | Reuse candidate | [blackstone_command.png](../assets/ui/locations/blackstone_command.png) |
| Restroom | interior | New | `assets/ui/locations/interiors/blackstone_hq/restroom.png` |
| Loading compound | outdoor | Reuse candidate | [blackstone_loading.png](../assets/ui/locations/blackstone_loading.png) |

## Smaller factions

### lantern-house

**Lantern House** — planning key `lantern_house`.

Leader-residence subdivision is a proposed production layout, not established detailed canon; review before generation.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/lantern_house/entrance.png` |
| Waiting room | interior | New | `assets/ui/locations/interiors/lantern_house/waiting_room.png` |
| Meeting room | interior | Reuse candidate | [lantern_house.png](../assets/ui/locations/lantern_house.png) |
| Office | interior | New | `assets/ui/locations/interiors/lantern_house/office.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/lantern_house/stairway.png` |
| Private flat living repair room | interior | New | `assets/ui/locations/interiors/lantern_house/private_flat_living_repair_room.png` |
| Private bedroom | interior | New | `assets/ui/locations/interiors/lantern_house/private_bedroom.png` |
| Private bathroom | interior | New | `assets/ui/locations/interiors/lantern_house/private_bathroom.png` |
| Visitor restroom | interior | New | `assets/ui/locations/interiors/lantern_house/visitor_restroom.png` |

### saints-depot

**Saints Rail Depot** — planning key `saints_depot`.

Leader-residence subdivision is a proposed production layout, not established detailed canon; review before generation.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/saints_depot/entrance.png` |
| Waiting room | interior | New | `assets/ui/locations/interiors/saints_depot/waiting_room.png` |
| Meeting room | interior | Reuse candidate | [saints_depot.png](../assets/ui/locations/saints_depot.png) |
| Dispatch workshop | interior | New | `assets/ui/locations/interiors/saints_depot/dispatch_workshop.png` |
| Private converted office living sleeping room | interior | New | `assets/ui/locations/interiors/saints_depot/private_converted_office_living_sleeping_room.png` |
| Private bathroom | interior | New | `assets/ui/locations/interiors/saints_depot/private_bathroom.png` |
| Visitor restroom | interior | New | `assets/ui/locations/interiors/saints_depot/visitor_restroom.png` |

### purple-clubhouse

**Purple Skulls clubhouse** — planning key `purple_clubhouse`.

Leader-residence subdivision is a proposed production layout, not established detailed canon; review before generation.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/purple_clubhouse/entrance.png` |
| Waiting room | interior | New | `assets/ui/locations/interiors/purple_clubhouse/waiting_room.png` |
| Meeting room | interior | Reuse candidate | [purple_clubhouse.png](../assets/ui/locations/purple_clubhouse.png) |
| Members lounge | interior | New | `assets/ui/locations/interiors/purple_clubhouse/members_lounge.png` |
| Garage | interior | New | `assets/ui/locations/interiors/purple_clubhouse/garage.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/purple_clubhouse/stairway.png` |
| Private residence living room | interior | New | `assets/ui/locations/interiors/purple_clubhouse/private_residence_living_room.png` |
| Private bedroom | interior | New | `assets/ui/locations/interiors/purple_clubhouse/private_bedroom.png` |
| Private bathroom | interior | New | `assets/ui/locations/interiors/purple_clubhouse/private_bathroom.png` |
| Visitor restroom | interior | New | `assets/ui/locations/interiors/purple_clubhouse/visitor_restroom.png` |

### hamayashi-house

**Kurose House** — planning key `hamayashi_house`.

Leader-residence subdivision is a proposed production layout, not established detailed canon; review before generation.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/hamayashi_house/entrance.png` |
| Reception waiting hall | interior | New | `assets/ui/locations/interiors/hamayashi_house/reception_waiting_hall.png` |
| Meeting room | interior | Reuse candidate | [hamayashi_house.png](../assets/ui/locations/hamayashi_house.png) |
| Records room | interior | New | `assets/ui/locations/interiors/hamayashi_house/records_room.png` |
| Rear residence living room | interior | New | `assets/ui/locations/interiors/hamayashi_house/rear_residence_living_room.png` |
| Private bedroom | interior | New | `assets/ui/locations/interiors/hamayashi_house/private_bedroom.png` |
| Private bathroom | interior | New | `assets/ui/locations/interiors/hamayashi_house/private_bathroom.png` |
| Visitor restroom | interior | New | `assets/ui/locations/interiors/hamayashi_house/visitor_restroom.png` |
| Bonsai courtyard | outdoor | New | `assets/ui/locations/interiors/hamayashi_house/bonsai_courtyard.png` |

### rojos-courtyard

**Los Rojos base** — planning key `rojos_courtyard`.

Despite its filename, the current picture depicts a covered indoor meeting setting; use for meeting room, not the separate open courtyard. Leader-residence subdivision is a proposed production layout, not established detailed canon; review before generation.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/rojos_courtyard/entrance.png` |
| Waiting room | interior | New | `assets/ui/locations/interiors/rojos_courtyard/waiting_room.png` |
| Meeting room | interior | Reuse candidate | [rojos_courtyard.png](../assets/ui/locations/rojos_courtyard.png) |
| Office | interior | New | `assets/ui/locations/interiors/rojos_courtyard/office.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/rojos_courtyard/stairway.png` |
| Upstairs living guitar room | interior | New | `assets/ui/locations/interiors/rojos_courtyard/upstairs_living_guitar_room.png` |
| Private bedroom | interior | New | `assets/ui/locations/interiors/rojos_courtyard/private_bedroom.png` |
| Private bathroom | interior | New | `assets/ui/locations/interiors/rojos_courtyard/private_bathroom.png` |
| Visitor restroom | interior | New | `assets/ui/locations/interiors/rojos_courtyard/visitor_restroom.png` |
| Courtyard | outdoor | New | `assets/ui/locations/interiors/rojos_courtyard/courtyard.png` |

### consortium-house

**Waterfront Consortium House** — planning key `consortium_house`.

Leader-residence subdivision is a proposed production layout, not established detailed canon; review before generation.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/consortium_house/entrance.png` |
| Waiting room | interior | New | `assets/ui/locations/interiors/consortium_house/waiting_room.png` |
| Boardroom | interior | Reuse candidate | [consortium_house.png](../assets/ui/locations/consortium_house.png) |
| Office | interior | New | `assets/ui/locations/interiors/consortium_house/office.png` |
| Stairway | interior | New | `assets/ui/locations/interiors/consortium_house/stairway.png` |
| Upper apartment living chart room | interior | New | `assets/ui/locations/interiors/consortium_house/upper_apartment_living_chart_room.png` |
| Private bedroom | interior | New | `assets/ui/locations/interiors/consortium_house/private_bedroom.png` |
| Private bathroom | interior | New | `assets/ui/locations/interiors/consortium_house/private_bathroom.png` |
| Visitor restroom | interior | New | `assets/ui/locations/interiors/consortium_house/visitor_restroom.png` |

### hamayashi-annex

**Hamayashi riverside annex** — planning key `hamayashi_annex`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/hamayashi_annex/entrance.png` |
| Meeting office room | interior | Reuse candidate | [hamayashi_annex.png](../assets/ui/locations/hamayashi_annex.png) |
| Restroom | interior | New | `assets/ui/locations/interiors/hamayashi_annex/restroom.png` |

### hamayashi-store

**Hamayashi supply house** — planning key `hamayashi_store`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entrance | interior | New | `assets/ui/locations/interiors/hamayashi_store/entrance.png` |
| Stock hall | interior | Reuse candidate | [hamayashi_store.png](../assets/ui/locations/hamayashi_store.png) |
| Office | interior | New | `assets/ui/locations/interiors/hamayashi_store/office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/hamayashi_store/restroom.png` |

## Owned properties

### crew-lot-west

**West workshop** — planning key `crew_lot_west`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entry | interior | New | `assets/ui/locations/interiors/crew_lot_west/entry.png` |
| Workshop | interior | New | `assets/ui/locations/interiors/crew_lot_west/workshop.png` |
| Office | interior | New | `assets/ui/locations/interiors/crew_lot_west/office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/crew_lot_west/restroom.png` |

### crew-lot-docks

**Dock warehouse** — planning key `crew_lot_docks`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entry | interior | New | `assets/ui/locations/interiors/crew_lot_docks/entry.png` |
| Warehouse | interior | New | `assets/ui/locations/interiors/crew_lot_docks/warehouse.png` |
| Meeting office | interior | New | `assets/ui/locations/interiors/crew_lot_docks/meeting_office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/crew_lot_docks/restroom.png` |

### crew-lot-north

**Northern offices** — planning key `crew_lot_north`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Reception | interior | New | `assets/ui/locations/interiors/crew_lot_north/reception.png` |
| Meeting room | interior | New | `assets/ui/locations/interiors/crew_lot_north/meeting_room.png` |
| Workroom | interior | New | `assets/ui/locations/interiors/crew_lot_north/workroom.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/crew_lot_north/restroom.png` |

### crew-lot-south

**South garage** — planning key `crew_lot_south`.

| Room / image view | Type | Art action | Existing image or proposed new target |
| --- | --- | --- | --- |
| Entry | interior | New | `assets/ui/locations/interiors/crew_lot_south/entry.png` |
| Garage | interior | New | `assets/ui/locations/interiors/crew_lot_south/garage.png` |
| Office | interior | New | `assets/ui/locations/interiors/crew_lot_south/office.png` |
| Restroom | interior | New | `assets/ui/locations/interiors/crew_lot_south/restroom.png` |

## Existing art not allocated to an interior

| Existing asset group | Decision |
| --- | --- |
| `site_01.png`–`site_08.png` | Keep as exterior frontages; do not count as room images. |
| `site_01_interior.png`–`site_08_interior.png` | Older reception-like alternates. Do not allocate to secure corridors or additional rooms just to reduce new-art count. Newer dedicated reception/briefing files are selected. |
| `crew_lot_*.png` | Keep as exteriors; all property interiors require new artwork. |
| `ivan_home.png` | Legacy home art; current shared home is `valentina_home`. Do not invent a room to reuse it. |
| `arcade.png`, `bar.png`, `bowling_alley.png`, `library.png`, `nightclub.png`, `shopping_mall.png` | Existing flat placeholder artwork; replacement required for finished interiors. |
| `campus-day.png`, `track.png`, `fox_hideout.png`, `gordon_apartments.png` | Exterior/arrival views. New campus/pavilion interiors are separate. Fox/Gordon residence interiors use their actual home files. |
| `beach.png` | Simple outdoor placeholder: replacement is required and budgeted in the Silver Sands entry. |
| Parks, wetlands, downtown, Blackhaven, trails, orchard, pier, lookout, lighthouse walk | Existing illustrated outdoor destinations; retain unless a later audit identifies a placeholder or incompatible view. Outdoor placeholder replacement is in scope, but these images are not all automatically regenerated. |
| `garrett-hong-kong-school.png`, `rei-high-school.png` | Existing historical exterior views. Preserve for supported flashbacks; not present-day university rooms. |
| `transit.png`, `motorcycle.png`, phone wallpapers, UI frames and portrait/gallery art | Not reusable as empty architectural room backgrounds. |

## Placeholder replacement requirements

The update must replace simple placeholder location art wherever used, including outdoor destinations. The current visual audit identifies seven active files: `arcade.png`, `bar.png`, `bowling_alley.png`, `library.png`, `nightclub.png`, `shopping_mall.png` and `beach.png`. The six interior replacements are already covered by New rows for cabinet floor, bar/seating room, lane hall, reading room, dance hall and mall concourse respectively; do not count them twice. Silver Sands adds one outdoor image.

Each replacement must be a finished, distinct architectural/environment illustration consistent with the existing game artwork, with clear space for live character overlays. Preserve original venue IDs, activity access, fees, schedules and indoor/outdoor weather behaviour. Update the actual scene lookup and any Maps/arrival/preview consumers so the old placeholder cannot remain visible through an alternate path.

Audit every enabled location/view, including missing-file fallbacks, before release. Any further simple placeholder must be added as an explicit replacement row. Archived placeholders, such as the old public-park file, are not active replacement work unless still referenced. Existing finished public-park artwork should be retained.

Inspect `tools/build_venue_art.py` before production: its bulk primitive renderer can overwrite venue PNGs, including finished assets. Add overwrite protection or retire that production path when implementing the update; do not run it to create the new art. Verify all seven replacements at full size and in actual rendered scenes, and record source/prompt provenance. No replacement has been generated or installed by this planning change.

## Campaign, meeting and wardrobe coverage

- Council uses Syndicate council chamber; diplomacy uses assigned meeting/boardrooms; JobSeek uses the listed staff areas and named tenant. No extra image is needed per event when events occupy the same physical room at different times.
- Glasshouse review/reunion, archive records, Kurose testimony/records, Blackstone records/lab/command and Interpol briefing/training/containment all have dedicated rows. Garrett's home dining and noodle-shop aftermath have dedicated views. Subsequent indoor campaign stages must resolve to these rows or add an explicit new row before being enabled.
- Reviewed Charles search/extended Garrett chapters and repeatable post-story destinations: Blackhaven, public market and waterfront outdoor handovers remain outdoor where authored. Do not build a fictitious indoor market room solely for a combat objective.
- Fixed-domain characters do not receive invented private houses: Crow uses HQ, Takeo/Thirteen existing briefing rooms, Charles Glasshouse rest/review/work rooms.
- Newer campaigns and historical scenes still require the integration plan's exhaustive stage-to-room audit. This is a release gate, not a hidden unbudgeted assumption: an unmapped indoor stage cannot ship until added here. Unspecified Bubblegram district venues stay blocked for indoor production until an actual building is selected; outdoor contracts stay outside.
- Beach/gym/formal/home outfit switching reuses scene images; it adds wardrobe assets only if separately requested. Listed dressing/changing rooms already cover the architectural requirement. No per-outfit or per-character background variants.

## Audit and maintenance

- Visually reviewed contact sheets 01–06 covering all current location PNGs plus café/campus art. Sheets 07–08 contain remaining UI/wallpaper assets and are not location-reuse evidence.
- Checked selected asset existence, dimensions, hashes, unique IDs and one-to-one reuse assignment when generating this inventory. No new art, runtime integration or in-game render test was performed.
- Contact-sheet matches are provisional production reuse recommendations. Inspect full-size candidates before final installation; reject unwanted baked-in signage, incompatible room geometry, bad crop or missing foreground space.
- Source data and reproducible renderer: `tools/build_interiors_art_inventory.py`. Machine-readable companion: [INTERIORS_IMAGE_INVENTORY.json](INTERIORS_IMAGE_INVENTORY.json). Contact sheets: [audit directory](interiors-art-audit/).
- Proposed new paths are reserved planning targets, not existing files. Do not generate art for unresolved layouts. Preserve stable row IDs when modifying the plan; add newly navigable spaces rather than hiding them under an existing room.
