"""Install Neo and Alyssa's authored Grove photos without replacing old posts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / 'assets/grove/posts.json'
    posts = json.loads(path.read_text(encoding='utf-8'))
    keys = {p['key'] for p in posts}
    for author in ('neo', 'alyssa'):
        plan = json.loads((ROOT / 'assets/grove' / author / 'generation-prompts.json').read_text(encoding='utf-8'))
        for i, item in enumerate(plan['images']):
            key = author + ':' + item['slug']
            if key in keys:
                continue
            image = f'assets/grove/{author}/{item["slug"]}.png'
            if not (ROOT / image).is_file():
                raise FileNotFoundError(image)
            posts.append(dict(key=key, author=author, image=image,
                              published_at=f'2049-{9 + i // 3:02d}-{5 + i % 3 * 8 + (author == "alyssa"):02d}T18:30',
                              caption=item['caption'], engagement_basis_points=700 + i * 70,
                              comments=item['comments']))
            keys.add(key)
    path.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
