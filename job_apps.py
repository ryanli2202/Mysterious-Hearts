"""Local careers and anonymous criminal contracts; authored, saved game rules."""
import careers
import bubblegram_progression as progression
import jobseek_progression as civilian


def job(title, venue, ranks, pay, brief, hours=(8, 20)):
    return dict(title=title, venue=venue, ranks=ranks, pay=pay, brief=brief, hours=hours)


JOBS = {
    'photographer': job('Studio photographer', 'studio', ('Assistant photographer', 'Photographer', 'Senior photographer', 'Photography director'), 240, 'The client needs a difficult portrait before the studio closes.'),
    'model': job('Studio model', 'studio', ('Junior model', 'Booked model', 'Campaign model', 'Lead model'), 260, 'A revised campaign brief calls for a new interpretation.'),
    'librarian': job('Librarian', 'library', ('Library assistant', 'Librarian', 'Senior librarian', 'Library manager'), 200, 'A busy reading-room event clashes with a catalogue deadline.'),
    'oculus': job('Oculus receptionist', 'site_07_reception', ('Reception assistant', 'Receptionist', 'Senior receptionist', 'Front desk manager'), 230, 'A visitor wants an appointment without the required confirmation.'),
    'cinema': job('Cinema attendant', 'cinema', ('Cinema attendant', 'Projection assistant', 'Shift supervisor', 'Cinema manager'), 190, 'A screening delay leaves a queue of impatient customers.'),
    'barista': job('Café team', 'cafe', ('Café assistant', 'Barista', 'Shift lead', 'Café manager'), 180, 'The lunchtime queue grows while a new colleague learns the menu.'),
    'florist': job('Florist', 'flowers', ('Flower assistant', 'Florist', 'Senior florist', 'Shop manager'), 200, 'A large arrangement needs reworking before collection.'),
    'chef': job('Golden Dragon kitchen', 'noodle_shop', ('Kitchen assistant', 'Line cook', 'Sous chef', 'Head chef'), 220, 'An evening booking needs a menu adjustment.'),
    'retail': job('Galleria retail', 'shopping_mall', ('Sales assistant', 'Sales specialist', 'Team lead', 'Store manager'), 190, 'A customer needs help while a delivery waits to be checked.'),
    'arcade': job('Pixel Pier team', 'arcade', ('Arcade attendant', 'Cabinet technician', 'Floor supervisor', 'Arcade manager'), 200, 'A popular cabinet stops working during a tournament.'),
    'gardener': job('Community gardens', 'public_park', ('Grounds assistant', 'Gardener', 'Senior gardener', 'Grounds supervisor'), 180, 'An event needs a clear path while a planting project is unfinished.'),
    'bartender': job('Copper Lantern team', 'bar', ('Bar assistant', 'Bartender', 'Shift supervisor', 'Bar manager'), 220, 'An unusually busy evening puts pressure on the service team.', (17, 24)),
}
# Promotions require an explicit review, experience, craft and reliability.
LADDER = ((0, 0, 0), (3, 6, 55), (8, 16, 65), (15, 30, 75))
BRANCHES = {
    'Clubs': ('Syndicate', 'site_04', ('Probationary associate', 'Clubs operative', 'Clubs specialist', 'Clubs team leader', 'Clubs lieutenant')),
    'Hearts': ('Syndicate', 'site_05', ('Probationary associate', 'Hearts operative', 'Hearts coordinator', 'Hearts producer', 'Hearts lieutenant')),
    'Diamonds': ('Syndicate', 'site_06', ('Probationary associate', 'Diamonds clerk', 'Diamonds analyst', 'Diamonds controller', 'Diamonds lieutenant')),
    'Spades': ('Syndicate', 'site_08', ('Probationary associate', 'Spades operative', 'Spades specialist', 'Spades handler', 'Spades lieutenant')),
    'Shinokami': ('Shinokami', 'site_02', ('見習い · Minarai · Apprentice', '構成員 · Kōseiin · Member', '班長 · Hanchō · Squad leader', '隊長 · Taichō · Unit captain', '幹部 · Kanbu · Executive')),
}
SHINOKAMI_COMMAND = '最高司令官 · Saikō Shireikan · Supreme Commander — Takeo Mishima (reserved story role)'
for _branch, (_faction, _site, _ranks) in tuple(BRANCHES.items()):
    if _faction == 'Syndicate':
        BRANCHES[_branch] = (_faction, _site, (*_ranks, _branch+' executive', 'Jack of '+_branch))
BRANCHES['Shinokami'] = ('Shinokami','site_02',(*BRANCHES['Shinokami'][2],
    '上級幹部 · Jōkyū Kanbu · Senior executive',
    '地方司令官 · Chihō Shireikan · Regional commander',
    '総司令官 · Sōshireikan · General commander'))


def executive(s, who=None):
    """Read-only, save-local clearance; never upgrades the global cast roster."""
    if not s.get('player') or (who is not None and who != s['player']): return False
    m=s.get('job_apps', {}).get('membership') or {}
    return (m.get('faction')=='Syndicate' and m.get('branch') in ('Clubs','Hearts','Diamonds','Spades')
            and m.get('rank',0)>=5)


def executive_briefing(s):
    if not executive(s): raise ValueError('Syndicate executive clearance is required.')
    import four_aces
    return ('Executive induction: headquarters access authorised. The Four Aces are the Cardmaster’s '
            'direct mission specialists, not Suit commanders.\n'+
            '\n'.join(f'{p["name"]} — Ace of {p["suit"]}.' for p in four_aces.CAST.values())+
            '\nThese identities are confidential. Discuss them only with cleared insiders; no guest clearance is granted.')
CONTRACTS = {
    'parcel': dict(title='Unregistered parcel', alias='@nightparcel', venue='downtown', rep=0, pay=300, faction=None, brief='An anonymous broker offers cash for an unregistered delivery. The contents are undisclosed.'),
    'resale': dict(title='Off-book resale', alias='@greylist', venue='market', rep=10, pay=420, faction=None, brief='A reseller wants help moving a disputed lot. No legitimate ownership record is supplied.'),
    'crew': dict(title='Crew obligation', alias='@sidechannel', venue='downtown', rep=20, pay=500, faction=None, brief='A local crew requests help settling an internal dispute over missing proceeds.'),
    'syndicate': dict(title='Syndicate broker trial', alias='@suitrelay', venue='downtown', rep=30, pay=650, faction='Syndicate', brief='A masked intermediary offers a small off-book commission to assess your reliability.'),
    'shinokami': dict(title='Shinokami broker trial', alias='@moonrelay', venue='market', rep=30, pay=650, faction='Shinokami', brief='An anonymous intermediary offers a consignment review for a distant organisation.'),
}
CONTRACTS['network'] = dict(title='Inter-gang settlement',alias='@districtrelay',venue='downtown',rep=55,pay=950,faction=None,brief='Two crews dispute the proceeds of an off-book commission. Your crew must decide how to respond.',gang=True)
CONTRACTS['leadership'] = dict(title='Underworld leadership commission',alias='@councilrelay',venue='market',rep=75,pay=1400,faction=None,brief='A network broker requests a decision on competing criminal obligations. The decision affects your standing, without granting command of another organisation.',gang=True)
for _key,_cap in (('parcel',20),('resale',40),('crew',60),('syndicate',80),('shinokami',80)):
    CONTRACTS[_key]['rep_cap']=_cap


def ensure(s):
    d = s.setdefault('job_apps', {})
    for key, value in dict(version=1, employment=None, jobs={}, reputation=0, heat=0,
                           heat_day=s['world']['minute']//1440, last_shift=-1, last_contract=-1,
                           completed=0, connections={'Syndicate': 0, 'Shinokami': 0},
                           gang=None, membership=None, pending=None, history=[]).items():
        if key not in d:
            d[key] = value
    elapsed=max(0, s['world']['minute']//1440-d['heat_day'])
    d['heat']=max(0,d['heat']-elapsed*5)
    d['heat_day']=max(d['heat_day'],s['world']['minute']//1440)
    civilian.ensure(s)
    progression.sync(s,d)
    import keisuke
    keisuke.ensure(s)
    import thirteen
    thirteen.ensure(s)
    import gang_leaders
    gang_leaders.ensure(s)
    import gang_members
    gang_members.ensure(s)
    import custom_gangs
    custom_gangs.sync(s, d)
    return d


def log(s, text, private=False):
    import town
    d=ensure(s)
    d['history'].append(dict(minute=s['world']['minute'], text=text, private=private))
    town.log(s, 'Bubblegram private activity updated.' if private else text)
    return text


def profile(s, key):
    if key not in JOBS: raise ValueError('Choose an advertised career.')
    return civilian.upgrade(ensure(s)['jobs'].setdefault(key, dict(rank=0, shifts=0, craft=0, reliability=50)))


def apply(s, key):
    d=ensure(s)
    if d['pending']: raise ValueError('Finish or withdraw the current assignment first.')
    profile(s,key)
    if d['employment']==key: raise ValueError('You already hold this job.')
    d['employment']=key
    s['world']['job']=civilian.titles(key)[profile(s,key)['rank']]
    return log(s,'Jobseek: hired as '+s['world']['job']+'. Previous career progress is retained.')


def promote(s):
    d=ensure(s); key=d['employment']
    if not key: raise ValueError('Apply for a career first.')
    if d['pending']: raise ValueError('Finish or withdraw the current assignment before a promotion review.')
    civilian.available(s,0)
    p=profile(s,key)
    if p['rank']>=3: return civilian.review(s)
    shifts,craft,reliability=LADDER[p['rank']+1]
    if p['shifts']+p.get('origin_experience',0)<shifts or p['craft']<craft or p['reliability']<reliability:
        raise ValueError(f'Review requires {shifts} shifts, {craft} craft and {reliability} reliability.')
    p['rank']+=1
    s['world']['job']=civilian.titles(key)[p['rank']]
    return log(s,'Jobseek promotion: '+JOBS[key]['ranks'][p['rank']]+'.')


def guard(s, venue, duration=60, exclude=None):
    __import__('combat').guard(s)
    import autonomy
    w=s['world']; actor=w['cast'][s['player']]
    if actor.get('journey') or w['location']!=venue or actor['location']!=venue:
        raise ValueError('Travel to the assignment location and finish arriving first.')
    if (autonomy.person(s,s['player']).get('sleep_until') or 0)>w['minute']:
        raise ValueError('Wake up before working.')
    if s.get('careers',{}).get('active') or s.get('crime_operations',{}).get('people',{}).get(s['player'],{}).get('active'):
        raise ValueError('Finish your other work session first.')
    if careers.conflict(s,w['minute'],w['minute']+duration,exclude):
        raise ValueError('This assignment overlaps a calendar or career commitment.')


def begin_shift(s):
    d=ensure(s); key=d['employment']
    if not key: raise ValueError('Apply for a career first.')
    if d['pending']: raise ValueError('Finish or withdraw the current assignment first.')
    spec=JOBS[key]; now=s['world']['minute']
    guard(s,spec['venue'])
    if d['last_shift']==now//1440: raise ValueError('One Jobseek shift per day, including job changes.')
    if not spec['hours'][0]*60<=now%1440<=spec['hours'][1]*60-60:
        raise ValueError('The entire hour must fit within workplace hours.')
    d['pending']=dict(kind='shift', key=key, venue=spec['venue'], started=now, deadline=now+60,
                      brief=civilian.shift_brief(key,profile(s,key)))
    return 'Shift briefing ready. Choose craft, teamwork or a measured pace.'


def contract_spec(s, key):
    spec = CONTRACTS[key]
    import bubblegram_roles
    if s['player'] in bubblegram_roles.ROLES: return bubblegram_roles.contract(s, key, spec)
    if key == "crew":
        import gang_members
        return gang_members.contract(s, spec)
    return spec


def accept(s, key):
    d=ensure(s)
    if key not in CONTRACTS: raise ValueError('Choose an advertised contract.')
    if d['pending']: raise ValueError('Finish or withdraw the current assignment first.')
    spec=contract_spec(s,key)
    import bubblegram_roles
    if s['player'] in bubblegram_roles.ROLES and spec['faction']:
        raise ValueError('Your established Syndicate role does not use newcomer trials. Choose a mandate commission or the Leadership desk.')
    if d['reputation']<spec['rep']: raise ValueError('Build more criminal reputation to unlock this channel.')
    if (key=='crew' or spec.get('gang')) and not d['gang']: raise ValueError('Join or create a gang first.')
    if spec['faction'] and spec['faction'] not in d['invitations'] and not (d['membership'] and d['membership']['faction']==spec['faction']):
        raise ValueError('Earn an invitation first: reputation 40, eight contracts, gang standing 3 and heat below 30.')
    if d['membership'] and spec['faction'] and spec['faction']!=d['membership']['faction']:
        raise ValueError('Your sponsor will not accept work for a rival faction.')
    if d['last_contract']==s['world']['minute']//1440: raise ValueError('One Bubblegram contract per day.')
    if d['heat']>=60: raise ValueError('Heat is too high. It falls by 5 each story day; wait before accepting work.')
    now=s['world']['minute']
    d['pending']=dict(kind='contract',key=key,venue=spec['venue'],started=now,deadline=now+1440)
    if s['player'] in bubblegram_roles.ROLES: d['pending']['brief'] = spec['brief']
    if spec.get('coworkers'):
        d['pending'].update(coworkers=list(spec['coworkers']), brief=spec['brief'])
    return log(s,'Accepted '+spec['title']+'. Complete within 24 hours; reserve 60 minutes at the destination.',True)


def resolve(s, choice):
    d=ensure(s); a=d['pending']; now=s['world']['minute']
    if not a: raise ValueError('There is no current assignment.')
    if choice not in (0,1,2): raise ValueError('Choose an available approach.')
    duration=a['deadline']-now if a['kind']=='shift' else 60
    if duration<=0 or now+duration>a['deadline']: raise ValueError('The assignment expired. Withdraw it before accepting another.')
    guard(s,a['venue'],duration)
    if a['kind']=='shift':
        if d['last_shift']==now//1440: raise ValueError('You already worked today.')
        p=profile(s,a['key']); spec=JOBS[a['key']]
        p['shifts']+=1; p['craft']+=(4,2,1)[choice]; p['reliability']=min(100,p['reliability']+(1,4,2)[choice])
        pay=civilian.wage(a['key'],p); d['last_shift']=now//1440
        p['earnings']+=pay
        s['world']['job']=civilian.titles(a['key'])[p['rank']]
        text=f'{spec["title"]}: completed a shift; earned ${pay}. Craft +{(4,2,1)[choice]}, reliability +{(1,4,2)[choice]}.'
        text+=civilian.complete_shift(s,a['key'],p,choice)
    else:
        if d['last_contract']==now//1440: raise ValueError('You already completed a contract today.')
        spec=contract_spec(s,a['key']) if a['kind']=='contract' else None
        # Reckless choices create deterministic setbacks, with the risk visible in UI.
        success=choice!=2 or d['heat']<25
        if choice==2:
            import interpol
            interpol.record_offence(s,'reckless_commission',documented=True)
        import interpol
        faction=(spec or {}).get('faction') or (d.get('membership') or {}).get('faction') or (d.get('gang') or {}).get('id','')
        disrupted=interpol.read(s).get('disruption',{}).get(faction.lower(),0)>now
        pay=(spec['pay'] if spec else 800)*(1 if choice!=0 else .75) if success else 0
        if disrupted: pay*=.5
        d['last_contract']=now//1440
        d['heat']=min(100,d['heat']+(2,8,20)[choice])
        gain=min((4,6,8)[choice],max(0,(spec or {}).get('rep_cap',100)-d['reputation'])) if success else -5
        d['reputation']=max(0,min(100,d['reputation']+gain))
        if success:
            d['completed']+=1
            if d['gang']: d['gang']['standing']+=1
            if spec and spec['faction']: d['connections'][spec['faction']]+=1
            if a['kind']=='faction': d['membership']['assignments']+=1
        elif a['kind']=='faction':
            d['membership']['strikes']+=1
        text=('Completed ' if success else 'Failed ')+(spec['title'] if spec else 'sponsor assignment')+f'; earned ${int(pay)}. Reputation {d["reputation"]}; heat {d["heat"]}.'
    if a['kind']!='shift' and disrupted: text+=' Interpol disruption reduced this commission by half.'
    if a['kind'] == 'contract':
        import custom_gangs
        bonus = custom_gangs.operation(s, a['key'], success)
        pay += bonus
        if bonus: text += f' Officer support bonus ${bonus}.'
        if a['key'] in ('crew','network','leadership') and (d['gang'] or {}).get('members'):
            text += f' After crew support: heat {d["heat"]}; gang standing {d["gang"]["standing"]}.'
    if a.get('coworkers'):
        text += ' Worked alongside ' + ' and '.join(a['coworkers']) + '.'
    d['pending']=None
    s['world']['money']+=int(pay); s['turn']+=1
    careers.spend_time(s,duration,(8,12,18)[choice])
    return log(s,text,a['kind']!='shift')


def withdraw(s):
    d=ensure(s); a=d['pending']
    if not a: raise ValueError('There is no current assignment.')
    if a['kind']=='shift':
        p=profile(s,a['key']); p['reliability']=max(0,p['reliability']-3)
    else: d['reputation']=max(0,d['reputation']-2)
    d['pending']=None
    return log(s,'Assignment withdrawn; no pay. '+('Reliability −3.' if a['kind']=='shift' else 'Criminal reputation −2.'),a['kind']!='shift')


def gang(s, name=None):
    if name is None: return progression.join(s,'lantern')
    d=ensure(s)
    if d['gang']: raise ValueError('You already belong to a gang.')
    if d['pending'] or d['membership']: raise ValueError('Finish your assignment; sponsored members cannot found a new gang.')
    if d['reputation']<20 or d['completed']<4: raise ValueError('Gangs require 20 reputation and 4 completed contracts.')
    if name is not None and not 3<=len(name.strip())<=32: raise ValueError('Use a gang name between 3 and 32 characters.')
    if name.strip().casefold() in {g['name'].casefold() for g in progression.GANGS.values()} | {'red dragons','syndicate','shinokami'}:
        raise ValueError('Choose an original crew name; founding cannot claim an existing organisation.')
    d['gang']=dict(name=name.strip(), role='Founder', standing=0,rank=0)
    return log(s,'Gang established: '+d['gang']['name']+' · '+d['gang']['role']+'. Crew obligations build standing.',True)


def sponsor(s, branch):
    import hidden_cast
    d=ensure(s)
    if s['player'] in hidden_cast.SYNDICATE_MEMBERS:
        raise ValueError('Your established Syndicate role is retained; the newcomer ladder does not replace it.')
    if branch not in BRANCHES: raise ValueError('Choose an available branch.')
    if d['membership']: raise ValueError('You already have a sponsor. Branch and faction commitments are exclusive.')
    import crime_diplomacy
    if crime_diplomacy.has_obligations(s): raise ValueError('Resolve your leadership meetings and deals before changing faction authority.')
    faction,site,ranks=BRANCHES[branch]
    if faction.lower() in s.get('combat',{}).get('expelled',[]): raise ValueError('You were excommunicated from this organisation.')
    if faction not in d['invitations']: raise ValueError('Build reputation and receive a faction invitation before seeking sponsorship.')
    if d['reputation']<50 or d['connections'][faction]<3 or not d['gang'] or d['gang']['standing']<3:
        raise ValueError('Sponsorship requires 50 reputation, 3 trials for this faction and gang standing 3.')
    if d['heat']>=30: raise ValueError('Reduce heat below 30 before sponsorship.')
    d['membership']=dict(faction=faction, branch=branch, sponsor='@'+branch.lower()+'-liaison', rank=0, assignments=0, strikes=0)
    d['invitations'][faction]['status']='accepted'
    if faction == 'Shinokami':
        import keisuke
        keisuke.ensure(s)
        import thirteen
        thirteen.ensure(s)
        return log(s,'Shinokami sponsorship accepted. Keisuke Hachimura is your main liaison; his number and introduction are in Messages. Meet him at Pacific Relay Depot reception. Probation begins; three successful sponsor assignments and a review are required. No headquarters or command clearance granted.',True)
    return log(s,'Sponsorship accepted: '+branch+'. Probation begins; three successful sponsor assignments and a review are required. No headquarters or command clearance granted.',True)


def faction_assignment(s):
    d=ensure(s); m=d['membership']
    if not m: raise ValueError('Earn sponsorship first.')
    if m['strikes']>=2: raise ValueError('Sponsorship suspended. Request rehabilitation before more assignments.')
    if d['pending']: raise ValueError('Finish or withdraw the current assignment first.')
    if d['heat']>=60: raise ValueError('Reduce heat below 60 before another assignment.')
    if d['last_contract']==s['world']['minute']//1440: raise ValueError('One Bubblegram contract per day.')
    now=s['world']['minute']
    # Public reception only. No permits, hidden cast discovery or HQ invitations.
    d['pending']=dict(kind='faction', key=m['branch'], venue=BRANCHES[m['branch']][1]+'_reception', started=now, deadline=now+1440)
    if m['faction'] == 'Shinokami':
        import keisuke
        d['pending']['liaison'] = keisuke.NAME
        return log(s,'Keisuke Hachimura: report to Pacific Relay Depot reception within 24 hours for your sponsor assignment. Use the assignment controls to resolve the disputed commission.',True)
    return log(s,'Sponsor briefing: report to the designated reception within 24 hours. Handle a disputed commission under local supervision.',True)


def review(s):
    d=ensure(s); m=d['membership']
    if not m: raise ValueError('Earn sponsorship first.')
    if m['strikes']>=2:
        if d['heat']>=20 or d['reputation']<50: raise ValueError('Rehabilitation requires heat below 20 and reputation 50.')
        m['strikes']=0
        return log(s,'Sponsor restored after rehabilitation. Rank retained; promotion requires a separate review.',True)
    if m['rank']>=len(BRANCHES[m['branch']][2])-1: raise ValueError('You reached the playable rank ceiling. Story leadership remains reserved.')
    target=m['rank']+1; count,rep=progression.REVIEWS[target]
    if m['assignments']+m.get('origin_experience',0)<count or d['reputation']<rep or d['heat']>=30:
        raise ValueError(f'Review requires {count} successful sponsor assignments, reputation {rep} and heat below 30.')
    m['rank']=target
    if m['faction']=='Shinokami' and target>=4:
        return log(s,'Sponsor review passed: '+BRANCHES[m['branch']][2][target]+'. Number Thirteen, commander of US operations, is your second Shinokami contact. Pacific Relay Depot briefing access authorised; Takeo clearance remains separate.',True)
    if executive(s):
        return log(s,'Sponsor review passed: '+BRANCHES[m['branch']][2][target]+'. '+executive_briefing(s),True)
    return log(s,'Sponsor review passed: '+BRANCHES[m['branch']][2][target]+'. Clearance remains limited to public reception.',True)


def travel(s, venue):
    import town
    import crime_operations
    if venue in crime_operations.ROOMS:
        site,area=crime_operations.ROOMS[venue]
        if crime_operations.site_of(s['world']['location'])!=site:
            return town.travel(s,site)
        if area=='briefing' and s['world']['location']==site:
            return crime_operations.enter(s,site,'reception')
        return crime_operations.enter(s,site,area)
    return town.travel(s,venue)
