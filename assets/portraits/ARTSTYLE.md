# Mysterious Hearts portrait art direction — MH-013

Effective for future project-authored transparent portraits from 2026-11-10. Supersedes the former anime/hip-up specification. Eight pilot PNGs are now installed in [Batch 1](../../roadmap/artwork-batch-01/README.md); remaining portraits await production. [Production plan](../../roadmap/PORTRAIT_ARTWORK_UPDATE_PLAN.md) · [Complete baseline audit](../../roadmap/artwork-portrait-audit/PORTRAIT_AUDIT.md).

## Firm target

**Semi-realistic illustrated manhwa; one recognisable character; complete head through mid-thigh; genuine transparent background.** Primary rendering references: `ivan-selection.png` and `charles-selection-v2.png`. The latter is the active Charles scene image; unversioned Charles is an unchanged supplied source image, not a transparent style master.

Treat style, identity, outfit/context and composition as separate references. Never copy Ivan's or Charles's face, complexion, age, masculinity, hair, clothes or physique onto another person. Women, older people, different complexions, smaller bodies, elves and robots retain their own features within the same drawing language.

## Face and anatomy

- Construct brow ridge, eyelids, nose bridge/tip, cheeks, lips, jaw and chin. Use the anchors' dimensional nose/lip construction and restrained eye scale. Avoid tiny nose marks, oversized irises, needle chins and graphic tooth bars.
- Preserve individual proportions, age cues, skin tone, hair texture and expression. A warm smile need not become a stern idol pose. Keep Minsu's softer contours, April's petite build, Emily's delicate face and older residents' wrinkles and broader forms.
- Use plausible neck, shoulders, ribcage, pelvis, elbows and hands. Retain canonical athletic or exceptional muscular builds; describe volume through planes rather than repeated hard abdominal grooves. Do not arbitrarily slim or enlarge people.
- Preserve tattoos and laterality, scars, moles, glasses and jewellery. Clothes occlude tattoos naturally. Historical variants match their age and period; adult art is not automatic historical authority.

## Line, colour and light

- Clean tapered contours with selective weight. Facial detail is lighter than the silhouette; wrinkles and muscles do not all receive heavy black outlines.
- Combine designed shadow shapes with soft transitions where surfaces turn. Skin has volume without waxy photorealism. Charles's stronger garment shadows and Ivan's softer facial modelling can coexist.
- Hair has directional locks, restrained highlights and a few edge strands. Preserve curls, braids, locs and coarse textures; do not standardise everyone to fine waved hair.
- When reducing over-rendered skin or fabric, preserve detailed hair strands, layered locks and controlled highlights. Emily's refinement retains fine blonde hair detail; simplifying her skin and clothes is not a direction to flatten her hair into broad empty shapes.
- Use material-specific reflections: soft cloth, restrained satin/leather sheen, small metal accents. Dark outfits remain legible on slate without white outlines or glowing edges.
- One coherent soft key light. No extreme coloured rim light in civilian art. Combat lighting stays local and cannot erase faces, hands, costume or silhouette.

## Mandatory three-quarter-body composition

“3/4 body” means **head to mid-thigh**, with pelvis and useful length of both thighs visible below the crotch. It does not mean a three-quarter camera angle. Frontal or modestly turned poses are allowed.

Use a 2:3 master, normally 1024x1536 or higher at that ratio. Full hairstyle inside the frame, roughly 3–5% headroom, side clearance for hands/sleeves/hair/props. Aim for a figure occupying about 88–94% of canvas height; anatomy and mid-thigh coverage take priority over percentages. Do not shrink an old half-body into more empty space, stretch the torso, or attach trouser pixels beneath a waist crop without constructing pelvis and legs.

Both shoulders and arms stay intact. Visible hands and required objects fit completely; naturally pocketed hands are acceptable. Finish the thigh crop cleanly with a small transparent margin. Match face scale, eye line and body landmarks across one person's wardrobe. Maintain canonical relative stature through rendering; petite adults must not become childlike.

For skirts and dresses, do not terminate the cutout at a complete floating hem with no legs beneath it. Show a short visible section of anatomically connected thighs below the hem, ending at true mid-thigh. Keep knees, kneecaps and knee creases out of frame. Do not extend the portrait toward the knees to show the legs; Emily's Batch 1 follow-up corrects that overlong framing.

Ivan and Charles are rendering anchors, not automatic framing passes. Extend their composition as needed. Combat poses follow the same coverage contract; effects can require side space but cannot turn the person back into a bust.

## Context locks

- Civilian/formal/work/home/sleep/beach/gym variants retain one face and body with their own clothes, colours and ordinary expression.
- Historical characters retain period age, tattoos, clothing and props. School scenes must not gain adult sexualisation or present-day details.
- Syndicate uniforms keep opaque masks, hoods, symbols and concealed identities. Civilian and operational appearances remain distinct.
- Guards retain MH-010/MH-011 clothing, insignia, weapons and robotics. Rendering cleanup does not authorise faction/equipment redesign.
- Combat retains source-backed powers, effect colours, gear and identity. Translucent energy frames readable faces/hands. Civilian portraits do not gain auras.
- Player-owned custom portraits and historical original references are not overwritten by this policy.

## File and alpha delivery

Deliver standalone RGBA PNGs to verified existing runtime paths only after acceptance. Stage work outside `assets/portraits` so candidates cannot enter wardrobe discovery. Retain originals/hashes for rollback. Preserve historical prompt manifests and create a new MH-013 manifest.

Clear transparency surrounds the body and passes through open gaps. No background, checkerboard, floor, rectangle of haze, lettering, signature or watermark. Antialiasing belongs at the silhouette; deliberate powers can use graded alpha. Near-opaque pixels of 254 rather than 255 are not alone defects.

Inspect on slate, a middle-value colour and a light diagnostic background, then over location art. Light QA canvases are offline review, not phone UI. Inspect curls, glasses, fingers, jewellery, lace and effects at 100% and real game sizes. Remove signature-like corner marks from new deliverables; preserve immutable originals.

## Reusable production brief

> Create one transparent character portrait for Mysterious Hearts. Reference 1 defines [identity/age/body/markings]. References 2 and 3 are Ivan and Charles for SEMI-REALISTIC ILLUSTRATED MANHWA RENDERING ONLY. Reference 4, if present, defines [outfit/context]. Preserve [specific identity locks]. Draw [character/age/context] in [outfit] with [pose/expression]. Construct a dimensional face with natural eye scale, readable nose and lip planes, selective tapered contours and controlled soft-plus-shaped shading. Preserve this person's own face, body and skin tone. Show the full hairstyle, both shoulders, complete arms and visible hands, pelvis and both legs to MID-THIGH. This means body coverage, not a three-quarter camera angle. Vertical 2:3 canvas, safe margins. [Combat only: source-backed effects subordinate to figure.] Genuine RGBA transparency around the silhouette and through gaps, containing only the character and permitted effects.

> Reject: bust/waist/hip-only crop; oversized anime eyes; shorthand nose; needle chin; identical idol faces; photo/3D rendering; stretched anatomy; clipped head/fingers/weapons; backdrop/checkerboard/haze; signature/text; unauthorised costume, power, age or identity changes.

## Acceptance

Identity, style, mid-thigh coverage, anatomy, transparency, context and in-game presentation must each pass. An attractive face cannot excuse the wrong person or crop. Accept a character master before variants; compare every variant against that master and both anchors. Record actual findings, fixes and evidence rather than treating successful generation as production acceptance.
