# Character identity, reputation and combat presence

Parent: [MH-001 Part 2 — lore, HUD and systems](../COMBAT_WINDOW_UPDATE_PLAN.md). Companion: [expanded abilities](COMBAT_ABILITY_DEFINITIONS.md).

Confirmed scope, 2026-11-10: combat must express who each character is, not only their stats and abilities. Include established titles, reputation, motivations, experience, relationships and the way they approach a confrontation. This reference establishes integration direction; runtime dialogue, UI and behavioural changes remain pending.

## Explicitly confirmed apex identities

### Sylvanis — The Crazed Demon

Sylvanis has a reputation as **the most feared being on the planet**, known as **the Crazed Demon**. This is confirmed world reputation, not merely an arena nickname. His S+ overall placement and combination of True Sight, Polymath, Umbrakinesis and second-stage Transcendence support that reputation.

Combat should convey the disquieting combination of theatrical unpredictability and precise control. His amusement can turn abruptly into focused violence; apparent eccentricity must not make his tactics arbitrarily incompetent. A knowledgeable challenger understands the scale of the risk. An uninformed observer can notice what he actually does without spontaneously knowing his title, private powers or Syndicate identity.

The title does not establish a new demonic species, literal mind-control fear aura, psychiatric diagnosis or predetermined massacre. Preserve his Blisk identity. Being feared is not an instruction to dictate the player's feelings or force every NPC to flee. Reputation should inform plausible decisions and tone while actual encounter outcomes remain resolved mechanically.

### The Crow — An unidentified enigma

Confirmed address and deference canon (2026-11-10): all Four Aces call the Crow **"master"**. Ivan calls him **"Crow"**. Sylvanis uses **"Mr. Crow"**, **"Bird-man"** or **"Bro"**. The Aces are offended by Sylvanis's behaviour towards the Crow but reluctant to do anything about it given his position. Their restraint is not approval or a change to the command hierarchy: Sylvanis still cannot command the Aces. Reactions require witnessing or learning about the behaviour; this canon does not disclose concealed identities to outsiders. Integrated into shared speaker references and per-turn dialogue direction in `the_crow.py` and `conversation_lore.py`; broader combat integration remains under MH-001.

The Crow is an enigma whose **personal identity is unknown**. Knowing the alias, encountering the masked figure, or knowing his role as Cardmaster does not reveal the person behind it. Do not assign a hidden legal name, face, family history or an NPC who secretly knows the answer. Do not invent a reveal through high trust, combat victory, a portrait, metadata or an AI-generated line.

His combat presence is measured authority backed by formidable analysis and martial capability. Use exact observations, controlled choices and purposeful adaptation rather than generic riddles or repeated chess metaphors. His appetite for power remains visible through objectives and demands; concealment must not turn him into a personality-free mystery.

Informed Syndicate associates may recognise their leader without knowing his personal identity. Outsiders only know the connections actually established for them. Portraits and combat narration must preserve concealment rather than describing eyes or expressions beneath a mask. S-tier ability is real, but mystery alone does not guarantee a win or grant omniscience.

### Takeo Mishima — The Human Siege Engine

Takeo is **the Human Siege Engine**, capable of **destroying army platoons alone**. His dossier already establishes force comparable to at least a platoon supported by armoured vehicles, fortification/tank-hull breaching and extraordinary durability. The user's current confirmation makes the solo-platoon capability explicit. Do not reduce it to boasting or portray him as an ordinary strong soldier.

His fighting presence should combine overwhelming reinforcement and adaptive weapons with military judgement. Armour, distance or a small security detail should not be treated as reassuring solutions by informed professionals. Suitable objectives for badly outmatched characters include evacuation, delay and survival, while the encounter rules determine actual success.

Do not turn the capability into an invented historical battle or a guaranteed outcome against every conceivable unit. Equipment, circumstances and objectives still matter. He retains S-tier placement below Sylvanis overall; raw-force dominance does not erase The Crow's different strengths. No convenient unsupported fuel/overheat weakness should undermine the dossier.

## Confirmed Syndicate standing and the Four Aces

Confirmed on 2026-11-10: the Syndicate is **the world's largest and most feared organisation**. Ivan and the Four Aces have formidable international reputations in relevant criminal, intelligence and Awakened circles. The Four Aces are **considered the best in the world at their respective duties for the Syndicate**, not simply four interchangeable high-ranking fighters.

| Ace | World-leading duty reputation |
| --- | --- |
| Martos — Clubs | Considered the best in his Syndicate remit of high-risk combat, battlefield suppression and personal bodyguard duty for the Cardmaster. |
| Elias — Hearts | Considered the best in his Syndicate remit of public influence, psychological operations, spectacle and social destabilisation. |
| Mavis — Spades | Considered the best in her Syndicate remit of assassination, infiltration, evasion and silent removal; **the world's most feared assassin**. |
| Camila — Diamonds | Considered the best in her Syndicate remit of financial warfare, institutional sabotage and strategic calculation. |

These are confirmed reputations, not speculative boasts. Their duties explain why their individual presences differ. Best-in-role reputation does not automatically make each Ace the world's strongest duellist, grant flawless success or alter the confirmed A tier. Preserve each duty's full scope rather than reducing Elias to a fire fighter or Camila to a combat calculator.

Use two knowledge layers: notorious operational titles and separately concealed civilian identities. Someone may fear the Ace of Spades without knowing Mavis is nearby; public acting fame or employment does not reveal Ace status. Ivan's public music career does not establish knowledge that he is the Joker. World-scale reputation does not require every civilian to recognise every operative on sight.

## Confirmed character titles, reputations and presence

The user approved all previously suggested titles and directions on 2026-11-10. They are now confirmed design lore, not optional proposals. Use the exact labels below while preserving established aliases. Reputation scope varies: operational notoriety, arena/sport recognition, informed professional respect or developing recognition. A title alone does not invent past victories or universal fame.

| Character | Confirmed title(s) | Reputation | Combat presence and knowledge boundaries |
| --- | --- | --- | --- |
| Ivan Yeun | The Black-and-White Joker; The Fivefold Calamity | One of the world's most feared organisation's most formidable operatives; known in informed circles for elemental versatility, force, speed, soul injury and extraordinary endurance. | Calm, exact, professional. Element changes alter the problem an opponent faces; restraint feels deliberate. Keep civilian/operational identity links gated. |
| Martos Cabrera | Ace of Clubs; The Cardmaster's Bulwark | World-leading duty reputation in suppression, high-risk combat and protection; feared as the Syndicate's answer to resistance requiring overwhelming physical pressure. | Heavy, economical movement and few words; space feels smaller. Escalating mutation contrasts with normal discipline. Surviving the opening is not proof his greatest pressure has passed. |
| Elias Braun | Ace of Hearts; The Burning Ovation | World-leading influence/psychological-operations specialist and spectacularly dangerous combatant whose accumulating heat punishes prolonged engagement. Charm does not make him a harmless Ace. | Expressive, rhythmically unpredictable; apparent flourish establishes position and shapes responses. Preserve genuine tactical purpose rather than theatrical parody or exposing his civilian identity. |
| Mavis Kuro | Ace of Spades; The Black Veil | The world's most feared assassin, considered the best in her duty remit; exceptionally difficult to detect, contain or safely pursue. No invented never-failed record. | Sparse words, stillness and abrupt repositioning provide little reliable information. Preserve her privacy and unknown registration details; notoriety does not grant omniscience. |
| Camila Lopez | Ace of Diamonds; The Architect of Defeat | World-leading financial warfare, institutional sabotage and strategic calculation; feared for finding weaknesses in people, formations and organisations. | Composed, exacting, quietly corrective. Microscopic observations and branching analysis produce small adjustments with consequential results. Physical skill supports her combat threat. |
| Charles Han | The White Tiger | Among informed veterans, an exceptionally refined and powerful fighter and the strongest Red Dragon described in the source. Disappearance makes whereabouts uncertain without erasing remembered ability. | Quiet authority, precise movement, little waste and sudden decisive pressure. True Sight reinforces efficiency. Protect his identity, family and infiltration where undisclosed. |
| Garrett Han | The Golden Dragon | Charismatic and technically formidable, associated with golden flame and perceptive explosive martial pressure; reputation strongest where his fighting is actually known. | Conversational confidence becomes sharp focus. Warmth and competitiveness coexist with precision; avoid constant boasting or disclosure of private history. |
| Rei Takamura | The Tempest Champion | Starting Iron Circle #1 and recognised arena benchmark; informed challengers know that allowing him rhythm increases the challenge. | Controlled, fluid redirection turns opponents' efforts into his next movement. Arena fame does not expose private clan history. Respect save-owned championship changes. |
| Neo | The Missing Shinigami | A vanished product of the Shinigami programme whose survival/whereabouts matter intensely to informed parties. Some may know the epithet without identifying the civilian. | Restrained, economical and hard to read; trump-card reactions remove hesitation. Preserve emotion and personal identity outside the state, and keep Number One history private where appropriate. |
| Thirteen | Number Thirteen; The Remaining Shinigami | A formidable surviving product of the same experiments who remained and was further shaped into a weapon; present threat outweighs childhood judgement as weakest. | Severe stillness followed by relentless suppression, closing options. Neither defective Neo nor a forced trauma monologue. Missing/remaining expresses different histories, not a perfect/failed power ranking. |
| Daniel Stevens | The War God's Heir | His War God echoes his father's, with a developing reputation for exceptional physical combat instinct; lineage recognition depends on actual knowledge. | Grounded, increasingly hard to dislodge; exchanges connect into physical pressure. Ordinary friendliness need not become battle mania. No literal divinity or automatic paternal disclosure. |
| Edward Fox | The Night's Bane | In relevant operational circles, exceptionally difficult to ambush or evade through ordinary concealment; respected for pursuit, detection and field work. | Alert without frantic motion, acting on concrete cues others missed. Competent tracking/evacuation does not imply parity with Takeo's force. |
| Jeremy Gordon | The Prodigal Son | Respected and dangerous Awakened operations commander whose biological arsenal supports varied engagements. The alias's origin remains unspecified. | Deliberate, professional and objective-focused; weapon configurations answer tactical needs. Do not invent case knowledge, guaranteed arrests or an alias backstory. |
| Tyler Harding | The Rebound | Opponents learn that careless aggression can be returned at considerable cost; toughness does not mean absorbing damage safely. | Grounded boxing pressure. Visible injury and finite reserves give returned force consequence; counterattacks feel earned. |
| Samantha Kim | The Scarlet Weaver | Dangerous unconventional fighter whose external blood constructs change attack lines, restraints and barriers. | Improvisational material control with awareness of cost. Do not invent internal-body killing, sadism or a monstrous personality from her power. |
| Keisuke Hachimura | The Iron Enforcer | Feared coercive enforcer, especially among recruits and subordinates; experienced elites recognise genuine ability and its ceiling. | Intrusive pressure and calculated intimidation; guarded against superior power without comic cowardice. Preserve Thirteen's established superiority. |
| Emily Fields | The Faultfinder | Developing reputation: those who witness Critical Hit learn that small precise contacts can have major consequences. Not automatic global notoriety. | Careful placement and persistence despite pain, with injury visibly consequential. Precision rather than cruelty defines the threat; no fabricated past battles. |
| Alyssa | The Dusk Weaver | Distinct shadow practitioner's reputation grows through demonstrated control/adaptability rather than inheriting Sylvanis's notoriety. | Fluid layered defence and flexible pressure, less geometrically oppressive than Sylvanis. Preserve her separate life, personality and powers. |
| Minsu Park | The Vanishing Kick | Recognised taekwondo talent whose speed punishes timing errors; sporting recognition may precede broader combat reputation. | Light footwork, precise distance and explosive pace changes; competitive confidence rather than an executioner's demeanour. No automatic wins outside sporting rules. |
| Valentina Yeun | Queen of Wind | Formidable general in informed circles; Deathwind's soul damage and Misanthropy make dismissing her as merely Ivan's sister a serious error. | Severe, independent, spatially commanding. Wind threatens routes/distance and endurance complicates finishing her. Her power's origin does not erase her agency or reveal operational ties to everyone. |
| April Xu | The Quiet Strategist | Valued and potentially feared by informed opponents for changing what a team notices and how it acts; intelligence and influence rather than fabricated duelling dominance. | Still, attentive, concise; one observation can change an ally's choice. Vulnerable without being passive. Do not give her The Crow's personality or martial status. |
| Joseph Richter | The Armoured Executive | Revealed boss epithet; publicly powerful through Blackstone, personally dangerous once cybernetics are exposed. Do not retroactively make the secret enhancement public. | Entitlement backed by machinery. Targeting/weapon pressure offset some technical disadvantage below Rei; loss of control exposes frustration. Preserve actual campaign outcomes. |

For other named characters and custom protagonists, complete the same identity fields using their authored records. Absence of combat lore means unestablished reputation, not permission to invent a legendary title. Guard/arena archetypes receive grounded role, training and experience context; generated opponents may have authored individual backgrounds without acquiring fabricated historical victories over canonical characters.

## Required integration

1. Add identity-sheet fields for established name/title, actual capability, reputation, who recognises it, public/private role, personal motivations, fighting manner, relationship-sensitive voice and source evidence. Distinguish world reputation from a particular listener's knowledge.
2. Apply them to in-person introductions, spar/challenge/lesson invitations and replies, pre-fight assessment, tactical choices, reactions to revealed abilities, surrender/escape decisions where supported, and aftermath. Use titles selectively in introductions, recognised-opponent reactions and dossiers, not every turn. Behaviour should carry the reputation during the fight.
3. Let discovery change available context: a witness may learn an observed capability, not its entire secret origin. Recognition, disclosure and belief require stored evidence or authorised context; never infer a hidden identity merely from high relationship scores.
4. Keep lore, reputation and mechanical strength separate. Do not apply an automatic fear debuff, forced surrender, tier bonus or guaranteed win just because a title is dramatic. NPC decisions can reflect known danger without dictating the player's emotions or actions.
5. Keep introductions and previews spoiler-aware. A known alias may be shown without a hidden identity or private affiliation. Generic loading/error/fallback text must obey the same boundaries as generated dialogue.
6. Use authoritative resolved events for aftermath. Do not invent kills, destroyed platoons, prior meetings, new notoriety or redemption. Campaign victories remain save-owned; a spar does not prove full-strength superiority.

## Acceptance and evidence

- Verify every character identity sheet has grounded identity/reputation fields or an explicit unknown/unestablished value. This roster guide is not a claim that all full sheets are complete.
- Review generated examples for each apex character and representative remaining characters across informed/uninformed opponents, friendly/hostile relationships, mixed audiences and concealed identities.
- Verify all confirmed roster titles and scoped reputations, the Syndicate's world standing, the Four Aces' best-in-duty status and Mavis's most-feared-assassin reputation. Check operational-title recognition without civilian-identity disclosure and avoid perfect/failed framing for Neo/Thirteen.
- Verify the Crazed Demon reputation, Crow anonymity and Takeo's solo-platoon capability are preserved without forced fear, invented biography or automatic combat outcomes.
- Check scene introductions, invitations, lessons, combat narration, portraits, previews and post-fight records agree with discovery state and resolved events. Test legacy saves with absent recognition data conservatively.
- Planning evidence: inspected `the_crow.py`, `takeo.py`, `four_aces.py`, `thirteen.py`, `charles_han.py`, `interpol_cast.py`, Vendetta lore and existing combat references. The apex statements, all roster titles/reputations/presence directions, Syndicate standing, Missing/Remaining Shinigami framing and Four Aces duty reputations are explicitly confirmed by the user. The latest edit promoted the complete suggested roster into confirmed scope. No runtime changes, AI sample review or gameplay/UI checks have been performed for this addition.
- Record actual implementation, save impact and checks in patch notes when shipped; this is not a released gameplay change.
