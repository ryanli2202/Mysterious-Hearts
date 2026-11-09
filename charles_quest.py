"""Garrett's authored investigation. Evidence, not dialogue, advances the search."""
import copy
LAB = 'glasshouse_lab'
# title, location, question, choices, verified finding. No future finding appears in the current view.
STEPS = (
 ('Mei’s delivery slip','noodle_shop','Mei’s old dispatch photo shows a correction eleven days after Charles left his job. The crooked H resembles his notes on the fridge.',('Keep the slip as a lead, not proof','Write down why the handwriting feels familiar'),'A dispatch slip was corrected from six crates to four. The handwriting resembles Charles’s, but authorship is unverified.'),
 ('The receiving copy','noodle_shop','The photo cuts off the stamp. Mei can provide the complete receiving copy.',('Compare both copies','Ask Mei to preserve the original'),'West Pier Cold Storage, Hong Kong, received four crates eleven days after Charles left work. The driver did not sign.'),
 ('Reconcile the crates','archive','The duplicate tally lists six packed crates and four collected. A discrepancy is not a missing passenger.',('Separate packed from collected totals','Record the uncertainty'),'Two crates remained at dispatch. The correction reconciles the totals; it proves neither Charles’s handwriting nor his travel.'),
 ('What the stamp proves','interpol_hq','At the public desk, Dana explains what receiving records establish. This is a records enquiry, not an announced investigation.',('Ask for the authorisation procedure','Request a public records form'),'The stamp confirms delivery acceptance only. A dated dispatch authorisation is needed to identify who ordered collection.'),
 ('Mei’s missing page','noodle_shop','Mei has found the matching index, but its authorisation page is absent. Her former records custodian may have the retained copy.',('Request the retained copy','Send the matching index number'),'Mei’s index matches the consignment. The missing authorisation has been requested from the records custodian.'),
 ('A Winterfield connection','archive','The custodian’s retained page is now available. Compare its date, crate count and reference number with the receiving copy.',('Cross-check all three fields','Treat the name alone as proof'),'The matching authorisation names Greyglass Service House in Winterfield as the equipment-service correspondent. It names no passenger and does not locate Charles.'),
 ('The service-house account','site_08','A frontage clerk recalls a quiet martial artist checking returned equipment. The description could fit Charles, but it is not identification.',('Ask for the dated service receipt','Accuse the clerk of hiding Charles'),'A dated receipt connects the old consignment to a private research-office account. The clerk accepts a sealed family enquiry through the existing return-document channel.'),
 ('Separate evidence from rumour','archive','The returned reference mentions blue and red research files. A street rumour calls every associate a dealer. Neither explains why Charles disappeared.',('Follow the document chain, not the rumour','Treat the rumour as a confirmed confession'),'The office references are consistent across the retained copies. Blue and red file labels are not evidence that Charles sells drugs or was abducted. Your sealed enquiry has reached the office.'),
 ('A question only family can answer','noodle_shop','A handwritten reply asks: “When we tried to make her broth again, what did we use to measure it?” It offers no number. Answer from your own memory.',('Our father’s chipped teacup','A measuring jug from the restaurant'),'The reply answers with the unfinished shrimp-shell argument from your last call. Charles offers a private evening meeting at the Glasshouse, 19:00–23:00. A personal visitor authorisation and directions are enclosed. Come alone; this is not faction clearance.'),
 ('The brother in the laboratory',LAB,'Charles is here, alive. The room must be private before you confront the silence between you.',('Ask why he let you keep searching','Tell him you needed to know he was alive'),'Charles confirms that he disappeared deliberately to infiltrate the Syndicate and work beside Sylvanis, seeking to avenge your parents. He names no newly established culprit. He withheld contact to protect his cover, admits that it hurt you, and shares his private number for direct texts. Until now only Sylvanis could call him. He stays in the laboratory; this is a reunion, not a rescue or extraction.'),
 ('Choose what comes next',LAB,'You know the truth now. Charles asks you not to expose his cover. You can support him without pretending his silence was fair.',('Protect the cover and agree to keep in touch','Protect the cover, but demand honest boundaries'),'You agree to private direct texts. Brief written check-ins through the existing document channel remain an optional fallback. He remains at the lab. The search is resolved: he is alive, and you know why he disappeared. His mission remains unfinished and private.'),
)


def read(s):
    if 'charles_quest' in s: return s['charles_quest']
    old=s.get('charles_lead','unopened')
    step=0 if old=='unopened' else 1 if old=='slip' else 2
    prior=s.get('living_world',{}).get('mystery',[])
    if step==2: step+=min(3,len(prior))
    return dict(version=1,step=step,evidence=[dict(title=STEPS[i][0],finding=STEPS[i][4],legacy=True) for i in range(step)],
                choices=[],last_day=prior[-1].get('day',-1) if prior else -1,retry_day=-1,setbacks=0,ending=None,checkins=[])


def data(s):
    return s.setdefault('charles_quest',copy.deepcopy(read(s)))


def guest(s,who):
    return bool(s and who=='garrett' and ((s.get('player')=='garrett' and read(s)['step']>=9) or __import__('charles_disclosure').read(s).get('stage',0)>=3))


def reunited(s):
    return bool(s and s.get('player')=='garrett' and read(s)['step']>=10)


def objective(s):
    d=read(s)
    if d['step']>=len(STEPS): return ('Written check-in','noodle_shop','The search is complete. Read a new note here once per story day.')
    title,venue,question,*_=STEPS[d['step']]
    return title,venue,question


def guard(s,venue,private=False):
    if s['player']!='garrett': raise ValueError('This investigation belongs to Garrett’s story.')
    actor=s['world']['cast']['garrett']
    if s['world']['location']!=venue or actor['location']!=venue or actor.get('journey'):
        raise ValueError('Visit the current objective in person before proceeding.')
    if actor.get('activity')=='Sleep': raise ValueError('Wake up before investigating.')
    if private:
        now=s['world']['minute']%1440
        if not 19*60<=now<23*60: raise ValueError('Charles’s private visitor window is 19:00–23:00.')
        if s['world'].get('party') or s['world'].get('npcs') or any(who not in ('garrett','charles') and a['location']==LAB and not a.get('journey') for who,a in s['world']['cast'].items()):
            raise ValueError('Wait until you and Charles are alone. No sensitive discussion with other listeners.')
        charles=s['world']['cast']['charles']
        if charles['location']!=LAB or charles.get('journey'): raise ValueError('Charles must be here.')


def advance(s,choice):
    d=read(s); step=d['step']
    if step>=len(STEPS): raise ValueError('The search is already resolved.')
    if type(choice) is not int or choice not in (0,1): raise ValueError('Choose one of the current responses.')
    title,venue,question,options,finding=STEPS[step]
    guard(s,venue,step>=9)
    day=s['world']['minute']//1440
    if day<d.get('retry_day',-1): raise ValueError('The contact needs until the next story day before another enquiry.')
    if 2<=step<=8 and day<=d['last_day']: raise ValueError('The next document response arrives on the next story day.')
    d=data(s)
    if 5<=step<=8 and choice==1:
        d['setbacks']+=1;d['retry_day']=day+1
        d['choices'].append(dict(step=step,choice=options[choice],day=day,outcome='unverified'))
        return ('That does not establish the connection. The enquiry pauses; retry tomorrow with the document evidence.' if step!=8 else 'The reply cannot authenticate you. Review the family memory and try again tomorrow.')
    if step==9:
        finding += ('\n\nCharles sets down the file. “I thought keeping you out of it would keep you safe. It left you searching instead.” '
                    'He looks at the old slip. “I came here deliberately. Sylvanis thinks I work for him. I needed to get close enough to understand what happened to our parents.” '
                    'He offers no proof against a named killer and no promise of a quick end.')
        finding += ('\n\n“You should have trusted me with the choice,” you tell him. Charles does not argue.' if choice==0 else
                    '\n\n“I needed my brother, not another mystery,” you tell him. “I know,” Charles says. For once, there is no efficient answer.')
    if step==10:
        finding += ('\n\n“I will keep your cover,” you say. “But you write. Even if all you can say is that you are still here.” Charles agrees. A quiet alliance replaces the silence.' if choice==0 else
                    '\n\n“I will not expose you. That does not make the silence all right.” Charles accepts that forgiveness cannot be demanded. The reunion ends with firm boundaries and a promise to write.')
    d['evidence'].append(dict(title=title,finding=finding,day=day))
    d['choices'].append(dict(step=step,choice=options[choice],day=day,outcome='verified'))
    d.update(step=step+1,last_day=day,retry_day=-1)
    s['charles_lead']='slip' if step==0 else 'traced'
    if step==9:
        import hidden_cast
        hidden_cast.mark_met(s,'charles')
        import messaging
        messaging.initiate(s,'charles','After the private reunion, send Garrett a brief private reassurance that this is your number and you will keep in touch. Keep operational details out of the message.')
    if step==10:
        d['ending']='quiet alliance' if choice==0 else 'guarded reconciliation'
        bond=s['friendships']['charles'];bond['trust']=min(100,bond['trust']+(6 if choice==0 else 3));bond['closeness']=min(100,bond['closeness']+6)
    return finding


def check_in(s):
    guard(s,'noodle_shop')
    d=read(s);day=s['world']['minute']//1440
    if d['step']<len(STEPS): raise ValueError('Finish the reunion first.')
    if d['checkins'] and d['checkins'][-1]['day']==day: raise ValueError('No further note has arrived today.')
    notes=('“Still here. I have not forgotten our agreement.” Charles gives no operational details.',
           '“You were right about the broth. Toast them first.” A small ordinary answer, after so much silence.',
           '“I will tell you when I can speak safely. Do not mistake caution for permission to disappear on you again.”')
    text=notes[len(d['checkins'])%len(notes)]
    data(s)['checkins'].append(dict(day=day,text=text))
    return text


def knowledge(s,who,listeners=()):
    if not s: return ''
    if s.get('player')!='garrett': return __import__('charles_disclosure').knowledge(s,who,listeners)
    if who not in ('garrett','charles'): return ''
    d=read(s)
    if d['step']<10:
        return ('Garrett’s verified search evidence: '+ ' '.join(r['finding'] for r in d['evidence']) + ' His brother’s true purpose is still unknown to Garrett.') if who=='garrett' else ''
    shared=bool(listeners) and set(listeners)<= {'garrett','charles'}
    return ('Authoritative completed reunion overrides earlier missing-brother assumptions: Garrett has met Charles alive in the lab. '+
            ('The brothers privately discussed Charles’s undercover mission to avenge their parents. ' if shared else 'Do not disclose the location, infiltration, revenge motive or cover to these listeners. ')+
            'Charles shares his private number only with Sylvanis and, after this reunion, Garrett. Direct private texts are allowed; no group messages. He remains in the laboratory. No death, extraction or completed revenge occurred. Ending: '+str(d.get('ending') or 'reunion in progress')+'.')


def recognise(s):
    """A legitimate early lab visitor need not pretend not to see his brother."""
    guard(s,LAB,True)
    import criminal_dynamics, hidden_cast
    if not criminal_dynamics.lab_access('garrett',s): raise ValueError('You need existing laboratory clearance.')
    if read(s)['step']>=9: raise ValueError('The reunion is already available.')
    d=data(s);d['step']=9
    d['evidence'].append(dict(title='Direct encounter',finding='You saw Charles alive in the Glasshouse. The unvisited documentary trail is not treated as completed.',day=s['world']['minute']//1440))
    hidden_cast.mark_met(s,'charles')
    return 'You recognise your brother. Ask him privately why he disappeared.'
