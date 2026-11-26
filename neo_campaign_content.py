"""Neo's authored visual-novel scenes. Progress and outcomes belong to neo_campaigns.

Keep pre-encounter scenes separate from earned aftermath. Interior narration is
Neo's private viewpoint, never an automatic disclosure to the on-screen cast.
"""
from copy import deepcopy


def b(who=None, text='', narration=''):
    return dict(player='', speeches=[[who, text]] if who else [], narration=narration)


def p(text):
    return b(narration=text)


def scene(title, room, briefing, aftermath):
    return dict(title=title, room=room, briefing=briefing, aftermath=aftermath)


CHAPTERS = {
    'NE01': scene('Two mugs', 'neo_mariko__kitchen', [
        p("By closing time the makerspace smelled of warm dust and solder. Neo returned a repaired radio to its owner, wrote a new fault beside the controller he had failed to fix, and washed his hands twice. There were days when the simple order of that felt extraordinary: somebody brought him a broken thing, he tried to help, and at six he was allowed to leave."),
        p("At the apartment, Alyssa had spread an album beneath the lamp. Two mismatched mugs stood beyond the reach of the paste. He stopped with the controller in his hand, waiting for her to finish drawing a thread through the binding. The rice cooker clicked behind him."),
        b('neo', "Can I move the sketches?"),
        b('alyssa', "The ones marked plants, or the ones you keep insisting are a repair log?"),
        b('neo', "The plants have a very complicated wiring diagram."),
        p("She smiled without lifting her eyes. He liked being able to wait beside her. Nothing needed defending in this room; the silence did not mean someone was deciding what to do to him. He put the controller down and started clearing their place at the table."),
        b('alyssa', "Leave that until tomorrow. I want my turn at it."),
        b('neo', "It still drifts left."),
        b('alyssa', "So do you when I ask you to chop onions."),
        p("Her album belonged to a customer from Alfheim. A corner of one photograph had torn away, and Alyssa was making a support for what remained. She showed him where the new paper would sit. He listened; later, she listened while he explained why the controller had defeated him. Neither problem needed to be the more important one."),
        p("When they left for Mariko's house, he checked the apartment door once, then made himself walk away. A future had begun to take shape in small, almost embarrassing wishes: another shelf, a cat someday, enough ordinary evenings to stop counting them. He wanted it fiercely. He had never quite learned to want something without also imagining its loss."),
        b('mariko', "You're early. Good. The radio has developed opinions about the news."),
        p("Her kitchen was brighter than theirs. Choir music lay under a shopping list; a cardigan hung from the chair she always told him not to put his jacket on. She moved it before he could mention the inconsistency."),
        b('neo', "I wasn't going to say anything."),
        b('mariko', "Your face was preparing a statement."),
        b('alyssa', "It was a very thorough statement."),
        p("Mariko tapped the radio. It swallowed the same syllable every minute. Neo knew the probable fault, but first he asked whether she wanted him to look. Years ago she had had to teach him that being wanted in her kitchen and being useful in it were different things. Sometimes she still had to remind him."),
        b('mariko', "Dinner or the radio. I leave for choir at seven. You cannot finish everything before I go."),
        b('neo', "The radio has never complained about my cooking."),
        b('mariko', "Excellent manners. It gets those from me."),
        p("She pointed out the fundraiser books. Tyler's father was coming on Thursday to help untangle them; they had arranged an accessible car. Mariko sounded more concerned about the treasurer's arithmetic than any inconvenience. She had people to see, a part to rehearse, and an argument about expenses she fully intended to win."),
        p("April's request reached him while Mariko looked for the good serving spoon. A private meeting. A suspicious transport. Could he listen? His thumb stayed over the message. The terms were harmless by themselves. Put together, they made the kitchen feel briefly far away."),
        b('alyssa', "You don't have to answer this minute."),
        b('neo', "I know. I'd like to finish being here first."),
        p("He set the phone face down. Static cracked through the radio, and his hand paused beside the dial. For a moment he was twelve again, looking at this same pool of kitchen light and wondering what it would cost to stay.")
    ], [
        p("Mariko gathered her music, discovered the shopping list among the pages, and accused the household of sabotage. Neo held out her cardigan. The ordinary fuss of leaving filled the hall."),
        b('mariko', "Lock up if you leave after me. And don't take that thing apart unless you're prepared to label the screws."),
        b('neo', "You don't trust my system?"),
        b('mariko', "I have vacuumed your system."),
        p("He laughed. Afterwards he would have other things to remember about this house. This evening happened too: his mother complaining, Alyssa hiding a smile, the kitchen still warm when he turned out the light.")
    ]),
    'NE02': scene('Old friends, new debts', 'neo_club__back_room', [
        p("Before Tyler's bout, Neo waited in the club back room with a paper cup slowly softening between his hands. Beyond the wall a crowd shouted for the sort of contact he preferred to keep inside controlled drills. Tyler was taking a paid fight, not asking Neo to return to anything. Neo repeated the distinction until it almost settled."),
        b('tyler', "Saved it. Sit down."),
        p("Tyler lifted his bag from the chair. It was such an old gesture that Neo moved before thinking. At school he had spent weeks standing at the edge of rooms, leaving everyone the easy option of not making space for him. Tyler had been infuriatingly casual about ruining that arrangement."),
        b('daniel', "Film plans later. I'm paying attention to this bout first."),
        b('neo', "That bad?"),
        b('daniel', "The film? Catastrophic. I'm going to make you watch it anyway."),
        p("The sounds beyond the wall faded beneath another room: the squeak of trainers, a gym bench, Tyler's bag shifting out of the way.")
    ], [
        p("Outside the club, Tyler flexed his hand and checked the time. The purse was settled; leaving with it had cost more than it should. Neo could still feel how readily his body had found the distance between the two house fighters. It had been easy to know where to stand. That was what troubled him."),
        b('tyler', "Thanks. Dad's going to ask why I'm late."),
        b('neo', "Tell him the arithmetic took a while."),
        b('daniel', "Technically accurate. Terrible review of the evening."),
        p("April waited in the quieter part of the back room with Garrett. She laid out transport sightings and a witness account. No secret file, no assertion that she understood him. Just enough evidence to make the request difficult to dismiss."),
        b('april', "People are being pressured into going with them. We have a route and someone willing to speak. We could use your help."),
        b('neo', "No."),
        p("It came out harder than he meant. Garrett's gaze moved from the papers to him. Neo put his cup down before he crushed the rim."),
        b('neo', "Sorry. I can listen. I'm not joining an operation."),
        b('garrett', "Nobody's handing you a uniform."),
        b('neo', "That's not the part that worries me."),
        p("He could already see how it would happen: one evening, one favour, one person who needed what he could do. Then every useful skill would point him back towards locked rooms and men who used people up. His father had built a whole world out of the claim that Neo belonged wherever his violence was valuable. He hated how easy it was to hear that claim inside an innocent request."),
        b('neo', "I've got work tomorrow. Dinner with Alyssa. It sounds small when I say it here. It isn't small to me."),
        b('april', "It doesn't sound small."),
        b('neo', "I spent years getting out. I don't want to get good at being back."),
        p("Tyler stopped worrying at the tape around his wrist. Daniel looked away from the papers. They knew enough of the home Neo had escaped to let the silence stand; he had not given them the programme or his father's name."),
        b('april', "Then no is the answer. Is there a detail you want us to have, or would you rather leave it there?"),
        b('neo', "The loading gate you marked has a broken latch. Don't put a witness on that side. That's all I can offer."),
        b('garrett', "All right. We'll work with that."),
        p("Leaving brought relief, then shame at feeling relieved. Neither proved he had chosen badly. Elsewhere, a retrieval order already bore the designation Number One. It had been issued without asking whether he was helping April. His refusal changed nothing on that page.")
    ]),
    'NE03': scene('Alfheim', 'neo_alfheim__square', [
        p("Alfheim had first entered Neo's life as a damaged album on their dining table. Now Alyssa recognised the shop beside the community room, and someone called to ask how the binding was going. She answered with an apology for the delay. For a few seconds it was an ordinary visit."),
        p("Then Soren put the pouch on the counter. Loose notes slid out beside a folded dispatch slip. He wore his defiance as if he had dressed carefully for the occasion; it did not quite cover the fear underneath."),
        b('soren', "It was their money. The crew took it. I took it back."),
        b('alyssa', "And the people they took?"),
        b('soren', "I was trying to do something."),
        b('alyssa', "I know. I'm asking what happened after."),
        p("Her voice softened at the edges without becoming less direct. Neo stayed beside her and let her speak to her brother. He could not solve their disagreement by stepping in, any more than he could make the pouch harmless by understanding why Soren had stolen it."),
        b('soren', "I didn't know there was a slip. I didn't think they'd come this quickly."),
        p("A shutter slammed at the far end of the square. Another followed. Hachimura's retaliation was already moving through the street. A man carrying a box abandoned it to help his neighbour; somebody called a name and received no answer. Neo felt the old cold calculation arrive before the fear: entrances, sightlines, distances."),
        p("He hated the relief that came with knowing what to do. At the bench a failed repair could occupy him for hours. Here his hands seemed to understand at once. That did not make this his home. He held on to the thought while he found the side passage."),
        b('neo', "This way. Walking pace. There's room."),
        b('alyssa', "I can cover this sightline if I stay here. Only this one. Tell me before you move."),
        b('neo', "I will."),
        p("Her shadow work blurred the near approach. Beyond its reach the square remained exposed. He wanted to tell her to get behind him. Instead he looked where she was looking, saw the people she was bringing through, and took the position she needed him to hold."),
        b('april', "Emergency response is on the line. Keep the passage open. Soren, help at the far end."),
        b('soren', "I'm going."),
        p("Neo planted his feet. He had said no to the operation. He had not said no to the person stumbling towards him with another person's weight on her shoulder.")
    ], [
        p("Once the passage was clear, the damage became strangely audible: a shutter knocking in its frame, glass under a careful shoe, Soren dragging a chair out of the way. The residents taken from the square were alive, but they were gone. Their families had to say the names into the space they had left."),
        b('alyssa', "Start again. Slowly. I want to spell it the way she spells it."),
        p("She wrote a first-hand list, checking each account. Neo brought water and waited until her pencil stopped."),
        b('neo', "Your hand's shaking."),
        b('alyssa', "So is yours."),
        p("They looked down together. He had managed not to notice. She touched the back of his hand only after he turned it towards her."),
        b('alyssa', "I need to find them. I'm frightened, and I still need to."),
        b('neo', "I'll help get the names straight."),
        p("It was something he could do without promising an entire future. He read the list back. At the edge of the square a surveillance team watched him leave. Their later trail came from following a living person through the city, not from a magical address hidden in Soren's stolen pouch.")
    ]),
    'NE04': scene('The house on the quiet street', 'neo_mariko__hall', [
        b('mariko', "I am not asking for every detail. I'm asking who we call if the danger reaches this door."),
        b('neo', "April. Use the phrase we agreed. Then the side door. Don't wait for me to come and get you."),
        p("Tyler's father had spread the fundraiser books across the table. His chair stood clear of the route to the accessible car. Mariko had moved the hall rug because its edge curled, then complained that everyone was looking at her instead of the very obvious tripping hazard."),
        p("Neo checked the side passage again. He wanted to send them away and wanted, just as badly, to sit down and hear them argue over receipts. Mariko caught him looking at the table."),
        b('mariko', "I heard you the first time. So did he. Come here a moment."),
        b('neo', "Mum—"),
        b('mariko', "A moment. You haven't eaten."),
        p("The word had come easily. Mum. It had taken years to stop feeling as though he were asking for something when he said it. She put a plate within reach, and he was opening his mouth to complain about the portion when the sound came from the front."),
        b('hachimura', "You've had enough time playing house."),
        p("Hachimura filled the entrance with the certainty of someone who thought a doorway was his as soon as he stood in it. Behind him the squad spread out. Neo stepped between the hall and the people at the table."),
        b('neo', "You want me. They're leaving."),
        b('hachimura', "You don't set the terms."),
        p("Mariko sent the warning. He heard the clipped phrase they had agreed, then the movement of Tyler's father's chair towards the side passage. She did not waste breath arguing with Hachimura. Her hand found the chair handle; her eyes found Neo's."),
        b('mariko', "The side door. I've got him."),
        p("Neo would remember the plate left near the table's edge. The radio still on in the kitchen. The unbearable fact that the house had continued being a house while Hachimura crossed it. His mother's life did not become smaller because the moment that ended it was brief."),
        p("Hachimura killed Mariko before Garrett forced the opening. Neo moved towards her without deciding to. The hall narrowed to the place where she had fallen; everything in him insisted that if he could reach her, the next second might be different."),
        b('garrett', "Neo. Look at me. The exit. I've got this side."),
        p("Tyler's father was still in the passage. Still breathing. Still needed someone between him and the squad. Neo could not make himself understand that his mother was gone, but he could understand where to put his body."),
        b('neo', "Get him through."),
        p("The three words scraped his throat. He turned back towards Hachimura, not for a duel, but to keep the narrow exit open long enough for a living man to leave.")
    ], [
        p("Outside, the receiving team took Tyler's father alive. The chair's wheels caught on a seam in the pavement and Neo bent to lift them, though there were already hands there. Garrett had to say his name twice before he let go."),
        b('garrett', "They have him. You can stop."),
        b('neo', "She's inside."),
        p("Nobody mistook who he meant. Nobody told him she would be all right. The absence of that lie was the first thing that made the loss real."),
        p("His hand went to his phone. He used to call Mariko after a bad day because she would ask whether he had eaten before asking what had happened. He stared at her name until the screen dimmed."),
        b('neo', "I need to tell her—"),
        p("There was no end to the sentence. Hachimura was still somewhere beyond the line Garrett was holding, alive in the same world in which Mariko was not. Neo's anger had no words yet. It was a direction his whole body wanted to take."),
        b('garrett', "Stay here with me."),
        p("He stayed. It did not feel like courage. The people treating Tyler's father kept speaking, asking practical questions, making room for the next person who needed help. Neo stood among them with his mother's name dark in his hand.")
    ]),
    'NE05': scene('The day after', 'neo_refuge__sitting', [
        p("The first day had been treatment and calls. On the next, Neo discovered that grief could survive a kettle boiling, a person asking for a signature, even an hour in which he had forgotten to think about it. The forgetting frightened him most. It felt like leaving her somewhere a second time."),
        p("Mariko's choir programme lay beside the practical papers. He kept turning it face down and turning it back. Nothing on it knew she would not be at the next rehearsal."),
        b('tyler-father', "Someone needs to tell the club treasurer those receipts are wrong. I'd prefer to be that someone."),
        b('tyler', "I'll bring the books."),
        b('tyler-father', "Bring my glasses as well. Everyone keeps handing me things and then looking sorry when I can't read them."),
        p("Neo almost smiled. Then he remembered who should have answered him, and the effort hurt. Tyler sat beside his father, carefully leaving the way clear for the medical staff."),
        b('neo', "He was there because of us. Both of them were."),
        b('tyler', "Dad was there to help with the books. You didn't invite the men who hurt him."),
        p("Neo knew the distinction. His mind kept erasing it. He could picture every visit to the house, each turn on the way there, every ordinary act that surveillance had made into a trail. Hachimura had done the killing. Neo still wanted a moment he could go back and punish himself into changing."),
        p("Later Alyssa sat with him while the others gathered the next day's arrangements. She had her own list, names from Alfheim written carefully enough for frightened relatives to read. She put it down rather than hide it."),
        b('alyssa', "I can stay tonight. Tomorrow I'm meeting the families."),
        b('neo', "You should go now if you need to."),
        b('alyssa', "I said tomorrow. Tonight I want to sit with you."),
        p("He watched her thumb catch on a rough edge of paper. A tiny familiar movement. He wanted to tell her that it was holding the room still for him. The admission felt larger than anything he knew how to say."),
        b('neo', "When you're here, I can find where I am."),
        b('alyssa', "Here is a terrible sofa. And tea I let go cold."),
        b('neo', "Still here."),
        p("She put her hand where he could take it. He did. She was not a replacement for the woman he had lost, and he did not need her to become one. He needed Alyssa: her impatience with a damaged page, her terrible co-op detours, the way she let a silence belong to both of them."),
        b('neo', "I don't want to go back into this."),
        b('alyssa', "I know."),
        b('neo', "I want him. Every time I close my eyes, I think about finding him. Then I think about going home with you, and I don't know how both can fit in my head."),
        b('alyssa', "They fit. That doesn't tell you what to do with them."),
        p("She did not turn his anger into a noble thing for him. He loved her for that, and resented for a moment how little comfort it offered. Then he told her the uglier truth."),
        b('neo', "I'm afraid I'll go after him and stop caring what it costs."),
        b('alyssa', "Then tell us when that's happening. Don't disappear and make us guess."),
        p("When the crew returned, Neo left the programme beside his chair. There were people still confined, an existing order to take him alive, and a man who had walked through his mother's door as though her life were an obstacle. Staying out had been a real choice. After the attack, pretending the threat would respect that choice was something else."),
        b('neo', "The team wants me alive. Hachimura takes orders from someone above him. That's what you need to know to plan safely."),
        b('april', "And what are you agreeing to?"),
        b('neo', "Getting the people out. Stopping this retrieval team. Finding Hachimura."),
        b('garrett', "You don't owe me for the exit."),
        b('neo', "Good. Because this isn't repayment."),
        p("He was not rejoining his father's organisation. He was agreeing to step back into the criminal world it occupied, with people whose conditions he could question and a home he intended to return to. The difference mattered. It would not make the work clean."),
        b('neo', "If I start chasing him and leave someone exposed, stop me."),
        b('tyler', "We will."),
        b('daniel', "You won't enjoy the conversation."),
        b('neo', "I'm counting on that."),
        p("Before they went through the papers, his gaze settled again on the choir programme. He remembered another time Mariko had been frightened and wrong, and had stayed in the room long enough to admit it.")
    ], [
        p("Care and preparation took several days. Neo did not sleep himself into greater strength. He learned which movements pulled at a bruise, which questions he could answer once, and which he could not bear to hear again that morning."),
        p("Garrett brought the working notes. April crossed out a route that left the families exposed. Alyssa went to the meetings she had said she would attend and came back with more names. Each departure made Neo's chest tighten. Each return gave him something true to set against the fear."),
        b('neo', "I want there to be an end to this job."),
        b('april', "Then we keep the objective specific. People out. Orders secured. The field command stopped."),
        b('garrett', "And nobody buys your whole life with one favour."),
        p("Neo nodded. He could not yet imagine missing his mother without feeling that he was failing to do something. For now he could put one task beside another, eat when the food arrived, and let the people in the room remain people instead of possible losses.")
    ]),
    'NE06': scene('Two fronts', 'neo_refuge__sitting', [
        p("By the third morning Neo knew which chair in the refuge creaked and which tap needed an extra turn. He had started correcting small faults without noticing. An uneven table could be made level. The larger wrongness of the room stayed where it was."),
        p("Garrett had gone to a warehouse linked by the dispatch slip and a witnessed collection route. The successor clan used different signs from the old Hamayashi-kai; the people being pushed into its vehicles were no less real. April kept the copied evidence on the table, each piece beside the account that explained where it came from."),
        b('daniel', "You don't have to fix the chair as well."),
        b('neo', "It rocks."),
        b('daniel', "It's a chair. None of us have found that especially threatening."),
        p("Neo stopped with his fingers around the short leg. Daniel was not smiling much. He moved a folded scrap of card across the table instead, and Neo took it. Help could be that small; he did not have to refuse it on principle."),
        b('april', "That courier vehicle has passed twice. Same damage above the rear wheel."),
        p("Her voice changed the room. She checked the window from its edge, then moved the noncombatants towards the rear access. Neo felt the familiar urge to hold the front alone. His bruises answered before anyone else did."),
        b('neo', "How long do you need?"),
        b('april', "Enough to leave. We aren't defending the furniture."),
        b('daniel', "I can take the next corner."),
        b('neo', "With Tyler. Not ahead of him."),
        p("The retrieval squad came in while the last chair was still warm. Neo saw Mariko's hall for a heartbeat, so clearly that he almost chose the wrong door. Tyler called the rear route. Neo made himself look at the room in front of him."),
        b('tyler', "This one. We're here."),
        p("He went with them. Leaving an empty room standing felt like failure only if he let Hachimura decide what had to be held.")
    ], [
        p("They reached the rear access together. Neo counted heads, lost the count, began again. April let him finish before telling him she had already checked. He was grateful she had not said it sooner."),
        b('neo', "I saw the other house for a second."),
        b('tyler', "You came through this one."),
        p("VIEWPOINT INTERLUDE — At the warehouse, Garrett cleared the bounded room connected to the pickup lead. Among the transport papers he found a note naming a Blackhaven contact and a collection point. He copied the note rather than turn a warehouse full of unrelated business into an explanation for everything."),
        p("Later April put that copy into Neo's hands. He read it twice. He had not been there; he asked Garrett which part he had seen himself."),
        b('garrett', "The note, the room, the contact's name. The next step still needs checking."),
        b('alyssa', "The families saw the van leave towards the same yard. I've kept their accounts separate. They don't all remember the same things."),
        b('neo', "You got back."),
        b('alyssa', "I said I would call if the meeting changed."),
        p("He wanted to apologise for the relief in his voice. Instead he moved a chair clear for her. The crew had a lead they could follow and witnesses whose lives were larger than the information they supplied. Alyssa spread the names beside the copied note. Neo read those first.")
    ]),
    'NE07': scene('Blackhaven', 'neo_yard__loading', [
        p("Before they left, Daniel asked Garrett for a proper spar. Neo watched from the wall, recognising the careful casualness of the request. Daniel wanted a challenge he had chosen. Garrett gave him one, then kept talking after the point had already landed."),
        b('garrett', "That opening was bait. You practically thanked me for it."),
        b('daniel', "Tell me the fault. Not what sort of person it makes me."),
        p("Garrett lowered his hands. For once the quick answer did not come first."),
        b('garrett', "Fair. You follow the first opening past your cover. We work on the second step."),
        b('neo', "And stop before the lecture gets a sequel."),
        p("Daniel's smile was brief but real. They worked the movement again. Nothing about his War God had disappeared; he was learning when not to commit the body it gave him. Neo understood the difficulty more than he wanted to say."),
        p("At Blackhaven the contact handed over the pickup location before anyone recognised them. Neo checked it against the warehouse note. A loading door, a stationary stop, a narrow interval. Concrete facts made a person tempting to reduce to a plan. He thought of Alyssa's list and read the place again."),
        b('tyler', "That's him."),
        p("The retrieval leader from Mariko's house crossed the yard. Tyler moved after him. Neo heard his friend's breathing change and knew, with shameful immediacy, exactly what that forward step promised: no more waiting, no more helpless rooms, one person close enough to hurt."),
        b('neo', "Tyler. Keep the door."),
        p("Daniel crossed too far to cover him. The lieutenant took the gap and knocked him out of the line. Neo saw Daniel regain his feet, furious and embarrassed. There was no time to make either feeling useful."),
        b('neo', "Back to the loading door. Together."),
        b('tyler', "He's right there."),
        b('neo', "So is Daniel."),
        p("Tyler looked back. Neo had no moral distance from the mistake he was asking his friend to correct. He wanted Hachimura with the same sickening certainty. For the moment he could still choose the person beside him over the man running away.")
    ], [
        p("They came out through the yard's finite chain of cover, lane and loading apron. Once the pursuit broke, Daniel sat on a low concrete edge and pressed a hand to the place the lieutenant had hit. Tyler stood nearby with his anger suddenly unable to find anywhere to go."),
        b('tyler', "I left the line. You covered me."),
        b('daniel', "Badly. We can both have been wrong."),
        b('neo', "I knew why you went."),
        b('tyler', "That doesn't help much."),
        b('neo', "No."),
        p("He sat beside Daniel instead of trying to improve the answer. Eventually Tyler sat too. The silence was different from school, but it still had room for three."),
        p("Their report reached Fox through the regional response channel. A report was not permission for every next step, and Fox was not a spare pair of hands they could summon out of danger. The pickup location remained the useful thing they had actually obtained."),
        b('daniel', "Second step. Next time I leave myself one."),
        b('neo', "I'll be there to complain if you don't."),
        p("Daniel nodded. Neo sent Alyssa the verified location and a plain account of their condition. He deleted the first version, which had said only that they were fine.")
    ]),
    'NE08': scene('The people on the list', 'neo_transport__boarding', [
        p("At the stationary loading stop, Alyssa folded the list along a crease it had already acquired from being carried everywhere. Neo knew several names now. He knew which family had corrected a spelling and which had asked the same question twice because neither answer had been enough."),
        b('alyssa', "The vehicle stops before anyone boards. I check who's here, and then who isn't."),
        b('april', "Garrett contains the escort. Tyler and Daniel keep the return lane open. Medical transport waits beyond it."),
        p("The closed compartment was quiet. Neo found that worse than shouting. For years he had been grateful for any door he could close from the inside. Here the lock faced him. He made himself look away from it long enough to check the lane."),
        b('neo', "I'll take the door. Tell me when your side is ready."),
        b('alyssa', "Look at me first."),
        p("He did. Her expression was worried, concentrated, impatient with having to repeat herself. Familiar enough to bring the present back into focus."),
        b('alyssa', "I'm asking about the lane. Are you looking at it?"),
        b('neo', "Yes. Sorry. Yes, I am."),
        p("She nodded once. An anchor, he thought, and almost disliked the word for how passive it made her sound. Alyssa was doing her own work, frightened for her own people. What steadied him was the fact that she expected him to be here doing his, beside her."),
        b('tyler', "Return lane's ours."),
        b('daniel', "And we're keeping it."),
        p("Neo checked the stopped vehicle and the route to the receiving team. Opening a door would be a beginning. He wanted, fiercely, to be there for everything that had to happen after.")
    ], [
        p("The six passengers reached the receiving team alive. One kept looking back at the transport even after the medic had drawn a blanket around her shoulders. Neo stayed where she could see him until she chose to turn away."),
        b('alyssa', "Six here. Six received."),
        p("She said it a second time, more quietly. Neo watched her cross the last mark. His mind supplied another room, other children, an account that had ended in deaths instead of names answered aloud. He could not exchange one group for the other. These six people were not a way to make the old number come out right."),
        b('neo', "Who's still missing?"),
        b('alyssa', "The others are at the annex. The passengers' accounts match the transfer manifest."),
        p("He took the recovered pages. A commander photograph was clipped among the orders. There was something in the face he did not allow himself to examine in a place where people still needed the route kept clear. He set it aside with the manifest, meaning to look in private."),
        b('alyssa', "Neo?"),
        b('neo', "After they're settled. I'll look after."),
        p("She did not pull the photograph out of his hand. When the last passenger had been received, she leaned against the wall for a moment and closed her eyes. He brought her water. Neither of them called the work finished.")
    ]),
    'NE09': scene('Hold the line', 'neo_refuge__exit', [
        p("The courier had followed the hostile van from the loading stop. April spotted the trail before the punitive squad reached the temporary evacuation centre, but warning did not make the last group move faster. Someone needed help standing. Someone else would not leave without the person in the next room."),
        p("Hachimura appeared beyond the road. Neo recognised his posture before his face. The world seemed to offer him a clean, vicious arrangement: a gap, a distance he might close, the man who had killed his mother."),
        b('hachimura', "Still standing in doorways?"),
        p("He heard the radio in Mariko's kitchen. His hand tightened until the damaged skin pulled. Hachimura was close enough to stop being an idea. Neo wanted to make him afraid. He wanted one moment in which the man understood that there were things he could not simply walk through."),
        b('april', "The last group is inside. If you follow him, they lose this exit."),
        b('neo', "I can reach him."),
        b('april', "I know. The exit, Neo."),
        p("She did not tell him what his mother would have wanted. He would have hated her for presuming to know. She gave him the fact in front of him, and he had to make his own choice with it."),
        b('neo', "Then I stay."),
        p("He meant it and resented it. The anger did not leave when he turned his shoulder back towards the door. It came with him into the position he had agreed to hold."),
        p("Garrett took the accompanying force away from the road. Alyssa protected the other passage, still within the narrow reach of her concentration. Tyler held his assigned side. Daniel moved for the opening, stopped at cover, and returned."),
        b('daniel', "Second step. I'm here."),
        b('tyler', "So am I."),
        p("Neo heard them. Hachimura could see him too. Let him see this, then: three people keeping a door open, refusing to make the frightened people behind them pay for what they wanted.")
    ], [
        p("The centre emptied through a counted exit. The last person came through leaning on another pair of shoulders, alive and complaining about the cold. Neo had never been so grateful to hear a complaint."),
        b('april', "All received. You can move."),
        p("By then Hachimura's brief opening was gone. Neo stood looking at the space where it had been. Staying had saved the exit; it had not made him peaceful."),
        b('alyssa', "Come away from the door."),
        b('neo', "I wanted to follow him."),
        b('alyssa', "I saw."),
        b('neo', "I still do."),
        p("She nodded, tired enough that even that small movement seemed costly. He stepped aside so she could sit. There was a cup in his hand before he remembered picking it up."),
        b('neo', "We stop this at the annex. No more waiting for him to choose a house."),
        b('april', "We have the manifest and the witnesses. We can identify the rooms we need."),
        p("A place, an objective, a route out. Neo listened to each. He was beginning to understand that restraint might have to be done while furious, without the reward of feeling better afterwards.")
    ]),
    'NE10': scene('One and Thirteen', 'neo_refuge__sitting', [
        p("Alone with the recovered manifest, Neo finally turned the commander photograph towards the lamp. An adult face, hardened by years he had not seen. He looked past what had changed and found the boy who had once stood at the far end of a table, waiting to see whether there was room."),
        p("Thirteen. Not a rumour about a number, not a resemblance he could dismiss. The face held him still. He had carried guilt for leaving the boy behind without knowing he had lived. Now the years of not knowing had a shape, and that shape was looking out from the orders that had confined Alyssa's neighbours."),
        p("Relief came first. It was so sharp he almost laughed. Then he saw the command designation again and felt ashamed of being relieved. A living child had become a man other people needed rescuing from. Both facts stayed on the page."),
        b('neo', "You were there."),
        p("He said it to the photograph. There was no one in the room to answer. He wanted to ask where Thirteen had been, who had stood beside him, whether anyone had ever opened a door without wanting something in return. Questions filled the years where knowledge should have been. Neo could not answer them by remembering harder."),
        p("He thought of the other subjects. His mind did not preserve them evenly. A small gesture could remain painfully clear while a voice slipped beyond reach. He hated himself for the gaps, as though perfect recollection were another test he had failed. They had died. He had lived long enough to mislay details."),
        p("Being called Number One had taught him to be responsible for every result. The lesson survived the people who taught it. It whispered that if he had been as good as they said, he would have found another route, held another door, brought everyone out. He had been ten. He could know that and still feel the accusation."),
        p("Takeo had called it a programme. His father. Neo had spent years trying to keep those two words from occupying the same sentence. He hated Takeo for the children he had reduced to results; he hated him for the reflex that still made Neo measure his own grief as a failure of performance. No wish for a throne lived underneath it. He wanted his father to lose the right to decide what any of them were for."),
        p("Alyssa knocked. He put the photograph beside the manifest before telling her to come in. She saw his face, then the empty chair, and waited for him to choose."),
        b('neo', "Someone from before. I recognise him."),
        b('alyssa', "Do you want me to stay?"),
        b('neo', "When I come out. I need a minute first."),
        b('alyssa', "I'll be next door."),
        p("There was no injury in her voice. She did not need a complete account to believe the minute mattered. After she left, Neo drew the photograph closer and let the old room return: bowls against a table, supervised quiet, a boy trying to make himself smaller than his hunger.")
    ], [
        p("VIEWPOINT INTERLUDE — After Neo's escape, Thirteen survived further coercive training. The place left by Number One did not become freedom for the boy still inside. Achievement could remove one accusation and supply the terms of the next. He learned to offer results before anyone could ask whether he deserved to remain."),
        p("Years later, at the current command position, Thirteen refused relief and continued reviewing the response. Fatigue had begun to show in the time it took him to settle after a movement. He treated the delay as an error to suppress, not a reason to stop. None of this belonged to Neo's memory. Neo had only the photograph, the orders and the person he would meet."),
        p("Back in the refuge, Neo took his place beside the others. He laid the operational pages down and kept the childhood account to himself unless he chose a private listener."),
        b('neo', "The commander is still responsible for what's happening at the annex. We stop him. I want a medical route kept open as well."),
        b('april', "We can prepare that. It doesn't make the corridor safe by itself."),
        b('neo', "I know. He may not want anything I offer."),
        b('garrett', "Then don't make the plan depend on gratitude."),
        p("Neo nodded. Empathy was not evidence that Thirteen would surrender, and guilt was a dangerous reason to walk into his reach. He could care about the boy at the table without offering the people at the annex to the man he had become."),
        b('alyssa', "The people inside still come first."),
        b('neo', "Yes. Including the ones who won't thank us."),
        p("He did not forgive his father. He did not forgive himself on command. He asked April where the receiving team would stand and listened until he could picture the route.")
    ]),
    'NE11': scene('The outer rooms', 'neo_annex__entry', [
        p("The annex looked disappointingly ordinary from the approach. Neo had wanted some mark that made it impossible to mistake for a place where people went to work and returned home. Instead there were doors, a service route, a light left on. He knew better than to expect cruelty to announce itself in the architecture."),
        p("Reports, living witnesses and the recovered manifest had brought a bounded police and Interpol response to this site. Beyond the perimeter, medical staff waited for the people still inside. Neo checked the route to them, then checked it again without pretending the second look was tactical."),
        b('april', "Entry, records, medical corridor. Tyler has the retrieval leader's lane. Daniel has a return route from the lieutenant. Choose where you support first."),
        b('tyler', "I'm staying where we agreed."),
        b('daniel', "And I'm leaving myself a second step."),
        p("Neither said it as a boast. Neo preferred that. They had all seen what wanting a particular man could do to a formation. The correction had to survive the room, not merely sound convincing before it."),
        b('alyssa', "I can hold the reinforcement sightline from that corner. If I move, the cover goes. Don't plan around it lasting after I leave."),
        b('neo', "If you need to move, say so. We'll change with you."),
        p("He wanted one last quiet word with her and could not find one that did not sound like an ending. She seemed to hear the difficulty. She lifted her chin towards his hands."),
        b('alyssa', "You've checked the strap three times. It's fastened."),
        b('neo', "Four."),
        b('alyssa', "Then trust the first three."),
        p("He let go. In the entrance, a guard moved across the route to the inner rooms. Neo saw the opening, the cover, the way out. He also saw the door beyond which someone was waiting without any of that information. He wanted them to have a next room that was not another cell."),
        b('neo', "One room at a time. Nobody drops off the list."),
        p("April touched the service latch they had checked during preparation. Tyler and Daniel took their lanes. Neo entered with the others still in his awareness, resisting the old temptation to make the whole task depend on him.")
    ], [
        p("Four captives reached the medical corridor and were received alive. Neo watched the fourth handoff before letting himself look back towards the records room. The current retrieval orders were secured. For once a document that had been used to move people against their will would have to answer for where it had sent them."),
        p("Tyler held his lane through the retrieval leader's defeat. Daniel drew the lieutenant beyond his own cover, stopped, and won the returning exchange. April, briefly cut off, reached the records room through the checked service route. Alyssa held the nearby sightline until the last movement through it was complete."),
        b('daniel', "Second step."),
        b('tyler', "You mentioned."),
        b('daniel', "I'm going to mention it again."),
        p("Neo laughed once, unexpectedly. The sound felt wrong in the corridor until he looked at the people beside him. They were alive. He was allowed to hear something other than danger in their voices."),
        b('alyssa', "Four received here. The six from the transport are accounted for. We have everyone on this list."),
        p("Ten people. He let the number mean ten actual people, with families waiting and things to complain about and lives he would never fully know. The dead children of the facility remained dead. He would not make these survivors responsible for redeeming him."),
        b('neo', "Keep the corridor open. Hachimura's still ahead."),
        p("He could feel the anger waiting now that there was less practical work between him and it. He checked where his friends stood before he moved.")
    ]),
    'NE12': scene('Hachimura', 'neo_annex__command', [
        b('hachimura', "Brought an audience this time. Couldn't manage it alone?"),
        p("The command room offered space Mariko's hall had not. The civilians were already clear; the response team waited beyond the exit. Neo had prepared for Hachimura's pressure. None of those facts stopped him seeing his mother whenever the man shifted his weight."),
        b('neo', "They're out. You don't have anyone to put between us."),
        b('hachimura', "You think that changes what you are?"),
        p("Neo wanted to hit him before he could finish. He wanted the contempt gone from his mouth, wanted the certainty broken, wanted to hurt him in a way that would reach backwards into the hall and alter a single second. His body leaned towards the impossible bargain."),
        b('neo', "Her name was Mariko."),
        b('hachimura', "I heard her."),
        p("That was worse than denial. Hachimura had heard her and acted anyway. Neo's anger lost the last shelter of imagining some explanation might make the man less responsible."),
        b('neo', "She had rehearsal. There were books on the table. You walked into her life and decided none of it mattered."),
        b('hachimura', "You should have come when you were told."),
        b('neo', "You killed her. You don't get to put that in my hands."),
        p("He said it for Hachimura to hear and because he needed to hear himself say it. Then he set his feet. His father had taught him to pursue an advantage until nothing else existed. Hachimura wanted that boy in this room: alone, enraged, easy to draw away from the exit. Neo would have to deny him that satisfaction while wanting revenge with every breath."),
        p("HISTORICAL INTERLUDE — Hachimura had killed a leader he considered weak, risen within the successor clan and submitted when Thirteen's greater power stood above him. The hierarchy gave his contempt a direction. It had never supplied a reason to care for the people beneath it. Neo had not witnessed that history; it offered him no secret weakness in the room."),
        p("The man in front of him was enough. Neo kept the exit in view and his hands ready. He was going to stop Hachimura. The fury could come with him; it would not choose who else paid.")
    ], [
        p("Hachimura was down and alive. The prepared response team closed around him, securing the hands Neo could not stop looking at. Those hands had been part of the world before Mariko died. They were still part of it now."),
        b('hachimura', "Don't expect thanks."),
        b('neo', "I don't."),
        p("The victory gave him no sudden quiet. His mother did not come back. The kitchen did not reassemble around a version of the evening in which he had been faster. He could have struck again; the desire was plain, ugly and present. He stepped back until another person's shoulder stood between them."),
        b('neo', "He's staying in custody. Check the restraints."),
        p("He waited until the receiving officer had actually taken responsibility. That was the revenge he could finish here: Hachimura stopped, his authority over this operation broken, his victims beyond his reach. It was not the whole of what Neo wanted. It was what he chose to do."),
        p("He owed Hachimura no forgiveness and would offer none. What he said next, or refused to say, could belong to him without changing the living handoff.")
    ]),
    'NE13': scene('No number owns you', 'neo_annex__medical', [
        p("Garrett had kept Thirteen away from the evacuation route until holding the position cost more than he could continue paying. His guard had opened; his stance took effort to recover. He made it back to the corridor rather than turn exhaustion into a final performance. Neo moved into the space he left."),
        b('thirteen', "Number One."),
        p("A designation, spoken without surprise. Neo had heard it in memory for years. Hearing it from this adult face made the lost interval between them suddenly physical."),
        b('neo', "Neo."),
        b('thirteen', "A name changes very little."),
        b('neo', "It changed something for me."),
        p("Thirteen's eyes moved past him to the corridor. Whatever the recognition cost him, he was still directing an operation. Neo saw the delay after a movement, the effort spent concealing it, and the controlled refusal to step away. He could not diagnose years from a few exhausted seconds."),
        b('april', "His return is late. Tyler, hold. Daniel, leave the second step open for Neo."),
        b('thirteen', "I'm not the weak one you remember."),
        p("Neo remembered a hungry child watching the space beside a bowl. He also saw a commander blocking the route Alyssa was still using to reach the receiving team. Pity that ignored the second fact would put people in danger. Anger that erased the first would make the old programme's judgement his own."),
        b('neo', "I'm not asking you to prove anything."),
        b('thirteen', "You don't decide what is required."),
        p("There it was: a familiar shape of sentence, authority passing through a mouth that had once been afraid of it. Neo thought of Takeo and felt the old hatred sharpen. His father was absent from this corridor, still managing to fill it with things two children had learned to say."),
        b('neo', "No. But I can stop you taking anyone else."),
        p("Alyssa called that the medical route was holding. Tyler answered from his side. Daniel left Neo room to move. Thirteen would not be talked harmless by the fact that Neo cared. They would have to earn the openings together, and keep the corridor clear while they did.")
    ], [
        p("After the third supported opening, Thirteen overextended. His body failed to return with the command he gave it. Neo saw the collapse beginning and kept the route open as the medical team moved. The fight was over; the person in front of him was still alive."),
        b('thirteen', "Don't."),
        p("Neo stopped reaching. A medic knelt within view instead. Thirteen's gaze stayed on him, severe even through the effort it took to focus."),
        b('neo', "They're taking you out of this corridor."),
        b('thirteen', "Under guard."),
        b('neo', "Yes."),
        p("He would not dress custody up as a homecoming. People had been taken on Thirteen's orders. Help did not remove their claim on the truth."),
        b('thirteen', "You left."),
        p("The words reached a place the blows had missed. Neo's first impulse was explanation: his age, the raid, the route that had been available. All of it mattered. None of it could give Thirteen back the years Neo had lived elsewhere."),
        b('neo', "I did. I didn't know you were alive."),
        b('thirteen', "You had a life."),
        b('neo', "Yes."),
        p("He could not apologise for Mariko's kitchen, Tyler's saved seat, Alyssa asleep beside a book. He could grieve that Thirteen had not had those things without pretending they were stolen from him by a ten-year-old who escaped."),
        b('neo', "I kept thinking I should have found a way back. I don't know if there was one. I wanted there to have been."),
        p("Thirteen looked away. Neo let the answer remain unanswered. A confession was not a demand that the other person make it bearable."),
        b('neo', "I won't tell you I understand everything that happened after. I wasn't there. I'm here now. The stretcher is here."),
        b('thirteen', "No promises."),
        b('neo', "You don't need to make one to get help."),
        p("Thirteen allowed the immediate aid. He offered no allegiance, no forgiveness, no sudden trust. The medical team took him into secure custody alive. Neo stayed until the handoff was complete, then moved out of the way."),
        p("The child he had left behind had survived. That truth would take time to live beside the truth of what the man had done. Neo did not need to settle either by himself in this corridor.")
    ]),
    'NE14': scene('A place to come back to', 'neo_home__kitchen_dining', [
        p("At their apartment, two mugs waited where they had always waited. Neo stood just inside the door while Alyssa took off her coat. The room had acquired no wisdom in their absence. The controller still drifted left. A plant wanted watering. There was barely enough clear space on the table for dinner."),
        p("The ten captives had been received alive. Hachimura was in custody, Thirteen receiving care under guard, the current retrieval operation dismantled. Takeo remained at large. Neo could say each fact without turning it into a promise that nothing would ever happen again."),
        p("Over the following days, Alfheim's damaged meeting space filled with repair work. Soren carried things where he was asked, sometimes bristling at the instruction and doing it anyway. Tyler brought his father the club books and sat through a correction that lasted longer than the journey there. None of them had become a different person because the immediate danger had ended."),
        b('daniel', "Friday. My choice this time. You can complain afterwards."),
        b('neo', "How long afterwards?"),
        b('daniel', "I'd like a quiet walk to the door first."),
        p("The invitation stayed with Neo after Daniel left. A date on a calendar that was not a hearing, a medical appointment or a practical arrangement for someone dead. He wanted to go. Wanting to go hurt less than he had expected, and then more."),
        b('neo', "I keep thinking of things to tell her."),
        b('alyssa', "Mariko?"),
        b('neo', "The chair here. Daniel's film. Something stupid the radio did. It takes a second every time."),
        p("Alyssa set her mug down. He looked at the empty part of the table and let the second happen without trying to outrun it."),
        b('neo', "I don't want the last thing I remember to keep being the loudest."),
        b('alyssa', "Tell me one of the other things. If you want."),
        p("He reached for the choir programme. The paper had softened where he kept holding it. He thought of Mariko coming home annoyed about a note, hungry enough to eat what he had cooked without first asking how he had made it."),
        p("The kitchen around him held steady while the older one returned. He could miss his mother here. There was room.")
    ], [
        p("After the remembrance he had chosen, Neo returned to the table. Alyssa had moved her binding work into a careful stack. He asked where she wanted it; she pointed, and he carried it without rearranging her system."),
        b('alyssa', "The controller still drifts left."),
        b('neo', "Tomorrow."),
        b('alyssa', "I'm having first try."),
        b('neo', "I know. I was going to hold the torch."),
        p("She smiled, then watched him for a moment. He could feel a question there and was grateful when she let him take his time."),
        b('neo', "I used to think being happy meant I'd forgotten someone. Like I had to keep hurting to prove I hadn't left them."),
        p("He did not have to supply a history for every word. Alyssa rested her hand beside his, the same quiet offer she had made in the refuge."),
        b('alyssa', "Do you want to put the programme somewhere you can see it?"),
        b('neo', "Yes. Not in the middle of your work."),
        b('alyssa', "Thank you. My plants have enough competition."),
        p("They found a place. It did not cure the grief or close the years he could never recover for Thirteen. He still hated Takeo. He was still angry that Hachimura could wake to another day when Mariko could not. Those feelings no longer had to make every decision before he got a turn."),
        b('neo', "I love you."),
        b('alyssa', "I love you too. Dinner's getting cold."),
        p("He sat. There would be difficult mornings and ordinary ones, calls he dreaded and repairs he could not finish. Tonight Alyssa nudged her mug out of his elbow's way, and he moved the serving bowl closer to her. The life he wanted was here, asking him to take part.")
    ]),
}

MEMORIES = {
    'NE-M01': dict(title='The kitchen light', era='neo_home12', background='home_kitchen', text=[
        p("EARLY HOME · Neo 12, Mariko 39. The placement had come after protected care, independent decisions and time spent getting to know one another. This was not the night she took him out of the facility. This was an evening in a house he was slowly learning he could remain in."),
        p("The radio lay silent on a cloth. Neo had taken the back off with permission and made the fault worse. He had arranged the screws in a straight line, as if tidiness could explain the result before Mariko saw it."),
        b('mariko', "Oh. Completely silent, then."),
        b('neo', "I can put it back."),
        b('mariko', "Will that make it work?"),
        b('neo', "No."),
        p("He waited. She was annoyed; pretending otherwise would have made the waiting worse. Her programme was starting and he had broken the thing that played it. She looked at the clock, sighed, and turned back to the cooker."),
        b('mariko', "Leave the screws on the cloth. We can look tomorrow. Bowls are in the cupboard beside you."),
        b('neo', "Do you still want me to—"),
        p("He could not decide whether the question was about the bowls or the rest of the evening. Mariko held out a spoon."),
        b('mariko', "Taste this. I think I've been too generous with the ginger."),
        p("Dinner continued. His mistake stayed on the shelf instead of becoming the only thing anyone could see about him. When she asked which bowl he wanted, he pointed at one. She gave him that one without turning the choice into another test."),
        b('neo', "Can the kitchen light stay on?"),
        b('mariko', "Yes. I can reach the switch in the morning."),
        p("She did not ask him to earn the electricity or explain the dark. He ate while the light made a small yellow shape in the hall. The radio remained broken. He remained welcome.")
    ]),
    'NE-M02': dict(title='A seat saved for you', era='neo_school16', background='school_gym', text=[
        p("SCHOOL · Neo, Tyler and Daniel 16. The gym smelled of dust and rubber soles. Neo stood near the bench, considering whether leaving would look more deliberate than waiting."),
        b('tyler', "Saved it. Sit down."),
        p("Tyler lifted his bag without making an occasion of the invitation. Neo sat at the far edge. There was still plenty of room between them, and nobody hurried to fill it with questions."),
        b('daniel', "There's a film after school. I want to see it. You can come."),
        b('neo', "You make that sound like a warning."),
        b('daniel', "Depends how much you talk through it."),
        b('tyler', "He's seen the trailer six times."),
        b('daniel', "Four. Two were by accident."),
        p("Neo looked between them, trying to decide whether he had missed a rule. They were disagreeing without checking his reaction. He was allowed to be present without giving a performance."),
        b('neo', "What if it's bad?"),
        b('daniel', "Then I'll be disappointed. You can still come."),
        p("It was such a modest promise that he could believe it. He did not have to be interesting enough to justify the seat, or explain the place he had lived before Mariko's house. Tyler asked whether he needed to tell home about the later bus. Neo said yes and reached for his phone."),
        b('tyler', "We'll wait."),
        p("They left through the courtyard together. Neo walked a little behind them until Tyler slowed to complain about a loose shoelace he did not actually retie. By the gate all three were level. Nothing had been demanded in return.")
    ]),
    'NE-M03': dict(title='Before nine', era='neo_home16', background='home_living', text=[
        p("SETTLED HOME · Neo 16, Mariko 43. He came home angry that she had called Tyler's house before the check-in they had agreed. She stood near the living-room doorway, relieved enough to make the anger worse."),
        b('neo', "You said nine. You called before nine."),
        b('mariko', "I was worried. You didn't answer the first—"),
        b('neo', "Because I wasn't supposed to yet."),
        p("She stopped. Neo could feel himself preparing to apologise simply to end the disagreement. It was easier than standing in a room with an adult who was unhappy with him. He made himself keep his hands still."),
        b('neo', "We had a plan."),
        b('mariko', "We did. I broke it. That was my mistake."),
        p("The answer disarmed him without making him less irritated. He had wanted to win the argument; he had not quite believed winning was possible. Mariko sat down rather than keep blocking the doorway."),
        b('mariko', "If your plans change, you message. If they don't, I wait until the time we agreed."),
        b('neo', "Even if you're worried."),
        b('mariko', "Even then. I might complain privately to the kettle."),
        p("He agreed to message if they stayed out later. She agreed that being frightened did not make the agreement disappear. Neither of them became cheerful immediately. She went to the kitchen and came back with the leftovers."),
        b('neo', "You saved the good rice?"),
        b('mariko', "I'm annoyed, not wasteful."),
        p("He took the bowl. The room had survived an argument in which he had not surrendered. So had the home. He ate beside her while they both pretended to pay more attention to the radio than they were.")
    ]),
    'NE-M04': dict(title='Before we had names', era='neo_facility10', background='facility_dorm', text=[
        p("BEFORE THE RAID · Number One and Thirteen 10. The other trainees were alive in this supervised interval. At the table, bowls made small hard sounds whenever a child forgot to put one down carefully."),
        p("One had finished the exercise first. The result followed him into the room. He knew where to sit and how to hold his shoulders; he did not know what to do with Thirteen standing near the end of the table, looking at the food."),
        b('thirteen', "You finished first again."),
        b('neo', "There's still food."),
        b('thirteen', "I can see."),
        p("One looked down at his bowl. He had meant to help and had made it sound as if the other boy could not count. Before he found a better sentence, the trainee beside him nudged an elbow away from the gap."),
        b('trainee', "They're counting bowls, not places. Move yours a little."),
        p("One moved it. Thirteen sat, carefully enough that the bench barely sounded. Across the table another child rubbed at a stubborn mark with a thumb. Ordinary movements, each made small by the room around them."),
        b('thirteen', "You're in the way of my arm."),
        b('neo', "Sorry."),
        b('trainee', "Now you're in mine."),
        p("They shifted again. For a moment the problem was only elbows and space. One did not have to be the best at making room. He could get it wrong and move over."),
        p("The supervision remained. So did the next exercise and all the comparisons waiting beyond the meal. No promise was made across the bowls. Nobody knew what the raid would bring. There was simply a place beside him, and for that meal Thirteen occupied it.")
    ]),
    'NE-M05': dict(title='The extraction', era='neo_raid10', background='facility_hall', text=[
        p("FIXED HISTORY · Neo 10, Mariko 37. During the Interpol raid, the available route ran towards a door One could see but could not make himself approach. Mariko reached him there, low enough that he did not have to look up to find her face."),
        b('mariko', "I'm Mariko. We're going to that door. The next officer will walk with us."),
        b('neo', "The others."),
        p("She looked where he looked. He wanted her to have an answer large enough for every room. She gave him the part she could actually do."),
        b('mariko', "I can get you through this door. Stay where I can see you."),
        p("He moved, then tried to look back. The route did not open into all the places he wanted to search. He had been trained to respond quickly and to treat hesitation as failure. Now every direction felt like a failure he could not name."),
        b('neo', "I can't see them."),
        b('mariko', "Look at me for this step. Just this one."),
        p("He took the step. He would spend years asking it to become a different one. It remained the step a ten-year-old had been able to take while an officer kept the available evacuation route in front of him."),
        p("The other subjects were killed. The account Neo carried out did not identify who killed them. Thirteen survived without Neo knowing it. Nothing in the broken view through that doorway could tell the child what had happened in every room."),
        p("SCRIPTED RECOLLECTION · Before the raid, Takeo's presence belonged to the programme's supervised exercises. One remembered waiting for a look that might mean something other than assessment."),
        b('takeo', "The exercise is finished. Return to your assigned place."),
        p("There had been no other instruction. One had returned. The memory was brief; adulthood would supply a word for the ache inside it, and then years of anger that the word father had ever belonged there."),
        p("After the extraction came protected care and separate placement decisions. Mariko did not take him straight from the raid into her kitchen. There were rooms he did not know, people whose names he forgot, and the slow discovery that her return did not depend on giving useful testimony. A home would come later. First there was the fact of having got out, and the absence of the children who had not.")
    ]),
    'NE-M06': dict(title='Rehearsal night', era='neo_home16', background='home_kitchen', text=[
        p("SETTLED HOME · Neo 16, Mariko 43. She came in from choir with her music crushed under one arm and a grievance she had clearly been saving all the way home. Neo turned the heat down before she reached the kitchen."),
        b('mariko', "Forty minutes. One note."),
        b('neo', "Did it improve?"),
        b('mariko', "The note or the argument?"),
        p("He handed her a bowl. She tasted it, decided she was hungry enough to postpone criticism, and sat. The radio remained in pieces on its cloth. He had chosen to cook tonight, without turning the meal into instalments on a debt for being her son."),
        b('neo', "I can finish that after."),
        b('mariko', "You can finish your dinner after you sit down."),
        b('neo', "The radio."),
        b('mariko', "Yes. I was being difficult. It's one of my interests."),
        p("He sat. She told him who had disagreed about the note, imitating no one's singing quite fairly. He disagreed with her account on principle and received an indignant explanation. There were parts of her day that had nothing to do with him. He liked being invited to hear them."),
        b('neo', "Are you going back next week?"),
        b('mariko', "Of course. I intend to be right again."),
        p("He laughed into his bowl. No one in that kitchen knew it would become an evening he reached for years later. She was alive, opinionated and hungry; he was home, with unfinished work allowed to wait until morning.")
    ]),
}

RETURNS = {
    'NE-M01': [p("The static thinned. Neo took his hand from the dial. Mariko was waiting for an answer about tonight, not a repaired radio or evidence that the years she had given him had been worthwhile. He could stay because he wanted to.")],
    'NE-M02': [
        p("The bag was still hooked over the chair. In the present, Tyler had finished the paid bout. The promoter counted gate receipts without counting Tyler's purse, while two house fighters occupied the back door."),
        b('tyler', "I fought the bout. Give me what we agreed."),
        b('neo', "Move away from the door."),
        p("He kept his hands open. A saved seat did not create a debt Tyler could call in. It did mean Neo recognised exactly who was standing beside him, and why he intended to leave with him.")
    ],
    'NE-M03': [
        p("In the refuge, the choir programme waited beside the papers. Neo had been angry with her that evening. She had been alive enough to irritate him, and safe enough to disagree with. He wanted that back with a force that left him unable to lift the cup."),
        b('neo', "We argued about nothing sometimes."),
        b('alyssa', "You can miss that too."),
        p("He nodded without looking up. He did not owe anyone a version of his mother too perfect to have lived with.")
    ],
    'NE-M04': [
        p("The bowls and bench receded. The commander photograph remained beneath the lamp. Neo's memory had not supplied a secret promise or an explanation for the years between. It had given him a boy with elbows, hunger and a place to sit."),
        p("He could remember that without excusing the orders beside the photograph. He could remember the others without making their deaths proof that his own life was a mistake.")
    ],
    'NE-M05': [
        p("Back in the refuge, Neo pressed his palms against the table until he could feel its edge. He had left. He had also been a child being taken out of a place children should never have been. Neither fact erased the ache of imagining Thirteen still inside."),
        p("Takeo had been the adult with power over that world. Neo hated him for what he had made of it, and for how long Neo had mistaken surviving it for a betrayal. He could not reach his father from this room. He could help make a route out of the annex."),
        b('neo', "A medical team. We need one ready for him too."),
        p("The request was quiet, made to himself before he went to the crew. It promised preparation, not an outcome he could force Thirteen to accept.")
    ],
    'NE-M06': [
        p("The smell of dinner belonged to the apartment again. Neo put the programme beside his own mug and told Alyssa about the argument over the note. He got partway through Mariko's indignant explanation before his voice broke."),
        b('neo', "She'd say I was telling it wrong."),
        b('alyssa', "You can tell it again."),
        p("He would. Not immediately, and not perfectly. The story could wait at the table with them.")
    ],
}
for key, spec in MEMORIES.items():
    spec['after_encounter'] = RETURNS[key]

MEMORY_AT = {0: ('NE-M01',), 1: ('NE-M02',), 4: ('NE-M03',),
             9: ('NE-M04', 'NE-M05'), 13: ('NE-M06',)}

# Kept for already-saved isolated sessions. New readings finish in the reader,
# without a separate generic reflection/journal checklist.
MEMORY_TASKS = {
    key: [dict(prompt='Finish this saved recollection.', options={
        'detail': ('Stay with the remembered moment', 'The remembered moment settles.'),
        'listen': ('Let the conversation finish', 'The remembered voices fall quiet.')}),
        dict(prompt='Return to the present.', options={
            'return': ('Let the memory end', 'The room around Neo comes back into focus.')})]
    for key in MEMORIES
}


def copy_scene(key, field):
    return deepcopy((MEMORIES if key in MEMORIES else CHAPTERS)[key][field])


CHOICE_LABELS = {
    'ordinary': ('How does Neo spend the evening?', {'repair': 'Ask to work on the radio', 'meal': 'Help with dinner', 'evening': 'Stay and keep her company'}),
    'disclosure': ('How much is Neo ready to share in private?', {'private': 'Keep the deeper history private', 'programme': 'Offer to discuss the programme', 'parentage': 'Offer to discuss the programme and his father'}),
    'later_disclosure': ('After remembering, what is Neo ready to share?', {'private': 'Keep the deeper history private', 'programme': 'Offer to discuss the programme', 'parentage': 'Offer to discuss the programme and his father'}),
    'approach': ('How does Neo approach the contact?', {'meeting': 'Take the agreed meeting · closer position', 'observe': 'Check the side lane first · wider position'}),
    'boarding': ('How does Neo reach the stopped transport?', {'lane': 'Use the boarding lane · 4 stamina', 'barrier': 'Clear the stationary barrier · 7 stamina'}),
    'allocation': ('Who does Neo support first?', {'tyler': "Support Tyler's lane · 4 stamina", 'daniel': "Support Daniel's return · 8 stamina"}),
    'response': ('Hachimura is under guard. What does Neo do?', {'property': "Ask for the victims' belongings", 'speak': 'Say what he came to say', 'silence': 'Leave without another word'}),
    'contact': ('What contact can Neo offer after medical care?', {'supervised': 'Offer a later supervised conversation', 'statement': 'Keep contact to the necessary statement'}),
    'remembrance': ('How does Neo want to remember Mariko?', {'invited': 'Invite a few people to remember her', 'private': 'Keep a private remembrance', 'quiet': 'Spend quiet time with Alyssa'}),
}


def choice_scene(chapter, value):
    """Local choices rejoin without asserting an unchosen branch happened."""
    if chapter == 13:
        return {
            'invited': [p("Neo invited a few people who had known Mariko. When it was his turn, he spoke about the choir argument. Halfway through he had to stop. Nobody supplied the rest of the sentence for him."), b('neo', "She was very sure she was right. She usually was. Please don't tell anyone I admitted that."), p("There was laughter, then room for the tears he had been trying to postpone. He let someone else remember her too.")],
            'private': [p("Neo kept the remembrance private. He set out the programme and sat with the radio silent beside it. He did not rehearse something eloquent for an audience that was not there."), b('neo', "I miss you, Mum."), p("It was enough to say for now. He stayed until he wanted to get up, not until he thought he had suffered for the right length of time.")],
            'quiet': [p("Neo asked Alyssa for a quiet evening. She brought her mug to the table and let him decide whether to talk."), b('neo', "Can we just sit?"), b('alyssa', "Yes."), p("He leaned towards her; she met him halfway. There was no speech to fail to finish. When he did say something about Mariko, it was a small memory, and Alyssa listened.")],
        }[value]
    if value in ('private', 'programme', 'parentage'):
        return [p({
            'private': "Neo left the deeper account where it was. The crew had the safety facts. Trust did not have to be measured by how much of himself he could bear to explain tonight.",
            'programme': "Neo could offer someone a little more of the account. He would choose a listener and speak in private; deciding he was ready did not put the story into anyone else's hands yet.",
            'parentage': "Takeo's name pressed against the back of Neo's teeth. He could tell a chosen listener in private. It would be a fact about the man who had hurt him, not a claim that Neo belonged to him.",
        }[value])]
    return deepcopy({
        'repair': [b('neo', "Can I look at the radio?"), b('mariko', "Until dinner. I'm setting the timer for you as well as the rice."), p("He worked beside her until the timer interrupted. The repair was unfinished when she left for choir. He labelled the screws this time.")],
        'meal': [b('neo', "I'll help with dinner. The radio can complain."), b('mariko', "Good. Start with the onions. You are not a guest every time you visit."), p("He stayed at the counter with her, passing things before she asked and accepting corrections when he guessed wrong. They ate before rehearsal.")],
        'evening': [b('neo', "I'll just stay a while, if that's all right."), b('mariko', "I did invite you. Sit down."), p("He sat. There was no job to complete before he could count the evening as worthwhile. She told him about choir and asked whether he wanted tea.")],
        'meeting': [p("Neo took the agreed meeting at the nearer loading door. He could see the contact's hands and the approach through the yard. It would put him closer if the crew recognised him.")],
        'observe': [p("Neo checked the side lane before the meeting. The wider position left him farther from the likely approach, with more ground between him and the retrieval crew. He kept the contact in sight.")],
        'lane': [b('neo', "I'll use the clear lane. Keep it open behind me."), p("He marked the wider boarding position beside the stopped vehicle. The approach would cost four stamina; he would need the rest for the escort.")],
        'barrier': [b('neo', "I'll clear that barrier. Don't move the vehicle."), p("The closer approach would take seven stamina. Neo checked that the receiving lane stayed clear before committing to the extra work.")],
        'tyler': [b('neo', "Tyler, I'm on your side first. Daniel, keep the return open."), p("He took the wider entry position. Four stamina for the approach, then he could turn towards Daniel's lane if needed.")],
        'daniel': [b('neo', "Daniel, I'll cover the return. Tyler, call before you move."), p("The closer entry would cost eight stamina. Neo accepted the extra effort to keep Daniel from being stranded beyond cover.")],
        'property': [b('neo', "The things you took. I want them back with the people they belong to."), p("He addressed the receiving officer when Hachimura tried to answer. The request was not a bargain with the man under guard. It was practical work still owed to the victims.")],
        'speak': [b('neo', "You don't get another house. Another person you can hurt to make me come when you call."), p("Hachimura stared at him. Neo waited for a satisfaction that did not arrive, then stopped waiting."), b('neo', "I hate you. I'm leaving you here."), p("He turned towards the people receiving custody. He did not need Hachimura to agree that it was over.")],
        'silence': [p("Hachimura watched him, waiting for a final exchange he could still spoil. Neo had nothing he wanted to give him. He checked that the receiving team had taken custody and left without another word.")],
        'supervised': [b('neo', "If you want to speak later, it can be arranged. With supervision. You don't have to answer now."), b('thirteen', "I haven't asked for that."), b('neo', "I know."), p("Neo left the offer with the medical handoff. It was not a promise to make Thirteen's recovery his life, or a condition attached to care.")],
        'statement': [b('neo', "I'll give the statement they need. I can't promise more than that."), b('thirteen', "Then don't."), p("Neo accepted the answer. The medical team still received Thirteen alive. A boundary did not have to become another abandonment to count as real.")],
    }[value])


def disclosure_scene(person, topic):
    """Only the chosen listener hears these facts; no global relationship gain."""
    if topic == 'parentage':
        lines = [p("When they were alone, Neo kept his hands flat on the table. It was easier than watching them shake."),
                 b('neo', "Takeo Mishima is my father. I don't use his name."),
                 b('neo', "I hate him. I need you to understand that this isn't me asking how to make peace with him."),
                 p("Saying it brought anger, not relief. There had been a time when he wanted something from his father besides distance. He hated that memory too.")]
        replies = {
            'alyssa': "I wasn't going to ask you to. You're Neo. That's who I live with.",
            'tyler': "You don't have to go near him for my sake. Ever.",
            'daniel': "I won't turn that into advice about families. I don't know enough. I can listen.",
            'april': "I'll keep that between us. The operational notes don't need your parentage.",
            'garrett': "You don't owe him a reunion. Or me the rest of the story.",
        }
    else:
        lines = [b('neo', "I was Number One in the Shinigami programme. They trained children. Compared us until we started doing it for them."),
                 p("He paused, letting the listener hear a sentence he had usually kept inside his own head."),
                 b('neo', "The other subjects died. I don't know who killed them. Mariko got me out during the raid. The home came later."),
                 b('neo', "I keep thinking being the best should have meant I could do something. I was ten. I know how that sounds. It doesn't stop.")]
        replies = {
            'alyssa': "You don't have to make it sound reasonable for me to stay. Do you want my hand?",
            'tyler': "Ten. You should have had someone getting you out. I'm glad she did.",
            'daniel': "I don't have something clever to say. I'm sorry they put you there.",
            'april': "You don't have an account of every room. I won't fill the gaps and call that evidence against you.",
            'garrett': "They made you a kid responsible for their results. That doesn't make their failures yours.",
        }
    lines += [b(person, replies[person]), b('neo', "Thank you. That's enough for tonight."),
              p("The listener let him stop. Nothing in the room required him to turn the rest of his life into an explanation.")]
    return lines

