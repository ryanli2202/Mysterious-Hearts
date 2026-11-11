# MH-001 combat animation batch 04

Eight boxing-master sprite sheets were generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves the full prompt set, source paths and hashes. The tool does not expose a verified model version.

Open [the combined animated preview](batch-04-preview.gif).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| hurricane punches | [GIF](gifs/hurricane-punches.gif) | [PNG](spritesheets/hurricane-punches.png) |
| ghost step | [GIF](gifs/ghost-step.gif) | [PNG](spritesheets/ghost-step.png) |
| unseen spectre | [GIF](gifs/unseen-spectre.gif) | [PNG](spritesheets/unseen-spectre.png) |
| power breaker | [GIF](gifs/power-breaker.gif) | [PNG](spritesheets/power-breaker.png) |
| phantom cadence | [GIF](gifs/phantom-cadence.gif) | [PNG](spritesheets/phantom-cadence.png) |
| thunderclap counter | [GIF](gifs/thunderclap-counter.gif) | [PNG](spritesheets/thunderclap-counter.png) |
| iron constellation | [GIF](gifs/iron-constellation.gif) | [PNG](spritesheets/iron-constellation.png) |
| vanishing bell | [GIF](gifs/vanishing-bell.gif) | [PNG](spritesheets/vanishing-bell.png) |

Each source is 1536x1024 with six 512x512 frames in row-major order. Each GIF uses six 150ms action frames (900ms), matching the plan's 700–1100ms master-move timing, followed by a 720ms blank review pause. Total loop duration is 1620ms. Backgrounds are opaque dark slate with original generated shading; no transparency is claimed.

Rebuild from the project root with `python tools/build_combat_batch_gifs.py --batch 4`. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. All source sheets and the assembled contact image were visually inspected. Some figures remain visible in their last pose before the blank review pause; these are finite keyframe previews, not seamless loops. Phantom cadence includes a quiet third frame before its burst. The contact image shows frame three, so the fourth-frame constellation, barrage and bell finishers are best reviewed in the GIFs or sheets.

The illustrations represent the planned successful-action choreography, not verified runtime outcomes or exact hit counts. Ghost step represents the movement portion only. Generic figures differ across sheets and are not named-character portraits. Power-breaker, counters and multi-hit visuals still require outcome-specific variants; do not infer extra damage or successful guard breaks from the art.

This is unreleased artwork preparation. Runtime action-ID mapping, integration inside the in-person window, compositing, opponent mirroring, outcome synchronization, Reduced Motion and Fast Combat remain pending. No game code, phone UI or saves changed. Release patch notes belong with player-visible integration.
