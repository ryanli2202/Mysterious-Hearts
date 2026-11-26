"""Authored visual-novel passages for A Life on Loan.

Past-tense recollections are bounded accounts, not interactive historical actors.
Present scenes retain the campaign's existing rooms, choices and fixed outcomes.
"""

def p(text):
    return dict(player='', speeches=[], narration=text)

def b(who, text):
    return dict(player='', speeches=[[who, text]], narration='')


MEMORIES = {
    'IV-M03': [
        p('The paper is too ordinary. Ivan had expected something in its appearance to acknowledge what it contained: a warning, perhaps, or a stain someone had failed to clean. Instead the scan shows a straight margin and a place for a signature. The image is an archival reconstruction from his private institutional records. He has no memory of the room in which it was signed.'),
        p('The Korean company had begun its work before he was born. It engineered him to become a powerful Awakened with Conduit. The record follows that work through to a completed sale at birth, to the Conclave’s Russian affiliate. Someone had needed a price and a destination. Nobody had needed a name he could answer to.'),
        p('He reads the sale entry again. For years, eighteen had served as a useful border in his thoughts. Before the Syndicate; after the Syndicate. The distinction had let him imagine that the life before the handover might contain something untouched, if he went back far enough. The earlier transaction sits quietly on the page and removes that possibility.'),
        p('There are things the document does not give him. No mother’s voice. No face to place beside his own in a mirror. No account of who held him, or whether anybody had hesitated before letting go. He catches himself furnishing the missing room with a cradle and takes it away again. He will not call an imagined kindness a memory simply because he needs one.'),
        p('His hands rest on either side of the file. These are the hands he uses to find a difficult chord, retie a wrap, lift something Valentina has already told him she can carry. They are also the end of a process somebody once expected to be profitable. He turns one palm upward, irritated by the impulse to inspect it for evidence.'),
        p('Conduit had always been the part of him that answered most readily. Change the element, change the problem his body could solve. In training, that adaptability earned attention. Here it appears as an anticipated result. Long before he had learned to be good at anything, someone had already decided what good would mean.'),
        p('He wants to be furious with a person. A person can look away, deny an accusation, be made to hear the whole sentence. The file offers institutional names and the outline of an exchange. It leaves his anger with nowhere satisfying to stand.'),
        p('For a moment he considers destroying the copy. He could at least decide what happened to this piece of his history. Then he imagines having to rely on somebody else’s account of it again. He saves it, closes it, and remains at the desk with both hands flat.'),
        p('He was wanted. That is the phrase he cannot stop turning over. Wanted for something. He had spent so much of his life trying to make the last two words unnecessary.'),
    ],
    'IV-M04': [
        p('The days he remembers from the Conclave’s Russian affiliate were divided by instruction. A stance corrected. A grip broken and taken again. Footwork until the next movement arrived without a pause to think. There was always another art to study, another distance at which he was expected to be dangerous. Getting something right did not end the work. It made the next demand possible.'),
        p('He learned to listen to footsteps outside a practice space without appearing distracted. He learned that a question could sound like reluctance if he asked it before completing the task. Later, people would praise his composure. They would not see the part of composure that consisted of having an answer ready before anyone had decided whether he was allowed a question.'),
        p('The small intervals with Valentina had no grandeur. Sometimes the equipment bench was the only place to sit. He would put his hands on his knees so she would not see him testing the ache in his fingers. She would notice anyway and move whatever they were doing to a rhythm he could tap with the heel of his palm.'),
        p('“You missed one,” he told her once. She tapped the altered rhythm again. “I changed it.” He supplied the proper ending. She waited until he was satisfied, then changed it a second time. He looked at her. She looked back with the patience of someone entirely prepared to waste his precious free minute.'),
        p('He laughed too loudly and glanced toward the door. The laughter stopped before hers did. That was what returned most sharply now: not a blow, not a command, but the speed with which he could interrupt his own pleasure in case someone else was about to do it.'),
        p('Valentina nudged his hand back onto the bench. “Again.” He started more quietly. This time he left a space at the end and let her fill it. The result was not a rhythm he would have chosen by himself. He kept it.'),
        p('He had wanted to be strong enough to prevent the next interruption. It was a practical ambition before it became a large one. If he mastered the exercise sooner, perhaps there would be another minute. If he became indispensable, perhaps somebody would ask what he wanted. When success produced a harder task, he blamed the remaining distance between his strength and whatever strength would finally be enough.'),
        p('He also remembers being cross with her for taking a risk he had not approved. He had called it looking after her. She had asked why looking after her always seemed to require her to do what he said. He did not remember a clever answer. He remembered being hurt that she could mistake his care, and being too young in that moment to examine whether she had mistaken it at all.'),
        p('The next instruction ended the interval. He rose at once. Valentina tapped the last beat against the empty place where his hand had been, making him turn back for a second. It was a tiny disobedience to his own urgency: he stayed long enough to answer her.'),
        p('He could not give either of them the day. That failure would remain with him much longer than the ache in his hands. But when he remembered the bench, he wanted to remember that she had made something there too. He had not been the only person keeping them alive inside the hours.'),
    ],
    'IV-M05': [
        p('At eighteen, Ivan waited outside the handover room with nothing useful to do. The corridor held a chair and a closed door. He stood. Sitting made the waiting feel like something he had accepted, although he knew that distinction would not matter to anyone on the other side.'),
        p('The trade was part of a deal. He understood that much before he understood what his life inside the Syndicate would look like. People spoke of the destination as if it answered the question of what happened to him next. Nobody asked whether there was another place he wanted to go.'),
        p('He practised a small turn of his wrist. The movement had no purpose here; it was a way of occupying the space between instruction and instruction. When he noticed himself doing it, he stopped. A moment later, he began again. He had been taught to make waiting useful, and had never been taught what to do with waiting that could not improve him.'),
        p('The appointment made him the second Joker Card. For a breath, despite himself, he felt pride. They recognised what he could do. The title belonged to a position few people would ever approach. He had worked for every part of the fighter they were receiving, even if he had never agreed to be received.'),
        p('That involuntary pride was harder to forgive than the fear. He wanted to refuse the title and wanted them to pronounce it correctly. He wanted the respect in the room to mean they could no longer treat him as an object. Instead the respect accompanied the arrangements already made for him.'),
        p('Being the second Joker did not make him second in command. Sylvanis already occupied that place, and the distinction would become painfully familiar. There were people Ivan could order, doors his rank could open, resources made available for his work. Above those freedoms sat the work itself, and above the work sat the people who could require it.'),
        p('He tried to imagine asking the simplest question: what if I decline? His mind supplied everything except the spoken words. In the life he knew, refusal was something to be overcome, negotiated downward, trained out of a body. It was not an ordinary answer someone expected to receive.'),
        p('He entered when the door opened. The threshold was narrow enough to cross in a single step. Later he would think of his life as having two distinct sides, but his body had made no such distinction. It carried the same habits into the new room: straighten, attend, conceal the question until it can be asked safely.'),
        p('The permission to work as an idol came later. He would care about it more than he could explain to people who treated it as decoration beside his real duties. Rehearsal contained work he had chosen to do well. A song could ask for an emotion rather than a result. The work was his, even while the permission to continue it belonged to somebody else.'),
        p('That was the beginning of the bargain he made with himself, without ever saying it aloud. Use the position. Become stronger inside it. Build enough that the next door would open because he decided to leave. He had not yet admitted how easily “enough” could move each time he reached it.'),
    ],
    'IV-M06': [
        p('Valentina was the first person he asked. That seemed so obvious to Ivan that he almost failed to make it an invitation. He began with what they would need, what they could build, how much safer she would be with power of her own. She listened until he began describing her part as though the question were settled.'),
        p('“You have gone past the bit where I answer.” She was sitting opposite him, close enough to stop his hand as he moved a page across the table. She did not stop it. She let it rest between them. “Start there.”'),
        p('He started again. Officially, the Black and White Joker Network would operate beneath the Syndicate. Privately, he wanted it to become strong enough to leave. He wanted territory, people, resources that would not disappear the moment permission was withdrawn. Saying it to her made the desire sound less like a private fever and more like work two people might undertake.'),
        p('“I want you beside me,” he said. She asked whether that meant beside him when she disagreed. He nearly answered that of course it did. The speed of the reassurance embarrassed him. He took a moment instead and told her what authority he meant to give her, and where he thought their decisions might meet.'),
        p('He chose her because she acted when he was still calculating how to make an action perfect. Because she could explain a difficult thing without making the listener feel small. Because she had known him before any title, and he wanted one person in the organisation who would look at him without seeing a card first. He did not say all of that elegantly. She let him struggle through it.'),
        p('Valentina wanted a life in which their next hour was not always somebody else’s to allocate. She also wanted him to stop making the whole escape a test he had to pass alone. “I am joining because I want this,” she told him. “Do not make me spend the next year proving I meant it by agreeing with everything you say.”'),
        p('In the cleared practice space, he gave her wind and Deathwind. She tested the ordinary movement first, making a directed gust settle where she intended. Ivan began to correct her stance, then stopped when she adjusted it herself. She caught the aborted instruction and smiled without looking away from the target.'),
        p('The dangerous part required more care. Deathwind could injure the soul; the endurance carried with it could keep her functioning through damage. Neither made her invulnerable. He explained the limits with the excessive precision of someone trying to guarantee what he could not guarantee. She listened, then asked him to move clear so she could make the next attempt.'),
        p('Queen of Death. He offered the title with the solemnity he thought it deserved. She tried the weight of it in silence. Then she asked whether he expected her to answer to it over breakfast. “Only on formal occasions,” he said. “Burnt toast. Disputes over the last egg.” She laughed, and for a moment the future felt like something with a kitchen in it.'),
        p('He would remember the grant whenever he feared losing her. He would remember the promise of escape whenever he wanted her agreement. What he needed to remember, and often found less convenient, was the hand she had not put over his: she had left him room to ask properly. He had owed her the same room ever since.'),
    ],
    'IV-M07': [
        p('Sowon made him wait until she finished the sequence. It was not a performance arranged for him. She had been working on an entry, and she completed the attempt, considered it, then repeated the part that dissatisfied her. Ivan recognised the discipline before either of them spoke. He also recognised how seldom anyone let him finish his own work before beginning theirs.'),
        p('Her taekwondo and Olympic medal were already hers. He had nothing to offer that could take credit for them. Minsu’s sister was an easy description for people who knew Minsu; it told Ivan very little about the woman checking whether he had actually watched her feet. He had watched. When he named the correction she had made, her attention sharpened.'),
        p('“And what would you change?” she asked. He answered with an angle. She tried it, rejected half of it, and explained why. He liked her more for refusing the flattering version of the exchange in which his presence made him the teacher.'),
        p('He needed someone who could reach an opening before it closed and still understand why it was an opening. More than raw pace, he wanted trained judgment at speed. Sowon did not waste a difficult movement. He could imagine entrusting her with something that would fail in the interval between an order and its repetition.'),
        p('“You have described what I can do for you,” she said when he made the offer. “What am I joining?” He gave her the branch’s public purpose, then its private ambition. He did not use her brother as a recommendation or a point of pressure. This was her decision, and she required him to address it that way.'),
        p('The prospect appealed to her. A difficult undertaking, real authority, power that would extend a skill she had earned. She was not so innocent of ambition that he had to hide those parts. But she wanted to know whether he valued her judgment or merely liked the thought of a medalist carrying his orders quickly.'),
        p('“If I see a better route?” she asked. “Take it.” “If I think the destination is wrong?” He took longer over that answer. He said he would hear her. She noticed the difference between the two replies. She accepted without pretending it was a difference they had resolved.'),
        p('Blue lightning made the first controlled acceleration strange. Her intention reached a familiar movement and found more distance available than habit expected. She checked herself, reset, and tried again. Ivan watched the adjustment with a pleasure that had nothing to do with possession. It was beautiful to see someone understand a new possibility so quickly.'),
        p('“Again?” he asked. “Obviously.” Then she looked back at him. “That was a request, by the way.” He gave her a small bow from where he stood clear of the lane. She did not smile until she was facing away.'),
        p('She became Queen of Storms because she chose the work and the chance it offered. Her willingness was real. It was also specific: she had agreed to help build an organisation that would listen to her. In the present, Ivan could no longer remember that promise without hearing the question he had answered too slowly.'),
    ],
    'IV-M08': [
        p('Kouji Mitaka was unwinding a hand wrap when Ivan found the moment to speak with him. He kept the cloth neat despite the tiredness in his fingers. A Japanese K-1 kickboxer with debts pressing on him was an easy story to simplify: a man in trouble, an offer of help. Ivan had watched him fight before making the offer. He knew there was more to choose than the trouble.'),
        p('Kouji could commit without becoming careless. He understood the short space in which a guarded approach became a strike, and he could change that commitment when the person opposite him changed the problem. Off the floor, he made room in a conversation with a joke. Ivan, who usually tried to control a conversation by making it precise, found that ability unexpectedly useful.'),
        p('“If this is criticism,” Kouji said, “give me a minute. I like to have both hands free for professional despair.” Ivan said he had an offer. The joke remained on Kouji’s face a fraction longer than it belonged there. Then he set the wrap down and listened.'),
        p('Ivan could offer resources, work, and power. Kouji did not ask him to explain what relief would feel like. Debt had already taught him to hear the next obligation beneath an ordinary invitation. What he asked was how long the new work would follow him after the immediate help had been used.'),
        p('Ivan described a place in the network. He spoke of an organisation that would eventually stand on its own, of people whose skills would give them a claim on the thing they helped create. Kouji asked about the first assignment. Ivan answered it in detail. The large question remained between them, partly obscured by an answer that was genuinely useful.'),
        p('He could see the calculation Kouji was making because he had made versions of it himself. The offer did not have to be free of danger to be better than the pressure already here. That recognition should have made Ivan more careful. It also made him confident that Kouji would accept.'),
        p('“I am not asking you to be grateful,” Ivan said. Kouji’s smile changed. “Good. I am likely to be, and I would rather know it is not in the job description.” He asked to hear the practical terms once more, this time without the speech about the future. Ivan obliged.'),
        p('The flame and physical strength altered the test; they did not replace the man performing it. Kouji planted his stance, controlled his distance, and brought the new force through a motion he understood. Afterwards he flexed his hand and looked at Ivan with a brief, unguarded astonishment. “All right. That part was not oversold.”'),
        p('King of Flames pleased him more than he tried to show. It offered a way to be seen that did not begin with what he owed. He stood a little straighter while pretending to inspect the practice floor. Ivan let him have the moment without commenting on it.'),
        p('Kouji joined willingly, with relief and ambition mixed into the same decision. Ivan had helped him; that fact would survive every later argument. But when Ivan remembered how readily he had answered the small question instead of the large one, he could no longer pretend that gratitude alone explained the loyalty he expected.'),
    ],
    'IV-M09': [
        p('Paul Samsen did not begin by asking Ivan to believe him. He had already lost a friend and been falsely accused of killing him. Repeating the truth to a new listener meant watching for the moment when the listener decided whether the truth was useful. He sat where he could see the door, attentive to the room without making a display of vigilance.'),
        p('Ivan had come with an offer of shelter. He also wanted the former judo practitioner’s judgment: the patience to let someone commit their weight, the ability to find leverage without confusing force with haste. A network built only from people eager to strike would be easy to provoke. Paul could see the moment before a bad decision became difficult to reverse.'),
        p('“You keep saying protection,” Paul said. “From what, precisely?” Ivan answered what he could actually offer. He could not name the real killer, settle the accusation, or return the friend. Paul watched him leave those things unsaid and relaxed by so little that Ivan almost missed it.'),
        p('“I would rather you tell me the limit now,” Paul said. “It costs less than finding it later.” Ivan thought of the rooms in which he had been told about his own future. For a moment he wanted simply to provide the limit and keep it. Then he thought of what Paul could become with ice, with Tranquility, and began speaking about the network.'),
        p('Paul asked what the work would involve. He did not confuse taking shelter with endorsing every person who offered it. He also did not pretend he could make the decision from a place of safety he did not have. He wanted somewhere to remain long enough to think, and work in which his judgment was more than a description in someone else’s account.'),
        p('Ivan told him why he wanted him. Paul listened closely to that part. Being selected for a skill was different from being accepted as a problem, even by someone kind. He asked one further question: if they disagreed about an order, would Ivan still call the room shelter?'),
        p('Ivan said yes. He meant it in the room where he said it. Later, when the network became something he was terrified to lose, meaning it would prove less useful than keeping it.'),
        p('The ice test was quiet. Paul worked through contact and balance, careful of the newly altered footing. Tranquility let him perceive and begin his response at once, but his body still had to make the movement. He corrected an overreach without becoming angry at the correction. Ivan watched the second attempt and understood why he had chosen him.'),
        p('Afterward, Paul remained seated for a little while. Ivan asked whether anything was wrong. “No. I was thinking I would have told him about this.” He did not need to name the friend. Ivan found himself without a practical answer and, for once, did not invent one.'),
        p('Paul became King of Ice. He accepted the shelter, the role and the power. His grief came with him, unchanged by the title. So did the capacity to say that an account was false, even when the person giving it had helped him. Ivan had valued that precision before it was directed at him.'),
    ],
    'IV-M10': [
        p('Somchai made no useful attempt to resemble Paul. The Thai street criminal was a mass murderer and a fugitive from the police; Ivan knew the murders were real before he entered the backroom. There was no false accusation to correct, no hidden innocence that would make the choice easier to describe afterward.'),
        p('Somchai moved a chair with his foot so Ivan could sit, a small courtesy delivered without ceremony. Dense tattoos continued over his face and disappeared beneath his clothes. His attention travelled from Ivan’s hands to the door, then returned to the conversation. He seemed interested in what Ivan wanted, and even more interested in what Ivan would admit to wanting.'),
        p('“You have already decided I am useful,” he said. “Otherwise you would have sent somebody.” Ivan remained standing long enough to dislike the accuracy of that. Then he sat. He had come for force he could direct, for a man willing to press where the other recruits might stop and ask him why.'),
        p('That was the part of the decision he would later dress in operational language. Different capabilities. Necessary reach. A deterrent. Sitting opposite Somchai, he knew the simpler appeal: fewer objections between his intention and its result.'),
        p('Somchai wanted cover, power, and a place where the violence he could offer had value. He did not pretend Ivan’s dream of freedom had become his own. “Your new organisation,” he said. “It will need people who can make a refusal expensive.” Ivan replied that he would set limits. Somchai asked how expensive was permitted.'),
        p('Ivan named restrictions. He heard himself speaking with the certainty he used when uncertainty would look like weakness. Somchai listened without interrupting. When Ivan finished, he asked whether the limits belonged to every assignment or could be changed when something mattered enough.'),
        p('The honest answer was already in the room. Ivan had crossed one limit by coming here. He told himself that command would contain what recruitment empowered, that his strength and attention would be sufficient. He had made versions of that promise about his own life for years. This time the risk would be carried by people who had not agreed to his calculation.'),
        p('The red lightning made the controlled strike hit with brutal force. Somchai regarded the result, then looked back at Ivan with an interest that no longer needed polite conversation to sustain it. Ivan had offered him something he wanted. That made the alliance possible. It did not make their reasons the same.'),
        p('“King of Chaos,” Somchai repeated. He seemed amused by the title, but he waited for the next instruction before moving. The obedience was reassuring. Ivan allowed himself to be reassured by a man who had just asked when the rules could change.'),
        p('He could still name all the reasons he had chosen each of the others. With Somchai, he had to resist the temptation to keep adding reasons until the original one disappeared. He wanted to become strong enough that no one could use him again. He had decided he could use this man, and manage what followed.'),
    ],
}


# Briefing and aftermath stay separate for legacy saves. The reader combines
# briefing, account and return for new chapter entries without changing IDs.
SCENES = {}
RETURNS = {}
CHOICES = {}

SCENES['IV01'] = ([
    p('Ivan stops at the piano before taking off his coat. The phrase is still wrong in the place it was wrong at the studio: the last note arrives too neatly, resolving a feeling he has not finished having. He plays it again and lets the ending hang. Behind him, Valentina puts down what she is carrying and waits for the sound to disappear.'),
    b('valentina', 'That version. Keep the untidy bit.'),
    b('ivan', 'It is not untidy. It is unresolved. There is a considerable professional difference.'),
    b('valentina', 'Good. I liked it professionally.'),
    p('He moves along the bench without thinking. She takes the space, bumping his shoulder while she settles. It is an ordinary arrangement, worn comfortable by repetition. He values it most fiercely at moments when she seems unaware there is anything to value.'),
    p('The summons waits beside the music. He has already read it. Reading it again will not change the time, but his eyes keep returning to the small rectangle of light. He turns it face down. A second later he calculates how long he has left.'),
    b('valentina', 'You had an evening before somebody put something in it. What were you going to do?'),
    b('ivan', 'Finish this. Eat something that has not travelled in a paper bag. Hear you explain why your karaoke score was wrong.'),
    b('valentina', 'It was wrong. That machine is frightened of commitment.'),
    p('He laughs and nearly begins the phrase again. Then he sees the time. The laugh has left him with an ache behind the ribs, absurdly close to grief. He can perform for a room full of people; he cannot promise his sister he will be here long enough to eat.'),
    b('ivan', 'People think the music proves I have another life.'),
    b('valentina', 'It is another part of your life. It matters.'),
    b('ivan', 'Until it gets in the way of the part they own.'),
    p('He dislikes how bitter that sounds, as though the hours at the studio were counterfeit. They are not. He knows the satisfaction of finding the breath a line needs, the private excitement of a song beginning to work. The cruelty is that something real can still depend on permission.'),
    b('valentina', 'Do you want me to listen, or do you want me to help you hide how angry you are?'),
    b('ivan', 'I would settle for another ten minutes.'),
    p('She does not tell him to take them. Both of them know the difference between suggesting courage and bearing the consequence of someone else’s suggestion. She puts one hand on the piano lid and waits for him to decide what they can do with the minutes that remain.'),
], [
    p('At the door he puts his coat straight, although it has never been off. Valentina stays at the piano. She does not follow him to make the departure easier, and he is grateful enough for that to find it irritating.'),
    b('valentina', 'I will eat if it gets late.'),
    b('ivan', 'You should.'),
    b('valentina', 'I know. I was telling you, not asking.'),
    p('He leaves the music open. The small, ridiculous hope that he might return before the room changes is something he keeps to himself. Outside, he begins arranging his face for people who will call his obedience professionalism.'),
])

SCENES['IV02'] = ([
    p('The executive meeting room has enough empty chairs to make Ivan’s standing feel deliberate. His branch results wait on the table. He has brought figures that demonstrate success, a revised schedule, and an argument he has stripped of every word that might sound like pleading.'),
    p('Sylvanis treats the room as though he has wandered into it on the way to something more entertaining. The opaque operational mask gives Ivan no expression to read. He has learned to attend to smaller things: how abruptly the stillness changes, how a light remark can arrive with the precision of a blade.'),
    b('ivan', 'The work is ahead of the required schedule. I want control over the next interval.'),
    b('sylvanis', 'Want. There he is. I thought we would spend all evening listening to your reports.'),
    b('ivan', 'You asked for results. I have brought them.'),
    p('Sylvanis lets the answer sit. Ivan keeps his hands still. He can order almost anyone below him, yet here he is rehearsing a reasonable request for the use of his own evening. The title has enlarged the number of people who must listen to him without reducing the number of times he must ask.'),
    b('sylvanis', 'And you would like a treat. A clear afternoon? A little door with your name on it?'),
    b('ivan', 'I would like the authority my responsibilities imply.'),
    b('sylvanis', 'Oh, that is a much prettier way to beg.'),
    p('Ivan wants to hit him. The impulse is so clean that he almost welcomes it. It offers a simple action in place of the exhausting work of sounding uninjured. He leaves it where it is and looks down at the schedule.'),
    b('ivan', 'You leave when you want. You choose what interests you. The same rank appears beside my name, and I still have to justify this.'),
    b('sylvanis', 'You think the little card makes us alike?'),
    p('The amusement stops. Sylvanis is suddenly attentive, and the change makes the distance across the table feel shorter.'),
    b('sylvanis', 'Mr. Crow keeps my cooperation. You keep appointments. Work out which of those can be put on a schedule.'),
    p('There it is, without the language of duty to cover it. Sylvanis’s place beside the Cardmaster rests on a kind of strength and independence Ivan cannot borrow from a title. Ivan hates him for making the difference sound natural. He hates himself for wanting the difference removed by becoming more like him.'),
    b('ivan', 'Then I will build something that does not depend on your permission.'),
    b('sylvanis', 'Please do. Build your little branch. Make it worth breaking.'),
    p('He laughs once, suddenly delighted by whatever violence he has imagined. Ivan gives him nothing in return. There are private reasons the threat reaches deeper than this meeting, and he will not drag them into the open to win a sentence.'),
], [
    p('The concession he receives is tied to the next assignment. More latitude over how to deliver, no right to refuse delivery. He takes the revised schedule because refusing the concession would not make him free. That calculation is so familiar that it barely feels like a choice.'),
    p('Outside the room, he stops before he reaches the corridor’s next turn. For an instant he cannot bear to go directly where he is expected. He stands still, doing nothing useful, until the small defiance begins to feel childish. Then he resents having learned to call it that.'),
    p('The network is officially a Syndicate branch. He has made it valuable under their protection while imagining the day it could survive without them. Tonight, what he wants is larger than survival. He wants Sylvanis to have to wait outside one of his doors.'),
    p('The thought gives him pleasure. He lets it. Later he will have to reckon with how often he has confused that pleasure with the hope of freedom.'),
])

SCENES['IV03'] = ([
    p('In the network’s review room, the silence feels purchased. Ivan has the desk, the keys, the right to keep people outside. He closes the door and catches himself enjoying the sound of it. At headquarters a closed door means somebody is deciding when to admit him. Here he can make the same sound from the other side.'),
    p('He has opened the private institutional file to check the handover at eighteen. An earlier transfer catches his eye. He scrolls back, slowly, as though speed might make him mistake what is written. The words are administrative and patient. They can wait for him to understand.'),
    p('There is no one in the room to perform composure for. He puts the schedule from headquarters aside. It lands across the corner of the older record, and for a moment the two documents look like parts of the same unfinished instruction.'),
], [
    p('The screen darkens before he touches it again. His reflection appears over the file: a face people recognise, carefully lit on posters, professionally composed at doors. He wonders how much of being recognisable has ever belonged to him.'),
    p('Valentina could sit across this desk and read what he has read. The thought comforts him until it begins to feel like another task: explain the discovery correctly, make it bearable for someone else, receive the right sort of sympathy. He decides that he can choose the size of this conversation, even if he could not choose the beginning of his life.'),
    p('He puts the file away. There are still things he does not know. Tonight he will not fill them with a story simply to have somewhere to put the pain.'),
])

SCENES['IV04'] = ([
    p('Valentina hears the error before Ivan does. He has been tapping the same interval against the piano bench while she talks, correcting its length each time his attention drifts. She stops halfway through her sentence and taps a deliberately uneven reply.'),
    b('ivan', 'That is not the count.'),
    b('valentina', 'No. It is me being very patient about you not listening.'),
    p('He turns toward her. She has left room for an apology without arranging herself to receive one. It is a kindness he can recognise more easily when somebody else is the recipient.'),
    b('ivan', 'Sorry. Tell me again.'),
    b('valentina', 'In a minute. Where did you go?'),
    b('ivan', 'Back to learning how long a minute was.'),
    p('She looks at his hand on the bench. The same habit has survived changing rooms, countries, titles. He can make himself appear entirely at rest while some part of him counts down to the next instruction. Beside him, she taps the old altered ending once more.'),
], [
    b('valentina', 'You remember wanting the break to last. I remember wanting you to stop checking the door.'),
    b('ivan', 'I was trying to keep us out of trouble.'),
    b('valentina', 'I know. Sometimes I wanted you in the room with me anyway.'),
    p('He had remembered those intervals as the best of what he could give her. It hurts to discover the absence inside them. She is not asking him to apologise for having been trapped. She is telling him what it was like to sit beside him, waiting for the part of his attention that belonged to them.'),
    b('ivan', 'I thought if I became good enough, they would stop deciding everything.'),
    b('valentina', 'What did good enough look like?'),
    b('ivan', 'It kept changing.'),
    p('This time he hears the answer after he has said it. The network has given the old pursuit new rooms and better equipment. He still measures his life against a strength he has not yet reached.'),
    b('valentina', 'I wanted a brother. I already had one. You did not have to finish becoming something first.'),
    p('He cannot make a joke quickly enough to protect himself. She lets that be all right. When she resumes the story he failed to hear, he listens without counting beneath it.'),
])

SCENES['IV05'] = ([
    p('The record of his arrival at the Syndicate fits into far less space than the event occupies in him. Ivan lays the appointment beside it. The second Joker Card: an impressive phrase, polished smooth enough that someone could say it admiringly without encountering the trade underneath.'),
    p('He knows what an outsider might see. Rank, money, access. A man allowed to pursue a public career and command a private organisation. He has used that appearance himself. It is easier to let someone envy him than to explain why he checks an incoming instruction before answering an invitation.'),
    p('What returns first is not the announcement. It is the corridor outside the handover room, and how precisely he remembers the amount of space he was taking up.'),
], [
    p('He has a room of his own now, and the ability to make other people wait outside it. He looks at the closed door from behind the desk. For years he has counted these differences as progress toward an exit. He has scarcely asked what they are making him practise along the way.'),
    p('Sylvanis’s voice returns with unpleasant clarity: You keep appointments. Ivan imagines a stronger version of himself answering. The imagined answer changes each time; the audience remains the same. Even alone, he is still trying to win a conversation Sylvanis has already left.'),
    p('He closes the folder without putting the appointment on top. The title can no longer cover the transaction. But he keeps the title. He still intends to use everything it gives him, and he is not yet ready to ask where using it will stop.'),
])

SCENES['IV06'] = ([
    p('Valentina has moved the route marker before Ivan reaches the table. The change is small on paper. In practice it keeps people out of the far end of a space the network wants clear. He notices the lost efficiency first and dislikes himself for noticing it first only after he has begun to object.'),
    b('ivan', 'You could have asked.'),
    b('valentina', 'You gave me responsibility. I used it.'),
    b('ivan', 'The original route was faster.'),
    b('valentina', 'For us. The people clearing it would have had a different evening.'),
    p('She places her fingertip on the point where the two routes diverge. It is an invitation to examine the problem with her. He hears a challenge instead. Being contradicted by Valentina still reaches a part of him that expects affection to make agreement easier.'),
    b('ivan', 'I am trying to make something that protects you.'),
    b('valentina', 'Then do not use me to finish an argument about someone else.'),
    p('He stops. She does not soften the sentence, but she takes her hand off the marker. He remembers the first conversation about the network, before Deathwind, when she had made him go back to the part where she was allowed to answer.'),
], [
    b('ivan', 'I chose you because I trust your judgment.'),
    b('valentina', 'I would like to recognise that while I am using it.'),
    p('He looks at the changed route again. This time he follows it all the way to the exit. There is a consequence he had been willing to leave outside the frame of the task. She has put it back where he has to see it.'),
    b('ivan', 'The change stays.'),
    b('valentina', 'Good. Now tell me the part you still dislike.'),
    p('It would be easier if she accepted the concession and left him alone to feel generous. Instead she remains at the table, prepared to work with him while they disagree. He had wanted loyalty to feel like relief. Hers often feels like being asked to stay awake.'),
    p('When they finish, she takes her own copy of the route. He does not remind her who gave her the power that makes it possible. The fact crosses his mind, and the shame of that is private. He lets her leave without making it her work to reassure him.'),
])

RETURNS.update({
    'IV-M03': [p('The review room returns in the faint hum of the screen. Ivan has been sitting very still. He moves his fingers before reaching for the file, then decides whether he wants anyone beside him when he opens it again.')],
    'IV-M04': [p('The present piano bench is smooth beneath his palm. Valentina waits beside him, older than the voice in the memory and entirely capable of telling him what he has left out of it.')],
    'IV-M05': [p('There is no one waiting to receive him when he looks up. The review room is his to use. He sits with that limited freedom for a moment before touching the appointment again.')],
    'IV-M06': [p('Valentina’s hand rests beside the altered route. The power he gave her is no longer new. The question she asked before accepting it has lost none of its force.')],
})

SCENES['IV07'] = ([
    p('Sowon has timed the proposed crossing twice. Ivan finds the figures already written beside the route, along with a mark showing where the people using it would have to move. She has done the work thoroughly enough that he cannot mistake her objection for uncertainty about whether she can perform it.'),
    b('sowon', 'The timing works. That was not my question.'),
    b('ivan', 'Then ask it again.'),
    b('sowon', 'Why does getting there first matter more than knowing who is still in the way?'),
    p('He begins to explain the advantage of speed. She waits until he hears himself describing her own specialty to her, then raises an eyebrow. The expression is so familiar from their first conversation that he almost smiles.'),
    b('ivan', 'You are enjoying that.'),
    b('sowon', 'A little. I did the figures. I earned a little.'),
    p('He does smile, briefly. This is part of why he wanted her: the confidence to be difficult without making difficulty the whole relationship. She can admire a good decision and reject the next one. He has sometimes treated that as inconsistency when it was simply attention.'),
    b('sowon', 'I joined because you wanted people who could think quickly. Let me finish thinking.'),
    p('Her finger stays on the route. He remembers a training lane, her refusal to stop midway through an attempt just because he had arrived, and how much he had respected it before the interruption became his own.'),
], [
    b('ivan', 'I do remember why you joined.'),
    b('sowon', 'Then you remember I wanted a say in where we were going. That was the attractive part.'),
    p('She closes the timing notes but leaves the route between them. The gesture is economical: she will not repeat work she has already done to make him feel more comfortable with the answer. He knows the discipline in it. He once mistook that discipline for how easy she would be to command.'),
    b('ivan', 'And the speed?'),
    b('sowon', 'Also attractive. I can want two things.'),
    p('She gives him the quick smile he has been trying to recover from the conversation, then grows serious again. There is no contradiction to exploit. She wants the alliance, likes what she can do, and has a question he owes more than a deadline.'),
])

SCENES['IV08'] = ([
    p('Kouji brings the second page in separately. He places it beside the first, neatly enough to suggest he has spent some effort deciding how to begin. Ivan waits for the joke that usually allows them both to settle into a difficult conversation.'),
    b('kouji', 'I had a very good opening for this. Then I read the second page and became less charming.'),
    b('ivan', 'What is wrong with it?'),
    b('kouji', 'I said I would do the job. I did not agree to every job after it.'),
    p('There is no joke at the end of the sentence. Kouji keeps one hand on the page. He is not asking Ivan to forget the help he received. He is trying to keep that help from becoming an answer to a question he has not been allowed to finish.'),
    b('ivan', 'The next stage depends on continuity.'),
    b('kouji', 'Then ask me about the next stage. Do not staple it to the one I already accepted.'),
    p('Ivan looks at the fastening in the corner. The concrete absurdity nearly makes him laugh. He does not, because Kouji is watching to see whether humour will become another way to avoid the terms.'),
    b('ivan', 'I thought this was what you wanted. A place. Work you could rely on.'),
    b('kouji', 'It is. I would like to rely on the part where I get an answer as well.'),
    p('The request sounds painfully like the one Ivan took to headquarters. He wants to explain all the ways this situation is different. Before he can begin, he remembers the wrap in Kouji’s hands when they first spoke, and the relief he had recognised before he made the offer.'),
], [
    p('Kouji leaves the pages separate. He helps Ivan shift the heavy end of the table back into place after they have leaned it aside to look at the route. The help is immediate, unremarkable, and not an apology for the argument.'),
    b('ivan', 'You do not have to make this easier for me.'),
    b('kouji', 'I am making the table easier to walk past. The other thing still needs your attention.'),
    p('Ivan finds himself laughing at last. Kouji allows the laugh, then taps the second page once before he leaves. Warmth has not withdrawn the question. Ivan has depended on people confusing the two more often than he wants to count.'),
])

SCENES['IV09'] = ([
    p('Paul notices the untouched cup before he sits. He moves it out of reach of Ivan’s papers, a small practical adjustment made without interrupting the conversation. Ivan thanks him. For a moment there is nothing in the room that needs a title.'),
    b('paul', 'I need to know whether you are asking me or informing me.'),
    b('ivan', 'You are safe here.'),
    b('paul', 'That is not the same answer.'),
    p('Ivan hears the sharpness in his own silence. Paul has not raised his voice or accused him of a hidden intention. He has made an inaccuracy impossible to continue using. The skill that once made Ivan choose him is now holding the conversation still.'),
    b('ivan', 'I would not put you outside because you questioned an assignment.'),
    b('paul', 'Then tell me what happens if I refuse this one.'),
    p('The distinction is small enough that Ivan could pretend to miss it. He does not. Questioning can be permitted indefinitely, provided the person eventually obeys. Refusal would require him to accept a limit he has not imposed himself.'),
    b('paul', 'I want to keep working with you. I would not be asking so carefully if I did not.'),
    p('That reaches him more effectively than an accusation. He remembers how carefully Paul had listened to the offer of shelter, and how little a man could afford to assume when a false story had already taken so much from him.'),
], [
    b('ivan', 'Does it ever stop following you?'),
    p('Paul looks at him for a moment. The question is too broad, but this time he lets Ivan leave it broad. He does not make him identify which part of the past he means.'),
    b('paul', 'Sometimes I am occupied with something else. Then something small brings it back. I have learned not to call the whole day lost.'),
    b('ivan', 'That sounds difficult.'),
    b('paul', 'It is. I did not mean it as advice.'),
    p('They sit without trying to improve the answer. When Paul rises, he brings the cup back within Ivan’s reach. His own case remains unresolved. He has offered company for a few minutes, not a model of recovery Ivan can apply to himself and declare finished.'),
])

SCENES['IV10'] = ([
    p('Somchai arrives ready to discuss the assignment and apparently content to let Ivan believe that is all he wants. He takes the chair nearest the door. When Ivan asks him to move to the other side of the table, he does so readily, watching how long it takes Ivan to return to the papers.'),
    b('somchai', 'Better?'),
    b('ivan', 'We need to be exact about the limits.'),
    b('somchai', 'We usually are. Until the limits get in the way.'),
    p('Ivan places the route between them and names the people who are to be left out of the operation. Somchai studies it with an attention that can look reassuring if Ivan chooses to see only the attention. He has become practiced at that choice.'),
    b('somchai', 'You want them frightened, or you want them listening? Pick one before you send me.'),
    b('ivan', 'You will do what the assignment permits.'),
    b('somchai', 'That is why I am asking the man who permits it.'),
    p('The reply contains no challenge to his authority. That is what makes it difficult to answer. Somchai is offering the very obedience Ivan has wanted, stripped of the good intentions he usually supplies on behalf of the person obeying.'),
    p('He thinks of the care he took choosing the others. Judgment, competence, loyalty, the wish for a life with more room in it. He took care with Somchai too. He cannot claim that care made the choice innocent.'),
], [
    b('somchai', 'You can keep me close if it helps you sleep.'),
    b('ivan', 'This is not about my comfort.'),
    b('somchai', 'All right.'),
    p('The easy agreement is worse than an argument. Somchai has heard the restriction and found no immediate advantage in resisting it. Ivan watches him leave and catches himself counting that as evidence of control.'),
    p('He stays with the route after the door shuts. The appointment had given Somchai more power. It had also given Ivan a new obligation to everyone who might encounter that power. He has spent far more time calculating the first fact than attending to the second.'),
])

RETURNS.update({
    'IV-M07': [p('The training lane recedes. Sowon is still waiting across the review table, her timing notes complete and her question unanswered. He has always admired how little room she gives him to pretend he has not heard.')],
    'IV-M08': [p('Kouji’s hand rests beside the second page. The debt that once made Ivan’s offer persuasive has not turned this new page into something Kouji already signed.')],
    'IV-M09': [p('The cup is still cooling out of the way of his papers. Paul waits for a precise answer in the present, where Ivan has the opportunity to give one.')],
    'IV-M10': [p('Somchai leans back from the route. Ivan returns to the limits with the knowledge that the man listening has a reason to accept them today. Tomorrow will still require a decision.')],
})

SCENES['IV11'] = ([
    p('Five chairs are occupied around Ivan’s table. He remembers choosing every person in them; the arrangement still gives him a private satisfaction. Here is something he assembled. A room in which his arrival begins the meeting instead of ending his wait outside it.'),
    p('The unnamed intermediary runs a small criminal dispatch operation. Its routes would give the network another foothold in the underworld. Officially, this is Syndicate branch business. Inside the review room, the generals know how Ivan wants such gains to accumulate into the means to break away.'),
    b('ivan', 'We need cooperation that lasts beyond the first agreement. If every route can be withdrawn, we have borrowed reach. We have not built it.'),
    b('kouji', 'All right. Tell me what we are promising before I carry it in.'),
    b('paul', 'And which part the other side can refuse.'),
    p('Kouji nudges the route toward Paul so he can see the annotation without leaning across Sowon. It is an ordinary courtesy, and Ivan finds himself wanting this group to remain precisely as it is: capable, familiar, needing him at its centre. The desire is stronger than he had expected.'),
    b('valentina', 'Keep the workers out of the negotiation. They are there for a shift, not to join us.'),
    b('sowon', 'And leave them a way to finish it. This exit matters.'),
    b('somchai', 'If refusal is the point, why bring force?'),
    p('Silence follows the question. Somchai has not introduced violence into an innocent room. They all know what the network is. He has merely said the part Ivan prefers to keep beneath a more attractive description.'),
    b('ivan', 'Because an agreement has to mean something after we leave.'),
    b('paul', 'To whom?'),
    p('Ivan looks at the routes instead of the people. In his mind they connect to other operations, then to a reach the Syndicate would have to reckon with. He can almost feel what it would be like to receive an order and consider whether to accept it. The imagined freedom makes the small acquisition in front of him seem urgent beyond its size.'),
    b('ivan', 'We begin here. I am not asking for the whole city tonight.'),
    p('He hears how reasonable that sounds. He has not answered the question about the workers. The meeting moves toward a method, and he allows the movement to spare him the answer.'),
], [
    p('The intermediary’s cooperation is secured. Ivan reads the result twice, experiencing the uncomplicated pleasure he had hoped for. A route that was outside his reach is now available. People who would once have dismissed his branch will have to account for it.'),
    p('Then he sees the extra availability attached to the agreement. Somebody must remain later. Somebody must leave another way. Small inconveniences, he almost calls them, and recognises the phrase before he can say it aloud.'),
    b('ivan', 'I want to see the receiving desk myself.'),
    p('It is a useful decision. It also lets him postpone deciding what the result means. He puts the figures in order first. For several minutes the gain remains the largest thing on the page.'),
])

SCENES['IV12'] = ([
    p('The dispatch worker is still wearing the concentration of someone whose shift should have ended. They stand beside the receiving desk with an ordinary request: leave the old exit open, and let the agreed finishing time mean what it said. They have somewhere else to be. Ivan does not know where, and they do not offer it as evidence that their time deserves respect.'),
    p('Garrett stands nearby, having heard enough to stay. The desk is cluttered with the end of a working day. Ivan notices a pen rolling toward the edge and catches it automatically. For a second he has accomplished something simple and useful. Then the worker asks when they can leave.'),
    b('ivan', 'The arrangement should not have been communicated like that.'),
    b('garrett', 'How was it supposed to sound?'),
    p('There is no aggression in the question. Garrett looks from the worker to Ivan and waits. Ivan has been prepared to correct an interpretation, perhaps to reprimand somebody who carried an instruction too far. He is less prepared to hear the instruction repeated without embellishment.'),
    b('ivan', 'I can change it.'),
    b('garrett', 'Then change it. They should not need a better reason to go home.'),
    p('The worker watches Ivan, not Garrett. His ability to settle the matter is obvious to everyone. He should be pleased that his authority can help. Instead he feels the ugly closeness between being able to remove a burden and having put it there.'),
    b('ivan', 'There was a practical reason for controlling the route.'),
    b('garrett', 'I believe you. I am asking whether the reason was good enough to do this to them.'),
    p('Ivan looks at the door. He knows exactly how a door can occupy your thoughts while someone else is discussing reasons. For a moment the receiving desk and the handover corridor sit too close together in his mind. He pushes the association away because it feels unfair to him, then hears whose comfort he is protecting.'),
], [
    p('When the immediate conversation ends, Garrett does not ask for a confession. He has seen an instruction and its consequence. That is enough to give him a concern without giving him access to everything Ivan has ever kept private.'),
    b('garrett', 'You can tell me it is complicated. I can listen. Just do not make complicated mean nobody gets an answer.'),
    b('ivan', 'You make it sound easy.'),
    b('garrett', 'This part is small. That is why I do not want us to miss it.'),
    p('Ivan puts the rescued pen back beside the worker’s papers. It is a little too straight. He leaves it that way and walks out carrying the larger problem he had hoped a visit would settle.'),
])

SCENES['IV13'] = ([
    p('The intermediary withdraws cooperation. On paper it is a change in access. In Ivan’s body it is the floor becoming unreliable beneath him. He had let himself imagine the route as something secured, something nobody above him could take away. Its loss reaches all the way back to that foolish moment of relief.'),
    p('He brings the next instructions to Valentina, Sowon, Kouji and Paul. Somchai is not in this review. Ivan has already caught himself anticipating how much simpler the conversation would be with him, and that anticipation is something he does not want to examine in company.'),
    b('kouji', 'We have reached the end of the job I agreed to.'),
    b('ivan', 'The other side changed the terms.'),
    b('kouji', 'I noticed. It does not change what I agreed to.'),
    p('Kouji’s voice has lost its cushioning humour. Paul watches Ivan rather than the route. Sowon remains standing, ready to examine a practical alternative if one is offered. Valentina has not touched the new instructions.'),
    b('ivan', 'If we give up every gain the moment somebody objects, there will never be enough to stand on our own.'),
    b('paul', 'We can be under pressure and still be responsible for the next instruction.'),
    b('sowon', 'I can carry it out. I am asking you to think before you make me.'),
    p('He hears doubt in every voice and, beneath it, the possibility that the room he built could become a room he loses. He wants to remind them of what he provided. The words come close enough that he feels their shape before he stops them.'),
    b('valentina', 'Say it.'),
    b('ivan', 'There is nothing to say.'),
    b('valentina', 'You looked at us as if we had forgotten what we owe you.'),
    p('For a moment he hates her accuracy. He chose her because she could reach him without the distance of rank. Now there is nowhere behind rank to step. He looks at Paul, at Kouji, at Sowon, and sees the people they were when his offer had mattered most.'),
    b('ivan', 'If we lose the chance now, everything after it becomes somebody else’s decision.'),
    b('valentina', 'And in the organisation you are building, who gets to refuse you?'),
    p('He has an answer about urgency. He has another about the Syndicate, and a third about the years none of them can give him back. He can hear how every answer ends with the same demand: trust him enough to let him continue. It is not what she asked.'),
], [
    p('The argument ends without reconciliation. They have not left him. They have also not supplied the agreement he wants to call loyalty. He remains at the table after the last reply, arranging the instructions in the order he intended before anyone entered.'),
    p('He accelerates the preparations. The decision brings a brief relief, because deciding feels better than waiting to discover whether other people will allow him a future. He recognises the relief from smaller, better choices. That resemblance makes it easier to trust.'),
    p('At the top of the page he has written the network’s name. Beneath it are the people whose time he is allocating. He turns to the next sheet before the resemblance can become a complete thought.'),
])

SCENES['IV14'] = ([
    p('April does not take the seat he offers until she has seen the route. Ivan has prepared explanations for several kinds of opposition. Her quiet attention makes him wish she would choose one of them and begin.'),
    b('april', 'Garrett told me about the exit and the finishing time. I am asking about the next order.'),
    b('ivan', 'The intermediary is withdrawing. I intend to keep the operation available.'),
    b('april', 'By agreement?'),
    p('He looks at her. She waits. There is no accusation he can rebut in place of answering the question. He could speak about the organisation he hopes to build, the size of what opposes him, the unfairness of being judged at the point where his options narrow. She would still be waiting for the same answer.'),
    b('ivan', 'If I cannot hold one operation, I cannot build anything capable of standing against them.'),
    b('april', 'You keep describing other people’s choices as something you need to hold.'),
    p('He draws the route toward himself. The movement is defensive enough to embarrass him. The proposed takeover is still a proposal; its consequences have not happened. He wants credit for that distinction, although it exists because he has not reached the moment of giving the order.'),
    b('ivan', 'You do not know what it is like to have every useful part of you belong to someone else.'),
    b('april', 'Then tell me what you want me to understand. It will not make the workers part of your escape plan.'),
    p('The answer is neither permission nor refusal to care. He does not know where to put it. He has become accustomed to people choosing one: excuse him because they understand, or judge him because they do not. She has left him responsible in the middle.'),
    b('april', 'Meet with us before this goes any further. Garrett, Neo, Daniel, Tyler and me. Let us say it to you properly.'),
    b('ivan', 'You have already said it.'),
    b('april', 'You have heard a problem to get around. I want you to hear people who will stand in the way.'),
], [
    p('He agrees to the meeting and sends the generals to separate preparations away from the practice room. He tells himself he is preventing a confrontation from spreading. He is also choosing to face his friends where he will not have to hear his generals agree with them.'),
    p('April leaves with what he actually admitted about the proposed compulsion. He has not given her the private files. The thought brings him a mean little comfort, as though keeping one boundary could balance the boundary he is preparing to cross.'),
    p('He remains beside the route until the quiet becomes intolerable. Then he goes to the practice room. There, at least, he knows what to do with a body that will not rest.'),
])

SCENES['IV15'] = ([
    p('April, Garrett, Neo, Daniel and Tyler arrive together. Ivan counts them before he means to. The habit arranges familiar people into distances and possible approaches, and he resents them for making him notice he is doing it. They have brought no easy promise of extraction, no secret door out of the Syndicate.'),
    b('tyler', 'Sit down with us first.'),
    b('ivan', 'Would that make the conversation less prepared?'),
    b('daniel', 'No. It would make it seated. We have not been very subtle about why we came.'),
    p('Ivan almost smiles. Daniel sees the almost and does not use it to pretend the tension has passed. Garrett stays where Ivan can see him clearly. Neo’s attention travels over the room once, then settles back on Ivan.'),
    b('april', 'Stop the order. The dispatch workers are not a resource you can take with the routes.'),
    b('garrett', 'You know what it is like when somebody calls your life part of an arrangement.'),
    b('ivan', 'Do you think I have forgotten?'),
    p('The sharpness changes the room. Garrett lets it reach him without stepping back from the point. Ivan wants someone to offer a reason strong enough to end this. He also wants every reason to fail, because then he can continue without the burden of having chosen badly.'),
    b('neo', 'You can keep whatever history you do not want to tell us. We know enough about this order to say no.'),
    b('ivan', 'And after I stop? They still own tomorrow. Do you have an answer for that?'),
    p('No one answers at once. The silence is honest, and he is cruel enough to welcome it as a weakness. He sees how easy it would be to demand a complete solution from them before accepting a limit on what he does tonight.'),
    b('daniel', 'No. I wish we did. I am still not going to help you make somebody else’s life smaller.'),
    b('tyler', 'We can stay. We can stop this part.'),
    b('ivan', 'You will stop me.'),
    b('tyler', 'If that is what standing here means.'),
    p('For a moment he sees the room at headquarters again: someone stronger refusing him a future. But these people are not asking for his service. They are asking him to leave others a choice. He knows the difference. Knowing it does not make him willing to surrender the plan.'),
    b('ivan', 'I cannot keep asking for permission to live.'),
    b('april', 'Then stop making the question about whether you may control them.'),
    p('He has no answer that does not return to the same fear. If he stops, he will still be trapped. He takes that truth, which they have not denied, and uses it to close the conversation they came to have.'),
], [
    p('Garrett moves into the path to the exit. The movement is measured, giving Ivan time to recognise the boundary before touching it. Neo shifts with him. April is watching Ivan’s shoulders. Daniel and Tyler have stopped trying to find a seat.'),
    b('garrett', 'Last chance to keep this a conversation.'),
    b('ivan', 'I heard you the first time.'),
    p('He wishes that were the same thing as listening. Then he sets his feet. The people in front of him remain his friends, and he begins to prepare to defeat them.'),
])

SCENES['IV16'] = ([
    p('They move as a group. April watches for the turn Ivan favours when someone closes from the side; Garrett supplies the pressure that makes the turn useful. Neo changes the expected entry, Daniel looks for a way to control the follow-through, and Tyler commits to the opening they create. Ivan recognises the thought in it. They have taken him seriously enough to prepare.'),
    p('That should make it harder to be angry. Instead it hurts. They have discussed how to stop him without him in the room. He knows why, and still some part of him experiences their care as another arrangement made around his life.'),
    b('ivan', 'You have been busy.'),
    b('neo', 'We would rather not need it.'),
    b('ivan', 'Then move.'),
    p('Nobody does. He lets the plea harden into a command and feels the familiar relief of having a task. Distances, timing, the body opposite his own: these are problems his upbringing taught him to solve. The reason they are here is harder to hold in his mind while he solves them.'),
    p('He does not find them helpless. Their pressure makes him adjust. A familiar motion becomes unusable, and he chooses another; an opening closes before he reaches it, and he has to make a different one. Each answer comes from years of work he never freely chose and made his own through the effort of surviving it.'),
    b('garrett', 'You can stop without giving them the rest of your life.'),
    b('ivan', 'You do not get to promise that.'),
    p('He is right about the promise. He uses being right about it to avoid everything else. His attention narrows until the room contains positions instead of people who know how he takes his tea, who have heard an unfinished song, who arrived because they did not want to lose him.'),
], [
    p('All five are defeated, and Ivan has chosen to spare them. The room is quiet in the wrong way. Nobody is applauding the precision of what he can do. Nobody has changed their mind. The only thing his victory proves here is that they could not physically stop him.'),
    p('He stands with the dreadful surplus of an action still available after its purpose has gone. He could return to the plan. He could give the next order. The people on the floor would remain the people who came to stop it, and winning would not make them admire him for proceeding.'),
    b('ivan', 'I told you to move.'),
    p('The words sound smaller outside him. Garrett looks up but does not supply the argument again. Ivan has defeated their ability to keep standing in the way. He has not defeated the reason they stood there.'),
    p('He takes one step toward them, uncertain whether help from him would be welcome. Before he can ask, another presence reaches the entrance. His whole body recognises the change. He has spent the evening demonstrating power, and someone has arrived who can make it feel like a rehearsal.'),
])

SCENES['IV17'] = ([
    p('Sylvanis arrives at the branch’s declared practice-room rendezvous, a place on an ordinary oversight schedule. The humiliation begins with that ordinary fact. Ivan has imagined himself reaching beyond the Syndicate’s grasp, and the man at the door has found him by coming where he said he would be.'),
    b('sylvanis', 'There you are. And you have brought an audience. Oh, Ivan. You should have told me it was a performance.'),
    b('ivan', 'They are leaving. You can leave with them.'),
    b('sylvanis', 'Can I? How generous. I do love being given something I already have.'),
    p('He moves into the room with an eagerness that makes the mockery secondary. This is not a reluctant official sent to restore order. Sylvanis wants the confrontation for himself. His attention fixes on Ivan with a delight that stops abruptly, becomes exact, and is worse for the silence.'),
    b('sylvanis', 'Show me what you have been building.'),
    p('Ivan sets himself. There is still a possible future in which he makes this man step back. He has furnished that future carefully: Sylvanis surprised, the title finally insufficient to describe the threat, an order failing in the speaker’s mouth. The need to reach it is almost unbearable.'),
    b('ivan', 'You think I cannot change anything.'),
    b('sylvanis', 'No. I think you are desperate to change who gets to give the orders. Much funnier.'),
    p('Ivan’s anger steadies rather than scatters. He knows how to use it. Tranquility sharpens the instant in which he perceives the opening; the rest of his body still has to carry him there. Across from him is a difference in power no amount of resentment can make imaginary.'),
    p('He refuses the comfort of blaming what he has given his generals. His strength has not vanished into them. He is here with what he can do, and Sylvanis is here with more. It is the fact Ivan has spent years trying to turn into a temporary inconvenience.'),
    b('sylvanis', 'Come on, then. Do something I have to remember.'),
    p('Behind Ivan, his friends are still present. He cannot turn this into a private fantasy of triumph. They will see whatever happens. For the first time that evening, there is no useful way to make the audience smaller.'),
], [
    p('A little blood gathers at the seam of Sylvanis’s glove. Ivan has cut through it. The line is small enough that it might disappear beneath a fold of dark cloth, but it is there. For one disloyal instant his mind tries to enlarge it into the thing he wanted: proof that the whole distance between them has closed.'),
    b('sylvanis', 'There. A little blood. You can keep that. Shall I put it beside your other achievements?'),
    p('Sylvanis raises the hand, inspecting the mark. His opaque mask conceals everything it concealed before. Then his attention returns to Ivan, sudden and avid. The next violence gives the wound its proper scale: a success inside a defeat, nowhere near enough to reverse it.'),
    p('Ivan knows what is coming soon enough to begin an answer. He cannot make the answer sufficient. His control breaks against a force that does not need to borrow his hesitation. The floor meets him, and for a moment he can do nothing except feel the effort of trying to rise.'),
    p('This is the part he had never allowed the imagined confrontation to contain. In it, he had always found one more opening, one more refinement, some final use of a life spent becoming exceptional. On the practice-room floor, the next movement is simply too much to complete.'),
    b('ivan', 'You have made your point.'),
    b('sylvanis', 'Have I? You spent so long making yours. Five friends, all that fuss. I would hate to rush.'),
    p('Ivan plants a hand and tries again. Sylvanis watches with cruel interest. He need not pull the mask aside or raise his voice to make the attention intimate. Ivan is aware of every witness, every failed effort to recover the posture he uses when he has nothing else left to control.'),
    b('sylvanis', 'A Syndicate pet, dreaming about who he will own when the door opens.'),
    b('ivan', 'I am not yours.'),
    b('sylvanis', 'Then stop looking at me as if I am the door.'),
    p('The sentence finds the place Ivan has been protecting. He hates Sylvanis’s freedom almost as much as his cruelty: the ease with which he chooses a fight, leaves a room, makes cooperation something other people must maintain. Ivan has wanted him beaten partly so he could stop measuring his own captivity against that ease.'),
    b('sylvanis', 'You were given a title and thought they had given you yourself. That is the lovely part.'),
    p('Ivan cannot answer without giving him more. Silence is all he has left that does not require standing. He keeps it, though it feels nothing like victory.'),
    p('Sylvanis leaves him alive. The departure is almost casual after the intensity of the fight. He has had what he came for, and he does not need permission to end the encounter. Ivan follows the sound of him leaving until there is nothing left to follow.'),
    p('Then he notices that Garrett is still watching him. The shame comes back in a different shape. These are people Ivan has hurt, and he wants them close enough to keep the room from becoming empty. For a while he can neither ask nor make himself stop wanting it.'),
])

SCENES['IV18'] = ([
    p('At home, the piano lid is closed. Valentina has put a chair near it so Ivan does not have to lower himself onto the bench. He notices the arrangement and nearly objects on principle. Then he sits, which costs enough that he is grateful she does not comment.'),
    p('April, Garrett, Neo, Daniel and Tyler remain in the room. Nobody has come to celebrate the outcome. Practical care occupies the first minutes because practical care can be given while people are angry. Ivan accepts water from a hand he remembers trying to defeat.'),
    b('ivan', 'The dispatch takeover stops. I called the pressure temporary because I wanted it to be somebody else’s problem.'),
    b('april', 'Then keep it stopped. We can help look for safer choices. We will not help you take theirs.'),
    p('He nods. It is a smaller response than the speech he had prepared on the way home. The speech explained everything. The nod leaves the obligation where she put it.'),
    b('ivan', 'I hurt you. I knew who you were, and I did it anyway.'),
    b('garrett', 'Yes.'),
    p('The answer lands without punishment added to it. Ivan waits for a reassurance that does not come. Garrett stays seated. Both things are true at once, and Ivan has to remain in the room long enough to let them be.'),
    b('daniel', 'I am not ready to make it a good story about how we helped you. It hurt. I still wanted to come.'),
    b('tyler', 'Next time, call before you give the order.'),
    b('ivan', 'You make next time sound ordinary.'),
    b('tyler', 'It will happen. We should have something better ready.'),
    p('Ivan looks at Valentina. He had wanted to build something that would free them both. He has also wanted her to recognise the scale of that effort whenever she questioned the harm it caused. The wish remains in him even now, inconveniently alive after defeat.'),
    b('valentina', 'I am still angry. I can sit beside you while I am angry.'),
    b('ivan', 'I do not know how to stop hearing him.'),
    p('No one asks which sentence. The room heard enough. Ivan looks down at his hands. They are his hands, capable of music and injury and the small decision not to close around a reply before somebody else has finished speaking.'),
    b('neo', 'You do not have to give us the rest of your history to make us stay. What you do next matters.'),
    b('ivan', 'I still want out. I have not become content with any of it.'),
    b('april', 'I did not ask you to be content. I asked you to stop the takeover.'),
    p('He lets the distinction stand. Restraint will not require him to call captivity acceptable. It will require him to stop using captivity as an answer to every person he might hurt on the way out.'),
], [
    p('The coercive operation is cancelled. Ivan sends the instruction without turning it into a proclamation about the sort of man he has become. The network remains, with people whose loyalty he will have to answer for in separate rooms and on less convenient days. One stopped order cannot make those conversations unnecessary.'),
    p('He makes room at the piano. Valentina sits beside him, and for a moment he lets the unfinished music wait while he listens to the people around it. The Syndicate obligation on his schedule is still there. He will keep building his power secretly. He cannot promise that the wish to be strong enough will stop frightening him into bad decisions.'),
    b('ivan', 'I do not have a date to offer you. For any of it getting better.'),
    b('garrett', 'Then do not offer a date. Tell us when you are about to do something you do not want us to see.'),
    p('That will be difficult. He knows it before he agrees. It will require admitting a thought before he has made it persuasive, allowing someone else to stand beside the plan while it can still be changed. He has spent most of his life learning to present a finished answer.'),
    b('ivan', 'I can try that.'),
    p('He is still in the Syndicate. Sylvanis can still leave rooms that hold him. There is no victory hidden inside the defeat, no release waiting to reward the right words. But when Valentina shifts beside him, he does not move to protect the unfinished page from her view. He leaves it where they can both see.'),
])

SPARING = [
    b('ivan', 'No. It ends here.'),
    p('He releases the pressure and steps back. All five are alive. The next act is still his to choose, and he chooses not to kill them. Sylvanis has not yet arrived; no interruption can take the decision out of his hands.'),
    p('For an instant, the absence of a command leaves him unsteady. He has been fighting toward a clear result. Now he must look at the result as himself, without the task to stand between him and what he has done.'),
    b('ivan', 'Do not try to get up yet.'),
    p('It sounds like another order. He hears that too. He lowers his hand and gives them space, frightened by how badly he wants this small mercy to make the rest of the evening different.'),
]

CHOICES = {
    'IV01': {
        'music': [b('ivan', 'Once more. Tell me where you expect it to end.'), p('He plays the phrase without looking at the time. Valentina waits past the expected last note, letting him hear the space he has made. He marks the page only after the sound is gone.')],
        'rhythm': [p('Valentina taps the old, deliberately wrong ending. Ivan begins to correct it, catches her eye, and repeats the error exactly.'), b('valentina', 'Excellent. Years of training finally useful.'), b('ivan', 'Please put that in my professional biography.')],
    },
    'IV03': {
        'private': [p('He closes the file without making a copy for anyone else. Valentina can be close to him without having to witness every discovery. For tonight, choosing not to explain is the one part of this history he can decide for himself.')],
        'excerpt': [p('He sets aside the part about the engineering and sale for Valentina alone. He leaves the rest of the file closed. Preparing something to show her is different from having shown it; for now the conversation is still his to begin.')],
    },
    'IV06': {
        'hear': [b('ivan', 'Show me where my route fails.'), b('valentina', 'Here. You counted the time we saved and left out the time they lost.'), p('She takes him through it without making the explanation kinder than the facts. He listens all the way to the altered exit.')],
        'object': [b('ivan', 'I still dislike losing that much time.'), b('valentina', 'So do the people you were going to take it from.'), p('He does not withdraw her authority. The objection remains between them, stripped of the comforting idea that only one side has something to lose.')],
    },
    'IV07': {
        'answer': [b('ivan', 'Who still uses the route?'), b('sowon', 'Now we can talk about it.'), p('She turns the notes so they can examine them together. He lets the people on the route remain the subject until she has finished, without trying to win the timing argument again.')],
        'defer': [b('ivan', 'The deadline cannot move.'), b('sowon', 'That answers when. I will keep asking why.'), p('She marks the unresolved concern beside the timing. He has a schedule he can use, and an objection he has chosen to carry forward unanswered.')],
    },
    'IV08': {
        'limit': [b('ivan', 'This assignment ends where the first page says it ends. The next one requires another conversation.'), b('kouji', 'Good. Please remain this clear when I arrive for that conversation.'), p('He smooths the first page with his palm, relieved by a limit he can actually point to.')],
        'review': [b('ivan', 'We will settle the next stage at the review.'), b('kouji', 'We will discuss it. Settled is what happens after I answer.'), p('Ivan agrees to the distinction. Kouji leaves the second page unsigned by any promise in the room.')],
    },
    'IV09': {
        'discuss': [b('ivan', 'Tell me which instruction you cannot accept.'), p('Paul identifies it precisely. He does not make the whole network defend itself at once. Ivan hears the limited objection without answering it with the larger fact that he has offered shelter.'), b('paul', 'That is what I needed you to hear.')],
        'review': [b('ivan', 'At the command review. Before we agree the next instruction.'), b('paul', 'Before is the part I need you to keep.'), p('Ivan gives him a specific place in the discussion. Paul accepts the arrangement without turning the waiting period into agreement.')],
    },
    'IV10': {
        'restrict': [b('ivan', 'No contact with the intermediary’s workers. I am taking that part away from your assignment.'), b('somchai', 'You will send someone else to do the asking.'), b('ivan', 'I have told you the limit.'), p('Somchai nods. Ivan has narrowed the immediate danger. He has not changed the identity of the man he recruited.')],
        'oversight': [b('ivan', 'Direct oversight. Nothing beyond the instruction because you think I would have wanted it.'), b('somchai', 'Then make sure you are clear when it matters.'), p('The agreement is practical, and Ivan keeps it practical. Supervision is something he will have to do, not a property the word gives him.')],
    },
    'IV11': {
        'negotiate': [p('Ivan chooses an agreement with the intermediary. In the negotiation he is precise about routes, cooperation and availability. He speaks as though the intermediary’s consent can cover everyone whose shift will make the arrangement possible.'), p('The agreement is reached. The workers were not at the table. Their extra availability appears among the obligations someone else has accepted on their behalf.')],
        'display': [p('Ivan chooses a display of force. No assault is needed to make the meaning plain. The intermediary sees what refusal might invite and agrees to cooperate.'), p('The workers see enough to change how they leave the building. Ivan has obtained the answer he wanted. The threat continues doing work after the people who brought it have gone.')],
    },
    'IV12': {
        'direct': [b('ivan', 'The old shift exit stays open. Your agreed finishing time stands. I am removing the instruction now.'), p('He gives the correction where it can be acted on. The worker checks that it applies today, receives an answer, and begins collecting their things. They do not pause to make him feel forgiven.')],
        'delegate': [b('ivan', 'I will have the command review it.'), p('The worker asks when. He hears the question clearly and still refers it onward. The request remains unfulfilled; he has turned something he could settle here into another wait.'), b('garrett', 'They asked you because you could answer.')],
    },
    'IV13': {
        'private': [p('Ivan hears the remaining objections separately. He gives each person a little more room to speak than the table allowed. They do not acquire one another’s private histories by being called in turn. What he carries between the conversations is the repeated discomfort of being asked for limits.')],
        'review': [b('ivan', 'Keep it here. If it concerns the operation, we all need to hear it.'), p('The operational objections stay in the assembled review. Nobody offers another person’s recruitment history as an argument. Ivan has to hear the disagreement in the room he hoped would confirm his decision.')],
    },
    'IV14': {
        'admit': [b('ivan', 'I intend to compel the intermediary to continue. That is the order you are asking about.'), p('April lets the sentence remain as clear as he has made it. She can take this admission to the five attending the intervention. He has given her the proposed action, not the private files behind his anger.')],
        'temporary': [b('ivan', 'Forced cooperation, for now. Long enough to secure the operation.'), b('april', 'For now ends when you decide it ends?'), p('He does not deny it. She has his plan and his justification to repeat to the intervention group. The word temporary has not made the intended compulsion disappear.')],
    },
    'IV15': {
        'limited': [b('ivan', 'I cannot leave them. Not freely. Whatever you think my rank means, it has never meant that.'), p('He gives the five that much and no more. The origin papers, the signed order and the generals’ private identities remain outside the conversation.'), b('neo', 'I heard you. It does not make this order right.')],
        'present': [b('ivan', 'I am not opening my life for you to decide whether I have suffered enough to want out.'), b('garrett', 'You do not have to. We came about what happens next.'), p('He keeps his history private. They remain in the room, refusing both the order and the idea that he must surrender his privacy to deserve their concern.')],
    },
}


def callbacks(data):
    """Consequences in Ivan's private POV; never a shared recruitment dossier."""
    index = data.get('chapter', 0)
    choices = data.get('choices', {})
    out = []
    if index in (11, 13, 17) and 'IV11' in choices:
        out.append(p('He remembers the agreement and how easily the intermediary’s assent stood in for the workers’ own. Nobody had needed to raise a hand to take their time.' if choices['IV11']['value'] == 'negotiate' else 'He remembers the workers changing their route after the display. The force had remained in their evening long after he was finished using it.'))
    if index in (12, 17):
        echoes = {
            'IV06': {'hear': 'Valentina had shown him the cost he left outside the route. He had been able to listen then.', 'object': 'He had let Valentina’s decision stand while disliking it. Disagreement had not cost him her presence.'},
            'IV07': {'answer': 'Sowon had turned her notes toward him when he finally asked who was in the way. The work became clearer, not weaker.', 'defer': 'Sowon was still owed an answer about the objective. He could remember the deadline more easily than the reason he had used it to stop listening.'},
            'IV08': {'limit': 'He had given Kouji an end to an assignment. That limit would matter most when it became inconvenient.', 'review': 'Kouji had agreed to a discussion. Ivan could not honestly remember it as agreement to the next job.'},
            'IV09': {'discuss': 'Paul had asked him to hear one exact concern. It had taken less time than avoiding it.', 'review': 'Paul had asked to speak before the next instruction was settled. Ivan still had to keep the word before.'},
            'IV10': {'restrict': 'He had kept Somchai away from the workers. The restriction remained necessary because of a danger he had chosen to empower.', 'oversight': 'He had required direct oversight of Somchai. He would have to keep providing it; writing the limit had not done the work.'},
        }
        for key, versions in echoes.items():
            value = choices.get(key, {}).get('value')
            if value in versions:
                out.append(p(versions[value]))
    if index == 17:
        out.append(p('The shift exit is already open and the agreed finishing time restored. Ivan leaves that correction in place without presenting it as payment for everything else.' if choices.get('IV12', {}).get('value') == 'direct' else 'The shift-exit request is still waiting because he referred it onward. Ivan now removes the restriction and confirms the finishing time. He names the delay as his responsibility before he can describe it as a misunderstanding.'))
        out.append(p('He returns to the unfinished phrase. This time he does not reach for a tidy last note. Valentina listens beside him until he decides where to stop.' if choices.get('IV01', {}).get('value') == 'music' else 'Valentina taps the altered ending on the piano lid. He answers with the same chosen mistake. For these few beats he is present, listening for her reply instead of the next instruction.'))
    return out

