"""Civilian career development; deterministic, save-local and independent of crime."""

# Workplace roles deliberately do not grant cast contacts or security clearance.
WORKPLACES = {
    'photographer': ('Portrait exhibition', 'Lighting specialist', 'Client producer', 'Studio producer', 'A portrait has uneven lighting.', 'The client changes the selection.', 'An assistant needs a clear handover.'),
    'model': ('Seasonal campaign', 'Editorial specialist', 'Campaign coordinator', 'Booking coordinator', 'The campaign needs a difficult pose.', 'The fitting schedule has changed.', 'A new model needs rehearsal support.'),
    'librarian': ('Community reading programme', 'Archive specialist', 'Community coordinator', 'Head librarian', 'A catalogue record is incomplete.', 'Two groups request the same room.', 'A volunteer needs accessible instructions.'),
    'oculus': ('Visitor service redesign', 'Reception specialist', 'Service coordinator', 'Reception supervisor', 'A visitor has incomplete confirmation.', 'Two public appointments overlap.', 'A new receptionist needs a public-desk handover.'),
    'cinema': ('Community film festival', 'Projection specialist', 'Events coordinator', 'Duty manager', 'A screening needs a sound check.', 'A delayed screening creates a queue.', 'An usher needs a revised seating plan.'),
    'barista': ('Seasonal café launch', 'Coffee specialist', 'Service coordinator', 'Café owner', 'A new blend needs calibration.', 'The lunch queue exceeds capacity.', 'A trainee needs a simpler station plan.'),
    'florist': ('Community celebration display', 'Floral designer', 'Events coordinator', 'Shop owner', 'A fragile arrangement needs rebuilding.', 'A collection deadline has moved.', 'A junior florist needs a packing demonstration.'),
    'chef': ('Seasonal menu launch', 'Menu specialist', 'Kitchen coordinator', 'Kitchen lead', 'A dish needs a consistent finish.', 'A booking changes its menu request.', 'A new cook needs a station handover.'),
    'retail': ('Accessible shopping event', 'Merchandising specialist', 'Service coordinator', 'Store supervisor', 'A display needs clearer product information.', 'A delivery arrives during a busy period.', 'A colleague needs help with returns.'),
    'arcade': ('Community tournament', 'Cabinet specialist', 'Tournament coordinator', 'Floor supervisor', 'A cabinet needs a maintenance check.', 'Tournament entrants dispute the queue.', 'An attendant needs an accessible event plan.'),
    'gardener': ('Neighbourhood garden opening', 'Planting specialist', 'Grounds coordinator', 'Grounds lead', 'A planting bed needs careful preparation.', 'An event needs a safe pedestrian route.', 'Volunteers need a manageable work plan.'),
    'bartender': ('Community evening launch', 'Drinks specialist', 'Service coordinator', 'Venue manager', 'A drinks menu needs consistent preparation.', 'Several bookings arrive together.', 'A colleague needs help pacing service.'),
}
COURSES = {
    'craft': ('Professional practice', 120, 'craft', 4),
    'service': ('Client communication', 100, 'service', 4),
    'leadership': ('Team leadership', 160, 'leadership', 4),
}
TITLES = ('Department lead', 'Regional coordinator', 'Regional director', 'Career fellow')
# shifts, craft, reliability, certificates, delivered projects, professional standing
REVIEWS = ((24, 48, 78, 1, 1, 20), (36, 72, 82, 2, 3, 40),
           (50, 100, 86, 3, 5, 60), (70, 140, 90, 3, 8, 80))


def ensure(s):
    d = s['job_apps']
    for key, value in dict(saved_jobs=[], training_day=-1, networking_day=-1).items():
        d.setdefault(key, value)
    return d


def upgrade(p):
    for key, value in dict(service=0, leadership=0, standing=0, mentor=0, team=0,
                           courses={}, certificates=[], specialty=None, project=None,
                           portfolio=[], earnings=0, management_day=-1, budget=0,
                           morale=50, initiatives=0).items():
        p.setdefault(key, value)
    return p


def current(s):
    import job_apps as jobs
    d = jobs.ensure(s)
    if not d['employment']:
        raise ValueError('Apply for a career first.')
    key = d['employment']
    return key, jobs.profile(s, key)


def titles(key):
    import job_apps as jobs
    return (*jobs.JOBS[key]['ranks'], *TITLES)


def wage(key, p):
    import job_apps as jobs
    return jobs.JOBS[key]['pay'] + p['rank']*100 + (40 if p['specialty'] else 0)


def available(s, minutes):
    import job_apps as jobs
    key, p = current(s)
    d = jobs.ensure(s)
    if d['pending']:
        raise ValueError('Finish or withdraw the current assignment first.')
    spec = jobs.JOBS[key]
    jobs.guard(s, spec['venue'], minutes)
    now = s['world']['minute']
    if not spec['hours'][0]*60 <= now % 1440 <= spec['hours'][1]*60-minutes:
        raise ValueError('The whole activity must fit within workplace hours.')
    return d, key, p, now


def save_job(s, key):
    import job_apps as jobs
    if key not in jobs.JOBS:
        raise ValueError('Choose an advertised career.')
    saved = jobs.ensure(s)['saved_jobs']
    if key in saved:
        saved.remove(key)
        return 'Removed from saved jobs.'
    saved.append(key)
    return 'Job saved. Open Development to compare retained career progress.'


def train(s, course):
    import job_apps as jobs
    if course not in COURSES:
        raise ValueError('Choose an advertised course.')
    d, key, p, now = available(s, 30)
    title, cost, skill, gain = COURSES[course]
    if course in p['certificates']:
        raise ValueError('This qualification is already complete for this career.')
    if d['training_day'] == now//1440:
        raise ValueError('One training session per day across all employers.')
    if s['world']['money'] < cost:
        raise ValueError(f'Training costs ${cost}.')
    s['world']['money'] -= cost
    d['training_day'] = now//1440
    p[skill] += gain
    p['courses'][course] = p['courses'].get(course, 0)+1
    text = f'Jobseek: {title}, session {p["courses"][course]}/3; {skill} +{gain}; paid ${cost}.'
    if p['courses'][course] == 3:
        p['certificates'].append(course)
        text += ' Qualification earned.'
    s['turn'] += 1
    jobs.careers.spend_time(s, 30, 4)
    return jobs.log(s, text)


def network(s, kind):
    import job_apps as jobs
    if kind not in ('mentor', 'team'):
        raise ValueError('Choose mentoring or team support.')
    d, key, p, now = available(s, 20)
    if d['networking_day'] == now//1440:
        raise ValueError('One workplace relationship session per day across employers.')
    if p[kind] >= 100:
        raise ValueError('This workplace relationship is already at its maximum.')
    d['networking_day'] = now//1440
    p[kind] = min(100, p[kind]+10)
    skill = 'craft' if kind == 'mentor' else 'service'
    p[skill] += 2
    s['turn'] += 1
    jobs.careers.spend_time(s, 20, 2)
    return jobs.log(s, f'Jobseek: {kind} session; relationship {p[kind]}/100, {skill} +2.')


def specialise(s, choice):
    import job_apps as jobs
    _, key, p, _ = available(s, 0)
    if choice not in ('expert', 'coordinator'):
        raise ValueError('Choose a listed specialisation.')
    if jobs.ensure(s)['pending']:
        raise ValueError('Finish the current assignment first.')
    if p['specialty']:
        raise ValueError('Your specialisation is already chosen for this career.')
    certificate = 'craft' if choice == 'expert' else 'service'
    if p['rank'] < 2 or certificate not in p['certificates'] or p['mentor'] < 20:
        raise ValueError('Specialisation requires rank 3, mentor 20 and the matching qualification.')
    p['specialty'] = choice
    return jobs.log(s, 'Jobseek specialisation: '+WORKPLACES[key][1 if choice=='expert' else 2]+'. Shift pay +$40; matching shift skill gain +2.')


def project(s):
    import job_apps as jobs
    d, key, p, now = available(s, 0)
    if p['project']:
        raise ValueError('Deliver or close the current project first.')
    if p['rank'] < 1 or p['mentor'] < 20:
        raise ValueError('Projects require rank 2 and mentor relationship 20.')
    p['project'] = dict(title=WORKPLACES[key][0], deadline=now+7*1440,
                        stages=0, quality=0, choices=[])
    return jobs.log(s, 'Jobseek project accepted: '+p['project']['title']+'. Complete three shifts, then deliver at work within seven days.')


def deliver(s, abandon=False):
    import job_apps as jobs
    key, p = current(s)
    if jobs.ensure(s)['pending']:
        raise ValueError('Finish the current assignment first.')
    item = p['project']
    if not item:
        raise ValueError('There is no active career project.')
    now = s['world']['minute']
    if abandon or now > item['deadline']:
        p['project'] = None
        p['standing'] = max(0, p['standing']-3)
        return jobs.log(s, 'Jobseek project closed without payment; professional standing −3.')
    available(s, 20)
    if now+20 > item['deadline']:
        raise ValueError('The full 20-minute delivery must fit before the project deadline.')
    if item['stages'] < 3:
        raise ValueError('Complete three project shifts before delivery.')
    reward = 300 + item['quality']*30 + p['rank']*100
    p['portfolio'].append(dict(item, delivered=now, reward=reward))
    p['project'] = None
    p['standing'] = min(100, p['standing']+8)
    p['budget'] += 200
    p['earnings'] += reward
    s['world']['money'] += reward
    s['turn'] += 1
    jobs.careers.spend_time(s, 20, 3)
    return jobs.log(s, f'Jobseek project delivered; earned ${reward}, standing +8, department budget +$200.')


def shift_brief(key, p):
    return WORKPLACES[key][4+p['shifts']%3]


def complete_shift(s, key, p, choice):
    """Called only after the normal shift guards; no separate clock or payout."""
    p['service'] += (0, 3, 1)[choice]
    p['leadership'] += (1, 2, 1)[choice]
    p['team'] = min(100, p['team']+(1, 3, 2)[choice])
    p['standing'] = min(100, p['standing']+1)
    p['morale'] = min(100, p['morale']+(0, 2, 1)[choice])
    if p['specialty'] == 'expert' and choice == 0:
        p['craft'] += 2
    elif p['specialty'] == 'coordinator' and choice == 1:
        p['service'] += 2
    item = p['project']
    if item and s['job_apps']['pending']['deadline'] <= item['deadline'] and item['stages'] < 3:
        item['stages'] += 1
        item['quality'] += ((3, 2, 1)[choice] + (1 if p['specialty'] else 0)
                            + (1 if p['service'] >= 12 and p['team'] >= 30 else 0))
        item['choices'].append(choice)
        return f' Project stage {item["stages"]}/3; quality {item["quality"]}.'
    return ''


def review(s):
    import job_apps as jobs
    _, key, p, _ = available(s, 0)
    if jobs.ensure(s)['pending']:
        raise ValueError('Finish the current assignment before a promotion review.')
    if p['rank'] < 3:
        raise ValueError('Complete the local promotion ladder before a senior review.')
    if p['rank'] >= 7:
        raise ValueError('Career fellowship is the top of this ladder.')
    shifts, craft, reliability, certs, projects, standing = REVIEWS[p['rank']-3]
    leadership = (p['rank']-2)*12
    if p['leadership'] < leadership or p['morale'] < 50:
        raise ValueError(f'Senior review requires leadership {leadership} and team morale 50.')
    if (p['shifts'] + p.get('origin_experience', 0) < shifts or p['craft'] < craft or p['reliability'] < reliability
            or len(p['certificates']) < certs or len(p['portfolio']) < projects
            or p['standing'] < standing or not p['specialty']):
        raise ValueError(f'Review requires {shifts} shifts, craft {craft}, reliability {reliability}, '
                         f'{certs} qualifications, {projects} projects, standing {standing} and a specialisation.')
    p['rank'] += 1
    s['world']['job'] = titles(key)[p['rank']]
    return jobs.log(s, 'Jobseek promotion: '+titles(key)[p['rank']]+'. Shift pay +$100.')


def manage(s, choice):
    import job_apps as jobs
    if choice not in ('quality', 'team', 'outreach'):
        raise ValueError('Choose an available department initiative.')
    d, key, p, now = available(s, 30)
    if p['rank'] < 3 or not (p['portfolio'] or p.get('origin_portfolio')):
        raise ValueError('The management desk requires rank 4 and a delivered project.')
    if p['management_day'] == now//1440:
        raise ValueError('One department initiative per workplace per day.')
    if p['budget'] < 100:
        raise ValueError('An initiative needs $100 department budget; deliver projects to replenish it.')
    p['budget'] -= 100
    p['management_day'] = now//1440
    p['initiatives'] += 1
    p['leadership'] += 3
    if choice == 'quality': p['craft'] += 4
    elif choice == 'team':
        p['morale'] = min(100, p['morale']+10)
        p['reliability'] = min(100, p['reliability']+3)
    else: p['standing'] = min(100, p['standing']+4)
    s['turn'] += 1
    jobs.careers.spend_time(s, 30, 5)
    return jobs.log(s, f'Jobseek department initiative: {choice}; budget −$100, leadership +3.')
