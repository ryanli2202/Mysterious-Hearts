"""Rebuild MH-013 inspection sheets and metadata; never edits source artwork."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)


def main():
    paths = sorted((ROOT / 'assets/portraits').rglob('*.png'))
    paths += [ROOT / p for p in (
        'assets/profiles/charles-v2.png', 'assets/profiles/crow.png',
        'assets/grove/garrett/appearance-reference.png',
        'assets/grove/garrett/arm-tattoo-reference.png',
        'assets/grove/rei/appearance-reference.png',
        'assets/grove/rei/tattoo-reference.png')]
    # This is an immutable planning baseline. A later production audit needs
    # a new directory instead of silently changing A001-A306 or their evidence.
    previous = OUT / 'inventory.json'
    if previous.exists():
        baseline = json.loads(previous.read_text(encoding='utf-8'))['assets']
        current_paths = [p.relative_to(ROOT).as_posix() for p in paths]
        if current_paths != [r['path'] for r in baseline]:
            raise SystemExit('Baseline file set changed; create a new audit directory.')
        for path, row in zip(paths, baseline):
            if sha256(path.read_bytes()).hexdigest() != row['sha256']:
                raise SystemExit(f'Baseline source changed: {row["path"]}; preserve this audit.')
    rows = []
    for i, path in enumerate(paths):
        with Image.open(path) as source:
            im = source.convert('RGBA')
            alpha = im.getchannel('A')
            hist = alpha.histogram()
            row = dict(id=f'A{i+1:03}', path=path.relative_to(ROOT).as_posix(),
                       size=list(im.size), source_mode=source.mode,
                       alpha_min=alpha.getextrema()[0],
                       transparent_fraction=round(hist[0]/(im.width*im.height), 4),
                       partial_alpha_fraction=round(sum(hist[1:255])/(im.width*im.height), 4),
                       alpha_bbox=list(alpha.getbbox()) if alpha.getbbox() else None,
                       sha256=sha256(path.read_bytes()).hexdigest(),
                       sheet=f'review-{i//12+1:02}.jpg')
            rows.append(row)
    for start in range(0, len(rows), 12):
        board = Image.new('RGB', (1280, 1320), '#182233')
        draw = ImageDraw.Draw(board)
        for n, row in enumerate(rows[start:start+12]):
            x, y = (n % 4) * 320, (n // 4) * 440
            draw.rectangle((x+3,y+3,x+316,y+436), outline='#536175')
            label = row['id'] + ' ' + row['path'].replace('assets/portraits/', '')
            draw.text((x+9,y+8), label[:42], font=FONT, fill='#f0d6a0')
            if len(label)>42: draw.text((x+9,y+27), label[42:], font=FONT, fill='#f0d6a0')
            with Image.open(ROOT / row['path']) as source:
                im = source.convert('RGBA')
                # Display complete canvas: do not hide original clipping or margins.
                im = ImageOps.contain(im, (300, 372))
                board.paste(im, (x+(320-im.width)//2, y+53+(372-im.height)//2), im)
            draw.text((x+9,y+420), f"{row['size']} alpha min {row['alpha_min']}", font=FONT, fill='#bdc8d8')
        board.save(OUT / rows[start]['sheet'], quality=94)
    (OUT / 'inventory.json').write_text(json.dumps(dict(
        recorded='2026-11-10', method='File metadata and complete-canvas slate inspection sheets; visual findings are in PORTRAIT_AUDIT.md.',
        count=len(rows), assets=rows), indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(count=len(rows), sheets=(len(rows)+11)//12,
                         opaque=[r['path'] for r in rows if r['alpha_min']==255],
                         dimensions=dict(Counter(str(r['size']) for r in rows))), indent=2))


if __name__ == '__main__':
    main()
