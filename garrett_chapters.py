"""Second act of Find Charles: the Red Dragons' promise is tested in public."""

# Appended, never inserted: old reunion saves keep their evidence and chapter indices.
STEPS = (
 ('The chair at the table','garrett_home',
  'Back home, Garrett sets out two bowls before remembering Charles is staying at the lab. Finding him has not returned the years. His mother’s recipe book lies beside the Red Dragons accounts. He can neither cook his parents back into the room nor make an organisation good by calling it family.',
  ('Keep a place for Charles without waiting to live','Put the spare bowl away until he can visit'),
  'Garrett keeps the recipe book and admits that relief and anger can coexist. His brother is alive; their parents’ killers remain unproven. He decides that the people still here deserve more than a leader consumed by revenge.'),
 ('Protection is not ownership','noodle_shop',
  'After service, a shopkeeper brings two demands: a Shinokami collection notice and a Syndicate freight surcharge. A Red Dragons runner offers to make the problem disappear if the street pays them instead. Garrett stops him. “If they have to buy our kindness, we have only changed the name on the threat.” The shopkeeper asks who will listen when the threatening man wears Garrett’s colours.',
  ('Give residents a direct complaint channel','Appoint rotating civilian witnesses to review complaints'),
  'Garrett forbids protection fees, forced recruitment and retaliation against complainants. The runner is removed from civilian-facing duty pending review. Residents can refuse escorts and aid. The Red Dragons commit to protecting civilians from both rival organisations and their own members.'),
 ('Two demands, two trails','archive',
  'With permission, Garrett compares the demands against retained delivery records. A Shinokami collection crew has marked a Blackhaven market handover. A separate Syndicate escort order targets the waterfront shipment. Neither paper names the person who killed his parents. He resists treating every new enemy as the answer to an older wound.',
  ('Keep separate files and redact the residents’ names','Make copies for the residents before taking the originals back'),
  'The documents establish two specific threats, not guilt by association. Garrett records the market collection and waterfront interception as separate civilian-protection missions. Witness names stay out of the crew briefing.'),
 ('The market belongs to its people','blackhaven',
  'The Shinokami collectors arrive while residents are packing their stalls. Garrett orders the Dragons to keep an exit open. “Nobody earns their place here by standing behind me,” he tells the shopkeeper. “Leave if you want to.” The collectors demand the witnesses and raise their weapons. Defeat the collection detail before securing the market.',
  ('Escort the residents out first','Hold the escape route while residents leave together'),
  'The Shinokami collection detail is defeated. Residents leave without paying either gang. Garrett preserves the collection demands and returns seized takings to their documented owners; this is restitution, not player loot. The market is protected in this incident, not permanently conquered.'),
 ('The cost of wearing our colours','syndicate',
  'At the Red Dragons lounge, the runner admits threatening a trader with losing protection. He insists he was keeping rivals away. Garrett hears Charles’s old argument in different words: deciding for someone else, then calling it care. The trader wants safety, not a speech. The crew waits to see whether the rule applies to one of its own.',
  ('Remove the runner from protection work and arrange restitution','Permit supervised restitution, with no civilian contact until review'),
  'Garrett records the complaint, bars the runner from unsupervised civilian contact and requires restitution. Rank cannot excuse coercion. He gives residents a way to challenge the Dragons without joining them. The crew accepts a written no-extortion, no-narcotics, no-forced-recruitment charter.'),
 ('No one is cargo','syndicate_office',
  'The waterfront escort intends to seize a driver and the driver’s load as collateral for the disputed surcharge. Garrett refuses the offer to buy an exclusive Red Dragons route in exchange for looking away. “They get to go home. That is the whole bargain.” The armed Syndicate detail moves to block the exit. Defeat it before releasing the driver.',
  ('Shield the driver while the workers withdraw','Keep the loading exit clear for everyone'),
  'The Syndicate interception detail is defeated and the driver leaves freely. The disputed load is returned to its documented owner. The Dragons take no cut, claim no ownership of the workers and acquire no general access to Syndicate headquarters.'),
 ('A brother, not a weapon','glasshouse_lab',
  'Alone in the evening laboratory, Garrett tells Charles only what he can safely share. “I keep wanting every fight to lead to Mum and Dad.” Charles closes his notebook. “So do I.” Garrett asks whether protecting people now has become a distraction from justice. “No,” Charles says. “But I used justice to excuse what I did to you. Do not let me teach you that.” No new culprit emerges from their conversation.',
  ('Agree to share verified leads, never order each other into danger','Keep the missions separate and maintain personal check-ins'),
  'The brothers agree that family is not permission to command each other. Charles’s cover remains private; Garrett’s civilian work does not depend on laboratory intelligence. Their parents’ deaths remain an open question, not an excuse to punish an unproven suspect.'),
 ('An anchor, not a throne','syndicate',
  'Both threats were stopped, but fresh demands will come. Garrett lays the charter beside the accounts. Some Dragons want to charge for the next rescue; others want to chase the defeated crews into a turf war. He rejects both. The organisation must remain a counterweight to the Shinokami and Syndicate without making civilians its territory. He chooses how the promise will be maintained.',
  ('Establish a standing civilian escort and relief rota','Establish a resident-led request and accountability council'),
  'Garrett commits the Red Dragons to lasting civilian protection, voluntary help and review of their own conduct. Neither rival is destroyed. The Dragons remain an independent anchor in the criminal world, measured by whom they protect and whether people can safely tell them no.'),
 ('A meal after closing','noodle_shop',
  'After closing, Garrett reads a short note from Charles: “Still here. Toast the shells first.” He laughs, then lets himself miss him. The shopkeeper returns a borrowed bowl; there is no envelope of protection money inside it. Tomorrow there will be requests, arguments and work. Tonight Garrett can make a meal without pretending it is a victory over grief.',
  ('Write back, then cook for the people still at the table','Keep the note beside the recipe and take a quiet evening'),
  'Garrett’s chapter closes with reconciliation on chosen terms and a renewed Red Dragons charter. The market witnesses and waterfront driver are safe from these incidents. Family justice remains unfinished; protecting the living is a purpose of its own. Daily family check-ins remain available; the protection commitment continues.'),
)

# Persistent mission victories, independent of replenishing local patrols.
BATTLES = {14: ('shinokami', ('yokai','oni','tengu')),
           16: ('syndicate', ('clubs','spades','affiliate'))}

def scope(index):
    return 'garrett:protection:'+str(index)

def remaining(s,index):
    import organisation_guards as guards
    won=guards.data(s)['victories'].get(scope(index),[])
    return [(scope(index)+':'+str(i),kind) for i,kind in enumerate(BATTLES[index][1])
            if scope(index)+':'+str(i) not in won]

def fight(s,index):
    import organisation_guards as guards
    rows=remaining(s,index)
    if not rows: raise ValueError('This civilian-protection detail is defeated. Continue the chapter.')
    ident,kind=rows[0]
    return guards.start(s,ident,guards.profile(s,kind),scope(index))

def consequences(d,index,choice):
    policies={12:('direct complaint channel','civilian review witnesses'),
              15:('removed from protection work','supervised restitution'),
              17:('verified leads by consent','separate missions, personal check-ins'),
              18:('standing escort and relief rota','resident-led accountability council')}
    if index in policies:
        d.setdefault('red_dragons',{})[str(index)]=policies[index][choice]
        return ' Recorded commitment: '+policies[index][choice]+'.'
    if index==19:
        d['complete']=True
    return ''
