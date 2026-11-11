# MH-001 combat animation batch 08

Eight Sanda/Jeet Kune Do master sprite sheets generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves exact prompts, source paths and source/output hashes. Exact generator model identity is unverified.

Open [the combined animated preview](batch-08-preview.gif).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| storm bridge | [GIF](gifs/storm-bridge.gif) | [PNG](spritesheets/storm-bridge.png) |
| sky catch reversal | [GIF](gifs/sky-catch-reversal.gif) | [PNG](spritesheets/sky-catch-reversal.png) |
| horizon breaker | [GIF](gifs/horizon-breaker.gif) | [PNG](spritesheets/horizon-breaker.png) |
| cyclone sweep | [GIF](gifs/cyclone-sweep.gif) | [PNG](spritesheets/cyclone-sweep.png) |
| stillpoint intercept | [GIF](gifs/stillpoint-intercept.gif) | [PNG](spritesheets/stillpoint-intercept.png) |
| vanishing line | [GIF](gifs/vanishing-line.gif) | [PNG](spritesheets/vanishing-line.png) |
| one beat thunder | [GIF](gifs/one-beat-thunder.gif) | [PNG](spritesheets/one-beat-thunder.png) |
| empty rhythm | [GIF](gifs/empty-rhythm.gif) | [PNG](spritesheets/empty-rhythm.png) |

Each sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 150ms action frames (900ms) plus a 720ms blank review pause, repeating every 1620ms. These are opaque dark-slate keyframe previews, not transparent overlays or seamless loops.

Rebuild: python tools/build_combat_batch_gifs.py --batch 8. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. The combined 960x1056 preview passed independent decoding, frame/timing/loop checks. All source sheets and the assembled contact image were visually inspected.

Storm bridge links a straight strike to grip and throw. Sky-catch reversal catches the airborne opponent and bends the trajectory down. Horizon breaker uses a heel-led side kick. Cyclone sweep takes the target off balance with a low circular sweep. Stillpoint intercept shows a small contact flash along the incoming line; its drawing approximates hand-to-hand contact rather than an exact wrist interception. Vanishing line shows an afterimage and a diagonal exit, with the strike passing through empty space. One-beat thunder holds a quiet starting stance before a short strike and strong ring. Empty rhythm alternates attacks with quiet frames two and four; the imagery illustrates timing and does not prove successful hits.

Generic figures have hair and skin tones, matching batch seven's treatment. They are not named characters. Scale and spacing vary between sheets. Faint figures remain at frame six, especially One-beat thunder, before the blank pause. The art is stylized choreography, not technical martial-arts instruction.

Unreleased asset preparation only. Runtime action-ID mapping, integration inside the in-person window, unsuccessful/resisted variants, compositing, mirrored opponents, Reduced Motion and Fast Combat remain pending. Artwork does not establish damage, hit counts or guaranteed throws. No game code, phone surfaces or saves changed; no gameplay smoke-test pass is claimed. Release patch notes belong with player-visible integration. Catalogue validation passed with 461 entries and the Markdown export was refreshed.
