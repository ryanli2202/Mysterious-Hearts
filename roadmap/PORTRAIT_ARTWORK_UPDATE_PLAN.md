# MH-013 — Semi-realistic manhwa portrait artwork update

**Status:** In progress; Batch 1 released 2026-11-10. **Recorded:** 2026-11-10 (Australia/Brisbane). **Full-update release/version/date:** unassigned.

The requested outcome is one coherent collection of transparent character portraits: semi-realistic manhwa rendering led by Ivan and Charles, with head-to-mid-thigh composition instead of the current mixture of busts, waist-up and hip crops. [Batch 1](artwork-batch-01/README.md) now installs the eight-portrait representative pilot and source-specific height fitting. The rest of this document remains the production contract for later batches.

## Plugin task assignments

**Assigned:** 2026-11-11. Remaining artwork/integration only. Preserve released masters and the staged, not live-installed, Stage 3 wardrobes.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Stage 4: historical, masked, combat and guard briefs | Story Skills for character/era continuity; Writer's Loop for substantial appearance revisions | Check age/tattoo differences, masked identities, equipment and power descriptions against source sheets; preserve the current manhwa art direction. |
| Stages 3–5: cutout preparation and edge corrections where required | Bulk BG Remove | Run the memory planner, preserve originals and inspect hair/clothing/gear on dark backgrounds; do not flatten existing alpha or replace an accepted cutout merely because a tool is installed. |
| Stage 5: required format/export preparation | prompt-to-asset only for supported local validation/export tasks | Keep portrait aspect, head-to-mid-thigh crop and source-specific height metadata. The restricted SVG tool is not a raster portrait generator; retain the established portrait pipeline where unsupported. |
| Stages 5–6: resolver, wardrobe, historical and combat integration | falsegreen-skill | Review real loader/path, saved-choice, occasion, stature and historical-fallback regressions; run portrait/guard/wardrobe checks and dark-phone smoke, then inspect normal/compact game screens before installation/release. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Deliverables and evidence

- [Firm production art direction](../assets/portraits/ARTSTYLE.md), replacing the former anime/hip-up instruction.
- [Individual portrait audit](artwork-portrait-audit/PORTRAIT_AUDIT.md): findings, identity features to retain, changes and disposition for every inventoried file.
- [Baseline inventory](artwork-portrait-audit/inventory.json): 306 files with dimensions, alpha statistics, bounding boxes and SHA-256 hashes; 300 files under `assets/portraits`, two transparent profile images and four transparent appearance/tattoo references.
- 26 labelled complete-canvas contact sheets, [anchor alpha comparison](artwork-portrait-audit/anchor-alpha-review.jpg) and [face comparison](artwork-portrait-audit/face-comparison.jpg). These are inspection composites of existing files, not proposed replacement artwork.

All 306 files were visually reviewed on labelled slate sheets. Ivan's current selection image and Charles's active v2 image were additionally opened individually and compared over slate and neutral grey. Twelve face crops were compared. This is an art-direction/composition audit, not pixel-by-pixel approval of every source. Full-resolution edge, finger, insignia, tattoo and in-game acceptance remains required during production.

## Scope and boundaries

Include all 295 alpha-bearing PNGs in `assets/portraits`: selection/default portraits, civilian outfits, sleep/home/beach/gym/formal variants, historical scenes, seven masked leadership uniforms, 24 combat portraits and 19 guard/boss role portraits. Reconcile the two related alpha profile files and four appearance/tattoo reference files without losing their source-reference purpose. Alpha presence alone does not prove a clean cutout.

Five portrait-directory files are fully opaque: `charles-selection.png`, `fox-contact.png`, `gordon-contact.png`, `neo-selection.png`, and `town-residents-preview.png`. These are individually reviewed and classified as source/reference, contact/scenic or preview assets, not failed transparent deliveries. Charles's supplied original remains unchanged. Neo's actual scene portrait is `neo-scene.png`; Charles's active scene portrait is `charles-selection-v2.png`.

Grove photographs, gallery illustrations, wallpapers, ordinary opaque phone avatars, animation sprite sheets, chibi/side-view gameplay sprites and raw generated-image archives are separate asset classes. Do not convert those compositions to mid-thigh portraits. Existing player-owned custom portraits are preserved; the direction applies to future project-authored portraits, not automatic rewrites of imports. Runtime fallback and creator-preview checks still include custom characters.

## Direction decisions

1. **Style anchors:** `ivan-selection.png` and `charles-selection-v2.png`. Use their dimensional nose/eyelid/lip construction, selective contours, believable neck/shoulder anatomy and controlled material shading. Preserve illustrated manhwa. Their faces, physiques, skin colours and clothing are not templates for other people.
2. **Framing:** complete head through **mid-thigh**, with visible pelvis and meaningful thigh length below the crotch. This is body coverage, independent of camera angle. No breast-, waist- or waistband-level cutoff; no missing anatomy hidden behind a crop, aura or extended empty canvas. Charles is closer to the desired coverage, but neither anchor is automatically exempt from reframing.
3. **Identity:** retain each character's age, complexion, facial structure, stature, build, hair texture, scars, glasses, jewellery, tattoos and fantasy anatomy. Older residents retain age; smaller adults retain adult proportions; elves retain ears; robots retain mechanical bodies. Do not turn every resident into the same young idol face.
4. **Rendering:** soften transitions between facial planes while retaining deliberate shadow shapes. Avoid oversized eyes, shorthand noses, triangular chins, outlined tooth bars and flat poster-like skin. Many outfit sets already have detailed clothing; prioritise facial construction and composition before more fabric texture.
5. **Context:** preserve outfits, privacy masks, historical differences, weapons and power identities. Civilian portraits remain free of combat effects. Combat uses the same person and costume with deliberate stance and subordinate effects.
6. **Transparency:** genuine RGBA cutouts with clear spaces around and within the silhouette. No baked scenery, checkerboard, watermark, signature, ambient rectangle or ground shadow. Pale clothes remain content; they do not justify light UI surfaces.

## Production sequence

| Stage | Required work | Exit condition |
| --- | --- | --- |
| 0 — Baseline and direction | Preserve hashes, review every file, replace conflicting guide, map special routing and record planning status. | Completed in this planning pass; visual production remains pending. |
| 1 — Representative pilot | Reframe Ivan and Charles; produce Emily, Minsu, Priya Shah and Otis Bell; include one masked guard and one combat derivative. | Completed and installed in Batch 1: Clubs guard and combat Ivan; review, corrections and rendered evidence linked above. |
| 2 — Character masters | 107 accepted masters: 89 characters and 18 guard roles, seven carried forward from the pilot. Installed with a full height audit on 2026-11-11; Richter's cybernetic form remains a Stage 4 variant. [Roster and evidence](artwork-stage-02/height-review/README.md). | Completed for default masters: identity sheets, source hashes, all-character stature checks and normal/compact game review. |
| 3 — Wardrobes | Completed production: [146 staged variants across ten characters](artwork-stage-03/README.md), with immutable originals, exact generation provenance and hash-bound per-outfit review. Live installation remains pending. | All sets reviewed against installed masters; corrected heights and mid-thigh picture crop preserved. Normal/compact loader, scene and dark-phone presentation verified. |
| 4 — Historical, masked and combat | Produce age-appropriate historical variants, masked uniforms, 24 combat portraits and remaining guard refinements. | Age/tattoo differences, concealed identities and combat powers preserved; anatomy complete. |
| 5 — Integration | Default-master integration completed early for the requested Stage 2 in-game height fix. Stage 3 wardrobes pass staged real-loader, height, saved-choice and occasion-routing checks; their live installation is pending. Apply the same verification to later context assets. | Default-master and staged-wardrobe evidence recorded; complete collection remains pending. |
| 6 — Release | Reconcile appearance wording; record before/after evidence, actual counts and limits; publish a separate Release record. | Roadmap Released only after implementation and verification. |

The pilot is a production quality gate, not an assumed user approval or a reason to ask permission again during authorised implementation. Do not mass-produce variants before their master passes. No completion date, generation cost or generation count is promised; revision demand is unknown.

## Runtime integration contract

| Consumer / dependency | Observed behaviour and required protection |
| --- | --- |
| `game.py:Game.portrait` | Resolves NPC name slugs, home/sleep/occasion outfits, player wardrobe, headquarters uniforms, guards and historical overrides. Preserve names and precedence. Explicitly selects Charles v2 and Neo scene art. |
| `game.py` height handling | Superseded the four-character/pilot whitelist with `assets/portraits/stature.json`, `character_stature.py` and `portrait_framing.py`. All 107 masters use 29 unchanged original authored heights, seven explicit user heights and 71 stable varied defaults within 175–180 cm male / 160–165 cm female. [Current roster](artwork-stage-02/height-variation/HEIGHTS.md). Group members share pixels/cm independent of slot width; alpha padding is excluded and uniform resizing preserves proportions. The visible head-to-mid-thigh span is modelled as 70% of full stature, not a complete standing body; the bottom is a picture crop, not feet. Later wardrobe/context art must retain these rules and achieve consistent anatomical coverage. |
| `start_ui.py`, `character_dossier.py`, `playable_cast.py` | Selection/dossier paths can differ from scene paths. Verify actual loaded images, versioned files, Neo, compact picker and custom entries. |
| `hangout_ui.py`, `artwork.py` | In-person and multi-person layouts must display lower-body coverage without clipped heads/hands or unreadably small faces. Bottom anchoring should meet the scene/dock rather than float visibly above it. |
| `combat_portraits.py`, `combat_rpg_ui.py` | Whitelisted combat art uses whole-image thumbnailing; aura bounds affect apparent size. Fit bodies consistently across effect extents, preserve fallback and UI readability. |
| `guard_portraits.py`, `organisation_guards.py` | Keep 19 role IDs, post encounters, old saved-slot fallback and Richter's context-sensitive boss form. Do not expose cybernetic Richter in reception/contact views. |
| `four_aces.py`, `camera.py`, `contact_profiles.py` | Preserve masked operational art and saved civilian choice. Stage candidates outside live portrait discovery. Audit alias/reference selection before retiring versioned files. |
| `campaign_flashbacks.py`, `flashback_visits.py` | Historical art overrides current wardrobe in the relevant scene. Do not copy adult tattoos, jewellery or mature bodies into earlier scenes without source support. |
| Appearance documents / prompt manifests | Existing prompts are historical provenance, not current directions. Preserve them; create an MH-013 manifest. Correct crop-dependent prose only when actual replacements are installed. |

Preserve in-person activity routing. Phone pages stay dark using `winterfield_ui.py`, `phone_theme.py` and embedded `phone_dialogs`; diagnostic art-review backgrounds are not game UI. Runtime/UI changes are conditional integration work, not implemented by this plan.

## Acceptance gates

Every asset needs a path, old/new hash, character/context, identity and style references, crop description, actual alpha inspection and review findings. Link before/after composites and record exceptions explicitly.

- **Identity:** face, age, skin tone, build, hair, markings and costume agree with source canon and the accepted character master. Style cannot compensate for identity drift.
- **Style:** matches Ivan/Charles rendering at full size and actual scene/selection sizes. Retains distinct faces and bodies; fabric detail alone is not a pass.
- **Coverage:** head-to-mid-thigh, full hairstyle and shoulders, complete visible hands and required items. No cut elbows/fingers. Pocketed hands are allowed when natural, not cropped away to evade review.
- **Anatomy:** correct limb connections, joints, hands, weight distribution, clothes and props; consistent proportions through variants.
- **Technical:** 2:3 RGBA master, target 1024x1536 or higher at that ratio, safe margins and genuine clear background. Never stretch old art into compliance. Antialiasing is allowed; near-opaque alpha values alone are not defects.
- **Context:** opaque privacy masks, correct historical age, existing powers/weapons and MH-010/MH-011 designs. No unsolicited costume or lore redesign.
- **Presentation:** readable normal/compact selection, one-on-one/group scenes, historical scenes, wardrobe previews and combat. Auras cannot shrink bodies disproportionately. Phone previews retain every dark control state.

All gates are mandatory; no weighted average excuses a wrong identity, missing body or broken alpha. Audit categories estimate work, not final acceptance.

## Verification plan and current evidence

**Performed:** metadata/alpha/hash inventory; all 26 sheet reviews; individual anchors and two-background comparison; twelve face crops; portrait, wardrobe, historical, selection, combat and guard route inspection. Documentation and patch-note checks are recorded in [verification](artwork-portrait-audit/VERIFICATION.md).

**Batch 1 implementation:** eight installed replacements, original backups, prompt/input manifest, alpha/before-after review, known-height fitting and actual unit/rendered check results are recorded in [Batch 1 evidence](artwork-batch-01/README.md). That record includes failures outside this patch and framing tolerances. The following checklist continues to apply to later batches.

**Pending after implementation:** image decode/alpha/changed-file coverage; unit suites `test_combat_portraits.py`, `test_guard_portraits.py`, `test_character_selection.py`, `test_campaign_flashbacks.py`, `test_flashback_visits.py`, `test_syndicate_cast.py`, plus relevant wardrobe/appearance checks. Run affected existing smokes: `character_selection_ui_smoke.py`, `start_ui_smoke.py`, `town_portraits_smoke.py`, `combat_portraits_ui_smoke.py`, `guard_portraits_ui_smoke.py`, `syndicate_uniform_smoke.py`, `syndicate_guard_encounters_smoke.py`, `campaign_flashbacks_ui_smoke.py`, `flashback_visits_ui_smoke.py`. Add coverage only for actual uncovered integration behaviour. If phone surfaces change, run `tests/phone_dark_theme_smoke.py`, relevant feature smokes and inspect interactive states.

The original planning pass did not run gameplay/phone smokes. At release run patch-note validation, its unit suite and export, plus reader/start-screen smokes when UI changes occur.

**Stage 3 production, 2026-11-11:** All 146 wardrobes pass visual, format, alpha, margin and provenance review. Staged real-loader verification covers all paths at two thumbnail sizes, normal/compact solo and group scenes, and three dark-phone correction previews (20 inspected screenshots). All 306 live baseline files and the height table are unchanged; 292 height comparisons, 62 saved wardrobe round trips and 26 automatic routes pass. Dark-phone, lifestyle and start smokes pass; 70/71 related unit tests pass with the existing Theo camera fixture failure. [Stage 3 delivery](artwork-stage-03/README.md) records exact checks, publication results and limitations. Candidates remain staged for later installation; historical, masked, combat and remaining guard production stays pending.

## Access, saves and release record

After implementation the refreshed art appears through existing character selection, in-person conversations/hangouts, wardrobes, historical scenes and combat. Existing unlocks, restrictions and masked-uniform locations remain. No new portrait-unlock activity is planned.

Planning had no save impact. Batch 1 preserves paths, IDs and save fields; restart to load assets and the pilot fitting code. Rendered restored guard saves, historical precedence, wardrobe choices and custom fallback are covered by the Batch 1 evidence. Do not alter stored relationships, outfits, powers, histories or user-created portraits to accommodate art.

The original planning work remains a **Development report** in `patch_notes/catalog.json`; the schema has no Planned release type. [Read the exported planning record](artwork-portrait-audit/PLANNING_RECORD.md). Separate Release `release-2026-11-10-artwork-batch-01` records only the eight installed pilot assets, fitting, access, saves and actual checks. Later production stages remain pending.
