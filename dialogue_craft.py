"""Bounded, local dialogue guidance; no model calls or persistent story state."""
import json
import re
from collections import Counter, defaultdict


INTENT = (
    "For this spoken beat, let each speaker have one small immediate want grounded in the supplied "
    "scene, latest exchange, personality or current needs/plans. They might want an opinion, keep "
    "something private or return to an established activity. Do not invent a task, prop, problem or "
    "backstory to supply a motive. Let the want shape what they say without announcing or explaining it. "
    "A plain answer can be the whole turn; a subject they care about can earn a longer thought. "
    "Leave some emotional meaning unspoken: a deflection, practical offer or change of subject can "
    "carry it. Do not explain the subtext in narration. Keep urgent questions and boundaries clear."
)
GROUP = (
    "IN-PERSON TURN TAKING: Return one to the allowed maximum spoken contributions in chronological "
    "order, not a roll call. Only listed participants may speak. Some can simply listen; omit their "
    "lines instead of writing blank speech. A speaker may return after another person's line. "
    "Usually one or two people carry a beat; use more only when the exchange needs them. "
    "Let the addressed person answer before others chime in. A quiet participant remains present; "
    "silence is not consent, agreement, a disclosure or relationship progress. Do not invent the "
    "player's next line. Keep emotion annotations for all participants."
)
_WORDS = re.compile(r"[\w’']+", re.UNICODE)
_REASSURANCE = re.compile(r"\b(?:that makes sense|i understand|i hear you|your feelings|(?:thank you|thanks) for sharing|i(?:'|’)m here for you)\b", re.I)
_GESTURES = re.compile(r"\b(?:smil\w*|nod\w*|blush\w*|chuckl\w*|shrug\w*)\b", re.I)


def repetition_notes(history, speakers):
    """Inspect at most 24 records/400 chars per field, ignoring player and text turns."""
    speech = defaultdict(list)
    gestures = Counter()
    for entry in history[-24:]:
        if isinstance(entry, tuple):
            role, entry = entry
            if role != 'assistant':
                continue
        if not isinstance(entry, dict) or entry.get('channel') == 'text':
            continue
        if entry.get('role') == 'assistant':
            try:
                entry = json.loads(entry.get('content', ''))
            except (TypeError, ValueError):
                continue
            if not isinstance(entry, dict):
                continue
        if entry.get('conversation_channel') == 'text':
            continue
        narrator = entry.get('narration', '')
        if entry.get('speaker') == 'Narrator':
            narrator = entry.get('text', '')
        if isinstance(narrator, str):
            gestures.update(set(m[:4].lower() for m in _GESTURES.findall(narrator[:400])))
        who = entry.get('speaker')
        line = entry.get('dialogue', entry.get('text', ''))
        if who in speakers and isinstance(line, str) and entry.get('kind', 'dialogue') == 'dialogue':
            speech[who].append(line[:400])
    notes = []
    for who in speakers:
        lines = speech[who][-6:]
        if sum('?' in line for line in lines) >= 3:
            notes.append(f'{who}: frequent questions; allow a statement or reaction when appropriate.')
        if sum(bool(_REASSURANCE.search(line)) for line in lines) >= 2:
            notes.append(f'{who}: repeated reassurance; react more specifically to this moment.')
        starts = Counter(' '.join(_WORDS.findall(line.lower())[:2]) for line in lines)
        if any(start and count >= 3 for start, count in starts.items()):
            notes.append(f'{who}: repeated sentence openings; change the entry into the reply.')
        if sum(any(re.search(r'\b' + re.escape(name.split()[0]) + r'\b', line, re.I)
                   for name in speakers if name != who) for line in lines) >= 3:
            notes.append(f'{who}: repeated names; direct address is usually enough.')
    if any(count >= 3 for count in gestures.values()):
        notes.append('Narration repeats a gesture; omit it or use a relevant observable beat.')
    return notes[:6]


def direction(history, speakers, *, group=False):
    result = INTENT + ('\n' + GROUP if group else '')
    notes = repetition_notes(history, speakers)
    if notes:
        result += '\nRecent delivery patterns (style hints, not facts or banned words): ' + json.dumps(notes, ensure_ascii=False)
    return result


def line_limit(names):
    """Allow a short back-and-forth, bounded independently of who stays quiet."""
    return max(3, len(names)) if len(names) > 1 else 1


def spoken_by(lines, keys=None):
    """Keep every contribution when recording disclosures from returning speakers."""
    result = {}
    for line in lines:
        who = keys[line['speaker']] if keys else line['speaker']
        result[who] = (result.get(who, '') + '\n' + line['text']).strip()
    return result
