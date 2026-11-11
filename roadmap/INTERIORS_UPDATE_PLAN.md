# MH-004 — Lived-In Interiors

**Status:** In progress — 89 images across batches 01 and 02 generated and statically reviewed 2026-11-11; runtime implementation pending.  
**Sequence:** 1 — before MH-016, the four Ace campaigns and Sylvanis; confirmed 2026-11-11 in the [approved roadmap order](../ROADMAP.md#approved-update-order--2026-11-11).  
**Added:** 2026-11-10  
**Roadmap:** [MH-004](../ROADMAP.md#mh-004-lived-in-interiors-room-by-room-exploration)

**Integrated design review:** [Shared contracts, resolved gaps and end-to-end acceptance](INTERIORS_INTEGRATION_REVIEW.md) (2026-11-11). Read this with the residential and public/faction layouts. It resolves earlier tentative rules for location state, movement, schedules, work access, guards and migration; runtime verification is still pending.

**Room/image production inventory:** [Building-by-building image list and reuse audit](INTERIORS_IMAGE_INVENTORY.md), with [machine-readable rows](INTERIORS_IMAGE_INVENTORY.json). The current baseline enumerates 508 interior room/views across 90 building/group entries: 87 reuse candidates and 421 new images, plus 20 outdoor views and two conditional dorm bathrooms. The outdoor count includes the required Silver Sands placeholder replacement. Reuse candidates were inspected in contact sheets; final full-size/in-game approval remains pending. The inventory explicitly resolves service rooms, stairs, navigable zones and bounded gang-residence subdivisions for planning.

## Plugin task assignments

**Assigned:** 2026-11-11. Interiors remains first in the approved sequence. Batches 01 and 02 art are ready; runtime rooms and the remaining release gates are pending.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Residential room layouts, routines and room-aware conversation briefs | Story Skills + Writer's Loop | Check household identity, schedules, privacy and character-specific room activities; revise descriptions against the integration review without promoting proposed layouts into canon. |
| Dedicated room-image coverage and wardrobe cutout preparation | Bulk BG Remove only for portrait/prop layers; prompt-to-asset only for required local icons/exports | Keep each room background opaque and unique. Preserve accepted art and source references; review any cutout edges and wardrobe identity. These plugins do not generate the required room paintings. |
| Penthouse, workplace/event and secure-faction pilots | falsegreen-skill | Review tests for real co-presence, access, companions, zero-additional-minute adjacent movement, schedule precedence and local guards; run the relevant suites and inspect all three in-person pilots. |
| Automatic outfits, event destinations and legacy-save migration | falsegreen-skill + Story Skills for appearance/knowledge contracts | Assert visit overrides, departure restoration, missing-outfit fallback, idempotent room migration and preserved campaign clearance. Verify phone handoffs with dark-theme and feature smokes when touched. |
| Optional later room/door ambience request | Pro Motion for synthetic cues; SFXMint for suitable explicitly free library effects | Conditional; no ambience redesign is included. Keep accepted sounds local, record SOUNDS.md provenance and verify mute/volume and in-context playback. |

Batch 02 artwork and brief-review execution is recorded separately in its [production review](interiors-generation-batches/interiors-02-production/PRODUCTION_REVIEW.md). Evidence for the runtime assignments above remains pending. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Purpose and scope

**Artwork production evidence (2026-11-11):** [Batch 01 production review](interiors-generation-batches/interiors-01-production/PRODUCTION_REVIEW.md) and [gallery](interiors-generation-batches/interiors-01-production/gallery.html) cover the 48 accepted new images. Original assets and saves are unchanged. Runtime integration, in-person rendered verification and final reuse approval remain pending. Full-size review rejected Garrett’s existing exterior image as an indoor living-room reuse candidate; its replacement requires an explicit inventory/batch revision, outside these 48 assigned new images.

**Batch 02 artwork evidence (2026-11-11):** Artwork is complete. The [production review](interiors-generation-batches/interiors-02-production/PRODUCTION_REVIEW.md) and [gallery](interiors-generation-batches/interiors-02-production/gallery.html) cover 41 accepted images with static coverage, provenance, dimensions, opacity, distinctness, unchanged original-reference hashes and overwrite checks. Lena's and Naomi's original living-room art shows open sleeping areas; reconcile its reuse with planned private bedrooms before runtime room/privacy implementation.

**Batch 03 unfinished and paused (2026-11-11):** Four Rosa views generated before the pause: entrance accepted and installed, three other views retained as staged drafts, 47 remaining views not started. [Partial production record](interiors-generation-batches/interiors-03-production/PRODUCTION_REVIEW.md). Rosa's existing dining reference depicts an outdoor terrace, so its indoor reuse needs reconciliation before integration. No runtime changes or release.

Buildings become connected rooms, explored in the in-person window. Characters spend time in particular rooms according to their routines instead of being treated as present everywhere within a building. The user's example is Yuriko relaxing in her bedroom or the living space in Rei's penthouse.

The user originally requested a proposed interiors plan and confirmed it as the first queued update on 2026-11-11. Room exploration and room-specific character presence are the requested core. Unresolved design details below remain proposals for scope agreement; recording the order does not start implementation. No delivery date or release version is assigned.

## Existing foundations

- `world_loop.py` assigns homes and daily routines. Yuriko shares Rei's penthouse and currently returns there for dinner and model building.
- The penthouse description includes a library, paintings, Yuriko's scale models, a dedicated art space and an intimate kitchen.
- `crime_operations.py` already defines reception and briefing rooms with site-specific access checks, including companion checks.
- `town.py` provides location and interaction integration that must remain compatible.

These observations come from source inspection during the proposal conversation. They do not establish that a general room system already exists.

## In-person exploration

Travelling to a building brings the player to its entrance or established arrival area. The in-person window shows the building and current room, room-specific artwork and description, physically present characters, connected doors and relevant activities.

A compact navigation panel offers adjacent rooms. Movement follows authored connections rather than allowing arbitrary jumps to any room. The living space might connect to the kitchen and hallway, with bedrooms opening onto that hallway. A movement minigame is not required.

The phone retains building travel and messaging. Room navigation, knocking, exploration and physical activities stay in the in-person window. Any affected phone surfaces must reuse the existing dark styles and embedded phone dialogs, including interactive and popup states.

## Proposed penthouse pilot

These divisions are proposed additions based on the existing home description, not newly established character canon.

| Room | Typical use |
| --- | --- |
| Entrance | Arrivals, greeting visitors and leaving |
| Living space | Relaxing, conversation and spending time together |
| Kitchen and dining area | Cooking, meals and clearing up |
| Library | Reading, studying and quiet conversation |
| Art space | Rei painting; Yuriko building scale models when appropriate |
| Hallway | Connecting shared spaces and bedrooms |
| Rei's bedroom | Sleeping, resting and personal downtime |
| Yuriko's bedroom | Sleeping, studying, model-making and relaxing privately |

Example: the player arrives in an empty living space while Yuriko is relaxing in her bedroom. The player walks to the hallway and knocks. Yuriko can invite them in, come out or explain that she is busy. Later she independently moves to the living space and becomes available there.

## Room routines

Track both the character's building and their room. Existing schedules choose the building; a second layer chooses an appropriate room and activity within it.

| Yuriko's context | Proposed room and activity |
| --- | --- |
| Returning from university | Kitchen for a snack, then bedroom to unwind |
| Evening project work | Art space for model building or bedroom for studying |
| Shared dinner | Kitchen and dining area |
| Free evening | Living space relaxing or library reading |
| Night | Her bedroom, sleeping |

Use weighted preferences and variation without moving characters on every screen refresh. Give activities meaningful dwell time. Active conversations, accepted invitations and important scenes take precedence over ordinary room changes. Preserve weekday/work/sleep commitments and existing outdoor travel routines.

## Expanded home layouts and routines — proposed 2026-11-11

The user requested layouts and character routines for the other homes. This section expands the proposed design; it does not commit new architecture or routines to runtime canon. Existing descriptions, household relationships and schedule anchors come from `world_loop.py`, `hidden_cast.py`, `four_aces.py`, `interpol_cast.py` and `vacant_homes.py`; new room divisions and within-home activities are proposals.

### Layout conventions

`A ↔ B` means a traversable connection in both directions. Braces list separate branches from the preceding room. An exterior entrance always leads back to the existing building destination. Bedrooms, bathrooms and private workrooms have their own access rules; a route through a shared hall does not grant entry. Each enclosed home includes a bathroom reached from its hall or main room unless specified otherwise; occupied bathrooms are unavailable for social interaction.

Open-plan corners are activity zones in the same physical room, not soundproof rooms. Moving between the sofa and desk in a studio does not hide a conversation from someone sitting nearby. Loft sleeping areas without an actual door use availability/privacy boundaries, not a fictional locked door. Outdoor balconies, gardens, decks and roofs remain in-person areas and respect weather; routines choose an indoor fallback.

The following graphs are the proposed explorable layouts. Rooms not listed are not implied to exist. Access to home workshops does not grant access to the resident's workplace or private records.

### Core cast residences

| Home / existing location | Proposed connected layout | Character room preferences while home |
| --- | --- | --- |
| Emily's garden apartment (`emily_home`) | Entrance ↔ living room ↔ {kitchen, LEGO workroom, flower balcony, hall}; hall ↔ {bedroom, bathroom}. | After returning around 19:00: kitchen for tea/food, LEGO workroom for a build, then living room with plushies or bedroom to unwind. On a free home morning, tend balcony flowers when weather permits. Sleep in bedroom. |
| Sophie's trackside loft (`sophie_home`) | Entrance ↔ open living/kitchen space ↔ {stretching area, balcony, stairs}; stairs ↔ sleeping loft. Bathroom opens off the entrance. Stretching area is an open zone. | Around 21:00 recovery: stretching area, kitchen for recovery food, sofa for downtime, then sleeping loft. Home mornings can include meal preparation before leaving; do not replace her 07:00 track session or add exhausting late training. |
| Amy's student dorm (`amy_home`) | Corridor door ↔ single dorm room with easel, study desk, armchairs and sleeping zone; room ↔ private bathroom proposed for layout review. | Around 20:00: easel for painting, desk for reading/philosophy notes, armchair to relax, then bed. Drying paintings and reading can share the room. Dorm bathroom arrangement is unresolved and must be checked before artwork. |
| Minsu's student dorm (`minsu_home`) | Corridor door ↔ single dorm room with study desk, sitting area, kit storage and sleeping zone; room ↔ bathroom subject to the same dorm-layout review. | Around 19:00: desk for medical study, sitting area for a snack/downtime, kit corner to prepare for the next day, then bed. Taekwondo practice remains at the existing training location; the small room does not become a dojo. |
| Samantha's garage flat (`samantha_home`) | Street entrance ↔ garage/workbench ↔ stairs ↔ living/kitchen space ↔ {bedroom, bathroom}; heavy-bag zone branches within the garage. | Around 23:00: secure bike/equipment in garage, kitchen for a drink or food, living space to unwind, then bed. Maintenance and heavy-bag practice are free-time choices, not mandatory after every fight. Workshop access is separate from bedroom permission. |
| April's observatory townhouse (`april_home`) | Entrance ↔ sitting/chess room ↔ {kitchen, hall}; hall ↔ {study/lab desk room, bathroom, stairs}; stairs ↔ upper landing ↔ {bedroom, roof access}; roof access ↔ telescope terrace. | Around 18:00: study/lab desk for science projects, kitchen for dinner, chess room for a puzzle. Around 22:00: telescope terrace in suitable weather; study for sky charts/books otherwise. Bedroom for sleep. Scientific props do not introduce unapproved experiments or powers. |
| Garrett's hillside estate (`garrett_home`) | Foyer ↔ {living room, dining room, stairs, garage passage}; dining room ↔ noodle kitchen; living room ↔ terrace; garage passage ↔ garage; stairs ↔ landing ↔ {Garrett's bedroom, bathroom}. | Around 18:00: noodle kitchen then dining room; preserve the 20:00 Red Dragons appointment. Around 23:00: living room or terrace before bed. Free home periods allow cooking and time in the garage. No invented resident staff, relatives or guest occupants. |

Amy and Minsu remain one dorm apart, not roommates. Their home graphs connect only through the building's public corridor, with separate entry permission. Visiting one does not reveal the other's presence or grant entry. The dorm corridor should not create an automatic encounter with either character.

### Shared households

| Home / existing location | Proposed connected layout | Independent and shared routines |
| --- | --- | --- |
| Yeuns' Ferry Signal House (`valentina_home`; Ivan and Valentina) | Entrance ↔ harbour living room ↔ {kitchen/dining room, piano alcove, sail workroom, mezzanine stairs}; stairs ↔ reading mezzanine ↔ {Ivan's bedroom, Valentina's bedroom, bathroom}. Piano alcove remains part of the living room for presence. | Ivan returns around 18:00 for dinner and existing martial-arts practice in a cleared living-space zone; preserve his 20:00 HQ departure. Around 23:00 he writes songs at the piano or reads quietly. Valentina's home evenings favour the sail bench, dinner and reading; optional karaoke is an agreed activity. Each sleeps in their own bedroom. They do not automatically follow one another or answer for each other. |
| Neo and Alyssa's station apartment (`neo_home`) | Entrance ↔ living room ↔ {kitchen/dining room, hall, herb balcony}; hall ↔ {shared bedroom, bathroom}. Console/sofa and a compact repair/bookbinding desk are zones in the living room. | Around 19:00, either can start cooking; shared dinner or co-op requires both to be home and available. Neo alternates repair work and sofa downtime. Alyssa alternates notebook work, botanical sketches and herbs. The dining table stays clear for meals. Each can pursue a different activity without ending their relationship or forcing the other to join. Shared bedroom remains private to both residents. |
| Tyler's East Ward duplex (`tyler_home`) | Accessible porch ↔ entry/living room ↔ {kitchen/dining room, level hall}; hall ↔ {Tyler's bedroom, father's bedroom, accessible bathroom}. | Home evenings: kitchen meal, dominoes in living room or ballgame on porch when weather permits; bedroom for sleep. Preserve commitments to his father and boxing-club work. His father's room reflects established co-residence, but this plan does not invent a new fully simulated NPC, medical routine or dependency mechanic. Any future father interactions need separate authored scope. |

For Rei's existing pilot, propose entrance ↔ living space ↔ {kitchen/dining area, library, art space, hallway}; hallway ↔ {Rei's bedroom, Yuriko's bedroom, bathroom}. Rei's 17:00 home period alternates art space and cooking; preserve the 20:00 Iron Circle departure and 23:00 library reading. Yuriko's 18:00 return uses kitchen, art space, bedroom or living space as already proposed. Neither resident's home presence guarantees the other's presence.

### Other established residents

For Lena, Naomi, Celeste, Dev, Rosa and Elliot, preserve existing weekday employment, variable after-work outings, free-day leisure and unhurried home mornings. The examples below apply only when the building scheduler actually places them at home, typically from 19:00; they are not new fixed appointments overriding outings.

| Home / existing location | Proposed connected layout | Proposed home routine |
| --- | --- | --- |
| Lena's clocktower flat (`lena_home`) | Entrance ↔ living/record room ↔ {kitchen, photo workroom, hall}; hall ↔ {bedroom, bathroom}. | Kitchen meal → photo sorting/drying in workroom → records in living room → bedroom. Slow morning: inspect drying prints, breakfast. The shop below is not her room or an automatic business access route. |
| Naomi's riverside maisonette (`naomi_home`) | Entrance ↔ living room ↔ {kitchen, balcony, stairs}; stairs ↔ landing ↔ {bedroom, bathroom}. Hangboard is a living-room exercise zone. | Meal/tea using handmade mugs → brief hangboard session if rested, or mystery novel in living room → bedroom. Balcony herbs in suitable weather. Bicycle repair work remains at the cycle shop. |
| Celeste's blue-door cottage (`celeste_home`) | Entrance ↔ piano sitting room ↔ {kitchen/dining room, hall}; hall ↔ {bedroom, bathroom}. | Kitchen baking or dinner → piano or bird-guide reading → bedroom. Home morning: bread preparation or reading star maps. Piano playing is interruptible by invitation and does not force an audience. |
| Dev's station studio (`dev_home`) | Entrance ↔ single studio with kitchenette, component desk, game table and sleeping zone; studio ↔ bathroom. | Component desk repairs → kitchenette meal → tabletop setup or quiet downtime → sleeping zone. Games require actual available participants; no imaginary guests. Workbench and sofa share presence. |
| Rosa's market terrace (`rosa_home`) | Entrance ↔ sitting room ↔ communal dining room ↔ {kitchen, shared courtyard}; sitting room ↔ stairs ↔ landing ↔ {bedroom, bathroom}. | Recipe planning/cooking → dinner → sitting-room rest, or courtyard gardening while light/weather allow. A large table does not create a nightly gathering: visitors need invitations. She can choose private downtime. |
| Elliot's willow cabin (`elliot_home`) | Covered porch ↔ living/work room ↔ {kitchenette, bedroom, bathroom}. Carving desk is a living-room zone. | Store field notebooks → kitchen meal → listen to recordings or carve at desk → bedroom. Porch observation only in suitable conditions; field surveys stay at work. |
| Daniel's flat above the Bijou (`daniel_home`) | Stair entrance ↔ poster-lined hall ↔ {living/drawing room, kitchen, bedroom, bathroom}. | Dinner → draw lobby cards or read film notes in living room → bedroom. Judo kit is stored rather than creating a home training arena. Preserve cinema commitments; residential stairs do not unlock projection-room access. |
| Fox's Blackhaven hideout (`fox_home`) | Entrance ↔ living/kettle room ↔ {equipment workshop, private evidence room, hall}; hall ↔ {bedroom, bathroom}. | Around 16:00: workshop equipment maintenance; preserve 19:00 patrol. Around 23:00: evidence-room observations, then bedroom. A visitor waiting in the living room cannot inspect records or hear private work automatically. |
| Gordon's Civic Court apartment (`gordon_home`) | Entrance/uniform locker ↔ living/reading room ↔ {small kitchen, hall}; hall ↔ {bedroom, bathroom}. | Around 20:00: stow uniform, cook/eat, read in the quiet chair, then sleep. Existing headquarters and field duties remain off-site. No confidential case material appears in casual room descriptions. |
| Sylvanis's shuttered flat (`sylvanis_home`) | Bell entrance ↔ bare sitting room with two chairs ↔ {small kitchen, private notes room, bedroom, bathroom}. | Preserve 23:00 research-note review in the private room and overnight sleep. Sitting-room interactions retain his established volatility; domestic routines do not turn him into a gentle host. The flat is not the Glasshouse laboratory, and visiting does not grant research clearance. |

### Four Aces' private homes

Keep current cover schedules and the staggered 20:00–22:00 HQ appointment. Home activity never exposes an operational identity, mission, real-time location or address to outsiders. These authored graphs are design data, not publicly revealed maps.

| Home / existing location | Proposed connected layout | Proposed home routine |
| --- | --- | --- |
| Martos's private apartment (`martos_home`) | Entrance ↔ living room ↔ {kitchen, watch workroom, hall}; hall ↔ {bedroom, bathroom}. | Cook rice/eat → watch repair at the desk or quiet living-room rest → bedroom. Pause for the existing private appointment when scheduled. Tools and heavy curtains are ordinary visible details, not evidence of his role. |
| Elias's private penthouse (`elias_home`) | Entrance ↔ sitting/rehearsal room ↔ {kitchen, script study, hall}; hall ↔ {bedroom, bathroom}. Stretching mat is a sitting-room zone. | Meal → scripts/film scores in study or stretches in sitting room → private downtime and sleep. Rehearsal does not imply he is performing for every visitor. |
| Mavis's private room (`mavis_home`) | Authorized threshold ↔ single room with headphone/repair desk, chair and sleeping zone. Do not invent adjoining rooms, a registered address or a leaseholder. | Listen to field recordings → headphone repairs → quiet rest/sleep; preserve scheduled departures. Entry is permission-gated at the threshold because there is no separate public lounge. Bathroom/building facilities remain unspecified until separately established. |
| Camila's private apartment (`camila_home`) | Entrance ↔ living/chess room ↔ {kitchen, private study, hall}; hall ↔ {bedroom, bathroom}. Tango floor is an open living-room zone. | Dinner → chess problem, fountain-pen writing in study or tango practice → bedroom. Practice can be solo; paired dancing needs agreement. Home access never unlocks Oculus finances or private papers. |

### Custom protagonist residences and exceptions

| Existing selectable property | Proposed connected layout | Occupancy and routine rule |
| --- | --- | --- |
| Downtown apartment (`vacant_downtown_home`) | Entrance ↔ open living room/kitchen ↔ hall ↔ {bedroom, bathroom}. | Player-controlled meals, rest and any supported furnished activities; no autonomous movement of the active player. |
| Suburban house (`vacant_suburbs_home`) | Entrance ↔ living room ↔ {kitchen, garden, hall}; hall ↔ {bedroom 1, bedroom 2, bathroom}. | Second bedroom starts unassigned; selecting the house does not create a roommate. Garden activity respects weather. |
| Beach cottage (`vacant_beach_home`) | Entrance ↔ living room ↔ {kitchen, dune-facing deck, hall}; hall ↔ {bedroom, bathroom}. | Quiet indoor or deck activities as chosen by the player; deck uses outdoor conditions. |
| University apartment (`vacant_university_home`) | Entrance ↔ living/study area with kitchenette ↔ {separate bedroom, bathroom}. | Study is a zone, not an invented extra room. Preserve the property's unfurnished starting description. |

Unselected properties remain vacant. Layouts do not add residents, purchased furniture or possessions. Any inactive custom-character routine must follow supported existing scheduling and owned furnishings; a saved player room is never randomly reassigned while the player is exploring.

The Crow has no known private residence: do not generate one. Takeo, Thirteen and Charles use special HQ/laboratory locations and fixed story-sensitive appointments in the current home registry. Keep these under the public/faction-interior phase with existing story and clearance rules; do not move them into invented domestic bedrooms. Ordinary locals without an authored home are outside this residential inventory until a home is explicitly designed.

### Routine resolution and rollout checks

1. Resolve the existing building appointment, travel and story constraints first. All times above are current schedule anchors, not promises that a character will be home on every story day.
2. When arrival completes, select an accessible room matching the activity. Never leave a ghost occupant in the previous building or change rooms while travelling.
3. Sleeping uses the assigned bed/sleeping zone. Awake home activities vary by preference and recent activity, with proposed 20–60 story-minute dwell periods; exact values await tuning. Screen refreshes never reroll positions.
4. Conversations and agreed shared activities temporarily hold participating characters. An actual departure deadline should produce a visible wrap-up rather than silent disappearance. Solo pursuits do not summon housemates.
5. On free days or weather changes, use the existing building decision, then choose an appropriate available room. Roof/balcony/porch routines fall back indoors without forcing new travel.
6. The active player chooses room movement. NPC routine simulation must never move the player out of their current exploration, conversation or activity.

Proposed residential delivery batches after the penthouse: core homes and shared households; other established residents; private Ace homes and supported custom-home layouts. This is a dependency suggestion, not a committed delivery order. Each batch requires its room artwork, access coverage and save checks before being called complete.

Add acceptance cases for Amy/Minsu separate thresholds; studio zones sharing witnesses; Ivan/Valentina separate bedrooms; Neo/Alyssa independent activities and shared-bedroom privacy; accessible Tyler routes without compulsory stairs; every resident's work departure and free-day behaviour; Mavis's undisclosed address; faction-sensitive exceptions; vacant/custom properties remaining correctly occupied; and adverse-weather fallback. Validate each graph for connected public routes, correct private gates and safe legacy arrival defaults. Record actual results only when implementation exists.

**Planning evidence (2026-11-11):** Reviewed the source files named above, including home aliases, special fixed appointments, free-day routing and custom-home selection in `custom_protagonist.py`. Added proposed layouts/routines for all distinct named residential homes represented by those sources and the four selectable custom properties, with explicit exceptions. No runtime or save changes, generated art, gameplay tests or UI inspection performed.

## Presence, knowledge and privacy (shared rules)

### Public buildings, headquarters and established events

The [public buildings and faction rooms specification](INTERIORS_PUBLIC_AND_FACTION_PLAN.md) expands this plan with connected layouts, workplace routines and an explicit event-to-room migration contract (2026-11-11). The user requires previously established indoor events and meetings to occur in specific rooms. Preserve existing event identities, participants, timing, access, outcomes and progression; assign rooms without inventing new events. Detailed architecture remains proposed. This requirement applies to residential scenes too.

- Only characters physically in the current room appear as nearby partners or automatically witness its interactions. Someone upstairs does not automatically react to kitchen conversation.
- Building invitations and faction clearance remain necessary. Home entry does not automatically permit private bedroom entry.
- Closed private doors offer Knock. Responses depend on availability, relationship and established access permissions.
- Household familiarity can reduce unnecessary friction while preserving personal boundaries.
- Companions need their own access and can wait in an allowed shared room; entering a room must not silently bypass their checks.
- Navigation does not reveal exact occupants through walls. Visible occupants, witnessed movement or an informed answer provide whereabouts. Last-known information can become outdated.
- Dialogue context must use actual room presence and appropriately scoped knowledge, without leaking unseen conversations or confidential faction information.

## Room activities and invitations

Initial candidates include cooking/eating in kitchens, reading in libraries, painting/model-making in workspaces, relaxing together in living rooms and sleeping/resting in suitable private rooms.

Offer invitations such as “Want to sit in the living room?” Recipients can accept, decline or suggest later. Acceptance moves the participants together only when access permits, while preserving the ongoing interaction.

Adjacent-room movement should be quick and avoid repetitive confirmations. The reviewed design uses immediate, zero-additional-minute adjacent moves with per-edge access checks; timed routes must be explicitly authored. Activities retain their existing duration. See the integration review for event timing and multi-room routing.

## Automatic location-appropriate wardrobes — required scope

The user requested automatic wardrobe switching as part of interiors: characters use an available appropriate outfit at the beach, boxing gym and other relevant locations, homewear at home, and formal wear for formal settings, then change out automatically when leaving. Apply this to NPCs and the active protagonist using their own available wardrobes. This is planned behaviour, not implemented functionality.

| Context | Outfit category and activation |
| --- | --- |
| Beach/swimming visit | Beach outfit at an authored beach/activity destination. Merely visiting a nearby coastal shop, pier or cottage does not imply swimming attire. |
| Boxing gym, training hall, exercise | Gym/training outfit for an actual gym visit or training activity. A spectator meeting in an arena lounge does not automatically require workout clothes. |
| Character's own home | Homewear during ordinary at-home time; sleepwear only for an actual sleep/bedtime activity if available. Visiting someone else's home does not automatically put the visitor in homewear. |
| Formal setting or event | Formal outfit for explicitly tagged formal rooms/events, such as an authored formal reception. Do not classify every workplace, HQ corridor or library as formal. |
| Work, faction duty or campaign | Appropriate available work/role outfit where authored; preserve required uniforms, masks and scene-specific appearance constraints. Homewear or generic formal rules cannot remove required protective equipment or reveal a concealed identity. |
| Ordinary destination / leaving a special context | Recompute the destination's appropriate outfit; if none applies, restore the underlying everyday/manual outfit. Leaving the beach for home selects homewear; leaving for ordinary streets restores everyday clothing. |

### Availability, selection and transitions

- Add explicit category tags and stable outfit references to existing wardrobe options. Reuse the current wardrobe/image selection and availability checks; do not infer eligibility solely from filenames, generated prompt prose or an outfit's colour.
- Choose only an outfit belonging to that character, currently available/unlocked, with a valid supported appearance reference. Do not create, purchase, unlock or generate clothes automatically. Characters with no eligible category outfit retain a valid baseline outfit.
- Where multiple eligible outfits exist, select one once per context visit, optionally preferring a different choice from the previous visit. Persist that choice; moving between gym rooms, refreshing or loading must not reroll it. New category tags for custom outfits require explicit assignment/review, not guessing from arbitrary text.
- Resolve outfits after arrival and room/activity intent, before portrait/dialogue rendering. On departure remove the old automatic context and restore baseline for travel, then apply the new context at arrival. A room-level event override ends when that event/room context ends. Do not flicker between baseline and homewear on each room transition within one house.
- Changing is a discreet presentation transition with no extra time charge or new compulsory minigame. Use a changing area where one exists without adding a blocking path or claiming public undressing. The automatic wardrobe feature is not a clothing inventory transport simulation.
- Keep the underlying baseline separate from the effective automatic outfit. Automatic selection must never overwrite the saved everyday preference with beachwear and later restore the wrong outfit. A manual choice during a visit overrides automatic preference for that visit; provide an explicit resume-auto option. A persistent manual lock is an optional user setting, not assumed for all existing saves.
- Proposed priority: required scene/role appearance, explicit manual visit override, active activity/event category, room category, building category, baseline. Missing optional category assets fall back safely; mandatory masks/equipment use existing canonical presentation and cannot be discarded by a manual override.

### Shared-system integration and verification

Use the [integration review's wardrobe contract](INTERIORS_INTEGRATION_REVIEW.md#wardrobe-and-location-resolution) for scheduling, campaign, rendering and save interactions. Camera-specific staged photo outfits remain local to the photo unless the player explicitly chooses to wear them. Automatic switching does not grant private gallery looks, reveal locked bedroom art, change combat stats or count as a gameplay action/reward.

Acceptance includes beach → street, beach → home, home → gym → home, gym room-to-room continuity, formal event inside an otherwise ordinary building, work uniform precedence, character without category outfits, multiple available outfits, manual selection/resume-auto, missing/deleted assets, custom protagonist, NPC departures, mid-journey saves and reload during an active campaign. Verify portrait, outfit label and dialogue appearance agree without altering completed photos or historical scenes.

**Planning evidence:** Inspected `camera.py` available outfit/default handling, `lifestyle_apps.py` player-outfit storage, wardrobe use in `hangout_ui.py`, and existing alternate-outfit manifests. Full category/asset and rendering-consumer audit remains pending. No automatic switching implementation or runtime checks performed.

## Artwork and rollout (delivery)

**Generation batches:** [Ten numbered image batches](INTERIORS_GENERATION_BATCHES.md) assign all 438 currently required new images (421 interior, 17 outdoor) exactly once. Each batch has a room-by-room Markdown list and JSON manifest. Keep reuse candidates and unresolved dorm bathrooms outside generation until reviewed/resolved. These are production groupings, not completed art or release milestones.

**Required placeholder correction:** Replace all active simple placeholder location art with finished illustrations as part of this update, including outdoor places. The current audited list is Pixel Pier arcade, Copper Lantern bar, Winterfield Lanes, the public library, Afterglow nightclub, Winterfield Galleria and Silver Sands beach. Six interior replacements are already included in the new-room image budget; the beach adds one outdoor image. Audit remaining enabled locations and missing-art fallbacks before release, add any further affected locations to the inventory, preserve finished existing art, and ensure scene/Map/preview routes all use the replacements. Protect finished artwork from the bulk primitive renderer in `tools/build_venue_art.py`. Artwork generation, installation and render verification remain pending.

1. Complete Rei's penthouse pilot: connected rooms, Rei/Yuriko routines, doors, privacy, companions, room-aware conversation and saves.
2. Verify a public workplace/event and a secure council/laboratory location with guards, following the integration review's cross-system pilot gates.
3. Expand to the remaining agreed residences, public buildings and faction interiors, preserving site clearance, assignments and guard authority. Layouts must fit their size and existing descriptions; a dorm should differ from an estate.

Complete the agreed interiors release criteria before MH-016 implementation and campaign shot production. Campaign chronology review and manuscript drafting may proceed earlier; room-specific staging and final shot artwork wait for stable implemented locations. The confirmed sequence does not reduce the agreed interiors or artwork scope.

Every distinct explorable interior space must have its own dedicated image before release. This includes entrances, corridors, bedrooms, public rooms, staff areas, meeting rooms, secure rooms and campaign spaces. Separately displayed/navigable zones require their own views; ordinary activity hotspots within one room do not create additional image requirements. Do not reuse a generic building image across separate rooms or duplicate an image under different filenames. Existing artwork may satisfy one matching space after inspection. Shared placeholders are development-only and do not meet acceptance. Follow the integration review's image manifest, complete-coverage and visual checks; record production and inspection evidence when actually performed.

## Integration and save compatibility

Use the shared registry and semantic building/room/zone contract in the integration review. Existing faction-room IDs must retain their meaning or receive an explicit compatible mapping; do not create a parallel system that bypasses current access checks. Final code/schema names remain implementation choices.

Introduce additive, versioned room state with appropriate defaults for characters saved at expanded buildings. Save/load must preserve room positions and accepted activities, tolerate unavailable or renamed rooms through a safe fallback, and retain relationships, invitations, assignments, property ownership and story progress. Migration must be idempotent and require no save reset.

Review travel arrival, nearby-character lists, dialogue witnesses, group invitations, companions, scheduled meetings, sleep, campaign scenes and restricted access against the same room model. Buildings not yet expanded should keep their existing behaviour.

## Milestones

- [x] Inspect current home/routine and faction-room foundations and record this proposal.
- [x] Confirm first place in the update sequence and Planned status, including the penthouse/public/secure-location pilot progression (2026-11-11).
- [x] Draft layouts and room routines for other established homes and custom residence options, with explicit privacy and schedule exceptions (2026-11-11).
- [x] Draft public/faction layouts, workplace routines and established-event room mappings (2026-11-11).
- [x] Record required campaign, Bubblegram, JobSeek, schedule/preference and expanded room-guard integration (2026-11-11).
- [x] Review the complete design across systems, resolve shared contracts and document end-to-end acceptance scenarios (2026-11-11).
- [x] Record requested automatic location/activity wardrobe switching and its integration rules.
- [ ] Tag available wardrobe assets and implement/verify automatic outfit selection, restoration, manual overrides and shared appearance rendering.
- [ ] Implement room-aware campaign/app work flows, NPC preferred rooms and larger saved guard deployments; verify progression, scheduling, balance and legacy clearance.
- [ ] Inventory every indoor event producer and consumer; implement room assignments, access, attendance and legacy-event migration without changing established outcomes.
- [ ] Agree pilot layout, activities, artwork scope and movement/time rules.
- [ ] Establish shared location/room contracts and compatibility handling.
- [ ] Implement navigation, room routines and co-presence for the pilot.
- [ ] Implement privacy, companions, invitations and agreed activities.
- [ ] Produce and inspect room artwork and interactive layouts.
- [ ] Replace all active simple placeholder location art, including the seven identified venues, audit remaining scene/fallback routes and prevent primitive-generation tools overwriting finished images.
- [ ] Verify dedicated image coverage for every enabled interior room/view, including corridors and campaign/work spaces; reject missing assets and duplicated placeholder backgrounds.
- [x] Enumerate the current production room/view baseline and identify one-to-one existing-art reuse candidates, with asset existence/dimensions/hash checks and contact-sheet review.
- [ ] Verify migration and relevant regression/smoke scenarios.
- [ ] Expand to the agreed subsequent buildings.
- [ ] Document actual release behaviour and checks; validate/export patch notes.

## Acceptance and verification plan

- Yuriko independently spends time in her bedroom and living space; Rei follows appropriate room activities.
- Every pilot room is reachable through its intended connections entirely in the in-person window.
- Off-room characters are neither nearby conversation partners nor automatic witnesses.
- Knocking, refusal, allowed entry and restricted entry work for residents, visitors and companions.
- Room navigation does not disclose private or stale location information as current fact.
- Conversations, accepted invitations and scheduled activities remain consistent across room transitions.
- Save/load preserves room state; legacy saves migrate safely and repeated migration has no extra effects.
- Existing faction gates, assignments, ordinary travel and unexpanded buildings retain their behaviour.
- Inspect rendered room layouts and interactive states, including compact windows, empty rooms, closed doors and access errors.
- Run relevant room/routine/dialogue/access/save tests and feature smoke checks. Run `tests/phone_dark_theme_smoke.py` for the completed update and whenever phone surfaces change.
- For delivered player-visible work, follow `patch_notes/AUTHORING.md`, record actual evidence in `patch_notes/catalog.json`, run `patch_notes.py validate` and refresh `patch_notes/PATCH_NOTES.md` using `patch_notes.py export`.

## Current evidence and unresolved decisions

Initial proposal recorded 2026-11-10; residential/public expansions and integrated source/design review recorded 2026-11-11. No runtime changes, save changes, artwork generation, gameplay tests or rendered UI checks were performed for this plan. Planning is not a release, so it does not create a released patch-note entry.

Use the reviewed movement, location, scheduling and privacy contracts. Before enabling each building, finish its machine-readable graph/activity/access inventory, guard allocations, migration fixtures and artwork inventory; resolve non-established layout details where needed. Preserve in-person-only exploration and Yuriko's bedroom/living-space example. The integration review distinguishes resolved design rules from implementation validation still required.
