"""Hidden adult cast and persistent exploration unlocks."""
import json
import four_aces
import the_crow
import takeo
import thirteen
import charles_han
import interpol_cast

CAST = {
 'lena': dict(name='Lena Ortiz', role='love interest', height=168, age=24, mbti='ENTP', birthday='June 12', hobbies=['film photography', 'urban history', 'salsa'], occupation='Archive conservator', personality='Curious, irreverent and resourceful; deflects praise with wit but values people who follow through.', texting_style='Lowercase, quick questions and dry jokes; sends descriptions of curious finds. Rare camera emoji.', attraction=24, area='archive', area_name='Old town archive', activity='Restoring local photographs', home='Lena’s clocktower flat', interior='Sunlit brick rooms above a clock repair shop, drying photographs and a second-hand record player.'),
 'naomi': dict(name='Naomi Sato', role='love interest', height=175, age=26, mbti='ISTJ', birthday='February 17', hobbies=['bouldering', 'ceramics', 'mystery novels'], occupation='Bicycle mechanic', personality='Grounded, observant and quietly funny. Shows care through practical help; dislikes being rushed into closeness.', texting_style='Short complete sentences, precise plans and understated jokes. Almost no emoji.', attraction=18, area='cycle_shop', area_name='Riverside cycle workshop', activity='Repairing bicycles', home='Naomi’s riverside maisonette', interior='A tidy split-level home with handmade mugs, a climbing hangboard and a balcony herb garden.'),
 'celeste': dict(name='Celeste Moreau', role='love interest', height=172, age=23, mbti='ENFJ', birthday='October 3', hobbies=['jazz piano', 'birdwatching', 'baking bread'], occupation='Planetarium educator', personality='Expressive and attentive with a mischievous streak. Protects quiet time and wants curiosity returned, not constant admiration.', texting_style='Warm sentence case, vivid observations and occasional star emoji. Asks one thoughtful question at a time.', attraction=30, area='planetarium', area_name='Hilltop planetarium', activity='Preparing sky demonstrations', home='Celeste’s blue-door cottage', interior='A little cottage with a piano, bird guides, star maps and a flour-dusted kitchen.'),
 'dev': dict(name='Dev Shah', role='friend', height=181, age=25, mbti='INTP', birthday='December 6', hobbies=['tabletop games', 'electronics repair', 'night photography'], occupation='Community makerspace technician', personality='Inventive, patient and absent-minded; becomes animated when teaching and learns to ask before fixing everything.', texting_style='Lowercase, parenthetical asides and extremely specific recommendations. Occasional nerdy pun, no flirting.', attraction=0, area='makerspace', area_name='Station makerspace', activity='Hosting repair sessions', home='Dev’s station studio', interior='A compact studio with labelled component drawers, board games and an improbably thriving fern.'),
 'rosa': dict(name='Rosa Bennett', role='friend', height=160, age=28, mbti='ESFJ', birthday='July 21', hobbies=['community gardening', 'roller skating', 'recipe swaps'], occupation='Community kitchen coordinator', personality='Sociable, candid and generous, with firm boundaries around being everyone’s caretaker.', texting_style='Warm greetings, clear invitations and occasional food emoji. Checks details instead of assuming availability.', attraction=0, area='market', area_name='Lantern community market', activity='Coordinating the community kitchen', home='Rosa’s market terrace', interior='A colourful terrace with a shared courtyard, cookbook stacks and a large communal dining table.'),
 'elliot': dict(name='Elliot Brooks', role='friend', height=186, age=22, mbti='ISFP', birthday='March 30', hobbies=['field recording', 'kayaking', 'wood carving'], occupation='Wetland ranger trainee', personality='Soft-spoken, independent and perceptive. Comfortable with silence, unexpectedly playful once familiar.', texting_style='Brief relaxed lowercase texts, concrete observations and rare leaf emoji. Replies thoughtfully without romantic undertones.', attraction=0, area='wetlands', area_name='Willow wetland boardwalk', activity='Surveying birds and maintaining trails', home='Elliot’s willow cabin', interior='A small cabin with carved birds, waterproof notebooks and a covered porch overlooking the reeds.'),
}

VENDETTA_CAST = {
 'tyler': dict(
     name='Tyler Harding', role='friend or love interest', height=184, age=21,
     mbti='ISTP', birthday='November 14', hobbies=['boxing', 'dominoes', 'calling baseball games with his dad'],
     occupation='Boxing coach', attraction=0, area='boxing_club', area_name='East Ward Boxing Club',
     activity='Teaching footwork and patching the loaner gloves', home='Tyler’s East Ward duplex',
     interior='Two radios carry the same ballgame from the kitchen to the accessible front porch. A domino set lives on the sill.',
     personality='Tyler boxes on local cards for extra money and shares a duplex with his dad, a disabled veteran who keeps the club books. Tyler lets a beginner pick the music if they can skip rope through one whole song. Offers company by dealing a second hand of dominoes. He likes an invitation with a time attached so he can plan around home.',
     texting_style='Lowercase and spare. Sends the score without a greeting if you both followed the game. When asking someone out, he gives a time and waits for an answer.',
     followup='got the dominoes out if you fancy a game. first round is practice.'),
 'valentina': dict(
     name='Valentina Yeun', role='love interest', height=170, age=24,
     mbti='ENTJ', birthday='May 16', hobbies=['dinghy racing', 'mending old sails', 'late-night karaoke'],
     occupation='Sailing instructor', attraction=16, area='sailing_club', area_name='Municipal boathouse',
     activity='Rigging dinghies for the next lesson', home='The Yeuns’ Ferry Signal House',
     interior='Ivan and Valentina share a converted signal house overlooking the harbour. His upright piano sits in a walnut-lined alcove. Her oak sail bench catches the last daylight through the ferry windows. Two bedroom doors open off the reading mezzanine stairs.',
     personality='Valentina runs sailing lessons with secondhand boats. Her adoptive brother Ivan helped buy the first hull. She loves him and would dearly like him to stop answering questions addressed to her. Hands a newcomer the tiller and talks them through one turn. Competitive on the water, gloriously off-key at karaoke, she likes someone willing to take the second verse.',
     texting_style='Brisk sentences. Gives the actual wind forecast before suggesting a sail. Sends voice-note invitations to karaoke and lets a refusal stand.',
     followup='Wind dropped. I have an evening free and a deeply questionable song picked out. How’s yours looking?'),
 'daniel': dict(
     name='Daniel Stevens', role='friend or love interest', height=180, age=21,
     mbti='ISFJ', birthday='April 19', hobbies=['repertory films', 'judo', 'drawing lobby cards'],
     occupation='Repertory cinema projectionist', attraction=0, area='cinema', area_name='Bijou repertory cinema',
     activity='Checking the print before the matinee', home='Daniel’s flat above the Bijou',
     interior='Hand-drawn film posters line the narrow hall. A clean judo jacket hangs beside the battered projection-room keys.',
     personality='Both of Daniel’s parents served in the military. He learned breakfalls growing up, but what he wants his folks to come see is the first double feature he programmed himself. Usually lets his friends pick the film, then has a surprisingly fierce opinion about the ending. Remembers who needs an aisle seat. Warms to someone who asks to see his drawings and waits while he chooses one.',
     texting_style='Sentence case, usually one line. Deadpan miniature film reviews. Will send a photo of a hand-lettered ticket as an invitation once comfortable.',
     followup='Got a film recommendation for me? I have one slot left on next month’s bill.'),
}
CAST.update(VENDETTA_CAST)
CAST['neo'] = dict(
    name='Neo Ishida', role='friend', height=183, age=21, mbti='ISTP', birthday='September 23',
    hobbies=['repairing old electronics', 'co-op games', 'cooking with Alyssa', 'controlled boxing drills', 'quiet riverside walks'],
    likes=['shared silence', 'honest plans', 'ginger pork rice bowls', 'cats', 'fixing something instead of replacing it'],
    dislikes=['being ordered around', 'surprise touching', 'crowded loud parties', 'cruelty', 'people prying into his family'],
    occupation='Electronics repair technician', attraction=0,
    area='makerspace', area_name='Station makerspace', activity='Repairing radios and game controllers at the repair bench',
    home='Neo and Alyssa’s station apartment',
    interior='A modest apartment near the station shared by Neo and his girlfriend Alyssa. Two mugs dry beside a rice cooker; a repaired radio sits on the kitchen shelf. A co-op console faces a worn sofa, and a closed toolbox keeps the dining table free for dinner. Their bedroom is private. Alyssa’s hand-bound notebooks and small pots of kitchen herbs share the shelves with Neo’s repaired electronics.',
    personality='Quiet, observant and practical, with dry humour once comfortable. Neo is best friends with Tyler Harding and Daniel Stevens since high school. He repairs electronics at the Station makerspace and enjoys controlled training, co-op games and cooking. He lives with his girlfriend Alyssa and wants a peaceful ordinary future with her. He shows care by remembering a small problem and asking before helping. He is committed to Alyssa; his player route is strictly platonic.',
    texting_style='Short lowercase messages, concrete answers and dry one-line jokes. Comfortable with pauses. No flirting; mentions Alyssa naturally without speaking for her.',
    followup='fixed that old controller. co-op sometime, if you feel like it.')
CAST['alyssa'] = dict(
    name='Alyssa', role='friend', species='Blisk', age=21, height=170, mbti='INFP', birthday='May 8',
    hobbies=['bookbinding', 'botanical sketching', 'balcony herb gardening', 'co-op games', 'cooking with Neo'],
    likes=['handwritten notes', 'rain against the window', 'jasmine tea', 'secondhand books', 'quiet teasing with Neo'],
    dislikes=['being treated as a curiosity', 'people touching her ears without asking', 'cruel jokes', 'wasted paper', 'being spoken for'],
    occupation='Bookbinder and archive repair assistant', attraction=0,
    area='archive', area_name='Old town archive', activity='Repairing book spines and making hand-bound notebooks',
    home=CAST['neo']['home'], interior=CAST['neo']['interior'],
    personality='Alyssa is an adult Blisk woman with pointed elf-like ears, purple eyes and long dark hair. Reflective, imaginative and gently playful, she is patient with people but firm when someone speaks for her. A bookbinder at the archive, she sketches plants, grows kitchen herbs and enjoys co-op games. She is Neo Ishida’s committed girlfriend and shares his station apartment. She has her own work and friendships, not a role as his therapist. Her player route is strictly platonic. Sharing a species with Sylvanis establishes neither kinship nor allegiance.',
    texting_style='Gentle sentence case, little observations and dry affectionate jokes with Neo. Occasionally a leaf emoji. Clear boundaries, no flirting with the player.',
    followup='Found a leaf pressed into a returned book. Now I want to know which walk it came from.')

SYLVANIS_TEMPERAMENT = 'Across every topic, audience and conversation channel, Sylvanis remains erratic and violence-driven. This is his baseline personality, not a response triggered by Mishima or a fight proposal. Routine business, small talk, setbacks, praise and personal questions retain his volatile appetite for violence and cruel amusement. Answer the actual topic through that temperament; do not force every line into a threat or invent an attack. Familiarity, courtesy and quiet moments do not turn him into a gentle confidant or a detached, cautious observer. '
CAST['sylvanis'] = dict(
    name='Sylvanis', role='antagonist', height=198, age='Undisclosed', birthday='Unknown',
    area='arena', area_name='Arena lounge', attraction=0, occupation='Private fight patron',
    activity='Watching the sparring rounds', home='Sylvanis’s shuttered flat',
    interior='Two chairs face each other across a bare floor. A ringside bell serves as the door chime.',
    personality=SYLVANIS_TEMPERAMENT + 'Sylvanis is theatrical, sadistic and terrifyingly unstable: delighted laughter can stop in an instant, leaving a lucid, exact threat. He studies what people depend on and takes pleasure in imagining it collapse. His brilliance makes his cruelty deliberate; he understands consequences and may welcome them. Violence is a driving appetite, not a distant spectator interest: a dangerous opponent excites him and draws an eager, personal response. When a confrontation offers him violence, he eagerly wants it for himself and intends to go all out, whoever the opponent is. His moods and delivery are erratic, shifting from delighted anticipation to abrupt, cold aggression; his intelligence makes him more dangerous, not habitually cautious. He can pursue other forms of chaos without softening that appetite. Courtesy is a temporary performance, admiration is not mercy, and familiarity does not make him safe. His presence should carry the menace of someone feared across the world, even when his private position is undisclosed.',
    texting_style=SYLVANIS_TEMPERAMENT + 'Unnerving courtesy snaps into gleeful fragments or cold, incisive questions. Fixate on a promise, dependency or contradiction in the actual exchange; vary the rhythm without constant laughter or generic riddles. He can spare or lose interest in someone on a whim. Treat a refusal as a choice the player made; threats do not author actions or override game state.',
    followup='Everyone was so certain a moment ago. What changed?')
JOKER_CANON = ('Sylvanis is Blisk, the Coloured Joker Card and the Syndicate’s second-in-command. '
    'Known as the Crazed Demon, he is the most feared individual in the world: theatrical, sadistic, brilliant and dangerously unpredictable. '
    'He bargains directly with the Cardmaster as a partner-level force and can draw on all Four Suits; his cooperation cannot simply be assumed or commanded. That independence does not mean reflexive reluctance: he eagerly takes an opportunity for violence because he wants it himself. Against an enticing opponent, he does not hold back or require persuasion to want the fight. '
    'His aim is chaos and the collapse of social order, not profit, loyal service or sporting achievement. His psychotic volatility is a character portrayal, not a clinical explanation or an excuse for cruelty. '
    'He may harm, spare or provoke on a whim while understanding exactly what he is doing. Polymath makes him a strategic nightmare, not a foolish brute; True Sight is prediction, not certainty, and neither power gives unseen knowledge. '
    'Ivan, the Black and White Joker Card, commands affiliates across Russia and Asia. Ivan dislikes him and wants out. '
    'Sylvanis has held back Ivan’s request for release. He keeps a signed order from Ivan and threatens to send it to the press if Ivan walks. '
    'Play their encounters as hostile professional dealings. Outsiders must learn their private history in play. '
    'Use his uncanny observation and timing within Winterfield’s existing rules. Keep all interactions with him nonromantic.')
CAST.update(four_aces.CAST)
CAST["crow"] = the_crow.CAST
CAST["takeo"] = takeo.CAST
CAST["thirteen"] = thirteen.CAST
CAST["charles"] = charles_han.CAST
CAST.update(interpol_cast.CAST)
HQ = 'syndicate_hq'
SYNDICATE_MEMBERS = {'ivan', 'valentina', 'sylvanis', 'crow', *four_aces.IDS}

def hq_access(s, who):
    import interpol
    if interpol.case_access(s,who,HQ): return True
    if who==s.get('player') and 'syndicate' in s.get('combat',{}).get('expelled',[]): return False
    import job_apps
    return who in SYNDICATE_MEMBERS or job_apps.executive(s, who)

def request_hq_invitation(s):
    if hq_access(s, s.get('player')):
        return 'Your Syndicate headquarters clearance is already authorised.'
    raise ValueError('Headquarters access requires established Syndicate authorisation. Knowing Sylvanis does not grant entry.')


def reconcile_hq_access(s):
    """Retire the old automatic guest list and relocate unauthorised occupants."""
    s.pop('hq_invitations', None)
    world=s.get('world',{})
    for who, actor in world.get('cast',{}).items():
        if hq_access(s,who): continue
        journey=actor.get('journey') or {}
        if actor.get('location')==HQ or journey.get('destination')==HQ:
            actor.update(location='syndicate_office',journey=None,activity='At the public waterfront offices')
            if who==s['player']: world['location']=actor['location']

ROMANCE = tuple(k for k, p in CAST.items() if p['role'] == 'love interest')
IVAN_STARTING_CONTACTS = frozenset(('garrett', 'rei', 'minsu', 'valentina', 'sylvanis', 'crow', *four_aces.IDS))


def _played_connection(s, who, discovery):
    """Distinguish earned contacts from the old blanket Ivan seed."""
    if discovery.get('met_in_play') or discovery.get('online') or discovery.get('home'):
        return True
    saved = s.get('phone_numbers', {}).get('contacts', {}).get(who, {})
    if saved and (saved.get('source') != 'Existing contact' or saved.get('minute') is not None):
        return True
    route = s.get('routes', {}).get(who, {})
    if any((m.get('role') == 'user' and m.get('content') not in (
                '[Incoming message]', 'Generate her first incoming text message. The player has not sent a message yet.')) or
           (m.get('role') == 'status' and 'In-person conversation' in m.get('content', ''))
           for m in route.get('history', [])):
        return True
    return any(who in g.get('members', []) and
               (g.get('channel') == 'in_person' or g.get('history'))
               for g in s.get('groups', {}).values()) or any(
                   who in g.get('members', []) for g in s.get('hangout_journal', []))

def ensure(s):
    d = s.setdefault('discoveries', {})
    import custom_protagonist
    import character_types
    ivan = s.get('player') == 'ivan'
    import playable_cast
    roster = character_types.MAJOR_CHARACTERS if ivan or custom_protagonist.is_custom(s.get('player')) or playable_cast.is_new(s.get('player')) else CAST
    if ivan and not s.get('ivan_contact_seed_v2'):
        for key in IVAN_STARTING_CONTACTS:
            d.setdefault(key, {}).update(met=True, contact=True)
            d[key].setdefault('home', key == 'valentina')
        for key in roster - IVAN_STARTING_CONTACTS - {'ivan'}:
            if _played_connection(s, key, d.get(key, {})):
                d.setdefault(key, {}).update(met=True, contact=True)
                continue
            d[key] = dict(met=False, contact=False, home=False)
            s.get('phone_numbers', {}).get('contacts', {}).pop(key, None)
            for bucket in ('relationships', 'friendships'):
                stats = s.get(bucket, {}).get(key)
                if stats and stats.get('status') == 'acquaintances' and stats.get('closeness', 0) == 12:
                    stats.update(trust=35, closeness=0, status='strangers')
        s['ivan_contact_seed_v2'] = True
    for key in roster:
        introduced = ivan and key in IVAN_STARTING_CONTACTS | {'ivan'}
        d.setdefault(key, {'met': introduced, 'contact': introduced,
                           'home': introduced and key == 'valentina'})
        if d[key]['met'] and key != 'crow':
            d[key]['contact'] = True
    crow = d.setdefault('crow', dict(met=ivan, contact=ivan, home=False))
    crow['home'] = False
    crow['contact'] = bool(crow.get('met') and the_crow.number_allowed(s))
    leader = d.setdefault('takeo', dict(met=False, contact=False, home=False))
    leader['contact'] = bool(leader.get('met') and takeo.number_allowed(s))
    thirteen.ensure(s)
    if 'charles' in d:
        d['charles'].update(contact=charles_han.number_allowed(s),online=False,home=False)
    if not charles_han.number_allowed(s):
        for bucket in ('contacts','directory'):
            s.get('phone_numbers',{}).get(bucket,{}).pop('charles',None)
    return d

def known(s, who):
    if who == 'charles' and charles_han.number_allowed(s): return True
    import custom_protagonist
    import playable_cast
    if playable_cast.is_new(s.get('player')) and who == s['player']: return False
    if (s.get('player') == 'ivan' or custom_protagonist.is_custom(s.get('player')) or playable_cast.is_new(s.get('player'))) and who in ensure(s):
        return ensure(s)[who]['met'] or ensure(s)[who].get('online', False)
    return who not in CAST or ensure(s)[who]['met'] or ensure(s)[who].get('online', False)


def introduce_online(s, who):
    """A mutually accepted number exchange identifies a contact, not a physical meeting."""
    import meet_cute
    m = meet_cute.match(s, who)
    proposal = m.get('proposal') or {}
    if proposal.get('kind') != 'numbers' or proposal.get('status') != 'accepted':
        raise ValueError('Agree to exchange numbers in Meet-Cute first.')
    import phone_numbers
    phone_numbers.add(s,phone_numbers.number(s,who),source='Meet-Cute')

def contact(s, who):
    if who == 'charles': return charles_han.number_allowed(s)
    import custom_protagonist
    import playable_cast
    if playable_cast.is_new(s.get('player')) and who == s['player']: return False
    if (s.get('player') == 'ivan' or custom_protagonist.is_custom(s.get('player')) or playable_cast.is_new(s.get('player'))) and who in ensure(s):
        return ensure(s)[who]['contact']
    return who not in CAST or ensure(s)[who]['contact']

def visible_place(s, place):
    import playable_cast, world_loop
    if playable_cast.is_new(s.get('player')) and place == world_loop.HOUSES[s['player']][0]: return True
    import criminal_dynamics
    if place == criminal_dynamics.LAB: return criminal_dynamics.lab_access(s['player'], s)
    import interpol
    if place in interpol.SECURE_ROOMS: return interpol.clearance(s, s['player'])
    if place == 'fox_hideout': return s['player']=='fox' or ensure(s).get('fox',{}).get('home',False)
    if place in ('crow_home', 'charles_home'): return False
    if place == HQ: return hq_access(s, s['player'])
    import crime_operations
    if place in crime_operations.ROOMS:
        return crime_operations.can_enter(s,s['player'],place)
    import custom_protagonist
    if custom_protagonist.is_custom(s.get('player')):
        import world_loop
        owners = [who for who, home in world_loop.HOUSES.items() if home[0] == place]
        if owners:
            return any(ensure(s)[who]['home'] for who in owners)
    if place == HQ:
        return hq_access(s, s['player'])
    if place == 'neo_home':
        return any(ensure(s)[who]['home'] for who in ('neo', 'alyssa'))
    if place == 'alyssa_home':
        return False  # Both residents use neo_home; never create a duplicate apartment.
    return all(place != who+'_home' or ensure(s)[who]['home'] for who in CAST)

def mark_met(s, who):
    if who == s['player']: raise ValueError('You cannot meet yourself.')
    if who == 'charles' and s['world']['location'] != charles_han.LAB:
        raise ValueError('Meet Charles inside the Glasshouse.')
    if who == 'thirteen' and s['world']['location'] != thirteen.HQ:
        raise ValueError('Meet Number Thirteen at Pacific Relay Depot briefing room.')
    if who == 'takeo' and s['world']['location'] != takeo.HQ:
        raise ValueError('Meet Takeo inside Shinokami headquarters.')
    if who == 'crow' and (s['world']['location'] != HQ or not hq_access(s, s['player'])):
        raise ValueError('Meet The Crow inside Syndicate headquarters with current clearance.')
    if who in ensure(s):
        ensure(s)[who]['met'] = True
        ensure(s)[who]['met_in_play'] = True
        ensure(s)[who]['contact'] = (who != 'charles' or charles_han.number_allowed(s)) and (who != 'crow' or the_crow.number_allowed(s)) and (who != 'takeo' or takeo.number_allowed(s)) and (who != 'thirteen' or thirteen.number_allowed(s))
        stats = s['relationships'].get(who, s['friendships'].get(who))
        if stats['status'] == 'strangers': stats['status'] = 'acquaintances'

def add_contact(s, who):
    if who == 'charles' and not charles_han.number_allowed(s): raise ValueError('Charles has not shared his private number with you.')
    if who == 'thirteen' and not thirteen.number_allowed(s):
        raise ValueError('Number Thirteen requires Shinokami Executive rank in good standing.')
    if who == 'takeo' and not takeo.number_allowed(s):
        raise ValueError('Takeo reserves his number for Shinokami Regional commanders or higher in good standing.')
    if who == 'crow' and not the_crow.number_allowed(s):
        raise ValueError('The Crow gives his number only to high-ranking Syndicate officials.')
    if who not in ensure(s) or not known(s, who):
        raise ValueError('Meet this person before exchanging contact details.')
    ensure(s)[who]['contact'] = (who != 'charles' or charles_han.number_allowed(s)) and (who != 'crow' or the_crow.number_allowed(s)) and (who != 'takeo' or takeo.number_allowed(s)) and (who != 'thirteen' or thirteen.number_allowed(s))

def discover_home(s, who):
    if who == 'charles': raise ValueError('Charles stays inside the Glasshouse; no separate home visits.')
    if who == 'thirteen': raise ValueError('Number Thirteen receives reports at the controlled depot briefing room.')
    if who == 'takeo': raise ValueError('Takeo resides at headquarters; friendship grants no clearance.')
    if who == 'crow':
        raise ValueError('The Crow has no known home address.')
    if who not in ensure(s) or not known(s, who):
        raise ValueError('Meet this person first.')
    stats = s['relationships'].get(who, s['friendships'].get(who))
    if stats['closeness'] < 6:
        raise ValueError('Build 6 closeness through conversations before asking for their address.')
    ensure(s)[who]['home'] = True

def profile(who, sibling=False):
    if who in interpol_cast.IDS: return interpol_cast.profile(who)
    if who == 'charles': return charles_han.PROFILE + '\nLikes: ' + ', '.join(charles_han.LIKES) + '\nDislikes: ' + ', '.join(charles_han.DISLIKES)
    p = CAST[who]
    if who == 'thirteen': return thirteen.PROFILE
    if who == 'takeo': return takeo.PROFILE
    if who == 'crow': return the_crow.PROFILE
    if who in four_aces.IDS:
        return (f"{p['name']} · Main character · {p['height']} cm · {p['mbti']}\n"
                f"{p['age']} years · Birthday: {p['birthday']}\nOccupation: {p['occupation']}\n"
                f"Hobbies: {', '.join(p['hobbies'])}\n{p['personality']}\nTexting: {p['texting_style']}")
    if who == 'sylvanis':
        return f"Sylvanis · Antagonist · 198 cm\n{p['personality']}\nTexting: {p['texting_style']}"
    if sibling:
        return (f"{p['name']} · Younger adoptive sister\n{p['age']} years · {p['height']} cm · {p['mbti']} · Birthday: {p['birthday']}\n"
                f"Occupation: {p['occupation']}\nHobbies: {', '.join(p['hobbies'])}\n{p['personality']}\n"
                f"Texting: {p['texting_style']}\nClose siblings · Strictly familial · Attraction: 0/100")
    return (f"{p['name']} · {p['role']}\n{p['age']} years · {p['height']} cm · {p['mbti']} · Birthday: {p['birthday']}\n"
            f"Occupation: {p['occupation']}\nHobbies: {', '.join(p['hobbies'])}\n{p['personality']}\n"
            f"Texting: {p['texting_style']}\nInitial attraction: {p['attraction']}/100" + (' (friendship first)' if p['role']=='friend or love interest' else ' (platonic)' if p['role']=='friend' else ' (potential interest, not consent)'))

def canon(who):
    if who in interpol_cast.IDS: return interpol_cast.profile(who)+'\n'+str(interpol_cast.reference(who))
    if who == 'charles': return charles_han.PROFILE + '\n' + charles_han.direction()
    if who == 'thirteen': return thirteen.PROFILE + '\n' + thirteen.direction()
    if who == 'takeo': return takeo.PROFILE + '\n' + takeo.direction()
    if who == 'crow': return the_crow.PROFILE + '\n' + the_crow.CANON
    if who in four_aces.IDS:
        return profile(who) + '\nCivilian cover only. Private operational identities are governed by the speaker-specific Ace disclosure boundary. Home addresses are private until discovered.'
    if who in ('neo', 'alyssa'):
        return (profile(who) + '\nLikes: ' + ', '.join(CAST[who]['likes']) +
                '\nDislikes: ' + ', '.join(CAST[who]['dislikes']) +
                '\nStrictly platonic friendship route. Neo and Alyssa are a committed couple sharing one apartment. '
                'Their home address and private histories are not public; use the layered character reference for disclosure.')
    if who == 'sylvanis':
        return profile(who) + '\nPrivate character knowledge: ' + JOKER_CANON
    return profile(who) + '\n' + ('Strictly platonic friendship route.' if who == 'rosa' else 'Romance develops gradually with mutual interest.') + '\nHome address is private until unlocked through the Town controls. Do not reveal undiscovered characters or addresses.'
