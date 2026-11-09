"""Install Tyler's authored Grove archive; safe to rerun."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPTIONS = [
    'doors open at six. beat the alarm for once.',
    'patched up. back on the loaner shelf tomorrow.',
    'one whole song without catching the rope. then you pick the music.',
    'game on the radio. tiles on the table. decent afternoon.',
    'good round. same time thursday?',
    'dad said it was a practice hand. apparently only when i win.',
    'home before the first pitch. dinner sorted.',
    'got another hand in me. probably said that three hands ago.',
]
COMMENTS = [
    'You beat me to the gym. That is early.',
    'Someone will get their first round out of those.',
    'Brave offer. Some songs are seven minutes long.',
    'Which game are you calling today?',
    'Thursday works. I will bring my wraps.',
    'That smile says he had the winning tile for a while.',
    'Good timing. Hope the game was worth getting home for.',
    'That is how an afternoon disappears.',
]


def main():
    path = ROOT / 'assets/grove/posts.json'
    posts = json.loads(path.read_text(encoding='utf-8'))
    plan = json.loads((ROOT / 'assets/grove/tyler/generation-prompts.json').read_text(encoding='utf-8'))
    keys = {p['key'] for p in posts}
    for i, item in enumerate(plan['images']):
        key = 'tyler:' + item['slug']
        if key in keys:
            continue
        posts.append(dict(key=key, author='tyler',
            image='assets/grove/tyler/' + item['slug'] + '.png',
            published_at=f'2049-{9 + i // 3:02d}-{4 + (i % 3) * 10:02d}T{8 + i:02d}:18',
            caption=CAPTIONS[i], engagement_basis_points=[680, 450, 910, 590, 820, 1140, 520, 740][i],
            comments=[dict(author='ivan', text=COMMENTS[i], delay_minutes=24 + i * 13)]))
    path.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
