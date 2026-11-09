"""Read the authored appearance document for dialogue and physical-type matching."""
from functools import lru_cache
from pathlib import Path

DOCUMENT = Path(__file__).with_name('Mysterious Hearts - Character Appearances.md')
DETAIL_FIELDS = ('hair', 'eyes', 'facial_features', 'body_type')


@lru_cache(maxsize=1)
def records():
    result = {}
    for section in DOCUMENT.read_text(encoding='utf-8').split('\n## ')[1:]:
        who, body = section.split('\n', 1)
        fields = {}
        for line in body.splitlines():
            if line.startswith('|'):
                cells = [cell.strip() for cell in line.strip('|').split('|')]
                if len(cells) == 2 and cells[0] not in ('Field', '---'):
                    fields[cells[0]] = cells[1]
        result[who] = fields
    import thirteen
    result['thirteen']={'Appearance':thirteen.APPEARANCE,'Height':'194 cm'}
    import the_crow
    result['crow'] = {'Appearance': the_crow.APPEARANCE, 'Height': 'Unknown'}
    import custom_protagonist
    return custom_protagonist.Registry(result, lambda p: {'Gender': p['gender'], 'Appearance': p['appearance'], 'Hairstyle': p['hairstyle'], 'Height': str(p['height']) + ' cm'})


def traits(who):
    row = records().get(who, {})
    return {key: tuple(row.get(key, '').split('; ')) if row.get(key) not in (None, '', 'Unspecified') else None
            for key in DETAIL_FIELDS}


def reference(who):
    row = records().get(who, {})
    return {key: value for key, value in row.items()
            if key not in DETAIL_FIELDS and not key.startswith('Headquarters uniform')}
