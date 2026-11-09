"""Editable public profiles and private, source-backed contact notebooks."""
import copy
import re
import memory_store
import sexuality

FIELDS = ('About me', 'Sexuality', 'Food', 'Movies', 'Music', 'Hobbies', 'Likes', 'Dislikes',
          'Boundaries', 'Communication', 'Status', 'Profile picture')
EDITABLE_FIELDS = tuple(field for field in FIELDS if field != 'Sexuality')


def ensure(s):
    d = s.setdefault('contact_profiles', {})
    d.setdefault('people', {}); d.setdefault('notebooks', {})
    for who in s['world']['cast']:
        if who not in d['people']:
            import grove
            fields = {'About me': grove.BIOS.get(who, ''),
                      'Communication': 'I sometimes need time to find the words.' if who == 'emily' else 'Leave me a message; I will reply when I can.'}
            import four_aces
            if who in four_aces.CAST:
                person = four_aces.CAST[who]
                fields.update({'Hobbies': ', '.join(person['hobbies']), 'Likes': ', '.join(person['likes']),
                               'Dislikes': ', '.join(person['dislikes']), 'Communication': person['texting_style'],
                               'Boundaries': 'Ask before calling, photographing me or sharing my contact details.'})
            import interpol_cast
            if who in interpol_cast.IDS:
                person=interpol_cast.CAST[who]
                bio=('Edward Fox. Licensed Interpol associate. Keep your message direct.' if who=='fox'
                     else 'Jeremy Gordon. Team 9, Interpol. Official reports belong at the regional desk.')
                fields.update({'About me':bio,'Hobbies':', '.join(person['hobbies']),'Likes':', '.join(person['likes']),'Dislikes':', '.join(person['dislikes']),'Communication':person['texting_style'],'Boundaries':'Private cases stay private. Home visits by invitation.','Profile picture':'contact'})
            if who == 'charles':
                import charles_han
                fields.update({'About me':charles_han.PROFILE, 'Likes':', '.join(charles_han.LIKES), 'Dislikes':', '.join(charles_han.DISLIKES), 'Boundaries':'Laboratory conversations only. No outings.', 'Communication':'Measured, direct replies.'})
            if who == 'thirteen':
                import thirteen
                fields.update({'About me':thirteen.PROFILE,'Communication':'Concise operational reports.','Boundaries':'Official business at Pacific Relay Depot briefing room.'})
            if who == 'takeo':
                import takeo
                fields.update({'About me': takeo.PROFILE, 'Likes': 'strength, domination', 'Dislikes': 'weakness, mercy', 'Communication': 'Concise reports. State the result.', 'Boundaries': 'Official business at headquarters. No outings.'})
            if who in ('neo', 'alyssa'):
                import hidden_cast
                neo = hidden_cast.CAST[who]
                fields.update({'Hobbies': ', '.join(neo['hobbies']), 'Likes': ', '.join(neo['likes']),
                               'Dislikes': ', '.join(neo['dislikes']), 'Status': 'In a relationship with ' + ('Alyssa' if who == 'neo' else 'Neo'),
                               'Boundaries': 'Friendship only. Ask before touching; home visits by invitation.',
                               'Communication': 'Short messages are fine. Give me time to reply.' if who == 'neo' else 'Ask me directly; a quiet reply still means I care.'})
            d['people'][who] = dict(fields=fields, visibility={k:'public' for k in fields}, shared={}, versions={})
        if who in sexuality.CANON:
            # Authored identity is public on contact profiles, including older saves.
            d['people'][who]['fields']['Sexuality'] = sexuality.CANON[who][1]
            d['people'][who]['visibility']['Sexuality'] = 'public'
    return d


def edit(s, actor, field, value, visibility='public', recipients=()):
    if field == 'Sexuality': raise ValueError('Sexuality is part of this character’s canon and cannot be edited.')
    if field not in FIELDS or visibility not in ('public', 'private', 'selected'):
        raise ValueError('Choose a profile field and visibility.')
    if len(value) > 500: raise ValueError('Keep each profile field under 500 characters.')
    if field == 'Profile picture' and value:
        import game_core as core
        if value not in [path.stem[len(actor)+1:] for path in (core.ROOT/'assets/portraits').glob(actor+'-*.png')]:
            raise ValueError('Choose an available portrait outfit.')
    if any(who not in s['world']['cast'] for who in recipients): raise ValueError('Unknown contact.')
    p = ensure(s)['people'][actor]
    p['fields'][field] = value.strip(); p['visibility'][field] = visibility
    p['shared'][field] = list(recipients)
    p['versions'][field] = p['versions'].get(field, 0)+1
    p.setdefault('updated_at', {})[field] = s['world']['minute']


def public(s, subject, observer):
    if subject == 'crow':
        return {'About me': 'Undisclosed', 'Boundaries': 'Identity and personal details are unknown.'}
    p = ensure(s)['people'][subject]
    return {k:v for k,v in p['fields'].items() if subject == observer or
            p['visibility'].get(k) == 'public' or
            p['visibility'].get(k) == 'selected' and observer in p['shared'].get(k, [])}


def notebook(s, observer, subject):
    return ensure(s)['notebooks'].setdefault(observer, {}).setdefault(subject, [])


def add(s, observer, subject, kind, text):
    if kind not in ('Private note', 'Question', 'Memory', 'Keepsake', 'Promise', 'Plan'):
        raise ValueError('Choose a notebook category.')
    text = text.strip()
    if not text or len(text) > 500: raise ValueError('Write between 1 and 500 characters.')
    rows = notebook(s, observer, subject)
    rows.append(dict(id=len(rows)+1, kind=kind, text=text, minute=s['world']['minute'], pinned=False, done=False))


def toggle(s, observer, subject, ident, field):
    if field not in ('pinned', 'done'): raise ValueError('Unknown notebook action.')
    row = next(r for r in notebook(s, observer, subject) if r['id'] == ident)
    row[field] = not row[field]


def initially_close(observer, subject):
    """Starting familiarity survives later hurt; new bond points aren't disclosures."""
    import town
    import world_loop
    if observer == subject: return True
    pair = {observer, subject}
    if pair in ({'rei', 'garrett'}, {'rei', 'yuriko'}, {'ivan', 'valentina'}): return True
    for first, second in ((observer, subject), (subject, observer)):
        baseline = town.STARTING_RELATIONSHIPS.get(first, {}).get(second)
        if baseline and baseline[1] >= 70 and baseline[2] >= 55: return True
    for key, (_, trust, closeness, _) in world_loop.BONDS.items():
        if set(key.split(':')) == pair and trust >= 70 and closeness >= 55: return True
    return False


def starting_favourites(subject, observer):
    import conversation_lore
    if not initially_close(observer, subject): return {}
    return {key: dict(value=value, source='character_reference',
                     provenance='Your established tastes' if subject == observer else 'Known from your shared history')
            for key, value in conversation_lore.everyday_favourites(subject).items()}


def known_favourites(s, subject, observer):
    """Read-only knowledge lookup for prompts; never create notebook entries."""
    facts = starting_favourites(subject, observer)
    for field, fact in learned_details(s, subject, observer).items():
        if field.startswith('favourite:'): facts[field.split(':', 1)[1]] = fact
    return facts


def disclosures(s, subject, observer):
    rows = [r for r in s.get('memory_store', {}).get('records', {}).values()
            if subject in r['subjects'] and observer in r['owners'] and
            (r['kind'] in ('fact', 'belief') or r.get('certainty') == 'quoted speech')]
    rows = [dict(r) for r in rows]
    for n in s.get('profile_notes', {}).get(subject, []):
        if observer in n.get('owners', [s['player'], n['source']]):
            rows.append(dict(text=n['quote'], source=n['source'], speaker=n['source'],
                             minute=n['minute'], kind='fact' if n['source'] == subject else 'belief',
                             certainty='self-reported' if n['source'] == subject else 'reported by another person'))
    return sorted(rows, key=lambda r:r.get('minute') or 0)


def learned_details(s, subject, observer):
    import personal_details
    fields = {}
    for r in disclosures(s, subject, observer):
        if r['kind'] == 'belief' or r.get('speaker', subject) != subject: continue
        text = r['text']
        for prefix in (subject+': ', subject+' said: '):
            if text.startswith(prefix): text = text[len(prefix):]; break
        extracted = ({r['profile_field']:r['profile_value']} if 'profile_field' in r else personal_details.extract(text))
        for field, value in extracted.items():
            if field in ('Likes', 'Dislikes', 'Hobbies', 'Allergies'):
                values = list(fields.get(field, {}).get('values', []))
                if value.casefold() not in [v.casefold() for v in values]: values.append(value)
            else: values = None
            fields[field] = dict(value=value, source=r['source'], minute=r.get('minute'),
                                 provenance='Learned in conversation', certainty='self-reported')
            if values is not None: fields[field].update(values=values, value='; '.join(values))
            if field == 'Dislikes':
                for opposite in ('Likes', 'Hobbies'):
                    if opposite in fields:
                        kept = [v for v in fields[opposite].get('values', []) if v.casefold() != value.casefold()]
                        fields[opposite].update(values=kept, value='; '.join(kept))
    return fields


def self_reference(subject, observer):
    """Own biography has no disclosure gates, but never becomes a public bio."""
    if subject != observer: return {}
    import conversation_lore
    table = conversation_lore.character_tables().get(subject, {})
    labels = {'Public life': 'Your life', 'Familiar': 'Your background',
              'Personal': 'Your personal history', 'Confidence': 'Your private history',
              'World knowledge': 'Your experience', 'Appearance': 'Your appearance',
              'Everyday favourites': 'Your tastes'}
    return {label: table[key] for key, label in labels.items() if table.get(key)}


def field_value(data, field, *, own=False):
    """Use saved edits first, then known canon, without suggesting self-discovery."""
    if field == 'Sexuality': return data['public'].get(field, 'Not established')
    aliases = {'Food': ('Food', 'Dessert'), 'Movies': ('Movie', 'Film'),
               'Music': ('Music', 'Song'), 'Hobbies': ('Hobby',)}
    learned = data.get('details', {}).get(field)
    if learned is None:
        learned = next((data['favourites'][key] for key in aliases.get(field, (field,))
                        if key in data['favourites'] and data['favourites'][key].get('source') != 'character_reference'), None)
    if learned and (field not in data['public'] or
                    (learned.get('minute') or 0) > data.get('field_times', {}).get(field, -1)):
        return learned['value']
    if field in data['public']: return data['public'][field]
    for key in aliases.get(field, (field,)):
        if key in data['favourites']: return data['favourites'][key]['value']
    if field == 'Food':
        meals = [key+': '+data['favourites'][key]['value'] for key in ('Breakfast', 'Lunch', 'Dinner', 'Snack') if key in data['favourites']]
        if meals: return '\n'.join(meals)
    return 'Not set — add your preference' if own else 'Not shared yet'


def view(s, subject, observer):
    records = [copy.deepcopy(r) for r in memory_store.ensure(s)['records'].values()
               if observer in r['owners'] and subject in set(r['subjects']) | set(r['owners'])]
    discoveries = [r for r in disclosures(s, subject, observer) if r['kind'] in ('fact', 'belief')]
    unique = {}
    for r in discoveries: unique[(r['text'], r.get('minute'))] = r
    discoveries = list(unique.values())
    favourites = known_favourites(s, subject, observer)
    return dict(public=public(s, subject, observer), discoveries=discoveries,
        field_times=dict(ensure(s)['people'][subject].get('updated_at', {})),
        favourites=favourites,
        details=learned_details(s, subject, observer),
        self_reference=self_reference(subject, observer),
        memories=[r for r in records if r['kind'] == 'experience'][-30:],
        promises=[r for r in memory_store.open_commitments(s, [observer]) if subject in r['owners'] or subject in r['subjects']],
        notebook=copy.deepcopy(sorted(notebook(s, observer, subject), key=lambda r: (not r['pinned'], -r['id']))))


def context(s, observer):
    result = {}
    for who in ensure(s)['people']:
        fields = public(s, who, observer)
        known = starting_favourites(who, observer)
        if known:
            fields['Favourites already known before the story'] = {k:v['value'] for k,v in known.items()}
        learned = learned_details(s, who, observer)
        if learned: fields['Later disclosures (supersede older tastes)'] = learned
        if fields: result[who] = fields
    return result


def tick(s):
    # Public statuses reflect observable daily activity, never private crushes.
    for who, actor in s['world']['cast'].items():
        if who == s['player']: continue
        p = ensure(s)['people'][who]
        activity = actor.get('activity', '').casefold()
        # An internal schedule is not permission to publish a private occupation,
        # location or meeting. Only broad availability becomes a public status.
        status = ('Taking time to recharge' if any(word in activity for word in ('sleep', 'winding down')) else
                  'Away for a little while' if actor.get('journey') or any(word in activity for word in
                    ('work', 'shift', 'business', 'meeting', 'training', 'class', 'recording', 'modelling')) else
                  'Making a little time for myself')
        if p['fields'].get('Status') != status:
            edit(s, who, 'Status', status)
        if 'Communication' not in p['fields']:
            edit(s, who, 'Communication', 'I sometimes need time to find the words.' if who == 'emily' else 'Leave me a message; I will reply when I can.')
        if 'About me' not in p['fields']:
            import grove
            if who in grove.BIOS: edit(s, who, 'About me', grove.BIOS[who])
