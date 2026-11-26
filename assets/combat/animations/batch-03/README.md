# MH-001 combat animation batch 03

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Eight sprite sheets were generated first with built-in image_gen and then sliced into GIFs using Pillow. [The manifest](manifest.json) preserves full generation/edit prompts, source paths and source/output hashes. The tool does not expose a verified model version.

Open the combined animated preview (retired path: `batch-03-preview.gif`). Individual assets:

| Effect | GIF | Sprite sheet |
| --- | --- | --- |
| Poison | GIF (retired path: `gifs/poison.gif`) | PNG (retired path: `spritesheets/poison.png`) |
| Burn | GIF (retired path: `gifs/burn.gif`) | PNG (retired path: `spritesheets/burn.png`) |
| Stagger | GIF (retired path: `gifs/stagger.gif`) | PNG (retired path: `spritesheets/stagger.png`) |
| Weak-point mark | GIF (retired path: `gifs/weak-point-mark.gif`) | PNG (retired path: `spritesheets/weak-point-mark.png`) |
| Concealment | GIF (retired path: `gifs/concealment.gif`) | PNG (retired path: `spritesheets/concealment.png`) |
| Barrier break | GIF (retired path: `gifs/barrier-break.gif`) | PNG (retired path: `spritesheets/barrier-break.png`) |
| Recovery | GIF (retired path: `gifs/recovery.gif`) | PNG (retired path: `spritesheets/recovery.png`) |
| Movement/escape | GIF (retired path: `gifs/movement-escape.gif`) | PNG (retired path: `spritesheets/movement-escape.png`) |

Each original sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 80ms action frames plus a 720ms blank review pause, repeating every 1200ms. Backgrounds are opaque dark slate with generated shading retained. No transparency is claimed.

Rebuild from the project root with `python tools/build_combat_batch_gifs.py --batch 3`. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. All final sheets and the assembled contact image were visually inspected. Movement was revised to remove panel borders; stagger was revised to fade the final poses. The combined preview contains all eight assets in three rows.

Poison and burn are finite status pulses; these previews are not seamless sustained-status loops. The posture and movement cues use generic martial artists, with appearance differences between sheets, not a continuous named-character animation set. Recovery means regaining posture, not restoring health. Barrier break and escape movement must only accompany appropriate resolved events; they do not determine combat outcomes.

This is unreleased artwork preparation. In-game playback, overlay compositing, opponent mirroring, persistent status-loop behavior, Reduced Motion and Fast Combat remain pending. No game code, phone UI or saves changed. Runtime playback must be event-driven and finite where appropriate rather than blindly following the GIF review loop. Release patch notes belong with player-visible integration.
