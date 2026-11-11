"""Record generated interiors artwork without changing runtime room mappings."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'roadmap/interiors-generation-batches/interiors-01.json'
PRODUCTION = BATCH.parent / 'interiors-01-production'

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    global BATCH, PRODUCTION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=int, choices=range(1, 11), default=1)
    parser.add_argument('--id', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--review', required=True)
    args = parser.parse_args()
    BATCH = ROOT / f'roadmap/interiors-generation-batches/interiors-{args.batch:02d}.json'
    PRODUCTION = BATCH.parent / f'interiors-{args.batch:02d}-production'
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    row = next(r for r in batch['images'] if r['id'] == args.id)
    prompts = json.loads((PRODUCTION / 'prompts.json').read_text(encoding='utf-8'))
    prompt = next(r for r in prompts['prompts'] if r['id'] == args.id)
    source = Path(args.source).resolve(strict=True)
    target = (ROOT / row['target']).resolve()
    target.relative_to(ROOT.resolve())
    if target.exists():
        raise FileExistsError(f'Refusing to overwrite {target}')
    with Image.open(source) as im:
        im.load()
        assert im.format == 'PNG', im.format
        assert im.size == (1536, 1024), im.size
        dimensions, mode = list(im.size), im.mode
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = PRODUCTION / 'staging' / (args.id + '.png')
    staging.parent.mkdir(parents=True, exist_ok=True)
    if staging.exists():
        raise FileExistsError(staging)
    shutil.copy2(source, staging)
    staging.rename(target)
    row.update(generation_status='accepted', generated_date='2026-11-11',
        output_path=row['target'], source_path=str(source), dimensions=dimensions,
        mode=mode, sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
        tool='built-in image_gen', model='Not exposed by built-in tool',
        prompt_manifest=(PRODUCTION / 'prompts.json').relative_to(ROOT).as_posix(),
        prompt_id=prompt['id'], visual_review=args.review,
        integration_status='pending; no runtime room mapping added',
        rendered_verification='pending in-person room implementation')
    batch['status'] = 'in_progress'
    batch['production_started'] = '2026-11-11'
    batch['accepted_count'] = sum(r['generation_status'] == 'accepted' for r in batch['images'])
    write_json(BATCH, batch)
    inventory_path = ROOT / 'roadmap/INTERIORS_IMAGE_INVENTORY.json'
    inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
    inventory['production_status'] = 'in_progress'
    view = next(v for b in inventory['buildings'] for v in b['views'] if v['id'] == args.id)
    view.update(generation_status='accepted', output_path=row['target'], dimensions=dimensions,
        sha256=row['sha256'], production_manifest=BATCH.relative_to(ROOT).as_posix(),
        integration_status=row['integration_status'])
    write_json(inventory_path, inventory)
    print(json.dumps(dict(id=args.id, accepted=batch['accepted_count'], total=len(batch['images']), output=row['target'])))

if __name__ == '__main__':
    main()
