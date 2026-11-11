# MH-013 planning verification

Recorded 2026-11-10 (Australia/Brisbane). Documentation and inspection artifacts only; no runtime, save or character PNG changes made by this task.

## Completed review

- Inventoried 300 portrait-directory PNGs and six related transparent profile/appearance reference files. Recorded dimensions, source mode, alpha minimum/fractions/bounds and SHA-256 for all 306.
- Scanned alpha-bearing PNGs outside the portrait directory to identify the two profile files and four Grove appearance/tattoo references. Sprites, scenery, UI marks and raw generation archives are separate asset classes.
- Visually inspected all 26 complete-canvas slate sheets (A001–A306).
- Opened Ivan selection and Charles selection v2 individually, then reviewed their slate/neutral-grey comparison.
- Reviewed twelve face crops: both anchors, Amy, April, Emily, Garrett, Rei, current Minsu, archived Minsu v1, Sophie, Yuriko and Priya.
- Inspected portrait resolution, special Charles/Neo paths, four-character relative height code, wardrobe discovery, historical priority, combat thumbnail fitting and guard/boss routing.
- Confirmed five byte-identical source groups, recorded in the audit. Alpha presence and partial-alpha percentage are not production acceptance.
- `python roadmap/artwork-portrait-audit/compile_audit.py`: passed 306 unique ordered assessments, valid dispositions and 26 linked sheets. Totals: R 210, P 50, F 25, H 7, E 14.

## Documentation/catalogue checks

- Inventory/content check: passed. Exactly 306 ordered notes cover 306 files; all 300 portrait-directory PNGs are accounted for; 295 have alpha below 255.
- Source-preservation check: passed. All 306 SHA-256 hashes still match the baseline after planning edits.
- Local-link check: passed for 344 links in the plan, art guide, audit and verification documents at the time of checking.
- Roadmap check: passed. One MH-013 row and section; concurrent MH-012 Ace-campaign planning remains preserved. The earlier unrelated duplicate MH-004 was not renumbered.
- `python patch_notes.py validate`: passed, 481 entries at verification time.
- `python -m unittest discover -s tests -p test_patch_notes.py -v`: final result **5 passed, 1 failed**. The existing archive-source check fails because `tests/screenshots/mixtape-art-review-0.jpg` is missing. This was already documented by earlier release records; no historical evidence was fabricated.
- The initial test run also exposed an ordering assumption when the new Development report preceded the curated releases. Moving this planning record to the start of the existing Development-report section restored the preference test. Final run has only the historical missing-source failure; no runtime/test implementation was changed.
- `python patch_notes.py export`: completed, refreshing `patch_notes/PATCH_NOTES.md` with its normal curated scope.
- `python patch_notes.py export --reports --query MH-013 --output roadmap/artwork-portrait-audit/PLANNING_RECORD.md`: completed, exporting the single planning record separately.

These are actual planning/catalogue checks. The five passing patch-note tests do not validate replacement artwork or in-game presentation.

## Pending production acceptance

No replacement generation, full-resolution acceptance of every source/replacement, game screenshots, gameplay checks or phone smoke checks were performed in this planning pass. New artwork, rendering changes and save compatibility remain pending. The plan names the checks to run when those changes exist.

The planning catalogue record uses `Development report` with a date of recording, not `Release` or a promised release date. Default patch-note export excludes Development reports; a separate MH-013-only Markdown export preserves the planning record without changing that established behaviour.
