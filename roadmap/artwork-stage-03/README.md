# MH-013 Stage 3 — wardrobe variants

**Status:** Stage 3 production complete; staged for later integration. MH-013 remains In progress. **Added:** 2026-11-11 (Australia/Brisbane).  
**Area:** Contemporary character wardrobe artwork.  
**Detailed specification:** [Production plan](../PORTRAIT_ARTWORK_UPDATE_PLAN.md).

The frozen scope is **146 wardrobe variants for ten characters**. Each must match its installed Stage 2 master and the corrected, stable height table. The lower thighs, knees, lower legs and feet are outside the picture; the bottom is a mid-thigh picture crop, never a foot baseline. The existing 70% visible-body fitting convention and uniform scaling remain authoritative.

## Milestones

- [x] Freeze all 146 original outfit files, ten installed masters and the current stature table, with hashes.
- [x] Generate and visually review each wardrobe against its character master and original costume.
- [x] Verify RGBA, composition, provenance, unchanged master/height data and complete per-character sets.
- [x] Inspect normal/compact game scenes and dark phone wardrobe previews; record actual checks.
- [x] Record delivery, save impact and patch-note evidence; validate and export.

**Dependencies:** Accepted Stage 2 masters; `character_stature.py`; `portrait_framing.py`; existing wardrobe, scene and camera routing.

**Completion criteria:** All 146 outfits preserve individual face, body, height, costume and markings; clean transparent head-to-mid-thigh cutouts; normal/compact presentation and save routing verified. Historical, masked and combat variants remain Stage 4.

**Save impact:** Accepted production candidates remain outside live wardrobe discovery until the later integration stage. No saved outfit, relationship, unlock, custom portrait or height is changed.

**Progress and evidence:** [Manifest](manifest.json), [hash-bound visual acceptance](reviews.json), [frozen roster](roster.json), [source hashes](before-state.json), [height snapshot](before-stature.json), [outfit briefs](outfit-briefs.json), [exact generation records](generations/). All 146 candidates are accepted after full-size output review and complete character-set/three-background inspection. Every final file is an unchanged built-in `image_gen` PNG; the generator's model identifier is not exposed. Python only creates diagnostic review composites and exercises the existing runtime renderer.

## Delivered scope

| Character | Wardrobes |
| --- | ---: |
| Amy | 14 |
| April | 14 |
| Emily | 14 |
| Garrett | 16 |
| Ivan | 13 |
| Minsu | 16 |
| Rei | 17 |
| Samantha | 14 |
| Sophie | 14 |
| Yuriko | 14 |
| **Total** | **146** |

The final artwork is in [candidates/](candidates/), outside live asset discovery. The [originals](originals/) and [installed master snapshots](masters/) remain immutable. [Source and candidate sheets](reviews/) provide whole-family comparisons; `*-alpha-*.jpg` sheets show slate, middle and light diagnostic backgrounds. Those light backgrounds are offline inspection aids, not phone UI.

Production used 167 successful generation/edit outputs, including superseded revisions, and three recorded failed attempts. Exact prompts, input paths, raw output paths and output hashes are in [generations/](generations/); superseded candidate PNGs are preserved there. [Jobs](jobs/) retain each requested edit. No stretch, pixel paint-over, alpha extraction or local image-editor correction was applied to the delivered artwork.

## Corrections and approved exceptions

- Initial two-reference Amy beach attempts drifted from the accepted head/body proportions. They were replaced using the Stage 2 master as the sole edit target and visually transcribed wardrobe descriptions. Additional old references are used only where required to map newly exposed Garrett/Rei tattoos.
- The user authorized covered sleepwear in original colours. Final covered variants are Amy white, April black, Emily blush pink, Minsu charcoal, Rei charcoal, Samantha burgundy and Sophie cobalt blue. Garrett's original black shorts design succeeded and is retained; Yuriko has a home outfit and no separate sleep asset in this frozen scope.
- Emily's light formal jacket now accompanies a continuous ivory pleated A-line skirt, correcting the shorts-like split identified by the user. Her gym variant retains full leggings; an intermediate dark alpha-edge defect was rejected and regenerated.
- Minsu's charcoal pyjama shorts now end above two connected visible upper thighs. The user identified the missing thighs in the first covered version. The lower thighs, knees and lower legs remain outside the frame. His beach shorts also retain their original muted ocean-blue colour.
- Samantha's three swim outfits and burgundy dress had pocket-pose fingers disappearing into skin/fabric. The repaired hands rest on the outside of the upper thigh with complete fingers. Her formal black suit, red flannel and red motorcycle jacket also received complete-hand and missing-sleeve repairs. Other actual pockets use natural hand occlusion, allowed by the production plan. All fourteen were reviewed again.
- Yuriko's pocketless outfits explicitly show both complete hands instead of carrying over the master's hidden fingers. Her study glasses, hair clip, cheek mole, gym watch and theatre pencil remain outfit-appropriate.
- April's pendant scale was corrected; exposed Garrett neck tattoos were restored above the tuxedo, changshan and hanfu collars; Sophie's picnic skirt was extended through the picture edge. Long trousers, leggings and robes remain long garments despite the mid-thigh picture crop.
- Ivan's first beach attempt was rejected by the image tool. The user's requested identical retry succeeded, retaining the original coral swim shorts. [Failed-attempt ledger](generations/failed-attempts.json) records the rejection and resolution without claiming the failed attempts produced artwork.

## Verification and limits

The [routing/stature audit](checks/staged-routing-heights.json) verifies all **306 live baseline assets unchanged**, the entire corrected height table unchanged, all 146 accepted hashes, 292 normal/compact variant-to-master/Ivan height comparisons, 62 saved player-wardrobe JSON round trips, and 26 automatic occasion/sleep routes. Height fitting retains the existing 70% visible-body convention and uniform shared scale. This is a display convention for cropped bodies, not reconstructed full-body measurements.

[Unit results](checks/units.json): 70 of 71 tests pass across nine suites covering framing, selection, camera, lifestyle/wardrobes, combat, guards, campaign flashbacks, flashback visits and Syndicate routing. The existing `test_local_date_partner_can_join_photo` failure still reports Theo absent from its companion fixture. Runtime code and that test were not changed by this production stage.

The [presentation harness](../../tests/artwork_stage_03_ui_smoke.py) substitutes only the 146 exact image paths in memory. It uses the real game loader and existing outfit resolver, disables save writes and AI calls, and captures normal/compact thumbnails, in-person solo/groups and dark phone previews. Its first attempt completed the full gallery and height/routing audit, then failed because the fixture requested a nonexistent Ivan polo variant. The fixture now selects the roster's `fashion-ivory`; the failed log is retained. The complete rerun passes with all 146 paths rendered at two thumbnail sizes, **20 screenshots** and no Tk callback errors. All thirteen gallery screenshots, both sizes of solo/group scenes and all three phone correction previews were visually inspected. [Presentation results](checks/presentation-render.json) and [screenshots](screenshots/) record the final outcome. The normal 1280x900 capture can include an outer desktop strip below the client on this display; the game client remains intact.

[Existing UI smoke results](checks/smokes.json) also pass: `phone_dark_theme_smoke.py` checks 34 phone pages, chat, contact details and embedded control states; `lifestyle_ui_smoke.py` checks eight apps, saved drafts and outfit-generation/switch/failure/cancellation states; `start_ui_smoke.py` checks 28 previews, paging and default/minimum layouts. The dark-phone mosaic and wardrobe screen were inspected and preserved alongside the staged screenshots.

## Publication evidence

Development report `development-2026-11-11-artwork-stage-03-wardrobes` records the production scope, access, save impact, corrections and limitations in `patch_notes/catalog.json`. [Portable development record](DEVELOPMENT_RECORD.md). The default release export deliberately excludes Development reports; enable **Include original chat reports** in the patch-note reader to find this entry.

[Publication checks](checks/publication.json): catalogue validation passed with 498 entries, the main `patch_notes/PATCH_NOTES.md` export refreshed, and `patch_notes_ui_smoke.py` passed search, filters, read/bookmark state, export, empty/error states and both window sizes. Its compact screenshot was inspected. The first patch-note unit run exposed a test fixture that assumed the first catalogue entry was visible with Development reports hidden. The test now selects a default-visible entry, preserving the intended reader behavior. [Rerun](checks/publication-unit-rerun.json): **five of six tests pass**; the existing archive-source failure remains because `tests/screenshots/mixtape-art-review-0.jpg` is missing. No substitute evidence was fabricated.

**Access and save impact:** These are staged production assets, not a live artwork release. Review the candidates, sheets and screenshots directly. Existing game sessions still load the old wardrobe files. No restart or migration is needed for this staged delivery; no saved outfits, custom art, heights, relationships or unlocks changed. Historical, masked, combat and remaining guard variants belong to Stage 4; live wardrobe installation and complete-collection release remain later integration work. MH-013 stays **In progress**.

[Final verification](checks/final-verification.json) confirms all 146 acceptance hashes, all 306 unchanged live files, the unchanged stature table, existing review evidence and patch-note sources, 37 local documentation links, compilation of the two Stage 3 helpers and corrected patch-note test, and refreshed catalogue validation/export.
