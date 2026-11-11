"""MH-013 wardrobe production ledger. Never alters portrait pixels.

Only inspection composites are rendered here. Artwork is copied byte-for-byte
from the built-in image generator, and visual acceptance is recorded separately.
"""
import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'roadmap/artwork-stage-03'
FAMILIES = ('amy', 'april', 'emily', 'garrett', 'ivan', 'minsu', 'rei', 'samantha', 'sophie', 'yuriko')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    if (OUT / 'roster.json').exists():
        raise SystemExit('Frozen roster already exists; originals are immutable.')
    for name in ('originals', 'masters', 'candidates', 'generations', 'reviews', 'checks', 'screenshots'):
        (OUT / name).mkdir(parents=True, exist_ok=True)
    baseline = read(ROOT / 'roadmap/artwork-portrait-audit/inventory.json')['assets']
    notes = {r['id']: r for r in csv.DictReader((ROOT / 'roadmap/artwork-portrait-audit/review_notes.psv').open(encoding='utf-8'), delimiter='|')}
    masters = {r['id']: r for r in read(ROOT / 'roadmap/artwork-stage-02/roster.json')['assets']}
    heights = read(ROOT / 'assets/portraits/stature.json')
    shutil.copy2(ROOT / 'assets/portraits/stature.json', OUT / 'before-stature.json')
    rows = []
    for who in FAMILIES:
        master = masters[who]
        shutil.copy2(ROOT / master['path'], OUT / 'masters' / (who + '.png'))
        for asset in baseline:
            path = Path(asset['path'])
            if path.parent.as_posix() != 'assets/portraits' or not path.stem.startswith(who + '-'):
                continue
            variant = path.stem[len(who) + 1:]
            if variant in ('high-school', 'syndicate') or variant.startswith('selection'):
                continue
            note = notes[asset['id']]
            shutil.copy2(ROOT / path, OUT / 'originals' / path.name)
            row = dict(id=path.stem, character=who, variant=variant, path=path.as_posix(),
                       audit_id=asset['id'], original='originals/' + path.name,
                       old_sha256=digest(ROOT / path), master='masters/' + who + '.png',
                       master_path=master['path'], master_sha256=digest(ROOT / master['path']),
                       height_cm=heights['characters'][who]['height_cm'],
                       identity=master['identity'], observed=note['observed'], required_change=note['required_change'])
            row['prompt'] = (
                'Use case: identity-preserve. Create ONE wardrobe variant for Mysterious Hearts MH-013 Stage 3. '
                f'Subject: adult {who}; outfit: {variant}. '
                'Image 1 is the ACCEPTED STAGE 2 MASTER: exact face, hairstyle, age, complexion, eye colour, body build, '
                'head/body proportions, pose, rendering and head-to-mid-thigh composition. Keep that same person. '
                'Image 2 is the OLD OUTFIT REFERENCE ONLY: transfer its clothing design, colours, materials, patterns, '
                'jewellery and outfit-specific exposed markings onto Image 1. Never copy Image 2\'s old face, short crop or anatomy. '
                f'Character reference: {master["identity"]}. This person\'s corrected full stature is {row["height_cm"]} cm. '
                f'Outfit observations: {note["observed"]}. Source audit: {note["required_change"]}. '
                'Match the master\'s face size, eye line, shoulder width, waist, pelvis and thigh landmarks precisely; '
                'clothes change, body proportions and apparent stature do not. Master clothing is replaced by the outfit reference. '
                'Keep semi-realistic ILLUSTRATED MANHWA with dimensional nose, eyelids and lips, restrained eye scale, '
                'selective tapered outlines and controlled soft-plus-shaped shadows; no photographic or 3D skin, no generic idol face. '
                'Preserve fine individual hair strands and the master\'s facial softness. Tattoos retain correct side and natural clothing occlusion. '
                'Vertical 2:3, 1024x1536 RGBA. Complete hairstyle, shoulders, arms and visible hands; natural fingers. '
                'Show connected torso, pelvis and BOTH upper thighs through true MID-THIGH. THE LOWER THIGHS, KNEES, LOWER LEGS AND FEET ARE CROPPED OUT. '
                'The image bottom is a picture crop, never feet or floor. Do not lengthen the torso, stretch limbs, show knees, '
                'zoom out to full body or shrink the head to fit legs. Preserve full-length garments by cropping their fabric at mid-thigh, '
                'never shorten a gown or robe just to reveal skin. Short hems show a little connected thigh below, without knees. '
                'Keep small clear margins above hair and beside hands; clean horizontal mid-thigh cutoff near bottom. '
                'Genuine transparent background around and within silhouette. No backdrop, checkerboard, floor, ground shadow, '
                'ambient rectangle, glow, white fringe, caption, signature or watermark. No new weapons or magic. '
                'One standalone character only. Ordinary nonsexual wardrobe catalogue pose; preserve existing garment coverage.'
            )
            rows.append(row)
    write(OUT / 'roster.json', dict(roadmap_id='MH-013', stage=3, recorded='2026-11-11',
          scope='Contemporary wardrobe variants for ten characters; historical, masked and combat variants remain Stage 4.', assets=rows))
    write(OUT / 'before-state.json', {r['path']: digest(ROOT / r['path']) for r in baseline})
    write(OUT / 'reviews.json', {})
    print(json.dumps({'total': len(rows), 'families': {w: sum(r['character'] == w for r in rows) for w in FAMILIES}}))


def queue(who=None, count=4, ids=None):
    rows = read(OUT / 'roster.json')['assets']
    briefs = read(OUT / 'outfit-briefs.json')
    supporting = read(OUT / 'supporting-references.json') if (OUT / 'supporting-references.json').exists() else {}
    pending = [r for r in rows if r['id'] in ids] if ids else [r for r in rows if (who is None or r['character'] == who) and not (OUT / 'candidates' / (r['id'] + '.png')).exists()]
    jobs = []
    for row in pending[:count]:
        brief = briefs[row['id']]
        refs = [str(OUT / row['master'])]
        prompt = (
            'Edit this EXACT image, preserving face, hair, head size and position, body proportions, hand position, pose and mid-thigh framing. '
            f'This is {row["character"]}\'s accepted Stage 2 master, {row["height_cm"]} cm full stature. '
            f'Change ONLY the clothing to this established wardrobe outfit: {brief}. '
            'Replace the master clothes completely. The character is an adult in an ordinary neutral wardrobe catalogue pose. '
            'Keep the same underlying body and hand positions. Do not redraw, enlarge or change the face or hair. '
            'Keep the EXACT eye-line, chin, shoulders, hips, crotch and thigh cutoff at their current positions. '
            'Do not copy clothing bulk into the body. Preserve age, complexion, build, eye colour, glasses, hair ornaments and visible markings. '
            'Clothes occlude tattoos naturally. Preserve fine individual hair strands and the master\'s soft-plus-shaped illustrated manhwa rendering. '
            'The LOWER THIGHS, KNEES, LOWER LEGS AND FEET remain OUTSIDE the frame. Keep the complete head through true MID-THIGH; '
            'never lengthen torso/legs, zoom out to full body, crop at hips or add knees. The bottom is a picture crop, not feet or a floor. '
            'Preserve the BODY crop, not the master clothing hem. If the requested outfit has trousers, leggings, overalls or a long garment, '
            'its fabric continues to the bottom picture cutoff: NO finished lower hem and NO strip of bare skin underneath. '
            'Do not turn trousers or leggings into shorts, even when the master wears a short skirt. '
            'Only requested shorts or short skirts have a finished hem above the body crop. '
            'When a shorts or short-skirt hem is above that crop, the visible upper thighs MUST continue naturally below the hem to the body cutoff; never erase the thighs or end the body at the clothing hem. '
            'Same 1024x1536 2:3 transparent RGBA canvas, clear top and side margins and complete hands. '
            'Genuine alpha everywhere outside the character and in the arm gaps; no background, haze, glow, ground shadow, '
            'text, watermark or signature. Do not add props or change the face expression.'
        )
        if row['id'] in supporting:
            refs.extend(str(OUT / path) for path in supporting[row['id']])
            prompt += (' Image 1 is the sole EDIT TARGET and is authoritative for face, hair, physique, proportions, pose and framing. '
                       'Additional images are ONLY detailed tattoo maps for skin newly exposed by the outfit. '
                       'Preserve those specific tattoo designs and anatomical sides, with clothing occlusion, on the Image 1 body. '
                       'Do NOT adopt the additional images\' faces, head size, body bulk, muscle rendering, pose, clothes or short crop. '
                       'Keep Image 1\'s current visible neck/chest tattoos aligned exactly; extend only the uncovered mapped markings.')
        job = dict(id=row['id'], prompt=prompt, referenced_image_paths=refs, transparent_background=True)
        jobs.append(job)
        write(OUT / 'jobs' / (row['id'] + '.json'), job)
    write(OUT / 'queue.json', jobs)
    print(json.dumps({'pending': len(pending), 'jobs': [r['id'] for r in jobs]}))


def register(ident, source, prompt=None, references=None):
    rows = {r['id']: r for r in read(OUT / 'roster.json')['assets']}
    row = rows[ident]
    source = Path(source)
    with Image.open(source) as im:
        im.load()
        if im.mode != 'RGBA' or im.size != (1024, 1536) or im.getchannel('A').getextrema()[0] != 0:
            raise ValueError(f'Expected transparent RGBA 1024x1536, got {im.mode} {im.size}')
    records = list((OUT / 'generations').glob(ident + '-[0-9][0-9].json'))
    number = len(records) + 1
    candidate = OUT / 'candidates' / (ident + '.png')
    if candidate.exists():
        shutil.copy2(candidate, OUT / 'generations' / f'{ident}-{number-1:02d}.png')
    shutil.copy2(source, candidate)
    write(OUT / 'generations' / f'{ident}-{number:02d}.json', dict(
        id=ident, tool='built-in image_gen', model='not exposed', generated_source=str(source),
        sha256=digest(source), prompt=prompt or row['prompt'],
        referenced_image_paths=references or [str(OUT / row['master']), str(OUT / row['original'])],
        transparent_background=True, pixel_postprocessing=False))
    print(ident, digest(candidate))


def panel(path, colour, size):
    with Image.open(path) as source:
        im = source.convert('RGBA')
        im.thumbnail(size, Image.Resampling.LANCZOS)
    frame = Image.new('RGBA', size, colour)
    frame.alpha_composite(im, ((size[0]-im.width)//2, size[1]-im.height))
    return frame.convert('RGB')


def sheets(who, source=False):
    rows = [r for r in read(OUT / 'roster.json')['assets'] if r['character'] == who]
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    paths = [('STAGE 2 MASTER', OUT / rows[0]['master'])] + [(r['variant'], OUT / (r['original'] if source else 'candidates/' + r['id'] + '.png')) for r in rows]
    paths = [(label, path) for label, path in paths if path.exists()]
    for start in range(0, len(paths), 8):
        items = paths[start:start+8]
        board = Image.new('RGB', (1280, 540*((len(items)+3)//4)), '#18232b')
        draw = ImageDraw.Draw(board)
        for i, (label, path) in enumerate(items):
            x, y = (i%4)*320, (i//4)*540
            draw.text((x+6,y+5), label, font=font, fill='#eee9e1')
            board.paste(panel(path, '#273744', (320,500)), (x,y+35))
        target = OUT / 'reviews' / f'{who}-{"source" if source else "set"}-{start//8+1:02d}.jpg'
        board.save(target, quality=95)
        print(target)


def verify():
    rows = read(OUT / 'roster.json')['assets']
    reviews = read(OUT / 'reviews.json')
    errors, pending, assets = {}, [], []
    assert digest(ROOT / 'assets/portraits/stature.json') == digest(OUT / 'before-stature.json'), 'Height table changed'
    for row in rows:
        assert digest(OUT / row['original']) == row['old_sha256'], row['id']
        assert digest(OUT / row['master']) == row['master_sha256'] == digest(ROOT / row['master_path']), row['id']
        candidate = OUT / 'candidates' / (row['id'] + '.png')
        if not candidate.exists():
            pending.append(row['id']); continue
        with Image.open(candidate) as im:
            im.load()
            a = im.getchannel('A'); h = a.histogram(); total = sum(h)
            bounds = a.point(lambda v: 255 if v >= 16 else 0).getbbox()
            issues = []
            if im.mode != 'RGBA' or im.size != (1024,1536): issues.append('Wrong format/size')
            if not (h[0] and sum(h[:8])/total > .10 and sum(h[220:])/total > .15): issues.append('Invalid cutout alpha')
            if not (bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<im.width): issues.append('Top/side edge contact')
            if issues: errors[row['id']] = issues
            record = sorted((OUT / 'generations').glob(row['id'] + '-[0-9][0-9].json'))[-1]
            provenance = read(record)
            assert digest(candidate) == provenance['sha256'], row['id']
            review = reviews.get(row['id'], {})
            if review.get('accepted') and review.get('accepted_sha256') != digest(candidate):
                errors.setdefault(row['id'], []).append('Visual acceptance does not match candidate hash')
            row = dict(row, candidate=candidate.relative_to(OUT).as_posix(), new_sha256=digest(candidate),
                       size=list(im.size), alpha_extrema=list(a.getextrema()), visible_bbox=bounds,
                       clear_fraction=round(sum(h[:8])/total,5), solid_fraction=round(sum(h[220:])/total,5),
                       generation_record=record.relative_to(OUT).as_posix(), review=reviews.get(row['id']))
        assets.append(row)
        if not reviews.get(row['id'], {}).get('accepted'): pending.append(row['id'])
    manifest = dict(roadmap_id='MH-013', stage=3, total=len(rows), generated=len(assets),
                    visually_accepted=sum(bool(r['review'] and r['review'].get('accepted')) for r in assets),
                    pending=pending, technical_errors=errors, assets=assets)
    write(OUT / 'manifest.json', manifest)
    print(json.dumps({k:(len(v) if k == 'pending' else v) for k,v in manifest.items() if k != 'assets'}))


def alpha_sheets(who):
    rows = [r for r in read(OUT/'roster.json')['assets'] if r['character'] == who and (OUT/'candidates'/(r['id']+'.png')).exists()]
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
    for start in range(0,len(rows),7):
        subset=rows[start:start+7]
        board=Image.new('RGB',(1120,220*len(subset)), '#18232b')
        draw=ImageDraw.Draw(board)
        for i,row in enumerate(subset):
            for j,colour in enumerate(('#273744','#647c87','#e6e3dd')):
                board.paste(panel(OUT/'candidates'/(row['id']+'.png'),colour,(240,220)),(j*240,i*220))
            draw.text((730,i*220+35),row['id'],fill='#eee9e1',font=font)
        path=OUT/'reviews'/f'{who}-alpha-{start//7+1:02d}.jpg'
        board.save(path,quality=95)
        print(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare','queue','register','sheets','alpha','verify'))
    parser.add_argument('--who')
    parser.add_argument('--count', type=int, default=4)
    parser.add_argument('--id')
    parser.add_argument('--source')
    parser.add_argument('--ids')
    parser.add_argument('--job')
    args = parser.parse_args()
    if args.command == 'prepare': prepare()
    elif args.command == 'queue': queue(args.who,args.count,args.ids.split(',') if args.ids else None)
    elif args.command == 'register':
        job = read(Path(args.job)) if args.job else None
        register(args.id,args.source,job['prompt'] if job else None,job['referenced_image_paths'] if job else None)
    elif args.command == 'sheets': sheets(args.who,bool(args.source))
    elif args.command == 'alpha': alpha_sheets(args.who)
    else: verify()
