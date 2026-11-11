# MH-001 combat animation batch 03

Eight sprite sheets were generated first with built-in image_gen and then sliced into GIFs using Pillow. [The manifest](manifest.json) preserves full generation/edit prompts, source paths and source/output hashes. The tool does not expose a verified model version.

Open [the combined animated preview](batch-03-preview.gif). Individual assets:

| Effect | GIF | Sprite sheet |
| --- | --- | --- |
| Poison | [GIF](gifs/poison.gif) | [PNG](spritesheets/poison.png) |
| Burn | [GIF](gifs/burn.gif) | [PNG](spritesheets/burn.png) |
| Stagger | [GIF](gifs/stagger.gif) | [PNG](spritesheets/stagger.png) |
| Weak-point mark | [GIF](gifs/weak-point-mark.gif) | [PNG](spritesheets/weak-point-mark.png) |
| Concealment | [GIF](gifs/concealment.gif) | [PNG](spritesheets/concealment.png) |
| Barrier break | [GIF](gifs/barrier-break.gif) | [PNG](spritesheets/barrier-break.png) |
| Recovery | [GIF](gifs/recovery.gif) | [PNG](spritesheets/recovery.png) |
| Movement/escape | [GIF](gifs/movement-escape.gif) | [PNG](spritesheets/movement-escape.png) |

Each original sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 80ms action frames plus a 720ms blank review pause, repeating every 1200ms. Backgrounds are opaque dark slate with generated shading retained. No transparency is claimed.

Rebuild from the project root with `python tools/build_combat_batch_gifs.py --batch 3`. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. All final sheets and the assembled contact image were visually inspected. Movement was revised to remove panel borders; stagger was revised to fade the final poses. The combined preview contains all eight assets in three rows.

Poison and burn are finite status pulses; these previews are not seamless sustained-status loops. The posture and movement cues use generic martial artists, with appearance differences between sheets, not a continuous named-character animation set. Recovery means regaining posture, not restoring health. Barrier break and escape movement must only accompany appropriate resolved events; they do not determine combat outcomes.

This is unreleased artwork preparation. In-game playback, overlay compositing, opponent mirroring, persistent status-loop behavior, Reduced Motion and Fast Combat remain pending. No game code, phone UI or saves changed. Runtime playback must be event-driven and finite where appropriate rather than blindly following the GIF review loop. Release patch notes belong with player-visible integration.
