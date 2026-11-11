"""Read-only starting and saved dossiers. Never calls save/load or an AI service."""
import copy
import combat_profiles
import combat_moves
import custom_protagonist


def starting(who, custom=None):
    import game_core as core
    import playable_cast
    import character_biographies
    import town
    from start_ui import CAST
    if custom is not None:
        p = custom_protagonist.validate(copy.deepcopy(custom))
        name = p['name']
        tag, hook, interests, accent = ('YOUR STORY', p.get('motivation') or 'A new life, on your terms.',
                                        ' · '.join(p['interests']), '#99d9c6')
        biography = p.get('biography') or 'An adult newcomer to Winterfield. Local relationships develop through play.'
        details = {'Age': p['age'], 'Height': f"{p['height']} cm", 'Occupation (descriptive)': p['occupation'],
                   'MBTI': p['mbti'], 'Home': custom_protagonist.home(p)[1], 'Starting funds (game balance)': '100,000',
                   'Employment': 'Looking for work', 'Hometown': p.get('hometown') or 'Unspecified',
                   'Preferred address': p.get('preferred_name') or name,
                   'Pronunciation': p.get('pronunciation') or 'Unspecified'}
        if p.get('private_history'):
            biography += '\n\nPrivate history · visible only to you in this dossier\n' + p['private_history']
        try:
            portrait = custom_protagonist.portrait_path(custom)
        except ValueError:
            portrait = None
        combat = combat_profiles.make('custom_preview', p)
        if p.get('origin'):
            import character_origins
            origin = character_origins.resolve(p['origin'], p['awakened'], bool(p.get('awakening_trait')))
            job = origin['employment']
            details['Employment'] = (f"{job['title']} · {job['venue']} · pay {job['pay']} · hours {job['hours'][0]}–{job['hours'][1]}" if job else 'Looking for work')
            details['Criminal background'] = p['origin']['crime']
            details['Affiliation'] = p['origin']['organisation'] or 'None'
            details['Starting standing'] = f"Reputation {origin['reputation']} · heat {origin['heat']}"
            details['Combat experience / target'] = origin['experience'] + ' · ' + origin['target']
            details['Stat contributions'] = '\n'.join(origin['contributions'])
    else:
        if who not in dict(core.PLAYERS):
            raise ValueError('Choose an available protagonist.')
        name = core.PLAYERS[who]
        tag, hook, interests, accent = CAST[who]
        spec = playable_cast.STARTS.get(who, {})
        biography = character_biographies.biography(who)
        details = {**character_biographies.facts(who),
                   'Home': town.HOMES.get(who, 'Unspecified').replace('_', ' ').title(),
                   'Starting funds (game balance)': f"{spec.get('money', 100000):,}",
                   'Starting activity': spec.get('title', 'See in-person work and story activities')}
        portrait = core.ROOT / 'assets' / 'portraits' / ('neo-scene.png' if who == 'neo' else who + '-selection.png')
        combat = combat_profiles.make(who)
    return dict(identity=who, label='Starting profile', name=name, tag=tag, hook=hook,
                interests=interests, accent=accent, biography=biography, details=details,
                portrait=portrait, combat=copy.deepcopy(combat), custom=custom is not None)


def saved(state, save_identity):
    """Saved progress belongs to the supplied snapshot, never the menu selection."""
    snapshot = copy.deepcopy(state)
    who = snapshot['player']
    dossier = starting(who, snapshot.get('custom_protagonist') if custom_protagonist.is_custom(who) else None)
    dossier['label'] = 'Saved progress · ' + str(save_identity)
    dossier['saved'] = True
    dossier['combat'] = copy.deepcopy(snapshot.get('combat', {}).get('profiles', {}).get(who))
    for key in list(dossier['details']):
        if key.startswith('Starting ') or key in ('Employment', 'Combat experience / target', 'Stat contributions', 'Criminal background', 'Affiliation'):
            del dossier['details'][key]
    dossier['details']['Current funds'] = snapshot.get('world', {}).get('money', 'Unspecified')
    if 'Occupation / studies' in dossier['details']:
        dossier['details']['Background occupation / studies'] = dossier['details'].pop('Occupation / studies')
    import job_apps
    jobs = snapshot.get('job_apps', {})
    job = jobs.get('employment')
    spec = job_apps.JOBS.get(job)
    if spec:
        rank = jobs.get('jobs', {}).get(job, {}).get('rank', 0)
        title = spec['ranks'][rank] if isinstance(rank, int) and 0 <= rank < len(spec['ranks']) else spec['title']
    else:
        title = job or snapshot.get('world', {}).get('job') or 'None recorded'
    dossier['details']['Current employment'] = title
    if jobs:
        dossier['details']['Recorded reputation / heat'] = f"{jobs.get('reputation', 'Unknown')} / {jobs.get('heat', 'Unknown')}"
    return dossier


def text(dossier, tab):
    if tab == 'Overview':
        if dossier.get('saved'):
            return f"{dossier['label']}\n\n{dossier['name']}\n\nRead-only snapshot of the selected save. Load / restore resumes this story. No starting values are substituted for missing saved combat progress."
        return f"{dossier['label']}\n\n{dossier['name']}\n{dossier['tag']}\n\n{dossier['hook']}\n\nInterests\n{dossier['interests']}\n\nA reusable profile begins a new story. Continue resumes your saved story independently of this selection."
    if tab == 'Backstory':
        return dossier['biography']
    if tab == 'Details':
        return '\n\n'.join(f'{k}\n{v}' for k, v in dossier['details'].items())
    p = dossier['combat']
    if not p:
        return 'No saved combat profile recorded. Starting values are not substituted for saved progress.'
    trait = p.get('trait')
    lines = [dossier['label'], 'Awakened' if p['awakened'] else 'Unawakened',
             'Path: ' + p.get('path', {}).get('stage', 'Not recorded'), '\nTrait: ' + (trait['name'] if trait else 'No named starting Trait')]
    if trait: lines.append(trait['description'])
    lines += ['\nRatings · game balance, not overall character quality']
    lines += [k.replace('_', ' ').title() + f': {v}/100' for k, v in p['stats'].items()]
    lines += ['\nMartial arts: ' + (', '.join(p['arts']) or 'No trained styles'), '\nRecorded techniques · baseline resource costs']
    book = p.get('moveset', {})
    moves = list(combat_moves.UTILITIES) + [combat_moves.MOVES[m] for m in book.get('learned', []) if m in combat_moves.MOVES]
    moves += book.get('unique', [])
    for move in moves:
        lines.append(f"{move['name']} · stamina {move.get('stamina', 0)} · mana {move.get('mana', 0)}")
    lines += ['\nTrait amplifications']
    for amp in p.get('moveset', {}).get('amplifications', []):
        lines.append(f"{amp['name']} · mana {amp.get('mana', 0)}\n{amp.get('description', '')}")
    card = p.get('path', {}).get('trump_card')
    if card:
        lines += ['\nEarned form: ' + card['name'], card['limitations']]
    lines += ['\nFuture advancement is earned in play. Conversation and romance do not award Awakening; Transcendence is not guaranteed.']
    return '\n'.join(lines)
