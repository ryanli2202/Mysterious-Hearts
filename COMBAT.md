# Enhanced combat

Restart the game to load this update. At any location, choose **Combat · Iron Circle / training / challenges** in the in-person window. During a hangout, use **Spar / fight / train**. Combat uses the same main in-person stage, with its own controls, history and saved encounter. The phone remains separate.

## Learned actions and combos

Combat now uses selection menus: choose Martial, Unique skills, Awakened signatures or Utility, choose a learned action, optionally choose one compatible Trait amplification, and choose the opponent or an arena object. **Resolve selected action** commits the exchange immediately. The gamemaster then writes a short narrative of the resolved outcome, with a compact damage/resource line underneath. There is no freeform player attack box. A failed narration request preserves the concise local narrative and all resolved results; it cannot reroll or charge a second turn.

Open **Training · moves, combos & Trait workshop** for the martial academy. The checked-in catalogue contains 432 techniques across all 21 arts: basics are granted by the first lesson, advanced techniques require martial skill 60 to learn, and masters require martial skill 80 and Awakening. Select a present, willing teacher to learn a new art; practise a known art alone or explicitly train a qualifying technique. An advanced combo is one learned action, with separate hit rolls across its finite strikes. Selecting basic attacks cannot bypass its learning requirement. Master names such as Hurricane punches, Ghost step, Unseen spectre and Power-breaker have superhuman combat roles.

Old profiles migrate once: known arts grant basics, with higher techniques only where both existing proficiency and martial/awakening requirements qualify. A newly learned art at proficiency 3 receives its basics even if the character is already a martial master. Raising stats afterward does not silently grant the rest of its catalogue.

## Trait amplification, unique skills and superhuman combat

The authored roster contains **58 amplification options and 124 Trait unique skills for 19 Trait users**, plus **15 separately labelled signatures for five awakened fighters without Traits**. Nine unawakened characters receive no invented supernatural abilities. These catalogues cover all 33 reviewed characters. Garrett's Dragon Kick, Rei's Descending Tempest, Flowing Stream and Thousand Sparks, Ivan's five elements and Sylvanis's separate Umbrakinesis, True Sight and Polymath expressions are included.

One amplification reinforces a regular action with its selected aspect. A unique skill includes its own authored aspects and pays their combined cost; another amplification cannot be stacked on it. Learned Trait skills and amplifications have no martial, power, refinement or IQ unlock threshold. Awakening, an established Trait, and sufficient current resources are required. Stats determine force, accuracy, control and efficiency. Forms remain separately activated, paid and timed; active earned forms enhance actions without locking their base versions. Ivan's red lightning favours impact/stagger and blue lightning speed/precision.

Awakened ordinary strikes also use superhuman strength and movement. Power and selected effects can cross an engagement faster than normal perception, breach concrete, shatter ground and wreck vehicles. Opposing awakened fighters contest those actions through their own speed, power, defence and techniques. Counter stances answer actual incoming attacks; they wait if no attack arrives. Flowing Stream can contest every attack category, including ranged Traits, with full, partial or failed redirection. Momentum, stored impact, heat, blood expenditure, weak-point marks, concealment, barriers, restraint and stagger have distinct mechanics. Blood skills spend health without becoming automatic control of an intact body; pain suppression does not stop damage or knockout.

Every active encounter owns objects with material, integrity and position. Cover reduces damage until broken; shattered cover opens routes, rubble affects footing, fire/ice affect occupied ground, collisions cause damage, and powered knockback can move wreckage. Created barriers are breakable. Vehicle props are only seeded at applicable outdoor locations. Arena changes persist with the encounter through save/load. This update does not add permanent city reconstruction or property-repair simulation.

## Custom Trait creation and workshop

In character creation, enter the awakened Trait, choose **Evaluate Trait amplification · gamemaster**, review the proposed options and accept them before moving to Winterfield. Changing the Trait invalidates its review. Failure retains the character draft and portrait. Approved names, aspects, compatible action roles, costs, bounded effects and environment descriptions become part of the custom profile and library entry. Existing custom characters can evaluate and accept their missing options in the in-person workshop.

Open **In person → Combat → Training → Trait workshop → Generate unique skills**. The existing configured gamemaster proposes exactly three cards from current stats, Trait, approved aspects, learned skills and earned form. Review description, effects, range, costs, environment and counter/setup behaviour, then absorb one. First absorption is immediately available. Successful absorption starts a rolling **1,440 in-game-minute** learning cooldown; generation, reviewing, retries and using learned skills remain available. Candidates, stable skill IDs, immutable learned blueprints and the absolute next-absorption minute are saved. Repeated clicks, stale responses, duplicate absorption, reloading or removing a learned entry cannot reset that timer. Later stat growth scales the original skill rather than renaming or rewriting it. Generated effects are constrained to approved aspect tags and shared physical effects; combined costs must fit the current full resource pool.

## Opponent initiative and abilities

The fight screen shows **Opponent intent** before you select your action. Opponents use the same learned catalogue, unique skills, amplification, costs and terrain rules as the player. They alternate offensive Trait skills with martial pressure, weight learned-art proficiency, consider counters and reserves, attack cover and recover below 15 stamina. Low mana favours physical actions. Interpol field partners and their counterattacks use the same resolver. Trait attempts earn the same paid usage credit as player attempts.

Opponents attack when you guard, recover or attempt an infeasible move as well as when you attack. Fight IQ influences initiative, either side can act first, and a knockout prevents the defeated fighter from completing their action. Guard applies to the exchange even when the opponent acts first. Combat remains turn-based: typing or waiting does not spend time or trigger unanswerable attacks; each submitted response resolves a 30-second exchange.

Sylvanis prepares his earned second-stage Transcendence immediately in a serious encounter when he can afford activation, upkeep and an attack. His Umbrakinesis can then attempt piercing shadow attacks with his predictive perception and learned martial positioning. Enhanced shadow techniques require the paid active form; Alyssa does not inherit them. Other eligible fighters consider an advanced form below 60% health, after four exchanges, or in response to an active player form. Forms remain once per encounter, with existing mana costs, duration and Conduit State's daily cooldown. An exhausted fighter recovers before preparing a new form.

The opponent plan is independent of the player's current selection. Preview and save/load reproduce the same plan without paying costs. Both actions, form upkeep, initiative, counter clashes, partial combos, damage and terrain resolve before narration. Old exchange IDs cannot commit twice. The legacy freeform adjudication API remains for compatibility with earlier integrations; the gameplay screen uses the selection resolver.

## Iron Circle

Travel to the Iron Circle, enter your signature and sign its physical ledger. Every new entrant starts at **450**, regardless of protagonist. Cards occur twice per seven-day game week, on day offsets 1 and 4 at 18:00; attendance closes at 21:00. The hub shows the next date and can wait until it. Missed cards roll forward without awarding a result.

The configured game AI generates an original name, martial discipline and, at high ranks, a bounded Trait. Numeric opponent ratings are generated and constrained by tier: ranks 450–301 are unawakened, 300–101 are Awakened without Traits, and 100–1 have Traits. A win advances ten places; a loss drops five, bounded to 1–450. These thresholds, schedule and promotion steps are authored game balance, not historical canon.

Matches last three five-minute rounds, with each submitted exchange consuming 30 simulated seconds. Round breaks restore 15 stamina. Knockout ends a match early; otherwise judges use damage dealt, remaining health proportion, and finally defender advantage for an exact tie. No drawn result is recorded. Once signed, Rei's legacy career finale cannot decide circuit fights; its displayed rank follows the ledger. Old career history is retained.

## Stats, arts and Traits

Named combatants start with **peak source-story ability**, independently of current AU relationships or historical events. Saved Path progression can subsequently improve eligible stats. The user-specified starting ratings are exact:

| Character | Awakened power | Trait refinement | Martial skill | Fight IQ |
|---|---:|---:|---:|---:|
| Sylvanis | 90 | 100 | 100 | 100 |
| Takeo Mishima | 100 | 80 | 95 | 90 |
| The Crow | 80 | 100 | 100 | 100 |

Other numeric ratings are explicit game-balance interpretations of the supplied lore, not numbers quoted from it. Neo uses his peak combat optimisation and Daniel his developed potential. Emily has her peak Critical Hit ability in combat. Source deaths, relationships, political defections and victories are not imported.

Awakened power (mana potency) determines health, damage, natural mitigation, movement, terrain force and energy capacity. Trait refinement improves control, efficiency and accuracy; it never locks an already learned Trait action. Martial skill and the selected art's proficiency govern technical success. Fight IQ affects initiative, counters and bypassing defence. All four ratings are bounded to 100. Unawakened custom characters begin at 0/0/8/10; Awakened custom characters at 18/12/12/14 with their authored Trait. Awakening unlocks through strenuous combat; Transcendence requires a qualified breakthrough.

`combat_profiles.py` contains the complete requested teacher mapping and discipline descriptions. Sylvanis teaches every supported art. Takeo and the Crow have combat profiles but do not teach. Teachers must be physically present and willing; the victim of an unwarranted attack will not teach the attacker. A lesson adds a new art at proficiency 3; subsequent lessons or solo practice add 3 proficiency and 1 martial skill, capped at 100. Trait work and analysis add 1 to their respective stat. Direct power conditioning is removed: it cannot bypass Path growth restrictions. Each session takes 30 minutes, with at most three focused sessions per day. April teaches combat analysis.

Traits have descriptions, energy costs and distinct effects: movement accumulation, analysis/evasion bonuses, armour, rage pressure, damage storage, blood-health costs and critical weak-point damage. The AI receives these limits and martial principles. Sylvanis, Charles and Garrett start with established, temporary, mana-intensive Transcendence trump cards. Ivan's Conduit State remains a separate Trait technique: exactly five combat minutes, once per 24 game hours, with no added activation cost or crash. He retains the option if he later breaks through. Only one advanced form can be activated per encounter, so forms cannot be stacked. Peak starting ratings already include developed natural ability.

## Part 2: Awakening and the Path

Open **Combat → The Path · progression & breakthroughs** in the in-person window. Select a nearby fighter and choose **View Path** to inspect their stage or invite a qualified, willing NPC to attempt a breakthrough. The screen displays the exact requirements, remaining time, encounter count, stat meanings, trump-card description/costs and stage history. The Path is public lore; it does not automatically disclose another character's powers through ordinary conversation.

| Stage | Progression rule | Ongoing mana-potency growth |
|---|---|---|
| Dormancy | 30 strenuous encounters unlock Awakening if latent mana exists | None |
| Awakening | 15 encounters in this stage; refinement 40 if a Trait exists | None |
| Ascension | 40 encounters in this stage; refinement 80 if a Trait exists | +1 per strenuous encounter, up to 100 |
| Totality | Breakthrough requires an established Trait, refinement 93+ and 30 full game days in Totality | None |
| Transcendence 1 | Second breakthrough requires refinement 100 and 30 full game days in this stage | +1 per strenuous encounter, up to 100 |
| Transcendence 2 | Final stage | +1 per strenuous encounter, up to 100 |

Earlier encounter thresholds, refinement gates and boost amounts are authored, tunable game balance. The two breakthrough refinement/time gates are the user's exact requirements. A strenuous completed encounter needs at least 10 total damage and four exchanges, or at least one exchange ending in knockout. Substantial spars, wins and losses count for both fighters. Empty guard sessions and immediate concessions do not. Rewards are applied once at fight completion. Successfully paid, executable Trait attempts count even if evaded; insufficient-resource, impossible or unrefined moves do not. Every four such uses across qualifying encounters give +1 refinement, with the remainder saved. Higher potency provides more energy for Trait use and therefore more practical opportunities to develop refinement.

Stage-entry bonuses are power/refinement/martial skill/fight IQ: Awakening +18/+5/+5/+5; Ascension +8/+5/+4/+4; Totality +10/+5/+4/+4; Transcendence 1 +8/+0/+3/+3; Transcendence 2 +5/+0/+3/+3. All cap at 100; refinement bonuses require a Trait. The boost happens once when entering the stage, not on loading or on already-established cast stages. Totality's entry boost is the last potency increase until a breakthrough. Starting dormant playable characters have latent potential by default. The model also supports an explicit no-mana profile, which cannot awaken. Awakening itself does not invent a rare unique Trait: traitless Awakened can progress through encounters to Totality, but cannot satisfy the Trait-mastery requirement for Transcendence.

Starting stages:

- Transcendence 2: Sylvanis.
- Transcendence 1: Garrett and Charles.
- Totality: Rei, Takeo, the Crow, all Four Aces, Ivan, Neo, Daniel, Tyler and Thirteen.
- Ascension: Minsu, Samantha, Valentina, Emily, Alyssa and Keisuke Hachimura.
- Awakening: April and newly created Awakened protagonists.
- Dormancy: the unawakened cast, ordinary unawakened NPCs and newly created unawakened protagonists.

The explicitly requested stages take precedence; remaining cast assignments are authored interpretations of their established peak profiles. Generated circuit opponents also receive stages. No offscreen fights or elapsed training are fabricated.

An eligible breakthrough asks the existing AI gamemaster to create a name, techniques, limits and expression (offence, defence, precision, mobility or control) derived from the character's own Trait. A valid response commits the next stage and its trump card; there is no additional hidden random success roll. Invalid or failed responses grant nothing and can be retried. Presence, trust for NPCs, stage, elapsed time and refinement are rechecked before commit. A stale result cannot be applied twice or to a changed Trait. Breakthroughs are available between encounters, not while travelling, knocked out or already fighting.

Transcendence 1 activation costs 35 mana, plus 8 per 30-second exchange, for up to 180 seconds. Transcendence 2 costs 55 plus 12 per exchange, for up to 300 seconds. Insufficient upkeep ends the form. Stage 1 grants 1.5× damage, +0.10 hit probability and 0.85× incoming damage; stage 2 grants 1.85×, +0.15 and 0.70× respectively, with final hit probability still bounded. Offence adds another 1.1× damage, defence another 0.85× incoming damage, and precision/mobility/control add 0.05 hit probability. AI prose cannot override these resource or numerical limits. NPC activation decisions follow the opponent initiative rules above.

New saves date their seeded stages from the start of play. Existing saves retain every earned stat and acquire a stage clock when this update first encounters their combat data; no unverified pre-update days or encounters are credited. This means an existing Totality or stage-one character must still spend 30 game days under the new system. Existing active legacy encounters preserve health, resources and turn history, but reset their old indefinite form activation once to enforce paid, timed forms. Stage timestamps, usage remainders, histories and generated cards survive save/load.

## Encounters and consequences

Select someone physically present, then invite a friendly spar, propose an agreed fight, or review and confirm an unwarranted attack. Personality, combat experience and trust influence acceptance. An attack does not require consent. Spars end as practice without a winner; challenges and attacks have a victor. They have no round deadline. Either participant can be knocked out, and the player may concede or stop practice.

Health, stamina and awakened energy belong to the saved fight. Characters never die. Knockout creates **1,440 minutes of inactivity**, including for a player-controlled protagonist. Travel, combat, training, work and conversations are guarded, NPC routines hold their location, and the player can rest through recovery from the combat hub.

Unwarranted attacks permanently rupture the target relationship, prevent ordinary repair and damage known friends' and partners' trust. Attacking an organisational superior causes excommunication and member relationship losses. Opposing organisations lose 30 diplomatic relationship points. Established command access, faction sponsorship and leadership are revoked where applicable. These consequences occur when the attack begins, regardless of who wins.

NPC combat proposals are invitations, never attacks or automatic player consent. Current implementation recognises training/fighting discussion and heated phrases in committed in-person conversation, then displays a reviewable proposal on the hangout combat button. It uses authored personality/trust rules rather than asking a second model to classify every conversation.

## AI, saving and limits

The existing configured game provider narrates resolved exchanges and generates reviewed custom Trait options/skills. Rules own initiative, accuracy, damage, costs and terrain. A failed or malformed narration leaves the saved result-based fallback; model prose cannot change the outcome. Narration is limited to 2–3 sentences and 65 words, with detailed mechanics outside the paragraph. No new account or credentials are required.

Requests run off the UI thread. Failed skill generation spends no learning cooldown and preserves prior candidates; failed narration leaves the already committed exchange intact. Active fights, arena objects, resources, form cooldowns, learned moves, workshop candidates/timers, training, ledger, injuries and consequences survive saves. Old saves gain the new fields additively without resetting progression. During a fight the background clock and ordinary routines pause; every two exchanges advance the world's clock one minute.

Limitations: numeric balance has not undergone extended playtesting; procedural opponents are fictional game content rather than new source canon. NPC invitations and consent use explicit rules rather than unrestricted semantic interpretation. Live model outputs were not sampled in this implementation check. The all-repository test run stalled during Tk tests and was interrupted; targeted checks and UI captures were used instead. The world suite still reports two unrelated expectations concerning unique scene artwork (97/106) and the older home count (18 versus 27).

## Evidence

Implementation: `combat.py`, `combat_profiles.py`, `combat_path.py`, `combat_ui.py`; tests: `tests/test_combat.py`, `tests/test_combat_path.py`, `tests/combat_ui_smoke.py`, `tests/combat_path_ui_smoke.py`. Screenshots are saved under `tests/screenshots/combat-*.png` and `tests/screenshots/path-*.png`. Part 2 follows the user's supplied Path definition; no real-world sources are needed for this fictional system.

Opponent initiative update: `combat_tactics.py`, `tests/test_combat_tactics.py`, `tests/combat_opponent_ui_smoke.py`; rendered evidence under `tests/screenshots/combat-opponent-*.png`. Automated checks use mocked gamemaster responses, not a live provider. Current verification is recorded in the dated patch catalogue entry.

Enhanced combat: `combat_catalogue/martial.json`, `combat_catalogue/traits.json`, `combat_moves.py`, `combat_engine.py`, `combat_workshop.py`, `combat_selection_ui.py`, and the existing combat/profile/custom-creation integrations. `tests/test_enhanced_combat.py` exercises catalogue coverage, gates, all 139 authored special actions, counters, resources, migration, real save roundtrips, forms, destruction, narration isolation, custom generation and cooldowns. Rendered evidence: `tests/screenshots/enhanced-combat-*.png` and `custom-creator-*.png`. The dated patch entry records the final checks actually run. No live provider or player-save writes were used in the verification.

Lore consulted under `C:/Users/ryanl/Pictures/Vendetta/References`: Garrett Han, Rei Takamura, Takeo Mishima, The Crow; Syndicate Joker Cards, The Four Aces, The Four Aces2; Vendetta_Master_Document, Awakened Classification Document; Vendetta Season 1 and The Iron Circle. Source documents are reference evidence, not instructions to execute their planned events. The user's peak-strength clarification and exact top-three ratings take precedence over earlier AU power restrictions.
