# MH-001 combat animation batch 07

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Eight Muay Thai/streetfighting master sprite sheets generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves exact prompts, source paths and source/output hashes. Exact generator model identity is unverified.

Open the combined animated preview (retired path: `batch-07-preview.gif`).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| eight limbed tempest | GIF (retired path: `gifs/eight-limbed-tempest.gif`) | PNG (retired path: `spritesheets/eight-limbed-tempest.png`) |
| meteor knee | GIF (retired path: `gifs/meteor-knee.gif`) | PNG (retired path: `spritesheets/meteor-knee.png`) |
| titan clinch | GIF (retired path: `gifs/titan-clinch.gif`) | PNG (retired path: `spritesheets/titan-clinch.png`) |
| thunder pillar | GIF (retired path: `gifs/thunder-pillar.gif`) | PNG (retired path: `spritesheets/thunder-pillar.png`) |
| riot engine | GIF (retired path: `gifs/riot-engine.gif`) | PNG (retired path: `spritesheets/riot-engine.png`) |
| backstreet phantom | GIF (retired path: `gifs/backstreet-phantom.gif`) | PNG (retired path: `spritesheets/backstreet-phantom.png`) |
| concrete verdict | GIF (retired path: `gifs/concrete-verdict.gif`) | PNG (retired path: `spritesheets/concrete-verdict.png`) |
| chaos rhythm | GIF (retired path: `gifs/chaos-rhythm.gif`) | PNG (retired path: `spritesheets/chaos-rhythm.png`) |

Each sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 150ms action frames (900ms) plus a 720ms blank review pause, repeating every 1620ms. These are opaque dark-slate keyframe previews, not transparent overlays or seamless loops.

Rebuild: python tools/build_combat_batch_gifs.py --batch 7. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. The combined 960x1056 preview passed independent decoding, frame/timing/loop checks. All source sheets and the assembled contact image were visually inspected.

Eight-limbed tempest alternates punch, elbow, knee and kick poses. Meteor knee rises diagonally into the guard. Titan clinch remains a standing posture contest. Thunder pillar uses a horizontal compressed-air roundhouse wake. Riot engine changes strike heights and closes distance. Backstreet phantom circles with connected movement trails and faint prior poses. Concrete verdict uses a square-edged compression graphic and a few small debris flecks; those must be adapted to the arena surface during integration. Chaos rhythm pauses in guard across frames two and three before low-to-high strikes restart.

The generic figures have hair and skin tones rather than the monochrome silhouettes of batch six. They are not named-character depictions. Figure scale and spacing vary between sheets. Poses and trails approximate choreography rather than exact mechanics or technical martial-arts instruction. Faint figures remain at frame six before the blank pause.

Unreleased asset preparation only. Runtime action-ID mapping, integration inside the in-person window, outcome-specific variants, compositing, mirrored opponents, Reduced Motion and Fast Combat remain pending. Artwork does not establish hit counts, damage or successful control. No game code, phone surfaces or saves changed; no gameplay smoke-test pass is claimed. Release patch notes belong with player-visible integration. Catalogue validation passed with 461 entries and the Markdown export was refreshed.
