# MH-017 — Campaign flashback areas and historical conversations

**Continuity and voice coordination, 2026-11-11:** [MH-019](CAMPAIGN_REVISION_PLAN.md) records the user's selection of Garrett's sixteen-year-old school confrontation as canon and plans reconciliation of the older Mrs Lau/Kit account without inventing a second beating. Its era/voice review preserves this plan's independent historical references and optional-visit isolation. The proposed Auntie Lau companion must not silently reintroduce the superseded event; identity and ordinary-role authoring remain separate decisions. No runtime profile or visit changes are made by this link.

**Status:** Planned — design recorded, implementation pending.  
**Recorded:** 2026-11-11, Australia/Brisbane.  
**Tracking:** [Roadmap MH-017](../ROADMAP.md#mh-017-campaign-flashback-areas-and-historical-conversations).  
**Scope:** Every campaign protagonist has an accessible, repeatable historical area with places to explore and people to talk to. Eight area designs cover nine campaign protagonists; Emily and Sophie retain their existing school access, for eleven supported protagonists in total.

This extends the existing optional flashback-visit feature. A freeform visit is distinct from an authored campaign memory, mission or fight. Room-specific art/implementation follows the approved order: interiors, MH-016, Ace campaigns in order, then Sylvanis. Design and chronology work can proceed now. MH-016 and campaign image production remain paused as recorded; this plan does not resume them or invent a new release priority.

## Plugin task assignments

**Assigned:** 2026-11-11. Planned shared work; interiors/MH-016 dependencies and new-route order remain in force.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Eight areas/nine campaign protagonists: period, room and cast inventory | Story Skills (worldbuilding, character/era continuity, interactive-fiction) | Separate each era and branch, proposed names and confirmed history; preserve Emily/Sophie's existing school access and the Garrett school-confrontation canon decision. |
| Mandatory reference sheet and dialogue style for every character/era | Story Skills + Writer's Loop | Author/review both records, including minor and scripted-only cast; distinguish era personality and voice as well as factual knowledge. No present-day fallback. |
| Optional topics, ordinary activities and campaign-memory boundaries | Writer's Loop + Story Skills | Review openings and follow-ups by period/location and available audience; optional visits must not perform fixed missions, unlock powers or disclose future secrets. |
| Runtime period/room switching and save isolation | falsegreen-skill | Review future-knowledge canaries, missing/unreviewed-profile rejection, stale replies/history, optional-vs-mandatory memory gates and exact live-state restoration; run flashback/lore/save checks and in-person smokes. |
| Historical portraits and reusable room scenery | Bulk BG Remove only for portrait cutouts; Story Skills for era art briefs | Preserve ages, tattoos and concealment; reuse accepted room art only when the era fits. Full scenery painting remains outside the local media plugins. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Current foundation and requested experience

[flashback_visits.py](../flashback_visits.py) currently supports two areas: `school` for Rei/Emily/Sophie and `hong-kong-school` for Garrett. [flashback_visit_ui.py](../flashback_visit_ui.py) embeds them and the memory journal in the main in-person window. Present time pauses; the player can choose companions, speak, perform a freeform action and return. [flashback_lore.py](../flashback_lore.py), [independent character sheets](../flashback_character_references.json) and [historical voices](../flashback_dialogue_guides.json) keep conversations separate from adult lore. Fox/Gordon, the Aces and Sylvanis have no visit areas in this implementation.

The new areas use that experience and the future [room system](INTERIORS_UPDATE_PLAN.md). Each has a recognisable setting, a small room network, an era-specific cast, optional activities and authored conversation openings. Walking between historical rooms stays inside the memory and advances no present-day time.

All new NPC names, extra rooms, exact historical ages and casual incidents below are proposed authoring details. Existing canon, user-established campaign premises and current access are preserved. Stable area/period/room IDs below are design identifiers, not implemented map keys. Character traits, secrets and historical appearances require separate per-period sheets before generation is enabled.

## Coverage and delivery

| Area ID / working title | Protagonist access | Present implementation | Planned delivery |
| --- | --- | --- | --- |
| **school — The Courtyard Years** | Rei; retain Emily and Sophie | Existing area and four-person school cast | Preserve now; room expansion with existing-campaign conversion after interiors |
| **hong-kong-school — After the Last Bell** | Garrett | Existing area with Charles | Preserve existing snapshot; additional rooms/cast with existing-campaign conversion |
| **fg-early-partnership — The Blackhaven Annex** | Fox and Gordon, each as their own past self | No optional visit area | Existing-campaign integration alongside MH-016 after interiors |
| **mavis-before-spades — Rooms Without a Name** | Mavis | No optional visit area | With Mavis's MH-012 route |
| **martos-service-years — The People at His Table** | Martos | No optional visit area | With Martos's MH-012 route |
| **elias-family-stage — The House and the Stage** | Elias | No optional visit area | With Elias's MH-012 route |
| **camila-upbringing — The House That Raised Her** | Camila | No optional visit area | With Camila's MH-012 route |
| **sylvanis-early-earth — Before the Cards** | Sylvanis | No optional visit area | With MH-014, after the four Ace routes |

An area is a collection of related recollections, not a claim that every room existed beside every other room in the same year. An explicit **Period** selector changes time and, where necessary, site. Adjacent-room controls only join rooms within the selected period/site. Characters do not walk through a door into a later year.

## Shared visit design

**Entry:** keep **Visit flashback area** in the main in-person view. It opens the selected protagonist's area, a clear time/place card and the last safe room/period. Existing school access remains available on its current terms. New campaigns supply an initial non-spoiler period when their route becomes available; later periods unlock through the specific completed memory flags below. Opening/repeating a visit never marks the campaign memory complete.

**Room flow:** a compact in-person room strip shows reachable rooms and who is currently available there. Choose a room, then one companion or a compatible small group. Selected people may accompany a local walk only when that movement belongs to the scene; private meetings require the proper cast. No universal roster that summons every historical NPC into any room.

**Conversation:** each NPC offers three initial topics, a concrete opening and freeform Speak/Do action. Topics refresh with local conversation rather than offering future plot spoilers. A quiet shared activity can begin without an interrogation. Each NPC has concerns beyond supplying exposition or praising the protagonist.

**Return:** always provide **Return to the present**, including after an error or cancelled reply. Restore the same live location, party, resources, time fraction and pending story state. A saved visit resumes in the main in-person window, never a separate native window. The journal records who, which period and which room participated.

**Activity boundary:** share food, rehearse, repair a harmless personal item, discuss work, read or walk within the memory. Optional visits do not execute contracts, atrocities, the coup, assassinations, the Crow duel, adoption outcomes or promotion. They do not grant money, evidence, contacts, combat stats, relationship points or campaign completion. Authored scenes use their real handlers and, once implemented, [MH-016's illustrated shot presentation](CAMPAIGN_PRESENTATION_UPDATE_PLAN.md).

**Spoilers:** the player inhabits the younger self. A companion knows only that period's facts and legitimate disclosures. Earlier and later versions of the same person are separate historical profiles. Reopening an earlier period restores its earlier knowledge, not memories of the player's later conversations.

## 1. Rei — The Courtyard Years

**Era:** preserve the existing 2046–2047 school snapshot: Rei 17, Emily 16, Sophie 17 and Marcus 17. Marcus is alive and his film unfinished. This is an ordinary school interval, with no future death, suspension, adult careers or current romances.

**Visual design:** weathered school brick, a courtyard bench, charcoal sketches and miniature cardboard sets; afternoon light and greenery. Historical portraits retain the school identities and tattoo-free appearances. Colour belongs in scenery and artwork; navigation stays in the dark shared style.

**Room layout:** `R1 courtyard` connects to `R2 art classroom`, `R3 model garden` and `R4 sports-ground edge`. Movement stays within the same school break. These are proposed room variants of the existing area, not already separate runtime rooms.

| Room | People and interaction |
| --- | --- |
| R1 — Courtyard bench | All four friends can share lunch or plan what to make next. Default arrival preserves the current group selection. |
| R2 — Art classroom | Marcus and Rei work on drawings/film props; Emily or Sophie may join a chosen group activity. |
| R3 — Model garden | Emily shows the greenhouse; friends can help choose a small detail without deciding for her. |
| R4 — Sports-ground edge | Sophie invites a walk or light challenge; ordinary conversation does not award adult athletic/combat progress. |

| Talkable companion | Topics and voice anchor |
| --- | --- |
| Marcus | Stop-motion scene; cardboard pigeon; an ordinary school frustration. “The pigeon has fallen over again. I think it wants a smaller role.” Curious, playful, with his own ideas. |
| Emily | Greenhouse windows; plants she wants to try; where to sit at lunch. “I-I think these windows should open. Would you help me test one?” Gentle but able to disagree. |
| Sophie | Practice; a friendly challenge; an afternoon with the group. “One lap, or we can walk. You still have to tell me about the drawing.” Energetic without pressure. |
| Rei, when playing Emily/Sophie | Sketchbook; film collaboration; a quiet shared task. “That roof is leaning. We can call it a design choice.” Preserve the existing historical voice. |

**Activities:** work on the film, share lunch, build the greenhouse, walk toward the track. Preserve their existing meanings. Joseph Richter remains a separately authored school-era character, not an automatic member of the friendly default group. Do not turn optional visits into repeated bullying/loss scenes.

**Entry/knowledge:** existing `school` access and saves stay intact; no new mandatory gate. No revival, restored childhood memories or new present contacts are produced.

## 2. Garrett — After the Last Bell

**Era:** preserve Garrett at 16 and Charles at 21. Charles is his older brother visiting/picking him up, not a pupil given Garrett's uniform. Keep the existing family and school-crew boundaries from the independent sheets.

**Visual design:** a Hong Kong school gate opening into a lived-in side street, food steam, worn tiled counters and evening shop lights. Friendly everyday detail precedes the adult disappearance story.

**Room layout:** `G1 school gate ↔ G2 side street ↔ G3 noodle counter ↔ G4 back table`. The final two rooms belong to one proposed neighbourhood shop, not a retroactive relocation or founding of Garrett's adult Golden Dragon business.

| Talkable companion | Presence, topics and voice anchor |
| --- | --- |
| Charles — existing core companion | G1–G4; the school day, walking home, a family meal. “Bag on the other shoulder. You keep saying it doesn't hurt.” Practical older-brother care without knowing his later infiltration or disappearance. |
| Auntie Lau — proposed shopkeeper, an affectionate title, not established kinship | G3/G4; a busy afternoon, food preferences, repairing a wobbly table. “You can argue after you eat. The noodles won't wait for a verdict.” Has work to do and no secret future Syndicate knowledge. |
| Min Lok — proposed school peer | G1/G2; a school project, a competitive game, weekend plans. “You said you had a better idea. I brought paper.” Wants Garrett to follow through, without an invented future gang role. |

**Activities:** share an after-school snack, help set the table, compare school drawings, walk home with Charles. Any reference to school crews follows current era sheets; it does not create a new initiation, rival death or crime route.

**Entry/knowledge:** existing Charles-only visit remains valid without the proposed new cast. Added companions require independent historical references and first introductions. April's later `missing-charles` memory remains a distinct adult scripted period; do not put her adult knowledge or portrait into this school area. Garrett's parents' deaths and Sylvanis's history cannot be learned here.

## 3. Fox and Gordon — The Blackhaven Annex

**Era:** a calm interval after the names exchanged in their first-meeting memory, before the present Interpol campaign. [Existing first-meeting/partnership history](FOX_GORDON_CHAPTER_OUTLINE.md) and FM01–FM04 in [campaign prose](../campaign_prose/catalog.json) remain authoritative. Precise ages and ranks remain unspecified until chronology review.

**Visual design:** rain on a repair-shop window, a borrowed interview table, mismatched mugs and a small covered courtyard. This is an early working space in Blackhaven, not Geneva or a new global Interpol headquarters.

**Room layout:** `F1 repair counter ↔ F2 covered lane ↔ F3 annex table ↔ F4 kettle alcove`. Counter and interview access follow the worker's agreement; the area does not expose protected destinations. Fox and Gordon have separate journals and viewpoint profiles in the shared history.

| Talkable companion | Presence, topics and voice anchor |
| --- | --- |
| Gordon when playing Fox | F2–F4; a precise report, a promised follow-up, why he changed a plan. “Tell me which part I wrote incorrectly. I'll change that part.” Direct, accountable, not a caricature of bureaucracy. |
| Fox when playing Gordon | F2–F4; what he heard, an earlier disagreement, the usefulness of a good exit. “I came back when you asked. You can stop writing as though I didn't.” Dry, perceptive, capable of cooperation. |
| Repair-shop worker — existing unnamed historical role | F1/F3 by consent; a repair, reopened business, what assistance was actually useful. “If you're staying, hold that lamp where I can see.” Knows the local incident, not future Ace cases or the Crow. |
| Annex clerk — proposed role, name to be locked | F3/F4; legible statements, missed appointments, keeping a borrowed room usable. “One copy for the file. One you can actually read.” Local administrative knowledge, no all-access case dossier. |

**Activities:** compare two accounts of an already observed event, help with a harmless repair, share a quiet drink, review a fictional route sketch without starting a real case. Eight Senses cannot detect guilt; Gordon's abilities do not solve unknown facts.

**Periods:** `FG-A introductions complete` is the initial visit; `FG-B learning to work together` unlocks after FM03; `FG-C a report with both names` after FM04. FM02 is already past within FG-A, but opening the area never marks FM02 read or bypasses its campaign scene. No additional case outcome is created by casual dialogue.

## 4. Mavis — Rooms Without a Name

**Era structure:** `MV-A before the contract` at age twenty; `MV-B newly recruited` after the fixed recruitment; `MV-C early service` after the later memories, with age and roster tenure verified. The area moves between two historical sites through the Period selector, not a physical door.

**Visual design:** the Quiet House safehouse has rain-dark windows, an improvised sound-repair bench, plain temporary furniture and a kettle nobody quite owns. Early Syndicate quarters are more deliberate and spacious, with private doors and a small covered terrace. This contrast gives Mavis concrete boundaries to negotiate.

**Rooms:** in MV-A, `M1 stair landing ↔ M2 common table ↔ M3 repair bench`, with `M2 ↔ M4 handler's office` for a private appointment. In MV-B/C, `M5 receiving room ↔ M6 quiet terrace`; additional mission rooms are authored campaign destinations, not unlocked by freeform chat.

| Talkable companion | Period/room, subjects and voice anchor |
| --- | --- |
| The Broker — proposed former handler | MV-A/M4; current terms, what Mavis was told, what he expects reported. “Sit down if you're staying. Stand if you've decided.” He treats availability as an entitlement. No later archive scheme or knowledge of her future allegiance. |
| Noor Vale — proposed equipment caretaker | MV-A/M2–M3; a faulty headphone channel, a borrowed tool, how to share a cramped space. “You returned it working. That's already better than most people.” Practical and protective of her own time; no assumption of knowing the target contract. |
| Ivo Serrin — proposed runner | MV-A/M1–M2; a mundane errand, waiting for payment, finding somewhere to eat. “I said I'd bring food. I didn't say I could carry everyone's complaints.” A colleague with limited knowledge, not an omniscient conspirator. |
| The Crow | MV-B/M5 after recruitment; the explicit undertaking, a report, why a useful observation matters. “Give me what you established.” Masked; no unearned future missions or private biography. |
| Sylvanis | MV-C/M5 or M6 after MV-F05; an observed method, her reserve, why she prefers a quiet room. “You chose the only chair with a view of the door.” Unsettling interest; not a gentle confidant or her commander. |
| Martos | MV-C/M6 once the joint-service chronology is locked; a practical commitment, a shared meal, what help she actually wants. “I can stay until six. Tell me if that is useful.” |
| Elias | MV-C/M6 under the same chronology rule; an intrusive audience, keeping a cover simple, a performance he actually attended in this era. “Would you like company, or a quieter version of it?” Expressive without compulsory flirtation. |
| Camila | MV-C/M5–M6 under the same rule; an assumption in the plan, choosing what to disclose, a chess problem. “Which part do you want help with?” No automatic adoption/successor reveal. |

**Activities:** repair headphones, compare rain recordings, share a late meal, read a permitted historical briefing, sit without talking. None grants stealth skill, completes a target or creates a current relationship.

**Gates:** MV-A is initial; contract-specific topics require MV-F01's actual established content. MV-B unlocks after MV-F03. MV-C follows MV-F05 and MV-F06 and the approved roster timeline. The previous Spade is an authored adversary, not a casual companion whose death can be undone by visiting. Historical Crow appearances can use authored sites outside HQ.

## 5. Martos — The People at His Table

**Periods:** `MT-A selection and early unit life`; `MT-B later deployment, before desertion`; `MT-C refuge after desertion`; `MT-D early Syndicate service`. Exact adult ages follow [his treatment](MARTOS_CAMPAIGN_PLAN.md) after chronology lock. Do not mix pre-atrocity camaraderie with knowledge of his later refusal.

**Visual design:** a functional mess room, worn lockers, a shaded exercise yard and a small infirmary. Later refuge is cramped, with a clean kettle, rationed space and an unfinished watch repair. Early Syndicate quarters feel materially secure but carry different obligations. Depict military competence without real operational training instructions.

**Rooms:** MT-A/B use `T1 mess ↔ T2 lockers ↔ T3 yard`, with `T1 ↔ T4 infirmary` and an authored briefing appointment. MT-C uses `T5 refuge table`; MT-D uses `T6 service sitting room`. Period cuts separate sites.

| Talkable companion | Presence, subjects and voice anchor |
| --- | --- |
| Sera Dalm | MT-A/B at T1/T4, MT-C at T5 when able, MT-D only by established arrangement; ordinary unit life, fatigue, what he has actually promised. “You can put the kettle on before deciding you have to fix everything.” Later injury and disagreement use that period's specific sheet. |
| Adrien Voss | MT-A/B at an appointed T1/T2 briefing; readiness, standards, a report actually completed. “Tell me what you can guarantee.” Earlier professionalism and later evasions differ; no admission of his future consortium or upcoming disposal order. |
| Tomas Reed — proposed unit technician | MT-A/B at T2; a watch mechanism, a shared chore, making room for somebody else's method. “That spring is small. Your patience had better be larger.” Gives Martos a peer relationship unrelated to praise for strength. |
| The Crow | MT-D/T6 after recruitment; actual terms, a completed historical report, accepting the cost of a failed approach. “State the failure accurately. Then the correction.” No magical cure for Rage. |

**Activities:** cook a simple meal, repair a watch, share post-exercise conversation, help organise a communal space. Optional movement practice is descriptive and yields no stats, injuries or military qualifications. Voss cannot order a live atrocity through freeform chat; the fixed campaign events stay authored.

**Gates:** MT-A initial; MT-B after MT-F03, with a fixed interval before the disposal order; MT-C after MT-F05; MT-D after MT-F07. Sera's condition must match the interval. Lena is not summoned into an early military social circle: any historical conversation with her remains campaign-authored until a specific prior encounter is established. Replaying MT-A never makes Voss confess or turns Sera into a speaker from the ending.

## 6. Elias — The House and the Stage

**Periods:** `EL-A adult actor before the invasion` is the initial visit; `EL-B childhood prodigy` opens after EL-F01; `EL-C family after absorption` after EL-F06; `EL-D early service and theatre` after EL-F08. Childhood age and all adult years require explicit sheets. No earlier period anticipates his first inferiority.

**Visual design:** an elegant German family property with a music/rehearsal room, a gallery of performance memorabilia, private meeting rooms and a lived-in kitchen; a separate theatre wing/site uses work lights, half-finished scenery and dressing mirrors. Preserve the distinction between legitimate art and private criminal knowledge.

**Rooms:** family site `E1 entrance gallery ↔ E2 music room ↔ E3 kitchen`, with `E1 ↔ E4 private meeting room`; theatre site `E5 rehearsal stage ↔ E6 dressing corridor`. Use a labelled site cut, not an invented architectural connection, unless final geography places the rehearsal rooms on the estate.

| Talkable companion | Presence, subjects and voice anchor |
| --- | --- |
| Johanna Braun | EL-A/C at E1/E3/E4; what administration actually involves, a family occasion, an expectation he has overlooked. “You can dislike the meeting. Someone still has to finish it.” Her judgement is useful without secretly surpassing his established talents. |
| Konrad Braun | EL-A/B as age-appropriate family contact, EL-C at E4; succession expectations, family pride, his view of a proper obligation. “They would listen if you sat at the head of the table.” No present-day breakaway conspiracy leaks into the past. |
| Anja Keller — proposed early arts teacher | EL-B/E2; a piece he enjoys, a scene he understands unusually well, an artistic challenge suitable for his age. “You found the difficult part. Now tell me why it matters.” Her praise is earned, not purchased. |
| Lotte Weiss | EL-A/D at E5/E6, once the collaboration is historically established; rehearsal, an interpretation, being available to colleagues. “Again, if you want. This time listen to the silence after it.” Knows his acting life, not automatically his family's crimes or Ace identity. |
| The Crow | EL-C/E4 for a separately authored post-defeat settlement interval; later EL-D in a private service appointment. Discuss the actual affiliation terms or an established assignment. “The undertaking has been made. Keep it.” He appears at the family headquarters as authorised, masked and superior without replaying a fight. |

**Activities:** rehearse a scene, practise a rhythm, share a family meal, discuss a costume or old performance programme. Theatre mirrors cannot expose the Crow's concealed face. Childhood interactions remain age-appropriate; talent does not become instant adult combat expertise in a child portrait.

**Fixed history:** Elias personally defeated every incoming Syndicate force, then the Crow defeated him **at his family's crime headquarters**. These events are authored scenes, not random challenges in the visit area. EL-C includes fear/awe from what has happened; EL-A/B know none of it. A freeform compliment cannot end his later obsession or earn a rematch.

## 7. Camila — The House That Raised Her

**Periods:** `CA-A childhood after adoption` is the initial area; `CA-B orphanage before departure` after CA-F01; `CA-C adolescent lessons` after CA-F04; `CA-D adult protégée` after CA-F08. All exact childhood/adolescent ages must be locked before portraits/prompts; adult sheets cannot substitute. The successor intention is genuine, but her knowledge of its explicit wording depends on era.

**Visual design:** a modest orphanage common room and garden; then a private household with a reading room, dining table, study and music/dance space. A place can be comfortable and still be where her future is deliberately shaped. No room design should reveal the Crow's civil identity, home address or unspecified family history.

**Rooms:** orphanage `C1 common room ↔ C2 courtyard`; household `C3 reading room ↔ C4 dining room ↔ C5 study`, with `C3 ↔ C6 music room` and `C4 ↔ C7 covered garden`. The period change is a memory cut, not an orphanage-to-house travel command.

| Talkable companion | Presence, subjects and voice anchor |
| --- | --- |
| Elena Sanz — proposed orphanage caregiver | CA-B/C1–C2; a shared book, the day ahead, a small disagreement between children. “Tell me what happened before you decide whose fault it is.” Caring without an invented abusive institution or Syndicate affiliation. |
| Pilar — proposed childhood peer | CA-B/C1–C2; a game, a favourite story, sharing materials. “You can choose first if I get to change the next rule.” A child with preferences, not a future operative in disguise. |
| The Crow | CA-A/C3–C5 and C7; CA-C lessons; CA-D private conversation. Early topics include a book, a question and a promise to return; later topics include an observed assumption, delegated responsibility and succession only after her explicit knowledge is established. Opening: “Show me where you became uncertain.” Direct parenting can include quiet attention and no assessment. |
| Mara Esteve | CA-A/C3/C6 and CA-C, later CA-D by authored visit; a lesson, ordinary frustration, something Camila wants for herself. “We can stop for a moment. The page will still be here.” Knows her own part in the household, not the Crow's hidden identity. |
| Inez Salcedo | CA-D only, in a specifically authorised C5 appointment or later workplace room; practical costs, a commitment, a professional disagreement. “I can make that promise when I know what it costs the people keeping it.” No implied childhood connection. |

**Activities:** read together, play an age-appropriate chess problem, write with a chosen pen, share a meal, listen to music or practise an ordinary dance step. No investment simulator, live money movement, power awakening or promotion. Private parental address requires the agreed historical guide, not automatic adult “master” in every childhood sentence.

**Knowledge:** maintain adopted daughter, protégée, financial Ace and intended successor as separate facts. A teenager's analysis cannot know an adult campaign outcome; CA-A cannot discuss the exact heir conversation before it occurs. Public visitors do not learn the adoption or succession through a shared group greeting. Ordinary childhood actors cannot be invited to the adult strategic group. Adoption is fixed and cannot be revoked by losing a chess game.

**Crow art:** retain established concealment. Later masked appearances use the era-appropriate mask; any approved pre-mask/unmasked historical presentation follows the blank-face-and-glasses convention defined in MH-014. Do not manufacture a recognisable father portrait, reflection or accessible description.

## 8. Sylvanis — Before the Cards

**Source:** [The Crow's Patience](SYLVANIS_CAMPAIGN_UPDATE_PLAN.md). Sylvanis remains chaotic evil, acts for amusement and has no remorse/redemption arc. He already mastered human martial arts and acquired his fearsome reputation before recruitment. Blisk chronology must not use invented human-equivalent aging.

**Periods:** `SY-A the Organisation before the coup` initial; `SY-B early Syndicate` after SY-M05/06; `SY-C the early Glasshouse and arena` after SY-M07; `SY-D Charles's arrival` after SY-M09; `SY-E first Shinokami business` after SY-M10. Each is a distinct fixed interval; later knowledge does not infect earlier groups.

**Visual design:** SY-A is a practical mercenary compound with a functioning aid room, communal table and people genuinely helping others. SY-B alters the same place into a more controlled command site, reflecting the Organisation's loss of purpose. SY-C/D use the historical laboratory/arena observation spaces; SY-E uses an authorised private reception at Takeo's headquarters, not a relocation of him into the Glasshouse.

**Rooms:** early compound `S1 mess ↔ S2 courtyard ↔ S3 aid-room threshold`, with `S1 ↔ S4 planning room`; laboratory `S5 workroom ↔ S6 observation gallery ↔ S7 staff landing`; business period `S8 private reception`. Site changes use the Period selector. Access to an observation gallery does not authorise improvised experiments or arena fights.

| Talkable companion | Presence, subjects and voice anchor |
| --- | --- |
| Kaden Mourne | SY-A/S1–S3; people being protected, care for wounded members, an ordinary meal. “Eat if you're staying. I need that chair for someone who has been standing all day.” Older, muscular, mercenary gear; sincere kindness and competence. Sylvanis's response remains selfish. |
| Bespectacled strategist — the future Crow, concealed display identity | SY-A/S4 and bounded shared S1 scene; current organisation, allocation of effort, a concrete observation. “They have enough to continue. They could have more.” Blank featureless face with glasses; no civil name. Private coup planning belongs only after the authored proposal, not in casual pre-coup chatter. |
| Organisation quartermaster — proposed role | SY-A/S1–S2; a delayed delivery, equipment returned damaged, making room for protected civilians. “People are using that doorway. Find another place to stand.” Ordinary competence does not give them insight into the coup or require fearlessness in every exchange. |
| The Crow | SY-B/S4 or a correctly authored early command room; expansion, an actual inconvenience, limits of their cooperation. “Tell me which agreement you have made inconvenient.” Mask/blank-face treatment follows era. His tolerance is not affection. |
| Charles | SY-D/S5–S7; limited laboratory work, a recorded observation, the next authorised task. “The result is in the report. Which part do you want repeated?” Adult historical Charles pursues his own concealed aims. No automatic confession or knowledge that Sylvanis knows about infiltration. |
| Takeo Mishima | SY-E/S8 only; an established fictional deal's purpose, reliability, what was actually agreed. “State what will be delivered.” No live drug manufacture, real recipe, unrestricted travel or automatic disclosure of the separate betrayal plan. |

**Activities:** sit through a meal, inspect an ordinary damaged object, discuss a remembered briefing, watch an already recorded fictional bout, review a permitted historical report. These can be tense and revealing without changing history. Freeform visits do not perform live human experiments or murder Kaden again; fixed harmful events remain in the campaign's authored scenes and outcomes.

**Critical boundaries:** Kaden is alive only in SY-A; revisiting it does not resurrect him. The strategist's relationship to Kaden is heavily implied as father/son, never explicitly confirmed. No names, captions, metadata, portraits or replies turn the implication into fact. The conspiring future Crow is a separate character from Kaden. Early characters cannot discuss Cards or call him Crow before those roles exist. Garrett's parents are not added as casual companions; their authored deaths and Sylvanis's motives remain intact and private to the correct viewpoint.

## Historical cast and conversation authoring contract

**Mandatory user requirement — 2026-11-11:** Every flashback character requires both a **character reference sheet** and a **dialogue style guide for each era in which they appear**. This applies across all campaigns, including future additions, to the historical playable protagonist, optional companions, returning characters, new supporting NPCs and scripted-only appearances. A silent appearance still needs the pair; its dialogue guide can explicitly prohibit speech in that scene. A different portrait, age label or costume does not constitute an independently authored historical version.

Identify each pair by stable character ID and era ID, with its own content revision. The two records may live in the existing shared historical JSON files; separate physical files are not required. Maintain an inventory of every scene/area/period's cast, its reference-sheet key, dialogue-guide key and review status. Split an era further when an intervening event changes a character's knowledge, outlook or relationships. A profile can be reused across scenes only when their historical state is genuinely the same.

| Required record | Required era-specific content |
| --- | --- |
| Character reference sheet | Historical name/role, age, appearance and clothing; personality and temperament **at that time**; skills, goals, worries, beliefs and loyalties; relationships and attitudes toward each relevant person; experienced events, facts known, secrets and who may hear them; facts/events not yet known; permitted scene/group presence. |
| Dialogue style guide | Vocabulary, register, sentence rhythm, humour, emotional expression, confidence and habits at that time; forms of address and differences by listener; permitted topics, prohibited future references and a natural response to unknown information; multiple example lines and follow-ups demonstrating the historical voice. |

For minors, exact age and suitable portrait/voice must be locked before use; an unestablished adult age may be explicitly unknown. Preserve established enduring traits while authoring development only where the story supports it. Sylvanis's earlier version, for example, remains chaotic evil; an earlier era does not automatically make a character kinder or less capable.

**No present-day or cross-era fallback:** Historical scenes must resolve their exact reference/style pair. Never merge in present-day biographies, `dialogue_styles.json`, current personalities, relationships or knowledge, and never substitute a later historical version. Both authored dialogue and generated replies must follow the selected era. A missing or unreviewed pair blocks that new scene/period's dialogue with an inline explanation and a return option until authored; it must not silently use adult defaults. Review existing historical pairs against the same contract when integrating them, preserving released access and save compatibility.

Concrete authoring distinctions include Mavis before versus after recruitment; Martos during service, after desertion and after recruitment; Elias before versus after his first defeat by the Crow; and Camila before adoption, during upbringing and during successor preparation. The Crow also requires separate versions for the early conspirator and each later historical context. These versions must reflect what has actually happened and been disclosed by that point, including their then-current attitudes and speech, rather than importing the endpoint of their campaigns.

The openings above are draft voice examples, not mandatory repeated catchphrases or new historical events. Each final sheet needs more than one greeting and concrete topic follow-ups. Example: Mavis asking Noor about the left audio channel can lead to a shared repair or a boundary about borrowed tools; it cannot disclose the Broker's future archive scheme. The same person can remember different established experiences in a later period without learning them from another snapshot's chat history.

Room/group rules are part of the authored data. Private handler meetings, adoption discussions, case testimony, succession conversations and conspirator meetings cannot gain extra listeners through a checkbox. Companions may refuse a topic or proposed activity. The player's freeform assertion is conversation, never a canon amendment. A future question gets natural uncertainty or a present concern, not a prophecy disguised as a joke.

## Runtime work required later

1. **Area and period routing:** replace the single-area assumptions in `area_for`, `active`, `available` and the UI with area/period/room-aware definitions. Preserve `school` and `hong-kong-school` IDs and their current access. `display_people` currently hard-codes two eras; use the selected historical profile for labels so a later identity cannot overwrite an earlier one.
2. **References:** extend the independent JSON schema/version deliberately, matching every character/era pair across reference and voice files and every scripted/optional cast inventory. Validate completeness, explicit era selection and review status before enabling new content. The current prompt's school-only setting/minor rules must become period-aware while retaining school protections. Missing references or dialogue guides fail closed with an inline explanation; never use adult biographies or current dialogue styles to fill a gap. Script writers and historical artwork briefs use the same era references as conversations.
3. **Visit state:** record protagonist, area, period, room, compatible participants, unique visit ID and revision. Increment the revision on room/period/group changes. Late, duplicate, cancelled or cross-save responses cannot commit to another scene.
4. **Journal/migration:** partition local history by protagonist and period as well as area; Fox and Gordon must not share each other's private visit choices. Migrate existing saved visits without losing dialogue, member selection, reference revision or exact present state. Preserve old records as history when references change; exclude obsolete guidance from new prompts.
5. **Isolation:** generated output is only narration and selected-speaker lines. Whitelist historical context and compatible local history; exclude live calendars, relationship scores, secret dossiers and later campaign flags. UI labels can read unlocks, but the dialogue model does not receive the whole present save.
6. **Entry/exit:** maintain time pause without elapsed-time catch-up and the existing active-journey/encounter/scene checks. Return/escape/cancellation always remains available. Memory-room movement cannot call live travel or grant live room permission. A live Maps destination required by a campaign still uses MH-016's proper travel flow.
7. **Artwork:** use room scenery consistent with implemented interiors and independently verified historical portraits. Follow [portrait direction](../assets/portraits/ARTSTYLE.md), era-specific tattoos/clothes/ages and Crow concealment. Reusable room artwork supports freeform visits; an authored campaign sequence needs its own MH-016 shot coverage. No artwork production or paused-job resumption is authorised by this planning update.

## Milestones and verification

- [x] Inventory current optional areas, historical sheets, main-window UI, isolation tests and all existing/planned campaign protagonists.
- [x] Design eight areas, room networks, periods, conversational casts, sample topics, activities and knowledge boundaries.
- [x] Record the mandatory separate character reference sheet and dialogue style for every character/era, including scripted appearances and historical protagonists.
- [ ] Lock new NPC names, exact chronology/ages, introductions, coexisting rosters and period-specific knowledge with the campaign manuscripts.
- [ ] Complete and review the full character/era inventory and both records for every listed version; audit existing historical pairs before integration. Draft topic/opening tables do not satisfy this milestone.
- [ ] Implement the shared room/period system after interiors, preserving released visits and the approved campaign order.
- [ ] Deliver Fox/Gordon with existing-campaign integration and each new protagonist's area with its own route.
- [ ] Complete approved historical artwork and missing/unreviewed-profile error states, with no present-day fallback.
- [ ] Verify new/legacy saves, retries, period/room/group switches, both Fox/Gordon viewpoints and absent/locked companions.
- [ ] Inspect rendered rooms and interactive states in the main window; verify no extra window and no live-world mutation.
- [ ] Record actual release behaviour/access/save impact, run relevant checks and validate/export patch notes.

Planned tests include the existing flashback-visits and flashback-lore unit suites, mandatory-memory/prose regressions, new access/period/cast matrices, canary tests for future knowledge, every room transition, asynchronous stale results, historical artwork routing, Crow concealment, fixed-event isolation and exact live-state restoration. UI checks cover compact layouts, journal, errors, loading/cancel, locked entries, keyboard exit and saved resume. Any touched phone handoff/Maps surface needs `tests/phone_dark_theme_smoke.py` and its feature smoke. No live provider quality pass or gameplay test is claimed from design alone.

**Historical-version acceptance gate:** Check every cast occurrence against the inventory for both records, including minor and scripted-only characters. Inspect assembled context for any present-day profile/style fields. Test later secrets, titles and relationships as future-knowledge canaries, return from a later era to an earlier one, and reject conversation history or pending replies from another era/revision. Review sample dialogue and authored scenes for the era's personality, confidence, worldview and voice as well as factual knowledge; a reply can avoid spoilers and still wrongly sound like the present-day character. These are required implementation/editorial checks, not completed tests from this planning update.

## Actual evidence — 2026-11-11

Inspected current area/visit/lore/UI code, independent sheets, existing isolation tests, Ace treatments, Fox/Gordon memories, Sylvanis's expanded history, MH-015 embedding, MH-016 presentation/pause and the approved update order. All eight designs and cast/period contracts above are authored proposals beyond the stated existing facts. No runtime, artwork, live provider calls or saves changed. Implementation and rendered review remain pending.

Verification performed:

- Document checks passed for eight ordered area designs/unique IDs, all 13 local links, eight inbound plan links and their section anchors, Markdown table structure and the single MH-017 row/detailed entry. Minor table-column errors found during checking were corrected.
- Coverage review accounts for nine campaign protagonists and retained Emily/Sophie access, period-specific conversation casts and fixed-event isolation. These checks establish design coverage, not playable functionality or editorial approval of new NPC histories.
- Approved release order and MH-016's Deferred status/pause remain intact. No released MH-015 scope/status was rewritten.
- Added `plan-2026-11-11-campaign-flashback-areas` as a **Development report** among the existing reports in `patch_notes/catalog.json`, preserving all 492 prior records and their order. It explicitly describes planned access and no new playable content.
- `python -X utf8 patch_notes.py validate` passed with 493 entries. `python -X utf8 patch_notes.py export` refreshed the generated history.
- Final `python -X utf8 -m unittest discover -s tests -p test_patch_notes.py -v`: five passed; the existing archive-source failure remains for missing `tests/screenshots/mixtape-art-review-0.jpg`. An initial extra preference-test failure from placing a hidden Development report ahead of curated releases was resolved by putting it with the existing report group; no runtime or tests were changed.
- No gameplay unit suites, UI smokes, rendered-screen inspection or live dialogue-quality tests were run for this documentation-only task. They remain implementation acceptance work.

### Historical character versions follow-up — 2026-11-11

- Recorded the user's mandatory reference-sheet/dialogue-style pair for every character and era, across optional and scripted flashbacks. Added the cast inventory, personality/voice review, exact-era selection and no-present-day/later-era-fallback requirements. Linked the contract from the roadmap, Ace master plan, Sylvanis plan and shared campaign presentation plan. Actual character-sheet/style authoring is still pending.
- Documentation checks passed across those five files: contract links, all 13 local links/anchors in this area plan, Markdown table structure, one MH-017 row/entry, UTF-8 integrity and retained MH-016 Deferred status. These checks verify the written requirement, not runtime isolation or the quality of unwritten character versions.
- Added `plan-2026-11-11-era-specific-flashback-references` as a Development report, preserving all 494 prior catalogue records and their order. `python -X utf8 patch_notes.py validate` passed with 495 entries; `python -X utf8 patch_notes.py export` refreshed the generated history.
- `python -X utf8 -m unittest discover -s tests -p test_patch_notes.py -v`: five passed; the existing archive-source failure remains for missing `tests/screenshots/mixtape-art-review-0.jpg`. No runtime, profile JSON, artwork, save, gameplay/UI or live-provider changes/tests were performed in this planning follow-up.
