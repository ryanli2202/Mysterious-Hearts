"""Rei: What Remains. Authored evidence and victories, never generated claims."""
import organisation_guards as guards

# Each scene supplies testimony or documents, not a diagnosis or perfect memory.
SCENES = (
 ('The blank spaces', 'rei_home',
  'An old sketchbook contains a training timetable in your childhood handwriting. You remember counting the intervals between instructions, not the whole room. Yuriko left the book with you years ago; it is not a newly discovered message from her. You set it beside a drawing made after you escaped. Both belong to your life.',
  ('Record the fragment without filling its gaps', 'Pause, ground yourself, then record what is actually on the page'),
  'The childhood timetable carries the Hamayashi-kai seal. A present-day Kurose House public notice uses the same name. Shared names do not establish surviving clan members.'),
 ('A name that survived', 'archive',
  'The archive holds dated filings: the original clan ended, while a later successor adopted its name. A retained training ledger corroborates imposed drills and punishment, with Rei recorded as a child subject, never a consenting recruit. A transfer notation confirms that records, rather than the old clan itself, survived. It does not identify his parents or restore every moment of the escape.',
  ('Copy the records and their dates', 'Keep the original gaps visible beside the evidence'),
  'The current organisation operates Kurose House, a riverside annex and a supply house. Emi Suda and Ren Aoki administer the successor. Daichi Kurose leads it after Keisuke’s departure.'),
 ('Marcus, beyond what happened', 'rei_home',
  'You open the school storyboard you kept: Marcus’s miniature city, the impossible bus timetable, a pigeon filmed one frame at a time. You remember his joke about your hand being a very local weather event. You also remember Joseph Richter and the classmates who repeatedly bullied him. Marcus later died by suicide. There is no single explanation on this page, and no fight can finish the film or make you responsible for saving him.',
  ('Write about the person Marcus was', 'Set the storyboard somewhere you can return to it'),
  'Rei distinguishes remembered school grief from his childhood memory gaps. He records Joseph’s repeated bullying and later minimisation without inventing final words or a cause of death.'),
 ('The consent that was not there', 'blackstone_hq',
  'At reception you request the publicly available research participation form. It describes Awakened performance assessment, but its withdrawal clause points to a separate security contract. Robin provides the published form, not access to private patient files. A public procurement reference identifies the archive copy of that contract.',
  ('Compare the referral number and withdrawal clause', 'Photograph the public form and retain its provenance'),
  'Blackstone’s public referral and security contract use the same project number. The records warrant investigation; the clerk has not confessed to an experiment.'),
 ('The experimental programme', 'archive',
  'The matching contract and an anonymised complaint filed with it describe restraint trials on Awakened participants who attempted to withdraw. Richter’s signed authorisation retains subjects for weapons-response testing. Equipment deliveries identify a loading compound, records office, experimental wing and executive command. These documents establish this Winterfield programme without exposing participant names.',
  ('Preserve the authorisation with the complaint', 'Separate documented conduct from unanswered questions'),
  'The records corroborate Richter’s coercive Awakened experimentation. Blackstone deploys PMC guards, Seeker cyborgs and Headhunter cyborgs. Rei retains an evidence copy before approaching headquarters.'),
 ('The successor answers', 'hamayashi_house',
  'Emi Suda meets you with Ren Aoki and Daichi Kurose. “The name frightens you for a reason,” Emi says. “We do not recruit children. Adults can leave. No one is trained through torture.” Ren produces the adult roster and departure records; they match the current filings. Daichi accepts responsibility for this organisation, not credit for changing the dead: “What they did to you was wrong. We cannot ask you to call this home.” He offers to relinquish command if you choose to lead under that charter. You owe them neither membership nor forgiveness.',
  ('Review the adult roster and departures', 'Question the charter and record their answers'),
  'The current roster, departure records and staff testimony corroborate an adult-only successor with voluntary membership and no coercive child training. The original clan is gone. Rei can destroy this successor, take its leadership or leave it alone.'),
)

def data(s):
    return s.setdefault('rei_story',dict(version=1,stage=0,journal=[],choices=[],hamayashi=None,richter=False,complete=False))

def check(s,venue=None,solo=False):
    if s['player']!='rei': raise ValueError('This is Rei’s personal storyline.')
    __import__('campaign_flashbacks').require(s)
    guards.here(s,venue)
    if solo and s['world'].get('party'): raise ValueError('This is a solo mission. Leave your companions before entering Blackstone.')

def record(s,text):
    data(s)['journal'].append(dict(text=text,minute=s['world']['minute']))
    return text

def advance(s,choice=0):
    check(s); d=data(s)
    if d['stage']>=len(SCENES): raise ValueError('The investigation is ready for its two confrontations.')
    title,venue,scene,options,finding=SCENES[d['stage']]
    check(s,venue)
    if type(choice) is not int or choice not in (0,1): raise ValueError('Choose a current response.')
    if d['stage'] in (0,2) and s['world'].get('party'): raise ValueError('Take this private moment alone.')
    d['choices'].append(options[choice]); d['stage']+=1
    if d['stage']==2:
        import job_apps
        job_apps.ensure(s)['hamayashi_discovery']['return_known']=True
    return record(s,title+' — '+finding)

def choose(s,ending):
    check(s,'hamayashi_house'); d=data(s)
    if d['stage']<6 or d['hamayashi']: raise ValueError('Hear the successor’s answers first; the decision cannot be repeated.')
    if ending not in ('destroy','lead','leave'): raise ValueError('Choose destroy, lead or leave.')
    import job_apps
    jobs=job_apps.ensure(s)
    if ending=='lead' and (jobs.get('membership') or (jobs.get('gang') and jobs['gang'].get('id')!='hamayashi') or jobs.get('pending')):
        raise ValueError('Resolve your current assignment and leave conflicting affiliations before accepting leadership.')
    d['hamayashi']=ending
    if ending=='lead':
        jobs['gang']=dict(id='hamayashi',name='Hamayashi-kai',role='Leader',rank=4,standing=100)
        jobs['hamayashi_affiliated']=True
        import gang_members, gang_leaders
        gang_leaders.ensure(s); gang_members.ensure(s)
        text='Daichi relinquishes command. Rei leads the successor under its adult-only, voluntary charter. Emi and Ren remain colleagues. Leadership does not erase his childhood.'
    elif ending=='destroy':
        if (jobs.get('gang') or {}).get('id')=='hamayashi': jobs['gang']=None
        text='Rei chooses to dismantle the successor. Defeat every guard at all three locations. Until then, it remains operational.'
    else: text='Rei leaves the successor alone. Its organisation and guards remain; he owes it no further part of his life.'
    update(s)
    return record(s,text)

def update(s):
    d=data(s)
    if d['hamayashi']=='destroy' and guards.cleared(s,guards.HAMAYASHI,'rei:hamayashi'):
        d['hamayashi']='destroyed'
        if 'hamayashi' not in guards.data(s)['disabled']: guards.data(s)['disabled'].append('hamayashi')
        record(s,'All three garrisons defeated. The successor closes its operations; its guards no longer replenish. Staff survive and leave organisational duty.')
    d['complete']=d['richter'] and d['hamayashi'] in ('destroyed','lead','leave')

def fight_guards(s):
    check(s); d=data(s); venue=s['world']['location']
    if d['stage']<6: raise ValueError('Complete the investigation before launching a mission.')
    if venue in guards.HAMAYASHI:
        if d['hamayashi']!='destroy': raise ValueError('The destruction route has not been chosen.')
        return guards.begin(s,venue,'rei:hamayashi')
    if venue in guards.BLACKSTONE:
        check(s,solo=True)
        if d['richter']: raise ValueError('The Blackstone mission is resolved.')
        guards.check_trip(s,'rei',venue)
        return guards.begin(s,venue,'rei:blackstone')
    raise ValueError('Travel to a mission location.')

RICHTER_DIALOGUE = ('Richter’s sleeves part around reinforced arms; a powered spinal frame locks into place. '
    '“You think your awakening makes you exceptional. I built my own advantage.” '
    'Rei lays the copied authorisation on the desk. “They withdrew. You kept experimenting. And Marcus was a person, not a story you get to minimise.” '
    '“You cannot make me answer for all of it,” Joseph says, bringing his weapons online. Rei takes his stance. The confrontation becomes a fight.')

def confront(s):
    check(s,'blackstone_command',solo=True); d=data(s)
    if d['stage']<6 or d['richter']: raise ValueError('No unresolved Richter confrontation.')
    if not guards.cleared(s,guards.BLACKSTONE,'rei:blackstone'): raise ValueError('Defeat every Blackstone HQ guard in all five areas first.')
    p=guards.profile(s,'headhunter'); p['name']='Joseph Richter · cybernetic enhancement'
    p['portrait']='richter_cybernetic'
    __import__('combat_boss').install(p)
    record(s,RICHTER_DIALOGUE)
    return guards.start(s,'Joseph Richter',p,'rei:richter')

def resolve(s,e):
    d=data(s)
    if e['scope']=='rei:richter':
        d['richter']=True
        if 'blackstone' not in guards.data(s)['disabled']: guards.data(s)['disabled'].append('blackstone')
        record(s,'Richter’s powered frame fails. “I bullied Marcus. I chose to hurt him, and then pretended it did not matter. I am sorry. I am sorry for what I did to these people too.” Rei does not have to forgive him. He secures the research records and disables the containment controls. The programme is shut down; surviving participants can leave. Victory is not a cure for grief, and Joseph’s apology cannot undo his actions.')
    update(s)

def context(s,who,listeners):
    d=s.get('rei_story',{})
    if not d: return ''
    if who=='rei' and not set(listeners)-{'rei'}:
        return 'Private authored investigation: '+' '.join(r['text'] for r in d['journal'])
    if who=='Joseph Richter' and d.get('richter'):
        return 'Rei defeated your cybernetically enhanced form, stopped your programme and received your apology for bullying Marcus and coercive experiments. Do not undo that apology or claim the programme still operates. Do not disclose private details to bystanders.'
    if who in ('Emi Suda','Ren Aoki','Daichi Kurose'):
        return 'Saved successor outcome: '+str(d.get('hamayashi'))+'. Rei leads only if the outcome is lead. Destroyed means operations closed. Never resurrect the original clan.'
    return ''
