"""Small deterministic helpers shared by the desktop convenience screens."""
import copy
import json
from pathlib import Path
import story_calendar as calendar
import scheduled_events


def backup(path):
    if not path.exists(): return
    # Do not replace a good recovery point with a truncated/corrupt file.
    json.loads(path.read_text(encoding='utf-8'))
    latest = path.with_name(path.stem + '.backup1.json')
    if latest.exists() and latest.read_bytes() == path.read_bytes(): return
    for n in range(4, 0, -1):
        source = path.with_name(path.stem + f'.backup{n}.json')
        if source.exists(): source.replace(path.with_name(path.stem + f'.backup{n+1}.json'))
    path.with_name(path.stem + '.backup1.json').write_bytes(path.read_bytes())


def stats(s):
    return copy.deepcopy({**s.get('friendships', {}), **s.get('relationships', {})})


def changes(before, s):
    result = []
    for who, record in stats(s).items():
        for field in ('trust', 'closeness', 'attraction'):
            delta = record.get(field, 0)-before.get(who, {}).get(field, 0)
            if delta: result.append(f'{who.title()} · {field.title()} {delta:+}')
    return result


def agenda(s):
    import town
    now = s['world']['minute']
    lines = [town.loop.clock(s), 'Location: ' + town.loop.place_name(s)]
    lines += ['Today: '+title for title, _, _ in calendar.events(s, calendar.story_date(now))]
    lines += [scheduled_events.describe(e) for e in sorted(s.get('scheduled_events', []), key=lambda e:e['start'])
              if not e.get('cancelled') and e['end'] > now][:8]
    for who in s.get('relationships', {}):
        session = town.dating.session(s, who)
        if session:
            lines.append('Date with '+who.title()+(' · In progress' if session['started'] else ' · Planned'))
            lines += ['  '+goal for key,goal in session['goals'].items() if key not in session['done']]
    for i, (_, name, pay, start, end) in enumerate(town.CAREERS.get(s['player'], [])):
        key = f"{now//1440}:{s['player']}:{i}"
        status = 'Completed today' if key in s['world'].get('career_shifts', []) else 'Available now' if start*60 <= now%1440 and now%1440+45 <= min(end*60,1439) else 'Outside booking hours'
        lines.append(f'{name} · 45 min · +${pay:,} · {start:02}:00–{end:02}:00 · {status}')
    return lines


def recap(s):
    import game_core as core
    lines = agenda(s)
    who = s['active']
    dialogue = s['routes'][who].get('dialogue')
    if dialogue: lines += ['', 'Last conversation · '+core.contact_name(s, who), dialogue]
    lines += ['', 'Recent events', *s['world'].get('log', [])[-5:]]
    return '\n'.join(lines)


def history(s):
    import game_core as core
    records = []
    for key, route in s['routes'].items():
        for i, m in enumerate(route.get('history', [])):
            text = m['content']
            if m['role'] == 'assistant':
                try:
                    data = json.loads(text)
                    text = '\n'.join(str(data.get(k, '')) for k in ('narration', 'dialogue'))
                except (ValueError, TypeError): pass
            minute = m.get('minute')
            stamp = str(calendar.story_date(minute)) if isinstance(minute, int) else 'Earlier'
            records.append((f'route:{key}:{i}', core.contact_name(s, key), stamp, text, key, False, i))
    for key, group in s.get('groups', {}).items():
        for i, m in enumerate(group.get('history', [])):
            minute = m.get('minute')
            stamp = str(calendar.story_date(minute)) if isinstance(minute, int) else 'Earlier'
            records.append((f'group:{key}:{i}', group['name'], stamp,
                            m.get('speaker', '')+': '+m.get('text', ''), key, True, i))
    return records


def travel_preview(s, destination):
    import world_loop
    import hidden_cast
    w = s['world']
    lines = ['Instant travel · Your party arrives with you']
    if w['cast'][s['player']]['journey']: lines.append('Finish your current drive first.')
    elif destination == w['location']: lines.append('You are already here.')
    for who, actor in w['cast'].items():
        if who == s['player'] or not hidden_cast.contact(s, who): continue
        place = None if actor['journey'] else actor['location']
        if place == destination: lines.append(who.title()+' expected there')
    return '\n'.join(lines)
