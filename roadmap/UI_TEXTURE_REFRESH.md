# MH-008 Textured interface and navigation refresh

**Status:** Released  
**Added:** 2026-11-10  
**Area:** Shared presentation, start screen, in-person shell and phone

Introduce subtle locally generated woven slate textures, framed scene panels, a separate brand masthead and navigation toolbar, clearer Speak/Actions selection and composer buttons, and a readable phone home information panel with direct Home navigation. Preserve character/location art, saved stories, phone customisation and in-person activity routing.

### Milestones

- [x] Inspect shared styling, start, phone and in-person layouts.
- [x] Implement textures and layout improvements.
- [x] Run regression checks and inspect rendered layouts and interactive states.
- [x] Publish verified patch notes.

**Dependencies:** winterfield_ui, existing Pillow/Tk runtime, phone_theme and existing phone controls.

**Completion criteria:** Readable textured surfaces; reachable navigation/composer at supported sizes; dark phone controls; passing relevant smoke checks and visual review.

**Save impact:** No migration or new save fields. Restart to load UI changes; existing story and phone preferences remain intact.

**Progress and evidence:** Implemented and verified locally on 2026-11-10. Passed `tests/hangout_scene_smoke.py`, `tests/start_ui_smoke.py`, `tests/phone_home_smoke.py`, `tests/ui_texture_refresh_smoke.py`, `tests/phone_dark_theme_smoke.py` and `tests/patch_notes_ui_smoke.py`. Reviewed rendered compact start, in-person Speak/Actions, phone Home, and long-title phone screens including Home hover/focus. Dark audit covers 34 phone pages and embedded control states. The new smoke verifies compact/wide navigation bounds and Home action dispatch.

**Verification limits:** `tests/phone_navigation_smoke.py` stops at line 64: its old global-busy `Writing response` expectation differs from the current message-pump delivery statuses in `phone_ui.py`; messaging behavior was not edited. Five of six patch-note unit tests passed; archive source coverage fails on missing historical `tests/screenshots/mixtape-art-review-0.jpg`. This update refreshes shared framing and primary screens, not every individual app layout.

**Release record:** `release-2026-11-10-textured-interface` in `patch_notes/catalog.json`. Catalogue validation and Markdown export completed.

## Plugin task assignments

**Assigned:** 2026-11-11. Released scope; future requested maintenance only. Keep historical checks and release records intact.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Needed local assets for shared navigation and phone UI | prompt-to-asset | Author/validate/export only required icons or framing assets; reuse existing woven-slate styles and inspect compact, focus, hover, selected and disabled states. |
| Layout, interaction and navigation regressions | falsegreen-skill | Review assertions for reachable controls and real dispatch/state effects; run relevant feature smokes and tests/phone_dark_theme_smoke.py whenever phone surfaces change. No new audio/animation is required by this assignment. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

