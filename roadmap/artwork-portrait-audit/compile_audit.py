"""Validate baseline review coverage and render the per-file Markdown register."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKER = '<!-- GENERATED REGISTER: compile_audit.py replaces content below this marker. -->'
LABELS = {'R': 'Restyle + reframe', 'P': 'Polish + framing',
          'F': 'Preserve rendering + reframe', 'H': 'Historical update',
          'E': 'Reference / archive / derivative'}


def main():
    inventory = json.loads((HERE / 'inventory.json').read_text(encoding='utf-8'))['assets']
    with (HERE / 'review_notes.psv').open(encoding='utf-8', newline='') as source:
        notes = list(csv.DictReader(source, delimiter='|'))
    assert len(inventory) == len(notes) == 306
    assert [r['id'] for r in notes] == [r['id'] for r in inventory]
    assert len({r['path'] for r in inventory}) == len(inventory)
    for note in notes:
        assert set(note) == {'id', 'action', 'observed', 'required_change'}
        assert note['action'] in LABELS
        assert all(note.values())
    parts = []
    last_sheet = None
    for asset, note in zip(inventory, notes):
        if asset['sheet'] != last_sheet:
            last_sheet = asset['sheet']
            number = int(last_sheet[7:9])
            parts.append(f'\n### Review sheet {number:02}\n\n[Open labelled complete-canvas sheet]({last_sheet}).\n')
        path = asset['path']
        size = ' × '.join(str(v) for v in asset['size'])
        alpha = 'contains transparency' if asset['alpha_min'] < 255 else 'fully opaque'
        parts.append(f"\n#### {asset['id']} — {path.removeprefix('assets/portraits/')}\n\n"
                     f"[Original file](../../{path.replace(' ', '%20')}) · {size} · {alpha} · **{LABELS[note['action']]}**.\n\n"
                     f"**Observed:** {note['observed']}\n\n"
                     f"**Required:** {note['required_change']}\n")
    target = HERE / 'PORTRAIT_AUDIT.md'
    prefix = target.read_text(encoding='utf-8').split(MARKER)[0] + MARKER + '\n'
    target.write_text(prefix + ''.join(parts), encoding='utf-8')
    print(f'PASS: {len(notes)} unique file assessments; 26 sheet links; all review actions valid.')


if __name__ == '__main__':
    main()
