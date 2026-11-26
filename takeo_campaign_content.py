"""Empire of One: authored scenes; outcomes belong to the runtime receipts."""
from copy import deepcopy

HQ='site_01__briefing_room'
RELAY='site_02__briefing_room'
COMMAND='takeo_meridian__command'
RESEARCH='takeo_meridian__research'
ENTRY='takeo_meridian__entry'
ARCHIVE='takeo_meridian__archive'

def b(who=None,text='',narration=''):
    return dict(player='',speeches=[[who,text]] if who else [],narration=narration)
def p(text):return b(narration=text)

# Fine dates are deliberately relative except the confirmed 2024 and 2027 events.
MEMORIES={
 'TK-F01':dict(title='The captain',era='takeo_directive',background='directive_briefing',text=[
  p('Before Onami, Captain Mishima stands at the head of Directive 0’s briefing table. The United Nations seal is inside the folder, not on the door. There are no unit photographs in the corridor. Men who have spent the night carrying out its orders will return to other postings without a line explaining their absence. Takeo likes the arrangement. A conventional commander must make a performance of asking what his men already know needs doing. Here, the objective arrives sealed, and he is trusted to achieve it.'),
  b('takeo-deputy','The perimeter report leaves out the people still inside.', 'Kenji Arakawa keeps the folder open beneath his hand. Across the table, the medic has not taken off her field jacket. Its cuffs are stiff where she washed them.'),
  b('takeo','Then amend it. Do not bring me a report you cannot defend.'),
  b('takeo-medic','I can defend the number I treated. I cannot certify the people we left behind.'),
  p('He remembers the withdrawal clearly: the short transmission, the time remaining, Arakawa waiting for permission to send men back. There was no confusion to unravel afterward. Takeo chose the extraction window over the people beyond the perimeter. He would make the same choice with a quieter radio and better light. What irritates him now is the suggestion that a successful operation has become unfinished because someone dislikes its price.'),
  b('takeo','We recovered the team and completed the assignment. Put both facts in the report.'),
  b('takeo-deputy','And put your decision beside them. You gave the order to leave.'),
  p('The deputy has followed him through enough operations to know when the captain is angry. He does not mistake the stillness for patience. Takeo reads the casualty sheet again, not because the numbers trouble him but because Arakawa has made them a dispute about command. His squad’s skill, discipline and capacity to survive have always seemed to him the most honest qualifications for deciding who gets to leave a battlefield.'),
  b('takeo','A force that sacrifices itself for everyone it encounters ceases to be a force.'),
  b('takeo-medic','You did not ask whether we could reach them. I was there. You told us they were not part of the objective.'),
  p('She speaks about particular people. He hears a demand that his strongest men be made answerable to the needs of strangers. The difference does not embarrass him. Directive 0 has given him equipment, intelligence and a field in which the distinction can be enforced. For years, a satisfactory result has been enough for the people who sign his orders.'),
  b('takeo-deputy','If the work can be defended, Captain, sign the whole account.'),
  p('Takeo separates the casualty sheet from the operational summary. He signs the second with the same steady hand that gave the withdrawal signal. Arakawa remains standing. The captain puts down the pen, leaving the other page between them. For the first time that evening, no one moves when he dismisses the room.')]),
 'TK-F02':dict(title='An order to stop',era='takeo_dissolution',background='directive_briefing',text=[
  p('The dissolution order is shorter than the last deployment list. Directive 0 is being disbanded over ethical concerns: its conduct, its methods, and the distance between the authority it was given and the violence it exercised. Equipment is to be returned. Surviving records are to be placed under review. Takeo turns the final page, expecting an annex that tells him where to report. There is none. Beyond the briefing-room door, a quartermaster is counting equipment into cases.'),
  b('takeo-deputy','They are ending the unit. I will give evidence about my part in it.'),
  b('takeo','You think their signature changes what the world requires.'),
  p('Arakawa has brought his own copies. Takeo recognises the habit: duplicate the orders, check the routes, leave nothing necessary in another man’s pocket. He once valued it. Now the same care has been turned toward preserving a record that the captain cannot reduce to missions accomplished.'),
  b('takeo-deputy','It changes what they authorise. What you do after this belongs to you.'),
  b('takeo','They asked for a unit that could go where their public forces could not. We went. Now they want men who can pretend they never asked.'),
  b('takeo-deputy','Some of them may. That does not make every complaint false. You read the same reports I did.'),
  p('He did read them. There are details in those pages that no argument about secrecy can erase. Takeo has no need to erase them. He believes the institution has lost its nerve, not that the reports have mistaken him for someone else. The people reviewing Directive 0 can object to the way power was exercised because other men are still exercising power around them. He considers their protection evidence of dependence, and their dependence evidence that their judgement need not bind him.'),
  b('takeo','The world does not stop selecting the strong because a committee dislikes the result.'),
  b('takeo-deputy','Those people were not competing with you. You chose them as expendable.'),
  p('Arakawa’s voice has gone flat. It is easier to hear than an accusation shouted across the table. Takeo could accept another posting. He could submit his account, surrender the equipment and spend the rest of his career within a narrower command. None of those possibilities appeals to him. They require him to recognise a limit imposed by people he does not respect.'),
  b('takeo','And you will let them decide what your service was worth?'),
  b('takeo-deputy','I will answer for what I did. That includes following you.'),
  p('The deputy removes his unit patch and sets it beside the copies. Takeo watches the small square of cloth settle. He feels contempt, and beneath it the hard irritation of losing something useful. He will miss the access, the reach, the trained men who understood a gesture. He does not miss the authority that has withdrawn them. When he leaves, no order sends him to Onami. He is looking for a power willing to continue.')]),
 'TK-F03':dict(title='A man worth following',era='takeo_onami',background='onami_hall',text=[
  p('In 2024, the conquered command hall still smells of damaged plaster. Shinzo Kazama studies a map that has outgrown its original frame. Takeo has helped Onami conquer Japan, and there are officers outside waiting to be told what victory permits them to keep. Kazama has left them waiting. He is looking beyond the coastline. Takeo remembers why he chose to join this militant terrorist organisation: its leader wanted power without the consoling language that had surrounded Directive 0’s orders.'),
  b('takeo-kazama','You have commanded men. Can you accept an order?', 'Kazama does not rise for him. He clears a dispatch from the map with the back of his hand and indicates the space opposite.'),
  b('takeo','From a man who can carry it.'),
  b('takeo-kazama','Then look at what comes after this. Half the men outside want a country to reward them. I want a country that can carry the next war.'),
  p('Takeo has seen Kazama’s absolute strength, and he respects it. More than that, he respects the appetite behind it. Other leaders reach a defensible position and begin inventing reasons to remain there. Kazama treats the subjugation of Japan as a beginning. When he speaks of the world, he means territories, forces and people that must eventually submit. Takeo does not have to translate an assurance about peace into its useful military meaning.'),
  b('takeo','Occupation will take men away from the advance. There are districts that cannot be held by a flag.'),
  b('takeo-kazama','Then give me the force that can hold them. You are my military commander, Mishima. Do not bring me a victory that needs me in every street.'),
  p('There is a correction in it. Takeo accepts it without the silent resistance he used to reserve for distant superiors. Kazama is demanding something difficult from him, in person, with enough power to stake his own rule on the answer. Takeo finds that worthy of service. The distinction matters to him: he has not become incapable of obedience. He has become unwilling to offer it to anyone whose authority rests on permission alone.'),
  b('takeo','I will consolidate the command. After that, we can extend it.'),
  b('takeo-kazama','After that, you will tell me what it costs to extend it again.'),
  p('Months of service gather around that exchange: maps reopened after midnight, dispatches returned because a commander has counted territory without counting resistance, troops reorganised for the next demand. Takeo values the labour. Onami gives his violence a direction that does not end when the immediate assignment is complete. Its atrocities do not become doubts he must put aside; they belong to the same project he has willingly accepted.'),
  p('Before he leaves, Kazama moves a marker beyond the edge of Japan. Takeo watches where he places it. He has not asked for gratitude, a ceremonial title or a promise of personal safety. He leaves with work, and with the rare satisfaction of serving a man whose ambition does not require him to become smaller.')]),
 'TK-F04':dict(title='The original weapon',era='takeo_research',background='onami_research',text=[
  p('After the 2024 conquest and before the 2027 defeat, Onami’s research rooms acquire the same late hours as its command hall. Senda has left a meal untouched beside two folders. One describes observations of Mishima’s Nanoengine. The other bears the Shinigami Protocol heading. The distance between them is the reason Takeo has come. His body can break a defensive formation; it cannot stand at every crossing that Kazama intends to hold.'),
  b('takeo-researcher','A baseline gives us a question. It does not give us another you.'),
  b('takeo','Then stop presenting the question as a result.'),
  p('He lifts the thinner folder. There are projected capabilities in it that no observed subject has demonstrated reliably. Senda has marked those passages. The corrections annoy Takeo less than the promises did. He wants an army with power he can deploy, not a roomful of people competing to tell him that his wishes have already become facts.'),
  b('takeo-researcher','Your Nanoengine is the baseline. It is not evidence that the subjects can develop the same power. I cannot make that claim.'),
  b('takeo','I require the battlefield effect. Establish what the programme can actually produce.'),
  p('Through the glass, an attendant replaces the paper on an examination couch. The ordinary care of the movement catches his attention: the corners tucked down, the crease smoothed away. Senda waits until the attendant leaves before opening the observations. The people behind those pages have names elsewhere. Here, the columns make them easier to compare.'),
  b('takeo-researcher','There are objections to continuing with the subjects who are deteriorating.'),
  b('takeo','Are the objections about the observations?'),
  b('takeo-researcher','They are about what continued observation requires of them.'),
  p('Takeo puts the folder down. He understands the distinction. Pain has never seemed to him an argument against a useful result; it is something to account for when it changes performance. Nor does the absence of consent trouble him. In his view, people without the strength to determine their own conditions will inevitably live under conditions chosen by others. He intends to be the one choosing.'),
  b('takeo','Continue the work. Remove unsupported claims. Bring me a result that survives examination.'),
  p('Senda crosses out a line in the forecast, then stops with the pen held above the next. Takeo is already looking at the deployment map pinned beside the glass. He imagines commanders able to carry Onami’s expansion beyond the reach of his own hands. It is an ambition large enough, to him, to absorb any number of individual lives without becoming a question about them.'),
  p('The examination room empties. His reflection remains over the couch: composed, uninjured, waiting for improvement. The thinner folder is still an aspiration when he leaves. He has authorised its continuation, not proved its promises.')]),
 'TK-F05':dict(title='What survived',era='takeo_founding',background='early_command',text=[
  p('In 2027, after the United Nations Military defeats Onami, Takeo receives confirmation that Shinzo Kazama is dead. The report does not identify his killer. Takeo reads it twice. Around him, the remnants have begun speaking in the language of temporary arrangements: somewhere to sleep, someone to surrender to, a route that might still be open. There is an empty place at the table. For once, he does not expect the man who belongs there to arrive with a larger demand.'),
  b('takeo-officer','Are we rebuilding Onami, or following you?'),
  b('takeo','Count the units that can move. Leave the dead off the strength return.'),
  p('The officer does not leave. He has men waiting for an answer they can carry back. Takeo recognises the need even as he dislikes it. He could scatter what remains, preserve himself and let Onami become another organisation described in the past tense. His own power has survived. That makes retreat possible, and it makes retreat intolerable to him. He has not spent years commanding a force in order to become a powerful man with nothing left to command.'),
  b('takeo-officer','Some of them will follow Kazama’s name. Others want to know whether there is still a war.'),
  b('takeo','Kazama is dead. They will follow the man who can keep a force in the field.'),
  p('He will not pretend that death has made Kazama contemptible. Takeo respected his strength when it was real, and the memory does not disappear because the command has fallen. But respect is no reason to kneel beside a ruined organisation. Kazama wanted the world brought under power. Preserving his empty chair would accomplish nothing.'),
  b('takeo-officer','And the research staff? We have requests to disperse them.'),
  b('takeo','Retain the staff we can use. Retain the observations. The Shinigami Protocol continues.'),
  p('That settles what kind of refuge he is offering. The new organisation will shelter the means of further conquest: armed personnel, supply routes, discipline and research. It will not exist to provide absolution for survivors. Men who expected to be thanked for their loyalty hear assignments instead. Those too injured to fill them are moved to a separate list. He does not ask who has family still missing.'),
  b('takeo-officer','What name do I give them?'),
  b('takeo','Shinokami.'),
  p('The officer writes it at the top of a clean sheet. Takeo watches him rule the first column. Directive 0 had been able to revoke his commission. Onami’s command had ended with a man he considered worthy of following. This time the authority will be his. He will choose the objectives, decide which lives may be spent and pursue the work without waiting for another institution to recover its conscience.'),
  p('He pulls the radio toward him and begins calling the surviving units. Some answer immediately. Some require a second call. The empty chair stays where it is until he orders the room rearranged.')]),
 'TK-F06':dict(title='One',era='takeo_one',background='early_archive',text=[
  p('Later, under the Shinokami, the private record room has a chair too large for the boy sitting in it. His feet do not rest comfortably on the floor. He keeps them still anyway. Takeo enters while Senda is waiting over a blank field on the cover sheet. The boy is his son. No one in the room needs to explain the relationship, and no one uses it to ask Takeo to sit beside him.'),
  b('takeo-researcher','What name belongs on the record?'),
  b('takeo','One. That is sufficient.'),
  p('The boy looks up at the sound of the designation. Takeo notices the speed of the response and counts it as attention. The child’s gaze moves from his face to the folder in his hand. Takeo opens it before the boy can decide whether anything else is expected. The observations are exceptional. He pauses over one result, compares it with the earlier entries, and asks Senda whether it has been repeated.'),
  b('takeo-researcher','The improvement is recorded. It does not tell us what he will become.'),
  b('takeo','It tells you which subject deserves continued work.'),
  p('He has heard objections framed around the boy’s relationship to him. They strike him as evidence of a weakness he refuses to indulge. If he exempts his own blood from the demands imposed on others, then even his household becomes an exception to the rule by which he claims to govern. He finds that thought more offensive than the sight of his son watching for permission to move.'),
  b('takeo-researcher','He has been waiting to see you.'),
  b('takeo','He is seeing me.'),
  p('Senda’s pen stops. The answer is exact enough to make another attempt difficult. Takeo has no hidden reassurance ready, no gentler name that he will use when the staff leave. He wants the boy’s potential developed into power. The fact that it is his son’s life being narrowed around that demand strengthens his sense of entitlement rather than weakening it.'),
  b('takeo','Stand.'),
  p('The boy gets down from the chair. One foot has gone numb; he places it carefully before straightening. Takeo waits until he is balanced, then returns his attention to the folder. He mistakes the child’s careful silence for an absence of competing needs. It is convenient to do so. A numbered subject can be evaluated, directed and retained. A son might eventually ask for something the programme has no use for.'),
  b('takeo','Record the result without embellishment. I do not want praise. I want to know what he can do.'),
  p('Senda fills the designation field. The boy remains standing while the adults close the review. Outside, someone laughs at a remark too distant to distinguish. His head turns a little toward the sound. Takeo is already reaching for the next page.')]),
 'TK-F07':dict(title='The retained success',era='takeo_postraid',background='early_command',text=[
  p('After the Interpol raid, the survivor list fits on a page that once needed an index. One has escaped. The other subjects are dead; the account does not identify who killed them. Takeo lays the page flat with both hands. The failure is not abstract. Years of work have passed beyond his control, and the most exceptional subject has left without his permission.'),
  b('takeo','You survived.'),
  b('thirteen','There was no one left to answer.'),
  p('Thirteen stands with his hands against his trousers. He had once been the weakest child in the programme. Takeo remembers that assessment, and revises it as readily as he would revise a deployment figure. Survival has changed the boy’s value to him. It has not made him curious about what the boy remembers when the room becomes quiet.'),
  b('takeo','You will report to me. Your training continues.'),
  b('thirteen','Here?'),
  p('The question is small. Takeo considers the condition of the remaining facilities before answering. Thirteen is looking at the doorway. When footsteps stop outside it, his shoulders stiffen. Neither response enters the commander’s assessment except as something that discipline might correct.'),
  b('takeo','Where I assign you. You are the success we retained. Act accordingly.'),
  p('Retained is the word that makes the distinction possible. One’s exceptional performance has not become imaginary because he escaped, but Takeo cannot issue orders to an absence. Thirteen is here. He can still be shaped into a subordinate whose strength extends Takeo’s reach. The commander offers more attention, closer instruction and a future arranged entirely around usefulness. To a child waiting to learn whether he has a place, the offer can resemble rescue.'),
  b('thirteen','What do you want me to do first?'),
  b('takeo','Learn to give an answer before I have to ask twice.'),
  p('Thirteen nods immediately. Takeo sees improvement. There will be years in which he measures the young man by how quickly he understands an order and how completely he carries it out. Later, when he gives him command across the water, he will regard that distance as proof that the work succeeded. He will not consider what the distance permits Thirteen to decide without him.'),
  p('For now, the boy waits until Takeo dismisses him. The door closes softly. Takeo changes a heading on the assessment, replacing a comparison with the dead subjects with an instruction for continued development. He has found a use for the survivor. He has asked nothing about the grief.')]),
 'TK-F08':dict(title='Terms across the water',era='takeo_supply',background='kestrel_reception',text=[
  p('At Kestrel, after the raid and before the present crisis, Takeo opens the American map for Sylvanis. There are routes pencilled across the water and an unmarked space where a regional command might eventually stand. He has a force to send and a subordinate he intends to put over it. What he lacks is a reliable supply arrangement. Sylvanis notices that Takeo has placed his chair where the map will be visible without inviting him to sit beside it.'),
  b('sylvanis','You want regular quantities. Such a tidy word, regular.'),
  b('takeo','I want the terms in writing.'),
  b('sylvanis','Then read what they buy. They do not buy me.'),
  p('Takeo has never enjoyed the pause Sylvanis leaves after an answer. It invites him to fill the silence with a demand that can be refused. He keeps his attention on the proposed deliveries of Red Magic and Blue Magic. Temporary enhancement may serve the expansion, but it is not the reproducible force promised by his research forecasts. He wants both, on terms he can make predictable.'),
  b('takeo','Thirteen will command the force. Supply does not confer authority over him.'),
  b('sylvanis','Of course. Your young commander will obey you. The people carrying my stock will still expect payment.'),
  p('The amusement is deliberate. Takeo has dealt with men who become agreeable when they realise what his hands can do. Sylvanis is not one of them. His power is real, his appetites are his own, and a threat would settle none of the quantities on the page. Takeo resents the necessity of the bargain precisely because he understands it.'),
  b('takeo','We establish the foothold. Then we expand its capacity. I will not spend the next decade guarding the same patch of ground.'),
  b('sylvanis','No. You would find that unbearable. All that strength, keeping something the size it already is.'),
  p('Takeo lets the remark pass. Japan did not satisfy Kazama, and command of the Shinokami does not satisfy him. The Americas offer room, resources and a larger field in which to prove that the defeat of Onami did not set the limit of his life. He would never offer Sylvanis that explanation. The supplier already finds too much entertainment in his necessities.'),
  b('takeo','Deliver what is contracted. I will provide the force.'),
  p('He reads the service obligations twice before signing. In time, Pacific Relay will become Thirteen’s standing command and the first expansion will become an established foothold. Tonight it is still an agreement between men who do not trust one another. Takeo accepts the dependency because he expects to outgrow it. Sylvanis takes his copy without making any such promise.')]),
}

CHAPTERS={}
def chapter(n,title,room,opening,closing):
    CHAPTERS[f'TK-{n:02}']=dict(title=title,room=room,briefing=opening,aftermath=closing)

chapter(1,'State the Result',HQ,[
 p('Kestrel is awake before the first strength return reaches its command room. Through the closed door come the small sounds of an organisation making itself ready for inspection: a trolley stopped short of the threshold, a conversation lowered, the latch tested before anyone knocks. Takeo has made no demand for silence. His presence has become a condition people plan around. At roughly fifty-six, with little of that time visible in his face, he watches younger officers grow careful in rooms he has already outlived their ambitions in.'),
 b('takeo','State the result. Not the promise.'),
 p('Three reports lie on the table. Keisuke counts recruited bodies. Thirteen, writing from Pacific Relay, counts units that can still move. Sylvanis’s delivery sheet counts what the Shinokami must keep buying. All three describe progress. Put beside one another, they describe a force whose next advance depends on men who have never agreed what ready means. Takeo smooths the pages with his palm, as if their disagreement were a crease.'),
 p('Pacific Relay is already his American foothold. Meridian would make it the base of something larger: a regional command with research capacity, its own routes and enough force to survive without waiting for him to cross the water. Thirteen will keep American command. Keisuke will handle enforcement and recruitment. The arrangement is useful only if command can travel farther than Takeo’s physical presence.'),
 b('takeo','A shipment is not an army. Count the men who can deploy. Then tell me what will keep them there.'),
 p('He writes the instruction across Keisuke’s summary. It is not concern for the recruits. An exhausted man who cannot hold a position has been entered as an asset without delivering one. Takeo dislikes waste more than suffering, and he has built a command in which the distinction is felt by everyone beneath him. A junior officer will spend the morning trying to decide whether an accurate answer is safer than a pleasing one.'),
 p('The proposed research centre holds his attention longest. His own strength has carried the Shinokami through challenges that would have ended a lesser organisation. But he has no interest in spending his life hurrying between fires set beyond his reach. Power worth founding an empire upon must multiply. A single overwhelming body, however formidable, still leaves an empty room when it walks out.'),
 b('takeo','Meridian proceeds. I will inspect the approach myself.')],
 [p('He marks the site on the map and closes the report. Outside, the waiting officer stands straighter as the latch turns. Takeo gives him the amended figures and watches him read the instruction twice. The man asks no questions. For the moment, Takeo considers that efficiency.'),
 p('On the table, Thirteen’s note remains beneath the supply schedule. Its last sentence concerns a route that cannot carry the force described in Keisuke’s return. Takeo takes it with him.')])
chapter(2,'Directive 0',ENTRY,[
 p('The Meridian approach ends in a barricade assembled across the service road. Behind it, armed men have chosen positions that would make an ordinary convoy hesitate. Takeo gets out before his driver can finish describing them. He has come to inspect a route, and someone has mistaken the route for a place where his authority can be negotiated. The commander’s loudspeaker calls the obstruction a border.'),
 b('takeo','Clear the road. Keep the route usable.'),
 p('He gives the order to his own escort, not the men behind the barricade. They begin moving back from the space he will need. Fear spreads across the opposing line unevenly: first recognition, then a glance toward a superior who cannot afford to be the first to step away. Takeo has watched that sequence in several uniforms. He does not pity the men trapped inside it. To him, their need for reassurance is one more admission that someone stronger must decide the terms.'),
 p('A copied demand has been fixed to the gate. Beneath the present accusations is an old designation: Directive 0. For a moment the damaged entrance gives way to a sealed briefing room, equipment cases and a deputy who would not accept a signature on half a report. The memory has retained its small irritations more clearly than the applause that followed other operations.'),
 p('Directive 0 had understood what he was useful for. Until it did not. Takeo remembers the efficiency with which a classified institution could make a problem disappear, then the solemn voices that discovered objections to the work. He can still recall how heavy the dissolution folder felt for so few pages.'),
 b('takeo','Keep the vehicles clear of the entrance. I want this road open when we are finished.')],
 [p('After the resistance is cleared, the road is visible again. What it leads to is less impressive than the briefing promised. An access gate is damaged; vehicles have been left where supplies ought to move. Takeo has overcome the men who challenged him. He still needs an answer about whether his own command can use what remains.'),
 p('He removes the copied demand from the gate. Directive 0’s name survives among people who were never meant to know it. He folds the paper once and carries it into Meridian. No one offers to take it from his hand.')])
chapter(3,'A Man Worth Following',HQ,[
 p('Sylvanis arrives with the ease of a man who expects the door to open and feels no need to thank it. He lays the delivery schedule on the table, but his attention follows the departing officer. The man has agreed to three instructions in succession. On the last, he answered before Takeo finished speaking.'),
 b('sylvanis','Your new officers have learned to agree with you before the question is finished.'),
 b('takeo','We are discussing deliveries.'),
 b('sylvanis','Yes. How comforting to have something countable.'),
 p('Takeo remains standing. Sylvanis studies the proposed quantities as though they were a mildly amusing habit. Neither posture is accidental. The Human Siege Engine is accustomed to rooms adjusting themselves around him; Sylvanis occupies his own share without adjustment. Takeo needs the drugs and the supply connection. He would prefer to need neither.'),
 b('takeo','The schedule supports the first stage. What can you guarantee after that?'),
 b('sylvanis','What I sign. Such a disappointing answer, I know. You were hoping for loyalty at the price of freight.'),
 p('Takeo turns the paper so its conditions face him. The insolence is inexpensive for Sylvanis because he can sustain it. There was another man whose refusal to accommodate Takeo had drawn a different response. Kazama could give an order without begging the room to agree that he deserved to. Takeo had respected the force behind it, and the scale of the appetite it served.'),
 b('takeo','I have followed a man before. Do not mistake a purchase for that.'),
 b('sylvanis','I would never confuse myself with someone you remember so fondly.'),
 p('The word fondly earns no reply. Takeo’s regard for Kazama is real, but he will not offer it to this man as entertainment. He points instead to a limit in the delivery schedule. Sylvanis agrees to correct the quantity and refuses the extension of obligation beneath it. The negotiation continues, exact and unpleasant, between two men who know intimidation will not settle it.')],
 [p('Takeo accepts the bounded schedule. When Sylvanis leaves, he marks the services supplied by outside parties in a different ink. The contract has given him access, and no obedience at all.'),
 p('For a while he remains beside the map. He can remember taking an order from Kazama without resenting it. The memory does not make his present officers more tolerable. It gives him a measure by which he finds them wanting, and no reason to ask whether he has ever offered them the same freedom to choose.')])
chapter(4,'The Original Weapon',RESEARCH,[
 p('The Meridian research room has been prepared for a commander who is expected to like the answer. The projection is large; the observations beneath it are small. Takeo stands close enough to read both. The heading promises a reproducible Shinigami force. The individual results do not. A supervisor has circled the difference between temporary drug effects and the years of development behind Thirteen, then left the ambitious heading untouched.'),
 b('takeo','Strike the production claim. Keep the observations.'),
 p('Someone beside him begins explaining what the forecast could mean if the next stage succeeds. Takeo raises one hand. The explanation stops. He dislikes optimism when it interferes with command. He also knows what has invited it: he has demanded a force worthy of his own power, and the staff have begun reporting proximity to his desire as though it were an experimental result.'),
 b('takeo','I can read what you hope to achieve. Show me what has happened.'),
 p('The pages turn more slowly. He sees exceptional performance, uneven development, effects that do not repeat on demand. None of it changes the Nanoengine in his own body. He flexes his hand above the table and considers the absurdity of an empire dependent on that one hand being present. Onami understood the promise of making his battlefield effect available elsewhere. He has carried that ambition through its defeat and into the organisation he founded.'),
 p('The suffering in the observations does not interrupt his assessment. A warning about deterioration matters when it threatens a result; a plea for an end to the work has no place in his calculation. He is not searching for language that makes the programme humane. He wants it honest enough to be useful.'),
 b('takeo','There will be no deployment estimate built from an exception. Correct it before it reaches command again.')],
 [p('The corrected forecast occupies less space. Under it sits a worse problem: the accumulated experimental record is unique. There are scattered historical traces elsewhere, but no complete backup capable of replacing this archive. The planned transfer would put the work of years on the same contested routes as the regional force.'),
 p('Takeo asks for the transfer schedule. For the first time, the archive appears on his map as something that can be lost without anyone defeating him in a room. He leaves the reduced forecast where the staff must continue looking at it.')])
chapter(5,'What Survived',COMMAND,[
 p('The command room overlooks a yard where vehicles wait with their rear doors open. From above, the arrangement looks orderly. On the table, two separate lists have claimed the same capacity. One would carry laboratory equipment. The other would carry the personnel needed to sustain the regional force. There is not enough transport to make both promises true.'),
 b('takeo','I will inspect the force we have. Not the force you put in the heading.'),
 p('Keisuke’s return counts every recruit as deployable. Thirteen’s written amendment describes a route that could not be held. Between them are men whose exhaustion has vanished into a total and equipment whose value assumes it reaches an intact programme. Takeo runs a finger down each list. The conflict annoys him, but its shape is familiar. After Onami fell, he had to decide what could be carried out of a defeat and made to serve another ambition.'),
 p('He had not founded Shinokami because the survivors deserved a home. He had founded it because armed men, research and supply could still be made into power. That distinction remains clear to him. He can spend equipment to keep an organised force alive, or spend transport resilience to carry the equipment. Neither choice requires him to pretend the people involved are equals whose interests he must weigh against his own.'),
 p('Outside, a driver climbs down to ask where his vehicle is wanted. The answer will run through several people before reaching him. Takeo watches the delay and remembers the first radios answering under the new name. A force begins when enough people believe an order will be followed by another one. It ends when every man decides for himself what can be abandoned.'),
 b('takeo','Bring the loading figures. We will choose what goes, and stop assigning the same capacity twice.'),
 p('Prioritising personnel will leave laboratory equipment behind. Giving the heavy transport to equipment will cost two vehicle sections during the later withdrawal. He studies the figures until each loss is something he can name.')],
 [p('The selected priority moves down the chain of command. In the yard, men stop waiting for a version of the order that gives everyone what they requested. Loads are shifted. A space opens where something had been promised a place.'),
 p('Takeo remains at the window until the movement becomes coherent. There is no satisfaction in the loss itself. There is satisfaction in seeing his decision become an arrangement of bodies and machinery. It is the first pleasure he remembers from the days after Onami, when an organisation with a new name began answering him.')])
chapter(6,'One',RESEARCH,[
 p('Takeo has the room cleared before opening the designation index. The book contains less than the experimental archive: identifiers, status, the high-level facts needed to know what was once under his control. One remains marked escaped. There is no chosen name beside the designation and no address. He sets it next to the replication forecast. Several of its most confident claims rely on the performance of a subject the programme no longer holds.'),
 b('takeo','Do not turn an escaped subject into a production estimate.'),
 p('No one is left in the room to answer. He writes the correction himself. His son’s exceptional results remain exceptional. Losing possession of the boy did not make them false, however much he dislikes the distinction. What it did was expose a failure in the kind of power Takeo had imagined he was building. Strength developed inside his command had continued beyond it.'),
 p('He remembers the record room and the blank name field more clearly than he remembers the boy’s face that day. One had been sufficient for the work. It told the staff where to place a result and the child when to answer. Takeo had seen no purpose in granting an identity that might compete with the one he intended to make useful.'),
 p('That judgement has not softened with time. He does not look at the designation and discover the father he should have been. He considers the resources spent, the capacity lost, and the presumption of departure. His irritation is sharpened by the possibility he cannot control: somewhere beyond this room, his son may have become powerful without being his.'),
 b('takeo','Exceptional is not reproducible.'),
 p('He underlines the sentence once. The correction belongs to the forecast, but his hand rests on the index afterward. The page will not supply the life missing from it. It cannot make a command reach the person he reduced to a number.')],
 [p('He closes the designation index without changing the entry. The experiment records remain elsewhere; this thin book cannot reconstruct them. Nor does it offer a route to the escaped boy.'),
 p('When the door opens, Takeo has already put the forecast back on top. He gives the next instruction in his ordinary voice. The private review has disturbed his sense of ownership, not awakened an interest in asking what his son wanted.')])
chapter(7,'Thirteen',RELAY,[
 p('At Pacific Relay, Thirteen has placed the original report beside a corrected one. He remains standing when Takeo enters. The room has the practical wear of an occupied command: a repaired chair, old route markings beneath new ones, a cup moved far enough from the papers that it cannot spill. Takeo notices the arrangement before he notices that Thirteen’s hands are resting flat against his trousers.'),
 b('thirteen','I withdrew the unit. Your order left it with no resupply.'),
 b('takeo','Your report said the position held.'),
 b('thirteen','The men held. The position did not.'),
 p('The answer comes without an apology. Takeo looks up from the page. Years ago, a pause this long would have made the boy try again with whatever words he thought the commander wanted. Now Thirteen waits. He has a force behind the report, living people available for the next operation because he chose to move them.'),
 b('takeo','You concealed a withdrawal.'),
 b('thirteen','Yes.'),
 b('takeo','Why?'),
 p('Thirteen’s gaze lowers to the first report, then returns. He does not claim that the message was lost or that someone misunderstood him. He has had time to consider those answers. They would leave the next order just as impossible.'),
 b('thirteen','I expected you to order us back before the route was restored. So I gave you the answer that kept us here.'),
 p('Takeo steps closer to the table. Thirteen does not move away. The defiance is not theatrical; it is the unhelpful solidity of a fact. An intact unit stands behind a dishonest report. Punishing the decision and overlooking the lie would teach the wrong lesson in either direction. Takeo wants a subordinate who can act beyond his sight, but resents discovering what independent action feels like when it contradicts him.'),
 b('takeo','You denied command the information needed to change the order.'),
 b('thirteen','Then let the information reach you this time. We cannot hold that position without supply.'),
 p('The younger man’s voice stays controlled. Takeo remembers a child asking what he should do first, desperate to place one foot on safe ground. The commander before him is asking what his force can actually achieve. Takeo can recognise the difference without enjoying it.')],
 [p('Takeo takes the corrected report. Thirteen keeps his command, and the withdrawal remains recorded as a withdrawal. The earlier deception is entered separately. Neither man is permitted to make one fact erase the other.'),
 b('takeo','When a position cannot be held, state what can. I will have the loss before I have a false success.'),
 b('thirteen','Then I need an order that says what we are preserving.'),
 p('Takeo does not answer immediately. Beyond the window, a returning unit breaks formation and begins unloading. He watches how many hands are needed to bring a single vehicle back into service. Thirteen waits beside the table until he looks away.')])
chapter(8,'Across the Water',COMMAND,[
 p('The transfer ledger arrives with three sets of attachments. Transport belongs to one contractor, servicing to another, and the temporary drug supply comes through a third agreement. Each arrangement looked manageable when it was signed. Together they describe a command that can be stopped by people who never have to meet Takeo in the field. He lays the contracts out until the points of dependence form a route across the table.'),
 b('takeo','Separate what we own from what we are allowed to use.'),
 p('An officer has used the word secured beside every service with a current contract. Takeo crosses it out. A signature may secure access for a time. It does not make the driver, the workshop or the supply chain answer to him. The difference has become visible because the expansion needs them all at once. Pacific Relay can continue as a foothold; the larger Meridian ambition has been growing around borrowed capacity.'),
 p('He remembers the first bargain with Sylvanis, and the care with which he read it. Nothing in the clauses has secretly changed. What has changed is the scale of what he needs them to support. He accepted dependence as a temporary expedient and kept building while it remained beneath him. His officers learned to call the resulting structure his.'),
 b('takeo','Trace each service to the party that can stop it. I want the answer even if it is the same party three times.'),
 p('The name that returns is the Syndicate. That establishes a capacity to interfere, not proof of a takeover already under way. Takeo is too experienced to confuse the two when it matters. He begins looking for independent routes. He also rereads the arrangements for everything Sylvanis had refused to promise.'),
 p('He had believed growth would free him from the supplier. Instead, each new obligation has made interruption more expensive. The discovery brings an anger he can use: cold enough to keep examining the page after he wants to tear it.')],
 [p('The checked ledger stays open on the command table. Outside dependence is now an established constraint, and the search for an independent route has become urgent. Takeo has grounds for suspicion. He does not yet have evidence of the Crow’s next move.'),
 p('He sends the findings down the chain with a demand for alternatives. For once, he needs his officers to tell him exactly what his organisation cannot do.')])
chapter(9,'The Last Captain',ENTRY,[
 p('Kenji Arakawa waits where the approach widens enough for both parties to withdraw. He is older than the deputy in Takeo’s memory. The difference is visible around the eyes and in the care with which he shifts his weight. Takeo’s own face has changed much less. For a moment, the imbalance seems to him an argument that requires no words. Arakawa does not look at him as though it settles anything.'),
 b('takeo-deputy','Kenji Arakawa. Former Directive 0 deputy. This operation is authorised to stop the regional programme and secure its records.'),
 b('takeo','You know what an assault on me costs.'),
 b('takeo-deputy','That is why you are not the objective.'),
 p('He offers an authenticated notice. Takeo accepts it without taking his eyes off him. The deputy’s teams are moving around the programme, its records and the routes it needs. There is no claim to have found a switch that turns off Nanoengine, no new weapon presented as an answer to his body. Arakawa has remembered what can happen to men sent merely to stand in Takeo’s way.'),
 b('takeo','You spent years following my orders. Now you have found a cleaner signature.'),
 b('takeo-deputy','My service is part of the review. The records are not being collected to make me innocent.'),
 p('Takeo opens the notice. The provision is there, in plain language. He would prefer hypocrisy; it would give him an easier way to dismiss the man. Arakawa has not denied what they did together. He has chosen to place it where someone other than Takeo can judge it.'),
 b('takeo','Directive 0 did what they could not bring themselves to do in public.'),
 b('takeo-deputy','And it ended. You joined Onami afterward. No one gave you that order.'),
 p('For a few seconds neither speaks. The gap contains the last briefing room, the patch on the table, the road that took Takeo toward a man he considered worth serving. He does not offer regret. Arakawa has not asked for a confession that will turn him into someone else.'),
 b('takeo','You will not take the programme.'),
 b('takeo-deputy','Then you know what we are here for.')],
 [p('Arakawa withdraws along the approach with his people. Takeo retains the demand. Its authority and its objectives belong to the UN operation; the contracts on his table belong to the Syndicate. The two threats may converge without becoming one.'),
 p('He watches the deputy leave until the road bends out of sight. The man has failed to impress him with strength and succeeded in making strength insufficient to answer the question. That irritates Takeo far more.')])
chapter(10,'Good News Only',COMMAND,[
 p('Keisuke brings the original returns himself. He is well prepared: the pages are ordered, the discrepancies marked, the explanation ready before Takeo asks for it. He has built a career on making reluctant people comply. There is nothing foolish about the man standing across the table. That is why the selection of reassuring numbers is harder to dismiss as a mistake.'),
 b('keisuke','The recruits reported ready. Their officers signed for them.'),
 b('takeo','You punished the officer who reported otherwise.'),
 p('Keisuke places the original beside his summary. The omission is visible between them. A unit short of capacity has become ready through a change in language, and a warning has become evidence of the warning’s author being unreliable. Takeo lets the silence continue until Keisuke has to decide whether his prepared explanation is still useful.'),
 b('keisuke','He challenged the deployment in front of the men. If I let that stand, every shortfall becomes a reason to refuse an order.'),
 b('takeo','Did punishing him restore the capacity?'),
 b('keisuke','No.'),
 p('The answer costs him more than the original distortion. Takeo can see that. He has rewarded certainty, punished hesitation and treated bad news as an obstacle brought into the room by the person reporting it. Keisuke has learned the system well enough to reproduce it beneath him. Recognising the result does not make Takeo wish to become a kinder commander. It makes him angry that his own machinery has begun feeding him useless information.'),
 b('takeo','You will report under countersignature. You will not discipline the author of an adverse return before it reaches command.'),
 b('keisuke','I can maintain discipline under that restriction.'),
 b('takeo','Then maintain it. The report reaches me first.'),
 p('Keisuke gathers the pages only after Takeo releases them. His enforcement and liaison work remain useful. His discretion does not remain intact. The distinction gives him a place to stand without giving him a defence of what he has done.')],
 [p('The next return carries two signatures. Takeo reads the adverse entries before the total. Keisuke waits without supplying a more attractive version of them.'),
 p('No apology is offered to the officer who was punished. The changed order protects the passage of information because command needs it. The people who live under the rule will discover its limits later. For now, a report has reached the table with its warning still attached.')])
chapter(11,'Borrowed Ground',ENTRY,[
 p('The service gate is closed when Takeo reaches it. A contractor who had been careful to answer every call now sends a written denial of access. The instruction comes through the Syndicate. Beyond the gate, armed personnel are taking control of assets that Takeo’s officers had been describing as secured. The withdrawal of support and the local seizure have finally given his suspicion a shape he can strike.'),
 b('takeo','Break their local control. Keep the independent route open.'),
 p('The Crow’s takeover has begun at Meridian. Takeo studies the movement rather than the insult. Vehicles have been positioned to narrow the route; people who know the site are using its service arrangements against the force that relied on them. Their strength lies in the preparation, not in any belief that one of them can overpower him. He recognises the logic, and hates being made to respect its usefulness.'),
 p('He could tear a gate from its housing. That would not restore the withdrawn drivers, reopen every workshop or force Sylvanis to continue a bargain he has left. Each problem exists at a different distance from his hands. The command he intended to expand has become a set of demands arriving at once.'),
 b('takeo','No pursuit beyond the route. I want a passage our force can use.'),
 p('The restraint is deliberate. He wants the local seizure broken, not a satisfying chase that leaves the crossing unavailable. Behind the service buildings, the UN operation is still moving toward the records under its own authority. Arakawa has not become the Crow’s subordinate merely because their attacks on Takeo’s plans have found the same hour.'),
 p('Takeo advances toward the gate. The men behind it begin moving before he touches it. For a moment, force is again a language in which he can make himself understood without ambiguity.')],
 [p('The cleared route carries its first vehicles through while the damaged service area is still being checked. Takeo does not call the whole complex secure. He has won access that must now be used before another part of the operation closes around it.'),
 p('News arrives from the archive perimeter. Arakawa’s teams are still moving. The relief of a settled local fight lasts only as long as it takes to unfold the next message.')])
chapter(12,'Name the Objective',RELAY,[
 p('Thirteen has cleared everything from the table except the current routes. He places the orders on them one at a time. Hold Pacific Relay. Preserve the research transfer. Reinforce Takeo. Each instruction can be read without difficulty. The difficulty appears when Thirteen puts a finger on each of the three positions and leaves it there.'),
 b('thirteen','Name the objective. I cannot hold three positions.'),
 p('Takeo studies the distances. The archive’s transfer window will close before the command can clear a route wide enough for every demand. His own power is available, intact and terrible. It cannot put him on both sides of the water at once. The staff have stopped offering optimistic estimates. He has finally obtained a truthful picture, and it contains a loss he cannot order out of existence.'),
 b('takeo','You have the force to hold the relay.'),
 b('thirteen','If it remains here. If I divide it as ordered, I will send you three reports about positions I could not keep.'),
 p('There is no raised voice and no appeal to affection. Thirteen is refusing the impossible in the language Takeo taught him to value: capacities, positions, results. Behind it is something less convenient. He expects his own judgement to count. Takeo feels the old impulse to make the room remember who commands it, then looks again at the routes. Fear would change the answer spoken aloud. It would not change the distance.'),
 b('takeo','Preserve the regional force. Keep your command intact. I will deny the archive.'),
 b('thirteen','The research transfer is cancelled?'),
 b('takeo','Cancelled. You are not to divide your force to recover it.'),
 p('The unique programme archive will be lost. There is no complete backup behind the decision. Takeo considers the years represented by it, the work he carried out of Onami, the lives he spent pursuing a force that could reproduce its promise. He does not suddenly regret those lives. He refuses to let the research become another man’s instrument at the price of losing the command he still possesses.'),
 p('He writes Keisuke’s bounded withdrawal duty beneath the preservation order. For once, the subordinates will receive a priority before they have to invent one.')],
 [b('thirteen','Preserve the regional force. Keep the relay. No detachment for the archive.'),
 b('takeo','That is the order.'),
 p('Thirteen takes his copy. The relief is visible only in the speed with which he begins working: no pause to interpret what Takeo will later claim he meant. A separate signed reply from Sylvanis closes the question of contested support. The supplier has chosen his own limits. Takeo can threaten neither the distances nor the agreement into becoming something else.'),
 p('He leaves Pacific Relay with a smaller objective and an intact force assigned to it. It is a concession to circumstance. He does not intend to mistake it for surrender.')])
chapter(13,'The Human Siege Engine',ENTRY,[
 p('Meridian’s service entrance opens onto a three-sided crisis. Syndicate personnel contest the complex; Arakawa’s teams pursue its archive; Thirteen holds the route for his force. Takeo steps into the approach with his own Nanoengine and the strength left to him after the preceding engagements. The building is no longer the future research centre described in his opening report. It is a place through which people and records are trying to leave.'),
 b('takeo','One objective. Bring the command through.'),
 p('His escort falls back to its assigned work. He does not need an audience at his shoulder. The familiar certainty returns as he faces resistance close enough to touch: mass, angle, the position that will collapse if he breaks the right support. These are problems his body knows how to answer. Beyond them lies the less agreeable task of ensuring that the opening he creates serves the order he has finally made clear.'),
 p('The archive is deeper in the complex. He remembers the examination-room glass in Onami, Senda’s pen stopped over a forecast, the first Shinokami return with a new heading. He once intended all of that work to become an army capable of carrying power beyond his reach. Now he is going to destroy the contested record of it so neither the UN operation nor the Syndicate can possess it.'),
 b('takeo','Keep the withdrawal channel clear. Report when the command is through.'),
 p('He does not tell himself the archive is worthless. It would be easier if it were. Nor does he pretend that every trace of the programme will disappear with it. He is denying this unique body of work at this site, at a cost that cannot be repaired by opening a second cabinet. First he must break the resistance, secure the passage and reach it.'),
 p('The first defenders shift behind their cover. Takeo advances, already measuring the space they have left him.')],
 [p('The last confirmed movement reaches the retained bridgehead. Thirteen’s command has come through. Takeo stands beyond the broken archive housing while the building settles into the quieter noise of withdrawal. The contested programme record is destroyed by his own hand. The immediate replication project ends here, although scattered historical traces elsewhere remain.'),
 p('Arakawa withdraws alive with his people and a bounded account of what they observed. He has not secured the programme archive. The Syndicate’s local seizure has failed. None of those facts cancels the material cost of the route Takeo chose, or makes Meridian the independent centre he intended to build.'),
 p('He listens to the final report without interrupting it. For once, the voice on the other end can name both the success and the loss. Takeo acknowledges the surviving command and turns toward the exit.')])
chapter(14,'Empire of One',HQ,[
 p('Back at Kestrel, Takeo finds the command room prepared as though the map were about to justify itself. It does not. Pacific Relay survives under Thirteen, but the independent regional operation is smaller than the one he approved. The Meridian replication programme has no archive to reopen. The local takeover has been repelled; the UN deputy has withdrawn without the programme records. Keisuke has placed those results on separate pages. Takeo reads each before looking at the total. Outside, the same trolley stops at the door, and the same conversations become quiet.'),
 b('keisuke','The revised returns are countersigned. The shortfalls are attached, including the transport losses. I have not returned any of them for a more favourable estimate.', 'He has brought the originals as well. The narrowness of his new discretion has not made him harmless; it has made him careful about where his authority ends.'),
 b('takeo','Keep them that way. Your discretion ends where the adverse report begins. You will enforce the order after command has the facts, not decide which facts it deserves.', 'Keisuke accepts the limit without asking whether it is temporary. Takeo dismisses him with work still to do. There is no absolution in keeping a useful subordinate.'),
 p('A separate private exchange closes the failed supply arrangement. Sylvanis offers only limited, separately priced future business. Takeo accepts that no term gives him command over its supplier.'),
 b('thirteen','What does the next order require of me? I will not hold three positions again.', 'At Pacific Relay, before Takeo returns to Kestrel, Thirteen meets him beside the map of the surviving operation. The repaired chair is still there. Outside, the force they preserved is returning to work. He asks without lowering his eyes or offering a reassurance in place of a question.'),
 b('takeo','You command the surviving regional operation. Submit a plan it can carry. State the limits before you ask for the resources.', 'Thirteen considers the instruction, then nods once. Takeo has not called him a replacement for One. He has given the commander a task that requires judgement and left him at the post from which he will exercise it. The distinction is small enough for Takeo to accept and large enough for Thirteen to use.'),
 p('Later, with the command business finished, Takeo opens the high-level designation index. It contains no experimental record that could replace the archive he destroyed. One: escaped. Thirteen: active. He leaves both entries untouched. The first names a limit to his ownership; the second names a man whose usefulness now includes telling him when an order cannot be obeyed. Neither fact has made Takeo charitable. He still believes strength gives him the right to determine the shape of other lives. He has merely been forced to encounter lives, distances and decisions that do not become his because he believes it.'),
 b('takeo','Bring the current command map.', 'He closes the index. There is no private vow to change, no tenderness recovered from the ruins of the programme. He wants to see what remains available, what can be rebuilt and where power might next be extended. Kazama’s ambition had once given him a direction worth following. The next direction will have his own signature beneath it.')],
 [p('The clerk brings the map with the morning’s first adverse report clipped to its edge. Takeo reads the report before allowing the clerk to leave. The man waits through the silence and receives a question about capacity rather than a punishment for naming its limit.'),
 p('After the door closes, Takeo draws the surviving regional operation into a new outline. The bridgehead remains under Thirteen’s command. The replication archive does not remain at all. His pen stops at the edge of the territory he controls, then moves into the empty space beyond it.')])

# Both captaincy and dissolution belong to TK-02; later memories retain IDs.
MEMORY_AT={1:('TK-F01','TK-F02'),2:('TK-F03',),3:('TK-F04',),4:('TK-F05',),5:('TK-F06',),6:('TK-F07',),7:('TK-F08',)}

# Each recollection returns to the actual present problem in the same reader.
# These beats confer no historical knowledge on present-day listeners.
RETURNS={
 'TK-F01':[p('At Meridian, Takeo unfolds the copied demand again. The name of his old unit has survived its closed doors and sealed reports. He remembers Arakawa’s hand on the casualty sheet. It is the persistence of the gesture, rather than the accusation on the gate, that holds him for a moment.')],
 'TK-F02':[p('The service road returns to focus. Takeo has spent years beyond the authority that dissolved Directive 0, under Kazama’s banner and then his own. No revoked commission can explain away those choices. He folds the demand and puts it inside his jacket. The present obstruction is still in front of him.')],
 'TK-F03':[p('Back at Kestrel, Sylvanis’s contract is still on the table. Takeo has once offered allegiance freely, to a man whose strength and ambition he respected. He is purchasing supply now. The memory makes the difference sharper, and does nothing to remove the limits written beneath the price.')],
 'TK-F04':[p('The old observation glass gives way to Meridian’s projection. The promise has grown more confident while the proof remains narrower than the heading. Takeo strikes out the production claim. His own power has survived every organisation that housed the research; the unique archive has no such protection, and no complete backup.')],
 'TK-F05':[p('The yard at Meridian comes back into view. Drivers wait beside loads that cannot all be carried. The first Shinokami return had also begun with what remained available, not what he wished had survived. Takeo looks from the personnel list to the equipment schedule. He must choose which loss the next command will inherit.')],
 'TK-F06':[p('The present index lies beneath his hand. One: escaped. There is still no name or address for the life beyond that designation. He closes it and corrects the forecast. Whatever his son has become outside this room, the programme cannot list him among its available resources.')],
 'TK-F07':[p('At Pacific Relay, Thirteen stands across the table with the corrected withdrawal account. The child who waited for a use has become a commander asking for a feasible order. Takeo takes the truthful report. Its existence does not excuse the earlier lie, but it leaves him less room to pretend the order could have been obeyed.')],
 'TK-F08':[p('The first contract once seemed a bridge to independence. The present ledger shows how much command has been built on top of it. Takeo marks the services whose owners can stop them and sends for alternatives. He has evidence of dependence now. The next move belongs to people he does not control.')],
}

def copy_scene(key,field):return deepcopy((MEMORIES if key in MEMORIES else CHAPTERS)[key][field])

# Existing town-NPC identity, not a new duplicate major character.
for spec in CHAPTERS.values():
    for field in ('briefing','aftermath'):
        for beat in spec[field]:
            beat['speeches']=[['Keisuke Hachimura' if who=='keisuke' else who,text] for who,text in beat['speeches']]

# TK-14 starts with the surviving commander at his actual post. The remaining
# headquarters settlement is a separate saved in-person scene after Maps travel.
final=CHAPTERS['TK-14']['briefing']
commander=final[4:6]
headquarters=final[:3]
supply=[b('sylvanis','The old schedule is closed. You may buy a limited delivery at a new price. You may not buy my obedience.', 'In Kestrel’s operations office, Sylvanis glances over the settlement before setting it down. He has brought no expression of regret for the support he withdrew. The wreck of Takeo’s larger ambition interests him more than the arithmetic, but he is quite willing to be paid for whatever comes next.'),b('takeo','Separate deliveries. Separate payment. No standing claim over our command routes.', 'Takeo names each limit. Sylvanis agrees to the terms without becoming less amused. The failed arrangement is finished; limited future business remains possible. When the supplier leaves, Takeo lets him go. He has learned the cost of depending on this man, and has not discovered a way to make him belong to anyone else.')]
final[:]=commander+headquarters+supply+final[6:]
CHAPTERS['TK-14']['room']=RELAY
for index,beat in enumerate(final):beat['room']=RELAY if index<2 else 'site_01__operations_office' if index in (5,6) else HQ
for beat in CHAPTERS['TK-14']['aftermath']:beat['room']=HQ
