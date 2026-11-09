"""Install Sylvanis's authored Grove archive; safe to rerun."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPTIONS = [
    'Round three. The hesitation was worth the price of admission.',
    'The bell is impartial. The room is not.',
    'A small consideration. Do make the next round interesting.',
    'Please. Take the empty seat.',
    'Midnight. Everyone arrived with something to lose.',
    'Your copy remains sealed. How considerate of me.',
    'Two chairs. I have left you the choice.',
    'Thirteen. I could have watched another.',
]
COMMENTS = {
    0: 'The round was over. Leave it there.',
    2: 'They came here to box.',
    5: 'This is not a conversation for here.',
    7: 'They were finished. You heard the bell.',
}


def main():
    path = ROOT / 'assets/grove/posts.json'
    posts = json.loads(path.read_text(encoding='utf-8'))
    plan = json.loads((ROOT / 'assets/grove/sylvanis/generation-prompts.json').read_text(encoding='utf-8'))
    keys = {p['key'] for p in posts}
    for i, item in enumerate(plan['images']):
        key = 'sylvanis:' + item['slug']
        if key in keys:
            continue
        comments = [dict(author='ivan', text=COMMENTS[i], delay_minutes=43 + i * 17)] if i in COMMENTS else []
        posts.append(dict(key=key, author='sylvanis',
            image='assets/grove/sylvanis/' + item['slug'] + '.png',
            published_at=f'2049-{9 + i // 3:02d}-{6 + (i % 3) * 9:02d}T{20 + i % 4:02d}:13',
            caption=CAPTIONS[i], engagement_basis_points=[920, 560, 740, 680, 430, 510, 390, 1080][i],
            comments=comments))
    path.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
