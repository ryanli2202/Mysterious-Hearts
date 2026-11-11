"""Authored faction work, scoped credentials and enterable city interiors."""
import copy
import crime_sites as sites

BRANCHES = dict(site_01='Regional command', site_02='Logistics', site_03='Research',
                site_04='Clubs', site_05='Hearts', site_06='Diamonds', site_07='Corporate', site_08='Spades')
ROOMS = {key+'_'+area: (key, area) for key in sites.SITES for area in ('reception', 'briefing')}
CASES = {
    'site_01': ('A regional order demands a contractor surrender personal records.', 'Protect the contractor’s records'),
    'site_02': ('Shinokami logistics wants Syndicate-assisted expansion supplies approved despite a disputed territorial boundary.', 'Hold the consignment for review'),
    'site_03': ('A research contractor cannot produce the consent paperwork.', 'Suspend the disputed referral'),
    'site_04': ('Clubs proposes intimidating Red Dragons volunteers challenging Blue Magic distribution in their neighbourhood.', 'Reject intimidation and mediate'),
    'site_05': ('Hearts asks for a campaign discrediting civilian complaints about Blue Magic while presenting Shinokami cooperation as stability.', 'Preserve the complaint and correct the brief'),
    'site_06': ('Diamonds wants a Sylvanis supply payment approved despite conflicting Blue Magic and Red Magic harm reports.', 'Freeze the disputed payment'),
    'site_07': ('A corporate manager asks for broader access to customer records.', 'Keep access limited to the agreed purpose'),
    'site_08': ('Spades requests civilian addresses near a contested Shinokami expansion corridor without an authorised purpose.', 'Withhold the address and challenge the request'),
}
HIERARCHY = {
    'Syndicate': ('The Crow / Cardmaster sets strategic authority. Sylvanis is second-in-command and the Coloured Joker. '
        'Ivan is the Black and White Joker, with cross-Suit authority and five generals including Valentina, Queen of Wind. '
        'Clubs, Hearts, Diamonds and Spades have their own branch leadership and local supervisors. '
        'The Four Aces are hidden mission specialists directly assigned by the Crow, not Suit commanders. '
        'An Ace mandate can override a local task but does not give a visitor permanent rank.'),
    'Shinokami': ('Takeo Mishima is supreme commander. Number Thirteen commands US operations; Keisuke Hachimura handles recruits beneath US command. Local operations pass through regional command, '
        'then logistics, research and enforcement supervisors, then operatives and contractors. '
        'Neo is an escaped former subject, not a current member or an authorised heir. '
        'Contractor clearance is site-specific and never grants access to Mishima’s command or protected research.'),
}


def site_of(location):
    return ROOMS.get(location, (location, None))[0]


def read(s, who=None):
    return s.get('crime_operations', {}).get('people', {}).get(who or s['player'], {})


def data(s):
    return s.setdefault('crime_operations', {'version': 1, 'people': {}}).setdefault('people', {}).setdefault(
        s['player'], {'sites': {}, 'permits': {}, 'history': [], 'active': None})


def progress(s, key):
    return read(s).get('sites', {}).get(key, {'days': [], 'standing': 0, 'pressure': 0, 'harm': 0, 'evidence': 0, 'last_work': -1})


def authority(who, key):
    if sites.SITES[key]['faction'] == 'Shinokami': return who == 'thirteen'
    if sites.SITES[key]['faction'] != 'Syndicate': return False
    return who in ('ivan', 'sylvanis') or who == 'valentina' and key == 'site_04'


def permitted(s, who, key):
    if who==s['player'] and __import__('organisation_guards').breach(s,key): return True
    if who==s['player'] and sites.SITES[key]['faction'].lower() in s.get('combat',{}).get('expelled',[]): return False
    import thirteen
    if key=='site_02' and (who=='thirteen' or who==s['player'] and thirteen.number_allowed(s)): return True
    import four_aces
    import takeo
    if key == 'site_01' and (who == 'takeo' or who == s['player'] and takeo.number_allowed(s)): return True
    if who in four_aces.IDS and sites.SITES[key]['faction'] == 'Syndicate': return True
    if authority(who,key): return True
    if read(s,who).get('sites',{}).get(key,{}).get('pressure',0)>=15: return False
    permit=read(s,who).get('permits',{}).get(key,{})
    return permit.get('until',-1)>s['world']['minute']


def access_text(s,key):
    import thirteen
    if key=='site_02' and thirteen.number_allowed(s): return 'Executive clearance: report to Number Thirteen, commander of US operations, in the briefing room.'
    import takeo
    if key == 'site_01' and takeo.number_allowed(s): return 'Regional command clearance: Takeo receives reports in the headquarters briefing room.'
    if authority(s['player'],key): return 'Command authority · '+BRANCHES[key]
    import four_aces
    if s['player'] in four_aces.IDS and sites.SITES[key]['faction'] == 'Syndicate':
        return 'Ace operational clearance · all Syndicate affiliate interiors · no Suit command authority'
    if progress(s,key)['pressure']>=15: return 'Clearance suspended by the local supervisor · reduce pressure through responsible reception work.'
    permit=read(s).get('permits',{}).get(key,{})
    if permitted(s,s['player'],key):
        return 'Escorted briefing clearance · '+str(permit['until']-s['world']['minute'])+' story minutes remaining'
    if key=='site_07' and s['player'] not in sites.INSIDERS:
        return 'Briefing clearance locked · Oculus does not grant operational access through public visitor work.'
    return 'Briefing room locked · complete reception work on two separate days, then request a 24-hour pass. Command records require faction authority.'


def can_enter(s,who,destination):
    import organisation_guards as security
    key,area=ROOMS.get(destination,(None,None))
    actor=s['world']['cast'].get(who,{})
    if key and who==s['player'] and site_of(actor.get('location'))==key and not actor.get('journey') and security.slots(s,key) and not security.remaining(s,key): return True
    if destination not in ROOMS: return True
    key,area=ROOMS[destination]
    actor=s['world']['cast'].get(who,{})
    if actor.get('journey') or site_of(actor.get('location')) != key: return False
    if area=='reception': return True
    return permitted(s,who,key) and actor.get('location') in (key+'_reception',destination)


def check_trip(s,who,destination,passengers=()):
    if destination in ROOMS and any(not can_enter(s,p,destination) for p in (who,*passengers)):
        raise ValueError('Enter from this site’s reception. Every person needs their own valid briefing clearance; membership is not transferable.')


def enter(s,key,area):
    if key not in sites.SITES or area not in ('reception','briefing'): raise ValueError('Choose an available room.')
    import town
    town.travel(s,key+'_'+area)
    if not sites.records(s).get(key,{}).get('inspected'):
        sites._entry(s,key).update(inspected=True,observation=sites.SITES[key]['exterior'],minute=s['world']['minute'])
    return 'Entered '+('public reception' if area=='reception' else 'the controlled briefing room')+'.'


def exit_site(s,key):
    import town
    if site_of(s['world']['location']) != key: raise ValueError('You are not at this site.')
    town.travel(s,key)
    return 'Returned to the public frontage.'


def guard(s,key,area):
    actor=s['world']['cast'][s['player']]
    if actor.get('journey') or actor['location']!=key+'_'+area or s['world']['location']!=actor['location']:
        raise ValueError('Visit this site’s '+area+' first.')
    if area=='briefing' and not permitted(s,s['player'],key): raise ValueError('Your briefing clearance has expired. Return to reception.')


def log(s,key,text):
    item=dict(site=key,minute=s['world']['minute'],text=text)
    data(s)['history'].append(item)
    return text


def request_pass(s,key):
    guard(s,key,'reception')
    if progress(s,key)['pressure']>=15: raise ValueError('The local supervisor has suspended clearance. Resolve reception work responsibly to reduce pressure.')
    if permitted(s,s['player'],key): raise ValueError('You already have access.')
    if key=='site_07' and s['player'] not in sites.INSIDERS:
        raise ValueError('Oculus grants no operational clearance through public visitor work.')
    if len(progress(s,key)['days'])<2: raise ValueError('Build a reception work record on two separate story days first.')
    data(s)['permits'][key]=dict(until=s['world']['minute']+1440,issuer='Local '+BRANCHES[key]+' supervisor',scope='Escorted briefing only')
    return log(s,key,'The local supervisor issued a personal, site-specific 24-hour escorted briefing pass. No command access or membership was granted.')


def begin(s,key,kind,colleague=None):
    if key not in sites.SITES or kind not in ('reception','briefing','command'): raise ValueError('Choose an available assignment.')
    if read(s).get('active'): raise ValueError('Finish or abandon the active assignment first.')
    guard(s,key,'reception' if kind=='reception' else 'briefing')
    if kind=='command' and not authority(s['player'],key): raise ValueError('Only a commander with authority in this branch may issue this decision.')
    if progress(s,key)['last_work']==s['world']['minute']//1440: raise ValueError('One assignment per site per story day.')
    if colleague:
        import faction_work, four_aces
        faction_work.validate_colleague(s,key,colleague)
        if kind=='command' and colleague in four_aces.IDS and not faction_work.disclosure(s):
            raise ValueError('This mandate requires a private discussion with informed colleagues only.')
    if kind=='reception':
        question='A visitor packet has an unsigned declaration. The desk wants a quick approval.'
        options=('Document the missing declaration','Approve it without checking','Decline and return the incomplete packet')
        issuer='Visitor-services supervisor'
    else:
        question=CASES[key][0]
        options=(CASES[key][1], 'Approve the supervisor’s request', 'Escalate the disputed order')
        issuer=('Crow-authorised '+('Diamonds' if key=='site_07' else BRANCHES[key])+' Ace mission liaison' if kind=='command' else
                BRANCHES[key]+' supervisor')
        if sites.SITES[key]['faction']=='Shinokami': issuer='Regional command through the '+BRANCHES[key]+' supervisor'
    data(s)['active']=dict(site=key,kind=kind,issuer=issuer,question=question,options=options,started=s['world']['minute'])
    if colleague:
        import game_core as core
        data(s)['active'].update(colleague=colleague, colleague_label=core.contact_name(s,colleague))
    return 'Assignment opened. Issuer: '+issuer+'.'


def resolve(s,choice):
    active=read(s).get('active')
    if not active or choice not in (0,1,2): raise ValueError('Choose a response to the active assignment.')
    key=active['site'];kind=active['kind']
    guard(s,key,'reception' if kind=='reception' else 'briefing')
    if kind=='command' and not authority(s['player'],key): raise ValueError('This decision requires branch command authority.')
    colleague=active.get('colleague')
    if colleague:
        import faction_work, four_aces
        faction_work.validate_colleague(s,key,colleague)
        if kind=='command' and colleague in four_aces.IDS and not faction_work.disclosure(s):
            raise ValueError('An uninformed listener is present. Defer the private mandate discussion.')
    day=s['world']['minute']//1440
    if progress(s,key)['last_work']==day: raise ValueError('This site already recorded an assignment today.')
    p=data(s)['sites'].setdefault(key,copy.deepcopy(progress(s,key)))
    p['last_work']=day
    if kind=='reception' and choice!=1 and day not in p['days']: p['days'].append(day)
    p['standing']=max(-100,min(100,p['standing']+(4 if choice==1 else 2 if choice==0 else -1)))
    delta=5 if choice==2 else (-3 if kind=='reception' else 2) if choice==0 else -3
    p['pressure']=max(0,min(100,p['pressure']+delta))
    p['harm']=max(0,p['harm']+(2 if choice==1 else -1 if choice==0 else 0))
    if choice==1 and kind!='reception':
        import interpol
        interpol.record_offence(s,'coercion',documented=True)
    p['evidence']+=int(choice==0)
    pay=0 if choice==2 else (80 if kind=='reception' else 160 if kind=='briefing' else 240)
    s['world']['money']+=pay
    # One bounded authored decision, no invented arrests, victims, rescues or secret disclosures.
    outcome=('The disputed request is held and the concern retained.' if choice==0 else
             'The request is approved; local standing rises, with greater unresolved harm.' if choice==1 else
             'The objection is sent up the chain; pressure rises while a response remains pending.')
    if kind=='command' and choice==2: outcome='The objection to the Ace mandate is sent to the Crow’s office. A response remains pending; the mandate is still in force.'
    text=active['issuer']+': '+active['question']+' Decision: '+active['options'][choice]+'. '+outcome+f' Pay ${pay}. Standing {p["standing"]}; pressure {p["pressure"]}; unresolved harm {p["harm"]}; evidence {p["evidence"]}.'
    data(s)['active']=None
    if colleague: text='Joint review with '+active['colleague_label']+'. '+text
    result=log(s,key,text)
    if colleague:
        person=s['crime_operations']['people'].setdefault(colleague,dict(sites={},permits={},history=[],active=None))
        person['history'].append(dict(site=key,minute=s['world']['minute'],text='Participated in a joint review. Decision: '+active['options'][choice]+'. '+outcome))
    reconcile(s)
    return result


def abandon(s):
    active=read(s).get('active')
    if not active: raise ValueError('No active assignment.')
    data(s)['active']=None
    return log(s,active['site'],'Assignment abandoned without pay or progress.')


def reconcile(s):
    """Expired/revoked access returns occupants to reception, even after loading."""
    world=s.get('world',{})
    for who,actor in world.get('cast',{}).items():
        location=actor.get('location')
        if location in ROOMS and ROOMS[location][1]=='briefing':
            key=ROOMS[location][0]
            if not permitted(s,who,key) and not (who==s['player'] and __import__('organisation_guards').slots(s,key) and not __import__('organisation_guards').remaining(s,key)):
                actor.update(location=key+'_reception',journey=None,activity='Clearance expired · reception')
                if who==s['player']: world['location']=actor['location']


def hierarchy(s,key):
    if not sites.affiliation_known(s,key): return 'Local supervisor → visitor services → approved contractors. The operator’s wider affiliations are not established for you.'
    import criminal_dynamics
    faction = sites.SITES[key]['faction']
    return HIERARCHY[faction] + ' ' + criminal_dynamics.DOCTRINES[faction.lower()]


def context(s,who):
    # Only the speaker's own record; no transfer of player orders into an NPC prompt.
    return dict(recent=copy.deepcopy(read(s,who).get('history',[])[-3:]),
                guidance='Room clearance, membership and orders come only from recorded game actions. Never grant access or promotions through prose. Ace authority is mission-based, not Suit leadership.')
