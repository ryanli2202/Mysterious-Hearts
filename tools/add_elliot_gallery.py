"""Install the authored Elliot gallery catalog entries (safe to rerun)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPTIONS = [
    'first round of the boardwalk. just me and the early shift.',
    'same fishing spot three mornings running. fair enough.',
    'twenty minutes of reeds. one very loud frog.',
    'three herons. none of them willing to help with the shavings.',
    'took the long way back. water was too good.',
    'rain on the porch roof. staying here a bit.',
    'finished this little one before the light went.',
    'batteries charged. remembered the pencil this time.',
]
COMMENTS = [
    'That light was worth getting up for.',
    'Better patience than either of us.',
    'Send me the frog take. I want to hear the interruption.',
    'The one on the right looks ready to leave.',
    'Good day to take your time.',
    'That roof must sound good in the rain.',
    'You got the tilt of its head just right.',
    'Spare batteries too. Learned that one the hard way.',
]


def main():
    path = ROOT / 'assets/grove/posts.json'
    posts = json.loads(path.read_text(encoding='utf-8'))
    plan = json.loads((ROOT / 'assets/grove/elliot/generation-prompts.json').read_text(encoding='utf-8'))
    keys = {p['key'] for p in posts}
    for i, item in enumerate(plan['images']):
        key = 'elliot:' + item['slug']
        if key in keys:
            continue
        posts.append(dict(key=key, author='elliot',
            image='assets/grove/elliot/' + item['slug'] + '.png',
            published_at=f'2049-{9 + i // 3:02d}-{5 + (i % 3) * 9:02d}T{8 + i:02d}:24',
            caption=CAPTIONS[i], engagement_basis_points=[650, 480, 720, 890, 810, 560, 1040, 430][i],
            comments=[dict(author='ivan', text=COMMENTS[i], delay_minutes=31 + i * 17)]))
    path.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
