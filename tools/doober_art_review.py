"""Build review sheets from bundled assets without modifying source artwork."""
from pathlib import Path
import json
from PIL import Image, ImageOps, ImageDraw
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root/'assets/doober/manifest.json').read_text())
for index, (restaurant, items) in enumerate(manifest['items'].items()):
    sheet = Image.new('RGB', (1200, 1040), '#141c28')
    draw = ImageDraw.Draw(sheet)
    for n, item in enumerate(items.values()):
        x, y = n % 5 * 240, n // 5 * 260
        path = root / item['image']
        if path.exists():
            with Image.open(path) as source:
                thumb = ImageOps.contain(source.convert('RGB'), (230, 230))
                sheet.paste(thumb, (x + (240-thumb.width)//2, y))
        draw.text((x+5, y+235), item['name'], fill='#edf0f8')
    sheet.save(root/f'tests/screenshots/doober-art-review-{index}.jpg')
