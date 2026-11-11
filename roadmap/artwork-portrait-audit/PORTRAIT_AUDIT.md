# MH-013 — Individual transparent portrait audit

**Reviewed:** 2026-11-10, Australia/Brisbane. **State:** baseline planning review; no replacement PNGs installed. [Production plan](../PORTRAIT_ARTWORK_UPDATE_PLAN.md) · [Mandatory art direction](../../assets/portraits/ARTSTYLE.md) · [Metadata and source hashes](inventory.json) · [Verification](VERIFICATION.md).

## What was actually examined

All 300 PNGs under `assets/portraits`, including its 24 combat and 19 guard files, plus six related transparent profile/appearance references: **306 reviewed files**. There are 295 alpha-bearing portrait-directory files and five opaque source/contact/preview files. Review sheets show the complete source canvas on dark slate, retaining original margins and clipping. Every file appears in the individual register below, with its own observation, required change and disposition. The inventory records dimensions, source mode, alpha bounds/fractions and hashes.

All 26 sheets were visually examined. Ivan's selection and Charles's active v2 were also opened individually and compared over slate and neutral grey; twelve face crops were compared. These reviews support style, composition and visible identity findings. They do not certify every pixel, finger, tattoo line, insignia or alpha edge at production resolution. Those checks and actual game renders remain pending for replacement work. A visible issue is an art assessment, not a failing automated test.

No replacements were generated. Sheets and comparison boards are inspection composites, not new character art. `build_review.py` builds baseline sheets/metadata; `compile_audit.py` checks one-to-one note coverage and renders the individual register from `review_notes.psv`. IDs A001–A306 refer to this fixed baseline, not roadmap IDs or release versions.

## Findings and disposition

| Action | Meaning | Files |
| --- | --- | ---: |
| R — Restyle and reframe | Substantial face/rendering and body-composition work. Keep identity, outfit and useful existing detail. | 210 |
| P — Polish and standardise | Retain overall design/pose; target facial/material planes, hands and exact framing. Not an automatic pass. | 50 |
| F — Preserve rendering, reframe | Closest to target rendering; extend lower anatomy, standardise margins and complete technical QA. | 25 |
| H — Historical variant | Separate period/age/marking review, then style and body update. | 7 |
| E — Reference/archive/derivative | Explicitly reviewed; preserve source/scenic function or reconcile derivative use. No blind overwrite. | 14 |

This gives **292 portrait-file production candidates**, including duplicate active paths, plus 14 reference/archive dispositions. The 14 comprise five opaque files, three older versioned portrait files and six external transparent references/derivatives. Versioned files must have their consumers checked before they are considered inactive; classification does not authorise deletion. If a legacy version is still reachable as scene/wardrobe art, promote that path into production scope or point the consumer to its accepted replacement, preserving a separate archived original. Update actual counts accordingly. Shared byte content can reduce unique image work but cannot remove path/consumer checks.

Most current images fail the new coverage requirement even where their rendering is strong. Adding transparent space, upscaling, changing the canvas ratio or drawing only trousers under an old crop will not fix composition. Reconstruct the figure through pelvis and mid-thigh. Some guards and Yuriko variants already approach that coverage and need less reconstruction.

## Why Ivan and Charles work as references

**Ivan — A157.** The face has a developed nose bridge/tip, visible upper and lower lip planes, restrained eyelid shape, subtle skin variation and a believable neck/shoulder connection. Hair is grouped into directional locks with controlled highlights. Clothing has selective hard shadows and readable lapel construction. These traits supply a clear illustrated style target. His actual source is 1122x1402, starts very close to the hair and ends near the hips: it is not a final composition template. Preserve rendering while constructing more lower body and headroom.

**Charles — A042.** The active 1024x1536 v2 has deeper nose/lip/cheek modelling, amber eyes, thick brows, layered curtain hair and a more grounded jaw. The black jacket has clear material planes; silver chain and hoops stay legible. It already reaches farther down the upper thighs than many sprites, but needs the explicit mid-thigh endpoint and margin review. A043 is the original opaque landscape source with printed information; it must remain unchanged. A301 is byte-identical to A042, so a future derivative decision must preserve that relationship deliberately.

**What is not being copied.** Neither man's facial anatomy, hair, colouring, age, clothing, expression or male body is a template for the cast. The goal is consistent construction and rendering while preserving character differences. Retain clean manhwa linework; avoid switching the game into photographic realism, 3D figures or uniformly soft airbrushed faces. Charles's bold jacket shadows also show that hard shading itself is not the problem: flat skin, shorthand facial construction and inconsistent detail distribution are the issue.

**Known reference conflict.** Ivan's written appearance specifies dark eyes and ash-brown hair; the inspected PNG renders the eyes pale grey/green and the hair quite light. An older Charles generation prompt calls Ivan's hair blond. Use the current written identity for the eye/hair colour brief and the PNG for rendering structure; do not propagate that old prompt's colour description as new canon. Preserve the recognisable hairstyle, face and overall colouring while resolving this in the pilot. Other unspecified freckles/accessories must not become universal cast traits.

## Character-family analysis

These directions apply to every variant in the register. The per-file row adds its own visible outfit, pose, crop or context issue. All R/P/F/H candidates inherit the same mandatory head-to-mid-thigh target and seven acceptance gates in the art guide.

| Character/family | Retain | Detailed change direction |
| --- | --- | --- |
| Amy | Ginger waved bob, hazel eyes, slim adult build, thoughtful warmth and warm clothing palette. | Clothing is often much more dimensional than her face. Develop nose bridge/tip, cheek turn and lips; moderate eye/chin stylisation without making her stern. Keep clasped hands but construct separate fingers and wrists. Extend pelvis and legs consistently through every dress, shorts and trouser variant. |
| April | Petite 150 cm adult, brown bob/eyes, fine features and composed crossed-arm posture. | Preserve a small adult body rather than enlarging the head. Model cheeks, nose and lips while keeping delicate features. Resolve forearm/hand overlap and garment tension at elbows; the repeated crossed arms must not conceal incomplete anatomy. Continue garments through thighs. |
| Emily | Petite 154 cm adult, long blonde hair/fringe, blue eyes, round glasses and gentle manner. | The large eyes/tiny nose/pointed chin combination is markedly doll-like beside Charles. Build adult facial planes and eyelids behind correctly seated glasses; retain her delicacy and gentle smile. Keep long hair separated from sleeves/hands and fine ribbons/lace readable. Historical school art keeps its own age and miniature prop. |
| Garrett | Tall 188 cm broad athletic adult, gold hair/eyes, confident expression, gold styling and reference tattoo map. | Reduce the graphic wedge chin/eye treatment; give nose, mouth and cheeks volume. Preserve broad shoulders and athletic muscle without etching every abdomen segment. Tattoos must follow anatomy and clothing occlusion, including corrected arm maps. School variant stays younger and untattooed where shown. |
| Rei | Tall 184 cm lean adult, layered dark hair, restrained expression and dense neck/chest/arm ink. | Preserve individuality without sharpening everything to a point. Add nose/lip/cheek depth, retain lean rather than bulky anatomy, and keep fine tattoo density readable at game size. Garments already have useful texture; further texture is secondary to face and crop. Earlier school art remains free of adult tattoos. |
| Minsu | 177 cm lean athletic adult, softer contours, dark parted hair and open smile. | Current v2-style art relies on hard facial wedges and a broad white tooth shape; gym variants exaggerate muscle segmentation. Keep warmth but construct lips/teeth/cheeks. Archived v1 offers useful softer rendering, not permission to change likeness wholesale. Rebuild one approved master before all medical, study, street and sport variants. |
| Sophie | 170 cm runner, brown ponytail, green eyes, lively confidence and athletic posture. | Moderate large eye/small nose/chin shorthand; maintain a healthy adult runner's body. Align hand-on-hip anatomy and leg length across dresses, shorts and training sets. School baton/backpack art remains age-appropriate. |
| Samantha | Athletic adult build, cropped dark hair, confident expression and exact floral tattoo map. | Preserve muscle and attitude while giving eyelids/nose/lips depth. Replace engraved abdominal shadows with believable planes. Keep tattoos stable across exposed/covered outfits and ensure low hands are entirely within frame. |
| Yuriko | Petite 159 cm adult, black bob, amber clip and expressive face. | Many 2:3 outfit images already show complete hands and useful thighs. Prioritise large-eye/tiny-nose facial construction and adult proportions; do not erase cheerfulness. Bring the shorter selection/home variants into line with the longer wardrobe composition. |
| Ivan | 193 cm tall broad-shouldered lean adult, waves, angular face, restrained style. | Retain the rendering anchor; standardise framing throughout civilian wardrobe, soften occasional hard shirtless muscle facets and resolve written eye/hair colours. Masked and combat variants are separate context work, not reasons to copy civilian facial features through masks. |
| Charles | 191 cm athletic adult, black curtains, amber eyes, under-eye mark, hoops/chain in current context. | Preserve v2 rendering and identity. Extend lower body without lengthening torso. Young-adult art keeps its period-specific accessories. Preserve original opaque source and synchronise linked derivatives deliberately. |
| Fox / Gordon | Fox's weathered face, silver hair, stubble and tattoos; Gordon's adult stubble, glasses and Interpol kit. | Already useful secondary examples of more grounded adult depiction. Concentrate on complete body framing, readable tactical materials and accurate gear/hand edges. Keep their scenic close-contact images as avatars rather than making faces tiny to satisfy a scene-art crop rule. |
| Celeste / Lena / Naomi / Dev / Elliot / Rosa | Individual curls, complexion, age, glasses, body shape and styling as applicable. | Apply each register row, not a shared face template. Celeste is relatively dimensional. Lena's earlier version has useful face planes. Rosa's warmth/curves must survive smile refinement. Preserve Dev's glasses and Naomi's practical styling rather than making every character glamorous. |
| Camila / Elias / Martos / Mavis | Civilian identities, glasses/scars/piercings/tattoos, exact body scales and separate concealed uniforms. | Several civilian crops are especially short. Keep Camila upright, Elias softer-faced, Martos exceptionally broad and Mavis petite/wiry. White-robed variants require whole-body cloth/anatomy construction while every facial/identifying feature remains concealed. |
| Alyssa / Sylvanis | Pointed ears, long hair and distinctive fantasy identities. | Naturalistic facial planes do not remove fantasy anatomy. Avoid interchangeable narrow idol faces; maintain their distinct features, expressions and builds. Long hair and effects must not hide incomplete body coverage. |
| Daniel / Neo / Tyler / Valentina / Thirteen / Takeo / Keisuke | Distinct builds, hair, complexion, facial hair, wraps, tattoos and canonical unusual size. | Reconcile bold cel treatment with dimensional facial planes. Preserve Takeo's exceptional bulk and Thirteen's severe build, Neo's ink, Tyler's locs/moustache and Valentina's silver waves. Avoid treating every sharp feature as a defect; correct construction and rendering rather than erase identity. |
| Town residents / street recruits / faction staff | Wide age and complexion range, curls/braids/locs, workwear, body diversity and individual expressions. | Many are true chest/waist busts. These need new arms, hands, pelvis and legs, not outpainting a tiny lower strip. Preserve older people as older; turn heavy wrinkle lines into subtle planes, not youthful smoothing. Rebuild smiles naturally without removing warmth or making everyone fashion-model thin. |
| Guards / robots | Recent MH-010/MH-011 designs, masked privacy, role equipment and mechanical anatomy. | Most already have longer standing coverage. Refine material/skin transitions and exact crop rather than undo recent designs. Robots need joint/material logic, not human facial corrections. Human guard faces remain distinct; opaque masks stay opaque. |
| Combat | Same character identity, existing powers/colours/weapons, intentional fighting gestures. | Rebuild complete mid-thigh stances. Check foreshortened fists, finger joints and effect overlap individually. Equal canvas size does not give equal visible body scale when large auras dominate bounds. Keep aura lighting subordinate to face/hands; do not add effects to civilians. |

## Alpha, duplicates and technical findings

Having alpha minimum zero is only a basic format observation. Many images have predominantly near-opaque alpha over the figure; the reported partial-alpha fraction is not proof of damaged transparency. Review isolated low-opacity residue, matte contamination and fine cutouts at full resolution during production. Small dark corner marks are visible on several home/sleep sources; the register flags them for inspection and removal in new deliverables, without claiming every mark is a signature or erasing historical source evidence.

Source SHA-256 checks establish these byte-identical groups:

- Charles scene v2 and `assets/profiles/charles-v2.png`.
- Crow selection, Crow Syndicate and `assets/profiles/crow.png`.
- Garrett home and Grove arm-tattoo reference.
- Garrett sleep and Grove appearance reference.
- Rei sleep and both Grove appearance/tattoo references.

These are separate files and paths, not necessarily filesystem links. Replacing one does not automatically update the others. Archive original identity/tattoo references; create versioned updated masters rather than changing historical evidence invisibly. Reconcile any active derivative deliberately. The three older versioned Lena/Minsu files were reviewed individually; they are not declared byte duplicates.

The source collection uses many aspect ratios. A 2:3 delivery standard requires anatomical recomposition and renderer review. `game.py` currently uses a hard-coded older reference ratio for relative height of four leads; `combat_portraits.py` fits the entire image, including effect extents. Both behaviours must be checked against new sources before release. No runtime change is made by this audit.

## Individual file register

<!-- GENERATED REGISTER: compile_audit.py replaces content below this marker. -->

### Review sheet 01

[Open labelled complete-canvas sheet](review-01.jpg).

#### A001 — ada-mensah-selection.png

[Original file](../../assets/portraits/ada-mensah-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Ada already has a long standing silhouette, braided updo, glasses and layered charcoal knitwear; face and sleeves use hard graphic shadows.

**Required:** Keep braids, mature face and tailoring; model cheek/nose planes more softly and standardise the thigh endpoint and hand clearance.

#### A002 — alyssa-selection.png

[Original file](../../assets/portraits/alyssa-selection.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Alyssa has pointed ears, long dark waves and lavender cardigan; large eyes and tapering chin dominate a short thigh/hip composition.

**Required:** Retain elven ears and slim build; give nose, lips and cheeks adult dimensional structure, lengthen lower-body coverage and clarify overlapping wrists.

#### A003 — amy-beach-daisy.png

[Original file](../../assets/portraits/amy-beach-daisy.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Amy's daisy bikini has readable pattern and fine hair detail, but the face is simplified and the crop ends high on the legs.

**Required:** Apply Amy master corrections; retain blue floral fabric, reconstruct pelvis-to-mid-thigh anatomy and preserve the clasped-hand pose without merging fingers.

#### A004 — amy-beach-sage.png

[Original file](../../assets/portraits/amy-beach-sage.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Amy's sage swim set has soft fabric shading, repeated large-eyed face and a high leg crop.

**Required:** Retain sage colour and modest athletic cut; use the approved adult face and extend both thighs with natural hip volume.

#### A005 — amy-beach-terracotta.png

[Original file](../../assets/portraits/amy-beach-terracotta.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Terracotta swimwear and ginger bob are consistent; very smooth face and upper-leg cutoff remain.

**Required:** Retain warm colours and strap construction; model facial planes and extend thighs without exaggerating waist or breast shape.

#### A006 — amy-floral-dress.png

[Original file](../../assets/portraits/amy-floral-dress.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Blue floral dress has fine print and soft folds; head feels more stylised than the garment and skirt ends soon below waist.

**Required:** Keep print, flutter sleeves and waist tie; improve face construction and continue skirt over a believable pelvis to mid-thigh.

#### A007 — amy-formal-plum.png

[Original file](../../assets/portraits/amy-formal-plum.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Plum satin is richly rendered; Amy's face and folded hands repeat the short wardrobe master.

**Required:** Keep satin drape, soften stylised eyes/chin, review finger overlap and extend the skirt composition.

#### A008 — amy-formal-tweed.png

[Original file](../../assets/portraits/amy-formal-tweed.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Tweed tailoring and bow blouse are detailed; jacket hem and clasped hands crowd the lower crop.

**Required:** Preserve tweed, bow and warm palette; use corrected face/body master and show the garment continuing over both thighs.

#### A009 — amy-gym-training.png

[Original file](../../assets/portraits/amy-gym-training.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Plum training top and dark shorts read clearly; legs are cut immediately below the shorts.

**Required:** Keep practical outfit and slim build; extend thighs and relax the schematic facial planes and hand overlap.

#### A010 — amy-gym-yoga.png

[Original file](../../assets/portraits/amy-gym-yoga.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Sage yoga set has useful material shading; large eyes and hip-level framing persist.

**Required:** Retain sage separates and waistband; adopt adult facial construction and show leg anatomy beyond the hip curve.

#### A011 — amy-library-knit.png

[Original file](../../assets/portraits/amy-library-knit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Cable-knit vest and ivory shirt offer clear layering; face remains lightly modelled and trousers barely extend below waist.

**Required:** Keep knit pattern and cuff construction; apply Amy master and extend trouser thighs with credible creases.

#### A012 — amy-selection.png

[Original file](../../assets/portraits/amy-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Amy's signature ginger bob and rust cardigan are distinct; small nose, pointed chin and short trouser crop create a stylised read.

**Required:** Build Amy's master first: retain hazel eyes, soft bob and thoughtful smile; model nose/lips/cheeks and reconstruct head-to-mid-thigh coverage.

### Review sheet 02

[Open labelled complete-canvas sheet](review-02.jpg).

#### A013 — amy-sleep.png

[Original file](../../assets/portraits/amy-sleep.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** White lace sleepwear repeats Amy's stylised face and upper-leg crop; a small dark corner mark is visible.

**Required:** Preserve adult identity and existing sleepwear coverage; extend anatomy, inspect/remove non-character corner marks and keep lace alpha clean.

#### A014 — amy-studio-overalls.png

[Original file](../../assets/portraits/amy-studio-overalls.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Paint-marked overalls and denim shirt are convincing; hands and pelvis cluster at the lower boundary.

**Required:** Keep paint marks and straps; improve facial volume and extend overall legs with clear wrist/finger separation.

#### A015 — amy-summer-linen.png

[Original file](../../assets/portraits/amy-summer-linen.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Sage summer shirt and light shorts have coherent cloth detail; composition ends just below shorts.

**Required:** Keep fabric and belt, use Amy master and show both thighs to the common endpoint without lengthening torso.

#### A016 — amy-weekend-denim.png

[Original file](../../assets/portraits/amy-weekend-denim.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Denim jacket, striped tee and olive trousers are clear; face remains the same stylised short master.

**Required:** Keep stripes, denim seams and warm hair; correct face and extend trousers while keeping shoulder width stable.

#### A017 — amy-winter-coat.png

[Original file](../../assets/portraits/amy-winter-coat.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Camel coat and green scarf give useful material contrast; lower coat and body are truncated early.

**Required:** Keep scarf volume and coat construction; apply face correction and extend coat/trousers to consistent mid-thigh framing.

#### A018 — anton-bellamy-selection.png

[Original file](../../assets/portraits/anton-bellamy-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Anton has curly brown hair, beard and black utility jacket; full hands are present but shading is sharply graphic.

**Required:** Preserve rugged face and curls; soften skin transitions, refine beard volume and give the lower legs sufficient thigh coverage.

#### A019 — april-beach-bikini.png

[Original file](../../assets/portraits/april-beach-bikini.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** April's teal bikini retains crossed arms and bob; tiny nose and smooth narrow chin read more stylised than anchors.

**Required:** Use April's petite adult master; retain teal set, natural crossed-arm anatomy and extend both thighs.

#### A020 — april-beach-swimsuit.png

[Original file](../../assets/portraits/april-beach-swimsuit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Navy one-piece shares April's face and crossed arms; high lower crop conceals leg length.

**Required:** Keep swimwear coverage and composed expression; add dimensional face and visible pelvis-to-mid-thigh form.

#### A021 — april-blue-oxford.png

[Original file](../../assets/portraits/april-blue-oxford.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Blue Oxford sleeves and belt are detailed; lower crop stops near the hip and folded forearms dominate.

**Required:** Preserve rolled cuffs and navy trousers; refine face and hand junctions, then extend trouser anatomy.

#### A022 — april-burgundy-dress.png

[Original file](../../assets/portraits/april-burgundy-dress.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy wrap dress has convincing drape but short skirt coverage and the repeated simplified face.

**Required:** Retain wrap direction and waist knot; use April master and extend skirt to a clear mid-thigh endpoint.

#### A023 — april-camel-trench.png

[Original file](../../assets/portraits/april-camel-trench.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Camel trench and teal top preserve identity; fingers and lower jacket sit close to crop.

**Required:** Keep lapels, buttons and outfit layering; model face and continue coat/trousers with complete arms.

#### A024 — april-cream-cable-knit.png

[Original file](../../assets/portraits/april-cream-cable-knit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Cream cable knit is detailed against a very smooth face; jeans are only briefly visible.

**Required:** Retain knit scale and dark jeans; add subtle cheek/nose volume and adequate thigh coverage.

### Review sheet 03

[Open labelled complete-canvas sheet](review-03.jpg).

#### A025 — april-denim-weekend.png

[Original file](../../assets/portraits/april-denim-weekend.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Denim jacket, white tee and olive trousers are cohesive; face and hip crop retain the older style.

**Required:** Apply April master without changing petite build; retain seams and crossed arms, extend trouser legs.

#### A026 — april-formal-emerald.png

[Original file](../../assets/portraits/april-formal-emerald.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Emerald satin dress has rich reflections; its face is flatter and lower drape ends high.

**Required:** Retain elegant drape and restrained smile; improve facial planes and continue skirt over pelvis/thighs.

#### A027 — april-formal-ivory-suit.png

[Original file](../../assets/portraits/april-formal-ivory-suit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Ivory suit and satin blouse are clear; folded arms and high crop compress the figure.

**Required:** Retain adult proportions, pale suit and blouse; give face depth and show jacket hem and upper legs fully.

#### A028 — april-gym-plum.png

[Original file](../../assets/portraits/april-gym-plum.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Plum sports set shows abdomen and crossed arms; simplified face contrasts with detailed body shading.

**Required:** Retain slim adult body and sports outfit; refine eyes/nose/lips and extend to mid-thigh without increasing muscularity.

#### A029 — april-plaid-blazer.png

[Original file](../../assets/portraits/april-plaid-blazer.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Plaid blazer and pale knit have useful texture; crop is hip-high.

**Required:** Keep plaid aligned over seams, preserve bob and fine features; build deeper face planes and extend trousers.

#### A030 — april-rose-cardigan.png

[Original file](../../assets/portraits/april-rose-cardigan.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Rose cardigan and pleated lower garment are distinctive; face and short lower crop are unchanged.

**Required:** Keep buttons and pleats; use corrected April master, resolve forearm contact and continue lower garment to mid-thigh.

#### A031 — april-sage-knit.png

[Original file](../../assets/portraits/april-sage-knit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Sage knit and light trousers read softly; facial modelling is sparse and thigh coverage short.

**Required:** Preserve sage/light palette, petite stature and composed gaze; refine facial depth and trouser length in frame.

#### A032 — april-selection.png

[Original file](../../assets/portraits/april-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** April's navy cardigan, blouse and crossed arms identify her well; eyes, tiny nose and pointed chin remain stylised.

**Required:** Create the petite adult master with brown eyes and fine features; keep warmth/composure, build face volume and complete lower-body framing.

#### A033 — april-sleep.png

[Original file](../../assets/portraits/april-sleep.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Black lace sleepwear retains crossed arms and a high thigh crop; small corner mark present.

**Required:** Preserve adult identity and outfit; extend legs, inspect/remove non-character mark and preserve transparent lace gaps without pale fringe.

#### A034 — arthur-finch-selection.png

[Original file](../../assets/portraits/arthur-finch-selection.png) · 1261 × 1247 · contains transparency · **Restyle + reframe**.

**Observed:** Arthur is a waist/chest crop with silver hair, glasses, age lines and sweater vest; wrinkles are outlined heavily.

**Required:** Preserve age and gentle expression, construct torso/arms/pelvis through mid-thigh and soften line-heavy wrinkles into skin planes.

#### A035 — beatrice-cole-selection.png

[Original file](../../assets/portraits/beatrice-cole-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Beatrice has grey curls, warm complexion and burgundy cardigan; the bust crop and flat skin shading differ strongly from anchors.

**Required:** Retain age, curls and pearl-like earrings; construct complete arms/lower body and add nuanced cheek, nose and neck modelling.

#### A036 — ben-okafor-selection.png

[Original file](../../assets/portraits/ben-okafor-selection.png) · 1217 × 1293 · contains transparency · **Restyle + reframe**.

**Observed:** Ben's broad shoulders, close curls and beard read well; bright tooth bar and chest crop create a cartoon-like presentation.

**Required:** Retain deep complexion and joyful grin; model lips/teeth naturally and build hands, pelvis and thighs under mechanic clothes.

### Review sheet 04

[Open labelled complete-canvas sheet](review-04.jpg).

#### A037 — callum-webb-selection.png

[Original file](../../assets/portraits/callum-webb-selection.png) · 1190 × 1322 · contains transparency · **Restyle + reframe**.

**Observed:** Callum's short brown hair, stubble and grey work jacket are clear; portrait ends across the torso.

**Required:** Preserve sturdy adult features, give face/neck volume and build complete jacket, arms, hands and trouser thighs.

#### A038 — camila-selection.png

[Original file](../../assets/portraits/camila-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Camila's glasses, ponytail and burgundy blouse identify her; angular cel blocks and waist cutoff flatten the body.

**Required:** Retain warm tan skin and business styling; refine facial depth through glasses, construct complete hands and mid-thigh tailoring.

#### A039 — camila-syndicate.png

[Original file](../../assets/portraits/camila-syndicate.png) · 1183 × 1330 · contains transparency · **Restyle + reframe**.

**Observed:** Camila's Diamonds uniform has a sealed symbolic mask and layered white cape, but ends around waist.

**Required:** Keep identity fully concealed and diamond symbol exact; extend robe, belt and arms to mid-thigh with softer cloth planes.

#### A040 — celeste-selection.png

[Original file](../../assets/portraits/celeste-selection.png) · 1145 × 1374 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Celeste has convincing curls, warmer dimensional skin and knit volume; figure still ends high on the legs.

**Required:** Retain complexion, curly updo and purple knit; harmonise face shading to anchors and extend lower garment with complete relaxed hands.

#### A041 — celia-brooks-selection.png

[Original file](../../assets/portraits/celia-brooks-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Celia's curly updo and green cardigan are distinct; half-body crop and flat cheek shadows need work.

**Required:** Retain mature face and orange blouse; give facial planes depth and construct full arms, hands and lower body.

#### A042 — charles-selection-v2.png

[Original file](../../assets/portraits/charles-selection-v2.png) · 1024 × 1536 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Active Charles v2 has dimensional nose/lips, defined eyelids, coherent jacket and visible upper thighs; hair nearly meets the source top.

**Required:** Use as rendering anchor, preserve amber eyes/mark/hoops/chain; add safe headroom and extend to explicit mid-thigh without changing identity.

#### A043 — charles-selection.png

[Original file](../../assets/portraits/charles-selection.png) · 1920 × 1080 · fully opaque · **Reference / archive / derivative**.

**Observed:** Opaque landscape Charles source includes a background and printed character information.

**Required:** Preserve supplied original unchanged as identity provenance; never treat it as the transparent runtime delivery or redraw it in place.

#### A044 — charles-young-adult.png

[Original file](../../assets/portraits/charles-young-adult.png) · 1024 × 1536 · contains transparency · **Historical update**.

**Observed:** Young-adult Charles retains black jacket and recognisable face, with fewer visible accessories than v2; crop is upper-thigh.

**Required:** Preserve period-specific age/accessories; use Charles rendering, extend framing and avoid copying present-day jewellery automatically.

#### A045 — combat/alyssa.png

[Original file](../../assets/portraits/combat/alyssa.png) · 1312 × 1199 · contains transparency · **Restyle + reframe**.

**Observed:** Alyssa combat has an especially short waist crop, large foreshortened hand and purple tendrils consuming width.

**Required:** Rebuild complete fighting stance to mid-thigh from approved master; preserve ears/purple ability, check hand perspective and reduce effect dominance.

#### A046 — combat/april.png

[Original file](../../assets/portraits/combat/april.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** April combat has tactical layers and geometric violet effects; face is stylised and lower body short.

**Required:** Retain specialist gear and existing geometry; use petite adult master, extend stance and keep geometry from masking hands/face.

#### A047 — combat/camila.png

[Original file](../../assets/portraits/combat/camila.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Camila combat combines glasses, business suit, gold figures and wrist-level gestures with a waist cutoff.

**Required:** Keep glasses, suit and source-backed gold motifs; restore full stance and model face/hands with adult depth.

#### A048 — combat/charles.png

[Original file](../../assets/portraits/combat/charles.png) · 1145 × 1374 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Charles combat has dimensional features and white tiger aura but a high body cutoff; aura occupies much of the frame.

**Required:** Retain Charles identity and tiger motif, extend stance to mid-thigh and keep all hands/effects within safe bounds.

### Review sheet 05

[Open labelled complete-canvas sheet](review-05.jpg).

#### A049 — combat/crow.png

[Original file](../../assets/portraits/combat/crow.png) · 1199 × 1312 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Crow combat preserves hood, beaked mask, blade and teal geometry; lower robes end at hip.

**Required:** Maintain complete concealment, etched metal and current power/weapon; extend robe/body coverage and separate blade from robe folds.

#### A050 — combat/daniel.png

[Original file](../../assets/portraits/combat/daniel.png) · 1086 × 1448 · contains transparency · **Polish + framing**.

**Observed:** Daniel combat has blue energy, raised fists and dark hoodie; face/hood shadows are hard and thighs short.

**Required:** Keep stern brown-haired identity and blue effects; refine facial planes, construct legs and preserve clear fist silhouettes.

#### A051 — combat/elias.png

[Original file](../../assets/portraits/combat/elias.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Elias combat has blond hair, black layers and orange flames; composition is waist-high and fists crowd face.

**Required:** Retain blue eyes and warm fire identity; build full stance, soften skin planes and place flames around readable hands.

#### A052 — combat/emily.png

[Original file](../../assets/portraits/combat/emily.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Emily combat shows glasses, pinafore and pale precise effects with a strongly enlarged forward hand; skirt crop is high.

**Required:** Apply Emily master, preserve glasses and existing power symbols; correct foreshortening and extend stance/skirt to mid-thigh.

#### A053 — combat/fox.png

[Original file](../../assets/portraits/combat/fox.png) · 1145 × 1373 · contains transparency · **Polish + framing**.

**Observed:** Fox combat retains silver hair, tattoos and tactical layers with pale rings; body stops just below belt.

**Required:** Preserve weathered face and markings; extend trousers/stance and ensure rings do not hide arm tattoos or shrink the person.

#### A054 — combat/garrett.png

[Original file](../../assets/portraits/combat/garrett.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Garrett combat has golden flames and signature suit, but angular face and huge foreground fist dominate the short torso crop.

**Required:** Apply Garrett master, preserve tattoo locations/gold power; resolve hand perspective and extend pelvis/thighs with measured effects.

#### A055 — combat/gordon.png

[Original file](../../assets/portraits/combat/gordon.png) · 1145 × 1374 · contains transparency · **Polish + framing**.

**Observed:** Gordon combat uses glasses, Interpol vest, pistol and green effects; legs are truncated early.

**Required:** Retain mature face and exact gear; extend stance, check gun/trigger-hand construction and keep ability light subordinate.

#### A056 — combat/ivan.png

[Original file](../../assets/portraits/combat/ivan.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Ivan combat retains recognisable face and multiple coloured elements; high crop and wide effects reduce body coverage.

**Required:** Use Ivan master, preserve all existing element identities/colours, extend to mid-thigh and fit effects without reducing face readability.

#### A057 — combat/keisuke-hachimura.png

[Original file](../../assets/portraits/combat/keisuke-hachimura.png) · 1122 × 1402 · contains transparency · **Polish + framing**.

**Observed:** Keisuke combat keeps brown coat, stubble and golden forearm energy; jacket and stance end near hips.

**Required:** Retain mature face and coat; refine fist/forearm planes and extend trousers, avoiding new weapons or power motifs.

#### A058 — combat/martos.png

[Original file](../../assets/portraits/combat/martos.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Martos combat is broad, scarred and surrounded by red energy; foreshortened fist and high crop dominate.

**Required:** Keep exceptional breadth/scars and red effect identity; rebuild full stance and soften face modelling without slimming him.

#### A059 — combat/mavis.png

[Original file](../../assets/portraits/combat/mavis.png) · 1199 × 1312 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Mavis combat has hood, piercings, neck/hand tattoos and pale smoky coils; hands sit at a waist cutoff.

**Required:** Preserve wiry adult identity and markings; extend legs, check hand anatomy and smoke alpha without exposing uniform-hidden identity elsewhere.

#### A060 — combat/minsu.png

[Original file](../../assets/portraits/combat/minsu.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Minsu combat repeats a broad graphic grin and angular facial shadows; cyan rings cross the short body.

**Required:** Use softer-contoured adult Minsu master; keep open expression and current effect, extend stance and clarify both hands.

### Review sheet 06

[Open labelled complete-canvas sheet](review-06.jpg).

#### A061 — combat/neo.png

[Original file](../../assets/portraits/combat/neo.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Neo combat has strong tattooed arms, black tee and blue geometric energy; upper-body composition remains dominant.

**Required:** Preserve tattoos and face from scene identity, soften facial planes and construct full stance with clear forearms.

#### A062 — combat/rei.png

[Original file](../../assets/portraits/combat/rei.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Rei combat shows green lightning/wind and dense tattoos; angular face, open hands and short lower crop remain.

**Required:** Use Rei master and exact markings; preserve green power identity, check finger anatomy and extend pelvis/thighs.

#### A063 — combat/samantha.png

[Original file](../../assets/portraits/combat/samantha.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Samantha combat retains short hair, tattoos and red energy but waist-high framing compresses the stance.

**Required:** Preserve athletic adult build and tattoo map; refine face and complete mid-thigh stance with separated fists/effects.

#### A064 — combat/sylvanis.png

[Original file](../../assets/portraits/combat/sylvanis.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Sylvanis combat has long hair, ears and violet shadow tendrils; face is narrow and idealised, lower body short.

**Required:** Keep elven identity and violet shadows; give face/neck credible volume and extend stance while preserving fingers and hair silhouette.

#### A065 — combat/takeo.png

[Original file](../../assets/portraits/combat/takeo.png) · 1086 × 1448 · contains transparency · **Polish + framing**.

**Observed:** Takeo combat keeps extreme muscular scale, black clothing and red armoured energy; body crop is high.

**Required:** Retain massive canonical build and facial hair; improve plane transitions and show pelvis/thighs without enlarging fists further.

#### A066 — combat/thirteen.png

[Original file](../../assets/portraits/combat/thirteen.png) · 1129 × 1393 · contains transparency · **Restyle + reframe**.

**Observed:** Thirteen combat has severe buzzcut face, angular cel blocks and pale motion effects; short jacket/hip framing.

**Required:** Retain distinctive build and face; soften facial planes, construct lower stance and avoid inventing power or clothing details.

#### A067 — combat/tyler.png

[Original file](../../assets/portraits/combat/tyler.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Tyler combat keeps locs, moustache, wraps and golden rings; grin and skin planes are graphically simplified.

**Required:** Retain complexion/locs/wraps and enthusiasm; model mouth/cheeks, extend legs and separate rings from wrapped hands.

#### A068 — combat/valentina.png

[Original file](../../assets/portraits/combat/valentina.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Valentina combat has silver waves and cyan wind-like ribbons; large eyes and pointed chin repeat the civilian style.

**Required:** Preserve silver hair and lively expression; refine face, build complete stance and keep ribbon alpha off face/hands.

#### A069 — crow-selection.png

[Original file](../../assets/portraits/crow-selection.png) · 1199 × 1312 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Crow's mask, embroidery and layered dark cape are detailed and convincing; crop stops around waist.

**Required:** Keep all concealment and symbolic details; extend sleeves, robe and implied leg volume to mid-thigh with readable dark materials.

#### A070 — crow-syndicate.png

[Original file](../../assets/portraits/crow-syndicate.png) · 1199 × 1312 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Crow's Syndicate portrait visually repeats the short masked civilian/default composition.

**Required:** Keep the same identity and concealment; reconcile duplicate/reference use, extend consistently with Crow master and retain exact role routing.

#### A071 — daichi-kurose-selection.png

[Original file](../../assets/portraits/daichi-kurose-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Daichi has dark slick hair, burgundy shirt and navy suit with full hands; face and garment shadows are graphic.

**Required:** Keep stern features and tailoring, add facial plane transitions and ensure mid-thigh endpoint without clipping fingers.

#### A072 — dana-lin-selection.png

[Original file](../../assets/portraits/dana-lin-selection.png) · 1144 × 1375 · contains transparency · **Restyle + reframe**.

**Observed:** Dana has bob, navy suit and restrained smile; hands are near a hip-level cutoff and face is simplified.

**Required:** Preserve professional identity and fine features, model nose/lips/cheeks and continue suit/trousers to mid-thigh.

### Review sheet 07

[Open labelled complete-canvas sheet](review-07.jpg).

#### A073 — daniel-selection.png

[Original file](../../assets/portraits/daniel-selection.png) · 1086 × 1448 · contains transparency · **Polish + framing**.

**Observed:** Daniel already has a coherent long hoodie silhouette and readable face; hard shadow wedges and short thigh coverage remain.

**Required:** Keep hairstyle and quiet stern expression; soften face planes, continue cargo trousers and preserve natural pocketed hands.

#### A074 — dante-brooks-selection.png

[Original file](../../assets/portraits/dante-brooks-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Dante has twists, beard, green jacket and shoulder strap; torso ends abruptly below chest.

**Required:** Preserve deep complexion and sturdy build; construct full arms, bag connection and lower body, with dimensional face/beard.

#### A075 — darius-cole-selection.png

[Original file](../../assets/portraits/darius-cole-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Darius has grey close hair/beard and blue work jacket; long figure and complete hands are useful.

**Required:** Preserve mature age/build, soften facial/collar planes and confirm consistent mid-thigh crop rather than repainting identity.

#### A076 — dev-selection.png

[Original file](../../assets/portraits/dev-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Dev's glasses, curly hair and teal overshirt are clear; angular shadows and high hip crop remain.

**Required:** Retain glasses and gentle expression; refine nose/lips under frames and extend trousers with unchanged relaxed posture.

#### A077 — elias-selection.png

[Original file](../../assets/portraits/elias-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Elias has blond curtains, blue eyes and turtleneck; waist crop and smooth idealised face need development.

**Required:** Preserve soft angular identity and layered hair; construct whole arms/lower body and nuanced facial planes.

#### A078 — elias-syndicate.png

[Original file](../../assets/portraits/elias-syndicate.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Elias's Hearts robe has sealed mask, jewellery and layered white fabric; waist cutoff hides hands/lower form.

**Required:** Keep Hearts symbol and concealed features; continue robe and arms to mid-thigh, model cloth without adding face openings.

#### A079 — elliot-selection.png

[Original file](../../assets/portraits/elliot-selection.png) · 1086 × 1448 · contains transparency · **Polish + framing**.

**Observed:** Elliot's wavy blond hair, olive overshirt and relaxed hands read well; sharp fold shadows and high crop remain.

**Required:** Keep welcoming face and hair; refine face/cloth transitions and extend trouser anatomy to mid-thigh.

#### A080 — emi-suda-selection.png

[Original file](../../assets/portraits/emi-suda-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Emi's short bob, dark cardigan and burgundy blouse form a long figure with full hands; eyes/chin remain stylised.

**Required:** Preserve slim adult identity, soften face construction and ensure enough thigh length below the cardigan hem.

#### A081 — emily-beach-bikini.png

[Original file](../../assets/portraits/emily-beach-bikini.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Emily's blue floral bikini preserves glasses and long hair but eyes and face stay doll-like; crop is high on legs.

**Required:** Use delicate adult Emily master, retain hair/glasses and swimwear coverage, extend thighs with natural proportions.

#### A082 — emily-beach-swimsuit.png

[Original file](../../assets/portraits/emily-beach-swimsuit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Teal one-piece and long hair are coherent; tiny nose and large eyes contrast with the anchors.

**Required:** Preserve glasses and gentle identity; model face and extend lower-body coverage without adding glamour exaggeration.

#### A083 — emily-cafe.png

[Original file](../../assets/portraits/emily-cafe.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Rose cable cardigan and collared blouse are detailed, while face and lower skirt remain short/simplified.

**Required:** Keep knit, buttons and fine collar; apply Emily master and continue skirt over the pelvis through mid-thigh.

#### A084 — emily-florist.png

[Original file](../../assets/portraits/emily-florist.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Florist apron and pale shirt have distinct folds; clasped hands and long hair converge near bottom.

**Required:** Retain apron tie and work styling; refine face, separate fingers/hair and extend lower apron/legs.

### Review sheet 08

[Open labelled complete-canvas sheet](review-08.jpg).

#### A085 — emily-formal-satin.png

[Original file](../../assets/portraits/emily-formal-satin.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Navy off-shoulder satin has rich drape; Emily's face remains stylised and the skirt is cropped high.

**Required:** Keep satin and necklace where visible; apply adult master and continue skirt to standard coverage.

#### A086 — emily-formal-tailoring.png

[Original file](../../assets/portraits/emily-formal-tailoring.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Light tailoring and pink satin blouse are detailed; face and hand/pelvis composition repeat the short base.

**Required:** Preserve pale suit, glasses and gentle posture; add facial depth and extend trouser thighs with complete hands.

#### A087 — emily-garden.png

[Original file](../../assets/portraits/emily-garden.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Green floral dress and sheer sleeves are clear; face is simplified and skirt stops near upper hips.

**Required:** Retain fabric transparency as material, not background residue; use Emily master and extend the dress composition.

#### A088 — emily-gym.png

[Original file](../../assets/portraits/emily-gym.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Lavender sports top and dark leggings show a slim adult build; huge eyes and short leg crop remain.

**Required:** Retain glasses and long hair; refine face, construct both thighs and keep the same body shape across variants.

#### A089 — emily-high-school.png

[Original file](../../assets/portraits/emily-high-school.png) · 1055 × 1491 · contains transparency · **Historical update**.

**Observed:** School Emily holds a miniature greenhouse with visible hand support; familiar large-eyed face and short school skirt composition.

**Required:** Preserve historical age, glasses, hairstyle and miniature prop; render age-appropriate facial planes and complete mid-thigh scene coverage.

#### A090 — emily-picnic.png

[Original file](../../assets/portraits/emily-picnic.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Yellow gingham dress is detailed; repeated face and clasped hands sit above a short skirt crop.

**Required:** Keep check pattern and bow, apply Emily master and continue skirt folds without distorting pattern scale.

#### A091 — emily-rainy.png

[Original file](../../assets/portraits/emily-rainy.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Blue raincoat and striped top are readable; face remains flat and lower coat is truncated.

**Required:** Keep rainwear hardware and stripes; model face and extend coat/trousers with hands clear of the lower boundary.

#### A092 — emily-selection.png

[Original file](../../assets/portraits/emily-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Emily's signature glasses, blue pinafore, ribbon and long blonde hair are strong identity cues; very large eyes and small chin feel doll-like.

**Required:** Build a delicate adult master with blue eyes and dimensional nose/lips; retain glasses and ornate clothes, extend skirt to mid-thigh.

#### A093 — emily-sleep.png

[Original file](../../assets/portraits/emily-sleep.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Pink lace sleepwear shows adult body but repeats simplified facial proportions; high leg crop and small corner mark.

**Required:** Use adult Emily master, retain coverage and fine straps; extend thighs, inspect/remove corner artefact and verify hair/lace edges.

#### A094 — emily-velvet.png

[Original file](../../assets/portraits/emily-velvet.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy velvet has convincing sheen; face and upper skirt composition retain the old master.

**Required:** Retain velvet texture and necklace; refine face and extend dress with natural body volume beneath it.

#### A095 — emily-winter.png

[Original file](../../assets/portraits/emily-winter.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Camel coat and burgundy scarf are richly layered; face stays small-nosed and lower body short.

**Required:** Retain scarf/coat silhouette; apply Emily master and complete lower-body framing without compressing the neck.

#### A096 — emily-workshop.png

[Original file](../../assets/portraits/emily-workshop.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Workshop overalls, lavender shirt and paint marks are distinct; folded hands crowd the bottom.

**Required:** Preserve practical clothes and paint, refine face/fingers and extend overall legs to mid-thigh.

### Review sheet 09

[Open labelled complete-canvas sheet](review-09.jpg).

#### A097 — euan-marsh-selection.png

[Original file](../../assets/portraits/euan-marsh-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Euan's grey curls, glasses and apron identify an older worker; half-body crop and flat complexion remain.

**Required:** Keep age and kind expression, soften facial planes and construct full apron, arms and legs without youthful smoothing.

#### A098 — evelyn-mercer-selection.png

[Original file](../../assets/portraits/evelyn-mercer-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Evelyn has silver bob, glasses and dark suit over teal blouse; long body framing is closer to target.

**Required:** Preserve mature facial structure and complexion, soften hard skin shadows and standardise thigh/hand margins.

#### A099 — farah-haddad-selection.png

[Original file](../../assets/portraits/farah-haddad-selection.png) · 1163 × 1352 · contains transparency · **Restyle + reframe**.

**Observed:** Farah has grey-streaked curls, age lines and ochre apron; bust crop omits hands and lower body.

**Required:** Retain mature warmth and hair texture; model cheek/nose volume and construct practical apron/body to mid-thigh.

#### A100 — felix-ward-selection.png

[Original file](../../assets/portraits/felix-ward-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Felix's swept grey hair, stubble and green scarf sit on a long workwear figure; skin planes are graphic.

**Required:** Preserve age and scarf silhouette; refine facial volume, jacket weight and complete consistent thigh coverage.

#### A101 — fox-contact.png

[Original file](../../assets/portraits/fox-contact.png) · 1254 × 1254 · fully opaque · **Reference / archive / derivative**.

**Observed:** Fox contact image is intentionally opaque and scenic, with a close facial/tattoo view.

**Required:** Retain square scenic purpose; use for likeness consistency, not as a failed transparent portrait or forced mid-thigh avatar.

#### A102 — fox-selection.png

[Original file](../../assets/portraits/fox-selection.png) · 1024 × 1536 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Fox scene art already has weathered face, silver hair, tattoos and tactical gear; hands pocketed and thighs short.

**Required:** Retain mature character and gear/markings, extend to mid-thigh, add headroom and check fine tattoo/cable edges.

#### A103 — gabe-turner-selection.png

[Original file](../../assets/portraits/gabe-turner-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Gabe's tousled curls and wide smile are clear; torso cutoff and line-heavy face look more cartoon-like.

**Required:** Retain easy warmth and olive shirt; model mouth/teeth/cheeks and construct full relaxed stance, hands and legs.

#### A104 — garrett-beach-shorts.png

[Original file](../../assets/portraits/garrett-beach-shorts.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Garrett beach shows extensive tattoos and highly segmented muscles; crop ends at shorts/upper thighs.

**Required:** Preserve exact tattoo map and broad athletic build, soften muscle planes and apply mature face master with longer thigh coverage.

#### A105 — garrett-fashion-asymmetric.png

[Original file](../../assets/portraits/garrett-fashion-asymmetric.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Asymmetric black coat and gold chain have strong design; angular face and hip-level crop remain.

**Required:** Retain asymmetry and neck tattoo visibility; refine face and extend coat/trousers without changing signature physique.

#### A106 — garrett-fashion-pearl.png

[Original file](../../assets/portraits/garrett-fashion-pearl.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Ivory fashion cape layers and satin shirt are detailed; head and lower-body crop follow old master.

**Required:** Keep cape construction and gold accents; apply Garrett master and extend thighs with clean sleeve/body separation.

#### A107 — garrett-formal-burgundy.png

[Original file](../../assets/portraits/garrett-formal-burgundy.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy double-breasted tailoring has rich velvet reflections; face is graphic and lower coat cut high.

**Required:** Keep fabric, buttons and jewellery; improve facial depth and continue trousers to mid-thigh.

#### A108 — garrett-formal-tuxedo.png

[Original file](../../assets/portraits/garrett-formal-tuxedo.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Tuxedo, bow tie and gold pocket square are clear; face and high waist/hip framing need change.

**Required:** Retain formal coverage and concealed tattoos where clothed; apply master and extend jacket/trousers naturally.

### Review sheet 10

[Open labelled complete-canvas sheet](review-10.jpg).

#### A109 — garrett-gym-compression.png

[Original file](../../assets/portraits/garrett-gym-compression.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Compression shirt shows sharply segmented torso; tattooed forearms and waist crop dominate.

**Required:** Preserve tattoos and athletic size, reduce etched muscle shading through fabric and show legs to mid-thigh.

#### A110 — garrett-gym-tank.png

[Original file](../../assets/portraits/garrett-gym-tank.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Black gym tank exposes dense tattoo coverage and defined muscles; shorts/legs end early.

**Required:** Preserve exact ink locations and tank cut; soften anatomy planes, apply face master and extend thighs.

#### A111 — garrett-high-school.png

[Original file](../../assets/portraits/garrett-high-school.png) · 1145 × 1374 · contains transparency · **Historical update**.

**Observed:** School Garrett has golden hair, shirt/tie, bag and visibly untattooed neck/arms; short body crop.

**Required:** Preserve historical age and absence of adult tattoos, keep school/bag details and extend anatomy with age-appropriate rendering.

#### A112 — garrett-home.png

[Original file](../../assets/portraits/garrett-home.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** White ribbed tank exposes chest/arm tattoos; hip crop and small dark corner mark remain.

**Required:** Keep tank/ink map and mature build; refine face/anatomy, extend trousers and inspect/remove non-character mark.

#### A113 — garrett-ivory.png

[Original file](../../assets/portraits/garrett-ivory.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Ivory suit keeps gold detailing and open collar; face is angular and lower body truncated.

**Required:** Preserve outfit colour and visible tattoo boundary; build face volume and extend trouser thighs.

#### A114 — garrett-selection.png

[Original file](../../assets/portraits/garrett-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Garrett's gold hair/eyes, neck tattoos and black/gold tailoring are distinctive; sharp eyes and chin retain the old stylisation.

**Required:** Establish broad athletic adult master with dimensional nose/lips and natural eyes; preserve all identity marks and build full mid-thigh figure.

#### A115 — garrett-sleep.png

[Original file](../../assets/portraits/garrett-sleep.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Shirtless sleep Garrett exposes detailed tattoo map and hard abdominal segmentation; upper-leg cutoff and corner mark.

**Required:** Keep ink and adult build, soften muscle rendering, extend sleep trousers and remove non-character corner artefact in new art.

#### A116 — garrett-street-ink.png

[Original file](../../assets/portraits/garrett-street-ink.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Black streetwear jacket and ink-like sleeve design are clear; face and short crop need alignment.

**Required:** Preserve jacket closures and markings; apply Garrett master and extend lower body with complete pocketed-hand construction.

#### A117 — garrett-street-jade.png

[Original file](../../assets/portraits/garrett-street-jade.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Jade jacket, embroidery and cross-body bag are useful outfit cues; body ends high.

**Required:** Preserve embroidered pattern and bag attachment; refine face and extend trousers, ensuring the whole relevant bag fits.

#### A118 — garrett-summer-linen.png

[Original file](../../assets/portraits/garrett-summer-linen.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Light linen shirt reveals forearm/neck tattoos; muscular shading and hip crop remain.

**Required:** Keep airy cloth, tattoos and gold hair; refine face/body planes and extend both thighs.

#### A119 — garrett-traditional-changshan.png

[Original file](../../assets/portraits/garrett-traditional-changshan.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Red changshan has gold motifs and closures; collar correctly conceals most neck tattoo, lower garment cut high.

**Required:** Preserve cultural garment construction and tattoo occlusion; apply master and continue garment length over thighs.

#### A120 — garrett-traditional-hanfu.png

[Original file](../../assets/portraits/garrett-traditional-hanfu.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Teal floral hanfu and sash are detailed; face and short lower-body crop are unchanged.

**Required:** Preserve wrap/layer direction, pattern and sash, refine face and show coherent drape to mid-thigh.

### Review sheet 11

[Open labelled complete-canvas sheet](review-11.jpg).

#### A121 — garrett-winter-coat.png

[Original file](../../assets/portraits/garrett-winter-coat.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Camel coat, black knit and plaid scarf have convincing texture; face and trouser crop remain stylised/short.

**Required:** Retain layered winter silhouette; apply master and extend lower coat/trousers without altering head size.

#### A122 — gordon-contact.png

[Original file](../../assets/portraits/gordon-contact.png) · 1254 × 1254 · fully opaque · **Reference / archive / derivative**.

**Observed:** Gordon contact is a square opaque Interpol scene with glasses, stubble and detailed uniform.

**Required:** Keep scenic avatar function and identity reference; no mid-thigh conversion or transparency requirement for this file.

#### A123 — gordon-selection.png

[Original file](../../assets/portraits/gordon-selection.png) · 1024 × 1536 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Gordon scene portrait has mature face, glasses and detailed tactical kit; upper-thigh crop is relatively close.

**Required:** Preserve exact patches/vest and age, refine hand/gear edges and extend framing to explicit mid-thigh with safe margins.

#### A124 — greta-shaw-selection.png

[Original file](../../assets/portraits/greta-shaw-selection.png) · 1122 × 1402 · contains transparency · **Polish + framing**.

**Observed:** Greta's long silver braid and purple waistcoat are distinct; standing silhouette is useful but facial shadows remain graphic.

**Required:** Retain mature face, braid and sharp tailoring; add skin plane transitions and standardise lower-body endpoint.

#### A125 — guards/affiliate.png

[Original file](../../assets/portraits/guards/affiliate.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Affiliate has full helmet/mask, black military kit, gun and visible chest symbol; three-quarter coverage is already near target.

**Required:** Preserve MH-010 design and full concealment, refine material separation and verify weapon, insignia and thigh crop at full size.

#### A126 — guards/clubs.png

[Original file](../../assets/portraits/guards/clubs.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Clubs has hood/mask, club symbol, vest, gun and green fist energy; long figure reads coherently.

**Required:** Keep MH-010 mask/gear and energy; refine cloth/armour rendering, preserve insignia and extend thigh framing only as needed.

#### A127 — guards/crew_enforcer.png

[Original file](../../assets/portraits/guards/crew_enforcer.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Crew enforcer has brown jacket, raised gloved fists and warm energy; stance is long but heavily cel-shaded.

**Required:** Keep identity and current role gear; add facial volume, check wrist/fist anatomy and standardise thigh coverage.

#### A128 — guards/custom_awakened.png

[Original file](../../assets/portraits/guards/custom_awakened.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Custom awakened guard has close hair, dark vest and cyan hand effects; flat skin planes contrast with anchors.

**Required:** Preserve generic role appearance, complexion and equipment; refine skin, fingers and stance without inventing a named identity.

#### A129 — guards/custom_robotic.png

[Original file](../../assets/portraits/guards/custom_robotic.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Custom robotic guard has grey segmented armour, cyan lights and visible mechanical hands; long composition is useful.

**Required:** Retain wholly robotic anatomy and silhouette; refine material/joint logic, full hands and consistent thigh framing without adding skin.

#### A130 — guards/custom_unawakened.png

[Original file](../../assets/portraits/guards/custom_unawakened.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Custom unawakened guard has ponytail, vest and bare forearms in a defensive pose; body is long but face stylised.

**Required:** Preserve role equipment and no-power state; refine facial/forearm planes and full hand anatomy, confirm mid-thigh coverage.

#### A131 — guards/headhunter.png

[Original file](../../assets/portraits/guards/headhunter.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Headhunter has substantial cybernetic armour and mechanical arms with a visible adult face; long figure is close.

**Required:** Keep machinery and weathered identity; unify metal/skin rendering, inspect joints and ensure full required gear fits.

#### A132 — guards/interpol.png

[Original file](../../assets/portraits/guards/interpol.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Interpol guard has dark blue kit, badges and visible hands; face looks youthful and graphically simplified.

**Required:** Preserve existing person and uniform, model facial planes and garment weight, verify insignia and thigh framing.

### Review sheet 12

[Open labelled complete-canvas sheet](review-12.jpg).

#### A133 — guards/kai_guard.png

[Original file](../../assets/portraits/guards/kai_guard.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Kai house guard now wears navy tailoring and burgundy shirt with visible face/hands; pose is long and angular.

**Required:** Preserve MH-011 yakuza design and individual face; soften skin/cloth transitions and confirm complete hands and mid-thigh crop.

#### A134 — guards/kai_sentinel.png

[Original file](../../assets/portraits/guards/kai_sentinel.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Kai sentinel has restrained navy suit, gloves and small gold hand effect; long framing is near target.

**Required:** Keep current tailoring, exposed face and gear; add nuanced face shading and check effect/hand separation and lower crop.

#### A135 — guards/lookout.png

[Original file](../../assets/portraits/guards/lookout.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Lookout has curly hair, burgundy jacket and backpack; broad graphic shadow blocks flatten face/clothes.

**Required:** Retain complexion, curls and ordinary lookout styling; model face/folds, show complete hands and consistent thigh length.

#### A136 — guards/oni.png

[Original file](../../assets/portraits/guards/oni.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Oni now has horned robotic head, red optics, tailored black suit and burgundy layers; good long silhouette.

**Required:** Preserve fully mechanical body, forearm systems and MH-011 accessories; refine material transitions and verify crop/hand details.

#### A137 — guards/pmc.png

[Original file](../../assets/portraits/guards/pmc.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** PMC guard has grey tactical clothes, orange patches, rifle and helmet; torso/legs already visible.

**Required:** Keep equipment and adult identity, improve face/skin modelling and inspect rifle grip, straps and thigh clearance.

#### A138 — guards/richter_cybernetic.png

[Original file](../../assets/portraits/guards/richter_cybernetic.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Cybernetic Richter has blond hair, vest/tie and large mechanical arms; body is long but face remains stylised.

**Required:** Retain hidden boss design and arm structure; refine face and metal joints, standardise crop and preserve restricted runtime context.

#### A139 — guards/seeker.png

[Original file](../../assets/portraits/guards/seeker.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Seeker has dark bob, armour, gold eyewear/detail and mechanical limbs; big eyes are prominent.

**Required:** Keep cyborg design and gear, refine facial proportions and material shading; inspect full hands/joints and thigh coverage.

#### A140 — guards/spades.png

[Original file](../../assets/portraits/guards/spades.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Spades has opaque spade mask, layered dark cloak and knife; refreshed design is already long and detailed.

**Required:** Preserve MH-010 concealment/insignia/knife, refine dark material separation and validate blade/hand edges and crop.

#### A141 — guards/team9.png

[Original file](../../assets/portraits/guards/team9.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Team 9 has braided/updo hair, blue armour, sidearm and violet hand energy; long figure with stylised face.

**Required:** Preserve complexion, hair and equipment; add skin depth and check holster, hand/effect anatomy and framing.

#### A142 — guards/tengu.png

[Original file](../../assets/portraits/guards/tengu.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Tengu wears refreshed charcoal tailoring, patterned shirt and jewellery; full hands and thighs are visible.

**Required:** Preserve MH-011 luxurious civilian gear and no invented weapon/power; refine face/cloth planes and final crop.

#### A143 — guards/yokai.png

[Original file](../../assets/portraits/guards/yokai.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Yokai has broad build, pinstripe suit, patterned burgundy shirt and red fist energy; long figure is near target.

**Required:** Preserve MH-011 muscular identity and accessories, soften face/muscle planes and check complete fist/gear/thigh coverage.

#### A144 — hazel-reed-selection.png

[Original file](../../assets/portraits/hazel-reed-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Hazel has curls, freckles and green outerwear, but chest crop and flat skin separate her from anchors.

**Required:** Retain curls/complexion/freckles; construct arms/hands/lower body and add nuanced facial modelling without smoothing individuality.

### Review sheet 13

[Open labelled complete-canvas sheet](review-13.jpg).

#### A145 — imani-price-selection.png

[Original file](../../assets/portraits/imani-price-selection.png) · 1122 × 1402 · contains transparency · **Polish + framing**.

**Observed:** Imani's braids, navy work coveralls and orange headphones are distinct; long silhouette is useful but shading flat.

**Required:** Keep complexion, braids and workwear; model face and cloth volume, verify fingers and mid-thigh framing.

#### A146 — iris-selection.png

[Original file](../../assets/portraits/iris-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Iris has dark bob with teal ends and denim jacket; high hip crop and simplified facial planes remain.

**Required:** Preserve teal ends, jewellery and friendly adult face; refine nose/lips and extend relaxed trouser pose.

#### A147 — isabel-vega-selection.png

[Original file](../../assets/portraits/isabel-vega-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Isabel's red blazer, dark blouse and low bun create a long authoritative silhouette; hard shadows dominate.

**Required:** Retain strong features and mature styling, add skin transitions and credible trouser depth to mid-thigh.

#### A148 — ivan-beach.png

[Original file](../../assets/portraits/ivan-beach.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Ivan beach keeps anchor likeness but muscles have angular shadow facets and crop ends just below waistband.

**Required:** Preserve lean broad-shouldered build and coral shorts; soften torso planes and extend both thighs without changing face.

#### A149 — ivan-fashion-burgundy.png

[Original file](../../assets/portraits/ivan-fashion-burgundy.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Ivan burgundy fashion drape is richly rendered; composition remains hip-high.

**Required:** Keep face and asymmetric drape/brooch, extend trousers to mid-thigh with the same natural pocketed pose.

#### A150 — ivan-fashion-ivory.png

[Original file](../../assets/portraits/ivan-fashion-ivory.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Ivory double-breasted fashion suit retains strong likeness and material contrast; trouser length in frame is short.

**Required:** Preserve tailoring/face and extend anatomical lower body, avoiding stretched jacket or narrowed shoulders.

#### A151 — ivan-fashion-pearl.png

[Original file](../../assets/portraits/ivan-fashion-pearl.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Pearl-grey cropped jacket and dark high-neck top preserve anchor face; pelvis/legs barely appear.

**Required:** Retain cropped jacket length and pendant-like lapel detail; extend trousers, not jacket, to achieve mid-thigh coverage.

#### A152 — ivan-gym-tank.png

[Original file](../../assets/portraits/ivan-gym-tank.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Ivan gym tank preserves face and build; torso shading is graphic and lower body stops early.

**Required:** Keep dark tank and lean muscle scale; soften skin planes and show shorts/legs through mid-thigh.

#### A153 — ivan-gym-training.png

[Original file](../../assets/portraits/ivan-gym-training.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Blue training tee and dark trousers keep anchor likeness; waist/hip crop remains.

**Required:** Retain athletic fit and soft face rendering; continue trouser thighs and check arms connect naturally under sleeves.

#### A154 — ivan-idol-crimson.png

[Original file](../../assets/portraits/ivan-idol-crimson.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Crimson idol jacket, chains and stage detailing are clear; lower figure is short.

**Required:** Preserve stage costume and identity, extend trousers and maintain garment proportions instead of elongating torso.

#### A155 — ivan-idol-midnight.png

[Original file](../../assets/portraits/ivan-idol-midnight.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Midnight embroidered idol coat has useful texture and chain detail; high crop hides thigh length.

**Required:** Keep embroidery placement and face; extend coat/trouser silhouette and verify chains at display size.

#### A156 — ivan-idol-white.png

[Original file](../../assets/portraits/ivan-idol-white.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** White/gold stage tailoring preserves identity; low composition stops near belt/hip.

**Required:** Keep gold embroidery and closures; extend lower garment with natural stance and clear hip anatomy.

### Review sheet 14

[Open labelled complete-canvas sheet](review-14.jpg).

#### A157 — ivan-selection.png

[Original file](../../assets/portraits/ivan-selection.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Primary Ivan anchor has dimensional nose/lips, eyelids, subtle freckles and natural shoulders; source reaches hair at top and ends near hips.

**Required:** Preserve likeness/rendering, add headroom and rebuild lower composition to mid-thigh; do not use existing crop as acceptance standard.

#### A158 — ivan-street-denim.png

[Original file](../../assets/portraits/ivan-street-denim.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Denim jacket and cream hoodie have convincing material detail; framing retains Ivan's high crop.

**Required:** Keep face and layered denim/hood volume, extend trousers and maintain collar/neck proportions.

#### A159 — ivan-street-knit.png

[Original file](../../assets/portraits/ivan-street-knit.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Sage cardigan over white tee retains anchor face with good knit texture; lower body is brief.

**Required:** Preserve knit weight and relaxed posture; extend trousers and compare head/eye position across Ivan variants.

#### A160 — ivan-street-monochrome.png

[Original file](../../assets/portraits/ivan-street-monochrome.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Black monochrome streetwear jacket and white tee are clear; lower crop remains hip-high.

**Required:** Keep garment straps/closures and face, extend trousers with believable pelvis and complete pocketed wrists.

#### A161 — ivan-street-varsity.png

[Original file](../../assets/portraits/ivan-street-varsity.png) · 1122 × 1402 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Navy/cream varsity jacket uses crisp folds and the anchor face; legs are short in frame.

**Required:** Preserve varsity proportions and striped trims; extend trouser thighs without shrinking the head disproportionately.

#### A162 — ivan-syndicate.png

[Original file](../../assets/portraits/ivan-syndicate.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Ivan's masked Joker uniform is waist-up with strong black/white cloth blocks; no civilian features visible.

**Required:** Keep opaque Joker mask and concealed identity; construct complete arms/robe to mid-thigh and refine cloth planes, not face features.

#### A163 — jace-mercer-selection.png

[Original file](../../assets/portraits/jace-mercer-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Jace has close hair, dark tracksuit and strong brows; half-body crop and graphic skin shadows need restyling.

**Required:** Preserve individual brow/jaw and short hair, add face volume and construct full arms/trousers with no invented accessories.

#### A164 — jonah-price-selection.png

[Original file](../../assets/portraits/jonah-price-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Jonah has short locs, beard and work apron; chest cutoff omits hands and lower apron.

**Required:** Retain complexion, hair and approachable expression; build full working stance and nuanced face/apron rendering.

#### A165 — joseph-richter-high-school.png

[Original file](../../assets/portraits/joseph-richter-high-school.png) · 1122 × 1402 · contains transparency · **Historical update**.

**Observed:** School Richter has blond hair, burgundy sweater and backpack; younger clean-shaven face contrasts with adult.

**Required:** Preserve youth and period clothing, refine planes without adult ageing or cyborg additions, extend lower-body coverage.

#### A166 — joseph-richter-selection.png

[Original file](../../assets/portraits/joseph-richter-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Adult Richter has blond hair, stubble, waistcoat and adjusting hands; high crop and stylised face remain.

**Required:** Preserve age distinction, formal clothes and watch; model face/hands and extend trousers; no boss machinery in ordinary form.

#### A167 — jules-navarro-selection.png

[Original file](../../assets/portraits/jules-navarro-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Jules has dark swept hair, purple neck scarf and black utility clothes; long figure but highly graphic grin/shadows.

**Required:** Retain scarf and lively identity, model mouth/skin and inspect hands and trouser coverage.

#### A168 — june-selection.png

[Original file](../../assets/portraits/june-selection.png) · 1143 × 1376 · contains transparency · **Restyle + reframe**.

**Observed:** June's grey braid, green shirt and rust overalls are readable; lower crop remains around hips.

**Required:** Preserve mature age and garden gloves/overalls, soften facial rendering and extend body to mid-thigh.

### Review sheet 15

[Open labelled complete-canvas sheet](review-15.jpg).

#### A169 — keiko-tan-selection.png

[Original file](../../assets/portraits/keiko-tan-selection.png) · 1222 × 1287 · contains transparency · **Restyle + reframe**.

**Observed:** Keiko has short black bob and blue work shirt; oversized eyes, simple nose and chest crop are pronounced.

**Required:** Keep adult identity and bright expression, reconstruct natural facial planes and full practical standing body.

#### A170 — keira-shaw-selection.png

[Original file](../../assets/portraits/keira-shaw-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Keira has long braids, shaved side and plum bomber; waist crop and graphic face need change.

**Required:** Preserve hair pattern, complexion and earrings; model face and construct hands/pelvis/thighs with the same confident posture.

#### A171 — keisuke-hachimura-selection.png

[Original file](../../assets/portraits/keisuke-hachimura-selection.png) · 1122 × 1402 · contains transparency · **Polish + framing**.

**Observed:** Keisuke has swept dark hair, stubble and brown coat; reasonable adult face but hip cutoff.

**Required:** Retain mature identity and coat texture; refine skin transitions and extend coat/trousers to mid-thigh.

#### A172 — lena-selection-v1.png

[Original file](../../assets/portraits/lena-selection-v1.png) · 1086 × 1448 · contains transparency · **Reference / archive / derivative**.

**Observed:** Lena v1 has more dimensional face/hair than later version, burgundy waistcoat and bow; still short-framed.

**Required:** Preserve as historical style/identity evidence; do not silently make active. Use useful facial planes when correcting the current master.

#### A173 — lena-selection-v2.png

[Original file](../../assets/portraits/lena-selection-v2.png) · 1086 × 1448 · contains transparency · **Reference / archive / derivative**.

**Observed:** Lena v2 has larger graphic eyes and sharper chin than v1; outfit and pose remain similar.

**Required:** Retain version history and check consumers before retirement; active replacement must follow corrected master, not copy this stylisation.

#### A174 — lena-selection.png

[Original file](../../assets/portraits/lena-selection.png) · 1086 × 1448 · contains transparency · **Restyle + reframe**.

**Observed:** Current Lena combines detailed curls/waistcoat with simplified large-eyed face and high lower crop.

**Required:** Keep warm complexion, bow and adult features; use dimensional planes informed by v1/anchors and extend lower-body framing.

#### A175 — leo-selection.png

[Original file](../../assets/portraits/leo-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Leo's orange jacket, shoulder bag and open grin identify him; hard fold wedges and short framing remain.

**Required:** Preserve youthful adult identity, orange kit and bag; model mouth/skin and complete trousers to mid-thigh.

#### A176 — lucia-serrano-selection.png

[Original file](../../assets/portraits/lucia-serrano-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Lucia has long curls, red scarf and dark blouse with full hands; face/clothes are sharply graphic.

**Required:** Keep distinct stern face and curl volume, soften planes and standardise thigh composition.

#### A177 — luz-moreno-selection.png

[Original file](../../assets/portraits/luz-moreno-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Luz has curly ponytail, denim shirt and toothy smile; chest/waist crop hides hands and legs.

**Required:** Preserve complexion/curls and joyful expression; give lips/teeth depth and construct a full relaxed mid-thigh pose.

#### A178 — malik-reed-selection.png

[Original file](../../assets/portraits/malik-reed-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Malik Reed has glasses, short hair and green overshirt; long stance is useful but skin is flatly shaded.

**Required:** Retain adult identity and lean build, refine nose/cheeks through glasses and standardise hand/thigh margins.

#### A179 — malik-torres-selection.png

[Original file](../../assets/portraits/malik-torres-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Malik Torres has curly fringe, teal hoodie and patched vest; broad outlined grin and bust crop stand out.

**Required:** Keep hair, complexion and individual patches, soften mouth/face modelling and construct arms/lower body to mid-thigh.

#### A180 — mara-voss-selection.png

[Original file](../../assets/portraits/mara-voss-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Mara has short red hair, mustard scarf and dark tailoring; long pose but severe stylised face.

**Required:** Retain sharp individual features and scarf; model facial planes without generic beautification and verify thigh endpoint.

### Review sheet 16

[Open labelled complete-canvas sheet](review-16.jpg).

#### A181 — marcus-high-school.png

[Original file](../../assets/portraits/marcus-high-school.png) · 1145 × 1374 · contains transparency · **Historical update**.

**Observed:** Marcus school portrait has red hair, mustard cardigan, notebook and pen; slight youthful face and short thigh coverage.

**Required:** Preserve historical age, tools and warm expression; model age-appropriate planes, inspect pen grip and extend trousers.

#### A182 — mario-romano-selection.png

[Original file](../../assets/portraits/mario-romano-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Mario's moustache, grey-streaked curls and apron identify him; broad tooth bar and graphic shadows dominate.

**Required:** Keep mature robust build and chef styling; refine smile/cheeks, complete lower apron/body and preserve natural hands-on-hips anatomy.

#### A183 — marta-silva-selection.png

[Original file](../../assets/portraits/marta-silva-selection.png) · 1196 × 1315 · contains transparency · **Restyle + reframe**.

**Observed:** Marta has grey-streaked braid, age lines and plum shirt; half-body crop and flat skin modelling remain.

**Required:** Retain age and warm smile, soften wrinkle lines and construct arms/hands/pelvis/legs without youthful idealisation.

#### A184 — martos-selection.png

[Original file](../../assets/portraits/martos-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Martos's huge shoulders, scars, swept hair and pinstripe suit read clearly; portrait ends at torso.

**Required:** Preserve exceptional size/scars and mature face; construct full body through mid-thigh and model face/neck rather than slim him.

#### A185 — martos-syndicate.png

[Original file](../../assets/portraits/martos-syndicate.png) · 1312 × 1199 · contains transparency · **Restyle + reframe**.

**Observed:** Martos's Clubs robe is particularly broad and short-framed; mask and white layers conceal identity.

**Required:** Preserve Clubs symbol, large scale and sealed mask; build complete sleeves/robe and mid-thigh body volume with coherent cloth.

#### A186 — mateo-cruz-selection.png

[Original file](../../assets/portraits/mateo-cruz-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Mateo has moustache, burgundy work shirt and dark cargo trousers; full hands and long stance already visible.

**Required:** Preserve mature features and sturdy body, soften face/cloth shadow transitions and standardise thigh endpoint.

#### A187 — mavis-selection.png

[Original file](../../assets/portraits/mavis-selection.png) · 1199 × 1312 · contains transparency · **Preserve rendering + reframe**.

**Observed:** Mavis has detailed hood, wolf-cut hair, piercings and tattoos; face is closer to dimensional style but body ends near belt.

**Required:** Retain adult wiry identity and precise piercings/tattoos; extend legs and complete hands without reducing hood shadow excessively.

#### A188 — mavis-syndicate.png

[Original file](../../assets/portraits/mavis-syndicate.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Mavis's Spades robe has sealed mask, belt and layered white fabric; lower crop is waist-high.

**Required:** Keep concealed identity and exact symbol; extend robe/arms through mid-thigh, avoid any visible tattoos or facial features.

#### A189 — maya-selection.png

[Original file](../../assets/portraits/maya-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Maya has curls, gold headband and rust apron; large graphic smile and high lower crop remain.

**Required:** Preserve warm complexion, hair and work identity; model smile/skin and extend full apron/body with natural hands.

#### A190 — mina-cho-selection.png

[Original file](../../assets/portraits/mina-cho-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Mina has black ponytail, red blouse and charcoal trousers; long composition but angular face/garment planes.

**Required:** Keep precise face/hair and outfit, refine skin modelling and confirm complete hands and thigh coverage.

#### A191 — minsu-beach-shorts.png

[Original file](../../assets/portraits/minsu-beach-shorts.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Minsu beach has very segmented abdominal/pectoral shadows and a broad graphic grin; shorts cut high.

**Required:** Retain lean athletic identity rather than inflate muscle mass; soften body/face planes and extend thighs below blue shorts.

#### A192 — minsu-college-knit.png

[Original file](../../assets/portraits/minsu-college-knit.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Light blue knit polo and cream trousers are coherent; broad grin and angular face repeat the current master.

**Required:** Use softer-contoured Minsu master; retain shirt fit and watch, extend trousers to mid-thigh.

### Review sheet 17

[Open labelled complete-canvas sheet](review-17.jpg).

#### A193 — minsu-college-overshirt.png

[Original file](../../assets/portraits/minsu-college-overshirt.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Plaid overshirt, cream tee and pocketed hands share graphic face and short crop.

**Required:** Preserve plaid alignment and relaxed adult smile, apply corrected face and extend trousers with natural pocket openings.

#### A194 — minsu-college-rugby.png

[Original file](../../assets/portraits/minsu-college-rugby.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy/cream rugby top and backpack are distinct; large outlined grin and lower crop remain.

**Required:** Keep stripes and bag support, model facial volume and continue trousers without lengthening torso.

#### A195 — minsu-gym-compression.png

[Original file](../../assets/portraits/minsu-gym-compression.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Compression tee has hard abdominal shading through fabric; high crop and sharp jaw amplify stylisation.

**Required:** Retain athletic build and navy top, soften muscle definition through cloth and use master face/full thighs.

#### A196 — minsu-gym-tank.png

[Original file](../../assets/portraits/minsu-gym-tank.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Green gym tank exposes strongly segmented arms; cheerful face and waistband crop remain graphic.

**Required:** Preserve strength without body inflation, refine arm/face planes and extend shorts/thighs.

#### A197 — minsu-home.png

[Original file](../../assets/portraits/minsu-home.png) · 1264 × 1568 · contains transparency · **Restyle + reframe**.

**Observed:** Black fitted home shirt shows hard torso planes; high crop and small corner mark visible.

**Required:** Use Minsu master and softer fabric/anatomy shading, extend home trousers and inspect/remove corner artefact.

#### A198 — minsu-med-scrubs.png

[Original file](../../assets/portraits/minsu-med-scrubs.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Teal scrubs and badge are useful context cues; face and hip crop repeat the current stylisation.

**Required:** Retain medical outfit and badge without invented credentials/text; model face and extend scrub trousers with believable pockets.

#### A199 — minsu-med-white-coat.png

[Original file](../../assets/portraits/minsu-med-white-coat.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** White coat, stethoscope and blue shirt are detailed; face and lower frame remain short/stylised.

**Required:** Preserve medical gear and adult identity, refine hands/pockets and extend coat/trousers to mid-thigh.

#### A200 — minsu-selection-v1.png

[Original file](../../assets/portraits/minsu-selection-v1.png) · 1122 × 1402 · contains transparency · **Reference / archive / derivative**.

**Observed:** Minsu v1 has softer facial planes and less graphic garment shading than current art, still with high crop.

**Required:** Keep as archived secondary rendering evidence, not an automatic active replacement; reconcile likeness against canon/current master first.

#### A201 — minsu-selection.png

[Original file](../../assets/portraits/minsu-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Current Minsu uses sharp cheek/jaw shadows and a broad white tooth shape; bomber/tee crop ends around hips.

**Required:** Build softer-contoured adult master preserving dark hair, friendly smile and athletic build; model mouth/nose and show full mid-thigh body.

#### A202 — minsu-sleep.png

[Original file](../../assets/portraits/minsu-sleep.png) · 1264 × 1568 · contains transparency · **Restyle + reframe**.

**Observed:** Shirtless sleep Minsu has hard repeated muscle wedges, short lower-body crop and small corner mark.

**Required:** Preserve athletic identity and sleep trousers; soften anatomy, extend thighs, inspect/remove non-character mark.

#### A203 — minsu-street-denim.png

[Original file](../../assets/portraits/minsu-street-denim.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Denim street outfit and cross-body bag have fine detail; face and hip framing remain stylised.

**Required:** Retain bag/strap construction and denim, use corrected master and extend trousers with no clipped bag parts.

#### A204 — minsu-street-monochrome.png

[Original file](../../assets/portraits/minsu-street-monochrome.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Black monochrome jacket has graphic fold wedges and unchanged short-body master.

**Required:** Preserve dark layers and belt, model face/cloth transitions and continue lower body to mid-thigh.

### Review sheet 18

[Open labelled complete-canvas sheet](review-18.jpg).

#### A205 — minsu-street-track.png

[Original file](../../assets/portraits/minsu-street-track.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Blue/cream track jacket retains athletic colour blocking; toothy face and short lower frame remain.

**Required:** Keep tracksuit styling, use softer adult face and extend joggers/thighs with natural pocketed hands.

#### A206 — minsu-study-cardigan.png

[Original file](../../assets/portraits/minsu-study-cardigan.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Cable cardigan and glasses add study identity; face/grin still graphic and lower body short.

**Required:** Preserve optional glasses and knit, model face through lenses and extend trousers consistently with master.

#### A207 — minsu-study-hoodie.png

[Original file](../../assets/portraits/minsu-study-hoodie.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Lavender hoodie uses broad flat folds and the current sharp smiling face; waist/hip crop.

**Required:** Retain cosy volume and colour, soften skin/fabric transitions and construct full mid-thigh composition.

#### A208 — minsu-varsity.png

[Original file](../../assets/portraits/minsu-varsity.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Green varsity jacket and grey hood retain athletic silhouette; stylised grin and short lower crop remain.

**Required:** Preserve jacket trim and hood, apply master face and extend trousers with consistent head/eye position.

#### A209 — nadia-flores-selection.png

[Original file](../../assets/portraits/nadia-flores-selection.png) · 1200 × 1310 · contains transparency · **Restyle + reframe**.

**Observed:** Nadia has short layered hair, warm round face and amber scarf; torso crop and flat skin are strong departures.

**Required:** Preserve mature round features and transit shirt, model age/skin and build full arms/lower body without slimming her.

#### A210 — naomi-selection.png

[Original file](../../assets/portraits/naomi-selection.png) · 1086 × 1448 · contains transparency · **Polish + framing**.

**Observed:** Naomi's asymmetrical dark bob, blue overshirt and olive trousers are coherent; facial planes are simplified and legs short.

**Required:** Keep androgynous/practical styling and slim adult build, refine face and extend relaxed pose to mid-thigh.

#### A211 — neo-scene.png

[Original file](../../assets/portraits/neo-scene.png) · 1086 × 1448 · contains transparency · **Polish + framing**.

**Observed:** Neo's actual scene PNG has tattoo sleeves, black tee and long torso; angular face and high trouser crop remain.

**Required:** Preserve exact sleeve tattoos and scene identity, refine face/skin and extend legs; keep this transparent route distinct from scenic selection source.

#### A212 — neo-selection.png

[Original file](../../assets/portraits/neo-selection.png) · 1254 × 1254 · fully opaque · **Reference / archive / derivative**.

**Observed:** Neo selection is an opaque workshop scene and close portrait, unlike the separate transparent scene file.

**Required:** Retain scenic/reference purpose; verify selection routing to scene art and avoid mistakenly treating this photo-style composition as a cutout.

#### A213 — nessa-quinn-selection.png

[Original file](../../assets/portraits/nessa-quinn-selection.png) · 1122 × 1402 · contains transparency · **Polish + framing**.

**Observed:** Nessa has long ginger curls, ochre work apron and dark sleeves; long figure but hard face/fold lines.

**Required:** Preserve curls and workshop gear, add facial/material volume and ensure lower apron/legs reach standard crop.

#### A214 — noah-selection.png

[Original file](../../assets/portraits/noah-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Noah has short locs, burgundy overshirt and bag strap; graphic smile and high hip crop remain.

**Required:** Preserve complexion and friendly adult identity, refine mouth/cheeks and extend trousers with believable bag/hand placement.

#### A215 — otis-bell-selection.png

[Original file](../../assets/portraits/otis-bell-selection.png) · 1278 × 1230 · contains transparency · **Restyle + reframe**.

**Observed:** Otis has silver hair/beard, weathered face and broad build; bust crop omits arms/legs and age lines are heavily inked.

**Required:** Keep elderly robust identity, soften wrinkle/beard rendering without erasing age and construct full workwear stance to mid-thigh.

#### A216 — owen-pike-selection.png

[Original file](../../assets/portraits/owen-pike-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Owen's sandy swept hair, grey utility jacket and complete hands form a long figure; face/folds remain graphic.

**Required:** Retain angular identity and hair colour, refine face/cloth planes and standardise thigh endpoint.

### Review sheet 19

[Open labelled complete-canvas sheet](review-19.jpg).

#### A217 — priya-shah-selection.png

[Original file](../../assets/portraits/priya-shah-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Priya's bun, rectangular glasses and plum/teal clothes are distinctive; half-body crop and flat cheek shading stand out.

**Required:** Preserve mature face and medium-brown complexion, refine facial planes through glasses and build hands/lower body to mid-thigh.

#### A218 — rafe-calder-selection.png

[Original file](../../assets/portraits/rafe-calder-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Rafe has tied-back hair, grey beard and black/purple biker vest; muscular long figure but hard shadow anatomy.

**Required:** Retain mature build, beard and vest insignia, soften skin planes and inspect complete hands/thighs.

#### A219 — ravi-menon-selection.png

[Original file](../../assets/portraits/ravi-menon-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Ravi has curls, beard and navy chef coat; chest/waist crop and broad graphic smile need change.

**Required:** Retain warmth and facial hair, model mouth/cheeks and construct full chef coat, arms and trouser thighs.

#### A220 — rei-beach.png

[Original file](../../assets/portraits/rei-beach.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Rei beach already shows shorts and upper thighs; tattoos and muscles are dense, face remains sharply stylised.

**Required:** Preserve tattoo map, lean build and black hair; refine facial/muscle planes, extend slightly to standard endpoint and check laterality.

#### A221 — rei-black-sweater.png

[Original file](../../assets/portraits/rei-black-sweater.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Black sweater, chain and neck ink identify Rei; face is angular and lower crop near belt.

**Required:** Apply restrained adult Rei master, preserve visible tattoo limits and continue trouser anatomy.

#### A222 — rei-burgundy-shirt.png

[Original file](../../assets/portraits/rei-burgundy-shirt.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy shirt has rich sheen with exposed chest tattoos; facial planes and hip crop remain old style.

**Required:** Keep shirt opening and exact visible ink, refine face and extend trousers with natural cloth tension.

#### A223 — rei-camel-overcoat.png

[Original file](../../assets/portraits/rei-camel-overcoat.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Camel overcoat and black high neck cover tattoos appropriately; face and upper-leg crop remain short/stylised.

**Required:** Preserve coat construction and concealed ink, apply master and continue coat/trousers to mid-thigh.

#### A224 — rei-charcoal-hoodie.png

[Original file](../../assets/portraits/rei-charcoal-hoodie.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Charcoal hoodie over black layers retains tattoos and quiet expression; short crop and sharp face persist.

**Required:** Keep practical streetwear and visible neck markings, model face and extend lower body without increasing bulk.

#### A225 — rei-cream-cardigan.png

[Original file](../../assets/portraits/rei-cream-cardigan.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Cream cardigan has fine knit detail but face remains graphic and body ends near hips.

**Required:** Preserve knit scale, black tee and tattoo visibility; apply Rei master and continue trousers.

#### A226 — rei-denim-jacket.png

[Original file](../../assets/portraits/rei-denim-jacket.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Denim jacket and light tee have realistic texture; short crop and angular face are the main mismatch.

**Required:** Keep garment details and ink occlusion, improve face planes and extend thighs instead of adding more texture.

#### A227 — rei-gym.png

[Original file](../../assets/portraits/rei-gym.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Gym tank exposes tattoo sleeves and lean musculature; high leg crop and hard muscle grooves remain.

**Required:** Preserve exact ink and lean strength, soften anatomy planes and extend shorts/thighs.

#### A228 — rei-haori-hakama.png

[Original file](../../assets/portraits/rei-haori-hakama.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Haori/hakama layers and waist tie read clearly; facial planes and short lower crop need alignment.

**Required:** Preserve wrap construction and culturally coherent layers, apply master and extend hakama drape to mid-thigh.

### Review sheet 20

[Open labelled complete-canvas sheet](review-20.jpg).

#### A229 — rei-high-school.png

[Original file](../../assets/portraits/rei-high-school.png) · 1145 × 1374 · contains transparency · **Historical update**.

**Observed:** School Rei has untattooed neck/arms, blue overshirt and youthful face; lower crop short.

**Required:** Keep period age and absence of adult ink, refine youthful planes without making him older and extend trousers.

#### A230 — rei-home.png

[Original file](../../assets/portraits/rei-home.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Home tank exposes detailed ink and lean arms; hip crop and small corner mark visible.

**Required:** Preserve tattoo layout and adult body, refine face/anatomy, extend trousers and inspect/remove non-character mark.

#### A231 — rei-moto.png

[Original file](../../assets/portraits/rei-moto.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Leather moto jacket has convincing texture; face and high trouser crop remain old style.

**Required:** Retain leather seams and ink visibility, refine facial volume and extend legs while keeping jacket length.

#### A232 — rei-navy-yukata.png

[Original file](../../assets/portraits/rei-navy-yukata.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Navy yukata covers most torso ink and uses broad fold planes; crop ends near hip.

**Required:** Preserve wrap/obi and tattoo occlusion, model face and extend garment naturally through thighs.

#### A233 — rei-olive-bomber.png

[Original file](../../assets/portraits/rei-olive-bomber.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Olive bomber gives a clean silhouette; angular face and short lower body persist.

**Required:** Keep olive colour, dark knit and visible neck markings; apply master and extend trouser thighs.

#### A234 — rei-selection.png

[Original file](../../assets/portraits/rei-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Rei signature has dense neck/chest ink, layered black hair and dark tailoring; sharp jaw and minimal nose/lips read stylised.

**Required:** Build lean adult master with restrained expression and dimensional face, preserving ink map and complete mid-thigh composition.

#### A235 — rei-sleep.png

[Original file](../../assets/portraits/rei-sleep.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Shirtless sleep Rei exposes dense tattoo reference and strongly defined torso; high crop and corner mark.

**Required:** Preserve tattoo locations and lean build, soften anatomy planes, extend sleep trousers and remove non-character marks in new delivery.

#### A236 — rei-streetwear-sukajan.png

[Original file](../../assets/portraits/rei-streetwear-sukajan.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Green/cream sukajan has bird embroidery and satin reflections; face and lower framing remain old master.

**Required:** Retain embroidery, material contrast and visible neck ink, apply master and extend trousers.

#### A237 — rei-streetwear-techwear.png

[Original file](../../assets/portraits/rei-streetwear-techwear.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Black techwear has straps, chains and layered pockets; figure remains short despite ample garment detail.

**Required:** Keep gear arrangement and lean silhouette, refine face and extend legs without clipping hanging accessories.

#### A238 — rei-tailored-waistcoat.png

[Original file](../../assets/portraits/rei-tailored-waistcoat.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Waistcoat, white shirt and watch/chain read clearly; face and short lower crop remain stylised.

**Required:** Preserve shirt opening and visible tattoos, apply master and complete trouser thighs with coherent waistband.

#### A239 — ren-aoki-selection.png

[Original file](../../assets/portraits/ren-aoki-selection.png) · 1024 × 1536 · contains transparency · **Polish + framing**.

**Observed:** Ren has short black hair, glasses and navy workwear; long pose but stiff graphic facial construction.

**Required:** Preserve glasses and individual features, model face/neck and standardise complete hands and thigh endpoint.

#### A240 — rina-vale-selection.png

[Original file](../../assets/portraits/rina-vale-selection.png) · 1086 × 1448 · contains transparency · **Restyle + reframe**.

**Observed:** Rina has black/copper bob, paint-marked overalls and a confident face; close crop omits lower body.

**Required:** Retain hairstyle, complexion and paint marks; refine facial depth and construct full arms/pelvis/legs with practical stance.

### Review sheet 21

[Open labelled complete-canvas sheet](review-21.jpg).

#### A241 — robin-vale-selection.png

[Original file](../../assets/portraits/robin-vale-selection.png) · 1117 × 1408 · contains transparency · **Restyle + reframe**.

**Observed:** Robin has swept brown hair, waistcoat and name badge; hip crop and smooth simplified face remain.

**Required:** Preserve adult identity, vest and service styling, model face and continue trousers with complete visible hands.

#### A242 — rosa-selection.png

[Original file](../../assets/portraits/rosa-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Rosa has auburn curls, olive shirt and rust waist wrap; graphic grin and exaggerated facial shorthand stand out.

**Required:** Retain warm complexion, curvy build and lively expression, model smile/cheeks naturally and extend lower garment through thighs.

#### A243 — samantha-beach-black-bikini.png

[Original file](../../assets/portraits/samantha-beach-black-bikini.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Samantha black swim set shows detailed tattoos and strongly defined torso; stylised eyes/chin and high leg crop persist.

**Required:** Use athletic adult master, preserve exact tattoo map and swimwear cut; soften face/muscle planes and extend thighs.

#### A244 — samantha-beach-red-bikini.png

[Original file](../../assets/portraits/samantha-beach-red-bikini.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Red bikini retains dense tattoos and high crop; face is narrow and eyes heavily stylised.

**Required:** Keep red set and muscular build, refine facial planes and extend leg coverage without altering body proportions.

#### A245 — samantha-beach-teal-bikini.png

[Original file](../../assets/portraits/samantha-beach-teal-bikini.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Teal bikini preserves ink and athletic shape; short lower crop and repeated face remain.

**Required:** Retain teal colour and tattoo placement, apply master and extend thighs with natural hip/abdominal shading.

#### A246 — samantha-black-mockneck.png

[Original file](../../assets/portraits/samantha-black-mockneck.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Black sleeveless mockneck shows arm tattoos and waist/hip crop; face repeats older styling.

**Required:** Keep collar and tattoo occlusion, refine face and extend trousers while retaining complete hand-on-hip anatomy.

#### A247 — samantha-charcoal-hoodie.png

[Original file](../../assets/portraits/samantha-charcoal-hoodie.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Charcoal hoodie and burgundy top give convincing fabric; body ends at upper legs.

**Required:** Retain hoodie volume and visible ink, apply Samantha master and extend trousers without reducing athletic build.

#### A248 — samantha-denim-cargo.png

[Original file](../../assets/portraits/samantha-denim-cargo.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Denim vest, white top and cargo trousers are distinct; hand placement and lower crop remain short.

**Required:** Keep cargo/denim construction and exact visible tattoos, refine face and complete mid-thigh coverage.

#### A249 — samantha-formal-black-suit.png

[Original file](../../assets/portraits/samantha-formal-black-suit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Black formal suit and burgundy blouse have rich material detail; stylised face and thigh cutoff need alignment.

**Required:** Preserve tailoring and tattoos where visible, use master face and extend trousers with intact hands.

#### A250 — samantha-formal-burgundy-dress.png

[Original file](../../assets/portraits/samantha-formal-burgundy-dress.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy dress and tattoos are sharply rendered; short lower skirt and narrow stylised face persist.

**Required:** Keep dress shape and athletic body, add facial volume and continue skirt over pelvis/thighs.

#### A251 — samantha-gym-charcoal.png

[Original file](../../assets/portraits/samantha-gym-charcoal.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Charcoal sports set exposes tattooed arms and segmented abdomen; composition ends high on legs.

**Required:** Preserve athletic strength and ink, soften anatomy planes and extend leggings to standard crop.

#### A252 — samantha-gym-olive.png

[Original file](../../assets/portraits/samantha-gym-olive.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Olive top and black shorts retain muscle/ink detail but high leg crop and stylised face remain.

**Required:** Keep outfit and tattoo map, apply mature face master and show thighs below shorts.

### Review sheet 22

[Open labelled complete-canvas sheet](review-22.jpg).

#### A253 — samantha-olive-bomber.png

[Original file](../../assets/portraits/samantha-olive-bomber.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Olive bomber and dark jeans retain visible ink; facial construction and hip crop remain old style.

**Required:** Keep jacket volume and rolled sleeve exposure, refine face and extend jeans to mid-thigh.

#### A254 — samantha-red-flannel.png

[Original file](../../assets/portraits/samantha-red-flannel.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Red flannel has readable checks and rolled sleeves; lower body short and face unchanged.

**Required:** Preserve pattern scale, visible tattoos and muscular build, refine face and complete trouser thighs.

#### A255 — samantha-red-moto.png

[Original file](../../assets/portraits/samantha-red-moto.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Red leather jacket has rich highlights; facial planes and high lower crop lag behind garment detail.

**Required:** Keep leather/collar details and tattoo occlusion, refine face and extend trousers without changing jacket proportions.

#### A256 — samantha-selection.png

[Original file](../../assets/portraits/samantha-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Samantha's signature cropped hair, tattoos and sleeveless leather identify her; narrow chin/eyes and short body need change.

**Required:** Build strong athletic adult master, preserve all tattoo placements and grounded expression; model face and complete mid-thigh stance.

#### A257 — samantha-sleep.png

[Original file](../../assets/portraits/samantha-sleep.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy lace sleepwear repeats tattoos, stylised face and high leg crop; small corner mark visible.

**Required:** Retain adult identity and existing coverage, refine face/body, extend thighs and inspect/remove non-character mark.

#### A258 — samir-dutta-selection.png

[Original file](../../assets/portraits/samir-dutta-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Samir has dark curls, beard and navy jacket over rust shirt; half-body crop and flat face need change.

**Required:** Preserve mature warmth and complexion, model beard/cheeks and construct full arms/hands/trousers to mid-thigh.

#### A259 — sasha-quinn-selection.png

[Original file](../../assets/portraits/sasha-quinn-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Sasha has red asymmetric hair, glasses and burgundy work shirt; graphic shadows and torso cutoff dominate.

**Required:** Keep hairstyle, frames, expression and pocket tools; refine facial planes and build full practical pose.

#### A260 — sophie-autumn-knit.png

[Original file](../../assets/portraits/sophie-autumn-knit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Sophie autumn knit has fine texture and familiar ponytail; large eyes/small nose and short lower body remain.

**Required:** Use athletic adult Sophie master, retain rust knit and green eyes, extend jeans with natural hip stance.

#### A261 — sophie-beach-cobalt.png

[Original file](../../assets/portraits/sophie-beach-cobalt.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Cobalt swimwear retains athletic torso and hand-on-hip pose; oversized eyes and high leg crop remain.

**Required:** Preserve runner build and coverage, refine face and extend both thighs without exaggerating waist/hips.

#### A262 — sophie-beach-coral.png

[Original file](../../assets/portraits/sophie-beach-coral.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Coral swim set repeats large green eyes and very smooth facial planes with upper-leg crop.

**Required:** Keep colour and sporty adult identity, apply master and extend thighs with natural muscle shading.

#### A263 — sophie-beach-tropical.png

[Original file](../../assets/portraits/sophie-beach-tropical.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Tropical swim set has clear print and ponytail; lower crop short, face stylised.

**Required:** Preserve print, hair tie and athletic build, refine facial planes and continue legs to mid-thigh.

#### A264 — sophie-casual-denim.png

[Original file](../../assets/portraits/sophie-casual-denim.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Denim jacket and black trousers have convincing texture; face and short crop remain older style.

**Required:** Keep denim seams and relaxed hip pose, apply master and extend trousers without stretching jacket.

### Review sheet 23

[Open labelled complete-canvas sheet](review-23.jpg).

#### A265 — sophie-casual-varsity.png

[Original file](../../assets/portraits/sophie-casual-varsity.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy/cream varsity outfit gives useful sporty identity; face and thigh coverage remain short/stylised.

**Required:** Preserve trim and ponytail, model eyes/nose/lips naturally and continue jeans to standard crop.

#### A266 — sophie-formal-emerald.png

[Original file](../../assets/portraits/sophie-formal-emerald.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Emerald one-shoulder dress is richly rendered; face and short skirt remain stylised.

**Required:** Retain athletic shoulders and elegant drape, refine facial depth and extend skirt over pelvis/thighs.

#### A267 — sophie-formal-suit.png

[Original file](../../assets/portraits/sophie-formal-suit.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Navy suit and light blouse preserve athletic body; short trousers in frame and idealised face persist.

**Required:** Keep tailoring and hand-on-hip anatomy, use master face and extend trousers.

#### A268 — sophie-gym-cardio.png

[Original file](../../assets/portraits/sophie-gym-cardio.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Blue cardio top and black running shorts show athletic proportions but stop immediately below shorts.

**Required:** Keep runner build and outfit, refine face and show sufficient thigh length below hems.

#### A269 — sophie-gym-strength.png

[Original file](../../assets/portraits/sophie-gym-strength.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Plum strength set shows segmented abdomen and stylised face; lower frame ends high.

**Required:** Retain athletic build, soften muscle/skin planes and extend leggings through mid-thigh.

#### A270 — sophie-high-school.png

[Original file](../../assets/portraits/sophie-high-school.png) · 1145 × 1374 · contains transparency · **Historical update**.

**Observed:** School Sophie holds relay baton and backpack in green sportswear; smile/eyes are cartoon-like and crop short.

**Required:** Keep historical age, practical coverage and sports props, refine age-appropriate face/hands and extend uniform trousers.

#### A271 — sophie-picnic-dress.png

[Original file](../../assets/portraits/sophie-picnic-dress.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Yellow floral dress keeps ponytail and relaxed hip pose; face and skirt coverage remain short.

**Required:** Preserve print and athletic adult shape, model face and continue skirt to mid-thigh.

#### A272 — sophie-selection.png

[Original file](../../assets/portraits/sophie-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Sophie signature green tracksuit, ponytail and green eyes are distinct; large eyes and small pointed face read stylised.

**Required:** Build runner's adult master with lively expression, natural facial planes and complete mid-thigh tracksuit composition.

#### A273 — sophie-sleep.png

[Original file](../../assets/portraits/sophie-sleep.png) · 1280 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Blue lace sleepwear retains ponytail and stylised face; high leg crop and corner mark visible.

**Required:** Preserve adult identity and existing sleepwear coverage, extend thighs and inspect/remove corner artefact with clean lace edges.

#### A274 — sophie-summer-linen.png

[Original file](../../assets/portraits/sophie-summer-linen.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Light tied shirt and olive shorts have fine cloth texture; lower-body crop remains short.

**Required:** Keep summer outfit, belt and athletic body, apply master face and extend thighs beyond short hems.

#### A275 — sophie-winter-puffer.png

[Original file](../../assets/portraits/sophie-winter-puffer.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Light puffer and green knit show useful material contrast; stylised face and high crop remain.

**Required:** Keep puffer volume and ponytail, refine face and extend dark trousers with consistent stature.

#### A276 — sylvanis-selection.png

[Original file](../../assets/portraits/sylvanis-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Sylvanis has long black hair, pointed ears and white/open collar; face is narrow, sharp and idealised.

**Required:** Preserve elven anatomy and tall slim identity, model nose/lips/neck, extend thighs and keep jewellery/tattoo visibility consistent.

### Review sheet 24

[Open labelled complete-canvas sheet](review-24.jpg).

#### A277 — sylvanis-syndicate.png

[Original file](../../assets/portraits/sylvanis-syndicate.png) · 1216 × 1293 · contains transparency · **Restyle + reframe**.

**Observed:** Sylvanis's ornate masked uniform uses violet/teal accents and layered cloak; half-body framing.

**Required:** Keep sealed mask, symbols, dark layers and concealed identity, extend robe/body to mid-thigh with coherent material depth.

#### A278 — takeo-selection.png

[Original file](../../assets/portraits/takeo-selection.png) · 1086 × 1448 · contains transparency · **Polish + framing**.

**Observed:** Takeo has enormous muscular frame, buzzcut and moustache/goatee; face/neck and shirt shadows are very angular.

**Required:** Preserve canonical exceptional size and dark camouflage, soften planes without slimming; extend to clear mid-thigh and inspect full hands.

#### A279 — tess-morgan-selection.png

[Original file](../../assets/portraits/tess-morgan-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Tess has auburn bob/fringe, freckles and black/burgundy layers; big eyes and torso crop are conspicuous.

**Required:** Retain adult face and freckles, model nose/cheeks and build full arms/lower body without erasing friendly character.

#### A280 — theo-selection.png

[Original file](../../assets/portraits/theo-selection.png) · 1122 × 1402 · contains transparency · **Restyle + reframe**.

**Observed:** Theo has red waves, glasses, brown jacket and held book; simplified face and short lower frame remain.

**Required:** Preserve book, glasses and soft expression, add facial depth, check book grip and extend trousers.

#### A281 — thirteen-selection.png

[Original file](../../assets/portraits/thirteen-selection.png) · 1129 × 1393 · contains transparency · **Restyle + reframe**.

**Observed:** Thirteen's buzzcut, broad neck and severe face are distinctive; heavy shadow wedges and torso/hip crop feel graphic.

**Required:** Preserve canonical identity and build, model facial/neck planes, extend suit/trousers and avoid generic idol replacement.

#### A282 — town-residents-preview.png

[Original file](../../assets/portraits/town-residents-preview.png) · 774 × 684 · fully opaque · **Reference / archive / derivative**.

**Observed:** Opaque town-resident preview is a labelled contact sheet, not a single portrait.

**Required:** Preserve baseline evidence; generate a separately named post-update comparison after replacements, never route this preview as character art.

#### A283 — tyler-selection.png

[Original file](../../assets/portraits/tyler-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Tyler has locs, moustache, wraps and dark hoodie; broad grin and graphic skin/folds remain.

**Required:** Preserve complexion and lively adult identity, refine mouth/face, show complete wrapped hands and trouser thighs.

#### A284 — valentina-selection.png

[Original file](../../assets/portraits/valentina-selection.png) · 1145 × 1374 · contains transparency · **Restyle + reframe**.

**Observed:** Valentina has silver waves, green top and navy vest; large eyes and sharp chin with short crop.

**Required:** Preserve individual silver hair and lively expression, model natural face planes and extend lower body to mid-thigh.

#### A285 — wren-park-selection.png

[Original file](../../assets/portraits/wren-park-selection.png) · 1199 × 1312 · contains transparency · **Restyle + reframe**.

**Observed:** Wren has purple-streaked dark hair and hoodie; very large eyes, graphic grin and bust crop are strong mismatches.

**Required:** Retain adult identity and coloured streak, refine nose/mouth/eye scale and construct full relaxed arms/pelvis/legs.

#### A286 — yuriko-bikini-floral.png

[Original file](../../assets/portraits/yuriko-bikini-floral.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Yuriko floral bikini already shows long legs/complete hands relative to most sets; face remains large-eyed and tiny-nosed.

**Required:** Keep petite adult build, amber clip and floral set; refine facial planes and standardise true mid-thigh endpoint.

#### A287 — yuriko-bikini-navy.png

[Original file](../../assets/portraits/yuriko-bikini-navy.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Navy swim separates have complete hands and longer body coverage; stylised face persists.

**Required:** Preserve outfit coverage, petite adult shape and clip; apply Yuriko master and check proportion/leg endpoint.

#### A288 — yuriko-bikini-teal.png

[Original file](../../assets/portraits/yuriko-bikini-teal.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Teal sports-style swim set retains full arms and useful thigh framing; face is simplified.

**Required:** Keep practical cut and small stature, refine eyes/nose/lips and align thigh coverage with master.

### Review sheet 25

[Open labelled complete-canvas sheet](review-25.jpg).

#### A289 — yuriko-campus-cardigan.png

[Original file](../../assets/portraits/yuriko-campus-cardigan.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Mustard cardigan and jeans have long composition and intact hands; face remains anime-like.

**Required:** Preserve cheerful adult identity and clip, add facial volume and maintain complete hand/thigh margins.

#### A290 — yuriko-evening-dress.png

[Original file](../../assets/portraits/yuriko-evening-dress.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Burgundy satin dress has convincing drape and longer framing; very small nose and pointed chin remain.

**Required:** Keep petite body, satin and hair clip; refine face and confirm dress crop reaches mid-thigh.

#### A291 — yuriko-festival-yukata.png

[Original file](../../assets/portraits/yuriko-festival-yukata.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Navy floral yukata and gold obi have readable construction and full arms; face remains stylised.

**Required:** Preserve wrap/obi/pattern and adult stature, apply master face and confirm lower garment endpoint.

#### A292 — yuriko-gym-lavender.png

[Original file](../../assets/portraits/yuriko-gym-lavender.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Lavender gym layers and purple shorts have complete hands and visible thighs; face is still simplified.

**Required:** Keep outfit and petite adult proportions, refine facial planes and align thigh extent without torso stretching.

#### A293 — yuriko-gym-sage.png

[Original file](../../assets/portraits/yuriko-gym-sage.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Sage sports top and charcoal leggings have long framing; facial shorthand is primary mismatch.

**Required:** Retain subtle physique and adult identity, apply master and check hip/leg construction with intact hands.

#### A294 — yuriko-home.png

[Original file](../../assets/portraits/yuriko-home.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Home sweatshirt and joggers have soft texture but hip-level crop and large-eyed face.

**Required:** Keep cosy clothing volume and amber clip, model face and extend lower body to match longer Yuriko variants.

#### A295 — yuriko-selection.png

[Original file](../../assets/portraits/yuriko-selection.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Yuriko signature bob, amber clip, olive shirt and pens identify her; large eyes/tiny nose and shorter lower body read cartoon-like.

**Required:** Build a petite adult master with expressive but natural facial planes; preserve work cues and extend hands/pelvis/thighs.

#### A296 — yuriko-street-denim.png

[Original file](../../assets/portraits/yuriko-street-denim.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Denim jacket and dark skirt have complete arms and longer coverage; face retains stylised proportions.

**Required:** Keep denim/pleat details and adult build, refine face and align skirt/thigh endpoint to master.

#### A297 — yuriko-study-knit.png

[Original file](../../assets/portraits/yuriko-study-knit.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Study knit and round glasses are readable with full hands; tiny facial features remain.

**Required:** Preserve optional glasses and amber clip, model face through lenses and keep consistent body proportions/coverage.

#### A298 — yuriko-summer-dress.png

[Original file](../../assets/portraits/yuriko-summer-dress.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Green summer dress has fine floral print and long figure; face remains simplified.

**Required:** Retain print, petite adult anatomy and clip, refine face and keep lower edge at mid-thigh with clear hand margins.

#### A299 — yuriko-theatre-overalls.png

[Original file](../../assets/portraits/yuriko-theatre-overalls.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Theatre overalls have paint details and full hands; face is anime-like but framing is relatively close.

**Required:** Preserve workwear/tools/paint and adult identity, refine face and confirm thigh extent with no clipped fingers.

#### A300 — yuriko-winter-coat.png

[Original file](../../assets/portraits/yuriko-winter-coat.png) · 1024 × 1536 · contains transparency · **Restyle + reframe**.

**Observed:** Winter duffle coat and plaid scarf retain full hands and long figure; large eyes/tiny nose remain.

**Required:** Keep coat toggles, scarf volume and small adult stature, refine facial planes and standardise lower-body endpoint.

### Review sheet 26

[Open labelled complete-canvas sheet](review-26.jpg).

#### A301 — assets/profiles/charles-v2.png

[Original file](../../assets/profiles/charles-v2.png) · 1024 × 1536 · contains transparency · **Reference / archive / derivative**.

**Observed:** Transparent Charles profile v2 visually matches the active scene version and carries the same short thigh crop.

**Required:** Treat as a linked derivative/reference, verify actual avatar consumer before synchronising; preserve old source and avoid leaving contradictory faces.

#### A302 — assets/profiles/crow.png

[Original file](../../assets/profiles/crow.png) · 1199 × 1312 · contains transparency · **Reference / archive / derivative**.

**Observed:** Transparent Crow profile repeats the masked short-body design in a profile location.

**Required:** Preserve avatar framing function and full concealment; derive any future avatar from accepted Crow master without forcing a tiny mid-thigh phone face.

#### A303 — assets/grove/garrett/appearance-reference.png

[Original file](../../assets/grove/garrett/appearance-reference.png) · 1280 × 1536 · contains transparency · **Reference / archive / derivative**.

**Observed:** Garrett appearance reference is a tattooed shirtless adult with strongly segmented anatomy and short crop.

**Required:** Preserve source as tattoo/identity evidence; create a versioned updated reference from accepted master, retaining exact ink placement rather than overwriting history.

#### A304 — assets/grove/garrett/arm-tattoo-reference.png

[Original file](../../assets/grove/garrett/arm-tattoo-reference.png) · 1280 × 1536 · contains transparency · **Reference / archive / derivative**.

**Observed:** Garrett arm-tattoo reference uses white tank and detailed sleeve ink with hip crop.

**Required:** Preserve tattoo authority and laterality; make any updated reference separately and check all new outfits against this map.

#### A305 — assets/grove/rei/appearance-reference.png

[Original file](../../assets/grove/rei/appearance-reference.png) · 1280 × 1536 · contains transparency · **Reference / archive / derivative**.

**Observed:** Rei appearance reference shows shirtless adult ink map, lean musculature and short crop.

**Required:** Retain as immutable identity/ink evidence; create separate updated master reference after accepted face/body work, keeping tattoo placement exact.

#### A306 — assets/grove/rei/tattoo-reference.png

[Original file](../../assets/grove/rei/tattoo-reference.png) · 1280 × 1536 · contains transparency · **Reference / archive / derivative**.

**Observed:** Rei tattoo reference visually repeats the shirtless ink map and short composition.

**Required:** Preserve source and verify duplicate linkage; use to check new variants, with separately versioned updated reference instead of altering historical evidence.
