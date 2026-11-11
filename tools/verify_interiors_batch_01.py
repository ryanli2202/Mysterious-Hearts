"""Verify generated batch 01 files and build a local, read-only art gallery."""
from collections import Counter
import hashlib
from html import escape
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'roadmap/interiors-generation-batches'
PRODUCTION = DIRECTORY / 'interiors-01-production'

def main():
    batch = json.loads((DIRECTORY / 'interiors-01.json').read_text(encoding='utf-8'))
    inventory = json.loads((ROOT / 'roadmap/INTERIORS_IMAGE_INVENTORY.json').read_text(encoding='utf-8'))
    prompts = json.loads((PRODUCTION / 'prompts.json').read_text(encoding='utf-8'))['prompts']
    rows = batch['images']
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    ids = [r['id'] for r in rows]
    paths = [r['target'] for r in rows]
    check(len(rows) == 48, 'Batch 01 must retain its 48 assigned image rows.')
    check(len(ids) == len(set(ids)), 'Duplicate stable image ID.')
    check(len(paths) == len(set(paths)), 'Duplicate target path.')
    check(len(prompts) == 48 and {p['id'] for p in prompts} == set(ids), 'Exact prompt coverage failed.')
    by_view = {v['id']: v for b in inventory['buildings'] for v in b['views']}
    file_hashes, pixel_hashes = [], []
    total_bytes = 0
    for row in rows:
        path = (ROOT / row['target']).resolve()
        path.relative_to(ROOT.resolve())
        check(path.is_file(), f'Missing image: {row["id"]}')
        if not path.is_file():
            continue
        with Image.open(path) as image:
            image.load()
            check(image.format == 'PNG' and image.size == (1536, 1024), f'Format/size: {row["id"]}')
            pixel_hashes.append(hashlib.sha256(image.convert('RGB').tobytes()).hexdigest())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        file_hashes.append(digest)
        total_bytes += path.stat().st_size
        check(digest == row.get('sha256') == by_view[row['id']].get('sha256'), f'Hash/manifest mismatch: {row["id"]}')
        check(row['generation_status'] == 'accepted' and bool(row.get('visual_review')), f'Missing static review: {row["id"]}')
        check(row.get('output_path') == row['target'], f'Output mismatch: {row["id"]}')
    check(len(file_hashes) == len(set(file_hashes)), 'Duplicate file content.')
    check(len(pixel_hashes) == len(set(pixel_hashes)), 'Duplicate decoded image pixels.')
    originals = []
    for name in ('rei', 'emily', 'sophie', 'amy', 'minsu', 'samantha', 'april', 'garrett'):
        relative = f'assets/ui/locations/{name}_home.png'
        original = next(v for v in by_view.values() if v.get('existing') == relative)
        check(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == original['sha256'], f'Original altered: {relative}')
        originals.append(relative)
    all_batches = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(DIRECTORY.glob('interiors-*.json'))]
    all_rows = [r for b in all_batches for r in b['images']]
    required = {v['id'] for v in by_view.values() if v['status'] == 'new_image'}
    check(len(all_batches) == 10 and len(all_rows) == 438, 'Ten-batch baseline count changed.')
    check(len(all_rows) == len({r['id'] for r in all_rows}) and {r['id'] for r in all_rows} == required, 'Ten-batch coverage/uniqueness failed.')
    check(len(all_rows) == len({r['target'] for r in all_rows}), 'Duplicate target across batches.')
    protected = list(DIRECTORY.glob('interiors-*.*')) + [ROOT/'roadmap/INTERIORS_IMAGE_INVENTORY.json', ROOT/'roadmap/INTERIORS_IMAGE_INVENTORY.md', ROOT/'roadmap/INTERIORS_GENERATION_BATCHES.md']
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    guard_results = []
    for script in ('tools/build_interiors_art_inventory.py', 'tools/build_interiors_generation_batches.py'):
        result = subprocess.run([sys.executable, str(ROOT/script)], cwd=ROOT, capture_output=True, text=True)
        message = (result.stdout + result.stderr).strip()
        refused = result.returncode != 0 and 'Refusing to overwrite interiors production records' in message
        check(refused, f'Production overwrite guard failed: {script}')
        guard_results.append(dict(script=script, expected_refusal=refused, exit_code=result.returncode, message=message))
    protected_unchanged = all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in before.items())
    check(protected_unchanged, 'Planning scripts changed production records.')
    report = dict(date='2026-11-11', passed=not errors, assigned_images=len(rows), accepted_images=sum(r['generation_status']=='accepted' for r in rows),
        kinds=dict(Counter(r['kind'] for r in rows)), dimensions=[1536,1024], unique_file_hashes=len(set(file_hashes)),
        unique_decoded_pixel_hashes=len(set(pixel_hashes)), original_references_verified_unchanged=originals,
        exact_prompt_coverage=len(prompts), rejected_attempts=sum(len(p.get('rejected_attempts',[])) for p in prompts),
        ten_batch_unique_coverage=len(all_rows), total_bytes=total_bytes, errors=errors,
        planning_overwrite_guards=guard_results, protected_record_files_unchanged=protected_unchanged,
        limitations=['Static artwork only; no runtime room mappings or save changes.', 'In-person rendered verification and final reuse approval remain pending.',
        'Garrett existing living-room reuse candidate is an exterior; replacement requires explicit inventory/batch revision.'])
    (PRODUCTION/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if errors:
        raise SystemExit(json.dumps(report,indent=2))
    html = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Interiors batch 01 review</title>',
        '<style>body{background:#101722;color:#e4e9f1;font:16px system-ui;margin:0;padding:32px}h1{margin:0 0 12px}p{color:#aebed0;max-width:90ch}h2{margin-top:42px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:20px}figure{margin:0;background:#1c2838;border:1px solid #33475e;border-radius:12px;overflow:hidden}img{display:block;width:100%;height:auto}figcaption{padding:14px}small{display:block;color:#aebed0;margin-top:5px}a{color:#80cdbb}</style>',
        '<h1>Interiors · Batch 01</h1><p>48 individual backgrounds · 1536 × 1024 · static art reviewed. Click an image to view the full-size PNG. Runtime room integration and in-person verification are pending.</p>',
        '<p>Garrett’s original living-room candidate is an exterior view and requires a separately tracked replacement. Existing assets and saves are unchanged.</p>']
    for building in dict.fromkeys(r['building_id'] for r in rows):
        group = [r for r in rows if r['building_id']==building]
        html.append('<h2>'+escape(group[0]['building_name'])+'</h2><div class="grid">')
        for r in group:
            url = '../../../'+r['target']
            html.append('<figure><a href="'+escape(url,quote=True)+'"><img loading="lazy" src="'+escape(url,quote=True)+'" alt="'+escape(r['room'],quote=True)+'"></a><figcaption>'+escape(r['room'])+'<small>'+escape(r['id'])+' · '+escape(r['kind'])+'</small></figcaption></figure>')
        html.append('</div>')
    html.append('</html>')
    (PRODUCTION/'gallery.html').write_text('\n'.join(html),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
