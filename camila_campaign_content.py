"""The Inheritance. Authored words describe events; operations supply receipts."""
from copy import deepcopy

EXEC='syndicate_hq__executive_meeting_room'
REC='camila_meridian__receiving'
SIT='camila_meridian__sitting'
LOAD='camila_meridian__loading'

def b(speaker=None,text='',narration='',room=None):
    beat=dict(player='',speeches=[[speaker,text]] if speaker else [],narration=narration)
    if room:beat['room']=room
    return beat
def p(text,room=None):return b(narration=text,room=room)

MEMORIES={
 'CA-F01':dict(title='Before she was his',age=7,era='camila_adoption7',background='orphanage',text=[
  p('At seven, Camila keeps the wooden pieces in a biscuit tin. Pilar has borrowed the red counter and wants one more turn. Beyond the common-room windows, Elena is watering the garden. Nothing about the afternoon has been arranged for a visitor.'),
  b('camila-pilar','You counted my turn while I was finding it.'),b('camila','I counted it while you were hiding it.'),b('camila-elena','Then agree where a turn begins before you start again.'),
  p('The visitor returns after the game, as Elena said he would. His dark gloves rest on the table away from the pieces. The beaked mask gives Camila no face to read. She asks whether he has come to watch or to take something.'),
  b('crow','I have come to take you home, if you are ready to come with me.'),b('camila','Can I bring the tin?'),b('crow','Yes. And we will return for what you forget.'),
  p('Elena kneels beside her bag and checks the small practical things with her. Pilar asks for the red counter back. Camila gives it to her and keeps the tin. No one asks the child to earn the place waiting for her. The door closes behind a life that has already contained friends, rules and unfinished games.'),
 ],after_encounter=[p('Present, in the quiet receiving room, Camila turns the empty pen cap between her fingers. The tin is still at home. She remembers the question she asked him, and that he returned for her coat the next morning. Ansel’s first offer is still unverified. She opens the file again.',REC)]),
 'CA-F02':dict(title='A place kept for her',age=8,era='camila_home8',background='dining',text=[
  p('At eight, Camila has been in the household long enough to know which chair catches the afternoon light. She has covered the table with a paper house that will not stand. Mara brings bread and asks her to move the glue before supper.'),
  b('camila-mara','The roof can wait on the sideboard.'),b('camila','It falls when I stop holding it.'),
  p('The Crow returns at the time he gave her. His robe stays clear of the spilled glue; his face remains concealed. He puts the folded note she left him beside the plate. She has drawn three attempts and crossed out two.'),
  b('camila','Father, I haven’t finished.'),b('crow','I can see that. Put it somewhere safe. We will eat.'),b('camila','Will you look at it afterward?'),b('crow','Afterward.'),
  p('He does. She spends most of the time explaining why the roof should work. He holds one wall while she fixes the other. The house remains uneven. It stays on the sideboard for weeks, where people must take care not to knock it down.'),
 ],after_encounter=[p('Mara remembers the crooked roof when Camila mentions it. She also remembers the household learning to step around it. Camila smiles before asking what Mara wants from this meeting. The answer is an unhurried cup of tea, with the planner shut.',SIT)]),
 'CA-F03':dict(title='Who can afford to wait',age=11,era='camila_waiting11',background='study',text=[
  p('At eleven, Camila lays two sets of wooden counters on the study desk. Both exchanges look equal. Her father asks her to read the dates as carefully as the quantities.'),
  b('camila','This one gives everything back. It is fair.'),b('crow','When?'),b('camila','After the other household needs it.'),b('crow','Then the household that can wait holds the advantage. Count that too.'),
  p('She changes the arrangement and is pleased with how quickly the answer changes. Mara has been waiting to take her outside. The lesson has used most of the afternoon.'),
  b('camila-mara','You promised me twenty minutes of daylight.'),b('camila','We can go tomorrow.'),b('camila-mara','I cannot move today’s daylight into tomorrow’s pocket.'),
  p('Camila looks from the counters to the window. Her father lets the interruption stand. She puts a small mark beside the time she had treated as free, then follows Mara out.'),
 ],after_encounter=[p('Inez points at the payroll date. Camila has already compared the totals. She moves the dates into the same column. The discrepancy is visible now: the money is promised, but the dispatch operation cannot use the concession when its people need it.',REC)]),
 'CA-F04':dict(title='The answer she wanted',age=16,era='camila_correction16',background='study',text=[
  p('At sixteen, Camila has prepared an elegant conclusion from three supplied reports. Thin possible branches occupy her attention, each beginning in something she has actually seen. A fourth envelope lies sealed at the edge of the desk.'),
  b('camila','There is only one decision that fits.'),b('crow','There are three reports in your account. There are four on the desk.'),b('camila','You told me to work from the evidence.'),b('crow','Then tell me what you have not examined.'),
  p('She wants the envelope to confirm her work. She opens it and finds a refusal from the person whose cooperation her neatest branch required. The refusal gives a practical reason she had not considered.'),
  b('camila','I treated a likely answer as an agreement.'),b('crow','Correct it.'),b('camila','You could have told me.'),b('crow','I will not be the fact you omitted every time.'),
  p('Mara brings a clean sheet. Camila accepts it without tearing up the first one. Both remain on the desk when she begins again. No account of how her Trait first Awakened is supplied by this afternoon.'),
 ],after_encounter=[p('Camila crosses out “diverted reserve” in the present file. The observed schedule establishes an access problem. It does not yet establish where Ansel’s second promise begins. She writes the missing source beside the correction and leaves its box open.',REC)]),
 'CA-F05':dict(title='A lesson with consequences',age=22,era='camila_operation22',background='receiving',text=[
  p('At twenty-two, Camila brings a successful restriction proposal to a private affiliate office. It keeps a Syndicate-controlled contract intact. She has calculated how quickly the smaller independent contractor will run out of room to refuse the new terms.'),
  b('camila','They accepted the revision.'),b('crow','Then keep the access they have conceded. Build on it.'),
  p('The next report describes cancelled shifts at the independent workshop. Camila had put the pressure in her model. She had counted its owner’s concession as success and stopped the account there. Mara finds her reading the report a second time.'),
  b('camila-mara','Is something wrong with the figures?'),b('camila','No. They are doing what I expected.'),b('camila-mara','And the people?'),
  p('She can name the contract holder. She cannot name everyone who lost a shift. She asks for the attendance record and receives only part of it. Her father has not deceived her about the objective. She helped him secure it. The report remains a record of what her successful method cost other people.'),
 ],after_encounter=[p('Inez will not let “temporary disruption” stand in the current summary. Two shifts have already been cancelled. Camila asks which teams lost the work and records the answer she can obtain. She cannot restore those hours by choosing a better phrase.',REC)]),
 'CA-F06':dict(title='The Ace he made',age=24,era='camila_diamonds24',background='study',text=[
  p('At twenty-four, Camila has the results of three completed negotiations, the objections she answered and one margin she underestimated. She has earned the financial appointment with work that other specialists can examine.'),
  b('crow','You will serve as Diamonds. Protect what finances our advance, and make it capable of financing more.'),b('camila','I have revised the reserve limit. The third negotiation left too little room.'),b('crow','Then use the revised limit.'),
  p('He places the sealed operational mask beside the report. When she puts it on, the hood conceals her ponytail and the gloves cover her hands. The white diamond is the only face the role presents. She is proud of the appointment. It is not the beginning of his care for her.'),
  b('camila','Understood, master.'),
  p('Later, back at the household desk, she removes the mask and writes to an ordinary acquaintance about a dance class. She has spent enough of the day being correct. The class gives her something to learn with her feet.'),
 ],after_encounter=[p('Camila checks the undertaking against the access schedule. Ansel’s confidence in her narrowness has made him careless about which copy he signed. She can identify the clause that conflicts with Inez’s schedule. Obtaining the original still requires his actual attendance.',REC)]),
 'CA-F07':dict(title='What he meant to leave',age=26,era='camila_heir26',background='study',text=[
  p('At twenty-six, she waits in the household study after finishing a report. Her father has asked her to stay. The empty chair beside his has always been a place to put her papers.'),
  b('crow','I did not raise you to tend one part of this forever. You will learn what holds the whole of it together.'),b('camila','You mean after you.'),b('crow','I mean that what I build will continue under someone I have prepared to hold it.'),b('camila','Me.'),b('crow','You.'),
  p('Pride comes first, then a fear too large to describe as a difficult assignment. She has known his attention all her life. Now she sees how far forward it has been directed. His mask reveals nothing she can use to make the moment smaller.'),
  b('camila','I will need more than accounts.'),b('crow','Yes. You will need to judge people who can do things you cannot, and know what their cooperation costs.'),
  p('He is active, deliberate and still hungry for dominion. He has announced no illness, retirement or date. She leaves as Diamonds with a future he genuinely intends for her, and a responsibility she cannot satisfy by being loved.'),
 ],after_encounter=[p('Present, Camila leaves succession out of the evidence packet. It belongs to the private account between them. The records she is authorised to use say enough to establish Ansel’s contradiction without making anyone a witness to her childhood.',REC)]),
 'CA-F08':dict(title='A decision of her own',age=28,era='camila_delegation28',background='receiving',text=[
  p('At twenty-eight, Camila has a limited settlement to complete. Inez has declined her first schedule because the loading team cannot meet it. Camila knows what her father usually does with a counterparty that asks for more time.'),
  b('camila-inez','I can promise Tuesday. Monday would be a false promise.'),b('camila','Then I will put Tuesday in the agreement and change the receiving sequence.'),
  p('She makes the change within the resources entrusted to her. It gives the other operation time and costs her a useful slot. She expects to defend it when she reports.'),
  b('crow','Your result?'),b('camila','The settlement holds. I gave up the first slot because their refusal was credible. The second costs less than forcing a failure.'),b('crow','And if the second fails?'),b('camila','I reserved a receiving team. It is a narrower margin than I wanted.'),b('crow','Keep the team until the work is finished. This decision is yours.'),
  p('He accepts the defensible method without pretending it was his instruction. She keeps the cost in the report. When Inez later confirms the arrival, Camila feels relief before satisfaction. She had chosen without a guarantee.'),
 ],after_encounter=[p('The current reserve has seventy units. Ten will keep payroll preparation open. Camila has two feasible ways to spend what follows: lose the East concession and retain room for later trouble, or keep it by accepting a much tighter reserve. She must sign one plan before asking others to bear its cost.',REC)]),
}

CHAPTERS={
 'CA-01':dict(title='An account that balances',room=EXEC,briefing=[
  p('The two totals match. Camila checks them again because Inez’s dispatch team still cannot use the depot. At headquarters she puts the schedule before the Crow and keeps her personal planner closed. Their conversation is private.',EXEC),
  b('camila','The reported reserve is intact. Its availability is not. I need the original commitments before I call it theft.'),b('crow','Preserve the Meridian network. Do not let Vey detach what serves us. You will have a bounded reserve and access to the people this requires.'),b('camila','And the authority to settle a loss if that preserves the rest?'),b('crow','Within the mandate. You are preparing to hold more than my accounts, Camila. Begin by owning this one.'),
  p('She has known his intention for years. Hearing it inside a real crisis changes what she must do with it. He remains Cardmaster. The assignment supplies neither his answers nor the consent of every person she will need.'),
 ],aftermath=[p('At Meridian’s booked receiving office, she sets the limit at seventy allocation units and requests the original schedule. The appointment has given her a place to ask. It has supplied no evidence yet.',REC)]),
 'CA-02':dict(title='Before she was his',room=REC,briefing=[
  p('The fountain pen catches on a loose thread in its old case. Under the lining is a red mark she made years ago to distinguish it from another child’s bag. She remembers that she did not always own so many things with her name on them.',REC),
  b('camila','I was very particular about whose turn it was. Some defects have admirable endurance.'),
  p('No one else is in the room. She lets the file rest for a moment and remembers the garden house before the visitor became her father.'),
 ],aftermath=[p('She puts the case down with the marked side facing her. Ansel has dealt with her as a financial officer. He has never been entitled to the whole account of her life. The private memory has changed no public record and given him no new knowledge.',REC)]),
 'CA-03':dict(title='A place kept for her',room=SIT,briefing=[
  p('Mara accepts the sitting-room appointment on the condition that the tea is allowed to cool at an ordinary speed. Camila puts her planner under the cup’s saucer, then thinks better of the arrangement and moves it out of reach.',SIT),
  b('camila-mara','You used to put unfinished things where everyone had to see them.'),b('camila','A sound method of obtaining assistance.'),b('camila-mara','You asked us to look. That was different.'),
  p('Camila remembers the paper house, and a parent who came back at the time he had given her.'),
 ],aftermath=[b('camila-mara','You do not have to explain the whole operation to have tea with me.',room=SIT),b('camila','I was about to offer you a schedule.'),b('camila-mara','I know.'),p('Camila laughs and leaves the planner shut. Mara has her own afternoon to return to. Their conversation grants no operational clearance and reveals no succession intention.')]),
 'CA-04':dict(title='The price of waiting',room=REC,briefing=[
  p('Inez brings the original schedule to their agreed meeting. She leaves her finger beside the date when the depot must be available. Camila begins with the figures. Inez waits for her to reach the date.',REC),
  b('camila-inez','The dispatch team cannot spend a promise next week to move wages this week.'),b('camila','Show me the reservation itself.'),b('camila-inez','You may examine it here. I am keeping the original until we agree what happens to it.'),
  p('Camila recognises the shape of an old lesson before she finds a useful answer. Someone has priced the privilege of waiting as though everyone possesses it.'),
 ],aftermath=[b('camila','I have recorded what you showed me, including the date. I have not declared your cooperation secured.',room=REC),b('camila-inez','Good. I have not given it yet.'),p('The first original supplies a boundary for every plausible branch. Camila cannot observe the second document through the closed folder beside Ansel’s name.')]),
 'CA-05':dict(title='The answer she wanted',room=REC,briefing=[
  p('Her first hypothesis makes an elegant accusation: somebody diverted a reserve. The observed schedule contradicts it. Camila writes the contradiction in ink, where she cannot later mistake it for a passing doubt.',REC),
  b('camila','The access was promised twice. That does not yet tell me how Ansel worded his promise.'),
  p('Analysis draws possible consequences from the date, the signature and the available capacity. None of the branches contains an unseen agreement. The difference recalls the fourth envelope in her father’s study.'),
 ],aftermath=[p('She retains the rejected hypothesis with the source that disproved it. Anyone who examines her account can see the correction. She would prefer to submit a clean page. She submits the accurate one.',REC)]),
 'CA-06':dict(title='A lesson with consequences',room=REC,briefing=[
  p('Inez has spoken to the loading team before this meeting. Two independent shifts have already been lost. Camila offers to calculate how the interruption can be contained, and sees Inez’s face close.',REC),
  b('camila-inez','Hear what has happened before you tell me how quickly you can improve it.'),b('camila','You are right. Tell me who was affected.'),b('camila-inez','The night loading team and the contracted van crew. I can give you the rosters. I cannot give them yesterday back.'),
  p('Camila closes the planner. She has asked this kind of pressure to work for her before. The remembered success comes with its own report of lost shifts.'),
 ],aftermath=[b('camila','The lost shifts remain in the account. Neither viable plan refunds them.',room=REC),b('camila-inez','Then include them when you ask for my signature.'),p('The evidence of harm is specific. It does not turn Inez into a confessor or make Camila innocent of the institution she competently serves.')]),
 'CA-07':dict(title='The Ace he made',room=REC,briefing=[
  p('Ansel arrives carrying a copy. Camila asks for the signed undertaking identified in the meeting request. He objects to the inconvenience before producing it.',REC),
  b('camila-ansel','You have an excellent reputation for getting figures into the shape he wants.'),b('camila','This clause grants exclusive access. Inez’s schedule grants exclusive access. Which operation did you expect to wait?'),b('camila-ansel','You understand what can be made to balance.'),b('camila','I understand what cannot be used twice.'),
  p('Her appointment as Diamonds was earned in arguments with real counterparties and their own reasons to refuse. She has more experience than the obedient clerk he is trying to address.'),
 ],aftermath=[p('She records the observed original and the exact conflicting clause. Ansel has shown her something useful because he expected her to negotiate its appearance. She intends to negotiate its actual cost.',REC)]),
 'CA-08':dict(title='What he meant to leave',room=REC,briefing=[
  p('Both records lie open. Camila compares the dates, signatures and incompatible access clauses. She gives the promising branches names and keeps each conditional on the cooperation it needs.',REC),
  b('camila','The contradiction is established. His motive is an inference until he gives us something more.'),
  p('The larger expectation in this assignment is no mystery to her. She remembers the first time her father named it without leaving her to infer what he meant.'),
 ],aftermath=[p('Her report distinguishes observed contradiction, corroborated dependency and unresolved intention. The private heir conversation is absent from every operational copy. She is not going to spend that confidence to make Ansel’s documents agree.',REC)]),
 'CA-09':dict(title='A decision of her own',room=REC,briefing=[
  p('Seventy units remain allocated to the resolution. Keeping payroll preparation open needs ten. Beyond that, releasing the East concession costs twenty and leaves forty; retaining it costs forty-five and leaves fifteen. Both preserve the core payroll network. Neither restores the shifts already lost.',REC),
  b('camila','Forty gives the next disruption room. Fifteen keeps the depot and gives it much less.'),
  p('She writes both consequences before marking a choice. Her father could choose for her. He has entrusted her with a task that requires her to stop using that possibility as a hidden reserve.'),
 ],aftermath=[p('The ten-unit bridge commitment is now spent. The chosen final allocation remains conditional on the signed operating terms and actual recovery. She cannot change her plan afterward to write a cheaper history.',REC)]),
 'CA-10':dict(title='His other servants',room=REC,briefing=[
  p('Camila requests separate working appointments. She brings a bounded task to each colleague and leaves room for refusal. Their agreement will not be inferred from their loyalty to the Crow.',REC),
  b('camila','I need three things my records cannot perform: a clean records route, an escort who can bring the dispatch team out, and cover for a negotiation that may fail.'),
  p('She may share the authorised account of her adoption privately, with a chosen colleague. Succession remains between her and her father. Every operational request stands on the finite mandate rather than a family title.'),
 ],aftermath=[p('Three accepted specialist roles appear beside three names. None grants her command of their Suits, their private histories or their future time. She checks the actual arrival arrangements before moving on.',REC)]),
 'CA-11':dict(title='Who will follow',room=REC,briefing=[
  p('Inez and Ansel attend the private negotiation. Camila puts the chosen terms beside both originals. Inez reads the personnel clause before the allocation figures.',REC),
  b('camila-inez','My signature depends on the dispatch team actually coming back and payroll being funded. I am not signing for your confidence.'),b('camila','Then those are conditions of execution.'),b('camila-ansel','They will follow him. You are the person who explains the account afterward.'),b('camila','You offered the same concession twice. I am offering terms that can actually be carried out. Answer those.'),
  p('Ansel refuses release and calls his depot contractors. Camila records the refusal accurately. Inez does not withdraw her conditional signature, but she does not pretend the dispatch team is safe yet.'),
 ],aftermath=[p('The agreement exists with conditions still to satisfy. Ansel’s refusal is evidence of opposition, not consent. The next operation must earn the result the agreement describes.',REC)]),
 'CA-12':dict(title='The authority entrusted',room=SIT,briefing=[
  p('At the authored private sitting-room appointment outside headquarters, the Crow hears her account. No visitor has been given access to the room. His face, name and unrelated past remain concealed.',SIT),
  b('camila','The selected allocation is feasible. Inez has signed conditional terms. Vey refuses release. I can secure the core network if we recover the people and originals.'),b('crow','Then recover them. Retain what your terms preserve, and leave Vey no authority to promise it away again.'),b('camila','The reserve afterward will be smaller, or we will have lost the East concession. I have chosen which cost to carry.'),b('crow','You have my mandate for that choice. You do not have my command over everyone who serves me.'),
  p('She has asked for the authority she needs and received its limit. The final decision remains hers to execute. He has neither manufactured the crisis nor disappeared to make it meaningful.'),
 ],aftermath=[p('Camila returns to the receiving office to confirm the exact mandate and recovery plan. After that she must assemble the accepted specialists at the secured loading court. No arrival, signature or victory is supplied by the report itself.',REC)]),
 'CA-13':dict(title='The inheritance',room=LOAD,briefing=[
  p('The depot court is quiet enough to hear the dispatch crew behind the inner door. Camila wears the sealed Diamonds hood, mask and gloves. Ansel’s contractor controls the passage to the record cabinet. Her accepted specialists assemble through the actual appointment system; the public route must be separated before the confrontation.',LOAD),
  b('camila','The records and the people are separate objectives. Stop the obstruction. Then we verify the originals, bring the team through, and execute only the signed plan.'),
  p('She watches the guard’s planted foot and the way he checks the inner door. Analysis offers likely openings from observable movement. His next decision remains his own. She must enter the encounter and make her own actions succeed.'),
 ],aftermath=[p('The result is the sum of distinct acts: opposition stopped, originals sealed, personnel received, payroll allocation executed. Ansel’s competing promise has no remaining access to the settled concession. He has not been granted a global custody outcome or an invented death. The finite mandate expires with its work.',LOAD)]),
 'CA-14':dict(title='The chair beside his',room=REC,briefing=[
  p('Inez brings the completed receiving record to the final review. The dispatch team is accounted for and the allocation has funded payroll. The lost shifts remain in the report. Camila reads the remaining reserve aloud before reaching for the next page.',REC),
  b('camila-inez','I will work with an agreement you can carry out. Keep the conditions visible next time.'),b('camila','I intend to.'),
  p('After the professional review she has appointments with Mara and her father, and an evening she has deliberately left free. She will not let a successful operation consume every ordinary thing it was supposed to make room for.'),
 ],aftermath=[]),
}

SUPPORT_LINES={'mavis':'I will take the records route. Verify that I am there when you need it. A copied account will not become an original because we agree about it.',
 'martos':'I will escort the dispatch team to Inez. We count the people who arrive. Your mandate cannot count them ahead of us.',
 'elias':'I can hold the negotiation cover and separate the public approach. I would enjoy a better audience, but this one has useful work to do.'}

ACTION_TEXT={
 'task':{'mandate':'The private bounded mandate is recorded. Crow remains Cardmaster. Camila may disclose her upbringing privately to selected Aces, but succession is not part of their operational packet.',
 'schedule':'Inez places the original where Camila can examine its date and signature. Record only the schedule actually observed.',
 'correction':'The observed contradiction replaces the diverted-reserve hypothesis. Analysis retains possible branches without supplying the missing undertaking.',
 'testimony':'Inez gives the rosters and names the two lost shifts. Their cost remains even if the network is preserved.',
 'pledge':'Ansel produces his original undertaking. Its exclusive-access clause can now be compared with Inez’s observed schedule.',
 'corroborate':'Camila compares the unaltered originals. The contradictory commitments and dependency are corroborated through the supplied evidence. The review takes three minutes and six stamina.',
 'roles':'Each specialist has accepted a specific limited role. Their actual presence is still required at execution.',
 'agreement':'Inez signs the chosen conditional terms. Ansel acknowledges the contradiction and refuses release. His refusal is recorded without inventing consent.',
 'prepare':'The verified records, signed conditions and specialist agreements support the final recovery plan. The mandate remains limited to this crisis.'},
 'plan':{'release':'Commit the ten-unit bridge allocation and select release of the East concession. Final execution will cost twenty more units and leave forty. The asset loss is real.',
 'retain':'Commit the ten-unit bridge allocation and select retention of the East concession. Final execution will cost forty-five more units and leave fifteen. The restricted reserve is real.'},
 'cover':'Elias separates the public approach and holds the agreed negotiation cover. It does not stop the armed contractor by itself.',
 'objective':'The route to the dispatch team remains contested. Enter the actual encounter; a predicted opening cannot substitute for victory.',
 'seal':'After the obstruction is stopped, Mavis brings the recovered originals through the agreed route. Camila verifies both against the observed hashes and seals the record packet.',
 'escort':'Martos brings the dispatch team through the secured passage to Inez. She receives and counts the actual arrivals. The escort costs eight stamina and two minutes.',
 'allocate':'Inez and Camila execute the signed allocation after records and personnel recovery. The chosen units are consumed once. The resulting asset disposition and reserve remain in the account, and the finite mandate expires.'}

# Two harmless, saved decisions per required recollection. None changes fixed history.
MEMORY_TASKS={
 'CA-F01':[dict(prompt='Finish the ordinary game before leaving.',options={'share':('Agree one last shared turn','Pilar takes the agreed last turn and gives back the tin.'),'count':('Count the pieces with Pilar','They count the pieces together; Pilar keeps the red counter.')}),dict(prompt='Pack something that belongs to her.',options={'tin':('Pack the worn game tin','Camila puts the tin in her bag. Elena checks her coat.'),'coat':('Ask about the coat left behind','Her guardian promises to return for the coat. Adoption is not conditional on this choice.')})],
 'CA-F02':[dict(prompt='Make room for supper.',options={'move':('Move the paper house safely','The unfinished house is placed on the sideboard.'),'ask':('Ask Mara to hold one wall','Mara helps move the house without making Camila finish it.')}),dict(prompt='Accept ordinary parental attention.',options={'show':('Show Father the crooked roof','He holds a wall while she repairs the roof.'),'explain':('Explain what she tried','He stays to hear her explanation after supper.')})],
 'CA-F03':[dict(prompt='Examine the supplied lesson.',options={'dates':('Compare the two waiting dates','The dates change who can afford the exchange.'),'ask':('Ask who needs the counters sooner','Her father names the dependency already supplied by the exercise.')}),dict(prompt='Keep an ordinary promise.',options={'outside':('Go outside with Mara','She leaves the counters for the daylight she promised.'),'mark':('Mark the time, then go outside','She marks the overlooked time and joins Mara.')})],
 'CA-F04':[dict(prompt='Examine the evidence still unseen.',options={'open':('Open the fourth envelope','The supplied refusal contradicts the assumed agreement.'),'list':('List the missing source, then open it','She marks the source as unknown before reading the refusal.')}),dict(prompt='Own the correction.',options={'revise':('Revise on a clean sheet','She keeps both accounts and corrects the dependency.'),'admit':('State the inference that failed','A likely answer was never an agreement. She revises it.')})],
 'CA-F05':[dict(prompt='Look at the cost of her successful operation.',options={'read':('Read the cancelled-shift report','The report names the lost shifts produced by the pressure.'),'request':('Request the available attendance record','Only part of the record is available; the unknown people remain unknown.')}),dict(prompt='Keep responsibility in the account.',options={'retain':('Retain the harm beside the success','The successful objective and its outsider cost remain together.'),'name':('State what her model omitted','She counted the owner’s concession and omitted the people losing work.')})],
 'CA-F06':[dict(prompt='Present the work behind the appointment.',options={'results':('Present the completed negotiations','The completed negotiations support her earned specialist appointment.'),'limit':('Include the revised reserve limit','The error and revision remain part of the professional record.')}),dict(prompt='Leave room for her own interests.',options={'dance':('Write about the dance class','She chooses an ordinary class she wants for herself.'),'pen':('Put away the report and choose a pen','She puts down the role and prepares an ordinary personal note.')})],
 'CA-F07':[dict(prompt='Hear the intention already made explicit.',options={'scope':('Ask what lies beyond finance','Her father describes responsibility for cooperation beyond her own speciality.'),'future':('Name the future he means','He confirms that he genuinely means her to succeed him.')}),dict(prompt='Distinguish intention from present authority.',options={'learn':('Identify what she still needs to learn','She remains Diamonds, with a serious preparation ahead.'),'boundary':('Acknowledge that he still commands','No leadership transfer or new command follows this conversation.')})],
 'CA-F08':[dict(prompt='Choose a defensible method within the old mandate.',options={'tuesday':('Accept Inez’s credible Tuesday limit','She changes the sequence within the entrusted resources.'),'verify':('Check the receiving sequence first','The sequence supports Tuesday; she agrees it and loses the earlier slot.')}),dict(prompt='Report the decision and its cost.',options={'cost':('State the narrower reserve','Her father accepts the defensible method and requires the receiving team retained.'),'uncertainty':('State what could still fail','She owns the remaining uncertainty and keeps the team until arrival.')})],
}

def ending_pages(d):
    release=d['choices']['plan']=='release'
    result='The East concession is gone. Forty allocation units remain for the next disruption.' if release else 'The East concession is retained. Fifteen allocation units remain, and the next commitment will have much less room.'
    lines=[p(result+' Payroll is funded. The dispatch team has arrived. Two lost shifts remain lost.',REC),
      b('camila-inez','The people came through, and the signed terms were carried out. That is what I can answer for.'),b('camila','It is what I asked you to answer for. The rest is mine.'),
      p('Later Mara pours the tea. Camila starts to explain why the solution was defensible, then notices the second cup and stops.',SIT),b('camila-mara','You can tell me about your day without submitting it for a mark.'),b('camila','That is a remarkably inefficient offer.'),b('camila-mara','Sit down.'),
      p('At the final private appointment, the Crow reads the full account, including the cost. Camila has left the corrected first hypothesis attached. His mask remains still above the page.',EXEC),
      b('camila',result+' I chose it. I will carry that limit into the next account.'),b('crow','Then carry it accurately. You preserved what I entrusted to you and made the decision that required your judgement.'),
      b('camila','You still intend me to hold all of it one day.'),b('crow','Yes. Preparation continues. My command remains mine.'),
      p('The answer gives her neither a coronation nor release from the work she has knowingly done. She is his daughter, his protégée and his financial Ace. She intends to remain. The chair beside his is occupied by someone who can give an account in her own words.'),
      p('Back in the private sitting room, she opens a chessboard and puts the planner away. Mara accepts a game on the condition that Camila permits her to finish a bad move before explaining it.',SIT),b('camila','I can promise silence. I cannot promise not to notice.'),p('Her competitive laugh comes easily. For the rest of the evening the next move is allowed to belong only to the board.')]
    lines=__import__('camila_campaign_expansion').ending(lines,b,p,release)
    __import__('camila_campaign_visuals').bind(lines,'CA-14-ending','text','locations/campaign/camila/receiving',__import__('camila_campaign_visuals').CURRENT,room=REC)
    return lines

def copy_scene(key,field):return deepcopy((MEMORIES if key.startswith('CA-F') else CHAPTERS)[key].get(field,[]))

__import__('camila_campaign_expansion').apply(CHAPTERS,MEMORIES,b,p)
__import__('camila_campaign_visuals').apply(CHAPTERS,MEMORIES)
