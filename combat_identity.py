"""Source-linked combat identities and conservative, save-owned recognition."""
from pathlib import Path
import copy

TIERS={**dict.fromkeys(('sylvanis',),'S+'),**dict.fromkeys(('takeo','crow'),'S'),
       **dict.fromkeys(('ivan','charles'),'A+'),
       **dict.fromkeys(('martos','elias','mavis','camila','garrett','neo','daniel','fox','gordon','rei','thirteen'),'A'),
       **dict.fromkeys(('tyler','samantha','Keisuke Hachimura','emily','alyssa','minsu','valentina'),'B'),'april':'Specialist'}
NAMES=dict(zip(('Ivan Yeun','Martos Cabrera','Elias Braun','Mavis Kuro','Camila Lopez','Charles Han','Garrett Han','Rei Takamura','Neo','Thirteen','Daniel Stevens','Edward Fox','Jeremy Gordon','Tyler Harding','Samantha Kim','Keisuke Hachimura','Emily Fields','Alyssa','Minsu Park','Valentina Yeun','April Xu','Joseph Richter'),
               ('ivan','martos','elias','mavis','camila','charles','garrett','rei','neo','thirteen','daniel','fox','gordon','tyler','samantha','Keisuke Hachimura','emily','alyssa','minsu','valentina','april','Joseph Richter')))
SOURCE='roadmap/COMBAT_CHARACTER_LORE.md'
LORE={}
for line in (Path(__file__).parent/SOURCE).read_text(encoding='utf-8').splitlines():
    columns=[x.strip() for x in line.split('|')]
    if len(columns)==6 and columns[1] in NAMES:
        LORE[NAMES[columns[1]]]=dict(title=columns[2],reputation=columns[3],presence=columns[4])
LORE.update(sylvanis=dict(title='The Crazed Demon',reputation='The most feared being on the planet.',presence='Complete predictive martial pressure; reputation never forces fear.'),
            takeo=dict(title='The Human Siege Engine',reputation='Capable of destroying army platoons alone.',presence='Overwhelming reinforced physical pressure; no invented completed battles.'),
            crow=dict(title='The Crow',reputation='An enigmatic apex combatant; personal identity unknown.',presence='Analysis and martial mastery; no invented civilian identity.'))


def sheet(who,p=None):
    from combat_profiles import make
    from game_core import CONTACTS
    p=p or make(who); info=LORE.get('Joseph Richter' if p.get('boss')=='richter' else who,{})
    tier=p.get('arena_band') or p.get('combat_band') or (('C' if p['stats']['martial_skill']>=60 else 'D') if p.get('guard_kind') and not p.get('boss') else None) or ('Low A' if p.get('boss')=='richter' else TIERS.get(who,'Unranked'))
    return dict(id=who,name=CONTACTS.get(who,(who,))[0] if p['name']==who else p['name'],tier=tier,title=info.get('title','Unestablished'),
        reputation=info.get('reputation','No established reputation.'),presence=info.get('presence','Use authored personality; do not invent fame.'),
        ability=(p.get('trait') or {}).get('description',p.get('abilities') or 'No established supernatural ability.'),
        forms=[x for x in (p.get('form'),'Shinigami Protocol' if who in ('neo','thirteen') else None) if x],
        tactics=('Observe and support allies; avoid isolated direct exchanges.' if who=='april' else
                 'Use observed patterns and counters.' if who in ('crow','camila','neo','sylvanis') else
                 'Close distance and suppress movement.' if who in ('takeo','martos','thirteen','daniel') else
                 'Manage range, resources and known techniques.'),
        range='ranged' if who in ('gordon','valentina','ivan') else 'close or learned-technique range',
        limits='No omniscience or guaranteed results. Perception does not remove movement travel time. '+(p.get('trait') or {}).get('description',''),
        assumptions='Healthy solo baseline. Assess forms, preparation, equipment and coordinated groups separately; arena rank is competitive position.',
        restraint='Sparring uses explicit restraint; practice is not proof of full-strength superiority.',
        matchups='Tier guides baseline assessment; range, resources and observed tactics can change individual results.',
        sources=[SOURCE,'COMBAT_WINDOW_UPDATE_PLAN.md','roadmap/COMBAT_ABILITY_DEFINITIONS.md','combat_profiles.py'],
        actions=[m['id'] for m in p.get('moveset',{}).get('unique',[])])


def recognised(s,listener,who):
    if listener==who: return True
    if s.get('combat',{}).get('recognition',{}).get(listener,{}).get(who,{}).get('identity'): return True
    import interpol
    if interpol.known_identity(s,listener,who): return True
    if who in ('martos','elias','mavis','camila'):
        import four_aces
        return four_aces.knows_identities(s,listener)
    # The posted ring champion is public in the ring, not an identity reveal
    # about his clan or any other private history.
    if who=='rei' and s.get('world',{}).get('location')=='iron_circle': return True
    return False


def known_title(s,listener,title):
    """Operational reputation can be known without identifying a civilian."""
    return title in s.get('combat',{}).get('known_titles',{}).get(listener,[])


def learn_title(s,listeners,title,source):
    if title not in {v['title'] for v in LORE.values()} or not source:
        raise ValueError('Use an established title and an authored evidence source.')
    d=s.setdefault('combat',{})
    for listener in listeners:
        rows=d.setdefault('known_titles',{}).setdefault(listener,[])
        if title not in rows: rows.append(title)
        d.setdefault('title_sources',{}).setdefault(listener,{})[title]=str(source)


def public(s,who,listeners,p=None):
    record=sheet(who,p)
    if not listeners or not all(recognised(s,x,who) for x in listeners):
        return dict(name=record['name'],title='',reputation='',presence='Only describe observed actions; civilian identity does not disclose an operational title.')
    return {key:record[key] for key in ('name','title','reputation','presence')}


def public_titles(s,listeners):
    if not listeners: return []
    return [dict(title=info['title'],reputation=info['reputation']) for info in LORE.values()
            if all(known_title(s,x,info['title']) for x in listeners)]


def observe(s,listener,who,action):
    # Witnessing a move teaches the move, never an undisclosed identity or origin.
    entry=s.setdefault('combat',{}).setdefault('recognition',{}).setdefault(listener,{}).setdefault(who,{})
    seen=entry.setdefault('observed_actions',[])
    if action not in seen: seen.append(action)


def all_sheets(s=None):
    import game_core,organisation_guards,town,town_residents
    from combat_profiles import make
    roster=set(game_core.CONTACTS)|set(TIERS)|set(town_residents.RESIDENTS)
    roster.update(row[0] for row in (*town.NPCS,*town.VENUE_STAFF.values(),town.HQ_EXECUTIVE))
    result={who:sheet(who) for who in roster}
    if s:
        for who,p in s.get('combat',{}).get('profiles',{}).items(): result[who]=sheet(who,p)
        for kind in organisation_guards.TYPES:
            result['guard:'+kind]=sheet('guard:'+kind,organisation_guards.profile(s,kind))
    return result

def ability_details(p):
    """Player-facing mechanical contract alongside canon, not unreleased prose."""
    import combat_states as st
    parts=[(p.get('trait') or {}).get('name','No named Trait'),
           (p.get('trait') or {}).get('description',p.get('abilities',''))]
    if st.trait(p,'Shinigami Protocol'):
        parts.append('Activate after 4 meaningful varied exchanges against a credible opponent, or 3 under pressure below 60% health: 20 stamina, 4 complete exchanges, then 2 exchanges of reduced stamina recovery. Normal action costs apply. One use until an hour of genuine rest; restarting a fight does not restore it. Observed repetition improves reactive defence; movement and choices remain physically bounded. Neo favours economical interceptions; Thirteen adds suppression at +2 stamina per offensive action. You retain move selection.')
    if st.trait(p,'War God'):
        parts.append('Successful varied damaging moves build Engaged / Flowing / Dominant momentum (1–3). Each level adds 6% pressure. Contact coordination stabilises stance; combinations cost +3 stamina. At Dominant, a break or counter costs +10 stamina, adds 30% force and consumes momentum. Separation or decisive disruption decays a level.')
    if st.channels(p):
        parts.append('Switch channel: 8 mana; active channel: +4 mana per action. Red lightning: +22% strike force. Blue: faster approach and evasive movement. Fire: +12% physical force and structural breach. Ice: Tranquility removes reaction latency but retains approach travel time. Wind: 22% soul component partly avoids physical reinforcement; cover and active guard still protect. Soul injury reduces mana recovery; robotic bodies have no soul component. Only Conduit has all five channels; Deathwind has wind only.')
        parts.append('Misanthropy: 18 mana, once per encounter, lasts 4 exchanges. A finite reserve of 18% maximum health allows continued function while damage debt accumulates. No healing occurs; exceeding the reserve or ending with injury debt incapacitates the fighter.')
    if st.trait(p,'True Sight'):
        parts.append('Mana-flow perception improves precision, physical application and feasible reactions. Paid technique mana is multiplied by 0.65 after refinement, with a minimum of 1; channel upkeep remains separate. Form upkeep is not waived. Physical approach time and finite energy remain.')
    if st.trait(p,'Analysis'):
        parts.append('Observed exchanges supply fine-detail patterns. Once observed, precision and adaptation apply; repeated known incoming actions become easier to read. Branches remain uncertain; no hidden next-action access.')
    parts.append('Counters need an incoming attack and sufficient reach. Guard, cover, movement and interruptions can change outcomes. Repeated restraint/stagger cannot bypass the three-exchange resistance window. Sparring output is explicitly restrained. Reputation never adds a damage or fear modifier.')
    return '\n\n'.join(parts)
