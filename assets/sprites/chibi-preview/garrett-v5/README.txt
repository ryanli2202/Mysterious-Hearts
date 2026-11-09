Garrett fuller-arm revision

Open walk-right.gif and walk-left.gif for the revised walk previews.
Upper-arm width increases from 3.5 to 4.5 logical pixels; forearm/cuff/hand
width increases from 3.2 to 4.2. Both changes are about 30 percent.
The slimmer v4 torso, shoulder positions, head, legs and 24-frame timing
remain unchanged. No new image generation: existing parts are reused by
the animation rig. Previous versions remain available for comparison.

Rebuild: tools/build_garrett_walk_v3.cjs --fuller-arms with bundled Node.
Sources: v3 parts-source.png and v4 body-source.png. The latter is copied
here for provenance. Transparent 48x64 PNG frames and sprite-sheet.png,
timing manifest and check results are included. No map or save changes.

Checks passed: 24 frames per direction, 960ms loops, periodic rig state,
stance translation, lifted swing feet and reachable leg targets.
The full contact sheet was visually inspected. Earlier idle artwork is
still a separate preview and has not been matched to these proportions.
