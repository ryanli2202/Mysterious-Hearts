"""Betrayal consequences are applied once per informed person, with a source."""
import custom_protagonist
import living_world

def learn(s,report,who,source):
    import town
    if who in report['known']: return
    report['known'][who]=source
    living_world.record(s,f"report:{report['id']}:{who}",report['text']+' Source: '+source,[s['player'],who])
    r=s['relationships'].get(who)
    if not r: return
    r.setdefault('known_betrayals',[]).append(report['text'])
    partner=who in report['partners']
    r['trust']=max(0,r['trust']-(35 if partner else 15))
    r['closeness']=max(0,r['closeness']-(25 if partner else 5))
    if partner:
        repeated=bool(r.get('unresolved_harm'))
        r['unresolved_harm']='cheating'; r['status']='strained'
        r['jealousy']=min(100,r.get('jealousy',0)+40); s['emotions'][who]='angry'
        if repeated: town.log(s,town.end_relationship(s,who))
    target=report['target']
    # Inter-person tension requires both people to have learned what happened.
    for partner_id in report['partners']:
        if partner_id in report['known'] and target in report['known']:
            key=town.bond_key(s,partner_id,target)
            if key not in report.setdefault('tension_applied',[]):
                report['tension_applied'].append(key)
                s['girl_bonds'][key]='tension over overlapping romance'
                if partner_id in s['routes'] and target in s['routes']:
                    town.loop.bond_event(s,partner_id,target,report['text'],tension=35)

def observe(s,target,activity):
    import town
    partners=[who for who,r in s['relationships'].items() if who!=target and r['status'] in ('official','strained')]
    if not partners: return
    reports=living_world.ensure(s)['reports']
    report=dict(id=len(reports),target=target,partners=partners,minute=s['world']['minute'],known={},
                text=f"{custom_protagonist.display_name(s["player"])} pursued {activity} with {target.title()} while committed to {', '.join(p.title() for p in partners)}.")
    reports.append(report)
    # The involved person knows their own act. Nearby people only witness physical acts.
    learn(s,report,target,'direct participant')
    if activity in ('kiss','romance'):
        route=s['routes'].get(target,{})
        if route.get('channel')=='in_person' or target in s['world'].get('npcs',[]):
            for who in s['relationships']:
                if who!=target and town.present(s,who): learn(s,report,who,'witnessed in person')
    town.log(s,'Recorded privately: '+report['text'])

def disclose(s,report_id,who):
    import town
    reports=living_world.ensure(s)['reports']
    if not isinstance(report_id,int) or not 0<=report_id<len(reports): raise ValueError('Unknown event.')
    if who not in s['relationships'] or not town.hidden.contact(s,who): raise ValueError('Choose a known contact.')
    report=reports[report_id]
    if who in report['known']: raise ValueError('They already know about this event.')
    learn(s,report,who,'player disclosure by private message')
    route=s['routes'].get(who)
    if route is not None:
        route['history'].append(dict(role='status',content='You disclosed: '+report['text'],minute=s['world']['minute']))
    town.log(s,'Disclosed to '+who.title()+': '+report['text'])

def filter_context(s,data,members):
    """Prevent other relationship records and global bonds from leaking private events."""
    reports=living_world.ensure(s)['reports']
    permitted=[r['text'] for r in reports if all(m in r['known'] for m in members)]
    all_new={r['text'] for r in reports}
    for who,r in data['relationships'].items():
        r['known_betrayals']=[t for t in r.get('known_betrayals',[]) if t not in all_new or t in permitted]
        if who not in members:
            # Only their own relationship state is supplied. Public ties live in speaker references.
            for key in ('status','romance','trust','closeness','attraction','jealousy','unresolved_harm'):
                r.pop(key,None)
    for field in ('girl_bonds','bond_details'):
        data[field]={k:v for k,v in data[field].items() if all(who in members for who in k.split(':'))}
    data['witnessed_or_disclosed_betrayals']=permitted
    data['knowledge_rule']='Only the supplied witnessed/disclosed events establish knowledge. Other private relationships are not public knowledge. Legacy known events remain known.'
