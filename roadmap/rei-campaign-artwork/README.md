# Rei campaign scene artwork — MH-016

**Status:** Deferred — paused by the user on 2026-11-11; revisit after the [Lived-In Interiors update](../INTERIORS_UPDATE_PLAN.md) is implemented. Production started 2026-11-11. Gameplay integration remains pending.

The [manifest](../../assets/campaigns/rei/manifest.json) inventories **183 distinct images** across all **35 existing Rei scenes**, including conditional source pages, scripted reflections, optional attendance/privacy variations, recovery/retry pages and eight encounter-site establishing shots. Each final is a separate opaque landscape illustration under `assets/campaigns/rei/shots/`. Dynamic combat turns are not fixed authored scenes; action-confirmation UI controls retain the current shot rather than inventing new story content.

Use the compiled `campaign_prose/catalog.json` and assembly in `campaign_prose.py` as the text authority. Stable scene/shot IDs, complete source passages, branch mappings, exact generation prompts, immutable reference snapshots/hashes, generated source paths, image hashes/dimensions and individual review statuses are recorded in the manifest. The inventory utility never modifies gameplay or player saves.

All images use the built-in image-generation tool. Each call creates one standalone shot. The current in-game reader has not been changed to consume these files: this is the asset-production portion of MH-016, not a claim that gauntlets, Maps travel or the new reader are implemented.

## Plugin task assignments

**Assigned:** 2026-11-11. Deferred production record. Preserve one corrected opening, 182 pending shots and 29 reference snapshots; no automatic resume.

Follow the [shared plugin workflow and evidence rules](../PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| After interiors, reconcile 183 stable shot records with actual rooms/branches | Story Skills + Writer's Loop | Check scene text, cast, privacy variants and room-specific briefs; adult Rei retains exposed arm tattoos, school Rei remains tattoo-free. Re-review RD01-S01 before reuse. |
| Only if needed for a separately authorised source layer | Bulk BG Remove | Preserve original references and existing alpha; completed scene illustrations remain opaque. Full shot generation is not provided by the local plugin set. |
| Inventory-tool or eventual reader-routing changes | falsegreen-skill | Review exact coverage, immutable-source preservation, branch mapping and saved-cursor assertions; run actual checks when code changes. Runtime acceptance belongs to MH-016. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Identity and continuity

- Adult Rei has source-matched intricate dragon/floral/thorn ink on **both arms**, including exposed forearms, plus neck/upper chest. Fabric covers tattoos naturally; no tattoo ink on fabric. This requirement was explicitly reinforced by the user during production.
- Historical school Rei is 17 and tattoo-free, using his independent school reference. Adult body references are excluded from those generation calls.
- Marcus is present only in living school filmmaking memories, never as a present-day participant or ghost. Loss scenes show the friends and their grief, with no invented final moments or cause.
- Preserve the separate identities of Yuriko, Garrett, Emily, Sophie, Joseph, the current successor administrators and Robin. Generated scenes use their reference images, not recoloured versions of Rei.
- Images contain no narration/UI text. Scene illustrations have scenic opaque backgrounds, while the existing portrait references retain their own alpha.

## Progress and evidence

Inventory generated from all 35 compiled Rei scenes plus Python-authored variants: 183 shot records, 29 immutable reference images. The initial RD01-S01 generation omitted exposed arm tattoos; it was corrected and visually inspected before acceptance. [Exact opening generation/correction record](first-shot-generation.json).

At the pause there is **one generated/corrected image, RD01-S01, and 182 pending images**. The opening passed its initial identity/tattoo review; its room/background must be rechecked against implemented interiors before final reuse. No other generation was submitted. Preserve all existing assets, prompts, source passages, stable IDs and 29 reference snapshots.

Further generation and review are paused. On revisiting after interiors implementation, first reconcile the scene-to-room mapping, layouts, furnishings, reference images and all affected prompts with the implemented game. Treat this inventory as the saved production baseline, not a guarantee that the eventual shot count stays unchanged. Do not overwrite generated work or rebuild stable IDs indiscriminately. There is no automatic resume or scheduled reminder.

No completion or gameplay/UI test pass is claimed. The partial production and pause are recorded as a Development report, not a released feature.

Pause bookkeeping checks, 2026-11-11: confirmed Deferred status, no automatic resume, one accepted image preserved and 182 pending records; the interiors dependency path exists. `python patch_notes.py validate` passed with 490 entries and `python patch_notes.py export` refreshed the curated export. The six-test patch-note suite passed five tests; the existing archive-source test still fails because `tests/screenshots/mixtape-art-review-0.jpg` is missing. No additional image generation or gameplay checks were run after the pause request.
