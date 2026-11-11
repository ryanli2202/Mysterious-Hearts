# MH-001 combat animation batch 12

Eight Japanese Jujutsu/Wing Chun master sprite sheets generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves exact prompts, source paths, stable inventory production IDs and source/output hashes. Exact generator model identity is unverified.

Open [the combined animated preview](batch-12-preview.gif).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| thousand link bind | [GIF](gifs/thousand-link-bind.gif) | [PNG](spritesheets/thousand-link-bind.png) |
| earthfall reversal | [GIF](gifs/earthfall-reversal.gif) | [PNG](spritesheets/earthfall-reversal.png) |
| iron labyrinth | [GIF](gifs/iron-labyrinth.gif) | [PNG](spritesheets/iron-labyrinth.png) |
| silent avalanche | [GIF](gifs/silent-avalanche.gif) | [PNG](spritesheets/silent-avalanche.png) |
| thousand point rain | [GIF](gifs/thousand-point-rain.gif) | [PNG](spritesheets/thousand-point-rain.png) |
| centre line collapse | [GIF](gifs/centre-line-collapse.gif) | [PNG](spritesheets/centre-line-collapse.png) |
| mirror hands | [GIF](gifs/mirror-hands.gif) | [PNG](spritesheets/mirror-hands.png) |
| inch thunder | [GIF](gifs/inch-thunder.gif) | [PNG](spritesheets/inch-thunder.png) |

Each sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 150ms action frames (900ms) plus a 720ms blank review pause, repeating every 1620ms. These are opaque dark-slate keyframe previews, not transparent overlays or seamless loops.

Rebuild: python tools/build_combat_batch_gifs.py --batch 12. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. The combined 960x1056 preview passed independent decoding, frame/timing/loop checks. All source sheets and the assembled contact image were visually inspected.

Thousand-link bind moves contact markers between standing holds. Earthfall reversal tips an incoming commitment into a counterthrow. Iron labyrinth uses angular, sometimes arrow-shaped paths for positional pressure. Silent avalanche links entry, throw and grounded restraint. Thousand-point rain uses repeated compact punch poses, faint fist trails and small contact bursts; exact left/right alternation is not reliably depicted. Centre-line collapse compresses guard-line graphics while the guard remains present. Mirror hands alternates deflection and returning-strike poses, with exact hand switching illustrative. Inch thunder starts at very short range and produces a large local ring; its sixth pose remains fully visible before the blank pause.

Generic figure clothing, scale and spacing vary between sheets. Ghost poses and precise grips are illustrative. These are stylized action cues, not named-character depictions or technical martial-arts instruction. Successful control, guard breaks and hit counts must follow resolved gameplay outcomes.

Unreleased asset preparation only. Runtime action-ID mapping, integration inside the in-person window, failed/resisted variants, compositing, mirrored opponents, Reduced Motion and Fast Combat remain pending. No game code, phone surfaces or saves changed by this batch; no gameplay smoke-test pass is claimed. Release patch notes belong with player-visible integration. Catalogue validation passed with 462 entries and the Markdown export was refreshed. Batch 11 remains planned; batch 12 was produced directly at the user's request.
