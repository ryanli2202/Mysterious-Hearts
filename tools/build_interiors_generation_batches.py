"""Partition the current image inventory into ten reviewable generation batches."""
from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / 'roadmap'
for manifest in (ROADMAP / 'interiors-generation-batches').glob('interiors-*.json'):
    existing = json.loads(manifest.read_text(encoding='utf-8'))
    if existing.get('status') != 'planned' or any(
        row.get('generation_status', 'not_started') != 'not_started'
        for row in existing.get('images', [])
    ):
        raise SystemExit('Refusing to overwrite interiors production records; revise the existing manifests explicitly.')
source = json.loads((ROADMAP/'INTERIORS_IMAGE_INVENTORY.json').read_text(encoding='utf-8'))
GROUPS = [
 ('Penthouse pilot and core homes', 'rei_home emily_home sophie_home nest_dorm_corridor samantha_home april_home garrett_home'),
 ('Shared households and resident homes', 'valentina_home neo_home tyler_home lena_home naomi_home celeste_home dev_home'),
 ('Remaining private homes', 'rosa_home elliot_home daniel_home fox_home gordon_home sylvanis_home martos_home elias_home camila_home'),
 ('Custom homes and everyday shops', 'vacant_downtown_home vacant_suburbs_home vacant_beach_home vacant_university_home cafe noodle_shop marios_pizza chess flowers boutique'),
 ('Placeholder replacements and public recreation', 'shopping_mall bowling_alley arcade nightclub bar beach public_park_pavilion track arena'),
 ('University, creative work and learning', 'campus studio library archive makerspace cycle_shop planetarium cinema'),
 ('Outskirts, waterfront and crew properties', 'hill_tea_room farm_shop pottery_studio marine_centre harbour_market railway_museum southbank_diner sailing_club market crew_lot_west crew_lot_docks crew_lot_north crew_lot_south'),
 ('Syndicate and Red Dragons operations', 'syndicate_office syndicate_hq syndicate site_04 site_05 site_06 site_07 site_08 glasshouse_lab'),
 ('Shinokami, Interpol and campaign facilities', 'site_01 site_02 site_03 interpol_hq blackstone_hq hamayashi_house hamayashi_annex hamayashi_store boxing_club iron_circle'),
 ('Local faction bases and residences', 'lantern_house saints_depot purple_clubhouse rojos_courtyard consortium_house'),
]
by_id = {b['id']: b for b in source['buildings']}
required = {r['id'] for b in source['buildings'] for r in b['views'] if r['status']=='new_image'}
seen = set()
batches=[]
out=ROADMAP/'interiors-generation-batches'
out.mkdir(exist_ok=True)
for index,(title,keys) in enumerate(GROUPS,1):
    entries=[]; refs=[]
    for key in keys.split():
        b=by_id[key]
        for r in b['views']:
            if r['status']=='reuse_candidate':
                refs.append(dict(building_id=key,room=r['room'],path=r['existing']))
            if r['status']!='new_image': continue
            assert r['id'] not in seen, r['id']
            seen.add(r['id'])
            entries.append(dict(r,building_id=key,building_name=b['name'],generation_status='not_started'))
    batch=dict(batch_id=f'interiors-{index:02}',title=title,status='planned',images=entries,existing_references=refs)
    batches.append(batch)
assert seen==required, dict(missing=sorted(required-seen),extra=sorted(seen-required))
assert len(batches)==10 and all(b['images'] for b in batches)
paths=[r['target'] for b in batches for r in b['images']]
assert len(paths)==len(set(paths))
for b in batches:
    stem=b['batch_id']
    (out/(stem+'.json')).write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=[f"# {stem} — {b['title']}",'','**Status:** Planned; no generation performed.',f"**Image count:** {len(b['images'])}",'',
           'Follow the [shared generation requirements](../INTERIORS_GENERATION_BATCHES.md#shared-generation-requirements). Each row is one individual image, never a collage. Existing references are continuity guides, not additional generation tasks.','']
    for key in dict.fromkeys(r['building_id'] for r in b['images']):
        rows=[r for r in b['images'] if r['building_id']==key]
        lines += [f"## {rows[0]['building_name']} (`{key}`)",'','| Stable image ID | Room/view | Type | Planned output |','| --- | --- | --- | --- |']
        lines += [f"| `{r['id']}` | {r['room']} | {r['kind']} | `{r['target']}` |" for r in rows]
        refs=[r for r in b['existing_references'] if r['building_id']==key]
        if refs:
            lines += ['', 'Existing continuity references: '+', '.join(f"[{r['room']}](../../{r['path']})" for r in refs)+'.']
        lines += ['']
    (out/(stem+'.md')).write_text('\n'.join(lines),encoding='utf-8')
total=sum(len(b['images']) for b in batches)
kinds=Counter(r['kind'] for b in batches for r in b['images'])
excluded=Counter(r['status'] for b in source['buildings'] for r in b['views'] if r['status']!='new_image')
lines=['# Interiors — ten image-generation batches','','**Status:** Planned production grouping. No image generation or installation performed.','',
       f"The current [image inventory](INTERIORS_IMAGE_INVENTORY.md) requires **{total} new images**: **{kinds['interior']} interior views** and **{kinds['outdoor']} outdoor views**. They are assigned exactly once across ten batches. Whole buildings stay together; counts vary to preserve visual continuity and coherent review scope.",'',
       f"Excluded from generation: **{excluded['reuse_candidate']} reuse candidates** (87 interior and 3 outdoor) and **{excluded['layout_decision']} unresolved dorm bathrooms**. Reuse still needs final full-size/in-game approval. A rejected candidate or resolved new bathroom requires an explicit inventory/batch revision, not an untracked extra image.",'',
       '| Batch | Scope | Interior | Outdoor | Total | Manifest |','| --- | --- | ---: | ---: | ---: | --- |']
for i,b in enumerate(batches,1):
    c=Counter(r['kind'] for r in b['images'])
    lines.append(f"| [{i:02}](interiors-generation-batches/{b['batch_id']}.md) | {b['title']} | {c['interior']} | {c['outdoor']} | {len(b['images'])} | [JSON](interiors-generation-batches/{b['batch_id']}.json) |")
lines += ['', '## Order and review gates','',
          'Start batch 01 with Rei’s penthouse to establish the visual standard, then complete the rest of that batch. Numbering is a suggested production order, not a delivery date or authorization to generate all images. Batch 05 groups six placeholder venues including the beach; the library placeholder is replaced within batch 06. All seven required placeholder replacements are covered without duplicate image rows. Within each batch, finish and inspect one building at a time.', '',
          'The boxing club and Iron Circle are in batch 09 alongside controlled training/campaign settings to keep batch sizes practical. Cross-reference their public-layout rules; grouping does not change their faction affiliation. Batch 10 private-residence subdivisions and new service areas remain proposed layouts: resolve their briefs before generating rather than inventing canon.', '',
          '## Shared generation requirements','',
          '- One dedicated image per listed stable view ID and output path. No multi-room sheets, collages, duplicated backgrounds, embedded labels, UI or watermarks in finished assets.',
          '- Use the building’s existing approved/reviewed imagery and the plan as architectural continuity references: consistent materials, adjacent doors, windows, lighting logic and scale. Existing reuse candidates must pass full-size review before becoming style anchors.',
          '- Prepare an individual prompt for each row using its room purpose, privacy/access, layout connections and necessary activity furniture. A row is a production brief slot, not a claim that its final generation prompt has already been written.',
          '- Match the established illustrated game style; provide uncluttered foreground space for live character overlays. Keep people, guards, changing outfits and transient event props out of the static background. No generic primitive placeholder art.',
          '- Use a consistent approved landscape size/aspect per renderer after checking existing references. Validate resolution, crop, foreground clearance, indoor/outdoor treatment and distinctness at full size and in the in-person window.',
          '- Protect original and approved assets. Stage generated outputs, retain exact prompts/model/source provenance, and install only reviewed results. Do not run the bulk primitive venue renderer over finished location art.',
          '- Record status per image: not started → generated → visual review → accepted/needs revision → integrated → rendered verification. Generation alone does not mean integration or release. Keep actual output paths, checks and limitations current.',
          '- After each batch, verify image-ID/path uniqueness, completeness against its manifest and no duplicate image content. Update the inventory and actual evidence without claiming unrun checks. Required release patch notes are recorded when player-visible work is implemented.', '',
          '## Planning verification','',
          f"Validated ten nonempty batches, exact coverage of all {total} inventory rows marked `new_image`, no duplicate assignments and unique target paths. Reuse and conditional rows are excluded. Grouping script: `tools/build_interiors_generation_batches.py`. No generation, image-quality tests or runtime checks performed by this planning operation.",'']
(ROADMAP/'INTERIORS_GENERATION_BATCHES.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(total=total,kinds=dict(kinds),batches=[dict(id=b['batch_id'],images=len(b['images'])) for b in batches]),indent=2))
