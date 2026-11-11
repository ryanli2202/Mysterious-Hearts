"""Save-owned garrisons and scoped combat. Patrols replenish; campaign victories do not."""
import copy
import uuid

# name, kind, martial art, equipment, power, skill: authored sandbox balance.
TYPES = {
    'yokai': ('Yokai', 'awakened', 'Kyokushin', '', 48, 66),
    'oni': ('Oni', 'robotic', 'Military CQC', 'weapon systems', 46, 64),
    'tengu': ('Tengu', 'unawakened', 'Kyokushin', '', 0, 62),
    'clubs': ('Clubs enforcer', 'awakened', 'Military CQC', 'gun', 50, 68),
    'spades': ('Spades assassin', 'awakened', 'Krav Maga', 'knife', 48, 70),
    'affiliate': ('Affiliate member', 'unawakened', 'MMA', 'gun', 0, 35),
    'headhunter': ('Headhunter', 'cyborg', 'Military CQC', 'weapon systems', 50, 68),
    'seeker': ('Seeker', 'cyborg', 'Krav Maga', 'weapon systems', 44, 64),
    'pmc': ('PMC', 'unawakened', 'Military CQC', 'gun', 0, 34),
    'team9': ('Team 9 specialist', 'awakened', 'Military CQC', 'gun', 52, 70),
    'interpol': ('Interpol protection officer', 'unawakened', 'Military CQC', 'gun', 0, 62),
    'kai_sentinel': ('Kai sentinel', 'awakened', 'Kyokushin', '', 34, 54),
    'kai_guard': ('Kai house guard', 'unawakened', 'Judo', '', 0, 48),
    'lookout': ('Crew lookout', 'unawakened', 'Streetfighting', '', 0, 30),
    'crew_enforcer': ('Crew enforcer', 'awakened', 'MMA', '', 25, 45),
}
APPEARANCES = {
    'kai_sentinel': 'An adult male Hamayashi-kai yakuza sentinel with swept black hair wears a tailored navy suit, open-collar charcoal shirt, leather belt, modest gold lapel pin and watch, and black gloves. Compact gold Awakened energy gathers at one fist. His face is visible; he wears no ninja or martial-arts uniform.',
    'kai_guard': 'An adult female Hamayashi-kai yakuza house guard with hair in a bun wears a tailored navy pantsuit, burgundy open-collar blouse, leather belt, small gold lapel pin and stud earrings. Her face is visible and hands relaxed and ready. She is unawakened and carries no weapon.',
    'yokai': 'An adult muscular male Shinokami yakuza enforcer wears a luxurious black pinstripe suit, burgundy patterned silk shirt, gold necklace, rings, watch and lapel chain. A discreet protective underlayer and communications earpiece complement the tailoring. His face and short dark hair are visible; black fingerless gloves frame compact red Awakened energy. No ninja uniform or handheld weapon.',
    'tengu': 'An adult lean male Shinokami yakuza guard wears a tailored charcoal suit, black silk shirt with muted red floral pattern, silver necklace, rings and watch, pocket square, earpiece and belt radio pouch. Discreet protection sits beneath the suit. His face and short dark hair are visible. He is unawakened, with no magic or handheld weapon.',
    'oni': 'A fully robotic Shinokami yakuza security guard wears a structured black suit jacket with satin lapels, burgundy waistcoat, gold lapel chain, pocket square and trousers adapted to mechanical joints. Its horned oni faceplate, red optics, mechanical hands and integrated forearm weapon systems remain visible. It has no human flesh or human facial expressions.',
    'clubs': 'A black hood covers a full-face black military helmet and mask with a white clubs insignia. An opaque visor conceals the eyes; no face or hair is visible. A bulletproof vest sits under a black jacket with dark green trim. Gloved hands wield a gun and controlled green Awakened energy.',
    'spades': 'A black hooded jacket and full-face black assassin mask with a white spades insignia conceal the entire face, eyes and hair. A layered black cloak, draped cloths, restrained violet accents, straps, buckles and utility accessories frame the silhouette. Gloved hands wield a knife.',
    'affiliate': 'Full-face black military equipment includes a ballistic helmet, opaque goggles, face mask, fatigues, gloves, plate carrier, utility belt and cargo trousers. No face, eyes or hair is visible. The chest bears the Syndicate insignia: fanned playing cards with a skull inside the front ace of spades. The guard wields a gun and is unawakened, with no magical energy.',
}
MASKED_PRESENTATION = ('Keep the full-face mask and head covering on throughout the encounter. '
    'Convey reactions through voice, head turns, stance and gloved gestures; do not describe visible eyes, smiles, lips, cheeks, hair or other facial expressions behind the opaque covering. '
    'Do not invent unmasking, exposed identity, extra equipment or powers. Equipment descriptions do not change combat stats, grant immunity or resolve attacks.')

def appearance_for_profile(profile):
    """Resolve current visual canon, including profiles saved before this refresh."""
    kind=profile.get('portrait') or str(profile.get('combat_id','')).removeprefix('guard:')
    return APPEARANCES.get(kind,'')

def presentation_for(kind):
    if kind in ('clubs','spades','affiliate'):
        return MASKED_PRESENTATION
    return ('Preserve the current tailored yakuza appearance. Accessories and protective clothing do not change combat stats, grant immunity or add weapons or powers. '
            'Oni remains fully robotic; human guards retain visible faces. Do not substitute ninja outfits or martial-arts uniforms.')

LOCATIONS = {
    'hamayashi_annex': 'Hamayashi-kai · riverside annex',
    'hamayashi_store': 'Hamayashi-kai · supply house',
    'blackstone_loading': 'Blackstone · loading compound',
    'blackstone_records': 'Blackstone · research records',
    'blackstone_lab': 'Blackstone · experimental wing',
    'blackstone_command': 'Blackstone · executive command',
}
PROPERTIES = {
    'crew_lot_west': ('Vacant west workshop', 18000, (-340, 580)),
    'crew_lot_docks': ('Vacant dock warehouse', 32000, (1310, 840)),
    'crew_lot_north': ('Vacant northern offices', 24000, (620, -80)),
    'crew_lot_south': ('Vacant south garage', 16000, (290, 1190)),
}
POINTS = dict(hamayashi_annex=(80, 880), hamayashi_store=(70, 1030),
              blackstone_loading=(790, 350), blackstone_records=(790, 310),
              blackstone_lab=(830, 310), blackstone_command=(830, 350))
POINTS.update({k: v[2] for k, v in PROPERTIES.items()})
LOCATIONS.update({k: v[0] for k, v in PROPERTIES.items()})
HAMAYASHI = ('hamayashi_house', 'hamayashi_annex', 'hamayashi_store')
BLACKSTONE = ('blackstone_hq', 'blackstone_loading', 'blackstone_records', 'blackstone_lab', 'blackstone_command')
DEPLOYMENTS = {}
def deploy(faction, sites, types):
    for site in sites: DEPLOYMENTS[site] = (faction, types)
deploy('shinokami', ('site_01','site_02','site_03'), ('yokai','oni','tengu') * 3)
deploy('syndicate', ('site_04','site_05','site_06','site_07','site_08','syndicate_hq','glasshouse_lab'), ('clubs','spades','affiliate') * 2)
deploy('blackstone', BLACKSTONE, ('pmc','seeker','headhunter'))
deploy('hamayashi', HAMAYASHI, ('kai_guard','kai_sentinel'))
deploy('interpol', ('interpol_hq','interpol_briefing','interpol_training','interpol_containment'), ('interpol','team9'))
for faction, site in (('lantern','lantern_house'),('rail','saints_depot'),('purple','purple_clubhouse'),
                      ('rojos','rojos_courtyard'),('waterfront','consortium_house'),('dragons','syndicate')):
    deploy(faction, (site,), ('lookout','crew_enforcer'))
ORGANISATIONS = {
    'shinokami': 'Regional command directs Yokai assault teams, Oni robotic security and Tengu perimeter shifts.',
    'syndicate': 'Suit command deploys Clubs protection, Spades interception and affiliate perimeter teams.',
    'blackstone': 'Richter directs contracted PMC security, Seeker surveillance and Headhunter interception. Research and command are separate secured wings.',
    'interpol': 'Regional officers protect public desks and custody. Team 9 handles Awakened containment, field support and training under Gordon.',
    'hamayashi': 'The successor has house, supply and riverside teams. Its current charter bars child recruitment and coercive training; Rei must investigate that claim.',
}

def data(s):
    d=s.setdefault('organisation_guards', {})
    for k,v in dict(version=1, victories={}, disabled=[], encounter=None, properties={}, types={}, roster=[], history=[]).items():
        d.setdefault(k, copy.deepcopy(v))
    return d

def here(s, venue=None):
    import combat
    combat.guard(s)
    a=s['world']['cast'][s['player']]
    if a.get('journey') or a['location']!=s['world']['location'] or a.get('activity')=='Sleep':
        raise ValueError('Arrive in person and wake up first.')
    if venue and s['world']['location']!=venue: raise ValueError('Travel to the listed location first.')

def slots(s, venue):
    d=data(s); faction, types=DEPLOYMENTS.get(venue, (None, ()))
    if faction in d['disabled']: return []
    result=[dict(id=venue+':'+str(i),type=t,faction=faction,venue=venue) for i,t in enumerate(types)]
    result += [dict(r, faction='custom') for r in d['roster'] if r['venue']==venue]
    return result

def remaining(s, venue, scope='patrol'):
    key=scope+(':'+str(s['world']['minute']//1440) if scope=='patrol' else '')
    won=data(s)['victories'].get(key, [])
    return [r for r in slots(s,venue) if r['id'] not in won]

def cleared(s, venues, scope):
    return all(not remaining(s,v,scope) for v in venues)

def spec(s, kind):
    return TYPES.get(kind) or tuple(data(s)['types'][kind])

def profile(s, kind):
    import combat_profiles, combat_moves
    name, category, art, equipment, power, skill=spec(s,kind)
    p=combat_profiles.make('guard:'+kind, dict(name=name,awakened=category=='awakened',mana_potential=category=='awakened'))
    p['stats'].update(awakened_power=power,martial_skill=skill,fight_iq=skill,trait_refinement=0)
    p['arts']={art:skill}; p['guard_kind']=category
    p['combat_band']='D' if kind in ('affiliate','pmc','kai_guard','lookout') else 'C'
    p['portrait']=__import__('guard_portraits').type_id(s,kind)
    if kind in APPEARANCES:p['appearance']=APPEARANCES[kind]
    p['abilities']=equipment or art
    p.pop('moveset',None); combat_moves.initialise(p,'guard:'+kind)
    if equipment:
        move=combat_moves.spec('equipment:'+kind, equipment.title(), 'Limited bursts or close strikes; cover and evasion remain effective.',
                               kind='equipment',art=art,tags=['reach','precision'] if equipment!='knife' else ['precision'])
        move.update(range=5 if equipment!='knife' else 1,stamina=14,force=1.25)
        p['equipment_moves']=[move]
    return p

def patrol_allies(s):
    """Optional trusted companions already physically present; never mission recruitment."""
    import combat,groups,relationship_dynamics
    result=[]
    for who in sorted(groups.hanging_out_with(s)):
        if who==s['player'] or who in ('crow','sylvanis','takeo','thirteen'): continue
        if relationship_dynamics.stats(s,who).get('trust',0)<60: continue
        try: combat.check_pair(s,who)
        except ValueError: continue
        faction,_=combat.affiliation(s,who)
        defending=DEPLOYMENTS.get(s['world']['location'],(None,))[0]
        if faction and faction==defending: continue
        result.append(who)
    return result


def begin(s, venue=None, scope='patrol', ally=None):
    venue=venue or s['world']['location']; here(s,venue)
    if scope=='patrol' and ally and ally not in patrol_allies(s):
        raise ValueError('A field partner must be a willing trusted companion present in your in-person group, able to fight and not defending this post.')
    rows=remaining(s,venue,scope)
    if not rows: raise ValueError('This deployment is cleared.')
    result=start(s, rows[0]['id'], profile(s,rows[0]['type']), scope, rows[0], ally)
    if scope=='patrol':
        import interpol
        interpol.record_offence(s,'assault',rows[0]['id'])
    return result

def start(s, who, opponent, scope, slot=None, ally=None):
    import combat
    here(s)
    if data(s)['encounter']: raise ValueError('Close the previous encounter first.')
    e=dict(token=uuid.uuid4().hex, who=who, profile=opponent, scope=scope, slot=slot, venue=s['world']['location'])
    data(s)['encounter']=e
    try: f=combat.start(s,who,'guard')
    except Exception:
        data(s)['encounter']=None
        raise
    f['guard_token']=e['token']
    if ally:
        f['ally']=ally; f['ally_profile']=copy.deepcopy(combat.profile(s,ally)); f['ally_resources']=combat.resources(f['ally_profile'])
        __import__('combat_engine').ensure_arena(f)
        f['arena']['positions']['ally']=f['arena']['positions']['player']
    return 'Encounter started. Resolve it in Combat, then close the result to record progress.'

def validate(s,who):
    e=data(s)['encounter']
    if not e or e['who']!=who or e['venue']!=s['world']['location']: raise ValueError('No matching guard encounter.')
    return copy.deepcopy(e['profile'])

def resolve(s,f):
    if f.get('kind')!='guard': return
    d=data(s); e=d['encounter']
    if not e or f.get('guard_token')!=e['token']: return
    d['encounter']=None
    win=f.get('result','').startswith('Victory')
    d['history'].append(dict(scope=e['scope'],venue=e['venue'],won=win,opponent=e['who'],minute=s['world']['minute']))
    if not win:
        __import__('campaign_prose').after_guard(s,e,False)
        return
    key=e['scope']+(':'+str(s['world']['minute']//1440) if e['scope']=='patrol' else '')
    won=d['victories'].setdefault(key,[])
    ident=e['slot']['id'] if e['slot'] else e['who']
    if ident not in won: won.append(ident)
    if e['scope'].startswith('rei:'):
        import rei_story
        rei_story.resolve(s,e)
    narrated=__import__('campaign_prose').after_guard(s,e,True)
    if e['scope'] in ('rei:richter','charles:finale') and not narrated:
        from campaign_dialogue import beat
        lines=([beat('Say it without making an excuse.', 'Joseph Richter', 'I bullied Marcus. I chose to hurt him, and then I pretended it did not matter. I am sorry.', 'The powered frame is silent. Joseph has no weapon left between himself and the question.'),
                beat('And the people you kept here?', 'Joseph Richter', 'I am sorry for what I did to them too.', 'Rei secures the records and disables containment. The participants can leave. An apology does not require forgiveness.')]
               if e['scope']=='rei:richter' else
               [beat('Still think I need you to disappear to keep me safe?', 'charles', 'No. I should have seen you. I kept seeing someone I could lose.', 'Charles lowers his hands. Garrett has won. Return to Find Charles to finish their private reconciliation.')])
        s.setdefault('campaign_epilogues',[]).append(dict(lines=lines,venue=e['venue']))
    refresh(s)

def member(s, faction):
    import combat
    own,_=combat.affiliation(s,s['player'])
    return own==faction or (faction=='interpol' and s['player'] in ('fox','gordon'))

def npc_rows(s):
    venue=s['world']['location']; scope='patrol'
    q=s.get('rei_story',{})
    if s['player']=='rei' and q.get('stage',0)>=6:
        if venue in BLACKSTONE: scope='rei:blackstone'
        elif venue in HAMAYASHI and q.get('hamayashi')=='destroy': scope='rei:hamayashi'
    if s['player']=='garrett' and venue in ('site_08','glasshouse_lab'): scope='charles:search'
    return {'Post guard · '+spec(s,r['type'])[0]+' · '+str(i+1): r for i,r in enumerate(remaining(s,venue,scope))}

def refresh(s):
    if 'world' not in s:return
    names=s['world'].setdefault('npcs',[])
    names[:]=[n for n in names if not n.startswith('Post guard · ')]
    names.extend(npc_rows(s))

def npc_detail(s,name):
    row=npc_rows(s).get(name)
    if not row: raise ValueError('That guard is no longer on this post.')
    p=spec(s,row['type'])
    appearance=APPEARANCES.get(row['type'],'')
    return (name,'Unnamed area guard',p[0]+'; '+p[1]+'; '+p[2]+'. '+p[3]+'. '+appearance+' '+(presentation_for(row['type'])+' ' if appearance else '')+'This is a rotating adult guard post, not a named resident. No personal number, romance, secret disclosures or permanent individual identity. Use Stories, guards & gang properties for physical encounters.')

def directory(s):
    return [(venue,faction,len(remaining(s,venue)),[spec(s,t)[0] for t in dict.fromkeys(types)])
            for venue,(faction,types) in DEPLOYMENTS.items() if member(s,faction) and faction not in data(s)['disabled']]

def founder(s):
    import custom_gangs
    return custom_gangs.crew(s)

def buy(s, venue, use):
    founder(s); here(s,venue)
    if venue not in PROPERTIES or use not in ('Hideout','Affiliate'): raise ValueError('Choose a vacant site and its purpose.')
    d=data(s)
    if venue in d['properties']: raise ValueError('This property is already owned.')
    price=PROPERTIES[venue][1]
    if s['world']['money']<price: raise ValueError('Insufficient funds.')
    s['world']['money']-=price
    d['properties'][venue]=dict(use=use,owner=s['job_apps']['gang']['name'],paid=price)
    return 'Purchased '+PROPERTIES[venue][0]+' as '+use+'.'

def recruit(s, name, category, venue):
    crew=founder(s); here(s,venue)
    d=data(s); name=name.strip()
    if venue not in d['properties']: raise ValueError('Buy this property first.')
    if d['properties'][venue]['owner']!=crew['name']: raise ValueError('This property belongs to your former crew.')
    if category not in ('awakened','unawakened','robotic'): raise ValueError('Choose a guard category.')
    if not 3<=len(name)<=40 or any(ord(c)<32 for c in name): raise ValueError('Use a guard type name of 3–40 printable characters.')
    if len([r for r in d['roster'] if r['venue']==venue])>=12: raise ValueError('This site has twelve guard positions.')
    cost={'awakened':6000,'unawakened':1500,'robotic':9000}[category]
    if s['world']['money']<cost: raise ValueError('Insufficient funds for recruitment.')
    key='custom:'+crew['name'].casefold()+':'+category+':'+name.casefold()
    d['types'][key]=[name,category,'MMA','weapon systems' if category=='robotic' else '',0 if category=='unawakened' else 40,52]
    s['world']['money']-=cost
    d['roster'].append(dict(id=uuid.uuid4().hex,type=key,venue=venue))
    return name+' stationed here. Cost $'+str(cost)+'.'

def station(s, ident, venue):
    crew=founder(s); here(s,venue)
    d=data(s)
    if venue not in d['properties']: raise ValueError('Buy the destination first.')
    if d['properties'][venue]['owner']!=crew['name']: raise ValueError('The destination belongs to another crew.')
    r=next((r for r in d['roster'] if r['id']==ident),None)
    if not r: raise ValueError('Choose one of your guards.')
    if d['properties'][r['venue']]['owner']!=crew['name']: raise ValueError('That guard belongs to your former crew.')
    if sum(r['venue']==venue for r in d['roster'])>=12: raise ValueError('Destination roster is full.')
    r['venue']=venue
    return 'Guard reassigned to this property.'

def rename_type(s,kind,name):
    crew=founder(s); here(s)
    d=data(s); name=name.strip()
    if not 3<=len(name)<=40 or any(ord(c)<32 for c in name): raise ValueError('Use 3–40 printable characters.')
    assigned=[r for r in d['roster'] if r['type']==kind]
    if not assigned or any(d['properties'][r['venue']]['owner']!=crew['name'] for r in assigned):
        raise ValueError('Choose a guard type owned by your current crew.')
    d['types'][kind][0]=name
    return 'Guard type renamed to '+name+'. Existing guards retain their assignments and abilities.'

def check_trip(s,who,destination,passengers=()):
    if destination in BLACKSTONE[1:]:
        q=s.get('rei_story',{})
        if who!=s['player'] or who!='rei' or q.get('stage',0)<6 or passengers:
            raise ValueError('Blackstone interior access requires Rei’s solo investigation.')
        previous=BLACKSTONE[BLACKSTONE.index(destination)-1]
        if not cleared(s,(previous,),'rei:blackstone'): raise ValueError('Defeat every guard in the preceding Blackstone area first.')

def breach(s, key):
    """A cleared perimeter permits inspection, never membership or command authority."""
    return bool(slots(s,key)) and not remaining(s,key)
