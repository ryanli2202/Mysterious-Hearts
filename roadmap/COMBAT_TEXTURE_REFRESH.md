# MH-009 Combat texture refresh

Requested 2026-11-10. Scope: active/finished combat, HUD, command dock, inspection/history/settings/technique drawers, combat hub stats, Path stats, academy, Trait workshop, dossier and hangout combat invitations. Reuse Winterfield woven slate; do not change global phone styling or combat mechanics.

Implementation: shared combat_style panels and stat tiles; framed arena HUD and command dock; mint resolve action and segmented resource strips; two-column academy library/brief; textured invitation action rows and dossier; padded reading panels and workshop section hierarchy.

Verification completed 2026-11-10. No AI-generated artwork or provider calls required. Existing location and portrait artwork retained.


## Plugin task assignments

**Assigned:** 2026-11-11. Released scope; future requested maintenance only. Keep historical checks and release records intact.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Needed local assets for combat HUD, drawers and training layouts | prompt-to-asset | Author/validate/export only required icons or framing assets; reuse existing woven-slate styles and inspect compact, focus, hover, selected and disabled states. |
| Layout, interaction and navigation regressions | falsegreen-skill | Review assertions for reachable controls and real dispatch/state effects; run relevant feature smokes and tests/phone_dark_theme_smoke.py whenever phone surfaces change. No new audio/animation is required by this assignment. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Verification and release evidence

- 96 tests passed with `python -m unittest discover -s tests -p 'test_combat*.py'`; 23 with `test_enhanced_combat.py`.
- Passed UI scripts: combat_rpg_ui_smoke.py, combat_ui_smoke.py, enhanced_combat_ui_smoke.py, combat_path_ui_smoke.py, combat_dialogue_ui_smoke.py, combat_support_ui_smoke.py, combat_texture_ui_smoke.py, phone_dark_theme_smoke.py and patch_notes_ui_smoke.py.
- Inspected screenshots of large combat, large-text HUD, inspection, academy, workshop candidates, compact Path, hub and scrolled ledger. Fixed compact HUD clipping by reducing frame spacing and shortening the large-text latest-narration preview; full history remains available. Fixed hub overflow with local scrolling and compact navigation. New smoke verifies the ledger stays reachable after scrolling and navigation returns safely.
- Phone dark audit passed across 34 pages, chat/contact details and embedded states. No phone surfaces changed directly.
- Start UI smoke failed its character-selection assertion after change_page(1); start UI was not edited in this update. Patch-note unit suite: five passed, one failed on the previously recorded absent historical screenshot tests/screenshots/mixtape-art-review-0.jpg.
- Python compilation, patch-note validation and export passed. Providers and story persistence mocked in UI checks.

Save impact: restart required; no schema, balance, progression or routing changes. Published locally as release-2026-11-10-combat-texture-refresh. MH-001 animation scope remains separate.
