"""MH-005 authored chapter assembly, additive reading state and scene access.

Prose never grants evidence, travel, victories, contacts or rewards. Original
campaign handlers remain the only authority for those transitions.
"""
import copy
import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def library():
    return json.loads((Path(__file__).parent/'campaign_prose/catalog.json').read_text(encoding='utf-8'))['scenes']


def read(s):
    return s.get('campaign_prose',{}).get('players',{}).get(s.get('player'),{})


def data(s):
    root=s.setdefault('campaign_prose',{'version':1,'players':{}})
    d=root.setdefault('players',{}).setdefault(s['player'],{})
    for k,v in dict(read={},flags={},disclosures={},deferred=[],preferences={'size':15}).items():
        d.setdefault(k,copy.deepcopy(v))
    return d


def context(s, **extra):
    r=s.get('rei_story',{})
    return dict(player=s['player'],choice=0,phase='before',disclosure='private',support='quiet',direct=False,authenticated=False,
                richter=bool(r.get('richter')),ending=r.get('hamayashi'),
                last_ace=sum(bool(s.get('interpol',{}).get('files',{}).get('ace_'+suit,{}).get('complete'))
                             for suit in ('clubs','hearts','diamonds','spades'))>=3,
                **{}) | extra


MEMORY_ART = {
    'GD02':('locations/noodle_shop',{'garrett':'garrett-home','april':'april-selection'}),
    'GD21':('locations/garrett-hong-kong-school',{'garrett':'garrett-high-school','charles':'charles-young-adult'}),
    'RD09':('locations/rei-high-school',{'rei':'rei-high-school','marcus':'marcus-high-school'}),
    'RD11':('locations/rei-high-school',{'rei':'rei-high-school','emily':'emily-high-school','sophie':'sophie-high-school'}),
    'RD13':('locations/rei-high-school',{'rei':'rei-high-school','Joseph Richter':'joseph-richter-high-school'}),
    'GD04':('locations/noodle_shop',{}),'RD04':('locations/noodle_shop',{}),
    'GD15':('locations/noodle_shop',{}),'RD08':('locations/noodle_shop',{}),
    # Undated family memory: keep the neutral reading panel, without assigning
    # an unsupported age or using the adult laboratory portrait as historical art.
    'GD17':(None,{}),
    'FM01':('locations/blackhaven',{}),'FM02':('locations/blackhaven',{}),
    'FM03':('locations/blackhaven',{}),'FM04':('locations/interpol_briefing',{}),
}

# The same historical event has a separate reading record in each campaign.
# These IDs do not grant knowledge or advance the other protagonist's route.
SHARED_EVENTS = {'GD04':'GR-F01','RD04':'GR-F01','GD15':'GR-F02','RD08':'GR-F02'}


def page(text, key=None, **kwargs):
    spec=library().get(key,{})
    return dict(player='',speeches=[],narration=text,prose=True,scene_id=key,
                title=spec.get('title','A moment to consider'),chapter=spec.get('chapter','')) | kwargs


def pages(key, ctx):
    """Paragraph-preserving pages with explicit illustration/time transitions."""
    spec=library()[key]; result=[]; paragraphs=[]; words=0; mode='present'
    def flush():
        nonlocal paragraphs,words
        if paragraphs:
            background,portraits=MEMORY_ART.get(key,(None,{})) if mode=='memory' else (None,{})
            result.append(page('\n\n'.join(paragraphs),key,mode=mode,background=background,portraits=portraits))
            paragraphs=[];words=0
    for e in spec['elements']:
        if any(ctx.get(k)!=v for k,v in e.get('when',{}).items()):continue
        if 'mode' in e:
            flush();mode=e['mode']
        count=len(e['text'].split())
        if words and (words+count>170 or len(paragraphs)>=7):flush()
        paragraphs.append(e['text']);words+=count
    flush()
    if result:result[-1]['scene_end']=True
    return result


def reflection(key, prompt, options):
    return page(prompt, key, reflection=key, options=[dict(value=v,label=l,response=t) for v,l,t in options])


REFLECTIONS = {
    'GD07':('What does Garrett want to put into words?',[
        ('disappointed','Admit the disappointment','He let himself write that he had hoped for more. Disappointment did not make the copy useless; it made the next question harder to ask.'),
        ('question','Focus on the next verifiable question','He put a line beneath what the record could establish. The next question would have to begin there, even if hope had already gone farther.')]),
    'GD20':('What does Garrett hold onto before he speaks?',[
        ('relief','The need to hear his brother','Relief did not make the silence harmless. He wanted to hear Charles answer without having to hide how much he had needed it.'),
        ('anger','The right to name what hurt','He would not have to call the silence kindness. He could name what it had cost him and still be glad Charles was alive.')]),
    'GD25':('What intention can Garrett carry into tomorrow?',[
        ('time','Give trust time','An agreement was a beginning. Garrett would watch what they did with it instead of demanding that one evening repair every year.'),
        ('boundaries','Keep the boundaries clear','Love did not make every silence acceptable. He wanted their next conversation to have room for an honest no.')]),
    'RD01':('What does Rei want to keep visible?',[
        ('gaps','Leave the gaps unfilled','He would not turn an empty interval into a test he had failed. What he could read belonged in the notes; what he could not remember could stay uncertain.'),
        ('present','The drawing he chose to make','He rested a hand beside the other page. He had chosen that line himself. The present did not need permission from the timetable.')]),
    'RD20':('What does Rei need from the pause?',[
        ('evidence','Separate the name from the present evidence','The current records described people who could leave. He could hold that fact beside the harm associated with the name without making one cancel the other.'),
        ('boundary','Name a boundary before deciding','He did not owe them a place in his life. He also did not need to choose merely to prove that he was free to choose.')]),
    'RD31':('What can Rei say after the resolved confrontation?',[
        ('acknowledge','Acknowledge the apology without forgiveness','“I heard you,” Rei said. Hearing the words was all he could promise. He turned back to the people and records that needed attention.'),
        ('space','Keep space for what cannot return','Rei let the apology stand without supplying an answer that made the room easier. Marcus still had a place in his life beyond this confrontation.')]),
}


def assembled(s, keys, ctx=None, *, reflections=True):
    ctx=ctx or context(s); lines=[]
    for key in keys:
        lines.extend(pages(key,ctx))
        if reflections and key in REFLECTIONS:
            prompt,options=REFLECTIONS[key];lines.append(reflection(key,prompt,options))
    return lines


def choose_reflection(s,index):
    d=s.get('campaign_dialogue') or {};b=d.get('beats',[{}])[d.get('cursor',0)]
    if not b.get('reflection') or b.get('selected') is not None:raise ValueError('This reflection is not awaiting a choice.')
    if type(index) is not int or not 0<=index<len(b['options']):raise ValueError('Choose a displayed reflection.')
    option=b['options'][index];b['selected']=index
    d.setdefault('narrative_flags',{})[b['reflection']]=option['value']
    d['beats'].insert(d['cursor']+1,page(option['response'],b.get('scene_id')))


def finish(s,d):
    """Called after the authoritative action succeeds, once, or for social prose."""
    if not any(b.get('prose') for b in d['beats']):return
    record=data(s)
    for b in d['beats']:
        key=b.get('scene_id')
        if key:
            record['read'].setdefault(key,dict(title=b['title'],chapter=b.get('chapter',''),minute=s['world']['minute']))
            if key in SHARED_EVENTS:
                record.setdefault('shared_events',{}).setdefault(SHARED_EVENTS[key],dict(viewpoint=s['player'],scene=key,minute=s['world']['minute']))
    record['flags'].update(d.get('narrative_flags',{}))
    if d.get('social_id'):
        key=d['social_id'];ctx=d.get('prose_context',{})
        record['flags'][key+':support']=ctx.get('support','quiet')
        record['flags'][key+':disclosure']=ctx.get('disclosure','private')
        if ctx.get('disclosure')=='share':
            for who in d.get('social_cast',[]):
                topics=record['disclosures'].setdefault(who,[])
                topic=SOCIAL[key].get('topic')
                if topic and topic not in topics:topics.append(topic)
        if key in record['deferred']:record['deferred'].remove(key)


def continuity(s,key):
    flags=read(s).get('flags',{})
    if key=='GD37' and __import__('charles_quest').read(s).get('ending')=='guarded reconciliation':
        return 'Garrett had agreed to keep talking, not to pretend the silence had been fair. Charles made room for the visit without asking him to arrive already reconciled.'
    if key=='GD28' and flags.get('GD25')=='boundaries':
        return 'At home he had decided to keep the boundaries clear. Here that meant making room for someone else to tell the Dragons no.'
    if key=='GD27' and flags.get('GD20')=='anger':
        return 'He had chosen to name what hurt before entering the room. He could speak about that feeling now without giving away the private conversation.'
    if key=='RD22' and flags.get('RD20')=='boundary':
        return 'Rei had decided he needed a boundary before an answer. Garrett could ask him a question without being allowed to choose the answer for him.'
    if key=='RD33' and flags.get('RD01')=='gaps':
        return 'He had left the first gaps visible. Finishing the investigation did not require him to fill them now.'
    return ''


GARRETT_STEPS={0:['GD05'],1:['GD06'],2:['GD07'],3:['GD08'],4:['GD10'],5:['GD11'],6:['GD12'],7:['GD13'],
               8:['GD16','GD17'],9:['GD23'],10:['GD24'],11:['GD25'],12:['GD28'],13:['GD29'],14:['GD32','GD33'],
               15:['GD34'],16:['GD35','GD36'],17:['GD37','GD38'],18:['GD39'],19:['GD40']}
REI_STEPS={0:['RD01'],1:['RD05'],2:['RD15'],3:['RD16'],4:['RD17'],5:['RD19','RD20']}


def guard_prologue(s, case, index, count=3):
    settings={
        'ace_clubs':('The escort frontage','Their finding concerned who issued the order. The driver who received it was not the target.'),
        'ace_hearts':('The public-facing approach','The corrected timeline had kept the unrelated performer out of this confrontation. The team followed the independently supported deployment.'),
        'ace_diamonds':('The authorised approach','The copied records were already secured. The team did not need to gamble the evidence to reach the person who had authorised the disputed work.'),
        'ace_spades':('The handover approach','Fox had separated a transferred trace from a continuous route. He reported the limit before either of them acted on it.'),
        'crow_trail':('The courier’s screen','The authenticated transfer supported this approach. The rejected routing label supplied no reason to pursue anyone else.'),
        'crow_operation':('The command entrance','The summons matched this entrance. Knowing where the Crow was did not give the team control of the rooms beyond it.'),
    }
    title,setting=settings.get(case,('The supported route','The team checked the supported objective before approaching the opposition.'))
    kinds=('Clubs enforcer','Spades assassin','Syndicate affiliate') if case in settings else ('first guard','next guard','remaining guard')
    line=f'{setting}\n\n{index} of {count} mission posts already cleared. The {kinds[min(index,2)]} still blocked the approach.'
    line+='\n\n“Check before we move,” Gordon said.\n\n“I’m here,” Fox answered. The acknowledgment gave neither of them a reason to assume the next encounter was won.'
    return [page(line,title=title)]


def action_pages(s,action,args,preview=None):
    """Return a snapshot of eligible narrative, or None for unrelated campaigns."""
    player=s['player'];ctx=context(s,choice=args[0] if args else 0);keys=[]
    if action=='charles_quest.advance' and player=='garrett':
        import charles_quest
        step=charles_quest.read(s)['step'];keys=GARRETT_STEPS.get(step,[])
        if step in (14,16):ctx['phase']='after'
        if step==8 and args[0]==1:
            # The wrong-answer letter grants no invitation; the memory is family
            # history and its present return must reflect the failed enquiry.
            ctx['authenticated']=False
        else:ctx['authenticated']=step>=8
    elif action=='charles_quest.security_action' and player=='garrett':
        import charles_quest,organisation_guards as guards,garrett_chapters
        step=charles_quest.read(s)['step']
        if step in (14,16):
            prior=read(s).get('read',{});key='GD32' if step==14 else 'GD35'
            return assembled(s,[key],ctx) if key not in prior else [page('The threat remained unresolved. Garrett checked the remaining mission detail. The people beyond it still needed a clear exit.')]
        if step==9 and not guards.remaining(s,'glasshouse_lab','charles:search'):
            direct=any(e['title']=='Direct encounter' for e in charles_quest.read(s)['evidence'])
            ctx['direct']=direct
            keys=['GD43' if direct else 'GD20','GD22']
            if 'GD22' in read(s).get('read',{}):
                return [page('Charles still barred the way. The earlier exchange had not resolved the confrontation.\n\n“I’m still asking you to listen,” Garrett said. Charles raised his hands again. Reconciliation still required a real victory.')]
        else:return None
    elif action=='charles_quest.check_in' and player=='garrett':
        return [page((preview or {}).get('charles_quest',{}).get('checkins',[{'text':'A private family note is waiting.'}])[-1]['text'],title='A private family note')]
    elif action=='rei_story.advance' and player=='rei':keys=REI_STEPS.get(s.get('rei_story',{}).get('stage',0),[])
    elif action=='rei_story.choose' and player=='rei':
        keys=[{'lead':'RD23','leave':'RD24','destroy':'RD25'}[args[0]]]
        if args[0]!='destroy':keys+=['RD26']
    elif action=='rei_story.confront' and player=='rei':
        if 'RD30' in read(s).get('read',{}):return [page('The executive objective remained unresolved. Rei checked what he could do now, without pretending the previous attempt had supplied an apology or stopped the programme.')]
        keys=['RD30']
    elif action=='rei_story.fight_guards' and player=='rei':
        import organisation_guards as guards
        if s['world']['location'] in guards.BLACKSTONE:
            if 'RD29' not in read(s).get('read',{}):keys=['RD29']
            else:return [page('Rei checked the next actual guard post. The cleared positions remained cleared; wanting the next door open did not supply the strength to open it.')]
        else:return [page('The successor still had active posts. Rei faced the people defending this one. His decision had not made the remaining battles or their consequences disappear.')]
    elif action=='interpol.advance' and player in ('fox','gordon'):
        import interpol,organisation_guards as guards
        active=interpol.read(s)['active'];key=active['key'];step=interpol.objective(s)
        ctx['operation']=key
        if active.get('repeatable'):
            return assembled(s,['FD38'],ctx) if key.startswith('syndicate_') else None
        index=interpol.read(s)['files'][key]['step']
        if step['kind']=='combat':
            scope=f'interpol:{key}:{index}'
            count=3 if interpol.CASES[key]['faction'] in ('syndicate','shinokami') else 2
            won=guards.data(s)['victories'].get(scope,[])
            cleared=sum(f'{scope}:{i}' in won for i in range(count))
            if cleared<count:return guard_prologue(s,key,cleared,count)
            spec={'blackhaven':'FD05','rail':None,'shinokami':None,'ace_clubs':'FD14','ace_hearts':'FD17',
                  'ace_diamonds':'FD20','ace_spades':'FD23','crow_trail':'FD26','crow_operation':'FD30'}[key]
            if spec and spec in read(s).get('read',{}):return [page('The earlier attempt remained in the record. Their partner was here, the evidence retained, and the target unresolved. They checked the approach again without repeating a promise of success.')]
            if spec:keys=[spec]
            else:return [page('The field team had reached the supported target. The records were already secured; this encounter would determine whether they could complete the interception.')]
        elif key=='crow_operation' and step['kind']=='close':keys=['FD37']
        else:
            mapping={
                'blackhaven':{0:['FD01','FD02','FM01','FD03'],1:['FD04'],3:['FD05','FD06','FM02']},
                'rail':{0:[],1:['FD07','FD08'],3:['FD09']},
                'shinokami':{0:['FD10'],1:['FD10','FD11','FM03'],3:['FD12']},
                'ace_clubs':{0:[],1:['FD13'],3:['FD15']},
                'ace_hearts':{0:[],1:['FD16'],3:['FD18']},
                'ace_diamonds':{0:[],1:['FD19'],3:['FD21']},
                'ace_spades':{0:[],1:['FD22'],3:['FD24']},
                'crow_trail':{0:['FD25'],1:[],3:['FD26','FD27']},
                'crow_operation':{0:['FD28','FM04'],1:['FD29'],3:['FD30','FD31'],4:['FD32','FD33'],5:['FD34'],6:['FD35','FD36']}}
            keys=mapping[key].get(index,[])
            if index==3:ctx['phase']='after'
            if key=='shinokami' and index in (0,1):ctx['phase']='interview' if index==0 else 'after'
            if not keys:
                return [page('The team checked the original record at the current objective.\n\n'+step['finding']+'\n\nThe document supplied a starting point for comparison. It did not make a familiar name or a plausible story into an established identity.',title=step['title'])]
    else:return None
    lines=assembled(s,keys,ctx)
    if action=='charles_quest.advance' and __import__('charles_quest').read(s)['step']==0:
        lines.insert(0,page('The Golden Dragon had a working day to get through. April knew the unanswered-call habit; Rei knew when a late meal meant Garrett wanted someone to stay. Neither friendship could supply a missing brother. They were part of the life Garrett still had while he looked.\n\nToday he had one small thing to check. Mei’s dispatch photo was waiting on the counter. Familiar handwriting had caught his eye; hope had reached it before he could decide what it meant.','GD05'))
    if action=='rei_story.advance' and s.get('rei_story',{}).get('stage',0)==0:
        lines.insert(0,page('Rei had kept this book for years. Today he chose to open it. Yuriko had memories of her own; Garrett knew some of the broad history Rei had trusted him with. Neither could complete the gaps for him. He could ask for company later, or keep the page private. For now, he wanted to know what was actually there.','RD01'))
    for key in keys:
        text=continuity(s,key)
        if text:lines.insert(0,page(text,key))
    if action=='charles_quest.advance' and args and 5<=__import__('charles_quest').read(s)['step']<=8 and args[0]==1:
        lines.append(page('The enquiry has not advanced. The contact needs until the next story day before another response. The records and earned victories remain available.',title='An unresolved enquiry'))
    if action=='interpol.advance' and player in ('fox','gordon'):
        hypothesis=hypothesis_for(s)
        if hypothesis and hypothesis['id'] not in read(s).get('flags',{}):
            lines.insert(0,reflection(hypothesis['id'],'Which part of the lead should they check first?',[
                ('original','Begin with the original record','They began with the provenance, then compared the physical observation. Neither check could substitute for the other.'),
                ('observation','Begin with the observation','They began with what had actually been observed, then tested it against the original record. Both checks belonged in the account.')]))
        if step['kind']=='combat' and keys and keys[0] in ('FD14','FD17','FD20','FD23','FD30'):
            lines.insert(0,reflection(keys[0]+':approach','How should the team open this confrontation?',[
                ('finding','State the corroborated finding','Gordon stated what the evidence established. Fox kept his question to the part still unanswered.'),
                ('request','Focus on the immediate request','Fox kept the request concrete. Gordon would not let a dispute about their motives erase the supported operation.')]))
        if step.get('scripted_outcome')=='crow_defeat':
            lines.append(page('STORY CONFRONTATION\n\nThe Crow will defeat the team. Your combat actions play out, but survival and withdrawal carry this campaign forward after at most four exchanges. This encounter does not offer a capture outcome.',title='Before Night Ledger combat'))
    return lines or None


def memory_pages(s,key):
    mapping={'garrett-april-silence':'GD02','garrett-school-brother':'GD21',
             'rei-school-friends':'RD09','rei-school-news':'RD11','rei-school-suspension':'RD13'}
    ident=mapping[key];lines=assembled(s,[ident])
    triggers={
        'GD02':'Garrett reached toward his phone, then stopped. The ordinary shop around him made the remembered silence no less clear. He let himself remember the night April had stayed.',
        'GD21':'The laboratory door was in front of him now. Garrett paused at the thought of being told to go home for his own good. Another doorway, and the older brother beside it, returned to him.'}
    if ident in triggers:lines.insert(0,page(triggers[ident],ident))
    if key.startswith('rei-school'):
        lines.append(reflection(ident+':return','Back in the present, what does Rei do with the page?',[
            ('pause','Put it down and take a moment','Rei put the page down. He noticed the table beneath his hands and the room around it. The memory could remain true without filling every moment of the present.'),
            ('keep','Keep it open, without asking for more','He left the page where he could see it. He did not ask the memory to answer another question before he was ready.')]))
    return lines


# Optional visits retain their own availability window, never gate a main clue.
# They can be deferred; historical recollections never summon a live actor.
SOCIAL = {}
def social(key,player,minimum,maximum,venue,cast,keys=None,topic=None):
    SOCIAL[key]=dict(player=player,minimum=minimum,maximum=maximum,venue=venue,cast=cast,keys=keys or [key],topic=topic)

social('GD01','garrett',0,2,'noodle_shop',['april'])
social('GD03','garrett',0,8,'noodle_shop',['rei'],['GD03','GD04'])
social('GD09','garrett',3,8,'noodle_shop',['april'])
social('GD14','garrett',7,8,'noodle_shop',['rei'],['GD14','GD15'])
social('GD18','garrett',9,9,'noodle_shop',['april'],topic='private meeting planned')
social('GD19','garrett',9,9,'noodle_shop',['rei'])
social('GD26','garrett',12,20,'noodle_shop',['april'],topic='Charles is alive')
social('GD27','garrett',12,20,'noodle_shop',['rei'],topic='Charles is alive')
social('GD30','garrett',13,18,'noodle_shop',['rei'])
social('GD31','garrett',14,14,'syndicate',['Mina Cho','Anton Bellamy'])
social('GD41','garrett',20,20,'noodle_shop',['rei'])
social('GD42','garrett',20,20,'noodle_shop',[])  # one verified available visitor
social('RD02','rei',1,6,'rei_home',['yuriko'],topic='childhood timetable')
social('RD03','rei',1,6,'noodle_shop',['garrett'],['RD03','RD04'])
social('RD06','rei',2,6,'rei_home',['yuriko'],topic='training ledger')
social('RD07','rei',2,6,'square',['emily'])
social('RD08','rei',2,6,'noodle_shop',['garrett'])
social('RD10','rei',2,6,'square',['emily','sophie'])
social('RD12','rei',2,6,'park',['sophie'])
social('RD14','rei',2,6,'noodle_shop',['garrett'])
social('RD18','rei',4,6,'rei_home',['yuriko'])
social('RD21','rei',6,6,'square',[],topic='successor decision')
social('RD22','rei',6,6,'noodle_shop',['garrett'],topic='successor decision')
social('RD27','rei',6,6,'square',[],topic='solo mission planned')
social('RD28','rei',6,6,'noodle_shop',['garrett'])
social('RD32','rei',6,6,'park',['sophie'],topic='Blackstone outcome')
social('RD33','rei',6,6,'rei_home',[])
social('RD34','rei',6,6,'noodle_shop',['garrett'])
social('RD35','rei',6,6,'rei_home',[])


def present(s,who):
    # Mei is an authored story visitor, not a roaming/contact-enabled cast member.
    # No surname or new private biography is invented for the existing supplier.
    if who=='Mei':return s['player']=='garrett' and s['world']['location']=='noodle_shop' and 11*60<=s['world']['minute']%1440<17*60
    if who in s.get('combat',{}).get('ruptures',[]):return False
    if __import__('combat').recovering(s,who):return False
    if who in s['world']['cast']:
        actor=s['world']['cast'][who]
        if actor.get('location')!=s['world']['location'] or actor.get('journey') or actor.get('activity')=='Sleep':return False
        if not __import__('hidden_cast').known(s,who):return False
        bond=s.get('friendships',{}).get(who,{})
        if bond.get('trust',50)<20:return False
        return True
    return who in s['world'].get('npcs',[])


def stage(s):
    if s['player']=='garrett':return __import__('charles_quest').read(s)['step']
    return s.get('rei_story',{}).get('stage',0)


def eligible(s,key):
    spec=SOCIAL[key]
    if s['player']!=spec['player'] or not spec['minimum']<=stage(s)<=spec['maximum']:return False
    r=s.get('rei_story',{})
    if key in ('RD21','RD22') and r.get('hamayashi'):return False
    if key in ('RD27','RD28') and r.get('richter'):return False
    if key=='RD10' and 'rei-school-friends' not in s.get('campaign_flashbacks',{}).get('completed',[]):return False
    if key in ('RD12','RD14') and 'rei-school-news' not in s.get('campaign_flashbacks',{}).get('completed',[]):return False
    if key=='RD32' and not (r.get('richter') or any(h['scope'].startswith('rei:blackstone') or h['scope']=='rei:richter' for h in s.get('organisation_guards',{}).get('history',[]))):return False
    if key in ('RD33','RD34','RD35') and not r.get('complete'):return False
    return True


def scene_cast(s,key):
    if key in ('RD21','RD27'):
        people=[who for who in ('emily','sophie') if present(s,who)]
        return people[:1] if key=='RD21' else people
    if key=='RD35':return [who for who in ('yuriko','emily','sophie') if present(s,who)]
    if key=='GD42':return [who for who in ('april','Mei') if present(s,who)][:1]
    return SOCIAL[key]['cast'][:]


def unavailable(s,key):
    spec=SOCIAL[key]
    if not eligible(s,key):return 'This conversation does not belong to the current chapter.'
    if s['world']['location']!=spec['venue']:return 'Meet in person at '+__import__('town').location_name(s,spec['venue'])+'.'
    cast=scene_cast(s,key)
    if not cast and key not in ('RD33','RD35'):return 'The friend is not available here. You can return later.'
    missing=[who for who in cast if not present(s,who)]
    if missing:return 'Waiting for '+', '.join(missing)+' to be available here.'
    if key in ('RD33',) and s['world'].get('party'):return 'Take this private moment alone.'
    return ''


def begin_social(s,key,disclosure='private',support='quiet'):
    import campaign_dialogue,combat
    if key not in SOCIAL or disclosure not in ('private','share') or support not in ('quiet','help'):raise ValueError('Choose an available conversation.')
    combat.guard(s)
    if s.get('campaign_dialogue'):raise ValueError('Finish the current scene before starting another conversation.')
    reason=unavailable(s,key)
    if reason:raise ValueError(reason)
    spec=SOCIAL[key];cast=scene_cast(s,key)
    if spec.get('topic') and disclosure=='share':
        listeners=[who for who in s['world'].get('party',[]) if who not in cast]
        listeners += [who for who in s['world'].get('npcs',[]) if who not in cast and not who.startswith('Post guard')]
        # Authored public conversations use lowered voices; an attached party is
        # an actual listening group, so disclosure must wait until it is private.
        if any(who in s['world'].get('party',[]) for who in listeners):raise ValueError('Leave other companions before sharing this private subject.')
    ctx=context(s,disclosure=disclosure,support=support,visitor=(cast[0] if cast else ''))
    if key=='GD42' and cast and cast[0]=='Mei':ctx['visitor']='mei'
    lines=assembled(s,spec['keys'],ctx)
    text=continuity(s,key)
    if text:lines.insert(0,page(text,key))
    # Reconcile choices made in earlier meetings, rather than assuming promises.
    if key=='GD26' and read(s).get('flags',{}).get('GD18:support')!='help':
        lines[0]['narration']=lines[0]['narration'].replace('“If we agreed to talk, I should probably turn up.”','“I wanted to see you.”').replace('“If we agreed,” she corrected gently. “Don\'t borrow a promise you didn\'t make.”','“I’m glad,” April said.')
    if key in ('RD22','RD28') and disclosure=='private':
        lines=[page('Rei kept the details to himself.\n\n“I can’t give you the whole account,” he said.\n\n“Then don’t,” Garrett answered. “I can offer you a seat without asking for the file.”\n\nRei accepted the company. His decision and his next steps remained his own.',key)]
    if key=='RD27':lines=pre_mission_visit(s,cast,ctx)
    if key=='RD35' and len(cast)<3:lines=ending_visit(s,cast)
    campaign_dialogue.epilogue(s,lines)
    d=s['campaign_dialogue'];d.update(social_id=key,social_cast=cast,prose_context=ctx,title=library()[key]['title'])


def pre_mission_visit(s,cast,ctx):
    if len(cast)==2:return assembled(s,['RD27'],ctx)
    if cast==['emily']:
        text='“Do you want me to ask you not to go?” Emily asked.\n\n“I don’t know.”\n\n“I don’t know whether it would help either. I don’t want to say something brave just because you’re about to leave.”\n\nRei looked at her hands, then back at her face. “I’m going alone. I don’t know how long it will take.”\n\n“Then don’t promise me a time. I’d like to see you afterward. Not for a report.”\n\n“I might not be good company.”\n\n“You can let me decide whether I want the company.”\n\nHe smiled a little. “I can tell you when I’m able.”\n\n“That would help.” She paused. “Please be careful.”\n\n“I’ll pay attention,” he said. It was the promise he could make.'
    else:
        text='“What can you actually tell me?” Sophie asked.\n\n“That I’m going alone. That I don’t know how long it will take.”\n\n“Then don’t give me a time you made up.”\n\nRei nodded. He had been about to give her something reassuring because he wanted to stop seeing the worry.\n\n“I’d like an ordinary evening after this,” Sophie said. “Let me know when you’re able.”\n\n“Even if I’m not good company?”\n\n“We have survived quiet evenings before.”\n\n“That sounds like an accusation.”\n\n“Only if you need it to.”\n\nHe laughed briefly. They agreed only to a check-in when he could manage one. She would not follow him into the operation.'
    return [page(text,'RD27')]


def ending_visit(s,cast):
    if not cast:return [page('Rei set out a fresh page at home. Another afternoon could hold company; this one could be quiet without becoming a verdict on his recovery. He moved the old pages safely aside and began something he had chosen.','RD35')]
    lines=[page('The gathering was smaller than it might be another day. Rei made room for the people who were actually here. Nobody needed to supply an account of an investigation to earn a place at the table.','RD35')]
    for who in cast:
        text={
            'yuriko':'Yuriko turned a new page toward him. “You can disagree with the ending.”\n\n“I might.”\n\n“I know. That’s why I asked.”\n\nHe read slowly enough to answer the work she had actually made.',
            'emily':'Emily wanted to keep a colour Rei thought too loud. “It’s allowed to be noticeable,” she said.\n\n“So is the rest of it.”\n\nThey moved the pieces and compared them again. He found himself interested in the disagreement.',
            'sophie':'Sophie moved a cup clear of the fresh page. “You could leave some space.”\n\n“For what?”\n\n“Something you haven’t decided yet.”\n\nRei looked at it, then stopped trying to finish the arrangement before the afternoon had begun.'}[who]
        lines.append(page(text,'RD35'))
    return lines


def defer(s,key):
    if key not in SOCIAL or not eligible(s,key):raise ValueError('This conversation is not offered now.')
    d=data(s)
    if key not in d['deferred']:d['deferred'].append(key)
    return 'Conversation deferred. Your choice carries no relationship penalty; return while this chapter’s conversation is available.'


def offers(s):
    return [key for key in SOCIAL if eligible(s,key) and key not in read(s).get('read',{})]


def recap(s):
    lines=[]
    if s['player']=='garrett':
        q=__import__('charles_quest').read(s)
        lines=[r['title']+' — '+r['finding'] for r in q.get('evidence',[])]
    elif s['player']=='rei':lines=[r['text'] for r in s.get('rei_story',{}).get('journal',[])]
    elif s['player'] in ('fox','gordon'):
        for f in s.get('interpol',{}).get('files',{}).values():lines += [e['title']+' — '+e['finding'] for e in f.get('evidence',[])]
    if not lines:lines=['Your story is beginning. No investigative findings have been recorded yet.']
    flags=read(s).get('flags',{})
    reflections=[f'{library().get(k,{}).get("title",k)}: {v.replace("_"," ")}' for k,v in flags.items() if k in REFLECTIONS]
    if reflections:lines+=['Remembered reflections\n'+'\n'.join(reflections)]
    return lines


def knowledge(s,who,listeners):
    if not s:return ''
    player=s.get('player');d=read(s)
    if who==player:
        # A prompt in company cannot expose private internal narrative flags.
        if set(listeners)-{player}:return ''
        return 'Saved personal reflection choices (not new evidence): '+str(d.get('flags',{}))
    topics=d.get('disclosures',{}).get(who,[])
    if not topics or set(listeners)-{player,who}:return ''
    return ('This protagonist explicitly shared these subjects with you in completed in-person scenes: '+', '.join(topics)+
            '. Remember the subject without inventing further details. Charles being alive grants no location, cover, motive or number. '
            'A successor decision discussion grants no clan name or escape details. Keep disclosures private from other listeners.')


# Authored discriminating checks, separate from the original case findings.
HYPOTHESES = {
 'blackhaven':dict(id='FL01',step=1,title='The cleaner on the envelope',claim='The common chemical trace identifies the source of the demands.',checks=['A consenting worker identifies the cleaner used by several premises; a labelled container and routine supply record corroborate it.','Matching fibres and the physically observed collection route distinguish the supported route.'],conclusion='The scent is real but too common to identify a source. The fibres and observed route support the collection-point finding.'),
 'rail':dict(id='FL02',step=1,title='The number used twice',claim='The matching number alone identifies the linked shipment.',checks=['The full ledger heading establishes its period; the worker explains the normal numbering cycle.','The seal, receipt date and dated handover match the supported consignment, not the other period.'],conclusion='The tempting entry belongs to a different period. The unrelated shipment is excluded from this enquiry.'),
 'shinokami':dict(id='FL03',step=1,title='The date the contractor cannot supply',claim='The uncertain chronology proves the contractor is concealing a larger role.',checks=['The referral distinguishes processing date from physical visit.','The independently dated delivery manifest and exterior observation corroborate the supported part of the account.'],conclusion='The dates describe different events. The corroborated account stands; remaining memory gaps stay unresolved.'),
 'ace_clubs':dict(id='FL04',step=1,title='The driver everyone saw',claim='The substitute driver authored the escort order.',checks=['The willing driver distinguishes received instructions from decisions they made.','Receiving initials, the signed original, duty record and witnessed deployment distinguish delivery from authorisation.'],conclusion='Acknowledging the packet does not establish authorship. The original authorisation and independently witnessed operation establish the command link.'),
 'ace_hearts':dict(id='FL05',step=1,title='The face in the rumour',claim='The similarly dressed performer was the masked operative.',checks=['The witness separates observation from later retelling.','The original rehearsal schedule, voluntarily supplied dated call sheet and witnessed deployment cannot put that performer at the event.'],conclusion='The rumour’s attribution fails the timing check. Independent instruction and observation support the actual operative, with no proof of who started the rumour.'),
 'ace_diamonds':dict(id='FL06',step=1,title='The payment that explains too much',claim='A genuine routine invoice explains the whole disputed authorisation.',checks=['The accounts worker describes the process without claiming knowledge of a conspiracy.','Original transaction, service period, recipient, amount and approval authority distinguish the two authorisations.'],conclusion='The routine payment is genuine but does not explain the separate disputed instruction. The independent originals establish the relevant decision-maker.'),
 'ace_spades':dict(id='FL07',step=1,title='A trail with more than one owner',claim='The transferred trace proves one person’s continuous route.',checks=['A willing observer and dated service record establish that a shared handling trolley moved between the locations.','Independent handover timing and the witnessed operational encounter are compared with the accessible surfaces.'],conclusion='The trace can transfer with the trolley. It cannot establish a continuous personal route or a civil identity.'),
 'crow_trail':dict(id='FL08',step=0,title='A name that fits the story',claim='The index annotation identifies the command contact or the Crow.',checks=['The custodian explains the original index field and its issue date.','The annotation is tested against the authentication pattern in all four recovered command records.'],conclusion='The note is a local routing label in the wrong time window. It identifies neither the contact nor the Crow; the authenticated transfer remains the supported lead.'),
}


def hypothesis_for(s):
    a=s.get('interpol',{}).get('active') or {}
    h=HYPOTHESES.get(a.get('key'))
    if not h or a.get('repeatable'):return None
    f=s['interpol']['files'].get(a['key'],{})
    return h if f.get('step')==h['step'] else None


def record_hypothesis(s,key,index):
    h=HYPOTHESES.get(key)
    if not h or index!=h['step']:return
    target=s['interpol']['files'][key].setdefault('hypotheses',{})
    target.setdefault(h['id'],copy.deepcopy(h)|dict(status='tested; inference rejected',minute=s['world']['minute']))


def after_guard(s,e,won):
    """Result-sensitive narrative, called only by an authenticated guard result."""
    import campaign_dialogue
    scope=e['scope'];keys=[];ctx=context(s,phase='after' if won else 'failure')
    if scope=='rei:richter':keys=['RD31']
    elif scope=='rei:hamayashi' and won and s.get('rei_story',{}).get('hamayashi')=='destroyed':keys=['RD25','RD26']
    elif scope.startswith('rei:') and not won:
        lines=[page('The mission remained unresolved. Rei kept the evidence already secured. Resting and reassessing would not undo it; neither would pretending this attempt had finished the work.')]
        s.setdefault('campaign_epilogues',[]).append(dict(lines=lines,venue=s['world']['location']));return True
    else:return False
    lines=assembled(s,keys,ctx,reflections=won)
    s.setdefault('campaign_epilogues',[]).append(dict(lines=lines,venue=s['world']['location']))
    return True


def resolved_reaction(s,f):
    """Sparse dialogue from resolved exchanges; no predictions or new effects."""
    if s.get('player') not in ('fox','gordon') or f.get('kind')!='interpol':return
    if f.get('player',{}).get('health',0)<=0 or f.get('enemy',{}).get('health',0)<=0 or f.get('ally_resources',{}).get('health',0)<=0:return
    history=f.get('exchanges') or []
    if not history:return
    # The normal combat log remains authoritative; only observable results are
    # interpreted, and each exchange can produce at most one authored response.
    marker=len(history)
    if f.get('prose_reaction_exchange')==marker:return
    f['prose_reaction_exchange']=marker
    event=history[-1]
    line=''
    player=next((r for r in event['records'] if r['side']=='player'),{})
    enemy=next((r for r in event['records'] if r['side']=='enemy'),{})
    target=f.get('opponent')
    if target=='camila' and marker>=2 and player.get('outcome')=='countered' and any(
            r.get('side')=='player' and r.get('move_id')==player.get('move_id') for r in history[-2]['records']):
        line='Camila: “You have offered me that twice.” Gordon: “Reassess.” Fox: “I heard her.”'
    elif target=='elias' and enemy.get('outcome') in ('countered','interrupted'):
        line='Elias: “Again, then.” Fox noticed the shorter answer. Gordon kept his attention on the encounter.'
    elif target=='mavis' and player.get('outcome')=='missed':
        line='Fox: “No clean result.” Gordon: “Keep the limit in the account.”'
    elif player.get('outcome')=='countered':
        line='Fox: “That held.” Gordon: “Then reassess before the next action.”'
    elif target=='crow' and player.get('damage',0)>0:
        line='Fox: “That reached him.” Gordon: “It has not secured the objective.”'
    elif target=='crow' and marker==1:
        line='Gordon: “Keep the route in mind.” Fox: “I am.”'
    if line:f.setdefault('log',[]).append(line)


def after_interpol(s,f,key,repeatable):
    """Only authenticated operation resolution calls this; never a preview."""
    if s.get('player') not in ('fox','gordon'):return
    won=f.get('result','').startswith('Victory')
    if not won:
        lines=[page('“The objective’s still open,” Fox said.\n\n“Yes,” Gordon answered. “We keep what we established and reassess the attempt.”\n\nNeither treated a failed interception as a reason to invent a different record. The team would have to recover and regroup before returning.',title='An unresolved operation')]
    elif repeatable and key.startswith('syndicate_'):
        lines=assembled(s,['FD38'],context(s,operation=key,phase='after'))
    else:
        lines=[]
        who=f.get('opponent');actor=s['world']['cast'].get(who,{})
        if f.get('enemy',{}).get('health',0)>0 and actor.get('location')==s['world']['location']:
            answers={'martos':'“You got through this position,” Martos said.\n\n“This operation,” Gordon answered. “That is what the report will say.”',
                     'elias':'“You will make this very simple in your report,” Elias said.\n\n“Clear,” Gordon answered. “There is a difference.”\n\n“The instruction stays in it,” Fox said.',
                     'camila':'“You won this encounter,” Camila said. “Be precise about what you expect that to buy.”\n\n“We secured the material attached to this operation,” Gordon answered.',
                     'mavis':'“You have the handover,” Mavis said.\n\n“And the operational record,” Gordon answered.\n\n“Then stop adding things.”'}
            if who in answers:lines=[page(answers[who],title='After the encounter')]
    if lines:s.setdefault('campaign_epilogues',[]).append(dict(lines=lines,venue=s['world']['location']))
