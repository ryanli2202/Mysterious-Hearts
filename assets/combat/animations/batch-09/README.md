# MH-001 combat animation batch 09

Eight Military CQC/kickboxing master sprite sheets generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves exact generation and revision prompts, original paths and source/output hashes. Exact generator model identity is unverified.

Open [the combined animated preview](batch-09-preview.gif).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| breach sequence | [GIF](gifs/breach-sequence.gif) | [PNG](spritesheets/breach-sequence.png) |
| lockdown engine | [GIF](gifs/lockdown-engine.gif) | [PNG](spritesheets/lockdown-engine.png) |
| silent vector | [GIF](gifs/silent-vector.gif) | [PNG](spritesheets/silent-vector.png) |
| titan restraint | [GIF](gifs/titan-restraint.gif) | [PNG](spritesheets/titan-restraint.png) |
| tempest circuit | [GIF](gifs/tempest-circuit.gif) | [PNG](spritesheets/tempest-circuit.png) |
| sonic crescent | [GIF](gifs/sonic-crescent.gif) | [PNG](spritesheets/sonic-crescent.png) |
| iron comet | [GIF](gifs/iron-comet.gif) | [PNG](spritesheets/iron-comet.png) |
| phantom relay | [GIF](gifs/phantom-relay.gif) | [PNG](spritesheets/phantom-relay.png) |

Each sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 150ms action frames (900ms) plus a 720ms blank review pause, repeating every 1620ms. These are opaque dark-slate keyframe previews, not transparent overlays or seamless loops.

Rebuild: python tools/build_combat_batch_gifs.py --batch 9. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. The combined 960x1056 preview passed independent decoding, frame/timing/loop checks. All final source sheets and the assembled contact image were visually inspected.

Breach sequence links a low entry to disruption and standing arm control. Lockdown engine transfers markers between wrist, elbow and shoulder holds; this depicts one illustrative successful transition, and markers must follow actual resolved control outcomes during integration. Silent vector closes distance with faint low trails and no strike. Titan restraint shows standing struggle using brackets and tension strokes. Tempest circuit alternates punches and kicks. Sonic crescent separates the thin leading arc from the later wider wake. Iron comet follows a punch impact with a driving kick. Phantom relay alternates close and longer range with ghosted prior poses; a targeted image edit moved and reduced the lower-row afterimages to prevent clipping. Ghost scale is illustrative rather than physically consistent.

Generic figures have hair and skin tones; some kickboxing sheets include hand wraps. They are not named characters. Scale, spacing and exact hand placement vary between sheets. Faint figures remain at frame six before the blank pause. Choreography is stylized, not technical martial-arts instruction.

Unreleased asset preparation only. Runtime action-ID mapping, integration inside the in-person window, unsuccessful/resisted control variants, compositing, mirrored opponents, Reduced Motion and Fast Combat remain pending. Artwork does not establish damage, hit counts or guaranteed control. No game code, phone surfaces or saves changed; no gameplay smoke-test pass is claimed. Release patch notes belong with player-visible integration. Catalogue validation passed with 461 entries and the Markdown export was refreshed.
