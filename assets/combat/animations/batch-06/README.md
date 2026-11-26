# MH-001 combat animation batch 06

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Eight Kyokushin/MMA master sprite sheets generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves exact prompts, source paths and hashes. Exact generator model identity is unverified.

Open the combined animated preview (retired path: `batch-06-preview.gif`).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| mountain splitter | GIF (retired path: `gifs/mountain-splitter.gif`) | PNG (retired path: `spritesheets/mountain-splitter.png`) |
| adamant advance | GIF (retired path: `gifs/adamant-advance.gif`) | PNG (retired path: `spritesheets/adamant-advance.png`) |
| hundred beat barrage | GIF (retired path: `gifs/hundred-beat-barrage.gif`) | PNG (retired path: `spritesheets/hundred-beat-barrage.png`) |
| thunder heel | GIF (retired path: `gifs/thunder-heel.gif`) | PNG (retired path: `spritesheets/thunder-heel.png`) |
| apex chain | GIF (retired path: `gifs/apex-chain.gif`) | PNG (retired path: `spritesheets/apex-chain.png`) |
| predator switch | GIF (retired path: `gifs/predator-switch.gif`) | PNG (retired path: `spritesheets/predator-switch.png`) |
| gravity crash | GIF (retired path: `gifs/gravity-crash.gif`) | PNG (retired path: `spritesheets/gravity-crash.png`) |
| total control | GIF (retired path: `gifs/total-control.gif`) | PNG (retired path: `spritesheets/total-control.png`) |

Each sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 150ms action frames (900ms) plus a 720ms blank review pause, repeating every 1620ms. These are opaque dark-slate keyframe previews, not transparent overlays or seamless loops.

Rebuild: python tools/build_combat_batch_gifs.py --batch 6. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. The combined 960x1056 preview passed frame/timing/loop checks. All source sheets and the assembled contact image were visually inspected.

Mountain-splitter splits its impact graphic vertically. Adamant advance braces against incoming strikes. Hundred-beat barrage alternates torso impacts and a low kick. Thunder heel includes a stationary defender despite the single-figure prompt; its high heel drops into a compact ring. Apex chain reaches ground control; Predator switch ends at a low takedown entry; Gravity crash lands both figures at one point; Total control uses ghosted positions and shifting pressure markers. Some figures remain visible in the sixth frame before the blank pause. Figure appearances and spacing vary across sheets; choreography is stylized, not technical martial-arts instruction.

Unreleased asset preparation only. Runtime action-ID mapping, integration inside the in-person window, outcome-specific variants, compositing, mirrored opponents, Reduced Motion and Fast Combat remain pending. Artwork does not determine hit counts, damage or successful control. No game code, phone surfaces or saves changed; no gameplay smoke-test pass is claimed. Release patch notes belong with player-visible integration. Catalogue validation passed with 461 entries and the Markdown export was refreshed.
