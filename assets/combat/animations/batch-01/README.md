# MH-001 combat animation batch 01

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Six foundation effects: slash, blunt impact, projectile, magic, heal and shield.

Historical review paths: combined preview `batch-01-preview.gif`, individual animations in `gifs/`, and original generated PNGs in `spritesheets/`. These files were removed on 2026-11-13. These are project-local artwork deliverables, not an installed combat-window feature.

Each source is a 1536x1024 sheet with six 512x512 cells, ordered left-to-right then top-to-bottom. Each GIF displays those six frames at 80ms each, then a 720ms blank pause before repeating. No generated artwork was replaced with procedural drawings. A shared per-asset palette limits frame-to-frame colour changes. Backgrounds are opaque dark slate with original generated shading; transparency is not claimed.

Rebuild from the project root with `python tools/build_combat_batch_gifs.py`. This also decodes every result and verifies dimensions, frame counts, durations and looping, and updates file hashes in `manifest.json`. The manifest contains the full prompt set and generation source paths. Generation used built-in image_gen; Images 2.6 was requested but the tool did not expose or verify its exact model version.

Reviewed: all six source sheets and the assembled peak-frame contact image. Pending: in-game playback, dark-matte compositing on location art, resolved outcome timing, mirrored opponent variants, Reduced Motion and Fast Combat. The GIF loop is for review; runtime playback must finish after one event. No game or save changes. No gameplay tests were needed or claimed for this standalone asset batch.

Batch schedule: `roadmap/COMBAT_GIF_BATCHES.md` in the project root. Preserve existing action IDs and keep combat inside the in-person window during later integration. Release patch notes belong with the player-visible integration, not this unreleased asset preparation.

