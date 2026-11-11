# Interiors batch 02 — artwork production review

**Date:** 2026-11-11 (Australia/Brisbane)  
**Roadmap:** MH-004 Lived-In Interiors  
**Status:** 41/41 assigned new images generated and statically accepted. Runtime integration and in-person rendered verification are pending.

## Deliverables

[Open the full review gallery](gallery.html). Each scene links to its full-size PNG. Final files are under `assets/ui/locations/interiors/`, using the stable targets in the [batch manifest](../interiors-02.json).

| Building | Accepted new images |
| --- | ---: |
| Yeuns' Ferry Signal House | 9 |
| Neo and Alyssa's station apartment | 6 |
| Tyler's East Ward duplex | 6 |
| Lena's clocktower flat | 6 |
| Naomi's riverside maisonette | 7 |
| Celeste's blue-door cottage | 5 |
| Dev's station studio | 2 |
| Total | 41 |

38 interior views and three outdoor views. All final files are opaque 1536×1024 PNGs, totalling 102,203,921 bytes. Each is a separate scene, with no collage or embedded navigation labels.

## Generation and visual review

Built-in `image_gen` produced one scene per call/attempt. The underlying model identifier is not exposed and has not been guessed. [prompts.json](prompts.json) retains exact final prompts, reference paths and rejected-attempt provenance. The batch manifest records original generation paths, dimensions, hashes and individual visual-review notes. Original generated files remain at the tool-provided paths; accepted copies were installed without overwriting original location art.

All seven original home references were inspected at full size. Room prompts retained their architectural materials, light, household purpose and connections from the planned layouts. Each generated image was visually inspected before acceptance; checks covered room function, materials, activity furniture, clear foreground, people/text exclusion and indoor/outdoor treatment. These are static illustration reviews, not proof of physical dimensions, accessible-building compliance or runtime scene crops.

48 successful generation calls yielded 41 accepted scenes and seven replaced attempts:

| Corrected scene | Rejected issue and accepted correction |
| --- | --- |
| Neo kitchen/dining | Initial extractor was above the sink with no cooking hob; added a hob with the hood above it and kept the sink separate. |
| Tyler father's bedroom | Removed a rug visible in the adjoining hall to preserve the planned clear level route. |
| Tyler accessible bathroom | Frosted the large window, added a lever basin mixer and toilet grab rail; retained the roll-in shower, seat and open knee space. |
| Tyler accessible porch | Removed the mat, used a lever door handle and clarified the flush threshold; preserved the ramp and rails. |
| Lena bathroom | Frosted the large window and replaced the main timber floor with warm grey stone tile. |
| Naomi bathroom | Frosted the added large window for privacy. |
| Celeste kitchen/dining | Added a visible oven and hob to support the room's cooking and baking purpose. |

Both rejected originals and correction sources remain traceable; no discarded result was silently substituted for a final asset.

## Actual plugin/workflow execution

- **Imagegen skill:** used the built-in generation/editing workflow and preserved exact prompts, original output paths and selected copies. No external paid provider, new connection or sign-in was used.
- **Story Skills, revision-continuity:** read `writing/SOURCE_MAP.md`, reviewed household/layout authority and the seven existing references. Kept Ivan and Valentina's bedrooms separate, Neo/Alyssa's bedroom shared, Tyler's father's room and level routes intact, and the Yeun piano alcove an open shared zone. Lena's flat was not given shop access; Dev received only the two assigned new views. No campaign manuscript, schedules, outcomes or story-workspace canon was changed, and no story CLI validation is claimed.
- **Writer's Loop:** framed each room against the authorised brief, drafted prompts, reviewed generated scenes and made the seven targeted corrections above. Review retained the requested 41-image scope. No persistent preference learning or new user approval was inferred from generated art.
- **falsegreen-skill:** manually reviewed the changed verifier and recorder protection checks. No actionable false-positive finding remained in that focused review. The verifier uses the separately maintained Markdown allocation plus fixed building/outdoor counts, actual PNG decoding, source/copy hashes, inventory comparison and real failing-command probes. The initial incomplete-batch failure and recorder overwrite refusal below exercise negative outcomes. No automated falsegreen scanner or gameplay test result is claimed.
- **Context Guard:** the initial project status command reported no local session state; production records carried the working evidence. A later recovery hook supplied active-session evidence after compaction. No private state was edited and no stronger release contract was adopted.
- **Other community media plugins:** not invoked. These paintings require no isolated layers, SVG/icon export, synthetic sound, stock audio, animation or trailer. The documented scenic-painting capability gap was handled by the separately authorised built-in image workflow.

Assignments are preserved in the child plan and parent generation schedule. The evidence above records this batch's actual work only and does not retroactively attribute batch 01 to these plugins.

## Actual verification

`python tools/verify_interiors_batch_02.py` passed. [verification.json](verification.json) confirms:

- Exact 41-image membership, paths, classification and prompt coverage against the assigned batch; all 41 have static review records.
- Opaque PNG format at 1536×1024, with installed bytes matching generated original files and both manifest/inventory hashes.
- 41 unique file hashes and 41 unique decoded-pixel hashes, plus no repeated accepted file hash across completed batches. Full-size visual inspection also checked distinct room views.
- All seven original home images retain their inventory hashes.
- Ten batches retain all 438 baseline new-image IDs and unique target paths.
- Both planning generators reject overwriting production metadata; protected records remain unchanged during those probes.

The verifier was also run while only 34 scenes were installed and failed on exactly the seven unfinished outputs. That observed failure is retained in [verification-incomplete.json](verification-incomplete.json). It was not a passing result.

A repeated call to `tools/record_interiors_image.py --batch 2` for the existing Yeun entrance raised the expected `FileExistsError: Refusing to overwrite`. Its image, batch 02 manifest, inventory and batch 01 manifest remained unchanged during the probe; [recorder-overwrite-check.json](recorder-overwrite-check.json) records the point-in-time hashes. Later authorised documentation/status updates naturally change metadata hashes.

`python patch_notes.py validate` passed with 498 existing entries. `python patch_notes.py export` refreshed `patch_notes/PATCH_NOTES.md`. No new release entry was added because these assets are not routed into player-visible rooms.

## Integration limits

The requested artwork batch is complete. Access is through the gallery and asset files. Runtime navigation, saves and original scene routing are unchanged; no restart or migration is needed to review the images. Phone surfaces were not changed, so no phone smoke or gameplay/in-person rendered acceptance is claimed.

Before enabling these rooms, map each scene in the in-person window and verify actual crop, character overlays, connected doors, privacy, and indoor/outdoor weather/lighting treatment. Tyler's illustrated clear routes and bathroom fittings still need review in the actual rendered context; static artwork does not certify measured accessibility.

Lena's original living/record image shows an open loft bed and Naomi's original living image shows an open mezzanine sleeping area, while their planned new bedrooms are private rooms off the hall/landing. Reconcile those reuse candidates with room/privacy routing before integration. The original references and approved allocations were preserved; any replacement needs an explicit inventory/batch revision. Garrett's separate batch 01 exterior-as-living-room finding and the two unresolved dorm bathrooms remain unchanged.

Across batches 01 and 02, 89 of the 438 assigned new images are statically accepted. See the shared generation schedule for later batch progress; batch 03 is unfinished and generation is paused.
