# Mysterious Hearts roadmap

Track future updates here, with detailed plans linked from each entry. Roadmap entries describe intended work; shipped behaviour and release evidence belong in the [patch notes](patch_notes/PATCH_NOTES.md).

**Plugin planning:** [Assessment, all ten plugin routes and per-plan task assignments](roadmap/PLUGIN_ASSIGNMENTS.md). Every new or materially revised update and child plan must assign relevant plugins to concrete tasks using the [updated template](roadmap/UPDATE_TEMPLATE.md). Preserve current scope/order/pauses; distinguish allocation from actual execution and verification.

## Approved update order — 2026-11-11

The user confirmed this implementation and release sequence:

1. **Lived-In Interiors (MH-004):** establish the shared room, presence, privacy, access, guard and save contracts. Verify Rei's penthouse pilot, a public workplace/event and a secure faction location before expanding to the remaining agreed buildings and completing the interiors release criteria.
2. **Campaign systems and presentation (MH-016):** after interiors, implement Maps-based campaign travel, continuous building gauntlets and illustrated visual-novel scenes. Verify an existing-campaign pilot with save/resume, then complete the planned conversion of existing campaigns using the finished room layouts.
3. **Ace campaigns (MH-012): Mavis → Martos → Elias → Camila.** Release each route with its complete climax and aftermath; Mavis proves the new-route and playable-history foundations. Once implementation starts, MH-012 stays In progress until all four routes are available and verified.
4. **Sylvanis campaign (MH-014):** follow the four Ace routes, using the proven shared systems for his private arena, objective-based finale and knowledge-sensitive history.

Shared chronology, continuity review and manuscript drafting can proceed during interiors development. Room-specific staging and final campaign shot artwork wait for stable implemented locations; MH-016 and Rei image production remain deferred until interiors are implemented. This records the order without starting implementation or resuming image generation. No delivery dates or versions are assigned. Existing combat and portrait work retain their current statuses and scope outside this newly ordered sequence.

**Decision evidence:** The user requested this roadmap change on 2026-11-11 after reviewing the recommended sequence. Interiors is now Planned; campaign presentation remains Deferred pending interiors; the Ace and Sylvanis campaigns remain Planned. Detailed story proposals and unresolved layout choices retain their existing decision status. Planning is not a gameplay release.

**Verification (2026-11-11):** Checked the roadmap and four linked update plans for matching sequence/status fields, existing local link targets and UTF-8 integrity. `python patch_notes.py validate` passed with 490 entries; `python patch_notes.py export` refreshed the generated notes. No new release entry, runtime changes, artwork production or save changes; gameplay tests and UI smokes were not run for this documentation-only update.

## Future updates

| ID | Update | Status | Sequence | Plan |
| --- | --- | --- | --- | --- |
| MH-019 | Campaign writing, character continuity and dramatic revision | Planned | Editorial work alongside existing plans; runtime delivery follows parent workstreams and approved order | [Nine-campaign revision plan](roadmap/CAMPAIGN_REVISION_PLAN.md) |
| MH-004 | Lived-In Interiors: room-by-room exploration | In progress | 1 — batches 01 and 02 artwork ready; runtime implementation pending | [Interiors update plan](roadmap/INTERIORS_UPDATE_PLAN.md) |
| MH-016 | Campaign gauntlets, map access and visual novel scenes | Deferred | 2 — after interiors; preserve current pause until then | [Campaign presentation update plan](roadmap/CAMPAIGN_PRESENTATION_UPDATE_PLAN.md) · [Rei artwork](roadmap/rei-campaign-artwork/README.md) |
| MH-012 | Ace campaigns: four playable personal stories | Planned | 3 — after MH-016: Mavis → Martos → Elias → Camila | [Update plan](roadmap/ACE_CAMPAIGN_UPDATE_PLAN.md) · [Mavis](roadmap/MAVIS_CAMPAIGN_PLAN.md) · [Martos](roadmap/MARTOS_CAMPAIGN_PLAN.md) · [Elias](roadmap/ELIAS_CAMPAIGN_PLAN.md) · [Camila](roadmap/CAMILA_CAMPAIGN_PLAN.md) |
| MH-014 | Sylvanis campaign: The Crow's Patience | Planned | 4 — after all four Ace campaigns | [Campaign update plan](roadmap/SYLVANIS_CAMPAIGN_UPDATE_PLAN.md) |
| MH-015 | Flashback visits in the main window | Released | Implemented 2026-11-10 | [Scope and evidence](#mh-015-flashback-visits-in-the-main-window) |
| MH-017 | Campaign flashback areas and historical conversations | Planned | Shared integration with MH-016, MH-012 and MH-014; approved order retained | [Area, room and cast designs](roadmap/CAMPAIGN_FLASHBACK_AREAS_PLAN.md) |
| MH-018 | Takeo Mishima playable campaign: Empire of One | Planned | Order unassigned; existing approved sequence retained | [Confirmed campaign plan](roadmap/TAKEO_CAMPAIGN_PLAN.md) |
| MH-013 | Semi-realistic manhwa portrait artwork update | In progress | Stage 2 masters/heights installed; Stage 3 complete with 146 staged wardrobes; Stage 4 pending | [Production plan](roadmap/PORTRAIT_ARTWORK_UPDATE_PLAN.md) · [Stage 3 delivery](roadmap/artwork-stage-03/README.md) · [Stage 2 height evidence](roadmap/artwork-stage-02/height-review/README.md) · [Batch 1 evidence](roadmap/artwork-batch-01/README.md) · [Individual audit](roadmap/artwork-portrait-audit/PORTRAIT_AUDIT.md) |
| MH-011 | Hamayashi-kai and Shinokami yakuza appearance refresh | Released | Implemented 2026-11-10 | [Scope and evidence](#mh-011-hamayashi-kai-and-shinokami-yakuza-appearance-refresh) |
| MH-010 | Syndicate guard design refresh | Released | Implemented 2026-11-10 | [Scope and evidence](#mh-010-syndicate-guard-design-refresh) |
| MH-009 | Combat textures and training layout | Released | Implemented 2026-11-10 | [Scope and evidence](roadmap/COMBAT_TEXTURE_REFRESH.md) |
| MH-008 | Textured interface and navigation refresh | Released | Implemented 2026-11-10 | [Scope and evidence](roadmap/UI_TEXTURE_REFRESH.md) |
| MH-007 | Combat RPG interface revamp | Released | Implemented 2026-11-10 | [Standalone combat UI plan](roadmap/COMBAT_RPG_UI_PLAN.md) |
| MH-006 | Protagonist-specific Story tab | Released | Implemented 2026-11-10 | [Scope and evidence](#mh-006-protagonist-specific-story-tab) |
| MH-005 | Campaign prose and narrative continuity | Released | Implemented 2026-11-10 | [Campaign prose plan](roadmap/CAMPAIGN_PROSE_UPDATE_PLAN.md) |
| MH-001 | Combat window redesign and animated attacks | In progress | Existing work in progress; outside the newly ordered sequence | [Part 1: animations](COMBAT_ANIMATIONS_UPDATE_PLAN.md) · [Part 2: lore, HUD and systems](COMBAT_WINDOW_UPDATE_PLAN.md) |
| MH-002 | RPG main menu and character selection | Released | Implemented 2026-11-10 | [Character selection update plan](roadmap/CHARACTER_SELECTION_UPDATE_PLAN.md) |
| MH-004 | Narrated campaign and hangout actions | Released | Implemented 2026-11-10 | [Scope and evidence](#mh-004-narrated-campaign-and-hangout-actions) |
| MH-003 | Guard update Part 2: dialogue, recognition and contact restrictions | Released | Order not assigned | [Guard Part 2 plan](roadmap/GUARD_UPDATE_PART_2_PLAN.md) |

No delivery dates or release versions are assigned. Add further updates as they are requested; do not treat suggestions as committed work.

## MH-019 Campaign writing, character continuity and dramatic revision

**Status:** Planned — revision scope requested; detailed scene treatments remain proposals.  
**Added:** 2026-11-11  
**Area:** Existing and future campaign prose, character continuity, historical references, pacing and outcome presentation  
**Detailed specification:** [Campaign revision plan](roadmap/CAMPAIGN_REVISION_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/CAMPAIGN_REVISION_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Revise Garrett, Rei and Fox/Gordon, and develop Mavis, Martos, Elias, Camila, Sylvanis and Takeo using distinct voices, scene structures and concrete consequences. Preserve established lore, personalities, private knowledge, mandatory combat results and confirmed outcomes, including Takeo's single Empire of One ending. Remove authoring directions/duplication from compiled prose and address the specific thematic tensions in Garrett's reunion and Rei's successor choice. Existing and future stories retain their in-person access through their parent campaign workstreams.

**Confirmed continuity choice:** Garrett's campaign canon wins: the formative Charles conflict occurs outside his Hong Kong school at sixteen, with Charles's violence explicitly acknowledged as wrong. The older seventeen/Mrs Lau/Kit/proud-beating account is superseded as this event; do not invent a second beating. Reconciliation of derivative lore is planned, not implemented here. The present-day Charles fight, required Garrett victory, disclosure timing and both reconciliation policies remain unchanged.

### Milestones

- [x] Review campaign sources, critique and latest historical/Sylvanis/Takeo decisions; record the user's Garrett canon selection.
- [x] Draft protected outcomes, source reconciliation, nine route-specific revision packages, voice/pacing rules and verification plan.
- [ ] Complete continuity/scene/era inventories and revise the selected existing-route pilot scenes.
- [ ] Complete existing manuscript/compiler revisions and future story/manuscript development without changing fixed outcomes.
- [ ] Integrate with MH-016, MH-012, MH-014, MH-017 and MH-018 as applicable, preserving the approved order and artwork pause.
- [ ] Run relevant state/save/knowledge checks, inspect rendered scenes and record actual editorial/cold-read findings.
- [ ] Publish accurate implemented release records and keep this entry open until its included campaign work is complete.

**Dependencies:** Existing campaign/prose/flashback handlers; character/lore sources; independent era references; interiors and MH-016 for final staging/presentation; route-specific combat objectives and save contracts.

**Completion criteria:** Campaign canon is consistent across new prose/context; each route addresses its identified weaknesses while preserving confirmed facts/outcomes; complete assembled branches have distinct voices, meaningful consequences and no editorial leakage; old saves and historical visits remain compatible. Future treatment details remain proposals unless separately confirmed; Takeo's already confirmed treatment is retained.

**Save impact:** None during planning. Future text revision must preserve active/archived scene snapshots, stable IDs, evidence, progress, disclosures and one-time effects; no forced replay or invented memories.

**Progress and evidence:** Detailed plan and cross-links recorded 2026-11-11. Seven plans/123 local links and anchors, UTF-8, tables, nine route packages, the unique MH-019 registration and retained production constraints passed documentation checks. All 496 prior catalogue records and their order remain unchanged; added planning Development report `plan-2026-11-11-campaign-writing-revision`. Catalogue validation passed with 497 entries and export refreshed. Five patch-note tests passed; the existing missing `tests/screenshots/mixtape-art-review-0.jpg` archive-source failure remains. No runtime lore/prose, artwork or player-save changes; no gameplay/UI/cold-read verification claimed. Full evidence is in the linked plan. This adds no implementation slot, delivery date or release version.

## MH-018 Takeo Mishima playable campaign

**Status:** Planned — campaign treatment, Empire of One title and recommended ending confirmed by the user on 2026-11-11.  
**Added:** 2026-11-11  
**Area:** Playable character, Shinokami campaign, historical visits and command contacts  
**Detailed specification:** [Takeo Mishima: Empire of One](roadmap/TAKEO_CAMPAIGN_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/TAKEO_CAMPAIGN_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Make Takeo playable with no Grove account and Sylvanis, Number Thirteen and Keisuke Hachimura as his starting contacts. Record the confirmed Directive 0 captaincy, ethical dissolution, chosen Onami service, Shinzo Kazama, 2024 conquest, Nanoengine-based Shinigami research, 2027 defeat, Shinokami founding, nameless son One/Neo, surviving Thirteen and begrudging Sylvanis arrangement. User clarified that Takeo is roughly 56 and ages little visibly due to his Awakening; this supersedes the current age of 42 when implemented.

The confirmed treatment comprises fourteen chapters, eight historical sequences and a complete American-expansion crisis using the existing US foothold, the Crow's dependency/betrayal and a former Directive 0 deputy's UN operation. The selected ending preserves the bridgehead and Thirteen's command while Takeo personally destroys the contested programme archive; the full headquarters aftermath closes the campaign. The two brainstormed alternate endings are superseded and excluded from scope. Planned access is character selection, then the in-person Story view and Maps-based travel under MH-016. Historical areas, command meetings and combat stay in the in-person window. No implementation slot is assigned; the approved interiors → presentation → four Aces → Sylvanis sequence remains intact. The approved story is not yet implemented or released.

### Milestones

- [x] Inspect current lore, access/roster rules, chronology, shared campaign plans and roadmap workflow.
- [x] Record user-established history, age correction and playable-start requirements; draft a present story, climax, finale and historical visits.
- [x] Confirm Empire of One, the campaign treatment and the recommended ending; retain protagonist-only campaign travel and the full aftermath (2026-11-11).
- [ ] Finalise unnamed supporting-character details, fine chronology, room layouts and combat tuning; assign an implementation slot without changing the existing approved sequence.
- [ ] Reconcile canon sources and implement the playable start, no Grove and three persistent contacts.
- [ ] Implement the complete campaign, period-specific visits, locations and aftermath using the shared systems.
- [ ] Verify tactical/dialogue consequences, the confirmed ending, saves, knowledge, contact refresh, dark phone states and rendered in-person scenes.
- [ ] Record release access/save impact/checks; validate and export patch notes when implemented.

**Dependencies:** Interiors and MH-016; MH-017 historical-visit conventions; protagonist/contacts/Grove systems; campaign objectives, combat and save isolation. Coordinate the territorial betrayal with Sylvanis's distinct arena campaign; do not silently combine their outcomes.

**Completion criteria:** Takeo is selectable, has no Grove and starts with the three required contacts; his history and roughly-56 age are consistent; Empire of One completes with the bridgehead and Thirteen's command preserved, Takeo personally destroying the contested archive, and the full headquarters aftermath; visits and encounters run in person; existing protagonists and saves retain their boundaries.

**Save impact:** None from planning. Proposed additive Takeo-scoped progress, knowledge, objectives and historical records require compatibility checks before release. Do not globally trigger a faction war or rewrite saved conversations.

**Initial planning evidence:** Planning/source review completed 2026-11-11. The initial plan separated user-established facts from suggestions and flagged runtime sources requiring reconciliation. Checked 16 local links, fourteen chapter IDs, eight historical IDs, tables, UTF-8, age correction and preserved implementation order/pause. All 493 prior catalogue records remained unchanged; validation passed with 494 entries and export completed. Five patch-note tests passed; the existing missing `tests/screenshots/mixtape-art-review-0.jpg` failure remained. Development report `plan-2026-11-11-takeo-campaign` preserves that initial design record.

**Confirmation evidence (2026-11-11):** The user accepted the ideas as the confirmed campaign plan, selected Empire of One and chose the recommended ending. Updated the plan, milestones and completion criteria; removed alternative endings from active scope. Verified 16 links, fourteen chapter IDs, eight historical IDs, title/treatment/ending consistency, tables, UTF-8 and preserved order/pause. All 495 prior catalogue records and roadmap content outside MH-018 are unchanged. Validation passed with 496 entries; five patch-note tests passed with the existing missing historical screenshot failure, and export completed. Development report `plan-2026-11-11-takeo-campaign-confirmed` records the decision. Implementation, artwork, runtime canon changes and gameplay/UI verification remain pending.

## MH-017 Campaign flashback areas and historical conversations

**Status:** Planned  
**Added:** 2026-11-11  
**Area:** Optional in-person historical areas, room exploration and conversations  
**Detailed specification:** [Eight area designs and historical cast](roadmap/CAMPAIGN_FLASHBACK_AREAS_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/CAMPAIGN_FLASHBACK_AREAS_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Every campaign protagonist must have a repeatable flashback area with era-appropriate people to talk to. Eight designs cover Rei, Garrett, Fox/Gordon, Mavis, Martos, Elias, Camila and Sylvanis; existing Emily/Sophie school access remains intact. Each design specifies rooms, periods, companion placement, conversation topics/openings, optional activities, knowledge limits and unlocks. Reuse **Visit flashback area** in the main in-person view, with paused present time, local history and an explicit return. New areas and room expansions are planned, not playable yet.

**Required historical versions — 2026-11-11:** Every flashback character in every campaign requires a separate character reference sheet and dialogue style guide for each era, including younger playable protagonists and scripted-only characters. Each pair defines that era's personality, knowledge, relationships, appearance and voice. No present-day or later-era profile/style fallback. The [shared authoring contract](roadmap/CAMPAIGN_FLASHBACK_AREAS_PLAN.md#historical-cast-and-conversation-authoring-contract) defines the complete cast inventory, required fields, missing-profile behaviour and review gate; authoring the actual pairs remains pending.

### Milestones

- [x] Inspect released visits, independent historical sheets, isolation tests, all campaign treatments and the approved update order.
- [x] Design eight areas with room networks, period-specific casts, conversation topics, activities and continuity boundaries.
- [x] Specify mandatory character reference sheets and dialogue styles for every character/era across scripted and optional flashbacks.
- [ ] Lock new NPC names, ages, chronological coexistence, introductions and historical dialogue references.
- [ ] Author and review every character/era reference/style pair against a complete cast inventory; verify historical personality/voice and absence of present-day or later-era knowledge.
- [ ] Implement shared period/room support after interiors and preserve the existing school visits and saves.
- [ ] Integrate Fox/Gordon with existing-campaign conversion, each Ace area with its route and Sylvanis's area with MH-014.
- [ ] Verify access, historical knowledge, late responses, save/resume, live-state isolation and rendered in-person controls.
- [ ] Record actual release access/save impact/checks and validate/export release notes when implemented.

**Dependencies:** MH-015's released embedded visit foundation; independent flashback lore; Lived-In Interiors room contracts; MH-016 presentation/access rules; campaign chronology and historical artwork. No change to the approved order or current MH-016/artwork pause. Planning can proceed before those implementation dependencies.

**Completion criteria:** All nine campaign protagonists have appropriate visits; Emily/Sophie retain access. Every flashback character/era has a reviewed reference sheet and dialogue style, checked for historical personality/voice as well as knowledge, with no present-day or later-era fallback. Periods never mix ages, secrets or future events; optional conversation cannot resolve a campaign event, create live contacts/rewards or change present resources/time. The Crow's permitted campaign locations, Camila's private family history, Elias's family-HQ defeat, Sylvanis's character and the early conspirator's blank-face/glasses/implied-only parentage remain consistent.

**Save impact:** Proposed versioned, additive period/room/protagonist-scoped memory records. Preserve existing `school` and `hong-kong-school` IDs, histories, active visits and present state. Migration, restart requirements and UI behaviour remain to be verified; no saves changed by planning.

**Progress and evidence:** Source inspection and detailed area/cast design completed on 2026-11-11. Eight area/ID designs, 13 local links, eight inbound plan links/anchors, table structure and retained order/pause checked. New names, rooms and fine chronology remain proposed. Development report `plan-2026-11-11-campaign-flashback-areas` preserves all 492 prior catalogue records; validation passed with 493 entries and export completed. Final patch-note suite has five passes and the existing missing historical mixtape screenshot failure. Full evidence and the corrected report-ordering check are in the linked plan. Runtime, reference sheets, art, gameplay/UI verification remain pending. Planning is not a release; MH-015 remains Released on its original scope.

**Historical-version requirement follow-up — 2026-11-11:** Mandatory per-character/per-era reference sheets and dialogue styles now cover all campaigns and scripted/optional appearances. Five linked planning files and the shared plan's 13 local links/anchors/table structure checked; profile authoring and runtime enforcement remain pending. Report `plan-2026-11-11-era-specific-flashback-references` preserves all 494 prior records; catalogue validation passed with 495 entries and export completed. Patch-note tests: five passed, one existing failure for missing `tests/screenshots/mixtape-art-review-0.jpg`. No runtime, artwork or save changes; approved order and pause retained.

## MH-016 Campaign gauntlets, map access and visual novel scenes

**Status:** Deferred — paused by user; revisit after Lived-In Interiors is implemented  
**Sequence:** 2 — after Lived-In Interiors, before new Ace and Sylvanis campaign implementation; confirmed 2026-11-11.  
**Added:** 2026-11-11  
**Area:** Campaign combat flow, map discovery/access, scripted scenes and flashbacks  
**Detailed specification:** [Campaign presentation update plan](roadmap/CAMPAIGN_PRESENTATION_UPDATE_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/CAMPAIGN_PRESENTATION_UPDATE_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Keep successive campaign opponents in the same building inside one in-person gauntlet, without closing combat and returning through Story for the next guard. Move campaign destination travel from Story to Maps, where the player finds and selects the location. Required hidden/inaccessible destinations become available when the campaign needs them, with an authored post-objective choice to remain revealed/open, remain revealed but restricted, or become hidden again.

Present campaign scripts and flashbacks as visual novel shots, each with its own illustration of the action. Replace the separate novel reading panel with complete prose in the in-person narration window, one sentence per logical line, and page-flip animation between shots. Preserve outcomes, mandatory scenes, historical isolation, choices and saved progress. Apply these shared requirements to existing campaigns and future MH-012/MH-014 work; this entry implements no gameplay.

### Milestones

- [x] Record the requested scope and inspect campaign, combat, map/access, prose and flashback integration points.
- [x] Write the detailed flow, acceptance cases, artwork requirements, migration concerns and delivery sequence.
- [x] Confirm second place in the update sequence, preserving the interiors dependency and current artwork pause (2026-11-11).
- [ ] Inventory all travel controls, building encounters, location dispositions and authored shots/branches.
- [ ] Implement and verify a representative map-to-gauntlet-to-visual-novel pilot, including a flashback and save/resume.
- [ ] Convert existing campaigns, produce/review per-shot images and implement compatible saves.
- [ ] Run relevant gameplay/UI checks, including dark phone Maps states, and inspect rendered layouts/animations.
- [ ] Record actual access, save impact and verification; validate/export release notes and update status when available.

**Dependencies:** Authoritative campaign/combat handlers and guard victory IDs; map points and travel/access rules; in-person narration, prose/flashback state and scene artwork. Coordinate with MH-013 artwork, MH-015 embedded visits and the interiors plan without changing their historical release records.

**Completion criteria:** Same-building waves require no menu round trip; campaign travel requires Maps; every required site has verified reveal/entry/after-story rules; all campaign shots have matching art, sentence-formatted narration and reliable page flips; existing outcomes and save progress survive conversion.

**Save impact:** None during planning. Proposed additive gauntlet, location-grant and stable shot-position state must migrate existing victories, active fights, reading cursors and completed outcomes without resets or duplicate rewards. Actual compatibility remains to be verified.

**Progress and evidence:** Planning/source review completed 2026-11-11. The linked plan distinguishes user requirements from proposed resource/animation details and records actual documentation/catalogue checks. A Development report records planning only; implementation, artwork, gameplay tests and rendered UI verification remain pending.

**Artwork production and pause, 2026-11-11:** User requested all Rei campaign scene/shot images, then explicitly paused the work until the [Lived-In Interiors update](roadmap/INTERIORS_UPDATE_PLAN.md) is implemented. [Production record](roadmap/rei-campaign-artwork/README.md) preserves 183 shot records across 35 scenes: one generated opening image with corrected arm tattoos, 182 pending, plus prompts and 29 reference snapshots. Adult Rei's exposed arm tattoos remain mandatory; school-era Rei remains tattoo-free. No further generation is scheduled. On revisiting, reconcile room layouts, scene locations and references with implemented interiors, and recheck the opening image before reuse. Runtime gauntlets, Maps access and the new reader remain pending.

## MH-015 Flashback visits in the main window

**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person flashback visits and memory journal  
**Detailed specification:** Embed flashback visits and their journal in the main in-person content area. Reuse the existing historical scene and conversation controls, keep present-day time paused, resume saved visits in the same window and restore the present-day view on return.

**Plugin assignments (future maintenance only; assigned 2026-11-11):** Released status and historical evidence remain unchanged. Context Guard applies to complex/resumed work with actual hook evidence; follow the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md).

| Specific maintenance task | Assigned plugin / workflow | Required verification |
| --- | --- | --- |
| Historical dialogue/journal changes | Story Skills + Writer's Loop | Preserve exact era, cast and knowledge boundaries; substantive new historical areas belong to MH-017. |
| Embedded visit return/resume and live-world isolation regressions | falsegreen-skill | Run flashback visit/lore checks and inspect in-person return, journal, loading/error and saved resume states. |

These allocations have no new execution evidence; run and record the relevant checks when a maintenance task is requested.

Players continue to use **Visit flashback area** from the location or hangout view as Rei, Emily, Sophie or Garrett. No separate flashback window should open.

### Milestones

- [x] Confirm scope and inspect main-window routing, visit isolation and save resume.
- [x] Implement the embedded visit and memory journal, routing and lifecycle cleanup.
- [x] Run relevant checks and inspect normal, compact and interactive UI states.
- [x] Record save compatibility and actual release evidence; validate/export patch notes.

**Dependencies:** Main in-person container, HangoutCanvas, flashback visit state, simulation clock and dark theme helpers.

**Completion criteria:** Both entry buttons and saved resume display in the existing main window without a new top-level window; conversation, selection, cancel/retry, journal and return work; cleanup cancels abandoned polling/replies.

**Save impact:** No schema changes or migration. Existing active visits and memory history remain usable after restart.

**Progress and evidence:** Implemented 2026-11-10 in `flashback_visit_ui.py`, with location/hangout entry points and game render/resume/phone routing updated. The main window hosts the visit and its journal; Escape closes the journal or returns to the present. View teardown cancels polling and invalidates unfinished replies while preserving active visit saves. Verified:

- `python -m unittest discover -s tests -p 'test_flashback*.py' -v`: 16 passed. The save-isolation assertion now compares campaign progress before/after the visit instead of assuming an obsolete chapter order.
- `python -m unittest discover -s tests -p test_campaign_flashbacks.py -v`: six passed.
- `python tests/flashback_visits_ui_smoke.py`: passed for all four protagonists, both entry buttons, no new top-level windows, hidden phone, historical cast, selection, speech/actions, paging, cancellation/error drafts, unchanged time, saved resume, rebuild cleanup, keyboard Escape and location/hangout restoration. Provider mocked; no live generation or player-save writes.
- `python tests/campaign_flashbacks_ui_smoke.py`: passed for the five mandatory memories and present-day restoration.
- `python tests/phone_dark_theme_smoke.py`: passed across 34 phone pages and control states. Rendered dark surfaces inspected.
- `python tests/patch_notes_ui_smoke.py` and `python tests/start_ui_smoke.py`: passed; start-screen check covered 28 previews and minimum layout.
- Normal/compact scenes, embedded journal, pending/disabled controls and retry draft visually reviewed: [Rei](tests/screenshots/visit-rei.png), [Garrett compact](tests/screenshots/visit-garrett-compact.png), [journal](tests/screenshots/visit-rei-journal.png), [pending](tests/screenshots/visit-rei-pending.png), [error](tests/screenshots/visit-rei-error.png).
- `python patch_notes.py validate`: passed, 485 entries. `python patch_notes.py export`: refreshed `patch_notes/PATCH_NOTES.md`. Patch-note unit suite: five passed; one existing archive-source failure for missing `tests/screenshots/mixtape-art-review-0.jpg`. Changed Python files compile successfully.

**Release record:** `release-2026-11-10-flashback-main-window` in [patch notes](patch_notes/PATCH_NOTES.md), published 2026-11-10. Existing saves need no migration; restart to load the embedded view.

## MH-014 Sylvanis campaign: The Crow's Patience

**Status:** Planned  
**Sequence:** 4 — after interiors, MH-016 and all four Ace campaigns; confirmed 2026-11-11.  
**Added:** 2026-11-10  
**Area:** Sylvanis personal campaign, historical episodes, Syndicate origins and in-person arena conflict  
**Detailed specification:** [Sylvanis campaign update plan](roadmap/SYLVANIS_CAMPAIGN_UPDATE_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/SYLVANIS_CAMPAIGN_UPDATE_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Create a complete personal campaign for playable Sylvanis through the in-person **Stories, guards & gang properties → Story** tab. The requested history covers his mid-Blisk-war arrival after humans captured his planet; immediate criminality, mastery of all human martial arts and planetary fear; recruitment by protective mercenaries; immediate agreement with the future Crow to murder their leader and create the multinational Syndicate with its card/suit system; the Crow's growing tolerance without affection; Red/Blue Magic, live human experimentation and his private testing arena; murdering Garrett's parents after seeking strong eastern fighters; knowingly admitting Charles's infiltration years later for amusement; and the Takeo supply arrangement.

The proposed sixteen-chapter/ten-history treatment culminates in a deliberately disrupted arena demonstration and a personal confrontation with the Crow. The exhibition is conclusively shut down, losses and commercial consequences are settled, and Sylvanis remains a purely chaotic evil man driven by impulse, hedonism, chaos and curiosity. No moral development, redemption or hidden loyalty is allowed. Title, chapter structure, scene details and material ending variants are proposals; the user's history and character constraints are fixed. The release sequence is confirmed above; this entry adds no playable content.

**Campaign expansion, 2026-11-11:** The former mercenary group is **the Organisation**, led by **Kaden Mourne**, an older, muscular man in mercenary gear whose kindness and goodwill are genuine. Flashbacks show the betrayer/conspirator who becomes the Crow with a **blank face and glasses**, withholding his identity and appearance. It is **heavily implied that he is Kaden's son**, without confirming that relationship or assigning the Crow a civil name. The linked plan expands recruitment, trust and coup scenes, historical art requirements and knowledge boundaries; individual scene beats remain proposals. This updates planning within the existing release sequence.

**Agency and final-question clarification, 2026-11-11:** Sylvanis is not manipulated in any way, shape or form; he knowingly goes along because he thinks it will be fun. Apply this throughout the campaign, including the conspirator's proposal and the Crow's present confrontation. Before dying, Kaden directly asks Sylvanis whether he will ever truly find the thrill he is looking for. The question reinforces Sylvanis's existing pursuit without causing remorse, changing his motives or disclosing the conspirator's identity/parentage. The scene beat is required; exact wording and Sylvanis's response remain manuscript choices.

### Milestones

- [x] Record the requested history and unchanging character direction; inspect roadmap, Story routing and relevant character/criminal-world sources.
- [x] Draft chronological history, present escalation, a climax and conclusion, knowledge boundaries, implementation dependencies and acceptance criteria.
- [x] Confirm delivery after interiors, MH-016 and all four Ace campaigns; allow earlier chronology/manuscript work (2026-11-11).
- [x] Record the Organisation and Kaden Mourne, genuine goodwill, blank-face/glasses flashback direction and heavily implied parentage; expand the existing historical treatment and acceptance criteria (2026-11-11).
- [x] Establish Sylvanis's unmanipulated participation for fun throughout the treatment and Kaden's required question before death; clarify the coup and arena staging and add acceptance criteria (2026-11-11).
- [ ] Reconcile historical dates/ages, source conflicts and era-specific appearances/abilities; complete manuscripts and finale encounter design.
- [ ] Build the opening and first historical episode with save/resume and a safe return to the present.
- [ ] Implement the full campaign, secret-knowledge handling, private arena, objective-based climax and persistent aftermath.
- [ ] Verify both outcomes, existing saves/campaigns, in-person presentation and any affected dark phone states.
- [ ] Record implemented scope, access, save impact and actual checks; validate/export release notes and mark Released only when available.

**Dependencies:** Implemented interiors and MH-016 campaign systems/presentation; the approved delivery sequence places MH-014 after all four MH-012 routes. Existing protagonist selection, combat objectives, private knowledge, Glasshouse/Takeo access, criminal operations and historical portraits remain required. Reconcile Crow/Ace/Sylvanis chronology before manuscript lock, and coordinate with MH-013 artwork without changing its scope.

**Completion criteria:** All required history is established, including the Organisation, Kaden's appearance and genuine goodwill, his question to Sylvanis before death, the conspirator's blank face and glasses, and strongly implied but unconfirmed parentage. Sylvanis is clearly unmanipulated and participates because he expects fun throughout the campaign. The present provocation reaches a resolved climax and outcome-sensitive aftermath, and Sylvanis has no moral transformation. The Crow and Charles retain agency, concealed identity and separate character knowledge remain intact alongside existing campaign outcomes, and actual verification is recorded.

**Save impact:** None during planning. Proposed additive Sylvanis-scoped progression and isolated historical snapshots must preserve other stories, identities, contacts, resources and custody outcomes. Migration and compatibility with existing saves require implementation checks.

**Progress and evidence:** Planning and source review completed 2026-11-10. Explicitly identifies older restrictions that leave the parents' killer unconfirmed, deny Sylvanis's secret awareness, prohibit Crow campaign history/locations or treat all drug work as desk reviews. These require targeted future reconciliation; runtime sources are unchanged. Actual documentation/catalogue check results are recorded in the linked plan. A Development report records planning only; no campaign release is claimed.

**Expansion evidence (2026-11-11):** Recorded the Organisation/Kaden/flashback/parentage requirements in the linked plan and new Development report `plan-2026-11-11-sylvanis-organisation-kaden`. All 27 plan links resolve; sixteen chapter and ten historical IDs are preserved; the other roadmap entries and all 490 prior catalogue records are unchanged. Catalogue validation passed with 491 entries and export was refreshed. Five patch-note tests passed; the existing archive-source check still fails for missing `tests/screenshots/mixtape-art-review-0.jpg`. No runtime, artwork or save changes; gameplay/UI checks remain pending implementation.

**Agency/final-question evidence (2026-11-11):** The follow-up clarification is recorded in the linked plan and Development report `plan-2026-11-11-sylvanis-agency-final-question`. All 27 plan links, sixteen chapter IDs, ten historical IDs, the Planned status and approved sequence were checked; all 491 prior catalogue records remain unchanged. Validation passed with 492 entries and export was refreshed. Five patch-note tests passed; the same missing historical screenshot still fails the archive-source test. Planning only, with no runtime/artwork/save changes or gameplay/UI verification.

## MH-013 Semi-realistic manhwa portrait artwork update

**Status:** In progress — Batch 1 and Stage 2 default masters/height correction released  
**Added:** 2026-11-10  
**Area:** Transparent character artwork across selection, wardrobes, in-person scenes, historical scenes, combat and guards  
**Detailed specification:** [Production plan](roadmap/PORTRAIT_ARTWORK_UPDATE_PLAN.md) · [Firm art direction](assets/portraits/ARTSTYLE.md) · [306-file audit](roadmap/artwork-portrait-audit/PORTRAIT_AUDIT.md)

**Plugin assignments:** [Task-level allocations](roadmap/PORTRAIT_ARTWORK_UPDATE_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Bring all project-authored transparent character portraits into a cohesive semi-realistic illustrated manhwa style using Ivan and Charles as rendering anchors. Require complete head-to-mid-thigh body coverage, preserving each person's identity, age, build, tattoos, outfits and contextual masks/powers. Batch 1 installed eight pilot portraits; Stage 2 installs all 107 contemporary default masters with the full-roster height correction. Stage 3 has completed 146 staged wardrobe variants. Their live installation and the remaining contextual replacements are pending.

### Milestones

- [x] Inventory all 300 portrait-directory PNGs and six related transparent profile/reference files; record source hashes, dimensions and alpha metadata.
- [x] Visually review all 306 files on 26 labelled sheets; inspect the two anchors individually and on two backgrounds; compare twelve face crops.
- [x] Write individual findings and changes, replace conflicting anime/hip-up guidance, and define production stages and acceptance gates.
- [x] Produce, review and install the eight-portrait representative pilot (Batch 1); correct Emily's missing legs and Minsu/Otis framing.
- [x] Produce and review all 107 Stage 2 masters (89 contemporary characters, 18 guard roles), including seven pilot masters; preserve source snapshots and exact generation records in `roadmap/artwork-stage-02/`.
- [x] Audit all Stage 2 heights; install the 100 replacement default masters and keep seven pilot masters; correct shared stature fitting, transparent margins and cropped-body interpretation. [Height roster, installation and verification](roadmap/artwork-stage-02/height-review/README.md), 2026-11-11.
- [x] Vary the 71 remaining display defaults within 175–180 cm male / 160–165 cm female and apply seven explicit user heights without changing the original 29 authored heights. [Current height roster and follow-up](roadmap/artwork-stage-02/height-variation/README.md), 2026-11-11.
- [x] Produce and review all 146 Stage 3 wardrobe variants against the installed masters and corrected heights; verify staged normal/compact rendering, routing and dark phone previews. [Delivery and evidence](roadmap/artwork-stage-03/README.md), 2026-11-11.
- [ ] Complete historical, uniform, combat and remaining guard replacements; preserve archived originals and user-owned custom art.
- [ ] Install the accepted wardrobe and contextual replacements through the integration stage.
- [ ] Verify loaded paths, scaling, save compatibility and all affected rendered contexts/checks.
- [ ] Record actual installed scope and release evidence, validate/export patch notes and mark Released only when available.

**Dependencies:** Character appearance references, outfit/portrait resolution, historical overrides, combat and guard providers, selection/hangout scaling and MH-010/MH-011 guard designs.

**Completion criteria:** Every in-scope active portrait passes identity, semi-realistic rendering, mid-thigh coverage, anatomy, transparency, context and in-game presentation gates. Archived/scenic/reference files have explicit dispositions and no accidental runtime use.

**Save impact:** Batch 1 retains IDs, paths, outfits, relationships and save fields. Restart to load the new art and pilot height fitting. Existing guard encounters, historical overrides, custom fallback and wardrobe choices were checked; no migration.

**Progress and evidence:** Planning review completed 2026-11-10; the immutable baseline covers 306 files. Batch 1 replaces Ivan, Charles v2, Emily, Minsu, Priya Shah, Otis Bell, the Clubs guard and combat Ivan with eight 1024×1536 RGBA portraits; 298 baseline files remain byte-identical. Original backups, prompts, per-file reviews, hashes, alpha composites and actual check results are in [Batch 1 evidence](roadmap/artwork-batch-01/README.md). Pilot fitting preserves relative stature and legacy wardrobe scaling. The original [planning verification](roadmap/artwork-portrait-audit/VERIFICATION.md) remains historical evidence. Remaining wardrobes, historical art, uniforms, combat and guards are not claimed complete.

**Release record:** `release-2026-11-10-artwork-batch-01` in [patch notes](patch_notes/PATCH_NOTES.md); published 2026-11-10 for Batch 1 only. Same-day follow-up `release-2026-11-10-emily-mid-thigh-crop` tightens Emily to true mid-thigh with connected legs and no knees; [crop evidence](roadmap/artwork-batch-01/emily-mid-thigh-fix/README.md). `release-2026-11-10-emily-rendering-refinement` simplifies her skin/fabric shading while retaining detailed hair; [rendering evidence](roadmap/artwork-batch-01/emily-style-refinement/README.md). Full MH-013 remains In progress.

**Stage 2 follow-up, 2026-11-11:** `release-2026-11-11-stage2-character-heights` installs the accepted default masters at all 107 roster paths (100 changed, seven retained). All 29 recorded heights are preserved, including Ivan 193, Garrett 188 and Rei 184 cm; missing male/female heights use display defaults 178/163 cm. Shared fitting prevents the wider player slot from inflating stature and excludes transparent padding. The lower thigh/leg portion is off-image: visible portraits use a common cropped-body fraction, preserving aspect ratio and a picture baseline rather than treating the cut edge as feet. Selection, in-person groups, prose and combat use the shared height data; phone wardrobe previews retain RGBA. Existing IDs, wardrobe selections, custom heights, historical routing and saves remain intact; restart to reload. The [follow-up evidence](roadmap/artwork-stage-02/height-review/README.md) records actual automated and rendered checks. Later wardrobe/history/combat artwork production and full MH-013 completion remain pending.

**Current height refinement, 2026-11-11:** `release-2026-11-11-stage2-varied-heights` supersedes the uniform defaults above with stable individual values across the full requested ranges. Gordon is 183 cm, Fox 184 cm, the Crow 180 cm, Keisuke Hachimura 183 cm, Joseph Richter 190 cm, and both Oni and Custom Robotic 198 cm. All original 29 authored values remain unchanged; 71 other defaults vary by identity. Richter's cybernetic form shares his 190 cm height. [Current roster, checks and save impact](roadmap/artwork-stage-02/height-variation/README.md). No portrait PNGs or save fields changed.

**Stage 3 delivery, 2026-11-11:** All 146 wardrobe variants across ten characters are complete and staged outside live asset discovery. Full-size, whole-family and three-background reviews include the user's Emily skirt, Minsu upper-thigh and Samantha finger corrections, approved covered sleepwear in original colours, and Ivan's successful beach retry. All 306 baseline live files and the height registry remain unchanged. The staged checks pass 292 height comparisons, 62 saved wardrobe round trips, 26 automatic routes and 20 visually inspected runtime-loader/scene/phone screenshots. Dark-phone, lifestyle and start smokes pass; 70 of 71 related unit tests pass, with the existing Theo camera fixture failure recorded. [Delivery, publication checks and remaining limits](roadmap/artwork-stage-03/README.md) accompany Development report `development-2026-11-11-artwork-stage-03-wardrobes`. No player saves or live wardrobe paths changed. Stage 4 and later installation remain pending; full MH-013 stays In progress.

## MH-012 Ace campaigns: four playable personal stories

**Status:** Planned  
**Sequence:** 3 — after interiors and MH-016; Mavis → Martos → Elias → Camila, before Sylvanis; confirmed 2026-11-11.  
**Added:** 2026-11-10  
**Area:** Protagonist campaigns, playable memories, in-person missions and relationships  
**Detailed specification:** [Ace campaign update plan](roadmap/ACE_CAMPAIGN_UPDATE_PLAN.md), [Mavis campaign treatment](roadmap/MAVIS_CAMPAIGN_PLAN.md), [Martos campaign treatment](roadmap/MARTOS_CAMPAIGN_PLAN.md), [Elias campaign treatment](roadmap/ELIAS_CAMPAIGN_PLAN.md) and [Camila campaign treatment](roadmap/CAMILA_CAMPAIGN_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/ACE_CAMPAIGN_UPDATE_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Requested scope: a personal campaign when playing as each of the four Aces. Mavis's campaign must explore her twenty-year-old self killing the previous Ace of Spades for another group, subsequent Syndicate recruitment, infiltration and assassination work, relationships with the Crow, Sylvanis and the other Aces, and a concluding arc with a climax. Planned access is the existing in-person **Stories, guards & gang properties → Story** tab for the selected Ace. This planning entry adds no playable content.

Martos's requested scope now includes military and special-forces experience/backstories, heinous assignments followed by desertion, recruitment by the Crow, controlling Rage, and the personal worldview and reasons behind his blind loyalty. His detailed treatment proposes fourteen chapters and eight memories connecting that history to a present protection mission involving a survivor of his former unit's crimes.

Elias's user-established origin includes a German crime family, innate excellence in combat and the arts with lifelong praise, and acting chosen over family leadership because he considered other criminals beneath him. He personally defeated all incoming Syndicate forces sent against his family, then was personally defeated by the Crow **at his family's crime headquarters**; his organisation became an affiliate. That first inferiority produces fear, awe and obsession with the Crow. The detailed treatment proposes fourteen chapters and eight memories, followed through a present affiliate conflict.

Camila's user-established origin is adoption from an orphanage by the Crow, direct upbringing as his personal protégée, and deliberate preparation to be his financial Ace and successor. Her detailed treatment proposes fourteen chapters and eight memories connecting that parent-child relationship and education to a present crisis requiring her own judgement. Intended succession remains distinct from a current leadership transfer.

**Confirmed campaign rule:** The Crow may appear outside Syndicate headquarters in authored campaigns. Earlier blanket campaign restrictions and Elias's proposed Syndicate-HQ duel are superseded. Camila's established family history can be portrayed to informed audiences while his unrelated identity remains concealed. Runtime reconciliation is part of future implementation.

The confirmed rollout is Mavis → Martos → Elias → Camila, after interiors and MH-016 and before Sylvanis. Each route releases with its own complete ending and aftermath. The linked documents provide detailed treatments and shared implementation/verification; names, incidents, endings and chapter counts beyond user-established premises remain proposals. Chronology review and manuscript drafting can begin earlier; room-specific staging and final shot artwork wait for stable implemented interiors.

### Milestones

- [x] Record the requested scope and inspect current Ace/Crow/Sylvanis lore, Story routing, flashbacks and prose state.
- [x] Draft the four-campaign framework, Mavis treatment, relationship payoffs, dependencies and acceptance criteria.
- [x] Record Martos's requested military/loyalty scope and draft his detailed chronology, special-forces experience, complicity/desertion, recruitment, Rage arc, worldview, chapters and conclusion.
- [x] Record Elias's user-established prodigy/actor/family origin, defensive victories, Crow defeat, affiliate absorption and fear/awe/obsession; draft his detailed campaign and conclusion.
- [x] Record Camila's adoption, direct upbringing, personal mentorship and intended succession; draft her family/education arc, crisis, authority/knowledge boundaries and conclusion.
- [x] Update all four campaign plans for authorised Crow locations and correct Elias's defeat to his family crime headquarters.
- [x] Confirm the four-route rollout after interiors/MH-016 and before Sylvanis (2026-11-11).
- [ ] Resolve historical chronology, approve new story premises and lock the four route outlines.
- [ ] Build and review one complete Mavis chapter, including a playable memory, present-day consequence and save/resume.
- [ ] Complete and verify Mavis's campaign, climax and outcome-sensitive aftermath.
- [ ] Complete and verify Martos, Elias and Camila campaigns with their own conclusions.
- [ ] Verify legacy saves, cross-campaign boundaries, in-person presentation and affected phone states.
- [ ] Record actual save impact and release evidence; add implemented feature entries to the patch-note catalogue, validate and export.

**Dependencies:** Implemented interiors and MH-016 campaign systems/presentation precede route implementation. Existing protagonist selection and Story tab (MH-002/MH-006), campaign prose (MH-005), dialogue/flashbacks, combat, guarded location access, private knowledge and character appearance systems remain foundations. MH-001 animation production is not a proposed release prerequisite.

**Completion criteria:** All four selected Aces have distinct complete campaigns. Mavis's history and named relationships receive setup, development and payoff. Martos's military/special-forces history, heinous assignments, desertion, recruitment, Rage and worldview-driven loyalty are developed through scenes and conclusion. Elias's genuine talent/praise, acting choice, complete defensive victories, family-headquarters Crow defeat, first inferiority, affiliate absorption and obsession are preserved. Camila's adoption, upbringing, mentorship, financial competence and genuine intended succession receive a complete arc. Crow campaign appearances follow authored venues, including outside HQ; private family knowledge and bounded delegation are respected. Activities stay in person and existing identities, present hierarchy, campaign outcomes and saves remain consistent. Required checks have recorded evidence.

**Save impact:** Proposed additive protagonist-scoped campaign state and isolated historical mission snapshots. Existing stories, identities, contacts, resources, combat and completed outcomes must be retained. Migration and restart requirements remain to be verified during implementation; no saves changed by this plan.

**Progress and evidence:** Source inspection, shared framework and all four detailed campaign plans completed on 2026-11-10. Reviews cover character voices/abilities, Crow portrayal and existing campaign/knowledge foundations. Camila's family/succession history and the Crow location correction explicitly supersede older blanket campaign constraints; implementation must reconcile current runtime consumers. User-established history is distinguished from current code and proposed additions. Documentation/catalogue verification results are recorded in the update plan. Runtime implementation, manuscripts, artwork, gameplay tests and rendered review remain pending. No Ace campaign release claimed.

## MH-011 Hamayashi-kai and Shinokami yakuza appearance refresh

**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person guard artwork and appearance context  
**Detailed specification:** Five transparent portraits: understated navy yakuza suits for Kai sentinel and Kai house guard; richer tailoring, patterned shirts, jewelry and discreet gear for Yokai and Tengu; tailored outerwear and accessories over Oni's existing robotic body. Preserve identities, powers and equipment mechanics.

**Plugin assignments (future maintenance only; assigned 2026-11-11):** Released status and historical evidence remain unchanged. Context Guard applies to complex/resumed work with actual hook evidence; follow the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md).

| Specific maintenance task | Assigned plugin / workflow | Required verification |
| --- | --- | --- |
| Requested yakuza appearance/description maintenance | Story Skills + Writer's Loop; Bulk BG Remove for needed cutouts | Preserve Kai/Shinokami uniforms, equipment and Oni's robotic body; review alpha and actual in-person encounters. |
| Guard portrait resolver and older-save regressions | falsegreen-skill | Run guard portrait suites and relevant yakuza/in-person smokes; use MH-013 for further artwork production. |

These allocations have no new execution evidence; run and record the relevant checks when a maintenance task is requested.

Access through existing in-person Hamayashi-kai and Shinokami guard posts, conversations and combat after restart.

### Milestones

- [x] Confirm scope and inspect artwork and appearance consumers.
- [x] Generate and install five transparent portrait replacements; synchronize dialogue, NPC details and combat appearance context.
- [x] Verify alpha, portrait routing, old profile fallback, faction-specific presentation and rendered artwork.
- [x] Record save impact and actual checks; validate and export patch notes.

**Dependencies:** Existing guard portrait loader, appearance definitions and in-person encounter systems.

**Completion criteria:** Five tailored yakuza designs render transparently; human faces remain visible; Oni remains robotic; Syndicate masking rules remain scoped to Syndicate guards.

**Save impact:** Compatible with existing saves; restart to reload cached images and Python definitions. No migration or balance changes.

**Progress and evidence:** Six portrait, 19 dialogue and 23 enhanced-combat tests passed. `tests/yakuza_guard_art_smoke.py` and `tests/guard_portraits_ui_smoke.py` passed; five-character slate-background render and in-game combat inspected. Patch-note reader and start UI smokes passed. Catalogue validation and export passed. Patch-note unit suite has five passes and the existing missing `tests/screenshots/mixtape-art-review-0.jpg` archive-source failure. Prompts recorded in `assets/portraits/guards/yakuza-refresh-prompts.json`; visual evidence in `tests/screenshots/yakuza-guard-redesign.png`.

**Release record:** `release-2026-11-10-yakuza-guard-appearance` in [patch-note catalogue](patch_notes/catalog.json), implemented locally 2026-11-10.

## MH-007 Combat RPG interface revamp

**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person combat presentation  
**Detailed specification:** [Standalone combat RPG interface plan](roadmap/COMBAT_RPG_UI_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/COMBAT_RPG_UI_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Combat now uses much larger player and opponent portraits over shared location artwork, similar to the hangout window, with an RPG command dock, mirrored resource/status HUDs, objective and exchange-phase information, target feedback and expandable narration. Players access it through existing in-person combat routes after restarting. This remains separate from MH-001; its scope and evidence are unchanged. All eight approved additions are implemented: favourite moves/quick slots, last-exchange breakdown, tactical overlay, contextual boss presentation, resource cost ghosting, portrait inspection drawer, adjustable HUD density/text size and first-fight guided hints. Future Part 1 animation playback remains separate.

### Milestones

- [x] Confirm the requested visual direction and separate plan; inspect combat and hangout source.
- [x] Confirm all eight additional UI suggestions as required scope.
- [x] Implement the large-portrait arena and RPG controls described in the specification.
- [x] Implement all eight approved additional UI features and verify their acceptance criteria.
- [x] Run relevant combat checks and inspect new layouts and interactive states.
- [x] Document save impact and release evidence; validate and export patch notes, retaining the known historical archive-source test failure.

**Dependencies:** Existing in-person stage, location artwork, combat portrait provider and authoritative engine state. Coordinate HUD/effect contracts with MH-001 without duplicating mechanics or animation production.

**Completion criteria:** Large portraits over the encounter location, readable resources and states, usable action/target selection at normal and compact sizes, all eight approved additional UI features, preserved encounter rules and save restoration, and verified UI states.

**Save impact:** Restart required; existing stories and active encounters remain compatible. Additive protagonist-scoped preferences retain favourite move IDs, HUD settings and hint dismissal. New UI-resolved exchanges record resource/state snapshots; older exchanges remain readable. No destructive migration or balance changes.

**Progress and evidence:** Implemented on 2026-11-10. 96 combat and 23 enhanced-combat tests passed, along with new MH-007, existing combat, enhanced/opponent scenarios, portrait, Part 2, partner/boss, dialogue and Path UI smokes. Large/compact and interactive states inspected; large-text HUD clipping corrected. Patch-note reader and start-screen smokes passed; catalogue validation/export passed. Five patch-note unit tests passed; historical archive-source coverage still fails on missing `tests/screenshots/mixtape-art-review-0.jpg`. [Full implementation evidence](roadmap/COMBAT_RPG_UI_EVIDENCE.md) records actual checks and limits.

**Release record:** `release-2026-11-10-combat-rpg-interface` in [patch-note catalogue](patch_notes/catalog.json), available locally after restart.

## MH-005 Campaign prose and narrative continuity

**Status:** Released  
**Added:** 2026-11-10  
**Area:** Campaign storytelling and in-person scenes  
**Detailed specification:** [Campaign prose plan](roadmap/CAMPAIGN_PROSE_UPDATE_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/CAMPAIGN_PROSE_UPDATE_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Give campaigns clearer character motives, connective prose and emotional consequences through novel-like scenes with richer narration and inner thoughts. The user approved all initial ideas: opening context, arrival atmosphere, prose between dialogue, discovery interpretation, motivated transitions, aftermath, connected flashbacks, saved recaps/history, authored story foundations with optional bounded generated description, and a complete pilot chapter before expansion. The user also approved close third-person viewpoint, distinct narrative voices, emotional continuity, reflection choices, quiet scenes and recurring details, reading comfort, and chapter-level editorial review. Selective campaign expansion is also approved; Garrett G1–G6 and Rei R1–R6 are now approved, with substantial present-day supporting-cast involvement planned through 20 additional scene briefs.

### Milestones

- [x] Confirm initial scope and novel-like narrative style with inner thoughts.
- [x] Confirm close third-person viewpoint, distinct voices, emotional continuity, reflection choices, quiet scenes/recurring details, reading comfort and chapter editorial review.
- [x] Approve selective campaign expansion based on narrative gaps.
- [x] Approve Garrett G1–G6 and Rei R1–R6 and request many present-day supporting-cast scenes.
- [x] Choose pilot chapter and reading density; draft the ensemble scenes with cast, knowledge and access checks.
- [x] Draft and implement the agreed chapter and presentation.
- [x] Run relevant checks and inspect rendered scenes and affected UI states.
- [x] Assess save impact and record release evidence; validate and export patch notes when released.

**Dependencies:** Campaign dialogue, flashbacks, progression, in-person rendering and saved scene state.

**Completion criteria:** Clear motives and causal progression throughout the pilot, preserved player agency and knowledge boundaries, safe resume and verified presentation; expand coverage as agreed.

**Save impact:** Restart required. Additive narrative flags, recipient-specific disclosures, shared-memory records, read history, page position and text size. Original campaign indices, evidence, victories, contacts and rewards persist. Older active dialogue finishes as saved; completed gameplay is not repeated.

**Implementation and verification (2026-11-10):** Implemented all 120 authored sections across Garrett, Rei and both Interpol viewpoints, 28 optional visits, shared memories, reflection choices, safe disclosures, contextual memory gates and the dark in-person reader. 110 relevant unit tests pass, including both reconciliation policies, all Rei outcomes/orders, both viewpoints and all 24 Ace orders, current Crow defeat and legacy capture. Reading inventory, access, precise coverage and validation limits are in [MH-005 evidence](roadmap/CAMPAIGN_PROSE_EVIDENCE.md). An independent reader unfamiliar with external lore has not performed the planned cold read; this remains an explicitly unverified editorial check, not a claimed test result.

**Release record:** `release-2026-11-10-campaign-prose` in [patch-note catalogue](patch_notes/catalog.json). Available locally after restart.

### Earlier planning record

The statements below record the earlier planning/drafting stages; their pending-work statements are superseded by the implementation evidence above.

**Progress and evidence:** Initial source inspection and plan recorded on 2026-11-10. User confirmed all initial ideas and novel-like narration with inner thoughts; status advanced to Planned. All subsequent suggestions are now also approved, including close third-person viewpoint and emotional continuity. Selective expansion with new scenes/flashbacks is now approved. Garrett G1–G6 and Rei R1–R6 are approved for future implementation. Added 20 present-day supporting-cast briefs in response to the user request, with reciprocal support, privacy choices, character availability, solo-mission boundaries and save continuity requirements. Further source review identified overlap with The chair at the table and Protection is not ownership; expand those existing scenes to preserve purpose without repetition. No implementation or tests performed; no release claimed.

**Confirmed best-friend expansion (2026-11-10):** Add Garrett and Rei as recurring reciprocal supports in both campaigns, with the canonical Golden Dragon first meeting and developing friendship shown through two shared flashback briefs and twelve present-day scene briefs. Preserve protagonist viewpoint, the distinct receipt/till-drawer drawings, private disclosures, solo missions and independent campaign progress. Character-reference and relationship-source inspection complete; implementation and checks pending.

**Chapter organisation (2026-11-10):** [Chapter outlines](roadmap/CAMPAIGN_CHAPTER_OUTLINES.md) organise all approved scenes and five existing memories into ten Garrett chapters and eight Rei chapters/modules. Coverage index complete; preserve either order of Rei's resolution modules, Garrett's direct encounter path, canonical outcomes and saved progression. Memory-gate refactor, prose drafting, implementation and verification remain pending.

**Confirmed Fox/Gordon expansion (2026-11-10):** User requested comparable length to Garrett/Rei with first-meeting memories, present-day partnership scenes, arguments and misleading leads. [Fox/Gordon chapter outline](roadmap/FOX_GORDON_CHAPTER_OUTLINE.md) adds twelve planned chapters, 36 present-day briefs, four flashback sequences and eight explainable false-lead threads. Preserve both viewpoints, four parallel Ace enquiries and the existing Crow defeat/survival outcome. Current case/cast source inspection complete; historical-premise reconciliation, prose drafting, measured length comparison, implementation and checks pending. No release claimed.

**Fox/Gordon origin development (2026-11-10):** Expanded the four planned flashbacks into a detailed first meeting and gradual partnership arc, with early disagreements over priorities, earned trust through follow-through and honest reporting, and specific present-day payoffs. Draft dialogue and new historical premises are identified as adaptation planning, not existing source canon or released scenes. Full prose, chronology reconciliation, implementation and checks remain pending.

**Fox/Gordon investigations and guard fights (2026-11-10):** Added [detailed investigative beats](roadmap/FOX_GORDON_INVESTIGATION_BEATS.md) for all eight false leads/red herrings, with investigation, arguments, disproof and relationship payoffs; mapped six existing Syndicate guard sequences to distinct confrontation scenes. Source inspection confirms Clubs/Spades/affiliate guards precede each Syndicate combat target and Ace reveals precede these fights. Preserve scoped victories, ordinary retry rules and older earned Crow-capture saves alongside the newer defeat route. Planning only; implementation and checks pending.

**Ace/Crow confrontation development (2026-11-10):** Added [five confrontation treatments](roadmap/FOX_GORDON_CONFRONTATIONS.md) with authored dialogue examples, mutual reactions, combat-event conditions and result-sensitive aftermath. Reviewed Four Aces character/ability directions, Crow voice/secrecy and Interpol outcome branches. Preserve distinct personalities, loyalty, current defeat and earned legacy capture. Planning only; implementation, rendered review and checks pending.

**Lengthier emotional dialogue (2026-11-10):** User requested richer, longer exchanges throughout the campaigns, citing Rei learning about Marcus as one example. [Writing specification and scene drafts](roadmap/CAMPAIGN_DIALOGUE_DRAFTS.md) now include fuller Marcus-news, Garrett/Charles reunion-opening, Garrett/Rei friendship and Fox/Gordon post-defeat passages. Four illustrative drafts authored; remaining manuscript, runtime integration, visual review and checks pending. No release claimed.

**Rei dialogue manuscript (2026-11-10):** [Full-route first draft](roadmap/REI_DIALOGUE_MANUSCRIPT.md) adds 35 manuscript sections mapping all approved Rei scenes, retaining the full Marcus-news draft by reference, and writing the other memories, supporting-cast exchanges, investigation/confrontation dialogue, all three successor endings and Richter success/retreat aftermath. Coverage check performed; precise minor variants, editorial review, runtime integration and gameplay/UI checks pending. Garrett and Fox/Gordon full passes remain follow-on work. Documentation only; no release claimed.

**Garrett dialogue manuscript (2026-11-10):** [Full-route first draft](roadmap/GARRETT_DIALOGUE_MANUSCRIPT.md) adds 43 manuscript sections, covering all approved Garrett scenes and existing campaign stages, retaining D02/D03 by reference. Includes longer memories, April/Rei/Mei/Dana conversations, wrong-answer/daily response gates, reunion and both reconciliation choices, Red Dragons operations/accountability, ending variants and legitimate direct-encounter arrival. Documentation coverage/section/link checks performed; minor variants, editorial review, runtime integration and gameplay/UI checks pending. Fox/Gordon full manuscript remains outstanding. No release claimed.

**Fox/Gordon full manuscript (2026-11-10):** [Dual-viewpoint first draft](roadmap/FOX_GORDON_DIALOGUE_MANUSCRIPT.md) supplies 36 approved present-day scenes, four partnership memories and two additional legacy-capture/ongoing-operation sections. Includes written Fox/Gordon interior alternatives, all eight misleading leads, six guard sequences, Ace/Crow confrontations and result-sensitive aftermath; retains full D04 at FD32 with Fox interior assembly. Section/coverage/link checks performed. All three campaigns now have full-route first drafts; final state variants, editorial review, measured pacing parity, runtime implementation and gameplay/UI checks pending. Documentation only; no release claimed.

**Implementation started (2026-11-10):** Full approved scope requested. Garrett chapter 1 is the implementation pilot; default reading density is the full novel-style manuscript with immediate text, adjustable type and saved pages. Preserve all existing gameplay indices and resolve new narrative state additively.

## MH-001 Combat window redesign and animated attacks

**Status:** In progress  
**Added:** 2026-11-10  
**Area:** In-person combat  
**Detailed specification:** [Part 1 — animations and effects](COMBAT_ANIMATIONS_UPDATE_PLAN.md) · [Part 2 — lore, HUD, systems and all other changes](COMBAT_WINDOW_UPDATE_PLAN.md)

**Plugin assignments:** [Part 1 task allocations](COMBAT_ANIMATIONS_UPDATE_PLAN.md#plugin-task-assignments) and [completed Part 2 maintenance](COMBAT_WINDOW_UPDATE_PLAN.md#plugin-task-assignments), including the GIF schedule. Future use only; existing production and release evidence remains unchanged.

**Plan organisation (2026-11-10):** Two implementation parts under the unchanged MH-001 ID. Part 1 is In progress for asset production; Part 2 non-animation implementation and relevant acceptance are complete; Part 1 and combined visual integration remain In progress. See the Part 2 completion record below. Part numbers do not change priority or prescribe delivery order. Preserve shared resolved-event/HUD integration and existing evidence.

Build an RPG combat screen with the player portrait on the left, opponent portrait on the right, adjacent status panels, location artwork behind the arena, narration at bottom centre, and combat controls along the bottom. Add ordinary attack effects and distinct animations for every master move, Trait-exclusive skill, and awakened signature covered by the supplied design catalogue.

Confirmed revised scope (2026-11-10): the [hierarchy and balancing specification](COMBAT_WINDOW_UPDATE_PLAN.md#lore-based-balancing-and-character-power) now places Sylvanis alone at S+, Takeo and The Crow at S, Ivan and Charles at A+, and the Four Aces, Garrett, Neo, Daniel, Fox, Gordon, Rei and Thirteen at A. Tyler, Samantha, Keisuke, Emily, Alyssa, Minsu and Valentina occupy B; elite guards occupy C and ordinary lower-level guards D. April is a separate tactical specialist, superseding her earlier placement alongside the B-tier fighters. The approved plan defines small, moderate, large and overwhelming gaps, distinct combat roles, temporary peak states and evidence-based matchup limits.

Confirmed Iron Circle scope (2026-11-10): ranks 450–301 D, 300–101 C, 100–11 B and 10–2 low A, still below Rei, the starting #1 A-tier champion. All arena refinements are required: smooth band transitions, competitive rank separate from actual strength, an explicit bout against the actual current champion, preservation of earned titles, distinct contender styles and previews, and separate assessment of arena versus street/group combat. Previously approved alternative objectives, bounded counterplay, restrained sparring, lore-preserving difficulty and authored progression remain required. No gameplay balance changes are claimed released.

Confirmed Richter scope (2026-11-10): [boss placement and refinements](COMBAT_WINDOW_UPDATE_PLAN.md#joseph-richter-boss-placement--confirmed) places his active cybernetic form at low A, moderately below Rei. All boss-fight refinements are approved: weapon/targeting pressure, momentum interruptions, readable committed attacks, punishable recovery and clear counterplay, separate assessment of campaign attrition, and preservation of solo in-person access, victory requirements and save continuity. Ordinary civilian Richter remains unranked. Inspected the existing Headhunter-derived profile, powered-frame dialogue and solo campaign gates; tier tuning and gameplay verification remain pending. This is confirmed planned scope, not a released balance change.

Confirmed lore-balance extension (2026-11-10): add [combat identity and behavioural balance](COMBAT_WINDOW_UPDATE_PLAN.md#confirmed-combat-identity-and-behavioural-balance), identity sheets for every character, and recorded balance reviews for new moves and progression bonuses. Required refinements distinguish power/control/experience, perception/response, observed information, burst/sustained output, defensive mechanisms, group coordination, character-specific AI and willingness/capability. Outcomes must follow resolved mechanics without hidden guaranteed wins or protagonist advantages. Documentation only so far; implementation and verification remain pending.

Confirmed dialogue scope (2026-11-10): [in-character sparring, fight and lesson requests](COMBAT_WINDOW_UPDATE_PLAN.md#in-character-ai-generated-sparring-fight-and-lesson-requests) replace the fixed initiating question with AI-generated speech in the selected canonical/custom protagonist's voice. The recipient responds to that exact line, which remains consistent in display and saved history. Confirmed extension: martial-art lesson requests also reflect the protagonist's personality and relationship with the selected teacher, preserve the selected art and teaching prerequisites, and apply accepted training/time costs exactly once. Preserve selected intent, private-lore boundaries, eligibility, refusal and in-person access. Inspected `combat_dialogue.py`: initiating lines are currently fixed while recipient responses are generated. Implementation and verification remain pending.

Confirmed Trait lore changes (2026-11-10): [Trait revisions and Shinigami trump-card state](COMBAT_WINDOW_UPDATE_PLAN.md#confirmed-trait-lore-revisions-and-shinigami-trump-card-state) establish Shinigami Protocol for Neo and Thirteen, each with an ultra-instinct trump-card state that reacts, adapts and makes the best possible combat choices; War God for Daniel, like his father; and Polymath for April. Reconcile prior traitless descriptions, profiles, dialogue, identity sheets, signatures and saves. Baseline tiers remain unchanged. Shinigami activation after readiness (normally 3–5 meaningful exchanges), four-exchange duration, approximately 20% maximum stamina cost, normal action costs, two-exchange recovery strain, recovery-gated once-per-encounter reuse and temporary A+ effectiveness are now confirmed. Daniel's War God coordination/transitions/contact reading, three momentum levels and stamina-consuming finishers are confirmed; detailed formulas remain to be tuned. Planning only, with no runtime lore or mechanic changes claimed.

Confirmed definition scope (2026-11-10): create and integrate [expanded Trait and ability descriptions](roadmap/COMBAT_ABILITY_DEFINITIONS.md) covering function, applications, limits, forms, shared-power differences and source evidence, plus a detailed move-description contract. The reference is authored; runtime/UI integration and per-action mechanical verification remain pending. Shinigami timing/cost/power targets and detailed War God mechanics are confirmed scope; runtime integration and remaining formula-level tuning are pending.

Confirmed additional lore (2026-11-10): [mana perception and elemental revisions](COMBAT_WINDOW_UPDATE_PLAN.md#confirmed-mana-perception-and-elemental-lore-revisions) redefine True Sight as pure-mana/magical-flow perception and near-perfect Awakened efficiency, with precognition, improved perception/reflexes, enhanced speed/strength application and lower mana drainage; Charles also possesses it. Analysis sees minuscule/microscopic details and branching paths. Conduit gives red-lightning attack power, blue-lightning speed, wind soul damage, fire strength and ice reflex/reaction amplification. Ivan's ice-derived Tranquility grants instant reaction/perception and constant flow; wind-derived Misanthropy allows continued functioning under more damage. Valentina's Deathwind was provided by Ivan as an extension of his wind and explicitly inherits both soul damage and Misanthropy. Expanded definitions and plan updated; runtime reconciliation and gameplay checks are pending.

Confirmed combat identity scope (2026-11-10): [character lore integration](roadmap/COMBAT_CHARACTER_LORE.md) adds established reputations, roles and character presence throughout combat. Sylvanis is the Crazed Demon and the most feared being on the planet; The Crow's personal identity is unknown; Takeo is the Human Siege Engine capable of destroying army platoons alone. Authored directions cover the combat roster and require knowledge-sensitive introductions, invitations, lessons, tactics, reactions and aftermath without invented fame or guaranteed outcomes. Reference complete; runtime integration and verification pending.

Confirmed reputation expansion (2026-11-10): all suggested roster titles, reputations, presence and presentation refinements in the [character combat lore reference](roadmap/COMBAT_CHARACTER_LORE.md) are approved. The Syndicate is the world's largest and most feared organisation; Ivan and the Four Aces have formidable reputations. The Four Aces are considered the world's best at their respective duties, and the Ace of Spades is the world's most feared assassin. Preserve concealed civilian identities behind notorious operational titles, scoped recognition, selective title use and Missing/Remaining Shinigami framing without forced outcomes or tier inflation. Documentation updated; runtime integration and verification remain pending.

### Milestones

#### Part 1 — animations and effects

- [ ] Reconcile the original 227 supplied animation designs and new Shinigami state coverage with current action IDs and mechanics.
- [ ] Add outcome-driven ordinary effects, Reduced Motion, and Fast Combat.
- [ ] Implement and review animations for all master move signatures.
- [ ] Implement and review animations for all Trait skills and awakened signatures, including opponent mirroring.
- [ ] Integrate amplification/form animation layers and persistent visual recipes for generated skills.

#### Part 2 — lore, HUD, systems and all other changes

**Status:** Complete for non-animation scope.

**Progress and evidence (2026-11-10):** [Completion record](roadmap/COMBAT_PART_TWO_COMPLETION.md). Partner ability/state parity, trusted patrol support, April's observed openings, separate escort positions, title/identity recognition, current-force review hooks and remaining acceptance evidence completed. 92 combat, 23 enhanced-combat and 18 Interpol tests pass; 41,040 finite combination checks pass. Fresh/depleted Richter comparison, live custom invitation and compact partner/boss UI reviewed. Crow's four-exchange campaign defeat is preserved. Release: `release-2026-11-10-combat-part-two-completion`. Part 1 owns animations and final combined visual verification; this completion does not claim that work. Patch-note archive-source failure and unrelated story-test mismatch are explicitly recorded in the completion evidence.

- [x] Ship and verify the initial Trait identity migration, numeric arena calibration and resource HUD slice; preserve the broader acceptance checklist below.

- [x] Implement and verify the confirmed Iron Circle rank boundaries in generation and validation, smooth transitions and contenders below Rei.
- [x] Implement arena refinements: preserve entrant strength, explicit championship bouts, distinct contender styles/previews and ruleset-sensitive threat assessment; verify saved ranks, titles and active encounters.
- [x] Implement Richter's confirmed low-A enhanced boss balance and combat refinements; verify his moderate gap below Rei, fresh/depleted entry, counterplay, victory/retry, boss presentation and save continuity.
- [x] Integrate per-character combat identity/reputation and audience recognition across dialogue, tactics, previews and aftermath; verify the full confirmed title roster, apex lore, Crow anonymity, Syndicate/Ace global reputation, Mavis's assassin status, two-layer recognition, mixed audiences and legacy defaults.
- [x] Create source-linked combat identity sheets for every character and combat archetype; verify coverage, ability limits, states and unknown/unranked cases.
- [x] Implement and verify the confirmed behavioural, defensive, information, group and AI distinctions without forced outcomes.
- [x] Establish and complete recorded balance reviews for new/changed moves, generated skills and progression bonuses, including combination exploits, tier impact and save compatibility.
- [x] Reconcile character/guard lore and combat profiles with the confirmed power hierarchy, including specialised roles and form states.
- [x] Implement differentiated balance and verify reproducible matchup outcomes, ability limits, AI behaviour and legacy profile migration.
- [x] Implement and verify alternative objectives, bounded counterplay, specialist roles, labelled sparring restraint, lore-preserving difficulty and authored tier progression.
- [x] Implement and review protagonist-specific AI spar/challenge/lesson requests across combat and hangout flows; verify matching recipient context/history, selected teacher/art, refusal and training rules, once-only lesson effects, generation failure, stale/duplicate results and legacy records.
- [x] Author the expanded Trait/ability reference with confirmed lore separated from proposed mechanics.
- [x] Integrate expanded definitions into identity sheets, ability details, move previews and generation context; verify action mechanics, knowledge boundaries, stable IDs, saves and rendered UI.
- [x] Reconcile confirmed Trait names across lore, profiles, dialogue, previews and identity sheets; preserve unrelated history and knowledge boundaries.
- [x] Implement and verify confirmed Neo/Thirteen trump-card readiness, four-exchange duration, cost, recovery/reuse, temporary A+ effectiveness, reactive adaptation, player control and save migration; visual effects remain Part 1.
- [x] Implement and verify Daniel's confirmed War God coordination, transitions, contact reading, momentum levels/decay and stamina-consuming finishers.
- [x] Reconcile and implement mana-flow True Sight including Charles, microscopic/branching Analysis, Conduit channel amplification, Tranquility, shared Misanthropy and Deathwind soul damage; verify interactions, costs, hierarchy and saves.
- [x] Build the responsive arena layout, status displays, move previews, and narration history.

#### Shared integration and release checks

- [ ] Verify rendered screens, combat outcomes, callback cleanup, save compatibility, and relevant tests.
- [ ] Record actual release behaviour and evidence in patch notes, validate, and export them.

**Dependencies:** Existing combat resolution, action catalogues, portraits, location artwork, in-person stage, and save data. Inventory current interfaces before implementation.

**Completion criteria:** Both parts' acceptance checks pass; every applicable action has a mapped visual treatment; effects accurately reflect resolved outcomes; controls and narration remain readable; accessibility settings and existing saves work; release evidence is recorded.

**Save impact:** Intended to preserve existing encounter and progression data. Custom-skill visual recipes and presentation preferences may require additive defaults; confirm and document the actual migration during implementation. Lore-based rebalancing also requires a versioned stored-profile/encounter compatibility assessment that preserves earned progression, learned moves and custom-character choices.

**Balance planning evidence (2026-11-10):** Recorded the user's hierarchy and reviewed existing ratings, ability limits and relevant character lore. The linked plan adds matchup acceptance work; all suggested balancing refinements and Minsu/Valentina placements are approved. The revised hierarchy, April's separate specialist role, gap definitions and Iron Circle tier mapping are approved. Inspected the current three-band rank generation in `combat.py`; rank cutoffs and all arena refinements are now confirmed. Four-band implementation, numerical balance, April's tactical implementation and remaining roster tuning are pending. Balance implementation, simulations, gameplay checks and UI review remain pending; existing GIF production evidence below does not verify balance.

**Progress and evidence:** GIF asset production started on 2026-11-10. [Batch schedule and coverage](roadmap/COMBAT_GIF_BATCHES.md) preserves the 32-batch schedule and earlier blocked direct-GIF attempt. Batches 01–10 and 12 now contain 86 local 1536x1024 sprite sheets and 512x512 GIFs. The latest [batch 12 manifest](assets/combat/animations/batch-12/manifest.json) records eight Japanese Jujutsu/Wing Chun signatures and full prompts. `python tools/build_combat_batch_gifs.py --batch 12` passed decoding, frame-count, size, duration and loop checks: 900ms action plus 720ms review rest. Its combined preview passed decoding and timing checks. All eight source sheets and the assembled contact image were visually inspected. Exact built-in generator model identity is unconfirmed. Batch 11 remains planned. Patch-note validation passed with 462 entries and export refreshed; no unintegrated assets were labelled as a gameplay release. Runtime action-ID mapping, integration, in-game rendered review, outcome variants, compositing, accessibility and combat checks remain pending.

## MH-002 RPG main menu and character selection

**Status:** Released  
**Added:** 2026-11-10  
**Area:** Main menu, protagonist selection, character previews and integrated character creation  
**Detailed specification:** [Character selection update plan](roadmap/CHARACTER_SELECTION_UPDATE_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/CHARACTER_SELECTION_UPDATE_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Give the main menu an RPG presentation and let players inspect a selected protagonist's portrait, backstory, personal details and awakened abilities before beginning a story. Support existing protagonists and saved custom characters. Selection remains separate from starting or continuing a playthrough.

Approved scope addition on 2026-11-10: Emily begins awakened with her existing Critical Hit ability; align her current lore and dialogue with that starting state. Preserve existing ability limits and use current Ascension/rating defaults as the baseline, without additional power boosts.

Confirmed on 2026-11-10: characters saved through the custom creator appear directly alongside canonical characters in the main roster, including existing profiles. Provide All / Canonical / My Characters filters and the same dossier tabs, with profile identity preserved across duplicate names and multiple stories.

Expanded on 2026-11-10: improve character creation with combat, JobSeek, Bubblegram and authored backstory integration. The specification proposes a staged creator, live dossier preview and explicit review of descriptive choices versus gameplay effects. Backgrounds and starting ranks are now confirmed in the linked catalogue; Path/style/move allocations are now confirmed in the linked combat-kit catalogue; numeric balance remains a design decision.

Confirmed creator scope on 2026-11-10: save/resume unfinished drafts, meaningful JobSeek career choices, backstory-aware dialogue, selectable established criminal backgrounds with actual Bubblegram starting state, and an explicit AI Expand/Rewrite/Format tool for player-written creator text. AI suggestions require review before application. Established criminal starts are committed; the linked catalogue now confirms backgrounds and starting ranks, while numeric balance remains to be finalised.

Approved background catalogue: [Custom career and criminal starting backgrounds](roadmap/CUSTOM_STARTING_BACKGROUNDS.md) records the confirmed backgrounds, careers and starting ranks. Advanced starts are freely selectable without prior unlocks. Add a simple dark selection window with options, rank choices and effect previews. Reputation/heat and other numeric values remain proposed; implementation is pending.

**Final completion (2026-11-10):** The remaining creator, identity, portability, origin and Trait features are implemented. [Completion record, balance evidence and verification limits](roadmap/CHARACTER_SELECTION_COMPLETION.md) supersedes earlier remaining-work reports. Release: `release-2026-11-10-mh002-completion`. Existing stories are not reseeded; restart to load the update.

### Milestones

- [x] Confirm detailed design and reconcile character lore with actual starting combat profiles.
- [x] Align Emily's starting awakened abilities, biography and dialogue lore; verify new and existing story behaviour.
- [x] Build the responsive RPG menu, roster browser and preview tabs; further scaling/accessibility coverage remains part of final QA.
- [x] Integrate backstory, details, awakened profiles and saved custom characters through read-only preview data.
- [x] Include existing and newly saved custom profiles in the main roster; verify refresh, duplicate identities, legacy recovery and persistence independently of story saves.
- [x] Implement integrated creator steps for backstory, combat, JobSeek and Bubblegram, with explicit starting-state review.
- [x] Add persistent draft save/resume and reviewed AI text expansion, rewriting and formatting with cancellation, undo and stale-response protection.
- [x] Add player-controlled fact/wording locks for AI assistance and persistent, reversible draft revision history; verify conflict handling, restore compatibility and draft/story isolation.
- [x] Add autosave recovery, skippable writing prompts, linked completion checklist, selective randomisation and separate inspiration bookmarks; verify recovery, locks, undo and exclusion of unused ideas from dialogue.
- [x] Implement validated character export/import, isolated non-canonical dialogue previews and accessible field explanations/examples; verify compatibility, knowledge boundaries and no gameplay side effects.
- [x] Add session undo/redo, preferred address/pronunciation and identity visibility; complete the full creator usability pass.
- [x] Implement meaningful employment starts, established criminal presets and backstory-aware dialogue with appropriate knowledge boundaries.
- [x] Integrate progressive career/backstory combat tiers with noticeable power, refinement, martial skill and fight IQ gains; verify all tier/rank mappings, non-duplicated bonuses, Path/move consistency and preview/start equality.
- [x] Integrate structured Trait review, specialisation, tier-aware previews, one origin signature for eligible Veteran-and-higher builds, kit review and isolated in-person practice; verify validation, once-only seeding and workshop/save isolation.
- [x] Add signature intent controls, resolver-backed interaction explanations, authored work/exploration Trait actions and draft Trait-change comparison; verify role/domain validation, costs/outcomes, knowledge boundaries and save isolation.
- [x] Seed approved Path stages and exact learned martial kits for all seven tiers; verify no automatic all-moves grants, valid prerequisites and legacy-save preservation.
- [x] Build the dark options-selection window and verify all approved advanced starts, including low-A Exceptional Veteran across civilian/independent/faction backgrounds, are available to a new player without unlocks.
- [x] Extend profile persistence and once-only story setup; verify legacy profiles, private-history boundaries and isolation from existing playthroughs.
- [x] Preserve Continue, story library, creator, gallery, patch notes and account/audio access.
- [x] Verify keyboard navigation, spoiler boundaries, rendered states, preview isolation and save compatibility.
- [x] Record implemented behaviour and actual checks in patch notes; validate and export.

**Dependencies:** Existing start screen, playable roster, authored character references, combat profiles and Path, custom character library, save library, portraits and shared theme. MH-001 artwork may be reused where suitable. Menu/editor work can proceed independently; final starting-combat calibration depends on MH-001’s shared balance scale and matchup contract, not completion of all animation assets.

**Completion criteria:** Every selectable protagonist has a readable preview; all confirmed creator features and background/rank options work end to end; new-story and saved-story information are distinct; browsing does not mutate stories; existing entry points and saves remain usable; all linked acceptance checks and the integration-review scenarios pass.

**Save impact:** Menu browsing remains read-only and preferences stay separate from story saves. Emily's updated lore will affect current character context; audit whether older stored combat profiles need a compatibility correction. Preserve earned progression and story history, require no story reset, and document actual migration behaviour during implementation.

Creator extensions require optional, versioned profile fields with legacy defaults and story-owned snapshots. Apply new starting choices only at new-story creation; preserve existing jobs, affiliations, finances and progression on reload. Verify all new fields survive validation and library round trips.

**Additional planning evidence:** Inspected custom profile validation/background/registration, creator fields, JobSeek progression, Bubblegram progression and established-role rules. Identified the need to connect descriptive occupation to explicit employment choices and extend the fixed newcomer biography. Implementation and related checks remain pending.

**Confirmed refinement (2026-11-10):** Locked facts for AI expansion and draft revision history are required scope. Persist player-controlled locks, review generated conflicts, invalidate stale responses, and provide previewable/reversible draft restores without changing existing playthroughs. The user also approved all five subsequent suggestions: autosave recovery, optional/skippable writing prompts, a section completion checklist, selective randomisation and inspiration bookmarks. Remaining suggestions are explicitly separated in the specification. Implementation and verification remain pending.

**Further confirmed scope (2026-11-10):** Character export/import, non-canonical dialogue preview and field explanations/examples are now required. The specification includes package validation and conflict handling, explicit private-content export choices, preview isolation from gameplay/memory and accessible dark help surfaces. These features remain planned, not released.

**Earlier progress and evidence:** Implementation started 2026-11-10. The menu/dossier, stable profile library, draft/recovery/history/undo, optional backstory fields and initial career/criminal/combat origin picker are implemented. [Implementation evidence and remaining scope](roadmap/CHARACTER_SELECTION_IMPLEMENTATION.md) records actual tests, numerical decisions, save impact and required unfinished features. MH-002 remains In progress.

**Follow-up implemented (2026-11-10):** Added lore-based two-paragraph biographies for all 28 playable canonical characters; corrected sourced ages, occupations, birthdays, heights and MBTI, including Garrett/Rei/Ivan's underground jobs. Genuinely unknown dates/heights remain unknown; three newly authored MBTI interpretations are labelled. Added creator revision pin/unpin and fixed oldest-revision restore at the retention limit. Nine selection and eleven custom-profile tests passed; selection, start, dark-theme and patch-note UI smokes passed; wide/compact and pinned-history renders inspected. The known missing historical screenshot still fails one patch-note test. See detailed evidence for source boundaries and remaining MH-002 work. Scoped release: `release-2026-11-10-character-biographies-and-revision-pins`; no story migration or NPC knowledge changes.

**Further implementation (2026-11-10):** The Four Aces now show their exact Syndicate specialist status alongside public work. Added six-step creator navigation, contextual help, live starting-profile tab/checklist, editing a selected reusable character with stable identity and Save as new character, stale-profile/draft checks and Save draft as copy, manual/recovery comparison with saved editor step, and read-only Saved progress in Story library. Thirty-three focused unit tests and selection/creator/save-library/start/dark-theme/patch-reader UI smokes passed; compact and interactive renders inspected. The known historical screenshot test failure remains. [Detailed evidence and limits](roadmap/CHARACTER_SELECTION_IMPLEMENTATION.md#staged-creator-profile-editing-and-saved-previews--2026-11-10) tracks remaining scope; MH-002 remains In progress. Scoped release: `release-2026-11-10-staged-creator-and-profile-editing`.

**Historical planning evidence:** Planning review on 2026-11-10. Inspected `start_ui.py`, `playable_cast.py`, `combat_profiles.py`, `combat_path.py`, custom protagonist integration and relevant test names. The user resolved the Emily lore/combat-profile discrepancy in favour of starting awakened abilities and requested matching lore; this is now committed update scope. No runtime implementation or UI verification has been performed for MH-002. Optional suggestions in the specification are not committed scope.

**Plan integration review (2026-11-10):** Confirmed all four latest additions (undo/redo, preferred address/pronunciation, identity visibility and usability review). Reconciled save/start flow, free advanced starts versus discovery gates, optional headings and overlapping recovery/preview concepts. The main plan now defines shared data contracts, dependency order, acceptance scenarios and remaining balance/schema decisions. Documentation checks only; implementation and gameplay verification remain pending.

**Combat starting-power refinement (2026-11-10):** Career and recognised backstory experience now contribute progressively to starting combat ratings. Established faction leaders must start noticeably stronger than specialists and members. The background catalogue now confirms seven experience steps through low-A Exceptional Veteran plus progressive civilian-career contributions, with separate awakened eligibility and coherent Path/learned-move setup. Per the user’s follow-up, future stats must use MH-001’s lore-based balance plan. The temporary legacy 0–100 creator table and fixed point bonuses were withdrawn; exact values and lore-tier placements require shared calibration. The multi-tier behaviour is confirmed. This supersedes earlier wording that separated career seniority from combat stats.

MH-002 confirmed hierarchy follow-up (2026-11-10): the user approved the starting-tier placements and added freely selectable Exceptional Veteran at low A. Seven steps now span lower D, upper D, lower C, upper C, lower/mid B, upper B and low A. The catalogue includes confirmed Syndicate/Shinokami, street-crew and experienced-civilian mappings. Low-A experience is available without prior unlocks across civilian, independent and faction starts, while preserving selected organisational rank and granting no arena title or canonical powers. Exact numerical calibration remains pending under MH-001.

MH-002 combat-kit design follow-up (2026-11-10): [Starting Path stages, martial arts and learned moves](roadmap/CUSTOM_STARTING_COMBAT_KITS.md) records approved stages, style slots and starting move allocations for all seven confirmed combat tiers. Includes catalogue-backed examples, a Totality low-A Exceptional Veteran kit, unawakened/master restrictions and explicit prevention of automatic all-moves seeding. The user approved these kit details; numerical thresholds and matchup checks remain under MH-001. The user also approved all six Trait/package enhancements: structured builder, tier-aware preview, specialisation, reviewed starting signature for eligible Veteran-and-higher builds, kit review and isolated in-person practice. The user additionally confirmed signature intent controls, interaction explanations, authored work/exploration Trait uses and Trait change comparison. Source/catalogue inspection only; implementation and gameplay verification pending.

**Scoped canon integration (2026-11-10):** [Crow address and deference canon](roadmap/COMBAT_CHARACTER_LORE.md) now reaches shared speaker references and per-turn guidance: Aces use “master”, Ivan “Crow”, and Sylvanis “Mr. Crow”, “Bird-man” or “Bro”. Offended Aces hesitate to act given his position without changing command exceptions. New seven-speaker regression passed; conversation suite 29/32 passed (unrelated preference/audience/portrait data failures); patch-note suite 5/6 passed (missing historical screenshot). No UI or save migration; live generated wording unverified. Scoped release `release-2026-11-10-crow-address-canon`; broader MH-001 scope remains unchanged.

## MH-003 Guard update Part 2: dialogue, recognition and contact restrictions

**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person guards, dialogue, organisational recognition and contact eligibility  
**Detailed specification:** [Guard update Part 2 plan](roadmap/GUARD_UPDATE_PART_2_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/GUARD_UPDATE_PART_2_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Make present guards approachable through the in-person window, with dialogue guides for all 15 built-in types and three custom categories. Guards respond to the player's and other characters' current organisational ranks and roles, distinguishing own members, outside members, outside leaders and civilians while respecting recognition and confidential identity boundaries. Prevent guard hangouts from adding personal contacts and safely reconcile existing accidental contacts. All six suggested refinements are confirmed: duty-aware topics, readable warning escalation, visitor credentials/appointments, limited post memory, individual voice variation and supported command menus.

**Confirmed hierarchy clarification (2026-11-10):** Established high command has absolute authority over its defined subordinates, overriding ordinary post/department restrictions. Ivan and Sylvanis can each command any Syndicate member except the Four Aces. The Aces do not command guards, but receive fear and undying respect. Joseph Richter retains absolute Blackstone control. These examples establish a general command/exception matrix requirement for all organisations and custom crews; fear, respect and command are separate. Preserve actual story outcomes and explicit exceptions. The linked plan, dialogue guidance, milestones and acceptance checks now include this scope; implementation and verification are recorded below.

### Milestones

- [x] Inspect guard types, local dialogue/contact paths and existing affiliation helper; author the detailed plan and per-type voice directions.
- [x] Confirm authoritative rank/role sources and implement guard dialogue/context, explicit command/exception matrices and contact exclusion.
- [x] Implement and verify all six approved refinements and absolute-authority/fear/respect distinctions.
- [x] Implement and verify legacy contact cleanup, stable guard identities and save compatibility.
- [x] Run relevant regression and smoke checks and inspect rendered interaction states.
- [x] Record actual released behaviour, save impact and evidence; validate and export patch notes.

**Dependencies:** `organisation_guards.py`, `groups.py`, `town.py`, contact/phone-number routing, faction membership and leadership records, campaign outcomes and dialogue generation. Coordinate rank/role context with MH-002 custom starts and knowledge boundaries with MH-001 character lore.

**Completion criteria:** Every guard type can converse in person with its own guide; player and NPC rank/role reactions follow current known state; guards never gain phone eligibility through interaction or load; ordinary contacts, histories and campaign progression remain intact; acceptance checks in the linked plan pass.

**Save impact:** Additive version-1 guard-social data; idempotent load/sync cleanup archives accidental guard contacts and affected pending phone work. Legitimate contacts and old messages are retained. New conversations are scoped by faction, venue, stable slot/type and day. Restart required; no save reset. Tests used isolated states only.

**Initial planning evidence (2026-11-10, superseded by implementation below):** Source inspection found `groups.open_local` creates an NPC chat and `groups.sync_contacts` creates a direct phone thread for every NPC chat; `town.commit_npc` also invokes syncing. The guard detail already prohibits personal numbers in prose. Reviewed all 15 built-in types, custom categories and `combat.affiliation`; exact authority-source integration remains pending. Documentation only: no runtime reproduction, gameplay tests, UI inspection or release claimed. Existing portrait work remains under its original release ID, `release-2026-11-10-guard-portraits-and-cybernetic-richter`.


**Implementation and release evidence (2026-11-10):** All six refinements, individual guard guides, command/exception resolver, in-person conversation routing and contact migration are implemented. See the linked plan's implementation evidence for precise behaviour and limits. 101 focused tests passed, including 14 new guard tests. Guard-dialogue, guard-portrait, dark-phone (34 pages plus controls), patch-note reader and start-screen (28 previews) smoke checks passed. Inspected command, compact conversation and dark-phone screenshots. Catalogue validation/export passed. Five of six patch-note tests passed; the archive-source test reports missing historical `tests/screenshots/mixtape-art-review-0.jpg`. Live provider wording is unverified; provider tests are simulated. Visitor authorisation is local/day-scoped, referrals and visit requests do not fabricate remote completion, and campaign locks remain authoritative.

**Release record:** `release-2026-11-10-guard-dialogue-and-authority` in [patch notes](patch_notes/catalog.json), available 2026-11-10 after restart.


**Guard dialogue correction (2026-11-10):** A live reproduction found valid provider dialogue with empty narration was rejected and replaced by a stock greeting. `guard_dialogue.validate_reply` now permits narration-free speech; conversation topics use AI generation, malformed responses get one repair attempt, and persistent failures surface through the existing retry UI without saving a greeting. Sixteen guard-dialogue, six hangout-scene and three hangout-texting tests passed; asynchronous guard UI smoke passed and compact speech-only rendering was inspected. Two live Fox/Interpol turns produced contextual answers, recorded in `tests/guard_dialogue_live_check.json`; this supersedes the earlier no-live-sample limitation for this specific scenario only. Release: `release-2026-11-10-guard-ai-reply-validation`. Existing saved greetings are retained as history. Initial approach greetings and explicit desk actions remain authored.

## MH-004 Lived-In Interiors: room-by-room exploration

**Status:** In progress — batches 01 and 02 artwork ready; runtime implementation pending  
**Sequence:** 1 — before MH-016, Ace campaigns and Sylvanis; confirmed 2026-11-11.  
**Added:** 2026-11-10  
**Area:** In-person exploration, interior routines, room presence and privacy  
**Detailed specification:** [Interiors update plan](roadmap/INTERIORS_UPDATE_PLAN.md)

**Plugin assignments:** [Task-level allocations](roadmap/INTERIORS_UPDATE_PLAN.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Expand buildings into connected rooms explored entirely in the in-person window. Characters frequent specific rooms within their current building: Yuriko can relax in her bedroom or the living space in Rei's penthouse. Start with the penthouse pilot, then prove a public workplace/event and a secure faction location before expanding to remaining agreed buildings. The user confirmed this update first on 2026-11-11; unresolved detailed layouts and activities retain their existing proposal status. Complete the agreed interiors release criteria before proceeding to MH-016.

**Residential plan expansion (2026-11-11):** Added proposed connected layouts and room routines for the other core homes, Yeun and Neo/Alyssa households, Tyler's duplex, additional residents, Four Aces and four custom-home options. Preserve actual work/free-day appointments, shared-room witness rules, bedroom privacy, accessible routes, unknown addresses and special HQ/laboratory occupants. Reviewed `world_loop.py`, `hidden_cast.py`, `four_aces.py`, `interpol_cast.py`, `vacant_homes.py` and custom-home routing. Documentation only; status remains Proposed, with implementation and gameplay/UI checks pending.

### Milestones

- [x] Record the proposal and inspect existing home routines and faction-room foundations.
- [x] Confirm interiors as the first queued update in the new sequence and move its status to Planned (2026-11-11).
- [x] Expand residential layouts and character room routines from existing home descriptions and schedules (2026-11-11).
- [x] Draft [public/faction room layouts and event mappings](roadmap/INTERIORS_PUBLIC_AND_FACTION_PLAN.md), including workplace routines, headquarters and legacy event handling (2026-11-11).
- [ ] Complete the indoor event inventory and implement specific-room destinations, room-based attendance and compatible migration for existing meetings/scenes.
- [ ] Integrate all campaign, Bubblegram and JobSeek physical activities with rooms; update NPC schedules/preferred places and expand saved guard rosters across room posts, preserving progression and campaign clearance.
- [x] Review the complete interiors design and resolve shared location, movement, scheduling, work-access, guard-identity and migration contracts (2026-11-11).
- [ ] Implement available-outfit category tagging and automatic beach/gym/home/formal/work wardrobe selection, departure restoration and manual-override/save compatibility.
- [ ] Produce and visually verify a dedicated image for every enabled interior room/view, with complete manifest coverage and no shared generic room backgrounds.
- [x] Compile the [interiors image inventory](roadmap/INTERIORS_IMAGE_INVENTORY.md): 508 interior views across 90 building/group entries, 87 existing reuse candidates and 421 new images; track 20 outdoor views (including Silver Sands placeholder replacement) and two conditional dorm bathrooms separately. Contact-sheet review and asset existence/dimensions/unique-hash checks performed; final image acceptance and runtime rendering pending.
- [ ] Replace all active simple placeholder location art, including arcade, bar, bowling, library, nightclub, mall and beach; verify scene/preview routing and protect finished art from primitive-renderer overwrites.
- [x] Organise all 438 new images into [ten generation batches](roadmap/INTERIORS_GENERATION_BATCHES.md), preserving whole-building groups with per-image paths and manifests; verify exact coverage and no duplicate assignments. Reuse candidates and unresolved layouts excluded.
- [x] Generate and statically review all 48 batch 01 images (2026-11-11); save exact prompts, provenance and verification. In-person integration and rendered verification remain pending.
- [x] Generate and statically review all 41 batch 02 images (2026-11-11); save exact prompts, correction history, provenance and verification. In-person integration and rendered verification remain pending.
- [ ] Complete batch 03 — unfinished and paused at the user's request. Resume only after the user resumes generation. Four Rosa views generated: one accepted and installed, three staged drafts; 47 views not started.

**Placeholder-art correction:** The user explicitly included existing places with simple placeholder art. Seven active locations are identified in the image inventory; six interior replacements are already budgeted, and Silver Sands adds one outdoor image. Remaining-location/fallback audit and full rendered verification are required. Planning only; no images generated or installed.

**Interior artwork requirement:** The user requires each interior space to have its own image. All interiors specifications now make this a release criterion, including corridors, staff/secure rooms and campaign/meeting spaces. Existing art may satisfy one matching space; placeholders do not count as finished coverage. Batches 01 and 02 static artwork are ready; batch 03 is unfinished and paused with partial progress. Generation is paused; final reuse approval and in-person rendered verification remain pending.

**Batch 01 production (2026-11-11):** All 48 assigned images (44 interior, four outdoor) are generated with built-in image_gen, statically reviewed and saved at their planned asset paths. Three unsuitable attempts were replaced. [Production review and gallery](roadmap/interiors-generation-batches/interiors-01-production/PRODUCTION_REVIEW.md) records exact prompts, source provenance and per-image review. `tools/verify_interiors_batch_01.py` passed: 48 PNGs at 1536×1024, complete prompt/manifest coverage, unique file and decoded-pixel hashes, eight original reference files unchanged, all 438 baseline assignments unique, and both planning rebuild scripts safely refuse to erase production records. Patch-note validation passed (498 existing entries) and export refreshed. No release entry was added because no runtime room mapping or player-visible routing was implemented. In-person rendered verification and release remain pending; existing backgrounds and saves are unchanged. Garrett’s existing living-room reuse candidate is actually exterior artwork and needs an explicitly tracked replacement revision before the interiors release.

**Batch 02 production (2026-11-11):** Artwork is complete: 41 generated and statically accepted images. Exact prompts, corrections and static-verification results are preserved in the [production review and gallery](roadmap/interiors-generation-batches/interiors-02-production/PRODUCTION_REVIEW.md). No runtime mappings, saves or player-visible release changed. Lena's and Naomi's original living images show open sleeping areas; reconcile their reuse with planned private bedrooms before integration.

**Batch 03 unfinished and paused (2026-11-11):** Four Rosa views were generated before the pause. Entrance is accepted and installed; sitting room, kitchen and stairway are staged drafts under `media-workspace/interiors-03-paused/`. The remaining 47 batch 03 views and batches 04–10 have not started. [Partial production record](roadmap/interiors-generation-batches/interiors-03-production/PRODUCTION_REVIEW.md) retains prompts and provenance. No more generation until the user resumes it.

**Automatic wardrobe scope:** The user requested location-appropriate automatic outfits when available, including beachwear, gym clothes, homewear and formal wear, with automatic changing out on departure. The interiors plan and integration review now define per-visit selection, destination-aware restoration, safe missing-outfit fallbacks, work/campaign appearance precedence, manual visit overrides and shared portrait/dialogue/camera defaults. Existing outfit availability was inspected; implementation and verification remain pending.

**Integrated review (2026-11-11):** [Cross-system design review](roadmap/INTERIORS_INTEGRATION_REVIEW.md) reconciles both layout specifications. Added mappings for all 12 JobSeek jobs and missing staff areas, fixed-character meeting rules, room-safe campaign privacy, stable legacy guard IDs, local encounters and mission-versioned clearance, explicit schedule priority and zero-additional-minute adjacent navigation. Added end-to-end acceptance scenarios and staged activation gates. Source/document review only; exhaustive runtime inventory, manifests, migration implementation, balance and UI/gameplay checks remain pending. Status remains Proposed.

**Required integration follow-up (2026-11-11):** The user explicitly included campaign buildings/rooms, Bubblegram meetings, JobSeek jobs, room-aware character schedules and preferred places, and more guards stationed across interior rooms. The public/faction specification now requires complete activity mappings, in-person app handoffs, room preference/occupancy persistence and authored larger security manifests with local encounter scope. Guard additions must preserve completed campaign clearance and existing rewards; exact headcounts and balance remain proposed. Source inspection/documentation only; implementation and verification pending.

**Public/faction expansion (2026-11-11):** The user requires established indoor events and meetings to occur in specific rooms. The linked specification proposes public venue and headquarters graphs, NPC work locations and explicit assignments for council, diplomacy, careers, faction shifts, laboratory reviews, appointments and selected campaign scenes. Preserve existing named rooms, timing, attendees, access and outcomes. Completed history must not acquire invented room facts; active/pending saves need idempotent migration. Source review and documentation only; implementation, full event inventory and gameplay/UI verification remain pending. Status remains Proposed.
- [ ] Confirm detailed scope, room layouts, dependencies and movement/time rules.
- [ ] Implement the penthouse pilot, room routines, presence, access and companion behaviour.
- [ ] Implement agreed room activities, artwork and save migration; expand to agreed buildings.
- [ ] Run relevant regression and smoke checks and inspect rendered layouts and interactive states.
- [ ] Record actual delivered behaviour, save impact and verification; validate and export release patch notes.

**Dependencies:** `world_loop.py` home/routine data, `town.py` location and interaction routing, existing in-person scene rendering, `crime_operations.py` room/access rules, dialogue/witness context, companions, saves and room artwork. Preserve MH-003 guard authority and recognition boundaries where interiors overlap guarded sites.

**Completion criteria:** Room exploration and physical activities stay in person; Yuriko independently occupies her bedroom or shared living space; only co-present characters participate or witness; doors and companions respect access; activities and saves preserve room state; the linked plan's agreed acceptance checks pass.

**Save impact:** Proposed additive room state with safe defaults for legacy building locations and compatibility with existing faction-room identifiers. Preserve invitations, relationships, ownership and assignments. No saves changed during planning.

**Progress and evidence (2026-11-10):** Inspected `world_loop.py` home definitions and Yuriko's daily routine, `town.py` location references and `crime_operations.py` reception/briefing room and access helpers. Saved the conversation proposal as a detailed plan. Documentation only; no runtime implementation, gameplay tests, rendered UI verification or release claimed.

## How to maintain the roadmap





1. Add each requested future update using the [entry template](roadmap/UPDATE_TEMPLATE.md). Assign the next unused `MH-NNN` ID; never reuse or renumber an existing ID.
2. Add a summary row here and a matching detailed entry. Link a separate specification when needed instead of duplicating a long design catalogue.
3. Use **Proposed** for ideas awaiting scope agreement, **Planned** for requested queued work, **In progress** when implementation starts, **Blocked** when a named dependency prevents progress, **Ready for release** after implementation and required checks, and **Released** only after the change is available to players. Use **Deferred** or **Cancelled** when explicitly set aside.
4. Keep the summary status, detailed entry, and linked plan consistent. Update milestones and evidence as work happens. For blocked work, record the blocker and next action. Do not check off work without evidence.
5. Set dates, priorities, or target versions only when actually decided. A roadmap entry does not itself authorize implementation or publication.
6. Keep released and cancelled entries with their stable IDs. Link released entries to the corresponding patch-note entry and record the actual release date only when known.
7. Automatically assign relevant project plugins to specific tasks in every new or materially revised plan and child plan. Follow [the plugin assessment](roadmap/PLUGIN_ASSIGNMENTS.md) and template: name concrete outputs, checks, required/conditional/maintenance use and dependency or pause gates. Explain omitted routes/capability gaps, preserve assignments during document regeneration and record actual execution separately. Do not create unrelated media work or claim retroactive plugin use.

All updates must follow [AGENTS.md](AGENTS.md): in-person activities stay in the in-person window, phone surfaces remain dark, and implemented player-visible changes receive validated patch notes. Documentation-only roadmap maintenance is not a gameplay release.


## MH-004 Narrated campaign and hangout actions

**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person campaign and hangout narration  
**Detailed specification:** Action selections belong in the narrator area, with Game Master descriptions; genuine spoken dialogue retains speech bubbles.

**Plugin assignments (future maintenance only; assigned 2026-11-11):** Released status and historical evidence remain unchanged. Context Guard applies to complex/resumed work with actual hook evidence; follow the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md).

| Specific maintenance task | Assigned plugin / workflow | Required verification |
| --- | --- | --- |
| Narrator action descriptions versus spoken dialogue | Story Skills + Writer's Loop | Preserve the actual selected action/result and character voice; keep physical actions in the in-person narration area. |
| Narration/speech routing and authoritative action regressions | falsegreen-skill | Assert correct destination and actual one-time state effects; run affected campaign/hangout checks and inspect the rendered action flow. |

These allocations have no new execution evidence; run and record the relevant checks when a maintenance task is requested.

Campaign investigative choices now carry explicit action metadata. The configured AI provider generates a brief Game Master description asynchronously when the action beat is displayed. Saved generated descriptions are reused; failed requests retain the selected action and authored context with Retry narration. Continue remains available and only the authoritative campaign handler applies outcomes. Legacy active campaign choices and prefixed hangout actions receive compatible display handling. Hangout attack history is marked as action; solo, group and resident prompts explicitly place action descriptions in narration.

### Milestones

- [x] Confirm scope and affected campaign/hangout routes.
- [x] Implement action metadata, narrator presentation, asynchronous generation, retry and stale-result rejection.
- [x] Run feature checks and inspect campaign-action and attack-result screens.
- [x] Document save impact and release evidence; validate and export patch notes.

**Dependencies:** Existing in-person canvas, configured AI provider and authoritative campaign handlers.

**Completion criteria:** Action selections have no player speech bubble; spoken lines remain speech; AI narration cannot commit campaign progress; stale results are discarded.

**Save impact:** Restart required to load code. Existing progress and histories remain compatible. Active legacy campaign choice labels are normalized on display. Generated descriptions are saved with their beats; no destructive migration.

**Progress and evidence:** Eight campaign-dialogue, six hangout-scene, ten combat-dialogue, nine major-campaign and three hangout-texting tests passed. Campaign, hangout, combat-dialogue, patch-notes and start-screen UI smokes passed with AI/save writes mocked. Inspected `tests/screenshots/script-action-narrator.png` and `tests/screenshots/combat-dialogue-flee.png`. Real provider prose quality was not evaluated. Patch-note unit tests: five passed; historical source coverage still fails on the pre-existing missing `tests/screenshots/crow-contact.png`. Validation/export completed.

**Release record:** `release-2026-11-10-action-narrator` in [patch-note catalogue](patch_notes/catalog.json), available in the local game on restart.


## MH-006 Protagonist-specific Story tab

**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person Stories, guards & gang properties panel  
**Detailed specification:** One Story tab displays only the current protagonist’s personal campaign: Rei’s What Remains, Garrett’s Find Charles and subsequent chapters, or the Fox/Gordon Interpol campaign. Characters without an implemented personal campaign receive an empty state. Reuse existing campaign controls and preserve progression gates.

**Plugin assignments (future maintenance only; assigned 2026-11-11):** Released status and historical evidence remain unchanged. Context Guard applies to complex/resumed work with actual hook evidence; follow the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md).

| Specific maintenance task | Assigned plugin / workflow | Required verification |
| --- | --- | --- |
| Protagonist-specific campaign access and empty-state wording | Story Skills; Writer's Loop for substantial text | Preserve current protagonist/campaign boundaries and existing gates; new route implementation remains in its parent plan. |
| Story tab routing, save/resume and handoff regressions | falsegreen-skill | Test correct route plus absence of other protagonists' stories; inspect player Story and any changed dark phone handoff. |

These allocations have no new execution evidence; run and record the relevant checks when a maintenance task is requested.

### Milestones

- [x] Confirm current story routing and shared campaign controls.
- [x] Implement one Story tab, protagonist routing and existing-entry-point compatibility.
- [x] Verify all four protagonists, empty state, travel, action dispatch and active cases; inspect compact Garrett and Gordon screens.
- [x] Complete regression/UI checks and publish validated patch notes.

**Dependencies:** Existing campaign, Garrett quest and Interpol UI modules; in-person scene and authoritative campaign handlers.

**Completion criteria:** One Story tab, only the current protagonist’s campaign, functional existing controls and no changes to campaign progress or prerequisites.

**Save impact:** No migration or new save fields. Existing progress and evidence retained; restart to load changed UI code.

**Progress and evidence:** New `tests/player_story_ui_smoke.py` passed for Rei, Garrett, Fox, Gordon and Emily’s empty state, including travel, scripted-action dispatch, field partners and active objectives. Inspected compact Garrett and Gordon renders. Existing Interpol and twenty-chapter Garrett UI smokes passed; nine major-campaign, five Garrett-quest and eighteen Interpol unit tests passed. Major-campaign UI smoke also passed. Dark-theme smoke passed across 34 phone pages; patch-note reader and start-screen smoke passed. Catalogue validation/export passed; five of six patch-note unit tests passed, with the existing missing historical `tests/screenshots/crow-contact.png` source reference still failing. The shared scripted-scene smoke helper suppresses optional AI narration requests.

**Release record:** `release-2026-11-10-player-story-tab` in [patch-note catalogue](patch_notes/catalog.json), available in the local game on restart.

## MH-009 Combat textures and training layout

**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person combat, training and statistics  
**Detailed specification:** [Scope and evidence](roadmap/COMBAT_TEXTURE_REFRESH.md)

**Plugin assignments:** [Task-level allocations](roadmap/COMBAT_TEXTURE_REFRESH.md#plugin-task-assignments). Apply the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md) within this entry's existing status, dependencies and pause; assignments are not execution evidence.

Refresh combat surfaces with woven slate panels, stat cards, a split technique browser and clearer command emphasis. Preserve existing encounter mechanics and in-person routing.

### Milestones

- [x] Inspect combat, training, Path, workshop, dossier and invitation surfaces.
- [x] Implement shared textures, stat cards and training layout.
- [x] Run relevant checks and inspect rendered states.
- [x] Record release evidence, validate and export patch notes.

**Dependencies:** Existing Winterfield palette/texture, combat RPG interface and engine.

**Completion criteria:** Readable large/compact layouts; reachable combat/training controls; preserved combat state, save compatibility and in-person routing.

**Save impact:** Restart to load presentation changes; no migration or mechanics changes.

**Progress and evidence:** 119 combat unit tests and nine UI smoke scripts passed; rendered layouts inspected. Catalogue validated/exported. Start-screen selection assertion and historical archive-source failure are disclosed in the detailed evidence.

**Release record:** `release-2026-11-10-combat-texture-refresh` in [patch-note catalogue](patch_notes/catalog.json).

## MH-010 Syndicate guard design refresh

**Status:** Released  
**Added:** 2026-11-10  
**Area:** Syndicate guard artwork  
**Detailed specification:** Clubs: black hood, full-face black military helmet/mask with white clubs insignia, vest under jacket, gun and Awakened energy. Spades: black hooded jacket, full-face mask with white spades insignia, layered cloak cloths/accessories and knife. Affiliate: full-face military outfit, gun and Syndicate chest insignia. Replace all three transparent portraits at their existing paths.

**Plugin assignments (future maintenance only; assigned 2026-11-11):** Released status and historical evidence remain unchanged. Context Guard applies to complex/resumed work with actual hook evidence; follow the [shared workflow](roadmap/PLUGIN_ASSIGNMENTS.md).

| Specific maintenance task | Assigned plugin / workflow | Required verification |
| --- | --- | --- |
| Requested Clubs/Spades/affiliate appearance or dialogue maintenance | Story Skills + Writer's Loop; Bulk BG Remove for needed cutouts | Preserve full-face concealment, insignia, weapons and visible-gesture descriptions; inspect actual conversations and combat. |
| All deployment and legacy guard-profile routing regressions | falsegreen-skill | Run guard/encounter suites and Syndicate smokes; distinguish mocked prompt checks from live model adherence. |

These allocations have no new execution evidence; run and record the relevant checks when a maintenance task is requested.

### Milestones

- [x] Confirm scope, current portraits and existing Syndicate insignia.
- [x] Generate and install all three redesigned RGBA portraits; preserve prompts in the manifest.
- [x] Run guard portrait tests and rendering smokes; inspect the three-portrait slate-background review.
- [x] Record save impact and release evidence; validate and export patch notes.

**Dependencies:** Existing guard portrait resolver and in-person rendering.

**Completion criteria:** All requested equipment and insignia visible; real transparent backgrounds; existing encounter resolution preserved.

**Save impact:** No migration or gameplay changes. Restart to clear cached artwork.

**Progress and evidence:** Four guard portrait tests passed. Existing guard portrait UI smoke and `tests/syndicate_guard_art_smoke.py` passed. `tests/screenshots/syndicate-guard-redesign.png` visually inspected. Five patch-note tests passed; known archive-source failure remains for missing `tests/screenshots/mixtape-art-review-0.jpg`. Catalogue validation/export passed. Exact generation prompts are in `assets/portraits/guards/manifest.json`.

**Release record:** `release-2026-11-10-syndicate-guard-redesign` in [patch-note catalogue](patch_notes/catalog.json).

### MH-010 encounter coverage follow-up (2026-11-10)

Verified the shared portrait routing without changing runtime behaviour. The six-test guard portrait suite passes, now covering all three Syndicate types at all seven Syndicate deployments in conversation, combat and older saved-slot fallback; saved scripted fights without deployment slots also resolve the updated assets. Source inspection confirms Interpol, Garrett chapter and post-story guard fights use the same guard profile/portrait path. `tests/syndicate_guard_encounters_smoke.py` rendered all three types in actual in-person conversations and combat; all six `tests/screenshots/syndicate-{clubs,spades,affiliate}-{conversation,combat}.png` screenshots were inspected and show the updated transparent portraits. Existing release and restart guidance remain unchanged.

### MH-010 description and dialogue follow-up (2026-11-10)

Completed shared appearance descriptions for Clubs, Spades and affiliates in `organisation_guards.py`, used by NPC descriptions and in-person guard dialogue. Instructions preserve full-face masks, hide eyes/hair/facial expressions, describe visible gestures and keep equipment consistent. Combat profiles and resolved-exchange narration use current descriptions, including older saved guard profiles. Eighteen guard-dialogue tests, 23 enhanced-combat tests and guard-dialogue UI smoke passed. Prompt checks use mocked providers; live model adherence was not tested or guaranteed. Existing histories and mechanics remain unchanged; restart required. Release: `release-2026-11-10-syndicate-guard-description-continuity`. Patch-note validation/export passed; five patch-note tests passed and the existing missing historical mixtape screenshot failure remains.
