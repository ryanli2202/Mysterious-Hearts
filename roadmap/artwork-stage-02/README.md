# MH-013 Stage 2 — contemporary character masters

**Stage 2 completed:** 2026-11-11. **Current delivery:** all 107 default masters installed with the [full-roster height correction](height-review/README.md); 100 replacements and seven retained pilot masters. **Full MH-013:** In progress; wardrobe/context stages remain pending.

**Latest height data:** [Varied defaults and seven explicit heights](height-variation/README.md) supersede the initial uniform defaults. [Current 107-entry height roster](height-variation/HEIGHTS.md) preserves all original known heights and uses stable per-character values within the requested ranges.

The follow-up preserves authored heights, assigns the requested missing-height defaults, fixes unequal group-slot scaling and alpha padding, and accounts for the off-image lower thighs/legs. See the [audited height roster](height-review/HEIGHTS.md), [installation hashes/backups](height-review/installation.json) and [current verification](height-review/checks/). Historical production records below describe the initial staged-only delivery and are retained as evidence; their deferred default-master integration was completed by the follow-up.

## Original staged delivery record

The package contains **107 contemporary masters: 89 characters and 18 guard roles**. One hundred masters were newly produced, with 133 successful built-in `image_gen` outputs including revisions. Seven pilot masters are carried forward: Ivan, Charles v2, Emily, Minsu, Priya Shah, Otis Bell and Clubs. Emily uses the separately published rendering refinement observed during this work. Richter's cybernetic form is a Stage 4 context variant, not a second contemporary character.

Use the [master index](MASTERS.md) to open each final PNG, identity sheet and selected generation record. [Manifest](manifest.json) records source/output SHA-256, alpha statistics, visible bounds, review and exact target path. [Frozen roster](roster.json) and [turn-start hashes](before-state.json) retain the original scope. [Exact prompts](generations/) preserve every successful call, its image references and original generated output path. Built-in generator model identity is not exposed. No fallback API/CLI was used.

## Artwork and review

All candidates are 1024×1536 RGBA cutouts. Original assets remain under [originals](originals/); final staged assets are under [candidates](candidates/). Each generated PNG was copied byte-for-byte, with no pixel postprocessing. Python/Pillow only creates inspection composites and screenshots.

Full-size artwork and three-background comparisons were reviewed for individual identity, age, build, clothing, tattoo placement, props, hands, mid-thigh anatomy and alpha. The 107 identity sheets compare the frozen source, final master and face detail. [Per-asset findings](reviews.json) distinguish visual review from automated format checks.

Corrections include fuller thigh coverage, Celeste's clipped crown, Daniel's dark brown irises, natural dental arches/lips, practical trousers beneath Maya's apron and full-length June overalls. Neck/arm markings, Rei's existing lettering, guard masks, gear and local power colours were compared with source images. Existing older faces, varied builds and mechanical anatomy remain. Guard masters retain established guarded poses/equipment where present; no new combat derivatives or powers were introduced.

Framing tolerances are explicit: all figures clear top and side edges at alpha ≥16, but many margins are narrower than the preferred 3–5% headroom. Some clean thigh cutoffs reach the bottom canvas edge. Full hairstyles, visible hands and connected thigh coverage take priority; no knee-length composition is accepted. Exact bounds are in the manifest. Near-opaque alpha remains valid.

## Staged presentation evidence

[Preview harness](../../tests/artwork_stage_02_ui_smoke.py) redirects only the frozen roster's exact loaded paths. It does not copy anything into live asset discovery or write story saves. All 107 paths rendered at 150×225 and 86×129 in nine labelled loader galleries. The main run saved 33 screens: ten selection/dossier views, nine galleries, four solo/group views, three resident conversations, six guard-combat views and a wardrobe view. A targeted wardrobe follow-up adds a baseline comparison. [Visual findings and screenshot dimensions](checks/presentation-review.json) record the actual review.

Normal/compact game requests are 1280×900 and 1000×800; the desktop constrains the larger capture to its available client area (1280×833). Gallery captures are 1220×800. [Presentation boards](presentation-01.jpg), [compact selection/solo](presentation-02.jpg), [groups/residents/wardrobe](presentation-03.jpg) and [guard combat](presentation-04.jpg) are diagnostic composites, not game surfaces.

Two **preview-only integration proposals** are exercised in the harness; neither changes runtime code:

1. Add Garrett selection (188 cm) and Rei selection (184 cm) to the 2:3 path-specific fitting with reference stature 193. Legacy fitting makes these new masters too small beside Ivan. Four `legacy-fitting-*` captures preserve the comparison. Keep historical and wardrobe variants on their own fitting until those assets are ready.
2. Preserve RGBA in `lifestyle_ui.Screen.preview`. Its current RGB conversion discards transparency and exposes otherwise invisible RGB colours. [Current wardrobe preview](screenshots/legacy-wardrobe-preview.png) and [RGBA proposal](screenshots/wardrobe-preview.png) show the difference on the existing dark phone surface.

The staged art passes presentation review with these isolated proposals. **Live installation and full consumer/save compatibility remain Stage 5**, after wardrobe/context production. Historical scenes, alternate wardrobes, masked leadership uniforms and the separate combat set were not regenerated or certified by this stage. Combat previews use the new guard masters with existing pilot combat Ivan.

## Verification and limits

- `python tools/artwork_stage_02.py verify`: 107/107 accepted; dimensions, decode, clear/solid alpha, safe top/side bounds, frozen-original hashes and generated/carried-forward provenance pass. [Log](checks/asset-validation.txt).
- Runtime asset comparison: 305 of the 306 turn-start files are unchanged. The only difference is Emily's independently published refinement, verified against its release hash and carried into this package. [Carry-forward evidence](carried-forward-updates.json). Stage 2 wrote no live character assets.
- [Staged render](checks/presentation-render.txt): 107 loaded paths, 33 screenshots and no callback errors. [Wardrobe follow-up](checks/wardrobe-preview.txt) captures the alpha correction separately. UI fixture development initially used an invalid resident name; the corrected run uses actual resident routines.
- [Nine unit suites](checks/units.json): **62/63 tests pass**. Framing, selection, combat/guard routing, historical visits, Syndicate cast and hangout tests pass. Existing `test_camera.CameraTests.test_local_date_partner_can_join_photo` still fails because Theo is absent from the fixture's companion list. No gameplay code was changed to mask it.
- [Phone dark-theme smoke](checks/phone_dark_theme_smoke.txt): 34 pages plus chat/contact/embedded controls pass. [Rendered controls](screenshots/phone-dark-theme.png) inspected; no phone styles or activity routing changed.
- Patch-note validation, export and the patch-note unit suite are recorded in [publication checks](checks/patch_notes.json). The existing missing historical `tests/screenshots/mixtape-art-review-0.jpg` remains an archive-source limitation if reported there; it is unrelated to these masters.

## Access, saves and next stage

This is a **Development report**, not a new playable release. Inspect the staged PNGs or run the preview harness from the project root. Current player-facing artwork remains the installed pilot and prior assets. No restart or migration is required for this staged package; no relationships, unlocks, wardrobe choices, guard IDs, custom art or saved history changed.

Stage 3 can now derive outfits from these accepted masters, comparing each set for face/body/height consistency. Stage 4 handles historical/masked/combat variants and remaining contextual refinements. Stage 5 must install at the manifest's verified paths, apply and test the previewed fitting/alpha fixes, recheck mixed wardrobes, save compatibility and affected phone states. Stage 6 publishes the actual installed scope. Preserve original prompts, source snapshots and stable MH-013 IDs.
