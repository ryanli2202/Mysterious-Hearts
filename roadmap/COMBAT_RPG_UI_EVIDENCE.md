# MH-007 implementation evidence — 2026-11-10

## Delivered interface

`CombatView` now uses `RPGCombat` in `combat_rpg_ui.py` for active and completed encounters. Training and workshop routes retain the existing enhanced-combat implementation. The in-person stage contains a shared location backdrop, enlarged opposing portraits, mirrored resource HUDs, objective and exchange phase, a fixed command dock, latest narration and expandable history. Moves opens a scrolling card catalogue; direct selectors remain available for technique, amplification and target. Selecting a category also opens its cards.

The eight approved additions are implemented:

1. Six favourite move slots, stored by stable move ID and protagonist within each story. Quick slots select only; unavailable learned moves stay visible and can be cleared.
2. Last-exchange breakdown from resolver records, plus additive before/after resource and state snapshots for new UI-resolved exchanges. Old exchanges display recorded outcomes/costs and explicitly identify missing snapshots.
3. Toggleable tactical overlay for distance, objects, rubble and partner resources; full terrain text also appears in Forms / rules.
4. Revealed boss framing and Richter's real targeting/burst/recovery/ram cycle labels. No new boss phase or identity disclosure.
5. Gold hatched resource-cost previews, including form upkeep, distinct from actual committed bars. Damage and recovery are not predicted as guaranteed results.
6. Pointer/keyboard portrait inspection: player mechanics and only observed opponent techniques, with knowledge-sensitive titles. Generic state explanations and remaining duration are inspectable.
7. Detailed/Cinematic HUD density and 10/12/14-point text. At larger sizes, secondary titles and long state descriptions move to inspection; six quick slots use a drawer so essential HUD bars remain visible.
8. First-fight hint, an explicit targeting/amplification/simultaneous-exchange guide and persistent dismiss/restore control in Display / help.

## Compatibility and access

Restart and enter combat through existing in-person routes. No phone pages, combat balance or animation assets are changed. Both fighters still act in each exchange. Repeated clicks while narration is pending cannot resolve again; inspecting or selecting never resolves. Finished encounters offer a return to the location, preserving campaign epilogue routing.

Existing saves receive no destructive migration. `combat.ui_preferences[player]` stores optional favourites, density, text size and hint dismissal with legacy defaults. New exchanges may contain `ui_resource_audit` snapshots; old exchanges remain readable. Existing progression, resources, encounter IDs, learned moves and outcomes remain authoritative.

The arena exposes `combat_portrait_rail` and `portrait_items` for future Part 1 effect integration. This change adds no animated effects, so it does not claim validation of future animation playback or completion of MH-001 Part 1.

## Verification performed

Used the bundled executable at `C:/Users/ryanl/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.

- `-m unittest discover -s tests -p 'test_combat*.py'`: 96 passed, including four new presentation tests covering preference defaults/scoping, JSON persistence, opponent knowledge boundaries and truthful legacy/new breakdowns.
- `-m unittest discover -s tests -p test_enhanced_combat.py`: 23 passed.
- `tests/combat_rpg_ui_smoke.py`: real Tk checks for large/compact layouts, 10/12/14-point text, all eight features, long names/states, six pins, empty categories, unavailable slots, restored active saves, nonmutating selection, Enter activation of a technique card, duplicate-submit suppression, failed narration, depleted resources and missing-art fallbacks. Provider and story-save writes mocked.
- Existing `combat_ui_smoke.py`, `enhanced_combat_ui_smoke.py`, `combat_portraits_ui_smoke.py`, `combat_part_two_ui_smoke.py`, `combat_support_ui_smoke.py`, `combat_dialogue_ui_smoke.py` and `combat_path_ui_smoke.py`: passed. The opponent smoke is an alias of the enhanced-combat smoke; its underlying scenarios passed.
- Inspected `tests/screenshots/rpg-combat-large.png`, `rpg-combat-compact.png`, `rpg-combat-large-text-pins.png`, `rpg-combat-long-name-states.png`, `rpg-combat-techniques.png`, `rpg-combat-forms.png`, `rpg-combat-forms-large-text.png` and `rpg-combat-quick-slots.png`. A large-text clipping issue found during review was corrected by moving quick slots into a drawer and compacting secondary HUD text; bounds assertions cover resource panels and resolve controls.

Release checks: `patch_notes.py validate` passed. `tests/patch_notes_ui_smoke.py` passed search, filters, reader state, export, empty/error states and two sizes. `tests/start_ui_smoke.py` passed 28 previews, paging, explicit begin and default/minimum layouts. `-m unittest discover -s tests -p test_patch_notes.py -v` passed five tests; `test_archive_coverage_and_sources` failed on the pre-existing missing `tests/screenshots/mixtape-art-review-0.jpg`. No historical entries or evidence were fabricated to hide that failure. `patch_notes.py export` refreshed the generated notes.

The final MH-007 smoke also verified returning to the location after finishing, empty categories, unavailable favourite IDs, restored JSON active saves, keyboard Enter selection and large-text resource-panel bounds. The four presentation unit tests were rerun after extending the breakdown to include same-turn recorded field-partner outcomes; all passed.

No live AI prose evaluation is claimed; this update changes presentation and uses deterministic fallback fixtures for provider failures. No phone surface changed. Rendering at arbitrary OS scaling and future animation playback are outside the verification performed here; current window resizing and in-game text sizes were exercised.
