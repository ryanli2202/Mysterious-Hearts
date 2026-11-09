"""Install Valentina's authored Grove archive; safe to rerun."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPTIONS = [
    'Boats ready. Hair doing its own weather forecast.',
    'Light breeze, clear water. Took one extra lap before the lesson.',
    'My brother has been promoted to holding the sail still. Excellent work so far.',
    'Coffee first. Knot check second. Launch third.',
    'He gets the first verse. I get the loud one.',
    'Sail off the table. Soup on the table. We can negotiate.',
    'Secondhand hull. A lot of sanding. Ready for someone\'s first sail.',
    'Last boat tied up. Evening officially mine.',
]
COMMENTS = [
    'The boats look more prepared than your hair.',
    'One extra lap is what you said last time too.',
    'I would like my excellent work recorded in the family minutes.',
    'And then you check the knot I tied again.',
    'You took the chorus as well. And most of my verse.',
    'The soup had to apply for that table space.',
    'I remember the day we brought that hull home. Look at it now.',
    'Dinner is at seven. No sailcloth on your chair this time.',
]


def main():
    path = ROOT / 'assets/grove/posts.json'
    posts = json.loads(path.read_text(encoding='utf-8'))
    plan = json.loads((ROOT / 'assets/grove/valentina/generation-prompts.json').read_text(encoding='utf-8'))
    keys = {p['key'] for p in posts}
    for i, item in enumerate(plan['images']):
        key = 'valentina:' + item['slug']
        if key in keys:
            continue
        posts.append(dict(key=key, author='valentina',
            image='assets/grove/valentina/' + item['slug'] + '.png',
            published_at=f'2049-{9 + i // 3:02d}-{3 + (i % 3) * 10:02d}T{10 + i:02d}:32',
            caption=CAPTIONS[i], engagement_basis_points=[730, 850, 1150, 480, 1320, 1090, 690, 810][i],
            comments=[dict(author='ivan', text=COMMENTS[i], delay_minutes=19 + i * 11)]))
    path.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
