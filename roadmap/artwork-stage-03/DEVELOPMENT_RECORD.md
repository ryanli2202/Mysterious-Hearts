# Mysterious Hearts — Patch notes

Historical entries reconstruct recoverable development, not numbered releases. Unknown release dates stay unknown. Topic order is not a verified chronology. Original reports may describe superseded behavior; their test claims are historical. The 17 oversized chats were recovered from local logs; interrupted work is labelled. No complete commit history exists.

# MH-013 Stage 3: 146 wardrobe portraits prepared

development-2026-11-11-artwork-stage-03-wardrobes | Development report | Artwork
Date: 2026-11-11

Completed staged wardrobe artwork for ten characters, matching their installed Stage 2 masters and corrected heights; live installation remains pending.

## Details

Completed production

Prepared 146 transparent 1024x1536 wardrobe portraits: Amy 14, April 14, Emily 14, Garrett 16, Ivan 13, Minsu 16, Rei 17, Samantha 14, Sophie 14 and Yuriko 14. All final files were visually reviewed at full size and on whole-family, three-background and normal/compact runtime-loader sheets. The installed Stage 2 masters remain the identity/proportion references. The lower thighs, knees, lower legs and feet stay outside the frame; short hems reveal connected upper thighs, while full trousers, leggings and long dresses continue through the picture crop. The existing 70% visible-body fitting convention, shared scale and entire height registry are unchanged.

Corrections

Emily’s ivory formal outfit now has a continuous pleated skirt instead of a shorts-like split. Minsu’s charcoal pyjamas have both connected upper thighs below the shorts hems. Samantha’s affected swim/dress hands were rebuilt with complete visible fingers; her formal suit, red flannel and red motorcycle jacket also have continuous sleeves and complete hands. Yuriko’s pocketless outfits show complete hands. Additional repairs preserved April’s small pendant, Garrett’s exposed neck tattoos, Emily’s full gym leggings and clean alpha, Minsu’s original muted blue swim shorts, and Sophie’s picnic skirt length.

Authorized sleepwear change

The user approved covered sleepwear in original colours after image-tool rejections. Amy uses white, April black, Emily blush pink, Minsu charcoal, Rei charcoal, Samantha burgundy and Sophie cobalt blue. Garrett retains the original black shorts design; Yuriko has no separate sleep asset in this scope. Ivan’s original coral beach outfit succeeded on the identical retry requested by the user. The three failed attempts and their resolutions are recorded.

Access and provenance

Review roadmap/artwork-stage-03/candidates, README.md, manifest.json, reviews and screenshots. These candidates are outside live wardrobe discovery: the current game still loads existing wardrobe PNGs. This is a Development report, not an installed release. There are 167 successful built-in image_gen outputs including revisions; the tool does not expose its exact model identifier. Accepted files match raw generated PNGs byte-for-byte. Exact prompts, input roles, source/output paths and hashes are retained, alongside original snapshots and superseded candidates. No local pixel postprocessing was used.

Verification

All 146 final candidates pass format, alpha, margins, provenance and hash-bound visual acceptance. All 306 baseline live artwork/reference files and the complete corrected stature table remain unchanged. The staged audit passes 292 normal/compact height comparisons, 62 saved wardrobe JSON round trips and 26 automatic occasion/sleep routes. The real-loader smoke renders all 146 paths at two thumbnail sizes and captures 20 screens, including normal/compact in-person solo/groups and three dark-phone correction previews, with no callback errors. All were visually inspected. Its first run completed the gallery but failed on a nonexistent Ivan outfit in the scene fixture; the fixture was corrected and the full rerun passed, with both logs retained. Phone dark-theme smoke passes 34 pages and embedded controls; lifestyle smoke passes all eight apps and outfit-job states; start smoke passes 28 previews.

Known limits

Seventy of 71 tests pass across nine related unit suites. The existing camera test_local_date_partner_can_join_photo failure still reports Theo absent from its fixture. Tests are offline and do not write player saves or call AI providers. Historical, masked, combat and remaining guard artwork belong to Stage 4. Live wardrobe installation and complete-collection release remain pending; full MH-013 stays In progress. Catalogue validation passed with 498 entries, export refreshed, and the patch-note reader smoke passed. After correcting the preference test to select a default-visible entry instead of assuming the first entry is a release, five of six patch-note unit tests pass. The existing archive-source failure remains for missing tests/screenshots/mixtape-art-review-0.jpg. Initial and corrected check logs are retained.

## Save compatibility

No migration, restart or player save changes for staged production. Existing wardrobe selections, identities, custom artwork, stored custom heights, relationships, unlocks and historical/masked precedence remain unchanged. Live portrait paths are not replaced.

## Evidence and historical limits

Produced and verified on 2026-11-11 under the authorized Stage 3 continuation, with user corrections for Emily’s skirt, Minsu’s visible upper thighs and Samantha’s fingers, plus approved covered sleepwear and the requested Ivan beach retry. No runtime artwork installation or full-project release is asserted.

- roadmap/artwork-stage-03/README.md
- roadmap/artwork-stage-03/manifest.json
- roadmap/artwork-stage-03/reviews.json
- roadmap/artwork-stage-03/outfit-briefs.json
- roadmap/artwork-stage-03/generations/failed-attempts.json
- roadmap/artwork-stage-03/checks/staged-routing-heights.json
- roadmap/artwork-stage-03/checks/presentation-render.json
- roadmap/artwork-stage-03/checks/units.json
- roadmap/artwork-stage-03/checks/smokes.json
- tools/artwork_stage_03.py
- tests/artwork_stage_03_ui_smoke.py
- roadmap/artwork-stage-03/checks/publication.json
- roadmap/artwork-stage-03/checks/publication-unit-rerun.json
- tests/test_patch_notes.py
