"""Reproducible MH-013 pilot inventory and offline inspection composites.

Does not edit portrait pixels. Run before installation, then with --installed.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'roadmap/artwork-batch-01'
PATHS = {
    'ivan-selection': 'assets/portraits/ivan-selection.png',
    'charles-selection-v2': 'assets/portraits/charles-selection-v2.png',
    'emily-selection': 'assets/portraits/emily-selection.png',
    'minsu-selection': 'assets/portraits/minsu-selection.png',
    'priya-shah-selection': 'assets/portraits/priya-shah-selection.png',
    'otis-bell-selection': 'assets/portraits/otis-bell-selection.png',
    'guard-clubs': 'assets/portraits/guards/clubs.png',
    'combat-ivan': 'assets/portraits/combat/ivan.png',
}
REVIEWS = {
    'ivan-selection': 'Freckles, grey-green eyes, ash-brown hair, studs, chain and tailoring retained. Pelvis and both trouser thighs constructed; hands naturally pocketed.',
    'charles-selection-v2': 'Amber eyes, right-cheek mark, hoops, chain and black jacket retained. Full hairstyle and both trouser thighs; no change to opaque unversioned source.',
    'emily-selection': 'Latest style refinement uses simpler matte skin/fabric shading while retaining detailed blonde strands and highlights per user direction. Mid-thigh framing, short connected thigh sections with no knees, round glasses, blue eyes, embroidered pinafore and complete clasped hands retained.',
    'minsu-selection': 'Friendly smile with modelled lips, softer cheeks, dark hair, bomber and tee retained. Second framing pass extends both thighs substantially below crotch; pocketed hands.',
    'priya-shah-selection': 'Age 38, medium-brown complexion, low bun, rectangular glasses, beauty mark, oval earrings, plum cardigan and teal blouse retained. Complete clasped hands and dark trouser thighs.',
    'otis-bell-selection': 'Age 67, broad build, silver hair/beard, blue eyes, weathering and rust/navy workwear retained. Complete hands. Second framing pass provides substantive trouser thighs.',
    'guard-clubs': 'Opaque visor/mask, white and gold club symbols, olive trim, armour, pouches, holster, downward pistol and green hand energy retained. No face exposed; both gloves complete.',
    'combat-ivan': 'Accepted civilian likeness and outfit carried into fighting stance. Both open hands, pelvis and thighs intact; orange flame, cyan ice, silver wind and red/blue arcs retained and contained.',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def panel(path, colour, width=256, height=384):
    with Image.open(path) as source:
        im = source.convert('RGBA')
        im.thumbnail((width, height), Image.Resampling.LANCZOS)
    result = Image.new('RGBA', (width, height), colour)
    result.alpha_composite(im, ((width-im.width)//2, height-im.height))
    return result.convert('RGB')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--installed', action='store_true')
    args = parser.parse_args()
    baseline = json.loads((ROOT/'roadmap/artwork-portrait-audit/inventory.json').read_text(encoding='utf-8'))
    originals = {row['path']: row for row in baseline['assets']}
    records = json.loads((BATCH/'generation-records.json').read_text(encoding='utf-8'))
    assets = []
    for ident, path in PATHS.items():
        old, new = BATCH/'originals'/f'{ident}.png', BATCH/'candidates'/f'{ident}.png'
        assert digest(old) == originals[path]['sha256'], ('baseline changed', path)
        with Image.open(new) as im:
            im.load()
            assert im.mode == 'RGBA' and im.size == (1024, 1536), ident
            alpha = im.getchannel('A')
            hist = alpha.histogram()
            clear, solid = sum(hist[:8])/sum(hist), sum(hist[220:])/sum(hist)
            assert hist[0] and clear > .10 and solid > .15 and alpha.getextrema()[1] >= 250, ident
            bounds = alpha.point(lambda v: 255 if v >= 16 else 0).getbbox()
            assert bounds[0] > 0 and bounds[1] > 0 and bounds[2] < im.width, (ident, bounds)
            assets.append(dict(id=ident, audit_id=originals[path]['id'], path=path,
                               original=f'originals/{ident}.png', candidate=f'candidates/{ident}.png',
                               old_sha256=digest(old), new_sha256=digest(new), size=list(im.size),
                               alpha_extrema=list(alpha.getextrema()), clear_fraction=round(clear,5),
                               solid_fraction=round(solid,5), visible_bbox=bounds,
                               visual_review=REVIEWS[ident],
                               style_references=['originals/ivan-selection.png','originals/charles-selection-v2.png']))
        if args.installed:
            assert digest(ROOT/path) == digest(new), ('installed mismatch', path)
    changed = [row['path'] for row in baseline['assets'] if digest(ROOT/row['path']) != row['sha256']]
    if args.installed:
        assert set(changed) == set(PATHS.values()), ('unexpected baseline changes', changed)
    manifest = dict(roadmap_id='MH-013', batch=1, recorded='2026-11-10',
                    installed=args.installed, generator='Built-in image_gen; exact model identity not exposed',
                    generation_records='generation-records.json', generation_count=len(records),
                    pixel_postprocessing='None; originals from image_gen copied byte-for-byte.',
                    baseline_count=baseline['count'], changed_baseline_paths=changed, assets=assets)
    (BATCH/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
    ids = list(PATHS)
    contact = Image.new('RGB',(1024,832),'#18232b')
    draw = ImageDraw.Draw(contact)
    for i, ident in enumerate(ids):
        x, y = (i%4)*256, (i//4)*416
        contact.paste(panel(BATCH/'candidates'/f'{ident}.png','#273744'),(x,y+32))
        draw.text((x+8,y+7),ident,fill='#e9e4dc',font=font)
    contact.save(BATCH/'contact-sheet.jpg',quality=95)
    for page in range(2):
        compare = Image.new('RGB',(1536,840),'#18232b')
        alpha_sheet = Image.new('RGB',(768,1664),'#18232b')
        cdraw, adraw = ImageDraw.Draw(compare), ImageDraw.Draw(alpha_sheet)
        for i, ident in enumerate(ids[page*4:page*4+4]):
            x, y = (i%2)*768, (i//2)*420
            cdraw.text((x+8,y+7),ident+' | BEFORE / AFTER',fill='#e9e4dc',font=font)
            compare.paste(panel(BATCH/'originals'/f'{ident}.png','#273744',384,384),(x,y+32))
            compare.paste(panel(BATCH/'candidates'/f'{ident}.png','#273744',384,384),(x+384,y+32))
            adraw.text((8,i*416+7),ident+' | slate / middle / light diagnostic',fill='#e9e4dc',font=font)
            for j, colour in enumerate(('#273744','#647c87','#e6e3dd')):
                alpha_sheet.paste(panel(BATCH/'candidates'/f'{ident}.png',colour),(j*256,i*416+32))
        compare.save(BATCH/f'before-after-{page+1}.jpg',quality=95)
        alpha_sheet.save(BATCH/f'alpha-review-{page+1}.jpg',quality=95)
    print(f'{len(assets)} RGBA 1024x1536 portraits verified; {len(records)} generations; installed={args.installed}; {len(changed)} baseline files changed.')


if __name__ == '__main__':
    main()
