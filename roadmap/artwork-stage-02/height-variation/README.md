# MH-013 Stage 2 — varied default heights

**Status:** Released for this refinement; full MH-013 remains In progress.  
**Added / implemented:** 2026-11-11  
**Area:** Height data used by selection, in-person, prose, combat and phone portrait consumers.  
**Specification:** [Current 107-entry roster](HEIGHTS.md), [runtime data](../../../assets/portraits/stature.json), [production plan](../../PORTRAIT_ARTWORK_UPDATE_PLAN.md).

The original 29 authored heights are unchanged. Seven former display defaults now use the user's explicit values:

| Character / role | Height |
| --- | ---: |
| Jeremy Gordon | 183 cm |
| Edward Fox | 184 cm |
| The Crow | 180 cm |
| Keisuke Hachimura | 183 cm |
| Joseph Richter, including cybernetic portrait | 190 cm |
| Oni | 198 cm |
| Custom Robotic | 198 cm |

The other **71 display defaults vary by identity**: 39 male defaults span 175–180 cm and 32 female defaults span 160–165 cm. All six integer values in each range are represented. Values are stored explicitly, so loading, resizing, navigation, outfit changes and save resume do not randomize stature. The two robot heights are explicit exceptions, not range-limited defaults.

[Before data](before-stature.json) and [change record](changes.json) preserve the original heights, exact overrides and distributions. There are 67 numeric changes across the full roster; some varied assignments naturally retain their previous number. No PNG assets were edited or replaced.

## Milestones

- [x] Preserve all existing authored heights and snapshot the previous runtime table.
- [x] Assign varied stable defaults and apply all seven explicit heights.
- [x] Keep Joseph Richter's ordinary, cybernetic-path and direct guard-art aliases consistent at 190 cm.
- [x] Verify full-roster ratios, source hashes, persistence, aliases, custom profiles and normal/compact UI.
- [x] Update the current roster, roadmap and release notes; validate and export the catalogue.

**Dependencies:** Existing MH-013 master installation, shared stature resolver, crop-aware fitting and guard/save identity routing.

**Completion criteria:** Original 29 records unchanged; seven specified values exact; all 71 defaults inside the requested sex-specific ranges with variation across each full range; saved values stable; current game rendering uses these values without changing aspect ratio or the cropped-body convention.

## Verification and evidence

- `python tools/audit_character_stature.py`: **107/107** accepted installation/candidate hashes and paired height ratios pass at normal and compact sizes. All 199 other baseline assets remain unchanged. [Audit](height-audit.json).
- **29 targeted unit tests pass**: portrait framing (8), combat portraits (4), guard portraits (6), character selection (11). Tests compare all original authored records against the snapshot, check all seven overrides, all six values in each default range, stable reloads, custom height preservation, aliases and all-character rendering. [Logs](checks/units.json).
- `python tests/artwork_stage_02_ui_smoke.py --live --variation`: **107 paths at two thumbnail sizes, 41 screenshots, zero callback errors**. Includes added Fox/Gordon selections and Oni/Custom Robotic combat at two window sizes. The first run used a custom-role image ID as a built-in guard type; the corrected fixture registers a saved custom robotic type, matching actual game routing. Initial failure and successful rerun are retained in [smoke logs](checks/smokes.json) and [final render result](checks/render-final.json).
- Phone dark-theme smoke passes across **34 pages** plus chat, contact details and embedded controls. Start smoke passes **28 previews**, navigation and normal/minimum layouts. [Logs](checks/smokes.json).
- Visually reviewed the updated roster gallery, normal/compact robot combat, group presentation and dark wardrobe/control states. Robot portraits fit and remain slightly taller than Ivan at the shared scale. [Review](presentation-review.json), [Oni compact](presentation/screenshots/combat-oni-1000x800.png), [Custom Robotic](presentation/screenshots/combat-custom_robotic-1280x900.png).
- Catalogue validation passes with **488 entries**, export is refreshed and the patch-note reader smoke passes. Its unit suite has five passes and one pre-existing archive-source failure for missing `tests/screenshots/mixtape-art-review-0.jpg`. [Publication checks](checks/publication.json) record the actual results. All five changed Python files compile.

## Access, saves and scope

Restart the game to reload cached height metadata and portraits. Existing character selection, default outfits, in-person scenes, prose, combat and phone portraits use the revised table automatically. Custom protagonists keep their own saved height. Generic custom robotic guards use the requested 198 cm role value.

**Save impact:** No migration, save-field edits, outfit changes or progress changes. Dialogue disclosure rules remain unchanged; this refinement updates rendering metadata. The prior crop-aware calculation remains: the visible head-to-mid-thigh span is modelled as 70% of full stature, with uniform scaling, transparent-padding normalization and one shared scale per composition. No lower legs are invented or stretched. Later wardrobe/history/combat artwork stages remain pending.

**Release record:** `release-2026-11-11-stage2-varied-heights` in [patch notes](../../../patch_notes/PATCH_NOTES.md).
