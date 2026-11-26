"""Authored scene expansion for The Inheritance.

Insertions retain the original source IDs used by the five paintings. Saved
reader snapshots keep their own text; new scenes receive these longer passages.
"""


def _insert(beats, scene, field, additions):
    result = []
    for index, beat in enumerate(beats):
        source = f'{scene}:{field}:{index:03}'
        beat['source_id'] = source
        if scene == 'CA-F06' and field == 'text' and index in (4, 5):
            beat['camila_costume'] = 'camila-syndicate'
        result.append(beat)
        for offset, extra in enumerate(additions.get(index, [])):
            extra['source_id'] = f'{source}:expanded:{offset:02}'
            if beat.get('camila_costume'):
                extra['camila_costume'] = beat['camila_costume']
            result.append(extra)
    return result


def apply(chapters, memories, b, p):
    # Child Camila bargains over immediate things; adult Camila uses precision
    # to protect herself. Crow offers care without surrendering his ambitions.
    additions = {
        ('CA-F01', 'text'): {
            0: [p('The tin has a dent which makes the lid difficult to close. Camila likes to do it herself. When Elena asks for help gathering the pieces, she sorts them by colour first, although gathering them would be quicker. Pilar pushes a blue counter across the table with one finger and ruins the pattern. Camila pushes it back. The game matters more than the neatness, but she has not decided to admit that yet.')],
            3: [b('camila-pilar', 'If you go, who gets your next turn?'),
                b('camila', 'You can keep it until I come back.'),
                p('Pilar looks at Elena. Camila dislikes that look: the way grown-ups can become the people a question really belongs to. Elena sets the watering jug down and sits with them.'),
                b('camila-elena', 'You can miss someone and still want to go. You do not have to choose one feeling.'),
                p('Camila rubs the edge of the tin. She wants to see the house. She also wants Pilar to stop looking as though Camila has changed the rules halfway through.')],
            7: [b('camila', 'What if I forget where things go?'),
                b('crow', 'You will learn where they go. Some places will be yours to choose.'),
                p('She considers this. A place for her things sounds different from a place where she is allowed to put them. His gloves are very still. She cannot tell whether he is smiling, and she will not ask a question just to make him do it.'),
                b('camila', 'The tin is loud when you carry it.'),
                b('crow', 'Then I shall hear it.'),
                p('It is such an ordinary answer that she looks at him again. He has not asked her to demonstrate the game or count its pieces. She lifts the bag with both hands. Elena takes some of the weight, and Camila lets her.')],
            8: [p('At the threshold she turns back, not because she has changed her mind, but because the room looks different from here. Pilar raises the red counter. Camila raises her empty hand. For once neither of them insists on having the last word. The visitor waits beside the door until she is ready to walk through it.')],
        },
        ('CA-F02', 'text'): {
            0: [p('She knows the house by small permissions now: which drawer holds spare paper, which bell means supper, which door she should knock on. At first she had asked before taking a second sheet. Mara had moved the stack within reach instead of answering the same question every afternoon. Camila still checks how much is left. Having enough does not yet feel as permanent as being told she has enough.')],
            2: [b('camila', 'It was supposed to be finished before he came home.'),
                b('camila-mara', 'Did he ask for a finished house?'),
                b('camila', 'No. I wanted to show him.'),
                p('Mara wipes a spot of glue from the table. She does not tell Camila that the house is wonderful; one wall is plainly folding inward. Instead she clears a space where the whole awkward thing can stand.'),
                b('camila-mara', 'Then show him what you made. We can still eat with a roof unfinished.')],
            8: [b('camila', 'You are holding it too hard.'),
                b('crow', 'Show me.'),
                p('She moves his gloved finger to the corner. He lets her arrange it. For a while the room is quiet except for paper shifting against paper. Camila forgets the explanation she prepared and tells him instead about Mara getting glue on her sleeve.'),
                b('camila', 'We should make a bigger door.'),
                b('crow', 'Will the wall bear it?'),
                b('camila', 'It will if you keep holding that part.'),
                p('He stays. The roof dries crooked, and she can see exactly where she would change it next time. But nobody puts it away when the evening ends. Passing the sideboard the next morning, she straightens it by a fraction and goes to breakfast without asking whether it may remain.')],
        },
        ('CA-F03', 'text'): {
            0: [p('Camila has begun to enjoy the pause before her father answers. It gives her time to anticipate the objection and arrive at it first. Today she has checked the sums twice. When he asks about the dates, she feels briefly cheated, as though he has changed the contest after she has won it.')],
            4: [b('camila', 'So I should always be the one who can wait.'),
                b('crow', 'You should understand who cannot.'),
                p('She moves one counter to his side of the desk. The lesson becomes exciting again. An advantage can be invisible until somebody points to it; afterward it seems impossible not to see. She wants to find the next one herself.'),
                b('camila', 'And then ask for more?'),
                b('crow', 'Decide what their need is worth to you.'),
                p('She likes being asked to decide. She does not yet ask what it feels like to be the household on the other side of the desk.')],
            8: [b('camila', 'You could have interrupted.'),
                b('camila-mara', 'I did. You told me you were nearly finished.'),
                p('That is worse than a misunderstanding. Camila remembers saying it, then saying it again without looking up. She has treated Mara as a person who will wait because Mara usually does.'),
                b('camila', 'I wanted to get the answer right.'),
                b('camila-mara', 'I know. I wanted to go for a walk with you.'),
                p('There is no clever reply that gives them the afternoon back. Camila glances at her father, hoping for a ruling. He makes none. This small failure is hers to answer, and Mara is still standing by the door.')],
        },
        ('CA-F04', 'text'): {
            0: [p('Her pages are straight, their margins almost aggressively clean. She has imagined the small inclination of his head that will mean he sees what she has done. The branches come readily when she concentrates: agreements, delays, concessions. Their clarity is seductive. Each consequence appears to lead neatly to the next, provided the people inside it do what she expects.')],
            5: [p('The refusal is neither foolish nor hostile. The writer needs a receiving team at another site. Camila reads the sentence twice, trying to find a reason it should not count. Her first impulse is to defend the elegance of the work that came before it. That impulse embarrasses her more than the error.'),
                b('camila', 'The other three reports gave me every reason to expect cooperation.'),
                b('crow', 'They gave you three reports.'),
                b('camila', 'You make it sound as though I did not think.'),
                p('He leaves her pages where they are. He has not torn them up, or even pushed them away. She has supplied the humiliation herself.'),
                b('crow', 'You thought carefully. Now think with this included.')],
            9: [p('She hears the limit in that answer. His presence has made mistakes survivable, and she has quietly begun treating his presence as part of the method. One day the envelope will be on somebody else’s desk. Wanting him to be proud will not tell her what is inside it.'),
                b('camila', 'I can revise it. I would prefer not to enjoy your being right quite so much.'),
                b('crow', 'Your preference is noted.')],
            10: [b('camila-mara', 'Shall I take the first sheet?'),
                 b('camila', 'Leave it. Otherwise I shall convince myself I meant the second answer all along.'),
                 p('Mara puts the clean paper beside the old. Camila begins with the person who refused, this time giving that person a reason that is not merely an obstacle to her own success.')],
        },
        ('CA-F05', 'text'): {
            0: [p('She remembers the contractor’s silence before accepting. At the time it had pleased her: the pause in which an opponent discovers that every remaining route is worse. She had worked for that silence. Nobody had forced her to take pride in it. Her father’s approval afterward seemed to confirm what she already believed about the quality of her work.')],
            6: [b('camila', 'The pressure was supposed to reach the owner.'),
                b('camila-mara', 'Did you think he would bear all of it himself?'),
                p('She had not. That is the answer she keeps trying to improve. She had understood that reduced work would hurt someone beyond the negotiating table; she had simply left those people indistinct. Now the report gives their absence a length: hours that will not be paid.'),
                b('camila', 'No. I thought they were outside the decision.'),
                b('camila-mara', 'Outside yours, perhaps.'),
                p('Camila’s hand closes around the pen. She wants to point out how many livelihoods the protected contract supports, and the argument is true. It is also ready suspiciously quickly. She sets the pen down before using it to win an argument Mara has not offered.')],
            7: [b('camila', 'Would you like me to tell you I regret all of it?'),
                b('camila-mara', 'I would like you to tell me what you mean.'),
                p('Camila looks at the successful negotiation again. She would still protect the contract. She would still work for the man who taught her how. Saying so feels harsher than the tidy report, but it is the first answer she cannot mistake for an appeal to be forgiven.'),
                b('camila', 'I wanted us to win. I still want that. I do not want to become someone who stops asking what winning did.'),
                p('Mara does not absolve her. She sits beside her while Camila requests the names the report does not contain. Some will never arrive. The decision remains hers even where the account is incomplete.')],
        },
        ('CA-F06', 'text'): {
            0: [p('For days she has rehearsed how to present the underestimated margin. Too much explanation will sound like an excuse; too little will sound like concealment. Beneath that professional problem sits a more private one. She wants to know that he would choose this work even if someone else had brought it. She cannot make herself ask him to separate the daughter from the candidate as neatly as that.')],
            3: [b('camila', 'The result would have survived a poorer offer. The reserve would not have survived a second delay.'),
                b('crow', 'You have identified the limit. Do not spend the lesson defending the error.'),
                p('There is relief in being answered at the level of the work. There is a sharper pleasure in knowing how much work there is to answer for. He gave her the education; she endured the negotiations, the refusals, the evenings when a beautiful proposal had to be rebuilt.')],
            5: [p('Her voice sounds closer inside the mask. The title is no longer something she has heard bestowed on other people. It belongs to the person standing here, with a corrected margin and a pulse she hopes nobody can hear. She lets herself be proud before turning to the next instruction.')],
            6: [p('The invitation to the class lies under a page of figures. She has nearly declined it twice: once because she is busy, once because she dislikes being visibly bad at anything. The second reason persuades her to accept.'),
                b('camila', 'One evening. If I can negotiate this appointment, I can survive being told which foot to move.'),
                p('She writes the reply with her favourite pen. It is an absurdly fine instrument for a short note, which is part of the pleasure. Then she leaves the report where it can wait until morning.')],
        },
        ('CA-F07', 'text'): {
            5: [p('She had imagined a larger remit, more responsibility, a difficult part of the organisation placed in her hands. She had not imagined the organisation spoken of in his absence. The empty chair seems suddenly less like furniture. She resents it for making her think about a future she both wants and cannot bear to hurry.'),
                b('camila', 'You have been preparing this for how long?'),
                b('crow', 'Long enough that you should recognise the preparation.'),
                b('camila', 'That is not a date.'),
                p('She knows why she asks. A date would make it a plan she could interrogate, rather than a life he has been shaping alongside her own ambitions.'),
                b('crow', 'There is no appointment on a calendar. I intend what I build to endure.')],
            8: [b('camila', 'And if I judge them differently from you?'),
                b('crow', 'Then your judgement must accomplish something.'),
                p('He is not offering permission to turn his organisation into whatever would make her easiest to love. She knows what he wants it to do. She has helped it grow. Her hope is more difficult than innocence: that she can learn to hold it without simply repeating him.'),
                b('camila', 'I want the responsibility. I would rather you heard that from me than assumed gratitude was the same answer.'),
                b('crow', 'I have never mistaken your ambition for modesty.'),
                p('She laughs once, surprised into it. He knows that part of her too. The affection makes the future heavier, and makes her want it no less.')],
        },
        ('CA-F08', 'text'): {
            2: [b('camila-inez', 'Before you improve the sequence, tell me whether Tuesday is a real answer or a polite way to keep me here.'),
                b('camila', 'A real answer. You will have the revised sequence before you leave.'),
                p('Inez stays standing until Camila moves the earlier slot out of the proposal. The change costs something. That is why Inez begins to believe it. Camila feels the loss with an irritation she keeps out of her voice; listening has not made her enjoy giving ground.')],
            3: [p('She can picture the simpler report: the counterparty resisted, pressure was applied, the original schedule prevailed. It has the reassuring shape of a method she knows. The new report requires her to explain a concession without hiding behind an instruction from her father. She keeps reaching for a justification that will make it impossible for him to disagree. There is none.')],
            8: [b('camila', 'You would have pressed them harder.'),
                b('crow', 'Perhaps. You made this agreement.'),
                p('She waits for the rest: a correction, an order, something that will turn her decision back into his. He leaves the report in front of her. The receiving team remains her responsibility whether she is relieved or frightened by that.')],
            9: [p('Inez’s confirmation is short. The arrival happened; the team is where it needs to be. Camila reads it once for the facts and once because she wants the relief again. She has not discovered a way to make uncertainty disappear. She has discovered that she can carry it until something real answers.')],
        },
        ('CA-01', 'briefing'): {
            0: [p('The discrepancy has followed her out of the civilian day and into this closed room. In a different office she could have sent it back for clarification and let a meeting absorb the delay. Inez’s operation does not have that luxury. Camila has read the same short message three times: the dispatch team is ready; the promised access is not.'),
                p('Her father waits without prompting her. As a child she filled those silences with answers, afraid that hesitation would look like ignorance. Now she lays the two matching totals side by side and begins with what they cannot explain.')],
            4: [b('camila', 'If you wanted the answer you would give, you could send someone who knows how to agree with you.'),
                b('crow', 'Have I asked for agreement?'),
                p('There is the familiar challenge. She wants his confidence and dislikes how quickly she reaches for it. Vey’s promise is a business problem. Her need to prove that she deserves this room is an older problem, and she will make a poor decision if she lets the two become one.'),
                b('camila', 'No. I will bring you an answer I can defend.'),
                b('crow', 'Bring me a result with it.')],
        },
        ('CA-02', 'briefing'): {
            0: [p('It is a childish mark, no more elaborate than a red line, and she has paid someone to repair the case without removing it. She can afford a better one. That is not the point. Most things in her present life can be explained by their use or their cost. This one belongs to a girl who was sure that being able to recognise her own bag would make an unfamiliar journey manageable.')],
            2: [p('People who know only her current work sometimes speak as though she arrived fully formed: a sharp voice, a good education, a place prepared at the table. The place was prepared. She does not deny how much that matters. But there was a child before the title, and the child did not spend that afternoon dreaming of an empire. She wanted to finish a game without giving Pilar the satisfaction of winning by default.')],
        },
        ('CA-03', 'briefing'): {
            3: [b('camila', 'You make assistance sound like an unfortunate substitute.'),
                b('camila-mara', 'Today? It would be. I came to see you.'),
                p('Mara turns the cup so its handle faces her. It is the same small courtesy she used to perform around glue pots and unfinished lessons. Camila has been preparing an entertaining account of the crisis, one with a manageable problem and a suitably dry conclusion. Mara’s answer takes away the performance without taking away the invitation.'),
                b('camila', 'I have been difficult company.'),
                b('camila-mara', 'You have been busy. Those are different things. You can still choose the first one, of course.'),
                p('Camila laughs. There are very few people who can speak to her like this without either asking permission or enjoying the risk. Mara reaches for the tea. She has no intention of making the moment ceremonial.')],
        },
        ('CA-04', 'briefing'): {
            3: [b('camila', 'You think the original will disappear into an office and return as someone else’s interpretation.'),
                b('camila-inez', 'I think my team will ask me what I agreed to. I intend to be able to show them.'),
                p('Camila nearly answers that her word should be enough. She hears the weakness before she speaks it. Inez is accountable to people who will never sit in this room; surrendering the document would leave her with a promise she cannot explain to them.'),
                b('camila', 'Keep it in front of you. I will read from your side of the table if that helps.'),
                b('camila-inez', 'The other side is fine. Just ask before you turn the page.'),
                p('It is a small boundary, and an effective one. Camila draws her hand back. The meeting begins to feel less like receiving a report and more like meeting the person who has had to live with it.')],
        },
        ('CA-05', 'briefing'): {
            1: [p('The accusation had offered a comfortable arrangement of roles: Vey as thief, Camila as the person who caught him. A problem with access is less gratifying. It requires her to find out who can use which promise, and who has been relying on it. She cannot solve it merely by demonstrating that she is cleverer than its author.'),
                b('camila', 'A satisfying explanation. Pity about the evidence.'),
                p('She says it quietly to the empty room. The joke lets her breathe, but she keeps the crossed-out line. If she hides the wrong turn, the final report will make her certainty look inevitable. She has spent too much of this morning being certain to trust that version of herself.')],
        },
        ('CA-06', 'briefing'): {
            3: [b('camila', 'Were they told why?'),
                b('camila-inez', 'They were told to wait for confirmation. Then the shift was cancelled. Some had already arranged to be here.'),
                p('Camila opens her mouth to ask about compensation and shuts it again. Inez notices. The restraint feels clumsy, a skill she ought to have learned before becoming someone people approach with damage.'),
                b('camila', 'I keep trying to get to the part I can repair.'),
                b('camila-inez', 'So do I. But I had to make the calls.'),
                p('Camila has used pressure because it works. Vey has used it because it works. The resemblance offends her before she lets it instruct her. Her objections to his conduct are real; they do not make her own methods harmless. She asks Inez to finish, and this time waits for the answer.')],
        },
        ('CA-07', 'briefing'): {
            4: [b('camila-ansel', 'A little discretion would save everyone an unpleasant morning.'),
                b('camila', 'Whose morning, specifically?'),
                p('His thumb settles on the corner of the undertaking. Camila watches the hand rather than trying to read a confession into his face. He wants her to behave like a discreet functionary: absorb the discrepancy, protect the appearance, leave him room to move.'),
                b('camila-ansel', 'You were sent to preserve the arrangement.'),
                b('camila', 'And you have made two. You can understand my professional interest.'),
                p('She enjoys the neatness of the answer. Then she lets the pleasure pass. Humiliating him would be easy to mistake for progress, especially when he has gone to such trouble to underestimate her. The paper under his hand matters more than his expression.')],
        },
        ('CA-08', 'briefing'): {
            1: [p('She could put his patronising remark into the report. It would explain why she is angry, and tempt everyone reading it to mistake that explanation for proof. Instead she separates what he signed from what she thinks he wanted. The distinction is tedious at precisely the moment when anger would make certainty feel good.'),
                p('Her father has entrusted her with more than she can presently command. That future has been private for years. Vey does not know it, and his contempt cannot take it away. Nor would naming it make Inez’s team any safer. Camila turns the private thought over, then puts it where it belongs: among the reasons this matters to her, not among the terms anyone else owes her.')],
        },
        ('CA-09', 'briefing'): {
            1: [p('She imagines the report after each choice. In one, a concession once held is gone; there will be people eager to call that weakness. In the other, the asset remains and the next emergency meets a thinner reserve. She dislikes both reports. For several minutes she searches for a third version mainly because she would like to be the person who finds one.'),
                b('camila', 'Keeping everything would be an excellent answer. If I had the means to do it.'),
                p('The room offers no objection and no rescue. She thinks of the loading team, of a future request she cannot yet predict, and of the pleasure her father takes in retaining what he has acquired. His preference matters to her. She will not pretend it is the only thing she is weighing.'),
                p('A choice will make one loss hers in a way an analysis of both cannot. She sets the pen between the two proposals. Whichever one she signs must be a decision she can explain to Inez before she explains it to him.')],
        },
        ('CA-10', 'briefing'): {
            0: [p('She has rewritten the requests to remove the phrase “as discussed”. Nothing has been discussed yet. It is the sort of efficient phrase that can smuggle an assumption past the person expected to fulfil it. Mavis will want the route; Martos, the people and the way out; Elias, something worth doing with his attention. Camila needs all three without pretending they are interchangeable extensions of her own skill.')],
            2: [p('The possibility of telling them about her father unsettles her more than asking for help. In a professional refusal she knows where to stand. A confidence may be accepted, misunderstood, or answered with a kindness she has not prepared for. She does not owe them that vulnerability to make the operation work. If she chooses it, she wants it to be an offer of trust rather than another instrument of persuasion.')],
        },
        ('CA-11', 'briefing'): {
            4: [b('camila-ansel', 'If you were certain they would listen to you, you would not need so many conditions.'),
                p('There it is, stated plainly enough to hurt. She wants to tell him exactly whose daughter he is addressing. The impulse is hot, childish, and entirely useless. Inez has signed for an outcome, not a family.'),
                b('camila', 'I need conditions because other people have something to lose. You keep talking about who will listen. Inez is asking what I will do.'),
                b('camila-inez', 'And I am still asking.'),
                p('Camila looks at her instead of Vey. That costs her the last word in the quarrel and buys back the meeting. She goes through the personnel clause slowly, giving Inez room to stop her.')],
            5: [b('camila-ansel', 'You can put a refusal in whatever column pleases you.'),
                b('camila', 'It belongs beside your name.'),
                p('He reaches for his call. The room has changed: an argument about what can be promised has become a decision about what he will obstruct. Camila does not look to Inez for reassurance. She asks whether the conditions still describe what the team needs, and receives a careful yes.')],
        },
        ('CA-12', 'briefing'): {
            4: [b('camila', 'He thinks I only know how to explain your decisions.'),
                b('crow', 'Is that why you chose your terms?'),
                p('She had hoped for dismissal, perhaps a brief contemptuous remark about Vey. The question gives her no such comfort. She checks the answer before speaking. She wanted to prove him wrong; she still does. She has also chosen a plan with reasons that survive his opinion.'),
                b('camila', 'No. But I would enjoy his understanding the difference.'),
                b('crow', 'Enjoy it after the work is done.'),
                p('She smiles despite herself. Then the smile fades. The next room will not be a private room with her father. People who accepted her terms will be putting themselves within reach of someone who refused them.'),
                b('camila', 'I know what I am asking them to risk.'),
                b('crow', 'Then remain answerable for it.')],
        },
        ('CA-13', 'briefing'): {
            0: [p('The hood holds the warmth of her breath. Somewhere inside the loading court a latch knocks against metal and stops. She sorts the sounds before she can stop herself: a person moving, a door, a distance she cannot judge from here. Analysis can give her possibilities. It cannot tell her whether the people behind the door are frightened, or make their fear one more fact she can safely file away.')],
            1: [p('She has spent the operation turning uncertainty into terms other people can agree to. Here there are no sentences between her and the consequence. The contractor has a weapon and a reason to keep the passage closed. Her specialists have agreed to tasks, not to the fiction that she can guarantee their safety.'),
                b('camila', 'We keep the way out clear. If the plan needs changing, you tell me. Do not mistake silence for an instruction to persist.'),
                p('She hears her own voice inside the mask: level, more level than she feels. It is useful steadiness. She lets it serve its purpose without imagining that it has made her invulnerable.')],
        },
        ('CA-14', 'briefing'): {
            2: [b('camila-inez', 'You say that quickly.'),
                b('camila', 'I have been rehearsing a satisfactory answer since you arrived.'),
                p('Inez studies her, then gives a tired, brief smile. Camila stops reaching for the next page. There is no need to hurry this woman through the end of a crisis she has had to explain to everyone below her.'),
                b('camila-inez', 'Next time, call before the shift is lost.'),
                b('camila', 'Yes. That would be a more useful demonstration.'),
                p('The agreement between them is neither forgiveness nor friendship bestowed on demand. It is a reason to answer the next call. Camila finds that she values it more than the easier praise she had prepared herself to receive.')],
        },
    }
    replacements = {
        ('CA-F04', 'text', 10): 'Mara brings a clean sheet. Camila accepts it without tearing up the first one. Both remain on the desk when she begins again.',
        ('CA-02', 'aftermath', 0): 'She puts the case down with the marked side facing her. Ansel has dealt with her as a financial officer. He has never been entitled to the whole account of her life. Remembering the girl with the tin does not oblige her to explain that girl to him.',
        ('CA-03', 'aftermath', 3): 'Camila laughs and leaves the planner shut. Mara has her own afternoon to return to. For once Camila asks about it before offering a way to improve it.',
        ('CA-10', 'briefing', 2): 'She may share the authorised account of her adoption privately, with a chosen colleague. The larger future her father intends remains between them. She will ask for help on the strength of the work, and let a confidence remain a confidence.',
        ('CA-12', 'briefing', 0): 'In the private sitting room, the Crow settles into the chair opposite her. The closed door excludes the sounds of the receiving office. Camila knows the stillness of his mask better than she knows most people’s expressions. She puts the report within his reach.',
        ('CA-12', 'briefing', 5): 'The limit is clear. He will support the choice she has brought him; he will not become the reason it was right. Camila gathers the report, leaving the comfortable quiet of the room before she can mistake it for the result.',
        ('CA-13', 'briefing', 0): 'The depot court is quiet enough to hear the dispatch crew behind the inner door. Camila wears the sealed Diamonds hood, mask and gloves. Ansel’s contractor controls the passage to the record cabinet. She has asked her specialists to assemble here. The public approach still needs to be cleared.',
        ('CA-13', 'aftermath', 0): 'The inner door stands open. The record packet is sealed, and Inez has the dispatch team’s receiving count in front of her. Camila waits for the allocation confirmation before letting herself sit down. Vey’s competing promise can no longer spend the settled concession. This particular authority has done its work; she feels its end as an exhaustion she no longer needs to conceal.',
    }
    for (scene, field, index), text in replacements.items():
        collection = memories if scene.startswith('CA-F') else chapters
        collection[scene][field][index]['narration'] = text
    for collection in (chapters, memories):
        for scene, spec in collection.items():
            for field in ('text', 'after_encounter', 'briefing', 'aftermath'):
                if field in spec:
                    spec[field] = _insert(spec[field], scene, field, additions.get((scene, field), {}))


def ending(lines, b, p, release):
    return _insert(lines, 'CA-14-ending', 'text', {
        2: [p('Inez closes the receiving record but leaves the list of lost shifts beside it. Camila does not ask her to move it. A funded payroll is worth relief; it is not permission to rearrange the table until only the good result remains.'),
            b('camila', 'I gave up East because I wanted room to answer the next failure. I know a lost concession is not an abstract thing to the people using it.' if release else 'I kept East because losing the depot would narrow what the network can do. Fifteen means I will have to refuse something else. I will not call that reserve generous.'),
            b('camila-inez', 'Then tell people before you ask them to rely on it.'),
            p('It is practical advice, almost brusque. Camila is grateful for the absence of a speech about what kind of person she has become. There will be another decision. Inez expects her to be answerable then too.')],
        6: [p('She sits. For a moment she cannot think of anything to say that is not part of the report. Mara waits, and Camila realises how much of the day she has spent preparing to be challenged.'),
            b('camila', 'I was frightened they would do everything I asked and still not come back.'),
            b('camila-mara', 'That sounds like a long day.'),
            p('No lesson follows. Camila turns the cup between her hands. This is the part of being cared for she still finds difficult: nothing needs to be proved before the other person stays.'),
            b('camila', 'I would like you to stay a little longer.'),
            b('camila-mara', 'Then I will.')],
        11: [p('She remembers the paper house waiting on the sideboard, long after anyone had reason to admire it. He made a place for her before she had a useful answer to offer. He also taught her to secure concessions from people who could not afford to refuse. Both memories belong to the man across the desk. Loving him has never made the second one unreal.'),
             b('camila', 'I wanted you to be proud. I still do. But I cannot let that be the only explanation for a decision other people must live with.'),
             p('He rests a gloved hand beside the corrected page. He leaves it attached. She does not need to fill the silence this time.'),
             b('crow', 'Then keep giving me the other reasons.'),
             p('There is warmth for her in the attention he gives the answer, and no retreat from what he intends to build. She will not turn this evening into a story in which affection has made either of them innocent. She can remain his daughter and still name the work she has chosen.')],
        15: [p('Mara makes the bad move. Camila looks at the square, then at Mara, and presses her lips together with exaggerated effort. Mara begins to laugh first. It breaks the last of the formal composure Camila has carried from the meeting. She leans back in her chair, delighted, and lets the game take as long as it takes.')],
    })


def support(who, b, p):
    scenes = {
        'mavis': [b('camila', 'I need the original records brought through intact. What would make the route unworkable?'),
                  b('mavis', 'People treating “intact” as a flexible word. Who hands them over? Who receives them?'),
                  p('Camila puts the route between them. Mavis examines the handover before the destination. It is a different habit of attention from her own, and exactly why she asked.'),
                  b('camila', 'You recover them. I verify them against what I examined. If either step fails, we stop.'),
                  b('mavis', 'Good. Give me the route, then. I would rather have the awkward details now.'),
                  p('Camila supplies them. The questions grow more precise, and with each one her request becomes something another person can actually accept.')],
        'martos': [b('camila', 'The dispatch team needs an escort out. Inez receives them at the other end.'),
                   b('martos', 'Everyone. No one stays because a paper matters more.'),
                   p('There is no flourish in the condition. He waits for her answer as if it ought to be simple. She makes it simple.'),
                   b('camila', 'Everyone. The records have a separate route.'),
                   b('martos', 'Then show me the way out. And the place they can wait if it closes.'),
                   p('She turns the plan so he can mark it. He does not need a speech about her confidence. He needs space for the people he is agreeing to bring back.')],
        'elias': [b('camila', 'I need the public approach kept clear while we negotiate. You will have an audience. I cannot promise an appreciative one.'),
                  b('elias', 'At last, an honest booking. What must they be looking away from?'),
                  p('His smile invites her to enjoy the answer. She does, briefly. Then she shows him the crossing the dispatch team will need.'),
                  b('camila', 'This passage. And if the negotiation fails, the cover still has to hold.'),
                  b('elias', 'You want timing, restraint, and no applause. A severe assessment of my talents.'),
                  b('camila', 'An assessment that includes them. Will you do it?'),
                  p('He studies the passage again. When he answers, the performance has not vanished; it has acquired a purpose.'),
                  b('elias', 'Yes. Give me the signal before you need the room to turn.')],
    }
    return scenes[who]
