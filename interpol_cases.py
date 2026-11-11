"""Authored AU investigations: staged evidence, field objectives and earned reveals."""

def step(title, venue, finding, kind='inspect', **extra):
    return dict(title=title, venue=venue, finding=finding, kind=kind, **extra)


CASES = {
 'blackhaven': dict(title='Blackhaven protection racket', requires=(), faction='lantern', district='blackhaven',
    brief='Residents report repeated demands for protection money. Establish what happened and protect the witnesses.',
    steps=[
        step('Interview the shopkeeper', 'blackhaven', 'A consenting shopkeeper supplies dates and copies of three extortion demands.', 'interview'),
        step('Examine the collection point', 'blackhaven', 'Matching envelope fibres and an observed collection route corroborate the account.', sensory='Fox separates a repeated chemical scent from the street background; photographed fibres corroborate the route.'),
        step('Protect the witness during collection', 'blackhaven', 'The collector is stopped; a seized receipt identifies a rail-yard handover.', 'combat', enemy='Racket collector', power=25),
        step('Submit the corroborated report', 'interpol_hq', 'The corroborated records link this collection cell to the Lantern Crew, without assigning guilt to every member. The shopkeeper receives a protected contact route; the rail-yard lead opens.', 'review')]),
 'rail': dict(title='Rail-yard consignment trail', requires=('blackhaven',), faction='rail', district='west',
    brief='Compare a receipt with physical freight records before intercepting the linked consignment.',
    steps=[
        step('Compare the public freight ledger', 'archive', 'A dated ledger corroborates the handover number without identifying the entire supply chain.', 'records'),
        step('Observe the depot frontage', 'site_02', 'The same consignment number appears at the depot; a visible seal matches the recovered receipt.'),
        step('Intercept the linked courier', 'blackhaven', 'The courier is stopped with a matching consignment record and disputed research referrals.', 'combat', enemy='Armed freight courier', power=42),
        step('Review chain of custody', 'interpol_briefing', 'Independent records link this handover to a Rail Yard Saints consignment cell, then establish a Shinokami supply lead and a Syndicate payment lead. Other crew members are not automatically implicated.', 'review')]),
 'shinokami': dict(title='Shinokami research referrals', requires=('rail',), faction='shinokami', district='west',
    brief='Investigate the disputed referrals without assuming every employee knows the operation.',
    steps=[
        step('Interview a willing former contractor', 'interpol_hq', 'A consenting contractor provides their own referral documents and describes missing consent paperwork.', 'interview'),
        step('Corroborate the research frontage', 'site_03', 'A delivery manifest and recorded exterior observations corroborate the contractor’s dates.'),
        step('Protect the contractor from an enforcer', 'blackhaven', 'The enforcer is stopped before the witness is removed. A recovered transfer record links four coded Syndicate desks.', 'combat', enemy='Shinokami field enforcer', power=65),
        step('Authorise the four parallel enquiries', 'interpol_briefing', 'The file establishes four independent lines of enquiry. No Ace identity is yet proven.', 'review')]),
}

ACE_LINES = {
 'clubs': ('martos','site_04','Security escort records','A signed escort order and separately witnessed deployment link the same security operative.', 'Rage'),
 'hearts': ('elias','site_05','Publicity and intimidation records','A rehearsal schedule, an original instruction and a witnessed masked deployment match independently.', 'Pyromovement'),
 'diamonds': ('camila','site_06','Financial authorisation records','A verified authorisation trail and original transaction records establish a common decision-maker.', 'Analysis'),
 'spades': ('mavis','site_08','Surveillance handover records','A documented handover and a witnessed operational encounter link the chosen name to the masked specialist, not a civil registry identity.', 'Mist'),
}
for suit,(who,venue,title,finding,trait) in ACE_LINES.items():
    CASES['ace_'+suit] = dict(title=title, requires=('shinokami',), faction='syndicate', district='waterfront', reveal=who,
        brief='Corroborate one coded specialist’s role. A public job or a familiar face alone proves nothing.',
        steps=[
            step('Obtain the relevant original record', 'archive', 'The archived original establishes dates and a signature for the '+suit+' enquiry.', 'records'),
            step('Corroborate and reveal the Ace', venue, finding, 'reveal', sensory='Fox matches a previously recorded movement and scent trace; independent observation is still required.'),
            step('Confront the masked specialist', venue, 'The operation secures a direct observation and matching operational material.', 'combat', enemy='Masked '+suit.title()+' specialist', opponent=who),
            step('Review the defeated Ace’s command record', 'interpol_briefing', 'The previously corroborated identity, the victory and the recovered command material are entered together. The specialist was defeated in this operation; this does not destroy the Suit or imply permanent custody.', 'reveal')])

CASES['crow_trail'] = dict(title='The Cardmaster’s command trail',
    requires=tuple('ace_'+s for s in ACE_LINES), faction='syndicate', district='waterfront',
    brief='Combine all four independently established identities and their command records to locate the Crow.',
    steps=[
        step('Compare the four command records', 'interpol_briefing', 'Four independently recovered orders share a command authentication pattern.', 'records'),
        step('Verify the waterfront transfer', 'syndicate_office', 'A matching transfer record places the command courier at the waterfront frontage.'),
        step('Stop the command courier', 'syndicate_office', 'The courier is stopped with an authenticated summons to the underground command site.', 'combat', enemy='Cardmaster’s courier', power=80),
        step('Approve a scoped headquarters operation', 'interpol_briefing', 'The summons, timing and prior records establish the Crow’s command location. Temporary case-specific entry is authorised.', 'locate')])
CASES['crow_operation'] = dict(title='Operation Night Ledger', requires=('crow_trail',), faction='syndicate', district='waterfront',
    brief='Enter the located headquarters, find the Crow and attempt containment. This story confrontation ends in defeat; the final objectives address survival and the ongoing fight. His birth identity remains unconfirmed.',
    steps=[
        step('Brief the containment plan', 'interpol_briefing', 'The team agrees an entry route, witness protection and a nonlethal containment objective.', 'review'),
        step('Verify the command entrance', 'syndicate_hq', 'The authenticated summons matches the physical command entrance and current deployment.'),
        step('Confront the Crow', 'syndicate_hq', 'The Crow breaks the containment attempt and defeats the field team. Fox keeps the withdrawal route in sight while Gordon covers the retreat. They retain the evidence copied before entry, but obtain neither custody nor a new command archive. The Crow remains at headquarters; his birth identity is unknown.', 'combat', enemy='The Crow', opponent='crow', scripted_outcome='crow_defeat'),
        step('Account for the living', 'interpol_containment', 'At the recovery station, Gordon counts the returning team rather than suspects in cells. Fox asks him to stop saying the plan almost worked. Gordon records it plainly: the Crow defeated them. The witnesses were not taken on the raid and remain protected. No arrest, civilian massacre or new identity is invented.', 'review'),
        step('Name what the defeat did not erase', 'interpol_briefing', 'Fox lays out four completed files: Martos Cabrera, Ace of Clubs; Elias Braun, Ace of Hearts; Camila Lopez, Ace of Diamonds; Mavis Kuro, Ace of Spades. Each connection was independently established and each specialist was defeated in the field. Those victories did not make the Crow beatable. The HQ location remains verified; a known address is not control of the organisation.', 'review'),
        step('Return to the people behind the case', 'blackhaven', 'The team checks the protected contact route from the first case. Gordon asks what the residents need now, rather than asking them to celebrate the raid. Fox stays at the exit while a shopkeeper closes without paying the old collector. A local victory is real even when the organisation behind it survives.', 'interview'),
        step('Accept the unfinished fight', 'interpol_briefing', 'Fox admits he wanted one final target to make the street safe. Gordon accepts responsibility for treating a successful investigation as proof that the team could win the confrontation. Neither offers a promise of a decisive rematch. They commit to witness protection, disrupting specific operations and sharing only verified evidence. The Aces are exposed to the investigation team, HQ is found, and the Crow has been faced and survived. This campaign is complete; the fight against the Syndicate will be ongoing. Repeatable protection and interception operations remain available from the public desk.', 'ongoing')])

OPERATIONS = {
    'patrol': dict(title='Blackhaven witness-protection patrol', venue='blackhaven', faction='lantern', district='blackhaven', enemy='Witness intimidator', power=40),
    'intercept': dict(title='Depot consignment interception', venue='site_02', faction='shinokami', district='west', enemy='Armed consignment escort', power=60),
    'protect': dict(title='Waterfront witness extraction', venue='syndicate_office', faction='syndicate', district='waterfront', enemy='Syndicate interception team', power=70),
}

OPERATIONS.update({
 'syndicate_witness': dict(title='After Night Ledger · protect a threatened witness',venue='blackhaven',faction='syndicate',district='blackhaven',enemy='Syndicate witness-removal specialist',power=76,post_story=True,
    brief='A willing witness reports a fresh Syndicate threat. The team protects their departure without exposing the protected contact network.',
    finding='The witness reaches a protected contact. This removal attempt is stopped; the Crow’s saved status and the wider Syndicate remain unchanged.'),
 'syndicate_supply': dict(title='After Night Ledger · interrupt an armed supply run',venue='syndicate_office',faction='syndicate',district='waterfront',enemy='Syndicate supply-run commander',power=82,post_story=True,
    brief='Verified freight records identify a new armed Syndicate supply run. Intercept the specific shipment and preserve its records.',
    finding='The identified supply run is interrupted and its records secured. A local operation is disrupted, not the Syndicate itself; this is not a Crow rematch.'),
 'syndicate_coercion': dict(title='After Night Ledger · break a collection detail',venue='market',faction='syndicate',district='central',enemy='Syndicate coercion detail leader',power=72,post_story=True,
    brief='Consenting traders provide matching demands from a new Syndicate collection detail. Stop the armed collectors and protect the traders.',
    finding='The documented collection attempt is stopped. Traders retain their property and protected reporting route. The team accepts that further Syndicate operations will require continued work.'),
})
