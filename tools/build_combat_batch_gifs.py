"""Slice generated MH-001 sheets and encode review GIFs; no gameplay integration."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageStat

ROOT = Path(__file__).resolve().parents[1]


def build(batch_number=1):
    batch = ROOT / f'assets/combat/animations/batch-{batch_number:02d}'
    manifest_path = batch / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    cols, rows = manifest['grid']['columns'], manifest['grid']['rows']
    durations = [manifest['frame_duration_ms']] * (cols * rows) + [manifest['blank_hold_ms']]
    sequences = []
    for asset in manifest['assets']:
        sheet_path = batch / asset['sheet']
        sheet = Image.open(sheet_path).convert('RGB')
        assert sheet.width % cols == 0 and sheet.height % rows == 0
        w, h = sheet.width // cols, sheet.height // rows
        frames = [sheet.crop((x*w, y*h, (x+1)*w, (y+1)*h))
                  for y in range(rows) for x in range(cols)]
        # Keep the generated pixels intact; use the sheet's corner colour for rest.
        matte = tuple(round(c) for c in ImageStat.Stat(sheet.crop((0, 0, 24, 24))).mean)
        frames.append(Image.new('RGB', (w, h), matte))
        palette = sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        encoded = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
        dest = batch / asset['gif']
        dest.parent.mkdir(parents=True, exist_ok=True)
        encoded[0].save(dest, save_all=True, append_images=encoded[1:],
                        duration=durations, loop=0, disposal=2, optimize=False)
        with Image.open(dest) as gif:
            assert gif.n_frames == 7 and gif.size == (w, h)
            assert gif.info.get('loop') == 0
            actual = []
            for i in range(gif.n_frames):
                gif.seek(i)
                gif.load()
                actual.append(gif.info['duration'])
            assert actual == durations
        asset['verification'] = {'sheet_dimensions': list(sheet.size),
            'gif_dimensions': [w, h], 'decoded_frames': 7,
            'action_frames': 6, 'duration_ms': sum(actual), 'action_duration_ms': sum(actual[:6]),
            'frame_durations_ms': actual, 'loop': 'infinite preview',
            'sha256_sheet': hashlib.sha256(sheet_path.read_bytes()).hexdigest(),
            'sha256_gif': hashlib.sha256(dest.read_bytes()).hexdigest()}
        sequences.append(frames)
    overview = []
    overview_height = ((len(sequences) + 2) // 3) * 352
    for frame_index in range(7):
        canvas = Image.new('RGB', (960, overview_height), '#101824')
        draw = ImageDraw.Draw(canvas)
        for i, (asset, frames) in enumerate(zip(manifest['assets'], sequences)):
            x, y = (i % 3)*320, (i // 3)*352
            draw.text((x+16, y+12), asset['name'].replace('-', ' ').title(), fill='#dbe8f5')
            canvas.paste(frames[frame_index].resize((320, 320), Image.Resampling.LANCZOS), (x, y+32))
        overview.append(canvas)
    palette_source = Image.new('RGB', (960, overview_height*7))
    for i, frame in enumerate(overview):
        palette_source.paste(frame, (0, overview_height*i))
    palette = palette_source.quantize(colors=256)
    overview_encoded = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in overview]
    overview_encoded[0].save(batch / f'batch-{batch_number:02d}-preview.gif', save_all=True,
        append_images=overview_encoded[1:], duration=durations, loop=0, disposal=2, optimize=False)
    overview[2].save(batch / f'batch-{batch_number:02d}-contact.png')
    manifest['status'] = f'{len(sequences)} local sprite sheets and GIFs assembled and structurally verified; runtime integration pending.'
    manifest['validation_command'] = f'python tools/build_combat_batch_gifs.py --batch {batch_number}'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(sequences)} sheets and GIFs; 7 decoded frames each; durations and dimensions match manifest and sheets.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=int, default=1)
    build(parser.parse_args().batch)
