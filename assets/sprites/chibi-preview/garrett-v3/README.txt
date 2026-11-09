Garrett walk revision — 24 frames per direction

Open walk-right.gif and walk-left.gif for looping 4x previews on dark slate.
The transparent PNG sprite-sheet has 8 columns and 6 rows of 48x64 frames.
First 24 frames are right-facing; next 24 are mirrored left-facing.
Every frame lasts 40ms; a full two-step cycle is 960ms.

This revision replaces independent pose drawings with a periodic cutout rig.
Imagegen created the reusable head/torso, sleeves, trouser segments and shoe.
The packaging script rotates and positions those parts with two-joint leg
motion, alternating stance/swing, counter-swinging arms and gentle body bob.
The head and clothing no longer change identity between animation frames.
Each foot spends 60% of its cycle on the ground moving backward relative to
the torso, then lifts 6 pixels and swings forward. Shoe roll pivots around
the heel or toe instead of pushing the sole down through the ground.

Suggested integration speed is about 24.31 logical pixels/second, matching
the stance translation. Scale speed with display scale; change playback
speed with movement speed. Stop on an idle frame rather than playing this
cycle while motion is blocked. Existing v2 idle assets remain available.

Validation: encoder reports 24 frames and 960ms per direction. Rig checks
verify reachable leg targets, constant stance velocity, swing foot lift and
periodic positions. The wraparound foot displacement is no larger than
ordinary consecutive-frame displacement. Enlarged frame sheet inspected.
checks.json contains the measured results. These checks are not a claim
that movement/collision integration has been tested; it is not implemented.

Left direction mirrors costume asymmetries. Cutout joints and pixel rotation
can still be refined after reviewing the new motion at the intended scale.
Original v1/v2 previews are preserved. No game code or saves are changed.
Rebuild with tools/build_garrett_walk_v3.cjs using the bundled Node runtime.
