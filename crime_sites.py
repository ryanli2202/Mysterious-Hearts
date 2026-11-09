"""Discoverable public frontages; private affiliations never follow from a map pin."""
import copy
import four_aces

INSIDERS = frozenset(('ivan', 'valentina', 'sylvanis', *four_aces.IDS))


def site(name, point, district, faction, role, exterior, record):
    return dict(name=name, point=point, district=district, faction=faction, role=role,
                exterior=exterior, record=record)


# Opaque location keys prevent search and travel records from revealing factions.
SITES = {
    'site_01': site('Kestrel Operations Centre', (1370, 370), 'East industrial ward', 'Shinokami', 'Winterfield headquarters',
        'A contractor sign identifies Kestrel Operations. The visitor gate is shut; armoured shutters cover the rear loading bays.', 'Kestrel Operations lease K-41'),
    'site_02': site('Pacific Relay Depot', (1440, 700), 'Freight corridor', 'Shinokami', 'supply base',
        'Pacific Relay is painted above a dispatch window. A posted operator number matches the freight office sign; the fenced yard is private.', 'Pacific Relay operator PR-18'),
    'site_03': site('Stillwater Research Annex', (1220, 230), 'Medical business district', 'Shinokami', 'research front',
        'The sign advertises contract laboratory services. There is no walk-in clinic. A licensing notice identifies Stillwater Research; no experiments are visible from the pavement.', 'Stillwater Research licence SR-06'),
    'site_04': site('Breakwater Security Depot', (1290, 950), 'South docks', 'Syndicate', 'Clubs side base',
        'Breakwater Security lists a fleet-maintenance office. A visitor bell stands outside a locked vehicle gate; its operator certificate is posted behind glass.', 'Breakwater Security certificate BS-24'),
    'site_05': site('Aster Media House', (790, 20), 'Arts district north', 'Syndicate', 'Hearts publicity front',
        'Aster Media advertises production and campaign management. The public directory gives its registered company number, not its clients or private assignments.', 'Aster Media company AM-32'),
    'site_06': site('Meridian Capital Offices', (1080, 40), 'Civic business district', 'Syndicate', 'Diamonds finance front',
        'Meridian Capital occupies the upper floors. The street directory names the registered partnership; appointments are required beyond reception.', 'Meridian Capital partnership MC-12'),
    'site_07': site('Oculus Winterfield Campus', (1470, 80), 'Technology district', 'Syndicate', 'corporate affiliate',
        'Oculus branding identifies the campus. Public displays describe technology, media, logistics and infrastructure services. Staff-only data and security wings require credentials.', ''),
    'site_08': site('Greyglass Service House', (450, 1070), 'Old rail quarter', 'Syndicate', 'Spades support base',
        'Greyglass advertises equipment servicing by appointment. Its property-management notice identifies the leaseholder. The workshop doors remain closed.', 'Greyglass tenancy GG-09'),
}


def records(s, who=None):
    return s.get('city_sites', {}).get('people', {}).get(who or s['player'], {})


def known_name(s, key, who=None):
    who = who or s['player']
    return bool(records(s, who).get(key, {}).get('inspected') or
                who in INSIDERS and SITES[key]['faction'] == 'Syndicate')


def affiliation_known(s, key, who=None):
    who = who or s['player']
    return bool(records(s, who).get(key, {}).get('confirmed') or
                who in INSIDERS and SITES[key]['faction'] == 'Syndicate')


def label(s, key, who=None):
    if not known_name(s, key, who):
        return 'Unlabelled site '+key[-2:]+' · '+SITES[key]['district']
    return SITES[key]['name']


def detail(s, key, who=None):
    spec = SITES[key]
    text = ('Public frontage only. Travel here and inspect the exterior to identify the building.'
            if not known_name(s, key, who) else spec['exterior'])
    if affiliation_known(s, key, who):
        text += ' Known affiliation: '+spec['faction']+' · '+spec['role']+'.'
    text += ' Public reception is enterable from the frontage. Briefing rooms require individual clearance; command records require branch authority.'
    return text


def _guard(s, location):
    __import__('combat').guard(s)
    actor = s['world']['cast'][s['player']]
    if actor.get('journey') or s['world']['location'] != location or actor['location'] != location:
        raise ValueError('Visit '+('the public frontage' if location in SITES else
                         'the old town archive' if location == 'archive' else 'Interpol’s public desk')+' first.')


def _entry(s, key):
    return s.setdefault('city_sites', {'version': 1, 'people': {}}).setdefault('people', {}).setdefault(s['player'], {}).setdefault(key, {})


def inspect(s, key):
    if key not in SITES: raise ValueError('Choose a city site.')
    _guard(s, key)
    if records(s).get(key, {}).get('inspected'): raise ValueError('This exterior is already recorded in your notebook.')
    entry = _entry(s, key)
    entry.update(inspected=True, minute=s['world']['minute'], observation=SITES[key]['exterior'])
    return 'Recorded the public frontage of '+SITES[key]['name']+'.'


def research(s, key):
    if key not in SITES: raise ValueError('Choose a city site.')
    _guard(s, 'archive')
    prior = records(s).get(key, {})
    if not prior.get('inspected'): raise ValueError('Inspect the exterior and record its operator first.')
    if prior.get('researched'): raise ValueError('The public records are already in your notebook.')
    spec = SITES[key]
    if not spec['record']:
        note = 'Oculus’s public filings describe its legitimate businesses. They do not establish a criminal affiliation.'
    else:
        note = (spec['record']+' matches the operator in a published enforcement exhibit. '
                'The extract lacks its full certification page; verify the exhibit at Interpol’s public desk before drawing a conclusion.')
    _entry(s, key).update(researched=True, research=note)
    return note


def verify(s, key):
    if key not in SITES: raise ValueError('Choose a city site.')
    _guard(s, 'interpol_hq')
    entry = records(s).get(key, {})
    if not entry.get('researched'): raise ValueError('Read the matching public record at the archive first.')
    if not SITES[key]['record']: raise ValueError('There is no published evidence establishing an Oculus criminal affiliation.')
    if entry.get('confirmed'): raise ValueError('This published affiliation is already verified.')
    spec = SITES[key]
    note = (spec['record']+' matches the certified public exhibit: '+spec['name']+' operates as a '+
            spec['faction']+' '+spec['role']+'. This establishes the operator and site, not current occupants, '
            'a new crime, an invitation, or evidence about Charles.')
    _entry(s, key).update(confirmed=True, verification=note)
    return note


def notebook(s, key):
    entry = records(s).get(key, {})
    notes = [detail(s, key)]
    notes.extend(entry[field] for field in ('research', 'verification') if field in entry)
    return '\n\n'.join(notes)


def context(s, who, cue):
    """Only this speaker's knowledge; player discovery never informs the whole cast."""
    result = {}
    import crime_operations
    for key, spec in SITES.items():
        if crime_operations.site_of(s['world']['location']) == key or spec['name'].lower() in cue.lower() or ('oculus' in cue.lower() and key == 'site_07'):
            if known_name(s, key, who):
                result[spec['name']] = detail(s, key, who)
            elif key == 'site_07' and 'oculus' in cue.lower():
                result['Oculus public knowledge'] = 'A major technology, media, security, logistics and infrastructure corporation. No criminal affiliation is known to you.'
            else:
                result['Unidentified frontage'] = 'You have no recorded knowledge of this site’s operator or affiliation. A building or map pin is not proof.'
    if result:
        result['Privacy'] = 'Your private affiliation knowledge is not shared with listeners. Do not volunteer it or infer an outsider knows it. No dialogue can unlock an address, confirm an affiliation or grant entry.'
    return copy.deepcopy(result)
