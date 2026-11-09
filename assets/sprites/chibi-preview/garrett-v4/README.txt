Garrett proportions correction

walk-right.gif and walk-left.gif show the corrected proportions at 4x.
The transparent sprite-sheet and individual frames retain the 48x64 format,
24 frames per direction, 40ms frame duration and 960ms loop.

Imagegen edited the head/torso cutout to remove the baked-in sleeve and
narrow the chest and waist. The rig retains the head scale independently,
fits the torso to a slimmer side-profile width, moves shoulders inward,
and reduces upper-arm/forearm thickness. Hip position, leg trajectories,
foot lift, cycle timing and left/right mirroring are preserved from v3.

Rebuild: tools/build_garrett_walk_v3.cjs --slim with bundled Node.
Uses this folder's body-source.png and the preserved v3 parts-source.png.
The previous previews remain available; no map integration or save changes.
The old idle assets have not been restyled to this new body yet.

Checks: both GIFs contain 24 frames totaling 960ms. Rig continuity, stance
translation, swing lift and leg reach checks pass. Full contact sheet was
visually inspected. This remains a cutout-style art preview for review.
