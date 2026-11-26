# MH-001 combat animation batch 10

> **Withdrawn 2026-11-13.** All GIFs, sprite sheets, combined preview and contact image from this batch were removed for the combat animation reset. The manifest and this README are historical production evidence; paths below are retired, and rebuild commands are historical only. No runtime integration or release is claimed. Future work follows the [combat animation style guide](../../../../roadmap/COMBAT_ANIMATION_STYLE_GUIDE.md).


Eight Silat/Aikido master sprite sheets generated first with built-in image_gen, then sliced into GIFs locally with Pillow. [The manifest](manifest.json) preserves exact prompts, source paths and source/output hashes. Exact generator model identity is unverified.

Open the combined animated preview (retired path: `batch-10-preview.gif`).

| Move | GIF | Sprite sheet |
| --- | --- | --- |
| serpent lattice | GIF (retired path: `gifs/serpent-lattice.gif`) | PNG (retired path: `spritesheets/serpent-lattice.png`) |
| phantom crescent | GIF (retired path: `gifs/phantom-crescent.gif`) | PNG (retired path: `spritesheets/phantom-crescent.png`) |
| falling canopy | GIF (retired path: `gifs/falling-canopy.gif`) | PNG (retired path: `spritesheets/falling-canopy.png`) |
| mirror snare | GIF (retired path: `gifs/mirror-snare.gif`) | PNG (retired path: `spritesheets/mirror-snare.png`) |
| still water reversal | GIF (retired path: `gifs/still-water-reversal.gif`) | PNG (retired path: `spritesheets/still-water-reversal.png`) |
| world axis turn | GIF (retired path: `gifs/world-axis-turn.gif`) | PNG (retired path: `spritesheets/world-axis-turn.png`) |
| orbit of silence | GIF (retired path: `gifs/orbit-of-silence.gif`) | PNG (retired path: `spritesheets/orbit-of-silence.png`) |
| returning mountain | GIF (retired path: `gifs/returning-mountain.gif`) | PNG (retired path: `spritesheets/returning-mountain.png`) |

Each sheet is 1536x1024 with six 512x512 cells in row-major order. Each GIF uses six 150ms action frames (900ms) plus a 720ms blank review pause, repeating every 1620ms. These are opaque dark-slate keyframe previews, not transparent overlays or seamless loops.

Rebuild: python tools/build_combat_batch_gifs.py --batch 10. All eight GIFs passed decoding, seven-frame, dimensions, duration and loop checks. The combined 960x1056 preview passed independent decoding, frame/timing/loop checks. All source sheets and the assembled contact image were visually inspected.

Serpent lattice uses intertwined curved contact trails. Phantom crescent combines a faint high pose with a low sweep. Falling canopy dips under a strike, enters close and throws. Mirror snare cues right before reversing left, ending with the target crouched low rather than lying down. Still-water reversal turns the incoming line into a circle and downward redirection. World-axis turn uses a planted-foot marker and ghosted rotation arc, ending in a low landing pose. Orbit of silence keeps both figures standing with uninterrupted trails. Returning mountain absorbs a rush and redirects it into a grounded throw.

Generic figure clothing, hair, scale and spacing vary between sheets. Some generated outfits have tied waist sashes. Ghost poses emphasize motion, and precise grips and trajectory geometry are illustrative. Faint figures remain in the sixth frame before the blank pause. These are stylized action cues, not named-character depictions or technical martial-arts instruction.

Unreleased asset preparation only. Runtime action-ID mapping, integration inside the in-person window, failed/resisted variants, compositing, mirrored opponents, Reduced Motion and Fast Combat remain pending. Artwork does not establish damage, hit counts or guaranteed throws/control. No game code, phone surfaces or saves changed; no gameplay smoke-test pass is claimed. Release patch notes belong with player-visible integration. Catalogue validation passed with 461 entries and the Markdown export was refreshed.
