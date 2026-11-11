# Interiors — ten image-generation batches

**Status:** Generation paused at the user's request on 2026-11-11. Batches 01 and 02 artwork remain complete, with 89 generated and statically accepted images. Batch 03 is **unfinished** and paused after four generated images (one accepted, three staged); its remaining 47 and all batches 04–10 are not started. Runtime integration and release are pending. Production records: [batch 01](interiors-generation-batches/interiors-01-production/PRODUCTION_REVIEW.md), [batch 02](interiors-generation-batches/interiors-02-production/PRODUCTION_REVIEW.md), [batch 03](interiors-generation-batches/interiors-03-production/PRODUCTION_REVIEW.md).

The current [image inventory](INTERIORS_IMAGE_INVENTORY.md) requires **438 new images**: **421 interior views** and **17 outdoor views**. They are assigned exactly once across ten batches. Whole buildings stay together; counts vary to preserve visual continuity and coherent review scope.

Excluded from generation: **90 reuse candidates** (87 interior and 3 outdoor) and **2 unresolved dorm bathrooms**. Reuse still needs final full-size/in-game approval. A rejected candidate or resolved new bathroom requires an explicit inventory/batch revision, not an untracked extra image.

**Full-size review finding:** Garrett’s existing image is an exterior estate view, so its indoor living-room reuse is rejected. It was used only for architectural/material continuity in batch 01. The original 438-new-image allocation remains unchanged; add and budget its replacement through an explicit inventory/batch revision before enabling that room. Other reused-room approvals remain pending.

| Batch | Scope | Interior | Outdoor | Total | Manifest |
| --- | --- | ---: | ---: | ---: | --- |
| [01](interiors-generation-batches/interiors-01.md) | Penthouse pilot and core homes | 44 | 4 | 48 | [JSON](interiors-generation-batches/interiors-01.json) |
| [02](interiors-generation-batches/interiors-02.md) | Shared households and resident homes | 38 | 3 | 41 | [JSON](interiors-generation-batches/interiors-02.json) |
| [03](interiors-generation-batches/interiors-03.md) | Remaining private homes | 49 | 2 | 51 | [JSON](interiors-generation-batches/interiors-03.json) |
| [04](interiors-generation-batches/interiors-04.md) | Custom homes and everyday shops | 43 | 2 | 45 | [JSON](interiors-generation-batches/interiors-04.json) |
| [05](interiors-generation-batches/interiors-05.md) | Placeholder replacements and public recreation | 42 | 1 | 43 | [JSON](interiors-generation-batches/interiors-05.json) |
| [06](interiors-generation-batches/interiors-06.md) | University, creative work and learning | 42 | 0 | 42 | [JSON](interiors-generation-batches/interiors-06.json) |
| [07](interiors-generation-batches/interiors-07.md) | Outskirts, waterfront and crew properties | 43 | 3 | 46 | [JSON](interiors-generation-batches/interiors-07.json) |
| [08](interiors-generation-batches/interiors-08.md) | Syndicate and Red Dragons operations | 42 | 0 | 42 | [JSON](interiors-generation-batches/interiors-08.json) |
| [09](interiors-generation-batches/interiors-09.md) | Shinokami, Interpol and campaign facilities | 39 | 1 | 40 | [JSON](interiors-generation-batches/interiors-09.json) |
| [10](interiors-generation-batches/interiors-10.md) | Local faction bases and residences | 39 | 1 | 40 | [JSON](interiors-generation-batches/interiors-10.json) |

## Plugin task assignments

**Assigned:** 2026-11-11. Current status: batches 01 and 02 static artwork complete, batch 03 unfinished and paused with partial outputs, batches 04–10 unstarted. Generation remains paused; assignments do not authorise resuming it.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Each batch: whole-building visual/character continuity and image briefs | Story Skills + Writer's Loop | Review its listed rooms and household/work/faction purpose against authoritative layouts; keep stable image IDs and the 438-image baseline. Garrett's rejected living-room reuse needs an explicit inventory revision. |
| Each batch: full room/view paintings | No matching local community-plugin generator | Use the separately authorised artwork workflow when production is requested. Do not replace required paintings with SVG placeholders, remove scenic backgrounds or route to a paid provider. |
| Each batch: optional transparent prop/portrait layer preparation | Bulk BG Remove only when a listed deliverable needs isolation | Plan memory and review alpha/edges; this is conditional and does not add props, portraits or new images to a batch. |
| Coverage/build-script changes and eventual room-routing regressions | falsegreen-skill | Review changed substantive assertions for exact manifest coverage, duplicate IDs/hashes and production-record preservation, then run the actual verifier and inspect in-person routing. Current static acceptance is not runtime acceptance. |

Actual batch 02 use of Story Skills, Writer's Loop and falsegreen-skill is recorded in its [production review](interiors-generation-batches/interiors-02-production/PRODUCTION_REVIEW.md). This does not retroactively claim plugin use for batch 01. Evidence for the remaining batches and runtime tasks is pending. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Order and review gates

Start batch 01 with Rei’s penthouse to establish the visual standard, then complete the rest of that batch. Numbering is a suggested production order, not a delivery date or authorization to generate all images. Batch 05 groups six placeholder venues including the beach; the library placeholder is replaced within batch 06. All seven required placeholder replacements are covered without duplicate image rows. Within each batch, finish and inspect one building at a time.

The boxing club and Iron Circle are in batch 09 alongside controlled training/campaign settings to keep batch sizes practical. Cross-reference their public-layout rules; grouping does not change their faction affiliation. Batch 10 private-residence subdivisions and new service areas remain proposed layouts: resolve their briefs before generating rather than inventing canon.

## Shared generation requirements

- One dedicated image per listed stable view ID and output path. No multi-room sheets, collages, duplicated backgrounds, embedded labels, UI or watermarks in finished assets.
- Use the building’s existing approved/reviewed imagery and the plan as architectural continuity references: consistent materials, adjacent doors, windows, lighting logic and scale. Existing reuse candidates must pass full-size review before becoming style anchors.
- Prepare an individual prompt for each row using its room purpose, privacy/access, layout connections and necessary activity furniture. A row is a production brief slot, not a claim that its final generation prompt has already been written.
- Match the established illustrated game style; provide uncluttered foreground space for live character overlays. Keep people, guards, changing outfits and transient event props out of the static background. No generic primitive placeholder art.
- Use a consistent approved landscape size/aspect per renderer after checking existing references. Validate resolution, crop, foreground clearance, indoor/outdoor treatment and distinctness at full size and in the in-person window.
- Protect original and approved assets. Stage generated outputs, retain exact prompts/model/source provenance, and install only reviewed results. Do not run the bulk primitive venue renderer over finished location art.
- Record status per image: not started → generated → visual review → accepted/needs revision → integrated → rendered verification. Generation alone does not mean integration or release. Keep actual output paths, checks and limitations current.
- After each batch, verify image-ID/path uniqueness, completeness against its manifest and no duplicate image content. Update the inventory and actual evidence without claiming unrun checks. Required release patch notes are recorded when player-visible work is implemented.

## Planning verification

Validated ten nonempty batches, exact coverage of all 438 inventory rows marked `new_image`, no duplicate assignments and unique target paths. Reuse and conditional rows are excluded. Grouping script: `tools/build_interiors_generation_batches.py`. No generation, image-quality tests or runtime checks performed by this planning operation.

## Production verification — 2026-11-11

`tools/verify_interiors_batch_01.py` passed for all 48 files, exact prompt coverage, PNG resolution, unique file/decoded-pixel content, unchanged original references and the full ten-batch allocation. Both planning generators now refuse to overwrite started production metadata; refusal and unchanged-record checks passed. Revise inventories and manifests explicitly rather than rerunning initial planning generators. Static art acceptance is not runtime integration or release.

`tools/verify_interiors_batch_02.py` passed for all 41 files (38 interior and three outdoor), exact approved membership and prompt coverage, opaque 1536×1024 PNGs, unique file/decoded-pixel content, seven unchanged original references and all 438 baseline assignments. Original generated files match their installed copies. Both planning overwrite refusals and a repeated recorder-call refusal were verified with unchanged protected files. Seven initial images were corrected and re-reviewed; exact attempts and provenance are retained. Lena's and Naomi's original living-room images show open sleeping areas: reconcile those reuse candidates with the planned private bedrooms before integration. See the [batch 02 review](interiors-generation-batches/interiors-02-production/PRODUCTION_REVIEW.md).
