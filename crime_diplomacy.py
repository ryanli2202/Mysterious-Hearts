"""Scheduled, physical leadership meetings and saved organisation deals."""
import uuid
import job_apps as jobs
import careers
import gang_leaders

# The tuple layout remains compatible with existing leadership UI and saves.
ORGANISATIONS = {
    'dragons': ('Red Dragons','downtown','Red Dragons commercial executive','Red Dragons council leader','Civilian grievances, community restitution and refusal of narcotics revenue'),
    'joker': ('Black and White Joker network','downtown','Joker network executive','Joker network senior general','Cross-branch obligations'),
    'lantern': ('Lantern Crew','market','Lantern broker','Lantern crew chief','Off-book street-market commission'),
    'rail': ('Rail Yard Saints','market','Rail Yard negotiator','Rail Yard crew chief','Disputed warehouse commission'),
    'purple': ('Purple Skulls','downtown','Purple Skulls road captain','Purple Skulls chapter president','Club-to-club proceeds agreement'),
    'hamayashi': ('Hamayashi-kai','market','Successor clan executive','Successor clan regional boss','Successor clan brokerage agreement'),
    'rojos': ('Los Rojos','market','Los Rojos commercial executive','Los Rojos regional leader','Off-book consignment proceeds'),
    'waterfront': ('Waterfront Consortium','downtown','Consortium executive','Consortium chair','Waterfront brokerage agreement'),
    'syndicate': ('Syndicate','downtown','Syndicate branch executive','Syndicate regional director','Affiliate commission agreement'),
    'shinokami': ('Shinokami','market','Shinokami executive','Shinokami regional commander','Regional contractor agreement'),
}
TERMS = {'measured': dict(stake=1500,revenue=2700,heat=3,risk=None),
         'aggressive': dict(stake=4000,revenue=7200,heat=12,risk=40)}

ATTENDEES = {'dragons':'garrett', 'joker':'ivan', 'syndicate':'crow', 'shinokami':'takeo',
             **{k:p['name'] for k,p in gang_leaders.LEADERS.items()}}
VENUES = {'dragons':'syndicate', 'joker':'syndicate_office', 'syndicate':'syndicate_hq',
          'shinokami':'site_01_briefing', **{k:p['base'] for k,p in gang_leaders.LEADERS.items()}}
NAMES = {'garrett':'Garrett', 'ivan':'Ivan', 'crow':'The Crow', 'takeo':'Takeo Mishima'}
for _key, _spec in list(ORGANISATIONS.items()):
    _name = NAMES.get(ATTENDEES[_key], ATTENDEES[_key])
    ORGANISATIONS[_key] = (_spec[0], VENUES[_key], _name, _name, _spec[4])


def migrate_meeting(m):
    if m.get('meeting_v2') or m['status'] not in ('booked','in_progress'): return
    m.update(meeting_v2=True, attendee=ATTENDEES[m['target']], venue=VENUES[m['target']],
             representative=ORGANISATIONS[m['target']][2],
             agenda=[ORGANISATIONS[m['target']][4], 'Responsibilities, boundaries and mutual expectations',
                     'Terms, deadlines and decision'], agenda_index=0)


def access(s, target):
    import hidden_cast, crime_operations
    if target == 'syndicate': return hidden_cast.hq_access(s, s['player'])
    if target == 'shinokami': return crime_operations.permitted(s, s['player'], 'site_01')
    return True


def mandate(s):
    import combat
    if combat.affiliation(s,s['player'])[0] is None and s.get('combat',{}).get('expelled'): return None
    d=jobs.ensure(s)
    import bubblegram_roles
    canonical = bubblegram_roles.mandate(s['player'])
    if canonical: return canonical
    if s['player']=='garrett': return ('dragons','Red Dragons','Leader',25000)
    if s['player']=='ivan': return ('joker','Black and White Joker network','Black and White Joker',40000)
    m=d['membership']
    g=d['gang']
    if g and g.get('role')=='Founder' and not g.get('id') and not g.get('established'):
        if m and m.get('strikes',0)>=2: return None
        return ('crew:'+g['name'].casefold(),g['name'],jobs.progression.gang_title(g),5000)
    if m:
        threshold=5 if m['faction']=='Syndicate' else 4
        if m['rank']<threshold or m['strikes']>=2: return None
        return (m['faction'].lower(),m['faction']+' · '+m['branch'],jobs.BRANCHES[m['branch']][2][m['rank']],5000)
    g=d['gang']
    if g and g.get('rank',0)>=3:
        return (g.get('id','crew:'+g['name'].casefold()),g['name'],jobs.progression.gang_title(g),5000)
    return None


def books(s):
    return s.get('crime_diplomacy',{}).get('organisations',{})


def commitments(s):
    return [m for b in books(s).values() for m in b['meetings'] if m['status'] in ('booked','in_progress')]


def has_obligations(s):
    return bool(commitments(s) or any(d['status']=='active' for b in books(s).values() for d in b['deals']))


def ensure(s):
    role=mandate(s)
    if not role: raise ValueError('Leadership requires an established command or mission role, gang Captain / city-network Founder, or faction executive.')
    root=s.setdefault('crime_diplomacy',dict(version=1,organisations={}))
    key,name,title,budget=role
    b=root['organisations'].setdefault(key,dict(name=name,treasury=budget,influence=0,relations={},invitations=[],meetings=[],deals=[],history=[],last_invite_day=-1,last_request_day=-1,last_operation_day=-1))
    import bubblegram_roles
    if s['player'] in bubblegram_roles.ROLES and not b.get('playable_role_standing_v1'):
        b['relations']['syndicate'] = max(0, min(100, b['relations'].get('syndicate', 35) + 35))
        b['influence'] = max(b['influence'], 15 if s['player'] == 'sylvanis' else 10)
        b['playable_role_standing_v1'] = True
    if s['player']=='ivan' and not b.get('joker_standing_v1'):
        # Correct the generic baseline once, retaining any earned relationship delta.
        b['relations']['syndicate']=max(0,min(100,b['relations'].get('syndicate',35)+63))
        b['joker_standing_v1']=True
    if s['player']=='garrett' and not b.get('dragons_standing_v1'):
        b['relations']['dragons']=max(0,min(100,b['relations'].get('dragons',35)+60))
        b['dragons_standing_v1']=True
    if not b.get('faction_relations_v1'):
        import criminal_dynamics
        for target in ORGANISATIONS:
            base = criminal_dynamics.baseline(key, target)
            if base != 35:
                b['relations'][target] = max(0, min(100, b['relations'].get(target, 35) + base - 35))
        b['faction_relations_v1'] = True
    tick(s)
    day=s['world']['minute']//1440
    targets=[k for k in ORGANISATIONS if k!=key and access(s,k) and ATTENDEES[k]!=s['player']]
    if jobs.ensure(s)['heat']<60 and b['last_invite_day']!=day and len([i for i in b['invitations'] if i['status']=='offered'])<3:
        target=targets[day%len(targets)]
        leader=leader_ready(s,b,target)
        b['invitations'].append(dict(id=uuid.uuid4().hex,target=target,leader=leader,status='offered',start=(day+1)*1440+18*60))
        b['last_invite_day']=day
    for pair,value in s.get('combat',{}).get('diplomacy',{}).items():
        parts=pair.split('|')
        if len(parts)==2 and key in parts and b.get('combat_relation_markers',{}).get(pair)!=value:
            target=parts[1] if parts[0]==key else parts[0]
            b['relations'][target]=min(b['relations'].get(target,35),value)
            b.setdefault('combat_relation_markers',{})[pair]=value
    return b


def relation(b,target):
    return b['relations'].get(target,35)


def leader_ready(s,b,target):
    return jobs.ensure(s)['reputation']>=80 and b['influence']>=10 and relation(b,target)>=50


def record(s,b,text,success=None):
    b['history'].append(dict(minute=s['world']['minute'],text=text))
    jobs.log(s,text,True)
    # Explicit leadership actions feed the existing private career; no project is started.
    key={'garrett':'dragons','ivan':'joker'}.get(s['player'])
    import bubblegram_roles
    if s['player'] in bubblegram_roles.ROLES: key = 'cast_' + s['player']
    if key and success is not None:
        c=careers.get(s,key)
        c['reputation']=careers.clamp(c['reputation']+(2 if success else -3))
        c['pressure']=careers.clamp(c['pressure']+(-3 if success else 5))
        if success and c['project']: c['project']['quality']+=4
        careers.record(s,key,text)
    return text


def tick(s):
    now=s['world']['minute']
    for b in books(s).values():
        for invite in b['invitations']:
            if invite['status']=='offered' and now>=invite['start']: invite['status']='expired'
        for m in b['meetings']:
            migrate_meeting(m)
            if m['status'] not in ('booked','in_progress'): continue
            if now>=m['end']:
                m['status']='missed'; b['relations'][m['target']]=max(0,relation(b,m['target'])-6)
                b['influence']=max(0,b['influence']-2)
                record(s,b,'Missed the '+ORGANISATIONS[m['target']][0]+' leadership meeting. Relationship −6; influence −2.',False)
                close_scene(s,m)
            elif now>=m['start']-60 and not m['reminded']:
                m['reminded']=True
                s.setdefault('event_notifications',[]).append('Private Bubblegram appointment due. Open Leadership for details.')
        for deal in b['deals']:
            if deal['status']=='active' and now>deal['deadline']:
                deal['status']='defaulted'
                b['relations'][deal['target']]=max(0,relation(b,deal['target'])-10)
                d=jobs.ensure(s); d['reputation']=max(0,d['reputation']-3)
                record(s,b,'Defaulted on '+ORGANISATIONS[deal['target']][0]+' deal. Committed capital lost; relationship −10; criminal reputation −3.',False)


def book(s,target,start,leader=False):
    b=ensure(s); role=mandate(s)
    if jobs.ensure(s)['heat']>=60: raise ValueError('Reduce heat below 60 before arranging new business meetings.')
    if target not in ORGANISATIONS or target==role[0]: raise ValueError('Choose another organisation.')
    if ATTENDEES[target] == s['player']: raise ValueError('You cannot book a meeting with yourself.')
    if not access(s,target): raise ValueError('This leader receives visitors only at headquarters. Earn the existing headquarters clearance first; an appointment does not grant access.')
    if leader and not leader_ready(s,b,target): raise ValueError('Leader meetings require reputation 80, influence 10 and relationship 50 with this organisation.')
    if start<=s['world']['minute']: raise ValueError('Choose a future meeting.')
    if careers.conflict(s,start,start+60): raise ValueError('This meeting overlaps an accepted commitment. Choose another day.')
    import syndicate_council
    council_start=syndicate_council.week_start(start)
    if ATTENDEES[target] in syndicate_council.ROSTER and start<council_start+60 and council_start<start+60:
        raise ValueError('This leader is attending the Crow’s weekly council at that time.')
    spec=ORGANISATIONS[target]
    m=dict(id=uuid.uuid4().hex,target=target,start=start,end=start+60,venue=spec[1],
           title='Private leadership appointment',representative=spec[3 if leader else 2],leader=leader,status='booked',reminded=False)
    b['meetings'].append(m)
    migrate_meeting(m)
    record(s,b,'Booked a meeting with '+m['representative']+' at '+spec[1]+'. Arrive within 15 minutes; the appointment lasts one hour.')
    return m


def request(s,target,leader=False):
    b=ensure(s); day=s['world']['minute']//1440
    if b['last_request_day']==day: raise ValueError('One outgoing meeting request per story day.')
    m=book(s,target,(day+1)*1440+18*60,leader)
    b['last_request_day']=day
    return 'Meeting confirmed with '+m['representative']+'. See your private appointments.'


def invitation(s,ident,accept=True,delay=0):
    b=ensure(s); i=next((i for i in b['invitations'] if i['id']==ident),None)
    if not i or i['status']!='offered': raise ValueError('This invitation is no longer open.')
    if delay not in (0,1): raise ValueError('Choose the offered day or the following day.')
    if accept:
        book(s,i['target'],i['start']+delay*1440,i['leader'])
        i['status']='accepted'
    else: i['status']='declined'
    return 'Invitation '+i['status']+'.'


def meeting(s,ident):
    b=ensure(s); m=next((m for m in b['meetings'] if m['id']==ident),None)
    if not m or m['status'] not in ('booked','in_progress'): raise ValueError('This meeting is no longer booked.')
    return b,m


def cancel(s,ident):
    b,m=meeting(s,ident)
    late=s['world']['minute']>=m['start']
    m['status']='cancelled'
    close_scene(s,m)
    if late: b['relations'][m['target']]=max(0,relation(b,m['target'])-3)
    return record(s,b,'Meeting cancelled.'+(' Late cancellation: relationship −3.' if late else ' No penalty.'))


def reschedule(s,ident):
    b,m=meeting(s,ident)
    if s['world']['minute']>=m['start']: raise ValueError('Only future meetings can be rescheduled.')
    start=m['start']+1440
    if careers.conflict(s,start,start+60,ident): raise ValueError('The new time conflicts with another commitment.')
    import syndicate_council
    council_start=syndicate_council.week_start(start)
    if m['attendee'] in syndicate_council.ROSTER and start<council_start+60 and council_start<start+60:
        raise ValueError('This leader will be attending the weekly council. Choose a different appointment.')
    m.update(start=start,end=start+60,reminded=False)
    return record(s,b,'Meeting moved one day later.')


def guard(s,venue,duration,exclude=None):
    if jobs.ensure(s)['pending']: raise ValueError('Finish or withdraw your current Bubblegram / Jobseek assignment first.')
    jobs.guard(s,venue,duration,exclude)
    if s['world'].get('party'): raise ValueError('Attend this private business appointment without uncleared companions.')


def conclude(s,ident,approach):
    b,m=meeting(s,ident); now=s['world']['minute']
    require_scene(s,m)
    if m['agenda_index'] < len(m['agenda']): raise ValueError('Review every agenda item in person before making a decision.')
    if approach not in (*TERMS,'relations'): raise ValueError('Choose offered terms or relationship talks.')
    if approach in TERMS:
        if jobs.ensure(s)['heat']>=60: raise ValueError('Heat is too high for a new deal. Choose relationship talks or reduce heat first.')
        terms=TERMS[approach]
        if len([d for d in b['deals'] if d['status']=='active'])>=2: raise ValueError('Your organisation can manage two active deals. Complete or abandon one first.')
        if b['treasury']<terms['stake']: raise ValueError('Insufficient organisation funds. Choose relationship talks or add funding before the meeting.')
        b['treasury']-=terms['stake']
        deal=dict(id=uuid.uuid4().hex,target=m['target'],venue=m['venue'],terms=approach,
                  stake=terms['stake'],revenue=terms['revenue'],deadline=m['end']+3*1440,status='active',extended=False)
        b['deals'].append(deal)
        outcome=f'Agreed {approach} terms; ${terms["stake"]:,} committed. Complete the deal within three days.'
        if m['target']=='hamayashi': jobs.ensure(s)['hamayashi_affiliated']=True
    else: outcome='Agreed to maintain a direct negotiating channel; no money committed.'
    b['relations'][m['target']]=min(100,relation(b,m['target'])+(12 if m['leader'] else 8))
    b['influence']=min(100,b['influence']+(8 if m['leader'] else 5))
    m['status']='completed'; m['decision']=approach
    s['groups'][m['group']]['history'].append(dict(speaker=m.get('speaker',m['representative']),text=outcome,minute=now))
    careers.spend_time(s,m['end']-now,8)
    close_scene(s,m)
    return record(s,b,'Met '+m['representative']+'. '+outcome,True)


def deal(s,ident):
    b=ensure(s); d=next((d for d in b['deals'] if d['id']==ident),None)
    if not d or d['status']!='active': raise ValueError('This deal is no longer active.')
    return b,d


def settle(s,ident):
    b,d=deal(s,ident); now=s['world']['minute']; progress=jobs.ensure(s)
    if progress['heat']>=60: raise ValueError('Reduce heat below 60 before completing criminal business.')
    if now+60>d['deadline']: raise ValueError('There is not enough time to complete this deal. Extend it once or abandon it.')
    if progress['last_contract']==now//1440: raise ValueError('One criminal operation per day, shared with Bubblegram contracts.')
    guard(s,d['venue'],60)
    terms=TERMS[d['terms']]; success=terms['risk'] is None or progress['heat']<terms['risk']
    progress['last_contract']=now//1440; progress['heat']=min(100,progress['heat']+terms['heat'])
    d['status']='completed' if success else 'failed'
    dividend=0
    if success:
        dividend=(d['revenue']-d['stake'])//5
        b['treasury']+=d['revenue']-dividend
        s['world']['money']+=dividend
        progress['reputation']=min(100,progress['reputation']+3); progress['completed']+=1
        if progress['gang']: progress['gang']['standing']+=2
        b['relations'][d['target']]=min(100,relation(b,d['target'])+6)
        b['influence']=min(100,b['influence']+4)
    else:
        progress['reputation']=max(0,progress['reputation']-4)
        b['relations'][d['target']]=max(0,relation(b,d['target'])-10)
    careers.spend_time(s,60,12)
    return record(s,b,ORGANISATIONS[d['target']][0]+' deal '+d['status']+'. '+
        (f'Revenue ${d["revenue"]:,}; personal profit share ${dividend:,}. Organisation funds ${b["treasury"]:,}.' if success else 'Committed capital lost; relationship −10; reputation −4.'),success)


def extend(s,ident):
    b,d=deal(s,ident)
    if d['extended']: raise ValueError('Each deal can be extended once.')
    d['deadline']+=1440; d['extended']=True
    b['relations'][d['target']]=max(0,relation(b,d['target'])-2)
    return record(s,b,'Negotiated one additional day; relationship −2.')


def abandon(s,ident):
    b,d=deal(s,ident); d['status']='abandoned'
    b['treasury']+=d['stake']//2
    b['relations'][d['target']]=max(0,relation(b,d['target'])-6)
    return record(s,b,'Deal abandoned. Half the committed capital recovered; relationship −6.',False)


def fund(s):
    b=ensure(s)
    if s['world']['money']<1000: raise ValueError('You need $1,000 in your personal wallet.')
    s['world']['money']-=1000; b['treasury']+=1000
    return record(s,b,'Transferred $1,000 from personal funds into the organisation treasury.')


def wait(s,ident):
    b,m=meeting(s,ident); delta=m['start']-s['world']['minute']
    if not 0<delta<=2880: raise ValueError('Wait only for a meeting within the next two days.')
    if jobs.ensure(s)['pending'] or s.get('careers',{}).get('active'): raise ValueError('Finish your current assignment before waiting.')
    if careers.conflict(s,s['world']['minute'],m['start'],ident): raise ValueError('Another commitment occurs before this meeting.')
    if s['world']['cast'][s['player']].get('journey'): raise ValueError('Finish travelling before waiting.')
    import world_loop
    world_loop.advance(s,delta)
    return 'The meeting is ready. Attend at its venue.'


def context(s,who):
    if who!=s['player']: return []
    return [dict(e) for b in books(s).values() for e in b['history']][-8:]


def npc_appointment(s,who,now):
    for m in commitments(s):
        migrate_meeting(m)
        if m['attendee']==who and m['start']<=now<m['end']:
            return dict(venue=m['venue'],title='Leadership meeting with '+m['representative'])


def begin(s,ident):
    b,m=meeting(s,ident); now=s['world']['minute']
    if m['status']=='in_progress':
        require_scene(s,m)
        return m['group']
    if not m['start']<=now<=m['start']+15: raise ValueError('Arrive during the first 15 minutes of the booked meeting.')
    if not access(s,m['target']): raise ValueError('Your headquarters clearance is no longer valid.')
    guard(s,m['venue'],m['end']-now,ident)
    import groups, town
    who=m['attendee']
    if who in gang_leaders.BY_NAME:
        town.town_residents.refresh(s)
        gid=groups.open_local(s,who)
    else:
        actor=s['world']['cast'][who]
        if actor['location']!=m['venue'] or actor.get('journey'):
            raise ValueError('The scheduled attendee has not arrived. Advance the game clock to their appointment.')
        groups.form(s,[who]); gid=s['active_group']
    m.update(status='in_progress',group=gid,joined=now)
    import game_core
    m['speaker']=who if who in gang_leaders.BY_NAME else game_core.contact_name(s,who)
    group=s['groups'][gid]; group['leadership_meeting']=m['id']
    opening={'garrett':'All right. Let us talk business.', 'ivan':'Let us keep the obligations clear.',
             'crow':'Give your report.', 'takeo':'State the terms.',
             'Mara Voss':'Keep it precise. I need to know what my crew owes.',
             'Darius Cole':'First, I want to know who carries the cost.',
             'Rafe Calder':'Let us hear what you want from the club.',
             'Daichi Kurose':'We will proceed in order.',
             'Isabel Vega':'Be exact. I am listening.',
             'Evelyn Mercer':'Let us establish the obligations before discussing returns.'}[who]
    group['history'].extend([
        dict(speaker='Status update',text=f"Scheduled leadership meeting; {m['end']-now} minutes remaining. Agenda: "+'; '.join(m['agenda']),minute=now),
        dict(speaker=m['speaker'],text=opening,minute=now)])
    return gid


def require_scene(s,m):
    import town
    group=s.get('groups',{}).get(m.get('group'),{})
    who=m['attendee']; actor=s['world']['cast'][s['player']]
    present=(who in s['world']['npcs']) if who in gang_leaders.BY_NAME else (
        s['world']['cast'][who]['location']==m['venue'] and not s['world']['cast'][who].get('journey'))
    if (m['status']!='in_progress' or s.get('active_group')!=m.get('group') or not group.get('open')
            or group.get('channel')=='text' or not present or s['world']['location']!=m['venue']
            or actor.get('journey') or actor['location']!=m['venue'] or not s['world']['minute']<m['end']):
        raise ValueError('Continue this appointment together in the in-person window before its timer ends.')
    if not access(s,m['target']): raise ValueError('Current headquarters clearance is required to continue this meeting.')


def discuss(s,ident):
    b,m=meeting(s,ident); require_scene(s,m)
    if m['agenda_index']>=len(m['agenda']): raise ValueError('The agenda is complete. Choose the meeting decision.')
    if s['world']['minute']+10>=m['end']: raise ValueError('Not enough time remains for another ten-minute agenda item.')
    topic=m['agenda'][m['agenda_index']]; m['agenda_index']+=1
    s['groups'][m['group']]['history'].append(dict(speaker='Narrator',text='The meeting reviews: '+topic+'. No agreement is binding until the final decision.',minute=s['world']['minute']))
    careers.spend_time(s,10,2)
    return 'Agenda reviewed: '+topic+'.'


def close_scene(s,m):
    import groups
    if s.get('active_group') and s.get('active_group')==m.get('group'):
        groups.close_active(s,'Leadership appointment '+m['status']+'.')
        s['world']['party']=[w for w in s['world']['party'] if w!=m.get('attendee')]


def scene_context(s,who=None):
    for m in commitments(s):
        if (m.get('status')=='in_progress' and s.get('active_group')==m.get('group')
                and s.get('groups',{}).get(m.get('group'),{}).get('open')
                and s['world']['location']==m['venue']
                and (who is None or who in (s['player'],m.get('attendee')))):
            return dict(attendee=m['representative'], date=str(__import__('story_calendar').story_date(m['start'])),
                start=m['start'],end=m['end'],minutes_left=max(0,m['end']-s['world']['minute']),
                agenda=m['agenda'],reviewed=m['agenda_index'],
                rule='This is a real scheduled in-person negotiation. Discuss the agenda naturally. Only explicit meeting controls can commit money or conclude a deal.')
    return {}
