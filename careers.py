"""Saved, deterministic careers. No generated outcomes, real sporting rules or AI calls."""
import custom_protagonist
import copy
from datetime import date
import uuid
import story_calendar as dates


def track(player, title, venue, hours, pay, project, contacts, situations, private=False):
    return dict(player=player, title=title, venue=venue, hours=hours, pay=pay,
                project=project, contacts=contacts, situations=situations, private=private)


# Contacts are authored workplace roles, not additions to the romance/contact roster.
# Each decision grants a different benefit: craft, trust or personal direction.
TRACKS = {
    'restaurant': track('garrett', 'Golden Dragon', 'noodle_shop', (9, 18), 1500,
        'Seasonal tasting night', ('Kitchen lead', 'Regular customer'), (
        ('The lunch queue is growing.', 'Refine the small-batch preparation', 'Help the team clear orders', 'Keep a smaller, sustainable menu'),
        ('A regular finds the trial broth too strong.', 'Test a gentler variation', 'Listen and remake the bowl', 'Keep the bold recipe and explain it'),
        ('The tasting menu needs a final identity.', 'Perfect the signature dish', 'Credit the kitchen team', 'Choose a personal family-inspired theme'))),
    'modelling': track('rei', 'Modelling', 'studio', (9, 18), 4000,
        'Editorial campaign', ('Returning photographer', 'Booking coordinator'), (
        ('The brief leaves room for interpretation.', 'Rehearse a difficult pose', 'Develop the brief with the photographer', 'Propose your own visual direction'),
        ('The shoot is running behind.', 'Focus on one technically strong frame', 'Help the crew simplify the setup', 'Negotiate a firm finishing time'),
        ('The client needs a final selection.', 'Refine the strongest image', 'Review the selection together', 'Protect your creative credit'))),
    'music': track('ivan', 'Music and performance', 'studio', (9, 18), 4500,
        'Independent recording', ('Session producer', 'Rehearsal coordinator'), (
        ('The chorus needs another approach.', 'Practise a demanding harmony', 'Listen to the producer’s alternative', 'Keep your own arrangement'),
        ('Rehearsal time is limited.', 'Work on the difficult transition', 'Coordinate a simpler ensemble take', 'Protect time for your own song'),
        ('The recording is ready for review.', 'Polish the vocal details', 'Credit the session team', 'Retain control of the final interpretation'))),
    'study': track('minsu', 'Medical studies', 'campus', (8, 18), 0,
        'Supervised learning portfolio', ('Academic tutor', 'Study-group peer'), (
        ('A teaching case has a confusing explanation.', 'Review the lecture evidence', 'Ask the tutor for feedback', 'Set a realistic study boundary'),
        ('The group is preparing a demonstration.', 'Refine the teaching diagram', 'Rehearse with your peers', 'Plan around your training commitment'),
        ('Your portfolio needs reflection.', 'Revise a weak explanation', 'Discuss what you learned', 'Write an honest account of your limits'))),
    'iron': track('rei', 'Iron Circle champion', 'iron_circle', (20, 24), 8000,
        'Title defence camp', ('Corner coach', 'Ring coordinator'), (
        ('The next challenger favours pressure.', 'Practise controlled counters', 'Review the footage with your corner', 'Protect recovery time'),
        ('A younger fighter asks for help.', 'Demonstrate careful footwork', 'Mentor them through a round', 'Set limits before your defence'),
        ('The defence approaches.', 'Refine your technical plan', 'Rehearse corner communication', 'Commit to a measured pace')), True),
    'dragons': track('garrett', 'Red Dragons leadership', 'syndicate', (20, 24), 5000,
        'Leadership review', ('Senior lieutenant', 'Community liaison'), (
        ('Two members disagree over responsibilities.', 'Review their competing accounts', 'Mediate and hear both sides', 'Set a clear boundary against intimidation'),
        ('A lieutenant requests more authority.', 'Define accountable responsibilities', 'Delegate with a review date', 'Retain a smaller personal workload'),
        ('An unresolved grievance returns.', 'Examine what the earlier decision changed', 'Invite a reconciliation meeting', 'Commit to a reform of the disputed policy')), True),
    'joker': track('ivan', 'Joker Card responsibilities', 'syndicate_hq', (20, 24), 6000,
        'Cross-branch review', ('Branch liaison', 'Executive coordinator'), (
        ('Two branches demand your attention.', 'Compare the competing obligations', 'Arrange a joint discussion', 'Negotiate limits on your availability'),
        ('A colleague questions your priorities.', 'Explain a consistent decision', 'Hear the objection privately', 'Protect your independent commitments'),
        ('Another demand threatens your recording time.', 'Resolve the outstanding review', 'Delegate the follow-up responsibly', 'Negotiate greater personal autonomy')), True),
    'taekwondo': track('minsu', 'Olympic taekwondo ambition', 'arena', (8, 20), 0,
        'Competition preparation', ('Taekwondo coach', 'Training partner'), (
        ('Your next opponent controls distance.', 'Practise precise entries', 'Review sparring with your coach', 'Choose a sustainable training load'),
        ('A training round exposes a weakness.', 'Practise the technical correction', 'Ask your partner for feedback', 'Stop before fatigue harms the session'),
        ('Competition and studies share the week.', 'Rehearse your competition plan', 'Coordinate with your support team', 'Protect recovery and study time'))),
}

PATHWAY = ('Local open', 'Regional championship', 'National trials',
           'International selection event', 'Olympic tournament')
RIVALS = (('Pressure specialist', 60), ('Counter specialist', 66), ('Distance specialist', 72))

# New sessions snapshot their situations so loading a save never rewrites a choice.
# Legacy active sessions continue to use TRACKS' original three situations.
CRIME_SITUATIONS = {
    'dragons': (
        ('A family helped by the Red Dragons says a lieutenant now expects unpaid favours.',
         'Document the demand for review', 'Hear the family without the lieutenant present', 'Refuse to make aid conditional on favours'),
        ('A witness offers a statement but refuses to involve their friend.',
         'Record only the evidence they offer', 'Arrange a private liaison appointment', 'Keep the friend outside the protection plan'),
        ('Residents report Blue Magic sales along a Shinokami expansion corridor supported by the Syndicate. Red Dragons policy forbids narcotics sales; the report does not identify individual suppliers.',
         'Compare the consignment records', 'Ask the liaison to verify the contractor', 'Refuse narcotics revenue and prioritise civilian grievances')),
    'joker': (
        ('Diamonds and Clubs disagree over support for Shinokami expansion. The Crow plans a later betrayal; Ivan must coordinate support without exposing that plan.',
         'Reconcile the two reports', 'Request a joint accountable review', 'Hold approval until the discrepancy is explained'),
        ('Hearts wants favourable coverage of a Conclave-linked collection whose ownership record has gaps.',
         'Check the documented provenance', 'Ask both branches to correct the brief', 'Decline to endorse an unverified claim'),
        ('A recruiter proposes binding an Awakened recruit through debt. Valentina asks for your decision as a general.',
         'Audit the proposed obligations', 'Back Valentina in demanding voluntary terms', 'Reject recruitment through coercive debt')),
    'iron': (
        ('A promoter offers a dangerous Awakened matchup with little recovery time.',
         'Review the opponent’s observed techniques', 'Ask your corner to challenge the terms', 'Refuse the short-notice offer'),
        ('A promoter asks fighters to conceal injuries to keep the card profitable.',
         'Document the pressure without claiming a diagnosis', 'Support confidential medical assessment', 'Refuse an injury-concealment agreement'),
        ('A security recruiter wants private fighter details; Blackstone’s name is on the card, but their purpose is unverified.',
         'Keep a record of the request', 'Ask the ring coordinator to verify authority', 'Decline to disclose other fighters’ information')),
}


def current_situation(active):
    situations = active.get('situations', TRACKS[active['track']]['situations'])
    return situations[(active['scenario'] + len(active['choices'])) % len(situations)]

POLICIES = {
    'dragons': ('Accountability', 'Loyalty', 'Reform'),
    'joker': ('Fulfil responsibilities', 'Delegate fairly', 'Build independence'),
    'restaurant': ('Signature quality', 'Team development', 'Sustainable service'),
    'modelling': ('Technical craft', 'Collaboration', 'Creative ownership'),
    'music': ('Technical craft', 'Collaboration', 'Creative ownership'),
    'study': ('Evidence', 'Peer learning', 'Study balance'),
    'iron': ('Technical control', 'Mentorship', 'Longevity'),
    'taekwondo': ('Technique', 'Team feedback', 'Recovery balance'),
}


def available(s):
    return [key for key, spec in TRACKS.items() if spec['player'] == s['player']]


def ensure(s):
    data = s.setdefault('careers', dict(version=1, tracks={}, bookings=[], history=[], shares=[], active=None))
    for key in available(s):
        data['tracks'].setdefault(key, dict(craft=72 if key != 'study' else 45,
            reputation=65, reliability=70, autonomy=35, fatigue=0, pressure=0,
            last_day=-1, training_day=-1, recovery_day=-1, training=0,
            project=None, completed=0, policy=POLICIES[key][0],
            contacts={name: dict(trust=50, competence=60+i*12) for i, name in enumerate(TRACKS[key]['contacts'])},
            delegation=None, rank=1 if key == 'iron' else None, defences=0,
            defence_due=None, stage=0, medals=[], last_competition=-8,
            recovery_until=0, last_tick_day=s['world']['minute']//1440))
    return data


def get(s, key):
    if key not in available(s):
        raise ValueError('This career belongs to another protagonist.')
    return ensure(s)['tracks'][key]


def clamp(value):
    return max(0, min(100, value))


def record(s, key, text):
    import town, memory_store
    data = ensure(s)
    ident=uuid.uuid5(uuid.NAMESPACE_URL,f'career:{key}:{s["world"]["minute"]}:{len(data["history"])}').hex
    item = dict(id=ident, track=key, minute=s['world']['minute'], text=text)
    data['history'].append(item)
    memory_store.add(s, source='career:'+item['id'], text=text, owners=[s['player']],
                     location=s['world']['location'], minute=s['world']['minute'], importance=3)
    town.log(s, 'Private career journal updated.' if TRACKS[key]['private'] else text)
    return item


def conflict(s, start, end, exclude=None):
    import syndicate_council
    syndicate_council.ensure(s)
    import crime_diplomacy
    events = [e for e in s.get('scheduled_events', []) if not e.get('cancelled')]
    events += [e for e in crime_diplomacy.commitments(s) if e['id']!=exclude]
    bookings = [e for e in s.get('careers', {}).get('bookings', []) if e['status'] == 'booked' and e['id'] != exclude]
    return next((e for e in events+bookings if start < e['end'] and e['start'] < end), None)


def guard(s, key, duration=0, booking=None, venue=None):
    __import__('combat').guard(s)
    get(s, key)
    if ensure(s)['active']:
        raise ValueError('Finish or abandon your current work session first.')
    actor = s['world']['cast'][s['player']]
    if actor.get('journey'):
        raise ValueError('Finish travelling first.')
    import autonomy
    needs=autonomy.person(s, s['player'])
    if (needs.get('sleep_until') or 0) > s['world']['minute']:
        raise ValueError('Wake up before starting work.')
    if venue is not None and s['world']['location'] != venue:
        import town
        raise ValueError('Visit '+town.LOCATIONS[venue]+' first.')
    if duration and conflict(s, s['world']['minute'], s['world']['minute']+duration, booking):
        raise ValueError('This would overlap an accepted commitment. Reschedule or cancel it first.')


def spend_time(s, minutes, fatigue=0):
    import world_loop, autonomy
    world_loop.advance(s, minutes)
    needs = autonomy.person(s, s['player'])
    needs['energy'] = clamp(needs['energy']-fatigue/2)


def start_project(s, key):
    d = get(s, key)
    if d['project']:
        raise ValueError('Finish or extend the current project first.')
    title=TRACKS[key]['project']
    if d['completed'] and d['reputation']>=75:
        title={'restaurant':'Guest tasting commission','modelling':'Creative lead campaign',
               'music':'Self-directed performance','study':'Peer teaching presentation',
               'dragons':'Delegated leadership council','joker':'Independent commitments agreement',
               'iron':'Championship rematch camp','taekwondo':'Advanced competition preparation'}.get(key, 'Advanced ' + TRACKS[key]['project'])
    d['project'] = dict(title=title, started=s['world']['minute'],
        deadline=s['world']['minute']+7*1440, days=[], quality=0, extended=False, overdue=False)
    if key == 'iron' and d['defence_due'] is None:
        d['defence_due'] = s['world']['minute']+14*1440
    return record(s, key, 'Started '+d['project']['title']+'. Prepare on three separate days, then complete the review or competition.')


def set_policy(s, key, policy):
    d = get(s, key)
    if policy not in POLICIES[key]:
        raise ValueError('Choose an available direction.')
    d['policy'] = policy


def extend_project(s, key):
    d = get(s, key); p = d['project']
    if not p or p['extended']:
        raise ValueError('A project can be extended once.')
    p.update(deadline=max(s['world']['minute'], p['deadline'])+3*1440, extended=True, overdue=False)
    d['reliability'] = clamp(d['reliability']-2)
    return record(s, key, 'Negotiated three more days for '+p['title']+'; reliability -2.')


def book(s, key, day, time, kind='shift', duration=60, replace=None):
    d = get(s, key); spec = TRACKS[key]
    if kind not in ('shift', 'finale') or duration not in (60, 120):
        raise ValueError('Choose a 60 or 120 minute shift, or a 60 minute finale.')
    if kind == 'finale' and duration != 60:
        raise ValueError('Reviews and competitions last 60 minutes.')
    try:
        hour, minute = map(int, time.split(':'))
        if not 0 <= hour < 24 or not 0 <= minute < 60: raise ValueError()
        start = (date.fromisoformat(day)-dates.START).days*1440+hour*60+minute
    except (ValueError, TypeError):
        raise ValueError('Enter a valid date and time (YYYY-MM-DD and HH:MM).') from None
    if start <= s['world']['minute']:
        raise ValueError('Choose a future time.')
    if not spec['hours'][0]*60 <= start%1440 or start%1440+duration > spec['hours'][1]*60:
        raise ValueError('The entire booking must fit within workplace hours.')
    old = next((b for b in ensure(s)['bookings'] if b['id'] == replace), None)
    if replace and (old is None or old['status'] != 'booked' or old['start'] <= s['world']['minute'] or old['track'] != key):
        raise ValueError('Only a future booking on this career can be rescheduled.')
    if conflict(s, start, start+duration, replace):
        raise ValueError('You already have a commitment at that time.')
    item = dict(id=uuid.uuid4().hex, track=key, title=spec['title']+(' · review / competition' if kind=='finale' else ' · work'),
                start=start, end=start+duration, venue=spec['venue'], kind=kind, status='booked', reminded=[])
    if old: old['status'] = 'rescheduled'
    ensure(s)['bookings'].append(item)
    return item


def cancel(s, ident):
    item = next((b for b in ensure(s)['bookings'] if b['id'] == ident), None)
    if not item or item['status'] != 'booked': raise ValueError('This booking is no longer pending.')
    item['status'] = 'cancelled'
    d = get(s, item['track'])
    late = s['world']['minute'] >= item['start']
    if late: d['reliability'] = clamp(d['reliability']-3)
    return record(s, item['track'], 'Cancelled '+item['title']+(' after its start; reliability -3.' if late else ' ahead of time; no penalty.'))


def begin(s, key, duration=60, booking_id=None):
    d = get(s, key); spec = TRACKS[key]; now = s['world']['minute']
    if duration not in (60, 120): raise ValueError('Choose a 60 or 120 minute session.')
    b = None
    if booking_id:
        b = next((b for b in ensure(s)['bookings'] if b['id']==booking_id and b['track']==key), None)
        if not b or b['status'] != 'booked' or not b['start'] <= now < b['end']:
            raise ValueError('Join an accepted booking during its scheduled time.')
        duration = b['end']-b['start']
        if now-b['start']>15:
            raise ValueError('The 15-minute arrival window has passed. Cancel and rebook.')
        if b['kind'] == 'finale': return finish_project(s, key, b['id'])
    actual_duration=b['end']-now if b else duration
    guard(s, key, actual_duration, booking_id, spec['venue'])
    if not spec['hours'][0]*60 <= now%1440 or now%1440+actual_duration > spec['hours'][1]*60:
        raise ValueError('The full session must fit inside workplace hours.')
    if d['last_day'] == now//1440: raise ValueError('You have already worked on this career today.')
    if d['fatigue'] >= 85 or now < d['recovery_until']:
        raise ValueError('Recover before another demanding work session.')
    # Honour legacy daily booking locks when loading an old story.
    import town
    index = next((i for i, item in enumerate(town.CAREERS[s['player']]) if item[0]==spec['venue']), None)
    legacy_key = f'{now//1440}:{s["player"]}:{index}'
    if index is not None and legacy_key in s['world'].get('career_shifts', []):
        raise ValueError('This career booking was already completed today.')
    if b: b['status'] = 'in_progress'
    d['last_day'] = now//1440
    ensure(s)['active'] = dict(track=key, start=now, end=now+actual_duration, venue=spec['venue'], duration=duration,
                              booking=booking_id, choices=[], scenario=(now//1440)%3)
    if key in CRIME_SITUATIONS:
        ensure(s)['active']['situations'] = copy.deepcopy(CRIME_SITUATIONS[key])
        ensure(s)['active']['decisions'] = []
    return ensure(s)['active']


def choose(s, choice):
    a = ensure(s)['active']
    if not a or choice not in (0, 1, 2): raise ValueError('Choose an option in the active session.')
    actor = s['world']['cast'][s['player']]
    if actor.get('journey') or s['world']['location'] != a['venue']:
        raise ValueError('Return to your workplace to finish, or abandon the session.')
    if 'decisions' in a:
        scenario = current_situation(a)
        a['decisions'].append(dict(situation=scenario[0], choice=scenario[choice+1]))
    a['choices'].append(choice)
    if len(a['choices']) < 2: return a
    key=a['track']; d=get(s,key); spec=TRACKS[key]; p=d['project']
    effort = 2 if a['duration']==120 else 1
    for selected in a['choices']:
        stat = ('craft', 'reputation', 'autonomy')[selected]
        d[stat] = clamp(d[stat]+2*effort)
        person = spec['contacts'][len(a['choices'])%2] if selected==0 else spec['contacts'][selected-1]
        d['contacts'][person]['trust'] = clamp(d['contacts'][person]['trust']+(3 if selected==1 else 1))
    policy_choice = POLICIES[key].index(d['policy'])
    quality = 10+sum(3 if c==policy_choice else 1 for c in a['choices'])+effort*2
    if p and a['start']//1440 not in p['days']:
        p['days'].append(a['start']//1440); p['quality'] += quality
    d['fatigue'] = clamp(d['fatigue']+12*effort-4*a['choices'].count(2))
    d['reliability'] = clamp(d['reliability']+2)
    if key in ('dragons','joker'): d['pressure'] = clamp(d['pressure']+4-5*a['choices'].count(1)-3*a['choices'].count(2))
    # Competitive preparation pays nothing; prize money is earned at the bout.
    pay = 0 if key in ('iron','taekwondo') else spec['pay']*effort
    s['world']['money'] += pay
    if a['booking']:
        next(b for b in ensure(s)['bookings'] if b['id']==a['booking'])['status']='completed'
    ensure(s)['active'] = None
    remaining = max(0, a['end']-s['world']['minute'])
    spend_time(s, remaining, 12*effort)
    s['world']['job'] = spec['title']; s['turn'] += 1
    result = record(s, key, f'{spec["title"]}: completed {a["duration"]} minutes; earned ${pay:,}. Direction: {d["policy"]}.')
    if a.get('decisions'):
        details = ' '.join(item['situation']+' Decision: '+item['choice']+'.' for item in a['decisions'])
        decision_record = record(s, key, details + ' These are recorded work decisions; requests remain pending and no investigation, treatment, recruitment or bout outcome is established.')
        decision_record['decisions'] = copy.deepcopy(a['decisions'])
        decision_record['effects'] = dict(craft=d['craft'], reputation=d['reputation'], autonomy=d['autonomy'],
                                          fatigue=d['fatigue'], pressure=d['pressure'])
    if not spec['private']:
        s['world']['camera_activity'] = dict(text=result['text'], location=spec['venue'], minute=s['world']['minute'])
    return result


def abandon(s):
    a=ensure(s)['active']
    if not a: raise ValueError('There is no active session.')
    d=get(s,a['track']); d['reliability']=clamp(d['reliability']-3)
    if a['booking']: next(b for b in ensure(s)['bookings'] if b['id']==a['booking'])['status']='abandoned'
    ensure(s)['active']=None
    return record(s,a['track'],'Abandoned the session; no pay or project progress; reliability -3.')


def quick(s, key):
    begin(s,key)
    choose(s,1)
    return choose(s,2)


def prepare(s, key, focus):
    d=get(s,key); now=s['world']['minute']
    if focus not in ('technique','feedback','recovery'): raise ValueError('Choose a preparation focus.')
    venue = 'arena' if key in ('iron','taekwondo') and focus!='recovery' else None
    guard(s,key,60,venue=venue)
    if focus=='recovery':
        import town
        if s['world']['location'] != town.HOMES[s['player']]: raise ValueError('Return home to recover.')
        if d['recovery_day']==now//1440: raise ValueError('Recovery already completed today.')
        d['recovery_day']=now//1440; d['fatigue']=max(0,d['fatigue']-30)
    else:
        if venue is None and s['world']['location']!=TRACKS[key]['venue']: raise ValueError('Visit your workplace to prepare.')
        if d['training_day']==now//1440: raise ValueError('Preparation already completed today.')
        if now<d['recovery_until'] or d['fatigue']>=75: raise ValueError('Rest before more preparation.')
        d['training_day']=now//1440; d['training']=min(6,d['training']+1)
        d['fatigue']=clamp(d['fatigue']+10)
        if focus=='technique': d['craft']=clamp(d['craft']+2)
        else:
            person=TRACKS[key]['contacts'][0]
            d['contacts'][person]['trust']=clamp(d['contacts'][person]['trust']+5)
    spend_time(s,60,0 if focus=='recovery' else 8)
    return record(s,key,TRACKS[key]['title']+': completed '+focus+' preparation (60 minutes).')


def delegate(s,key,person):
    d=get(s,key)
    if key not in ('dragons','joker'): raise ValueError('Delegation is available for leadership careers.')
    if person not in d['contacts']: raise ValueError('Choose a member of this team.')
    guard(s,key,30,venue=TRACKS[key]['venue'])
    if d['delegation']: raise ValueError('Review the outstanding delegation first.')
    if not d['project']: raise ValueError('Start a leadership project first.')
    d['delegation']=dict(person=person,due=s['world']['minute']+1440,reviewed=False)
    spend_time(s,30,2)
    return record(s,key,'Delegated the follow-up to '+person+'. Review their report tomorrow.')


def review_delegation(s,key):
    d=get(s,key); task=d['delegation']
    guard(s,key,30,venue=TRACKS[key]['venue'])
    if not task or s['world']['minute']<task['due']: raise ValueError('The report is not ready yet.')
    person=d['contacts'][task['person']]
    strong=person['competence']+person['trust']>=115
    person['trust']=clamp(person['trust']+5); person['competence']=clamp(person['competence']+3)
    if d['project']: d['project']['quality']+=10 if strong else 5
    d['pressure']=clamp(d['pressure']+(-8 if strong else 3)); d['delegation']=None
    spend_time(s,30,2)
    return record(s,key,task['person']+(': delivered a clear report.' if strong else ': needed guidance; the review improved their experience.'))


def finish_project(s,key,booking_id):
    if key=='iron' and s.get('combat',{}).get('ledger'):
        raise ValueError('Your signed circuit uses Combat in the in-person window. Attend its next card; legacy career finales cannot decide circuit fights.')
    d=get(s,key); p=d['project']; now=s['world']['minute']; spec=TRACKS[key]
    b=next((b for b in ensure(s)['bookings'] if b['id']==booking_id and b['track']==key),None)
    if not b or b['kind']!='finale' or b['status']!='booked' or not b['start']<=now<=b['start']+15:
        raise ValueError('Start your scheduled review or competition at its booked time.')
    guard(s,key,b['end']-now,booking_id,spec['venue'])
    if not p or len(p['days'])<3: raise ValueError('Complete project work on three separate days first.')
    if d['delegation']: raise ValueError('Review the delegated report before completing this project.')
    if d['fatigue']>=85 or now<d['recovery_until']: raise ValueError('You need recovery before the finale.')
    competitive=key in ('iron','taekwondo')
    if competitive and (d['training']<2 or now//1440-d['last_competition']<7):
        raise ValueError('Prepare at least twice and allow seven days between competitions.')
    score=d['craft']*.55+min(30,p['quality']/2)+d['training']*3-d['fatigue']*.3
    if key in ('dragons','joker'): score-=d['pressure']*.2
    score += d['reliability']*.1
    score -= 8 if p['overdue'] else 0
    if key=='iron':
        rival, target=RIVALS[d['defences']%len(RIVALS)]
        score+=5 if d.get('match_plan')==('Counter patiently','Draw out an attack','Close distance carefully')[d['defences']%3] else 0
        won=score>=target
        d['rank']=1 if won else 2; d['defences']+=1
        d['defence_due']=now+14*1440; d['last_competition']=now//1440
        outcome=('Won against '+rival+'; rank #1 retained or reclaimed.' if won else 'Lost to '+rival+'; rank #2. A rematch camp is available.')
        if won: s['world']['money']+=spec['pay']
        else: d['recovery_until']=now+2*1440
    elif key=='taekwondo':
        stage=d['stage']; target=58+min(stage,4)*4; won=score>=target
        event=PATHWAY[stage] if stage<5 else 'Post-Games invitational'; d['last_competition']=now//1440
        if won and stage<4: d['stage']+=1
        if won and stage==4:
            medal='Gold' if score>=88 else 'Silver' if score>=82 else 'Bronze'
            d['medals'].append(dict(medal=medal,minute=now)); d['stage']=5; outcome=event+': '+medal+' medal.'
        elif stage==5: outcome=event+(': won.' if won else ': a learning result; prepare for another attempt.')
        else: outcome=event+(': advanced to the next stage.' if won else ': did not advance; prepare for another attempt.')
        if not won: d['recovery_until']=now+1440
    else:
        won=score>=60
        outcome=p['title']+(': successful review.' if won else ': completed with revisions requested; the next project is a chance to improve.')
    d['completed']+=1; d['reputation']=clamp(d['reputation']+(5 if won else -2))
    d['fatigue']=clamp(d['fatigue']+20); d['training']=0; d['project']=None
    b['status']='completed'
    spend_time(s,b['end']-now,15)
    reward = (' Keepsake: '+p['title']+'.' if won else '')
    if won:
        s.setdefault('career_keepsakes',[]).append(dict(track=key,title=p['title'],minute=now,outcome=outcome))
    return record(s,key,outcome+reward)


def tick(s):
    # Do not enrol players, create deadlines or penalise old saves just by loading.
    data=s.get('careers')
    if not data: return
    now=s['world']['minute']; day=now//1440
    active=data.get('active')
    if active and now>=active['end']:
        abandon(s)
    for key,d in data['tracks'].items():
        if key=='iron' and s.get('combat',{}).get('ledger'):
            d['rank']=s['combat']['ledger']['rank']; d['defence_due']=None
        elapsed=max(0,day-d['last_tick_day'])
        if elapsed:
            d['fatigue']=max(0,d['fatigue']-8*elapsed); d['last_tick_day']=day
        p=d['project']
        if p and now>p['deadline'] and not p['overdue']:
            p['overdue']=True; d['reliability']=clamp(d['reliability']-5)
            record(s,key,'Project overdue: '+p['title']+'. Reliability -5; extend once or finish late.')
        task=d['delegation']
        if task and now>task['due']+2*1440 and not task.get('late'):
            task['late']=True; d['pressure']=clamp(d['pressure']+10)
            record(s,key,'An unreviewed delegation has returned as an unresolved concern; pressure +10.')
        if key=='iron' and d['defence_due'] is not None and now>d['defence_due']:
            d['rank']=2; d['defence_due']=None
            record(s,key,'The title defence deadline passed; rank #2. Prepare a comeback camp to reclaim #1.')
    for b in data['bookings']:
        if b['status']!='booked': continue
        for lead in (60,15,0):
            if now>=b['start']-lead and now<=b['start'] and lead not in b['reminded']:
                b['reminded'].append(lead)
                s.setdefault('event_notifications',[]).append(b['title']+(' starts now.' if lead==0 else f' in {lead} minutes.'))
        if now>=b['end']:
            b['status']='missed'; d=data['tracks'][b['track']]
            d['reliability']=clamp(d['reliability']-5)
            for person in d['contacts'].values(): person['trust']=clamp(person['trust']-2)
            record(s,b['track'],'Missed '+b['title']+'. Reliability -5; book a new commitment to rebuild trust.')


def share(s, key, who):
    import hidden_cast, memory_store
    get(s,key)
    if who==s['player'] or who not in s['world']['cast'] or not hidden_cast.contact(s,who): raise ValueError('Choose an existing contact.')
    item=next((i for i in reversed(ensure(s)['history']) if i['track']==key),None)
    if not item: raise ValueError('Complete an activity before sharing an update.')
    if any(x['id']==item['id'] and x['recipient']==who for x in ensure(s)['shares']):
        raise ValueError('You already shared this update with that contact.')
    ensure(s)['shares'].append(dict(id=item['id'],recipient=who,text=item['text'],track=key))
    memory_store.add(s,source='career-share:'+item['id']+':'+who,text=custom_protagonist.display_name(s["player"])+' shared: '+item['text'],
                     owners=[s['player'],who],minute=s['world']['minute'],importance=3)


def context(s, members):
    if not members: return []
    return [copy.deepcopy(x) for x in s.get('careers',{}).get('shares',[]) if set(members).issubset({x['recipient'],s['player']})][-8:]


def match_plan(s,key,value):
    d=get(s,key)
    if key!='iron' or value not in ('Counter patiently','Draw out an attack','Close distance carefully'):
        raise ValueError('Choose a valid Iron Circle plan.')
    d['match_plan']=value


def casual_work(s):
    """Local shifts remain a low-complexity alternative to protagonist careers."""
    import town
    w=town.ensure(s); venue=w['location']; now=w['minute']
    if venue not in town.JOBS: raise ValueError('Visit a local workplace first.')
    if w['last_shift_day']==now//1440+1: raise ValueError('You already completed a local shift today.')
    guard(s,available(s)[0],60,venue=venue)
    if not 8*60<=now%1440<=19*60: raise ValueError('Local shifts run between 08:00 and 20:00.')
    data=ensure(s).setdefault('local_jobs',{})
    job=data.setdefault(venue,dict(shifts=0,reliability=50))
    name,pay=town.JOBS[venue]
    pay+=min(100,job['shifts']//3*20)
    job['shifts']+=1; job['reliability']=clamp(job['reliability']+2)
    w['last_shift_day']=now//1440+1; w['job']=name; w['money']+=pay
    spend_time(s,60,12); s['turn']+=1
    return town.log(s,f'{name}: 60-minute shift completed; earned ${pay:,}. Local reliability {job["reliability"]}.')
