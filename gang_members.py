"""Authored town coworkers for local gangs; no major-character routes."""
import gang_leaders

# Keep order stable: phone_numbers appends this roster after all older identities.
ROSTER = (
    ('lantern', 'Nessa Quinn', 28, 'shift coordinator', 'Copper curls, charcoal hoodie and amber work apron.', 'Dryly funny and organised; restores battered board games.', 'Checks the crew rota and hears both sides of disagreements.'),
    ('lantern', 'Malik Reed', 34, 'storeroom caretaker', 'Close-cropped hair, dark green overshirt and square glasses.', 'Soft-spoken, stubborn about fairness; grows chillies on his windowsill.', 'Checks shared supplies and flags disputed records.'),
    ('rail', 'Imani Price', 39, 'depot maintenance lead', 'Braided hair, navy coveralls and orange ear defenders.', 'Direct and patient with learners; sketches old locomotives.', 'Keeps the depot workshop usable and reviews repair priorities.'),
    ('rail', 'Owen Pike', 27, 'yard office clerk', 'Sandy hair, freckled face and a slate canvas jacket.', 'Careful with words, competitive at darts; keeps a battered scorebook.', 'Compares work logs and organises the shared shift board.'),
    ('purple', 'Jules Navarro', 33, 'clubhouse mechanic', 'Undercut dark hair, purple bandana and black work shirt.', 'Cheerfully blunt; builds miniature motorcycles from spare parts.', 'Maintains workshop tools and mediates shared-garage disputes.'),
    ('purple', 'Greta Shaw', 46, 'clubhouse steward', 'Silver-streaked braid, dark denim and a purple waistcoat.', 'Wry and hospitable without being gullible; collects concert tickets.', 'Runs the clubhouse rota and checks communal expenses.'),
    ('hamayashi', 'Emi Suda', 30, 'house administrator', 'Straight chin-length black hair and a charcoal cardigan.', 'Precise but quietly playful; practises calligraphy for herself.', 'Organises the successor organisation’s appointments and reconciles conflicting requests.'),
    ('hamayashi', 'Ren Aoki', 36, 'house maintenance coordinator', 'Short black hair, navy work jacket and round glasses.', 'Reserved, practical and fond of terrible puns; repairs ceramic planters.', 'Maintains Kurose House and reviews shared repair costs.'),
    ('rojos', 'Lucia Serrano', 32, 'courtyard office coordinator', 'Dark curls, red scarf and graphite blouse.', 'Brisk and sceptical of grand promises; enjoys puzzle magazines.', 'Keeps courtyard appointments running and checks disputed office records.'),
    ('rojos', 'Mateo Cruz', 41, 'courtyard caretaker', 'Salt-and-pepper moustache, burgundy shirt and dark work trousers.', 'Patient with people, impatient with waste; tends courtyard citrus pots.', 'Maintains communal spaces and brings unresolved work concerns to review.'),
    ('waterfront', 'Ada Mensah', 37, 'accounts clerk', 'Twisted updo, teal glasses and a charcoal knit jacket.', 'Exacting with numbers and generous with explanations; sings in a small choir.', 'Compares shared expense records and asks for missing explanations.'),
    ('waterfront', 'Felix Ward', 44, 'house facilities coordinator', 'Wavy greying hair, navy overshirt and a sea-green scarf.', 'Unhurried and observant; makes tiny model lighthouses.', 'Coordinates building upkeep and settles competing maintenance requests.'),
    ('dragons', 'Mina Cho', 29, 'lounge coordinator', 'Black ponytail, dark red blouse and charcoal trousers.', 'Quick-witted and firm about boundaries; loves rhythm games.', 'Organises the Red Dragons lounge rota and hears crew concerns.'),
    ('dragons', 'Anton Bellamy', 35, 'lounge maintenance lead', 'Short brown curls, trimmed beard and black denim jacket.', 'Calm and methodical; repairs old speakers as a hobby.', 'Maintains the private lounge and reviews disputed shared expenses.'),
)
MEMBERS = {name: dict(gang=gang, age=age, role=role, appearance=appearance,
                     personality=personality, work=work,
                     base='syndicate' if gang == 'dragons' else gang_leaders.LEADERS[gang]['base'])
           for gang, name, age, role, appearance, personality, work in ROSTER}
NAMES = tuple(MEMBERS)
BOUNDARY = ('Nonromantic town NPC. Membership and private affiliations are not public knowledge. '
            'Do not reveal rival secrets, private protagonist history or invent shared work. '
            'Dialogue cannot award membership, money, rank or completed assignments. '
            'Hamayashi coworkers belong only to the successor organisation, not the original clan.')
PROFILES = [(name, p['role'], f"Age {p['age']}. {p['appearance']} {p['personality']} {p['work']} " + BOUNDARY)
            for name, p in MEMBERS.items()]


def affiliation(s):
    gang = s.get('job_apps', {}).get('gang') or {}
    if gang.get('id') in gang_leaders.LEADERS:
        return gang['id']
    if gang.get('established') and gang.get('name') == 'Red Dragons':
        return 'dragons'
    return None


def coworkers(s):
    key = affiliation(s)
    return [name for name, p in MEMBERS.items() if p['gang'] == key]


def ensure(s):
    import groups, phone_numbers
    for name in coworkers(s):
        p = MEMBERS[name]
        chat = s.setdefault('npc_chats', {}).setdefault(name, {'history': []})
        chat.setdefault('connection', dict(status='acquaintances', trust=35, closeness=0))
        established = s['player'] == 'garrett' and p['gang'] == 'dragons'
        if established and not chat.get('garrett_worker_origin_v1'):
            connection = chat['connection']
            # Add the authored baseline once; preserve earned deltas and later losses.
            connection['trust'] = max(0, min(100, connection.get('trust', 35) + 45))
            connection['closeness'] = max(0, min(100, connection.get('closeness', 0) + 35))
            if connection.get('status') in ('strangers', 'acquaintances'):
                connection['status'] = 'established colleagues'
            chat['garrett_worker_origin_v1'] = True
        groups.sync_contacts(s)
        phone = s.setdefault('phone_numbers', {})
        phone.setdefault('contacts', {}).setdefault(name, dict(number=phone_numbers.NUMBERS[name],
            source='Gang coworker', minute=s['world']['minute']))
        if not chat.get('coworker_introduced'):
            import town
            line = dict(speaker=name, text=f"I handle {p['role']} duties at {town.LOCATIONS[p['base']]}. We will work together on crew obligations. You can find me there or call this number.",
                        minute=s['world']['minute'], channel='text')
            if established:
                line['text'] = f"Boss, you can reach me here as usual. I'm at the lounge handling {p['role']} duties; let me know when you want to review crew concerns."
            chat['history'].append(line)
            thread = s['groups']['npc:' + name]
            if thread['history'] is not chat['history']:
                thread['history'].append(dict(line))
            thread['unread'] = thread.get('unread', 0) + 1
            chat['coworker_introduced'] = True


def refresh(s):
    names = s['world']['npcs']
    names[:] = [name for name in names if name not in MEMBERS]
    names.extend(name for name, p in MEMBERS.items() if p['base'] == s['world']['location'])


def contract(s, spec):
    names = coworkers(s)
    if not names:
        return spec
    return dict(spec, venue=MEMBERS[names[0]]['base'], coworkers=names,
                brief='Work alongside ' + ' and '.join(names) + '. ' + spec['brief'])


def context(s, name):
    p = MEMBERS[name]
    pending = s.get('job_apps', {}).get('pending') or {}
    return dict(work=p['work'], same_gang=name in coworkers(s),
                established_relationship=(
                    'Garrett is your established Red Dragons leader. You already know each other through lounge work; '
                    'do not introduce yourself as a stranger or recruit him. Respect current saved trust and closeness; '
                    'this working history does not imply romance or knowledge of his private life.'
                    if s['player'] == 'garrett' and p['gang'] == 'dragons' else None),
                connection=dict(s.get('npc_chats', {}).get(name, {}).get('connection', {})),
                shared_assignment=pending if name in pending.get('coworkers', []) else None,
                boundary=BOUNDARY)
