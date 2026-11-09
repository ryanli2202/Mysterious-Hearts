"""Rebuild original, soft arcade effects using only Python's standard library."""
from pathlib import Path
import math
import random
import struct
import wave

ROOT = Path(__file__).resolve().parents[1] / 'assets' / 'sounds' / 'arcade'
NOTES = {
    'tap': (440,), 'flip': (600, 800), 'card': (360, 480), 'drop': (220, 140),
    'slide': (330, 440), 'merge': (523, 659, 784), 'eat': (880, 1175),
    'rotate': (440, 587), 'clear': (523, 659, 784, 1047), 'bounce': (740,),
    'score': (659, 880), 'win': (523, 659, 784, 1047, 1319),
    'lose': (392, 330, 262, 196), 'match': (587, 740, 880),
    'reveal': (660,), 'invalid': (180,), 'brick': (980, 660),
    'note0': (262,), 'note1': (330,), 'note2': (392,), 'note3': (523,),
}


def build():
    ROOT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(21)
    for name, notes in NOTES.items():
        duration = .37 if name.startswith('note') else .10 if name in ('win', 'lose') else .055
        rate = 22050
        frames = bytearray()
        for frequency in notes:
            count = int(duration * rate)
            for i in range(count):
                t = i / rate
                envelope = min(1, i / (rate * .006)) * min(1, (count - i) / (rate * .025))
                tone = math.sin(2 * math.pi * frequency * t) + .18 * math.sin(4 * math.pi * frequency * t)
                if name in ('card', 'flip', 'brick'): tone += .15 * rng.uniform(-1, 1)
                frames.extend(struct.pack('<h', int(6500 * envelope * tone)))
        with wave.open(str(ROOT / f'{name}.wav'), 'wb') as audio:
            audio.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
            audio.writeframes(frames)


if __name__ == '__main__':
    build()
    print(f'Built {len(NOTES)} original arcade effects.')
