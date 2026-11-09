"""Opt-in live conversation samples using synthetic stories, never the player's save.

Run with --live to use the currently configured provider. Output records latency,
request counts and consecutive turns for human review; it is not an automatic
quality score. No extra evaluation calls are added to normal gameplay.
"""
import argparse
import json
from pathlib import Path
import sys
import time
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import game_core as core
import groups

SCENARIOS = {
    'ordinary': ['What did you feel like doing today?', 'A quiet afternoon sounds good to me.'],
    'awkward': ['I had something to say and completely forgot it.', 'Nope. Still gone.'],
    'disagreement': ['I think a film needs a happy ending to be worth watching.', 'I still want something better than everyone being miserable.'],
    'flirting': ['I was hoping you would be here.', 'Yeah. I like spending time with you.'],
    'serious': ['I miss my dad today.', 'I do not really want advice. Just some company.'],
}


def run(output):
    report = dict(provider=core.check_model(), scenarios=[],
                  review=['Does each turn answer the actual input?',
                          'Do lengths, openings and questions vary across turns?',
                          'Does speech fit the character without counselling or explaining subtext?',
                          'Can group members listen or return without speaking for the player?'])
    output.parent.mkdir(parents=True, exist_ok=True)
    def save():
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for label, inputs in [*SCENARIOS.items(), ('group', ['Emily, what do you feel like doing?', 'That works for me.'])]:
        state = core.fresh('rei')
        core.town.summon(state, 'emily')
        if label == 'group': core.town.summon(state, 'sophie')
        gid = state['active_group']
        sample = dict(scenario=label, turns=[])
        report['scenarios'].append(sample)
        for line in inputs:
            started = time.perf_counter()
            with patch.object(core, 'request', wraps=core.request) as requests:
                try:
                    result = groups.generate(state, gid, line)
                    groups.commit(state, gid, line, result)
                    turn = dict(player=line, narration=result['narration'],
                                lines=result.get('lines', [dict(speaker=result.get('speaker'), text=result.get('dialogue'))]))
                except Exception as error:
                    turn = dict(player=line, error=str(error))
                turn.update(seconds=round(time.perf_counter()-started, 3), requests=requests.call_count)
            sample['turns'].append(turn)
            save()
            print(f'{label}: {turn["seconds"]}s, {turn["requests"]} request(s)' + (' FAILED' if 'error' in turn else ''), flush=True)
            if 'error' in turn: break
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Allow model requests using the configured provider')
    parser.add_argument('--output', type=Path, default=core.ROOT / '.test-tmp' / 'dialogue-evaluation.json')
    args = parser.parse_args()
    if not args.live: parser.error('--live is required; this evaluation makes model requests')
    report = run(args.output)
    sys.exit(int(any('error' in t for s in report['scenarios'] for t in s['turns'])))
