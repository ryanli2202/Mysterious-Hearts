"""Authored 2026-11-15 expansion of What Remains.

Explicit speakers and historical transitions are content, not inferred dialogue.
The compiler installs these passages; saved reading snapshots remain immutable.
"""
import copy


def n(text, **metadata):
    return dict(text=text, authored=True, **metadata)


def d(speaker, text, **metadata):
    return n('“'+text+'”', speaker=speaker, **metadata)


REPLACE = {
    'RD01': [
        n('Rei had slept with the hall light on. At three he had checked the front door; at four he had checked whether Yuriko’s shoes were still beside it. In daylight the shoes looked faintly ridiculous as evidence of anything. One lay on its side. She had come home tired, kicked them off, and gone to bed. He wanted to be the sort of brother who could stop there.'),
        n('The notice had arrived among ordinary post: Kurose House, a public address, the name Hamayashi-kai printed above an invitation to enquire. No threat. That had almost made it worse. Somebody could put the name on clean paper and send it into a home where he had finally learned to leave a door open.'),
        n('He had thrown it away, then retrieved it before Yuriko saw the bin. Now the old training notebook lay beside it. She had left that book with him years ago. Today he needed to know whether the people behind the notice were connected to the dead, whether the house still held children, and whether his sister had a reason to be afraid. Those were questions he could investigate. The tightness in his chest kept offering answers before he had asked them.'),
        n('He took a spare exercise book from the drawer. In one column he wrote what he could verify. In another he left room for what he only feared. At night those categories had started to blur. If he had to ask someone else for help, he wanted to be able to explain what had actually happened without making them untangle every thought in his head.'),
        d('rei', 'A place to put it. That’s all.'),
        n('The old timetable divided a child’s day into repetitions, assessments, punishments. He recognised the pressure of his own pencil. He could remember counting, and a kitchen clock somewhere beyond the wall. He could not walk through a complete day. Trying made his jaw hurt.'),
        n('Beside it he laid a drawing made after their escape: a bus passenger asleep under an oversized hat. Nobody had assessed the drawing. Nobody had asked him to improve the passenger. He had wanted to make it and had made it. Marcus would have asked where the bus was going, then invented an inconvenient answer.'),
        d('rei', 'I made this too.'),
        n('He meant the drawing. His hand remained over the timetable. For a moment he could not bring himself to move it.'),
        n('He left the gaps unfilled. The journal could hold a question without obliging him to answer it tonight. It would not become another timetable, another set of marks he had to earn before he was allowed to sleep.'),
        n('The Kurose House notice gave him an address to check against the archive. Before he closed the old book, the kitchen clock seemed to return: not a whole recovered past, but the narrow sound around which a child had once arranged his breathing.'),
    ],
    'RD05': [
        n('The archive’s clock had a plastic face and a second hand that hesitated. Rei watched it through an entire minute before admitting he had stopped reading. He had come to establish what Kurose House was. Instead he had caught himself measuring how long it would take to cross the room.'),
        n('The filings distinguished the destroyed original clan from a later organisation that had adopted the name. A transfer inventory accounted for records that survived elsewhere. Paper could outlive the people who wrote it. He understood that. His body continued to prepare for someone to enter behind him.'),
        n('In a retained training ledger, his childhood appeared as columns. An adult had written a punishment beside a missed interval, then drawn the same neat line used for equipment returns. There was no column for whether the child had agreed. He read his own name twice. For years he had wondered whether the pieces he could remember were somehow too distorted to be trusted. Here was an adult’s unembarrassed handwriting.'),
        d('rei', 'You wrote it down.'),
        n('He had expected a discovery to feel like a door opening. He wanted to put his fist through the filing cabinet. The impulse arrived so completely that he had to set the pencil down before it snapped. A reader at another desk turned a page, unaware of the effort it took him to remain seated.'),
        n('Emi Suda and Ren Aoki administered the present successor. Daichi Kurose led it after Keisuke’s departure. Its adult roster and recorded departures would have to be checked at the house. The filings gave him grounds to ask about the living; they did not put his old captors back inside their bodies.'),
        n('He copied the necessary dates once. After that he sat with the record of a boy who had never been asked what he wanted to become. The question he had brought to the archive was still there, but another had joined it: why did proof that the original clan was dead fail to make him feel safe?'),
    ],
    'RD11': [
        n('The folded corner of the storyboard caught under Rei’s thumb. Adult hands, his own table, the city outside the window. He knew where he was. The school morning came back anyway.'),
        n('FLASHBACK — School courtyard, after Marcus’s death', mode='memory'),
        n('Emily and Sophie were waiting beside the bench. Sophie had her bag on the ground instead of over one shoulder. Emily kept looking at the page under Rei’s arm. He had brought a new station roof for Marcus to complain about.'),
        d('rei', 'Where is he?'),
        d('emily', 'R-Rei. Can you come here?'),
        d('sophie', 'We didn’t want you hearing this in the corridor.'),
        n('He noticed Sophie’s voice before he understood the words. No invitation, no impatient joke about being late. He stopped just beyond her reach.'),
        d('emily', 'Marcus died. His family told the school. He… he died by suicide.'),
        n('The page bent against his ribs. For a moment all he could think was that he had brought the wrong thing. A roof. He had spent the evening drawing a roof while something had happened that made the whole morning impossible. Then the thought broke and Joseph’s face occupied the space it left.'),
        d('rei', 'Where’s Joseph?'),
        d('sophie', 'Stay here.'),
        d('rei', 'Where is he?'),
        n('Rei turned toward the buildings. Sophie stepped across his path. He tried to go around her, too fast; her bag caught under his shoe and he kicked it clear. The scrape made Emily flinch. He saw it and hated that he could still be moving.'),
        d('emily', 'D-Don’t. Please, look at me.'),
        d('rei', 'He kept doing it. He knew Marcus couldn’t—'),
        n('He could not finish. His breath was arriving in short, useless pieces. There was a railing beside him and suddenly he was gripping it hard enough for the cold to hurt. He wanted something he could stop. A person he could put between his hands. Grief had no shape he knew how to fight.'),
        d('sophie', 'I’m angry too. You’re scaring us. Take your hands off that.'),
        d('rei', 'Move, Sophie.'),
        d('sophie', 'No. I’m not letting you run straight into him like this.'),
        d('emily', 'You can be angry here. I-I’m staying. But I can’t help you if you disappear.'),
        n('Emily held out her hand without grabbing him. It shook. They had lost Marcus too, and he had made them spend their first words trying to keep him from hurting someone. The recognition reached him slowly, through the roaring in his ears. He let go of the railing.'),
        d('rei', 'I should have been there.'),
        d('emily', 'We don’t know everything he was carrying. I wish we did. That doesn’t mean you could have made him stay.'),
        d('rei', 'I got you out. I got—'),
        n('He stopped before he brought Yuriko into a school courtyard where her history did not belong. Emily knew the greenhouse. She did not know every room his mind had put beside it. In each of them there was someone he loved and a door he had reached either just in time or impossibly late.'),
        d('sophie', 'You don’t have to explain it properly. Sit down before you fall down.'),
        n('He sat. Emily sat beside him; Sophie stayed between the bench and the corridor until his gaze stopped searching past her. The storyboard lay closed on his knees. The next sob hurt more than the first because there was no anger in the way of it.', core_id='CS-R02'),
        d('rei', 'He still has my pencil.'),
        d('emily', 'I know.'),
        d('sophie', 'We’ll go to the counsellor together. In a minute. We can have a minute.'),
        n('They slowed him down that morning. They did not extinguish the anger; later it would find Joseph outside the administration entrance. For now Emily’s hand remained beside his, available without closing around it. He lowered his head and asked them to stay.'),
        n('PRESENT — Rei’s home', mode='present'),
        n('His thumb was still caught on the folded paper. He flattened the corner, then stopped trying to flatten it. He remembered their fear as clearly as their kindness. He had wanted protection to mean that nobody close to him could ever be hurt. The impossible demand had survived the boy who first made it.'),
    ],
    'RD15': [
        n('Rei laid the storyboard across the table. Marcus had drawn three possible endings and crossed out only one. At school Rei had found that indecision irritating. Now he missed being able to tell him which ending was the worst.'),
        n('Marcus had looked at his drawings before asking what he could do. No demonstration, no test of usefulness. At their first library table he had asked whether the sketched passenger was waiting for someone or resting. Rei had answered that he did not know. Marcus had said they could leave the passenger alone until he decided.'),
        n('He had not known about the clan. That mattered too. Rei had been allowed to become a friend before becoming a history somebody felt obliged to handle carefully. He could be late, irritating, wrong about an ending. Marcus could sulk and come back with two versions. There had been room for both of them to be unfinished.'),
        d('rei', 'You would hate how everyone gets sensible when I say your name.'),
        n('The laugh escaped him, then failed halfway. He put the storyboard where he could see it without treating it as a set of instructions from the dead. He would not turn a friend’s drawings into evidence that he ought to have known.'),
        n('Beside it lay two empty slots on an Iron Circle practice list. Jun, who used to lend him spare tape and complain about his handwriting. Luis, who stayed after bouts to help somebody else get their bag downstairs. Both had been offered Blackstone assessments. Neither had answered the private enquiries Rei had made after they stopped coming. They were people he knew, not names copied from a rumour.'),
        n('Jun’s last ordinary message had included a picture of the public referral form and a complaint about how long the appointment would take. Nothing in it had sounded like goodbye. Rei had initially assumed work, an injury, a week away from the arena. Now an unanswered call could hold every absence he had ever lived through.'),
        n('He had no proof of kidnapping yet. He had a document he could compare and a company he could ask. Joseph’s name made the decision hot and immediate; the thought of Jun and Luis gave it a direction beyond an old school wall. He took the referral reference to Blackstone.'),
    ],
    'RD16': [
        n('The receptionist’s desk was immaculate. Rei could see his reflection in the polished edge: someone who had dressed carefully enough to pass for calm. He had been awake most of the night. He had rehearsed an accusation on the way here and now could barely remember the polite version of the question.'),
        d('rei', 'I’m asking about your assessment programme. Two people I know came here.'),
        n('Robin could provide published participation information, not confirm private appointments. Rei knew why that distinction existed. Hearing it felt like being shut out of a room while somebody he knew was still inside.'),
        d('rei', 'Then the public form. Please.'),
        n('The project number matched Jun’s copy. A promise of performance assessment occupied most of the first page; withdrawal referred the reader to a separate security agreement. Rei ran a thumb under that sentence until the paper began to curl.'),
        d('rei', 'This says they can leave. Where does it say what happens when they try?'),
        n('Robin pointed to the public procurement reference for the archived agreement. She did not have the answer he wanted. He heard himself begin Joseph’s name in a tone that made her lean back, and stopped.'),
        d('rei', 'Sorry. I need the reference. That’s all I’m asking you for.'),
        n('Outside, he almost called Emily. He wanted her to answer immediately, to fill the space in which his mind had put her in the same building. Instead he looked at the unsent call and heard how frightened that would sound if he demanded to know where she was. She was Awakened too. That was a reason to tell her what he found, not a reason she owed him proof of safety every hour.'),
        n('He photographed the form once, with the reference visible. The question for the archive was precise: did the security agreement permit Blackstone to hold somebody who had withdrawn? Underneath it, unhelpfully, ran another: if he had checked sooner, would Jun have answered?'),
    ],
    'RD17': [
        n('The complaint described an assessment that did not end when the participant withdrew. The name was withheld. Rei kept it withheld as he compared the signed authorisation and the security contract. He had come looking for an explanation that left Jun and Luis somewhere ordinary. The documents kept removing those possibilities.'),
        n('Richter had authorised restraint and continued weapons-response trials on Awakened people who tried to leave. The delivery records linked the project number to the loading compound, records office, experimental wing and executive command. Voluntary participation had become a recruiting phrase for a programme that withheld departure.'),
        n('Jun’s voluntarily shared referral carried that same project number. Separately, a short account from Luis’s partner, supplied to Rei for the search, placed a Blackstone collection vehicle outside their building. Luis had said he was refusing further assessments. His bag was still at home. Taken together, the independent accounts and records described forced collection and confinement, not two competitors choosing to skip practice.'),
        n('Rei left the partner’s address out of his working copy. He kept the original account and its source separate, for someone able to follow the disappearances. They were not going to become names scattered across an angry public accusation.'),
        d('rei', 'They said no.'),
        n('The words emerged too loudly. He read the authorisation again, looking for an exception that was not there. His foot had begun tapping beneath the table. He held it still with the other and found his hand had started instead.'),
        n('He saw Jun handing a roll of tape to a nervous newcomer. Luis arguing that the arena stairs were a deliberate insult to injured knees. Then he saw Emily in the greenhouse years ago, and an empty bench, and Yuriko waiting for him to say she was safe. Different people, different rooms. His thoughts were beginning to force them into one demand: reach the door before it closes.'),
        n('Emily’s awakening made the programme’s criteria personal in another way. He had no record naming her as a target. He knew that. Fear did not wait for her name to appear. Joseph had hurt people before and explained it away; now he had money, guards and rooms designed to keep someone inside.'),
        n('Rei tried to write a sentence and found he had pressed through the paper. He put the pen away. A copied authorisation, the complaint, the referral match and the collection account were enough to establish the immediate work. He secured a duplicate of the evidence. Then he sat with his fists under the desk until he could stand without knocking the chair over.'),
        n('He had begun the journal to keep fear separate from fact. Tonight it could still do that much. It could not make him sleep, or stop him hearing every unanswered call as the start of another loss.'),
    ],
    'RD20': [
        n('Outside Kurose House, Rei could still hear Ren saying that people left. Ren had not said it triumphantly. He had pointed to a dated departure, then another, and waited for Rei to read them. The ordinary patience was almost unbearable.'),
        n('He wanted the name to have one meaning. If it did, he would know what to do with the shaking in his hands. Instead the present organisation had supplied evidence of voluntary adult membership, and the child in his head was still waiting for permission to stop.'),
        n('A door closed behind him. He flinched and turned so sharply that a passing stranger stepped aside. No one had followed him. He looked back at the street, ashamed of the stranger’s startled face, then angry that he had another thing to be ashamed of.'),
        d('rei', 'They’re gone.'),
        n('He meant the original clan. Saying it had not changed the sound of the door. Leading this successor, leaving it or dismantling it would each affect living people who had not trained him. None could retroactively reach the boy in the training hall. He could know that and still want the sign torn off the building.'),
        n('He rested his hands on the cold riverside rail. Jun and Luis were still missing. He had started counting exits at the archive and checking his phone in the middle of sentences. The danger at Blackstone was real. The certainty that every delay made him a bad brother, a bad friend, was becoming something he could barely question.'),
    ],
    'RD29': [
        n('Rei reached Blackstone with an evidence copy already secured elsewhere. That was the sensible part. He had told himself he would look at the entrance, check the route, give himself time to think. He had repeated the sentence all the way there.'),
        n('Then a loading shutter came down. Metal struck concrete with a flat, final sound. Behind it were people who had tried to leave. In his head the sound became the training-hall door, the greenhouse, a call that never connected. He knew those events were different. He could no longer make knowing it slow his body down.'),
        n('He called Jun once more. No answer. His thumb moved to Emily’s name before he stopped it. He had no evidence she was inside, no message saying she had been taken. The imagined picture was vivid enough to make him feel sick: Joseph deciding what her awakening was worth, Emily asking to stop, somebody noting the request and continuing.'),
        d('rei', 'No. You don’t get another one.'),
        n('He struck the wall beside the entrance. Pain ran up his arm. It did nothing useful; he hit it again before he could make himself stop. Breath caught in his throat and would not come cleanly. He bent over with his hands against his knees, furious at the tears, furious that he could not turn them into a plan.'),
        n('For years he had made competence stand in for being all right. Get Yuriko out. Keep Emily safe. Win the bout. Make dinner. If the person beside him could breathe, he could postpone asking why he could not. Marcus had broken the bargain he had made with the world, because it had never been a bargain the world agreed to keep.'),
        n('The part of him the clan had trained offered a familiar relief: stop thinking, find the obstruction, destroy it. It did not care about Jun’s jokes or Luis’s careful hands. Rei cared. At that moment he could barely separate caring from the urge to hurt the man who had taken them.'),
        n('He wiped his face with his sleeve and moved toward the guard line before his breathing had settled. This was an attack born of anger and a breakdown, not a clean rescue plan. He would still have to survive each actual encounter and open the places where people were held. Rage supplied neither victory nor their safety.'),
    ],
    'RD30': [
        n('The executive door closed behind Rei. He heard it as a challenge. Joseph stood beyond the desk, intact and composed in a building full of people whose right to leave he had signed away. Rei threw the copied authorisation onto the polished surface hard enough to scatter the sheets.'),
        d('rei', 'Where are Jun and Luis?'),
        d('Joseph Richter', 'If you mean programme participants, you have bypassed several proper channels.'),
        d('rei', 'They asked to leave. You collected one from his home. Don’t call that a channel.'),
        n('Joseph looked at the scattered signature pages. His mouth tightened, then smoothed. Rei had seen that adjustment at school: the instant before cruelty dressed itself as somebody else’s misunderstanding.'),
        d('Joseph Richter', 'These are specialised trials. Interruption creates risks you are not qualified to assess.'),
        d('rei', 'You put them in restraints. You tested weapons on them. Say what you did.'),
        n('He slammed a hand onto the desk. The sound startled even him. Joseph watched the hand, and Rei hated the small measuring look more than the evasion.'),
        d('Joseph Richter', 'You always did mistake losing control for having a point.'),
        d('rei', 'And you always found someone you thought couldn’t hit back.'),
        d('Joseph Richter', 'This is not school.'),
        d('rei', 'Marcus was not a rehearsal.'),
        n('The name broke his voice. He had wanted to speak it steadily. Instead he saw a library table and an unfinished argument about an empty room. Marcus would never get to be tired of this conversation. Rei was so tired he could feel the effort of remaining upright.'),
        d('rei', 'He made things. He wanted to finish a film. You made every room smaller for him and then acted like it was nothing. I can’t get him back. I know that. But you don’t get to keep doing this.'),
        d('Joseph Richter', 'You cannot lay an entire death at my feet.'),
        d('rei', 'I’m asking you to answer for what you chose. The bullying. The people locked downstairs. Your signature is right there.'),
        n('Joseph’s sleeves parted around reinforced arms. A powered spinal frame locked into place. Targeting lights moved across the desk and found Rei. The machinery supplied the answer Joseph had been working toward: another advantage he could bring to an argument instead of listening.', core_id='CS-R03'),
        d('Joseph Richter', 'Awakened people take their advantages for granted. I built mine.'),
        d('rei', 'Is that what Emily would be to you? An advantage to take apart?'),
        n('He had revealed the fear before he could swallow it. Joseph’s glance sharpened. Rei had no proof of a plan against her. He would not give Joseph another private detail to use.'),
        d('Joseph Richter', 'You brought that name into this room.'),
        d('rei', 'And it’s the last thing about her you’re getting from me.'),
        n('His hands were shaking as he raised them. The boy trained to obey could have stood more neatly. The person he wanted to be would have recognised how close he was to making violence the answer to everything he could not bear. Both were here. Neither could do this for him.'),
        d('rei', 'Open containment.'),
        d('Joseph Richter', 'Make me.'),
        n('Rei stepped forward, furious and frightened and past the point where he could pretend this was methodical. Joseph brought his weapons online. The confrontation would be decided by the fight, not by the force of either man’s words.'),
    ],
    'RD36': [
        n('FLASHBACK — Hamayashi-kai, Rei aged ten; Yuriko aged seven', mode='memory'),
        n('The kitchen clock could be heard through the training-hall wall. Rei had learned to count its ticks when the room went quiet. Quiet did not mean finished. Sometimes it meant an adult was deciding what to do about him.'),
        n('He held the stance until his legs trembled. A correction came from outside his field of vision. Again. Weight lower. Do not look toward the door. He knew the sequence well enough to anticipate the next instruction and still could not complete it to their satisfaction. Exhaustion was treated as disobedience. Pain was another thing he was expected to conceal.', core_id='CS-R07'),
        n('They called the work his purpose. A weapon did not ask whether it had done enough. It did not ask to eat because the kitchen smelled of rice. The adults had arranged a whole childhood around making that sentence feel as ordinary as his name.'),
        n('His heel shifted. He knew before anyone spoke that the interval would begin again. He stared at a pale scratch in the floor and tried to keep a room in his head where no one was watching. He could not picture what he would do in it.'),
        n('Later, in the siblings’ room, Yuriko was folding a scrap of paper. She had been corrected for answering an adult too directly. Her treatment was less brutal than his; it still taught her to lower her eyes before she was asked. She looked at his hands, then deliberately looked at the paper instead.', background='locations/hamayashi-siblings-room'),
        d('yuriko', 'It keeps falling down.'),
        d('rei', 'The wall’s too short.'),
        d('yuriko', 'Can you fix it?'),
        n('He reached automatically. She pulled the paper closer, not away from him entirely, just enough to save the roof from being crushed. He waited. No instructor had ever rewarded waiting when he could perform a task faster.'),
        d('yuriko', 'Tell me. I want to do that bit.'),
        d('rei', 'Fold here. No, the other edge. It needs somewhere to stand.'),
        n('She tried. The little house stood crookedly on the mat. Yuriko smiled with all her attention on it, and Rei found himself wanting the object to survive the evening. Not because anyone had ordered him to preserve it. Because she had made it.'),
        d('yuriko', 'Does it need a window?'),
        d('rei', 'Only if you want one.'),
        n('The answer surprised him. He watched her cut a small square with her fingernail, then flatten it carefully. In the training hall his hands were assessed for what they could do to someone. Here she wanted him to hold a paper wall while she decided where the light went. He held it.'),
        n('PRESENT — The open notebook', mode='present'),
        n('At his own table the clock was quieter. Adult Rei could remember the sound, the waiting, pieces of the room; other intervals remained blank. Knowing the childhood had happened did not give him uninterrupted access to it. He closed the timetable before searching for more. The paper house belonged to a history in which he had wanted something besides becoming useful.'),
    ],
    'RD37': [
        n('At the archive, the retained ledger’s phrase about obedience brought Rei back to the end of that childhood. There were pieces he knew, pieces Yuriko had told him, and stretches neither had laid out for the other. The old record could corroborate abuse. It could not make the whole night return.'),
        n('FLASHBACK — Hamayashi-kai, Rei aged fifteen; Yuriko aged twelve', mode='memory'),
        n('Yuriko’s blanket was folded before bedtime. That was what Rei noticed first. She sat beside it with her hands in her lap, trying to look as if she had chosen to be ready. An adult had told her she would be moved away from him. Obedient girls did not make arrangements difficult.'),
        d('yuriko', 'They said you already knew.'),
        d('rei', 'I didn’t.'),
        n('He had refused an instruction. It had not been a grand rebellion; he had reached the end of what he could make himself do and said no. Now the clan had found the place to apply pressure. They had told him that access to his sister depended on his usefulness. Yuriko’s life could be rearranged to correct his behaviour. His compliance had never bought her safety. It had only kept the threat available.'),
        d('yuriko', 'Did I do something?'),
        d('rei', 'No.'),
        d('yuriko', 'Then why do I have to go?'),
        n('He had no answer he could bear to give. For years he had told himself that if he endured what they did to him, she might be spared the worst of it. She had been sheltered from some of his treatment and subjected to a different kind of control. Now even the little space between them could be removed at an adult’s convenience.'),
        d('rei', 'You’re coming with me.'),
        n('He said it before he had a safe way to make it true. In the passage outside, an adult ordered him back to the training hall. Rei asked for the gate to be opened. The answer was another instruction: put his sister down as a concern, return to his purpose, and her treatment could be reconsidered. They spoke as though she were an object they could place beyond his reach.'),
        n('Rei had spent years noticing the smallest change in an adult’s voice. That night he noticed a different thing: he was listening for the command that would make him obey. He could feel the old habit trying to move his feet. Behind him Yuriko shifted on the mat, waiting to learn whether his promise meant anything.'),
        d('rei', 'Open it.'),
        n('The adult reached to force him back. Rei moved. The first crash brought others into the passage. Orders collided: stop, kneel, hold him. He had obeyed those words with aching muscles and a child’s belief that enduring the next interval might protect his sister. Now every attempt to restrain him met the violence they had spent his life teaching him.'),
        n('A lantern went over. He crossed the training-hall threshold in the wrong direction, driving the people who had once watched him from the doorway into the courtyard. Somebody used his name as if it were still an instruction. He shouted that they were letting her go. He could not remember afterward when he stopped saying it and simply kept moving.'),
        n('The resistance spread through the compound; so did what he did to end it. The clan that had made him a weapon could no longer make him stop. This was the destruction he would carry into the rest of his life: he killed the clan that had raised him. No clean moment separated getting them out from becoming terrified of what his own hands had done.'),
        n('In the courtyard afterward, Rei stood among the countless bodies of the Hamayashi-kai. The night had become terribly quiet. No one was going to give the next instruction. His hands still waited for it. He had ended the people who called him a weapon by doing the thing they had taught him to do.', core_id='CS-R08'),
        n('He could have remained there counting what he could see. Then he remembered that Yuriko was still waiting for an answer. He turned away from the courtyard and went back to her room.'),
        d('yuriko', 'Rei?'),
        n('She stopped at the sight of him. He knelt beyond her reach because he did not know what his hands looked like to her. He could hear himself breathing too hard. The room contained her blanket, the folded things she had been told to take, and a life that had just become impossible to return to.'),
        d('rei', 'It’s me. We can go now.'),
        d('yuriko', 'Are they coming?'),
        d('rei', 'No.'),
        n('He did not ask her to look at the courtyard. He held out a hand and waited for her to choose it. She did, after a moment that seemed longer than the night. He took his sister out. They would reach the United States; the whole route and every violent interval would never become a story adult Rei could reliably recite.'),
        n('PRESENT — The archive desk', mode='present'),
        n('The chair pressed against the backs of his knees. Rei sat down again. He had wanted the book to prove the old clan was gone. It did. He was still here, with the part of him they had trained, and that was the harder fact to put away.'),
    ],
    'RD38': [
        n('The ledger was closed, but the absence of another instruction carried a quieter scene behind it.'),
        n('FLASHBACK — A temporary room after the escape; Rei fifteen, Yuriko twelve', mode='memory'),
        n('The door had a latch on their side. Rei tested it, then tested it again. Yuriko watched from the bed with the blanket pulled around her shoulders. He wanted to tell her that a latch she controlled meant she could sleep. He could not stop checking it himself.'),
        d('yuriko', 'Will you sit down?'),
        d('rei', 'In a minute.'),
        n('He found water. Moved a cup away from the bed’s edge. Folded a towel. There was always another small thing he could make safe, and each one postponed the moment in which he would have to sit with what he had done. When he shut his eyes he saw the courtyard. He began keeping them open.'),
        d('yuriko', 'You said that before.'),
        n('He sat on the floor beside her. She asked whether they would be made to go back. He answered no too quickly. She asked again, more quietly, and this time he let her finish before answering.'),
        d('rei', 'I’m here. If you wake up, I’m here.'),
        d('yuriko', 'What if you wake up?'),
        n('He looked at the cup. He had prepared answers about food and doors and where her things were. No one had asked what would happen to him while he was busy making those answers.'),
        d('rei', 'You don’t have to worry about me.'),
        n('It was the first promise he made in that room that he had no right to ask her to believe. His stomach turned. His hands had started shaking again, so he tucked them beneath his arms where she could not see. He told himself he would deal with it after she slept.'),
        n('Yuriko talked about the paper houses they used to make. He asked where she would put a window now. She said somewhere she could see who was coming, then cried because she had not wanted that to be the answer. He stayed beside her while she cried. He did not correct her into gratitude.'),
        n('When she slept he remained on the floor, listening to her breathing and mistaking the fact that she was calmer for proof he was all right. Tomorrow he would find another practical task. There would be enough of them to postpone his own terror for years.'),
        n('PRESENT — The archive closes around an ordinary afternoon', mode='present'),
        n('Rei put a hand flat on the desk. He had learned to cook, pay bills, make a home. Those things were real; they had helped Yuriko build a life of her own. They had also given him a respectable answer whenever someone asked whether he was coping. He could point at dinner. He could point at her schoolwork. He rarely pointed at himself.'),
    ],
}


# Additions retain stable legacy source indices and conditional disclosure blocks.
APPEND = {
    'RD02': [n('Yuriko moved the water glass closer, then stopped before putting it into his hand. He recognised the restraint. She had learned it from him, and he was suddenly tired of being the person who taught everyone how gently to approach. He drank because he was thirsty, which was a small but distinct thing from doing it to make her stop worrying.')],
    'RD03': [n('The first mouthful was too hot. He swallowed it anyway and Garrett put the water within reach without comment. There had been years when Rei mistook being fed for another debt. Here the cost was on a menu; the company had gradually become something neither of them charged for. He let the plate occupy his attention for a while.')],
    'RD06': [n('He wanted to ask whether she thought he had protected her. The question would make her responsible for giving him an answer he could live with, so he left it unasked. She was allowed to have been frightened, to have loved him, to have needed things he had not known how to give. He listened without trying to rearrange those facts into a verdict.')],
    'RD07': [n('He realised he had been looking at the door whenever the building made a sound. Emily noticed too; her hands slowed over the model. He could feel the question she chose not to press. Her awakening had not made her less herself: she still cared exactly how two small pieces fitted, still disliked someone taking over because they could do it faster. Protecting that person ought to include leaving room for her preferences.')],
    'RD08': [n('There was a particular relief in sitting near someone who expected him to have an opinion about a dumpling. He had begun to lose that scale. A call unanswered for twenty minutes could occupy more of his mind than the meal in front of him. Garrett’s ordinary annoyance about a leaking container did not solve anything. It reminded Rei that ordinary problems still existed.')],
    'RD09': [n('Back at his own table, Rei thought of a different school afternoon: Marcus returning the borrowed eraser in a paper envelope labelled temporary custody concluded. It had been absurdly formal for a grubby rectangle of rubber. Rei had kept the envelope because someone had taken the trouble to make him laugh without needing him to perform first. He missed the next ridiculous thing Marcus would have wanted him to take seriously.')],
    'RD10': [n('For a moment they disagreed about which part of the film had been Marcus’s idea. The disagreement felt almost precious. He had existed in each of their lives separately; Rei could not hold every version of him by remembering harder. Emily’s recollection made him smile. Sophie corrected a detail and kept it corrected. Neither asked grief’s permission to remember him as occasionally infuriating.')],
    'RD12': [n('Sophie had to call his name twice at a crossing. He had been watching a dark vehicle turn into the next street and had not heard her first time. He apologised. She waited for him to actually look at her before continuing. The walk had no destination, but it still required him to be present for the person beside him.')],
    'RD13': [n('At home that day, he had hidden the suspension paper beneath a schoolbook before Yuriko could see it. The concealment frightened him more afterward than the letter. He had wanted to be her safe person and had come home rehearsing excuses for hurting someone. The anger was his; the training had given it a fluent language. Adult Rei could remember both without calling either an acquittal.')],
    'RD14': [n('Garrett did not fill the pause. Rei almost used it to say he was fine. The answer was so familiar it had become a reflex, like moving a hand to cover an old scar. He let the silence last long enough to miss his chance. For once, someone else remained in the room without being asked to believe that he had everything under control.')],
    'RD18': [n('Rei caught himself trying to solve a crooked piece before Yuriko had decided whether she liked it that way. He drew his hand back. She was building a set, not asking him to prevent every possible collapse. The distinction should have been easy. His head was full of people he could not reach, and here was one small thing he could fix if he stopped listening.')],
    'RD19': [n('Daichi’s offer did not land as an honour. Rei heard an adult telling him what his strength could be used for, and the old pressure rose so quickly that he had to look away. This man had not given those orders. That did not prevent the likeness from making him sick. Ren waited with the departure records still open. The evidence required Rei to see a difference he did not yet know how to feel.')],
    'RD21': [n('Rei had been waking at every notification. Sometimes there was nothing on the screen; his hand had reached for the phone before he was fully awake. He did not want the person beside him to start organising their day around preventing that feeling. He also did not know how to ask them to stay without making their departure feel like a failure. The conversation had room for that difficulty, even when he could not name it neatly.')],
    'RD22': [n('The question followed him after the conversation: who would he be if there was nobody left to rescue tonight? He disliked it. He had once had an answer involving a sketchbook, a badly lit kitchen and time to waste. Lately he could not imagine wasting time without immediately seeing someone pay for it. That was not the same as having a purpose, however much it felt like one.')],
    'RD23': [n('Accepting did not quiet the boy who associated this name with pain. Rei could feel him in the impulse to turn a request into an order, to make every uncertain thing stand still. He would have to be accountable when that impulse appeared. Emi and Ren were colleagues with the right to disagree, not people whose obedience could prove he had become different.')],
    'RD24': [n('He had expected leaving to feel larger. The street looked the same. A delivery driver wanted the pavement clear. Rei stepped aside and found that he could do that without giving the house any more of his life. The feeling in his chest came with him. Distance was something he could choose; relief would not necessarily arrive on command.')],
    'RD25': [n('He would not call the people who defended the successor his childhood captors. Their adult choices and their right to resent his decision remained real. Destroying the organisation could remove the sign and its operations. It could not turn every fear he carried into evidence that he had been right to do it.', when={'phase':'before'})],
    'RD26': [n('One decision was finished. His hands did not receive the news immediately. He kept finding them clenched while he stood still, as though they were waiting for the next obstruction. He opened them against his coat and felt the seam with each fingertip. Nothing about a resolved choice made the rest of the day simple.')],
    'RD27': [n('His friends’ concern had become harder to wave away. The little pauses were accumulating: forgetting which question he was answering, arriving exhausted, looking past a familiar face toward the nearest door. He hated being watched for signs that he might come apart. He hated more that he had given them reason to watch.'), n('He could hear how often protection had begun to sound like an instruction when it came out of his mouth. Go home. Don’t come here. Answer me. It was not the life he wanted to offer anyone. He wanted them safe and free, and fear kept telling him he could have only one.')],
    'RD28': [n('Rei could picture returning here afterward. That made leaving harder, which surprised him. He had spent so long using attachment as a reason to move toward danger that he had forgotten it might also give him a reason to come back. Garrett would still be irritated if he vanished without a word. The thought mattered because it belonged to tomorrow.')],
    'RD31': [n('Rei waited for the relief he had promised himself at the loading door. His breath still caught. Jun and Luis were among the surviving detainees: dazed, frightened, alive. When Jun recoiled from a sudden movement, Rei stopped approaching and let him choose the distance. Knowing someone from a ring did not give him the right to decide what that person needed now.', when={'phase':'after'}), n('He had opened containment and secured the records. He could help people reach the exit and appropriate care. He could not promise their bodies would forget the rooms. He knew exactly how empty such a promise could be.', when={'phase':'after'}), n('The urge to hit Joseph again returned after the apology. Rei stepped away from him instead, not because the urge was noble or because it had vanished, but because another blow would delay the living people waiting for help. Marcus did not become the price of this victory. Emily did not owe him gratitude for a threat he had feared on her behalf.', when={'phase':'after'}), n('The failed attempt left his anger without the ending it had demanded. Retreat meant the programme was still unresolved. Resting, getting care and returning prepared would be harder for him than calling exhaustion courage. It was also the only way to make another attempt possible.', when={'phase':'failure'})],
    'RD32': [n('He did not have an account of the operation that made him sound composed. He could have edited it into one. Instead he let the pauses remain, and let the person beside him see how much of his strength had gone into getting through the door at all. Coming back was not the same as being well. It was the necessary beginning of letting anyone help.')],
    'RD33': [n('The investigation journal had served its purpose: dates, sources, names kept out of careless circulation. He did not need to manufacture another entry to justify putting it away. On a separate page he wrote an ordinary task for himself: arrange support for the sleep he had been losing and the fear he kept disguising as responsibility. Then he left space for an actual appointment, not a promise that he would handle it alone.'), n('He still wanted to protect people. He wanted to make dinner and draw and disagree about a film ending too. The weapon the clan had raised did not vanish when he chose those things. It ceased, for one evening, to be the only account of what his hands were for.')],
    'RD34': [n('He stayed after the meal without inventing a reason to be useful. The bowls could wait a little. Garrett did not need a rescue, and Rei did not need to earn the chair by providing one. It felt unfamiliar enough that he almost stood anyway. He kept sitting.')],
    'RD35': [n('When he noticed himself checking the door, he returned his attention to the unfinished piece on the table. The people he loved were not proof that he had succeeded at keeping the world harmless. They were people, with evenings and preferences that belonged to them. He listened to the next small disagreement and let it matter on its own scale.')],
}


def install(library):
    for key, elements in REPLACE.items():
        if key not in library:
            title, chapter = {
                'RD36': ('A window of her own', 'Chapter 1 — Two pages on the table'),
                'RD37': ('The last instruction', 'Chapter 2 — What the paper remembers'),
                'RD38': ('After she sleeps', 'Chapter 2 — What the paper remembers'),
            }[key]
            library[key] = dict(title=title, chapter=chapter)
        library[key]['source'] = 'rei_campaign_expansion.py'
        library[key]['elements'] = copy.deepcopy(elements)
    for key, elements in APPEND.items():
        library[key]['elements'].extend(copy.deepcopy(elements))
    # Reviewed voice corrections, scoped to Emily's existing authored lines.
    corrections = {
        'RD07': [('I was hoping you would answer that part.', 'I-I was hoping you would answer that part.'),
                 ("Do you want to tell me how you've been?", "Do you… do you want to tell me how you've been?"),
                 ('I asked you here because I wanted your opinion.', 'I-I asked you here because I wanted your opinion.')],
        'RD10': [("I don't mean that badly.", "I-I don't mean that badly."),
                 ('I liked listening to him explain things.', 'I… I liked listening to him explain things.')],
        'RD21': [('Do you want my answer,', 'D-Do you want my answer,'),
                 ('I wish I could make it easier.', 'I-I wish I could make it easier.'),
                 ('I would still want to understand why,', 'I… I would still want to understand why,')],
        'RD27': [('Do you want us to ask you not to go?', 'D-Do you want us to ask you not to go?'),
                 ("I'd like to see you afterward.", "I-I'd like to see you afterward.")],
        'RD35': [('“Why?”', '“W-Why?”')],
    }
    for key, replacements in corrections.items():
        for old,new in replacements:
            matches=[e for e in library[key]['elements'] if old in e['text']]
            if len(matches)!=1:raise ValueError('Emily voice anchor changed: '+key+' / '+old)
            matches[0]['text']=matches[0]['text'].replace(old,new)
    return library


def pre_mission(cast, share):
    """Only actual attendees speak; private visits never disclose the operation."""
    lines = [n('Rei had checked his phone twice without unlocking it. He put it face down and found that he wanted it back in his hand immediately. There had been too many nights of listening for a door, too many mornings in which he said he was tired as though that explained the rest.')]
    if 'emily' in cast:
        lines += [n('Emily waited until he looked up.'),
                  d('emily', 'I-I’m going to ask you something. Please don’t say you’re fine before I finish.'),
                  d('rei', 'I wasn’t going to.'),
                  d('emily', 'You already look like you’re practising it.'),
                  n('He nearly smiled. She had left him the opening deliberately; when he failed to take it, her hands became very still.'),
                  d('emily', 'You’re not sleeping. You keep checking whether I’ve got home when I haven’t even left work yet. I’m worried about you.'),
                  d('rei', 'I know you can look after yourself.'),
                  d('emily', 'Then let that change what you ask of me. A little.')]
    if share:
        lines += [d('rei', 'People I know from the Iron Circle are missing. The records point to Blackstone keeping Awakened participants after they tried to leave. I can’t stop thinking about what happens if I’m late.'),
                  n('He kept their identifying details out of the conversation. Saying what was happening was difficult enough without turning frightened people into the evidence for his own distress.')]
        if 'emily' in cast:
            lines += [d('rei', 'You’re Awakened too. I keep seeing him take you somewhere I can’t get to.'),
                      d('emily', 'Has someone threatened me?'),
                      d('rei', 'No. There’s no record naming you. It’s what he’s doing to people like you.'),
                      d('emily', 'Then t-tell me what you know, and tell me when you’re afraid. Don’t make one sound like the other.'),
                      n('He looked away. She had made the distinction he was trying to keep in the notebook, and he wanted to resent her for saying it aloud. She had a right to make decisions about her own life. He had a right to be frightened. Neither gave him ownership of the other.')]
    else:
        lines += [d('rei', 'I can’t tell you the whole thing tonight. I am frightened. I keep trying to make that useful.'),
                  n('He kept the investigation private. Admitting the feeling did not give away anybody else’s account.')]
    if 'sophie' in cast:
        lines += [n('Sophie leaned forward, her usual restlessness held very still.'),
                  d('sophie', 'You don’t have to make it useful every second. You do have to stop snapping at people who ask if you’ve eaten.'),
                  d('rei', 'That was unfair.'),
                  d('sophie', 'Yes. Apology accepted. Now answer the question.'),
                  n('He had to think before he could say when he last ate. Sophie’s expression changed at the hesitation. She did not congratulate him for being honest; she moved something within reach and waited.'),
                  d('sophie', 'I remember having to stand in your way at school. I’m not interested in doing that again because you’ve decided fear means you have to run straight at somebody.'),
                  d('rei', 'This time there are people I can still reach.'),
                  d('sophie', 'Then stay alive long enough to reach them. Being furious doesn’t make you disposable.')]
    if 'emily' in cast:
        lines += [d('emily', 'You helped me. You don’t have to keep proving it by getting hurt.'),
                  d('rei', 'I couldn’t help Marcus.'),
                  d('emily', 'You were his friend. I miss him too. I-I’m not going to make your whole life a test you failed that morning.'),
                  n('Her voice caught, but the sentence stayed firm. Rei had expected comfort to feel softer. This asked him to put down something he had mistaken for love.'),
                  d('rei', 'I don’t know how to stop.'),
                  d('emily', 'Then we start with this minute. Sit with me for this one.')]
    lines += [n('He sat. It did not settle everything. He could feel the pressure to get up, get there, make the danger end before another call went unanswered. He stayed long enough to drink, and to admit that he needed someone to know he was struggling.'),
              d('rei', 'I’ll let you know when I can. I’m going alone.'),
              n('The people here did not become companions in the operation. Their concern remained a request to come back, and a boundary against making their safety an excuse to destroy himself. The fear did not cease because somebody loved him. He would have to carry this effort beyond this room.')]
    return lines
