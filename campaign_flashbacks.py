"""Mandatory, saved memories. Historical cast and art never relocate live actors."""
from campaign_dialogue import beat


SCENES = {
    'rei-school-friends': dict(player='rei', title='The impossible bus timetable', venue='rei_home',
        background='locations/rei-high-school', portraits={'rei':'rei-high-school', 'marcus':'marcus-high-school'}, beats=[
        beat(speaker='marcus', text='Hold the pigeon there. No, a little higher. It has a very important bus to miss.', narration='FLASHBACK · Rei’s high school. Lunch break. Marcus has covered the courtyard bench with cardboard buildings.'),
        beat('Your bus timetable says it arrives yesterday.', 'marcus', 'Exactly. Public transport, but with ambition.'),
        beat('And I am supposed to draw this?', 'marcus', 'You draw impossible things all the time. I just give them bus stops.'),
        beat('That roof keeps falling off.', 'marcus', 'Because your hand is a very local weather event. Hold still, storm warning.'),
        beat('You could ask someone with steadier hands.', 'marcus', 'I could. But then who would tell me my film makes no sense?'),
        beat('It makes no sense.', 'marcus', 'See? Essential member of the production team.'),
        beat('We could make the pigeon walk home. Past all the places the bus never goes.', 'marcus', 'Wait. That is actually good. Give me the pencil.'),
        beat('You are buying lunch after this.', 'marcus', 'Half my sandwich and a credit bigger than the pigeon’s. Final offer.'),
        beat('Deal.', narration='They bend over the storyboard together. For a while, the hardest thing in the world is keeping a cardboard roof in place.'),
    ]),
    'rei-school-news': dict(player='rei', title='The empty place on the bench', venue='rei_home',
        background='locations/rei-high-school', portraits={'rei':'rei-high-school','emily':'emily-high-school','sophie':'sophie-high-school'}, beats=[
        beat('Where is Marcus? I brought the next page.', 'emily', 'Rei… can you sit with us?', 'FLASHBACK · Another school morning. Emily and Sophie wait beside the courtyard bench.'),
        beat('Why are you both looking at me like that?', 'sophie', 'We did not want you to hear it from people in the corridor.'),
        beat(speaker='emily', text='Marcus died. His family told the school. He died by suicide.', narration='Emily stops to steady her breath. Sophie stays close beside her.'),
        beat('No. We were going to finish the film. He still has my pencil.', 'sophie', 'I know. I keep thinking he is just late.'),
        beat('Did he leave… did anyone say why?', 'emily', 'We do not know everything. I will not make something up just because the silence hurts.'),
        beat('Joseph kept doing it. Every day. And everyone just let him.', 'sophie', 'What Joseph did was cruel. We can say that. We cannot turn Marcus’s whole life into what Joseph did to him.'),
        beat('I should have stayed with him.', 'emily', 'You were his friend, Rei. You could not know everything he was carrying.'),
        beat('I do not know what I am meant to do now.', 'sophie', 'Nothing all at once. Sit here. We can go to the counsellor together when you are ready.'),
        beat('Can you stay?', 'emily', 'Yes. Both of us.', 'The storyboard remains closed on Rei’s knees. No one asks him to stop crying.'),
    ]),
    'rei-school-suspension': dict(player='rei', title='What anger could not repair', venue='rei_home',
        background='locations/rei-high-school', portraits={'rei':'rei-high-school','Joseph Richter':'joseph-richter-high-school'}, beats=[
        beat('Joseph. Look at me.', 'Joseph Richter', 'What do you want?', 'FLASHBACK · Later, outside the school administration entrance. Rei catches up with Joseph Richter.'),
        beat('You humiliated him. You took his things. You made every room somewhere he had to be afraid.', 'Joseph Richter', 'It was school. People get picked on. You cannot put everything on me.'),
        beat('His name was Marcus. Say his name.', 'Joseph Richter', 'You think shouting at me changes anything?'),
        beat('I want you to stop acting like he did not matter.', 'Joseph Richter', 'And I want you out of my way.'),
        beat(narration='Rei shoves Joseph against the wall, then punches him. Joseph staggers and raises his arms. Rei lunges again before a teacher pulls him back. The attack ends there.'),
        beat('Let go of me!', narration='“Rei, step back. Now.” The teacher keeps them apart and calls another member of staff. Joseph is taken to the nurse.'),
        beat('You saw what he did to Marcus. Where were you then?', narration='“We will take a statement about that. Right now, you attacked another student. You are coming to the office.”'),
        beat(narration='Later, in the office, the headteacher states the decision: “You are suspended for attacking Joseph. We are contacting your guardian and arranging a return meeting.”'),
        beat('So I go home, and he gets to pretend none of it happened?', narration='“The bullying report must be addressed separately. This suspension is for your actions today.” Rei stares at the paper on the desk.'),
        beat('I thought if he hurt, he might finally understand.', narration='Outside, Rei’s hand aches. The anger has not brought Marcus back. He folds the suspension letter around the unfinished storyboard and walks away.'),
    ]),
    'garrett-school-brother': dict(player='garrett', title='An older brother’s responsibility', venue='noodle_shop',
        background='locations/garrett-hong-kong-school', portraits={'garrett':'garrett-high-school','charles':'charles-young-adult'}, beats=[
        beat('You came all the way here to glare at me?', 'charles', 'I came because every school in the district seems to know your name.', 'FLASHBACK · Hong Kong. Garrett is sixteen. Charles waits outside his school after hearing that Garrett has united the high-school crews.'),
        beat('Then you heard I did it. They are together now. No more fighting each other.', 'charles', 'You beat people until they agreed to follow you. Do not dress it up as a school project.'),
        beat('They respect me.', 'charles', 'Some of them fear you. Learn the difference.'),
        beat('You do not get to turn up and order me around!', narration='Garrett pushes past him. Charles catches his arm. Anger overwhelms restraint: he strikes Garrett, knocks him down and hits him again before stopping. The pavement falls quiet.'),
        beat('Go on. Is that how you teach me not to fight?', 'charles', '…No.', 'Charles steps back, breathing hard. Garrett gets to his knees without accepting his hand.'),
        beat('You called me a delinquent. What does that make you?', 'charles', 'Your brother. Who just hurt you. I was wrong to do that.'),
        beat('You sound like you hate me.', 'charles', 'I am terrified of losing you. That is not an excuse. It is what I should have said before I touched you.'),
        beat('You never say anything. You just tell me what to do.', 'charles', 'Since Mum and Dad died, I keep thinking an older brother is supposed to have every answer. Food on the table. A safe place to sleep. You coming home.'),
        beat('I lost them too.', 'charles', 'I know. And I have been giving you rules when you needed someone who missed them with you.'),
        beat('I thought if I got strong enough, nobody could take anything else from us.', 'charles', 'So did I. But strength does not make that promise true.'),
        beat('Then what am I meant to do with everyone following me?', 'charles', 'Be responsible for what you ask of them. The Red Dragons are not just a name you put behind your fists. People live with the consequences of what we do.'),
        beat('I stopped the school crews going after each other.', 'charles', 'Then keep them safe. No making children prove themselves. No threatening families or shopkeepers. If someone wants out, you let them go.'),
        beat('And if they think that makes me weak?', 'charles', 'You take the insult. An older brother carries responsibility, not ownership. A leader should learn the same thing.'),
        beat('You have to learn it too.', 'charles', 'Yes. Starting with you. I am sorry, Garrett.'),
        beat('I miss them.', 'charles', 'Every day.', 'Garrett finally lets Charles sit beside him. For once, neither brother tries to make grief sound like an order.'),
        beat('Will you come home tonight?', 'charles', 'With you. And we will get that bruise looked at.', 'They leave the school gates together. The apology does not erase the beating; it gives Charles something he must live up to.'),
    ]),
    'garrett-april-silence': dict(player='garrett', title='When the calls stopped', venue='noodle_shop',
        background='locations/noodle_shop', portraits={'garrett':'garrett-home','april':'april-selection'}, beats=[
        beat('It rings. That is the worst part. It rings like he might still pick up.', 'april', 'How long have you been sitting here?', 'FLASHBACK · Years later, after Charles goes missing. April finds Garrett after closing at the Golden Dragon.'),
        beat('I do not know. I checked work again. Nobody has heard anything.', 'april', 'Have you eaten?'),
        beat('April, I cannot think about dinner.', 'april', 'Then do not think about it. I brought something. You do not have to finish it.'),
        beat('He promised he would come home. He used to make such a thing of it.', 'april', 'You believed him. Of course this hurts.'),
        beat('What if something happened? What if he needed me and I missed it?', 'april', 'We do not know what happened. A missed call is not proof you failed him.'),
        beat('First my parents. Now every time the phone stays quiet, I am sixteen again.', 'april', 'You do not have to be the strongest person in the room with me.'),
        beat('If I stop looking, it feels like leaving him behind.', 'april', 'Resting tonight is not leaving him. Tomorrow we can write down who you have spoken to and what they actually know.'),
        beat('You cannot promise he will come back.', 'april', 'No. I can promise I will sit here with you. I will not pretend to know more than we do.'),
        beat('Stay until I can put the phone down?', 'april', 'Of course.', 'April moves the bowl within reach. Garrett turns the phone face down, but keeps it beside him. For tonight, he does not wait alone.'),
    ]),
}


def pending(s):
    player = s.get('player')
    seen = s.get('campaign_flashbacks', {}).get('completed', [])
    if player=='rei' and s.get('rei_story',{}).get('stage',0)==2:
        candidates=('rei-school-friends','rei-school-news','rei-school-suspension')
    elif player=='garrett':
        step=__import__('charles_quest').read(s)['step']
        candidates=('garrett-april-silence',) if step==0 else ('garrett-school-brother',) if step==9 else ()
    else:candidates=()
    return next((key for key in candidates if key not in seen),None)


def venue(s,key):
    # Old in-flight memories retain their original venue in the dialogue snapshot.
    if key=='garrett-school-brother':return 'glasshouse_lab'
    return SCENES[key]['venue']


def require(s):
    # Let a conversation saved before this feature finish; gate the next action.
    if s.get('_finishing_legacy_campaign_dialogue'):
        return
    key = pending(s)
    if key:
        raise ValueError('Complete the mandatory flashback in the hangout window: ' + SCENES[key]['title'])


def validate(s, key):
    import organisation_guards, combat
    if key != pending(s):
        raise ValueError('This is not the next mandatory flashback.')
    organisation_guards.here(s, venue(s,key))
    combat.guard(s)
    if s['world'].get('party'):
        raise ValueError('Take this private moment alone.')


def start(s, key):
    import campaign_dialogue
    campaign_dialogue.begin(s, 'campaign_flashbacks.finish', (key,))


def finish(s, key):
    d = s.get('campaign_dialogue') or {}
    if (d.get('action') != 'campaign_flashbacks.finish'
            or d.get('args') != [key] or d.get('cursor') != len(d.get('beats', []))-1):
        raise ValueError('Read the flashback through its final line first.')
    completed=s.setdefault('campaign_flashbacks', {'completed': []})['completed']
    if key not in completed:completed.append(key)
    return 'Memory complete: ' + SCENES[key]['title']


def portrait_path(s, who):
    from pathlib import Path
    d = s.get('campaign_dialogue') or {}
    stem = d.get('portraits', {}).get(who)
    if not stem:
        stem=__import__('flashback_visits').portraits(s).get(who)
    return Path(__file__).resolve().parent / 'assets' / 'portraits' / (stem + '.png') if stem else None
