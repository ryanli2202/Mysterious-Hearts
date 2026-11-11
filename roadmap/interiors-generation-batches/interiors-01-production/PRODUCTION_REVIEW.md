# Interiors batch 01 — artwork production review

**Date:** 2026-11-11 (Australia/Brisbane)  
**Roadmap:** MH-004 Lived-In Interiors  
**Status:** 48/48 assigned new images generated and statically accepted. Runtime integration and in-person rendered verification are pending.

## Deliverables

[Open the full review gallery](gallery.html). Every image links to its full-size PNG. Final files are under `assets/ui/locations/interiors/`, using the stable targets in the [batch manifest](../interiors-01.json).

| Building/group | Accepted new images |
| --- | ---: |
| Rei and Yuriko’s penthouse | 8 |
| Emily’s garden apartment | 7 |
| Sophie’s trackside loft | 6 |
| Shared dorm corridor | 1 |
| Samantha’s garage flat | 6 |
| April’s observatory townhouse | 10 |
| Garrett’s hillside estate | 10 |
| Total | 48 |

44 interior views and four outdoor views; every final PNG is 1536×1024. The accepted files total 127,799,383 bytes. Each is a separate scene, with no collage or embedded navigation labels.

## Generation and review

Used built-in `image_gen`, one call per image/attempt. The underlying model identifier is not exposed by the tool and has not been guessed. Exact prompts, reference paths and rejected-attempt provenance are retained in [prompts.json](prompts.json). Final original-generation paths, hashes, image modes and individual visual-review notes are in the batch manifest.

Inspected the eight existing home references at full size, then generated and inspected one building at a time. Generated originals remain in the tool’s default output folder; selected files were copied through project staging into the planned asset paths without overwriting existing location art. Static review checked room purpose, materials, doors, foreground clearance, people/text exclusion, and indoor/outdoor treatment.

Three attempts were rejected and replaced: Emily’s bathroom initially showed the living room; April’s entrance added an unplanned staircase; April’s first stair view did not match the accepted hall’s turn and runner. Exact initial prompts, source paths and reasons are preserved. There were 51 successful image-generation calls yielding 48 selected deliverables and three discarded attempts. Discarded image files remain at their tool-provided source paths.

## Actual verification

`python tools/verify_interiors_batch_01.py` passed. [Machine-readable results](verification.json) confirm:

- Exact 48-image ID/path/prompt coverage and static review records.
- PNG format, 1536×1024 dimensions and matching batch/inventory SHA-256 hashes.
- 48 unique file hashes and 48 unique decoded-pixel hashes; full-size visual inspection also checked that the views are distinct.
- All eight original reference files still match their inventory hashes.
- Ten nonempty baseline batches retain all 438 assigned new-image IDs with unique target paths.
- Both planning generators refuse to erase started production metadata; protected record files remained unchanged during those checks.

`python patch_notes.py validate` passed with 498 existing entries. `python patch_notes.py export` refreshed `patch_notes/PATCH_NOTES.md`. No new release catalogue entry was created: these new files are not routed to runtime rooms and are not a player-visible release.

## Integration limits and next work

The generation request is complete for the 48 assigned rows. Access is through the gallery and asset files; room navigation has not been implemented. Original scene routing and saves are unchanged. No migration, restart, phone feature, gameplay test or in-person rendered acceptance is claimed by this artwork operation.

The new scenes need room mappings, weather/lighting classification, crop and live-character-overlay checks in the actual in-person window. Sophie’s sleeping-loft stair junction in particular should be checked in the final scene crop. Existing reused-room architectural compatibility and final in-game approval remain pending.

Garrett’s `assets/ui/locations/garrett_home.png` is an exterior estate facade/courtyard, despite its inventory allocation to living room. Its reuse as indoor living-room art was rejected; it was used only for architectural/material continuity. Add a dedicated living-room replacement through an explicit inventory/batch revision before enabling that room. This finding does not silently add a 49th image or alter the baseline allocation. The two unresolved dorm bathrooms remain excluded.

Initial planning scripts now stop if production metadata exists. Maintain stable IDs and revise the existing inventory/manifests explicitly instead of rebuilding them from planning-only inputs.
