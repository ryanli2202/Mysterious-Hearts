"""MH-013 Stage 2 production ledger and inspection boards; never edits portrait pixels.

Candidates stay outside live wardrobe discovery. Acceptance is a human/visual
decision in reviews.json, independent of these technical checks.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'roadmap/artwork-stage-02'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    if (OUT / 'roster.json').exists():
        raise SystemExit('Roster already frozen; refusing to replace originals.')
    import character_appearance
    import organisation_guards
    for name in ('originals', 'candidates', 'generations', 'identity-sheets', 'checks', 'screenshots'):
        (OUT / name).mkdir(parents=True, exist_ok=True)
    baseline = read(ROOT / 'roadmap/artwork-portrait-audit/inventory.json')['assets']
    audit = {r['path']: r for r in baseline}
    notes = {r['id']: r for r in csv.DictReader((ROOT / 'roadmap/artwork-portrait-audit/review_notes.psv').open(encoding='utf-8'), delimiter='|')}
    pilot = {r['path']: r for r in read(ROOT / 'roadmap/artwork-batch-01/manifest.json')['assets']}
    appearance = {k.lower().replace(' ', '-'): v for k, v in character_appearance.records().items()}
    paths = sorted((ROOT / 'assets/portraits').glob('*-selection.png'))
    paths = [p for p in paths if p.name not in ('charles-selection.png', 'neo-selection.png')]
    paths += [ROOT / 'assets/portraits/charles-selection-v2.png', ROOT / 'assets/portraits/neo-scene.png']
    # Richter's boss form is a context variant of his civilian master (Stage 4).
    paths += [p for p in sorted((ROOT / 'assets/portraits/guards').glob('*.png')) if p.stem != 'richter_cybernetic']
    rows = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        role = path.parent.name == 'guards'
        key = path.stem if role else path.stem.replace('-selection-v2', '').replace('-selection', '').replace('-scene', '')
        ident = 'guard-' + key if role else key
        canon = appearance.get(key, {})
        identity = '; '.join(v for k, v in canon.items() if k in ('Recognisable features', 'Appearance', 'Usual portrait styling, not today’s outfit'))
        if role:
            identity = organisation_guards.APPEARANCES.get(key, '')
        note = notes[audit[rel]['id']]
        original = OUT / 'originals' / (ident + '.png')
        shutil.copy2(path, original)
        row = dict(id=ident, character=key, role=role, path=rel, audit_id=audit[rel]['id'],
                   original='originals/' + ident + '.png', old_sha256=digest(path),
                   identity=identity, observed=note['observed'], required_change=note['required_change'],
                   status='carried-forward' if rel in pilot else 'pending')
        if rel in pilot:
            row['pilot_evidence'] = '../artwork-batch-01/manifest.json'
            row['review'] = pilot[rel]['visual_review']
            shutil.copy2(path, OUT / 'candidates' / (ident + '.png'))
        row['prompt'] = (
            'Use case: identity-preserve. Produce ONE contemporary character master for Mysterious Hearts, MH-013 Stage 2. '
            f'Subject: {key}. Image 1 is the exact IDENTITY, costume, age, body and markings reference to edit. '
            'Images 2 and 3 (Ivan and Charles) define SEMI-REALISTIC ILLUSTRATED MANHWA RENDERING ONLY, never their faces, bodies or clothes. '
            f'Identity and outfit locks: {identity or note["observed"]}. Source-specific observations: {note["observed"]}. '
            f'Required corrections: {note["required_change"]}. '
            'Preserve this individual\'s recognisable face, age, skin tone, body shape, hairstyle, eye colour, accessories, scars/tattoos and clothing colours/design. '
            'Model natural-size eyelids, nose bridge/tip, cheek turns and lips with soft plus deliberate shaped shading and selective tapered lines like the anchors. '
            'Retain older faces and body diversity; no de-ageing, idol-face substitution, needle chin or huge anime eyes. '
            'Neutral relaxed standing portrait, with the source expression and complete natural visible hands (or naturally pocketed hands if source). '
            'Construct anatomically connected head, torso, pelvis and BOTH THIGHS through TRUE MID-THIGH with substantial thigh length below crotch, NO KNEES. '
            'For skirts show a short visible section of connected thighs under the hem and stop at mid-thigh, never floating hems or knee-length framing. '
            'Do not stretch the old torso or pad a bust with empty canvas. '
            'Vertical 2:3, 1024x1536 RGBA PNG. Figure about 90% height, 4% clear headroom, full hairstyle/shoulders/arms/hands/props inside edges, small margin below clean thigh cutoff. '
            'Genuine clear alpha around and within silhouette. No background, haze rectangle, ground shadow, white outline, checkerboard, lettering, signature or watermark. '
            'Illustration, not photograph or 3D. '
            + ('Preserve opaque masks, faction symbols, weapons and mechanical anatomy exactly where present. Do not reveal a masked identity. Keep established local power colours subtle and subordinate; no new equipment or power. ' if role or key == 'crow' else 'No combat pose, weapons not present in source, or magical effects. ')
        )
        rows.append(row)
    priority = ['april', 'arthur-finch', 'beatrice-cole', 'amy', 'garrett', 'rei', 'sophie', 'samantha', 'yuriko', 'maya', 'leo', 'noah', 'iris', 'june', 'theo']
    rows.sort(key=lambda r: (0, priority.index(r['id'])) if r['id'] in priority else (1, r['role'], r['id']))
    write(OUT / 'roster.json', dict(roadmap_id='MH-013', stage=2, recorded='2026-11-10',
          scope='89 contemporary characters and 18 guard roles; Richter cybernetic form remains a Stage 4 context variant.', assets=rows))
    write(OUT / 'before-state.json', {r['path']: digest(ROOT / r['path']) for r in baseline})
    write(OUT / 'reviews.json', {})
    print(f'{len(rows)} masters; {sum(r["status"] == "carried-forward" for r in rows)} carried forward; {sum(r["status"] == "pending" for r in rows)} to generate.')


def panel(path, colour, width, height):
    with Image.open(path) as source:
        im = source.convert('RGBA')
        im.thumbnail((width, height), Image.Resampling.LANCZOS)
    frame = Image.new('RGBA', (width, height), colour)
    frame.alpha_composite(im, ((width-im.width)//2, height-im.height))
    return frame.convert('RGB')


def sheets(ids, source=False):
    rows = {r['id']: r for r in read(OUT / 'roster.json')['assets']}
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 19)
    board = Image.new('RGB', (1024, 480 * len(ids)), '#18232b')
    draw = ImageDraw.Draw(board)
    for i, ident in enumerate(ids):
        row = rows[ident]
        path = OUT / (row['original'] if source else 'candidates/' + ident + '.png')
        draw.text((10, i*480+5), ident + (' | SOURCE' if source else ' | old / new: slate, middle, light diagnostic'), fill='#e9e4dc', font=font)
        for j, colour in enumerate(('#273744', '#273744', '#647c87', '#e6e3dd')):
            item = OUT / row['original'] if j == 0 else path
            board.paste(panel(item, colour, 256, 440), (j*256, i*480+36))
    target = OUT / (('source-' if source else 'review-') + ids[0] + '.jpg')
    board.save(target, quality=94)
    print(target)


def register(ident, record_path):
    record = read(Path(record_path))
    path = Path(record['generated_source'])
    with Image.open(path) as im:
        im.load()
        alpha = im.getchannel('A') if im.mode == 'RGBA' else None
        if im.mode != 'RGBA' or im.size != (1024, 1536) or alpha.getextrema()[0] != 0:
            raise SystemExit(f'Invalid generated format {ident}: {im.mode} {im.size}')
    shutil.copy2(path, OUT / 'candidates' / (ident + '.png'))
    print(ident, digest(path))


def queue():
    """Prepare a small group for the built-in image tool; makes no API calls."""
    rows = [r for r in read(OUT / 'roster.json')['assets']
            if not (OUT / 'candidates' / (r['id'] + '.png')).exists()][:3]
    jobs = []
    for row in rows:
        refs = [str(OUT / row['original']), str(ROOT / 'assets/portraits/minsu-selection.png'),
                str(ROOT / 'assets/portraits/ivan-selection.png'), str(ROOT / 'assets/portraits/charles-selection-v2.png')]
        prompt = (
            f"Use case: stylized-concept. Draw ONE contemporary head-to-MID-THIGH character master: {row['id']}. "
            "First reference is exact identity, age, complexion, hair, physique, clothing and details. Retain these. "
            "Other references define semi-realistic ILLUSTRATED MANHWA rendering and thigh length only, not their identities. "
            f"Identity: {row['identity'] or row['observed']}. Source: {row['observed']}. Required: {row['required_change']}. "
            "NEW anatomical composition, camera zoomed back: whole hairstyle with clear headroom, shoulders, arms, complete hands, pelvis and BOTH LEGS TO MIDDLE OF THIGHS. "
            "In 1024x1536 place crown around y60, chin y280, waist y820, crotch y1080, relaxed fingertips y1250, mid-thigh cutoff y1500. "
            "Substantial 350-400px thigh length BELOW crotch; no knees. Not a hip crop. No torso stretching or padding a bust. "
            "Natural pocketed hands allowed. Dimensional natural-size eyes and eyelids, nose bridge/tip, cheek turns, lips; softly modelled transitions with selective shaped shadows. "
            "No shorthand line nose, huge anime eyes, needle chin or outlined white tooth bar. Retain distinct faces, age, body diversity, hair texture and fantasy/mechanical anatomy. "
            "Exact existing clothing, accessories, tattoos/scars and gear, no costume redesign. Trousers and overalls remain full-length garments cut by frame, not shorts. "
            "Aprons over practical dark trousers; existing skirts/shorts keep design. 2:3 RGBA PNG 1024x1536; genuine clear alpha around/within silhouette, safe head and side margins. "
            "No background, haze, glow, floor, scenery, border, text, watermark or signature; not photo/3D. "
            "Masked roles retain opaque masks and source equipment/powers without revealing concealed identity; civilian art has no new effects."
        )
        jobs.append(dict(id=row['id'], prompt=prompt, input_images=refs))
    write(OUT / 'next-jobs.json', jobs)
    if rows: sheets([r['id'] for r in rows], True)
    print(json.dumps([dict(id=r['id'], identity=r['identity'], observed=r['observed']) for r in rows]))


def corrections(ids):
    """Freeze reviewed drafts and prepare targeted edits, without pixel changes."""
    fixes = read(OUT / 'corrections.json')
    jobs = []
    for ident in ids:
        records = sorted((OUT / 'generations').glob(ident + '-[0-9][0-9].json'))
        number = int(records[-1].stem[-2:]) + 1
        previous = OUT / 'generations' / (ident + f'-{number-1:02d}.png')
        if not previous.exists():
            shutil.copy2(OUT / 'candidates' / (ident + '.png'), previous)
        prompt = (
            f'Use case: identity-preserve. Targeted correction of {ident}. Image 1 is the edit target. '
            'Preserve exact individual face, identity, age, complexion, build, hair, expression, clothing design/colours, accessories, tattoo motifs/laterality, pose and illustrated semi-realistic manhwa rendering. '
            + fixes[ident] + ' '
            'Do not stretch anatomy or redesign any unaffected details. Complete all visible hands, hair and required props inside frame. '
            'Output 1024x1536 2:3 RGBA with genuine transparent background and clear gaps, no scenery, halo, outline, text or watermark. '
            'Clear headroom and side margins, small transparent bottom margin; no knees. '
        )
        jobs.append(dict(id=ident, record_id=ident+f'-{number:02d}', prompt=prompt, input_images=[str(previous)]))
    write(OUT / 'next-jobs.json', jobs)
    print([j['record_id'] for j in jobs])


def identity_sheets():
    """Compare original and candidate pixels; these boards are not game assets."""
    reviews = read(OUT / 'reviews.json')
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
    small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 17)
    for row in read(OUT / 'roster.json')['assets']:
        candidate = OUT / 'candidates' / (row['id'] + '.png')
        if not candidate.exists(): continue
        board = Image.new('RGB', (1200, 1200), '#18232b')
        draw = ImageDraw.Draw(board)
        draw.text((20, 12), f"MH-013 Stage 2 | {row['id']} | {row['audit_id']}", font=font, fill='#e9e4dc')
        draw.text((20, 48), 'SOURCE / CONTEMPORARY MASTER / FACE DETAIL', font=small, fill='#bac6d2')
        board.paste(panel(OUT / row['original'], '#273744', 400, 720), (0, 84))
        board.paste(panel(candidate, '#273744', 400, 720), (400, 84))
        with Image.open(candidate) as im:
            detail = im.convert('RGBA').crop((160, 0, 864, 720))
            detail.thumbnail((400, 500), Image.Resampling.LANCZOS)
            tile = Image.new('RGBA', (400,720), '#273744')
            tile.alpha_composite(detail, ((400-detail.width)//2, 0))
            board.paste(tile.convert('RGB'), (800,84))
        presentation = OUT / 'checks/presentation-review.json'
        reviewed = presentation.exists() and read(presentation).get('accepted')
        status = ('Pilot carried forward' if row['status']=='carried-forward' else 'Offline artwork accepted') + ('; staged presentation reviewed' if reviewed else '; presentation pending')
        findings = reviews.get(row['id'], {}).get('findings', row.get('review', 'Review pending.'))
        lines = [status, '', 'IDENTITY: '+(row['identity'] or row['observed']), '', 'REVIEW: '+findings]
        y = 825
        for line in lines:
            for part in textwrap.wrap(line, 120) or ['']:
                draw.text((20,y),part,font=small,fill='#e9e4dc'); y += 23
        board.save(OUT / 'identity-sheets' / (row['id']+'.jpg'), quality=94)


def presentation_sheets():
    """Offline inspection boards; never used as portrait assets."""
    names = [n for n in read(OUT/'checks/presentation-render.json')['screenshots'] if not n.startswith('loader-')]
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    for start in range(0, len(names), 6):
        board = Image.new('RGB', (1280,1350), '#18232b')
        draw = ImageDraw.Draw(board)
        for i, name in enumerate(names[start:start+6]):
            x, y = (i%2)*640, (i//2)*450
            draw.text((x+8,y+4),name,fill='#e9e4dc',font=font)
            with Image.open(OUT/'screenshots'/name) as im:
                im.thumbnail((640,420))
                board.paste(im,(x,y+30))
        board.save(OUT/f'presentation-{start//6+1:02d}.jpg',quality=95)


def verify():
    roster = read(OUT / 'roster.json')
    reviews = read(OUT / 'reviews.json')
    accepted, pending, technical_errors = [], [], {}
    carry = read(OUT/'carried-forward-updates.json') if (OUT/'carried-forward-updates.json').exists() else {}
    expected_updates = {v['source']:v['sha256'] for v in carry.values()}
    installation = read(OUT/'height-review/installation.json') if (OUT/'height-review/installation.json').exists() else None
    if installation:
        # The requested height follow-up installed only the accepted default
        # masters. Validate its exact hashes/backups; never permit arbitrary art.
        for installed in installation['assets']:
            assert digest(OUT/installed['candidate']) == installed['installed_sha256'], installed['id']
            if installed.get('backup'):
                assert digest(ROOT/installed['backup']) == installed['before_sha256'], installed['id']
            expected_updates[installed['path']] = installed['installed_sha256']
    live_differences = []
    for path, old_hash in read(OUT/'before-state.json').items():
        current = digest(ROOT/path)
        if current != old_hash:
            live_differences.append(dict(path=path, before_sha256=old_hash, current_sha256=current))
            if expected_updates.get(path) != current:
                technical_errors[path] = ['Unexpected live asset change since Stage 2 start; investigate, never overwrite']
    for row in roster['assets']:
        assert digest(OUT / row['original']) == row['old_sha256'], row['id']
        candidate = OUT / 'candidates' / (row['id'] + '.png')
        if not candidate.exists():
            pending.append(row['id'])
            continue
        if row['status'] == 'carried-forward':
            expected = carry.get(row['id'], {}).get('sha256', row['old_sha256'])
            row['generation_record'] = carry.get(row['id'], {}).get('evidence', row['pilot_evidence'])
        else:
            records = sorted((OUT/'generations').glob(row['id']+'-[0-9][0-9].json'))
            assert records, row['id']
            record = read(records[-1])
            expected = digest(Path(record['generated_source']))
            row['generation_record'] = records[-1].relative_to(OUT).as_posix()
        assert digest(candidate) == expected, 'Candidate differs from generated/carried source: '+row['id']
        row['candidate'] = candidate.relative_to(OUT).as_posix()
        row['identity_sheet'] = 'identity-sheets/'+row['id']+'.jpg'
        with Image.open(candidate) as im:
            im.load()
            if im.mode != 'RGBA' or im.size != (1024,1536):
                technical_errors[row['id']] = [f'Expected RGBA 1024x1536; got {im.mode} {im.size}']
                pending.append(row['id'])
                continue
            a = im.getchannel('A'); h = a.histogram(); total = sum(h)
            clear, solid = sum(h[:8])/total, sum(h[220:])/total
            bounds = a.point(lambda v: 255 if v >= 16 else 0).getbbox()
            issues = []
            if not (h[0] and clear > .10 and solid > .15 and a.getextrema()[1] >= 250):
                issues.append('Insufficient clear background or solid figure alpha')
            if not (bounds and bounds[0] > 0 and bounds[1] > 0 and bounds[2] < im.width):
                issues.append(f'Silhouette touches top/side edge: {bounds}')
            if issues:
                technical_errors[row['id']] = issues
                pending.append(row['id'])
                continue
            row.update(new_sha256=digest(candidate), size=list(im.size), alpha_extrema=list(a.getextrema()),
                       clear_fraction=round(clear,5), solid_fraction=round(solid,5), visible_bbox=bounds)
        review = reviews.get(row['id'])
        if row['status'] == 'carried-forward' or review and review.get('accepted'):
            if review: row['review'] = review
            accepted.append(row)
        else: pending.append(row['id'])
    presentation = read(OUT/'checks/presentation-review.json') if (OUT/'checks/presentation-review.json').exists() else {}
    presentation_status = 'Staged preview accepted; live integration remains Stage 5' if presentation.get('accepted') else 'pending'
    if installation:
        presentation_status = 'Default masters installed with stature correction; see height-review/README.md. Wardrobe/context stages remain pending.'
    write(OUT / 'manifest.json', dict(roadmap_id='MH-013', stage=2, recorded=roster['recorded'],
          verified_at_utc=datetime.now(timezone.utc).isoformat(),
          total=len(roster['assets']), offline_accepted=len(accepted), presentation=presentation_status, pending=pending,
          live_differences_from_start=live_differences, carried_forward_updates=carry,
          default_master_installation='height-review/installation.json' if installation else None,
          generated_masters=sum(r['status']!='carried-forward' for r in roster['assets']),
          generation_records=len(list((OUT/'generations').glob('*.json'))),
          technical_errors=technical_errors, assets=accepted,
          pixel_postprocessing='None; generated PNGs copied byte-for-byte.',
          generator='Built-in image_gen; exact model identity not exposed'))
    print(f'{len(accepted)}/{len(roster["assets"])} offline accepted; {len(pending)} pending; presentation: {presentation_status}.')
    print(f'{len(live_differences)} separately evidenced live update(s); generated/carried source hashes verified.')
    for ident, issues in technical_errors.items(): print(ident + ': ' + '; '.join(issues))
    if technical_errors: raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('prepare','sources','sheets','register','verify','identity-sheets','queue','corrections','presentation-sheets'))
    parser.add_argument('items', nargs='*')
    args = parser.parse_args()
    if args.command == 'prepare': prepare()
    elif args.command in ('sources','sheets'): sheets(args.items, args.command == 'sources')
    elif args.command == 'register': register(*args.items)
    elif args.command == 'identity-sheets': identity_sheets()
    elif args.command == 'queue': queue()
    elif args.command == 'corrections': corrections(args.items)
    elif args.command == 'presentation-sheets': presentation_sheets()
    else: verify()
