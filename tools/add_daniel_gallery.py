"""Install Daniel's authored Grove archive; safe to rerun."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPTIONS = [
    'Matinee checked. The projector is more awake than I am.',
    'Two reels. One very good reason to stay for the ending.',
    'The detective has a hat now. This counts as progress.',
    'Ten minutes before doors. Best sound in here is almost nothing.',
    'An evening spent learning how to meet the floor politely.',
    'My first double feature. Drew the cards too. Mum and Dad have seats.',
    'Keys downstairs. Jacket upstairs. Occasionally I remember which is which.',
    'Good film. Terrible final five minutes. Tea is helping.',
]
COMMENTS = [
    'Give it a coffee break after the second screening.',
    'I will stay. You can ask what I thought afterwards.',
    'The reflection under the streetlamp is good. Keep that.',
    'Save me an aisle seat when the doors open.',
    'The floor remains undefeated, then.',
    'You should be proud of those. What time does the first one start?',
    'At least the commute is short.',
    'You looked ready to rewrite the ending on the way out.',
]


def main():
    path = ROOT / 'assets/grove/posts.json'
    posts = json.loads(path.read_text(encoding='utf-8'))
    plan = json.loads((ROOT / 'assets/grove/daniel/generation-prompts.json').read_text(encoding='utf-8'))
    keys = {p['key'] for p in posts}
    for i, item in enumerate(plan['images']):
        key = 'daniel:' + item['slug']
        if key in keys:
            continue
        posts.append(dict(key=key, author='daniel',
            image='assets/grove/daniel/' + item['slug'] + '.png',
            published_at=f'2049-{9 + i // 3:02d}-{7 + (i % 3) * 9:02d}T{12 + i:02d}:16',
            caption=CAPTIONS[i], engagement_basis_points=[650, 470, 820, 540, 740, 1120, 430, 680][i],
            comments=[dict(author='ivan', text=COMMENTS[i], delay_minutes=27 + i * 13)]))
    path.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
