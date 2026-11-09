Garrett side-scrolling sprite polish preview

Open walk-right.gif / walk-left.gif for eight-pose, 800ms walk loops.
Open idle-right.gif / idle-left.gif for held idle with a short blink.
GIFs display at 4x on dark slate; PNGs retain transparency at 48x64.
sprite-sheet.png: eight columns, four rows ordered idle-right, walk-right,
idle-left, walk-left. manifest.json supplies durations and the foot anchor.

Built-in image_gen produced the polish pass. The original output is retained
as source-sheet.png with its prompt. The packaging script aligns head centers
and foot baselines, holds one open-eye idle to reduce shimmer, and mirrors
the right-facing artwork for left. Asymmetric details mirror too.
The GIF encoder merges identical idle frames while retaining loop timing.

Movement direction is left/right only for the planned side-scrolling areas.
The original Garrett preview is preserved in the sibling garrett directory.
This asset revision does not yet connect to the map, movement or saves.
Generated details still vary slightly during walking and the blink. Actual
foot sliding must be evaluated against movement speed during integration.

Rebuild with tools/build_garrett_sprite_polished.cjs using bundled Node.
