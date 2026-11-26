"""What He Holds: authored route, separate from authoritative gameplay results.

Historical wrongdoing is fixed. Outcome prose is selected only after runtime
receipt validation. No manuscript function changes a save or manufactures a win.
"""
from copy import deepcopy

CONTENT_VERSION = 2


def b(speaker=None, text='', narration='', *, room=None):
    beat = {'player': '', 'speeches': [[speaker, text]] if speaker else [],
            'narration': narration}
    if room:
        beat['room'] = room
    return beat


def exchange(*lines, narration=""):
    """Keep a source slot stable while giving a conversation room to breathe."""
    return {"player": "", "speeches": [list(line) for line in lines], "narration": narration}


def prose(text, room=None):
    return b(narration=text, room=room)


CHAPTERS = {
 'MT-01': dict(title='A person in his care', location='syndicate_hq', briefing=[
    prose('The watch on the executive table is too small for Martos to mend in his gloves. He has taken them off, set them together and checked the repaired clasp a final time. Its owner has asked for it back when the repair is sound. Until the Crow opens the assignment folder, this is the only unfinished promise Martos has allowed himself to think about.\n\nAdrien Voss. The name is printed beneath a company heading, clear of the uniform Martos remembers. He reads it twice. He remembers Voss standing dry beneath a vehicle awning while the rest of the unit waited in the rain; remembers being grateful when the commander finally told them where to go. The gratitude is harder to look at than the face.\n\nHe puts the watch down. If the Crow has selected him because of that history, he will do the work. If the history is incidental, he will do it anyway. Years ago those would have seemed like two different decisions. Now his first concern is whether his hands have betrayed the hesitation.'),
    b('crow', 'Adrien Voss. His consortium has been interfering with my routes. This witness can establish which connections he still controls.'),
    exchange(('martos', 'I served under him.'), ('crow', 'Then you know the habits his new title may conceal.'), ('martos', 'Some of them. I will not give you guesses as knowledge.')), b('crow', 'That is why I expect a useful report. Keep her alive. Deliver the records on the terms she accepts. His interference ends.'),
    prose('The authorised meeting takes place later in the neutral receiving room. Lena Varo keeps her case against her knee. She studies Martos before looking at the offered chair.', 'neutral'),
    b('martos-lena', 'You stood at the cordon. I remember your hands on the barrier.'),
    b('martos', 'Yes.'), b('martos-lena', 'Then you can understand why your employer saying I am safe is not an arrangement.'),
    exchange(('martos', 'Tell me what you need.'), ('martos-lena', 'For once? To finish a sentence before someone decides where I should stand.'), ('martos', 'I will listen.'), narration='She studies the space he has left beside the chair. He had measured it for cover and a clear exit. She measures whether he will let her pass. He has spent years being the reassuring man at a door. It takes an effort to understand that she recognises him as the door itself.'),
    b('martos-lena', 'My independent witness archive liaison receives the original account. Intact. I choose onward accommodation with them. Your people get the operational information we agree to share. They do not get my relatives, my private correspondence or the right to rewrite what you did.'),
    prose('A knock comes before he answers: the agreed attendant reports unfamiliar people asking for Lena by name. Martos moves where he can watch the entrance. He leaves her case in her hands. An interruption makes consent more urgent; it does not supply it.'),
    b('martos', 'We can wait here while I secure the approach. Movement needs your agreement. I can offer a screened route and a safe stop, with a revised route if the first becomes unsafe.'),
    b('martos-lena', 'Explain both. I will choose after I hear them.'),
 ], operation_intro=[prose('The approach must be secured before Lena moves. A successful fight alone does not accept terms for her. If she rejects the proposed arrangement, return to negotiation; the safe receiving room remains the checkpoint.')], aftermath=[
    prose('Lena smooths the fold in her copy with a thumbnail. The paper has softened where she has opened it too often. Martos wants to give her a fresh sheet; he stops himself. She knows this one. She knows where the additions begin.\n\nHe has always found it easier to offer a thing than an explanation: a repaired strap, a hot meal, his own body between someone and an attack. None of those gifts can change the fact that she first saw that body holding a boundary against her. He listens while she checks the recipient and the fallback. When she pauses over the permitted disclosures, he leaves the pen beside her hand.'),
    b('martos-lena', 'You are not promising there will be no danger?'), b('martos', 'I cannot promise that. I can tell you what changes and keep the terms you accept.'),
    b('martos-lena', 'Start with that. Do not make it mean I trust you.'),
 ]),
 'MT-02': dict(title='Before the insignia', location='martos_safe_stop', memory='MT-F01', briefing=[
    prose('The safe stop smells of a kettle heated without enough water. Martos fills it before Lena can reach the sink. She thanks him, then moves the cup he has placed beside the inner-room door to the table facing the exit. He has already carried the spare blanket into that inner room. He has chosen the safest corner, checked the latch and begun arranging a life for her in it.\n\nHe knows this impulse well enough to mistake it for kindness. A room made ready leaves less for a frightened person to decide. It also leaves her with his decision. Lena settles into the chair she chose and keeps her coat on. On the supply shelf, a folded evacuation notice recalls wet boots, a school hall and the satisfaction of being able to tell somebody that a transport really was coming.'),
    b('martos-lena', 'You keep looking at the room behind me.'), b('martos', 'Fewer approaches. I was going to tell you to use it.'),
    exchange(('martos-lena', 'And if I cannot bear another room with no way to see who is coming?'), ('martos', 'Then it is the wrong room.'), ('martos-lena', 'You can say that without explaining the walls to me.'), ('martos', 'I was going to explain the walls.'), narration='A breath leaves her that almost becomes a laugh. He does not try to repeat the effect. She has given him a correction, not an invitation to become familiar.'),
    prose('He takes the other chair. In the earlier hall, shelter had meant an open door and someone who knew where the next transport was. He remembers why he first wanted to be the person standing there.'),
 ], aftermath=[
    b('martos', 'The inner room gives cover. This one gives you a view of the exit. We can secure either. Which do you need?'),
    b('martos-lena', 'This one. Tell me before anyone comes through that door.'),
    prose('He shifts the supplies out of her sightline. When the kettle clicks off, Lena pours her own cup and asks where the spoon is. It is the first thing she has asked him that does not concern getting away from someone. He sets it within reach.\n\nAt twenty, he had liked the exhausted relief on a stranger’s face when an instruction proved true. He had wanted to deserve it. Somewhere between that hall and the transfer cordon, deserving confidence had become expecting it. The work still felt the same in his hands. That was what frightened him now: how little the feeling had warned him.'),
 ]),
 'MT-03': dict(title='Selected', location='martos_safe_stop', memory='MT-F02', briefing=[
    prose('Martos draws two departure windows on the route sheet. He can picture both positions so precisely that for a moment he overlooks the distance between them. His name goes beside the second observation before he notices it already stands beside Lena.\n\nHe scratches it out carefully, making a small dense square. Asking another Ace to do the work is possible. Saying why he needs them will be harder. A request admits that the undertaking is larger than the man who accepted it, and some stubborn part of him still hears that as an attempt to return a gift. The Crow gave him a place. He should be equal to it.\n\nLena watches him darken the square. It begins to tear the page.'),
    b('martos', 'A separate observation is needed. I cannot verify the approach while staying with Lena.'),
    exchange(('martos-lena', 'That took longer to say than the plan took to draw.'), ('martos', 'I wanted to be certain.'), ('martos-lena', 'You wanted to be enough.'), ('martos', 'Yes.'), ('martos-lena', 'I need a second pair of eyes. Yours do not become a pair of people because you mean it.')),
    prose('The crossed-out line brings back selection: a task he nearly finished alone, and the person waiting at its far end who would have paid for that success.'),
 ], aftermath=[
    b('martos', 'A support request must name the leg, the information needed and when to stop. It cannot mean following me and guessing.'),
    b('martos-lena', 'Give them the pursuit details I authorised. My account stays with me.'),
    prose('He separates the route sheet from Lena’s testimony. The empty line is uncomfortable to look at. He leaves it empty until a colleague answers.\n\nIn the unit, he had learned to trust a voice returning over a radio. Later he had used the memory of those voices to justify remaining at a post he knew was wrong. Both things belonged to him: the skill and the excuse. Accepting help now would make this departure safer. It would not settle what he had once called loyalty. He folds the sheet so the unanswered request stays on the outside.'),
 ]),
 'MT-04': dict(title='The order behind the words', location='martos_safe_stop', memory='MT-F03', briefing=[
    prose('Lena opens the account at a list of removals. A copied transport stamp matches a Northline contractor record supplied through her archive liaison. The stamp links a present company to a surviving network. The names beside it concern people the company did not invent.'),
    b('martos-lena', 'This supports the connection. It is not permission to call every armed person from my past a Northline employee.'),
    b('martos', 'Understood.'), b('martos-lena', 'Read the paragraph under the stamp. The one about the guard at the second transfer.'),
    prose('The paragraph describes a broad man moving a chair back inside the boundary. He remembers its weight: almost nothing. One hand had been enough. He had been irritated that its legs caught on the uneven ground, and relieved when the woman stopped arguing.\n\nFor years the scene has existed in his memory as a difficult shift beneath a bad commander. The page gives the difficulty back to the woman. Her mother could not stand. He had made her wait standing. It is so small beside the later transfers that he wants to pass over it, and so exact that he cannot.\n\nHe rests his hands on his knees. Lena has not written about his unease, his private objection, or the sleeplessness afterward. She could not have known those things. He discovers that he resents their absence, then sits with the shame of wanting a witness to include his defence.'),
 ], aftermath=[
    b('martos', 'I held the cordon.'), b('martos-lena', 'You knew what was happening beyond it.'), exchange(('martos', 'By the second transfer, yes.'), ('martos-lena', 'I remember you watching the men who came back. You looked away when I saw you.'), ('martos', 'I had asked for treatment. Voss refused it.'), ('martos-lena', 'I did not ask what you asked for.'), ('martos', 'I kept the route clear for him.'), narration='She nods once. He wants that movement to mean something merciful. It means he has finally answered.'),
    b('martos-lena', 'Then put that in your account.'), b('martos', 'I will. I objected to Voss privately and stayed at the post. Both belong in it.'),
    prose('His statement goes on a separate sheet. Lena reads it, changes one time he remembered incorrectly, and leaves her own account intact. When he signs, the pen catches on the first letter. He has written his name on enough reports to know how to hide that hesitation. He does not start again.\n\nVoss once taught him to distinguish the task from the decision that produced it. He had been grateful for the distinction. It let a capable man remain capable while other people did the thinking he could not bear. Here his hand, his name and the boundary belong to the same person.'),
 ]),
 'MT-05': dict(title='More than he could hold', location='martos_departure', memory='MT-F04', briefing=[
    prose('The receiving door is close enough to see the worn paint around its handle. Martos measures the distance from the sheltered waiting point, then imagines shortening it with strength. Hold the attack, turn, guide Lena through: each part is something he can do. He begins to promise the sequence as if the parts cannot interfere with one another.\n\nLena waits. There is no admiration in the waiting, and that helps him hear himself. He can still remember a commander’s praise arriving before the pain had left his arms. The praise had made an error feel like proof that the next attempt should be larger.'),
    b('martos-lena', 'You stopped halfway through that sentence.'), b('martos', 'I was about to offer more than one pair of hands can do.'),
    prose('Pressure behind his eyes does not mean Rage has taken him. He is standing still, thinking clearly enough to notice how badly he wants the promise to be true. That is the dangerous part he can seldom explain. He does not always lose judgement in a sudden red interval. Sometimes he retains just enough to make a persuasive case for one more effort.\n\nAt twenty-three he had heard Sera ask for the guide position. He had understood her. Later it would have been easier to say he had not heard. He remembers her reaching for the load, trusting that his answer meant what it usually meant.'),
 ], operation_intro=[
    b('martos', 'The protected leg comes first. If strain rises, I report it. An agreed, available colleague can take the precision work while I hold the attack. Without that support, progress and the cost must be checked before we continue.'),
    prose('Calling the warning will not put strength back into his arms. It will give someone else time to take the guide position. If nobody can receive that handover, he will have to stop the movement before the protected group pays for his failing precision.'),
 ], aftermath=[
    prose('Back at the safe stop, Martos places the encounter record beside the route sheet. He leaves the fields for strain, paid resources and protected movement visible. Lena reads them before the next departure is discussed.'),
    exchange(('martos', 'Judge the next leg from what happened. Not from what I meant to do.'), ('martos-lena', 'You say that as if you are asking me to punish you.'), ('martos', 'I am trying to stop asking you to believe me instead.'), narration='The distinction takes him longer than the words. He can endure being blamed. Allowing somebody else’s assessment to change the next task asks for a kind of surrender endurance cannot supply.'),
    b('martos-lena', 'Keep the cost in the account. People who arrive later will need to know why the plan changed.'),
 ]),
 'MT-06': dict(title='The men left behind', location='martos_safe_stop', memory='MT-F05', briefing=[
    prose('Sera’s request is simple: a chair near the window, enough time to speak, and no one waiting outside to recruit her into the next emergency. Martos has put out the tea she used to drink. She asks for water. He brings water without mentioning the tea.\n\nHer presence returns him to the refuge more sharply than a scar would. He remembers listening for her breathing in the room beyond the stove, counting shifts by how long the food would last. He also remembers how often he had answered a question about what she wanted with an explanation of what he could provide. She has come to verify a command link and discuss the escape if she chooses. He repeats that purpose to himself before he speaks.'),
    b('martos-sera', 'I can tell you what I saw. I am not coming back into your unit.'), b('martos', 'I did not ask you to.'),
    exchange(('martos-sera', 'You used to make room beside yourself and assume the rest.'), ('martos', 'There was always room.'), ('martos-sera', 'Yes. You were very good at making a place I had not asked to occupy.'), ('martos', 'I thought it helped.'), ('martos-sera', 'Sometimes it did. That is why this is difficult.'), narration='She takes the glass with both hands. He remembers helping her hold one when she could not. She sees the direction of his glance and deliberately lifts it alone.'),
    prose('She sets a small packet of copied recovery notices on the table. One bears the old command authorisation also used by Northline. Before she turns it over, she asks which version of the escape he has given Lena.'),
 ], aftermath=[
    b('martos-sera', 'You got me out. You opened the side holding room. That is true. There were people beyond the closed partition when we left.'),
    b('martos', 'I could not reach them before the withdrawal.'), b('martos-sera', 'And some had been within reach earlier, while you were guarding transfers.'),
    prose('He could describe the weight he carried out, the wounded arm around his neck, the distance he crossed while the route narrowed behind them. Every detail would be true. None would answer her.\n\nSera turns the recovery notice toward him. This is what she can verify: Voss’s authority continuing into the recovery orders. Beyond it lie people neither of them can account for. In the refuge he had sometimes imagined returning with enough strength to open every locked room. The fantasy made loss bearable by turning it into unfinished work. It also let him postpone the earlier question: why had he kept those doors closed while he still had the choice?'),
    b('martos', 'Tomas was alive when I last saw him. I have no later record.'), b('martos-sera', 'Keep it that precise. We do not get to bury him in a sentence because we do not know.'),
 ]),
 'MT-07': dict(title='A commander with a name', location='syndicate_hq', memory='MT-F06', briefing=[
    prose('The executive room is quiet enough for Martos to hear the folder settle on the desk. He has arranged the authorised operational pages above the private account. The Crow asks which packet he may use, and Martos indicates it without needing to be reminded twice.\n\nHe is relieved to be here. The relief shames him more than the tension at Lena’s table. Here an objective will be named, its importance weighed, and his part made clear. He knows what an answer should look like. Lena asks what his answers cost other people. The Crow asks whether he can deliver them.\n\nHe has never confused the two questions. He has chosen to let the second come first.'),
    b('crow', 'Voss has kept the useful parts of his former authority. He will try to make you treat this as a private dispute.'), exchange(('martos', 'It is your assignment. He cannot take it from you by making it personal.'), ('crow', 'He can waste your attention. Do not give him that much authority.'), ('martos', 'No, master.'), narration='The correction settles him. That ease is part of the allegiance too: the wish to hear another voice identify the thing that matters, and then put everything he has behind it.'),
    prose('On his first visit, Martos had stood beside the same desk with borrowed transport money in his pocket. He had wanted a promise that would survive an inconvenient failure. He had not yet decided how much obedience such a promise could buy.'),
 ], operation_intro=[prose('Verify the present recovery notice and return through the authorised reporting route. A recovered document proves only its own source and handling; it cannot authenticate every claim in Voss’s network.')], aftermath=[
    b('crow', 'Your undertaking and my objective currently coincide. Keep both accurately.'), b('martos', 'Yes, master. The records remain unaltered. That includes my service under him.'),
    prose('The title comes without hesitation. He remembers rehearsing his first acceptance in the transport back to the refuge, trying to describe a bargain to Sera without admitting how badly he had wanted more than treatment for her. He had wanted a place for himself.\n\nThe Crow has not asked him to conceal his service under Voss. Martos takes pride in that. Then he thinks of the unaltered account moving into a strategy for weakening Northline, and recognises how neatly truth can serve power. Recognition does not loosen his loyalty. He straightens the authorised packet and waits for the next instruction.'),
 ]),
 'MT-08': dict(title='The promise kept', location='martos_safe_stop', memory='MT-F07', briefing=[
    prose('Sera brings the old notices in a folder whose elastic has stretched. Martos reaches for it, then lets her undo the fastening herself. He remembers the treatment figures down to the last increase. She remembers the receptionist who used to call her by name, the cancelled journey, the clothes she could finally fasten without help.\n\nFor him, the papers describe a commander keeping his word. For her, they describe years of living inside a body that needed care. He has spoken of those years so often as the reason he serves the Crow that he has begun to forget they did not happen to him.'),
    b('martos-sera', 'You remember the cost at the bottom. I remember having to ask whether the next appointment still existed.'), exchange(('martos', 'It did. He made sure it did.'), ('martos-sera', 'I know who paid. I also know who went to the appointments.'), ('martos', 'I should not have made it sound simple.'), ('martos-sera', 'It was simple to thank him. The rest is yours.')), b('martos-sera', 'Yes. Read the second notice too. Neither of us lived on one sentence.'),
 ], aftermath=[
    b('martos-sera', 'He kept his word to me. I know. I lived because of it.'), b('martos', 'That matters.'), exchange(('martos-sera', 'It does. You made it answer every other question.'), ('martos', 'I would still serve him if the account were settled tomorrow.'), ('martos-sera', 'It has been settled for years.'), ('martos', 'I know.'), narration='There it is, without a bill to hide behind. He does not believe his obedience has a balance that can reach zero. He has made it part of being a man whose word survives inconvenience, and he cannot imagine withdrawing it without hearing Voss explain why a promise no longer applies.'),
    prose('She folds the notices along their old creases. Martos watches her put away the evidence he has been using to tell his life. Gratitude has never obliged her to follow him. It has not even obliged her to remain grateful in the form he prefers.\n\nHe could tell her that the Crow has been good to them. The word them opens easily around Sera and closes before it reaches the people harmed by his assignments. He knows where the boundary is. He has held worse boundaries without needing anyone to draw them on the ground.'),
    b('martos', 'You owe him no service.'), b('martos-sera', 'Then stop explaining mine when I disagree with yours.'),
 ]),
 'MT-09': dict(title='What service costs', location='martos_safe_stop', memory='MT-F08', briefing=[
    prose('The liaison’s warning arrives before the case leaves the table: the first receiving window is compromised. Lena sits down again, carefully enough that Martos knows she had already begun imagining being gone. Outside, a supplier waits to learn whether Northline’s pressure has made another ordinary delivery unsafe.\n\nMartos knows the shape of that hesitation. A man with a van cannot simply decide that he is brave. He has tomorrow’s route, people expecting wages, a vehicle somebody can refuse to service. Martos has stood inside businesses while those calculations changed around him. Then he had called it securing a collection. Today he stands on the other side of a door and wants the delivery to come through.'),
    b('martos-lena', 'You know what it means when someone makes the safe route belong to them.'), b('martos', 'Yes.'), b('martos-lena', 'From being stopped, or from stopping people?'),
    prose('The answer belongs to a collection house he secured in the Crow’s service. There had been no false humanitarian name on that order. He had once treated that as the decisive difference.'),
 ], aftermath=[
    exchange(('martos', 'I knew the collection would close the business. I let the staff leave. Then I secured it.'), ('martos-lena', 'For him.'), ('martos', 'Yes.'), ('martos-lena', 'Would you do it again?'), ('martos', 'If he gave me that order, yes.'), narration='He does not raise his voice to make the answer stronger. He wishes she had asked whether he enjoyed it. That would have been an easy no.'),
    b('martos-lena', 'And the man who ordered it told you the truth. What did that give the owner?'),
    prose('The supplier’s receipt waits outside the door. Martos looks at the line where somebody will sign if the delivery can proceed. He wants to tell Lena about order: that unclaimed routes do not stay free, that another organisation would take what the Syndicate left, that the Crow at least stands behind the people carrying out his will.\n\nHe has used each argument before. He believes them. He also knows none explains why this particular owner should lose his livelihood to make Martos’s world dependable. The strongest part of his answer is the part he would be ashamed to offer her: this is the leader he trusts, and he will accept doing wrong before he accepts abandoning him.'),
    b('martos', 'Nothing that answers the loss.'), b('martos-lena', 'Keep that answer when the next order is easy to understand.'),
 ]),
 'MT-10': dict(title='The other Aces', location='syndicate_hq', briefing=[
    prose('In the cross-branch operations room, Mavis puts a fresh observation beside the contractor list. She has seen two vehicles exchange the same route authority; she has not seen Lena’s personal account.'),
    b('mavis', 'The second vehicle waits after the first leaves. You marked it as a reserve. It watches the departure.'), b('martos', 'I need you on the protected leg. I was going to keep the pursuit detail out of your brief.'), exchange(('mavis', 'Then you were going to send me in blind. Very protective.'), ('martos', 'I wanted to keep the risk with me.'), ('mavis', 'You kept the information. The risk travels.'), narration='She leaves him time to see it. Mavis does not look pleased at having corrected him. She looks as if she would prefer him to use the correction so she can get on with the work.'),
    b('martos', 'You get the authorised pursuit packet and the stop condition. Will you take that leg?'), b('mavis', 'If I am available at departure, yes. Confirm it then. Do not put an absent person in the plan.'),
    prose('Camila takes the route sheet next. She draws a box around a time Martos has treated as confirmed.'),
    exchange(('camila', 'That is a booking, Martos. It tells us somebody paid. It does not tell us who will arrive.'), ('martos', 'I treated the alternate as confirmed.'), ('camila', 'Twice. You were very consistent.'), narration='There is a brief competitive brightness in her expression, then she turns the sheet so he can follow the correction. He likes being shown where a practical assumption fails. It is less comfortable when Lena does the same thing to a conviction.'), b('martos', 'Then I have one verified route and an unverified fallback.'), b('camila', 'Now we can work. I can authenticate the receiving signal and analyse the change. I cannot promise a clear road.'),
    prose('Elias waits until the operational copies are separated. He has a cover arrangement for the departure and no reason to receive Lena’s private correspondence.'),
    b('elias', 'A discreet arrival I can arrange. A stirring account of the man who saved his accuser would attract precisely the wrong attention.'), b('martos', 'No account like that. The recipient gets my signed participation statement. Cover gets the agreed movement details.'), exchange(('elias', 'Good. I can arrange a discreet arrival. I cannot stop a heroic little anecdote growing legs once you give it a room.'), ('martos', 'I do not want an audience.'), ('elias', 'A useful beginning. Most people say that while checking whether the audience has arrived.'), narration='Elias lifts the cover sheet, leaving the personal account untouched. Martos has known him long enough to hear the serious care beneath the flourish. He has not asked for a confession, and Martos owes him no performance of one.'),
    prose('Later, in a separate authorised headquarters meeting, Sylvanis examines the limit Martos has asked him to respect. No historical file is on the table.'),
    b('sylvanis', 'A corridor I must leave boring. You make such small requests with such enormous solemnity.'), b('martos', 'The receiving corridor stays usable. No engagement through the protected departure. I do not have authority over your other business.'), b('sylvanis', 'And if I am offended by this dreadful lack of ambition?'), b('martos', 'We use the fallback. I will not stake her passage on your mood.'),
    prose('Sylvanis smiles. Martos keeps his hands open. Restraint here is neither victory over him nor proof that he has become safe; it is a practical requirement that can be accepted, refused or planned around.'),
 ], operation_intro=[prose('Validate current movement, agreed cover and receiving authentication. Each contribution has its own scope. Private history is optional disclosure; operational prerequisites must be available on the required route.')], aftermath=[
    prose('The plan returns with corrections in three hands. Mavis has stripped an unnecessary phrase out of the pursuit brief. Camila has written a question beside an uncertain time. Elias has made the cover explanation shorter. Martos can tell who made each alteration before he reads the name.\n\nThis is another reason he stays. Service to the Crow has given him people whose competence he can rely on, people who can refuse his methods without ceasing to stand beside him. He knows how easily that feeling can become an excuse. He has once already belonged to a good table inside a bad institution. Knowing the resemblance does not make him rise from this one.\n\nHe leaves their conditions visible. For this departure, at least, no one will have to disappear into the promise he made alone.'),
    b('martos', 'I will confirm the roles before we commit. If one changes, I report the changed plan.'),
 ]),
 'MT-11': dict(title='An order without disguise', location='syndicate_hq', briefing=[
    prose('Voss’s offer arrives as an authenticated transcription. Martos recognises the order of its arguments: necessity first, mutual advantage next, the unnamed people to be spent somewhere near the end. It is the rhythm in which Voss used to explain why a difficult duty must fall to dependable men.\n\nThe proposed concession could make Northline’s other routes easier to contest. Protection would end before the receiving window. Lena would be returned. Martos reads that sentence without letting his eyes move ahead to the benefit. The Crow has the same page before him. Martos waits for his judgement and discovers that waiting is a decision he is still capable of making.'),
    b('martos-voss', 'You have always understood the value of a workable command. Return the witness and the matter can become an arrangement between people equipped to settle it.'),
    prose('The Crow reads the authenticated transcription in the executive room. He checks the proposed concession against the value of exposing the network.'),
    b('crow', 'He offers a gate he will still be able to close. The record gives me more. The original objective stands.'), exchange(('martos', 'Lena will be told the threat. She is not to be offered as part of it.'), ('crow', 'You are stating the standing order.'), ('martos', 'Yes, master.'), narration='It is relief he feels, immediate and bodily. The order has not changed. He can keep faith with both promises. He dislikes knowing how much he needed the Crow to make that possible, and more than that he dislikes the thought of needing anyone else’s permission.'), b('crow', 'Then make the delivery useful. Do not confuse my reasons with hers.'),
 ], aftermath=[
    prose('At the safe stop, Martos gives Lena the authorised, truthful route warning. He describes the attempted bargain without handing over private headquarters material.', 'safe_stop'),
    exchange(('martos-lena', 'Your employer refused because keeping me is more useful.'), ('martos', 'Delivering you safely. Yes.'), ('martos-lena', 'And you waited to hear which would be useful.'), ('martos', 'I reported the offer.'), ('martos-lena', 'That is not a different answer.'), narration='He could tell her he had been ready to argue. He had been. He cannot honestly make an intention to argue stand in for a decision to disobey.'), b('martos', 'That was his reason. I cannot give you a different one.'), b('martos-lena', 'I expect my recipient and my account. Tell me if either changes.'),
    prose('They check the fallback. Lena asks practical questions because she intends to live beyond this conversation. Martos answers each one. He is grateful that she does not keep pressing, and aware that she has no duty to spend her strength examining him.\n\nHe will not leave the Crow. The certainty remains beneath the discomfort, solid as the desk on which the order was given. Once he imagined that certainty would spare him the fear of another betrayal. Now he can see whose fear has been left outside it. He checks the receiving time again. It is something he can still do for her.'),
 ]),
 'MT-12': dict(title='Terms before departure', location='martos_safe_stop', briefing=[
    prose('Lena has repacked the case. Martos notices the change because the strap no longer catches on the corner of the table. There is less in it than when they first met. She has chosen what she is willing to carry into the next part of her life. He does not ask what she left out.\n\nThe papers between them have been checked enough times for him to resent checking them again. Then he remembers who gets to return to headquarters when this is over, and who must trust the next door to open. He sits down. He will read the terms at her pace.'),
    b('martos-lena', 'Read it back without calling any of it standard.'), b('martos', 'You own the records. The independent witness archive liaison receives them intact and arranges onward accommodation with you. Our operational copies contain only what you permitted. A changed recipient requires your agreement.'),
    b('martos-lena', 'And Voss?'), b('martos', 'Stopping the attack serves this departure. If he is defeated and a separate secured transfer is possible, an authorised regional custody team can receive him. Pursuit cannot replace your delivery.'),
    prose('The support sheet lies separately. Mavis can accept the extraction leg if present; Camila verifies the receiving signal; Elias maintains the agreed cover. Sera has not accepted a combat role. A request to consult her cannot make her the only way Martos can recognise his limits.'),
    exchange(('martos', 'If my precision starts to go, I tell them. I hand over to someone who has agreed and is there.'), ('martos-lena', 'Even if you think you can finish?'), ('martos', 'Especially then.'), ('martos-lena', 'I do not want to be the next person in the story about how much you can carry.'), ('martos', 'You will not have to make that story kind.'), narration='He cannot ask her to believe he has learned enough. He can make it possible for the others to act before belief becomes necessary. For once, a limit feels like something he can offer instead of something he must conceal.'), b('martos-lena', 'Those are terms I can check. Confirm them against what people actually agreed.'),
 ], aftermath=[
    prose('The last check is attendance. Names are answered by people, not filled in by Martos’s hope of seeing them. Each accepted role keeps its conditions. He has spent years finding reassurance in the weight of a task placed wholly on him; the gaps between the names feel unfamiliar. They are where someone else will act.\n\nLena closes her case after her copy matches the terms. She asks him to move so she can get past the table. He steps aside at once. There is no forgiveness in the small passage they make together. There is enough room for her to choose it.'),
 ]),
 'MT-13': dict(title='What he holds', location='martos_departure', briefing=[
    prose('At the departure line, Voss appears beyond the route to the receiving area. Martos can see him clearly. The protected door is closer and less satisfying to watch. He checks it first.'),
    exchange(('martos-voss', 'You still need a voice to tell you where to stand. I gave you that once.'), ('martos', 'You gave orders.'), ('martos-voss', 'And you followed them. Does your new commander know how well?'), ('martos', 'He knows what I did.'), ('martos-voss', 'Then we have at least one judgement in common.'), narration='Martos feels the answer strike where he had hoped the years of service would protect him. Voss does not need to lie about everything to be his enemy.'),
    b('martos', 'You do not get to choose the task.'),
    prose('His voice becomes quieter. Beyond Voss is the old temptation: finish the man, end the argument, make one overwhelming act supply a verdict on everything that came before. Behind Martos is a person who needs a door kept usable.\n\nHe thinks of Sera trying to raise her arm, then refuses the relief of turning that memory into punishment he can deliver to Voss. The failure in that extraction was his own. Rage can give him strength here and take precision in return. It cannot choose which obligation he means to keep.\n\nThe Crow’s order is clear. Lena’s terms are clear. He faces the attack because the two still point in the same direction. Nothing about that alignment proves they always will.'),
 ], operation_intro=[
    prose('Hold the departure line while Lena and the case reach the receiving door. Report strain early enough for the agreed support to take over. Keep enough strength to protect the movement; Voss cannot be pursued at the cost of the people still waiting to leave.'),
    b('martos', 'The case and Lena reach the agreed receiver. Confirm movement before anyone follows Voss.'),
 ], aftermath=[
    prose('The departure desk is too low for him. He crouches beside it rather than lift it while the handover forms are spread out. His hands want a heavy task, something simpler than waiting for another person’s answer.\n\nLena’s receiving confirmation and Voss’s custody result occupy separate lines. Martos keeps them separate in his thoughts as well. He has spent much of his life allowing the thing he did well to explain the thing he did badly. No amount of force at the departure line can tell him who has reached the other side. He listens until there is an answer he can actually report.'),
 ]),
 'MT-14': dict(title='After the handover', location='martos_receiving', briefing=[
    prose('The receiving space contains ordinary things: a spare chair, a mark where a cabinet used to stand, a cup left to dry beside the sink. Martos had imagined a threshold after which the work would feel finished. Instead there is another room, and people with further questions.\n\nLena keeps her personal copy while the liaison confirms the handover. She speaks about onward accommodation without looking to Martos to supply the answer. He is relieved. He is also unexpectedly bereft of a task. The two feelings can occupy him at once. She is not his responsibility in the same way now, and she has never been his possession.'),
 ], aftermath=[
    b('martos-lena', 'Would you have brought me here if your orders had been different?'), exchange(('martos', 'I gave you my word.'), ('martos-lena', 'Would you break with him to keep it?'), ('martos', 'I would ask him to let me keep it.'), ('martos-lena', 'And if he did not?'), ('martos', 'I will not leave him.'), narration='He says it quietly because volume would only make the answer harder for her to refuse. It is the most faithful thing he can tell her and the least reassuring. She draws her case closer.'), b('martos-lena', 'Then do not ask me to call you safe.'),
    prose('He has no answer that makes her safe from every future version of his obedience. Lena turns toward her liaison. She does not thank him for being honest about the limit. Honesty is information she can use, and she uses it to decide where the next conversation belongs.\n\nMartos lets her go without following. He wants to be remembered as the man who brought her through. He knows he will also remain the man at the cordon. For once he does not ask which memory will count more.'),
    prose('At a later private appointment, Sera looks at the route’s actual cost rather than a story about how close it came to being worse.', 'safe_stop'),
    b('martos-sera', 'You can tell me you needed help without making it my job to say you have changed.'), b('martos', 'I needed help. I should have put the limit in the first plan.'), exchange(('martos-sera', 'That is something you can do next time. The rest of your choices remain yours.'), ('martos', 'I am staying in his service.'), ('martos-sera', 'I did not think you were announcing your retirement.'), ('martos', 'I wanted you to know I was not asking you to approve it.'), ('martos-sera', 'Good. Then we can finish the tea.'), narration='The ordinary invitation almost undoes him. Disagreement has not made her vanish. He sits without trying to purchase the moment with a promise about the man he will become.'),
    prose('At headquarters, he reports in the executive room. The signed account still names his complicity; the mission report identifies the receiving result and all recorded costs.', 'executive'),
    b('martos', 'The report is complete within the evidence we have, master. No claim about the old detainees beyond the known record.'), b('crow', 'Northline’s connections are now exposed to pressure. I will decide how to use that. Keep the limits in the working report.'),
    prose('The Crow will use the exposed connections to extend his reach. Martos understands the gain. He also understands that the unaltered statement names a man the Crow continues to employ. There is no need to pretend either fact has escaped his notice.\n\nHe waits to be dismissed, already sorting the remaining obligations in his mind. He would protect this commander with his life. He would enforce an order that left strangers poorer, frightened or without a place, and try to call the restraint in his method the part that belonged to him. The thought is uglier now that he has stopped hiding its recipients behind the word cost. It has not become less true.\n\nWhen he answers, the title is unchanged. His loyalty has survived the story he now tells accurately about himself.'),
    prose('Later, alone at a shared table in the headquarters members lounge, he takes the back off the watch he promised to return. He has already placed the help he received in the report. No one is waiting here to tell him what it means.', 'kitchen'),
    b('martos', 'The spring is sound. I fitted the wrong pin.'),
    prose('He replaces the pin rather than forcing the case closed. The owner will get an accurate explanation with the repaired watch. It is an ordinary obligation, small enough to keep without claiming that keeping it answers Lena.'),
 ]),
}

MEMORIES = {
 'MT-F01': dict(title='A door that opened', age=20, era='martos_conventional_age20', location='martos_unit_mess', text=[
    prose('Martos’s memory — age twenty, conventional service. Rain has driven families toward a school hall used for evacuation. He has been enlisted long enough to know that good intentions do not dry blankets or tell a waiting family where its missing transport went.'),
    b('martos-tomas', 'Your sleeve is soaked. Again.'), b('martos', 'It was dry when I enlisted.'), b('martos-tomas', 'A successful trial, then.'),
    prose('At eighteen, he had wanted work in which strength could have a purpose larger than being noticed. Training gave him instructions he could finish and people who noticed when he finished them properly. By twenty he liked the unremarkable parts best: a strap adjusted before it broke, supplies already there when somebody reached for them, the weight taken from a tired colleague without a speech about it.\n\nThe school hall offers no grand test. Water gathers beneath the coats hung on chair backs. People ask the same question because the first answer was uncertain, not because they failed to listen. Martos learns to stop saying soon when he means he does not know. Every time a transport arrives where he said it would, he feels a small piece of the world become reliable.\n\nHe begins to want that reliability the way other men want praise. There is nothing false about the relief in the hall. That will make the memory hard to surrender when he needs evidence that service must, somewhere beneath its later orders, still be good.'),
    exchange(('martos-sera', 'The woman by the doors will not board without her father. Find out which transport has him.'), ('martos', 'The group is ready.'), ('martos-sera', 'She is part of the group.'), ('martos', 'I will check.'), ('martos-sera', 'Thank you. And eat something when we are done. You are becoming very solemn about a stack of blankets.')),
    prose('The evacuation task is bounded: keep the sheltering group protected, open the marked onward leg and confirm the handover. The family decides whether the proposed movement meets its needs. A needless fight outside would leave the door unwatched.'),
    b('martos', 'I will stay at the door. Tell me when the next group is ready.'),
 ], after_encounter=[
    prose('The receiving attendant returns the signed handover list. Inside the hall, a woman finds her father on the onward list. Martos moves a supply box so they can sit together while they wait.'),
    b('martos-sera', 'You missed the hot meal.'), b('martos', 'Tomas saved me one.'), b('martos-tomas', 'I saved you food. Temperature was outside the agreement.'),
    prose('Later at the mess table, Tomas pushes the saved food toward him with the air of a man presenting a technical achievement. Martos takes a careful mouthful. It is cold enough to prove that Tomas has kept it rather than found another portion. Sera laughs when he continues eating without complaint.\n\nHis shoulders ache. Somebody has left a cup for him. The people from the hall are accounted for beyond the door he held. He does not yet divide these comforts from the institution that made the work possible. He belongs to the table, the unit and the purpose together. It will be years before he can imagine losing one without losing all three.'),
 ]),
 'MT-F02': dict(title='The person at the far end', age=22, era='martos_selection_age22', location='martos_training_yard', text=[
    prose('Martos’s memory — age twenty-two, special-forces selection and a later rescue in the same training interval. He reaches the end of the exercise with enough breath left to answer clearly. He has practised that: arrive useful, not merely arrive. When the evaluator asks who confirmed the last person through, he turns to the empty place where Tomas should be.\n\nThe embarrassment is fierce because he knows the answer before anyone gives it. He had wanted to be selected for judgement, not merely strength. Instead he has completed an impressive version of the wrong task. Sera is waiting farther back, one hand raised to stop the exercise. She does not lower it when he looks at her.'),
    b('martos-sera', 'You gave me the signal before Tomas answered. I stopped the exercise.'), b('martos', 'I thought he was behind me.'), b('martos-sera', 'That was the mistake. Not being slower than you.'),
    prose('He repeats the exercise with the group. Waiting for an answer takes longer than guessing it. So does admitting to Tomas that he had treated the man’s position as a detail that would sort itself out. Tomas lets him finish, tests the clasp on his equipment, and asks whether Martos would like to carry an imaginary technician through the next exercise as well.\n\nThe joke makes correction bearable without making the mistake smaller. This is how the unit wins him: not through speeches about brotherhood, but through the chance to be wrong in front of people who still expect him at supper. He wants to deserve their confidence. He is proud when the training begins to reward the person who can bring everyone through rather than the first body across the line.'),
    prose('Later, in operator equipment earned through that training, the team attempts a bounded rescue. The route changes before the protected group can leave. Sera catches his assumption that the first exit remains usable.'),
    b('martos-sera', 'That answer is old. Ask again.'), b('martos', 'New route. Confirm the last person before I move.'),
 ], after_encounter=[
    prose('After the confirmed rescue, the team eats in the mess. Tomas has repaired a clasp with more care than he is willing to admit. Martos checks it twice and receives a bread roll thrown gently at his chest.'),
    b('martos-tomas', 'It works. I have witnesses.'), b('martos', 'I was checking the bread.'),
    b('martos-sera', 'Next time tell me what you do not know before you make a plan around it.'), b('martos', 'Next time I will.'),
    prose('Tomas passes him the repaired clasp to put away. Sera asks whether he is cooking tomorrow and, before he can answer, tells him which pot somebody has already ruined. They make plans as if another meal is an ordinary certainty. Martos finds himself checking what is left in the stores.\n\nHe has earned his equipment and his place. The rescue has required the training, the correction, and answers from other people. He knows that. But belonging begins to gather its own authority around these facts. When later orders change the work, leaving will feel less like refusing a commander than walking away from the people who still need him to be dependable. He will make that feeling do work no feeling should be allowed to do.'),
 ]),
 'MT-F03': dict(title='The boundary', age=24, era='martos_deployment_age24', location='martos_unit_lockers', text=[
    prose('Martos’s memory — later deployment, age twenty-four, before desertion. The order calls the removal a protective cordon. A woman named Ilen asks to take a chair to her mother, who cannot stand in the waiting line. Martos moves it back behind the boundary. He tells her supplies will be provided at the next stop.'),
    b('martos-voss', 'The boundary stays closed. Individual exceptions make the whole movement impossible.'),
    prose('The supplies do not arrive while he is there. Ilen tries to lift the chair again and stops when he turns toward her. He has not raised a hand against her. He notices himself using that fact for comfort. Another civilian helps her mother sit on a case, knees drawn awkwardly up beneath her coat.\n\nMartos could carry the chair through. He is strong enough; there is space. What stops him is the thought of making an exception where others will see, then having to defend it to Voss, then returning to a post where the rest of the team must work around his refusal. Each consequence seems reasonable by itself. Together they keep an old woman on a case.\n\nHe tells himself the next stop will be better supplied. He has no confirmation. When Ilen asks again, he repeats the answer more slowly, as if the missing certainty were in her hearing.'),
    prose('By the second detainee transfer he has seen people return injured from questioning. A medic’s request has been refused. He understands enough to know the movement is intended to hide what happened, not simply move people out of danger.'),
    b('martos', 'They need treatment. Where are they being received?'), b('martos-voss', 'That is being handled above you. Your post is the transfer.'), b('martos', 'I need confirmation.'), b('martos-voss', 'You have my assurance. Do you intend to leave your team without its guard?'),
    prose('He stays. The familiar relief follows: a decision is made, a position assigned, the next hour filled with things he knows how to do. He turns people back and keeps the vehicle entrance clear. Injured detainees pass within reach. He has already asked the question that tells him he understands what he is seeing.\n\nVoss has not forced him to forget his objection. The commander has given him permission to carry it privately while continuing the work. Martos accepts that permission. It lets him remain, in his own estimation, the sort of man who objects. To anyone trying to reach the injured, he remains the man who prevents it.\n\nHe thinks of the team beyond his post, of Sera returning to limited service after the earlier extraction injury, of how much another failure would ask of them. He uses his concern for people he knows to close the argument against people he does not.'),
    b('martos-sera', 'You saw enough to ask. You are still standing here.'), exchange(('martos', 'Yes.'), ('martos-sera', 'Then move.'), ('martos', 'If I leave the post, they send someone else.'), ('martos-sera', 'You do not know that.'), ('martos', 'Voss will not stop the transfer.'), ('martos-sera', 'I am speaking to you.'), narration='He looks past her to the vehicle, where somebody is waiting for his signal. He gives it. Her silence afterward contains no agreement.'),
    prose('Ilen’s name remains on the removal sheet. The later column has no entry. Martos stands by the departure after the last transport has gone, with his objection still unanswered and his part in the work complete. The empty column tells him nothing about her safety.'),
 ]),
 'MT-F04': dict(title='The load shifts', age=23, era='martos_overmutation_age23', location='martos_training_yard', text=[
    prose('Martos’s memory — age twenty-three, an earlier deployment extraction. The obstruction gives a little under his hands. Rage has increased what he can move, and the movement rewards him with a dangerous certainty: more effort is still possible. He can see the route opening. He can picture everyone beyond it.\n\nHis fingers do not settle where he expects them to. He corrects the grip and calls that correction control. Sera asks for the guide position. If he gives it up, someone else will have to come nearer the weight. He turns this into a reason to keep both tasks, though she is already close enough to be hurt by his mistake.'),
    b('martos-sera', 'Your hand is shaking. Give me the guide position.'), exchange(('martos', 'I can finish.'), ('martos-sera', 'That was not what I asked. Give me the movement.'), ('martos', 'One more lift.'), narration='He hears the refusal in her breathing. For a moment he is angry at being doubted while he is trying to spare her work. The anger is ordinary. What he decides to do with it will not be.'),
    prose('He continues. The load shifts before he registers Sera’s position. She is struck while correcting the movement. He lowers the weight and hears her trying to tell the others where to stand through a breath that will not come evenly. Her arm hangs where she cannot make it useful.\n\nThere is a dreadful instant in which he wants her to say she is all right. He sees how much work that would ask of her: pain, assessment, and reassuring the man who caused it. He calls for a new handover before she can offer the lie. The protected group is still waiting. His strength remains available, but it has made another person part of the burden he claimed he could carry alone.'),
    b('martos', 'Sera is hurt. I caused it. New handover; she does not carry the next leg.'),
    prose('The admission comes late enough that it cannot protect her from the first cost. It can still change how he conducts the remaining extraction. Defeating resistance without moving the protected group would leave the task incomplete.'),
 ], after_encounter=[
    prose('In the infirmary afterward, Sera’s arm is supported. Voss reads the output figures before the injury note. Martos remains standing until she tells him the chair is not a test.'),
    b('martos-voss', 'You exceeded the expected capacity. That is the result command needs.'), b('martos', 'Record the loss of precision and her injury beside it.'), b('martos-voss', 'We can discuss recommendations separately.'),
    prose('The recommendation is separated. The praise circulates. Martos sees his capacity described in a line that can be passed from desk to desk without carrying Sera’s face with it. He goes to the infirmary and repairs the loose latch on a cabinet because it is something his hands can do correctly.\n\nShe watches him test it three times. He is waiting to be told the repair is enough, though he would deny that if she asked. Her recovery will take time and limited duty. There is no object in the room he can mend in exchange.\n\nHe begins noting the physical warnings: the grip corrected twice, the delayed answer, the growing effort required for a small precise movement. He recognises the signs. The harder work will be believing they still matter when somebody praises how much he can endure.'),
    b('martos-sera', 'Next time do not wait until honesty is all you can offer.'),
 ]),
 'MT-F05': dict(title='The side holding room', age=24, era='martos_desertion_age24', location='martos_unit_lockers', text=[
    prose('Martos’s memory — age twenty-four. Sera has been wounded during a failed operation, separately from the earlier extraction injury. Voss gives the withdrawal order with the same controlled attention he brings to every movement: the remaining detainees and witnesses are to be eliminated; the wounded are to be left. He presents it as protection for the people who can still be saved.\n\nMartos waits for the qualification. A different transport, another receiving point, an instruction that makes the words mean less than they do. Voss supplies none. The old habit of waiting for command to resolve the difficulty remains in Martos after the difficulty has become command itself.\n\nHe looks toward Sera. He knows that her being there makes refusal easier. He knows there were people without a friend at his shoulder in the earlier transfers. The knowledge does not make this refusal false. It makes it late.'),
    b('martos-voss', 'You know what happens if this account leaves with them.'), b('martos', 'I know what you are ordering.'), b('martos-voss', 'Then carry it out.'), b('martos', 'No.'),
    prose('He is frightened and deliberate. Rage has not made the decision. He has time to imagine being named a deserter, being hunted, leaving people in the unit to explain what he has done. None of it turns the order into something he can carry out.\n\nHe opens the reachable side holding room. The people inside pull back from him before anyone comes forward. He has been part of the arrangement that kept them here. A civilian refuses to leave until another person is brought from behind him, and Martos almost answers with the commanding tone he has used all evening. He stops. He explains where the open route is. Then he waits for an answer.\n\nHe has not become harmless by changing sides of a door. He can hold it open long enough for them to decide whether to pass.'),
    b('martos-sera', 'There are people past the partition.'), b('martos', 'I cannot open that route in time. I can take this group and you.'),
    prose('Martos supports wounded Sera toward the exit while the reachable group gathers beyond the open holding-room door. Behind the partition, somebody calls again. He cannot get to them before this route closes. Tomas was alive when he last saw him; he has no answer to the question Sera asks now. He keeps moving with the people he can reach.'),
 ], after_encounter=[
    prose('At the refuge, Sera is put into a chair that does not fit under the table. Martos moves the table. Only afterward does he notice that he is still wearing equipment belonging to the unit he has deserted.'),
    b('martos-sera', 'Put down what you can. You are making the floor shake.'), exchange(('martos', 'There is another way I should have found.'), ('martos-sera', 'Tonight? Or before tonight?'), ('martos', 'Both.'), ('martos-sera', 'Then keep them separate. You could not open everything tonight. You could have stopped guarding it sooner.'), narration='The equipment lies beside the chair. Without its weight he feels oddly unbalanced, as though standing upright ought to require another order. He has broken command’s hold over this decision. He has no idea yet how to live without someone telling him what the next decision should be for.'), b('martos-sera', 'I am not asking you to carry any more tonight. Sit here until you can hear that.'),
    prose('He takes off the remaining equipment. At the refuge, nobody can tell him how many days the supplies will last. Sera is alive in front of him; people have escaped through a door he opened; others remain beyond his knowledge. He cannot arrange those facts into a result that lets him sleep.\n\nHe has refused an order, not discovered that all his obedience was involuntary. That distinction will be harder to carry than the equipment. He begins with the small tasks the room actually needs, moving a basin within reach and asking whether Sera wants the lamp left on. She says no. He turns it off.'),
 ]),
 'MT-F06': dict(title='Terms at the desk', age=25, era='martos_recruitment_age25', location='martos_refuge', text=[
    prose('Martos’s memory — age twenty-five. Fugitive security work pays a few nights at a time. He knows which job will cover food and which might cover transport if the employer pays when promised. He cooks before a shift and leaves the pot where Sera can reach it. When he comes back, a care appointment has been cancelled: the provider is frightened of the old unit’s recovery inquiries.\n\nThere is no superior to appeal to. There is no useful act of strength. He can stand outside the closed office until morning and the appointment will still be cancelled. Independence, which ought to feel like having escaped Voss, begins to feel like being unable to guarantee the next week to anybody.\n\nSera is looking for alternatives. He hears the uncertainty in each one and starts calculating another shift. He trusts exhaustion because it is a price he knows how to pay. Uncertainty asks him to admit that willingness is not a resource.'),
    b('martos-sera', 'You cannot promise a month by refusing to sleep for a week.'), exchange(('martos', 'I can cover tonight.'), ('martos-sera', 'And tomorrow you will come home too tired to hear what I have arranged.'), ('martos', 'I hear you.'), ('martos-sera', 'You hear another thing you think you must fix. Sit down before you promise anything else.'), narration='He sits. The relief is immediate, and he resents how much that tells her.'), b('martos-sera', 'Leave tomorrow’s shift alone for five minutes. We have to talk about next month.'),
    prose('A Syndicate intermediary brings a bounded offer and transport for an authorised headquarters appointment. At the executive desk the Crow remains concealed. He has a dossier from that channel: known service, the refusal, capabilities and the people whose support Martos is trying to maintain. He does not know every private conversation at the refuge.'),
    exchange(('crow', 'You helped those operations function before you refused the last order. I am not offering innocence.'), ('martos', 'Then say what you need from me.'), ('crow', 'A man who can carry an objective through difficulty, and report the difficulty accurately. Your former commander wasted that capacity.'), narration='The judgement reaches him with uncomfortable force. He has expected contempt, punishment, perhaps an offer that pretends he was always on the right side. Being considered useful with the whole record visible is more tempting than any of them.'), b('martos', 'What are you offering?'), b('crow', 'Work with defined objectives, the resources to attempt it and a place in my service. I require results and allegiance. I intend to enlarge my power.'),
    b('martos', 'The medic comes under the agreement.'), b('crow', 'Her care and protection are included. Your service is the price. Hers is not.'), b('martos', 'And if the assignment fails?'), b('crow', 'The undertaking remains. Your failure will be dealt with separately.'),
    prose('Martos asks who authorises the care, how a changed provider is arranged, what freedom Sera retains. The answers can be tested. No one has asked him to call the Crow’s ambition humanitarian. He mistakes the absence of that insult for a kind of respect larger than the bargain before him.\n\nHe knows an organisation capable of protecting them will use force against other people. The Crow has said so. He tells himself that every dependable structure has a cost and someone must be willing to carry it. In the refuge, every unpaid hour had felt like another way of failing Sera. Here the failure seems to have an answer: give this man service, and service will have the means to keep a promise.\n\nHe is choosing under pressure. He is also choosing something he wants. He does not ask what place the people outside the agreement will have in the order the Crow intends to build.'),
    b('martos', 'I accept provisional service under those terms.'),
    prose('Before leaving the desk, he rehearses what to tell Sera. Care, protection, her right to refuse any work: he can give her those terms clearly. The rest is harder. He has found himself listening for an instruction with relief. He has found a man who will look at what he did and still make room for what he can do.\n\nThe Crow gains a capable servant whose need has been carefully understood. Martos understands that too. He does not yet think exploitation excludes loyalty. He thinks an acknowledged price may be more honourable than a promise whose price arrives afterward.'),
 ]),
 'MT-F07': dict(title='The undertaking remains', age=26, era='martos_early_service_age26', location='martos_service_sitting', text=[
    prose('Martos’s memory — age twenty-six, provisional service before appointment as Clubs. The first care provider closes. A replacement asks for a greater fee and an extended protected stay. The undertaking could be made cheaper by calling it fulfilled. The Crow authorises the replacement instead.'),
    b('crow', 'Her course continues. Transfer the care, not the obligation back to her.'),
    prose('Sera receives the replacement appointment. The greater cost has not been passed back to her, nor made into an invitation to work it off. She continues her recovery. When she comes to the service sitting room by arrangement, the acute refuge dressing is gone and her coat is her own choice.\n\nMartos has set out two cups. He is almost eager to show her that the undertaking survived its first inconvenience. She already knows; it is her care. He catches the eagerness too late to hide it. He wants the kept promise to say something decisive about the man whose service he accepted, and wants her to hear the same thing.'),
    b('martos-sera', 'It cost more. He signed it anyway.'), b('martos', 'He said it would remain.'), exchange(('martos-sera', 'I know. I can be glad without enlisting.'), ('martos', 'You do not owe service. He said that.'), ('martos-sera', 'Then you can stop looking as though I missed the important part.'), ('martos', 'I am glad it continued.'), ('martos-sera', 'So am I. Let that be enough for this cup of tea.')),
    prose('A separate early assignment goes wrong. The objective is lost when a hostile collection changes route. Martos reports the failure and the damaged return route. The Crow authorises the promised recovery team. At the loading court a recovery worker opens the transport door and reaches for the case. Martos has no case. He gives the worker his route correction instead, then leans against the door when his knee fails to hold.'),
    b('crow', 'The recovery remains authorised. Return with the accurate failure. I have not given permission to disguise it as a final stand.'),
    b('martos', 'The authority is gone. I can mark the changed route. I need a hand to board.'),
    prose('The worker takes his elbow. Martos is heavier than the help makes convenient; he can feel the adjustment in the other man’s stance. A second worker leaves damaged equipment where it fell because recovering it would keep the transport exposed. They bring him back without the objective and without that equipment.\n\nHe has prepared himself to argue that he can still be useful. No one in the transport asks him to make the argument. At headquarters the recovery expense is entered beside the failed assignment. The next place for his report remains open.\n\nHe remembers the order to leave the wounded, and something in him takes this ordinary act of recovery with the force of a vow. The Crow has preserved a valuable operative. Martos feels that he has been kept when he might have been discarded. The difference between those descriptions will never trouble him as much as it should.'),
    prose('At debrief, Martos reports that he pushed output after precision deteriorated. The Crow restricts his next assignment and funds controlled training. In the yard, Martos misses the handover signal on the first attempt. He stops the exercise instead of counting the lifted load as a pass.'),
    b('martos', 'I heard the signal. I thought I could finish before it mattered.'), b('crow', 'Then your report identifies the fault. Practise surrendering the task, not merely enduring it.'),
    prose('In repeated drills, reporting the warning has to be followed by actually yielding the precision work. Martos manages the first part more readily. His body keeps making the small movements that mean he intends to finish anyway. On one attempt he hears the accepted handover and still reaches back. The exercise stops.\n\nThere is no praise for a heavier lift after a missed signal. There is rest, another attempt, and a colleague who will not pretend to have received a task Martos has not released. No one’s voice switches Rage off. The physical recovery takes its own time.\n\nWhat the Crow supplies is the time and resources, with restrictions Martos cannot evade by being brave. Martos learns to trust that discipline. He begins to grant the person who funds it authority beyond the limits of an exercise, beyond the undertaking, into questions he once would have asked himself.'),
    b('martos', 'I will be reliable for you, master.'),
    prose('He has said master. It comes more easily than the earlier provisional terms. He thinks of the care appointment that remained, the worker’s hand under his elbow, the chance to return after failure and be corrected instead of erased. Each is real. Together he makes them into a rule: a leader who keeps his people has earned their obedience.\n\nHe does not ask who counts as his people. That omission leaves a great deal of space for the Crow’s ambition. Reliability has become the proof Martos reaches for whenever purpose becomes difficult. He can already imagine doing things he would condemn in Voss’s service, provided this commander accepts the result as his own. The thought does not arrive as corruption. It arrives as resolve.'),
 ]),
 'MT-F08': dict(title='The seat and the closed business', age=27, era='martos_appointment_age27', location='martos_service_sitting', text=[
    prose('Martos’s memory — age twenty-seven. The business has refused Syndicate terms. The collection order is plain: secure its stock and close the working route to anyone outside the Crow’s authority. Martos reads it without needing a euphemism explained.\n\nInside, staff are putting away the ordinary tools of a working day. Someone has left a meal wrapped beside a ledger. He knows what will follow the collection: wages no one can promise, goods no one can replace, another route claimed by the Syndicate. He has enough authority over the method to prevent needless injury. He has been given no authority to decide that the collection should not happen.\n\nHe could question it. He knows that. He has not been deceived about the purpose, and this fact reassures him more than the purpose itself disturbs him.'),
    exchange(('martos', 'There are staff inside. They leave first.'), ('martos', 'Take your coats. Personal things go with you.'), narration='The instruction sounds protective until he notices the staff looking at the stock they are not allowed to take. One keeps a hand on a shelf for a moment before letting go. Martos waits rather than pull the hand away. He will remember that patience later, and have to remind himself what he was waiting to do.'),
    prose('The staff leave. The owner remains long enough to watch the working route close under the enforced demand. Martos carries out the collection carefully. No one is injured to make an example. The stock and access are still lost.\n\nThere is satisfaction in a task done without the worst avoidable harm, and he allows himself to feel it. Then he sees the wrapped meal beside the ledger. He calls to have it returned. A member of staff takes it without thanking him. For a moment the scale of the gesture is plain: he can return lunch while making it harder for that person to earn tomorrow’s.\n\nHe finishes the assignment. This is not an order he will later discover was cruel. He knows while his hands are doing the work. The Crow has earned his faith; the people losing their livelihoods have been given no say in what that faith requires.'),
    prose('Later, at the executive desk, the Crow names the role he is offering. Martos’s repeated results have enlarged the Syndicate’s power. The appointment does not grant Rage or make him commander of the Clubs Suit.'),
    b('crow', 'You will serve me as the Ace of Clubs. High-risk protection, combat and suppression under my direct authority. The security work remains an obligation, not a substitute for that service.'), b('martos', 'I understand the work.'), b('crow', 'And that it will not always resemble the promise that first brought you here.'),
    prose('At the desk he thinks of care that continued, recovery after failure, a place that did not vanish when he became expensive. He can remember the abandoned equipment in the court more vividly than the stock he has just helped take. He notices the imbalance and does not correct the decision it supports.\n\nBreaking faith with the Crow has begun to feel like becoming Voss: the man who explains that his people no longer fit the objective. Martos has built himself a cruel choice. Either he remains loyal, or he becomes the kind of commander he despises. There is little room in it for the people who have never belonged to either man.\n\nHe is not asking to command the Clubs Suit. He is accepting direct service, high-risk protection and suppression under a sovereign whose appetite will not stop at keeping existing promises. He has heard the warning in the offer. He wants to answer it without reservation.'),
    exchange(('martos', 'I understand. I accept, master.'), ('martos', 'You will not have to wonder whether I am still yours when the work is ugly.'), narration='He means the assurance. The word ugly includes the collection house. It includes work he cannot yet name. His promise reaches farther than his knowledge, and that is exactly what he intends to give.'),
    prose('He leaves the executive room in the Crow’s service. The title has not changed the purpose of his strength; it has made the purpose easier to state. Outside the institution that now has a place for him, other people are trying to find another place to work.\n\nHe will be gentle with the small things he can repair. He will remember colleagues’ meals and make room for a tired person to sit. He will do frightening work for this leader and call the willingness to continue faithfulness. None of those parts of him is false. He has made the choice with his eyes open. He means to remain faithful for the rest of his life.'),
 ]),
}

DISCLOSURES = {
 'private': [b('martos', 'The operational brief contains the limits and support conditions. My private recollections stay private.')],
 'mavis': [b('martos', 'In selection I treated being ahead as proof I had brought everyone. Sera stopped me. I nearly made the same assumption about your leg.'), b('mavis', 'Give me the task and the information. Let my answer count.')],
 'camila': [b('martos', 'I kept putting myself beside every uncertain part. It made the page look stronger while making the timing impossible.'), b('camila', 'A limit we can calculate is more useful than a second copy of you on paper.')],
 'elias': [b('martos', 'I objected to the transfer privately and kept guarding it. Do not let my statement sound as though the objection stopped the work.'), b('elias', 'It will say both. I will not give it an audience you did not agree to.')],
 'sera': [b('martos', 'I kept your care notices because I wanted proof someone could keep a promise after failure. I made your life into evidence for my own choice.'), b('martos-sera', 'Keep the proof. Give me back the right to disagree with what you make of it.')],
}

OUTCOME_VARIANTS = {
 'promise_kept': [prose('The independent witness archive liaison has received Lena and the agreed intact records, and confirmed her onward safety arrangement. The active attack is stopped. A separate authorised regional receiving team has accepted disarmed Voss under recorded custody conditions. This is preservation and secured custody, not a verdict about every historical offence.'), b('martos-lena', 'The receipt names what arrived. My account still names what happened. Keep both.'), b('martos', 'Both remain in the record.')],
 'delivered_at_cost': [prose('The liaison confirms Lena’s arrival and the intact records. The attack has stopped, but the report has another line that Martos must read aloud: what the departure cost, and what danger remains beyond it. He leaves that line beside the receiving confirmation.'), b('martos-lena', 'Tell the liaison the remaining risk. I need to plan the next part of my life, not approve your report.'), b('martos', 'The recorded cost goes with it.')],
 'withdrawal_recovery': [prose('The receiving confirmation has not come. Martos returns to the agreed recovery point and checks who is safe, who holds the case and what they can still attempt. Exhaustion and spent supplies come back with him. Winning his own part of the fight would not have answered the empty receiving line.'), b('martos', 'We confirm who is safe and who holds the case. Then we agree the next attempt.'), b('martos-lena', 'And you ask again before changing where I go.')],
}

AGREEMENT_VARIANTS = {
 'refused': [b('martos-lena', 'Not yet. I want time to compare the route and fallback with my copy before I agree to move.'),
    b('martos', 'Then we remain here. I will secure this approach while the terms are revised.'),
    prose('Lena keeps the case on her side of the table. Martos removes the proposed movement from the departure sheet. Her refusal has changed the plan; it has not made her an obstacle he can move around.')],
 'revised': [b('martos', 'The liaison you chose receives the original. The fallback changes the route, not the recipient or ownership. Any further change comes back to you.'),
    b('martos-lena', 'And the list of permitted disclosures stays attached.'), b('martos', 'Yes. Operational necessity does not become permission to publish your private account.'),
    prose('She compares the revised terms with her own copy. A signature belongs after that comparison and her acceptance, not before it. The protected departure remains on hold until she agrees.')],
 'accepted': [b('martos-lena', 'I accept these terms: my selected liaison, intact records, agreed onward accommodation and the listed disclosures. If the route changes, tell me.'),
    b('martos', 'I will. The receiving role and your ownership remain the same.'),
    prose('He records the acceptance beside the terms she actually chose. It authorises this movement under these conditions. It gives him no wider consent over her testimony or her life.')],
}

PRIVATE_DISCLOSURES = {
 'mavis': [b('mavis', 'The operational brief is enough if it tells me what I need to do.')],
 'camila': [b('camila', 'Then keep the brief sufficient to act on. I do not need the rest to correct this plan.')],
 'elias': [b('elias', 'I can keep the cover narrow. Privacy needs no performance from either of us.')],
 'sera': [b('martos-sera', 'You can keep that private. It does not change which parts of my own life I choose to discuss.')],
}

CLOSING_VARIANTS = {
 'mavis': [prose('At the arranged lounge visit, Mavis turns the parts tray so its lowest edge faces Martos. The pin he dropped settles against the rim.', 'kitchen'),
    b('mavis', 'You put the handover in the report.'), b('martos', 'It was part of the work.'),
    b('mavis', 'You used to write it as though it happened because you let it.'),
    prose('He looks at the pin, then at the correction she has made without touching the watch.'),
    b('martos', 'You agreed to the leg. You did it. I needed the answer.'),
    b('mavis', 'Then ask me for it next time.'),
    prose('He sets the pin where both of them can see it before he fits the case. She stays for the ordinary work. Neither asks that it stand in for Lena’s answer.')],
 'alone': [prose('The lounge is quiet. Martos sorts the remaining pins by size, alone. Accepting help in the departure report has not bought anyone’s company afterward. He leaves the repaired watch with the promised explanation for its owner.', 'kitchen')],
}


def private_disclosure_scene(recipient):
    return deepcopy(DISCLOSURES['private'] + PRIVATE_DISCLOSURES.get(recipient, []))


def closing_scene(available_colleague=None):
    return deepcopy(CLOSING_VARIANTS['mavis' if available_colleague == 'mavis' else 'alone'])

SUPPORT_VARIANTS = {
 'accepted': [b('mavis', 'I can take the extraction leg under those conditions. Confirm me at departure; tell me before you change the route.'),
    b('martos', 'You have the authorised pursuit packet. If precision starts to go, I report it and keep the opposition away from your leg.'),
    prose('An accepted task takes one line on the sheet. It will still need an available colleague when the task begins. Martos leaves that condition underlined.')],
 'unavailable': [b('martos', 'The colleague named for this leg is unavailable. We use the fallback or delay. I will not report a handover that nobody can receive.'),
    b('martos-lena', 'Then show me what changes before we leave.'),
    prose('The empty role is a fact in the plan. Their earlier conversation cannot put a colleague at the departure line while that person is somewhere else.')],
 'declined': [b('martos', 'No support role has been accepted for this leg. The plan must fit that limit.'),
    b('martos-lena', 'Does it still meet the terms I accepted?'),
    prose('He checks the protected movement separately from the fight. If the remaining plan cannot meet the agreement, departure waits. Promising to endure more would not answer her question.')],
}

def agreement_scene(result):
    return deepcopy(AGREEMENT_VARIANTS.get(result, AGREEMENT_VARIANTS['refused']))


SUPPORT_ACCEPTED = {
 'camila': [b('camila', 'I can authenticate the receiving signal and check the route changes. Send the authorised source packet; do not turn an unverified booking into a guaranteed arrival.'),
    b('martos', 'I will report what is still uncertain before departure.'),
    prose('Camila marks the authentication step in her own hand. The agreement gives her a defined task and the information needed to attempt it, without claiming she can clear every road.')],
 'elias': [b('elias', 'I will maintain the agreed cover window. If the timing changes, tell me before the explanation starts attracting questions.'),
    b('martos', 'Movement details only. Lena’s private correspondence stays outside it.'),
    prose('Elias checks the permitted account against the departure time. He has agreed to make the arrival discreet, not to turn Martos’s past into a reassuring story.')],
}


def support_scene(result, recipient='mavis'):
    if result == 'accepted' and recipient in SUPPORT_ACCEPTED:
        return deepcopy(SUPPORT_ACCEPTED[recipient])
    return deepcopy(SUPPORT_VARIANTS.get(result, SUPPORT_VARIANTS['declined']))

# Each period is independent even where appearance continuity permits reuse.
for _key, _memory in MEMORIES.items():
    for _field in ('text', 'after_encounter'):
        for _index, _beat in enumerate(_memory.get(_field, [])):
            _beat.update(mode='memory', era=_memory['era'], memory_id=_key,
                         source_id=f'{_key}:{_field}:{_index:03}')
for _key, _chapter in CHAPTERS.items():
    for _field in ('briefing', 'operation_intro', 'aftermath'):
        for _index, _beat in enumerate(_chapter.get(_field, [])):
            _beat['source_id'] = f'{_key}:{_field}:{_index:03}'


def chapter_scene(chapter_id, phase='briefing', facts=None):
    return deepcopy(CHAPTERS.get(chapter_id, {}).get(phase, []))


def memory_scene(memory_id, phase='text'):
    return deepcopy(MEMORIES.get(memory_id, {}).get(phase, []))


def aftermath_scene(ending, facts=None):
    beats = deepcopy(OUTCOME_VARIANTS.get(ending, OUTCOME_VARIANTS['withdrawal_recovery']))
    # Runtime provides a human-readable description derived from its real ledger.
    # No claim about capture/ injury is inferred from an ending label here.
    if ending == 'delivered_at_cost' and isinstance(facts, dict) and facts.get('cost_description'):
        beats.insert(1, prose(str(facts['cost_description'])))
    return beats


def validate_inventory():
    assert tuple(CHAPTERS) == tuple(f'MT-{n:02}' for n in range(1, 15))
    assert tuple(MEMORIES) == tuple(f'MT-F{n:02}' for n in range(1, 9))
    assert {c['memory'] for c in CHAPTERS.values() if c.get('memory')} == set(MEMORIES)
    assert all(c.get('briefing') and c.get('aftermath') for c in CHAPTERS.values())
    assert all(b.get('mode') == 'memory' for m in MEMORIES.values() for f in ('text', 'after_encounter') for b in m.get(f, []))
    return True


# Explicit historical records for both optional visitors and scripted speakers.
# Runtime installs these into the two independent historical catalogues. No
# present character profile is read here, including for the concealed Crow.
_PERIODS = {
 'martos_conventional_age20': (20, ['martos', 'martos-sera', 'martos-tomas'],
    'Conventional service, before selection. A real evacuation has shown the value of dependable protection. No later deployment abuses, injury, desertion, fugitive life, Syndicate or Ace appointment has occurred.'),
 'martos_selection_age22': (22, ['martos', 'martos-sera', 'martos-tomas', 'martos-voss'],
    'Selection and early operator rescue. Team judgement and an answered handover matter. No age-23 extraction injury, later coercive transfers, desertion or Syndicate service is known.'),
 'martos_overmutation_age23': (23, ['martos', 'martos-sera', 'martos-tomas', 'martos-voss'],
    'Deployment extraction and its immediate infirmary debrief. Sera has the preventable extraction injury caused by Martos exceeding precision limits. No later desertion wound, disposal order, refuge or Crow bargain is known.'),
 'martos_deployment_age24': (24, ['martos', 'martos-sera', 'martos-tomas', 'martos-voss'],
    'Later deployment before disposal order. Forced removal and knowingly abusive second transfer have happened. Sera has returned to limited service after the earlier extraction injury. No desertion wound, refuge, recruitment or present consortium is known.'),
 'martos_desertion_age24': (24, ['martos', 'martos-sera', 'martos-voss'],
    'Fixed disposal order, refusal and limited escape into refuge. Sera has a separate recent desertion wound. No later care bargain, appointment or present-day outcome is known. Tomas was last known alive; later whereabouts are unknown.'),
 'martos_recruitment_age25': (25, ['martos', 'martos-sera', 'crow'],
    'Fugitive refuge and first authorised concealed-Crow appointment. Only the care/protection bargain and provisional service being offered are available. No future kept undertaking, training outcome, Clubs appointment, other Aces or present witness mission is known.'),
 'martos_early_service_age26': (26, ['martos', 'martos-sera', 'crow'],
    'Provisional Syndicate service. Costly care continuation, authorised recovery and repeated failed/revised handover practice occur in authored order. Sera visits by arrangement after recovery; she has not joined. No Clubs appointment, other Ace overlap or present route outcome is known.'),
 'martos_appointment_age27': (27, ['martos', 'crow'],
    'Knowingly coercive collection and later appointment as Clubs. No present-day protection mission or other Ace presence is established. Appointment timing within the Mavis entry interval is not made more exact. No command of Clubs Suit is granted.'),
}

_VOICES = {
 'martos': dict(voice='Reserved, concrete, short complete statements; dry humour in ordinary shared work. Under anger speak more quietly and precisely. Admit an uncertainty rather than inventing a guarantee.',
    habits=['Check what was actually agreed.', 'Offer practical work while allowing a refusal.'],
    avoid=['Affectless military caricature or constant tactical jargon.', 'Every frustration becoming Rage; affection curing a Trait.', 'Retrospective certainty, self-exoneration or present Ace authority before appointment.'],
    examples=['I thought you had answered. I should have checked.', 'I saved the meal. I made no promise about the temperature.'],
    unknown_response='I have no record of that. What do you need here?'),
 'martos-sera': dict(voice='Plainspoken, observant and willing to interrupt an unsafe assumption. Practical warmth coexists with disagreement; she does not speak as a cure or moral certificate for Martos.',
    habits=['Name the specific limit someone is ignoring.', 'Choose whether to help and state the conditions.'],
    avoid=['Automatic forgiveness, compulsory service or emotional cooling powers.', 'Naming future injuries or care before they happen.'],
    examples=['That answer is old. Ask again.', 'I can be grateful and still disagree.'],
    unknown_response='I do not know that. Tell me what is happening now.'),
 'martos-tomas': dict(voice='Adult unit technician; concrete attention to small repairs and understated teasing. Competent peer who can be tired, disagree and choose his own work.',
    habits=['Test a clasp or repair before calling it done.', 'Use an ordinary joke rather than a speech about camaraderie.'],
    avoid=['Prophetic farewell or invented later death.', 'Acting as combat narrator or knowing later Syndicate associates.'],
    examples=['It works. I have witnesses.', 'Temperature was outside the agreement.'],
    unknown_response='That is news to me. Is the repair still what we are doing?'),
 'martos-voss': dict(voice='Controlled administrative authority. Rationalises abuse through necessity, continuity and loyalty; recognises competence while redirecting responsibility upward.',
    habits=['Replace a question about purpose with an assigned task.', 'Emphasise institutional consequences.'],
    avoid=['Omniscience, control of every military institution or future Northline facts in military years.', 'Knowing Crow identity or gaining automatic access to him.'],
    examples=['Your post is the transfer.', 'Individual exceptions make the whole movement impossible.'],
    unknown_response='I have issued no instruction concerning that. Attend to the matter before us.'),
 'crow': dict(voice='Concealed sovereign at an authorised headquarters appointment. Formal, economical and exact about power, service, resources and consequences; no warmth offered as absolution.',
    habits=['Distinguish the undertaking from performance discipline.', 'Ask for an accurate result with its limits.'],
    avoid=['Revealing real identity, family, unshared history or other private campaigns.', 'Claiming omniscience, personal battlefield rescue, forgiveness or a Rage cure.'],
    examples=['The undertaking remains. Your failure will be dealt with separately.', 'Return with the accurate failure.'],
    unknown_response='That is outside the information before us. State what concerns this undertaking.'),
}


def _historical_character(who, era, age):
    early = age <= 20
    if who == 'martos':
        appearance = ('Broad adult man, dark hair, conventional olive fatigues; no invented scar origin.' if early else
            'Broad adult operator, dark hair; combat shirt, reinforced trousers, plate carrier, pouches, gloves and headset; no national insignia.' if age <= 24 and 'desertion' not in era else
            'Broad adult fugitive in practical worn civilian layers; no Ace uniform.' if age <= 25 else
            'Broad adult in plain provisional-service clothes before promotion; appointed attire only after the authored acceptance at twenty-seven.')
        role = 'Conventional service member' if early else 'Special-forces candidate/operator' if age <= 24 else 'Fugitive accepting provisional service' if age == 25 else 'Provisional Syndicate operative before appointment' if age == 26 else 'Operative accepting Clubs appointment'
        return dict(name='Martos', age=age, role=role, appearance=appearance,
            personality='Methodical, dependable, privately caring and dryly humorous; over-responsible and reluctant to request help. Later loyalty is learned within this period, never imported backward.',
            present_concerns=['Complete the specific agreed task.', 'Keep the team or protected group accounted for.', 'Respect the current period’s authority and available knowledge without inventing later experience.'],
            relationships={'martos-sera':'Adult medic peer with independent judgement; gratitude grants no obedience.', 'martos-tomas':'Adult technician peer known only where listed.', 'martos-voss':'Military commander only in military periods.', 'crow':'Unknown before the recruitment period; concealed contracting sovereign afterward.'},
            private_boundaries=['Rage Awakening and scar origin unspecified.', 'No current stats, signature history, money, social knowledge, contacts or biography can fill a missing historical fact.', 'Fixed wrongdoing cannot be undone by an optional conversation.'])
    names = {'martos-sera':'Sera Dalm', 'martos-tomas':'Tomas Reed', 'martos-voss':'Adrien Voss', 'crow':'The Crow'}
    looks = {
      'martos-sera':('Adult peer, brown skin, brown eyes, black curly hair in a low bun; practical civilian recovery clothes with a healing wound and support.' if era in ('martos_desertion_age24','martos_recruitment_age25') else
              'Adult peer, brown skin, brown eyes, black curly hair in a low bun; recovered civilian visitor clothes, no acute battlefield dressing.' if age >= 26 else
              'Adult peer, brown skin, brown eyes, black curly hair in a low bun; olive service medic uniform and vest, supported injured arm in the immediate extraction debrief.' if era == 'martos_overmutation_age23' else
              'Adult peer, brown skin, brown eyes, black curly hair in a low bun; olive service medic uniform and vest.'),
      'martos-tomas':'Adult unit technician peer. Use the accepted service-era portrait; no later uniform, death or injury is implied.',
      'martos-voss':'Adult commander visibly older than the unit; service-era portrait, no real national insignia or invented rank. Present consortium clothing is excluded.',
      'crow':'Concealed identity, dark formal silhouette and masked/obscured face. No portrait or wording reveals a civilian identity. Headquarters executive room only for these authored meetings.'}
    return dict(name=names[who], age=None,
        role={'martos-sera':'Independent team medic; later wounded survivor and voluntary visitor', 'martos-tomas':'Unit technician', 'martos-voss':'Commanding officer of fictional special-operations unit', 'crow':'Concealed Syndicate sovereign'}[who],
        appearance=looks[who], personality=_VOICES[who]['voice'],
        present_concerns=['Speak only from this exact period.', 'Attend only an established or arranged encounter; decline roles not accepted.'],
        relationships={'martos':'Bounded relationship described by the current era and authored scene; no present-day status is assumed.'},
        private_boundaries=_VOICES[who]['avoid'] + ['Do not infer facts from another era or current save.'])


ERA_REFERENCES = {era: dict(setting=boundary, knowledge_boundary=boundary + ' The era is an independent snapshot. Player suggestions are not evidence of future facts.',
    characters={who:_historical_character(who, era, age) for who in cast})
    for era, (age, cast, boundary) in _PERIODS.items()}
ERA_GUIDES = {era:{who:deepcopy(_VOICES[who]) for who in cast}
              for era, (_, cast, _) in _PERIODS.items()}

# Catalogue portraits are exact-period choices, never current-profile fallbacks.
_ERA_PORTRAITS = {
 'martos_conventional_age20': {'martos':'martos-service-early','martos-sera':'sera-service','martos-tomas':'tomas-service'},
 'martos_selection_age22': {'martos':'martos-special-forces','martos-sera':'sera-service','martos-tomas':'tomas-service','martos-voss':'voss-service'},
 'martos_overmutation_age23': {'martos':'martos-special-forces','martos-sera':'sera-service','martos-tomas':'tomas-service','martos-voss':'voss-service'},
 'martos_deployment_age24': {'martos':'martos-special-forces','martos-sera':'sera-service','martos-tomas':'tomas-service','martos-voss':'voss-service'},
 'martos_desertion_age24': {'martos':'martos-special-forces','martos-sera':'sera-refuge','martos-voss':'voss-service'},
 'martos_recruitment_age25': {'martos':'martos-fugitive','martos-sera':'sera-refuge','crow':'crow-mavis-history'},
 'martos_early_service_age26': {'martos':'martos-early-service','martos-sera':'sera-early-service','crow':'crow-mavis-history'},
 'martos_appointment_age27': {'martos':'martos-early-service','crow':'crow-mavis-history'},
}
for _era, _cast in _ERA_PORTRAITS.items():
    for _who, _portrait in _cast.items():
        ERA_REFERENCES[_era]['characters'][_who]['portrait'] = _portrait


# Copy stable staging into new snapshots only; never rebind a loaded snapshot.
__import__('martos_campaign_visuals').apply(CHAPTERS, MEMORIES, DISCLOSURES, OUTCOME_VARIANTS)
for _key, _beats in AGREEMENT_VARIANTS.items():
    __import__('martos_campaign_visuals').bind(_beats, 'MT-agreement:' + _key,
        'locations/campaign/martos/safe_stop', __import__('martos_campaign_visuals').CURRENT,
        room='martos_transfer_house__sitting')
for _key, _beats in SUPPORT_VARIANTS.items():
    __import__('martos_campaign_visuals').bind(_beats, 'MT-support:' + _key,
        'locations/interiors/syndicate_hq/cross_branch_operations_room' if _key == 'accepted' else 'locations/campaign/martos/safe_stop',
        __import__('martos_campaign_visuals').CURRENT,
        room='syndicate_hq__cross_branch_operations_room' if _key == 'accepted' else 'martos_transfer_house__sitting')
for _key, _beats in PRIVATE_DISCLOSURES.items():
    __import__('martos_campaign_visuals').bind(_beats, 'MT-private:' + _key,
        'locations/interiors/syndicate_hq/cross_branch_operations_room',
        __import__('martos_campaign_visuals').CURRENT, room='syndicate_hq__cross_branch_operations_room')
for _key, _beats in CLOSING_VARIANTS.items():
    __import__('martos_campaign_visuals').bind(_beats, 'MT-closing:' + _key,
        'locations/interiors/syndicate_hq/members_lounge',
        __import__('martos_campaign_visuals').CURRENT, room='syndicate_hq__members_lounge')
for _key, _beats in SUPPORT_ACCEPTED.items():
    __import__('martos_campaign_visuals').bind(_beats, 'MT-support:accepted:' + _key,
        'locations/interiors/syndicate_hq/cross_branch_operations_room',
        __import__('martos_campaign_visuals').CURRENT, room='syndicate_hq__cross_branch_operations_room')


