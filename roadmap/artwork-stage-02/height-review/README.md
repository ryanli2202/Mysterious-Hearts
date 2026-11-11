# MH-013 Stage 2 — in-game heights and default masters

**Later refinement:** the uniform 178/163 cm defaults in this original release record are superseded by [varied heights and explicit overrides](../height-variation/README.md). See the [current height roster](../height-variation/HEIGHTS.md). Installation evidence below remains unchanged.

**Status:** Released for this follow-up; full MH-013 remains In progress.  
**Added / implemented:** 2026-11-11  
**Area:** Contemporary default portraits, selection, in-person scenes, prose, combat and phone wardrobe preview.  
**Specification:** [Portrait production plan](../../PORTRAIT_ARTWORK_UPDATE_PLAN.md), [107-character height roster](HEIGHTS.md), [runtime height data](../../../assets/portraits/stature.json).

Garrett is 188 cm, Rei 184 cm and Ivan 193 cm. The previous renderer applied different framing rules to those characters, included unequal transparent margins, and sized the player from a wider group slot. This made small stature differences look much larger. Simply enlarging the old waist crops also enlarged their heads/torso relative to the new mid-thigh artwork.

The accepted Stage 2 default masters are now installed at all **107 exact runtime paths: 89 characters and 18 guard roles**. This replaces 100 files and retains seven accepted pilot masters. Every installed PNG is byte-identical to its accepted candidate. [Installation manifest](installation.json) records both hashes and rollback copies of each replaced original. All **199 other files** from the original 306-file baseline remain unchanged. No artwork was generated or pixel-edited in this follow-up.

## Height and framing rules

- Preserve all **29 authored heights**. Missing male heights use **178 cm**; missing female heights use **163 cm**, within the requested ranges. Masked/robotic generic roles use 178 cm unless the role has an authored female presentation. These are display defaults, not invented private disclosures; the Crow's dossier remains unknown.
- Custom characters retain their explicitly saved height, including menu previews before registration in the live game. Town names, canonical IDs, role aliases and restored guard encounters resolve to the same height data.
- Treat these as **head-to-mid-thigh portraits**. The lower thighs, knees and feet are absent. A common visible-body fraction of 0.70 converts full stature to the depicted span. This is a proportional presentation convention, not a measured full-body reconstruction. The aligned lower edge is a picture crop, not a ground plane or foot position.
- Remove transparent export padding before fitting. Resize uniformly on both axes, retain all visible artwork, and share pixels/cm across everyone in an in-person group, prose composition or combat pair. A wider player slot cannot increase the player's stature. Individual thumbnails use the tallest authored master, 211 cm, as their reference so Takeo, Martos and Sylvanis do not collapse to the same height at the size limit.
- Selection previews use the same height data. Wardrobe previews preserve RGBA so the transparent area displays the existing dark phone surface.

## Milestones

- [x] Audit all 107 Stage 2 identities against authored stature and missing-height defaults.
- [x] Preserve and install the accepted default masters; retain source snapshots, original generation records and rollback files.
- [x] Implement shared stature fitting, alpha-bound normalization, tall-thumbnail headroom and saved custom-height handling.
- [x] Verify all roster paths, paired ratios at two sizes, individual thumbnails, artwork hashes, routing, save compatibility and dark phone states.
- [x] Review rendered normal/compact screens and publish the follow-up release; preserve the full artwork roadmap's remaining stages.

**Dependencies:** Existing character/guard identity routing, accepted Stage 2 candidates, PIL/Tk consumers, custom profile registry and embedded dark phone UI.

**Completion criteria:** All 107 default paths match their accepted masters; 29 canonical heights remain intact; 78 display defaults follow the requested ranges; Garrett/Rei/Ivan remain in the correct relative order independent of slot width or alpha padding; no stretching or synthesized lower legs; old saves and protected portrait overrides remain usable.

## Actual verification

- `python tools/audit_character_stature.py`: **107/107** installed hashes, candidate hashes and per-character paired height ratios pass at two sizes, with no more than two pixels of rounding tolerance. Backup hashes verified; **199 non-master baseline files unchanged**. [Machine-readable audit](height-audit.json).
- `python tools/artwork_stage_02.py verify`: **107/107** accepted, zero pending. Decode, RGBA, alpha, safe top/side bounds, frozen originals and original generation/carried-forward hashes verified. The verifier now recognises only the exact recorded installation hashes as authorised live changes; the original production manifest retains the baseline differences.
- **73 tests pass across nine relevant unit suites**: portrait framing (7), character selection (11), hangout scene (6), guard portraits (6), combat portraits (4), campaign flashbacks (6), flashback visits (9), Syndicate cast (6), campaign prose (18). [Initial suite logs](checks/units.json); [final framing check](checks/framing-final.txt) supersedes its initial six-test run.
- Installed Stage 2 smoke: **107 paths at two thumbnail sizes, 33 screenshots, zero callback errors**. Includes normal/compact selection, solo/group scenes, residents, guard combat and wardrobe. The test no longer patches the renderer; it exercises the actual game implementation. [Installed render record](installed/checks/presentation-render.json).
- Start screen: **28 previews**, paging, explicit begin and normal/minimum layouts pass. Combat smoke renders **24 dedicated combat portraits** and checks both sides/actions in the compact in-person view. Prose smoke covers normal/compact readers, transitions and interactive controls. Flashback visit smoke covers all four protagonists, historical portraits, saved resume, cancellation/error states, journal and return with no extra top-level window.
- Phone dark-theme smoke passes across **34 pages** plus chat, contact details and embedded control states. Actual wardrobe alpha and dark scrollbar/control presentation inspected. Patch-note reader smoke passes search, filters, state, export, empty/error states and two sizes. [Smoke logs](checks/smokes.json), [final rerenders](checks/final-render-checks.json).
- Publication validation passes with **487 entries**, export is refreshed, and the patch-note reader smoke passes. The patch-note unit suite has **five passes and one existing archive-source failure** for missing `tests/screenshots/mixtape-art-review-0.jpg`. [Publication checks](checks/publication.json) record that failure; it is not counted as a pass.

**Rendered review:** [Normal group](installed/screenshots/group-1280x900.png), [compact group](installed/screenshots/group-1000x800.png), [Rei selection](installed/screenshots/selection-rei-1280x900.png), [female Team 9 guard](installed/screenshots/combat-team9-1280x900.png), [dark wardrobe](installed/screenshots/wardrobe-preview.png), nine loader galleries and the captured prose/flashback/phone states were inspected. Garrett and Rei remain slightly shorter than Ivan; Emily stays visibly petite; artwork retains full heads/hands and connected thigh cutoffs. Normal group/selection backgrounds and captions remain readable. Tests use local fixtures and mocked providers; no story saves or live AI calls are made.

## Access, saves and remaining scope

Restart the game to reload Python and cached images. Default/Automatic outfits appear through character selection and existing in-person scenes. A deliberately saved alternate outfit, headquarters uniform or historical override still takes precedence; choose the default outfit to see the new contemporary master. Guard role IDs and encounter saves retain their existing routing.

**Save impact:** No schema migration or changes to relationships, progress, unlocks, wardrobe choices, custom portraits or stored heights. Original target filenames are retained. Installation is independently reversible from the manifest backups.

**Limits:** Stages 3–4 still need wardrobe, historical, masked and dedicated combat artwork production. Their existing assets and narrative identities are preserved; scaling cannot make a legacy bust/waist crop anatomically equivalent to a new mid-thigh master, or remove pose/effect differences. This release does not certify the entire remaining collection. Stage 5 integration is complete for these default masters; later variants must repeat the same checks. Historical staged-only screenshots and logs remain in their original directories; `live/` here records the diagnostic before installation, `staged/` the corrected candidate comparison and `installed/` the actual final game.

**Release record:** `release-2026-11-11-stage2-character-heights` in [patch notes](../../../patch_notes/PATCH_NOTES.md).
