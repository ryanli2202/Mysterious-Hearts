"""MH-017 existing-route room/period staging delivered with MH-016.

New proposed named peers/shopkeepers are not promoted into canon. These areas
use the existing cast plus the already-authored unnamed repair-shop worker.
"""
ROOMS={
 'mavis-rooms':{
  'M1':('Quiet House landing','locations/mavis-quiet-house-landing',('M2',),('mavis','mavis-broker')),
  'M2':('Quiet House common room','locations/mavis-quiet-house-common',('M1','M3','M4'),('mavis','mavis-broker')),
  'M3':('Quiet House repair corner','locations/mavis-quiet-house-repair',('M2',),('mavis','mavis-broker')),
  'M4':('Quiet House handler office','locations/mavis-quiet-house-office',('M2',),('mavis','mavis-broker')),
  'M5':('Early-service receiving room','locations/interiors/syndicate_hq/security_foyer',('M6',),('mavis','crow','sylvanis')),
  'M6':('Early-service terrace','locations/mavis-early-service-terrace',('M5',),('mavis','crow','sylvanis'))},
 'school':{
  'R1':('Courtyard bench','locations/rei-high-school',('R2','R3','R4'),('rei','emily','sophie','marcus')),
  'R2':('Art classroom','locations/campaign-school-art',('R1',),('rei','marcus')),
  'R3':('Model garden','locations/campaign-school-garden',('R1',),('rei','emily','sophie')),
  'R4':('Sports-ground edge','locations/campaign-school-track',('R1',),('rei','emily','sophie'))},
 'hong-kong-school':{
  'G1':('School gate','locations/garrett-hong-kong-school',('G2',),('garrett','charles')),
  'G2':('Side street','locations/campaign-hk-street',('G1','G3'),('garrett','charles')),
  'G3':('Neighbourhood noodle counter','locations/campaign-hk-noodles',('G2','G4'),('garrett','charles')),
  'G4':('Back table','locations/campaign-hk-noodles',('G3',),('garrett','charles'))},
 'fg-early-partnership':{
  'F1':('Repair counter','locations/campaign-annex-counter',('F2',),('fox','gordon','repair-worker')),
  'F2':('Covered lane','locations/blackhaven',('F1','F3'),('fox','gordon')),
  'F3':('Annex table','locations/campaign-annex-table',('F2','F4'),('fox','gordon','repair-worker')),
  'F4':('Kettle alcove','locations/campaign-annex-kettle',('F3',),('fox','gordon'))},
}
PERIODS={
 'mavis-rooms':(('MV-QH20','Quiet House · age twenty','MV-F01'),
                ('MV-R20','Provisional service · age twenty','MV-F03'),
                ('MV-S23','Early service · age twenty-three','MV-F05')),
 'school':(('school-break','The courtyard years',None),),
 'hong-kong-school':(('after-school','After the last bell',None),),
 'fg-early-partnership':(('FG-A','Introductions complete',None),
                         ('FG-B','Learning to work together','FM03'),
                         ('FG-C','A report with both names','FM04')),
}
PERIOD_KNOWLEDGE={
 'MV-QH20':('The Quiet House contract has been offered; prior ordinary transactions and the current fee terms may be discussed.','The predecessor has not yet died in this interval. Recruitment, promotion, Sylvanis collaboration and the present auction are unknown.'),
 'MV-R20':('The predecessor is dead and Mavis accepted provisional service after the authorised headquarters summons.','Promotion, lasting allegiance at twenty-one, Sylvanis collaboration and the present auction have not happened.'),
 'MV-S23':('Recruitment and promotion are past. A narrowly bounded first substantial Sylvanis collaboration is established.','Present archive purchase, auction, completed campaign outcomes and unconfirmed Ace tenures are unknown.'),
 'FG-A':('Their doorway disagreement and the accurate account/appointment afterward are past events.','The later carrier-versus-witness dispute and failed-operation debrief have not happened.'),
 'FG-B':('They protected the witness, lost an unproven lead and argued afterward about explanation and cost.','The later failed-operation debrief and report with both names have not happened.'),
 'FG-C':('The failed attempt, shared-account debrief, practical communication limits and ordinary equipment task are past events.','No present-day Interpol cases, Ace identities or Crow outcomes are known.'),
}


ROOMS['martos-service-years']={
 'T1':('Unit mess','locations/campaign/martos/mess',('T2','T4'),('martos','martos-sera','martos-voss')),
 'T2':('Equipment lockers','locations/campaign/martos/lockers',('T1','T3'),('martos','martos-tomas','martos-voss')),
 'T3':('Training yard','locations/campaign/martos/yard',('T2',),('martos','martos-tomas')),
 'T4':('Unit infirmary','locations/campaign/martos/infirmary',('T1',),('martos','martos-sera')),
 'T5':('Refuge room','locations/campaign/martos/refuge',(),('martos','martos-sera')),
 'T6':('Early-service sitting room','locations/campaign/martos/service_sitting',(),('martos','crow')),
}
PERIODS['martos-service-years']=(('MT-A','Selection and unit life',None),('MT-B','Later deployment','MT-F03'),('MT-C','Refuge','MT-F05'),('MT-D','Early service','MT-F07'))
PERIOD_KNOWLEDGE.update({
 'MT-A':('Selection, team training and the rescue are bounded past events. Sera, Tomas and Voss are known in their military roles.','Later abusive deployments, overmutation injury, desertion, Crow and the Syndicate are unknown.'),
 'MT-B':('The forced removal and conscious guard duty are established culpability. Tomas is known alive.','The disposal order, desertion, fugitive interval and Crow bargain have not happened.'),
 'MT-C':('The disposal order was refused, Sera is wounded and only a limited escape succeeded.','Recruitment, costly Syndicate care, appointment and present companions are unknown.'),
 'MT-D':('The care bargain has been honoured. Recovery and control training take sustained work. Sera remains independent.','Appointment as Clubs and present Northline conflict have not happened. No other present Ace appears.'),
})

ROOMS['elias-family-stage']={
 'E1':('Family gallery','locations/campaign/elias/gallery',('E2','E4'),('elias','elias-johanna','elias-konrad')),
 'E2':('Music room','locations/campaign/elias/music',('E1','E3'),('elias','elias-anja')),
 'E3':('Family kitchen','locations/campaign/elias/kitchen',('E2',),('elias','elias-johanna','elias-konrad')),
 'E4':('Private meeting room','locations/campaign/elias/family_meeting',('E1',),('elias','elias-johanna','elias-konrad','crow')),
 'E5':('Repertory stage','locations/campaign/elias/stage',('E6',),('elias','elias-lotte')),
 'E6':('Dressing room','locations/campaign/elias/dressing',('E5',),('elias','elias-lotte')),
}
PERIODS['elias-family-stage']=(('EL-A','Independent family and theatre · age twenty-three',None),('EL-B','Childhood practice · age ten','EL-F01'),('EL-C','Later affiliate settlement · age twenty-three','EL-F06'),('EL-D','Early service and theatre · age twenty-four','EL-F08'))
PERIOD_KNOWLEDGE.update({
 'EL-A':('Elias is a successful actor, has refused succession, and the Braun family remains independent.','The invasion outcome, Crow defeat, affiliate settlement, Hearts appointment and present breach have not happened.'),
 'EL-B':('Elias is ten. Music, acting and supervised physical practice are real work; Anja and Konrad know only this childhood.','No professional career, adult combat, Crow, Syndicate service, present breach or future defeat.'),
 'EL-C':('The complete defence and later personal defeat are past. Affiliate terms are settled; this is a quiet later interval.','No Hearts appointment, present breakaway compact or other Aces’ histories.'),
 'EL-D':('Elias is twenty-four, serving Crow personally. The acknowledgement has occurred. Lotte knows only theatre work.','No Hearts appointment, present breach or automatic knowledge of Crow or family crime for Lotte.'),
})

ROOMS['camila-house']={
 'C1':('Garden-house common room','locations/campaign/camila/orphanage',('C2',),('camila','camila-elena','camila-pilar')),
 'C2':('Garden-house garden','locations/campaign/camila/garden',('C1',),('camila','camila-pilar')),
 'C3':('Household dining room','locations/campaign/camila/dining',('C4',),('camila','camila-mara','crow')),
 'C4':('Household study','locations/campaign/camila/study',('C3',),('camila','camila-mara','crow')),
 'C5':('Adult receiving appointment','locations/campaign/camila/receiving',('C6',),('camila','camila-inez')),
 'C6':('Private household sitting room','locations/campaign/camila/sitting',('C5',),('camila','crow'))}
PERIODS['camila-house']=(('CA-A','Before departure · seven','CA-F01'),('CA-B','A home · eight','CA-F02'),('CA-C','A correction · sixteen','CA-F04'),('CA-D','Adult protégée · twenty-eight','CA-F08'))
PERIOD_KNOWLEDGE.update({
 'CA-A':('Ordinary garden-house life, Elena and Pilar; a prospective guardian is known but is not present in optional visits.','No adoption reenactment, adult role, Syndicate, succession, birth-family revelation or present crisis.'),
 'CA-B':('Camila has a home and a masked adoptive father, and Mara teaches her.','No adult roles, adolescent exercise, awakening origin, succession or later crisis.'),
 'CA-C':('Camila is sixteen and has practised correcting an evidence-based inference.','No adult appointment, twenty-six heir conversation or current crisis; no invention of an Awakening date.'),
 'CA-D':('Camila serves as Diamonds and knows her private family and future intention. Inez knows only her professional counterpart. Crow knows their own private history.','No current Meridian conflict, newly granted authority or cross-recipient disclosure; no current leadership transfer.')})

ROOMS['sylvanis-before-cards']={
 'S1':('Organisation courtyard','locations/campaign/sylvanis/compound',('S2',),('sylvanis','kaden')),
 'S2':('Organisation briefing room','locations/campaign/sylvanis/briefing',('S1',),('sylvanis','kaden','conspirator')),
 'S3':('Early Syndicate office','locations/campaign/sylvanis/early_office',(),('sylvanis','crow')),
 'S4':('Historical Glasshouse','locations/campaign/sylvanis/historic_lab',('S5',),('sylvanis','charles')),
 'S5':('Historical arena gallery','locations/campaign/sylvanis/arena',('S4',),('sylvanis',)),
 'S6':('First business appointment','locations/campaign/sylvanis/takeo_meeting',(),('sylvanis','takeo'))}
PERIODS['sylvanis-before-cards']=(('SY-A','Organisation quiet interval','SY-M03'),('SY-B','Early Syndicate','SY-M06'),('SY-C','Later Glasshouse and arena','SY-M09'),('SY-D','First Shinokami arrangement','SY-M10'))
PERIOD_KNOWLEDGE.update({
 'SY-A':('Kaden leads the genuinely protective Organisation. Sylvanis joined for violence.','No coup, Kaden death, card system, drugs, parents murders or future ranks.'),
 'SY-B':('The coup and expansion have occurred. Crow is masked and tolerates Sylvanis.','No drugs, eastern murders, Charles, Takeo deal or present crisis.'),
 'SY-C':('Drugs, arena and eastern murders are past for Sylvanis. Charles believes his cover holds.','Charles does not know Sylvanis knows; no Takeo deal or present crisis; no automatic murder disclosure.'),
 'SY-D':('The first bounded supply agreement at Takeo’s headquarters is established.','No present crisis, direct Crow meeting, territorial betrayal knowledge or automatic other-route disclosure.')})

ROOMS['takeo-command-history']={'T1': ('Directive briefing room', 'locations/campaign/takeo/directive_briefing', ('T2',), ('takeo', 'takeo-deputy')), 'T2': ('Directive equipment room', 'locations/campaign/takeo/directive_equipment', ('T1', 'T3'), ('takeo', 'takeo-medic')), 'T3': ('Directive mess', 'locations/campaign/takeo/directive_mess', ('T2',), ('takeo', 'takeo-deputy', 'takeo-medic')), 'T4': ('Onami command hall', 'locations/campaign/takeo/onami_hall', ('T5',), ('takeo', 'takeo-kazama')), 'T5': ('Onami courtyard', 'locations/campaign/takeo/onami_courtyard', ('T4', 'T6'), ('takeo', 'takeo-kazama')), 'T6': ('Research observation room', 'locations/campaign/takeo/onami_research', ('T5',), ('takeo', 'takeo-researcher')), 'T7': ('Reconstituted command', 'locations/campaign/takeo/early_command', ('T8',), ('takeo', 'takeo-officer')), 'T8': ('Early Shinokami archive', 'locations/campaign/takeo/early_archive', ('T7', 'T9'), ('takeo', 'takeo-researcher')), 'T9': ('Training observation gallery', 'locations/campaign/takeo/early_gallery', ('T8',), ('takeo', 'takeo-officer')), 'T10': ('Post-raid command room', 'locations/campaign/takeo/early_command', ('T11',), ('takeo', 'thirteen')), 'T11': ('First supply reception', 'locations/campaign/takeo/kestrel_reception', ('T10',), ('takeo', 'sylvanis'))}
PERIODS['takeo-command-history']=(('TK-A', 'Directive 0', 'TK-F01'), ('TK-B', 'Onami after 2024', 'TK-F04'), ('TK-C', 'Early Shinokami', 'TK-F06'), ('TK-D', 'After the raid and first agreement', 'TK-F08'))
PERIOD_KNOWLEDGE.update({'TK-A':('Directive 0 captaincy before dissolution.','No dissolution, Onami, 2024 conquest or later family/programme history.'),'TK-B':('Onami allegiance and 2024 conquest; bounded research aspiration.','No 2027 defeat, Kazama death, One, raid or supply deal.'),'TK-C':('2027 defeat and founding; private designation One.','No later raid, escape, Thirteen command, supply deal or current crisis.'),'TK-D':('Raid and first supply agreement. Thirteen survived.','No present command dispute, takeover plan or current outcomes; no Neo address.')})

ROOMS['ivan-network-history']={
 'H1':('Waiting room','locations/campaign/ivan/handover',('H2',),('ivan',)),
 'H2':('Supervised corridor','locations/campaign/ivan/handover_corridor',('H1','H3'),('ivan',)),
 'H3':('Designated practice room','locations/campaign/ivan/handover_practice',('H2',),('ivan',))}
# First shared entry is the only period with a settled exact-age reference.
PERIODS['ivan-network-history']=tuple((r[0],r[1],r[2]) for r in sorted(__import__('ivan_history').PERIODS,key=lambda row:row[0]!='IV-H05'))
PERIOD_KNOWLEDGE['IV-H05']=('Ivan is eighteen, trained and just traded to the Syndicate as its second Joker.','No future generals, grants, network, present work, signed-order details, finale or invented staff.')

ROOMS.update(__import__('neo_history').ROOMS)
PERIODS.update(__import__('neo_history').PERIODS)
PERIOD_KNOWLEDGE.update({'SCHOOL':('Three boys sixteen, established friends.','No present attack, custody, adult relationship or raid revelation.'),'HOME-A':('Neo twelve, Mariko thirty-nine; home after protected care.','No later home/school events, death, parentage disclosure or Thirteen survival.'),'HOME-B':('Neo sixteen, Mariko forty-three; settled home and friendship.','No adult partnership, present attack or Thirteen survival.'),'FACILITY':('Children ten and alive before the raid.','No raid, deaths, escape, names, adoption, future scars or adult command.')})

ROOMS['takeo-command-history']={'T1': ('Directive briefing room', 'locations/campaign/takeo/directive_briefing', ('T2',), ('takeo', 'takeo-deputy')), 'T2': ('Directive equipment room', 'locations/campaign/takeo/directive_equipment', ('T1', 'T3'), ('takeo', 'takeo-medic')), 'T3': ('Directive mess', 'locations/campaign/takeo/directive_mess', ('T2',), ('takeo', 'takeo-deputy', 'takeo-medic')), 'T4': ('Onami command hall', 'locations/campaign/takeo/onami_hall', ('T5',), ('takeo', 'takeo-kazama')), 'T5': ('Onami courtyard', 'locations/campaign/takeo/onami_courtyard', ('T4', 'T6'), ('takeo', 'takeo-kazama')), 'T6': ('Research observation room', 'locations/campaign/takeo/onami_research', ('T5',), ('takeo', 'takeo-researcher')), 'T7': ('Reconstituted command', 'locations/campaign/takeo/early_command', ('T8',), ('takeo', 'takeo-officer')), 'T8': ('Early Shinokami archive', 'locations/campaign/takeo/early_archive', ('T7', 'T9'), ('takeo', 'takeo-researcher')), 'T9': ('Training observation gallery', 'locations/campaign/takeo/early_gallery', ('T8',), ('takeo', 'takeo-officer')), 'T10': ('Post-raid command room', 'locations/campaign/takeo/early_command', ('T11',), ('takeo', 'thirteen')), 'T11': ('First supply reception', 'locations/campaign/takeo/kestrel_reception', ('T10',), ('takeo', 'sylvanis'))}
PERIODS['takeo-command-history']=(('TK-A', 'Directive 0', 'TK-F01'), ('TK-B', 'Onami after 2024', 'TK-F04'), ('TK-C', 'Early Shinokami', 'TK-F06'), ('TK-D', 'After the raid and first agreement', 'TK-F08'))
PERIOD_KNOWLEDGE.update({'TK-A':('Directive 0 captaincy before dissolution.','No dissolution, Onami, 2024 conquest or later family/programme history.'),'TK-B':('Onami allegiance and 2024 conquest; bounded research aspiration.','No 2027 defeat, Kazama death, One, raid or supply deal.'),'TK-C':('2027 defeat and founding; private designation One.','No later raid, escape, Thirteen command, supply deal or current crisis.'),'TK-D':('Raid and first supply agreement. Thirteen survived.','No present command dispute, takeover plan or current outcomes; no Neo address.')})

def initial(area,period=None):
    if area=='takeo-command-history':return {'TK-A':'T1','TK-B':'T4','TK-C':'T7','TK-D':'T10'}.get(period,'T1')
    if area=='ivan-network-history':return 'H1'
    if area=='takeo-command-history':return {'TK-A':'T1','TK-B':'T4','TK-C':'T7','TK-D':'T10'}.get(period,'T1')
    if area=='sylvanis-before-cards':return {'SY-A':'S1','SY-B':'S3','SY-C':'S4','SY-D':'S6'}.get(period,'S1')
    if area=='camila-house':return {'CA-A':'C1','CA-B':'C3','CA-C':'C4','CA-D':'C5'}.get(period,'C1')
    if area=='elias-family-stage':return 'E5' if period=='EL-D' else 'E1'
    if area=='martos-service-years':return {'MT-C':'T5','MT-D':'T6'}.get(period,'T1')
    return 'M5' if area=='mavis-rooms' and period in ('MV-R20','MV-S23') else next(iter(ROOMS[area]))


def allowed_rooms(s,area=None,period=None):
    visit=s.get('flashback_visit') or {};area=area or visit.get('area');period=period or visit.get('period')
    if area=='takeo-command-history':return {'TK-A':('T1','T2','T3'),'TK-B':('T4','T5','T6'),'TK-C':('T7','T8','T9'),'TK-D':('T10','T11')}[period or 'TK-A']
    if area=='sylvanis-before-cards':return {'SY-A':('S1','S2'),'SY-B':('S3',),'SY-C':('S4','S5'),'SY-D':('S6',)}[period or 'SY-A']
    if area=='camila-house':return {'CA-A':('C1','C2'),'CA-B':('C3','C4'),'CA-C':('C3','C4'),'CA-D':('C5','C6')}[period or 'CA-A']
    if area=='elias-family-stage':return {'EL-A':('E1','E2','E3','E4','E5','E6'),'EL-B':('E1','E2','E3','E4'),'EL-C':('E1','E2','E3','E4'),'EL-D':('E4','E5','E6')}[period or 'EL-A']
    if area=='martos-service-years':return ('T5',) if period=='MT-C' else ('T6',) if period=='MT-D' else ('T1','T2','T3','T4')
    if area=='mavis-rooms':return ('M5','M6') if period in ('MV-R20','MV-S23') else ('M1','M2','M3','M4')
    return tuple(ROOMS.get(area,{}))


def reference_era(s,area=None):
    current=area or (s.get('flashback_visit') or {}).get('area')
    if current in __import__('neo_history').TITLES:
        visit=s.get('flashback_visit') or {};return __import__('neo_history').ERAS[visit.get('period',PERIODS[current][0][0])]
    visit=s.get('flashback_visit') or {};area=area or visit.get('area')
    if area=='ivan-network-history':return 'ivan_handover18'
    if area=='takeo-command-history':
        period=visit.get('period','TK-A');place=room(s)
        return 'takeo_postraid' if period=='TK-D' and place=='T10' else {'TK-A':'takeo_directive','TK-B':'takeo_research','TK-C':'takeo_one','TK-D':'takeo_supply'}[period]
    if area=='sylvanis-before-cards':return {'SY-A':'sylvanis_organisation','SY-B':'sylvanis_expansion','SY-C':'sylvanis_charles','SY-D':'sylvanis_takeo'}[visit.get('period','SY-A')]
    if area=='camila-house':return {'CA-A':'camila_adoption7','CA-B':'camila_home8','CA-C':'camila_correction16','CA-D':'camila_delegation28'}[visit.get('period','CA-A')]
    if area=='elias-family-stage':return {'EL-A':'elias_preinvasion23','EL-B':'elias_childhood10','EL-C':'elias_settlement23','EL-D':'elias_acknowledgement24'}[visit.get('period','EL-A')]
    if area=='martos-service-years':return {'MT-A':'martos_visit_selection','MT-B':'martos_visit_deployment','MT-C':'martos_visit_refuge','MT-D':'martos_visit_service'}[visit.get('period','MT-A')]
    if area=='mavis-rooms':
        return {'MV-QH20':'mavis_rooms_quiet20','MV-R20':'mavis_rooms_recruit20',
                'MV-S23':'mavis_rooms_service23'}[visit.get('period','MV-QH20')]
    return area


def cast(s,area):
    current=ROOMS[area][room(s) or initial(area)][3]
    if area=='elias-family-stage':
        visit=s.get('flashback_visit') or {};period=visit.get('period','EL-A');place=room(s) or initial(area,period)
        if visit.get('crow_arranged') and place=='E4' and period in ('EL-C','EL-D'):return ('elias','crow')
        if period=='EL-B':return {'E1':('elias','elias-konrad'),'E2':('elias','elias-anja'),'E3':('elias','elias-konrad'),'E4':('elias','elias-konrad')}[place]
        if period=='EL-C':return tuple(who for who in current if who not in ('crow','elias-anja','elias-lotte'))
        if period=='EL-D':return ('elias','elias-lotte') if place in ('E5','E6') else ('elias',)
        return tuple(who for who in current if who not in ('crow','elias-anja'))
    if area=='martos-service-years' and (s.get('flashback_visit') or {}).get('period','MT-A') in ('MT-A','MT-B'):
        return tuple(who for who in current if who!='martos-voss' or (s.get('flashback_visit') or {}).get('voss_arranged'))
    if area=='martos-service-years' and (s.get('flashback_visit') or {}).get('period')=='MT-D':return ('martos','martos-sera') if (s.get('flashback_visit') or {}).get('sera_arranged') else ('martos','crow')
    if area=='mavis-rooms':
        return ('mavis',{'MV-QH20':'mavis-broker','MV-R20':'crow','MV-S23':'sylvanis'}[(s.get('flashback_visit') or {}).get('period','MV-QH20')])
    return current


def periods(s,area):
    if area=='takeo-command-history':
        seen=s.get('takeo_campaign',{}).get('memories',[])
        return [(key,title) for key,title,gate in PERIODS[area] if gate in seen]
    if area in __import__('neo_history').TITLES:
        seen=s.get('neo_campaign',{}).get('memories',[]);return [(key,title) for key,title,gate in PERIODS[area] if gate is None or gate in seen]
    if area=='ivan-network-history':return [(row[0],row[1]) for row in __import__('ivan_history').PERIODS if not __import__('ivan_history').reason(s,row[0])]
    if area=='takeo-command-history':
        seen=s.get('takeo_campaign',{}).get('memories',[])
        return [(key,title) for key,title,gate in PERIODS[area] if gate in seen]
    if area=='sylvanis-before-cards':
        seen=s.get('sylvanis_campaign',{}).get('memories',[])
        return [(key,title) for key,title,gate in PERIODS[area] if gate in seen]
    if area=='camila-house':
        read=s.get('ace_campaigns',{}).get('camila',{}).get('memories',[])
        return [(key,title) for key,title,gate in PERIODS[area] if gate in read]
    if area=='elias-family-stage':
        read=s.get('ace_campaigns',{}).get('elias',{}).get('memories',[])
        return [(key,title) for key,title,gate in PERIODS[area] if gate is None or gate in read]
    if area=='martos-service-years':
        read=s.get('ace_campaigns',{}).get('martos',{}).get('memories',[])
        return [(key,title) for key,title,gate in PERIODS[area] if gate is None or gate in read]
    if area=='mavis-rooms':
        read=s.get('ace_campaigns',{}).get('mavis',{}).get('memories',[])
        return [(key,title) for key,title,gate in PERIODS[area] if gate in read]
    read=__import__('campaign_prose').read(s).get('read',{})
    return [(key,title) for key,title,gate in PERIODS[area] if gate is None or gate in read]


def room(s):
    visit=s.get('flashback_visit') or {};area=visit.get('area')
    if area not in ROOMS:return None
    return visit.get('room') if visit.get('room') in allowed_rooms(s) else initial(area,visit.get('period'))


def background(s):
    visit=s.get('flashback_visit') or {};return ROOMS[visit['area']][room(s)][1]


def activities(s):
    if (s.get('flashback_visit') or {}).get('area')=='takeo-command-history':return ('Discuss the supplied report','Observe the quiet room')
    if (s.get('flashback_visit') or {}).get('area') in __import__('neo_history').TITLES:return __import__('neo_history').activities(s)
    if (s.get('flashback_visit') or {}).get('area')=='ivan-network-history':return ('Observe the room','Practise a harmless wrist turn')
    if (s.get('flashback_visit') or {}).get('area')=='takeo-command-history':return ('Discuss the supplied report','Observe the quiet room')
    if (s.get('flashback_visit') or {}).get('area')=='sylvanis-before-cards':return ('Discuss the supplied ordinary schedule','Look over the room without enacting an event')
    visit=s.get('flashback_visit') or {}
    if visit.get('area')=='camila-house':
        return {'C1':('Play a wooden-counter game','Pack away the game together'),'C2':('Look after a garden pot','Share an ordinary childhood game'),'C3':('Help prepare supper','Show an unfinished paper house'),'C4':('Try a supplied harmless reasoning exercise','Discuss a correction without inventing facts'),'C5':('Discuss a professional appointment','Compare an ordinary receiving schedule'),'C6':('Play a quiet chess game','Discuss a bounded earlier commitment')}[room(s)]
    if visit.get('area')!='elias-family-stage':return ()
    current=room(s)
    return {
        'E1':('Discuss a family programme','Look over the gallery portraits'),
        'E2':('Practice a rhythm','Try a short music phrase'),
        'E3':('Share a meal','Help prepare the meal'),
        'E4':('Discuss a precise appointment','Review an exact service term') if visit.get('crow_arranged') else ('Review an ordinary family matter','Compare a practical note'),
        'E5':('Rehearse a short scene','Work through a stage cue'),
        'E6':('Discuss a costume detail','Review a programme note'),
    }[current]


def initial_topics(s,who):
    if (s.get('flashback_visit') or {}).get('area')=='takeo-command-history':return ('The report in this room','A practical command limit','What the report leaves unanswered')
    if (s.get('flashback_visit') or {}).get('area') in __import__('neo_history').TITLES:return ('An ordinary choice today','A quiet shared task','Something in this room')
    if (s.get('flashback_visit') or {}).get('area')=='takeo-command-history':return ('The report in this room','A practical command limit','What this period does not establish')
    if (s.get('flashback_visit') or {}).get('area')=='sylvanis-before-cards':return ('An ordinary practical limit','The supplied appointment','A detail in this room')
    period=(s.get('flashback_visit') or {}).get('period')
    if period in ('CA-A','CA-B','CA-C','CA-D'):
        return {'camila-elena':('A fair turn','An ordinary afternoon','Packing the game away'),'camila-pilar':('The red counter','A game in the garden','Whose turn begins now'),'camila-mara':('An unfinished project','Time for supper','An ordinary promise'),'camila-inez':('The agreed appointment','A credible receiving time','Work and personal boundaries'),'crow':('A quiet household task','A supplied lesson' if period!='CA-D' else 'A bounded commitment','A game of chess')}[who]
    if period in ('EL-A','EL-B','EL-C','EL-D'):
        return {'elias-johanna':('The gallery accounts','A shared meal','A practical family boundary'),'elias-konrad':('The family programme','A meal together','An ordinary expectation'),'elias-anja':('Piano rhythm','A short rehearsal','Practice after a mistake'),'elias-lotte':('A rehearsal cue','A costume detail','A programme note'),'crow':('The precise appointment','A limited task','The agreed terms')}[who]
    if period in ('MT-A','MT-B','MT-C','MT-D'):
        return {'martos-sera':('A practical limit','A quiet meal','Asking before helping'),'martos-tomas':('A watch mechanism','Checking an ordinary tool','The mess-room kettle'),'martos-voss':('Clarifying a limited order','A training route','A bounded equipment report'),'crow':('A precise undertaking','A training limit','The agreed recovery terms')}[who]
    if period in ('MV-QH20','MV-R20','MV-S23'):
        return {'mavis-broker':('A fee with clear terms','Correcting a route plan','The repaired desk fan'),
                'crow':('Reporting a changed objective','Provisional service terms','A precise return instruction'),
                'sylvanis':('A case and a corridor','An exact practical limit','An independent contribution')}[who]
    if who in ('fox','gordon'):
        return {'FG-A':('The lane observation','An accurate account','A practical follow-up'),
                'FG-B':('Explaining a changed plan','Keeping someone protected','Disagreeing afterward'),
                'FG-C':('Recording your own mistake','A report with both names','An ordinary shared task')}.get(period,('The lane observation','An accurate account','A practical follow-up'))
    return {'marcus':('The stop-motion shot','The cardboard pigeon','An ordinary school frustration'),
            'emily':('The greenhouse windows','Plants to try','Where to sit for lunch'),
            'sophie':('School practice','A friendly challenge','An afternoon together'),
            'rei':('The sketchbook','Film props','A quiet shared task'),
            'charles':('The school day','Walking home','A family meal'),
            'repair-worker':('A harmless repair','Keeping the counter clear','Useful local help')}[who]


def topics(s,who):
    initial=initial_topics(s,who)
    # Refresh suggestions only after a committed conversation in this period.
    # These prompts invite ordinary follow-up without inventing past events.
    history=__import__('flashback_visits').record(s).get('history',[])
    turns=sum(who in row.get('members',[]) for row in history)
    follow=('Something you want to ask','A small task to share','What would help right now')
    pool=initial+follow;offset=turns%len(pool)
    return tuple(pool[(offset+i)%len(pool)] for i in range(3))
