Winterfield Park — first playable side-scrolling area

Access: travel to Riverside park, then use the main game's In person screen
and choose Enter park. Entry is also available in the main location controls.
The phone map provides travel only; it does not host park exploration.
Move with Left/Right, A/D, or hold the on-screen arrows. Press E or the
context button at landmarks. West/east gates leave the area; Back and Esc
also return to Maps. Rest at the garden bench; movement resumes walking.
Back, Esc and gates return to the main location overview, not the phone.
The pond and old oak show local descriptions. No jumping is needed: this
is a continuous pedestrian trail with solid end boundaries.

Seven independently rendered pixel-art layers:
sky (fixed), distant hills/city (.16), woodland (.35), pond/shrubs (.7),
near trees (.9), playable path (1), foreground grass (1.12).
layers.json records asset order and scroll factors. The walkable world is
1600 logical pixels wide, with a 384x320 camera and ground baseline y=268.
All scenery uses a fixed dusk palette, independent of the story clock.
The polished scenery combines imagegen-authored oak/maple/willow trees,
gazebo, benches, lamps, flowers and woodland with code-native flagstones,
moss, fallen leaves, pond reflections and grass. Source atlases and prompts
are under source/. The original prototype planes are under prototype/.
Re-export with tools/build_park_assets.py (delegates to build_park_polish.cjs
when source artwork exists); rebuilding uses local assets without AI calls.
Winterfield Commons has separate illustrated art at
assets/ui/locations/public_park.png; the original Riverside park illustration
at assets/ui/locations/park.png is not replaced by these side-scroller planes.

Garrett's v5 sprite is the temporary visual test avatar for every player;
this does not change player identity, relationships or the actual cast.
The 24-frame walk is matched to movement speed. Matching static idle poses
are exported by tools/build_garrett_walk_v3.cjs --fuller-arms.

Travel uses the existing game rules and saves as before. Walking position,
camera and bench rest are temporary and reset on re-entry; there is no save
migration. Exploration does not advance story time or award items/rewards.
This first area has no NPC conversation encounters, jumping or combat.
Main-screen controls support resizing, focus-loss stopping, missing-art
errors and timer cleanup when leaving, starting a conversation or travelling.
Opening the phone does not relocate the park UI; it remains in the main game.

Checks: tests/test_park_scene.py, tests/park_smoke.py and existing map/dark
phone smoke checks. Rendered screens are under tests/screenshots/park-*.
