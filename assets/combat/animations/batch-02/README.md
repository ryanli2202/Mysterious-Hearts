# MH-001 combat animation batch 02

Eight sprite sheets were generated first with built-in image_gen, then sliced and encoded locally with Pillow. Full prompts, source paths and output hashes are in [manifest.json](manifest.json). The generator did not report a verifiable model version.

Open [the combined animated preview](batch-02-preview.gif) to review all eight effects. Individual GIFs and their original sheets:

| Effect | GIF | Sprite sheet |
| --- | --- | --- |
| Block | [GIF](gifs/block.gif) | [PNG](spritesheets/block.png) |
| Dodge | [GIF](gifs/dodge.gif) | [PNG](spritesheets/dodge.png) |
| Miss | [GIF](gifs/miss.gif) | [PNG](spritesheets/miss.png) |
| Critical emphasis | [GIF](gifs/critical-emphasis.gif) | [PNG](spritesheets/critical-emphasis.png) |
| Casting glow | [GIF](gifs/casting-glow.gif) | [PNG](spritesheets/casting-glow.png) |
| Buff particles | [GIF](gifs/buff-particles.gif) | [PNG](spritesheets/buff-particles.png) |
| Recoil | [GIF](gifs/recoil.gif) | [PNG](spritesheets/recoil.png) |
| Weapon trails | [GIF](gifs/weapon-trails.gif) | [PNG](spritesheets/weapon-trails.png) |

Each source is 1536x1024, arranged in three columns and two rows. Each GIF is 512x512 with six 80ms action frames followed by a 720ms blank rest, repeating for review. Original generated shading is retained on an opaque dark background. These are not transparent overlays. Dodge and recoil use generic faceless martial-artist figures as action cues rather than named-character artwork. Weapon trails provide a generic swing layer; weapon-specific variants remain integration work.

Rebuild from the project root: `python tools/build_combat_batch_gifs.py --batch 2`. All eight GIFs were decoded and checked for dimensions, seven frames, timing and looping. All source sheets and the assembled contact image were visually inspected. The combined preview accommodates all eight assets in three rows.

This batch is asset preparation, not a gameplay release. Combat-window playback, outcome synchronization, opponent mirroring, transparent compositing, Reduced Motion and Fast Combat remain pending. Runtime must play a finite event rather than following the preview's infinite loop. No game code, phone UI or saves changed. Release patch notes will accompany player-visible integration.
