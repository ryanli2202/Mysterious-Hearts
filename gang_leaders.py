"""Resident gang leaders: local conversations, private introductions and bases."""
LEADERS = {
    'lantern': dict(name='Mara Voss', base='lantern_house', title='Lantern House', age=32,
        role='Lantern Crew leader', appearance='Short dark auburn hair, olive skin, mustard scarf and charcoal jacket.',
        detail='A former night-market organiser who built a small crew around personal obligations. Sharp, economical and quietly calculating; remembers unpaid favours. Repairs old radios in her upstairs flat. She fears powerful patrons swallowing her crew and bargains for independence.'),
    'rail': dict(name='Darius Cole', base='saints_depot', title='Saints Rail Depot', age=45,
        role='Rail Yard Saints leader', appearance='Broad-shouldered Black man, cropped salt-and-pepper hair, short beard and navy work jacket.',
        detail='A former yard foreman who turned a neighbourhood protection circle into a criminal crew. Patient, territorial and deliberate; asks who bears the cost before agreeing. Lives in the converted depot office and restores railway clocks. His loyalty to his people coexists with ruthless exclusion of outsiders.'),
    'purple': dict(name='Rafe Calder', base='purple_clubhouse', title='Purple Skulls Clubhouse', age=48,
        role='Purple Skulls chapter president', appearance='Weathered face, tied-back brown hair, grey-streaked beard, purple-lined black leather vest.',
        detail='Rose from club mechanic to chapter president by arbitrating a bitter succession. Blunt, suspicious of polished promises and careful about member loyalty. Lives above the clubhouse garage. Keeps meticulous maintenance notebooks; resents outsiders treating the club as disposable muscle.'),
    'hamayashi': dict(name='Daichi Kurose', base='hamayashi_house', title='Kurose House', age=52,
        role='Successor Hamayashi-kai leader', appearance='Swept-back greying black hair, eyebrow scar, midnight navy suit and burgundy shirt.',
        detail='A broker who now leads the successor Hamayashi-kai after Keisuke Hachimura’s absorption into the Shinokami. He rebuilt influence around an inherited name, not a surviving original clan. Lives in the rear residence of Kurose House. Formal, controlled and ambitious, he cultivates bonsai and treats courtesy as a negotiating instrument. Rei destroyed the original clan; Rei is unaware of this successor until actual evidence is disclosed. Do not invent a prior meeting with Rei or Yuriko or disclose their private history.'),
    'rojos': dict(name='Isabel Vega', base='rojos_courtyard', title='Los Rojos Courtyard', age=40,
        role='Los Rojos leader', appearance='Dark hair in a sleek low bun, deep red blazer, black blouse and small gold earrings.',
        detail='Built her position by holding together a fractured regional cartel council. Exacting and unsentimental, she distinguishes respect from affection and insists on explicit obligations. Resides above the courtyard offices. Plays classical guitar privately; has no patience for associates who mistake her restraint for indecision.'),
    'waterfront': dict(name='Evelyn Mercer', base='consortium_house', title='Waterfront Consortium House', age=56,
        role='Waterfront Consortium chair', appearance='Dark brown skin, silver bob, thin gold glasses, sea-green blouse and charcoal long jacket.',
        detail='A former maritime accountant who assembled rival waterfront interests into a criminal consortium. Measured, incisive and difficult to fluster; asks precise questions about authority and accountability. Resides in the upper-floor apartment. Collects maritime charts and believes every alliance has an expiry date.'),
}
NAMES = tuple(p['name'] for p in LEADERS.values())
BY_NAME = {p['name']: p for p in LEADERS.values()}
LOCATIONS = {p['base']: p['title'] for p in LEADERS.values()}
BOUNDARY = ('Nonromantic town NPC, with no major-character route, Grove account or Meet-Cute profile. '
    'Lives at the named base and receives visitors in its meeting room. Dialogue cannot grant money, '
    'membership, promotion or completed deals; only explicit game controls do that. Do not invent '
    'player actions, private information, completed crimes or operational instructions.')
PROFILES = [(p['name'], p['role'], f"Age {p['age']}. {p['appearance']} {p['detail']} Residence: {p['title']}. {BOUNDARY}")
            for p in LEADERS.values()]


def reference_tables():
    """Derive shared references from authored leaders without inventing tastes or history."""
    privacy = (BOUNDARY + ' Your own biography is private speaker knowledge, not an automatic disclosure. '
        'Trust or membership does not reveal criminal affiliations, home addresses or other people’s history '
        'to listeners. Use actual meeting and disclosure records. Do not invent a prior meeting with Rei '
        'or Yuriko or reveal their private history.')
    manners = {
        'Mara Voss': 'Sharp, economical and quietly calculating; remembers unpaid favours.',
        'Darius Cole': 'Patient, territorial and deliberate; asks who bears the cost before agreeing.',
        'Rafe Calder': 'Blunt, suspicious of polished promises and careful about member loyalty.',
        'Daichi Kurose': 'Formal, controlled and ambitious; treats courtesy as a negotiating instrument.',
        'Isabel Vega': 'Exacting and unsentimental; distinguishes respect from affection and insists on explicit obligations.',
        'Evelyn Mercer': 'Measured, incisive and difficult to fluster; asks precise questions about authority and accountability.',
    }
    return {p['name']: {
        'Public life': f"Age {p['age']}. {p['role']}. This role is not automatically known to outsiders.",
        'Familiar': manners[p['name']] + ' ' + BOUNDARY,
        'Personal': p['detail'],
        'Confidence': 'No additional private history is established. ' + privacy,
        'World knowledge': 'Their own organisation and responsibilities, not rival secrets or unobserved player activity. ' + privacy,
        'With visitors': privacy,
        'Disclosure boundary': privacy,
        'Everyday favourites': 'Unknown',
        'Appearance': p['appearance'],
        'Portrait style': 'Cel-shaded manhwa transparent town NPC portrait and matching contact photo; not a live view during texting.',
    } for p in LEADERS.values()}


def ensure(s):
    gang = s.get('job_apps', {}).get('gang') or {}
    key = gang.get('id')
    if key not in LEADERS:
        return
    p = LEADERS[key]; name = p['name']
    chat = s.setdefault('npc_chats', {}).setdefault(name, {'history': []})
    chat.setdefault('connection', dict(status='acquaintances', trust=35, closeness=0))
    import groups, phone_numbers
    groups.sync_contacts(s)
    phone = s.setdefault('phone_numbers', {})
    number = phone_numbers.NUMBERS[name]
    phone.setdefault('directory', {}).setdefault(name, number)
    phone.setdefault('contacts', {}).setdefault(name, dict(number=number, source=p['role'], minute=s['world']['minute']))
    if not chat.get('gang_introduced'):
        line = dict(speaker=name, text=f"Your membership is confirmed. This is my direct number. Report to {p['title']} when you need to speak in person.",
                    minute=s['world']['minute'], channel='text')
        chat['history'].append(line)
        thread = s['groups']['npc:'+name]
        if thread['history'] is not chat['history']: thread['history'].append(dict(line))
        thread['unread'] = thread.get('unread', 0)+1
        chat['gang_introduced'] = True


def refresh(s):
    names = s['world']['npcs']
    if s['world']['location'] in LOCATIONS:
        names[:] = []
    names[:] = [n for n in names if n not in BY_NAME]
    names.extend(p['name'] for p in LEADERS.values() if p['base'] == s['world']['location'])


def context(s, name):
    p = BY_NAME.get(name)
    if not p: return {}
    import criminal_reputation, crime_diplomacy
    return dict(residence=p['title'], criminal_reputation=criminal_reputation.DIRECTION,
                meeting=crime_diplomacy.scene_context(s, name), boundary=BOUNDARY)
