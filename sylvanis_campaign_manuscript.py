"""SY-F02 authored visual-novel manuscript. Fixed history, never generated at runtime.

Each non-empty line is one staged prose or dialogue beat. Core tags attach a
painting to its narrative moment instead of relying on a mutable line offset.
"""


def scene(text):
    beats = []
    core = None
    background = None
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('@CS-'):
            core = line[1:]
            continue
        if line.startswith('@background '):
            background = line.split(' ', 1)[1]
            continue
        speaker, words = line.split(': ', 1)
        beat = dict(player='', speeches=[] if speaker == 'n' else [[speaker, words]],
                    narration=words if speaker == 'n' else '')
        if core:
            beat['core_id'] = core
            core = None
        if background:
            beat['background'] = background
        beats.append(beat)
    if core:
        raise ValueError('A core shot must introduce an authored beat.')
    return beats


MEMORY_TEXT = {
'SY-M01': scene('''
n: The customs clerk had drawn a neat line through the name of his planet. Beside it she wrote the human designation, hesitated, and asked whether he wanted to register as displaced. Behind her, a departure board kept revising the progress of a war that had already swallowed his home. Humans had captured the Blisk planet. The war itself was not finished.
n: Sylvanis watched the ink spread through the old name. He had expected to feel something more entertaining than impatience. All those towers, all those solemn little hierarchies; conquered at last, and still requiring paperwork.
sylvanis: Do I look misplaced?
n: The clerk pushed the form back without answering. He had been watching her hand rather than her face. It stopped shaking only when he looked away.
n: Among the Blisk, dark magic had been part of the foundations of civilisation: a means of building, coercing and deciding who could keep what they possessed. Violence supported rank. Selfishness wore the dignity of principle. The strong called their advantages proof that they deserved them, then built institutions to keep anyone from testing the claim.
n: He remembered arguments about which bloodline, which conqueror, which perfected technique should stand above another. Everyone wanted the highest seat. Having obtained it, everyone wanted the room to remain exactly as it was. He had understood their ambitions almost before they finished explaining them. That was the trouble.
sylvanis: Boring people. Such magnificent confidence in being boring.
n: A traveller beside him mistook the remark for homesickness and began to offer sympathy. Sylvanis smiled until the man reconsidered. He had not rejected Blisk cruelty. He liked cruelty. He despised the repetition, the tedious self-congratulation of people who called a familiar appetite destiny. Nothing about their civilisation required him to become what he was; he had made his own enthusiastic choices.
n: Across the hall, a collector took a traveller's purse while a second man blocked the side exit. Protection money, paid twice: once for arriving, once for leaving. Sylvanis abandoned the queue. The collector mistook his interest for negotiation.
sylvanis: You have made that look very easy.
@CS-SY01
n: The collector reached for a weapon. Sylvanis broke the movement before it finished and took the purse for himself. The traveller held out an empty hand. Sylvanis stepped around it, already interested in the second man's decision to draw. The customs bell rang behind him; he did not turn back.
n: By evening he had found people who paid for violence. They gave him a name and a warehouse and asked him to frighten the owner. He killed the owner's armed retainers, killed the owner, and broke the loading supports because someone had assured him that the building was secure. By dawn, the quay was blocked with its fallen frontage. The men who had hired him could no longer reach the cargo they had meant to acquire.
n: He listened to their outrage with growing pleasure. They offered more money, then threats, then an explanation of whose protection the warehouse had enjoyed. At the first useful name, his attention sharpened. He left them their money and went to find its owner.
sylvanis: A whole new world. Let us see what it does.
n: Ships waited offshore while rival crews argued over the damaged route. A broker disappeared. Two agreements collapsed because neither side could promise protection any longer. He had been on Earth only a short time, and people were already rearranging their lives around the possibility that he might come through the door.
'''),
'SY-M02': scene('''
n: The first instructor took his coat off carefully. He wanted the spectators to notice the insignia on his sleeve before he laid it down. Sylvanis watched his feet. The opening movement disclosed the structure of the school; the next disclosed the habit its founder had never corrected.
sylvanis: Again. Something you actually meant to hide.
n: He reproduced the technique, corrected it and passed through the instructor's guard. Other schools offered other answers. Polymath gave him their grammar as soon as he observed it, and his body made use of what he understood. There was no long apprenticeship, no patient climb towards mastery. Human martial arts became his almost as quickly as people could show them.
n: For a moment, he enjoyed the instructor's expression. Then even that became familiar. He could predict the appeal to rules, the accusation of trickery, the promise of a more formidable master elsewhere. He let the man finish because a new address sometimes emerged from wounded pride.
n: It was not only fighters who learned his name. He killed men sent to collect debts, demolished the rooms from which their employers issued orders, and then struck the employers who believed they had bought his help. An extortion ring lost its leadership in a night. Its rivals moved in, congratulated themselves, and discovered that he had no intention of letting them settle comfortably into the vacancy.
n: Some paid him to leave. He left when he wanted. Some offered surrender. He sometimes accepted, and sometimes asked why they had stopped just as he was enjoying himself. The uncertainty travelled farther than any single account of strength. There was no safe price, no reliable insult to avoid, no promise that survived his changing interest.
n: In a port alley, several factions finally sent their best remaining men together. Sylvanis was delighted by the cooperation. They had crossfire, overlapping fields of attack and enough bodies to block both exits. He understood the arrangement before the first signal. He let them give it anyway.
n: The fighting tore shutters from their hinges. A man went through a doorway that had been barred from within. Lamps broke; the sound of masonry followed the last volley. Sylvanis killed the attackers as they came, crossed the alley faster than their formation could turn, and ended the men who tried to regroup behind him. Their numbers gave the encounter length. They did not give it uncertainty.
@CS-SY08
n: Afterwards he stood in the ravaged night-alleyway among more bodies than the surviving lookout could count. Water carried splinters down the cobbles. The lookout's weapon slipped from his hands. Sylvanis rested his palm against the cracked wall and waited for the familiar surge of pleasure to become something that would last.
sylvanis: Is that everyone?
n: The lookout tried to answer. What emerged was a breath with no words in it. A shutter opened above them, then closed so softly that its owner must have caught it before it touched the frame. Sylvanis could hear someone holding back a sob.
n: Crazed Demon. Demon King. The names came from people who had run out of ordinary language for him. They spread through ports and security offices, through fighters who declined commissions and employers who removed addresses from their correspondence. Before the Organisation found him, he was already the most feared man on the planet.
n: He was also the strongest being on it. He could grasp a problem before others finished stating it and end a fight before they recognised the opening. Nothing in that supremacy supplied a reason to get out of bed. Tonight's victory had become a solved problem while the last man was still falling.
sylvanis: Do tell the next lot to be better. I am beginning to take this personally.
n: He walked past the lookout. Leaving a witness was a whim, not mercy. Behind him, the man stayed pressed against the wall long after the footsteps had gone.
'''),
'SY-M03': scene('''
n: Kaden Mourne was carrying an injured stranger when Sylvanis first saw him at the compound. The older man's mercenary coat hung from one shoulder; he had wrapped the other half around the man in his arms. Someone brought a tally of the rescued civilians. Kaden asked who was missing before he asked what the job would pay.
kaden: The wounded first. Nobody discusses payment while someone is still outside.
n: A younger mercenary began to explain that the contract covered a smaller number. Kaden sent him for more blankets. He did it without a speech, as though the answer ought to have been obvious. Sylvanis found that more interesting than the armed men watching him from the gate.
sylvanis: You have a remarkably expensive way of choosing enemies.
kaden: They cannot afford protection. We can afford to give it.
n: Kaden knew the name before the introduction. So did the medic, who stopped winding a bandage when Sylvanis stepped into the light. One of the guards shifted to cover the infirmary door. Kaden kept his hands where the guard could see them and asked Sylvanis to walk with him beyond the waiting wounded.
kaden: I know what you have done. Working here would not erase it.
sylvanis: How disappointing. I was hoping for a certificate.
kaden: You would have work. The people under our protection would have peace from you. If that condition bores you, leave now.
n: There was no performance of fearlessness in him. He judged the distance to the door, noticed who stood behind him and spoke anyway. Sylvanis recognised the effort. It was possible to understand another man's courage without valuing what he used it for.
n: Kaden described the next operation: armed men holding a road, families unable to cross it, a demand for payment that rose whenever anyone paid. Sylvanis asked about the defenders' weapons. Kaden answered precisely. Neither pretended they wanted the same thing from the encounter.
sylvanis: If you keep finding people who want to fight, I will keep coming.
n: He chose the work because it supplied opponents and a convenient explanation for killing them. The Organisation could call an operation a rescue. He could call it an evening well spent. Kaden's genuine purpose survived that difference for a while, though the cost of employing him was already visible in the way the guards watched his hands.
@CS-SY02
n: At supper Kaden set a bowl beside the bespectacled man without asking what he ate. The man's face remained blank and featureless in the recollection; the glasses were the only visible cue. Kaden moved a stack of reports to make room for him at his own table.
kaden: You used to wait up after every deployment. Eat before it goes cold this time.
conspirator: I learned that waiting did not make you return sooner.
n: Kaden's hand rested briefly on the back of his chair. The bespectacled man lowered his spoon but did not move away. Sylvanis watched the familiar gesture, then watched the command staff bring their questions to the same table. Affection and authority occupied a very small space here.
n: Outside, the rescued families began settling for the night. Sylvanis could hear a child laughing at something in the yard. He asked when they were leaving for the road.
'''),
'SY-M04': scene('''
n: The briefing ended with a shortage of transport and Kaden promising to go himself. The bespectacled man had supplied three alternatives. Each saved more equipment and left more people exposed. Kaden listened to all three, rejected them, and stayed to explain why after the officers filed out.
kaden: Stay a moment. You do not have to earn your place beside me.
n: Sylvanis heard that much from the corridor. Later, the same man found him alone and placed a sheet on the table. Its columns extended across borders that their current contracts barely touched. The face above it remained blank, glasses catching a colourless line of lamplight.
conspirator: We kill Kaden. We take the Organisation beyond mercenary contracts. A multinational syndicate. Cards and suits to organise its people.
sylvanis: Yes.
conspirator: You understand what I am proposing.
sylvanis: Perfectly. It sounds fun.
n: The answer came before the practical details. There was no loyalty to pry loose, no reluctant recruit to convince. Sylvanis had enjoyed Kaden's work while it offered violence. He liked the prospect of tearing apart the institution that supplied it. Both pleasures were his own.
n: The conspirator turned the paper so that Sylvanis could read the appointments. He had reserved a place for a force that could cross the proposed suits without belonging to one of them. Below it were lists of men who would resist the change. Several had known Kaden for years.
conspirator: They will fight for him. Others will submit when they learn that you have chosen us.
sylvanis: Us. You have fitted me into a rather useful little word.
@CS-SY03
n: Sylvanis put a finger across the proposed card structure. The conspirator left the paper beneath it. For the first time in their exchange, neither spoke. Each had found the part of the other he intended to use.
sylvanis: You want my reputation to walk into rooms before your orders arrive. I want you to keep opening rooms worth entering.
conspirator: I intend to own more than rooms.
sylvanis: There you are. Much better.
n: The ambition pleased him because it promised scale. Routes, governments, armies, rival criminals: a growing structure would keep discovering resistance. The conspirator was arranging opportunities calculated to hold his attention. Sylvanis understood the manipulation and offered his own, suggesting which stubborn commanders might need personal persuasion and watching the man's hand return to the list.
n: Neither believed the bargain made the other safe. The conspirator wanted the world's most frightening man associated with his coming order. Sylvanis wanted an ambitious man to keep supplying reasons that could be attached to whatever he chose to destroy. They could each see the danger in the arrangement. They went on drawing it.
conspirator: Kaden will come to the command room himself.
n: That confidence came from a trust Sylvanis had watched at supper. The door would open for this man. The paper did not explain why, and the recollection supplied no name or family title to settle it.
sylvanis: Then do make sure I am there when he does.
'''),
'SY-M05': scene('''
n: Kaden recognised the changed guard positions before anyone spoke. The infirmary had not finished evacuating. He stopped in the command-room doorway, saw who was holding the ledger he normally left within reach, and sent the attendant behind him back the way she had come.
kaden: After all those nights waiting for me, this is what you chose?
conspirator: The Organisation ends here.
sylvanis: I wanted to see this part myself.
n: Kaden looked at Sylvanis only long enough to judge the immediate danger, then returned his attention to the man with the glasses. There was a private hurt in the pause; it did not supply a family name. When the conspirator reached for the signal bell, Kaden moved to stop him.
n: He fought hard enough to break the first guard's advance and keep the passage open. Sylvanis intercepted him. Kaden changed his grip, gave ground, tried to turn the encounter towards the doorway. Sylvanis understood the aim and spoiled it with effortless precision. The wounded gained a few more seconds because Kaden spent his strength buying them.
n: He could have made the fight shorter. He did not mistake that choice for generosity. Kaden was a capable man, and the particular way he kept trying to reach the passage interested Sylvanis more than a quick death would have. When the opportunity stopped being new, Sylvanis struck him down.
n: The command ledger fell open on the floor. Kaden tried to draw breath around the injury. His attention shifted from the bespectacled man to Sylvanis, and for a moment the question in his face was clearer than the pain.
@CS-SY04
kaden: Sylvanis... will you ever truly find the thrill you are looking for?
n: It was not a plea for his life. That made it briefly difficult to dismiss as ordinary bargaining. Sylvanis looked down at him. He had been offered a useful cause, a place at a table, another man's trust in the possibility of restraint. None of it had made him want to be better. Now the dying man was asking whether anything he did want would ever be enough.
sylvanis: I intend to keep looking.
n: Kaden died after the question. Sylvanis waited for a second feeling and found only the familiar impatience to see what happened next. He had killed a good man knowingly. There was no hidden regret to discover beneath the pleasure.
n: The conspirator picked up the ledger. For a moment his thumb remained against a worn place on its cover. Then he called in the guards who had accepted his terms. His face stayed blank behind the glasses. Whatever Kaden had meant to him, he gave no explanation of it.
conspirator: Secure the accounts. The remaining commanders will answer to us.
n: Contracts that had protected people unable to pay became demands for payment. Some mercenaries left. Others discovered that refusing the new organisation meant confronting the man still standing beside Kaden's body. Sylvanis watched several of them make that calculation without a word.
n: The man with the glasses would eventually take the name Crow. The card structure became a means of distributing power, and Sylvanis's participation became an unspoken threat behind it. Nothing in the new insignia made the murdered man's work fraudulent. The Organisation had stood for something. That was part of what they had destroyed.
'''),
'SY-M06': scene('''
n: The Crow had secured the border route through weeks of negotiation. Sylvanis spoiled it in an afternoon. An escort challenged his right to enter a warehouse; he killed the escort, broke the gate and pursued the reinforcements into a loading bay that both sides had agreed to leave untouched. The shipment survived only because someone had the sense to move it before asking permission.
n: In the early Syndicate office, the Crow placed the repair account beside an unsigned offer from a rival. His beaked mask and dark lenses withheld everything that a face might have betrayed. He had already arranged a replacement route. The paperwork was evidence of work done, not a request for Sylvanis to help him think.
crow: You understood the agreement.
sylvanis: That was the boring part, Mr. Crow.
crow: I will take their next three contracts. You have made their guarantee worthless; I intend to make mine indispensable.
n: Sylvanis laughed. There was the quality that kept this association alive: the Crow could look at a ruined passage and see the beginning of a monopoly. The destruction was expensive, but he would attempt to own what grew around it. A lesser employer would still have been complaining about the gate.
sylvanis: You should put that in the thank-you letter.
crow: Your access to this consignment ends. I will not pay twice for your curiosity.
n: A messenger brought in a refusal from another district. The Crow read it, set it aside and asked Sylvanis whether the defending commander still claimed never to have lost. It was a calculated turn of the conversation. Both men knew it.
sylvanis: Oh, beautifully done. Show me a new toy while you take the old one away.
crow: You may decline. The commander will still have to choose between my terms and your attention.
sylvanis: And I get to call it your business. Such a respectable explanation for breaking him.
n: The Crow wanted his reputation as well as his hands: the closed shutters before a visit, the negotiations shortened by a name, the rivals too frightened to test whether a threat was real. He knew he was employing a wild-card. He tried to direct the cost towards people whose loss would enlarge the Syndicate.
n: Sylvanis used the ambition in return. He could invoke an expansion, an enforcement action, a failed agreement; each supplied an excuse without supplying the true motive. He did not need the Crow to absolve him. He enjoyed making the organisation accommodate what he wanted, then watching its master insist that he remained in control.
crow: I can use what you do. Do not confuse that with my approval of everything you may decide to do next.
sylvanis: Then keep deciding where you want the world to bend. I will see whether it makes an interesting noise.
n: They continued together. There was no friendship developing beneath the quarrels. Each was too useful to discard, too dangerous to trust, and entirely aware that the other was keeping a separate account.
'''),
'SY-M07': scene('''
n: The first trial began as a whim and survived because the failure irritated him. A man whose strength had doubled still fell exactly as Sylvanis expected. Another learned the pattern of an attack and could not move quickly enough to escape it. He turned the observations over, looking for the small distance between recognising an answer and being able to use it.
n: Red Magic and Blue Magic took shape around that distance. Blue could briefly awaken superhuman abilities in a subject before the effect faded. Red drove the temporary enhancement harder, with more harmful strain, disorientation and crashes. Neither bottle conferred a permanent Awakening or guaranteed a particular ability. He kept coming back because the right alteration might someday produce an opponent who could surprise him.
sylvanis: Stronger is easy to measure. I want to know when it becomes interesting.
n: He used living humans. Some accepted a risk they did not understand; others had never agreed to enter the room. A technician called the restraints precautions. Sylvanis did not bother with the euphemism. He watched a subject strain against the straps and asked for the earlier readings.
n: The work moved between the historical Glasshouse and his private underground arena. Fighters, paid observers and captive subjects entered through different doors. He owned the operation. It was neither the public lounge nor the Iron Circle, and no cheering crowd made the people inside its tests less real.
@background locations/campaign/sylvanis/arena
n: On one trial night he invited Martos Cabrera to the ring. Martos was already in the Crow's service. He came in his early-service field clothes, inspected the barred exits and waited by the inner gate. Sylvanis had requested his participation; the Ace had not become his subordinate.
sylvanis: Fight this one for me, Martos. Red Magic. I would like a result that survives contact with somebody substantial.
martos: What stops the test?
sylvanis: You do. Show me what he can actually make you do.
n: Martos looked from the observer's glass to the man in the ring. The subject's breathing had become rough and fast. His hands shook between bursts of unnatural stillness. When the gate closed, he attacked the nearest person standing between him and an exit.
n: The first impact sounded promising. Martos caught the next rush, planted his feet and answered with a force the subject could not absorb. Sylvanis leaned forward. The enhanced man managed one short strike through the closing distance before Martos broke his remaining advance. The exchange ended against the barrier. Martos destroyed the subject's resistance and killed him; there was no recovery hidden in the silence that followed.
martos: Finished.
n: Martos checked that the man was dead, then rubbed at an irritation beneath his nose. He looked at his knuckle. A thin red smear marked it. He pressed two fingers under one nostril, waited, and found a second small trace of blood. The mild nosebleed stopped almost at once. Otherwise he remained standing and in control.
martos: He caught me there.
n: Sylvanis had already left the viewing chair. He came to the glass with the sudden, complete attention that usually preceded violence. The body against the barrier interested him less than those few drops. The subject had been hopelessly outmatched and still produced a measurable effect on Martos.
sylvanis: There you are.
martos: He is dead.
sylvanis: Yes. And you are bleeding. Only a little. That is the part I had not already watched happen a hundred times.
n: He did not declare the subject Martos's equal, still less his own. The Ace had killed him decisively. The narrow result was more useful than a grand claim: something that would otherwise have been dismissed had crossed a small part of the distance. It suggested a question worth pursuing.
martos: Do not write that he nearly won.
sylvanis: Bro, if he had nearly won, I would be down there asking for my turn.
n: Martos left him with the dead subject and the readings. Sylvanis marked the instant of contact, then went back to the Blue trials. Power that arrived too slowly, perception that failed under pressure, a body unable to tolerate its own brief advantage: he wanted to see which limit would move next. He might never make the opponent he imagined. For once, that uncertainty held his attention longer than the fight.
'''),
'SY-M08': scene('''
n: The eastern training hall smelled of scrubbed wood and a meal left waiting somewhere beyond the passage. Sylvanis had followed accounts of two formidable fighters. By the time he found them, he had heard enough praise to become impatient with introductions.
n: They were Garrett and Charles's parents. Neither son was in the room. Their lives were larger than the encounter Sylvanis had come to demand: the repaired floorboards, an ordinary coat hung near the door, a cup that someone had put down expecting to return to it. He noticed these things as obstacles and positions before he considered the people attached to them.
parent-one: There are people behind us. Keep the doorway.
parent-two: I have it.
n: They moved together without needing a second instruction. One offered an opening the other could punish. Sylvanis took the opening, saw the answer and changed his line before it arrived. For a few exchanges their cooperation held his interest. They had learned each other's habits closely enough to make two bodies act with an uncommon fluency.
sylvanis: Again. Both of you this time. I came a very long way for the recommendation.
n: They had already given him both. He could see it in the adjustment of their feet, the effort to keep the passage covered while recovering from a blow that should not have landed. Knowing that did not lessen his appetite to force another answer from them.
@CS-SY05
n: He broke their coordination and killed them. They fought to protect the people beyond the doorway, and he used that commitment to choose where they would stand. No order required it. No danger made it necessary. He had come to find a fight and decided that their lives were available to complete it.
n: Afterwards the room kept the small sounds it had made before: a loose fitting ticking against the frame, something boiling beyond the passage. The surviving people did not immediately come out. Sylvanis waited as though the silence might conceal another opponent.
sylvanis: Was that all?
n: It was the wrong question for the room, but the only one he cared to ask. He was disappointed by the distance between their reputation and his own strength. Their courage had been real. So had their skill. Neither had obliged the world to contain somebody who could satisfy him.
n: He stepped over the broken edge of a floorboard and left. Somewhere beyond the hall were people whose next conversation would begin with news they would never stop carrying. The dead would have names and obligations and children who grew around the absence. Sylvanis took away another failed recommendation.
n: Later, he would remember the pair well enough to recognise a detail in an archive query. He would not return to the hall out of remorse. The harm did not become smaller because the man who caused it soon wanted something else.
'''),
'SY-M09': scene('''
@CS-SY06
n: Charles put his application on the desk with the edges already aligned. Sylvanis noticed that before he noticed the qualifications. The young man's explanation of his laboratory experience was concise, well prepared and almost entirely directed towards things he could prove.
charles: I can reconcile the trial records and maintain the archive. If something cannot be supported, I will mark it as such.
sylvanis: A man who enjoys finding mistakes. We may get along.
n: He assigned Charles an ordinary archive task. Later came a question about an eastern encounter entry: why it was incomplete, where the earlier version had gone, whether the omitted details had been moved to another register. The precision exceeded the needs of the assignment. The application had mentioned no corresponding personal interest.
n: Sylvanis remembered the hall and the pair who had kept trying to cover its doorway. He watched Charles stop just before the part of the record that would have made the inquiry unmistakable. A careful stop was still something to observe.
charles: I wanted to establish why that entry was incomplete.
sylvanis: Very thorough. You should stay.
n: Charles waited, as if the next sentence might change the offer. Sylvanis let him wait. Fear was easier to recognise here because it had work laid carefully over it: a controlled voice, a question narrowed until it seemed harmless, hands kept occupied with a document. The man had come despite that fear. That made him more interesting than another applicant who knew only when to agree.
n: Sylvanis recognised the infiltration from the discrepancy and the questions. True Sight had not opened a mind. He did not know every intention or every future move. He knew enough to let a dangerous possibility into the laboratory and leave it alive there.
sylvanis: You have something else to ask.
charles: When would you want me to begin?
n: A good answer. Sylvanis smiled and gave him a start time. The application went into the accepted tray. He left its omissions unmentioned. Charles took the practical offer as evidence that his cover had held, and nothing Sylvanis said corrected that belief.
n: Letting him in offered a pleasure different from breaking a fighter's guard. A clever man could prepare something unexpected if given time and imperfect information. Sylvanis could provide both. The possibility did not guarantee Charles success, and noticing the attempt did not make Sylvanis immune to it.
n: When Charles left, Sylvanis reopened the incomplete eastern entry. He read it once, then closed it without supplying the missing names. The blank space had become useful.
'''),
'SY-M10': scene('''
n: Takeo Mishima received him at headquarters. The meeting room had been cleared before he arrived, but two guards still checked the passage while an attendant set down the cups. The attendant put Sylvanis's cup within reach and withdrew the tray too quickly. Porcelain clicked against porcelain.
n: Takeo let the sound pass. He had invited a dangerous counterpart into a controlled room and intended to obtain something from the meeting. Fear could exist without becoming submission. Sylvanis liked watching where the distinction held.
takeo: Tell me what the supply does. Then tell me when it fails.
n: Sylvanis described Red Magic and Blue Magic as temporary advantages with temporary limits. He knew the tolerances, the inconsistency between subjects, the difference between a promising result and one that could be repeated. For several minutes he was exact enough to make the business possible. He enjoyed the moment Takeo realised that the reputation for madness had not been a warning of stupidity.
sylvanis: You expected a performance. I can do the arithmetic as well.
takeo: I expected a supplier to know his product.
n: Takeo asked who answered for failed deliveries, what observers could inspect and how an unstable result would be contained. Sylvanis answered the useful questions and tested the others with an extravagant promise. Takeo crossed that promise out before the paper moved back across the table.
takeo: I am buying a dependable supply. I am not buying your amusement.
sylvanis: You should. It is considerably less dependable.
takeo: Then keep it outside the agreement.
n: Their arrangement linked Syndicate supply to Shinokami demand within stated limits. The Crow's internal terms reached Takeo through Sylvanis. No meeting between Takeo and the Crow took place. No territorial betrayal was disclosed or decided in the room.
n: Sylvanis watched Takeo sign only the version he had corrected. Here was another institution sure it could put enough words around him to obtain the useful part and exclude the rest. Sometimes it could. The resulting friction was one reason he kept returning to people with plans.
sylvanis: And if I discover something worth a larger audience?
takeo: Bring me a new proposal. This one is finished.
n: Outside the room, the attendant stood well clear of the route to the exit. Sylvanis paused just long enough to make the man stop breathing, then walked on. Behind him, Takeo remained at headquarters with his own copy of the agreement. The boundaries had been understood. What Sylvanis chose to do with them would be another matter.
'''),
}

CHAPTER_TEXT = {
'SY01': scene('''
charles: The demonstration schedule is ready. One contracted lot, no substitutions, authorised observers only.
n: Charles laid the folder on the private review-room desk and kept his hand on it until Sylvanis looked up. Beyond the glass, the laboratory carried on in small, careful movements. A technician approaching with another question saw who was seated inside and decided that the question could wait.
sylvanis: How clean. Did anyone enjoy writing it?
charles: They were trying to make the result reproducible.
n: Sylvanis opened the folder. He understood the schedule at a glance: the pairings, the permitted doses, the time reserved for the delegation's questions. Every uncertainty that might have made the evening interesting had been identified and removed. The Crow had signed the final page.
n: Being brilliant made the task brief. Being stronger than anyone they might put in the ring made it faintly insulting. He had spent years finding that the thing other people anticipated for weeks could be exhausted in a moment of attention. Then the rest of the afternoon remained.
sylvanis: Bird-man wants an obedient miracle. Something frightening enough to sell and polite enough to finish on time.
charles: He wants the agreed demonstration.
n: Charles said it without smiling. Sylvanis tapped the blank audience column. He could hear a trolley stop outside the door, then move on. Even here, people made little choices about how close to come. The Crazed Demon did not need to shout to change the working day.
n: The Crow knew that. His signature bought the laboratory a measure of order while retaining the threat that made clients listen. Sylvanis could recognise the attempt to manage him and still enjoy deciding how much of it to tolerate.
sylvanis: Leave it with me, Charles. I should hate to disappoint him without first understanding the effort he has made.
n: The folder smelled of warm paper and disinfectant. For a moment the bright review room gave way to an arrival hall, another form, another person trying to fit him inside a useful description.
'''),
'SY02': scene('''
n: The roster included a recording of the proposed bout. Sylvanis watched it once without touching the controls. Before the second fighter committed his weight, he knew where the exchange would end. The replay confirmed the answer and offered nothing else.
sylvanis: They have even scheduled the applause.
charles: They were asked for a controlled comparison.
sylvanis: Yes. I can read.
n: The abruptness stopped Charles halfway through turning a page. Sylvanis smiled again, too late to make the interruption harmless. He named the flaw in the fighter's recovery, the reason the opponent had been chosen and the point at which an honest contest would have broken the script. Charles checked each observation against the supporting notes.
n: It was effortless. That was the part no one who wanted his abilities seemed to consider. An answer obtained without resistance left very little behind it. He wanted the instant when an opponent forced him to revise what he believed possible. Most people could not even make him revise his first impression.
charles: They are still taking a risk. Knowing the likely result does not remove it for them.
sylvanis: No. It removes it for me. You see the difficulty.
n: Charles closed the recording rather than argue about which difficulty mattered. Sylvanis found the small refusal amusing. He returned to the roster, studying the names for a trace of anything that might exceed the descriptions.
n: Outside, one of the proposed attendants asked to be moved to a different shift. The request did not mention Sylvanis. It did not need to. He had once enjoyed hearing how far his name had travelled. Now the reputation arrived before him and persuaded interesting people to stay away.
sylvanis: Find me the original footage as well. Before somebody made it reassuring.
n: Charles went to fetch it. The dark screen briefly reflected Sylvanis's face, almost as composed as a man who had found what he wanted.
'''),
'SY03': scene('''
charles: The staff want to know whether the cancelled shift will be restored. Some of them have already turned down other work.
n: The question had a particular weight because Charles brought it himself. A supervisor had written the message, revised it and left the request unsigned. Sylvanis read the revisions in the pressure marks beneath the final line. Even a complaint about lost pay became a small exercise in survival when it had to reach him.
sylvanis: A cause and a payroll. They do travel together.
charles: The lost pay is not theoretical.
n: Sylvanis looked up. Charles held his attention for a second, then set down the figures. They were modest beside the operation's cost, large enough to matter to the people losing them. He understood both scales without acquiring any obligation to care.
n: The Crow preferred dependencies he could maintain: wages, supplies, a place in the hierarchy. Sylvanis enjoyed discovering what happened when one was removed. He asked which supervisor had promised the shift before receiving approval. Charles gave him the name and repeated the amount owed, refusing to let the person disappear into the question of procedure.
sylvanis: You are very determined to keep this ordinary.
charles: Someone has to answer them.
n: Once, Kaden had answered people before anyone checked whether they could pay. Sylvanis remembered how that had puzzled the men who worked for him, as though kindness were a costly flaw in an otherwise competent operation. He had understood it well enough. Understanding a motive had never compelled him to share it.
n: He set the staff request beside the roster. The two documents offered different ways of changing the room: one through disappointment, one through fear. He was interested in the people who had to keep working between them.
sylvanis: Tell me exactly what they were promised. Start with the part the supervisor would prefer me to overlook.
'''),
'SY04': scene('''
n: Three versions of the evening lay before him. Takeo's delegation expected a useful commercial test. The supervisors expected to keep their people alive by following the approved programme. The Crow expected a dangerous asset to remain useful for the duration of an agreement.
n: Sylvanis could satisfy all three without effort. That was an available choice, and he disliked it. He turned the pages slowly, considering which expectation would make the most satisfying sound when it broke.
sylvanis: He knows what I am. That is what makes the little rules so affectionate.
n: No one was present to mistake the remark for warmth. The Crow's affection was for power. Sylvanis supplied an extraordinary quantity of it, badly behaved and impossible to make dependable. In return the Crow supplied scale: money, equipment, enemies who would otherwise never have been invited into the same problem.
n: Sylvanis wanted more than a rehearsal with frightened men. He wanted the careful buyer to lose the shelter of commercial language, or the supervisors to abandon their composed instructions, or the Crow to decide that the affair required his own presence. A response large enough to make the day change shape.
n: He knew that wanting it did not guarantee he would enjoy the result. The knowledge had never been an effective restraint. He had destroyed whole arrangements to discover that their collapse was as predictable as their construction. He still liked the moment before they fell.
sylvanis: Let us give somebody an evening they cannot prepare for.
n: His finger paused above the three names. The next choice would decide whose composure he went after first. It would not decide whether another person had made him do it.
'''),
'SY05': scene('''
crow: The agreement has not changed because you have become bored.
n: The executive meeting-room door shut behind the last aide. The man had taken care not to pass between them. Sylvanis remained standing beside the table in his sealed Coloured Joker mask and dark ceremonial coat. Across from him, the Crow's beaked mask turned towards the folder.
sylvanis: You used to bring more ambitious proposals, Bird-man.
crow: I am building something that survives its next amusement. You remain useful to that work.
n: It was an insult shaped like a fact. Sylvanis appreciated the precision. The Crow had never mistaken him for a loyal soldier; he preferred to behave as if knowing the danger made it manageable. Sometimes it did. Enough of the world had submitted to the Syndicate to give that belief evidence.
sylvanis: Useful. Is that what you tell them when they ask why you keep me?
crow: They ask less often after they have seen what refuses my terms.
n: There it was, openly. His name shortened negotiations. His presence changed the courage available to a room. The Crow could use a reputation earned before the first card existed and make the resulting concessions look like proof of his own inevitable command.
sylvanis: And when I do something inconvenient, you call it my initiative. When it works, the Syndicate has expanded. A lovely arrangement.
crow: You invoke my business whenever you want an audience and resources. Neither of us is being charitable.
n: Sylvanis leaned over the table. No face showed through either mask. He remembered another table, a sheet ruled into columns, a man with glasses proposing that they kill someone who trusted him. The terms had become more elaborate since then. The appetite behind them remained recognisable.
crow: Keep the demonstration within its agreement. There will be other opponents.
sylvanis: You always know when to mention those.
n: The Crow did. Sylvanis knew he did. The exchange continued because understanding the other's manipulation was part of the pleasure and part of the price.
'''),
'SY06': scene('''
n: The Crow did not repeat the history between them. He laid out the limits of the coming demonstration and let the silence around each one remain. One contracted lot. No additional subjects. No unscheduled exhibition. The ordinary commercial work could proceed; the private indulgence could not borrow its authorisation.
sylvanis: I understand every word.
crow: Then there will be no misunderstanding to settle afterwards.
n: An aide appeared at the door with the revised account. He addressed the Crow, kept the folder close to his chest and stopped when Sylvanis turned his masked head. The Crow instructed him to leave it on the table. He obeyed with the relief of a man given a task small enough to finish.
n: Sylvanis watched him go. There were people who could face armed rivals and still find it difficult to share a room with the Crazed Demon. A rival wanted something. Sylvanis might decide that the negotiation itself was less interesting than the consequences of destroying it.
sylvanis: You have them very well trained.
crow: I give them something to accomplish. You give them something to survive.
sylvanis: And you put the two together whenever it suits you.
n: The Crow neither denied it nor offered reassurance. He wanted the Syndicate's enemies to fear the force under his roof while its members believed his structures could keep that force pointed elsewhere. Sylvanis had no intention of helping him make the second promise absolute.
crow: I tolerate the uncertainty because the gain has justified it. That is an assessment I continue to make.
n: A direct threat would have been easier to enjoy. This was a boundary backed by logistics, people and the withdrawal of cooperation. Sylvanis could be stronger than everyone in the building and still have no interest in doing their work himself. The Crow knew where that difference mattered.
sylvanis: Then let us both keep assessing. It would be dreadful to become comfortable.
'''),
'SY07': scene('''
n: The workroom lights reflected in a red vial and a blue one standing beneath the inspection lamp. Sylvanis turned the blue vial until its label faced away. A clean colour, a familiar container, a result that depended on the human being made to receive it. The bottles always looked more manageable than what happened afterwards.
n: The current manifest held a single demonstration consignment and the original trial ledger. He had already spent too much of the day imagining an evening whose result he knew. The memory of Martos touching his nose returned with irritating clarity: surprise compressed into a small stain on a knuckle.
sylvanis: You would laugh, Bird-man. All that equipment, and the interesting result fit on one finger.
n: He said it to the empty space above the desk. Charles was occupied elsewhere in the workroom; the private recollection would not be spoken into the lab. Sylvanis opened the arena booking and considered the separate operating account. Eighty units were available to this undertaking. Reserving the venue would consume twenty.
n: A modest cost for access to the ring, its service passages and its equipment. The arena was his own underground operation. Neither the public lounge nor the Iron Circle belonged to this test. He selected the private site and began writing an exhibition programme under his own name.
sylvanis: Stronger. Faster. Clever enough to make the strength arrive in the right place. Somewhere in all those failures there ought to be a less disappointing question.
n: He knew that suffering was not evidence of progress. He had seen enough of it to tell the difference. He continued to cause it anyway, pursuing the possibility that a temporary alteration might bring one person far enough towards him to make a fight feel unfinished in advance.
n: The booking waited for his final confirmation while he looked at the ledger. For a moment he remembered the historical ring, the dead subject, and the much smaller mark that had held his attention.
'''),
'SY08': scene('''
charles: Some old records omit the names of the people affected.
n: He spoke while closing a register, as though the observation belonged to the routine reconciliation. Sylvanis noticed which page Charles had left beneath his thumb. It was not enough to tell him everything the man intended. It was enough to make him listen.
sylvanis: An omission can make a story terribly convenient.
charles: It can also make it wrong.
n: Charles's voice remained level. The laboratory gave him small tasks to perform while he waited for the response: square the register, cap the pen, move a loose sheet away from the edge. Sylvanis watched the practised steadiness. He had seen armed men with less control over their hands.
n: The absent names belonged to lives whose importance had never depended on their ability to hurt him. Sylvanis understood that proposition. He simply did not use it when deciding whether to kill. Their resistance had become an episode in his search; the episode had become an incomplete file; now the file was making someone choose his words with exceptional care.
sylvanis: Do you want the missing space filled, Charles, or do you want to know who left it?
charles: I want a record I can rely on.
n: Sylvanis let the answer stand. He did not confess to the eastern murders, and Charles did not learn that his purpose had been recognised. Nothing in the private exchange reached Garrett. The danger lay in the difference between what each man could infer and what either was prepared to say.
n: Beyond the review-room glass, a technician waited until Charles nodded before approaching. Sylvanis smiled at the courtesy of it. Even the people who worked nearest him preferred to find another person between themselves and his attention.
sylvanis: Reliability. Everyone is asking so much of me today.
n: The old hall returned to him with the cup by the doorway still standing where someone had left it.
'''),
'SY09': scene('''
charles: I need the archive window for the demonstration reconciliation. A bounded copy, not the whole register.
n: He had prepared the request narrowly enough to be reasonable. Trial discrepancies, supporting entries, a period in which to compare them. Nothing that openly declared a private investigation. Sylvanis read the limits and found himself interested in what Charles might manage inside them.
sylvanis: Take the window. I would hate to stop you being thorough.
charles: I will keep the copy separate from the active consignment.
n: That was ordinary good practice. It could also become an obstacle. Sylvanis could see both possibilities without knowing where the copy would be placed or who would eventually find it useful. He had no miraculous access to another man's intentions. The incomplete view was part of the attraction.
n: Charles did not relax when permission came. He checked the exact interval and put the approval with the request. A less careful person might have mistaken the easy answer for safety. Charles behaved as if a pleasant mood could end halfway through a sentence.
sylvanis: You are allowed to look pleased.
charles: I am pleased to have what the work requires.
n: The reply was so carefully fitted to its purpose that Sylvanis almost laughed. He remembered the application: the same discipline, the same effort to keep a larger question folded inside a smaller one. Letting Charles remain close was a risk he chose, not proof that the risk could never affect him.
n: He signed the limited access. The archive would contain information he could not stand over every moment. Somewhere, while he was enjoying himself at the arena, Charles might use it well. That possibility was far more engaging than an assistant who had nothing to conceal.
sylvanis: Carry on, then. Surprise me with your diligence.
'''),
'SY10': scene('''
n: Takeo received him in the briefing room at headquarters. The copy of the supply agreement on the table had the original limits marked. Sylvanis recognised his own earlier acceptance beside them. He sat without being invited a second time and asked how many observers would attend.
takeo: My delegation is authorised to observe the agreed test. It has no mandate for an exhibition.
sylvanis: I can promise a considerably better evening.
takeo: Promise what you can deliver. I will close the order if you cannot.
n: Takeo did not raise his voice. One of the guards in the passage had turned to face the door when Sylvanis laughed. The room's arrangements were visible to both men: exits, lines of approach, the distance between a contractual dispute and something that could break the building around it.
n: Sylvanis enjoyed the tension and understood the figures. A failed demonstration could cost the Syndicate a dependable line of business. It could cost Takeo time, personnel and confidence in his supplier. Those were real consequences. He was considering them as part of the evening's possibilities.
sylvanis: You keep saying exhibition as though it is an illness.
takeo: I know what your enthusiasm has cost other people. My agreement does not make them my expense.
n: For a moment Sylvanis's amusement vanished. Then it returned, sharper. Reputation could close a room against him as effectively as it frightened someone into opening a door. Takeo had invited the useful specialist and prepared to contain the Crazed Demon within terms. Sylvanis decided to promise him more than those terms allowed.
n: The authorised delegation would still attend for a controlled demonstration. His added promise described something larger. He understood the incompatibility and left it there. The Crow had not approved it, and invoking the Syndicate would not make the permission exist.
sylvanis: I will make certain they have something to report.
n: Takeo kept his own copy. He remained at headquarters when Sylvanis left; the guards followed their visitor only as far as the route required. No territorial operation had been discussed.
'''),
'SY11': scene('''
n: In the arena control room, two versions of the programme lay beneath the same lamp. The delegation's copy promised comparison under agreed conditions. The fighters' copy promised an unscheduled exhibition. Sylvanis read both and signed the alteration himself.
sylvanis: Put my name on it. I want him to know whose idea it was.
n: The operator who received the instruction glanced at the second copy, then at the door. He had enough experience to recognise the problem and enough fear to hesitate over naming it. Sylvanis waited. Waiting made the man more uncomfortable than an immediate threat would have.
n: Finally the operator asked which copy should be treated as authoritative. Sylvanis pointed to the signatures. The man understood that the contradiction was intentional. He carried it away with the expression of someone who would remember exactly how he had been instructed.
n: This was not carelessness. Sylvanis could have produced consistent paperwork in seconds. He wanted the collision to survive contact with people who had something to lose: the buyer's observers, the supervisors, the Crow. The incompatible programmes were an invitation and an accusation waiting to find their readers.
n: Below the control-room window, workers checked the ring. They tested latches twice. One man looked up, saw the figure behind the glass and lowered his eyes before returning to the same latch. The Crazed Demon had lent the place his attention; everyone else was trying to finish the evening alive and employed.
sylvanis: There. Now the opening is less predictable.
n: He set the pen down. The names in the programme were still ordinary people with a limited capacity to survive his interest. He knew that. The knowledge sharpened his sense of what he had set moving rather than stopping him.
'''),
'SY12': scene('''
n: Charles used the archive interval exactly as granted. Sylvanis could see the session in the access record and the missing reserve case in the dispatch tally. He could not see the separate sealed hold where Charles placed a bounded copy of the trial discrepancies. The copy had its own custody record, outside the consignment that could be retrieved at the arena.
charles: The reconciliation has an exception. I have retained its supporting record.
sylvanis: Naturally.
n: Charles placed the notice on the desk, leaving enough space between it and Sylvanis's hand to avoid brushing him. The gesture might have been courtesy. Sylvanis had seen him use the same care when handling a volatile sample.
sylvanis: You have made the consignment smaller.
charles: I stopped the reserve case from entering the loading stream. The discrepancy needs to remain traceable.
n: A useful obstruction, plainly stated. Sylvanis could undo the withheld case now and spoil the shape of the problem. Instead he let it stand. The exhibition would proceed with less, and the people accounting for it would have something concrete to dispute. He enjoyed that part of Charles's action.
n: The sealed copy was another matter. Sylvanis did not know its storage key or acquire its contents by noticing the absent vials. Charles had achieved something independently, with consequences that did not belong entirely to the man watching him. Recognising an infiltrator had never meant owning everything the infiltrator could do.
charles: I will remain here to finish the laboratory record.
sylvanis: Sensible. Somebody ought to be.
n: Charles collected the papers he needed and left the copy where Sylvanis could see it. His cover remained intact. He had not completed his revenge, disclosed the eastern murders to Garrett or secured an answer to every private question. He had preserved evidence and denied part of the operation its reserve. That was a real success, small enough to survive being mistaken for routine work.
'''),
'SY13': scene('''
crow: Your two programmes disagree. I am cancelling the event. My teams will secure the consignment, ledger and equipment; discretionary support ends now.
n: The Crow had brought both signed copies into the executive room. He set them side by side rather than allowing Sylvanis to describe the difference. The preparations for containment had already begun. This was the answer of a man determined to keep command, not a complaint from an inconvenienced employer.
sylvanis: And if I go ahead?
crow: I will close it in person if necessary.
n: Sylvanis went still. Then his laughter arrived, bright and immediate. The Crow had finally offered something more interesting than permission. Direct opposition, resources at stake, a serious man prepared to enter the room himself: the possibility made the whole failed rehearsal seem worthwhile.
sylvanis: There. A better invitation.
crow: It is a cancellation. You may find the distinction expensive.
n: He knew the Crow meant it. That mattered. A staged refusal would have been another demonstration with a scheduled finish. Sylvanis wanted the resistance precisely because it belonged to somebody with an aim of his own.
sylvanis: You keep my name because it frightens people into your arms. Then you wonder why I want to see you use them.
crow: I do not wonder. I decide what I will permit it to cost me.
n: Each tried to make the other serve his purpose. The Crow would use a visible shutdown to prove that the Syndicate could contain its own liability. Sylvanis would turn that act of control into a confrontation worth seeking. Neither intention guaranteed success in every part of the encounter.
n: The limits remained explicit: the consignment would be secured, the equipment decommissioned, the ledger withdrawn. The Aces remained the Crow's people. No order Sylvanis gave could quietly transfer them into his command.
sylvanis: I know exactly what you intend, Mr. Crow. I am going anyway.
n: He left with the cancellation understood. There would be no honest misunderstanding to invoke afterwards, only the pleasure or disappointment of a choice he had made himself.
'''),
'SY14': scene('''
n: The delegation arrived expecting the contracted demonstration. It found the altered programme posted at the private arena entrance. The lead observer read the heading twice, then asked the attendant to identify who had authorised it. The attendant pointed towards the ring without saying the name aloud.
n: Sylvanis watched the news move through the room. Seats remained empty as people reconsidered how much they needed to see. A man near the service door stopped joking when another attendee whispered Crazed Demon. The silence after the nickname had more weight than the public announcements.
n: Fear had become part of his entrance long ago. Tonight he resented it a little. A frightened audience could be entertaining, but an opponent who had already imagined his own defeat was less likely to invent anything worth remembering.
n: The contracted fighter stood at the ring boundary and refused to pretend that this was the agreed event. He was strong enough to be worth employing and experienced enough to recognise a changed risk. Sylvanis met the refusal with an eagerness that did nothing to reassure him.
sylvanis: Then we can finally stop rehearsing.
n: Charles was still at the Glasshouse. Takeo was still at headquarters. Neither had been pulled into the arena merely because Sylvanis wanted a bigger evening. The people here would face the consequences of their own part in it, while the shutdown teams were already approaching by the service route.
n: Winning the encounter could establish the display he had promised himself. It could not put him beside every vial, every document and every switch. The strongest man in the world still occupied one place at a time. The Crow had built an operation around that fact.
sylvanis: Come on, then. Make me change my mind about something.
n: He entered the ring. Whatever happened next would have to happen in the actual fight.
'''),
'SY15': scene('''
crow: My teams are closing your consignment routes and dismantling the equipment. I am withdrawing with the ledger. This arena operation ends tonight.
n: The Crow stood beyond the ring's service opening, fully concealed beneath his mask and robes. Behind him, equipment bays were being emptied. The arena had begun to lose the small mechanical sounds that made it feel like a working place. Sylvanis heard each silence arrive.
sylvanis: You brought yourself. I knew this could be worth doing.
crow: Contest the withdrawal if you intend to keep anything.
@CS-SY07
n: Sylvanis advanced towards the service passage. The Crow shifted across his approach, leaving the closed ledger between their routes for a moment. Neither man had secured it yet. The invitation to strike was also a demand to choose what an opening would be used for.
n: Four declared exchanges remained before the service-route withdrawal completed. He could pursue the Crow directly or spend opportunities attempting to secure the ledger. The Crow would contest either effort. The opposition was real; so was the trade-off.
n: Sylvanis did not need to believe the Crow his equal to want the fight. There was pleasure in forcing that composed authority to act, in finding the difference between a plan described at a table and one defended at close range. Yet he could already feel the familiar problem waiting beyond it: a victory might become another thing he had finished understanding.
sylvanis: All this work to make me manageable. You should have spent it making me a better opponent.
crow: I have spent it keeping what I intend to own. Your satisfaction is your concern.
n: A precise answer. Sylvanis wanted to hit him for it and laughed because he did. The Crow was prepared to concede nothing merely to preserve the fiction of a partnership without costs.
n: The shutdown itself would happen. Bodily dominance and retained assets were separate results. Sylvanis could be overwhelmingly dangerous and still lose things he had chosen not to protect. The encounter would settle which openings he actually used, what the resistance cost and who left with the ledger.
'''),
'SY16': scene('''
crow: Your rank remains. Your exhibition account does not. Any replacement site requires separate authorisation.
n: The executive meeting room looked as it had before the exhibition. That irritated Sylvanis more than a display of triumph would have. The Crow had survived another disruption and returned to the work of making the world answer to him. An aide had prepared the settlement, then found a reason to leave before Sylvanis arrived.
sylvanis: You have made that sound so uninviting, Bro.
crow: I intend to retain your usefulness. I have no obligation to finance every method you choose to demonstrate it.
n: The losses belonged to the campaign operation, not to his ordinary wallet. The public lounge, the Iron Circle and the Glasshouse remained standing. The private arena's exhibition was permanently closed; its equipment would not quietly become available again because he disliked the result.
sylvanis: Still keeping me, then.
crow: You know why.
n: He did. The same intelligence that made him impossible company could solve problems the Crow wanted solved. The same violence that wrecked an agreement could make a rival afraid to refuse one. The Crow had weighed the danger again and kept the relationship. Sylvanis, in turn, still had a man whose ambitions would continue finding things to break.
n: The transaction offered no comfort and asked for no affection. They had spent years making use of one another. Tonight added a restriction, a loss and another occasion each would remember when deciding how far to push the next.
sylvanis: Try to make the next offer sound less like a meeting.
n: The Crow closed the account. Sylvanis still had to face Takeo's answer to the failed order, then return to the laboratory where Charles had been working while the arena came apart. An ending, for everyone involved, required more than his opinion of the fight.
'''),
}

# These are scene exits, not journal summaries of the implementation contract.
AFTERMATH_TEXT = {
'SY01': 'Charles waited until Sylvanis closed the folder before reaching for the next report. The signed programme remained unchanged. For now, that was the only reassurance the room had.',
'SY02': 'Sylvanis returned the roster with a note beside the rehearsed finish. Charles read it, then looked up. The request was precise enough to obey and troubling enough to make obedience a choice.',
'SY03': 'The staff request stayed on the desk. Sylvanis had found it interesting without promising to repair the lost shift. Outside the room, the people who had sent it still needed an answer.',
'SY04': 'He had chosen where to put the first pressure. The programme remained in his hand, ready to become something the people expecting it would recognise too late.',
'SY05': 'The meeting ended without a raised voice. Beyond the door, the waiting aide searched the distance between them for a sign of how much trouble the conversation had created.',
'SY06': 'The Crow kept his copy of the instruction. Sylvanis took the other. He could no longer pretend that the boundary had been vague, and had never intended to.',
'SY07': 'The reservation went through. Twenty operating units bought the private venue; sixty remained. Sylvanis left the inspection lamp burning over the two vials and took the arena key.',
'SY08': 'Charles carried the register away. Sylvanis let him. Between the omission on the page and the question neither man had asked aloud, the room had acquired a little more tension.',
'SY09': 'The archive interval opened under the agreed limits. Charles went to work. Sylvanis resisted the uninteresting impulse to stand over him and inspect everything he did.',
'SY10': 'The delegation had its authorised purpose and Sylvanis had made his additional promise. Takeo stayed at headquarters. Neither copy of the agreement could contain both versions of the coming evening.',
'SY11': 'Both programmes left the control room. The contradiction now belonged to people who could act on it. Sylvanis watched the operator hurry down the passage and waited for the first reply.',
'SY12': 'A dispatch space remained empty where the reserve case should have been. Elsewhere in the Glasshouse, the sealed supporting copy stayed beyond the arena consignment. Charles had finished something Sylvanis could not recover merely by winning a fight.',
'SY13': 'Shared support was withdrawn. The cancellation followed Sylvanis out of headquarters as a fact, not a rumour. He went towards the private arena with considerably more energy than he had brought to the first meeting.',
'SY14': 'The encounter had supplied its own result and its own cost. Through the service opening came the sounds of the shutdown. Whatever Sylvanis thought of the exhibition, the evening had not yet finished answering him.',
'SY15': 'The last route out of the operation closed. What had been secured would appear in the settlement; what had been lost would not be restored by another boast. The arena fell quiet around the equipment that no longer belonged to an exhibition.',
}

MEMORY_RETURN_TEXT = {
 'SY-M01': 'The customs form gave way to the Crow’s signed programme. Sylvanis rubbed a thumb along its edge. Different paper, a grander institution, the same expectation that he would become manageable once somebody had written down what he was for. Charles was still waiting for his answer.',
 'SY-M02': 'The dead alley vanished from the dark screen. In its place waited a roster of men who knew his reputation and hoped the promised rules would protect them. He turned back to their recorded exchanges, looking past the rehearsed finish for anything they had failed to make predictable.',
 'SY-M03': 'Kaden’s table receded. The unpaid shift was still on the review-room desk. Sylvanis remembered what a good man had been willing to spend on people who could offer nothing back, then looked at the supervisor’s carefully revised request. He wanted to know what this man would do when his promise became expensive.',
 'SY-M04': 'He was alone with the three possible provocations again. Once, the man who became the Crow had brought him a sheet full of opportunities. Today he could return the courtesy. The question was which pressure would produce the response he most wanted to see.',
 'SY-M05': 'The Crow was still across the executive table, concealed behind the mask he had chosen long after that other room. Sylvanis let the memory remain unspoken. There were questions one could keep alive simply by declining to answer them. He turned back to the present disagreement.',
 'SY-M06': 'The restriction in his hand belonged to this evening, but he recognised its shape. Another limit, another assessment of how much inconvenience his usefulness could buy. He folded his copy once and considered what the Crow might have to offer when the familiar calculation failed.',
 'SY-M07': 'The inspection lamp shone over the red and blue vials. Sylvanis looked from them to the waiting reservation. A tiny unexpected result had kept him at the work for years. He wanted another one badly enough to put the private arena, the money and the Crow’s patience behind the attempt.',
 'SY-M08': 'Charles had not moved the register from his side of the desk. The remembered doorway belonged to Sylvanis alone; nothing about the silence disclosed what had happened there. He met Charles’s guarded attention with the easy expression that made the laboratory so difficult to trust.',
 'SY-M09': 'The old application became the present request for archive access. Charles had learned the routines of the laboratory without becoming as predictable as its schedules. Sylvanis read the proposed limits once more, interested in what a careful man might accomplish when allowed a little room.',
 'SY-M10': 'Takeo’s corrected agreement was still before them. Sylvanis recognised the same determination to separate a useful supplier from the danger that came with him. The authorised delegation was one thing; the evening Sylvanis had begun imagining was another. He would let both descriptions leave the room.',
}
