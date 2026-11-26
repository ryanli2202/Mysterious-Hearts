# MH-001 combat animation batch 05

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Eight taekwondo/judo master sheets generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves full prompts, source paths and source/output hashes. Exact generator model version is not exposed by the tool.

Open the combined animated preview (retired path: `batch-05-preview.gif`).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| skywheel barrage | GIF (retired path: `gifs/skywheel-barrage.gif`) | PNG (retired path: `spritesheets/skywheel-barrage.png`) |
| horizon step | GIF (retired path: `gifs/horizon-step.gif`) | PNG (retired path: `spritesheets/horizon-step.png`) |
| falling star | GIF (retired path: `gifs/falling-star.gif`) | PNG (retired path: `spritesheets/falling-star.png`) |
| mirage wheel | GIF (retired path: `gifs/mirage-wheel.gif`) | PNG (retired path: `spritesheets/mirage-wheel.png`) |
| world turner | GIF (retired path: `gifs/world-turner.gif`) | PNG (retired path: `spritesheets/world-turner.png`) |
| falling mountain | GIF (retired path: `gifs/falling-mountain.gif`) | PNG (retired path: `spritesheets/falling-mountain.png`) |
| zero point reversal | GIF (retired path: `gifs/zero-point-reversal.gif`) | PNG (retired path: `spritesheets/zero-point-reversal.png`) |
| iron orbit | GIF (retired path: `gifs/iron-orbit.gif`) | PNG (retired path: `spritesheets/iron-orbit.png`) |

Each sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF displays six 150ms action frames (900ms) plus a 720ms blank pause, repeating every 1620ms for review. Original generated shading remains on an opaque dark slate background; these are not transparent overlays or seamless loops.

Rebuild from the project root: `python tools/build_combat_batch_gifs.py --batch 5`. All eight GIFs passed decoding, seven-frame, dimensions, duration and looping checks. All source sheets and the assembled contact image were visually inspected. Zero-point reversal holds its balance pose across frames two and three before the counterthrow; Iron orbit keeps both figures in standing grip without a completed throw. Figure appearance and spacing vary between sheets. This is stylized keyframe choreography, not a technical martial-arts demonstration.

The contact image shows frame three; later kicks, landings and reversal finishes are visible in the GIFs and original sheets. Playback and outcome-specific variants must follow the combat engine, including unsuccessful throws and resisted control. The art does not establish damage or guaranteed landings.

Unreleased asset preparation only. Runtime action-ID mapping, integration inside the in-person window, compositing, mirrored opponents, outcome synchronization, Reduced Motion and Fast Combat remain pending. No game code, phone UI or saves changed. Release patch notes belong with player-visible integration.
