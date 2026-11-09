"""Additional canonical protagonists. Original starts and NPC registries stay intact.

Amounts and work rewards are sandbox balance, not claims about canonical wealth.
Story campaigns can be attached later without changing these stable character IDs.
"""
ORIGINAL = ('garrett', 'rei', 'minsu', 'ivan')
EXCLUDED = frozenset(('charles', 'thirteen', 'takeo', 'crow'))


def setup(venue, title, money, pay, hours, project, tasks, home, accent='#80c6ba', private=False):
    return dict(venue=venue, title=title, money=money, pay=pay, hours=hours,
                project=project, tasks=tasks, home=home, accent=accent, private=private)


STARTS = {
    'yuriko': setup('campus', 'Theatre design workshop', 14000, 0, (9, 18), 'Scale-model showcase',
        ('A model staircase blocks the lighting angle.', 'The group needs a portable set.', 'The showcase has less floor space than expected.'),
        ('Build a miniature set', 'Sketch a costume concept', 'Read a play'), '#b6a2df'),
    'emily': setup('flowers', 'Petal & Stem floristry', 22000, 240, (8, 18), 'Seasonal flower display',
        ('A bouquet must survive a warm afternoon.', 'A customer wants a quieter colour palette.', 'The display must fit a narrow shop window.'),
        ('Tend the balcony flowers', 'Build a LEGO arrangement', 'Sew a small plushie'), '#d49ab9'),
    'sophie': setup('track', 'Athletics training', 18000, 0, (6, 18), 'Track performance review',
        ('Your last interval slowed unexpectedly.', 'A training partner struggles with pacing.', 'Training and recovery compete for your afternoon.'),
        ('Stretch and review split times', 'Prepare tomorrow’s training meals', 'Plan a recovery evening'), '#9dc6a1'),
    'amy': setup('campus', 'Humanities and art study', 12000, 0, (9, 19), 'Illustrated philosophy portfolio',
        ('A sketch does not communicate your argument.', 'A seminar partner reads the image differently.', 'The portfolio needs a coherent final selection.'),
        ('Paint a small canvas', 'Read philosophy notes', 'Sketch in your dorm'), '#b9a4d8'),
    'samantha': setup('arena', 'Fighting technique workshop', 26000, 300, (12, 23), 'Controlled sparring exhibition',
        ('Your footwork leaves an opening.', 'A sparring partner needs a slower drill.', 'The exhibition needs clear stopping rules.'),
        ('Maintain your motorcycle', 'Practise controlled footwork', 'Check your training equipment'), '#d49879'),
    'april': setup('chess', 'Chess tuition', 30000, 400, (9, 20), 'Endgame teaching collection',
        ('A student memorises moves without understanding them.', 'Two variations lead to different endings.', 'The lesson collection needs a clear progression.'),
        ('Analyse a chess position', 'Read a scientific paper', 'Observe the night sky'), '#a4bbdd'),
    'lena': setup('archive', 'Archive conservation', 24000, 340, (9, 17), 'Community photograph exhibit',
        ('A photograph has a fragile handwritten caption.', 'Two public records disagree about a date.', 'The exhibit needs permission from a donor.'),
        ('Sort your film photographs', 'Read local history', 'Practise salsa steps'), '#d2ae7c'),
    'naomi': setup('cycle_shop', 'Bicycle repair', 28000, 420, (9, 18), 'Restored commuter bicycle',
        ('A wheel will not stay true.', 'A customer needs a comfortable riding position.', 'The restoration budget cannot cover every replacement.'),
        ('Shape a ceramic mug', 'Plan a climbing practice', 'Read a mystery novel'), '#91b4c6'),
    'celeste': setup('planetarium', 'Planetarium education', 25000, 350, (10, 21), 'Community night-sky programme',
        ('A sky demonstration is too complicated for beginners.', 'Cloud cover changes the evening plan.', 'The programme needs an accessible explanation of scale.'),
        ('Practise jazz piano', 'Bake a loaf of bread', 'Update your birdwatching notebook'), '#a9a7db'),
    'dev': setup('makerspace', 'Community repair bench', 20000, 320, (9, 19), 'Repair-clinic demonstration',
        ('A donated radio has an intermittent fault.', 'A visitor wants to learn instead of watching.', 'The clinic has more requests than workbench space.'),
        ('Repair a small electronic device', 'Arrange a tabletop game', 'Sort night photographs'), '#83bec4'),
    'rosa': setup('market', 'Community kitchen', 19000, 280, (8, 18), 'Neighbourhood recipe exchange',
        ('A recipe needs a less expensive ingredient.', 'Volunteers disagree about the serving rota.', 'The event needs a manageable menu.'),
        ('Test a shared recipe', 'Tend courtyard plants', 'Maintain your roller skates'), '#c6ad7b'),
    'elliot': setup('wetlands', 'Wetland ranger training', 16000, 220, (7, 17), 'Boardwalk survey report',
        ('A survey count needs checking.', 'A visitor mistakes a protected path for a shortcut.', 'The report must separate observations from guesses.'),
        ('Carve a small wooden bird', 'Review field recordings', 'Inspect kayaking equipment'), '#8eb7a5'),
    'tyler': setup('boxing_club', 'Boxing coaching', 21000, 360, (8, 20), 'Beginner boxing course',
        ('A beginner loses balance after a jab.', 'Two trainees need different practice speeds.', 'The next course needs room for recovery.'),
        ('Repair the loaner gloves', 'Set out a domino game', 'Listen to a baseball broadcast'), '#c5a181'),
    'valentina': setup('sailing_club', 'Sailing instruction', 38000, 550, (8, 17), 'Beginner sailing course',
        ('The wind changes before a lesson.', 'A newcomer hesitates at the tiller.', 'An old sail needs attention before the next course.'),
        ('Mend a sail', 'Review the tide notebook', 'Practise a karaoke verse'), '#84bfcf'),
    'daniel': setup('cinema', 'Repertory projection', 18000, 300, (12, 23), 'Repertory double feature',
        ('The print needs a careful inspection.', 'Two films compete for the same programme slot.', 'The lobby cards need a consistent design.'),
        ('Draw a lobby card', 'Review a film programme', 'Practise judo footwork'), '#b3a4cf'),
    'neo': setup('makerspace', 'Electronics repair', 23000, 380, (9, 18), 'Restored co-op controller set',
        ('A controller button fails intermittently.', 'A customer needs the repair explained plainly.', 'Two repairs compete for one spare component.'),
        ('Repair an old controller', 'Cook ginger pork rice bowls', 'Set up a co-op game'), '#8faeb9'),
    'alyssa': setup('archive', 'Bookbinding and repair', 20000, 320, (9, 17), 'Hand-bound botanical notebook',
        ('A book spine needs reinforcement.', 'A notebook commission requires different paper.', 'A binding design must lie flat for sketching.'),
        ('Bind a small notebook', 'Sketch a balcony herb', 'Prepare jasmine tea'), '#bca3d3'),
    'sylvanis': setup('syndicate_hq', 'Private patron oversight', 250000, 6000, (8, 23), 'Private patron review',
        ('Two branch reports contradict one another.', 'An intermediary challenges your proposed terms.', 'A patronage proposal promises more than its evidence supports.'),
        ('Review private research notes', 'Examine an opponent’s recorded technique', 'Reconsider a patronage proposal'), '#c18bc8', True),
    'martos': setup('downtown', 'Oculus security oversight', 95000, 1800, (8, 18), 'Security readiness review',
        ('A shift handover leaves a responsibility unclear.', 'A visitor-access procedure delays the staff.', 'An inspection exposes a maintenance gap.'),
        ('Restore a watch', 'Complete controlled strength training', 'Cook a rice dish'), '#b6aa89', True),
    'elias': setup('studio', 'Performance and rehearsal', 85000, 2200, (9, 20), 'Studio performance showcase',
        ('A rehearsal misses the intended timing.', 'A collaborator interprets the scene differently.', 'The final take needs a consistent performance style.'),
        ('Rehearse a performance', 'Review your recordings', 'Plan a quiet evening'), '#c4a4ce'),
    'mavis': setup('wetlands', 'Field recording practice', 70000, 0, (8, 19), 'Ambient sound collection',
        ('Wind obscures a field recording.', 'A recording site has unexpected visitors.', 'The collection needs a careful final edit.'),
        ('Repair a small object', 'Sort ambient recordings', 'Listen to the rain'), '#9cb9ae'),
    'camila': setup('downtown', 'Oculus financial review', 110000, 2400, (9, 18), 'Quarterly planning review',
        ('Two expense records disagree.', 'A projection relies on an untested assumption.', 'Competing proposals need a consistent comparison.'),
        ('Solve a chess problem', 'Read an architecture study', 'Review a personal budget'), '#9eafd2', True),
}

STARTS.update(
    fox=setup('blackhaven','Blackhaven patrol and liaison',32000,350,(10,24),'Neighbourhood protection review',
        ('A resident has an incomplete account of an incident.','A physical trace needs independent corroboration.','Patrol coverage leaves a residential street exposed.'),
        ('Maintain your field equipment','Review your private notebook','Practise controlled close combat'),'#93b5c3',True),
    gordon=setup('interpol_hq','Team 9 regional deployment',48000,650,(8,20),'Regional operational readiness',
        ('Two witness accounts disagree on timing.','Your team needs a controlled training plan.','A review must distinguish allegations from proof.'),
        ('Read a book off duty','Maintain your uniform and equipment','Prepare a quiet dinner'),'#79b7e3',True))

# The three choices feed craft, collaboration and autonomy respectively, but
# their actions belong to this person's work rather than a generic job prompt.
DECISIONS = {
    'yuriko': ('Rebuild the model at a smaller scale', 'Compare designs with the workshop group', 'Choose a simpler set that you can finish'),
    'emily': ('Rebalance the stems and colours', 'Ask the customer what matters most', 'Offer a smaller arrangement within the budget'),
    'sophie': ('Refine your stride and split targets', 'Review the session with a training partner', 'Shorten the session to protect recovery'),
    'amy': ('Revise the drawing and its argument', 'Compare interpretations with a seminar partner', 'Choose fewer pieces and develop them fully'),
    'samantha': ('Rehearse the opening at controlled speed', 'Work through the drill with your partner', 'Set a firm limit on the sparring intensity'),
    'april': ('Calculate the endgame variation', 'Ask the student to explain their reasoning', 'Teach one clear idea instead of three'),
    'lena': ('Check the original record carefully', 'Ask the donor about the missing context', 'Exhibit only material with verified permission'),
    'naomi': ('Measure and adjust the problem component', 'Explain the repair options to the rider', 'Prioritise the essential repair within budget'),
    'celeste': ('Rework the demonstration with a simple model', 'Invite the group to test their understanding', 'Choose a shorter programme with time for questions'),
    'dev': ('Trace the fault at the workbench', 'Let the visitor attempt the next step', 'Limit the repair queue to what you can finish'),
    'rosa': ('Test the ingredient substitution', 'Agree on a rota with the volunteers', 'Simplify the menu to keep the workload manageable'),
    'elliot': ('Repeat the observation and record uncertainty', 'Ask your supervisor to review the finding', 'Narrow the survey to accessible paths'),
    'tyler': ('Break the movement into slower steps', 'Ask the trainee what feels unstable', 'Stop the drill before fatigue spoils technique'),
    'valentina': ('Check the rigging and revise the lesson', 'Talk the newcomer through one controlled turn', 'Postpone the water session if conditions demand it'),
    'daniel': ('Inspect the print and projection timing', 'Compare programme notes with the team', 'Select a smaller double feature you can prepare well'),
    'neo': ('Isolate the intermittent circuit fault', 'Explain the test before attempting the repair', 'Set an honest limit on the repairs you can accept'),
    'alyssa': ('Test the paper grain and binding tension', 'Discuss how the notebook will be used', 'Choose a durable binding within the commission'),
    'sylvanis': ('Expose the contradiction in their account', 'Demand that the liaison defend the proposal', 'Withdraw patronage from an unconvincing proposal'),
    'martos': ('Audit the handover and access records', 'Clarify responsibilities with the shift leads', 'Reject a commitment the team cannot reliably cover'),
    'elias': ('Rehearse the timing of the scene', 'Try the collaborator’s interpretation', 'Keep control of the final performance choice'),
    'mavis': ('Adjust the microphone position and levels', 'Coordinate a quieter recording window', 'Keep a smaller collection of clear recordings'),
    'camila': ('Reconcile the records and test the assumption', 'Ask the budget owners to explain the discrepancy', 'Reject projections without adequate evidence'),
}


DECISIONS.update(fox=('Recheck the physical observations','Compare accounts with a willing witness','Limit the patrol to what you can cover'),
    gordon=('Verify the original record','Review the discrepancy with your team','Narrow the plan to a defensible objective'))

def is_new(who):
    return who in STARTS


def garage(who):
    # Player-only options do not alter the existing autonomous cast's vehicles.
    from protagonist_vehicles import GARAGES
    return GARAGES[who]


def voice(who, styles):
    import hidden_cast
    if who not in STARTS:
        import custom_protagonist
        return styles.get(who + '_player', custom_protagonist.VOICE)
    person = hidden_cast.CAST.get(who, {})
    return (styles.get(who, person.get('texting_style', 'Natural speech grounded in the character’s established personality.'))
            + ' Personality: ' + person.get('personality', '')
            + ' Adapt to the current spoken or text channel. Suggest optional first-person replies as this protagonist; '
              'never speak for the player, invent their feelings or rewrite their input. Preserve established ties and boundaries.')


def install(core):
    import town, careers, phone_personalization
    for who, spec in STARTS.items():
        core.PLAYERS[who] = core.CONTACTS[who][0]
        town.STARTING_RELATIONSHIPS[who] = {other: (0, 35, 0, 'strangers') for other in core.CONTACTS
                                          if town.romanceable({'player': who}, other)}
        town.HOME_ACTIONS[who] = list(spec['home'])
        town.CAREERS[who] = [(spec['venue'], spec['title'], spec['pay'], *spec['hours'])]
        key = 'cast_' + who
        decisions = DECISIONS[who]
        careers.TRACKS[key] = careers.track(who, spec['title'], spec['venue'], spec['hours'], spec['pay'], spec['project'],
            ('Workshop colleague', 'Review partner'), tuple((task, *decisions) for task in spec['tasks']), spec['private'])
        careers.POLICIES[key] = ('Precision', 'Collaboration', 'Sustainable pace')
        phone_personalization.PROFILES[who] = dict(accent=spec['accent'], favourites=[], names={},
            apps=['Messages', 'Calendar', 'Maps', 'Journal'], note=spec['project'] + '. Make time for ' + spec['home'][0].lower() + '.', messages=[])


def direction(state, members):
    if state['player'] not in STARTS: return ''
    text = ('The selected protagonist is ' + state['player'] + ', living their existing canonical life. '
            'Do not treat them as a newcomer, an NPC to be controlled, or one of the original four protagonists. '
            'They retain their own personality, family, occupation and established knowledge; private facts are not automatically shared with others. ')
    if state['player'] in ('neo', 'alyssa'):
        text += ('Neo and Alyssa are established committed partners. Their friendship-only player-route rules apply to other protagonists, '
                 'not to one another. When either is the protagonist, preserve their existing partnership, agency and consent; '
                 'do not describe them as strangers or invent a new courtship. Other romantic routes remain unavailable. ')
    return text


def seed(core, state):
    """New games only. Never reseed relationships, wealth or discoveries on load."""
    import town, world_loop, hidden_cast
    who = state['player']; spec = STARTS[who]
    home = world_loop.HOUSES[who][0]
    state['world'] = dict(location=home, money=spec['money'], inventory={}, job=None, last_shift_day=0, npcs=[], log=[])
    state['save_name'] = core.PLAYERS[who] + ' · ' + spec['title']
    state['playable_cast_version'] = 1
    relations = {other: dict(attraction=0, trust=35, closeness=0, status='strangers', known_betrayals=[]) for other in core.CONTACTS if other != who}
    for original in ORIGINAL:
        bond = town.STARTING_RELATIONSHIPS[original].get(who)
        if bond and bond[3] != 'strangers':
            relations[original].update(trust=bond[1], closeness=bond[2], status=bond[3])
    for pair, bond in world_loop.BONDS.items():
        members = pair.split(':')
        if who in members:
            other = members[1-members.index(who)]
            relations[other].update(trust=bond[1], closeness=bond[2], status=bond[0])
    siblings = {'yuriko': 'rei', 'valentina': 'ivan'}
    if who in siblings:
        relations[siblings[who]].update(trust=98, closeness=95, status='close siblings')
    if who in ('neo', 'alyssa'):
        partner = 'alyssa' if who == 'neo' else 'neo'
        relations[partner].update(attraction=80, trust=96, closeness=94, status='official')
        state['canonical_partner'] = partner
    if who == 'sylvanis':
        relations['ivan'].update(trust=5, closeness=0, status='hostile coworkers')
    if who in hidden_cast.SYNDICATE_MEMBERS:
        for other in hidden_cast.SYNDICATE_MEMBERS - {who}:
            if relations[other]['status'] == 'strangers':
                relations[other].update(trust=45, closeness=12, status='professional acquaintances')
    state['relationships'] = {k: v for k, v in relations.items() if town.romanceable(state, k)}
    state['friendships'] = {k: v for k, v in relations.items() if k not in state['relationships']}
    known = {k for k, v in relations.items() if v['status'] != 'strangers'}
    state['discoveries'] = {k: dict(met=k in known or k == who, contact=k in known and k != who,
        home=k == who or world_loop.HOUSES[k][0] == home) for k in core.CONTACTS}
    state['active'] = next(iter(sorted(known)), 'emily' if who != 'emily' else 'rei')
    state['routes'][who]['self_route'] = True
