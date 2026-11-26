"""Isolated, timeless school hangouts; never create present-day historical contacts."""
import copy
import json
import uuid
import flashback_lore as lore

AREAS = {
    'takeo-command-history':dict(title='Before the Orders Ended',players=('takeo',),cast=('takeo','takeo-deputy','takeo-medic','takeo-kazama','takeo-researcher','takeo-officer','thirteen','sylvanis'),background='locations/campaign/takeo/directive_briefing',activities=('Discuss the supplied report','Observe the quiet room'),portraits={'takeo':'takeo-directive'}),
    **{area:dict(title=title,players=('neo',),cast=(('neo','tyler','daniel') if area=='neo-school' else ('neo','mariko') if area=='neo-adoptive-home' else ('neo','thirteen','trainee')),background='locations/campaign/neo/home_kitchen',activities=('Share an ordinary meal','Try a harmless repair','Spend a quiet interval','Discuss an ordinary choice'),portraits={}) for area,title in __import__('neo_history').TITLES.items()},
    'ivan-network-history':dict(title='A Life on Loan · bounded history',players=('ivan',),cast=('ivan',),background='locations/campaign/ivan/handover',activities=('Observe the room','Practise a harmless wrist turn'),portraits={'ivan':'ivan-handover18'}),
    'takeo-command-history':dict(title='Before the Orders Ended',players=('takeo',),cast=('takeo','takeo-deputy','takeo-medic','takeo-kazama','takeo-researcher','takeo-officer','thirteen','sylvanis'),background='locations/campaign/takeo/directive_briefing',activities=('Discuss the supplied report','Observe the quiet room'),portraits={'takeo':'takeo-directive'}),
    'sylvanis-before-cards':dict(title='Before the Cards · Sylvanis',players=('sylvanis',),cast=('sylvanis','kaden','conspirator','crow','charles','takeo'),background='locations/campaign/sylvanis/compound',activities=('Discuss a practical limit','Share an ordinary meal','Review a supplied harmless schedule'),portraits={'sylvanis':'sylvanis-early'}),
    'camila-house':dict(title='The House That Raised Her · Camila',players=('camila',),cast=('camila','camila-elena','camila-pilar','camila-mara','camila-inez','crow'),background='locations/campaign/camila/orphanage',activities=('Play an ordinary game','Share a meal','Discuss a supplied lesson','Keep a quiet appointment'),portraits={'camila':'camila-child7'}),
    'elias-family-stage':dict(title='The House and the Stage · Elias',players=('elias',),cast=('elias','elias-johanna','elias-konrad','elias-anja','elias-lotte','crow'),background='locations/campaign/elias/gallery',activities=('Practice a rhythm','Rehearse a short scene','Share a meal','Discuss a costume or programme'),portraits={'elias':'elias-actor'}),
    'martos-service-years':dict(title='Service years · Martos',players=('martos',),cast=('martos','martos-sera','martos-tomas','martos-voss','crow'),background='locations/campaign/martos/mess',activities=('Prepare a simple shared meal','Repair an ordinary watch','Tidy the equipment bench','Discuss a practical limit'),portraits={'martos':'martos-special-forces','martos-sera':'sera-service','martos-tomas':'tomas-service','martos-voss':'voss-history'}),
    'mavis-rooms': dict(title='Rooms Without a Name · Mavis',
        players=('mavis',), cast=('mavis','mavis-broker','crow','sylvanis'),
        background='locations/mavis-quiet-house-landing',
        activities=('Check a practice route sketch', 'Discuss the terms of a task',
                    'Listen to the weather in the room', 'Ask about an ordinary practical limit'),
        portraits={'mavis':'mavis-age20','mavis-broker':'mavis-broker'}),
    'school': dict(title='School days · Rei, Emily, Sophie & Marcus',
        players=('rei','emily','sophie'), cast=('rei','emily','sophie','marcus'),
        background='locations/rei-high-school',
        activities=('Work on Marcus’s stop-motion film', 'Share lunch on the courtyard bench', 'Build a model greenhouse together', 'Walk to the sports ground'),
        portraits={who:who+'-high-school' for who in ('rei','emily','sophie','marcus')}),
    'hong-kong-school': dict(title='Hong Kong school days · Garrett & Charles',
        players=('garrett',), cast=('garrett','charles'), background='locations/garrett-hong-kong-school',
        activities=('Share an after-school snack', 'Talk about the school crews', 'Walk home together', 'Remember a family meal'),
        portraits={'garrett':'garrett-high-school','charles':'charles-young-adult'}),
    'fg-early-partnership':dict(title='The Blackhaven Annex · Early partnership',
        players=('fox','gordon'),cast=('fox','gordon','repair-worker'),background='locations/campaign-annex-counter',
        activities=('Compare two observed accounts','Help with a harmless repair','Share a quiet drink','Review a fictional route sketch'),
        portraits={'fox':'fox-early-partnership','gordon':'gordon-early-partnership'}),
}

def name(who):return lore.display_people()[who]['name']


def area_for(player,s=None):
    if player=='neo':return __import__('neo_history').area(s or {})
    return next((key for key, area in AREAS.items() if player in area['players']), None)


def active(s):
    visit=s.get('flashback_visit') or {}
    return visit if visit.get('player')==s.get('player') and visit.get('area')==area_for(s.get('player'),s) else None


def portraits(s):
    visit=active(s)
    if visit and visit['area'] in ('mavis-rooms','martos-service-years','elias-family-stage','camila-house','sylvanis-before-cards','neo-school','neo-adoptive-home','neo-shinigami-facility','takeo-command-history','ivan-network-history'):
        import campaign_memory_areas as spaces
        return {who:lore.profile(spaces.reference_era(s),who)['character_reference']['portrait']
                for who in (s['player'],*available(s))}
    return AREAS[visit['area']]['portraits'] if visit else {}


def available(s):
    area=area_for(s.get('player'),s)
    import campaign_memory_areas as spaces
    cast=spaces.cast(s,area) if area else ()
    return [who for who in cast if who!=s['player']]


def require_present(s):
    if s.get('neo_campaign',{}).get('session'):raise ValueError('Return from Neo’s recollection first.')
    if s.get('takeo_campaign',{}).get('session'):raise ValueError('Return from Takeo’s recollection first.')
    if s.get('sylvanis_campaign',{}).get('session'):raise ValueError('Return from the Sylvanis recollection first.')
    if any(s.get('ace_campaigns',{}).get(who,{}).get('session') for who in ('mavis','martos','elias','camila')):
        raise ValueError('Return from the campaign encounter before doing present-day activities.')
    if s.get('flashback_visit'):
        raise ValueError('Return from the flashback area before doing present-day activities.')


def record(s):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    root=s['flashback_memories'][visit['area']]
    import campaign_memory_areas as spaces
    period=visit.get('period',spaces.PERIODS[visit['area']][0][0])
    if period==spaces.PERIODS[visit['area']][0][0]:return root
    return root.setdefault('period_records',{}).setdefault(period,dict(history=[],members=available(s),exchange=opening(s,available(s))))


def opening(s, members):
    if s.get('player')=='neo':return __import__('neo_history').opening(s,members)
    if s.get('player')=='ivan':return __import__('ivan_history').opening(s)
    who=members[0] if members else None
    greetings={
        'camila-elena':'Let us agree whose turn it is before we start.',
        'camila-pilar':'I found the red counter. Do you want one more game?',
        'camila-mara':'There is time for this, and there is time for supper. Which do you need first?',
        'camila-inez':'I can discuss the appointment we actually agreed. Which detail needs checking?',
        'martos-sera':'Tell me what help you are offering before you start. I can answer for myself.',
        'martos-tomas':'The watch is losing a minute. Let us check the mechanism before blaming the clock.',
        'martos-voss':'State the bounded task and the equipment you require.',
        'rei':'I saved you a seat. Want to see what we have been drawing?',
        'emily':'I-I brought the little greenhouse. Would you like to help with the windows?',
        'sophie':'There you are! Lunch first, or do you want to come down to the track?',
        'marcus':'Good timing. My cardboard pigeon needs a second opinion.',
        'charles':'There you are, Garrett. Walk with me? We can get something to eat.',
        'fox':'A clear route on paper is still worth checking from the doorway.',
        'gordon':'Tell me which part of the account needs correcting. We can start there.',
        'repair-worker':'If you are staying, hold that lamp where I can see.',
        'mavis-broker':'Check the terms before you agree. Which part needs making precise?',
        'crow':'An accurate limit is useful. State what the assignment requires.',
        'sylvanis':'A quiet interval. How disappointing. Tell me which fragile little requirement matters to you.',
        'elias-johanna':'I have kept the figures separate from your programme. Which would you like to discuss?',
        'elias-konrad':'You have a fine ear for timing. Let us see what you make of today’s practice.',
        'elias-anja':'Listen to the rhythm once, then show me where you want to begin.',
        'elias-lotte':'The cue is yours when you are ready. Shall we try it once more?',
    }
    area=area_for(s['player'],s)
    if area=='takeo-command-history':
        d=s.get('takeo_campaign',{})
        if 'TK-F01' not in d.get('memories',[]):raise ValueError('Complete the captaincy recollection first.')
        if d.get('session') or s.get('campaign_dialogue') or d.get('scene_resume'):raise ValueError('Finish the campaign scene before optional history.')
    if area=='sylvanis-before-cards':
        greetings.update(kaden='Are the people outside sheltered? There is food if you want it.',conspirator='Which part of the supplied account needs checking?',charles='Which detail of this appointment needs checking?',takeo='State the commercial question.')
    spaces=__import__('campaign_memory_areas')
    narration=('Rain shifts on the repair-shop window. The borrowed room is quiet for a moment; the counter still needs to stay clear.'
               if area=='fg-early-partnership' else lore.era(spaces.reference_era(s,area))['setting'])
    if area=='martos-service-years':
        narration={'T1':'Steam rises from the mess-room kettle. For this quiet interval there is an ordinary meal to prepare.','T2':'A watch and an open tool roll wait on the equipment bench. Nothing on the bench needs to become an order.','T3':'The training yard has emptied. Their voices carry a little farther in the cool air.','T4':'A chair stands beside the infirmary table. Sera leaves room to sit without reaching for the equipment.','T5':'A kettle cools beside the narrow refuge bed. Rest and help still need to be asked about.','T6':'The sitting room is quiet. A repaired watch lies beside two cups on the table.'}[spaces.room(s) or spaces.initial(area)]
    if area=='mavis-rooms':
        current=spaces.room(s) or spaces.initial(area)
        narration={
            'M1':'Rain taps the landing window. The handler’s desk fan clicks behind the nearby door.',
            'M2':'A cup stands beside the common-room table. The repair lamp is still on in the adjoining corner.',
            'M3':'Coiled leads and a pair of headphones wait beneath the repair lamp. There is room for a small, patient task.',
            'M4':'The desk fan clicks on each turn. The Broker leaves space beside the papers rather than pushing them into her hands.',
            'M5':'The receiving doors have closed behind the last delivery. For a moment there is no one waiting for a report.',
            'M6':'Rain falls beyond the sheltered terrace. The chairs are close enough for conversation without closing the space between them.',
        }[current]
    if area=='elias-family-stage':
        current=spaces.room(s) or spaces.initial(area)
        narration={'E1':'Portraits line the family gallery. The house beyond it carries on with its ordinary work.','E2':'The piano stands in the music room. A phrase can be tried again without an audience.','E3':'A meal is being prepared in the family kitchen.','E4':'The family meeting room is private. Any service appointment here is separate from theatre work.','E5':'The repertory stage is at a separate theatre site. Work proceeds by cues and repeated practice.','E6':'Costumes and programme notes wait in the theatre dressing room.'}[current]
    if area=='takeo-command-history':
        greetings.update({'takeo':'State the detail in the report.','takeo-deputy':'Which part of this account can we actually certify?','takeo-medic':'I can answer for what I observed.','takeo-kazama':'You have read the order. What remains?','takeo-researcher':'An observation is not yet a repeatable result.','takeo-officer':'The return counts the units still answering.','thirteen':'State the objective.'})
        narration={'T1':'The last briefing has ended. Two folders remain apart on the table.','T2':'A radio clicks on the equipment bench. Kuroda puts an empty field bag beside it.','T3':'The mess has emptied. Someone has left the kettle warm.','T4':'Rain catches in the command hall’s damaged window. The map is still open.','T5':'Water runs between the courtyard stones. The next report is not due yet.','T6':'The observation glass reflects the closed forecast folder. The room beyond it is empty.','T7':'The salvaged radios are quiet. Mori checks the units still answering.','T8':'A desk lamp lights two closed files. The cabinets remain locked.','T9':'The training hall below the glass has emptied. Footsteps fade along the far corridor.','T10':'Thirteen waits beside the command table, watching for the next instruction.','T11':'The delivery schedule lies between two chairs. Sylvanis has not touched the pen.'}[spaces.room(s) or spaces.initial(area)]
    exchange=dict(player='',narration=narration,lines=[dict(speaker=who,text=greetings[who])] if who else [])
    if area=='fg-early-partnership' and who=='fox' and s['player']=='gordon':
        exchange['fox_opening_voice']=__import__('campaign_voice').fixed_binding('FG-ANNEX',greetings[who])
    return exchange


def sync_reference(s):
    """Keep old journal entries, but do not resume a reply from obsolete guidance."""
    saved=record(s);revision=lore.revision()
    if saved.get('reference_revision')!=revision:
        saved.update(reference_revision=revision,exchange=opening(s,active(s)['members']))
        active(s)['revision']+=1


def enter(s):
    if s.get('player')=='ivan':return __import__('ivan_history').enter(s)
    if active(s):
        import campaign_memory_areas as spaces
        visit=active(s);visit.setdefault('room',spaces.initial(visit['area']))
        visit.setdefault('period',spaces.PERIODS[visit['area']][0][0])
        sync_reference(s)
        return active(s)
    area=area_for(s.get('player'),s)
    if s.get('player')=='neo':
        reason=__import__('neo_history').locked(s,area)
        if reason:raise ValueError(reason)
        spaces=__import__('campaign_memory_areas');era=spaces.reference_era(s,area)
        for person in spaces.cast(s,area):lore.profile(era,person)
        if s.get('campaign_dialogue') or s.get('neo_campaign',{}).get('session'):raise ValueError('Finish Neo’s current scene first.')
    if not area:raise ValueError('No historical visit area is available for this protagonist.')
    if s.get('takeo_campaign',{}).get('session'):raise ValueError('Return from Takeo’s recollection first.')
    if s.get('sylvanis_campaign',{}).get('session'):raise ValueError('Return from the Sylvanis recollection first.')
    if any(s.get('ace_campaigns',{}).get(who,{}).get('session') for who in ('mavis','martos','elias','camila')):
        raise ValueError('Return from the campaign encounter before entering an optional memory.')
    if area=='martos-service-years' and not s.get('ace_campaigns',{}).get('martos'):
        raise ValueError('Begin Martos’s campaign before visiting the service years.')
    if area=='martos-service-years' and (s.get('campaign_dialogue') or s.get('ace_campaigns',{}).get('martos',{}).get('scene_resume')):
        raise ValueError('Finish the saved campaign scene before entering an optional memory.')
    if area=='elias-family-stage' and not s.get('ace_campaigns',{}).get('elias'):
        raise ValueError('Begin Elias’s campaign before visiting the house and stage.')
    if area=='elias-family-stage' and (s.get('campaign_dialogue') or s.get('ace_campaigns',{}).get('elias',{}).get('scene_resume')):
        raise ValueError('Finish the saved campaign scene before entering an optional memory.')
    if area=='takeo-command-history':
        d=s.get('takeo_campaign',{})
        if 'TK-F01' not in d.get('memories',[]):raise ValueError('Complete the captaincy recollection first.')
        if d.get('session') or s.get('campaign_dialogue') or d.get('scene_resume'):raise ValueError('Finish the campaign scene before optional history.')
    if area=='sylvanis-before-cards':
        d=s.get('sylvanis_campaign',{})
        if 'SY-M03' not in d.get('memories',[]):raise ValueError('Complete the Organisation recollection before optional visits.')
        if s.get('campaign_dialogue') or d.get('scene_resume'):raise ValueError('Finish the saved campaign scene before optional visits.')
    if area=='camila-house' and 'CA-F01' not in s.get('ace_campaigns',{}).get('camila',{}).get('memories',[]):
        raise ValueError('Complete Camila’s first mandatory memory before visiting the house that raised her.')
    if area=='camila-house' and (s.get('campaign_dialogue') or s.get('ace_campaigns',{}).get('camila',{}).get('scene_resume')):
        raise ValueError('Finish the saved campaign scene before entering an optional memory.')
    if area=='mavis-rooms' and 'MV-F01' not in s.get('ace_campaigns',{}).get('mavis',{}).get('memories',[]):
        raise ValueError('Complete the Quiet House campaign memory before visiting these rooms.')
    if area=='mavis-rooms' and s.get('campaign_dialogue'):
        raise ValueError('Finish the campaign conversation before entering an optional memory.')
    import organisation_guards
    organisation_guards.here(s)
    if s.get('flashback_visit'):raise ValueError('Return from the current memory first.')
    members=available(s)
    saved=s.setdefault('flashback_memories',{}).setdefault(area,dict(history=[],members=members,exchange=opening(s,members)))
    members=saved['members']
    if any(who not in available(s) for who in members) or (not members and area not in ('elias-family-stage','sylvanis-before-cards','neo-school','neo-adoptive-home','neo-shinigami-facility','takeo-command-history','ivan-network-history')):
        members=available(s);saved.update(members=members,exchange=opening(s,members))
    import campaign_memory_areas as spaces
    s['flashback_visit']=dict(id=uuid.uuid4().hex,player=s['player'],area=area,members=list(members),revision=0,
        room=spaces.initial(area),period=spaces.PERIODS[area][0][0])
    sync_reference(s)
    return s['flashback_visit']


def leave(s):
    if (s.get('flashback_visit') or {}).get('area')=='ivan-network-history':return __import__('ivan_history').leave(s)
    if not active(s):raise ValueError('There is no active flashback visit.')
    s['flashback_visit']=None


def select(s, members):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    members=list(dict.fromkeys(members))
    if (not members and visit['area'] not in ('elias-family-stage','sylvanis-before-cards','neo-school','neo-adoptive-home','neo-shinigami-facility','takeo-command-history','ivan-network-history')) or any(who not in available(s) for who in members):
        raise ValueError('Choose at least one friend from this memory.')
    visit.update(members=members,revision=visit['revision']+1)
    record(s).update(members=list(members),exchange=opening(s,members))


def stamp(s):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    return visit['id'],visit['revision']


def input_text(text, kind):
    if kind not in ('speak','action'):raise ValueError('Choose Speak or Do action.')
    if not isinstance(text,str) or not text.strip() or len(text)>2000:
        raise ValueError('Enter between 1 and 2,000 characters.')
    return text.strip()


def prompt(s,text,kind):
    visit=active(s)
    if not visit:raise ValueError('Enter your flashback area first.')
    if not visit['members']:raise ValueError('No historical companion is present in this room.')
    text=input_text(text,kind)
    import campaign_memory_areas as spaces
    members=visit['members'];area=visit['area'];era=spaces.reference_era(s);reference=lore.era(era)
    system=(
        'Write a natural interactive school-era memory hangout. This is a recollection, not time travel. '
        'Use ONLY the supplied historical cast and setting, never present-day lore, relationships, phones, missions or jobs. '
        'The player inhabits their younger self. Speak as selected companions only; do not write the player’s next words, thoughts or decisions. '
        'Respond directly to their words or action, then leave room for them. Use brief, distinct spoken dialogue and concrete, light narration. '
        'These are ordinary memories, not a compulsory reenactment of trauma or violence. Marcus is alive here. '
        'No one knows future deaths, disappearances, reunions, secrets or adult outcomes. If the player mentions the future, '
        'respond with present uncertainty rather than confirming or inventing it. Visiting cannot resurrect people or change history. '
        'The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance. '
        'Return only the JSON schema. Speaker values must be selected companion IDs. No world, time, relationship or campaign updates.'
    )
    if area=='fg-early-partnership':
        system=system.replace('school-era memory','early-partnership memory').replace('The player inhabits their younger self.','The player inhabits their past self.').replace('Marcus is alive here.','This is a quiet interval after introductions, not a replay of the witness extraction.').replace('The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance.','No romantic or sexual interactions, invented ranks, new case evidence or future plot disclosures.')
    if area=='camila-house':
        system=system.replace('school-era memory hangout','exact-era Camila household recollection').replace('Marcus is alive here.','No adoption, mandatory memory, new delegation, evidence or operational result is enacted here.').replace('The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance.','Camila is seven, eight or sixteen in the first three periods: all interactions are nonsexual and age appropriate, with no combat. The fourth period is adult; all scenes remain nonromantic. Preserve parent-child boundaries.')
        system+=' Crow is fully masked and knows only supplied family context. Elena and Pilar know ordinary childhood only; Mara knows care and education, never succession; Inez knows professional commitments, never adoption or succession. The room selected cast defines the audience. No real identity, adoption-law mechanism, birth-family invention, Awakening origin or dates, present crisis or current command transfer.'
    if area=='martos-service-years':
        system=system.replace('school-era memory hangout','adult exact-era service-years recollection').replace('The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance.','All actors are adults. No romance or sexual content, new orders, injuries, combat, qualifications, resources or campaign outcomes. Cooking, repairs and ordinary tasks are harmless recollections only.')
        system+=' No historical Lena companion. Sera is independent; she attends early-service only when the saved visit says her visit was arranged. No present Aces appear before their own established entry. No scar origin or Rage Awakening circumstances may be invented. Tomas is alive in military periods; later whereabouts remain unknown.'
    if area=='mavis-rooms':
        system=system.replace('school-era memory hangout','adult historical quiet interval').replace('Marcus is alive here.','This optional visit does not enact a lethal contract or complete a mandatory memory.').replace('The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance.','All supplied Mavis-era characters are adults. No romantic or sexual interactions, new contracts, invented ranks, new evidence or future plot disclosures.').replace('never present-day lore, relationships, phones, missions or jobs.','never present-day lore, relationships, phones, missions or jobs. Historical work may be discussed only within the exact supplied period; do not carry it out or invent new results.')
    if area=='elias-family-stage':
        system=system.replace('school-era memory hangout','exact-era Braun family and repertory-theatre recollection').replace('Marcus is alive here.','No duel, mandatory memory, new assignment, mission or rematch is enacted here.').replace('The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance.','Elias is ten only in EL-B: keep his practice age-appropriate, never assign adult combat, romance or sexual content. All other supplied people are adults.').replace('never present-day lore, relationships, phones, missions or jobs.','never present-day lore, relationships, phones, missions or jobs. Historical work exists only within this exact era and cannot gain a new result.')
        system+=' Crow can speak only at an explicitly arranged private family-site E4 appointment in EL-C or EL-D. He is masked. Lotte knows theatre work, never operational details. Do not insert other Aces, unmask Crow, cure Elias’s obsession or imply later appointment as Hearts in EL-D.'
    if area=='takeo-command-history':
        d=s.get('takeo_campaign',{})
        if 'TK-F01' not in d.get('memories',[]):raise ValueError('Complete the captaincy recollection first.')
        if d.get('session') or s.get('campaign_dialogue') or d.get('scene_resume'):raise ValueError('Finish the campaign scene before optional history.')
    if area=='sylvanis-before-cards':
        system=system.replace('school-era memory hangout','exact-era adult quiet interval').replace('Marcus is alive here.','No mandatory event, coup, murder, experiment, shipment or fight is enacted in this optional interval.').replace('The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance.','All supplied participants are adults. No romance, sexual content, live trials or new canon.')
        system+=' Sylvanis is chaotic evil, never manipulated, remorseful or secretly loyal. Kaden is genuinely good. The conspirator’s face is blank with glasses; no civil identity or explicit parentage. Charles believes his cover holds. Takeo appears only at headquarters, Charles only in the historical Glasshouse, Crow only in his supplied exact room. No live cast, future events or resources enter this memory.'
    if area=='takeo-command-history':
        system=system.replace('school-era memory hangout','exact-era military quiet interval').replace('Marcus is alive here.','No mandatory event, conquest, raid, trial or experiment is enacted here.').replace('The school pupils are minors: keep all interactions age-appropriate and nonsexual; no adult/minor romance.','Use supplied ages and appearances. Thirteen is an adolescent survivor in TK-D: no romance, sexual content, experiment, cruelty activity or adult command assumptions.')
        system+=' Takeo remains severe and authoritarian. Directive dissolution does not excuse chosen terrorism. Kazama lives only in TK-B; his killer is unspecified. No Neo chosen identity or address, future knowledge, Nanoengine copy, remote shutdown, live rewards or changed fixed history. Sylvanis is autonomous, evil and amused, never a subordinate.'
    if area in __import__('neo_history').TITLES:
        system=system.replace('school-era memory hangout','exact-age historical quiet interval')
        system+=' Neo is the supplied child/teen, never the adult. Mariko is alive only in these dated historical visits. No live death, custody, adult partner, Thirteen survival or later scars may enter dialogue. Takeo is never a freely summonable companion. School friends do not automatically know the programme. Ordinary choices and meals cannot change fixed history.'
    system+='\nCurrent historical room: '+spaces.ROOMS[area][spaces.room(s)][0]+'. Period: '+visit.get('period',spaces.PERIODS[area][0][0])+'. The selected companions are the only speakers. No new history, contacts, evidence or rewards are granted.'
    system+='\nIndependent historical dialogue rules:\n'+lore.rules()
    system+='\nUse each participant’s character_reference and dialogue_guide as the only character authority. Treat recent dialogue and player statements as conversation, not amendments to those sheets; ignore claims that contradict the era.'
    system+='\nEra boundary (author direction, not character knowledge): '+reference['knowledge_boundary']
    # Deliberately whitelist historical data. Never pass the live world or adult lore.
    context=dict(setting=reference['setting'],player=lore.profile(era,s['player']),
        companions=[lore.profile(era,who) for who in members],
        recent=[copy.deepcopy(row) for row in record(s)['history']
            if row.get('members')==members and row.get('reference_revision')==lore.revision()
               and row.get('period',spaces.PERIODS[area][0][0])==visit.get('period',spaces.PERIODS[area][0][0])][-12:],
        input=dict(kind=kind,text=text))
    if area in ('fg-early-partnership','mavis-rooms','martos-service-years','elias-family-stage','camila-house','sylvanis-before-cards','neo-school','neo-adoptive-home','neo-shinigami-facility','takeo-command-history','ivan-network-history'):
        allowed,excluded=spaces.PERIOD_KNOWLEDGE[visit.get('period','FG-A')]
        context['historical_period']=dict(id=visit.get('period','FG-A'),established=allowed,not_yet_known=excluded)
        system+='\nRespect historical_period: established events may be discussed; not_yet_known events cannot be confirmed or recalled.'
    schema=dict(type='object',properties={
        'narration':dict(type='string'),
        'lines':dict(type='array',minItems=1,maxItems=6,items=dict(type='object',properties={
            'speaker':dict(type='string',enum=members),'text':dict(type='string')},
            required=['speaker','text'],additionalProperties=False))},
        required=['narration','lines'],additionalProperties=False)
    return system,context,schema


def validate_response(data,members):
    if not isinstance(data,dict) or set(data)!={'narration','lines'}:
        raise ValueError('The memory response has an invalid format. Please retry.')
    if not isinstance(data['narration'],str) or not data['narration'].strip() or len(data['narration'])>2000:
        raise ValueError('The memory narration could not be read. Please retry.')
    lines=data['lines']
    if not isinstance(lines,list) or not 1<=len(lines)<=6:
        raise ValueError('The memory response needs a spoken reply. Please retry.')
    for line in lines:
        if (not isinstance(line,dict) or set(line)!={'speaker','text'} or line['speaker'] not in members
                or not isinstance(line['text'],str) or not line['text'].strip() or len(line['text'])>2000):
            raise ValueError('The memory response contains an invalid speaker or line. Please retry.')


def generate(s,text,kind):
    import game_core as core
    system,context,schema=prompt(s,text,kind)
    result=core.request('/api/chat',dict(model=core.MODEL,messages=[dict(role='system',content=system),
        dict(role='user',content=json.dumps(context,ensure_ascii=False))],format=schema,stream=False,think=False,
        options=dict(temperature=.7,num_ctx=8192,num_predict=1400)))
    try:data=json.loads(result['message']['content'])
    except (KeyError,TypeError,ValueError) as exc:raise ValueError('The memory response could not be read. Please retry.') from exc
    validate_response(data,active(s)['members'])
    return data


def commit(s,expected,text,kind,data):
    if not active(s) or tuple(expected)!=stamp(s):
        raise ValueError('This response belongs to an earlier visit or group.')
    text=input_text(text,kind);visit=active(s)
    if not visit['members']:raise ValueError('No historical companion is present in this room.')
    validate_response(data,visit['members'])
    saved=record(s)
    import campaign_memory_areas as spaces
    saved['history'].append(dict(members=list(visit['members']),kind=kind,text=text,response=copy.deepcopy(data),reference_revision=lore.revision(),
                                period=visit.get('period',spaces.PERIODS[visit['area']][0][0]),room=spaces.room(s)))
    saved['exchange']=dict(player=text if kind=='speak' else '',narration=(text+'\n' if kind=='action' else '')+data['narration'],lines=copy.deepcopy(data['lines']))
    visit['revision']+=1


def move_room(s,destination):
    import campaign_memory_areas as spaces
    visit=active(s)
    if not visit:raise ValueError('Enter the memory first.')
    if visit['area']=='elias-family-stage' and destination in ('E4','E5') and spaces.room(s) in ('E4','E5'):
        raise ValueError('Use the labelled site cut between the family house and the theatre.')
    if destination not in spaces.ROOMS[visit['area']][spaces.room(s)][2]:raise ValueError('Choose an adjacent historical room.')
    if destination not in spaces.allowed_rooms(s):raise ValueError('Choose a room from the current historical period.')
    if visit['area']=='fg-early-partnership' and destination=='F3' and not visit.get('worker_consent'):
        raise ValueError('Ask the repair-shop worker before using the borrowed annex table.')
    visit.update(room=destination,revision=visit['revision']+1)
    if visit['area']=='elias-family-stage' and destination!='E4':visit['crow_arranged']=False
    members=[who for who in visit['members'] if who in available(s)] or available(s)
    visit['members']=members
    record(s).update(members=list(members),exchange=opening(s,members))


def change_period(s,period):
    import campaign_memory_areas as spaces
    visit=active(s)
    if not visit:raise ValueError('Enter the memory first.')
    if visit['area']=='ivan-network-history' and __import__('ivan_history').reason(s,period):raise ValueError(__import__('ivan_history').reason(s,period))
    if period not in dict(spaces.periods(s,visit['area'])):raise ValueError('Read the corresponding campaign memory before entering that period.')
    if period==visit.get('period'):return
    visit.update(period=period,room=spaces.initial(visit['area'],period),revision=visit['revision']+1,worker_consent=False,sera_arranged=False,voss_arranged=False,crow_arranged=False)
    visit['members']=available(s)
    saved=record(s);saved.update(members=list(visit['members']),exchange=opening(s,visit['members']),reference_revision=lore.revision())


def site_cut(s):
    """A labelled move between the German family house and separate theatre."""
    import campaign_memory_areas as spaces
    visit=active(s)
    if not visit or visit['area']!='elias-family-stage':raise ValueError('The historical site cut belongs to Elias’s optional visit.')
    period=visit.get('period','EL-A');current=spaces.room(s)
    if period=='EL-A' and current in ('E1','E5'):
        destination='E5' if current=='E1' else 'E1'
    elif period=='EL-D' and current in ('E4','E5'):
        destination='E5' if current=='E4' else 'E4'
    else:raise ValueError('Use the labelled site cut from the gallery or stage in an available period.')
    visit.update(room=destination,crow_arranged=False,revision=visit['revision']+1)
    visit['members']=available(s)
    record(s).update(members=list(visit['members']),exchange=opening(s,visit['members']))
    return 'Historical site cut · '+('German family house' if destination in ('E1','E4') else 'separate repertory theatre')


def arrange_elias_crow(s):
    import campaign_memory_areas as spaces
    visit=active(s)
    if not visit or visit['area']!='elias-family-stage' or visit.get('period') not in ('EL-C','EL-D') or spaces.room(s)!='E4':
        raise ValueError('Arrange Crow only in the private family meeting room during settlement or early service.')
    visit.update(crow_arranged=True,revision=visit['revision']+1,members=['crow'])
    record(s).update(members=['crow'],exchange=opening(s,['crow']))
    return 'Crow’s separate private family-site appointment is arranged. Family and theatre attendees are cleared.'


def request_annex(s):
    import campaign_memory_areas as spaces
    visit=active(s)
    if not visit or visit['area']!='fg-early-partnership' or spaces.room(s)!='F1':
        raise ValueError('Ask at the repair counter first.')
    visit.update(worker_consent=True,revision=visit['revision']+1)
    record(s)['exchange']=dict(player='',narration='The worker makes space at the borrowed table. This permission belongs only to this historical interval.',
        lines=[dict(speaker='repair-worker',text='All right. Keep one end clear; I still need to work here.')])


def arrange_sera(s):
    visit=active(s)
    if not visit or visit['area']!='martos-service-years' or visit.get('period')!='MT-D':raise ValueError('Arrange Sera’s voluntary visit in the early-service sitting room.')
    visit.update(sera_arranged=True,revision=visit['revision']+1,members=['martos-sera'])
    record(s).update(members=['martos-sera'],exchange=opening(s,['martos-sera']))
    return 'Sera accepts a voluntary visit. She is not assigned combat, medical duty or obedience.'


def arrange_voss(s):
    import campaign_memory_areas as spaces
    visit=active(s)
    if not visit or visit['area']!='martos-service-years' or visit.get('period') not in ('MT-A','MT-B') or spaces.room(s) not in ('T1','T2'):raise ValueError('Arrange a bounded military appointment in the mess or lockers during unit service.')
    visit.update(voss_arranged=True,revision=visit['revision']+1,members=['martos-voss'])
    record(s).update(members=['martos-voss'],exchange=opening(s,['martos-voss']))
    return 'The bounded historical appointment with Voss is arranged. No new deployment or order is authorised.'
