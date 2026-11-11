"""Authored starting biographies for the owner-facing character selector.

Sources: Character References public/familiar rows, RPG Game dossiers,
hidden_cast, four_aces and interpol_cast. No future campaign outcomes.
These paragraphs are menu copy, never an NPC knowledge/disclosure source.
"""

BIOGRAPHIES = {
    'garrett': (
        'Garrett Han grew up in Hong Kong, where cooking meant family, noise and remembering what someone liked. After losing his parents young, he grew up under his older brother Charles’s care. His confidence and street fighting earned him the name Flaming Prince, but learning to take responsibility demanded more than winning a crowd. At eighteen he moved to Winterfield with his childhood friend April, eventually building a life around the Golden Dragon restaurant.',
        'Now a charismatic host and proud cook, Garrett balances the restaurant with leading the Red Dragons triad. Jeet Kune Do and Sanda remain part of his life, as do the quieter pleasures of feeding friends after closing. Rei became his best friend through repeated late meals and conversations at the Golden Dragon. Charles’s disappearance leaves a painful absence behind Garrett’s easy charm, and the search for his brother gives his present life an unfinished question.'),
    'rei': (
        'Rei Takamura has built a life in downtown Winterfield around art, work and the home he shares with his younger adoptive sister Yuriko. At seventeen a job painting studio backdrops unexpectedly led to modelling; his first cheque bought an easel and a rice cooker. Drawing, poetry and cooking give him ways to choose the shape of an ordinary day. Friends from school remember the quiet boy with a sketchbook before they remember the model.',
        'Beyond the studio, Rei is the reigning underground fighting champion of the Iron Circle. His precise fighting contrasts with a reserved manner and understated humour, but neither tells his whole story. Gaps in his childhood memories remain unresolved, and protecting his home does not make those questions disappear. Friendship with Garrett offers room for silence as well as conversation, while Yuriko’s growing independence asks him to care without making her decisions for her.'),
    'minsu': (
        'Minsu Park grew up in the United States with school holidays spent visiting family in Korea. His family encouraged both school and sport without expecting him to repeat the career of his older sister Jiwon, an Olympic taekwondo medalist and coach. Now a medical student in Winterfield, he is also a national taekwondo gold medalist and black belt. He enjoys understanding why something works, whether it is a clean kick or a scientific explanation.',
        'Training and study share space with anime, co-op games and surprisingly careful food reviews in the margins of his planner. His enthusiasm invites other people in rather than demanding an audience. Amy lives a dorm away and is willing to question his conclusions, including his snack ratings. Minsu’s everyday life brings together ambition, curiosity and friendships that matter beyond either grades or medals.'),
    'ivan': (
        'Ivan Yeun is a singer and model whose disciplined performances can hold an enormous audience, though he is far more reserved away from the stage. He learned harmony by following the kitchen radio and inherited a practical patience for repairs. He and his adoptive sister Valentina share the Ferry Signal House, where his piano and her sail bench make room for two distinct lives. Their closeness does not erase her wish to answer for herself.',
        'Alongside his public career, Ivan is a Syndicate executive: the Black and White Joker Card, with responsibility for affiliates across Russia and Asia. That private authority sits uneasily beside his wish for a life of his own. Rehearsals, martial arts and careful follow-through reveal his discipline; a repaired piano key or a shared duet shows a quieter side. His obligations remain part of his starting situation, without deciding how his future must unfold.'),
    'yuriko': (
        'Yuriko Takamura studies theatre design at Winterfield University and shares a downtown home with her older adoptive brother Rei. Miniature sets, costumes and fantasy books give her a world of ideas to work with. She cares about whether a reveal can be seen from the cheapest seat as much as from the front row. Her work asks for patient construction and a willingness to take a model apart when it does not yet work.',
        'Expressive, resourceful and increasingly independent, Yuriko wants her choices to be taken seriously on their own terms. Being the sister of a model is far less interesting to her than making something worth showing. She appreciates a hand offered with permission and resents having a task taken over. University and the workshop give her space to build a future that belongs to her while keeping the home and family she values.'),
    'emily': (
        'Emily Fields works at Petal & Stem, bringing careful attention to flowers, colour and the small practical needs of a customer. As a schoolgirl she built a model greenhouse and shaded its seedlings with a painted pane; making things remains a source of pleasure. LEGO sets, miniatures and collected plushies fill her quieter hours. Her friendships with Rei and Sophie began before fame and public images complicated their lives.',
        'Gentle and sometimes shy, Emily is still capable of a firm correction and prefers help that leaves her in charge of her own work. Her stutter changes with the situation rather than defining her judgement. She begins with the active Trait Critical Hit, which creates weak points and suppresses pain; pain suppression never prevents injury or knockout. Floristry, friendship and creative work remain as much a part of her identity as her awakened abilities.'),
    'sophie': (
        'Sophie Parker is a university runner known around Winterfield as the Track Queen. Training, competition and a public social-media following bring attention to the results she works hard to achieve. She likes the clarity of a timed lap and can give a training partner an honest account of an interval. Her ambition is real, and she is often more demanding of herself than of anyone watching.',
        'Parties, playful teasing and afternoons chosen for fun offer a different rhythm from the track. School lunches with Emily and Rei gave her somewhere to be loud without being assessed, and those friendships predate her public image. Sophie is learning the difference between getting a quick laugh and making someone comfortable. Her life leaves room for recovery and companionship as well as the next performance.'),
    'amy': (
        'Amy Hansen studies philosophy and paints, using both words and images to explore how people understand their lives. A humanities and psychology assignment brings her to interviews with Rei and Garrett, where she listens for the meaning someone gives an experience. She is thoughtful without treating her first interpretation as final. A better explanation can change her mind, and she is willing to say so.',
        'Living a dorm away from Minsu gives Amy a familiar partner for gentle disagreements and everyday observations. Her friendships bring her into contact with different ways of thinking, from April’s precise questions to Samantha’s plain answers. Painting offers another way to work through an idea before she can explain it. Her curiosity is personal, but learning someone’s story does not make it hers to distribute.'),
    'samantha': (
        'Samantha grew up in an orphanage and learned to fight on the street. In Winterfield, motorcycles and training remain central to the life she chooses for herself. She is practical, blunt and comfortable meeting a challenge directly. A place in the arena lounge does not make every encounter a fight; she can talk equipment, technique or the ordinary business of keeping a bike running.',
        'Playful flirting and direct humour come easily, while serious trust asks for more than banter. Samantha values clear intentions and sets her own terms rather than letting someone mistake teasing for a promise. She can offer practical care without dressing it up, and her friends receive different sides of that candour. Her independence leaves room for company when the invitation respects her choices.'),
    'april': (
        'April grew up with Garrett in Hong Kong and moved with him to Winterfield when he was eighteen. Their shared history reaches beyond the confident restaurant owner people meet today. Chess and science suit her habit of looking closely at the assumption underneath an answer. She is willing to spend time explaining a single important move instead of making knowledge into a performance.',
        'Quiet wit and exact questions make April a thoughtful presence among more outspoken friends. She rarely flirts and values being taken seriously without needing to raise her voice. Study and chess tuition give her room to turn careful reasoning into something useful to another person. Her longstanding connection with Garrett remains part of her life, alongside interests and decisions that are her own.'),
    'lena': (
        'Lena Ortiz conserves local photographs at the Old town archive, working with the fragile materials through which Winterfield remembers itself. Her curiosity reaches beyond the subject in the centre of a picture to what has been left outside the frame. Film photography and urban history make that attention part of her life beyond work as well. She approaches a discovery with questions and an irreverent sense of humour.',
        'Away from the archive, salsa and a second-hand record player bring a less painstaking rhythm to her days. Lena deflects praise with wit, but notices whether someone actually follows through. Her clocktower flat holds the practical traces of her interests rather than a polished public image. Conversation grows through shared curiosity and the willingness to look again when a first impression proves incomplete.'),
    'naomi': (
        'Naomi Sato works at the riverside cycle workshop, where a reliable repair matters more than a grand promise. Grounded and observant, she approaches practical problems with patience and a dry sense of humour. Her days involve making bicycles useful and comfortable for the people who ride them. Care often appears in the form of a small problem noticed and properly addressed.',
        'Bouldering, ceramics and mystery novels give Naomi interests well beyond the workbench. Handmade mugs and a climbing hangboard share her riverside home with a balcony herb garden. She prefers clear plans and time to become comfortable with someone, resisting pressure to turn acquaintance into instant intimacy. Her quiet manner leaves room for both firm boundaries and understated warmth.'),
    'celeste': (
        'Celeste Moreau teaches at the hilltop planetarium, helping visitors turn an unfamiliar sky into something they can begin to understand. Expressive and attentive, she enjoys questions that take a demonstration somewhere unexpected. Curiosity matters to her as an exchange rather than a chance to be admired. Her work combines explanation with the pleasure of noticing more than one saw before.',
        'Jazz piano, birdwatching and bread baking shape Celeste’s time away from the planetarium. Her blue-door cottage holds star maps, bird guides and a flour-dusted kitchen alongside the piano. She can be mischievous and warmly engaged while still protecting the quiet hours she needs. Good company makes room for that independence and returns some of the attention she gives.'),
    'dev': (
        'Dev Shah is a technician at the Station makerspace, helping people repair devices and understand what is happening inside them. Patient and inventive, he becomes especially animated when teaching. His practical curiosity can make him reach for a broken object before checking whether its owner wanted a demonstration or simply some advice. Learning to ask is part of making his help useful.',
        'Tabletop games, electronics projects and night photography fill the spaces between repair sessions. His compact studio holds labelled component drawers and board games, with a thriving fern among the equipment. Dev can be absent-minded about ordinary details while remembering a very specific recommendation. Friendship develops through shared projects, patient explanations and time spent enjoying an interest together.'),
    'rosa': (
        'Rosa Bennett coordinates the community kitchen at Lantern market, turning recipes, volunteers and practical arrangements into meals people can share. Sociable and candid, she gives an invitation clearly and checks whether someone can actually come. Generosity is part of her work, but so is knowing what the kitchen can realistically manage. She values participation that helps rather than quietly adding another obligation.',
        'Community gardening, roller skating and recipe swaps extend Rosa’s life beyond the serving counter. Her market terrace has a shared courtyard, cookbook stacks and a large table suited to company. She enjoys bringing people together while keeping firm boundaries around becoming everyone’s caretaker. Her warmth works best when responsibility and attention travel in both directions.'),
    'elliot': (
        'Elliot Brooks trains as a wetland ranger, surveying birds and helping maintain the Willow boardwalk’s trails. Soft-spoken and perceptive, he is comfortable paying attention without filling every moment with conversation. Field recordings preserve some of what he notices, while practical work gives that attention a purpose. His independence is a way of moving through the world rather than a refusal of company.',
        'Kayaking and wood carving occupy time away from ranger training. Carved birds and waterproof notebooks share his cabin near the reeds, where a covered porch offers another place to listen. Elliot’s playfulness becomes easier to see once someone knows him. He appreciates companionship that can include a long silence without mistaking it for something gone wrong.'),
    'tyler': (
        'Tyler Harding coaches boxing at East Ward and takes local bouts for extra money. He patches loaner gloves and makes room for beginners, sometimes letting a trainee choose the music after a full song of skipping rope. He shares a duplex with his father, a disabled veteran who keeps the club’s books. Work, training and responsibilities at home shape the plans he can make.',
        'Dominoes and baseball offer Tyler familiar ways to spend time with someone without demanding a speech. Quiet and practical, he often expresses care through a dependable arrangement or a small task completed. Neo and Daniel have been his best friends since high school. An invitation with a definite time lets him make room for company while respecting the life already around him.'),
    'valentina': (
        'Valentina Yeun teaches sailing with second-hand dinghies, repairing sails and helping beginners find confidence at the tiller. Her adoptive brother Ivan helped buy the first hull, and they share the converted Ferry Signal House. She loves him while firmly wanting to answer questions addressed to her herself. Competence on the water is something she practises and teaches, one turn at a time.',
        'Competitive and independent, Valentina enjoys a challenge and can be gloriously off-key at late-night karaoke. Her sail bench and Ivan’s piano give their shared home two different centres of activity. She likes company willing to take the second verse or try something unfamiliar. Clear invitations and respect for a refusal matter as much as enthusiasm.'),
    'daniel': (
        'Daniel Stevens works as a projectionist at the Bijou repertory cinema and draws its lobby cards. Both of his parents served in the military, and he learned breakfalls growing up, but the achievement he wants them to see is a double feature he has programmed himself. Judo remains part of his life alongside films. His flat above the cinema keeps those interests close at hand.',
        'Reserved at first, Daniel can become surprisingly fierce about a film’s ending after letting his friends choose what to watch. He remembers who needs an aisle seat and appreciates someone waiting while he chooses a drawing to show. Neo and Tyler have been his closest friends since high school. His dry humour and attention to small details make ordinary evenings worth remembering.'),
    'neo': (
        'Neo Ishida repairs electronics at the Station makerspace, bringing patience and practical judgement to radios, controllers and other objects worth keeping. Quiet and observant, he has been best friends with Tyler and Daniel since high school. Dry humour emerges when he feels comfortable, and he shows care by remembering a problem and asking before helping. Being useful does not mean surrendering his own boundaries.',
        'Neo shares an apartment with his girlfriend Alyssa and wants a peaceful ordinary future with her. Co-op games, cooking, controlled boxing drills and riverside walks give their days a familiar rhythm. Repaired electronics sit beside her hand-bound notebooks and kitchen herbs at home. Their committed relationship remains part of his starting life; new connections with him grow as friendships.'),
    'alyssa': (
        'Alyssa is a Blisk woman who works as a bookbinder and archive repair assistant at the Old town archive. Careful handwork suits her gentle, observant manner, and her independence becomes clear when someone assumes quietness means agreement. Binding notebooks and repairing books make useful things out of patient attention. Botanical sketches and small creative projects continue that interest beyond her work.',
        'She shares a station apartment with her boyfriend Neo, where notebooks and herbs occupy shelves alongside his repaired electronics. Cooking together and enjoying quiet domestic time are part of the ordinary future they want. Alyssa has a playful side that becomes easier to see in familiar company. Her commitment to Neo is established, and her relationships with new acquaintances remain platonic.'),
    'sylvanis': (
        'Sylvanis is a Blisk private fight patron whose theatrical courtesy can change abruptly into a cold, precise threat. Brilliant and deliberately cruel, he studies what people rely on and takes pleasure in imagining its collapse. His interest in violence is personal rather than detached: an enticing opponent can draw eager anticipation. Neither humour nor an attentive conversation makes him safe.',
        'His private position is the Coloured Joker Card and the Syndicate’s second-in-command. He pursues chaos rather than simply profit or sporting achievement, and his independence makes cooperation something others cannot assume. Extraordinary combat ability does not grant knowledge of unseen events or guarantee every outcome. His starting life retains that danger and authority without deciding what strangers know about him or promising a redemptive path.'),
    'martos': (
        'Martos Cabrera heads security for Oculus, bringing methodical attention and a difficult-to-hurry temperament to the work. His imposing build is immediately noticeable, but he dislikes the assumption that it explains everything about him. Reliability matters more to him than praise. He remembers a coffee order or repairs a loose chair with the same quiet attention he gives a professional responsibility.',
        'Restoring watches, strength training and cooking rice dishes occupy his time away from public work. An orderly apartment and a watch repair desk suit his preference for patient, concrete tasks. His humour is dry enough to arrive without a change of expression. Getting to know Martos means noticing consistency and chosen acts of care, while respecting the parts of his life he keeps private.'),
    'elias': (
        'Elias Braun is a famous actor whose days involve filming, rehearsal and the discipline behind an expressive performance. He notices when someone has been left outside a conversation and often finds a way to include them. Warmth and comic impressions can be sincere, though he also likes making an impression. Being watched for a living has made control of his off-camera time important.',
        'Repertory cinema, dance rehearsals and trained martial arts give Elias interests beyond a finished screen image. Scripts, film scores and a stretching mat share his quiet home. He would like to be asked what he thought of a scene rather than only how he looked in it. His playful delivery can give way to a plain sentence when something matters, and attention is never a claim on his whole private life.'),
    'mavis': (
        'Mavis Kuro moves through Winterfield under a chosen name, keeping her employer, official birthday and registered identity undisclosed. Watchful and resourceful, she prefers practical questions to personal paperwork. Ambient sound recording gives her a reason to listen closely to rain and the spaces between other people’s noise. She is comfortable with silence and does not treat it as permission for someone to pry.',
        'Repairing headphones and small objects offers Mavis another way to work with her hands and show care without a long explanation. A repaired pair might arrive before an account of how she fixed it. Her very dry humour and independent manner reward attention without promising immediate trust. Her private history stays unresolved in this starting portrait, and neither company nor curiosity entitles someone to it.'),
    'camila': (
        'Camila Lopez is chief financial officer of Oculus, bringing analytical discipline and a competitive mind to difficult decisions. She asks which assumption supports a claim and expects a useful answer. A sharp, fair disagreement can interest her more than easy agreement, and she can revise her position when the evidence warrants it. Uncertainty troubles her more than demanding work.',
        'Chess problems, fountain pens and tango provide interests beyond her public responsibilities. Precise speech and polished challenges are part of her humour, though a desire to solve a problem can make her miss the need simply to listen. She enjoys being surprised away from work and is neither emotionless nor all-knowing. Her ordinary relationships leave space for a person who is more than her professional judgement.'),
    'fox': (
        'Edward Fox is a former mercenary and licensed vigilante working around Blackhaven, Winterfield’s western suburb. Hardened and practical, he has a deeply negative view of organised crime and the exploitation it brings. Equipment repairs, patrols and checking physical leads shape his present routine. He helps through action more readily than reassurance, and his blunt humour leaves little room for empty promises.',
        'As an Interpol associate, Fox works with Jeremy Gordon despite distrust of institutions and impatience with procedure. Respect for Gordon’s competence gives their cooperation a foundation without removing every disagreement. His Eight Senses help him notice physical clues; they do not read minds or turn suspicion into proof. A private workshop and the possibility of an ordinary quiet moment remain part of his life alongside the investigation.'),
    'gordon': (
        'Jeremy Gordon is an Interpol premier operative and leader of Team 9, deployed to Winterfield’s regional headquarters. Disciplined and observant, he asks precise questions and follows corroborated evidence. Command does not keep him away from danger: he engages personally when an investigation turns into combat. His biological weapon Trait, Biocreation, gives him tactical options without making judgement or preparation unnecessary.',
        'Working with Edward Fox brings an effective but sometimes difficult ally into Gordon’s investigations. He respects competence while retaining responsibility for his own decisions and the evidence behind them. Away from reports, witnesses and training, books and a quiet dinner suit his restrained humour. His nearby apartment offers room for an ordinary evening, even when his professional obligations are demanding.'),
}

# Original-cast measurements and types are explicit RPG Game / core PEOPLE facts.
ORIGINAL_FACTS = {
    'garrett': (188, 'ENFJ'), 'rei': (184, 'INFP'), 'minsu': (177, 'ESFP'),
    'ivan': (193, 'ISTP'), 'yuriko': (159, 'ENFP'), 'emily': (154, 'ISFP'),
    'sophie': (170, 'ESTP'), 'amy': (163, 'ISFP'), 'samantha': (168, 'ESFJ'),
    'april': (150, 'INFJ'),
}
# Newly authored menu characterisations where source canon leaves MBTI unassigned.
# Label these explicitly; do not rewrite source canon or NPC knowledge.
MENU_TYPES = {'sylvanis': 'ENTP', 'fox': 'ISTP', 'gordon': 'ISTJ'}
OCCUPATIONS = {
    'garrett': 'Golden Dragon restaurant owner; Red Dragons triad leader',
    'rei': 'Professional model and artist; Iron Circle underground fighting champion',
    'ivan': 'K-pop singer and model; Syndicate executive (Black and White Joker Card)',
    'sylvanis': 'Private fight patron; Syndicate second-in-command (Coloured Joker Card)',
}


def facts(who):
    import four_aces
    import hidden_cast
    import meet_cute
    import story_calendar
    person = hidden_cast.CAST.get(who, {})
    height, mbti = ORIGINAL_FACTS.get(who, (person.get('height', 'Unspecified'), person.get('mbti')))
    if who in MENU_TYPES:
        mbti = MENU_TYPES[who] + ' (authored menu interpretation)'
    occupation = OCCUPATIONS.get(who, person.get('occupation', meet_cute.JOBS.get(who, 'Unspecified')))
    if who in four_aces.CAST:
        ace = four_aces.CAST[who]
        occupation += f"; Syndicate Ace of {ace['suit']} · direct specialist for the Cardmaster"
    return {'Age': person.get('age', meet_cute.AGES.get(who, 'Unspecified')),
            'Occupation / studies': occupation,
            'Birthday': story_calendar.BIRTHDAYS.get(who, 'Unknown'),
            'Height': f'{height} cm' if isinstance(height, (int, float)) else height,
            'MBTI': mbti or 'Unknown'}


def biography(who):
    return '\n\n'.join(BIOGRAPHIES[who])
