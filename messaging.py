"""Durable per-conversation delivery queues, with one non-blocking AI worker."""
import copy
import json
import queue
import threading
import time


def profile(s,who):
    import autonomy
    if who in s['world']['cast']: return autonomy.person(s,who)
    return ensure(s).setdefault('local_needs',{}).setdefault(who,dict(energy=75.,social=75.,happiness=60.,unanswered=0))


def activity(s,who):
    import autonomy
    if who in s['world']['cast']: return autonomy.status(s,who)
    # Legacy town contacts have no spatial actor; keep their phone usable with
    # a conservative ordinary work/sleep routine rather than inventing travel.
    hour=s['world']['minute']%1440/60
    return 'Asleep' if hour<8 or hour>=23 else 'At work / studying' if 9<=hour<17 else 'Free time'


def affinity(s, who):
    """Current relationship drives attention; authored affinity is not consent."""
    bond=s.get('relationships',{}).get(who,s.get('friendships',{}).get(who,s.get('npc_chats',{}).get(who,{}).get('connection',{})))
    score=.5*bond.get('closeness',0)+.3*bond.get('trust',0)+.2*bond.get('attraction',0)
    strained=bond.get('unresolved_harm') or bond.get('status') in ('strained','hostile coworkers')
    if (who,s['player'])==('emily','rei') and not strained: score=max(score,90)
    return max(0,min(100,score*.35 if strained else score))


def timing(s,who,burst=False):
    """Game-minute delays, measured from delivery/read rather than clock modulo."""
    import autonomy
    interest=affinity(s,who); needs=profile(s,who); state=activity(s,who)
    base=0 if interest>=75 else 2 if interest>=45 else 5
    busy=({'At work / studying':4,'Socialising':2,'Winding down':1}.get(state,0))
    drain=1 if needs['social']<20 or needs['energy']<20 else 0
    notice=base+round(busy*(1.6-interest/100))+drain
    compose=0 if interest>=75 else 1 if interest>=45 else 2
    # Sometimes the phone is already in hand, even for a newer acquaintance.
    sent=ensure(s)['threads'].get('route:'+who,{}).get('last_sent')
    if state in ('At home','Free time') and not drain and autonomy.chance(who,s['player'],sent,'phone-in-hand')<.2+interest/250:
        notice=compose=0
    if burst:
        notice=max(busy,notice//3); compose=0
    return notice,compose


def followup_spacing(s, who):
    """Match the Friends/Close friends thresholds used by contact profiles."""
    bond = s.get('relationships', {}).get(who) or s.get('friendships', {}).get(who) or s.get('npc_chats', {}).get(who, {}).get('connection', {})
    trust, close = bond.get('trust', 0), bond.get('closeness', 0)
    if trust >= 70 and close >= 55: return 1
    if trust >= 50 and close >= 25: return 2
    return 4


def followup_delay(s,who):
    import autonomy
    p=profile(s,who)
    base = round(25+(100-affinity(s,who))*2+(100-p['social'])*.3+autonomy.chance(who,'followup')*15)
    return base * followup_spacing(s, who)


def ensure(s):
    if 'messaging' not in s:
        s['messaging']=dict(version=1,serial=0,threads={})
        for who,route in s['routes'].items():
            if route.get('channel')=='text' and route.get('dialogue'):
                t=thread(s,who)
                t['last_reply']=route.get('awaiting_since')
                t['followups']=1 if route.get('followup_sent') else 0
    d=s['messaging']
    if d.get('version',1)<2:
        for t in d['threads'].values():
            # Legacy due was moved forward by every new bubble. Pending messages
            # now carry independent clocks, including already-read messages.
            t['due']=min([m['minute'] for m in t['pending']],default=t['due'])
        d['version']=2
    return d


def thread(s, key, group=False):
    return ensure(s)['threads'].setdefault(('group:' if group else 'route:')+key,
        dict(key=key, group=group, pending=[], reason=None, due=s['world']['minute'],
             error=None, revision=0, last_sent=None, last_reply=None, followups=0, muted_until=0))


def members(s,t):
    return s['groups'][t['key']]['members'] if t['group'] else [t['key']]


def chat(s,t):
    return s['groups'][t['key']] if t['group'] else s['routes'][t['key']]


def mark_inbox_activity(s, conversation):
    data = ensure(s)
    data['inbox_serial'] = data.get('inbox_serial', 0) + 1
    conversation['inbox_activity'] = dict(minute=s['world']['minute'], order=data['inbox_serial'])


def send(s,key,text,group=False,photo_id=None):
    import game_core as core
    import groups
    import autonomy
    attachment = None
    if photo_id is not None:
        import camera
        from PIL import Image
        record = next((r for r in camera.photos(s) if r['id'] == photo_id), None)
        if record is None: raise ValueError('Choose a photo from this story’s Gallery.')
        try:
            with Image.open(camera.photo_path(record)) as image: image.verify()
        except (OSError, ValueError): raise ValueError('This photo is no longer available.')
        attachment = copy.deepcopy(record)
        description = record.get('mode', 'Photo') + ' · ' + record.get('location', '')
        text = (text.strip() + '\n' if text.strip() else '') + '[Photo: ' + description.strip(' ·') + ']'
    if not text.strip(): raise ValueError('Write a message or choose a photo first.')
    t=thread(s,key,group)
    if group and 'charles' in members(s,t): raise ValueError('Charles accepts direct texts only.')
    groups.require_text_available(s,members(s,t))
    now=s['world']['minute']; d=ensure(s); d['serial']+=1
    entry=dict(id=d['serial'],text=text.strip(),minute=now,read_by=[],answered_by=[])
    t['pending'].append(entry); t['revision']+=1; t['error']=None
    t['last_sent']=now; t['followups']=0
    if t['reason'] and t['reason'].get('kind')=='silence':
        t['reason']=None
    if group:
        line=dict(speaker=core.PLAYERS[s['player']]+' (You)',text=text.strip(),minute=now,receipt='Delivered',message_id=entry['id'])
    else:
        line=dict(role='user',content=text.strip(),minute=now,channel='text',receipt='Delivered',message_id=entry['id'])
    if attachment is not None:
        line['photo'] = attachment
        entry['photo'] = copy.deepcopy(attachment)
    chat(s,t)['history'].append(line)
    mark_inbox_activity(s, chat(s,t))
    needs=autonomy.person(s,s['player'])
    needs['social']=max(0,needs['social']-.25)
    for who in members(s,t): profile(s,who)['unanswered']=0
    # Sending is immediate. Time advances through explicit waits and other activities,
    # allowing a genuine burst and simultaneous messages across conversations.
    t['due']=min(t['due'],now)
    for who in members(s,t):
        waiting=[m for m in t['pending'] if who not in m['answered_by']]
        notice,compose=timing(s,who,len(waiting)>1)
        for message in waiting:
            schedules=message.setdefault('notice_at',{})
            schedules[who]=min(schedules.get(who,message['minute']+notice),now+notice)
            if who in message['read_by']:
                ready=message.setdefault('ready_at',{})
                ready[who]=min(ready.get(who,message.get('read_at',{}).get(who,now)+compose),now+compose)
    chat(s,t).update(choices=[],suggestions_deferred=True)
    tick(s)
    return entry


def initiate(s,who,reason,offer=None):
    t=thread(s,who)
    if t['reason'] or t['pending']: return
    t['reason']=dict(text=reason,offer=offer)
    t['due']=s['world']['minute']+timing(s,who)[0]
    t['revision']+=1


def available(s,who):
    import combat
    if combat.recovering(s,who) or combat.recovering(s) or combat.active(s): return False
    if who == 'charles' and not __import__('charles_han').number_allowed(s): return False
    import autonomy
    import groups
    if who in groups.hanging_out_with(s): return False
    state=activity(s,who)
    if state in ('Asleep','Travelling'): return False
    return True


def tick(s):
    import autonomy
    import hidden_cast
    now=s['world']['minute']
    for t in list(ensure(s)['threads'].values()):
        if not t['pending'] and now<t['due']: continue
        for who in members(s,t):
            if not available(s,who): continue
            if t['reason'] and now>=max(t['due'],t['muted_until']):
                t['reason'].setdefault('eligible_at',{}).setdefault(who,now)
            waiting=[m for m in t['pending'] if who not in m['answered_by']]
            notice,compose=timing(s,who,len(waiting)>1)
            for message in t['pending']:
                if who in message['answered_by']: continue
                if who not in message['read_by']:
                    schedule=message.setdefault('notice_at',{})
                    due=schedule[who]=min(schedule.get(who,message['minute']+notice),message['minute']+notice)
                    if now<due: continue
                    message['read_by'].append(who)
                    message.setdefault('read_at',{})[who]=now
                    import memory_store
                    memory_store.utterance(s, 'delivered:'+str(message['id'])+':'+who, message['text'], s['player'], [s['player'],who], now)
                message.setdefault('ready_at',{}).setdefault(who,message.get('read_at',{}).get(who,now)+compose)
                if now>=message['ready_at'][who] and now>=t['muted_until']:
                    message.setdefault('eligible_at',{}).setdefault(who,now)
            for line in chat(s,t)['history']:
                message=next((m for m in t['pending'] if m['id']==line.get('message_id')),None)
                if message and message['read_by']:
                    line['receipt']='Read' if len(message['read_by'])==len(members(s,t)) else 'Read by '+', '.join(w.title() for w in message['read_by'])
        if t['pending'] or t['reason'] or t['group'] or t['error']: continue
        who=t['key']; p=autonomy.person(s,who)
        if not hidden_cast.contact(s,who) or not available(s,who) or now<t['muted_until']: continue
        if t['last_reply'] is None: continue
        elapsed=now-t['last_reply']
        delay=followup_delay(s,who)
        # Space repeated check-ins farther apart instead of permanently stopping.
        delay*=min(16,2**min(t['followups'],4))
        if activity(s,who)=='At work / studying': delay*=2
        if elapsed>=delay:
            receipt='delivered but not read' if chat(s,t).get('unread',0) else 'read without a reply'
            t['reason']=dict(kind='silence',eligible_at={who:now},text=f'Your last message was {receipt}. You have sent {t["followups"]} unanswered follow-ups. React in your own voice, considering your relationship, mood and responsibilities: a gentle check-in, concern, mild frustration, or giving space can fit. Repeated silence may warrant acknowledging the pattern, without guilt-tripping or assuming why. Add something relevant and avoid repeating earlier messages.',offer=None)
            t['followups']+=1; t['revision']+=1


def next_job(s):
    import autonomy
    tick(s)
    now=s['world']['minute']
    candidates=[]
    for t in ensure(s)['threads'].values():
        if t['error'] or t.get('prepared') or (not t['pending'] and now<t['due']) or now<t['muted_until']: continue
        if t['reason'] and t['reason'].get('offer'):
            offer=next((o for o in autonomy.ensure(s)['offers'] if o['id']==t['reason']['offer']),None)
            if not offer or offer['state']!='pending': t['reason']=None
        for who in members(s,t):
            overdue=any(who in m.get('eligible_at',{}) and m['eligible_at'][who]<now and who not in m['answered_by'] for m in t['pending'])
            reason_ready=(t['reason'] or {}).get('eligible_at',{}).get(who,now)
            overdue=overdue or reason_ready<now
            if not available(s,who) and not overdue: continue
            batch=[m for m in t['pending'] if who in m['read_by'] and who not in m['answered_by'] and now>=m.get('ready_at',{}).get(who,now)
                   and (available(s,who) or who in m.get('eligible_at',{}))]
            if not batch and not t['reason']: continue
            if not batch and t['pending']: continue
            job=dict(key=t['key'],group=t['group'],who=who,ids=[m['id'] for m in batch],
                     text='\n'.join(m['text'] for m in batch),reason=copy.deepcopy(t['reason']),revision=t['revision'],
                     eligible_at=min((m.get('eligible_at',{}).get(who,now) for m in batch),default=reason_ready))
            candidates.append(((0 if batch else 1,min(m['minute'] for m in batch) if batch else t['due'],-affinity(s,who)),job))
    return min(candidates,key=lambda item:item[0])[1] if candidates else None


def generate(s,job):
    import game_core as core
    import autonomy
    if job.get('group') and 'charles' in s.get('groups',{}).get(job['key'],{}).get('members',[]): raise ValueError('Charles accepts direct texts only.')
    if job['who']=='charles' and not __import__('charles_han').number_allowed(s): raise ValueError('Charles has not shared his private number.')
    who=job['who']; s['active']=who; s['_text_only']=True
    # Delivered-but-unread texts must not leak into prompt history or recall.
    pending_ids={m['id'] for t in ensure(s)['threads'].values() for m in t['pending']}
    if who in s['routes']: s['routes'][who]['history']=[m for m in s['routes'][who]['history'] if m.get('message_id') not in pending_ids]
    action=job['text'] or core.INCOMING_TEXT
    messages=core.build_messages(s,action) if who in s['routes'] else []
    if job['group']:
        audience=members(s,thread(s,job['key'],True))
        public_history=[m for m in s['groups'][job['key']]['history'] if m.get('message_id') not in pending_ids or m.get('message_id') in job['ids']]
        # Group generation uses only group history and public character canon.
        if who in core.hidden.CAST: public=core.hidden.profile(who)
        elif who in core.CONTACTS: public=core.lore.character_tables()[who]['Public life']
        else:
            people=[*core.town.NPCS,*core.town.VENUE_STAFF.values(),getattr(core.town,'HQ_EXECUTIVE',())]
            public=next((details for details in people if details and details[0]==who),(who,'a known adult town contact','Use only established shared history.'))
        messages=[dict(role='system',content='Write only as '+core.CONTACTS.get(who,(who,))[0]+' in a group text. Public character canon: '+str(public)+'. Texting voice: '+core.TEXT_STYLES.get(who,'Use your own voice.')+' Do not disclose private memories or secrets to this group.'),
                  dict(role='user',content=json.dumps({'group_history':public_history[-25:],'members':audience,'latest_read_messages':job['text']}))]
        listeners = list(dict.fromkeys([s['player'], *(person for person in audience if person != who)]))
        messages[0]['content'] += '\n' + core.social_world.CONTINUITY_DIRECTION
        messages[0]['content'] += '\nYour established familiarity with this audience: ' + json.dumps(
            core.social_world.conversation_knowledge(s, who, listeners), ensure_ascii=False)
    schema={'type':'object','properties':{
        'bubbles':{'type':'array','items':{'type':'string','minLength':1,'maxLength':1200},'minItems':1,'maxItems':3},
        'moment':{'type':'string','enum':['none','connection','setback']},
        'pause_minutes':{'type':'integer','minimum':0,'maximum':1440},
        'hangout_decision':{'type':'string','enum':['none','accepted']},
        'feeling':{'type':'string','enum':list(core.emotions.FEELINGS)},
        'social_event':{'type':'string','enum':list(core.town.SOCIAL_EVENTS)}},
        'required':['bubbles','moment','pause_minutes','hangout_decision','feeling','social_event'],'additionalProperties':False}
    own_context=autonomy.context(s,who) if who in s['world']['cast'] else dict(status=activity(s,who),needs=profile(s,who),recent_events=[])
    messages[0]['content'] += core.social_world.add_note_schema(schema, s, [who])
    if job.get('eligible_at',s['world']['minute'])<s['world']['minute']:
        messages[0]['content']+='\nThis reply became due while you were available before the player advanced time. Deliver the queued response naturally; do not claim to have just checked the phone while asleep or travelling.'
    import memory_store
    commitments=memory_store.open_commitments(s,[s['player'],who])[-8:] if not job['group'] else []
    if commitments and job['text']:
        schema['properties']['commitment_updates']={'type':'array','maxItems':3,'items':{'type':'object','properties':{
            'id':{'type':'string','enum':[r['id'] for r in commitments]},
            'status':{'type':'string','enum':['agreed','reported_fulfilled','cancelled']},
            'evidence':{'type':'string','maxLength':400}},'required':['id','status','evidence'],'additionalProperties':False}}
        schema['required'].append('commitment_updates')
        messages[0]['content']+='\nOpen commitments: '+json.dumps([dict(id=r['id'],text=r['text'],status=r['status']) for r in commitments])
        messages[0]['content']+='\nReturn commitment_updates only when the latest player message explicitly agrees to, cancels, or reports finishing that exact commitment. evidence must be an exact quotation from that message. Otherwise return an empty array. A question, hypothetical, meeting, or elapsed time never proves agreement or completion. Reported completion is a claim, not an independently verified action.'
    if job['group']:
        own_context['recent_events']=[e for e in own_context['recent_events'] if set([s['player'],*audience]).issubset(e['owners'])]
    messages[0]['content']+='\nFINAL DELIVERY OVERRIDE: Return only the supplied schema. Write 1–3 distinct message bubbles as this character; use a burst only if natural for their voice. Address only messages they have read. Do not automatically apologise for delays, use a stock asleep apology, repeat a greeting, demand a reply, or assume the player’s activity. A follow-up can add a new thought without a question. Read receipts do not reveal emotions or reasons for silence. Invitations remain proposals; only controls record travel, acceptance, sleepovers or promises fulfilled. moment is connection only for a meaningful reciprocal exchange, setback only for an actual hurtful exchange. pause_minutes is a delay explicitly requested by the player (e.g. talk tomorrow), otherwise 0. Do not invent new biographies, intimacy or shared experiences. Current own state: '+json.dumps(own_context)+'\nReason for this message: '+json.dumps(job['reason'])
    messages[0]['content']+='\nAlso return hangout_decision, feeling and social_event from the schema. Accept a current invitation only when genuinely free and willing; otherwise negotiate a later time. A group message cannot accept a private hangout. Feeling is your own immediate feeling, never the player’s. Classify social_event using: '+core.SOCIAL_GUIDE
    messages[0]['content']+='\n'+core.town.sexuality.direction(s['player'],audience if job['group'] else [who])
    if core.town.sibling_route(s,who) or who in ('sylvanis', 'neo', 'alyssa'):
        schema['properties']['social_event']['enum']=['none']
        messages[0]['content']+='\nThis player pairing is strictly nonromantic. Never flirt or imply intimacy.'
    elif not core.town.romanceable(s,who):
        schema['properties']['social_event']['enum']=[event for event in core.town.SOCIAL_EVENTS if event not in core.town.POSITIVE_FLIRTS]
        messages[0]['content']+='\nDo not reciprocate romantic advances toward the player. A refusal must be clear, with friendship still possible; do not imply that more trust would change orientation.'
    response=core.request('/api/chat',dict(model=core.MODEL,messages=messages,stream=False,think=False,format=schema,
        options={'temperature':.8,'num_ctx':16384,'num_predict':1200}))
    try:
        data=json.loads(response['message']['content']); bubbles=data['bubbles']
        if not isinstance(bubbles,list) or not 1<=len(bubbles)<=3 or any(not isinstance(b,str) or not b.strip() or len(b)>1200 for b in bubbles): raise ValueError()
        if data['moment'] not in ('none','connection','setback'): raise ValueError()
        if type(data['pause_minutes']) is not int or not 0<=data['pause_minutes']<=1440: raise ValueError()
        if data.get('hangout_decision','none') not in ('none','accepted') or data.get('social_event','none') not in core.town.SOCIAL_EVENTS: raise ValueError()
        if data.get('social_event','none') not in schema['properties']['social_event']['enum']: raise ValueError()
        if data.get('feeling','content') not in core.emotions.FEELINGS: raise ValueError()
        updates=data.get('commitment_updates',[])
        if not isinstance(updates,list) or len(updates)>3: raise ValueError()
        for update in updates:
            if (update.get('id') not in {r['id'] for r in commitments} or update.get('status') not in ('agreed','reported_fulfilled','cancelled')
                or not isinstance(update.get('evidence'),str) or not update['evidence'].strip() or update['evidence'] not in job['text']): raise ValueError()
        for bubble in bubbles:
            core.validate_response(dict(narration='Incoming message.',dialogue=bubble,memory='Source-backed memories are retained.',
                choices=[],suggestions_deferred=True,speaker=core.CONTACTS.get(who,(who,))[0],addressee=core.PLAYERS[s['player']],
                choices_speaker=core.PLAYERS[s['player']],conversation_channel='text',social_event=data.get('social_event','none')),s if who in s['routes'] else None)
    except (ValueError,KeyError,TypeError) as exc: raise ValueError('Invalid text response. Your delivered messages are safe; retry this chat.') from exc
    return data


def apply(s,job,result):
    import game_core as core
    if result.get('social_event') in core.town.POSITIVE_FLIRTS and not core.town.romanceable(s,job['who']):
        return False
    import autonomy
    import memory_store
    t=thread(s,job['key'],job['group']); c=chat(s,t); now=s['world']['minute']; who=job['who']
    if job['reason'] and job['reason'].get('offer'):
        offer=next((o for o in autonomy.ensure(s)['offers'] if o['id']==job['reason']['offer']),None)
        if not offer or offer['state']!='pending' or now>offer['expires']:
            if t['reason']==job['reason']: t['reason']=None
            if not job['ids']: return False
    # New messages do not invalidate a response to a previously read batch.
    if job['ids'] and not any(m['id'] in job['ids'] and who not in m['answered_by'] for m in t['pending']): return False
    if not job['ids'] and t['reason']!=job['reason']: return False
    for bubble in result['bubbles']:
        if job['group']:
            c['history'].append(dict(speaker=core.CONTACTS.get(who,(who,))[0],text=bubble,minute=now))
        else:
            data=dict(narration='Incoming message.',dialogue=bubble,memory=c['memory'],choices=[],suggestions_deferred=True)
            c['history'].append(dict(role='assistant',content=json.dumps(data,ensure_ascii=False),channel='text',minute=now))
            c['dialogue']=bubble; c['scene']='Incoming message.'
    if result['bubbles']: mark_inbox_activity(s, c)
    c['unread']=c.get('unread',0)+len(result['bubbles'])
    core.social_world.record_notes(s, result, {who:'\n'.join(result['bubbles'])},
                                  owners=[s['player'], *members(s,t)])
    c.update(choices=[],personal_choices=[],suggestions_deferred=True,suggestions_requested=[])
    for m in t['pending']:
        if m['id'] in job['ids'] and who not in m['answered_by']: m['answered_by'].append(who)
    t['pending']=[m for m in t['pending'] if len(m['answered_by'])<len(members(s,t))]
    if t['reason']==job['reason']: t['reason']=None
    t['last_reply']=now; t['error']=None
    t['muted_until']=max(t['muted_until'],now+result['pause_minutes'])
    p=profile(s,who)
    if job['ids']:
        for update in result.get('commitment_updates',[]):
            memory_store.report_commitment(s,update['id'],update['status'],update['evidence'],s['player'],who,
                'message-commitment:'+who+':'+str(job['ids'])+':'+update['id'])
        if result.get('hangout_decision')=='accepted' and not job['group']:
            core.town.accept_hangout(s,who)
        if result.get('feeling'):
            s['emotions'][who]=result['feeling']
            p['emotion_cause']=dict(text='Responding to the player’s message: '+job['text'][:300],minute=now,feeling=result['feeling'])
        interaction=result.get('social_event','none')
        if interaction!='none' and not core.town.sibling_route(s,who): core.town.social_event(s,who,interaction)
        if result['moment']=='connection':
            p['happiness']=min(100,p['happiness']+1)
            core.town.conversation_progress(s,who,'personal_detail',interaction)
        elif result['moment']=='setback':
            p['happiness']=max(0,p['happiness']-2)
            core.town.conversation_progress(s,who,'setback','none')
    memory_store.sync(s)
    import message_photos
    message_photos.schedule(s, job, result)
    return True


class MessagePump:
    def __init__(self,game):
        self.game=game; self.results=queue.Queue(); self.running=None; self.completed=None
        self.started=0
        from message_photos import PhotoPump
        self.photos=PhotoPump(game)

    def tick(self):
        game=self.game
        self.photos.tick()
        if not game.in_game or not game.state_data: return
        s=game.state_data
        if self.completed is None:
            try: self.completed=self.results.get_nowait()
            except queue.Empty: pass
        if self.completed:
            origin,job,result,error=self.completed
            self.running=None; self.completed=None
            if origin is s:
                if job.get('cancelled'): pass
                elif error: thread(s,job['key'],job['group'])['error']=error
                else: thread(s,job['key'],job['group'])['prepared']=dict(job=job,result=result)
                game.persist(); game.render()
        # A reply waiting for its sender to wake belongs to that chat, not to the
        # global worker. Other contacts can keep composing and replying.
        for t in list(ensure(s)['threads'].values()):
            prepared=t.get('prepared')
            if not prepared: continue
            if not available(s,prepared['job']['who']) and prepared['job'].get('eligible_at',s['world']['minute'])>=s['world']['minute']: continue
            before=copy.deepcopy(s)
            try:
                apply(s,prepared['job'],prepared['result'])
                t.pop('prepared',None)
            except (ValueError,KeyError) as exc:
                s.clear(); s.update(before)
                current=thread(s,t['key'],t['group']); current.pop('prepared',None); current['error']=str(exc)
            game.persist(); game.render()
        if self.running: return
        job=next_job(s)
        if not job: return
        self.running=(s,job); snapshot=copy.deepcopy(s)
        self.started=time.monotonic()
        def work():
            try: self.results.put((s,job,generate(snapshot,job),None))
            except Exception as exc: self.results.put((s,job,None,str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def typing(self,key,group=False):
        return bool(self.running and not self.running[1].get('cancelled') and self.running[0] is self.game.state_data and self.running[1]['key']==key and self.running[1]['group']==group and available(self.game.state_data,self.running[1]['who']))

    def cancel(self,key,group=False):
        t=thread(self.game.state_data,key,group)
        t['error']='Reply paused. Use Continue / retry when ready.'
        t.pop('prepared',None)
        if self.running and self.running[1]['key']==key and self.running[1]['group']==group: self.running[1]['cancelled']=True
        self.game.persist()
