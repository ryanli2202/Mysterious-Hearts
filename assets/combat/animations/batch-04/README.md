# MH-001 combat animation batch 04

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Eight boxing-master sprite sheets were generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves the full prompt set, source paths and hashes. The tool does not expose a verified model version.

Open the combined animated preview (retired path: `batch-04-preview.gif`).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| hurricane punches | GIF (retired path: `gifs/hurricane-punches.gif`) | PNG (retired path: `spritesheets/hurricane-punches.png`) |
| ghost step | GIF (retired path: `gifs/ghost-step.gif`) | PNG (retired path: `spritesheets/ghost-step.png`) |
| unseen spectre | GIF (retired path: `gifs/unseen-spectre.gif`) | PNG (retired path: `spritesheets/unseen-spectre.png`) |
| power breaker | GIF (retired path: `gifs/power-breaker.gif`) | PNG (retired path: `spritesheets/power-breaker.png`) |
| phantom cadence | GIF (retired path: `gifs/phantom-cadence.gif`) | PNG (retired path: `spritesheets/phantom-cadence.png`) |
| thunderclap counter | GIF (retired path: `gifs/thunderclap-counter.gif`) | PNG (retired path: `spritesheets/thunderclap-counter.png`) |
| iron constellation | GIF (retired path: `gifs/iron-constellation.gif`) | PNG (retired path: `spritesheets/iron-constellation.png`) |
| vanishing bell | GIF (retired path: `gifs/vanishing-bell.gif`) | PNG (retired path: `spritesheets/vanishing-bell.png`) |

Each source is 1536x1024 with six 512x512 frames in row-major order. Each GIF uses six 150ms action frames (900ms), matching the plan's 700–1100ms master-move timing, followed by a 720ms blank review pause. Total loop duration is 1620ms. Backgrounds are opaque dark slate with original generated shading; no transparency is claimed.

Rebuild from the project root with `python tools/build_combat_batch_gifs.py --batch 4`. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. All source sheets and the assembled contact image were visually inspected. Some figures remain visible in their last pose before the blank review pause; these are finite keyframe previews, not seamless loops. Phantom cadence includes a quiet third frame before its burst. The contact image shows frame three, so the fourth-frame constellation, barrage and bell finishers are best reviewed in the GIFs or sheets.

The illustrations represent the planned successful-action choreography, not verified runtime outcomes or exact hit counts. Ghost step represents the movement portion only. Generic figures differ across sheets and are not named-character portraits. Power-breaker, counters and multi-hit visuals still require outcome-specific variants; do not infer extra damage or successful guard breaks from the art.

This is unreleased artwork preparation. Runtime action-ID mapping, integration inside the in-person window, compositing, opponent mirroring, outcome synchronization, Reduced Motion and Fast Combat remain pending. No game code, phone UI or saves changed. Release patch notes belong with player-visible integration.
