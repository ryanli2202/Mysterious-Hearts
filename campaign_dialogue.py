"""Saved authored conversations displayed by the ordinary in-person hangout canvas."""
import copy
import json
import queue
import threading

def beat(player='', speaker=None, text='', narration=''):
    return dict(player=player,speeches=[[speaker,text]] if speaker else [],narration=narration)


def action_beat(action, narration=''):
    return dict(player='', action=action, speeches=[], narration=narration)


def normalize_actions(d):
    """Repair saved choice labels without reclassifying actual authored speech."""
    import rei_story, charles_quest
    labels = set()
    if d.get('action') == 'rei_story.advance':
        labels = {label for scene in rei_story.SCENES for label in scene[3]}
    elif d.get('action') == 'charles_quest.advance':
        labels = {label for i, scene in enumerate(charles_quest.STEPS) if i != 8 for label in scene[3]}
    for b in d['beats']:
        if b.get('player') in labels:
            b['action'] = b['player']
            b['player'] = ''


def generate_action_narration(player, venue, b):
    import combat
    context = dict(player=player, venue=venue, selected_action=b['action'], authored_context=b['narration'])
    data = combat.ask_ai('Act as the Game Master for an in-person campaign. Write 1-3 sentences '
        'describing the supplied selected action in third person. It is an action, not spoken dialogue. '
        'Preserve the authored context and uncertainty. Do not invent evidence, discoveries, success, '
        'consent, combat results, travel, rewards or subsequent decisions. No dialogue or future spoilers. '
        'This is presentation only; game rules resolve the outcome later. Context: '+json.dumps(context),
        combat.schema({'narration': {'type': 'string'}}))
    text = data.get('narration')
    if not isinstance(text, str) or not text.strip() or len(text) > 2000:
        raise ValueError('Invalid campaign narration.')
    return text.strip()


def request_narration(game, d, b):
    """Generate off-thread; discard replies after navigation or loading another save."""
    if not b.get('action') or b.get('gm_narration') or (b.get('optional_narration') and not b.get('_request_narration')):
        return
    job = (d, b)
    previous = getattr(game, '_campaign_narration_job', None)
    if previous and previous[0] is d and previous[1] is b:
        return
    game._campaign_narration_job = job
    origin = game.state_data
    results = queue.Queue()
    snapshot = copy.deepcopy(b)
    player, venue = d['player'], d['venue']
    def work():
        try: results.put((generate_action_narration(player, venue, snapshot), None))
        except Exception: results.put((None, 'Game Master narration unavailable; showing the selected action.'))
    def poll():
        if (game.state_data is not origin or origin.get('campaign_dialogue') is not d
                or d['beats'][d['cursor']] is not b):
            if getattr(game, '_campaign_narration_job', None) is job:
                game._campaign_narration_job = None
            return
        try: text, error = results.get_nowait()
        except queue.Empty:
            game.after(100, poll)
            return
        # Keep the job marker on failure so redraws do not retry endlessly.
        if text:
            b['gm_narration'] = text
            b.pop('_narration_error', None)
            game.persist()
        b['_narration_error'] = error
        show(game)
    threading.Thread(target=work, daemon=True).start()
    game.after(100, poll)

CHARLES_FIGHT = [
    beat('You were here. All this time, you were here.', 'charles', 'Lower your voice, Garrett.', 'Charles stands between his brother and the laboratory door.'),
    beat('I thought you were dead. I kept calling. Do you know what it was like to hear that phone ring?', 'charles', 'Every time I wanted to answer, I thought about what would happen if they found you through me.'),
    beat('So you decided I could live with losing you. You decided that for me.', 'charles', 'I decided you would live. Hate me for it if you have to.'),
    beat('Stop making that sound noble. I needed my brother, and you left me searching for a ghost.', 'charles', 'And I needed you somewhere they could not reach. I am not coming back into your life. Go home.'),
    beat('Look at me. Not the kid you remember. Me.', 'charles', 'You fought your way this far and you think that means you understand what is waiting here?'),
    beat('No. It means you do not get to call me helpless because being afraid is easier than trusting me.', 'charles', 'If you cannot get past me, you cannot survive what comes after me.', 'Charles’s voice breaks on the last word. He covers it by raising his hands.'),
    beat('Then stop hiding behind protection. Fight me. And when I am still standing, you listen.', 'charles', 'I will make you leave if that is what it takes.', 'Neither brother looks away. Continue to begin the mandatory fight; Garrett must win before they can reconcile.'),
]

RICHTER_FIGHT = [
    beat('I have your authorisation. They asked to withdraw. You kept them.', 'Joseph Richter', 'You brought paperwork into my headquarters and expected me to surrender?', 'The executive door seals behind Rei. Joseph’s sleeves part around reinforced arms.'),
    beat('I brought proof. You called restraint trials research and turned people into equipment.', 'Joseph Richter', 'Awakened people have advantages the rest of us never chose. I built mine.', 'A powered spinal frame locks into place. Targeting lights track Rei’s movement.'),
    beat('You always find a reason the person you hurt deserved it. You did it to Marcus too.', 'Joseph Richter', 'That was school. This is bigger than your old grievances.'),
    beat('Marcus had a life. He made things. He made us laugh. You do not get to make him small because you want to stop answering for what you did.', 'Joseph Richter', 'And you do not get to stand over me and demand an apology.'),
    beat('I am stopping what you are doing here.', 'Joseph Richter', 'Try.', 'Joseph brings his weapons online. Continue to begin the fight. Only victory resolves this confrontation.'),
]

def dispatch(s,action,args):
    module,name=action.split('.')
    if module not in ('rei_story','charles_quest','interpol'): raise ValueError('Unknown scripted campaign action.')
    return getattr(__import__(module),name)(s,*args)

def scenes(s,action,args):
    import rei_story, charles_quest
    player=s['player']
    if action=='charles_quest.security_action':return CHARLES_FIGHT
    if action=='rei_story.confront':return RICHTER_FIGHT
    if action=='rei_story.advance':
        i=rei_story.data(s)['stage'];title,venue,text,choices,finding=rei_story.SCENES[i]
        if i==5:
            return [beat('I know the name on this house. Tell me what you are doing with it.', 'Emi Suda', 'We do not recruit children. Adults can leave. No one is trained through torture.', 'Emi meets Rei with Ren Aoki and Daichi Kurose.'),
                    beat('A charter is easy to write.', 'Ren Aoki', 'These are the adult rosters. These are the departures. Compare them with the public filings; you do not have to take our word for it.'),
                    beat('They gave orders until I could not tell an order from my own thoughts.', 'Daichi Kurose', 'What they did to you was wrong. We inherited their name, not a right to your loyalty. We cannot ask you to call this home.'),
                    beat('And if I wanted it to end?', 'Daichi Kurose', 'I would ask you to judge the people who are here. If you chose to lead under this charter, I would relinquish command. But I cannot choose for you.'),
                    action_beat(choices[args[0]],narration='Rei compares the current adult roster and departures with the filings. The evidence supports a changed successor. His next choice remains his own.')]
        if i==2:
            return [beat(narration='Rei opens Marcus’s old storyboard: a miniature city, an impossible bus timetable and a pigeon filmed one frame at a time.'),
                    beat('You called my hand a very local weather event. I still cannot draw that pigeon without hearing it.',narration='The memory carries a laugh before it carries anything else.'),
                    beat('I remember what Joseph did. I remember you too. You were more than what happened to you.',narration='Marcus later died by suicide. The scene supplies neither a single explanation nor an obligation for Rei to have saved him.'),
                    action_beat(choices[args[0]],narration='He gives the storyboard a place in the room, without pretending that remembering has become easy.')]
        return [beat(narration=text),action_beat(choices[args[0]],narration=finding)]
    if action=='rei_story.choose':
        choice=args[0]
        return [beat({'lead':'If I lead, the charter stays. No children. No coercion. No exceptions.', 'leave':'I have heard you. I am leaving. Do not mistake that for belonging here.', 'destroy':'I cannot leave this organisation standing. I am going through every post.'}[choice],
                     'Daichi Kurose', {'lead':'Then command is yours. I will tell the house.', 'leave':'You owe us no place in your life.', 'destroy':'Then the people here will defend their posts. We will not make children fight for us.'}[choice])]
    if action.startswith('charles_quest.'):
        d=charles_quest.read(s);i=d['step']
        if action=='charles_quest.check_in':
            return [beat(narration='A private written check-in is waiting. Garrett reads it without sharing it with bystanders.')]
        if i==9:
            return [beat('I am still here. Now talk to me.', 'charles', 'You are stronger than I let myself believe. That does not make what I did to you right.', 'Charles lowers his hands. The fight has ended; neither brother pretends it did not hurt.'),
                    beat('Why did you disappear?', 'charles', 'I came here to get close to Sylvanis. To find out what happened to our parents. I thought keeping you out of it would keep you safe.'),
                    beat('I can stand beside you without exposing your cover. But you do not get to disappear on me again.', 'charles', 'All right. My number. Just you and me. I will answer when it is safe, and I will tell you when it is not.')]
        if i==10:return [beat('I will protect your cover. '+('But you write. Even if all you can say is that you are still here.' if args[0]==0 else 'But the silence was not all right. Trust has to go both ways.'),'charles','I hear you. I will keep in touch. You do not have to forgive everything tonight.')]
        if i<len(charles_quest.STEPS):
            title,venue,question,choices,finding=charles_quest.STEPS[i]
            # Failed investigative choices must never display the successful finding.
            return [beat(narration=question), (beat if i == 8 else action_beat)(choices[args[0]],narration='Garrett records his response and checks what the evidence supports.')]
        return [beat(narration='A private written check-in is waiting. Garrett reads it without sharing it with bystanders.')]
    if action=='interpol.advance':
        import interpol
        step=interpol.objective(s);partner=interpol.read(s)['active']['partner']
        if step.get('scripted_outcome')=='crow_defeat':
            return [beat(narration='The command entrance opens onto the Crow’s chamber. Their copies of the Ace evidence are already secured outside headquarters.'),
                    beat(speaker='gordon',text='We have established the command chain. End this here. Come with us.'),
                    beat(speaker='crow',text='You found a door and mistook it for the end of my organisation.'),
                    beat(speaker='fox',text='I found the people you keep putting between yourself and the street. I am done fighting your shadows.'),
                    beat(speaker='gordon',text='Stay together. If containment fails, we leave together.',narration='This is a playable story defeat. Combat resolves after at most four exchanges; survival carries the campaign forward. The Crow cannot be captured here.')]
        key=interpol.read(s)['active']['key']
        if key=='crow_operation' and step['kind']!='combat':
            return [beat(narration=step['finding']),
                    beat(speaker=partner,text='We take the next step together. We do not erase the people we helped because we could not finish the whole fight.')]
        if step['kind']=='reveal':
            import four_aces
            who=interpol.CASES[key]['reveal'];person=four_aces.CAST[who]
            return [beat(speaker='gordon',text=person['name']+' is the Ace of '+person['suit']+'. The records and the field encounter support the same conclusion.'),
                    beat(speaker='fox',text='Then put the name against what they did. Not everyone who worked beside them.'),
                    beat(narration='The verified identity is disclosed to the assembled investigation team. Other contacts do not automatically learn it.')]
        return [beat(speaker=partner,text='Our objective: '+step['title']+'.',narration='The field team reviews the current evidence at the objective location.'),
                beat('We keep the record to what we can establish.',partner,
                     'Guard posts first. Then the operation target. Stay ready.' if step['kind']=='combat' else step['finding'])]
    return []

def begin(s,action,args=()):
    if s.get('campaign_dialogue'): raise ValueError('Finish the current scripted conversation first.')
    if action=='campaign_flashbacks.finish':
        import campaign_flashbacks
        key,=args
        campaign_flashbacks.validate(s,key)
        scene=campaign_flashbacks.SCENES[key]
        lines=__import__('campaign_prose').memory_pages(s,key)
        stamp_pages(s,lines)
        s['campaign_dialogue']=dict(action=action,args=[key],beats=copy.deepcopy(lines),cursor=0,
            venue=s['world']['location'],player=s['player'],title=scene['title'],
            memory_key=key,background=scene['background'],portraits=copy.deepcopy(scene['portraits']))
        return
    # Existing authoritative mutations validate a copy; no evidence or combat is
    # committed until the last authored line. These handlers perform no I/O.
    preview=copy.deepcopy(s)
    dispatch(preview,action,args)
    import campaign_prose
    lines=campaign_prose.action_pages(s,action,args,preview)
    if lines is None:lines=scenes(s,action,args)
    if not lines:raise ValueError('No scripted conversation for this action.')
    if lines[0].get('prose') and action in ('rei_story.advance','charles_quest.advance'):
        module=__import__(action.split('.')[0])
        index=module.data(s)['stage'] if action.startswith('rei') else module.read(s)['step']
        spec=module.SCENES[index] if action.startswith('rei') else module.STEPS[index]
        if not (action.startswith('charles') and index==8):
            lines.append(campaign_prose.page('Selected action: '+spec[3][args[0]]+'\n\nThe response will be recorded when you continue to the outcome.',
                action=spec[3][args[0]],optional_narration=True,title='Your response'))
    stamp_pages(s,lines)
    s['campaign_dialogue']=dict(action=action,args=list(args),beats=copy.deepcopy(lines),cursor=0,venue=s['world']['location'],player=s['player'],flashback_gate_checked=True)

def stamp_pages(s,lines):
    for b in lines:
        if b.get('prose'):
            b.setdefault('venue',s['world']['location']);b.setdefault('minute',s['world']['minute'])


def epilogue(s,lines):
    if not s.get('campaign_dialogue'):
        stamp_pages(s,lines)
        s['campaign_dialogue']=dict(action=None,args=[],beats=lines,cursor=0,venue=s['world']['location'],player=s['player'])

def activate_epilogue(s):
    if not s.get('campaign_dialogue') and not s.get('combat',{}).get('active') and not __import__('combat').recovering(s) and s.get('campaign_epilogues'):
        entry=s['campaign_epilogues'][0]
        if entry['venue']==s['world']['location']:
            s['campaign_epilogues'].pop(0);epilogue(s,entry['lines'])

def next_line(s):
    d=s.get('campaign_dialogue')
    if not d:raise ValueError('No scripted conversation.')
    if s['player']!=d['player'] or s['world']['location']!=d['venue']:raise ValueError('Return to the saved conversation location.')
    b=d['beats'][d['cursor']]
    if b.get('reflection') and b.get('selected') is None:raise ValueError('Choose a reflection before continuing.')
    if d['cursor']<len(d['beats'])-1:d['cursor']+=1;return 'Next line'
    if d['action']=='campaign_flashbacks.finish':
        result=__import__('campaign_flashbacks').finish(s,*d['args'])
        __import__('campaign_prose').finish(s,d)
        s['campaign_dialogue']=None
        s.setdefault('campaign_dialogue_history',[]).append(d)
        return result
    s['campaign_dialogue']=None
    if not d.get('flashback_gate_checked'):
        s['_finishing_legacy_campaign_dialogue']=True
    try:result=dispatch(s,d['action'],d['args']) if d['action'] else 'Conversation complete.'
    except Exception:
        s['campaign_dialogue']=d
        raise
    finally:s.pop('_finishing_legacy_campaign_dialogue',None)
    __import__('campaign_prose').finish(s,d)
    s.setdefault('campaign_dialogue_history',[]).append(d)
    return result

def maybe_open(game,fn,args):
    action=fn.__module__+'.'+fn.__name__
    if action=='campaign_flashbacks.start':
        fn(game.state_data,*args);game.persist();show(game);return True
    if action=='campaign_prose.begin_social':
        fn(game.state_data,*args);game.persist();show(game);return True
    allowed=('rei_story.advance','rei_story.choose','rei_story.confront','rei_story.fight_guards','charles_quest.advance','charles_quest.check_in','interpol.advance')
    if action=='charles_quest.security_action':
        import charles_quest, organisation_guards
        s=game.state_data
        step=charles_quest.read(s)['step']
        if step not in (14,16) and (step!=9 or organisation_guards.remaining(s,'glasshouse_lab','charles:search')):return False
    elif action not in allowed:return False
    begin(game.state_data,action,args);game.persist();show(game);return True

def show(game):
    import tkinter as tk
    from tkinter import ttk
    from hangout_ui import Exchange
    import phone_theme, artwork, winterfield_ui as ui
    d=game.state_data.get('campaign_dialogue')
    if not d:return
    if d['beats'][d['cursor']].get('prose'):
        __import__('campaign_prose_ui').show(game)
        return
    __import__('campaign_prose_ui').hide(game)
    game.hide_phone_for_location()
    for name in ('campaign_view','interpol_view','combat_view'):
        panel=getattr(game,name,None)
        if panel is not None and panel.winfo_exists():panel.place_forget()
    area=getattr(game,'area_view',None)
    if area is not None and area.winfo_exists():area.pack_forget()
    game.presence_view.pack_forget();game.in_person_chat.pack(side='left',fill='both',expand=True)
    view=game.hangout_view;c=view.canvas
    view.script_mode=True
    if not hasattr(view,'script_panel'):
        view.script_panel=tk.Frame(c,bg=ui.PANEL,padx=14,pady=12)
        view.script_item=c.create_window(0,0,window=view.script_panel,anchor='sw')
    for w in view.script_panel.winfo_children():w.destroy()
    normalize_actions(d)
    b=d['beats'][d['cursor']]
    c.members=list(dict.fromkeys(who for line in d['beats'] for who,_ in line['speeches'] if who!=game.state_data['player']))
    narration = b.get('gm_narration') or ('Selected action: '+b['action']+'\n\n'+b['narration'] if b.get('action') else b['narration'])
    c.exchange=Exchange(player=b['player'],narration=narration,speeches=b['speeches'])
    c.speech_index=0;c.page_indices=dict.fromkeys(c.page_indices,0)
    c.artwork=d.get('background') or artwork.scene_art(d['venue'],minute=game.state_data['world']['minute'])
    heading=('MANDATORY FLASHBACK · '+d['title']) if d.get('title') else ('SCRIPTED CONVERSATION · '+__import__('town').location_name(game.state_data,d['venue']))
    ttk.Label(view.script_panel,text=f"{heading} · {d['cursor']+1} / {len(d['beats'])}",wraplength=700).pack(anchor='w')
    if b.get('action') and not b.get('gm_narration'):
        ttk.Label(view.script_panel, text=b.get('_narration_error') or 'Game Master is describing your action…').pack(anchor='w')
        if b.get('_narration_error'):
            def retry():
                game._campaign_narration_job = None
                b.pop('_narration_error', None)
                show(game)
            ttk.Button(view.script_panel, text='Retry narration', command=retry).pack(side='left')
    request_narration(game, d, b)
    def advance():
        try:next_line(game.state_data);game.persist()
        except ValueError as exc:
            ttk.Label(view.script_panel,text=str(exc),wraplength=700).pack(fill='x');return
        if game.state_data.get('campaign_dialogue'):show(game)
        else:
            restore(view);game.render()
            if __import__('combat').active(game.state_data):__import__('combat_ui').open_combat(game)
    ttk.Button(view.script_panel,text='Continue' if d['cursor']<len(d['beats'])-1 else 'Continue to outcome',command=advance).pack(side='right',padx=4)
    c.controls_height=90
    c.itemconfigure(view.controls_item,state='hidden');c.itemconfigure(view.header_item,state='hidden')
    c.itemconfigure(view.script_item,state='normal');c.redraw();phone_theme.apply_tree(view.script_panel)

def restore(view):
    reader=getattr(view,'prose_reader',None)
    if reader is not None and reader.winfo_exists():reader.place_forget()
    if not getattr(view,'script_mode',False):return
    view.script_mode=False;c=view.canvas
    c.itemconfigure(view.script_item,state='hidden');c.itemconfigure(view.controls_item,state='normal');c.itemconfigure(view.header_item,state='normal')
    c.controls_height=view.controls.winfo_reqheight()
