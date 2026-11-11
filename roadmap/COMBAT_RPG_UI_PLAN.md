# Combat RPG interface revamp

**Roadmap ID:** MH-007  
**Status:** Released locally on 2026-11-10 — implemented and visually verified; restart to load. See [implementation evidence and verification limits](COMBAT_RPG_UI_EVIDENCE.md).  
**Added:** 2026-11-10  
**Area:** In-person combat presentation

## Plugin task assignments

**Assigned:** 2026-11-11. MH-007 is Released. Future maintenance must use the authoritative engine and coordinate with MH-001 Part 1.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Arena HUD, drawers, resource/status symbols and compact layout | prompt-to-asset only for needed local assets | Validate/export icons or frame assets; reuse Winterfield/combat styles and inspect readability at supported sizes without obscuring combatants. |
| Animation handoff into the arena | DESIGN:OS SVG Animation / Pro Motion through MH-001 Part 1 | Reuse the Part 1 effect contract rather than duplicate production; preserve resolved-event ordering and in-person rendering. |
| Control, inspect/history, partner/boss and navigation regressions | falsegreen-skill | Review real interaction and state assertions; run combat RPG UI and affected combat suites/smokes, including cancellation and large-text/compact states. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Requested direction

Create a substantially more RPG-like combat screen, with much larger player and opponent portraits standing in front of the location artwork, similar to the hangout window. The arena should be the visual focus, with readable combat information and deliberate action selection around it.

This is a new, standalone plan, as explicitly requested. MH-001 remains unchanged. Coordinate with its existing HUD and animation work when implementing: reuse authoritative combat data, portrait assets and effect hooks rather than creating a second combat system. This plan defines the new screen composition and interaction design; it does not change combat balance, lore or animation production scope.

## Current implementation evidence

Source inspected on 2026-11-10:

- `combat_selection_ui.py`: opposing portraits are requested at 108 × 128 inside a horizontal information rail. Location artwork is rendered in a separate 48-pixel strip. Resources, intent, narration and action selection already exist, but the screen is predominantly stacked controls.
- `hangout_ui.py`: `HangoutCanvas` draws location artwork with large, bottom-anchored portraits and responsive scene composition. This is the visual reference, not a request to move combat into a conversation screen.
- `combat_portraits.py`: provides combat-specific portrait selection and fallback to the normal character portrait provider.
- `combat_ui.py`: combat occupies the in-person stage. Preserve its entry points and return-to-location behaviour.

These are source observations, not new test results or a claim that this redesign has shipped.

## Planned screen composition

1. **Encounter header:** location, encounter type, current objective and exchange number. Show round/time remaining only for encounters that actually use them.
2. **Large shared arena:** the correct encounter location fills the stage behind both characters. Player on the left, opponent on the right, anchored to a common visual floor. Preserve aspect ratio and character identity; avoid small headshot cards, stretched figures or opaque portrait panels hiding the environment. Keep faces and important silhouette details clear of HUD panels.
3. **Mirrored fighter HUDs:** names, knowledge-appropriate titles, health, stamina and mana with readable values. Place compact dark panels toward the centre beside the respective portraits. Display active forms and applicable combat states with text labels, remaining duration and inspectable explanations.
4. **Central tactical space:** retain visible background between fighters for target emphasis and Part 1 effects. Show readable opponent intent only to the extent the engine permits; never reveal a hidden action or imply certainty about a prediction.
5. **Narration area:** latest resolved exchange at bottom centre, with expandable history. Long prose must scroll or expand without progressively pushing the portraits off screen.
6. **Command dock:** prominent selectable action cards or buttons grouped by Martial, Unique skills, Awakened signatures and Utility. Preserve art filtering, amplification, form controls and target selection. A selected-action panel shows actual cost, target, effects and availability before a separate explicit resolve button commits the exchange.

At a reference 1280 × 900 window, aim for portraits roughly 320–480 pixels tall and a scene occupying around half the usable height. These are design targets to verify against real artwork and content, not fixed dimensions. At 1000 × 800 and smaller supported sizes, collapse secondary details into drawers and scroll the move catalogue before reducing portraits. Essential resources, action selection and the resolve control must remain reachable. Inspect larger windows and display scaling too.

## RPG UI elements within the redesign

- **Resource and state readability:** numeric bars, labelled status badges, form duration/readiness where supported, and clear empty/depleted states. Do not introduce decorative gauges for mechanics that do not exist.
- **Action selection feedback:** selected card emphasis, selected target outline/name, cost preview and explicit reasons for unavailable actions. Keyboard focus must offer the same information as hover.
- **Exchange phase indicator:** choosing action, resolving, narrating and finished. Both fighters currently act within an exchange; do not invent an alternating-turn or initiative queue.
- **Objective tracker:** display the encounter's real objective and rules, including restrained sparring and arena rounds when relevant.
- **Terrain inspector:** compact access to real distance, targetable objects, integrity and rubble information. Keep a text/list route alongside any graphical targeting.
- **Encounter ending:** clear outcome and return action, retaining access to the final narration. Show only actual recorded results and rewards.

All combat remains in the in-person window. Reuse `winterfield_ui.py` styling, dark slate information panels and coloured accents. No changes to the phone are required. Missing location or portrait art needs a deliberate dark fallback with readable names, not a blank or broken arena.

## Confirmed additional UI features

All eight suggestions below were approved on 2026-11-10 and implemented as MH-007 scope alongside the large-portrait redesign and baseline UI above. Actual behaviour and checks are recorded in the linked implementation evidence.

| Confirmed feature | Player benefit and limits |
| --- | --- |
| Favourite moves / quick slots | Pin learned moves for faster selection. Revalidate availability each exchange; a shortcut must not immediately spend resources. |
| Last-exchange breakdown | Expand damage, blocked/avoided outcomes, resource changes and status changes from recorded results. Do not invent causal explanations missing from the resolver. |
| Compact tactical overlay | Toggle distance, terrain targets and observed threats over the arena without permanently covering the artwork. |
| Contextual boss presentation | Distinct boss framing and phase labels only when an actual boss state supports them; no fabricated phase mechanics or concealed-identity spoilers. |
| Resource cost ghosting | Show the selected action's projected resource deduction on bars, clearly separated from committed values and uncertain results. |
| Portrait inspection drawer | Click or keyboard-select a fighter for known abilities and status explanations while respecting information boundaries. |
| Adjustable HUD density and text size | Offer cinematic and detailed views while retaining essential resources, focus visibility and controls. |
| First-fight guided hints | Brief dismissible explanations of targeting, amplification and simultaneous exchanges without changing opponent strength. |

Suggested implementation order begins with last-exchange breakdown, favourite moves and resource cost ghosting. All eight features remain required regardless of delivery order.

## Implementation milestones

- [x] Record the requested visual direction as a separate plan and inspect current combat/hangout composition.
- [x] Produce a reviewable arena layout at reference and compact sizes, using existing artwork.
- [x] Implement the large portrait/location stage and mirrored HUDs.
- [x] Implement the command dock, selected-action preview, status inspection, objective/phase display and collapsible narration/history.
- [x] Integrate existing targeting, forms, terrain and encounter completion; expose portrait/stage anchors for MH-001. Future animated playback remains Part 1 work.
- [x] Confirm all eight additional UI features as committed scope (2026-11-10).
- [x] Implement favourite moves/quick slots, last-exchange breakdown and resource cost ghosting.
- [x] Implement the tactical overlay, contextual boss presentation and portrait inspection drawer.
- [x] Implement adjustable HUD density/text size and dismissible first-fight guided hints.
- [x] Verify interaction, resize, save restoration and rendered states; document actual evidence.
- [x] Publish accurate patch notes for implemented behaviour, then validate and export them; record the pre-existing archive-source test failure.

## Acceptance and verification plan

- Visually inspect normal and compact windows: portraits are materially larger than the current 128-pixel height, both share the location backdrop, faces are unobscured and commands remain usable.
- Inspect long names, long narration, missing art, generated/custom opponents, alternate forms, depleted resources, unavailable actions, empty move categories, terrain targeting, active/finished fights and failed narration.
- Verify keyboard-only selection, focus, disabled-state explanations and text scaling. Avoid relying on colour alone. Preserve reduced-motion/fast-combat integration with MH-001.
- Ensure selecting or inspecting never resolves an action; resolving commits once even after repeated input. UI rebuilding, resizing, history viewing and AI narration must not reroll or spend resources.
- Verify favourites retain stable learned-move references, handle unavailable moves and only select actions. Verify cost ghosting updates with move/amplification changes without altering committed resources; breakdowns agree with recorded results.
- Inspect tactical overlay and portrait drawer with keyboard and pointer input, including unknown opponent information. Boss framing/phase labels must match real encounter state without identity spoilers.
- Verify both HUD densities and supported text sizes keep essential controls reachable. Guided hints must dismiss reliably, respect stored preferences and never change combat outcomes.
- Run applicable combat unit tests and existing `combat_ui_smoke.py`, `enhanced_combat_ui_smoke.py`, `combat_portraits_ui_smoke.py`, `combat_opponent_ui_smoke.py` and relevant Part 2/dialogue checks. Update meaningful layout assertions for the redesigned screen and inspect screenshots; file existence is not a passed check.
- Test existing active saves and re-entry after returning to the location. Keep training and in-person dialogue routes working.
- If implementation touches phone surfaces, run `tests/phone_dark_theme_smoke.py`, relevant feature checks and rendered-state inspection under AGENTS.md.
- Follow `patch_notes/AUTHORING.md` when implementation ships: catalogue entry, actual checks and limitations, validation, export, patch-note unit tests and reader/start-screen smokes.

**Save impact:** Restart required; no destructive migration or new story needed. Additive `combat.ui_preferences[player]` stores stable favourite IDs, density, text size and hint dismissal. New UI-resolved exchanges add resource/state audit snapshots; older records remain readable with explicit missing-snapshot text. Existing health, resources, objectives, learned moves, progression and encounter results are preserved.

**Progress and evidence:** Implemented on 2026-11-10 in `combat_rpg_ui.py` and integrated through `combat_ui.py`. All eight additions delivered. 96 combat and 23 enhanced-combat unit tests passed; new MH-007 and existing combat, portrait, Part 2, partner/boss, dialogue and Path UI smokes passed. Inspected large/compact layouts, cards, settings, inspection, quick slots, breakdown and large-text states; corrected large-text clipping. Patch-note reader and start-screen smokes passed. Patch-note validation/export passed; five patch-note unit tests passed and the historical archive-source check still fails on missing `tests/screenshots/mixtape-art-review-0.jpg`. See [full evidence](COMBAT_RPG_UI_EVIDENCE.md) for commands and limits.

**Release record:** `release-2026-11-10-combat-rpg-interface` in [patch-note catalogue](../patch_notes/catalog.json). MH-001 remains a separate update; its animation production is not claimed complete.
