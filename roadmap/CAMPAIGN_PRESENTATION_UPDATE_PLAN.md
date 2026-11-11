# MH-016 — Campaign gauntlets, map access and visual novel scenes

**Editorial coordination, 2026-11-11:** [MH-019](CAMPAIGN_REVISION_PLAN.md) plans manuscript/compiler cleanup and outcome-preserving narrative revisions before final shot assembly. Preserve stable scenes, saved reading/history and actual encounter outcomes; finish text/era review before producing dependent final artwork. This link does not resume the deferred implementation or paused Rei generation, or alter the interiors-first sequence.

**Related design — 2026-11-11:** [MH-017 flashback areas](CAMPAIGN_FLASHBACK_AREAS_PLAN.md) adds period/room-aware optional historical visits for every campaign protagonist while preserving MH-015. Integrate the existing-campaign areas when this update resumes after interiors; new Ace/Sylvanis areas accompany their own routes. Freeform visits use reusable room scenery and historical portraits; authored campaign sequences retain the per-shot requirements below. This planning link does not resume deferred implementation or image production.

**Required historical references — 2026-11-11:** Every campaign flashback must use the [mandatory character/era reference and dialogue-style pairs](CAMPAIGN_FLASHBACK_AREAS_PLAN.md#historical-cast-and-conversation-authoring-contract), including scripted scenes, historical protagonists and supporting appearances. Scene dialogue, generated conversations and image briefs must agree on the selected era's personality, knowledge, relationships, voice and appearance. Present-day/later-era defaults are forbidden; complete the cast inventory and review the pairs before enabling new content. This planning requirement does not resume implementation or image production.

**Status:** Deferred — paused by user on 2026-11-11; revisit after Lived-In Interiors is implemented.  
**Recorded:** 2026-11-11, Australia/Brisbane.  
**Tracking:** [Roadmap MH-016](../ROADMAP.md#mh-016-campaign-gauntlets-map-access-and-visual-novel-scenes).  
**Scheduling:** Second in the [approved roadmap order](../ROADMAP.md#approved-update-order--2026-11-11), confirmed 2026-11-11: after Lived-In Interiors and before new Ace/Sylvanis campaign implementation. No delivery date or release version assigned. The existing interiors-dependent pause remains in force; this scheduling update does not resume production.

**Production follow-up, 2026-11-11:** The user requested all Rei campaign scene/shot images. [Artwork production record](rei-campaign-artwork/README.md) and [183-shot manifest](../assets/campaigns/rei/manifest.json) track the 35 existing scenes, branches, scripted variants and encounter locations. Preserve adult Rei's exposed tattoos on both arms and the tattoo-free school-era appearance. This advances the art portion only; gauntlets, map rules and reader implementation remain pending. The planning evidence below remains a historical record of the preceding planning task.

**User-requested pause, 2026-11-11:** Stop image production and revisit after the [Lived-In Interiors update](INTERIORS_UPDATE_PLAN.md) is implemented. Preserve the one generated/corrected opening image, 182 pending shot records and all prompts/reference snapshots. Before restarting, reconcile the inventory and images with actual implemented rooms and scenery, including Rei's home; the existing opening needs an interiors continuity review before final reuse. This is a dependency note, not an automatic resume or reminder.

Campaigns should play as connected in-person experiences: enter a story destination through Maps, fight the building's successive opponents without returning to a menu, and read scripted scenes over illustrations composed for each shot. This document records the requested patch and its implementation/verification plan. It changes no gameplay, artwork or saves.

## Plugin task assignments

**Assigned:** 2026-11-11. Deferred. Planning allocations only; implementation and Rei image production remain paused until interiors is implemented and work is revisited under the existing pause.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Inventory travel, encounters, shot branches and historical casts | Story Skills (interactive-fiction/continuity) + Writer's Loop | Map stable scene/shot IDs to actual outcomes, audience, era and room; assemble readable sentence-per-line narration without losing conditional paragraphs or mandatory scenes. |
| Page-flip animation and lifecycle | DESIGN:OS SVG Animation for vector page motion; Pro Motion for local timing/compositing previews | Prototype deterministic transitions with Reduced Motion and cancellation; export a Tk-compatible implementation/asset path. Browser previews alone do not verify the game reader. |
| Per-shot artwork and historical portrait preparation | Story Skills for briefs; Bulk BG Remove only for portrait layers; prompt-to-asset only for local framing assets | Reconcile completed room layouts and character/era references before production. Shot paintings stay opaque; the local plugin set does not generate them. Preserve the paused 183-shot Rei baseline. |
| Map-to-gauntlet-to-reader pilot and legacy migration | falsegreen-skill | Review save/resume, defeat, inter-wave transitions, location reveal/entry/disposition, saved reading cursors and one-time rewards. Run campaign/combat/save suites and dark Maps smokes plus rendered in-person checks when resumed. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Required player experience

| Area | Required change |
| --- | --- |
| Combat in one building | Consecutive campaign guards/opponents form one gauntlet. The player remains in the in-person encounter presentation between opponents instead of closing combat, returning to Story and starting the second guard. |
| Campaign travel | Remove campaign travel from the Story menu. The player finds the destination in Maps, selects it and accesses it through the normal travel/arrival flow. Story remains an objective, journal and recap surface. |
| Hidden or inaccessible destinations | Make a required destination visible and accessible at the appropriate campaign stage. Afterward, the story explicitly determines whether it remains revealed or becomes hidden again, and whether entry remains permitted. |
| Scripted scenes and campaign flashbacks | Use visual novel presentation, with a dedicated illustration of the action for every authored shot/page. A generic location backdrop with standing portraits is not sufficient coverage. |
| Novel text | Replace the separate novel reading panel with the existing in-person narration window. Display each sentence on its own logical line, retaining the complete prose, dialogue and inner thoughts. |
| Shot changes | Animate a page flip when moving between shots, in both forward and backward reading directions. |

These requirements apply to existing campaign content and to future campaign work, including [MH-012's four Ace campaigns](ACE_CAMPAIGN_UPDATE_PLAN.md) and [MH-014's Sylvanis campaign](SYLVANIS_CAMPAIGN_UPDATE_PLAN.md). Their plot, character and outcome requirements remain in force. This plan supersedes their older Story-menu travel and separate-reader assumptions only.

All physical travel arrival, entry, combat and scenes use the main in-person window. Maps may provide the dark phone navigation controls; selecting a destination must hand physical activity back to the in-person view. Preserve [MH-015's embedded flashback visits](../ROADMAP.md#mh-015-flashback-visits-in-the-main-window). Freeform conversations in optional historical visits are not automatically a new authored campaign shot catalogue; scripted campaign sequences use this plan wherever they are launched.

## Current implementation and integration points

Source inspection on 2026-11-11 found the following. This is an integration map, not a claim that the future behavior exists.

| Current source | Observed behavior and planned integration |
| --- | --- |
| `campaign_ui.py`, `charles_quest_ui.py`, `interpol_ui.py`, `campaign_prose_ui.py`, `post_story_ui.py` | Campaign and related story boards expose direct travel controls. Inventory every campaign entry point, including mandatory memories, optional story visits, protection follow-ups and alternate case boards, so another menu cannot retain a campaign travel shortcut. |
| `organisation_guards.py`, `rei_story.py`, `garrett_chapters.py` | Mission defeats are scoped and recorded; `begin()` starts the first remaining guard. Use these stable scope/slot IDs to assemble ordered campaign gauntlets. |
| `combat.py`, `combat_rpg_ui.py`, `combat_ui.py` | `combat.close()` archives the result and invokes campaign/guard resolution; `close_encounter()` then leaves the view. Insert an idempotent next-wave handoff after authoritative resolution rather than bypassing it. |
| `phone_map.py`, `city_map.py`, `town.py`, `world_loop.py`, `hidden_cast.py` | Maps filters places through `visible_place()` and available map points; travel performs further access/party checks. Coordinate discovery and entry policy across the map and travel backend. A marker alone cannot make a gated destination reachable. |
| `campaign_prose/catalog.json`, `campaign_prose.py`, `campaign_dialogue.py` | Prose is currently assembled into pages using paragraph/word limits and committed through existing campaign handlers. Add stable authored shots without losing branch conditions, selected actions, final-page gates or reading history. |
| `campaign_prose_ui.py`, `hangout_ui.py`, `game.py` | The reader overlays the hangout with a separate text panel and a backdrop/portrait illustration, hidden at compact widths. The normal narration region pages a small number of lines. Replace the campaign reader presentation and adapt narration sizing/paging so the image and all text remain usable in compact layouts. |
| `campaign_flashbacks.py`, `flashback_visits.py`, `flashback_visit_ui.py` | Preserve historical appearance overrides, mandatory memory gates, paused present-day time, saved visit resume and return to the current world. |

## 1. Continuous building gauntlets

The intended flow is **enter the building in person → scene/briefing if authored → guard 1 → guard 2 → remaining waves/boss if authored → building outcome**. Between opponents, an inline result and a Continue control can allow the player to read and prepare; they must not have to leave the encounter and reopen Story. Never let an animation start an attack or consume a player turn automatically.

- Define each gauntlet by campaign, chapter/objective, building and ordered encounter IDs. Group by actual building identity, not faction or mission scope: separate Hamayashi properties are separate visits, while authored areas within one headquarters can belong to one building sequence.
- Include an authored room transition, locked door, conversation or boss introduction inside the same in-person sequence when required. Do not skip evidence, choices, prerequisites or mandatory flashbacks to reach the next enemy. Coordinate room IDs with the [interiors plan](INTERIORS_UPDATE_PLAN.md) without requiring that entire update to ship first.
- Commit each resolved encounter once through the existing combat/guard/campaign handlers, then select the next undefeated required opponent. Only the final required encounter completes the building objective. Re-rendering, double-clicking, loading or replaying history must not grant duplicate victories, rewards or Path progress.
- Preserve existing resolver mechanics, companion eligibility, knockout/recovery and authored outcomes. Scripted survival/defeat objectives, including Interpol's Crow encounter, must retain their own success conditions; a gauntlet cannot turn them into capture/victory objectives.
- Defeat, concession or an allowed withdrawal stops advancement. Preserve legitimate completed-wave records according to the campaign's retry rules and resume at the correct point. Exiting/reloading must not clear uncleared waves or replenish mission opponents as daily patrols.
- Keep ordinary patrol, sparring and Combat Circle encounters outside automatic campaign chaining unless separately requested.

**Proposed balance default to review during the pilot:** carry player and eligible ally health, stamina and mana between waves, with recovery only at authored breaks; preserve the existing lifecycle of short-lived effects. First document the current per-fight resource resets and compare a full building run. Continuous-screen flow is required; any additional difficulty change, rest checkpoint or reward adjustment must be explicit and recorded, not an accidental result of chaining fights.

## 2. Maps, discovery and story-controlled access

The intended flow is **read the objective/directions → open Maps → find and select the revealed destination → travel → arrive/access it in person → begin the eligible scene or gauntlet**. An Open Maps shortcut may open the general map, but must not travel, auto-enter or automatically select the objective in place of the player's search/selection. Recognizable place names, districts and authored directions keep the route discoverable.

- Replace campaign Travel/Visit buttons in Story and equivalent campaign boards with destination information and the Maps handoff. At-location Begin/Continue controls may remain, with backend location checks. Being already present at a valid destination never requires a redundant trip.
- Inventory every required venue, its map coordinates, display name, building/room relationship, reveal trigger and entry conditions. Story-required locations become visible and actually reachable when due, including locations currently blocked by unconditional hidden-place rules.
- Separate **map visibility**, **physical entry permission** and **historical knowledge**. Learning where somewhere is does not automatically grant permanent entry, contacts, identities or faction membership. A hidden destination must not leak through search results, marker labels, tooltips, route previews or stale selection cards.
- Add narrowly scoped story grants rather than globally disabling security checks. Reconcile campaign grants with existing legitimate home/faction/case access and companion/solo requirements. A story grant that expires must not revoke a separate valid access right.
- Re-evaluate access on reveal, branch choice, objective completion, failure/suspension and load. Refresh an open map immediately. Validate at trip start and entry/arrival so a stale selection cannot bypass an expired grant; if access ends while inside, provide the authored safe exit before removing re-entry.
- Historical-only locations remain in the isolated flashback setting. Do not add a childhood venue to the present-day map solely because the player viewed a memory.

Each destination needs an authored disposition; there is no universal permanent-unlock rule:

| Story state | Map behavior | Entry behavior |
| --- | --- | --- |
| Before discovery | Hidden unless independently known | Existing legitimate access only |
| Required campaign objective | Revealed with a usable map destination | Grant the access needed for that objective; enforce authored party and prerequisite rules |
| Afterward: keep revealed and open | Remains visible | Keep the authored ongoing access |
| Afterward: keep revealed but restricted | Remains visible with an appropriate locked explanation | Revoke temporary access while preserving independent rights |
| Afterward: rehide | Remove the campaign reveal and cached map details, unless independently visible | Revoke the temporary grant; retain other legitimate access and factual completed history |
| Later story revisit | Reveal/reactivate when the new objective requires it | Apply the new scoped grant; no dead end from an earlier rehide |

The exact disposition for each existing and future venue is an authoring milestone, not a newly invented campaign ending. Existing completed saves must derive the correct disposition from their recorded outcome.

## 3. Shot-based visual novel presentation

Use the existing main in-person stage for the illustration, with narration below and accessible Previous/Continue/choice controls. No separate novel panel or modal reading window remains for scripted campaigns. Returning to free conversation restores the usual in-person layout cleanly.

- Give every authored shot/page a stable ID, scene ID, branch conditions, ordered sentence content, illustration asset, viewpoint, era, location and cast/appearance references. Keep script boundaries intentional rather than regenerating them from a word-count threshold or window width.
- Compose each illustration around what is occurring in that shot: action, framing, expressions, props, location and era. Match established identities and the project's semi-realistic illustrated character direction. Coordinate with [MH-013 artwork](PORTRAIT_ARTWORK_UPDATE_PLAN.md); portrait production alone does not supply this scene-art requirement.
- Produce an image manifest with scene/shot coverage, branch variants, references, prompt/source records, asset paths and review status. The same shot may reuse its image on reread; distinct shots require their own deliberate illustration. Inventory determines the artwork count; no arbitrary production total is promised here.
- Keep images free of baked-in narration and UI text. Preserve readable narration, important action and faces under scaling/cropping, including compact windows. Unlike the current compact reader, the new layout must keep the scene illustration visible.
- Preserve the existing prose's depth, inner thoughts, dialogue, chronology and private knowledge. Split and stage content without replacing long passages with summaries. All novel prose appears in narration; character attribution and thought styling must remain understandable without duplicate speech bubbles repeating it.
- Treat one sentence per line as one sentence per logical text row separated by a newline. Long sentences may soft-wrap to the available width. Do not clip text or force horizontal scrolling to meet the rule. Review abbreviations, initials, quotations, ellipses and intentional fragments rather than splitting blindly on every period.
- When a shot contains more text than fits, page or scroll its narration while retaining the same image. Finishing a narration chunk is distinct from moving to a new shot. Advance to the next shot only on the player's action, retaining the existing required reading/choice gates.
- Retain font sizing, current-position resume, scene history and recap. History remains read-only and must never rerun campaign actions. Historical cast/clothing and world restoration must stay correct across forward/back navigation, scene exits and saved resume.
- Package reviewed images for deterministic playback. Do not require live image generation to advance a scene. A missing/corrupt asset needs a themed recoverable fallback that preserves text and progress; fallback is not accepted as finished artwork coverage.
- Any optional generated narration must preserve the authored facts, selected action and shot continuity, use the same sentence layout, and not gate progress on a network response. Audit whether to retain that control in the new reader during the pilot.

## 4. Page-flip animation and lifecycle

Animate the outgoing image/page turning to reveal the incoming shot, with direction matching Previous or Continue. Advance the matching narration and page indicator together at a defined transition boundary. A flashback-to-present transition uses the same shot framework with clear era context.

Proposed implementation: a short, nonblocking canvas animation with preloaded adjacent artwork, a reduced-motion/instant-transition preference, and keyboard equivalents. Coalesce repeated inputs while a flip is running; they must not skip unread shots or duplicate final commits. Save a stable shot/cursor boundary, never an intermediate animation frame. Resize, navigation, closing the view and loading another save cancel callbacks safely. A redraw, text scroll, font-size change or narration chunk within one shot does not trigger a page flip.

## Save contract and migration

Planning has no save impact. Implementation is expected to add versioned, protagonist/campaign-scoped state for gauntlet position, encounter-resolution markers, location grants/dispositions and stable shot reading position. Final field names and migration code remain to be designed.

Preserve chapter/evidence/branch completion, mission guard victories, current fights and resources, companions, relationships, contacts, location knowledge, private disclosures, history and reflection choices. Derive old-save defaults from authoritative progress, not a blanket unlock or campaign reset. An old active fight must resume before selecting another wave; a finished-but-unclosed fight must be committed once. Reconstruct remaining waves from existing scope/slot victories. Map old page cursors to stable shots with a documented fallback that does not repeat a reward or force the player to restart a chapter.

Keep historical world snapshots isolated from present-day travel, clock, people and access. Story history rereads never rehide/unhide locations or mutate the present. Save/load during a transition restores a coherent image/text/choice state. Verify migrations repeatedly on copies of legacy and current fixtures; do not use player saves as test fixtures. Record actual restart/migration guidance only after implementation checks.

## Delivery milestones

- [x] Record the user requirements and inspect the existing Story, guard/combat, map/access, prose/narration and flashback integration points.
- [x] Define observable acceptance cases, migration concerns, artwork coverage and the implementation sequence.
- [ ] Inventory all campaign travel entry points, building/room encounters, location reveal/entry/disposition rules and conditional script shots, including Garrett, Rei, Fox/Gordon and campaign follow-ups.
- [ ] Implement one representative pilot: map reveal/access, at least two same-building opponents, an inter-wave story beat, one present scene, one flashback, unique shot images, narration text and page flips; verify save/resume and defeat before expanding.
- [ ] Implement shared gauntlet and location policy support; convert all existing campaign travel controls and required sites.
- [ ] Author every in-scope shot/branch, produce and review its image, and replace the campaign reader with narration-based presentation.
- [ ] Convert existing campaigns and document the shared contract for MH-012/MH-014; complete migration and artwork coverage checks.
- [ ] Run gameplay/regression/UI checks and visually inspect the required layouts and interactive states; correct failures and record remaining limits.
- [ ] Publish actual implemented scope, access instructions, save impact and evidence; validate/export release notes, then advance the roadmap status when available to players.

## Acceptance and verification plan

These are future checks, not passed results. Extend the existing relevant suites where their assertions encode the old navigation/reader design, while preserving outcome and save assertions.

| Area | Observable acceptance cases | Existing suites to extend/run |
| --- | --- | --- |
| Gauntlet | Two or more guards in one building without a Story/menu round trip; room/boss beats retained; separate buildings still need Maps; defeat/concede/retry; ally and resource policy; once-only rewards; reload before/after a wave commit | `test_major_campaigns.py`, `test_combat.py`, `test_combat_rpg_ui.py`, `test_campaign_prose.py`; `major_campaigns_ui_smoke.py`, `combat_rpg_ui_smoke.py` |
| Travel/access | No direct campaign travel in any board; Maps find/select/arrival; required hidden site becomes reachable; keep-open, keep-visible/locked and rehide dispositions; later revisit; stale selection; overlapping independent rights; solo/partner rules; safe exit | `test_phone_map.py`, `test_major_campaigns.py`, `test_interpol.py`; `phone_map_smoke.py`, `player_story_ui_smoke.py`, `major_campaigns_ui_smoke.py` |
| Visual novel | Every reachable shot/branch has reviewed matching art; complete prose uses sentence rows; long/quoted sentences readable; image visible at normal/compact sizes; choices/history/font controls; no separate novel reader | `test_campaign_prose.py`, `test_campaign_dialogue.py`; `campaign_prose_ui_smoke.py`, `campaign_dialogue_ui_smoke.py` plus a shot-manifest coverage check |
| Flashbacks | Correct era/cast/art, isolated present, mandatory completion gates, present-day restoration and embedded visit resume | `test_campaign_flashbacks.py`, `test_flashback*.py`; `campaign_flashbacks_ui_smoke.py`, `flashback_visits_ui_smoke.py` |
| Animation/save | Forward/back flips, rapid clicks and keys, reduced motion, resize/close/load cancellation, no duplicate final action, stable image/text on reload, legacy cursor migration | Focused controller/state checks and rendered campaign smoke cases added during implementation |
| Phone and release | Dark map marker/cards/search/results/locked/error/disabled states; no native light prompts or popups; in-person handoff; release catalogue accurate | `phone_dark_theme_smoke.py`, relevant map smoke, `patch_notes_ui_smoke.py`, `start_ui_smoke.py`, patch-note validation/export and unit suite |

All filenames in this table are under `tests/`. Reuse `winterfield_ui.py`, `phone_theme.py`, existing phone/arcade styles and embedded `phone_dialogs` for any phone prompts. Inspect normal/compact renders, loading/errors, focus/hover/pressed/disabled controls, access changes with Maps already open and both page-flip directions. Record actual command outcomes and visual evidence; do not equate a screenshot capture with visual review.

## Planning evidence — 2026-11-11

Read `AGENTS.md`, `ROADMAP.md`, `roadmap/UPDATE_TEMPLATE.md` and `patch_notes/AUTHORING.md`; reviewed the source integration points above and the existing MH-012/MH-014 plans. Created this specification and the matching roadmap entry; linked the shared presentation requirements from the two queued campaign plans. Added catalogue record `plan-2026-11-11-campaign-presentation` as a **Development report**, visible when **Include original chat reports** is enabled. It is not a gameplay release and the default curated export excludes it.

Actual planning checks:

| Check | Result |
| --- | --- |
| Roadmap/document consistency | Passed: one MH-016 summary row and detailed entry, Planned status, existing local plan links, referenced test files/patterns and Ace/Sylvanis cross-links. |
| `python patch_notes.py validate` | Passed: 489 entries. |
| `python -m unittest discover -s tests -p test_patch_notes.py -v` | Final run: five passed, one failed. The remaining archive-source check references the existing missing `tests/screenshots/mixtape-art-review-0.jpg`. The initial run also exposed a first-entry assumption when the new report preceded curated releases; grouping it with Development reports resolved that failure without changing runtime/tests. |
| Existing catalogue preservation | Passed: all 488 prior entry IDs and content hashes unchanged; only `plan-2026-11-11-campaign-presentation` added. |
| `python patch_notes.py export` | Completed: refreshed `patch_notes/PATCH_NOTES.md`. The planning report remains excluded from the default curated export. |
| New planning record | Passed: searchable with reports enabled, excluded from default release selection/export, and all four source paths exist. |

No gameplay code, image generation, UI rendering or campaign test run is claimed for this planning task. The archive-source failure remains disclosed; no replacement historical evidence was fabricated. UI smoke checks are reserved for implementation because this task changes planning documents and the catalogue only.
