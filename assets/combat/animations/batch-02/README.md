# MH-001 combat animation batch 02

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Eight sprite sheets were generated first with built-in image_gen, then sliced and encoded locally with Pillow. Full prompts, source paths and output hashes are in [manifest.json](manifest.json). The generator did not report a verifiable model version.

Open the combined animated preview (retired path: `batch-02-preview.gif`) to review all eight effects. Individual GIFs and their original sheets:

| Effect | GIF | Sprite sheet |
| --- | --- | --- |
| Block | GIF (retired path: `gifs/block.gif`) | PNG (retired path: `spritesheets/block.png`) |
| Dodge | GIF (retired path: `gifs/dodge.gif`) | PNG (retired path: `spritesheets/dodge.png`) |
| Miss | GIF (retired path: `gifs/miss.gif`) | PNG (retired path: `spritesheets/miss.png`) |
| Critical emphasis | GIF (retired path: `gifs/critical-emphasis.gif`) | PNG (retired path: `spritesheets/critical-emphasis.png`) |
| Casting glow | GIF (retired path: `gifs/casting-glow.gif`) | PNG (retired path: `spritesheets/casting-glow.png`) |
| Buff particles | GIF (retired path: `gifs/buff-particles.gif`) | PNG (retired path: `spritesheets/buff-particles.png`) |
| Recoil | GIF (retired path: `gifs/recoil.gif`) | PNG (retired path: `spritesheets/recoil.png`) |
| Weapon trails | GIF (retired path: `gifs/weapon-trails.gif`) | PNG (retired path: `spritesheets/weapon-trails.png`) |

Each source is 1536x1024, arranged in three columns and two rows. Each GIF is 512x512 with six 80ms action frames followed by a 720ms blank rest, repeating for review. Original generated shading is retained on an opaque dark background. These are not transparent overlays. Dodge and recoil use generic faceless martial-artist figures as action cues rather than named-character artwork. Weapon trails provide a generic swing layer; weapon-specific variants remain integration work.

Rebuild from the project root: `python tools/build_combat_batch_gifs.py --batch 2`. All eight GIFs were decoded and checked for dimensions, seven frames, timing and looping. All source sheets and the assembled contact image were visually inspected. The combined preview accommodates all eight assets in three rows.

This batch is asset preparation, not a gameplay release. Combat-window playback, outcome synchronization, opponent mirroring, transparent compositing, Reduced Motion and Fast Combat remain pending. Runtime must play a finite event rather than following the preview's infinite loop. No game code, phone UI or saves changed. Release patch notes will accompany player-visible integration.
