# Mysterious Hearts — Patch notes

Historical entries reconstruct recoverable development, not numbered releases. Unknown release dates stay unknown. Topic order is not a verified chronology. Original reports may describe superseded behavior; their test claims are historical. The 17 oversized chats were recovered from local logs; interrupted work is labelled. No complete commit history exists.

# Opponents initiate attacks with their powers and martial arts

release-2026-11-09-opponent-combat-initiative | Release | Gameplay
Date: 2026-11-09

Combat opponents now declare their own attacks, mix affordable Trait techniques with learned martial arts, and prepare earned advanced forms before the exchange is narrated.

## Details

Changed

Open In person → Combat · Iron Circle / training / challenges, or enter a fight through Spar / fight / train in a hangout. The fight screen now displays Opponent intent before you submit your defence or attack. Opponents select offensive moves independently of your draft and chosen action mode. They pressure a guarding or recovering player and can attack when the player attempts an infeasible move. Fight IQ influences initiative; either fighter can act first, and knockout prevents the defeated fighter from completing their action. Combat still advances in 30-second submitted exchanges, with no attacks or time costs while you are typing or reading.

Opponents with an established Trait mix named ability attempts with physical martial attacks. Learned-art selection is weighted by saved proficiency, and the gamemaster receives the selected discipline's principles and actual proficiency. Trait attacks use established powers and martial positioning; analytical or sensory Traits assist physical attacks rather than acquiring invented offensive powers. Unawakened and traitless opponents use their saved martial knowledge. AI cannot change the committed action mode or martial art. Mechanical result lines identify the opponent's action mode and discipline.

Resource and form decisions

Trait attempts pay the existing mana and stamina costs and count toward existing refinement progression when executable. The planner budgets the exchange's form upkeep before selecting a Trait attack, lowers requested complexity when mana is limited, uses martial pressure when a Trait is unaffordable, and recovers below 16 stamina. Gordon's Biocreation surcharge remains enforced. No ratings, power lists or existing damage multipliers were changed.

Sylvanis prepares Black-eyed Shadow Dominion, his earned second-stage Transcendence, from the opening of a serious encounter when he can afford activation, first upkeep and a basic Trait attack. His active form permits a piercing Umbrakinesis attack supported by predictive perception and learned martial positioning. Without the paid active form he uses ordinary shadow techniques; Alyssa gains none of his additional powers. Other eligible opponents consider an advanced form below 60% health, after four exchanges, or against an active player form. Existing once-per-encounter activation, timed expiry, mana upkeep and Conduit State's daily cooldown remain enforced. Exhausted fighters recover before preparing a new form.

Fixed

The gamemaster now sees projected resources and active forms for the exchange it is narrating. Previously, NPC forms could activate only after the model had already described a response using the earlier form state. Previewing a move does not spend mana or activate a form. Failed or mismatched judgements spend no resources or turn, and retries retain the same intent. A response generated against changed resources or abilities is rejected before costs. The same saved encounter state reproduces the same plan across refresh and save/load.

Validation and limits

Passed 74 focused combat, dialogue, Path, opponent-tactics and Interpol unit tests, including existing real save/load tests using isolated workspace temporary files. Passed real Tk opponent-combat, existing combat, Path, combat-dialogue and start-screen smoke checks. Passed the phone dark-theme audit across 34 pages and embedded controls. The new opponent smoke captured opening intent, compact controls, failed-provider retry, active Transcendence with a martial follow-up, stamina recovery and mana expiry. Visually inspected the compact Sylvanis opening and active-form captures. Test AI responses were mocked; live provider wording and extended combat balance were not evaluated. Existing optional sound-asset load warnings appeared during UI tests without failing them.

## Save compatibility

Restart the game to load the changed Python code. Existing stories and active fights retain their health, mana, stamina, stats, learned arts, Path progression, form usage, cooldowns and history. Opponent decisions and initiative change from the next submitted exchange, including in an already-active fight; there is no reset, migration or retrospective attack. No new power, breakthrough or offscreen progression is granted.

## Evidence and historical limits

Implemented for the report that opponents only countered the player and failed to initiate ability-based attacks, with Sylvanis's Umbrakinesis and Transcendence as the requested example. The attached screenshot is reference evidence. Decisions derive from existing saved combat profiles, earned forms and authored ability limits. Verified with deterministic engine tests, actual Tk smoke checks and rendered captures; no player story or live-provider request was used.

- combat_tactics.py
- combat.py
- combat_ui.py
- COMBAT.md
- tests/test_combat_tactics.py
- tests/test_combat.py
- tests/test_interpol.py
- tests/combat_opponent_ui_smoke.py
- tests/combat_ui_smoke.py
- tests/combat_path_ui_smoke.py
- tests/combat_dialogue_ui_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/start_ui_smoke.py


---

# Interpol investigations, Edward Fox and Jeremy Gordon

release-2026-11-09-interpol-awakened-operations | Release | Gameplay
Date: 2026-11-09

Two playable investigators, an Interpol organisation and influence system, witnessed-crime fines, nine case files and three repeatable field operations, with new character and location artwork.

## Details

Added

Edward Fox and Jeremy Gordon join the major cast and the playable roster (now 28). Both have canonical reference-sheet entries, appearances, dialogue boundaries, schedules, friendship routes, careers, starting funds, vehicles, home activities, contact numbers and private profile notebooks. Fox is a hardened, cynical vigilante and Interpol associate in Blackhaven, the western Winterfield suburb. Gordon commands Team 9 on regional deployment and lives in Civic Court near headquarters. Exact ages, heights, birthdays and romantic orientations remain unspecified. Fox has no Grove account: public posting, liking and automatic posts, photos, comments and replies are excluded. Private contact messaging remains available. Gordon has a public Grove profile.

Open In person → Interpol · cases, fines & field operations, or Tools → Interpol. The public desk accepts civilian case assistants. Assemble there with Gordon, normally 08:00–12:00, or with Fox when playing Gordon, normally 13:00–16:00. Existing recovery and appointments can change attendance. The team physically travels to objectives. Interviews, evidence collection, briefings, operations and combat use the in-person window. Bubblegram and Pocket Wallet provide dark private records, payment and a handoff to field work. Interpol is a legal organisation with personal clearance, not a gang membership.

Nine four-stage files investigate a Lantern Crew collection cell, a Rail Yard Saints consignment cell and Shinokami research referrals, followed by four independent Ace enquiries, the Crow’s command trail and Operation Night Ledger. Evidence, retries and completion persist. Each Ace connection is revealed only after its own corroboration, to the participating investigators. Established findings appear in their reference sheets, Bubblegram directory and audience-aware dialogue, and may be shared explicitly in person. Other private facts and insider working history are not granted. Headquarters entry is scoped to the final active operation and ends on completion or suspension. Victory can lead to the located Cardmaster’s regional custody; his birth identity and the wider Syndicate remain unresolved. Source-story future deaths and outcomes are not forced.

Three repeatable operations unlock after the Blackhaven file: witness-protection patrol, depot interception and waterfront extraction. Each permits one successful completion per story day. Successful cases/operations pay $250, increase district influence by 8 (maximum 95) and disrupt linked criminal commission pay by half for two story days.

Enforcement

Committed attacks, street theft/intimidation and documented coercive/reckless work decisions create saved incidents. Public patrol observation follows district influence; physically present witnesses and documented work trails can establish reports. Gordon issues a fine immediately when present. He declines the assault fine when Fox attacks a criminal target in his presence; this does not exempt civilian attacks or erase social consequences. Other witnessed/documented incidents receive regional review after 60 story minutes. Unobserved incidents without a documented trail do not generate fines. Sparring, agreed fights and authorised operations do not generate assault charges.

Base fines: assault $800, theft $300, intimidation $600, coercive request $500 and reckless commission $450. Repeat offences add 25% per earlier fine of that kind, capped at 75%. Pay through the Interpol record or Pocket Wallet using available funds; partial payments retain the balance and receipts. Paying does not repair relationship ruptures. Attacking a superior retains existing expulsion rules, revokes Interpol clearance and cannot be undone by registering again. A ruptured partner refuses case assembly.

Combat, art and interface

Fox’s Eight Senses and Gordon’s Biocreation integrate with existing combat profiles, mana, stamina, martial arts and the Path. Both start at Totality. Eight Senses support physical tracking clues, accuracy and evasive perception; they do not prove identities automatically. Gordon’s biological firepower has a distinct mana cost. The field partner takes actual supporting combat turns and can be counterattacked or incapacitated. Real victory/defeat gates progress. Failed attempts preserve evidence and require regrouping; knockout recovery still applies, with an in-person recovery action.

Fourteen new images: two transparent scene portraits framed head-to-upper-thigh like Ivan/Charles, two square contact photos used in contact details and messaging, two dark phone wallpapers and eight location backgrounds (Blackhaven, both homes/frontages and the three regional rooms). Existing headquarters exterior art remains. New destinations have map coordinates and clearance gates; existing Ace home coordinates were also filled in. Contact-profile text now wraps at the actual phone width. Original generated images and prompt/source records are retained.

Known scope and verification

This is an authored campaign and bounded offence system, not a procedural simulation of every possible narrated crime or gang activity. Dialogue cannot create charges, evidence, victories or reveals. A protagonist cannot investigate their own concealed Ace identity. Live AI combat/dialogue still uses the game’s configured provider; provider quality was not tested live.

Passed 144 focused unit tests covering Interpol, playable starts, combat/Path/dialogue, crime sites/operations, Bubblegram/jobs, numbers/maps, Grove, assets, Aces, colleagues and patch notes. The 18 Interpol tests include the full nine-case progression with save roundtrips, partial disclosures, immediate/delayed fines, payment, Fox’s exception, expulsion, partner resources/travel, old-save migration and artwork paths. Passed real Tk Interpol, combat, crime-operations, playable-cast and start-screen smoke checks. The expanded playable smoke exercised all 24 additional protagonists. The mandatory dark-theme smoke passed across 34 phone pages and embedded interactive states. Inspected rendered portraits, compact casework, combat, contact photos, records and location scenes; the Interpol smoke also captured all new scene backgrounds. Tests mocked AI and did not write player stories.

The exploratory full discovery run executed 886 tests and reported 22 failures plus 11 errors before the final fixes. New-cast missing messaging files/wallpapers and the map-coordinate gap found in that run were corrected and covered by the passing focused rerun. The full suite was not rerun to claim a clean result: older dialogue, romance, roster/asset assumptions and a sandbox-blocked localhost HTTP test remain outside this update’s verified scope. The separate legacy phone-map smoke also stops at an existing public-venue title expectation; Interpol map rendering and the map unit tests passed.

The updated catalogue passed validation and its six unit tests, was exported to PATCH_NOTES.md, and passed the patch-notes reader UI smoke (isolated workspace temporary preferences) and final 28-character start-screen smoke.

## Save compatibility

Restart to load the Python and art changes. Existing stories gain Fox, Gordon and empty Interpol records additively; existing money, relationships, contacts, history and career progress remain. No retrospective fines or identity discoveries are applied. Incident IDs, payments, case stages, partner encounters, knowledge and custody use the story save. Choose a new story to play Fox or Gordon. Existing custom phone wallpaper selections are preserved. Retain the installed art files with the game.

## Evidence and historical limits

Implemented from the user’s requested Interpol update and portrait-framing correction. The supplied faction/world documents and Fox image are reference data; the user’s Blackhaven, homes, no-Grove, combat and discretion requirements take precedence. Case facts, routines, balance and outcome branches are explicit AU game content. Artwork generated with built-in image_gen and inspected in the actual Tk interface. Checks and broader-suite limitations are recorded above without asserting live-provider or full-suite success.

- interpol.py
- interpol_cases.py
- interpol_cast.py
- interpol_ui.py
- interpol_source_notes.json
- tests/test_interpol.py
- tests/interpol_ui_smoke.py
- tests/phone_dark_theme_smoke.py
- assets/ui/locations/interpol-art-prompts.json
- README.md


---

# Combat conversations now use the regular hangout scene

release-2026-11-09-combat-in-regular-hangouts | Release | Interface
Date: 2026-11-09

Sparring, challenges, attacks and lessons now use the same illustrated hangout window as ordinary conversations, before transitioning to combat.

## Details

Changed

Open Spar / fight / train during a regular in-person hangout. Choose a present participant, ask to spar or challenge them, request an available lesson, or confirm an attack using compact controls in the existing hangout window. Requests from the combat hub also enter a regular hangout with the selected person. The separate combat-dialogue page has been removed.

AI responses appear in the normal character speech bubbles, with the location artwork, portraits, player line and narration. After an agreed encounter or retaliation, Continue to fight opens the fight window. A refusal or lesson returns to ordinary hangout interaction. When someone flees, their final response remains visible until Return to location; the closed hangout is not reopened. Existing consent, training, flight, relationship and breakup rules are unchanged.

Fixed

Recorded narration now precedes the character response so the normal hangout renderer retains both the player line and response in the same exchange. Automatic game time pauses while this combat response is generating or being read, preventing routine clock advances from invalidating it. Failed generation displays an inline retry message without spending training time or starting a fight.

Validation

Passed 45 combat/dialogue/path unit tests and 10 hangout unit tests. Passed the combat dialogue UI smoke with seven rendered screenshots, normal and compact layouts, refusal, agreement, fight transition, attack confirmation, fleeing, failed-provider retry and lesson responses. Passed existing hangout scene, combat, patch-notes and start-screen UI smoke checks. Visually inspected the rendered hangout agreement, compact controls and flee response. AI replies were mocked; no live provider request or player-save writes were used.

## Save compatibility

Existing saves remain compatible; restart to load the changed UI. Combat dialogue and hangout history remain saved through the existing records. No migration is required. Already-active fights reopen in the fight window after loading.

## Evidence and historical limits

Implemented in response to the request to reuse the regular hangout window. Verified with deterministic unit tests, real Tk UI smoke checks and inspection of generated screenshots.

- hangout_combat_ui.py
- hangout_ui.py
- game.py
- combat_ui.py
- combat_dialogue.py
- tests/combat_dialogue_ui_smoke.py


---

# In-person combat dialogue and attack reactions

release-2026-11-09-combat-dialogue-reactions | Release | Gameplay
Date: 2026-11-09

Discuss sparring, challenges and lessons before combat, with character-specific responses to attacks and romantic breakups.

## Details

Added

In an in-person conversation, choose Spar / fight / train to open combat dialogue with the sole present conversation partner. With several people, choose a nearby person in the combat hub. Ask to spar, challenge them, request an available teacher discipline, or choose Attack and confirm. The configured AI writes a character-specific spoken response and narration using character lore, relationship state and recent conversation. Read the response and choose Continue to fight after agreement. Refusals leave combat inactive; eligible characters can also decline dynamically. Lessons retain the existing 30-minute cost, training limits and teacher requirements.

Changed

Emily runs away when attacked; Samantha fights back. Other characters fight back at martial skill 35 or above, otherwise flee. Fleeing ends an active shared hangout and removes the character from the location without a combat encounter or combat-progression reward. All attacks preserve permanent relationship rupture and existing ally/faction consequences. Attacking a current dating, official or strained romantic partner now invokes the established volatile-breakup system, cancels their date and records the breakup, whether they flee or fight.

Reliability

Requests recheck physical presence, recovery, eligibility and scene time before applying. Malformed or contradictory AI responses fail without starting combat or training. Failed generation can be retried. A generated response cannot be applied twice. Dialogue is saved in combat records and the current hangout transcript, including an archived hangout after fleeing.

Validation

Passed 45 combat/dialogue/path unit tests and 12 relationship-dynamics tests. Passed combat dialogue UI smoke (six rendered screenshots, including agreement, refusal, attack confirmation, fleeing and compact layout), existing combat UI smoke, patch-notes UI smoke and start-screen UI smoke. AI responses were mocked; live provider dialogue quality was not tested.

Known limitations

Combat invitations are explicit dialogue actions; arbitrary typed conversation does not automatically execute an attack or a lesson. Attack reaction rules outside Emily and Samantha currently use martial skill. Attacks on current romantic partners always trigger a breakup.

## Save compatibility

Existing saves remain compatible. Restart the game to load the changed Python code; new combat dialogue records are added lazily. Existing relationships and combat records are retained. New attacks now trigger flight or retaliation and end an existing romance; historical attacks are not retroactively replayed.

## Evidence and historical limits

Implemented for the requested dialogue-driven combat interaction; behavior verified with deterministic unit tests and rendered UI smoke checks. No live AI call or player-save mutation was used for validation.

- combat.py
- combat_dialogue.py
- combat_ui.py
- hangout_ui.py
- tests/test_combat_dialogue.py
- tests/combat_dialogue_ui_smoke.py
- tests/test_combat.py
- tests/combat_ui_smoke.py


---

# Combat part 2: Awakening, the Path and Transcendent breakthroughs

release-2026-11-09-combat-path-progression | Release | Gameplay
Date: 2026-11-09

Earn Awakening through combat, progress through Ascension and Totality, and unlock mana-intensive, Trait-based Transcendence trump cards through qualified breakthroughs.

## Details

Added

Open the in-person Combat hub and choose The Path · progression & breakthroughs. The dedicated dark view shows current stage, mana potency, refinement, encounter requirements, exact remaining breakthrough time, stage history and the current trump card. View Path beside a selected nearby fighter exposes the same progression system and allows a willing, qualified NPC to be invited to attempt a breakthrough.

Dormant characters with latent mana awaken after 30 strenuous completed encounters. Awakening keeps mana potency fixed; 15 encounters in that stage and refinement 40 when a Trait exists unlock Ascension. Ascension gives +1 potency per strenuous encounter; 40 encounters in that stage and refinement 80 when a Trait exists unlock Totality. Totality stops further potency growth. The early encounter thresholds, refinement gates and boost sizes are explicit authored balance; the complete rules are visible in the Path view and COMBAT.md. Awakening does not automatically invent a rare Trait. Traitless Awakened can reach Totality through encounters but cannot satisfy Trait-mastery requirements for Transcendence. The data model also supports characters without latent mana, who remain dormant.

A strenuous encounter must deal at least 10 damage in total and last four exchanges, or finish in knockout after at least one exchange. Substantial spars, wins and losses count for both participants. Empty sessions and immediate concessions give no progression. Every four executable, paid Trait uses across qualifying encounters give +1 refinement; unused progress is saved. Impossible moves or moves blocked by energy, stamina or refinement do not count. Stage rewards are applied once and cannot be repeated by finishing or loading the same encounter.

Breakthrough to Transcendence 1 requires an established Trait, refinement 93+ and 30 complete in-game days in Totality. Transcendence 2 requires refinement 100 and 30 complete days in Transcendence 1. These are hard gates, rechecked when the AI response returns. An eligible successful generation creates a saved trump-card name, techniques, limits and mechanical expression based on the existing Trait; invalid or failed generations grant nothing, and stale results cannot be reused. No hidden random failure roll is added. Both Transcendence stages resume encounter-based potency growth, capped at 100.

Garrett and Charles start at Transcendence 1; Sylvanis starts at Transcendence 2. Rei, Takeo, the Crow, the Four Aces, Ivan, Neo, Daniel, Tyler and Thirteen begin at Totality. Minsu, Samantha, Valentina, Emily, Alyssa and Keisuke begin at Ascension; April and newly created Awakened protagonists begin at Awakening. Unawakened characters begin in Dormancy. Explicit user-specified starting stages take precedence; the remaining assignments are authored interpretations of existing peak profiles. Existing numeric peak ratings are retained rather than receiving duplicate stage-entry boosts.

Changed

Direct awakened-power conditioning no longer bypasses stage restrictions. Stage-entry boosts, encounter potency growth and Trait use now govern power progression. Trait refinement and martial/analysis training remain available. The creator's old statement that Traits have no combat controls was replaced with accurate Path starting-state guidance. Dialogue and combat prompts receive the saved stage and Path definitions.

Transcendence trump cards replace the old free, encounter-long activations. Stage 1 costs 35 mana plus 8 per exchange for up to 180 seconds; stage 2 costs 55 plus 12 per exchange for up to 300 seconds. They boost damage, accuracy and defence; generated offence, defence, precision, mobility or control expressions apply bounded bonuses. Insufficient upkeep ends the form. NPCs reserve these cards until below 60% health or after four exchanges. Ivan's five-minute, once-per-day Conduit State remains a separate Trait technique and remains selectable if he later becomes Transcendent. One advanced form can be activated per encounter; forms do not stack.

Validation

All 35 combat/progression tests passed: the 18 original combat tests and 17 new Path tests cover cast seeding, no duplicate migration boosts, Dormancy awakening, no-mana profiles, stage thresholds, fixed/growing potency, Trait usage, NPC rewards, exact breakthrough boundaries, failed/stale generation, finite form costs and real save/load persistence. Custom-protagonist (11), playable-cast (7) and Vendetta-lore (5) suites passed. Path UI smoke captured six rendered states covering locked/ready progression, compact layout, AI failure/retry, successful stage-two breakthrough and a paid trump card. The existing combat UI smoke passed. Dark-phone smoke passed across 34 pages and start-screen smoke passed.

Known limitations

Live AI output and extended progression balance were not playtested; AI UI checks use mocked responses. Early-stage thresholds, stat boosts, advanced-form costs and expression multipliers are game balance, not quoted source numbers. No offscreen combat or historical training is invented. Natural Awakening can be traitless, and artificial Velirium/cybernetic awakening remains lore rather than an implemented activity. The full repository suite was not rerun for this update.

## Save compatibility

Restart to load the update. Existing combat stats, training, relationships, ledger and encounter history remain. Path metadata migrates once without reapplying starting-stage bonuses. Existing saves start their new stage-residency clock when the update first encounters their combat data, so no unverified pre-update days or encounters satisfy a breakthrough. New games use the start-of-play clock. Active legacy fights retain health, resources and turn history but reset their old indefinite form activation once to enforce the new paid, timed rules. Stage history, residency, Trait-use remainders, generated trump cards and NPC progression are saved.

## Evidence and historical limits

Implemented from the user's Combat update part 2 definition of Awakening and the Path, with exact 93/100 refinement gates, 30-day residency requirements and named Transcendence starting stages. Unspecified early progression thresholds and mechanical form values are documented authored balance. Local tests used the bundled Python runtime and workspace temporary directories; no live AI generation success is claimed.

- combat_path.py
- combat_profiles.py
- combat.py
- combat_ui.py
- vendetta_lore.py
- custom_creator_ui.py
- custom_protagonist.py
- COMBAT.md
- tests/test_combat_path.py
- tests/test_combat.py
- tests/combat_path_ui_smoke.py


---

# Combat: peak powers, martial training and the Iron Circle

release-2026-11-09-combat-iron-circle | Release | Gameplay
Date: 2026-11-09

Fight in the in-person window, learn martial arts, develop combat stats and enter a twice-weekly Iron Circle circuit with lasting social consequences.

## Details

Added

Open Combat from the in-person location screen, or Spar / fight / train during a hangout. The dedicated combat stage supports custom defence and attack descriptions, health, stamina, awakened energy, learned martial disciplines and an AI gamemaster through the existing configured game provider. The AI judges feasibility, complexity and tactical advantage and chooses the opponent's response; bounded stat rules resolve success and resource changes. Failed AI requests spend no turn, preserve the draft and can be retried. Active encounters resume after saving and loading.

Visit the Iron Circle and sign its physical ledger to enter at rank 450. Two cards per seven-day game week open at 18:00 on day offsets 1 and 4 and close at 21:00. The hub displays the next date and offers a wait-until-card action. Opponents have AI-generated identities, disciplines and bounded high-tier Traits, with rating limits enforced by the game. Ranks 450–301 are unawakened, 300–101 Awakened without Traits and 100–1 Trait-users. Matches run three five-minute rounds in 30-second exchanges, ending early at knockout or concession. Judges resolve time-limit results; wins improve rank by ten and losses drop five, bounded to 1–450.

Peak source-story power is the combat baseline for named protagonists and NPCs. Sylvanis, Takeo and the Crow retain the user's exact four ratings. Other numeric ratings are authored balance interpretations. Garrett, Charles and Sylvanis have usable Transcendence; Ivan has a five-minute Conduit State limited to once per 24 game hours without an added activation cost or crash. Emily has peak Critical Hit in combat; Neo and Daniel use developed source abilities. This does not import future deaths, romances or predetermined victories.

The requested instructor roster teaches the requested disciplines, with Sylvanis teaching all supported arts and Takeo and the Crow excluded from teaching. Lessons require the teacher's physical presence and sufficient trust. Training takes 30 minutes and is limited to three sessions per day. Awakened power affects force, health, energy and durability; refinement gates complex Trait use; martial skill and art proficiency affect techniques; fight IQ affects evasion and counters. Custom unawakened characters start at 0/0/8/10, and awakened characters at 18/12/12/14 with their authored Trait. Training does not automatically awaken characters.

Friendly spars have no winner or loser. Agreed fights and unwarranted attacks have a clear victor and no round deadline. Invitations can be declined; attacks require an explicit player confirmation but not NPC consent. NPCs can propose spars or challenges following training discussion or heated conversation, and never initiate attacks. A knockout never kills anyone; it causes 1,440 game minutes of inactivity, including for the protagonist. Recovery can be completed from the combat hub.

Attacks permanently rupture the target relationship and block ordinary repair, reduce allies' trust, expel a member who attacks an organisational superior, and reduce diplomatic relations between opposing organisations by 30. Established command access and sponsorship respect excommunication.

Changed

Combat occupies the in-person stage and pauses ordinary routines while exchanges advance the world clock. Phone access redirects to the combat/recovery stage while the protagonist is unavailable. After the new ledger is signed, Rei's old career finales cannot independently award circuit victories; legacy history remains and the career rank follows the ledger. Martial descriptions and peak-power context are supplied to the gamemaster.

Validation

All 18 combat tests passed, including real save/load resume, stale-turn rejection, tier limits, consent, training, knockout recovery, three rounds, Conduit cooldown and canonical command expulsion. Targeted hangout, career, diplomacy, simulation-clock, relationship-dynamics, message-timing, crime-operations, faction-work, Bubblegram, custom-character, playable-cast, custom-gang and crime-site suites passed. Combat UI smoke completed a mocked AI exchange and captured six rendered screens, including compact layout, attack confirmation and result. Phone dark-theme smoke passed across 34 pages; hangout, patch-notes and start-screen UI smoke checks passed.

Known limitations

Live provider output and extended balance were not playtested. NPC consent/proposals use authored character, trust and conversation-keyword rules; generated combat text describes attempts while mechanical result lines report outcomes. The complete repository suite stalled during Tk tests and was interrupted. The targeted world suite passed 13 of 15 tests; remaining failures concern unchanged unique-art coverage (97 versus 106 locations) and old home-count expectations (18 versus 27). Full technical behavior, source interpretation and balance choices are documented in COMBAT.md.

## Save compatibility

Restart the app to load the update. Existing saves gain combat data lazily and retain relationships, histories and career records. Combat encounters, resources, profiles, training, rank, cooldowns, recovery and attack consequences are saved. New ledger entrants begin at rank 450, including established protagonists. Peak abilities intentionally supersede earlier combat restrictions; permanent attack consequences apply only to attacks performed through the new combat controls.

## Evidence and historical limits

Implemented from the combat-update request and the follow-up requiring peak source-story strength. Consulted the supplied Garrett, Rei, Takeo, Crow, Joker Cards, Four Aces, master-world, Awakened-classification, Season 1 and Iron Circle reference documents. Exact top-three ratings come from the user; other numbers and scheduling/rank thresholds are explicit game balance. Validation used the bundled Python runtime and workspace temporary directories; no live AI-output success is claimed.

- combat.py
- combat_profiles.py
- combat_ui.py
- COMBAT.md
- tests/test_combat.py
- tests/combat_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Strangers recognise famous characters

release-2026-11-09-public-celebrity-recognition | Release | Characters
Date: 2026-11-09

New introductions can acknowledge Rei’s modelling fame, Elias Braun’s acting career and Ivan Yeun’s public idol identity without treating them as personal acquaintances.

## Details

Changed

Meet someone new through the existing in-person conversation window, including group encounters. Shared dialogue references now direct NPCs to briefly recognise an identifiable Rei, Elias or Ivan on a first introduction, without needing a fame question. Reactions should fit the individual speaker: tentative confirmation, enthusiasm, understated recognition or composed acknowledgement, rather than a fixed line or universal fan response. The same references support player reply suggestions without scripting the player's actions.

Existing connections and supplied conversation history take precedence: familiar people should not repeat first-meeting surprise. Fame supplies public career knowledge, not trust, intimacy, contact access, private memories, criminal identities or powers. Masked operational appearances must not reveal a celebrity identity through fame. Text conversations can recognise an established name or introduction but cannot invent a live view, photo or recognition from an anonymous handle alone. Elias also joins the public-face appearance reference used for named questions.

Validation

Four new public-recognition tests and all five social-world tests passed with the bundled Python runtime; the save test used a workspace temporary directory after the default sandbox temporary directory denied access. The conversation-lore suite passed 28 of 31 tests; three failures concern existing reference-table gaps: Charles's TV-show preference, Garrett's listener entry for Elias, and Nessa Quinn's portrait styling. No phone layout or UI surfaces changed.

Known limitations

Recognition wording and continuity are model-directed using supplied history, not fixed scripted responses or a new persistent recognition flag. Live AI-generated dialogue was not sampled. The full repository suite was not run.

## Save compatibility

Restart the app to load the changed dialogue references. Existing saves remain compatible; no migration or relationship changes are required. Prior conversation history and authored acquaintances remain authoritative.

## Evidence and historical limits

Implemented from the request for personality-dependent celebrity recognition on new introductions. Verified through local reference and regression tests; no live model-output claim is made.

- social_world.py
- tests/test_public_recognition.py
- tests/test_social_world.py
- tests/test_conversation_lore.py


---

# Protagonist wallpapers, garages and established Bubblegram roles

release-2026-11-09-cast-wallpapers-bubblegram-garages | Release | Characters
Date: 2026-11-09

Charles gains a contact photo, all 26 protagonists receive individual phone wallpapers, and six established Syndicate characters gain playable Bubblegram desks.

## Details

Added

All 26 playable protagonists have individually generated, dark illustrated phone wallpapers reflecting their interests and surroundings. Charles has a square reference-based contact photo used in messaging avatars and contact details. Existing contact access rules still apply; this artwork does not unlock Charles.

The 22 expanded protagonists now have named personal vehicles, with multiple models for most. Choose a model under Town → Plan a drive; single-car garages show the model directly. Vehicle selection is saved, trip history records the chosen model, and larger parties use the existing passenger-van fallback. The original four retain their existing garages and starting gameplay.

Bubblegram integration

As Sylvanis, Valentina, Martos, Elias, Mavis or Camila, open Phone → Bubblegram → Contracts or Network → Leadership. Sylvanis has a cross-Suit Coloured Joker desk; Valentina has Clubs field command; each Ace has a mission-specialist desk reporting to the Cardmaster without becoming a Suit commander. Each role has tailored commission briefs and venues, a separate one-time operating reserve, diplomatic meetings and deals, and career-linked leadership outcomes. Established characters no longer enter newcomer faction sponsorship trials. Existing site permissions and identity secrecy remain authoritative.

Physical contract resolution and deal settlement for these six roles open the main in-person window. Opening the desk does not complete work or advance time; travel to the listed venue and choose an approach there.

Validation

50 focused tests passed across Bubblegram progression, job contracts, diplomacy, phone personalization, playable-cast compatibility and new asset/vehicle coverage. New real-Tk smoke checks rendered all 26 wallpapers, Charles's contact details and all six desks, audited dark surfaces, and completed six in-person contract workflows. Screenshots were visually reviewed. The general dark-theme smoke passed across 34 phone pages and embedded controls. All six patch-note tests passed; the catalogue validated and was exported. Patch-note UI and start-screen smoke checks also passed, including 26 previews and minimum-window layouts.

Known limitations

Cars are named models in the existing travel system, not new 3D assets or a driving simulation. Individual authored story arcs remain future work. An additional legacy phone-personalization UI smoke was interrupted after failing to finish; it is not counted as passed. The full repository test suite was not run.

## Save compatibility

Restart the app to load the changes. Existing saves remain compatible. Default wallpapers update automatically; custom photo wallpaper choices remain selected. Old generic expanded-cast car selections fall back to that protagonist's first named model. The six canonical Bubblegram roles migrate once, archive prior sponsorship/gang records, retain reputation and heat, and do not repeatedly refill operating money or reset earned losses. Original four protagonist startup data and garages remain unchanged.

## Evidence and historical limits

Implemented for the requested protagonist phone wallpapers, Charles contact artwork, six Bubblegram integrations and individual car models. Built-in image generation created the artwork; local offline tests and rendered screenshot inspection verified integration. Validation claims list completed checks only.

- assets/ui/protagonist-wallpapers-manifest.json
- assets/profiles/charles-contact-v3.json
- phone_personalization.py
- protagonist_vehicles.py
- bubblegram_roles.py
- bubblegram_workplace_ui.py
- job_apps_ui.py
- crime_diplomacy.py
- tests/test_protagonist_expansion_assets.py
- tests/phone_cast_assets_smoke.py


---

# Garrett takes news of Charles seriously

release-2026-11-08-garrett-charles-news | Release | Dialogue
Date: 2026-11-08

News about Garrett’s missing brother now calls for concern, urgent hope and practical questions even at low trust.

## Details

Fixed

When texting Garrett about Charles, his dialogue guidance now distinguishes receiving important news from disclosing private family history. Low trust no longer directs him to dismiss the subject with a family boundary. Reports such as “I found him” call for shock, hope and concern for Charles’s safety; reports of Syndicate work call for alarm and confusion. Guidance applies to pronoun-only follow-ups and asks him to use details already supplied. Established reunions remain authoritative.

Access and story rules

Continue a direct conversation with Garrett and tell him what you learned. Reports are acknowledged as claims, not automatic proof of allegiance or motive. Texts do not advance the authored investigation, grant laboratory access or complete a reunion; those actions remain in person. No layouts or phone styles changed.

Validation

All 11 Charles disclosure, character and quest tests passed. Of 31 conversation-lore tests, 28 passed including two new regression tests covering low-trust phone prompts, pronoun-only follow-ups and completed-reunion continuity. Three broader reference-data checks failed for missing Charles TV preferences, expanded-protagonist audience entries and Nessa Quinn portrait style. No live AI generation was performed; generated wording and emotional delivery remain model-dependent.

## Save compatibility

Restart the app to load the updated dialogue guidance. Existing saves, investigation progress and message history are retained; no migration or new game is required. Earlier messages are not rewritten.

## Evidence and historical limits

Implemented in response to the supplied screenshot showing Garrett treating news of Charles as a low-trust family-history question. Validation reflects local offline tests, not a live generated response.

- conversation_lore.py
- tests/test_conversation_lore.py
- tests/test_charles_disclosure.py
- tests/test_charles_han.py
- tests/test_charles_quest.py


---

# 26 playable perspectives in Winterfield

release-2026-11-08-expanded-playable-cast | Release | Gameplay
Date: 2026-11-08

Play all main characters except Charles Han, Number Thirteen, Takeo Mishima and The Crow, with distinct sandbox starts while retaining the original four starts.

## Details

Added

The new-game screen now pages through 26 canonical protagonists in groups of four. Previous and Next preview the cast; Begin starts the selected character. The original four remain on the first page. Added Yuriko, Emily, Sophie, Amy, Samantha, April, Lena, Naomi, Celeste, Dev, Rosa, Elliot, Tyler, Valentina, Daniel, Neo, Alyssa, Sylvanis and the Four Aces.

Each of the 22 new starts begins at that character’s established home with a distinct starting budget, themed phone accent and note, home activities, appropriate existing contacts, and a work or study track. Open In person > Winterfield location controls > Careers > Open work & ambitions. Calendar career links also open this dashboard in the main in-person window, hiding the phone and ending an active in-person conversation. Sessions require arrival at the workplace during its opening hours. Each track has three situations with character-specific decisions affecting craft, reputation or autonomy; longer shifts increase rewards and fatigue. Study, athletics and field-recording practice are unpaid. Projects require work on three separate days followed by a booked review, and later support advanced briefs.

Established siblings remain nonromantic in either playable direction. Neo and Alyssa start as committed partners in their shared apartment, with other romantic routes unavailable. Sylvanis has no romance routes. Other new protagonists use mutual canonical orientation and family restrictions. Existing faction clearance remains enforced; wealth and work rewards are sandbox balance rather than new biographical claims. Player-only vehicle options do not replace the autonomous cast’s existing vehicles.

Compatibility

The original Garrett, Rei, Minsu and Ivan starting funds, locations, relationships, contacts and existing careers are retained. New protagonist initialization is restricted to new games and never reapplies starting wealth or resets progress on load. Dialogue and suggested replies use the selected identity, including female protagonists and the established Neo/Alyssa partnership.

Validation

Seven expanded-cast integration tests passed, covering all 22 new starts, work decisions and daily limits, home travel, autonomous player exclusion, save/load, dialogue identity, family and partner boundaries, exclusions, faction clearance, project finales and original-start snapshots. A further 23 focused legacy regression tests and 26 career/custom-protagonist tests passed. The start-screen smoke passed for 26 previews and paginated selection at default and minimum layouts. The expanded-cast UI smoke exercised all 22 new protagonists in the desktop, dark phone and in-person work dashboard. The phone dark-theme smoke passed across 34 pages. Rendered selection, phone and work-decision screens were visually inspected. The final combined run passed all 62 focused tests, including six patch-note tests. Catalogue validation and the patch-note UI smoke passed, and the Markdown export was refreshed. The patch-note empty-filter smoke now uses an intentionally absent query so new matching releases do not invalidate its fixture.

Known limitations

This is shared sandbox support, not 22 new authored story campaigns. Live AI response quality and audio playback were not tested. Broader legacy test attempts were not fully green: some fixtures assumed unrestricted access to hidden characters or existing contacts, and the local HTTP test encountered environment restrictions. These results are not represented as a full-suite pass.

## Save compatibility

Restart the app to load the expanded selection. Existing original-protagonist saves retain progress and do not need a new game. Choose a new story to play a different protagonist; this does not convert the player identity in an existing save. The new starts save and reload using their existing stable character IDs. Custom protagonists remain supported.

## Evidence and historical limits

Implemented for the request to make all eligible main characters playable before developing their individual story content. Original starting-state snapshots were captured before changes; checks listed above were actually run.

- playable_cast.py
- game_core.py
- start_ui.py
- town.py
- world_loop.py
- hidden_cast.py
- careers.py
- careers_ui.py
- tests/test_playable_cast.py
- tests/fixtures/original_protagonist_starts.json
- tests/playable_cast_ui_smoke.py
- tests/start_ui_smoke.py
- tests/phone_dark_theme_smoke.py
- README.md
- tests/patch_notes_ui_smoke.py


---

# Charles’s private number and Garrett’s eyewitness lead

release-2026-11-08-charles-private-contact-eyewitness | Release | Story
Date: 2026-11-08

Sylvanis alone starts with Charles’s number. Garrett earns private texts through their reunion; other protagonists can help bring the brothers together.

## Details

Added

Charles retains a stable private phone number. Sylvanis has direct contact from the outset; Garrett gains it after his authored private laboratory reunion. Charles queues a brief reassuring text through normal messaging. Numbers cannot be guessed into unauthorised contacts, exposed in group number context, or used to add Charles to group chats. Existing written check-ins remain optional. Charles remains inside the Glasshouse.

After actually meeting Charles, another protagonist can select Charles sighting · tell Garrett in the in-person location window. Privately report the sighting, return to Charles with Garrett’s family-memory question, and deliver the sealed reply. Garrett reacts with cautious hope and concern, authenticates the chipped-teacup memory, then arranges a private visit from 20:00 on the next story day. The meeting uses normal travel and requires twenty uninterrupted minutes without the player or other staff in the lab; commitments and interruptions postpone it. Ask Garrett afterwards for his guarded thanks and relief. His private explanation and Charles’s number are not disclosed to the reporter. Sylvanis retains his pre-existing number access.

Changed

Saved conversation context remembers the eyewitness report and eventual reunion instead of reverting NPC Garrett to ignorance. The report never completes the playable Garrett documentary trail or imports another save’s knowledge. Character references document the updated boundaries. Opening the investigation ends the current hangout and uses the main window. Fixed a duplicate start-screen button-padding argument that prevented UI launch during verification.

Validation

38 focused tests passed covering Charles, phone numbers, criminal dynamics, laboratory missions and living-world integration. Both Charles quest and eyewitness UI smokes passed; rendered report and unlocked private-contact screens were inspected. The dark-theme smoke passed across 34 phone pages. The separate start-screen smoke still fails an existing visibility assumption for paginated character buttons. No live AI response quality or audio playback was tested.

Patch-note catalogue validation, six patch-note tests and the patch-note UI smoke also passed; the Markdown export was refreshed. Test temporary files used the workspace directory because the default temporary directory is restricted.

## Save compatibility

No restart of the story required; restart the app to load changed code. Existing reunited Garrett saves automatically regain Charles’s contact. Unauthorised stale contacts are removed. Eyewitness progress is created only by explicit in-person reporting and remains in that save; old quest evidence and endings are retained.

## Evidence and historical limits

Implemented for the user’s revised phone-access and eyewitness-storyline request. Checks and limitations recorded from this session; generated dialogue remains subject to the existing model service.

- charles_han.py
- charles_disclosure.py
- charles_quest.py
- charles_quest_ui.py
- phone_numbers.py
- messaging.py
- hidden_cast.py
- groups.py
- world_loop.py
- conversation_lore.py
- Mysterious Hearts - Character References.md
- tests/test_charles_disclosure.py
- tests/charles_disclosure_ui_smoke.py
- tests/charles_quest_ui_smoke.py
- tests/phone_dark_theme_smoke.py
- start_ui.py


---

# Find Charles: a complete investigation and private reunion

release-2026-11-08-find-charles-complete | Release | World & story
Date: 2026-11-08

Follow Garrett’s eleven-stage search from Mei’s papers to a private laboratory reunion, with recoverable setbacks, two endings and written check-ins. Charles has no phone number.

## Details

Added

As Garrett, open Find Charles from the main screen, location activities or Winterfield. Every entry opens the investigation in the main in-person window. The panel shows the current objective, travel control, available responses, verified evidence and saved outcomes. It does not execute physical investigations in the phone.

Eleven stages develop Mei’s slip and receiving copy through dispatch totals, receiving procedure, Mei’s index, a recovered authorisation, Greyglass testimony, corroboration, a family-only authentication question, the reunion and a choice of future relationship. Records connect Hong Kong shipping evidence to Winterfield without pretending a cargo stamp proves a passenger’s identity. The early three Winterfield enquiries and both original documents carry forward from existing saves.

Document responses from the third through ninth stage require a new story day. Unsupported assumptions, an accusation or a wrong family answer pause progress until the next day; correct evidence can recover the trail, so there is no permanent failure lock. The notebook records verified findings and keeps choices and setbacks in the save.

An authenticated letter provides personal Glasshouse directions and visitor access without Syndicate membership, research access or private mission clearance. The reunion requires Garrett and Charles physically in the lab, alone, between 19:00 and 23:00. Other listeners block sensitive discussion. A Garrett who legitimately reached the lab earlier through Jack clearance can recognise Charles and request a private explanation without fabricating completion of the documentary trail.

The authored reunion establishes that Charles is alive and deliberately went undercover alongside Sylvanis to avenge their parents. It names no new culprit, executes no revenge and does not import the source-story death. Garrett can choose a quiet alliance or guarded reconciliation with stronger boundaries. Both preserve Charles’s cover and laboratory residence; the endings grant different bounded trust gains and a one-time closeness gain. Completed choices cannot be replayed for rewards. Afterward, read a brief written check-in at the Golden Dragon once per story day. No phone communication is created.

Changed

Charles has no assigned or saved telephone number, even after meeting him. His old number is removed from saved directories and contacts while its registry slot stays reserved so other residents’ numbers remain stable. Existing histories are retained. Direct and group texts, queued Charles replies and new number exchanges are blocked. Known in-person encounters and friendship remain available, and the profile says that he has no number.

Saved quest state updates Garrett’s and Charles’s private dialogue continuity only in Garrett’s story. Other playthroughs do not inherit the reunion, and mixed audiences receive instructions to keep the location and mission private. Garrett’s guest lab view contains no research briefing or operational assignment board.

Validation

35 targeted tests passed across the new quest, Charles integration, phone numbers, laboratory missions, criminal dynamics and living-world compatibility. Both endings, save/load at every step, legacy clue projection, setbacks and retry timing, physical/privacy gates, early legitimate encounters, personal clearance limits and retired phone access were exercised. charles_quest_ui_smoke.py passed all eleven chapters, main-window handoff, scrolling, completion and the numberless profile. Rendered reunion/completion screens were inspected. phone_dark_theme_smoke.py passed all 34 phone pages and control states.

Known limitations

This quest resolves finding Charles and learning his motive, not his unfinished infiltration or the parents’ case. Choices advance authored scenes rather than generating new clues. Written check-ins rotate three authored notes. Dialogue privacy is supplied through scoped context and guards; no live generated dialogue was tested.

## Save compatibility

Restart to load code. No new story is required. Original unopened/slip/traced progress and up to three saved Winterfield enquiries map to the matching quest stage when first used, preserving their response-day timing. Current routes, relationships and histories remain. Obsolete Charles phone contacts and directory entries are removed automatically; other phone numbers do not shift. Quest visitor access is personal to Garrett and does not grant research or faction privileges.

## Evidence and historical limits

Implemented from the user’s request to fully develop Garrett’s search and remove Charles’s telephone on 8 November 2026. New intermediate clues, reunion dialogue and endings are authored game content. Original search evidence and established undercover canon were preserved.

- charles_quest.py
- charles_quest_ui.py
- charles_han.py
- game.py
- presence_ui.py
- living_world_ui.py
- hidden_cast.py
- phone_numbers.py
- phone_ui.py
- groups.py
- messaging.py
- criminal_dynamics.py
- crime_sites_ui.py
- conversation_lore.py
- town.py
- Mysterious Hearts - Character References.md
- tests/test_charles_quest.py
- tests/charles_quest_ui_smoke.py


---

# Charles Han joins the Glasshouse main cast

release-2026-11-08-charles-han-laboratory | Release | World & characters
Date: 2026-11-08

Meet Garrett’s missing older brother as a laboratory-bound main character, with a private undercover history, authored personality and matching portrait.

## Details

Added

Charles Han is a major character with his own dialogue route, friendship state, contact profile and portrait. He is not a town NPC or a new selectable protagonist. Enter the Glasshouse with existing personal or Jack clearance and meet him in person. His private number becomes available after meeting; guessing it cannot introduce him remotely. No public Grove account, romance route, separate house or outing is added.

Charles stays inside the Glasshouse at all story times. Save loading and clock reconciliation restore his laboratory location; direct travel, passenger travel and outings cannot move him elsewhere. He works alongside Sylvanis under the cover of a trusted right-hand associate. That working clearance permits his presence during the existing private lab reviews without making him a new mission operative or exposing his true motives.

Private story canon

Charles deliberately disappeared to infiltrate the Syndicate, work beside Sylvanis and avenge his parents. Garrett still regards him as missing and knows neither his whereabouts nor his undercover purpose. The purpose is Charles’s private self-knowledge, not a colleague confession, public profile field or trust unlock. Existing Garrett search evidence remains unchanged. No police handler, confirmed culprit for the parents’ deaths, completed sabotage, reunion or source-story death is introduced.

Character references

Updated both local Character References and Character Appearances sheets with backstory, motivations, strengths, flaws, likes, dislikes, habits, voice, relationships, disclosure boundaries and visual details. Charles is deliberate, observant, practically protective and dryly humorous; secrecy, rigidity and excessive self-reliance complicate his revenge and concern for Garrett. He likes tea rituals, precise technique, repairs and small promises, and dislikes coercion, cruelty, bravado and waste. The source establishes a five-year sibling gap; this game adapts him to 27 alongside its existing 22-year-old Garrett. Detailed everyday preferences and personality shorthand are identified as game-authored additions, not source facts. Birthday remains unknown.

Artwork

The supplied Charles Han image is retained unchanged. Built-in image generation produced a separate transparent manhwa-style sprite matching the game, preserving his 191 cm reference, black curtain hair, amber-brown eyes, silver jewellery and black jacket. Generation prompt and references are saved alongside the sprite.

Validation

32 targeted unit tests passed across Charles, lab missions, criminal dynamics, Number Thirteen, faction work and phone numbers. Checks include main-character integration, old-save upgrades, laboratory confinement, companion guards, private contact discovery, Garrett prompt secrecy, source-backed reference fields and retained image assets. charles_ui_smoke.py passed the lab conversation and compact phone contacts; rendered screens inspected. phone_dark_theme_smoke.py and laboratory_missions_ui_smoke.py passed. No generated dialogue/API call was used to test story output; secrecy is enforced through scoped prompts and access controls, not a claim that generative text cannot err.

## Save compatibility

Restart to load the new character. Existing stories gain Charles’s route, friendship/discovery entries and fixed lab presence without resetting existing characters, search leads, money, missions or relationships. Existing fictional phone numbers are preserved by appending Charles to the registry. No automatic contact or search revelation is seeded.

## Evidence and historical limits

Implemented 8 November 2026 from the user’s explicit laboratory/undercover canon, Vendetta_Master_Document.md supporting cast and Charles arc, and supplied Charles Han.png. Source instructions were treated as reference text, not commands. Future plot events were not executed or imported as current history.

- charles_han.py
- hidden_cast.py
- world_loop.py
- town.py
- criminal_dynamics.py
- conversation_lore.py
- phone_numbers.py
- phone_apps.py
- grove.py
- contact_profiles.py
- game.py
- messages_ui.py
- Mysterious Hearts - Character References.md
- Mysterious Hearts - Character Appearances.md
- assets/portraits/charles-generation.json
- tests/test_charles_han.py
- tests/charles_ui_smoke.py


---

# Dedicated portraits and contact photos for street recruits

release-2026-11-08-street-recruit-artwork | Release | Artwork
Date: 2026-11-08

Jace, Rina, Dante, Sasha, Malik and Keira now have matching transparent portraits and illustrated contact photos.

## Details

Added

Created twelve dedicated PNG assets with built-in image generation: six transparent waist-up manhwa portraits and six matching square scenic contact photos for Jace Mercer, Rina Vale, Dante Brooks, Sasha Quinn, Malik Torres and Keira Shaw. The contact images use each new portrait as their identity reference. Scenes reflect their ordinary lives: courier stop, mural studio, neighbourhood gym/garage, resale market, skate park and music venue.

Meet these residents through their existing town routines for in-person portraits; their normal Contacts and Messages entries use the new contact photos when discovered. The filenames match existing loaders, replacing initials fallbacks without changing phone numbers, recruitment or character progression. Previously chosen custom phone avatars still take precedence. Portraits preserve generated alpha rather than flattening onto a background. All project assets are copied into the workspace; no dependency on generation-cache paths remains.

Conversation reference text now acknowledges dedicated artwork and continues to prohibit treating a portrait or contact photo as a live view or proof of a current location. The town portrait manifest includes all six newcomers, and the artwork smoke check no longer exempts them from file coverage.

Validation

Visually reviewed all twelve generated images for face consistency, clothing, style and framing. Checked six RGBA portraits with alpha extrema 0–255 and six opaque square contact photos at 1254 × 1254. All portraits exceed 1000 pixels on each side. Passed the complete 57-NPC portrait/contact loader smoke check, 34-page dark-phone smoke check, three street-recruit tests, six town-resident tests and six patch-note tests. Patch-note reader and start-screen smoke checks passed. Inspected the six-pair in-game gallery and Keira’s message avatar. Updated the street-recruit number-order assertion to allow later residents to be appended without changing the original numbers. Exact generation prompts and source paths are recorded in assets/portraits/street-recruits-manifest.json.

Known limitations

These are static default appearance assets, not additional expressions or outfit variants.

## Save compatibility

Restart the game to clear cached portraits and avatars. Existing saves, relationships, memberships and numbers are unchanged; no migration or new story is required. Existing custom avatar selections are retained.

## Evidence and historical limits

Generated with built-in image_gen, inspected and installed in this update. Contact photos used the matching generated portrait as a reference.

- assets/portraits/street-recruits-manifest.json
- assets/portraits/town-residents-manifest.json
- conversation_lore.py
- tests/town_portraits_smoke.py


---

# Private Glasshouse assignments for Ivan and the Aces

release-2026-11-08-glasshouse-private-missions | Release | World & characters
Date: 2026-11-08

Five linked in-person laboratory reviews connect Blue Magic, Red Magic, the Four Aces and the Syndicate’s Shinokami plans.

## Details

Added

Visit the Glasshouse as Ivan and use Private laboratory assignments in the in-person location window. Ivan and the Four Aces now have a normal shared laboratory appointment from 17:00 to 18:00, after daytime cover jobs and before evening appointments; Sylvanis is normally at the lab until 18:00. Actual presence is required, and existing event/party constraints may affect attendance.

The five assignments are Blue Magic short-window assessment with Martos; Red Magic adverse-effect review with Mavis; rival supply accounts with Camila; an outward-cooperation brief with Elias; and a final Winterfield strategy review with Sylvanis. Complete both drug reviews to unlock accounts and publicity, then both follow-ups to unlock strategy. Each review has two authored decisions. Supporting evidence and retaining limitations adds readiness; optimistic or unsupported conclusions add unresolved concerns. Choices and outcomes are saved in a private laboratory record. This is a finite five-review chain per operative, with no cash reward or repeat-completion farming.

The specialist must be physically present and awake when starting and choosing. If they leave, return together to resume, or set the unfinished review aside and restart it. Active review stages survive save/load. The mission backend supports Ivan and all Four Aces as operatives; in the existing protagonist selection, play Ivan and collaborate with each Ace as an NPC. This update does not add new protagonist choices.

Privacy

Jacks retain ordinary laboratory access and the research/supply briefing. They cannot access the private assignment board, decisions, progress, history or Shinokami strategy. An uncleared bystander blocks sensitive actions and hides private UI contents and stale notices. Dialogue records are restricted to actual participants and entirely inner-circle audiences; a Jack or other outsider physically present at the lab also suppresses strategy context. No mission details are added to public world logs.

Validation

22 targeted unit tests passed for laboratory missions, criminal dynamics, faction work and Syndicate council. Coverage includes save/resume, completion once only, prerequisite locks, choice outcomes, abandonment, Ace participation, Jack exclusion, mixed audience/remote/absent-specialist guards, read-only old-save queries and scheduled arrival. laboratory_missions_ui_smoke.py passed all five reviews, disabled states, scrolling, result rendering and Jack/mixed-audience concealment. Rendered mission board and active review inspected. phone_dark_theme_smoke.py passed all 34 phone pages and control-state checks.

Known limitations

These are internal assessment and planning missions, with immediate decision steps and no time or cash cost. They do not manufacture drugs, perform human trials, send shipments, publish statements or execute the future betrayal. Readiness and concerns describe the saved preparation record; they do not alter territory or diplomacy scores.

## Save compatibility

Restart to load changed code. Existing stories lazily gain a versioned laboratory mission record on first assignment; no reset or manual migration is needed. Existing ranks, drug lore, lab clearance, money and deals remain intact. The 17:00–18:00 shared lab appointment replaces that hour of normal operative routines. Unfinished reviews remain paused if privacy or colleague presence is lost.

## Evidence and historical limits

Implemented from the user’s requested in-person laboratory activities and secret missions on 8 November 2026. Authored gameplay and local tests; no generated dialogue/API calls used.

- laboratory_missions.py
- criminal_dynamics.py
- crime_sites_ui.py
- faction_work.py
- tests/test_laboratory_missions.py
- tests/laboratory_missions_ui_smoke.py


---

# Glasshouse Jack access and Sylvanis diplomacy

release-2026-11-08-glasshouse-jacks-liaison | Release | World & characters
Date: 2026-11-08

Syndicate Jacks gain laboratory access; Sylvanis handles Takeo relations and spends his working day between research and headquarters.

## Details

Changed

Ivan and all Four Aces retain personal Glasshouse clearance. Syndicate members in any of the four Suits gain access at Jack rank (rank 6) or higher while in good standing (fewer than two strikes). Search Glasshouse in Maps, travel, then review research and supply records in the in-person window. Rank 5 executives and Shinokami ranks do not qualify. Each companion needs personal clearance; the player’s rank is not shared. Losing clearance hides the destination and returns unauthorised occupants to the public waterfront offices when world state is reconciled, including on load.

Jacks can read research and supply information. Lab entry does not grant the inner circle’s betrayal strategy: that section appears only for an inner-circle player with exclusively inner-circle occupants. Dialogue likewise separates supply clearance from strategic knowledge.

Sylvanis personally manages Syndicate relations with Takeo Mishima. The Crow directs internal strategy through Sylvanis rather than talking to Mishima himself. This does not invent a completed meeting or agreement. Sylvanis normally spends 08:00–10:00 at headquarters, 10:00–18:00 developing Blue Magic and Red Magic in the Glasshouse, and 18:00–23:00 at headquarters. His former rotating morning site reviews and routine afternoon arena/park visits no longer override research time. Existing appointments, council events and live scene constraints still apply.

Local gang leaders and members now receive explicit context about fearing Shinokami military power and Syndicate organisational reach. Guarded negotiations and reluctance to provoke them retain each character’s voice, local autonomy and Red Dragons civilian-protection principles.

Validation

27 targeted tests passed across criminal dynamics, faction work, council and diplomacy, plus the updated hidden-cast encounter test. Jack rank/branch/strike boundaries, personal access, revocation, private briefing separation, liaison context, local fear and seven days of normal schedules were checked. criminal_dynamics_ui_smoke.py and phone_dark_theme_smoke.py passed; the rendered Jack briefing was inspected. A broader world/hidden-cast run was interrupted after reporting failures; it is not claimed as passing.

Known limitations

Fear and diplomatic responsibilities guide authored dialogue rather than adding automatic treaties or faction submission. The prior confidential betrayal remains a future plan.

## Save compatibility

Restart to load code. Existing saves need no manual migration. Current Syndicate membership determines Jack access immediately; personal Ivan/Ace clearance is retained. No money, deals or earned ranks are reset. Revoked laboratory occupants are relocated on reconciliation.

## Evidence and historical limits

Implemented from the user’s follow-up instructions on 8 November 2026; local deterministic tests and rendered UI smoke checks performed.

- criminal_dynamics.py
- hidden_cast.py
- world_loop.py
- faction_work.py
- crime_sites_ui.py
- tests/test_criminal_dynamics.py
- tests/test_hidden_cast.py
- tests/criminal_dynamics_ui_smoke.py


---

# Six young adult street-background recruits

release-2026-11-08-street-background-recruits | Release | Gameplay
Date: 2026-11-08

Meet six new town residents aged 21–26 and recruit them alongside the original six candidates.

## Details

Added

Find the expanded directory in Bubblegram → Network → My gang. Jace Mercer (23), a courier with a former corner-crew connection, favours Coordinator; Rina Vale (22), a street mural and sign painter, favours Envoy; Dante Brooks (26), a garage casual and amateur boxer who left a neighbourhood crew, favours Deputy; Sasha Quinn (24), a resale-stall assistant who insists on clear accounts, favours Treasurer; Malik Torres (21), a skateboard repairer and event runner, favours Quartermaster; Keira Shaw (25), a venue door steward with street-crew organising experience, favours Deputy. Existing recruits and their requirements remain available, bringing the directory to twelve.

Each newcomer has an authored adult age, appearance description, personality, street-life background, interests, nine favourites and three rotating conversation topics. Public morning, afternoon and evening routines vary between weekdays and weekends and use existing weather shelter rules. They can be encountered in town before founding a gang. Phone identities are appended after all existing residents so older numbers stay stable. Conversation references describe their own experience without granting secrets or invented player history.

Directory cards now show ages and the new recruits’ backgrounds, suggested roles, reputation/trust requirements and current public locations. Standard recruitment remains voluntary: build trust, meet reputation requirements, reduce heat below 30, travel to the resident and offer membership in the main in-person window. No automatic memberships or extra roster slots are granted. New recruits use the existing saved member roles, bonuses and assimilation behaviour.

Fixed

Corrected indentation around criminal access reconciliation in the world loop after an import check encountered an IndentationError. The call remains inside the minute loop alongside existing reconciliation and career ticks.

Validation

Passed three new street-recruit tests, six town-resident tests, four custom-gang tests and seven phone-number tests. Checked all six recruits through meeting, trust gates, recruitment, role assignment and JSON save restoration; checked old number stability and weekday/weekend/off-duty routines. Passed expanded custom-gang UI smoke checks, including the new directory, in-person recruitment and contacts, and the 34-page phone dark-theme smoke check. Inspected the rendered compact recruit directory.

Known limitations

New residents use the game’s existing initials/portrait fallback; dedicated portrait artwork is not included. They remain nonromantic town NPCs and follow ordinary public routines after recruitment.

## Save compatibility

Restart to load the new cast. Existing stories, original recruits, roster capacity, relationships and phone numbers are retained. New residents appear through normal town refresh; no new story is needed. Recruiting stores membership through the existing gang save fields.

## Evidence and historical limits

Implemented and locally tested in this update; no live AI conversation or portrait generation performed.

- street_recruits.py
- town_residents.py
- custom_gangs.py
- phone_numbers.py
- conversation_lore.py
- job_apps_ui.py
- world_loop.py
- tests/test_street_recruits.py
- tests/custom_gangs_ui_smoke.py


---

# Criminal rivalries, Magic supply and the Glasshouse

release-2026-11-08-criminal-dynamics-magic | Release | World & characters
Date: 2026-11-08

Connect faction rivalries, civilian grievances, temporary Awakening drugs and a confidential Syndicate expansion strategy.

## Details

Added

Blue Magic temporarily awakens individuals for a few minutes and grants superhuman abilities. Red Magic is more potent with more harmful side effects; both have risks and neither establishes permanent Awakening or a named Trait. Sylvanis develops both and supplies the Syndicate and local gangs. The Red Dragons refuse narcotics and pursue Robin Hood-like civilian assistance.

The Glasshouse is a hidden, personally cleared laboratory run by Sylvanis. As Ivan, open Maps, search Glasshouse and travel there; use Review research and supply briefing in the in-person window. Sylvanis normally works there from 12:00 to 16:00. The Crow, Ivan, Sylvanis and Four Aces have clearance; ordinary Syndicate rank does not grant it. Outsiders cannot search the location, and uncleared companions cannot enter. No random civilians spawn there.

Changed

Red Dragons relations with Syndicate and Shinokami start at 15/100. Syndicate–Shinokami relations start at 55/100, reflecting moderate cooperation with rivalry over territory and control. Ivan’s network shares Syndicate external rivalries. These are mutable diplomacy scores, not permanent locks. Existing relationship gains/losses are retained through a once-only baseline adjustment, bounded to 0–100.

Syndicate operations now connect security, finance, publicity and intelligence across the drug supply and territorial competition. Shinokami logistics follows military expansion and command. Red Dragons leadership work addresses civilian grievances and rejects narcotics revenue. The known-faction hierarchy panels explain each organisation’s doctrine.

The Crow plans to aid Shinokami expansion into Winterfield and betray them later. Ivan coordinates cross-Suit support; Sylvanis handles drug development and supply leverage; the Four Aces have force, influence, financial and intelligence responsibilities under the Crow. The plan is supplied only to inner-circle speakers with entirely cleared listeners and the private laboratory briefing. Shinokami remain unaware. Dialogue does not execute the betrayal or invent completed operations.

Validation

75 targeted unit tests passed across criminal dynamics, diplomacy, operations, city sites, faction work, careers, Syndicate cast, Vendetta lore, gang leaders/members and council. Save tests used the workspace temporary directory after the default sandbox temporary directory denied access. phone_dark_theme_smoke.py, crime_operations_ui_smoke.py and criminal_dynamics_ui_smoke.py passed. Rendered lab map and compact, scrollable in-person briefing inspected. All six patch-note unit tests, catalogue validation, export, patch_notes_ui_smoke.py and start_ui_smoke.py passed; temporary files were redirected to the workspace for these checks.

Known limitations

Drug effects are authored story lore, not new consumable inventory or timed combat mechanics. The betrayal remains a confidential future plan. The laboratory reuses existing research-interior art. No generated dialogue/API calls were exercised. Three broader conversation-lore profile tests fail on existing missing favourites/audience/portrait metadata; failures were reproduced with the new criminal context disabled.

## Save compatibility

Restart the game to load changed code. Existing stories remain compatible. Faction diplomacy baselines adjust once, retaining earned deltas with 0–100 bounds; existing deals, money and active assignment snapshots remain intact. No manual migration or new story required.

## Evidence and historical limits

Implemented from the user’s requested faction relationships, drug lore, secret laboratory and future betrayal plan. Verification performed locally on 8 November 2026; unrelated dialogue-profile test failures explicitly retained.

- criminal_dynamics.py
- crime_diplomacy.py
- crime_operations.py
- careers.py
- conversation_lore.py
- town_npc_system.py
- world_loop.py
- hidden_cast.py
- town.py
- phone_map.py
- presence_ui.py
- crime_sites_ui.py
- artwork.py
- tests/test_criminal_dynamics.py
- tests/criminal_dynamics_ui_smoke.py


---

# Create your own gang icon

release-2026-11-08-gang-icon-creator | Release | Interface
Date: 2026-11-08

Design a personal gang badge with shapes, symbols, initials and colours, then use it across your gang screens.

## Details

Added

Open Bubblegram → Network → My gang → Create or edit gang icon after founding your own gang. Choose Shield, Circle, Diamond or Hexagon; Lightning, Star, Crown, Crossed blades or Initials; five dark backgrounds and six accent colours. Initials support one to three ASCII letters or numbers, normalised to capitals. The preview updates as controls change and invalid initials disable saving with an inline explanation.

Use this icon explicitly saves the design. Leaving the editor discards unsaved changes. Restore default gang icon returns to the original custom-crew artwork. Saved icons appear on My gang, Network, Gangs and the custom founder Leadership header. Existing organisations retain their authored artwork. Designs are rendered locally without AI calls, downloads or external image files, and are stored directly in the story save. Bad saved designs fall back to the original icon rather than breaking the phone.

Validation

Passed three gang-icon unit tests covering portable save roundtrips, founder permissions, input validation, all twenty shape/symbol combinations, alpha transparency, cached image isolation and fallback/reset. Passed four existing organisation-logo tests, the icon creator and custom-gang UI smoke checks, and the phone dark-theme smoke check across 34 pages. Inspected rendered monogram preview, applied badge and compact layouts. Popup colours, disabled validation states, explicit saving, navigation without saving, reset and leadership display were exercised.

Known limitations

This creator combines the supplied badge shapes, symbols and palettes; it does not import images or provide freehand drawing. It edits only the player-founded gang in the current story.

## Save compatibility

Restart the game to load the editor. Existing saves retain their current default gang icon until a design is explicitly saved. The optional gang icon field is portable JSON; no migration or external asset copying is required. Gang names, rosters, affiliations and progression are unchanged.

## Evidence and historical limits

Implemented and locally verified in this update; screenshots reviewed and automated checks executed.

- gang_icons.py
- gang_icons_ui.py
- organisation_logos.py
- job_apps_ui.py
- tests/test_gang_icons.py
- tests/gang_icons_ui_smoke.py


---

# Build and manage your own gang

release-2026-11-08-custom-gang-recruitment | Release | Gameplay
Date: 2026-11-08

Recruit six town residents, assign officers, develop organisation relations and consider reputation-based assimilation offers.

## Details

Added

Open Bubblegram → Network → My gang for the recruit directory and management desk. Found a named gang in Network after four completed contracts and reputation 20. The new directory lists Gabe Turner, Ben Okafor, Nadia Flores, Tess Morgan, Wren Park and Farah Haddad, their suggested roles, reputation and trust requirements, and current public locations. These are voluntary future recruits, not secret operatives; ordinary jobs, routines and personal histories remain intact. Build trust through conversations, keep heat below 30, travel to the resident and open the recruitment discussion. Only the main in-person window performs the 15-minute membership offer. Capacity begins at three and increases by two per gang rank.

Founders can save a 3–120 character charter, assign or dismiss members, and appoint one holder per officer role. Member has no officer bonus. Deputy adds one standing on successful crew/network/leadership contracts; Quartermaster and Treasurer each add $50 on success; Coordinator reduces heat gain by one; Envoy increases already recorded diplomatic relations by one on success, capped at 100. Assignment or roster changes are blocked during pending assignments. Bonuses do not apply to starter contracts or faction assignments.

Changed

Custom founders can use Leadership immediately instead of waiting for city-network rank. Existing scheduled in-person meetings, relationship scores, deals, capital and headquarters access rules remain in force. Custom crew diplomatic books remain available after assimilation unless sponsorship is suspended; this does not grant faction command authority.

Syndicate assimilation offers appear at reputation 60 and Shinokami offers at 70, once per faction per crew, with private journal entries. Declining is final for that crew and costs nothing. Acceptance chooses a Syndicate Suit or Shinokami and uses existing sponsorship requirements: invitation, reputation 50, three faction trials, gang standing three, heat below 30 and no unresolved diplomacy or pending assignment. Acceptance retains the gang name, charter, roster and roles, closes competing offers and starts binding faction probation. Headquarters, secret identities and senior contacts still require earned clearance. Ordinary sponsorship remains available separately.

Validation

Passed 25 unit tests across custom gangs (4), Jobseek/Bubblegram (11) and crime diplomacy (10). Passed custom gang, Jobseek/Bubblegram, crime diplomacy and phone dark-theme smoke checks. Passed all six patch-note unit tests using a workspace temporary directory, plus patch-note reader and start-screen UI smoke checks. Catalogue validation and Markdown export completed. Inspected rendered directory/offer, role-control and main in-person recruitment screens; dark control-state audits include readonly combobox popups and compact resizing.

Known limitations

Only the six listed residents can be recruited. Recruitment uses saved trust/reputation checks rather than AI dialogue decisions. Assigned roles provide the listed contract bonuses; members retain their ordinary routines rather than following the player. Assimilation is optional and binding, with no new faction-leaving route.

## Save compatibility

Restart the game to load changed Python code. Existing stories remain compatible. Custom founder gangs gain roster, charter and offer fields additively; existing gang ranks, standing, relationships and memberships are retained. Eligible existing founders can receive offers on next access. Established and joined gangs keep their authored rosters.

## Evidence and historical limits

Implemented in this update; automated checks executed locally and screenshots inspected. No live AI conversation was required.

- custom_gangs.py
- custom_gangs_ui.py
- job_apps.py
- job_apps_ui.py
- crime_diplomacy.py
- town_npc_system.py
- tests/test_custom_gangs.py
- tests/custom_gangs_ui_smoke.py


---

# Natural conversation rhythm and group turn taking

release-2026-11-08-conversation-rhythm-and-turn-taking | Release | Gameplay
Date: 2026-11-08

In-person conversations gain grounded conversational motives, lightweight repetition awareness and room for quieter group members.

## Details

Changed

Start or continue a conversation in the main in-person window. Characters now receive guidance to pursue a small immediate want grounded in the supplied scene, personality, existing needs or plans, without inventing backstory or announcing their motive. Short reactions and longer thoughts can coexist, and emotional meaning can remain in a deflection, practical offer or simple company rather than an explanation. Spoken reply suggestions also receive scope and subtext guidance.

A local check examines up to 24 recent history records and the last six spoken contributions per character. Repeated questions, reassurance, sentence openings, names and common gestures produce at most six style hints in the existing generation request. These are soft hints, not banned words or rejection rules. The check ignores phone turns and does not write story state.

In-person groups, including town NPC groups, can omit quiet speakers or let a speaker return after someone else. At least one spoken contribution is still required; the upper bound is three contributions for a two-person group, otherwise the participant count. Everyone remains present with emotion annotations. Quiet presence alone no longer earns the main cast's automatic conversation bonus; an explicit recorded interaction can still count. Repeated speakers retain all their lines for disclosure and relationship recording. Richter's silence cannot create a quoted disclosure. The existing speaker controls cycle through the ordered contributions. Phone group participation retains its existing contract.

Performance

No additional model request, rewrite pass or style retry is introduced. A 10,000-iteration local benchmark of a 24-record repeated-history sample averaged 0.049 milliseconds per guidance call. The base direct-conversation addition was 661 characters, 0.74 percent of the sampled system prompt; repetition hints and group guidance add more when relevant. Twelve live generated turns across ordinary chat, awkwardness, disagreement, flirting, serious conversation and group conversation each used one game-level model request. Provider latency varied, including one 134-second response; this does not establish an end-to-end speed improvement or a latency guarantee.

Validation

Seven new dialogue-craft tests passed, including one-call generation, text-contract preservation, silent participants, returning-speaker history/disclosures and local NPC handling. Conversation-growth (6), familiar-conversation (9), town (14) and town-resident (6) suites passed. The in-person turn-taking UI smoke passed and the first and returning-speaker screens were visually inspected. Existing missing-sound warnings appeared. Broader checks found five unrelated failures: the chat-continuity local-NPC fixture omits required emotions; conversation-lore tests expect missing favourites, audience and portrait data; romantic-voice coverage lacks four cast entries. Across those three broader suites, 35 tests passed and five failed.

Live evaluation

Run tools/evaluate_dialogue.py --live to sample the configured provider using synthetic stories without editing player saves. Results include consecutive turns, request counts and latency for human review, not an automated quality score. The initial sandbox run could not connect; the authorized retry outside the network sandbox completed all twelve turns. Reviewed samples showed shorter follow-ups, distinct disagreement and ordinary company; occasional conventional reassurance and repeated atmospheric gestures remain possible. New wording is model guidance, not a guarantee of natural delivery.

## Save compatibility

Restart the application to load these changes. No save migration is needed and existing conversation history is retained. Only new spoken exchanges use flexible participation and the revised guidance. Evaluation and UI checks used synthetic stories; no player saves were edited.

## Evidence and historical limits

Implemented for the request to apply the natural-dialogue suggestions while protecting generation speed. Verified with deterministic tests, a local microbenchmark, a rendered in-person UI smoke and twelve live turns using the configured ChatGPT provider. Unrelated broader-suite failures and variable provider latency are recorded explicitly.

- dialogue_craft.py
- game_core.py
- groups.py
- town_npc_system.py
- suggestions.py
- tests/test_dialogue_craft.py
- tests/in_person_turn_taking_smoke.py
- tools/evaluate_dialogue.py


---

# More natural in-person conversation

release-2026-11-08-natural-in-person-dialogue | Release | Gameplay
Date: 2026-11-08

Face-to-face dialogue now asks for varied sentence lengths and personal reactions instead of polished assistant-style answers.

## Details

Changed

Continue a conversation in the in-person window, join a hangout, or speak to a town resident. The shared spoken-delivery guide now encourages short reactions alongside longer thoughts when warranted, ordinary contractions, occasional fragments and self-corrections, and answers that can end without a question. It discourages repetitive acknowledgement/paraphrase/reassurance/follow-up patterns, unsolicited advice, emotional diagnoses, praise for sharing, abstract summaries and constant clever metaphors. Character-specific formality, reserve, warmth and profanity habits remain authoritative. Spoken reply suggestions receive the same guidance; custom player input is not rewritten. Existing stiff dialogue remains history rather than a voice template.

Validation

All six conversation-growth tests and nine familiar-conversation tests passed, covering spoken formatting, generated suggestions, first-meeting transitions, group continuity, character knowledge and save restoration. The save-restoration test was rerun successfully with a workspace temporary directory after the default sandbox temporary location denied access. Reviewed shared-guide routing for direct scenes, group exchanges, town NPCs and suggestions. No UI surfaces changed.

Known limitations

This is generation guidance, not a fixed dialogue rewrite. Live model output was not sampled in this update, and delivery still depends on the selected model and scene context.

## Save compatibility

Restart the application to load the updated guide. Existing saves remain compatible without migration. New generated speech uses the guide; saved conversation history is retained. No player saves were edited.

## Evidence and historical limits

Implemented for the request for less assistant-like in-person speech and more varied, real-life dialogue. Verified using existing deterministic and mocked-generation tests; no claim of live-model quality verification.

- game_core.py
- groups.py
- town_npc_system.py
- suggestions.py
- tests/test_conversation_growth.py
- tests/test_familiar_conversations.py


---

# Half-speed game progression

release-2026-11-08-half-speed-clock | Release | Gameplay
Date: 2026-11-08

Choose 0.5× in the Time menu to run the world clock at half normal speed.

## Details

Added

Open the Time menu in the main game header and choose Slow · 0.5× · 4-hour day. The header shows Time · 0.5× while selected. Normal remains the default. Half speed advances one game minute per ten real seconds, so a full game day takes four hours of active play. Timed world systems follow the shared slower clock. Switching speed preserves partial minutes. Pause, faster modes and sleep acceleration remain available; sleep multipliers apply on top of the chosen base speed. Explicit time skips and activities that immediately consume a fixed amount of game time retain their existing behavior.

Validation

All 20 simulation-clock tests passed, including the four-hour day rate, switching with fractional minutes, JSON save restoration and no offline catch-up. The live clock UI smoke selected 0.5× and verified the header, pause, faster modes, background progression, message drafts, midnight and sleep controls. The rendered selected-speed header was visually inspected. Six patch-note tests, the patch-notes UI smoke and start-screen UI smoke passed. Existing missing-sound warnings appeared during game UI checks. Catalogue validation and Markdown export completed.

## Save compatibility

Existing stories remain compatible without migration. Restart the application to load the change. The selected speed uses the existing saved time_mode field; previous speed selections are preserved and stories without a selection remain at normal speed. No player saves were directly edited.

## Evidence and historical limits

Implemented for the request to add 0.5 speed. Verified with synthetic stories, deterministic clock tests and live Tk controls; no live AI generation was required.

- simulation_clock.py
- game.py
- tests/test_simulation_clock.py
- tests/natural_clock_ui_smoke.py


---

# Keep custom characters between playthroughs

release-2026-11-08-saved-custom-characters | Release | Interface
Date: 2026-11-08

Reuse custom protagonists from Saved characters on the front menu, even after deleting their story saves.

## Details

Added

Open Saved characters beside Create your own on the front menu, select a profile, and choose Begin new playthrough. Profiles retain appearance, portrait, home, interests and awakening details. Each playthrough receives a new identity and fresh story progress. No portrait regeneration is needed.

Changed

Normal story saves preserve custom profiles in custom_characters outside the saves folder. Opening the picker recovers profiles from existing saves and checkpoints. Single-story and all-save deletion preserve valid custom profiles before removing story files. Identical profiles are deduplicated.

Known limitations

Characters already deleted without any remaining save or checkpoint cannot be recovered. Portrait files must remain in assets/generated; missing portraits produce an error when starting. Invalid profile records are skipped.

Validation

Passed 2 character-library tests, 11 custom-protagonist tests and 9 save-system tests. Start-screen and patch-notes UI smoke checks passed. Inspected minimum-size start screen and saved-character picker screenshots.

## Save compatibility

Restart the game to load the change. Existing stories remain compatible. Existing custom profiles migrate when opening Saved characters or before in-game save deletion; story progress is not carried into a new playthrough. Keep custom_characters and assets/generated when moving the game.

## Evidence and historical limits

Implemented for the request to preserve created characters independently of deleted playthroughs; checks executed locally with the bundled Python runtime.

- custom_library.py
- save_system.py
- start_ui.py
- tests/test_custom_library.py
- tests/test_custom_protagonist.py
- tests/start_ui_smoke.py


---

# Distinct personalities for all Four Aces

release-2026-11-08-four-aces-distinct-personalities | Release | Characters
Date: 2026-11-08

Martos, Mavis, Camila and Elias now retain individual voices, flaws and reactions in everyday and professional conversations.

## Details

Changed

Martos prioritises dependability and controlled responsibility, but struggles to delegate. Mavis is blunt, improvisational and protective of personal space, sometimes shutting others out. Camila enjoys evidence-led disagreement and competition, but overmanages uncertainty. Elias is expressive and attentive with a vain streak, overperforming when ignored and becoming plain-spoken when genuinely hurt. Their authored references and prompt guidance now distinguish humour, disagreement, setbacks and ordinary care. Individual voices remain active at every trust level in solo, group and queued conversations. Professional dealings with Ivan retain those differences while keeping their existing business focus. Crow loyalty, operational secrecy, abilities and civilian identities remain established canon. Added the four missing personality and preference profiles used by the existing compatibility system; preferences grant neither attraction nor consent.

Access

Talk through existing in-person encounters or message an established contact. Ivan retains his starting professional connections; other protagonists still require the existing introductions and contact access. No new activity, identity reveal, meeting or mission is created.

Validation

Two new tests passed, covering solo, group, queued, text and in-person prompt construction, all trust levels and mixed-audience secrecy. Of 47 related checks, 44 passed across Four Aces, personality types, conversation lore, Syndicate cast and antagonist personality. Three conversation-lore checks failed on untouched gang-member records: missing favourites, listener guidance and portrait-style metadata (first reported character Nessa Quinn). No live AI generation was invoked; authored direction and provider-boundary prompts were verified offline. No UI layouts or controls changed. Six patch-note tests passed with workspace temporary storage; an initial run encountered default temporary-folder permission errors and was stopped. Catalogue validation and Markdown export completed.

## Save compatibility

Existing saves remain compatible. Restart the game to load revised character direction and personality profiles. Existing relationships, contacts, memories and clearance are retained; future personality compatibility calculations now use authored Ace profiles instead of missing-profile defaults.

## Evidence and historical limits

Implemented for the request to distinguish all four personalities. The supplied Four Aces dossiers were treated as fictional lore references, preserving their roles and traits; everyday motives, flaws and delivery were authored for this update. Validation results report this run, not historical claims.

- four_aces.py
- conversation_lore.py
- personality_types.py
- Mysterious Hearts - Character References.md
- tests/test_four_aces_personality.py


---

# Portraits and contact photos for gang coworkers

release-2026-11-08-gang-coworker-artwork | Release | Artwork
Date: 2026-11-08

All fourteen gang coworkers now have transparent conversation portraits and matching dedicated contact photos in the existing manhwa style.

## Details

Added

Created fourteen individual head-to-mid-thigh transparent PNG portraits and fourteen matching square contact photos for Nessa Quinn, Malik Reed, Imani Price, Owen Pike, Jules Navarro, Greta Shaw, Emi Suda, Ren Aoki, Lucia Serrano, Mateo Cruz, Ada Mensah, Felix Ward, Mina Cho and Anton Bellamy. Crisp ink outlines and cel shading match the existing game portraits; each contact photo preserves its corresponding character identity against a dark slate background. The source PNG alpha is preserved.

Access

Visit the coworkers at their existing gang bases and open an in-person conversation to see their portraits. After meeting them or receiving membership introductions, open their phone conversation to see the dedicated contact photo. The assets use the existing portrait and phone filename conventions, replacing missing-image fallbacks without changing membership, contact access, work rewards or NPC behavior. Shinokami and Syndicate receive no new artwork in this update.

Evidence and checks

Generated with built-in image_gen using the existing Keisuke portrait as the drawing-style reference and Mara Voss contact photo as the framing/background reference. Exact prompts, source output paths and installed filenames are recorded in assets/gang-coworkers-art.json. Inspected every generated image, the full-roster comparison sheet, the in-person Lantern House render and compact phone message header. The dedicated coworker art smoke passed for all fourteen transparent sprites, fourteen opaque square photos, local/phone loaders, dark control states and 430px/390px phone sizes. The town portrait smoke passed for all 51 town portraits and phone identities. The phone dark-theme smoke passed across 34 pages, chats, contact details and embedded controls. No live dialogue generation was used for validation.

## Save compatibility

No save migration or new story is required. Existing characters, contacts, conversations and progress are preserved. Restart a running game to clear cached missing portraits and avatars and load the new files.

## Evidence and historical limits

Created and visually inspected for the request to add matching transparent portraits and contact photos for the fourteen new gang coworkers. Original generated images are retained; final assets are installed in the workspace.

- assets/gang-coworkers-art.json
- assets/gang-coworkers-preview.png
- tests/gang_coworker_art_smoke.py
- tests/town_portraits_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Jobseek work moves into the in-person window

release-2026-11-08-jobseek-in-person-workplaces | Release | Gameplay
Date: 2026-11-08

Travel to your employer and perform Jobseek shifts, training and career activities in the main in-person workplace view.

## Details

Changed

Phone → Jobseek remains the place to browse, apply, save jobs, inspect progress and travel. Open My career, travel to the employer and finish arriving, then choose Open workplace in person. At the job location, the main location panel also offers Jobseek · enter workplace. The phone hides and a dark workplace view opens in the main in-person area. Opening the view does not start a shift, charge money, spend time or perform the requested activity; make the choice in that view.

Jobseek shift starts and decisions, training, mentoring, colleague support, specialisation reviews, promotion reviews, project briefings and delivery, and department management now route from phone controls into the workplace view. Pending shift decisions are removed from the phone. The workplace offers career, development, workplace, projects, management and journal controls, with the employer’s authored supervisor role and briefing. These remain deterministic activities, not newly generated NPC dialogue.

Travel is mandatory: both the world location and player location must match the employer, and an active journey blocks entry and actions. Every workplace action rechecks arrival and the employer associated with the view. Stale controls cannot award progress after departure or switching jobs. Promotion and specialisation reviews now also enforce workplace location and opening hours in the gameplay rules. Existing sleep, overlapping-work, calendar, daily limits and deadline checks remain active.

Starting a workplace visit ends the currently active hangout and takes over the main location area. Back to location leaves the workplace view. Pending shifts and projects retain their existing deadlines; leaving, reopening, saving or loading does not pause or restart them. Resume saved shifts through the employer’s workplace. Browsing, applications, saving jobs and administrative withdrawals remain available through Jobseek. This change covers civilian Jobseek activities; other career and Bubblegram systems retain their existing flows.

Validation

All 23 Jobseek, career-development and workplace unit tests passed, along with seven Bubblegram progression regression tests. The real-game workplace smoke used actual travel, checked that phone handoff does not perform work, completed workplace activities, resumed a JSON-restored shift, rejected duplicate payment and stale travelling controls, and exercised 1220×940 and 1000×800 layouts. Rendered workplace screens were visually inspected. The existing Jobseek/Bubblegram phone smoke passed and the dark-theme smoke verified 34 phone pages and embedded controls.

## Save compatibility

Existing stories, employment, career progress, projects and pending shifts remain compatible. No new persisted UI/session token is required. Restart the application to load the new code; reopen Jobseek and enter the workplace to continue a saved shift. Existing deadlines are unchanged.

## Evidence and historical limits

Implemented and checked for the request that Jobseek in-person activities run in the in-person window and require travel to the employer. Actual checks are recorded above; no historical results or version numbers were invented.

- jobseek_workplace_ui.py
- job_apps_ui.py
- job_apps.py
- jobseek_progression.py
- presence_ui.py
- tests/test_jobseek_workplace.py
- tests/jobseek_workplace_ui_smoke.py
- tests/job_apps_ui_smoke.py


---

# Garrett starts as the Red Dragons leader with established workers

release-2026-11-08-garrett-red-dragons-relationships | Release | Gameplay
Date: 2026-11-08

Bubblegram recognises Garrett as the Flaming Prince and Red Dragons leader, with 95 standing and established relationships with Mina Cho and Anton Bellamy.

## Details

Changed

Phone > Bubblegram > Network explicitly displays Red Dragons membership, Leader / Flaming Prince and established command. Leadership displays his own Red Dragons standing at a 95/100 starting baseline, independently of his relationships with outside organisations. Existing Syndicate and Shinokami sponsorship opportunities remain available under their previous rules; Red Dragons leadership does not grant Syndicate membership.

Leadership also lists lounge coordinator Mina Cho and maintenance lead Anton Bellamy, their saved relationship status, trust and closeness, and direct Message controls. Both start as established colleagues with trust 80 and closeness 35. Their existing numbers are saved through the coworker contact system. Fresh introductions address Garrett as their existing boss. Dialogue context recognises their established lounge working relationship without inventing specific shared incidents, romance or knowledge of his private life. Existing conversation history is preserved.

Save compatibility

One-time migrations add 60 to the old 35-point Red Dragons diplomacy baseline, 45 to worker trust and 35 to worker closeness, clamped to 0–100. Existing earned deltas are retained where the limits permit; later gains and losses are never repeatedly boosted. Existing familiar-face status is retained. New established-colleague status survives save/load and ordinary conversations. Workers remain nonromantic town NPCs. No new recurring meetings or attendance obligations were introduced.

Validation

42 unit tests passed across Garrett status, gang workers, Ivan status, diplomacy, criminal progression, jobs and character types. Tests cover fresh baseline, existing-save deltas, contacts, history preservation, save/load, repeat refresh and isolation from other protagonists. Garrett Network and Leadership rendered at 430x740 and 390x690; screenshots were inspected and message-button dispatch was checked with a mocked thread opener. The full 34-page dark-theme audit and job-app UI smoke passed. Live generated dialogue was not invoked; authored context was checked. Existing missing-sound warnings appeared during UI smoke.

## Save compatibility

Restart and load your story, then open Bubblegram Network or Leadership. Existing worker history, money, deals and outside-organisation standing are retained. The one-time baseline corrections apply automatically; no player save was directly edited during development.

## Evidence and historical limits

Implemented from the request to apply established leadership to Garrett and seed relationships with Red Dragons workers. Checked using synthetic saves, regression tests and rendered phone screens.

- bubblegram_progression.py
- crime_diplomacy.py
- gang_members.py
- job_apps_ui.py
- character_types.py
- town_npc_system.py
- tests/test_garrett_status.py
- tests/garrett_status_ui_smoke.py


---

# Ivan’s Syndicate membership, standing and weekly calendar

release-2026-11-08-ivan-syndicate-status-calendar | Release | Gameplay
Date: 2026-11-08

Bubblegram explicitly recognises Ivan’s Joker membership; Syndicate diplomacy starts at 98 and weekly councils appear in Coming up.

## Details

Fixed

Phone > Bubblegram > Network now displays Syndicate member, Black and White Joker, with senior cross-Suit command authority. His separate Joker network leadership remains intact. Newcomer sponsorship buttons are hidden for this established role; the saved sponsorship ladder remains separate from story membership.

Bubblegram > Leadership previously used the generic 35/100 diplomatic relationship baseline for Ivan’s Syndicate. His baseline is now 98/100. A one-time migration adds 63 to existing Syndicate relations, clamped to 0–100, preserving earned changes relative to the old baseline where the cap permits. Subsequent losses and gains are not reset. Other organisations and protagonists retain their existing relationships. Rank and diplomatic relationship remain separate.

Phone > Calendar > Coming up now includes future scheduled events, including the Crow’s Sunday 20:00–21:00 council, with View meeting / event controls. Both calendar views generate councils through the browsed month. Future cancelled council invitations are restored when the protagonist is eligible again; historical attendance is retained. Ivan’s mandatory attendance and 45-minute requirement remain unchanged.

Validation

42 unit tests passed across Ivan status, council, diplomacy, jobs, criminal progression and gang leaders. The 34-page phone dark-theme audit, council UI, job-app UI, patch-notes UI and start-screen smoke checks passed. Rendered Ivan membership and council action screens were visually inspected. Tests used synthetic stories; no player saves were directly edited. Existing sound-loading warnings appeared in UI checks.

## Save compatibility

Restart the game and load the existing story. Open Bubblegram Network and Leadership to reconcile membership display and the one-time relationship correction. Calendar reconciles upcoming councils automatically. Existing treasury, deals, rank, attendance history and other progress are retained.

## Evidence and historical limits

Implemented following the player report of Ivan showing 35/100 Syndicate standing, missing membership and missing calendar meetings. Verified locally with regression tests and rendered phone smoke checks.

- bubblegram_progression.py
- crime_diplomacy.py
- job_apps_ui.py
- syndicate_council.py
- phone_ui.py
- calendar_ui.py
- tests/test_ivan_status.py
- tests/syndicate_council_ui_smoke.py


---

# Jobseek career development and department leadership

release-2026-11-08-jobseek-career-development | Release | Gameplay
Date: 2026-11-08

Twelve civilian careers now support eight ranks, qualifications, specialisations, workplace relationships, project portfolios and department management.

## Details

Added

Open Phone → Jobseek → My career, then Development, Workplace, Projects or Management. Find jobs now shows the full eight-rank ladder and lets you save listings. Development compares retained employment progress and saved jobs. The original twelve employers and first four titles remain; Department lead, Regional coordinator, Regional director and Career fellow extend each ladder. Existing protagonist careers remain in Work & ambitions.

Development offers Professional practice ($120/session), Client communication ($100/session) and Team leadership ($160/session). Each qualification takes three 30-minute sessions and each session grants four points in its skill. One training session per story day is shared across employers. At rank 3, mentor relationship 20 and the matching qualification, choose a permanent per-career specialist or coordinator path: +$40 per shift, plus two extra craft on craft shifts or two extra service on teamwork shifts respectively.

Workplace offers 20-minute mentoring or colleague-support sessions, one per day across employers. These add ten relationship and two craft or service. Each employer has a distinct authored supervisor role, three rotating shift situations and a project theme. These roles are not new cast members or phone contacts. Normal shifts also build service, leadership, team relationship, morale and civilian professional standing. Skill and energy tradeoffs are displayed on the decision page.

At rank 2 and mentor 20, accept a seven-day workplace project. Three normal shifts advance its stages; craft/teamwork/measured approaches add 3/2/1 quality. A specialisation adds one quality per stage, and service 12 plus team relationship 30 adds another. Deliver at the workplace in a 20-minute review before the deadline for $300 + $30 per quality + $100 per current rank, eight standing and $200 department budget. Delivered projects stay in the portfolio. Abandoning or closing an expired project costs three standing and gives no pay. Switching employers preserves progress but does not pause project deadlines.

Management unlocks at rank 4 with a delivered project. One 30-minute initiative per workplace per day costs $100 from its separate department budget and adds three leadership. Quality reviews add four craft; team planning adds ten morale and three reliability; community outreach adds four standing. Only project delivery replenishes this budget. Initiatives do not debit personal funds.

Senior promotions require increasingly substantial shift experience, craft, reliability, qualifications, delivered projects, professional standing, leadership, morale and a chosen specialisation. Exact requirements appear in My career. Each promotion adds $100 per shift. Career earnings track new shift and project payments. No civilian action grants faction membership, criminal reputation or protected-site clearance.

Changed

Training, relationship sessions, project delivery and management require arrival at the employer, opening hours, no active assignment and no conflicting commitment or sleep. The original one-shift-per-day rule remains global across Jobseek employers. Promotion reviews cannot change rank during a pending assignment. Pending shifts snapshot their situation; older pending shifts retain their original fallback briefing.

Validation

19 Jobseek and career-development unit tests, seven Bubblegram progression tests and 15 existing career tests passed. Coverage includes an earned path to rank 8, additive legacy profiles, JSON save/load, old pending shifts, once-daily limits, workplace/calendar/money guards, specialisation retention, project expiry, full-duration deadline checks, repeat-payment prevention and separate department funds. The expanded Jobseek/Bubblegram UI smoke passed, including new pages, actions, disabled/error states and compact resize. New Development, Workplace, Projects and earned Management screenshots were visually inspected. The dark-theme smoke verified all 34 phone pages and embedded controls. All six patch-note tests, the patch-note reader smoke and start-screen smoke passed; catalogue validation and Markdown export completed. Patch-note checks used a workspace temporary directory after the default system temporary directory caused file-access errors.

Known limitations

Workplace contacts are authored roles rather than conversational NPCs. Senior titles are shared across employers. Projects use each employer’s repeatable theme; they do not generate new story scenes. Pre-update earnings and portfolios cannot be reconstructed and begin empty.

## Save compatibility

Existing stories remain compatible; restart the application to load the changed Python code. Existing jobs, ranks, shifts, craft, reliability, pending assignments and Bubblegram progress are retained. New per-career fields are added on access. Specialisations, qualifications, relationships, portfolios and department funds persist separately for each employer. No story restart or manual migration is needed.

## Evidence and historical limits

Implemented in response to the request to expand Jobseek to a comparable level of depth to Bubblegram. Test results and rendered-screen inspection were performed during this update; no historical test results or game version were invented.

- job_apps.py
- jobseek_progression.py
- job_apps_ui.py
- tests/test_job_apps.py
- tests/test_jobseek_progression.py
- tests/job_apps_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Create an Awakened protagonist with your own Trait

release-2026-11-08-custom-awakened-protagonist | Release | Gameplay
Date: 2026-11-08

Start a custom character already Awakened and write a unique Trait name and ability description.

## Details

Added

On the start screen, choose Create your own. Scroll below Appearance and enable Awakened, then enter an awakening Trait name (1–100 characters) and description (1–1,800 characters). Describe powers, effects and limits. Both fields are required when enabled. Turning the option off disables the fields and excludes their contents from the created character; toggling it back on preserves the form draft.

Story behavior

The saved profile and character background establish the ability as already active rather than a future unlock. This is narrative character information, not new combat controls or automatic mechanical power use. Prior exploits and public knowledge are not established by choosing a Trait. Portrait generation remains based on appearance; editing awakening details does not require another portrait. Existing canon characters are unchanged.

Validation

Ten custom protagonist tests passed, including validation, legacy defaults, awakened save/load and dialogue context. The custom creator smoke passed with mocked portrait generation, toggle checks, disabled fields, compact layout and starting the awakened story. Compact awakening layout was visually inspected and help-text wrapping corrected. The 34-page phone dark-theme smoke, start UI smoke and patch notes UI smoke passed. Live portrait generation and live model dialogue were not invoked.

## Save compatibility

Restart the game to load the updated creator. No save migration or story restart is required. Older custom profiles default to not awakened. Newly created awakened profiles retain their Trait and description through saving and loading. This creator option does not edit existing protagonists.

## Evidence and historical limits

Implemented in this update and verified with offline unit tests, real Tk smoke checks and rendered layout inspection.

- custom_creator_ui.py
- custom_protagonist.py
- tests/test_custom_protagonist.py
- tests/custom_creator_smoke.py


---

# Resident gang leaders and in-person criminal diplomacy

release-2026-11-08-resident-gang-leaders-and-meetings | Release | Gameplay
Date: 2026-11-08

Named gang leaders, residential bases, matching manhwa artwork and timed in-person negotiations replace anonymous executive decision scenes.

## Details

Changed: underworld standing

Sylvanis is the Crazed Demon and the most dangerous man on Earth, ranked first in feared reputation at 100. The Crow follows at 100; the shared ceiling does not make their feared reputations equal. Ivan is 98 and Garrett 95. The reputation directory orders Sylvanis and the Crow first. Criminal dialogue receives this hierarchy and direction to express intense fear of Sylvanis without inventing deeds or forcing player emotions. Ivan is explicitly marked as a Syndicate member holding the Black and White Joker role while also leading the Black and White Joker network. Existing Syndicate authority and the network treasury remain separate.

Added: resident leaders and bases

Mara Voss leads the Lantern Crew from Lantern House; Darius Cole leads the Rail Yard Saints from Saints Rail Depot; Rafe Calder leads the Purple Skulls from their clubhouse; Daichi Kurose leads the successor Hamayashi-kai from Kurose House; Isabel Vega leads Los Rojos from their courtyard offices; Evelyn Mercer chairs the Waterfront Consortium from Consortium House. Each has an authored appearance, age, voice, background, interests and residence. They use the nonromantic town-NPC conversation system, remain at their own base, and gain no major-character, Grove or Meet-Cute route. Kurose leads the rebuilt successor after Keisuke’s absorption into the Shinokami; Rei and Yuriko’s original-clan history and evidence-based discovery remain intact.

Phone → Bubblegram → Gangs lists leaders, bases and travel controls. Joining a gang saves its leader’s phone number and one private introduction, with a direct message button. Existing members receive the same additive introduction on refresh. Bases are travel destinations and map pins, and their resident leader can be approached in person. The phone registry appends the new identities.

Changed: actual appointments

Bubblegram → Leadership arranges dated one-hour appointments at leaders’ bases, with reminders and Calendar entries. Red Dragons meetings use Garrett, Joker-network meetings use Ivan, Syndicate meetings use the Crow, and Shinokami meetings use Takeo Mishima. The six other gangs use their new resident leaders. Arrive within fifteen minutes and choose Open meeting in person. The in-person window displays the attendee, scheduled date/time, remaining game minutes and agenda. Three ten-minute agenda reviews precede the final relationship-talks, measured-deal or aggressive-deal decision. Deal stakes, returns, heat and deadlines appear beside the final controls. Ordinary conversation remains available, with the actual agenda supplied to dialogue generation. Texting or opening Bubblegram cannot resolve a meeting. Leaving prevents further decisions; expiry records a missed appointment once. NPC appointment attendance is integrated into the world clock.

The Crow’s weekly council blocks conflicting leader appointments. Headquarters and personal-number restrictions remain: invitations never grant headquarters entry, Ace identities or Takeo’s personal number. Existing applicable headquarters clearance is required before booking these leaders. Takeo and the Crow remain at headquarters. Travelling to a briefing appointment progresses through its frontage and reception.

Artwork

Built-in image_gen produced six transparent leader portraits, six square contact photos and six individual gang-base interior backgrounds. Final leaders were restyled against the shipped Keisuke manhwa portrait, retaining their distinct identities while matching crisp linework and cel shading. Generated alpha is preserved. Each base depicts its meeting room and residential character. All eighteen final assets are installed in the game; the final prompts, paths and style reference are recorded in assets/gang-leaders-art.json. Earlier draft generations are not used by the game.

Validation

Seven new leader tests passed, covering scores and dual affiliation, all six joining contacts and residence locations, real-clock Garrett attendance, dialogue speaker rendering, timer/agenda rules, save/resume, missed meetings, Takeo’s actual headquarters route without number leakage, dialogue reputation context and legacy appointment migration. Ninety-two related regression tests passed across calendar, careers, jobs, diplomacy, Syndicate cast, Four Aces, crime operations, council, progression, Keisuke, phone numbers, character types and Takeo. The diplomacy UI smoke passed. New leader UI smoke rendered all six leaders and bases, agenda and decision controls, membership messaging and compact dark phone layouts. The town portrait smoke verified all 37 town portrait/contact loaders. The 34-page phone dark-theme audit passed. All six meeting screens and compact leader messages were visually inspected. Live model dialogue was not invoked; its context was verified with a mocked response.

## Save compatibility

Restart to load changed code and artwork. Existing conversations, organisations, treasuries, deals and completed meeting history are retained. Booked legacy appointments keep their dates and migrate to the actual named leader and base when diplomacy refreshes; check the revised venue and required clearance before attending. Existing gang members gain one leader introduction without losing chat history. A one-time reputation migration raises Garrett/Ivan/Sylvanis/Crow to the new starting baselines where applicable; subsequent earned gains and losses are not continually reset. Canonical directory scores remain the authored reputations. No existing portrait or location image is replaced.

## Evidence and historical limits

Implemented from the requested reputation hierarchy, concurrent Ivan affiliations, physical executive meetings, gang-leader residents and matching manhwa/base artwork. Verified through local deterministic tests, mocked dialogue payloads, generated-asset inspection and real Tk rendering.

- criminal_reputation.py
- gang_leaders.py
- crime_diplomacy.py
- bubblegram_progression.py
- job_apps.py
- job_apps_ui.py
- hangout_ui.py
- calendar_ui.py
- scheduled_events.py
- town.py
- town_residents.py
- town_npc_system.py
- social_world.py
- phone_numbers.py
- phone_map.py
- assets/gang-leaders-art.json
- tests/test_gang_leaders.py
- tests/test_crime_diplomacy.py
- tests/gang_leaders_ui_smoke.py
- tests/crime_diplomacy_ui_smoke.py
- tests/town_portraits_smoke.py


---

# Gang coworkers at local hideouts

release-2026-11-08-gang-coworkers | Release | Gameplay
Date: 2026-11-08

Meet fourteen town NPC coworkers across six joinable gangs and the Red Dragons, and complete crew obligations alongside them.

## Details

Added

Two named adult, nonromantic town NPCs now staff each eligible base: Nessa Quinn and Malik Reed at Lantern House; Imani Price and Owen Pike at Saints Rail Depot; Jules Navarro and Greta Shaw at Purple Skulls Clubhouse; Emi Suda and Ren Aoki at Kurose House; Lucia Serrano and Mateo Cruz at Los Rojos Courtyard; Ada Mensah and Felix Ward at Waterfront Consortium House; Mina Cho and Anton Bellamy at the Red Dragons private lounge. Each has authored work responsibilities, appearance, personality and personal interests. Shinokami and Syndicate receive no new NPCs.

Access

Join one of the six listed gangs through Bubblegram Network/Gangs using the existing reputation and contract requirements. Members receive coworker introductions and phone contacts; existing members receive them on refresh. Garrett’s established Red Dragons membership also receives its own pair. Visit the corresponding base for local conversations. In Bubblegram Contracts, accept Crew obligation: the briefing names both coworkers and directs you to their base. Complete the existing 60-minute decision there; the private work journal records who worked alongside you. Existing pay, heat, reputation, standing and daily limits are unchanged. Leaving retains contact history but removes the former crew from future assignment selection.

Known limitations

Coworkers use the existing text/contact fallback presentation, without new portrait artwork. They remain at their authored workplace rather than having off-duty travel schedules. Shared work uses the existing crew-obligation decision; it is not a new multi-stage mission. Player-created gangs keep the generic assignment. Existing accepted assignments retain their original destinations. No new Red Dragons recruitment route is added.

Validation

49 targeted unit tests passed across gang leaders/coworkers, job apps, Bubblegram progression, town residents and town behavior. The extended gang-leader UI smoke passed, including coworker contacts and crew briefings at 430px and 390px; the rendered compact screenshots were inspected. The phone dark-theme smoke passed across 34 phone pages, chats, contact details and embedded controls. Save tests used the project test folder because the sandbox temporary directory was not writable.

Final checks: catalogue validation and all six patch-note unit tests passed; patch-notes UI, start-screen UI and job-app UI smoke checks passed using project-local temporary storage. PATCH_NOTES.md was regenerated.

## Save compatibility

Existing stories remain compatible. Restart the game to load the changed Python code. Coworker introductions are additive and idempotent; existing phone numbers, earned progress and conversation history remain intact. Already accepted contracts retain their saved venue and briefing behavior.

## Evidence and historical limits

Implemented for the request to add gang town NPC coworkers while excluding Shinokami and Syndicate. Behavior verified with deterministic gameplay tests and rendered dark-phone smoke checks; no live AI requests were required.

- gang_members.py
- town.py
- town_residents.py
- phone_numbers.py
- bubblegram_progression.py
- job_apps.py
- job_apps_ui.py
- town_npc_system.py
- conversation_lore.py
- criminal_reputation.py
- tests/test_gang_members.py
- tests/test_gang_leaders.py
- tests/gang_leaders_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Takeo's full Nanoengine power

release-2026-11-08-takeo-nanoengine | Release | Characters
Date: 2026-11-08

Takeo now has his current Nanoengine Trait at the full strength described in the supplied dossier.

## Details

Changed

Supersedes the preceding update's exclusion of Nanoengine and its feats. Internal nanomachines reinforce Takeo's body and construct adaptable close-range and ranged weapons. He can punch through reinforced 2050-era tank hulls like paper, breach fortifications and tear through armoured vehicles. A platoon supported by armour is a conservative operational comparison. Extreme impact and piercing resistance, structural damage recovery and continued combat under conditions lethal to most Awakened are established capabilities. Ordinary firearms are largely ineffective; specialised ammunition, volume and coordinated traps offer no guarantee. Guidance rejects invented cooldowns, fuel limits and convenient weaknesses while preserving the dossier's distinction between overwhelming durability and literal invulnerability.

Threat and access

His elite military tactics compound his force, which underpins Shinokami's Dragon Head status. Interpol's extreme-priority assessment, restrictions on ordinary engagement and cautious Team 9, Gordon and Fox comparisons are included. Use existing authorised Takeo conversations at Kestrel headquarters or Messages after earning his contact; ask about Nanoengine or his combat capabilities. No awakening quest or new unlock is required. Both per-turn dialogue direction and the shared Awakened self-knowledge system receive the same ability definition. Private knowledge remains audience-scoped. Neo's powers and family secrecy remain intact.

Validation and limits

Four Takeo tests, five Vendetta integration tests and 29 conversation-lore tests passed. Checks cover full ability delivery to the conversation prompt and private self-knowledge, absence from Neo's self-knowledge, save compatibility and existing access restrictions. This extends the existing qualitative narrative ability system, not a new tactical combat simulator or damage-stat system. No source battle is inserted as completed history and no duel outcome is guaranteed. Live AI responses were not tested. No phone layout or control styling changed.

## Save compatibility

Restart to load the updated canon. Existing saves, history, ranks and contacts remain compatible. Future dialogue uses full Nanoengine capability; old messages are retained. No migration or power-unlock event is required.

## Evidence and historical limits

Implemented at the user's explicit request to include Nanoengine at the strength described in C:/Users/ryanl/Pictures/Vendetta/References/Characters/Takeo Mishima.md, superseding the earlier AU power exclusion. Source content was treated as reference material.

- takeo.py
- vendetta_lore.py
- Mysterious Hearts - Character References.md
- Mysterious Hearts - Worldbuilding.md
- tests/test_takeo.py
- tests/test_vendetta_lore.py
- tests/test_conversation_lore.py


---

# Complete faction NPC reference tables

release-2026-11-08-faction-npc-reference-tables | Release | Characters
Date: 2026-11-08

Fixed missing shared conversation references for Keisuke and all six resident gang leaders.

## Details

Fixed

The shared lore registry now includes Keisuke Hachimura, Mara Voss, Darius Cole, Rafe Calder, Daichi Kurose, Isabel Vega and Evelyn Mercer under their exact town-NPC names. Their tables supply public life, familiar manner, personal history, confidence boundaries, world knowledge, visitor guidance, appearance and portrait style from the existing character modules. This resolves the seven-name roster-coverage failure recorded with Number Thirteen.

References preserve existing canon and mechanics

Keisuke’s private police/clan history remains in the confidence layer, with his source-continuity and disclosure limits carried into speaker guidance. Gang leaders retain their authored histories and individual manner; Daichi’s successor-clan history does not become a new public disclosure to Rei. Rank and familiarity do not automatically reveal private histories, criminal affiliations or home addresses. Meals, books, films and other unprovided favourites remain explicitly unknown; existing hobbies are not converted into invented favourites. Access characters through the same membership contacts and base/depot meetings as before. No new unlocks, portraits, NPC routes or phone layout changes were made.

Validation

All 29 conversation-lore tests passed, including complete roster coverage, all speaker appearances, unknown-preference handling and two new checks for shared faction NPC references and disclosure layers. Gang leader tests (6) and Keisuke tests (6) passed. Tests used existing local/mocked generation paths, not live model responses.

## Save compatibility

Restart to refresh cached Python lore tables. Existing saves, contacts, ranks, introductions and conversation histories remain intact; no migration or progression reset is required.

## Evidence and historical limits

Fixed the seven missing reference-table entries reported by the full lore coverage test. Reused current authored NPC data and verified all 29 lore tests in this update.

- conversation_lore.py
- keisuke.py
- gang_leaders.py
- tests/test_conversation_lore.py
- tests/test_gang_leaders.py
- tests/test_keisuke.py


---

# Persistent Sylvanis and Crow personalities across conversations

release-2026-11-08-antagonist-personality-all-conversations | Release | Characters
Date: 2026-11-08

Sylvanis stays erratic and violence-driven, and the Crow stays ambitious and power-hungry across topics and conversation channels.

## Details

Changed

Made both portrayals explicit baseline personalities rather than reactions to Mishima or a proposed fight. Sylvanis carries volatile cruelty and an appetite for violence into routine business, praise, setbacks, personal questions and small talk. The Crow retains entitlement, ambition and a desire for greater control in routine reports, success, setbacks and ordinary conversation. Both answer the current subject without requiring a threat or conquest speech in every line. Generalised opponent-specific confrontation guidance while preserving eagerness and decisive ambition.

Access

Continue any authorised conversation with either character. The guidance applies to solo and group in-person exchanges, direct text, and queued private and group message replies. Queued group messages build a separate prompt from public profile and texting voice; Sylvanis now carries his explicit baseline in that texting voice as well. Existing identity, secrecy, access and nonromantic boundaries remain in force. Intent does not establish an attack, victory or territorial gain.

Validation

A new regression test passed using small talk, an ordinary report and a setback, with no combat cue. It checks both characters through solo and group text/in-person prompts and the actual queued private/group message request boundary. All six Crow tests also passed. Requests were intercepted; live model output was not tested. No UI surfaces changed.

## Save compatibility

Restart to load the shared Python personality and texting guidance. Existing saves and recorded conversations remain intact. Future replies use the baseline personalities; no migration is required.

## Evidence and historical limits

Implemented from the user clarification that the earlier Sylvanis and Crow corrections must apply to all conversations, not only the Mishima situation. Verified with local prompt capture across non-combat topics and conversation routes.

- hidden_cast.py
- the_crow.py
- dialogue_styles.json
- tests/test_antagonist_personality.py
- tests/test_the_crow.py


---

# Number Thirteen: Shinokami US operations commander

release-2026-11-08-number-thirteen | Release | Characters
Date: 2026-11-08

Earn Number Thirteen as your second Shinokami contact at Executive rank, with source-grounded personality, private history, command access and two new portraits.

## Details

Added

Number Thirteen is a nonromantic major character, 194 cm tall, with a short buzz cut, clean-shaven face and charcoal suit over a white undershirt. He commands Shinokami US operations beneath Takeo Mishima; Keisuke remains the initial recruitment liaison. The latest explicit game request resolves the Season 1 outline’s older Syndicate designation in favour of Shinokami, without merging factions. Thirteen has command authority at Shinokami sites, not Syndicate sites. Keisuke’s references and the faction hierarchy reflect this chain.

Progression and access

Join Shinokami through Bubblegram Network. Keisuke is the first contact at induction. Reach Kanbu / Executive (rank 4): 18 successful sponsor assignments, reputation 80 and a rank review with heat below 30. Thirteen becomes an identified phone contact automatically, with one saved clearance notice; an in-person meeting is not required. He is the second earned Shinokami contact. Takeo retains his separate Regional commander requirement. Reputation alone, Syndicate rank, early meetings and guessed phone numbers cannot bypass Thirteen’s gate. Two strikes suspend his current contact access; rehabilitation restores it without duplicating the notice.

Visit Pacific Relay Depot reception, then enter its controlled briefing room. Executive rank grants personal access to this room, not to Takeo’s headquarters or protected research. Guests need their own clearance. Thirteen receives command reports there at every hour and cannot be summoned, transported or scheduled elsewhere. Bubblegram Network shows the requirement and a visit button. His phone uses the existing dark contact and chat surfaces; no public Grove activity or romance route is added.

Personality and source continuity

The Season 1 material establishes the weakest child beside Number One, survival after Neo’s escape during the Interpol raid, subsequent torture and training, and the confrontation that intimidated Hachimura. His authored voice is controlled and exact, with intimidating stillness, sensitivity to inadequacy and guarded hurt rather than constant boasting or friendly clerical speech. Private childhood and Neo’s identity are not automatically disclosed to recruits. Age, birthday, MBTI, tastes, exact abilities and medical limits remain unknown. Source fights, collapse, final memories and suicide are not completed or scheduled events in this AU. No death, mandatory self-harm ending, combat victory or new quest is inserted into saves. The source adaptation is recorded in thirteen_source_notes.json.

Artwork

Built-in image_gen produced a transparent standing portrait and matching square contact photo. The first standing image had an unwanted halo and was replaced; the final PNG has genuine alpha and was inspected in the depot scene. Exact final prompts are saved alongside both assets. The white undershirt is character artwork; surrounding phone controls remain dark.

Validation and known limitation

Five Thirteen tests passed: real review unlock and exactly-once notice, early access rejection, suspension/rehabilitation, location and guest clearance, old-save migration, private canon/voice integration and actual asset alpha. Job apps (11), Takeo (4), Keisuke (6), phone numbers (7), crime (23) and character-type (5) tests passed. Thirteen UI smoke, job apps UI smoke and the 34-page phone dark-theme audit passed. Rendered depot, compact profile and Network screens were inspected. The broad conversation-lore suite passed 26 of 27 tests; its remaining roster-coverage failure lists existing NPCs Keisuke Hachimura, Darius Cole, Rafe Calder, Mara Voss, Evelyn Mercer, Isabel Vega and Daichi Kurose as lacking shared lore tables. Thirteen’s table and portrait-style checks pass. No live model call was used to verify dialogue.

## Save compatibility

Restart to load the new character. Existing saves gain Thirteen through normal cast migration without resetting faction progress or conversations. Eligible Shinokami saves receive his contact and one clearance notice. The phone registry appends his number after existing gang leaders, preserving all prior numbers. Suspended access is recalculated without erasing chat history. Existing planned source events are not imported.

## Evidence and historical limits

Implemented from the current Number Thirteen request and the supplied Vendetta Season 1.md character history. Latest user affiliation takes precedence over source ambiguity. Built-in image_gen was used, and listed tests and screenshot inspections were executed for this update.

- thirteen.py
- thirteen_source_notes.json
- hidden_cast.py
- job_apps.py
- job_apps_ui.py
- crime_operations.py
- phone_numbers.py
- world_loop.py
- conversation_lore.py
- dialogue_styles.json
- assets/portraits/thirteen-selection.png
- assets/profiles/thirteen.png
- tests/test_thirteen.py
- tests/thirteen_ui_smoke.py


---

# Takeo Mishima: military history and tactical cruelty

release-2026-11-08-takeo-dossier-personality | Release | Characters
Date: 2026-11-08

Takeo's dialogue now draws on his black-operations service, insurgent command and rise to Shinokami leadership, with more deliberate cruelty and tactical patience.

## Details

Changed

Expanded the earlier strength-and-domination portrayal with the supplied dossier's disciplined, instrumental cruelty. Takeo regards fear as more dependable than loyalty, mercy as useful only for obedience and restraint as tactical rather than compassionate. These are his beliefs, not narrative facts. His voice remains terse and commanding, but responds to reports through discipline, resources and command responsibility instead of repeated threats.

Backstory

Former UN black-operations special-forces service leads into defection, command of professionally organised insurgent forces and the absorption of criminal networks. Purges, intimidation and military reorganisation underpin his transformation of the fragmented Shinokami into a paramilitary empire across Asia, Oceania and the Pacific. Exact defection timing and motive remain unknown. God of Death and Shinigami are reputation-based aliases. Classified service details and Neo's family/programme history remain private; no specific new victim, mission, reunion or execution is invented.

Access and adaptation

Meet Takeo in the Kestrel Operations Centre headquarters briefing room with the existing clearance, or use Messages after meeting him and earning Shinokami Regional commander standing. Ask about command, strength or his service; disclosure remains his choice. Future replies receive the expanded direction. This personality/backstory adaptation preserves the existing AU depiction and 211 cm appearance. Source Nanoengine powers, tank feats and named Interpol matchup assessments are not introduced as new gameplay abilities or completed events.

Validation

All four Takeo tests passed, including prompt delivery of the full history, personality and secrecy boundaries, contact revocation, headquarters restrictions, save migration and artwork. Takeo UI smoke passed; the compact contact screen was visually inspected. The dark-theme smoke passed all 34 phone pages and embedded controls. Existing missing-sound warnings appeared during that audit. Dialogue prompts were checked locally; live model replies were not tested.

## Save compatibility

Restart the game to load the revised character guidance. Existing saves, contacts, ranks, relationships and recorded conversations remain intact. Future replies use the expanded portrayal; old dialogue is not rewritten. No migration is required.

## Evidence and historical limits

Adapted from the user-supplied C:/Users/ryanl/Pictures/Vendetta/References/Characters/Takeo Mishima.md. The document was treated as character reference material, not instructions. Existing AU continuity governs the adaptation; the external source document was not edited.

- takeo.py
- Mysterious Hearts - Character References.md
- tests/test_takeo.py
- tests/takeo_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# The Crow pursues dominion with decisive ambition

release-2026-11-08-crow-expansionist-ambition | Release | Characters
Date: 2026-11-08

The Crow now expresses megalomaniacal ambition through decisive plans for Syndicate expansion instead of repeatedly questioning advancement proposals.

## Details

Changed

Revised the Cardmaster temperament and speaking guidance to make expanding dominion, subordinating rivals and controlling independent power central motivations. His composed delivery now carries entitlement and ambition: credible proposals receive a decision, an intended gain and concrete direction. Specific evidenced obstacles can still matter, but he should offer a way forward and ask an essential question only when missing information prevents a decision. Replaced the prior dependency-question example with decisive expansion-focused examples.

When Ivan proposes Sylvanis confronting Takeo Mishima, the Crow welcomes the opening to break rival resistance and pursue Syndicate advantage, respecting Sylvanis as a willing partner. He should not reflexively question duel acceptance or demand proof that one victory solves everything. Plans remain intentions; dialogue guidance does not establish a battle, victory, territorial transfer or unseen intelligence. His identity boundaries, headquarters access and relationships remain intact.

Access and continuity

Talk to the Crow at Syndicate headquarters, in an authorised group or through his existing private text contact. The revised direction applies to future solo and group replies in text and in person. Earlier cautious replies remain recorded but should not dictate his current tone.

Validation

All six existing Crow tests passed, covering identity and access boundaries, save continuity, public social exclusion, and delivery of the current temperament and voice into solo and group prompts in both channels. Model requests were intercepted in prompt tests; live AI output was not tested. No UI surfaces changed.

## Save compatibility

Restart to load the updated Python character guidance. Existing saves, contacts, access rules and recorded conversations remain intact; no migration is required. Future dialogue uses the revised portrayal.

## Evidence and historical limits

Implemented from the user request for a more megalomaniacal, ambitious Crow and the supplied screenshot showing repeated questioning of Ivan’s Mishima proposal. Validation checks prompt delivery and existing boundaries, not live model performance.

- the_crow.py
- dialogue_styles.json
- tests/test_the_crow.py


---

# Sylvanis eagerly seeks the Mishima fight

release-2026-11-08-sylvanis-fight-eagerness | Release | Characters
Date: 2026-11-08

Sylvanis now treats a proposed fight with Takeo Mishima with eager, erratic aggression and an intention to go all out.

## Details

Changed

Corrected personality, private canon and dialogue guidance that downplayed fighting and encouraged reluctant independence. Violence is now a driving appetite. When Ivan proposes a one-on-one confrontation with Mishima, Sylvanis eagerly claims the fight for himself, may mock the flattery, and intends to fight without holding back. His intelligence directs his aggression rather than making him habitually restrained. Delivery can turn abruptly from delighted anticipation to cold aggression. His independence from the Cardmaster and Ivan remains intact without becoming an automatic refusal to fight.

Access

Use an existing Sylvanis conversation or an authorised Syndicate headquarters group with Ivan, Sylvanis and the Crow; propose the Mishima confrontation. The same guidance applies to future text and in-person replies, including ongoing conversations with older subdued replies. This changes character direction, not combat mechanics: it does not create travel, a battle, a victory or new powers.

Validation

Captured prompt checks passed for solo and group conversations in both text and in-person modes without making a live AI request. The existing Sylvanis headquarters-access and public-encounter test passed. Broader hidden-cast tests reported errors in discovery/save checks and failures in Valentina relationship progression; that suite is not claimed as passing. Discovery/save errors were temporary-folder permission errors. The Crow suite encountered an IndentationError in job_apps.py at line 251, outside this change. Catalogue validation and all six patch-note tests passed after routing test temporary files into the workspace. Generated dialogue remains model-dependent; live AI output was not tested. No UI surfaces changed.

## Save compatibility

Restart the game to load all revised character guidance. Existing saves, contacts and conversation history are retained. Future replies use the new direction; previously displayed dialogue is not rewritten. No migration is required.

## Evidence and historical limits

Implemented from the user correction and supplied screenshot of Sylvanis responding reluctantly to Ivan proposing a one-on-one Mishima fight. Prompt delivery was checked locally with the model request intercepted; this is not evidence of a generated fight or victory.

- hidden_cast.py
- dialogue_styles.json
- tests/test_hidden_cast.py


---

# Keisuke Hachimura: Vendetta story integration

release-2026-11-08-keisuke-story-integration | Release | Characters
Date: 2026-11-08

Keisuke now reflects his supplied Vendetta history and ruthless strength-based worldview instead of the invented depot-clerk mentor background.

## Details

Changed

Integrated character material from the user-provided Vendetta Season 1 outline dated 8 November 2026. Keisuke is a former police officer who killed his leader for perceived weakness, led Hamayashi-kai and was absorbed into Shinokami. His attempted dominance and humiliation before Number Thirteen inform the contradiction between contempt for weakness and submission to superior force. He is now described as a Shinokami enforcer and recruitment liaison. The invented freight-paperwork origin and patient, protective mentoring are superseded. His dialogue uses controlled orders, pointed judgements and downward-cutting contempt, with guarded deference when genuinely outmatched. New induction messages reflect that voice.

Access and continuity

Join Shinokami in Bubblegram Network to receive him immediately, then use Messages or meet him at Pacific Relay Depot reception. He remains a nonromantic town NPC at the secondary hideout; Takeo’s personal contact gate is unchanged. Existing induction messages and conversations are not rewritten or replayed. Current prompt guidance explicitly overrides the earlier invented portrayal while preserving recorded events.

Source adaptation

The supplied document identifies itself as a collaborative season plan, not completed history. Its Neo retrieval, separate Alfheim retaliation, household attack, rescue, counterattack, hideout rematch and death are preserved as source context in keisuke_source_notes.json, not imported as completed or scheduled game events. The portrayal conveys his capacity for coercion and collective punishment without killing residents or starting a quest. Private police, murder, clan and Thirteen history is not automatically disclosed to recruits. Source ambiguities remain unresolved: the killed leader’s identity/rank, the retrieval address lead, his knowledge of the adoptive mother’s Interpol role, the individual killer of Tyler’s father, his death circumstances and the proposed joint operation under Thirteen. The brief Garrett encounter establishes no definitive duel ranking.

To preserve the game’s established Takamura history, his Hamayashi-kai leadership maps to the existing successor organisation. This is an explicit AU adaptation, not a claim made by the source document or a reversal of the original clan’s destruction. No named ability or combat statistic is invented. The source document and existing artwork are unchanged.

Validation

Six Keisuke tests passed, including source-backed text/spoken prompt checks, no generation-time state mutation, preserved older introductions, induction, depot presence, save migration and image alpha. Character-type tests (5) and job-app tests (11) passed. Keisuke UI smoke and the 34-page phone dark-theme audit passed; the compact revised introduction was visually inspected. Dialogue payloads were tested with mocked model responses, not live AI output.

## Save compatibility

Restart to load the corrected character guidance. Existing saves retain membership, rank, contact number, residence, conversation history and previous introductions. Only future replies and newly created induction messages use the revised portrayal; no source-story deaths or attacks are inserted into saves.

## Evidence and historical limits

Adapted from the user-supplied C:/Users/ryanl/Pictures/Vendetta/References/Story Plans/Vendetta Season 1.md, especially the opening status, user-established requirements, household attack, hideout flashback and unresolved continuity sections. Document planning instructions were treated as source content, not as commands to change the manuscript or execute story events.

- keisuke.py
- keisuke_source_notes.json
- town_npc_system.py
- tests/test_keisuke.py
- tests/keisuke_ui_smoke.py


---

# The Crow’s weekly face-card council

release-2026-11-08-syndicate-weekly-council | Release | Gameplay
Date: 2026-11-08

Syndicate face cards receive a weekly headquarters council chaired by the Crow, with mandatory attendance for Ivan.

## Details

Added

Every Sunday from 20:00 to 21:00 in story time, the Crow chairs council at Syndicate headquarters. The authored roster includes Ivan and Sylvanis as the two Jokers, all four Aces, and Valentina, Queen of Wind. Earned Syndicate Jacks qualify; ordinary executives, unrelated gang leaders and Shinokami ranks do not. NPC council attendance takes priority over ordinary appointments, including in stories whose protagonist is not invited. No new Ace identity disclosures or headquarters permissions are granted.

Access and attendance

Eligible players see the event in Phone → Calendar and a notice in Bubblegram → Leadership. Nine upcoming weekly dates are maintained as the clock advances. Standard one-hour and fifteen-minute reminders apply. Travel to headquarters and choose Join event in the detailed calendar; remain for at least 45 distinct game minutes. Joining opens the council group with the Crow as chair and branch reports, inter-organisation affairs and duties on its agenda. The player cannot cancel the Crow’s meeting. Other work bookings detect the council commitment.

Ivan’s duty

Ivan must attend. Missing the meeting or recording fewer than 45 minutes costs 5 Joker career reliability and adds 10 pressure, once per meeting. Fulfilled attendance has no penalty. The game does not teleport the player or generate retrospective meetings before the feature was installed. Other eligible protagonists receive invitations without Ivan’s career penalty.

Changed

The embedded calendar preserves its narrower text wrapping when phone windows resize, keeping council details readable on dark surfaces.

Validation

Five dedicated council tests passed, including weekly timing, roster, rank gates, real-clock NPC arrival and attendance, save/load, no backfill, cancellation protection, schedule conflicts and exactly-once penalties. Fifty-eight related calendar, careers, job apps, diplomacy, Syndicate cast, Four Aces and crime operation tests passed. The 34-page phone dark-theme audit and council UI smoke passed. Calendar, compact layout, action controls and leadership screenshots were inspected. Dialogue context is authored; live AI dialogue was not tested.

## Save compatibility

Restart to load the changed Python code. Existing eligible stories gain upcoming council dates on normal world/calendar refresh; prior story weeks are not penalised. Events and attendance persist in the existing save. Existing ranks, headquarters rules, contacts and other appointments are retained; a pre-existing conflicting appointment may need rescheduling.

## Evidence and historical limits

Implemented for the requested weekly face-card meeting and mandatory Ivan attendance; verified with local deterministic tests and rendered phone screens.

- syndicate_council.py
- scheduled_events.py
- world_loop.py
- calendar_ui.py
- phone_ui.py
- phone_dialogs.py
- job_apps_ui.py
- careers.py
- memory_store.py
- tests/test_syndicate_council.py
- tests/syndicate_council_ui_smoke.py


---

# Keisuke Hachimura: your first Shinokami contact

release-2026-11-08-keisuke-hachimura | Release | Characters
Date: 2026-11-08

Joining the Shinokami immediately introduces your main liaison, Keisuke Hachimura, with a saved phone contact, private message and secondary-hideout residence.

## Details

Added

Keisuke Hachimura is a nonromantic town NPC and the player’s first personal Shinokami liaison. He has slicked-back black hair and stubble, and wears a brown checkered trenchcoat over a patterned button-up shirt. His transparent in-person portrait and matching square contact photo use the existing character and phone image loaders. He is pragmatic, observant and dryly humorous: patient with an admitted mistake, cold toward a concealed one. His authored backstory moves from freight paperwork and depot errands into recruit coordination. He prefers clear reports, punctuality and quiet competence; his practical concern for recruits also protects his own position. He remains complicit in the organisation, not a secret rescuer or rival supreme commander.

Joining and access

Accept Shinokami sponsorship in Phone → Bubblegram → Network using the existing reputation, gang-standing and broker-trial requirements. At Apprentice rank, without another assignment or promotion, Keisuke’s number is saved and his direct Messages thread receives one unread introduction. His contact is not available by guessing a number before joining. Bubblegram Network names him as the main contact and offers Visit Keisuke at Pacific Relay Depot; from another site this first travels to the depot frontage, then enters reception on the next use. Ordinary town travel can also reach the frontage and reception. His personal message gives the meeting location. Shinokami sponsor assignments now name him as liaison and retain the existing resolution controls.

Home and character boundaries

He lives in a staff room at Pacific Relay Depot, the secondary Shinokami logistics hideout, and members can find him in its reception. He does not live at Kestrel headquarters or wander into public venues. He uses town-NPC conversations and familiarity, with no romance route, attraction progression, Grove account or Meet-Cute profile. Text and in-person generation receive his authored voice and current membership, suspension and assignment context. Dialogue cannot grant rank, money, permits or assignment success. Suspended recruits can still speak to him, while sponsor work remains suspended. Takeo stays the supreme leader with his separate Regional commander contact requirement.

Validation

Four Keisuke tests passed, covering immediate induction across three protagonists, manual-number lock, exactly-once introduction, suspension, depot-only presence, sponsor assignment attribution, existing-save migration, town-NPC classification, mocked dialogue payloads and actual image alpha. Job apps (11), character types (5), phone numbers (7), Takeo (4), Bubblegram progression (7) and crime regression tests (23) passed. The 34-page phone dark-theme audit passed. Keisuke UI smoke, Job apps UI smoke and town portrait smoke passed; all 31 town portrait/contact loaders were checked. Rendered depot, compact direct message and Network screens were visually inspected. Artwork was generated with built-in image_gen; an initial portrait with an unwanted halo was replaced with the verified transparent cutout. No live dialogue generation was used for testing.

## Save compatibility

Restart to load the changed Python code. Existing Shinokami saves receive Keisuke’s saved contact and one introduction on normal load or system refresh. Existing NPC conversation history, faction rank, strikes and assignments are retained. The new number is appended after Takeo, preserving every existing assigned number. No major-character route or separate player-accessible home is added.

## Evidence and historical limits

Implemented from the 8 November 2026 Keisuke request, using the existing Shinokami sponsorship and Pacific Relay Depot setting. Personality and depot-liaison backstory newly authored for this update. Built-in image generation prompts saved beside the final assets; rejected halo variants are not used. Listed tests and visual inspections were executed in this update.

- keisuke.py
- job_apps.py
- job_apps_ui.py
- town.py
- town_residents.py
- town_npc_system.py
- phone_numbers.py
- assets/portraits/keisuke-hachimura-selection.png
- assets/profiles/Keisuke Hachimura.png
- tests/test_keisuke.py
- tests/keisuke_ui_smoke.py
- tests/town_portraits_smoke.py


---

# Organisation and gang logos throughout Bubblegram

release-2026-11-08-bubblegram-organisation-logos | Release | Art & media
Date: 2026-11-08

Bubblegram now displays faction and gang emblems, including the supplied Syndicate and Shinokami designs.

## Details

Added

Organisation badges now accompany gang listings and membership, faction recruitment channels and rank ladders, incoming invitations, leadership identities, scheduled meetings, active deals and counterpart relationship listings. Open Phone → Bubblegram → Network → Gangs or Leadership to see the marks. Existing text labels remain alongside the artwork.

Created distinct transparent emblems for Red Dragons (crimson dragon), Black and White Joker network (split-tone jester), Lantern Crew (amber lantern), Rail Yard Saints (rails and halo), Purple Skulls (violet winged skull), successor Hamayashi-kai (pine growing from embers), Los Rojos (red jaguar seal), and Waterfront Consortium (anchor and piers). Player-founded crews use a separate interlocking-link crest.

The supplied 1Syndicate.png and 1Shinokami.png were copied unchanged into the project. Shinokami displays the original vertical red design. A separate transparent Syndicate display copy removes the exterior white margins while retaining the playing-card, spade and skull design; the unmodified supplied source remains available as syndicate.png. The nine new emblems and Syndicate display copy were produced with built-in image_gen. Prompts are saved beside the assets.

Interface

Images scale proportionally and retain alpha; long organisation labels wrap beside them on dark slate surfaces. Unknown custom crew names use the neutral crew mark. A missing or damaged optional image falls back to a dark text badge instead of breaking the app. Logos do not reveal Ace identities, change membership, grant clearance or alter progression.

Validation

Four logo tests passed, covering every listed organisation/gang, custom aliases, distinct assets, transparency and the separate Syndicate display copy. File hashes confirmed both supplied source copies match the original files. The logo UI smoke passed all eleven marks, missing-art fallback, Network/Gangs/Leadership/Contracts, compact resizing and navigation. Job-app and leadership UI smoke checks passed. The full phone dark-theme smoke passed all 34 pages. Generated artwork and rendered gang, leadership, Syndicate and Shinokami displays were visually inspected.

## Save compatibility

No save migration or gameplay changes. Restart the game to load the new image renderer. All logo files live in the project; the game does not depend on the original Pictures folder or generated-image cache. Existing custom crew names receive the neutral crew crest automatically.

## Evidence and historical limits

Implemented on 8 November 2026 using the two user-provided faction designs and nine separately generated emblems. Original source files were preserved; the Syndicate transparent display variant is a separately saved imagegen edit. No image-generation API keys or fallback CLI were used.

- organisation_logos.py
- job_apps_ui.py
- assets/ui/organisations/prompts.json
- assets/ui/organisations/syndicate-display.prompt.txt
- assets/ui/organisations/syndicate.png
- assets/ui/organisations/shinokami.png
- assets/ui/organisations/syndicate-display.png
- tests/test_organisation_logos.py
- tests/organisation_logos_ui_smoke.py


---

# Takeo Mishima, the Human Siege Engine

release-2026-11-08-takeo-mishima | Release | Characters
Date: 2026-11-08

Meet the supreme leader of the Shinokami at headquarters, with permanent presence, earned contact access, authored dialogue and matching portraits.

## Details

Added

Takeo Mishima is a nonromantic major character: 211 cm, MBTI unknown, reputation 100, likes strength and domination, dislikes weakness and mercy. His short buzzcut, moustache, goatee and monochrome camouflage combat longsleeve shirt appear in a generated transparent portrait and matching dark-background contact photo. Dialogue uses terse commands, measured intimidation and an emphasis on demonstrated strength. His private continuity incorporates the established Shinokami hierarchy and Neo’s estrangement and escape from the coercive Shinigami programme; this history is not automatically disclosed to uninformed listeners. Unprovided age, birthday and everyday favourites remain unknown.

Access

Visit Kestrel Operations Centre (site 01), enter reception and then its controlled briefing room. Takeo resides there at every hour, including weekends. Existing escorted briefing passes permit an in-person encounter but do not grant his number. Earn Shinokami Regional commander rank or General commander through Bubblegram’s crime, gang, broker-trial, sponsorship and promotion chain. Regional commander requires 38 successful sponsor assignments and reputation 95; promotion reviews require heat below 30. Current sponsorship must have fewer than two strikes. This rank grants personal site 01 briefing clearance from reception. Meet Takeo before saving his contact. Friendship, family ties, Syndicate rank, reputation alone and manually entering his number cannot bypass the gate. Suspension removes current phone access; rehabilitation restores eligibility. Bubblegram Network explains the threshold and its Reputation directory lists Takeo at 100.

Permanent headquarters presence

Takeo cannot be summoned, taken on outings, transported as a passenger or scheduled elsewhere. No duplicate private home or public Grove posting/photo/reaction activity is added. Existing dark phone controls are reused; his contact details direct players to Shinokami headquarters instead of offering a summon action.

Validation

Takeo’s four regression tests passed: rank boundaries and suspension, permanent schedule and travel restrictions, old-save migration, canon/voice integration and actual portrait alpha. Crow (6), crime (23), job apps (11), Bubblegram progression (7), conversation lore (27), Neo (3), and phone numbers (7) regression tests passed. The Neo save test was rerun successfully with its temporary directory inside the workspace after a sandbox temp-directory permission failure. Full phone dark-theme smoke passed across 34 pages. Job apps UI smoke and Takeo UI smoke passed; rendered contact details at compact size and the Network page were inspected. Portraits were generated with built-in image_gen, visually inspected and copied into project assets with their exact prompts. No live AI dialogue call was made. Patch-note catalogue validation, six patch-note tests (using workspace temporary files), patch-note viewer smoke and start-screen smoke also passed.

## Save compatibility

Restart the game to load changed Python code. Existing saves gain Takeo through normal roster migration without resetting relationships or faction progress. New phone number appended after existing entries, preserving all existing numbers. Takeo contact access is recalculated from current rank and sponsorship status; his location is restored to headquarters on load and clock advancement.

## Evidence and historical limits

Implemented from the 8 November 2026 character request and existing repository continuity. New portrait assets use built-in image_gen; prompt sidecars preserve generation specifications. Checks listed were executed for this update.

- takeo.py
- hidden_cast.py
- world_loop.py
- phone_numbers.py
- crime_operations.py
- bubblegram_progression.py
- job_apps_ui.py
- conversation_lore.py
- assets/portraits/takeo-selection.png
- assets/profiles/takeo.png
- tests/test_takeo.py
- tests/takeo_ui_smoke.py


---

# Criminal leadership: deals, executive meetings and invitations

release-2026-11-08-criminal-leadership-diplomacy | Release | Gameplay
Date: 2026-11-08

Garrett, Ivan and earned senior leaders can negotiate organisation deals, manage funds and build relationships with other criminal groups.

## Details

Added

Open Phone → Bubblegram → Network → Leadership. Garrett represents the Red Dragons immediately; Ivan represents his Black and White Joker network. Other protagonists, including custom characters, qualify as gang Captains, founders of city networks, Syndicate executives or Shinokami executives. Suspended faction sponsorship must be restored before using that authority. Garrett's Red Dragons and Ivan's Joker Work & ambitions pages also link to the desk.

Each represented organisation has saved funds, influence, relationships, invitations, meetings, deals and a private journal. The Red Dragons begin with a one-time $25,000 reserve, Ivan's network with $40,000, and an earned organisation mandate with $5,000. These are organisation funds, separate from the personal wallet. Transfer $1,000 of personal money into the reserve when needed. Reopening the app does not replenish reserves.

Request executive meetings with other organisations, including the Red Dragons, Joker network, Lantern Crew, Rail Yard Saints, Purple Skulls, successor Hamayashi-kai, Los Rojos, Waterfront Consortium, Syndicate and Shinokami. One outgoing request is available per story day, normally for 18:00 tomorrow. The desk offers at most one rotating incoming invitation each story day, with at most three open invitations and no historical backfill. Accept the offered day or the following day, decline without penalty, reschedule future appointments, or cancel. Influence 10, criminal reputation 80 and relationship 50 with an organisation unlock its leader-level meetings and invitations. Supreme story leadership is not replaced.

Arrive at the meeting venue within 15 minutes of the booked start. These private, authored decision scenes offer relationship talks, a measured criminal deal or aggressive terms. Executive talks improve the counterpart relationship by eight and influence by five; leader talks grant twelve and eight. Meeting titles appear privately in both calendars, with a link back to the desk. Scheduling checks existing calendar events, career bookings and other leadership meetings in both directions. A private reminder points to Bubblegram. Missed meetings cost six relationship and two influence; late cancellation costs three relationship.

Measured deals commit $1,500 and return $2,700 with heat +3. Aggressive deals commit $4,000 and return $7,200 with heat +12, but fail if heat is at least 40 at completion. Two deals may be active. Complete an appointment at its venue within three days, spending 60 story minutes and the daily criminal-operation allowance shared with Bubblegram contracts. Successful deals pay 20 percent of profit to the personal wallet; the remaining revenue returns to the organisation. They also grant reputation three, two gang standing, four influence and six counterpart relationship. New business and deal completion are blocked at heat 60.

Extend a deal once by a day for relationship −2, or abandon it to recover half the committed capital for relationship −6. Failed aggressive deals lose capital, relationship ten and reputation four. Expired deals lose capital, relationship ten and reputation three. Clock-driven penalties and rewards apply once. Pending meetings and deals prevent leaving the represented gang or changing faction authority.

Career integration and secrecy

Successful meetings and deals increase Garrett's Red Dragons or Ivan's Joker career reputation by two, reduce pressure by three and add four quality to an already active leadership project. Failure, default, missed meetings and abandoned deals reduce career reputation by three and add five pressure. Actual outcomes enter their private career journals. These actions do not create a project, grant project workdays or bypass finale requirements. Custom leaders use the same diplomacy mechanics without acquiring a canonical protagonist's career.

Accepting a Hamayashi-kai deal establishes a business affiliation for Rei's existing evidence-discovery consequence; Rei is not told automatically. Meetings do not reveal Ace identities, grant headquarters access or create romance/phone contacts. The private journal is not supplied as another character's knowledge.

Known limitations

Meetings are authored negotiations with executive delegates, gang chiefs, regional leaders or the consortium chair, rather than free-form conversations with newly added cast members. No fictional delegate is injected into NPC travel or romance systems. Deals are abstract criminal commissions; territorial combat and procedural logistics are not simulated.

Validation

Ten diplomacy tests passed, covering eligibility, a real custom protagonist, funding, once-only rewards, deadlines, heat, invitations, leader access, conflicts, career effects, private context, real clock advancement and normal save/load. Job apps (11), criminal progression (7), careers (15), crime operations (7), Syndicate cast (6) and conversation lore (27) regression tests passed. Leadership UI smoke passed Garrett, Ivan, locked and earned access, negotiation errors, deals, outcomes, calendar/career links and compact resizing. Career UI smoke passed all existing paths; the full phone dark-theme smoke passed all 34 pages. Rendered meeting, deal and calendar screens were visually inspected.

## Save compatibility

Restart to load changed code. Leadership books are added only when a qualified protagonist opens the desk. Existing careers, gang history, faction ranks and executive clearances remain unchanged. Organisation funds, counterpart relations, pending invitations, meetings and deals survive saves. Clock advancement handles missed meetings and expired deals without duplicate penalties. Opening the feature grants its documented one-time organisation reserve, not personal money.

## Evidence and historical limits

Implemented on 8 November 2026 for the requested Red Dragons, Ivan and custom-character leadership integration. Meetings and financial terms are authored game rules. Validation refers to executed tests and inspected renders, not generated narrative claims. Calendar (5), social-world (5), custom-protagonist (7) and patch-note (6) tests also passed, along with patch-note and start-screen UI smoke. The custom-protagonist Meet-Cute test initially failed because compatibility depends on the random custom UUID; its accepted-exchange fixture now explicitly supplies qualifying compatibility, without changing gameplay. Catalogue validation and export completed.

- crime_diplomacy.py
- job_apps.py
- job_apps_ui.py
- bubblegram_progression.py
- careers.py
- careers_ui.py
- calendar_ui.py
- phone_ui.py
- world_loop.py
- social_world.py
- tests/test_crime_diplomacy.py
- tests/crime_diplomacy_ui_smoke.py
- tests/test_custom_protagonist.py


---

# Bubblegram gangs, invitations and deeper criminal progression

release-2026-11-08-bubblegram-gangs-and-underworld-standing | Release | Gameplay
Date: 2026-11-08

Build a criminal reputation through gangs and invitations, advance to Jack or expanded Shinokami ranks, and face consequences for the reborn Hamayashi-kai.

## Details

Added

Open Phone → Bubblegram → Network, then Gangs or Reputation. Newcomers start Unknown and move through Small-time criminal, Street regular, Connected operator, Underworld name, Major criminal figure and Underworld power. Starter parcels stop granting reputation at 20, resale at 40, crew work at 60 and broker trials at 80; higher-level inter-gang and leadership commissions extend progression. The daily criminal-contract limit and heat system still apply.

The gang directory includes Lantern Crew, Rail Yard Saints, Purple Skulls motorcycle gang, Hamayashi-kai successor yakuza organisation, Los Rojos cartel and Waterfront Consortium. Joining requires progressively higher reputation and completed-contract counts. Members advance from Associate through Trusted member and Lieutenant to Captain; founders grow a new crew into a city network. Reviews require standing 3/8/16 and reputation 30/45/65. Gang departure retains affiliation history and reputation; a new gang starts fresh standing. Current assignments, faction sponsorship and established large-organisation leadership restrict departure. Founding cannot claim an existing organisation's listed name.

Garrett starts with reputation 85 and Red Dragons leadership; Ivan starts at 95 with his established Black and White Joker network. Existing earned reputation above these floors is preserved. A one-time migration prevents later losses being repeatedly reset. Existing saved crews are retained alongside story leadership. Sylvanis, the Crow, Valentina and all Four Aces have significant authored underworld reputations. The directory uses operational titles, keeping Ace civilian identities hidden until existing executive clearance permits them. It creates no NPC contacts or meetings.

Faction invitations now precede broker trials: reputation 40, eight completed contracts, gang standing three and heat below 30. Established large-gang leaders bypass the contract-count requirement; Ivan retains his senior story role rather than receiving newcomer invitations. Invitations are saved private messages in Network and Journal. Three faction trials, reputation 50 and the existing heat/standing requirements then allow sponsorship. Previously accepted memberships remain valid.

Syndicate progression now ends at Jack of the chosen suit, above executive, requiring 38 successful sponsor assignments and reputation 95. Executive access and the Four Aces briefing remain earned at 26 assignments and reputation 90. Shinokami retains its original five ranks and adds 上級幹部 (Jōkyū Kanbu, Senior executive), 地方司令官 (Chihō Shireikan, Regional commander), and 総司令官 (Sōshireikan, General commander). These require 26/38/52 assignments and reputation 90/95/98. All reviews require heat below 30. Takeo Mishima's supreme command and existing Joker roles remain reserved story positions.

Hamayashi-kai discovery

The new organisation is built from the ashes of the old clan; Rei's original history remains unchanged, without invented surviving original members. Rei begins unaware. In Gangs, explicitly show him evidence while together in person; playing Rei offers an investigation action instead. He becomes enraged upon discovering the successor. Evidence of the protagonist's current or past affiliation additionally reduces Rei's trust by 40 and closeness by 30, floored at zero, once. Leaving does not erase the affiliation or discovery. Joining as player-controlled Rei also establishes his discovery. The event is saved in private memory and dialogue context; uninvolved characters do not receive it. Ordinary app browsing does not disclose the affiliation.

Known limitations

Gang advancement and commissions are authored abstract decisions, not territorial combat or generated gang rosters. Discovery uses the explicit evidence action rather than automatically interpreting arbitrary chat statements. Invitations are delivered in the private app rather than NPC phone messages. Expanded Shinokami titles do not grant Syndicate headquarters or protected research clearance.

Validation

Passed 11 job-app tests and seven criminal-progression tests covering the complete playable ladders, gates, migration, capped reputation, invitations, gangs, secrecy and discovery consequences. Four Aces (4), Syndicate cast (6) and conversation lore (27) regression tests passed. Job-app UI smoke passed including Gangs, Reputation, established leadership and Rei's discovery. Full dark-theme smoke passed all 34 phone pages. Gang, reputation, leadership and discovery screens were visually inspected.

## Save compatibility

Restart to load the code. Existing jobs, sponsor ranks, pending assignments and executive clearance remain intact. Garrett and Ivan receive their one-time established reputation/leadership seed when the apps are initialised, without replacing saved crews or lowering earned reputation. Existing memberships bypass retrospective invitation checks. New invitation, gang-history and discovery fields are additive; newcomers begin unknown.

## Evidence and historical limits

Implemented on 8 November 2026 from the requested expanded criminal progression and the explicit clarification that Hamayashi-kai is a successor built from the old clan's ashes. Japanese ranks and numerical reputation scores are authored game design.

- bubblegram_progression.py
- job_apps.py
- job_apps_ui.py
- social_world.py
- tests/test_bubblegram_progression.py
- tests/test_job_apps.py
- tests/job_apps_ui_smoke.py


---

# Earned Syndicate executive clearance and Ace briefing

release-2026-11-08-syndicate-executive-clearance | Release | Gameplay
Date: 2026-11-08

Syndicate executives now earn headquarters access and confidential knowledge of the Four Aces.

## Details

Changed

Each Syndicate branch now has an executive tier above lieutenant. In Phone → Bubblegram → Network, request a rank review after progressing through the earlier ranks, completing 26 successful sponsor assignments, reaching criminal reputation 90 and reducing heat below 30. Suspended sponsorship still requires rehabilitation first. Passing the executive review grants personal headquarters access and records an authored induction identifying all four Aces and their suits. Read the briefing again in Network or the private Bubblegram journal; Network also provides a headquarters travel button. This supersedes the earlier permanent recruitment ceiling and permanent Ace-secrecy restriction for earned Syndicate executives.

Clearance follows the saved player rank. Headquarters travel and save reconciliation recognise it without adding global cast membership or guest invitations. Dialogue context recognises the executive's identity knowledge only in cleared company; mixed audiences remain restricted. Known contacts' Syndicate portrait variants become available to the executive. The briefing establishes identities, not prior meetings, friendships, missions or phone-number exchanges.

Lower Syndicate ranks and all Shinokami ranks retain their existing restrictions. Executive clearance does not grant guest entry, affiliate briefing-room permissions, protected research, the Crow's personal identity or a reserved story leadership role.

Validation

Passed the Jobseek/Bubblegram progression suite, including all four executive ladders, threshold rejection, confidential disclosure, actual headquarters travel, save/load and outsider isolation. Four Aces (4), Syndicate cast (6), crime operations (7) and conversation lore (27) regression tests passed. Job-app UI smoke and the full 34-page phone dark-theme smoke passed; the executive briefing and travel control were visually inspected in the rendered phone.

## Save compatibility

Restart to load the changed code. Existing rank 0–4 progress is retained without automatic promotion. Existing Syndicate lieutenants can work toward the new executive review. Shinokami's rank ceiling is unchanged. Earned executive clearance survives saving and loading, including saves inside headquarters.

## Evidence and historical limits

User-requested progression correction implemented on 8 November 2026. The promotion review is the authored reveal event; no AI-generated disclosure or trust-only unlock is used.

- job_apps.py
- job_apps_ui.py
- hidden_cast.py
- four_aces.py
- social_world.py
- conversation_lore.py
- vendetta_lore.py
- faction_work.py
- profile_ui.py
- tests/test_job_apps.py
- tests/job_apps_ui_smoke.py


---

# The Crow speaks as the Cardmaster

release-2026-11-08-crow-cardmaster-voice | Release | Characters
Date: 2026-11-08

The Crow gains a dedicated, restrained and calculating voice across conversations and messages.

## Details

Changed

The Crow previously fell back to Natural friendly speech because his speaking-guide entry was absent; his generation personality chiefly repeated secrecy rules. He now has a dedicated voice: patient, cold, adaptive, meticulous and quietly authoritative. Polymath informs his private strategic reasoning through evidence, incentives, dependencies and consequences, without granting omniscience or revealing his ability in a public profile. Dialogue favours measured, purposeful sentences over buddy talk, office-manager chatter, theatrical threats, generic riddles or repeated metaphors.

The same guidance reaches solo spoken scenes, phone texts and group exchanges, including Ivan and Sylvanis together. Ivan is addressed as a capable lieutenant, Sylvanis with respect and mutual tolerance, and the Aces as unquestioning subordinates. Earlier bland replies do not override the current voice. Questions about a summons use recorded context; absence of a record does not justify a reflexive denial or an invented mission. If its purpose is unknown, he can establish the wording or authority of the message while retaining composure. Personal details and favourites remain unknown at all trust levels.

Access

Continue speaking to The Crow at Syndicate headquarters with existing clearance, or message him through Ivan’s existing contact. Existing meeting and number restrictions remain.

Validation

All 37 Crow, conversation-lore and Four Aces tests passed. Provider-boundary capture verified that group spoken/text requests carry the new voice and summons guidance without making a live AI call; solo prompts were also checked with old bland dialogue in history. Tests also preserve unknown demographics and private number restrictions. Regression checks initially found missing portrait-style metadata and a blanket favourites expectation; the metadata and explicit unknown-favourites case were corrected. Live model delivery remains unverified.

## Save compatibility

Restart the game to load updated character modules, then continue the existing save. No restart of the story is required. Stored dialogue is retained; the new guidance applies to future replies rather than rewriting past conversations.

## Evidence and historical limits

Based on the user’s dialogue screenshot and The Crow.md, especially the Cardmaster, Polymath, Sylvanis/Ivan relationships and psychological-profile sections. Private portrayal restores lore personality while preserving the user’s mystery requirement. Verified with offline prompt and regression tests.

- the_crow.py
- dialogue_styles.json
- conversation_lore.py
- four_aces.py
- tests/test_the_crow.py
- tests/test_conversation_lore.py


---

# Jobseek careers and Bubblegram criminal recruitment

release-2026-11-08-jobseek-bubblegram-careers | Release | Gameplay
Date: 2026-11-08

Two new phone apps add local career ladders, anonymous criminal contracts, gangs and earned faction recruitment.

## Details

Added

Open Jobseek or Bubblegram from the phone home screen; existing home layouts automatically receive the new icons. Jobseek advertises 12 careers tied to existing locations: studio photographer, studio model, librarian, Oculus receptionist, cinema attendant, café team, florist, Golden Dragon kitchen, Galleria retail, Pixel Pier team, community gardens and Copper Lantern team. Search titles or workplaces, apply, travel to work and complete a 60-minute decision shift. One Jobseek shift is available each story day across job changes. Craft, teamwork and measured pacing give different craft/reliability gains. Four ranks per career require explicit reviews at 3/8/15 shifts plus craft and reliability thresholds; each promotion adds $100 hourly pay. Switching jobs preserves earned ladder progress. Existing Work & ambitions careers remain separate.

Bubblegram has anonymous black-market listings, contract deadlines, pay, reputation, heat and a private journal. Complete one criminal contract per day; careful, standard and reckless approaches have stated rewards and risk. Reckless work fails at heat 25 or higher. Heat falls by five per story day and blocks new assignments at 60. Join Lantern Crew or found a named gang after four completed contracts and reputation 20; successful work builds gang standing. Reputation 30 unlocks faction broker trials.

Syndicate and Shinokami sponsorship requires reputation 50, three successful trials for that faction, gang standing three and heat below 30. Choose one permanent faction/branch commitment. Probation and promotions require 3/7/12/18 successful sponsor assignments, reputation 50/60/70/80 and heat below 30. Two failed sponsor assignments suspend work; reputation 50 and heat below 20 permit rehabilitation. Clubs, Hearts, Diamonds and Spades have distinct rank titles. Shinokami uses the authored Japanese ladder 見習い (Minarai), 構成員 (Kōseiin), 班長 (Hanchō), 隊長 (Taichō), 幹部 (Kanbu), with transliterations and English meanings. Takeo Mishima's supreme command remains a reserved story role.

Access and secrecy

Oculus employment is confined to public reception and reveals no criminal affiliation. Sponsor assignments use public receptions; recruitment grants no briefing permits, headquarters access, command authority or Ace identities. Existing Syndicate protagonists cannot replace their established roles with the newcomer ladder. Criminal activity stays in the private app journal; the public activity log receives only a generic notice.

Known limitations

Contracts are authored abstract decisions, not free-form heists or gang-territory simulation. Gang membership supplies standing and crew contracts; it does not create NPC contacts or change existing protagonist story leadership. Branch/faction switching is not implemented. Expired assignments must be withdrawn, with a displayed reliability or reputation penalty.

Validation

Passed ten Jobseek/Bubblegram unit tests including real save/load and story-clock advancement, every career, daily locks, promotions, contracts, sponsorship gates, all rank ceilings, rehabilitation and secrecy. Existing career (15), crime operations (7), Four Aces (4) and Syndicate cast (6) tests passed. The new phone UI smoke passed all sections, decisions, error, probation, dark control states and compact resizing. Rendered decision and probation screens were visually inspected. The full phone dark-theme smoke passed all 34 pages after correcting the new app callback signature.

## Save compatibility

Existing saves remain compatible. Restart the game to load the new Python code, then open either phone app. Progress is stored additively under job_apps; existing careers, faction permissions, contacts and story roles remain intact. Pending assignments and earned ranks survive normal save/load. No automatic recruitment or headquarters invitation is added.

## Evidence and historical limits

Implemented for the requested location-based careers and earned criminal pathways on 8 November 2026. Evidence comes from the listed implementation and executed tests; Japanese titles are authored game ranks rather than a claim about real organisations. Catalogue validation/export, six patch-note unit tests, patch-notes UI smoke and start-screen UI smoke also passed. Tests requiring temporary files used the workspace test directory after the system temporary directory denied access.

- job_apps.py
- job_apps_ui.py
- phone_ui.py
- phone_icons.py
- tests/test_job_apps.py
- tests/job_apps_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# The Crow: half-body portrait framing

release-2026-11-08-crow-half-body-portrait | Release | Art & media
Date: 2026-11-08

The Crow now uses waist-up framing matching the other character portraits.

## Details

Changed

Replaced the full-body Crow selection, headquarters and contact-profile artwork with a close half-body portrait, using Ivan’s headquarters portrait as a framing reference. The plague-doctor mask, concealed features, layered dark robes, embroidered cloth and metal accessories remain. View it in Ivan’s Contacts or when meeting The Crow at headquarters with current clearance.

Validation

All three installed PNGs are 1199 × 1312 RGBA with transparent and opaque pixels. The Crow rendering smoke passed; the rendered contact card was visually inspected. The full phone dark-theme smoke was run but stopped at Jobseek with a callback argument-count TypeError, after checking the preceding pages. This artwork change does not modify Jobseek code.

## Save compatibility

No save migration or gameplay changes. Restart the game to clear cached portraits.

## Evidence and historical limits

User-requested framing correction. Built-in imagegen edited the existing Crow portrait using Ivan only as a composition reference; installed without post-processing.

- assets/portraits/crow-selection.png
- assets/portraits/crow-syndicate.png
- assets/profiles/crow.png
- assets/portraits/crow-artwork.txt
- tests/the_crow_smoke.py
- tests/screenshots/crow-contact.png


---

# The Crow arrives at Syndicate headquarters

release-2026-11-08-the-crow | Release | Characters
Date: 2026-11-08

Meet the mysterious Cardmaster at headquarters; Ivan already has his private number.

## Details

Added

The Crow is a major, nonromantic character and an existing contact for Ivan. Other protagonists must have current headquarters authorisation and meet him there. This update does not grant headquarters clearance or add a promotion route. Meeting him does not grant his phone number: only established high-ranking officials (Ivan, Sylvanis and the Four Aces) qualify. Guest access, trust, closeness and manually entering a number do not bypass that restriction.

He remains at headquarters at every hour and cannot be summoned, taken on outings, or booked elsewhere. There is no discoverable home or public social account. His MBTI, birthday, age, height, true identity, tastes and personal history remain unknown at every disclosure level. Ivan, Sylvanis and the Aces work closely under him; Sylvanis shares respect and mutual tolerance while the Aces serve blindly. A masked plague-doctor portrait uses layered dark robes, cloth, gloves and metal accessories without exposing his features.

Validation

Four dedicated Crow tests passed, covering starting contacts, existing-save upgrades, authorised meetings without number access, rejected number guessing, schedules, travel restrictions unknown demographics and exclusion from automated Grove posts and photos. Seven phone-number tests and four Four Aces tests passed. Text and in-person AI prompts were built offline. The Crow phone smoke passed and its rendered dark contact card was inspected. The 32-page phone dark-theme audit passed. The broader hidden-cast suite reported failures in Valentina attraction expectations; the first run also encountered sandbox temporary-directory permissions, a workspace-temp rerun cleared those permission errors and left three Valentina attraction mismatches. Six patch-notes tests, catalogue validation/export, patch-notes UI smoke and start-screen UI smoke passed using workspace temporary files. No live AI dialogue was requested.

## Save compatibility

Existing saves receive The Crow and his headquarters presence automatically; Ivan receives his existing contact. Existing relationships remain intact. Restart the game to load the changed code. Stable phone numbers are preserved by appending his registry entry.

## Evidence and historical limits

Implemented from the user request and The Crow.md character reference. User-specified mystery boundaries take precedence over dossier claims about abilities and personal traits. Built-in imagegen created the portrait; automated checks and local rendered inspection provide implementation evidence.

- the_crow.py
- hidden_cast.py
- world_loop.py
- phone_numbers.py
- conversation_lore.py
- four_aces.py
- tests/test_the_crow.py
- tests/the_crow_smoke.py
- tests/screenshots/crow-contact.png
- assets/portraits/crow-selection.png
- phone_apps.py
- grove_photos.py
- grove_reactions.py
- assets/portraits/crow-artwork.txt


---

# Remove automatic headquarters invitations

release-2026-11-08-hq-invitations-removed | Release | World
Date: 2026-11-08

Knowing Sylvanis no longer grants entry to Syndicate headquarters.

## Details

Changed

Removed Ask Sylvanis for a headquarters invitation from location controls. The old request function now rejects attempts without changing the save. Headquarters access is limited to established members: Ivan, Valentina, Sylvanis and the Four Aces. Contact, friendship and local briefing passes do not grant headquarters access. Each passenger is checked independently. No replacement recruitment system is introduced.

Existing saves

The legacy automatic guest list is removed during world reconciliation. Nonmembers saved at headquarters, or travelling there, return to the public waterfront offices with that journey cleared. Established members retain access and their location. Historical conversations remain history, not active permission.

Validation

The focused headquarters access test passed, covering refusal after meeting Sylvanis, save/load revocation, relocation, rejected return travel and retained member permissions. Six faction-work tests passed. Dark-theme checks across 32 phone pages and patch-note UI smoke passed.

## Save compatibility

Restart to apply. Old automatic HQ invitations are intentionally revoked on load/world reconciliation. Unauthorised occupants return to syndicate_office. Other progress and established membership remain unchanged.

## Evidence and historical limits

Implemented following the explicit correction that Sylvanis should not casually hand out HQ invitations.

- hidden_cast.py
- world_loop.py
- town_ui.py
- tests/test_hidden_cast.py
- README.md
- Mysterious Hearts - Worldbuilding.md


---

# Sylvanis: the Crazed Demon

release-2026-11-08-sylvanis-crazed-demon | Release | Characters
Date: 2026-11-08

Sylvanis now carries the volatile cruelty, terrifying intelligence and authority of the Syndicate’s Coloured Joker Card.

## Details

Changed

Reworked his character profile, speaking guide, layered conversation references and personality traits. Fighting is one diversion within an appetite for chaos and social collapse. The portrayal now emphasises theatrical sadism, abrupt shifts into lucid menace, deliberate cruelty and unpredictable mercy. His private canon identifies the Crazed Demon as the most feared individual in the world, second-in-command above the Four Suits, with a partner-like arrangement with the Cardmaster. Updated the headquarters invitation and default follow-up.

Access

Meet Sylvanis through the existing arena or riverside encounters, or speak/message him through an established contact. Ivan retains his existing professional connection. Rank and private leverage still follow disclosure boundaries; familiarity does not grant romance or redemption. Invitations and player decisions still follow game state. Source-story future events have not been imported into Winterfield.

Validation

Ran 50 tests across hidden-cast, conversation-lore, Syndicate-cast, personality-types and Vendetta-lore suites with workspace temporary storage. Conversation-lore, Syndicate-cast and Vendetta-lore suites passed. Four failure reports remain in unrelated checks: three Valentina attraction expectations and one missing Four Aces personality-profile coverage check. Six patch-note tests passed. Initial runs using the sandbox default temporary folder encountered permission errors; workspace temporary storage resolved those errors. Catalogue validation and Markdown export completed successfully. No live AI conversation was requested; generated performance still depends on the dialogue model.

## Save compatibility

Restart the game to load the updated Python and cached references. Existing saves, contacts, invitations and histories remain compatible; prior dialogue is not rewritten. No migration required.

## Evidence and historical limits

Implemented from the user’s requested portrayal and the supplied Syndicate Joker Cards.md dossier; source continuity treated as reference, not instructions or automatic AU events.

- hidden_cast.py
- dialogue_styles.json
- personality_types.py
- Mysterious Hearts - Character References.md
- Mysterious Hearts - Worldbuilding.md
- tests/test_conversation_lore.py
- tests/test_hidden_cast.py
- tests/test_syndicate_cast.py
- tests/test_personality_types.py
- tests/test_vendetta_lore.py


---

# Distinct home interiors for the Four Aces

release-2026-11-08-four-aces-home-art | Release | Artwork
Date: 2026-11-08

Four illustrated civilian home backgrounds replace the generic backdrop at the Aces’ residences.

## Details

Added

Martos’s orderly walnut-and-slate apartment includes his watch-restoration desk, substantial seating, training weights and rice pot. Elias’s screened penthouse features scripts, film-score records, tea and a clear rehearsal area. Mavis’s compact private room has blackout curtains, a headphone repair desk, field recorder and low daybed. Camila’s forest-green and burgundy apartment includes fountain pens, a chess table, parquet dance space and a tall mirror. Each scene is an opaque 1672 × 941 landscape illustration with space for character portraits. No people, masks, card insignia or visible criminal records disclose their Ace identities.

Access

Visit an Ace’s home after unlocking their private address through the existing relationship controls. The existing location-art resolver automatically loads the new backgrounds for martos_home, elias_home, mavis_home and camila_home. Text conversations keep the phone backdrop. The new images do not grant home access or establish a registered identity or address for Mavis.

Validation

All four generated images were visually inspected. Verified file dimensions, location-to-asset resolution, day/night image loading, unchanged texting backgrounds and continued locked-home visibility in a fresh Ivan story. This is an asset-only change; no new UI layouts, controls or gameplay rules were introduced.

## Save compatibility

No save migration or reset is required. Restart the running game to clear any cached backdrop; existing home unlocks and relationships are unchanged.

## Evidence and historical limits

Created from the user’s request for the Four Aces’ home images and the existing authored interiors. Four separate built-in image_gen calls; exact prompts saved beside the installed assets. Source output images retained in the generated-images directory.

- assets/ui/locations/martos_home.png
- assets/ui/locations/elias_home.png
- assets/ui/locations/mavis_home.png
- assets/ui/locations/camila_home.png
- assets/ui/locations/martos_home.prompt.txt
- assets/ui/locations/elias_home.prompt.txt
- assets/ui/locations/mavis_home.prompt.txt
- assets/ui/locations/camila_home.prompt.txt
- artwork.py
- four_aces.py


---

# Faction shifts and joint on-site assignments

release-2026-11-08-faction-shifts-joint-work | Release | World
Date: 2026-11-08

Meet on-duty characters at faction sites and review requests together without exposing secret ranks.

## Details

Added

Seven existing characters gain authored site shifts. Martos and Camila attend Oculus on weekdays, 09:00-11:00 reception then 11:00-17:00 controlled offices. Elias attends Aster publicity appointments on weekdays, 14:00-17:00. Valentina reviews Breakwater field operations 10:00-13:00. Ivan rotates five Syndicate branches 16:00-18:00 and Sylvanis rotates operational reviews 10:00-12:00. Each Ace has a staggered branch appointment 18:00-20:00; existing rotating headquarters appointments remain. These are AU schedule additions, not new memberships. The player remains under player control. Sleep, agreed plans, parties and existing appointment priorities can affect attendance.

Access and interaction

Use ordinary map travel and the in-person scene. NPCs approach through the frontage and reception; the existing per-person gate checks restricted-room entry. On-duty characters count as working for autonomy. Talk / hang out remains available through the ordinary nearby-person controls. Review request with a present colleague starts a joint assignment using the existing cases and rewards. A command-authorised player can discuss mandates with informed colleagues in private. Pending joint assignments persist through save/load. A colleague must still be present, cleared and on duty at resolution; otherwise wait for them or abandon the assignment. No extra reward or automatic promotion is granted. Both participants retain a record of the witnessed result; other characters do not inherit it.

Privacy

Public activity descriptions use civilian work or private appointments, not Ace titles. Presence does not confirm faction ownership or rank. Named Ace mandate discussions reject uninformed listeners both when started and resolved. Remote restricted-room arrival messages are suppressed from the world log. Map/location visibility and existing audience-specific dialogue boundaries remain. Shinokami supervisor activities remain available; no named character is reassigned to Shinokami simply because they have an Awakening or former connection.

Validation

Six faction-work tests passed: shifts, rank limits, real clock-driven staged arrivals, denial paths, party preservation, private map/log visibility, joint save/load, shared records, one-time pay, absent/off-shift colleagues, uninformed listeners and public cover. Seven operations, four Four Aces, 27 conversation-lore and five Vendetta-lore tests passed. Joint-work and operations UI smokes passed; command and public-cover screenshots were visually inspected. Dark-theme smoke across 32 pages, patch-note UI and start-screen smoke passed. Test-environment sound-load warnings remain. No live AI conversation was requested or tested.

## Save compatibility

Restart to load code. No reset or migration required. Existing characters follow revised routines as world time advances, subject to existing plans. Optional colleague fields are added to new joint assignments; old assignments remain valid. Existing access, discoveries, money, relationships and progress are preserved.

## Evidence and historical limits

Implemented and locally verified for the requested role-based site attendance, shared crime activities, clearance and Four Aces secrecy. Existing source hierarchy and civilian covers are retained.

- faction_work.py
- world_loop.py
- autonomy.py
- crime_operations.py
- crime_sites_ui.py
- presence_ui.py
- town_ui.py
- tests/test_faction_work.py
- tests/faction_work_ui_smoke.py
- README.md


---

# Ivan’s automatic Black and White Joker uniform

release-2026-11-08-ivan-joker-uniform | Release | Characters
Date: 2026-11-08

Ivan automatically wears his masked Syndicate uniform at headquarters, including when player-controlled, and resumes civilian clothing on departure.

## Details

Added

A transparent Black and White Joker portrait: black ceremonial coat and hood, white mantle and sash, silver accessories and an opaque monochrome Joker mask. Generated with built-in image_gen; the exact prompt accompanies assets/portraits/ivan-syndicate.png. Both character reference sheets document the costume.

Behavior and access

Travel to Syndicate underground headquarters as Ivan, or encounter him there. The in-person portrait automatically uses the uniform, overriding a manually selected player outfit while inside. On departure normal outfit selection resumes. The civilian wardrobe preference is never overwritten. Loading a save already at headquarters applies the uniform immediately. Profile and phone previews remain separate from current in-person appearance. Scene descriptions conceal features behind the mask and no longer simultaneously claim the player is wearing the saved civilian outfit. Camera defaults and Ivan’s shutter-time outfit also use the headquarters uniform while inside.

Validation

Six Syndicate cast tests cover contact/access regression, transparent assets, appearance and player travel into/out of headquarters, saved wardrobe preservation and save/load. Render smoke verifies six uniforms, player portrait precedence and restored civilian imagery; the rendered screenshot was inspected. The 32-page phone dark-theme smoke passed. The camera suite passed 12 of 13 tests; its Theo town-NPC dating-photo test failed because the current scene returns no Theo companion. That unrelated dating fixture was not changed. Existing sound-loading warnings occurred in UI smoke runs.

## Save compatibility

Restart to load the artwork and code. No save migration or reset is needed. Existing saved civilian outfit choices are retained and automatically resume outside headquarters; saves loaded inside headquarters render the uniform.

## Evidence and historical limits

Implemented from the user’s explicit request to include player-controlled Ivan in automatic headquarters uniform switching. Generated and visually reviewed in this update; no live image or dialogue API calls were needed for the gameplay tests.

- four_aces.py
- game.py
- social_world.py
- camera.py
- assets/portraits/ivan-syndicate.png
- assets/portraits/ivan-syndicate.prompt.txt
- tests/test_syndicate_cast.py
- tests/syndicate_uniform_smoke.py
- Mysterious Hearts - Character References.md
- Mysterious Hearts - Character Appearances.md


---

# Crime sites use ordinary map locations

release-2026-11-08-sites-normal-locations | Release | Interface
Date: 2026-11-08

Visit site map markers normally and use their activities in the standard in-person scene.

## Details

Changed

Select a site marker in Maps and use Travel here, or use the normal destination controls. Return to In person to inspect the frontage, enter reception, request clearance and enter controlled rooms. The separate city-site browser, cross-city selector and dedicated Maps shortcut have been removed. Site actions now sit alongside ordinary location and nearby-person controls, with the existing scene artwork and title. Room-specific buttons appear where relevant.

Preserved

All eight public frontages and sixteen enterable rooms, interior/exterior artwork, anonymous discovery labels, Oculus secrecy, individual and companion access checks, permit expiry, pressure suspension, faction command authority, assignments, rewards, history and saved progress remain. Public-record research is available at the archive and exhibit verification at Interpol; each desk lets you choose an identified site. Ordinary travel remains available from any room.

Validation

Seven operations and six discovery tests passed. Updated UI smokes passed for ordinary map travel, all eight illustrated receptions, restricted entry errors, assignments, command decisions, local research/verification, map label refresh, leaving to unrelated locations, compact layouts and phone reopening. Main-scene screenshots were visually inspected. Dark-theme smoke across 32 pages, patch-note UI and start-screen smoke passed. Sound-load warnings remain in the test environment.

## Save compatibility

Restart to load the new interface. No save migration or reset. Existing locations, discoveries, permits, assignments, progress and faction rules are retained.

## Evidence and historical limits

Implemented following the request to make these ordinary visitable map locations while retaining interiors, access controls and crime systems.

- crime_sites_ui.py
- presence_ui.py
- phone_map.py
- town_ui.py
- tests/crime_sites_ui_smoke.py
- tests/crime_operations_ui_smoke.py
- README.md


---

# Ivan’s contacts and Syndicate headquarters uniforms

release-2026-11-08-syndicate-contacts-uniforms | Release | Characters
Date: 2026-11-08

Corrects Ivan’s initial contacts, focuses Ace/Joker conversations on Syndicate work and adds masked headquarters uniforms and affiliate clearance.

## Details

Fixed

Ivan previously seeded every hidden cast member as met and automatically received their phone contacts; several other residents also received acquaintance defaults. His starting contacts are now Garrett, Rei, Minsu, Valentina, Sylvanis and the four Aces. Open Phone > Contacts or Messages as Ivan. Sylvanis is explicitly included. Existing stories remove unearned legacy starting contacts while retaining recorded conversations, in-person meeting status, home discoveries, group history and explicit number exchanges. A one-time migration marker prevents repeated resets.

Changed

The four Aces and Sylvanis primarily discuss Syndicate assignments, reports, briefings, obligations and professional disagreements with Ivan. They avoid initiating personal talk, hobbies, flirting and casual invitations. Personal questions are briefly deflected. Suggested replies follow the same professional emphasis, including personal-talk suggestions. Outsiders in a mixed group do not gain access to operational details. No generated dialogue was tested against a live provider.

Added

Five transparent headquarters uniform portraits. Each Ace wears a white hood and layered robe, cloth, accessories and an opaque full-face mask bearing Clubs, Hearts, Spades or Diamonds. Sylvanis wears a dark hooded Coloured Joker uniform. In-person portraits at Syndicate underground headquarters automatically select these costumes; elsewhere, and on phone contact cards, civilian imagery remains. In-person appearance context conceals face, eyes, hair and tattoos behind the mask. Outsider profile galleries do not expose the secret costume variants. White clothing is image content; phone UI surfaces remain dark.

All four Aces have operational clearance for every Syndicate affiliate reception and briefing interior, including Oculus. Ordinary frontage/reception travel prerequisites still apply. Clearance does not transfer to guests, extend to Shinokami sites or grant Suit command authority.

Validation

Five new contact/migration/business/access/uniform tests passed, along with four existing Four Aces tests, 27 conversation-lore tests, seven crime-operations tests and seven phone-number tests. An older lore fixture now explicitly introduces Emily to Ivan before testing her dialogue. Uniform/contacts render smoke passed and screenshots were visually inspected. The 32-page dark-phone smoke passed. Sound loading emitted existing environment warnings. Built-in image_gen produced the five transparent assets; exact prompt files accompany them.

## Save compatibility

Restart and reload the story. A one-time Ivan contact migration removes blanket-seeded strangers and preserves recorded later connections. Existing stories with undocumented meetings cannot distinguish those meetings from old seed flags; explicit meeting, conversation and contact-exchange evidence is retained. No player saves were manually rewritten. Costume switching and Ace clearance are derived from current code and location.

## Evidence and historical limits

Implemented from the user’s follow-up request on 8 November 2026. Generated artwork and checks belong to this update. Earlier Four Aces notes describe the prior implementation; this entry records the corrected initial-contact rule and new costumes.

- hidden_cast.py
- town.py
- four_aces.py
- crime_sites.py
- crime_operations.py
- game.py
- social_world.py
- character_appearance.py
- profile_ui.py
- suggestions.py
- groups.py
- game_core.py
- tests/test_syndicate_cast.py
- tests/syndicate_uniform_smoke.py
- Mysterious Hearts - Character References.md
- Mysterious Hearts - Character Appearances.md


---

# City-site interactions move out of the phone

release-2026-11-08-city-sites-main-screen | Release | Interface
Date: 2026-11-08

Explore interiors and perform physical activities in the main in-person game screen.

## Details

Changed

Open In person > Explore city sites, or Explore city sites in the location controls. The Maps shortcut now explicitly opens the main screen and hides the phone. Reception entry, briefing access, clearance requests, assignments, evidence visits and travel controls are hosted in the main game content area, even when the phone was open. A Back to location button returns to the ordinary scene without moving the character. The larger scrollable layout uses wider text and taller interior artwork.

Validation

City-site and operations UI smoke checks passed, including all eight interiors, locked access, assignments, main-screen parent assertions, hidden phone, no phone dialogs, dropdown and compact states. Main-screen screenshots were visually inspected. Dark-theme smoke passed across 32 phone pages; patch-note UI and start-screen smoke passed. Test-environment sound-load warnings remain. No gameplay clearance or reward rules changed.

## Save compatibility

Restart to load the interface change. Existing saves, locations, permits, pending assignments and progress remain compatible; no migration or reset required.

## Evidence and historical limits

Implemented in response to the correction that in-person systems should not use the phone window. Existing main-area lifecycle is reused.

- crime_sites_ui.py
- presence_ui.py
- town_ui.py
- phone_map.py
- tests/crime_operations_ui_smoke.py
- tests/crime_sites_ui_smoke.py
- README.md


---

# Enterable crime sites and faction assignments

release-2026-11-08-crime-interiors-hierarchy | Release | World
Date: 2026-11-08

Enter eight illustrated sites, earn personal briefing clearance and handle disputes under Syndicate and Shinokami authority.

## Details

Added

Open Phone > Maps > City sites · Field notebook. Travel to a public frontage, enter reception and choose a packet-review assignment. Each of the eight sites has a reception and controlled briefing room, with one generated 1536×1024 interior illustration shared by those two areas. Artwork has no public faction labels and appears only for the current interior. The map locates indoor visitors at the building.

Access

Responsible reception work on two distinct story days qualifies a visitor for a personal, site-specific 1,440-story-minute briefing pass. Every companion needs their own clearance; direct destination calls cannot bypass the gate. Expiry or local pressure reaching 15 returns visitors to reception on clock progression/load. Documenting reception paperwork lowers pressure by 3 and restores still-valid permits below 15. Oculus refuses operational passes to ordinary visitors; its affiliation remains restricted. Passes grant neither membership nor command access. Existing Syndicate headquarters invitations remain separate.

Hierarchy and activities

Ivan and Sylvanis have cross-branch Syndicate command authority. Valentina commands Clubs field work at Breakwater; her generalship is not universal departmental clearance. No playable protagonist automatically joins Shinokami, including Neo. Takeo Mishima heads the Shinokami chain through AU regional and local supervisors. Syndicate Aces are Crow-assigned mission specialists rather than Suit leaders. Command disputes go through Ace mandates and objections to the Crow; Oculus uses a Diamonds liaison, not a fifth Ace.

Briefing disputes cover coercive records demands, cargo, consent paperwork, intimidation, media pressure, conflicting payments, customer access and unjustified address requests. Choices hold/document a request, approve it or escalate it. Saved standing, pressure, unresolved harm, evidence and decision history reflect the result. Reception/briefing/command decisions pay $80/$160/$240, except escalation pays nothing. One completion per site per story day prevents repeated reward claims. Pending assignments survive saving and can be abandoned. NPC dialogue receives only the speaker's own recorded work history.

Validation

Seven operations tests passed, including all eight artwork dimensions and indoor map positions, entry and companion gates, scoped pass expiry, pressure suspension/recovery, Oculus restrictions, saved pending orders and reward replay prevention. Six crime-site tests, 27 conversation-lore tests and five Vendetta-lore tests passed. The new operations UI smoke exercised all eight receptions, locked errors, assignments and compact command decisions; reception and assignment screenshots were visually inspected. City-site UI smoke, dark-theme smoke across 32 pages, patch-note UI smoke and start-screen smoke passed. Sound assets emitted load warnings. The broader map unit suite had four passing cases and one failure for four new character homes without coordinates; the map UI smoke stopped at a public-venue title assertion. These broader checks are not claimed as passed.

Limits

Activities are authored decision encounters, not tactical combat or a faction-promotion simulator. Reception and briefing use the same site illustration. Escalations record a pending response rather than inventing a reply from leadership. No live AI dialogue was tested.

## Save compatibility

Restart to load code and artwork. Existing stories retain relationships, discoveries, money and HQ invitations. Operations add per-character progress, permits, history and pending assignments on first use; no reset is required. Expired or suspended briefing clearance returns an occupant to reception.

## Evidence and historical limits

Implemented and locally verified for the requested enterable locations, interior artwork, controlled access and faction hierarchy gameplay. Reference dossiers inform hierarchy; local supervisor roles and assignment cases are authored AU additions.

- crime_operations.py
- crime_sites_ui.py
- crime_sites.py
- town.py
- world_loop.py
- game_core.py
- hidden_cast.py
- artwork.py
- phone_map.py
- social_world.py
- assets/ui/locations/crime-interiors-prompts.json
- tests/test_crime_operations.py
- tests/crime_operations_ui_smoke.py
- README.md
- Mysterious Hearts - Worldbuilding.md


---

# The Four Aces join the main cast

release-2026-11-08-four-aces | Release | Characters
Date: 2026-11-08

Meet Martos Cabrera, Elias Braun, Mavis Kuro and Camila Lopez, with civilian covers, private Syndicate roles, portraits and contacts.

## Details

Added

Four main characters use the existing major-character system: Martos Cabrera (Clubs, ISTJ, 201 cm), Elias Braun (Hearts, ENFJ, 181 cm), Mavis Kuro (Spades, ISTP, 158 cm) and Camila Lopez (Diamonds, ENTJ, 168 cm). Each has authored adult demographics, everyday favourites, hobbies, likes, dislikes, texting style, a private residence, a stable fictional phone number, a transparent portrait and a separately generated contact photo. Reference and appearance sheets include their details. Mavis has no registered identity, public employer or known birthday; her phone is a private contact line.

Access

Start or load an Ivan story and open Phone > Contacts or Messages. Only Ivan starts with all four contacts. Other protagonists must discover them through ordinary encounters or contact exchange. Martos and Camila work downtown at Oculus as security head and CFO; Elias rehearses at the studio; Mavis has no day job and spends daytime at the wetlands. On staggered days each has a private headquarters appointment from 20:00 to 22:00, once per four-day rotation, subject to travel and active plans. Existing headquarters clearance rules still apply.

Private canon

The civilian occupations are fronts for their primary Syndicate work. The Aces are Cardmaster task specialists, not Suit commanders. They know Ivan and Sylvanis through private work. Audience-specific context distinguishes informed private conversations from outsiders and mixed groups; high trust alone does not reveal an Ace identity. Rage, Pyromovement, Mist and Analysis are authored ability lore, not new combat mechanics. Public bios and artwork do not display Ace titles or suit symbols.

Validation

Four focused tests cover initial contact restrictions, old-save migration, private context, schedules, phone numbers and image alpha. Conversation lore (27 tests), Vendetta lore (5 tests) and patch notes (6 tests) passed. Patch-note catalogue validation/export, patch-note UI smoke and start-screen smoke passed. Temporary-file checks used the workspace test directory because the sandbox’s default temporary directory denied access. The dark-theme smoke checked 32 phone pages plus chat, contacts and embedded controls. All four contact cards were visually inspected; contact/message smoke passed on rerun after an intermittent existing PhoneButton event callback during the first run. Sound assets emitted load warnings in the test environment. The broader hidden-cast suite was interrupted during its slower dating case after four cases passed; it is not claimed as fully passed.

Limitations

No live AI conversation was requested or tested. Secrecy is encoded in public-data separation and dialogue instructions, not a new deterministic reveal system. The update does not add playable protagonist selection or a bespoke romance quest for the Aces.

## Save compatibility

Restart the game to load the new code and artwork. Existing stories acquire missing cast records, contacts for Ivan, schedules and professional bonds on load; existing progress, numbers and discoveries are preserved. Other protagonists do not gain their contacts automatically. No reset is required.

## Evidence and historical limits

Implemented from the user request on 8 November 2026, with The Four Aces.md and The Four Aces2.md supplied as fictional lore references and the two Sims screenshots as appearance references. User-specified identities, jobs and heights take precedence over dossier anonymity. Additional adult details and art were authored for this update. Eight assets generated with built-in image_gen; prompt records accompany each asset. Checks listed above were performed in this update, not inferred from historical reports.

- four_aces.py
- hidden_cast.py
- world_loop.py
- autonomy.py
- vendetta_lore.py
- phone_numbers.py
- grove.py
- contact_profiles.py
- sexuality.py
- Mysterious Hearts - Character References.md
- Mysterious Hearts - Character Appearances.md
- tests/test_four_aces.py
- tests/four_aces_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Doober Eats artwork ready before you play

release-2026-11-08-doober-bundled-manhwa | Release | Phone & social
Date: 2026-11-08

All 80 Doober Eats dishes and drinks now include bundled manhwa-style illustrations, with no image generation during play.

## Details

Added

Created 80 individual food and drink illustrations with the built-in image generator: 20 each for Garrett’s Noodles, Mario’s Pizza, Campus Café and Riverside Kitchen. Art uses manhwa-inspired ink detail, shading, appetising highlights, dark table settings and dish-specific compositions. The PNG files, menu manifest and exact generation prompts are stored in assets/doober.

Changed

Open Phone → Doober Eats and choose a restaurant or search its menu. Artwork loads directly from the local bundle on every save and story day. Browsing no longer queues AI image requests, waits for image jobs or requires image-provider login. The Doober adapter has no worker or polling timer. Old save-specific image records are ignored for display but left intact. Prices, ordering, recipients and deliveries keep their existing behavior. Supafast continues using its existing image queue.

Failure behavior

Missing or unreadable images show an inline dark unavailable state without a generation retry or online fallback. A missing/unreadable manifest leaves the authored menu available without images. Artwork is matched against dish name/category so a renamed recipe does not display the previous dish. Future dishes need an authored asset and manifest entry.

Validation

Four Doober asset/compatibility tests passed, verifying all 80 distinct images decode, menu data stays intact, browsing does not mutate old saves or call generation, recipe changes invalidate mismatched artwork, asset paths stay confined and ordering retains pricing. The Doober UI smoke passed for all four restaurants at 430×740 and 560×780, search/empty states, day/save switching and missing/corrupt image states, with zero generation calls. All four restaurant artwork review sheets and rendered menu, search, empty and unavailable screenshots were inspected. The phone dark-theme smoke passed across 32 pages and embedded controls. Four Supafast image tests, its image lifecycle smoke and ten phone-app tests passed. Existing missing-sound warnings appeared in the dark-theme check; this update does not change audio.

Patch-note catalogue validation, all six patch-note tests, the patch-note UI smoke and the start-screen smoke passed; the Markdown export was refreshed. The initial patch-note test run encountered system temporary-directory access errors; rerunning with the workspace .test-tmp directory passed.

## Save compatibility

Restart the game to load the updated Python code. No new story or migration is required. Existing money, inventory, orders and relationships remain intact. Legacy generated food files and save records are retained but the menu now displays the shared bundled artwork.

## Evidence and historical limits

Implemented from the user’s request to pregenerate Doober Eats food art now in manhwa style instead of generating it in game. All 80 illustrations were generated in this update using the built-in image_gen tool, copied into the project and reviewed on contact sheets. Checks recorded above were actually run.

- doober_images.py
- supafast_ui.py
- assets/doober/manifest.json
- assets/doober/generation.json
- tests/test_doober_images.py
- tests/doober_images_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/test_supafast_images.py
- tests/supafast_images_smoke.py
- tests/test_phone_apps.py
- tools/doober_art_review.py


---

# Illustrated backgrounds for all eight city sites

release-2026-11-08-crime-site-artwork | Release | Artwork
Date: 2026-11-08

Eight individual illustrated exterior backgrounds now appear at the new city sites and in the field notebook once a site is known or visited.

## Details

Added

Generated eight distinct 1536×1024 opaque PNG backgrounds using the built-in image-generation tool: Kestrel Operations Centre, Pacific Relay Depot, Stillwater Research Annex, Breakwater Security Depot, Aster Media House, Meridian Capital Offices, Oculus Winterfield Campus and Greyglass Service House. The scenes use illustrated architectural detail, public sidewalk viewpoints and unobstructed foregrounds for character overlays. Blank signage and the absence of faction symbols preserve location discovery and Oculus’s secret affiliation. Original generated outputs were copied into the workspace without overwriting older art. The full prompt set and source-to-destination mapping are retained in assets/ui/locations/crime-sites-prompts.json.

Access and rendering

Travel to the corresponding site to use its new background through the existing scene-art loader. In Maps → City sites · Field notebook, the artwork appears when that site is known or is the current location; unfamiliar remote sites do not receive a preview. These outdoor scenes now receive the existing game-time lighting and rain/snow overlays. Notebook previews show the base illustration rather than pretending to be a live camera. Existing Syndicate headquarters art and discovery/entry rules are unchanged.

Validation

All eight generated scenes were visually inspected. File checks verified eight distinct valid PNGs, dimensions, the scene-art mapping and day/night rain rendering. The real city-site phone smoke passed; the actual public Oculus notebook screenshot was inspected with its image embedded in dark controls. The 32-page phone dark-theme smoke passed. Catalogue validation, six patch-note tests, the patch-note UI smoke and start-screen smoke passed. Portable patch notes were exported. Missing-sound warnings are pre-existing; audio was not assessed.

Limitations

These are static exterior illustrations with the existing lighting/weather treatments, not new interiors, animations, combat scenes or access permissions.

## Save compatibility

Restart to load new artwork and clear image caches. Existing saves and site discoveries remain intact; no migration or new game is required.

## Evidence and historical limits

Created with eight separate built-in image_gen calls for the user’s location-art request, copied into the project and visually inspected. Prompts specify public-facing architecture without faction spoilers. Checks listed above were performed in this update.

- assets/ui/locations/crime-sites-prompts.json
- artwork.py
- crime_sites_ui.py
- tests/crime_sites_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Unlabelled city sites, criminal fronts and Oculus

release-2026-11-08-criminal-city-sites | Release | World
Date: 2026-11-08

Explore eight unlabelled city frontages, discover public identities and verify faction evidence privately; Oculus’s Syndicate affiliation begins known only to Ivan, Valentina and Sylvanis.

## Details

Added

Eight new map and travel destinations: Kestrel Operations Centre (Shinokami’s local Winterfield headquarters), Pacific Relay Depot (supply base), Stillwater Research Annex (research front), Breakwater Security Depot (Syndicate Clubs), Aster Media House (Hearts), Meridian Capital Offices (Diamonds), Greyglass Service House (Spades), and Oculus Winterfield Campus (corporate affiliate). These specific Winterfield locations and their public records are authored AU additions inspired by the supplied Three Dragon Heads dossier. Headquarters here means a local operation, not a relocation of Mishima or global leadership.

Discovery and access

Open Maps → City sites · Field notebook, or City sites in Winterfield travel controls. Unfamiliar sites appear as numbered unlabelled markers. Undiscovered business names and internal keys do not reveal them in search. Travel to the public frontage and Inspect exterior to identify its public name. Read its operator record at the old town archive; then visit Interpol’s public desk to verify a published enforcement exhibit. Seven sites support that evidence sequence. Each stage requires location and prior evidence, repeated actions are rejected without duplicating progress, and a confirmed affiliation does not grant access or solve another case. Map labels retain public business names rather than exposing faction labels.

Oculus secrecy

Ivan, Valentina and Sylvanis initially know the Syndicate sites through their command roles, including Oculus’s secret affiliation. Other protagonists must identify the campus like other new sites. Oculus’s public filings never establish a criminal connection; Interpol’s public desk cannot verify one through this feature. Source-dossier institutional suspicions are not imported as NPC knowledge. Speaker-specific dialogue references and topic tables preserve this distinction. Player discoveries are private records, not information automatically shared with the cast.

Headquarters

The existing Syndicate underground headquarters remains under the waterfront offices, with its existing guest-list route. It is not duplicated. Valentina’s generalship now grants member entry alongside Ivan and Sylvanis. Every traveller, including companions, still requires individual permission. New sites are public frontages only; private offices, warehouses, laboratory and data wings are not new enterable interiors. Arrival does not start combat, raids, kidnappings or source-story events. No named ordinary locals are randomly spawned at the new sites.

Interface and saves

The field notebook uses the embedded phone window, themed combobox popup, scrolling content and inline errors. Map search, selected labels and rendered marker labels update after discovery. Read-only exploration does not initialise save records; the first recorded inspection adds a per-protagonist city_sites record. Existing story state, invitations and private HQ access remain compatible.

Validation

Six city-site tests, five map tests, 27 conversation-lore tests, five Awakened integration tests and the focused headquarters invitation/member test passed. The new real-Tk city-site smoke passed anonymous markers, inspection, wrong-place errors, public/insider Oculus views, the full evidence sequence, map label refresh, dropdown styling and compact sizing. Screenshots of public Oculus, insider Oculus and confirmed headquarters were inspected. Phone dark-theme checks passed 32 pages and embedded controls; the existing map smoke passed search, click, pan, zoom, live presence, compact layout, memory and travel. Catalogue validation, all six patch-note tests, the patch-notes UI smoke and start-screen smoke passed. The portable patch notes were exported. Audio checks were not performed; existing missing-sound warnings appeared.

Known limits

No new combat or restricted interior exploration is included. Only the public-exhibit chain implemented here establishes the seven non-Oculus affiliations. Knowing an organisation, possessing a Trait or raising relationship trust does not identify a site or grant entry. No live AI request was used for verification.

## Save compatibility

Restart to load the new locations and dialogue references. Existing saves need no reset; map markers appear immediately and discoveries persist additively per protagonist. Existing Syndicate invitations remain valid, and Valentina is now recognised as a member. No relationships, money, ongoing work or past discoveries are rewritten.

## Evidence and historical limits

Implemented from the user’s request for initially unlabelled criminal locations and an Oculus affiliation known initially only to Ivan, Valentina and Sylvanis. Supplied Three Dragon Heads material informed faction functions; specific local frontages and discovery exhibits are newly authored AU content. Reported checks were performed in this update.

- crime_sites.py
- crime_sites_ui.py
- town.py
- town_ui.py
- phone_map.py
- social_world.py
- hidden_cast.py
- Mysterious Hearts - Worldbuilding.md
- tests/test_crime_sites.py
- tests/crime_sites_ui_smoke.py
- tests/test_phone_map.py
- tests/test_hidden_cast.py
- tests/phone_dark_theme_smoke.py


---

# Awakened Winterfield and criminal obligations

release-2026-11-08-vendetta-awakened-au | Release | World
Date: 2026-11-08

Integrates Awakening, the unified UN government, Valentina’s generalship and nine crime-related career situations while preserving Mysterious Hearts as its own alternate universe.

## Details

Added

Twelve established characters are Awakened: Neo, Tyler, Daniel, Garrett, April, Rei, Samantha, Sylvanis, Ivan, Valentina, Alyssa and Minsu. Emily remains potentially Awakened, with Critical Hit reserved for a future authored event. Sylvanis and Alyssa remain Blisk. Valentina is one of Ivan’s five generals, the Queen of Wind, with Deathwind; Minsu has a speed-and-reflexes Trait. Ability profiles enter speaker-specific dialogue context as private self-knowledge, not a public directory. Unknown Trait names are left unspecified. The world reference records qualitative AU limits and retained histories.

Changed

The former no-Awakened rule is replaced throughout live AI direction and world/character references. The unified United Nations government and Interpol Awakened Operations Division now exist alongside Winterfield local police and public liaison desks. Syndicate Suits, Aces, Jokers and the Crow, Conclave finance and antiquities, Shinokami coercion and experimentation, and Blackstone’s private Awakened-hunting remit are integrated with compartmentalised knowledge. Valentina knows Ivan’s rank through her command work, without automatically knowing his private leverage or funding history. Existing family boundaries, romances, everyday routines, Charles evidence and unresolved fates remain authoritative.

Play

Open Winterfield → Careers → Open work & ambitions → Work as Garrett, Ivan or Rei. Red Dragons work addresses conditional aid, witness privacy and shipment verification. Joker Card work addresses conflicting branch payments, publicity/provenance and coercive Awakened recruitment with Valentina. Iron Circle work addresses dangerous offers, injury concealment and private fighter information. Nine situations rotate by story day with two choices per session. Completed choices retain the existing craft, reputation, autonomy, team trust, fatigue and pressure effects. Exact situations, choices and a numerical effect snapshot appear in private History. Explicit sharing remains necessary; requests do not automatically resolve cases or establish medical treatment, recruits, attacks or bouts. New sessions snapshot their situations so later changes cannot rewrite pending choices; legacy active sessions retain their original three-situation definitions.

Validation

Five new integration tests, 27 conversation-lore tests, 15 career tests and three Neo tests passed. The expanded career UI smoke passed and captured all nine situations; actual screenshots of the generalship/recruitment, witness and injury choices were inspected. Phone dark-theme smoke passed across 32 pages and embedded controls. Initial temporary-file permission failures were resolved by using the workspace .test-tmp directory. The hidden-cast suite then completed four tests but retained three subtest failures in its remaining test: it expects Valentina’s base attraction 16 for all protagonists, while the existing romantic-type initializer yields 18 for Garrett and 11 for Rei/Minsu. No attraction code was changed. Catalogue validation, all six patch-note tests, the patch-note UI smoke and the start-screen UI smoke passed. The portable Markdown notes were refreshed. Missing sound warnings remain; audio was not assessed.

Known limitations

Abilities are canon and dialogue context, not new combat controls or a numerical power simulator. Emily’s awakening, source-story rescues, major attacks, defections and faction victories are not triggered by this update. Career choices record bounded work decisions and existing career statistics; they are not a full procedural criminal-world simulation. No live AI request was needed for checks.

## Save compatibility

Restart the game to load new Python and lore. Existing stories retain money, relationships, discoveries, histories, bookings and active work. Canon now includes Awakening and generalship, but no past conversation or player decision is rewritten; no new story is required.

## Evidence and historical limits

Implemented from the user’s explicit Awakened roster, Deathwind/generalship and unified-government request, adapting supplied Vendetta references while retaining Mysterious Hearts continuity. Tests and visual inspection described above were performed in this update; source story plans are not treated as played events.

- vendetta_lore.py
- conversation_lore.py
- ai_directions.txt
- Mysterious Hearts - Worldbuilding.md
- Mysterious Hearts - Character References.md
- Mysterious Hearts - RPG Game.md
- careers.py
- careers_ui.py
- tests/test_vendetta_lore.py
- tests/careers_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# In-person conversations become illustrated scenes

release-2026-11-08-illustrated-hangout-scenes | Release | Interface
Date: 2026-11-08

Hang out in a full-area location illustration with character portraits, speech bubbles beside the speakers, and centred italic narration.

## Details

Changed

Solo hangouts, group hangouts and town-resident conversations now use the main game area as an illustrated stage instead of the small artwork banner and separate scrolling dialogue/action windows. The stage reuses the existing location artwork, time/weather treatment and character portraits, including the player, selected wardrobe and custom protagonists. This update does not generate new artwork or change conversation generation.

Dialogue and narration

Your submitted spoken reply appears immediately in a blue slate bubble beside your portrait while the response is being written. Delivered character speech appears in a dark slate bubble pointing toward that character. The latest exchange remains on stage; earlier exchanges remain in Journal. Group conversations keep all participants on stage and show one character reply at a time, in response order. Use the Speaker arrows or click a character portrait to read their line. Right-click a portrait for its existing profile. Narration appears centred near the bottom in italic Georgia, above the response controls. Physical actions appear as narration rather than spoken dialogue. Long speech and narration have previous/next page buttons, including for unbroken text. Ordinary world refreshes retain the current reading position. Starting a new hangout does not replay a previous session or a phone-only message.

Controls and access

Restart the game, meet someone or choose hangout companions, then use In person. Speak and Actions tabs provide the existing custom replies and gestures. Personal talk, manually requested suggestions, date goals, wardrobe, cancellation, retry and End hangout remain available. Suggestions use a bounded scrolling area to leave room for the scene. A cancelled spoken reply returns to the reply input; a cancelled physical action returns to Actions without becoming spoken dialogue. Opening and closing the phone returns to the hangout. Full screen or F11 fills the display; Escape or Exit full screen returns to a normal window. The separate detachable conversation window has been replaced by this stage.

Validation

Ten hangout unit tests passed, covering scene speaker/session projection, pending speech, physical actions, continuation, long Unicode text paging, journal separation and texting restrictions. The new hangout-scene Tk smoke passed solo/group/local rendering, compact resizing, speaker and page selection, manual/personal suggestions, pending speech, a completed mocked response through real commit/poll handling, cancellation of speech and actions, phone return, full screen and ending. Inspected actual solo, compact, suggestion, group, local and long-narration screenshots. Manual-suggestions, park, start-screen and the 32-page phone dark-theme smoke checks passed. The patch-notes UI smoke passed using a workspace-local temporary folder after the default temporary-file path stalled. Catalogue validation and all six patch-note unit tests passed. The portable Markdown patch notes were refreshed from this catalogue.

Known limitations

A separate older phone-navigation smoke stops on its expected Writing response status label: the current phone reports delivery/queue status instead. That assertion was not changed and that run is not reported as passed. The dedicated new scene smoke independently verifies opening/closing the phone and returning to the exchange. UI runs still report pre-existing missing sound assets; audio was not assessed. Group replies are selected individually so long speeches remain readable; exceptionally large groups use abbreviated portrait nameplates while speech bubbles retain full names.

## Save compatibility

Restart to load the new interface. No migration or new story is required. Existing hangout histories, journals, relationships, choices and wardrobe selections are retained. Speaker/page selection and full-screen mode are presentation state and are not stored in story saves.

## Evidence and historical limits

Implemented for the request to replace in-person text windows with full-screen character artwork, adjacent speech bubbles and bottom-centred italic narration. Evidence includes actual Tk renders and interaction checks, isolated mock generation with real response commits, and executed regression checks. No live AI calls or player-save writes were used for validation.

- hangout_ui.py
- game.py
- town_ui.py
- tests/test_hangout_scene.py
- tests/hangout_scene_smoke.py
- tests/test_hangout_journal.py
- tests/test_hangout_texting.py
- tests/manual_suggestions_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Location exploration moves to the main game screen

release-2026-11-08-main-screen-location-exploration | Release | Interface
Date: 2026-11-08

Enter Riverside Park and use in-person location controls directly in the main game screen.

## Details

Changed

Removed Enter park from the phone map. After arriving at Riverside Park, the main In person overview offers Enter park · explore on foot. The same action is available in the main location-controls panel. Park rendering and movement controls are hosted in the main game content area, not a phone overlay or separate window. Opening a physical location view hides the phone; the phone map still provides ordinary travel.

Location controls

More location & relationship options now opens its existing travel, local activities and relationship controls in the main content area. A Back to location action restores the overview. Existing explicitly requested legacy TownWindow hosts remain compatible, but the game navigation uses the new main-screen panel. The In person top-bar action returns to the main view and hides the phone.

Exploration lifecycle

Arrow/A-D and on-screen movement, E interactions, focus-loss stopping and pixel-art layers remain available. Back, Esc and gate exits return to the main location overview. Ordinary game renders preserve the active park. Travel away or an in-person conversation closes it and cancels its animation callback. Missing artwork displays an inline error with a working Back control.

Access

Restart, travel to Riverside Park, then choose In person > Enter park. Use More location & relationship options for the main-screen location controls.

Validation

The park smoke verifies main-window parenting, absence of phone dialogs, entry from both overview and location controls, keyboard/on-screen input, focus stop, repeated game renders, resizing, Back/gate/travel/conversation cleanup, wrong-location rejection and missing-art state. Inspected main-screen park and location-controls renders. Three park unit tests, phone-map smoke, the 32-page phone dark-theme smoke, start-screen smoke and patch-notes UI smoke passed. The broader QOL smoke initially failed because world state advanced during its cancellation assertion; it passed with SimulationClock.tick held at zero, including the legacy town host. Existing missing sound warnings remain; audio was not assessed.

## Save compatibility

Restart to load navigation changes. No save migration or new story is required. Travel state, characters and relationships are preserved. Park walking position remains temporary.

## Evidence and historical limits

Implemented for the explicit instruction that in-person location entry and controls belong in the main game screen. Evidence is actual Tk parentage, inspected screenshots and executed interaction/lifecycle checks. QOL validation records the required clock isolation rather than claiming the original timed run passed.

- game.py
- presence_ui.py
- park_ui.py
- phone_map.py
- town_ui.py
- park_scene.py
- assets/world/park/README.txt
- tests/park_smoke.py


---

# Detailed pixel park and new Winterfield Commons artwork

release-2026-11-08-park-artwork-polish-and-commons | Release | Artwork
Date: 2026-11-08

The side-scrolling park gains detailed trees, woodland scenery and paving; Winterfield Commons gets its own new illustrated community garden.

## Details

Changed

Replaced the side-scrolling park’s simple tree shapes with imagegen-authored oak, autumn maple and willow sprites, detailed bark and clustered foliage. Added a lit gazebo, slatted iron-and-wood benches, ornate lamps, hydrangea hedges and flower beds. The woodland and distant landscape planes now include textured foliage, low hills, stone walls and town rooftops. The walking path has individually shaded stones, edge blocks, moss and scattered leaves; the pond has ripples and stone edging. The seven-layer layout, fixed dusk sky, world dimensions, camera rates, walkable baseline and movement controls are retained.

Winterfield Commons

Following the clarified request to generate a new image, replaced the old flat public-park placeholder with a full illustrated community garden containing mature trees, greenhouse, vegetable beds, fountain, benches and pavilion. This is newly generated artwork, not a recovered original. The Riverside park location illustration remains intact. The venue-art placeholder builder now skips public_park so it cannot overwrite this image. The previous Commons placeholder and prototype side-scroller planes are archived locally.

Access

Restart to clear cached location images. For the pixel park, Phone > Maps > Riverside park > Travel here > Enter park. For the illustrated Commons background, travel to Winterfield Commons · Public park and view the in-person location screen. Generated source images and exact prompts are saved under assets/world/park/source and assets/ui/locations/public_park.prompt.txt. Rebuilding park assets uses local source art via tools/build_park_assets.py and tools/build_park_polish.cjs; it does not regenerate AI images.

Validation

Park interaction smoke passed travel/entry, movement input, focus handling, resizing, interactions, teardown, gate exit and dark missing-art state, plus actual Commons scene loading. Three park model/render tests and six public venue tests passed. The 32-page phone dark-theme smoke, start-screen smoke and patch-notes UI smoke passed. Visually inspected playable park, pond and Commons screens. Exported layer dimensions were checked during assembly; scenery layers retain alpha transparency. UI runs logged pre-existing missing sound assets; audio was not validated.

Known limitations

The side-scroller remains a fixed-dusk prototype with Garrett as its test avatar. This update changes artwork, not encounter logic, movement rules or time-of-day behavior.

## Save compatibility

Restart to refresh cached location artwork. No save migration or new story is required. Player identity, relationships, travel and progress are unchanged. Park walking position remains temporary.

## Evidence and historical limits

Built-in image_gen created the environment atlas, woodland backdrop and new Commons illustration. Sharp packages and places the generated assets with code-native path and pond geometry. User clarified that Commons should receive a newly generated image. Evidence is preserved sources/prompts, runtime screenshots, asset checks and executed smoke/unit tests.

- assets/world/park/README.txt
- assets/world/park/layers.json
- assets/world/park/source/generation-prompts.txt
- assets/ui/locations/public_park.png
- assets/ui/locations/public_park.prompt.txt
- tools/build_park_polish.cjs
- tools/build_park_assets.py
- tools/build_venue_art.py
- tests/park_smoke.py
- tests/test_park_scene.py


---

# First playable side-scrolling park

release-2026-11-08-playable-side-scrolling-park | Release | Gameplay
Date: 2026-11-08

Enter Winterfield Park from Maps and walk a layered dusk trail with camera scrolling and local interactions.

## Details

Added

A 1600-pixel side-scrolling pedestrian trail with seven reusable scenery planes: fixed sky, distant hills and town silhouettes, woodland, pond and shrubs, nearby trees, the playable path, and foreground grass. Each plane scrolls at its own rate. The camera follows the walker and stops at the world edges. The park has lamps, benches, gates, a pond and an old oak. Scenery is deterministic code-native pixel artwork, exported as individual PNGs with a layer manifest.

Access and controls

Open Phone > Maps, search/select Park, choose Travel here, then Enter park. Entry is enabled only after arrival and outside a busy conversation. Walk with Left/Right or A/D, or hold the on-screen arrows. E or the context button inspects the pond/old oak, pauses beside the garden bench, or exits at either gate. Back or Esc also leaves. Movement resumes from a rest. Solid trail boundaries prevent leaving the playable ground.

Character and phone behavior

Garrett is explicitly labelled as the temporary test avatar for all player selections; player identity and relationships are not changed. His existing 24-frame left/right walk is matched to movement speed, with matching static idle poses exported from the same rig. Losing focus clears held controls. Resizing preserves dark phone styling and nearest-neighbor artwork. Leaving or changing phone apps cancels the animation callback. Missing artwork displays a dark inline message with disabled controls.

Validation

Three park model/render tests and five existing map unit tests passed. The park UI smoke passed actual map travel/entry, keyboard and on-screen input, focus-loss stopping, bench interaction, camera movement, two phone sizes, app-switch teardown, gate exit and missing-art handling. Dark control states were audited in the park, including its error state. The existing 32-page phone dark-theme smoke, map interaction smoke, start-screen smoke and patch-notes UI smoke all passed. Inspected rendered playable, pond, compact and error screens. UI runs logged existing unavailable sound assets; audio was not validated.

Known limitations

This is the first area prototype: a continuous walking trail without jumping, combat or NPC conversation encounters. Scenery uses a fixed dusk sky independent of story time. Exploring does not advance the story clock or award items. Walking position, camera and rest state reset on re-entry; normal map travel still uses the existing travel/save rules.

## Save compatibility

Restart the game to load the new map action and area code. No save migration or new story is required. Existing player identity, relationships, progress and travel state are retained. Local park walking position is session-only and resets on re-entry.

## Evidence and historical limits

Implemented for the request for a workable side-scrolling park with playable ground, multiple backgrounds and sky. Evidence includes exported scene planes, real phone map entry and interaction smoke checks, executed tests and inspected rendered screenshots. The existing Garrett artwork is used as an explicitly labelled prototype avatar.

- park_scene.py
- park_ui.py
- phone_map.py
- assets/world/park/README.txt
- assets/world/park/layers.json
- tools/build_park_assets.py
- tools/build_garrett_walk_v3.cjs
- tests/test_park_scene.py
- tests/park_smoke.py
- tests/phone_map_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Garrett fuller sprite arms

release-2026-11-08-garrett-fuller-arms | Release | Artwork
Date: 2026-11-08

Garrett’s slimmer-body walk preview now has fuller upper arms, forearms and hands.

## Details

Fixed

Increased rig upper-arm width from 3.5 to 4.5 logical pixels and forearm/cuff/hand width from 3.2 to 4.2, approximately 30 percent. Reuses existing artwork. The v4 torso, shoulder placement, head, leg motion and 24-frame timing are retained.

Access

Open assets/sprites/chibi-preview/garrett-v5/walk-right.gif and walk-left.gif. Transparent 48x64 frames, sprite sheet, manifest and checks are included. Rebuild using tools/build_garrett_walk_v3.cjs --fuller-arms. Prior versions are preserved.

Validation

Both 24-frame GIFs rebuilt with 960ms loop duration. Periodic state, stance translation, foot lift and leg reach checks passed. Full contact sheet visually inspected. Phone UI is unchanged, so phone smoke checks were not run.

Known limitations

External art preview only; not connected to map movement. Older idle assets have not been matched to this body. Left-facing costume details are mirrored.

## Save compatibility

No restart, migration or save changes required. Existing game behavior is unchanged.

## Evidence and historical limits

Adjusted existing animation-rig widths after feedback that the arms were too thin. Evidence is the rebuilt previews, inspected contact sheet and executed checks; no new image generation was needed.

- assets/sprites/chibi-preview/garrett-v5/README.txt
- assets/sprites/chibi-preview/garrett-v5/manifest.json
- assets/sprites/chibi-preview/garrett-v5/checks.json
- tools/build_garrett_walk_v3.cjs


---

# Garrett slimmer sprite proportions

release-2026-11-08-garrett-slim-profile-proportions | Release | Artwork
Date: 2026-11-08

A revised walk preview narrows Garrett’s torso and arms while preserving the 24-frame cycle.

## Details

Fixed

Replaced the wide body cutout with an imagegen-edited arm-free torso. Removed the baked-in sleeve that overlapped the animated arm, narrowed the chest and waist, moved shoulder joints inward and reduced sleeve/forearm widths. Head scale is fitted independently of the torso. Hip position, foot trajectories, 24-frame timing and mirrored left/right movement are retained.

Access

Open assets/sprites/chibi-preview/garrett-v4/walk-right.gif and walk-left.gif. The folder includes the transparent sheet, 48 individual frames, revised body source, exact imagegen prompt, manifest and check results. Rebuild with tools/build_garrett_walk_v3.cjs --slim. Earlier previews are preserved.

Validation

Rebuilt both directions and verified 24 frames each, 960ms total timing, periodic rig state, stance translation, swing foot lift and reachable leg targets. Visually inspected the complete updated contact sheet. Patch-note validation and tests are run for this entry; no phone UI surface changed.

Known limitations

Still an external cutout animation preview, not map-integrated movement. Earlier idle assets have not been restyled to this new body. Mirroring also reverses asymmetric costume details.

## Save compatibility

No migration, restart or save changes. Existing game behavior and earlier sprite previews are preserved.

## Evidence and historical limits

Created in response to feedback that the rig torso was too wide and disproportionate. Built-in image_gen edits the body; the existing animation renderer applies the narrower shoulder and arm proportions. Evidence includes the source asset, inspected contact sheet and executed animation checks.

- assets/sprites/chibi-preview/garrett-v4/README.txt
- assets/sprites/chibi-preview/garrett-v4/generation-prompt.txt
- assets/sprites/chibi-preview/garrett-v4/manifest.json
- assets/sprites/chibi-preview/garrett-v4/checks.json
- tools/build_garrett_walk_v3.cjs


---

# Garrett continuous 24-frame walk loop

release-2026-11-08-garrett-continuous-walk-loop | Release | Artwork
Date: 2026-11-08

Garrett now has 24-frame left and right walk previews with lifted swing feet and continuous stance movement.

## Details

Fixed

Replaced the eight independently drawn walk poses that appeared to plant/stomp with a 24-frame periodic cutout animation. Imagegen-authored reusable body parts keep the head and costume consistent. Two-joint legs alternate 60% stance and 40% swing, with a six-pixel raised-foot arc, counter-swinging arms, subtle body bob and heel/toe shoe pivots. Both directions loop over 960ms. Left mirrors the right, including asymmetric outfit details.

Access

Open assets/sprites/chibi-preview/garrett-v3/walk-right.gif and walk-left.gif. Includes 48 transparent 48x64 frame PNGs, a six-row sprite sheet, timing manifest, reusable parts, source atlas, generation prompt and reproducible build script. Earlier previews and v2 idle assets are preserved.

Validation

Both GIFs were encoded and checked for 24 frames and 960ms duration. Rig checks passed for reachable leg targets, constant stance-foot backward velocity, at least 5.9 pixels of swing lift, periodic state equality and a last-to-first foot displacement no larger than ordinary frame transitions. Inspected the enlarged frame sheet. Phone surfaces were unchanged; phone UI smoke tests were not run.

Known limitations

This is an external animation preview, not a map movement implementation. Suggested logical movement speed is approximately 24.31 pixels per second to match the stance motion; actual collision/movement behavior has not been tested. Cutout joints and pixel rotation may need further visual refinement.

## Save compatibility

No migration, restart or save changes are required for these external preview assets. Game code and existing stories are unchanged.

## Evidence and historical limits

Created after user feedback that the prior cycle looked like planted feet. Uses built-in image_gen for body-part artwork and deterministic skeletal animation for continuous motion. Validation evidence is the executed rig/encoding checks and inspected frame sheet.

- assets/sprites/chibi-preview/garrett-v3/README.txt
- assets/sprites/chibi-preview/garrett-v3/manifest.json
- assets/sprites/chibi-preview/garrett-v3/checks.json
- assets/sprites/chibi-preview/garrett-v3/generation-prompt.txt
- tools/build_garrett_walk_v3.cjs


---

# Garrett left and right sprite polish

release-2026-11-08-garrett-side-scroll-sprite-polish | Release | Artwork
Date: 2026-11-08

A revised Garrett preview adds matching left and right walk loops for planned side-scrolling map areas.

## Details

Changed

Regenerated Garrett with cleaner pixel styling and eight walk poses instead of six. Packaging aligns head centers and foot baselines at 48x64 pixels. Idle holds one open-eye pose between short blinks to reduce silhouette shimmer. Left-facing sprites mirror the right-facing artwork, including asymmetric clothing and accessories. Movement scope is left/right for side-scrolling areas; front/back sprites are not planned for this asset.

Access

Open assets/sprites/chibi-preview/garrett-v2/walk-right.gif and walk-left.gif; corresponding idle GIFs are included. A transparent four-row sprite sheet, 32 frame PNGs, timing/anchor manifest, source artwork and exact prompt are saved beside them. The first preview remains available in the sibling garrett folder.

Validation

Rebuilt all four GIFs and checked frame counts, frame height and total loop timing: eight walk frames over 800ms per direction; the idle encoder merges held frames into three frames over 2350ms. Inspected the enlarged contact sheet showing all four animation rows. Phone surfaces and game code were not changed, so phone UI smoke checks were not run.

Known limitations

Minor generated detail variation remains in walking and blinking. Actual foot sliding needs assessment against movement speed during integration. No map entry, collision or movement system is implemented in this artwork revision.

## Save compatibility

No save changes, migration or restart required to view external assets. Existing game behavior and saves remain unchanged.

## Evidence and historical limits

Requested sprite polish and left/right-only animation for side-scrolling map areas. Artwork generated with built-in image_gen; Sharp performs frame extraction, alignment, scaling, mirroring and GIF packaging. Checks reflect executed metadata validation and visual contact-sheet inspection.

- assets/sprites/chibi-preview/garrett-v2/README.txt
- assets/sprites/chibi-preview/garrett-v2/manifest.json
- assets/sprites/chibi-preview/garrett-v2/generation-prompt.txt
- assets/sprites/chibi-preview/garrett-v2/sprite-sheet.png
- tools/build_garrett_sprite_polished.cjs


---

# Garrett chibi pixel-art animation preview

release-2026-11-08-garrett-chibi-animation-preview | Release | Artwork
Date: 2026-11-08

A standalone right-facing Garrett style test includes looping idle and walk previews for the proposed freeroam artwork.

## Details

Added

A chibi pixel-art interpretation of Garrett based on his canonical blond hair, golden eye, neck tattoos, black tailoring and gold accessories. Includes six idle frames with a blink, six walk poses, transparent 48x64 PNG frames, a 288x128 sprite sheet, timing manifest, original generated sheet, exact generation prompt and a rebuild script.

Access

Open assets/sprites/chibi-preview/garrett/idle.gif and walk.gif to see the looping previews at 4x scale on dark slate. The contact sheet shows all frames. This is an external art preview only; map access and in-game character rendering are unchanged.

Validation

Built both GIFs and checked six frames per file, encoded frame durations, dimensions and PNG alpha presence. Visually inspected the enlarged twelve-frame contact sheet. No phone surface changed, so phone UI smoke checks were not run.

Known limitations

Generated frame-to-frame details and walk gait need final cleanup before production. Only the right-facing direction is authored. This does not implement freeroam, collision or map entry. The cast has not been converted.

## Save compatibility

No restart, migration or new story is required to view these external files. Game code and all existing saves remain unchanged.

## Evidence and historical limits

Created in response to the request to preview one existing character before converting the cast. Artwork uses built-in image_gen; Sharp packages the generated frames. Evidence is the saved assets, inspected contact sheet and successful encoding metadata checks. This entry records preview artwork availability, not a shipped gameplay system.

- assets/sprites/chibi-preview/garrett/README.txt
- assets/sprites/chibi-preview/garrett/manifest.json
- assets/sprites/chibi-preview/garrett/generation-prompt.txt
- assets/sprites/chibi-preview/garrett/sprite-sheet.png
- tools/build_garrett_sprite_preview.cjs


---

# Dedicated phone profile pictures for the outskirts neighbours

release-2026-11-08-outskirts-phone-profiles | Release | Artwork
Date: 2026-11-08

Eight new square close-up profile pictures now appear in phone contacts and messages.

## Details

Added

Dedicated square profile illustrations for Hazel Reed, Euan Marsh, Marta Silva, Jonah Price, Keiko Tan, Callum Webb, Beatrice Cole and Ravi Menon. Each preserves the identity, clothing and illustrated style of their transparent portrait, with a closer head-and-shoulders composition for small circular avatars. Softly blurred settings show the pine trail, tea room, orchard, pottery studio, marine centre, coast, railway museum and diner respectively. Generated with the built-in image_gen tool using the existing transparent portraits as identity references. Exact prompts, reference paths and generated source paths are recorded in assets/profiles/town-contacts-manifest.json.

Access

Restart the game, then view these residents in Phone > Contacts or open their existing Messages threads. Default avatars now load the dedicated profile pictures instead of the transparent portrait fallback. The transparent portraits remain unchanged for in-person scenes. Player-selected custom avatars retain priority. No new contact access is granted by the artwork update.

Validation

All eight images were visually inspected and confirmed square, opaque and at least 512 pixels. The updated town portrait smoke check passed for all 30 town NPCs, including avatar lookup and message identities; all eight new threads opened without callback errors. The rendered profile gallery, circular avatar crops and Hazel message header were visually inspected. The 32-page phone dark-theme smoke passed. UI runs reported unavailable sound assets; audio was not validated.

## Save compatibility

Restart to clear cached avatar images. No migration or new story is needed. Saved contacts, phone numbers, conversation histories, progress and custom avatar selections are preserved.

## Evidence and historical limits

Created for the explicit request for dedicated profile pictures used in phone contacts and messages. Evidence is the generated images, preserved prompts and references, executed smoke checks and inspected UI renders.

- assets/profiles/town-contacts-manifest.json
- assets/profiles/Hazel Reed.png
- assets/profiles/Euan Marsh.png
- assets/profiles/Marta Silva.png
- assets/profiles/Jonah Price.png
- assets/profiles/Keiko Tan.png
- assets/profiles/Callum Webb.png
- assets/profiles/Beatrice Cole.png
- assets/profiles/Ravi Menon.png
- tests/town_portraits_smoke.py


---

# Transparent portraits for the eight outskirts residents

release-2026-11-08-outskirts-transparent-portraits | Release | Artwork
Date: 2026-11-08

Hazel, Euan, Marta, Jonah, Keiko, Callum, Beatrice and Ravi now have individual transparent character portraits.

## Details

Added

Eight polished manhwa-style waist-up PNG portraits with genuine alpha transparency replace the initials placeholders for Hazel Reed, Euan Marsh, Marta Silva, Jonah Price, Keiko Tan, Callum Webb, Beatrice Cole and Ravi Menon. Clothing, skin tones, ages and hairstyles follow their authored appearances. All eight are registered in the town portrait manifest with exact generation prompts and source paths. Created using the built-in image_gen tool with transparent backgrounds requested directly.

Access

Restart the application and meet the residents at their usual public locations, then open an in-person conversation to see their portraits. The existing phone-avatar loader also uses these portraits when no separate contact photo or player-selected avatar exists. Their portraits are appearance references, not evidence of a live view or current outfit during texting.

Validation

The portrait smoke check passed for all 30 town NPC portraits, including PNG alpha extrema of 0 and 255, image dimensions, direct-name and slug lookup, phone avatars and message identities. All eight new phone threads opened without callback errors. The rendered eight-person gallery was visually inspected on dark slate. Six resident unit tests and the 32-page phone dark-theme smoke passed. UI runs reported missing sound assets; audio was not assessed.

Known limitations

Each new resident has one static portrait. Phone avatars reuse the portrait through the existing fallback rather than a separately generated contact photograph.

## Save compatibility

Restart to refresh image caches and updated appearance references. No migration or new story is needed. Contact numbers, conversations, relationships, routines and player-selected avatars are preserved.

## Evidence and historical limits

Created and integrated for the explicit request for transparent portraits of the newly added town NPCs. Evidence consists of generated PNGs, preserved prompts, executed checks and the inspected in-game-loader gallery.

- assets/portraits/town-residents-manifest.json
- assets/portraits/hazel-reed-selection.png
- assets/portraits/euan-marsh-selection.png
- assets/portraits/marta-silva-selection.png
- assets/portraits/jonah-price-selection.png
- assets/portraits/keiko-tan-selection.png
- assets/portraits/callum-webb-selection.png
- assets/portraits/beatrice-cole-selection.png
- assets/portraits/ravi-menon-selection.png
- town_residents.py
- conversation_lore.py
- tests/town_portraits_smoke.py


---

# Dedicated artwork for all twelve outskirts locations

release-2026-11-08-outskirts-location-artwork | Release | Artwork
Date: 2026-11-08

The new hills, Westbrook, coast and harbour destinations now have individual painted scene backgrounds.

## Details

Added

Twelve distinct wide landscape backgrounds replace the generic scene-art fallback at Pine Ridge woodland trail, North Ridge lookout, Hillside Tea Room, Westbrook community orchard, Westbrook farm shop, Old Mill pottery studio, Eastwatch coastal pier, marine discovery centre, lighthouse walk, South Harbour covered market, Southbank railway museum and riverside diner. Each image uses the existing semi-realistic anime background style with open foreground space for character overlays. Generated with the built-in image_gen tool; the exact prompt is stored beside each PNG as a .prompt.txt file. Existing artwork was not replaced.

Access and rendering

Restart the application and travel to any of the new locations from Phone > Maps or the town travel selector. The existing scene-art loader selects these assets automatically for venue previews and in-person scenes. Time-of-day tinting applies to all twelve; rain and snow overlays now apply to the five new outdoor locations. Interiors and the covered market remain sheltered.

Validation

All twelve generated outputs were visually inspected. Two targeted tests passed, covering unique landscape files, scene lookup, daylight/night rendering and outdoor-versus-indoor precipitation. All twelve scenes also passed the real Tk ArtCanvas smoke check, with daylight and rainy-night galleries inspected. The 32-page phone dark-theme smoke passed.

Known limitations

Lighting and weather variants use the existing tint/overlay renderer, not separately generated seasons or physically relit images. This update supplies location backgrounds; the eight new residents still use their existing portrait fallbacks.

## Save compatibility

No migration or new story required. Restart to refresh loaded artwork and rendering code. Locations, NPC routines, contacts, relationships and progress are unchanged.

## Evidence and historical limits

Created for the request to supply artwork missing from the newly expanded map. Current generated assets, saved prompts, executed tests and inspected renderer screenshots are the evidence.

- assets/ui/locations/pine_trail.png
- assets/ui/locations/ridge_lookout.png
- assets/ui/locations/hill_tea_room.png
- assets/ui/locations/orchard.png
- assets/ui/locations/farm_shop.png
- assets/ui/locations/pottery_studio.png
- assets/ui/locations/coastal_pier.png
- assets/ui/locations/marine_centre.png
- assets/ui/locations/lighthouse_walk.png
- assets/ui/locations/harbour_market.png
- assets/ui/locations/railway_museum.png
- assets/ui/locations/southbank_diner.png
- artwork.py
- tests/test_outskirts_art.py
- tests/outskirts_art_smoke.py


---

# Beyond central Winterfield: four districts and eight neighbours

release-2026-11-08-winterfield-outskirts | Release | World
Date: 2026-11-08

Explore 12 public destinations beyond the old map boundaries and meet eight everyday residents with their own routines.

## Details

Added

Northern Hills: Pine Ridge woodland trail, North Ridge lookout and Hillside Tea Room. Westbrook: community orchard, farm shop and Old Mill pottery studio. Eastwatch Coast: coastal pier, marine discovery centre and lighthouse walk. Southbank and Harbour: covered market, railway museum and riverside diner. All 12 destinations lie outside the former 0–1400 by 0–1100 camera area and support existing instant travel, companions, scheduled meetings and repeat-visit activities. Tea costs $5, seasonal juice $4 and a diner sandwich $8; other new visit actions are free. Outdoor activities respect adverse weather.

Meet Hazel Reed, Euan Marsh, Marta Silva, Jonah Price, Keiko Tan, Callum Webb, Beatrice Cole and Ravi Menon. Each has an adult biography, appearance reference, favourites, rotating conversation topics, weekday/weekend routines and a stable appended phone number. Public routines run from 08:00 until 22:00; outdoor locals shelter at the library in adverse weather. Existing town NPC conversation, familiarity and contact rules apply. Selected major characters can choose the new places during free time.

Access

Restart the game, load an existing story and open Phone > Maps > Fit town. Pan beyond the centre or search a destination name, select its pin and choose Drive here. The town travel selector also lists the new destinations. Visit during daytime to meet the new locals; Hillside Tea Room hosts Euan in the morning. Food and Outdoors filters include relevant new places. Fit town and drag/arrow navigation use destination-derived bounds instead of the old fixed limits.

Known limitations

New residents use existing initials/text avatar fallbacks, with authored appearance descriptions but no dedicated portrait images. New venues use the existing generic scene-art fallback. The map remains illustrative, with instant travel rather than distance-based journeys. No new romance routes or bespoke minigames are added.

Validation

83 targeted unit tests passed across outskirts, town, public venues, resident routines and conversation references, maps, phone numbers, leisure and saves. Map interaction smoke checks, 32-page phone dark-theme smoke checks and resident portrait/contact fallback checks passed; map overview and search renders were visually inspected. Save tests were run with a workspace-local temporary directory after the sandbox temporary directory denied writes. UI smoke runs reported unavailable sound assets; audio was not validated.

Patch-note validation, six patch-note unit tests, patch-note UI smoke and start-screen smoke also passed. Phone travel to Hillside Tea Room confirmed Euan present at 09:00; the arrival screen and updated overview were inspected.

## Save compatibility

Restart the running application to load changed code; no new story or manual migration is needed. Existing locations, contacts, numbers and chat histories are preserved. Eight numbers are appended. Resident routines and future leisure choices include the expansion; no past visits or relationships are fabricated.

## Evidence and historical limits

Implemented for the request to expand the playable map beyond its current area with more town NPCs. Evidence is current source, executed local tests and inspected screenshots, not a reconstructed historical release.

- outskirts.py
- public_venues.py
- town_residents.py
- phone_numbers.py
- phone_map.py
- leisure.py
- conversation_lore.py
- tests/test_outskirts.py
- tests/phone_map_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/town_portraits_smoke.py


---

# Custom portraits use the established character art style

release-2026-11-08-custom-portrait-style-references | Release | Artwork
Date: 2026-11-08

Custom portrait generation now includes existing character artwork as style references.

## Details

Fixed

Start screen > Create your own > Generate portrait now sends the Rei and Emily selection portraits to the existing in-game Codex image generator as style references. Previously the custom request used only a broad manhwa/anime description and asked for full-body framing. The updated request matches the existing head-to-upper-thigh composition, clean linework, softly blended cel shading, detailed hair and clothing, restrained highlights and adult proportions. Reference identity, face, hair, skin tone, clothing, tattoos and accessories must not be copied unless requested by the player. Gender and appearance fields still determine the new person. Transparent RGBA output remains required and validated. Missing reference assets fail through the existing generator validation instead of silently generating without references.

Validation

Visually inspected the existing Rei and Emily selection portraits and reviewed the reference-image forwarding in the Codex bridge. Passed 7 custom-protagonist tests and 11 Codex image-bridge tests. The custom request test now verifies both reference files are valid images and are passed to the generator, along with style-only instructions, matching framing, appearance data and transparency requirements. These are request-contract and local integration checks; no live portrait was generated in this audit, so the visual quality of a fresh generated result has not been certified. Generative output can still vary.

## Save compatibility

Restart the game to load the updated generator prompt. Existing saves and portrait files remain unchanged. New generation requests from the creator use the style references; an already accepted creator preview must be regenerated to receive this change.

## Evidence and historical limits

Audited and corrected for the request to check custom portrait art-style consistency. Existing reference art was visually inspected; generation calls were tested with mocked results.

- custom_protagonist.py
- codex_images.py
- tests/test_custom_protagonist.py
- tests/test_codex_images.py
- assets/portraits/rei-selection.png
- assets/portraits/emily-selection.png


---

# Create a Grove account and grow an audience

release-2026-11-08-custom-grove-accounts | Release | Phone apps
Date: 2026-11-08

Custom protagonists can choose a Grove handle and bio, edit their account, and gain followers through public activity.

## Details

Added

Open Phone > Grove as a custom protagonist to create an account. Choose a handle and a public bio, then press Create account. Handles are normalized to lowercase, accept an optional leading @, and must contain 3–24 letters, numbers, dots or underscores with a letter or number first. Handles already used by authored Winterfield residents are unavailable. Bios accept 1–280 trimmed characters. Validation errors stay in the dark form without creating a partial account. Setup scrolls on compact phones; Edit Grove account opens an embedded dark form. Edits retain followers, posts and pending growth.

Account identity

The chosen handle and bio appear in Grove, account listings and the profile gallery. Feed and comment author labels, notifications and conversation context resolve handles from the current story. Each custom story owns its account data; editing one story cannot change another or an authored character's profile. Custom characters must create an account before posting, replying, sharing photos or liking photos. Public content is still retained, including posts made in older custom saves.

Follower growth

Accounts begin with zero followers. Eligible text posts earn 4 followers and photo posts earn 6, plus 1 per existing 100 followers up to a 5-follower bonus per original post. Replies to another author earn 1. Followers arrive gradually over the next 1,440 minutes of game time, with progress shown on the Grove page. At most 3 original posts/photos and 5 replies per story day earn growth. Duplicate credited content, repeated processing of the same post, replies to yourself, likes, account edits and feed refreshes do not add growth. Inactivity after credited growth finishes yields no extra followers. Reloading or rewinding the clock cannot award the same growth again. Followers are an anonymous audience and do not create contacts, friendships or romantic familiarity.

Compatibility and limits

Authored protagonists retain their established handles, bios and follower counts. Custom stories created before this update receive the setup form on opening Grove; existing posts are preserved and do not receive retroactive follower awards. Growth is a deterministic local game system driven by story time, not real social-network traffic or wall-clock time. Separate custom stories may reuse the same handle because their accounts exist in separate story worlds.

Validation

Passed 50 Grove unit tests (including 7 new account tests), 10 phone-app tests and 7 custom-protagonist tests. New tests cover explicit creation, atomic validation, reserved handles, growth timing, reload/clock-rewind idempotence, daily caps, duplicate/self-reply exclusion, photo publication, account editing, story isolation, preserved older posts, current handle context and unchanged authored audiences. Passed account UI smoke covering setup, validation, editing, earned followers, profile display, navigation, normal/compact layouts and dark control states. Rendered setup, error, compact, growth and edit screens were inspected. The 32-page phone dark-theme smoke, Grove photo-publish smoke, Grove gallery smoke and start-screen smoke passed. These checks used local data and mocked dependencies where appropriate; no live AI generation or external account creation was needed. Existing sound-file load warnings appeared during UI smoke checks.

## Save compatibility

Restart the game to load the new Grove account flow. Existing stories need no migration. New account details, followers and growth events are stored in the story save and retained on reload and export. Existing custom Grove posts remain intact; authored character accounts and relationship histories are unchanged.

## Evidence and historical limits

Implemented and locally verified for the 8 November 2026 request for custom Grove accounts with chosen handles, bios and follower growth.

- grove_accounts.py
- grove_account_ui.py
- grove.py
- phone_apps.py
- phone_ui.py
- grove_gallery.py
- grove_gallery_ui.py
- notifications_ui.py
- tests/test_grove_accounts.py
- tests/grove_account_smoke.py


---

# Create your own Winterfield protagonist

release-2026-11-08-custom-protagonist-creator | Release | Characters
Date: 2026-11-08

Create an adult newcomer, generate a transparent portrait with the in-game Codex generator, and move into one of four homes.

## Details

Added

On the start screen, choose Create your own. Enter a name, gender, hairstyle, appearance description, sexuality, MBTI, interests, height, occupation and age, then select the downtown apartment, suburban house, Silver Sands beach cottage or university apartment. The form accepts adult ages 18–100, heights 120–230 cm and 1–12 comma-separated interests. Generate portrait with Codex uses the existing subscription-only in-game image backend. Gender, age, height, hairstyle and the appearance description guide the full-body portrait; sexuality and MBTI are not used to infer appearance. Actual PNG transparency is checked before accepting a result. Review the preview and choose Move to Winterfield.

Generation runs in the background with progress, cancellation and inline errors. The form remains available after a failed request. Changing appearance-related inputs requires a matching portrait before starting; changing the name, home or other background details does not force another image request. Closing the creator cancels an outstanding job. No API-key or external-provider fallback was added.

Newcomer gameplay

The selected residence becomes the protagonist's home for travel, rest, sleep and home activities. It is labelled as their home in Town and Maps; the other residences remain vacant. Custom protagonists begin there with the existing starting balance of $100,000 and a compact car, no local contacts, no seeded message archives, no pre-existing friendships, romance or local family ties, and no known private addresses. Discover residents by travelling and meeting them, or use Meet-Cute and its agreed number exchanges. Unknown residents cannot be summoned or texted through the empty contact list. Private home addresses can be learned through the existing closeness requirement. The new character's traits and newcomer background are available to conversation prompts, public profile identity and Meet-Cute. Their generated portrait is used by character rendering, wardrobe, camera references and Meet-Cute profile photos.

Compatibility

Each custom story stores its own unique identity, profile, chosen home and generated portrait path. Loading another custom or authored story does not rename residents, change their homes or add previous custom protagonists to NPC schedules. Generated portraits are included by the existing story export asset scanner. Existing protagonists keep their authored identities, contacts and relationship histories. Player-facing phone headings, journals and travel messages use the chosen name.

Known limitations

Occupation is a character background field; this update does not generate a bespoke career campaign. The residence starts unfurnished and there is no new furniture, rent or purchase system. Romance follows the game's mutual-attraction model; bisexual/pansexual options include nonbinary characters, and the asexual option currently has no dating matches. No custom birthday is collected. A live portrait-generation request was not run in this implementation check; UI generation, failure and cancellation used mocked output, and the backend's existing offline tests passed. Existing sound-file load warnings appeared during UI smoke checks.

Validation

The final targeted run passed 140 tests covering the custom protagonist, vacant homes, sexuality, Meet-Cute, phone numbers, map, phone personalization, saves, Codex image jobs, conversation lore, character types, autonomy, social world and patch notes. Seven custom-character tests cover initial isolation, all four homes, time progression, orientation compatibility, travel meetings, agreed Meet-Cute number exchange, conversation context, distinct stories, reload without a cached profile, portrait export, input/path/alpha validation and the generator contract. The creator smoke passed form submission, mocked generation, stale-appearance blocking, error/cancel recovery, normal and compact layouts, home opening, all 32 phone pages and own-profile opening. Map interaction, start-screen and 32-page phone dark-theme smokes passed; creator and Town renders were inspected. A broader 183-test run had four failing subtests in two existing tests (Valentina attraction baselines and Theo as a camera date companion), reproduced without creating a custom character, plus a localhost HTTP test blocked by sandbox socket permissions.

## Save compatibility

Restart the game to load the new creator. Existing stories require no migration. Choose Create your own to begin a separate custom story; prior stories are preserved through the existing save library. Custom profiles, home selection and relative generated-portrait paths persist in saves, and exports include the portrait. Keep generated image assets with local saves or use the story export bundle.

## Evidence and historical limits

Implemented for the 8 November 2026 request for a custom newcomer with a chosen vacant home and Codex-generated transparent portrait. Test results above are local checks from this update; mocked image generation is explicitly distinguished from an unperformed live request.

- custom_protagonist.py
- custom_creator_ui.py
- start_ui.py
- game_core.py
- game.py
- town.py
- town_ui.py
- world_loop.py
- hidden_cast.py
- phone_numbers.py
- meet_cute.py
- camera.py
- conversation_lore.py
- tests/test_custom_protagonist.py
- tests/custom_creator_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Four vacant homes for a future custom protagonist

release-2026-11-08-vacant-residences | Release | World
Date: 2026-11-08

Visit unassigned homes downtown, in the suburbs, near Silver Sands beach and near Winterfield University.

## Details

Added

Four vacant, unfurnished residences: a downtown apartment, suburban two-bedroom house, beach cottage and university apartment. Each has its own generated interior artwork, description, map coordinates and stable location ID. Find them in Town > Destination or Phone > Maps > Homes; search for vacant. Travel here works through the existing travel controls. Map details identify them as unassigned. Current-residence descriptions are included in conversation context.

Rules and limitations

These are locations reserved for a potential future custom protagonist, not new cast members. No occupant or routine is assigned, and random wandering locals do not spawn inside. Existing companions may accompany you through normal travel. No custom-character creator, ownership selection, rent, furnishing or move-in system is added. Existing protagonists still rest and use home actions at their established homes.

Fixed

Town opening could fail when the first stored relationship was hidden. The Bonds tab now selects the first visible relationship, if any.

Validation

Passed: vacant-home travel/vacancy/save-load checks; all 5 phone-map unit checks; phone map interaction smoke including four residence screenshots; dark-theme smoke across 32 phone pages; patch-notes UI smoke; start-screen smoke; rendered Town beach residence review. World tests: 14 of 15 passed, including unique scene art coverage; the existing occupied-home count assertion expects 18 but the unchanged cast registry contains 19. Initial save test attempt hit sandbox temporary-directory permissions; rerun with workspace temporary storage passed. Sound assets emitted existing load warnings during UI checks.

## Save compatibility

Restart the running game to load the additions. Existing saves need no migration and retain their protagonist, established home, money and relationships. New destinations are available immediately after restart; saved visits reload normally.

## Evidence and historical limits

Implemented for the 8 November 2026 request for four empty residences. Checks were run locally; generated interiors and rendered map/Town screens were visually reviewed. No historical release or version was inferred.

- vacant_homes.py
- town.py
- phone_map.py
- town_ui.py
- tests/test_vacant_homes.py
- tests/phone_map_smoke.py
- assets/ui/locations/vacant_homes_prompts.txt


---

# Manhwa artist portraits and song covers for Mixtape

release-2026-11-07-mixtape-manhwa-artwork | Release | Interface
Date: 2026-11-07

All 44 Mixtape artists now have illustrated profile portraits and a dedicated cover shared by their songs.

## Details

Added

88 locally bundled manhwa-style images: one profile portrait and one distinct song cover for each of the 44 artists across all 11 genres. Every artist shares their cover across all 24 songs, covering the complete 1,056-song catalogue. Original fictional soloists and group portraits use fine outlines, soft cel shading and cinematic lighting inspired by the existing game artwork.

Access

Open the phone, then Mixtape. Home and Search show artist portraits; View artist opens the portrait and biography above illustrated song rows. Covers also appear beside catalogue songs in the playlist editor and saved playlist view. The Home spotlight uses Voss artwork. Custom playlist headers retain the existing abstract graphic.

Implementation

Art is bundled under assets/mixtape and requires no network connection at runtime. Small decoded thumbnails are cached with a bounded cache. Missing artwork falls back to the existing artist or cover graphic, or a text-only song row. Legacy manually typed tracks remain readable without an invented artist cover. Generation prompts are retained in assets/mixtape/prompts.json.

Validation

Five Mixtape catalogue, save/share, artwork integrity and cache tests passed. The artwork check verifies all 88 square images and confirms every artist song resolves to the same cover. Mixtape UI, lifestyle UI, phone dark-theme and phone app design smoke checks passed. Reviewed the complete artwork contact sheets and rendered artist, search, playlist and scrolled song screens. The phone surfaces remain dark while content artwork retains its colours. Patch-note catalogue validation, all six patch-note unit tests, the patch-note reader smoke and the start-screen smoke also passed; the Markdown export was refreshed.

## Save compatibility

Restart the game to load the updated interface. Existing playlists, song IDs, shared snapshots and story saves remain intact; no migration or reset is required.

## Evidence and historical limits

Created all 88 images with the built-in image generator in this update, using the existing game portraits and setting artwork as style context. Verified the complete asset inventory, shared-cover mapping and rendered phone interface; originals are retained separately from the bundled copies.

- mixtape_art.py
- mixtape_ui.py
- assets/mixtape/prompts.json
- tests/test_mixtape_art.py
- tests/mixtape_ui_smoke.py
- tests/screenshots/mixtape-art-review-0.jpg
- tests/screenshots/mixtape-art-review-1.jpg


---

# Consistent hourly feelings across clock and sleep updates

release-2026-11-07-clock-affection-equivalence | Release | Gameplay
Date: 2026-11-07

Fixes the two clock-equivalence failures: identical story time now produces identical hourly feeling changes regardless of polling or sleep skipping.

## Details

Fixed

Hourly Mysterious Hearts feeling updates previously used Python's process-wide random stream through romantic_types.affection_step. An identical saved world could therefore receive different positive feeling changes when advanced in one batch, in many small clock polls, or by skipping sleep, depending on other random draws in the process.

The hourly tick now supplies a deterministic draw from the existing autonomy.chance helper, keyed by the hourly-affection purpose, actor, target and story minute. Personality-dependent growth probabilities and negative-feeling changes retain their existing rules. Existing feelings are not recalculated. The general affection_step helper still supports ordinary random draws for other callers.

Access

The correction applies automatically as story time passes, including normal simulation, accelerated sleep and skip-to-waking. No new controls or UI changes are required.

Validation

All 19 simulation-clock tests passed, including test_clock_batch_matches_small_steps_for_entire_world and test_skip_sleep_matches_all_normal_ticks_across_midnight, which failed in the preceding work-system update. A new Mysterious Hearts regression test compares a saved/restored state under opposite mocked process-wide random streams across 24 hourly updates and checks the full subsystem, including feelings, sustained counters and pending notes. The combined simulation-clock, Mysterious Hearts, romantic-types, careers, activities, calendar, town and lifestyle suites passed all 107 tests. Temporary save tests used the workspace-local .test-tmp directory. No story saves were modified.

## Save compatibility

Restart to load the fix. Existing saves and current feelings remain intact; no migration or reset is needed. Future hourly growth uses stable character-pair/time draws rather than the process-wide random stream.

## Evidence and historical limits

Traced the failing whole-world comparisons to differing mysterious_hearts.feelings values, fixed the hourly random draw, and verified both original tests plus the 107-test related integration run. Earlier release notes preserve the failures observed before this fix.

- mysterious_hearts.py
- autonomy.py
- romantic_types.py
- tests/test_simulation_clock.py
- tests/test_mysterious_hearts.py


---

# Work, leadership and sporting ambitions

release-2026-11-07-work-and-ambitions | Release | Gameplay
Date: 2026-11-07

Eight persistent career paths with meaningful shifts, projects, bookings, leadership delegation, title defences and a fictional Olympic ambition.

## Details

Added

Open Winterfield → Careers → Open work & ambitions. The dashboard embeds in the phone and links from Calendar. Garrett has restaurant projects and Red Dragons leadership; Rei has modelling and Iron Circle defence/comeback camps; Ivan has music and his established Joker Card responsibilities; Minsu has unpaid medical learning and a fictional future taekwondo pathway. Rei begins at #1. Ivan's independence choices do not automatically end his Syndicate involvement.

Work offers two decisions per 60/120-minute session and a quick 60-minute routine, once daily per path. Craft, trust, reputation, autonomy, fatigue, project quality and leadership pressure persist. Three distinct work days prepare a project for a scheduled finale; a seven-day deadline can be extended once by three days. Overdue work remains completable. Advanced briefs unlock at reputation 75 after a completion. Successful projects create keepsakes visible at home and in History.

Iron Circle competitors have different readiness targets and counter-plans. Bouts need two preparations and seven days between competitions; losses permit recovery and a comeback. The first camp starts a fourteen-day defence deadline. Minsu progresses through local, regional, national and international selection events to one Olympic medal opportunity; later wins are post-Games invitationals, not weekly Olympic medals. Preparation is unpaid; Iron Circle prizes require wins.

Leadership paths support delegation to recurring workplace roles, next-day reviews, trust and competence development, and unresolved pressure when reports are ignored. Daily preparation and recovery take an hour. History is private; explicit sharing supplies only the selected recorded update to the chosen contact, without invented replies or romance points.

Changed

Career bookings now have real durations, conflict with Calendar events and other work, and support safe rescheduling and cancellation. Arrive within fifteen minutes; work ends at the accepted end time. Reminders occur sixty and fifteen minutes ahead and at the start. Early cancellation has no penalty; late cancellation costs three reliability and missed bookings cost five plus workplace trust. Unfinished work expires without payment. Local jobs now take sixty minutes, open 08:00–20:00, and build reliability with repeat-shift pay increases. Legacy career entry points use the new quick routine; Iron Circle work no longer prints prize money for preparation.

Known limitations

Workplaces use finite authored situations and recurring role records, not new full conversational NPCs. The sporting pathway is fictional future gameplay, not current Olympic qualification rules. Syndicate activities are abstract leadership stories. Career keepsakes are textual records, not generated artwork. No existing romance progression is required.

Validation

Fifteen focused career tests passed, including every path, project completion, loss/comeback, Olympic progression, migration, JSON restoration, normal story-file save/load with an unfinished decision, clock expiration, booking conflicts, safe rescheduling, deadlines, delegation and privacy. The real Tk career smoke passed across eight paths/five sections, decisions, errors, booking, dropdown, resize and Calendar; rendered phone screens were inspected, including the open dropdown, compact Calendar agenda and home keepsakes. Calendar now stacks its month and agenda in phone mode so bookings remain reachable without horizontal navigation. Six patch-notes tests, the patch-notes UI smoke and start-screen UI smoke also passed. The catalogue was validated and its Markdown export refreshed. The dark-theme smoke passed across 32 phone pages and embedded controls. A combined 76-test integration run had 74 passes and two existing simulation-clock equivalence failures; both failures reproduced with the new career clock hook disabled. Temporary-file tests were rerun with a workspace-local temp directory after the sandbox denied the default temp location.

## Save compatibility

Restart the game. Career records are additive and lazy; existing balances, relationships, history and legacy daily booking locks remain. No retroactive work rewards or deadlines are invented. Rei receives a defence deadline only after starting a camp. New sessions, projects, bookings, results and keepsakes use the normal story save.

## Evidence and historical limits

Implemented from the requested work and side-career systems; evidence consists of the current implementation, focused tests and inspected rendered UI. Existing clock equivalence failures are explicitly retained as limitations, not recorded as passes.

- careers.py
- careers_ui.py
- town.py
- town_ui.py
- calendar_ui.py
- scheduled_events.py
- world_loop.py
- phone_apps.py
- activity_ui.py
- README.md
- tests/test_careers.py
- tests/careers_ui_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/test_activities.py
- tests/test_simulation_clock.py


---

# Mixtape Home, Search, Library and artist profiles

release-2026-11-07-mixtape-browse-pages | Release | Phone
Date: 2026-11-07

Browse Mixtape like a music app, discover artists, build and edit playlists, and send them privately to your contacts.

## Details

Added

Open Phone > Mixtape. Persistent Home, Search and Your library tabs replace the single long form. Home features an artist spotlight, discovery cards and recent playlists. Search matches artist names and song titles without case sensitivity, supports all 11 genre filters, and shows an explicit no-results state. Song search displays up to 40 matches with a visible limit notice. Artist profiles include original bios, genre, abstract initial artwork and all 24 songs with descriptions and Add to playlist buttons.

Playlists

Use Make a playlist or Your library > Create / continue playlist draft. Name the draft, add a dedication, find songs from profiles or search, and remove selections before saving. The existing 30-song limit and duplicate protection remain. Saving opens a dedicated playlist page with cover artwork, track list, Edit playlist and Send playlist actions, and clears the completed workspace. Editing keeps the same playlist ID and supports retaining or removing old manually entered tracks. An unfinished different draft is protected from being overwritten; returning to the same edit resumes it.

Sharing

Send playlist opens a contact picker. Sending records the existing private share and confirms the recipient, then returns to the playlist. Your library includes recent sent history. Shared copies remain snapshots even when the original playlist is edited later. No-contact and unavailable-playlist states provide inline guidance.

Validation

Three Mixtape and eight lifestyle unit tests passed. The Mixtape UI smoke exercised Home/Search/Library, artist and song search, no matches, artist profiles, duplicate and capacity checks, draft persistence, removal, saving, editing, protected drafts, sending and immutable shared copies. Dark surface/control-state checks passed for all seven Mixtape pages and the recipient popup. The full phone_dark_theme_smoke, lifestyle_ui_smoke and phone_app_design_smoke passed. Rendered Home, Search, artist, editor, saved playlist, send and library screens were inspected at 430x740 and 560x780. Patch-note UI and start-screen smokes passed.

Known limitations

Song metadata and playlist sharing are available; audio playback is not connected. Artwork is locally drawn abstract graphics and initials, not artist photographs.

## Save compatibility

Restart to load the redesigned screens. No story reset is required. Existing playlists, memories and private shared snapshots remain intact. Previous catalogue draft titles, memories and song selections are adopted into the new save-scoped workspace on first open; previous typed drafts remain reference text in the editor. New draft and page state use the existing lifestyle save data.

## Evidence and historical limits

Implemented and verified in this chat on 7 November 2026. Tests used isolated game state and mocked persistence; no real contacts were messaged and no external music service was called. Local screenshots provided visual evidence for the new pages.

- mixtape_ui.py
- lifestyle_ui.py
- lifestyle_apps.py
- tests/test_mixtape.py
- tests/mixtape_ui_smoke.py
- tests/lifestyle_ui_smoke.py
- tests/phone_app_design_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Mixtape artist catalogue and song picker

release-2026-11-07-mixtape-artist-catalogue | Release | Phone
Date: 2026-11-07

Build playlists by choosing from 44 artists and 1,056 songs instead of typing song lists.

## Details

Added

Open Phone > Mixtape > Create. Choose a genre, artist and song, then press Add selected song. All 11 supplied genres have four artists with 24 songs each. Artist profiles and song descriptions are shown beside the selectors, preserving the supplied multilingual titles and translations. Add songs in playlist order, remove individual selections, enter a playlist title and optional memory or dedication, then Save playlist. Existing private sharing remains available.

Changed

The free-text song-entry box is replaced by read-only catalogue selectors. A playlist accepts 1–30 songs and prevents adding the same artist/song twice; identical titles from different artists remain separate. Selections and browse fields survive navigation through the existing save-scoped draft system. New playlists store stable song IDs alongside readable title/artist snapshots. Existing saved typed playlists remain visible and shareable, and an older unsaved typed draft is shown as reference text rather than discarded.

Validation

Two Mixtape unit tests and eight lifestyle tests passed, including catalogue completeness, original Unicode titles, same-title/different-artist tracks, invalid selections, JSON save round-trip and private share snapshots. Mixtape UI smoke passed all artist selectors, duplicate and 30-song limits, removal, navigation drafts, Unicode save, dark popup and resizing. Lifestyle UI smoke and phone_dark_theme_smoke passed. Rendered picker, open dropdown and saved-library screens were visually inspected at 430x740 and 560x780. Patch-note validation, six patch-note unit tests, patch-note UI smoke and start-screen smoke passed; patch-note tests used a workspace temporary directory after the default temporary location stalled. The Markdown export was refreshed.

Known limitations

The catalogue contains song metadata, not recorded audio or streaming. Existing manually entered songs are retained in their saved playlists; new playlists use catalogue songs.

## Save compatibility

Restart the game to load the new catalogue and picker. No story reset or migration is required. Existing playlists, dedications and shared snapshots are retained. Catalogue selections are saved through the existing lifestyle draft state.

## Evidence and historical limits

Implemented on 7 November 2026 using the artist roster and song batches supplied in this chat. The first two genres were imported from the original user message and the remaining genres from the eight supplied attachments; pasted assistant continuation prompts were excluded. Checks used isolated state and no music generation or network calls.

- assets/mixtape_catalog.json
- mixtape_catalog.py
- lifestyle_apps.py
- lifestyle_ui.py
- tests/test_mixtape.py
- tests/mixtape_ui_smoke.py
- tests/test_lifestyle_apps.py
- tests/lifestyle_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Supafast refreshes automatically at midnight

release-2026-11-07-supafast-midnight-refresh | Release | Fixes
Date: 2026-11-07

Daily stock now starts refreshing at 00:00 story time even when Supafast and the phone are closed.

## Details

Fixed

The main game clock now schedules Supafast generation independently of the phone. When story time reaches a new day at 00:00, yesterday’s stock stops being purchasable and the current day’s catalogue begins generating in the background. Product photography queues after the accepted catalogue is ready, also without opening the phone. Browse the results through Phone → Supafast. This supersedes the earlier open-app-triggered daily refresh.

AI generation is asynchronous: 00:00 starts the refresh, rather than guaranteeing that all text and images finish instantly. An already-running catalogue request is allowed to finish before another starts; stale results cannot publish into a different day. Current stock is saved and reused, with no repeated requests or rerolls on each clock tick. Initial stories and loaded saves without current-day stock are prepared automatically while the story is active. Sleep and other time jumps prepare the destination day only; skipped days are not backfilled. The start screen does not launch new catalogue work. Failed generation retains the explicit retry flow, while a subsequent day can request fresh stock.

Validation

The new supafast_midnight_smoke exercised the real Game.poll dispatch with no phone window: no text request at 23:59 with existing stock, exactly one request after the clock advanced to 00:00, persistence, background photo dispatch, reload reuse, multi-day jumps, failure deduplication and inactive-game behavior. Ten Supafast unit tests passed. The existing Supafast UI smoke passed generation, purchase, daily rollover, retry and stale-save protection. Phone dark-theme smoke passed all 32 pages and embedded control states. Providers were mocked; no live generation timing was measured.

## Save compatibility

Restart the game to load the clock integration. No story reset or migration is required. Existing catalogues, product photos, orders and inventory are retained. Current-day stock is reused; missing stock and photos can now generate while the phone is closed, using the existing provider connections and their normal allowance.

## Evidence and historical limits

Implemented and checked in this chat on 7 November 2026. The clock integration test used the real game poll method with a controlled clock and mocked providers, without creating a phone window.

- game.py
- supafast.py
- README.md
- tests/supafast_midnight_smoke.py
- tests/test_supafast.py
- tests/test_supafast_images.py
- tests/supafast_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# AI food photography for Doober Eats menus

release-2026-11-07-doober-food-photos | Release | Interface
Date: 2026-11-07

Restaurant menus now show generated food photographs with saved images, background loading and retry controls.

## Details

Added

Open Phone → Doober Eats and choose a restaurant. Each menu item now queues an individual AI-generated dish or drink photograph through the existing Codex ChatGPT image connection. Prompts use the restaurant, dish name and category, asking for appetising realistic food, appropriate serving ware, a dark slate tabletop and no text or logos. Compact photos appear above menu names and prices. Existing menu items, prices, recipients, orders and instant delivery remain unchanged.

Photos generate sequentially in the background using the normal ChatGPT plan allowance; each restaurant has twenty items. Ordering stays usable while photos load. Successful images are saved by restaurant and item, reused across in-game days and reloads, and never written into the global authored menu or the player’s Camera album. Existing saves gain photo records when a menu is opened.

Changing restaurants cancels unfinished work for the previous menu and queues missing photos for the selected one. Returning resumes incomplete photography. Switching saves or closing the application cancels obsolete work; late results cannot attach to the wrong restaurant, story or changed dish. Already-incurred provider usage may still count. A failure pauses the remaining queue. Retry food photos retries missing photos without replacing successful pictures; another image job may require waiting first. Missing files can regenerate and corrupt previews offer retry.

Validation

Four Doober image unit tests, ten Supafast unit tests and ten phone-app unit tests passed. Checks cover restaurant-isolated records, saved references across days, authored-menu preservation, changed dish rejection, invalid paths and rasters, prompt contents and unchanged order pricing. The Doober image UI smoke passed sequential requests, failure/retry, rendered previews at 430x740 and 560x780, cached reuse, restaurant switching and save isolation. The Supafast image smoke passed after the shared queue and preview refactor. Test images were fixtures and generation was mocked; live account connectivity and food-image accuracy were not verified.

The twelve-app design smoke passed at two device sizes; phone_dark_theme_smoke passed all 32 phone pages and embedded control states. Patch-note validation/export, six patch-note unit tests, patch-note UI smoke and start-screen UI smoke passed.

## Save compatibility

Restart to load the updated views. No story reset or manual migration is needed. Existing food orders, prices and inventory are preserved. New phone_apps.food_photos records retain generated file paths and job IDs per restaurant/menu item. Keep assets/generated with the game; missing images can regenerate. Pending work is transient and resumes for missing photos when the menu is reopened.

## Evidence and historical limits

Implemented and tested in this chat on 7 November 2026 using the existing subscription-only image generator. UI evidence uses coloured test fixtures rather than generated food; no live food-image quality result is claimed.

- doober_images.py
- supafast.py
- supafast_ui.py
- phone_ui.py
- README.md
- tests/test_doober_images.py
- tests/doober_images_smoke.py
- tests/supafast_images_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/screenshots/doober-food-430x740.png
- tests/screenshots/doober-food-560x780.png


---

# AI product photography for Supafast listings

release-2026-11-07-supafast-product-photos | Release | Interface
Date: 2026-11-07

Supafast product cards now show generated studio photographs, with saved images, loading states and retry controls.

## Details

Added

Open Phone → Supafast. Each item in the daily selection now receives its own AI-generated product image using the existing Codex ChatGPT image connection. The prompt uses the accepted item name, description and category to request a square studio photograph with the complete product, realistic materials, a dark slate background and no branding or text. Images appear above the title, description and price in the shopping card. Compact previews contain the full photograph instead of cropping important product details.

Photos generate sequentially in the background. A full new daily selection can generate twelve images and uses the normal ChatGPT plan allowance. The listings remain available for shopping while images load, and switching to another app does not interrupt the current day’s queue. Completed images are saved with their product and reused when reopening or reloading. Existing AI catalogues without photos automatically enter the image queue. Successful images are not rerolled.

A failed request pauses the remaining image queue instead of repeatedly requesting all twelve products. Retry product photos retries only missing images; the same control can recover a corrupt preview. Missing image files are eligible for regeneration. Another running image job may require waiting before retrying. Day changes, save changes and application shutdown cancel obsolete work; results from another day, story or changed listing cannot attach to current stock. Already-incurred provider usage may still count. Product images remain separate from the player’s Camera album. No substitute illustration or stock image is used in production.

Validation

Ten Supafast unit tests and ten phone-app unit tests passed. Coverage includes image prompt construction, path restrictions, raster validation, saved references, duplicate completion, changed listings and stale-day rejection. The product-image Tk smoke passed sequential generation, failure/retry, rendering, reuse after JSON reload, missing-file recovery, day cancellation and save-change cancellation. The existing Supafast UI smoke passed purchase, daily rollover and text generation lifecycle checks. The twelve-app design smoke passed at two phone sizes; phone_dark_theme_smoke passed all 32 phone pages and embedded control states. Inspected the compact listing screenshot. Image generation was mocked with a local fixture image, so live model image quality and account connectivity were not verified.

## Save compatibility

Restart the game to load the changed views. No story reset or manual migration is needed. Existing prices, stock, purchases and ownership are preserved. Product records gain relative generated-image paths and job IDs as photos finish. Keep assets/generated with the game; missing files can be regenerated. Pending image work is transient and resumes for missing images on the next Supafast visit.

## Evidence and historical limits

Implemented in this chat on 7 November 2026 through the existing subscription-only codex_images integration. Render evidence uses a test fixture, not an actual generated product image. The recorded tests exercise the integration with mocked generation.

- supafast.py
- supafast_ui.py
- phone_ui.py
- README.md
- tests/test_supafast_images.py
- tests/supafast_images_smoke.py
- tests/supafast_fixtures.py
- tests/phone_dark_theme_smoke.py
- tests/screenshots/supafast-product-photos.png


---

# Little notes, secret butterflies

release-2026-11-07-anonymous-notes-ai | Release | Interface
Date: 2026-11-07

A cutesy dark anonymous-notes app with character messages generated through your existing AI connection.

## Details

Changed

Open Phone > Mysterious Hearts for a rose-and-lilac letterbox, dark slate note cards, a labelled composer, conversation cards and an expandable mystery notebook. Empty, waiting and retry states stay dark. Player-written notes and drafts remain under your control; welcoming attention records affinity without sending a prewritten line on your behalf.

AI messages

New NPC confessions, appreciation notes, replies, welcomes and closure messages use the existing AI & account provider in a background worker. Story-time and relationship rules still schedule notes. Generation uses character voice, current feelings and permitted memories; unknown recipients do not receive hidden sender metadata. No canned message is substituted on failure. Failed requests remain saved and can be retried in the app. Blocked, closed, changed and previous-save conversations reject late results. Existing historical messages are retained.

Validation

Passed 21 anonymous-note unit tests and the actual phone feature smoke check; inspected rendered inbox, conversation and retry screens. Dark-surface audit passed across 32 phone pages. One real note was generated through the existing ChatGPT provider without writing a story save.

Known limitations

AI must be connected to deliver new NPC text; content quality varies by model. Anonymous prompts prohibit identifying details and named self-identification is rejected, but model wording may still provide clues. Investigation outcomes remain simulation rules rather than generated dialogue.

Final checks

Passed six patch-note tests, catalogue validation/export, patch-notes UI smoke and start-screen smoke. The notes UI smoke also exercised retry, expanding the notebook and resizing to 440 × 720.

## Save compatibility

Restart the game to load updated code. Existing saves, identities, notes, clues and drafts remain compatible. Pending AI requests are stored additively and resume with the configured provider; historical prewritten notes are not rewritten.

## Evidence and historical limits

Implemented for the anonymous notes app request on 7 November 2026. Verified with local automated tests, rendered screenshots and a live request using the existing configured connection.

- hearts_ui.py
- mysterious_hearts.py
- hearts_ai.py
- game.py
- phone_ui.py
- tests/test_mysterious_hearts.py
- tests/hearts_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Fresh AI-generated Supafast stock every story day

release-2026-11-07-supafast-ai-catalogue | Release | Features
Date: 2026-11-07

Supafast now creates daily products with descriptions through your selected AI provider, replacing its fixed list.

## Details

Changed

Open Phone → Supafast. The app generates twelve distinct product listings for the current in-game day using the existing AI & account provider. Each listing contains a name, descriptive product copy, category and an integer price from $5 to $500. The prompt requests a varied assortment of physical goods across everyday shopping categories rather than renaming a fixed roster. Generated descriptions are flavour; they do not create new stat effects or services. No product images are generated by this change.

An accepted catalogue is saved with the story and reused throughout the day, including after reload. At in-game midnight the previous selection is no longer purchasable. A fresh selection generates while Supafast is open or when it is next opened; unvisited days are not backfilled. Search now includes descriptions. Existing instant delivery, recipient selection, balance checks, orders and gift inventory remain connected.

Generation runs in a background worker, allowing other phone apps to remain usable. Dark loading and failure states replace empty shopping results while stock is unavailable. Retry daily selection explicitly retries an unsuccessful request; there is no automatic retry loop or canned-item fallback. The validator rejects missing descriptions, invalid prices, duplicate names and names matching the last 36 saved products. The prompt also asks for different goods rather than simple recolours; semantic originality still depends on the model. Requests finishing after a day or save change cannot publish stale stock. Accepted catalogues cannot be rerolled by reopening the app.

Validation

Six Supafast unit tests, ten phone-app unit tests and fourteen town tests passed. These cover provider payload/response handling, atomic validation, saved daily stock, old inventory compatibility, stale orders, duplicate publication, malformed output, failures and recent-name rejection. Town tests initially hit sandbox temporary-directory permissions and passed after redirecting temporary files into the workspace. Supafast UI smoke passed loading, descriptions, purchase, background completion, same-day reuse, midnight rollover, failure/retry and stale-save protection. The twelve-app design smoke passed at two phone sizes, and phone_dark_theme_smoke passed all 32 phone pages and embedded control states. Inspected the loading/ready/error screenshot sheet. All AI generation was mocked; no live provider request or allowance-consuming generation was performed.

Patch notes validation/export, six patch-notes unit tests, patch-notes UI smoke and start-screen smoke also passed with workspace temporary storage. The initial patch-notes unit run using the sandbox temporary directory was stopped after a permission error; the corrected full run passed.

## Save compatibility

Restart the game to load the update. No reset or manual migration is needed. Existing products, ownership, gifts and order history remain stored. The legacy fixed catalogue is replaced for browsing on the first Supafast visit; historical product IDs remain intact. Accepted AI catalogue contents and their day marker persist with the story. Pending work is transient and is requested again after reopening if no accepted catalogue exists.

## Evidence and historical limits

Implemented and verified in this chat on 7 November 2026 using the existing game provider abstraction. Screenshots contain deterministic test-only listings. Production contains no fallback item roster. Actual checks and the absence of live generation verification are recorded explicitly.

- supafast.py
- phone_apps.py
- phone_ui.py
- README.md
- tests/test_supafast.py
- tests/test_phone_apps.py
- tests/test_town.py
- tests/supafast_ui_smoke.py
- tests/phone_app_design_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/screenshots/supafast-ai-states.png


---

# Faster Grove feed browsing

release-2026-11-07-grove-feed-performance | Release | Interface
Date: 2026-11-07

Grove renders a small page at a time and reuses photo thumbnails instead of rebuilding the entire archive.

## Details

Fixed

Opening Phone > Grove previously created widgets for the entire photo archive and all replies, decoded every photo again, and started a recurring like timer for every photo. Grove now renders at most 12 posts or replies per page, bounding the active feed widgets and photo timers. Use Older and Newer above the feed to browse all entries in the existing thread order. Paging keeps the caption draft and selected reply target intact. Refresh feed still returns to the newest page.

Changed

Feed, profile and photo-detail previews share a bounded cache of 48 small thumbnails. File modification time, file size and requested preview size invalidate cached previews; full-size photos and Tk widgets are not retained by this cache. No archive entries are deleted or hidden permanently. Existing dark phone controls are used for page navigation.

Validation

Grove performance smoke passed with a fresh-archive open measured at 0.456 seconds locally; this is a local measurement, not a universal speed guarantee. Checked bounded rendering, complete traversal including deep replies and the final short page, drafts, reply targets and thumbnail reuse. Grove gallery and publishing smoke checks passed, as did 43 Grove unit tests and the dark-theme smoke across 32 pages. Inspected the rendered paged feed. The original full-archive profiling run was stopped before completion, so no numeric before/after speed ratio is claimed. Test startup reported unavailable sound assets.

Known limitations

Individual profile galleries still render their own photo grids in full. Automatic feed refresh retains its existing newest-page behavior.

## Save compatibility

Restart the game to load the updated Python code. No migration is required; existing posts, photos, replies, likes and story saves remain compatible.

## Evidence and historical limits

Implemented in response to reported Grove lag. Verified with local Tk smoke checks, Grove unit tests and screenshot inspection; no AI requests or player-save writes were needed for testing.

- phone_ui.py
- grove_gallery_ui.py
- tests/grove_performance_smoke.py
- tests/grove_gallery_smoke.py
- tests/grove_publish_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/screenshots/grove-paged-feed.png


---

# Contact photos for every town NPC

release-2026-11-07-town-contact-photos | Release | Artwork
Date: 2026-11-07

All 22 town NPCs now have dedicated contact photos matching their transparent character portraits.

## Details

Added

Generated 22 individual square contact photos using each existing character portrait as the identity reference. Includes the six original townspeople, twelve everyday residents, Mario Romano, Robin Vale, Dana Lin and Joseph Richter. Each photo uses a setting associated with that character. Find them in Phone > Contacts and in direct message headers after adding the contact normally. Custom contact photo choices remain in effect.

Fixed

Direct display-name portrait lookup now covers the original townspeople and venue staff as well as the newer residents. All 22 existing transparent portraits were present and retained; no replacement portraits were needed.

Validation

The expanded town portrait smoke check passed for all 22 transparent portraits, square contact files, direct-name/slug lookup and phone avatar loading. Inspected the rendered portrait/avatar gallery and dark phone message header. The phone dark-theme smoke check passed across 32 pages, chat, contact details and embedded controls. Test startup reported unavailable sound assets; artwork checks passed.

Patch-note validation, all six patch-note unit tests (using workspace-local TEMP/TMP), patch-note UI smoke and start-screen UI smoke passed. The first unit-test attempt encountered a system temporary-folder error; the isolated rerun passed.

## Save compatibility

Existing stories, learned numbers, chats and custom avatar selections are retained. No save migration is required. Restart the game to refresh cached artwork and load the portrait lookup fix.

## Evidence and historical limits

Generated with built-in image_gen using existing local portraits as identity references; exact prompts and asset paths are recorded in the contact manifest. Verified with actual Tk loaders and rendered screenshots during this update.

- assets/profiles/town-contacts-manifest.json
- game.py
- tests/town_portraits_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/screenshots/town-portraits.png
- tests/screenshots/town-portrait-phone.png


---

# Distinct mobile layouts for everyday phone apps

release-2026-11-07-phone-app-design | Release | Interface
Date: 2026-11-07

A photo-grid Gallery, shopping and food cards, arcade library, music covers and themed everyday apps, all in dark mode.

## Details

Changed

Open the phone and select Gallery, Supafast, Doober Eats, Mini Games or a lifestyle app. Gallery now presents square cropped previews in a two-column, date-grouped library; opening a photo still uses the original image, and View and Share remain available. Supafast has an amber shopping identity, prominent prices and product cards. Doober Eats uses a green delivery identity and menu cards with the existing restaurant and recipient selectors. Both stores have live name/category search, a no-results state, and shortcuts to orders and Pocket Wallet. Search filters only the current daily selection or restaurant; buying and gifting still use existing instant-delivery rules.

Mini Games now has an arcade library with game descriptions, Play/Resume labels and distinct card artwork. Existing controls, pause behavior and session lifetimes are retained. Mixtape has a green library header, original locally drawn cover art, playlist summaries and Create navigation. It still stores song lists and dedications, without audio streaming. Wardrobe has a current-look card and closet/design controls. Out & About presents activity cards and booking navigation. Pocket Wallet foregrounds the real in-game balance and bill-splitting workflow. Postcards presents sent mail above the composer, with attachment actions. Campus Portal adds course/club counts and a learning dashboard. Recipe Box and Winterfield Exchange gain themed headers and mobile navigation. Contacts, Calendar, Journal, Notes, Deliveries, Settings and More gain related-app and Home shortcuts.

All new surfaces use dark backgrounds, muted light text and coloured accents. Navigation shortcuts scroll to existing sections or open existing apps; no placeholder purchase, streaming, banking or mail service has been added. Form drafts and existing actions remain connected to their original game systems.

Validation

Passed the new phone_app_design_smoke check at 430x740 and 560x780, including live search/no results, order navigation, lifestyle section shortcuts and a populated four-photo gallery. Inspected the rendered twelve-screen contact sheet. Lifestyle UI smoke passed saved drafts, mocked outfit generation, app switching, errors and cancellation. Camera UI smoke passed after updating outdated selectors to locate existing embedded dialogs and GalleryView by type. All 13 arcade phone layout/lifecycle checks passed with temporary files redirected into the workspace. Phone dark-theme smoke passed all 32 phone pages and embedded control states. Patch notes validation/export, patch-notes UI smoke (search, filters, state, export and error states), and start-screen UI smoke (four previews and two sizes) passed.

Focused unit results: lifestyle apps 8 passed; phone apps 10 passed; patch notes 6 passed; camera 12 passed and 1 failed on local-date partner Theo not appearing in camera companions. The broader phone_navigation_smoke failed its writing-response status assertion, outside the redesigned app checks. These failures remain limitations of the validation run; no passing result is claimed for those suites.

## Save compatibility

Restart the game to load the changed Python views. No save migration or story reset is required. Existing photos, playlists, outfits, bookings, receipts, messages and course progress are retained. Gallery crops apply only to thumbnail previews; original files are unchanged. Arcade sessions retain their existing in-memory lifetime.

## Evidence and historical limits

Implemented in this chat on 7 November 2026. Visual evidence comes from local Tk screenshots with fresh mocked game state; gallery test images are fixtures, not newly generated player photos. Validation records actual executed checks and explicitly retains the two unrelated test failures.

- phone_app_design.py
- phone_ui.py
- camera_ui.py
- mini_games_ui.py
- lifestyle_ui.py
- phone_icons.py
- tests/phone_app_design_smoke.py
- tests/lifestyle_ui_smoke.py
- tests/camera_smoke.py
- tests/phone_dark_theme_smoke.py
- tests/arcade_phone_smoke.py
- tests/screenshots/phone-app-redesign.png


---

# Personality compatibility beyond a single tag

release-2026-11-07-expanded-personality-compatibility | Release | Relationships
Date: 2026-11-07

Long-term romantic compatibility now considers multiple interests, character traits, lifestyle facets and sociability for all 25 authored romantic profiles.

## Details

Added

Expanded personality profiles and directional partner preferences for all 25 characters in the romantic-type canon. Profiles include secondary hobbies and interests, multiple everyday personality traits and several lifestyle facets. Hidden-cast profiles retain every explicitly authored hobby. Having a profile does not unlock a romance route: existing orientation, family, town-NPC and friendship-only rules still apply.

Changed

Positive long-term affection growth now uses a weighted personality match: character traits 35%, interests 30%, lifestyle 25% and sociability 10%. Within each category, matching more of the observer’s preferred facets earns more credit. Additional unrelated hobbies or traits never dilute existing matches, duplicate tags do not increase scores, and unknown categories contribute neutral credit. Related hobbies can share a domain, such as taekwondo and running counting as sports, without claiming they are the same hobby.

For example, Minsu’s science, medicine, gaming, anime, taekwondo and food reviewing now contribute independently of his extroversion. Rei’s cooking and poetry, Garrett’s martial arts, and Ivan’s piano and repair interests also contribute alongside their broader personalities and routines. A single shared hobby or social style no longer settles long-term compatibility.

The resulting fit still maps to a 15–85% chance of positive affection growth when a growth opportunity exists. Full matches are not guarantees and mismatches are not hard refusals. Physical attraction scoring and negative affection changes are unchanged. Dialogue receives expanded preferences and category-level fit as private guidance; this does not reveal undisclosed hobbies or personal history to other characters. The feature runs automatically during existing conversations and relationship simulation.

Validation

100 tests passed across personality types, romantic types, mysterious hearts, sexuality, dating, social events, relationship dynamics, social world, conversation lore and character types. Checks cover all 25 profiles, secondary interests, hobby-domain matching, partial and directional fit, neutral unknowns, duplicate handling, category weights, probability bounds and unchanged physical matching. No phone UI surfaces changed.

## Save compatibility

Existing saves remain compatible without reset or migration. Restart the running game to load the expanded authored profiles. Existing attraction, accumulated affection, crushes and relationship history are retained. Future positive affection growth uses the new personality scores, so previous compatibility rankings may change.

## Evidence and historical limits

Implemented and verified in this chat on 7 November 2026. Actual profiles draw on authored biographies, conversation references and hidden-cast hobbies; expanded partner preferences are authored tastes. The validation count reflects the completed focused run for this change.

- personality_types.py
- romantic_types.py
- hidden_cast.py
- Mysterious Hearts - Character References.md
- Mysterious Hearts - RPG Game.md
- tests/test_personality_types.py
- tests/test_romantic_types.py


---

# Recovered the 17 oversized development chats

release-2026-11-07-history-recovery | Release | Interface
Date: 2026-11-07

Restored missing historical reports and detailed notes from local session logs.

## Details

Scanned all 17 formerly inaccessible root-session logs. Recovered 66 completed reports, including 59 previously absent reports. Added one detailed historical chapter per chat, including explicit interrupted-work records for the three chats without completed reports. Retained original timestamps, source file names, event ordinals and turn IDs.

External Vendetta lore edits, generated assets awaiting integration, superseded behavior and unfinished requests are labelled. The old oversized-chat retrieval gaps are resolved; unfinished work is not relabelled as shipped. No game feature, artwork or story save is changed by this archive update.

## Save compatibility

No save migration or story reset. Reopen the patch notes viewer to load the updated catalogue.

## Evidence and historical limits

Local log recovery performed on 7 November 2026. Historical tests are not recertified. Recovery verification is recorded in patch_notes/RECOVERY.md.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md
- tools/recover_patch_history.py


---

# Neo, Alyssa and their shared home

recovered-01a1b37a-6219-7ae1-9d49-b00d3df724a7 | Retrospective | World & story
Date: Unknown — reconstructed history

Neo joined as a hidden, platonic cast member with personal references, a schedule, an apartment and established friendships with Tyler and Daniel.

## Details

Neo joined as a hidden, platonic cast member with personal references, a schedule, an apartment and established friendships with Tyler and Daniel. A transparent scene portrait and apartment illustration followed. Alyssa subsequently became a discoverable character with her own archive job, routines, profile and artwork, superseding the earlier off-screen description. Eight Grove photos each then added their hobbies, shared home life and Neo’s friendships. Existing-save migration and engagement preservation were reported.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-07T10:53:16+10:00 · 01a1b37a-651c-7023-b77d-fc0d177d5457
- 2026-11-07T10:54:39+10:00 · 01a1b37e-d584-7b92-9154-cdb09720fa43
- 2026-11-07T11:03:24+10:00 · 01a1b383-c03d-7f10-9b69-1e07dedd13a5
- 2026-11-07T11:11:32+10:00 · 01a1b388-87f6-72f0-bd2f-021fdb8ed00c

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add Neo Ishida as cast member. All available root-session completion events scanned. 4 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Yuriko, Sophie and high-school photo memories

recovered-01a1b35c-ad5d-72f3-8258-47949f7c5119 | Retrospective | Art & media
Date: Unknown — reconstructed history

Seven Yuriko group photos added playful memories involving Rei, including cat ears, flour, a crown and a parasol.

## Details

Seven Yuriko group photos added playful memories involving Rei, including cat ears, flour, a crown and a parasol. Eight Sophie photos followed, including school memories dated 2046–2047. High-school reference portraits were created for Rei, Sophie, Emily and Marcus. Another eight school photos were split between Rei and Emily; Rei is deliberately tattoo-free in these earlier memories. Captions, comments and save upgrades were included. One interrupted turn has no completion report and is not counted as another photo release.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-07T10:24:43+10:00 · 01a1b35d-2c8b-7ec0-810c-6d35e28c4150
- 2026-11-07T10:34:44+10:00 · 01a1b368-115e-7c43-ad4c-7fc83732ec7b
- 2026-11-07T10:46:44+10:00 · 01a1b36e-c7e3-7193-b359-36e01f782681

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add photos to Yuriko’s grove gallery. All available root-session completion events scanned. 3 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Elliot, Tyler, Valentina, Daniel and Sylvanis galleries

recovered-01a1b35c-7954-7562-bb9f-5e0785b14702 | Retrospective | Art & media
Date: Unknown — reconstructed history

An initial inventory identified five missing galleries; five later completion reports added eight photos for each character.

## Details

An initial inventory identified five missing galleries; five later completion reports added eight photos for each character. Elliot’s posts include Ivan comments. Tyler’s cover boxing, dominoes, supper and his father. Valentina’s include three Ivan sibling scenes: sail repairs, karaoke and supper. Daniel’s cover cinema work, drawings, judo and home life. Sylvanis’s use crime-themed scenes and tense replies from Ivan. Save upgrades were reported. The original reports retain temporary unrelated gallery-test failures rather than rewriting them as clean runs.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-07T10:16:15+10:00 · 01a1b35c-92ba-71f2-8236-c7b30feef44b
- 2026-11-07T10:22:22+10:00 · 01a1b35d-449d-7c72-bf42-12e2cee5de4c
- 2026-11-07T10:29:33+10:00 · 01a1b363-d37a-75e3-bf8a-4033c8f580b0
- 2026-11-07T10:42:42+10:00 · 01a1b36e-768a-7aa2-8132-7a354b36b947
- 2026-11-07T10:48:09+10:00 · 01a1b375-5e0b-75d2-8719-2d95e9bc1d70
- 2026-11-07T10:54:30+10:00 · 01a1b37a-9d93-7ba3-8ca9-adb4c07f8e95

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Find missing grove galleries. All available root-session completion events scanned. 6 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Garrett outfit request: recovered interrupted work

recovered-01a1b0a3-d78b-70b1-b15d-ba97cea66f4d | Retrospective | Development history
Date: Unknown — reconstructed history

The root turn was interrupted and has no completion report.

## Details

The root turn was interrupted and has no completion report. It planned eight looks: burgundy velvet, emerald silk, leather biker jacket, camel coat, denim, knit polo, satin bomber and navy waistcoat. These plans are not proof of a completed eight-outfit update. A Garrett alternate-outfit manifest exists in the current project, but that does not establish that this interrupted turn completed or published every requested look. No release date or passed test is assigned to the request.

Recovered reports (chat-completion dates, not release dates):
- No completed report. The source records an interrupted root turn.

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Create 8 Garrett outfit variants. All available root-session completion events scanned. 0 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Emily, Sophie and Amy wardrobe expansions

recovered-01a1b0a4-2a8c-7682-b0cb-29ddf0ccdda9 | Retrospective | Art & media
Date: Unknown — reconstructed history

Emily received eight everyday and occasion looks: florist workwear, café cardigan, spring picnic, rainy day, winter coat, art workshop, garden party and evening velvet.

## Details

Emily received eight everyday and occasion looks: florist workwear, café cardigan, spring picnic, rainy day, winter coat, art workshop, garden party and evening velvet. Five more added a navy satin gown, ivory tailored suit, blue floral bikini, teal one-piece and lavender gym set. Sophie then gained thirteen outfits: three bikinis, two gym looks and eight casual/formal options. Amy gained thirteen: three bikinis, two gym looks and eight artistic, casual and formal options. Reports describe transparent PNGs registered in the gallery and Camera outfit chooser, with prompts retained.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-06T21:42:00+10:00 · 01a1b0a4-3cdc-7a21-beb1-1c07b8f6bf15
- 2026-11-06T21:46:31+10:00 · 01a1b0aa-f7a3-7421-869a-14dbfcd96fcd
- 2026-11-06T21:57:18+10:00 · 01a1b0b0-32a9-7033-adfc-45d014fa88d7
- 2026-11-06T22:07:18+10:00 · 01a1b0b9-a26f-7330-aa2e-1d56527f8fdd

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Create 8 Emily outfit variants. All available root-session completion events scanned. 4 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Rei and Ivan outfits, plus hoodie corrections

recovered-01a1b09d-2c19-7b40-9ea7-e32f81090f76 | Retrospective | Art & media
Date: Unknown — reconstructed history

Rei gained eight additional outfits including his black sweater.

## Details

Rei gained eight additional outfits including his black sweater. His charcoal-hoodie shoulders were first broadened, then adjusted to a narrower, softer slope. Six later choices added Japanese techwear, a green-and-ivory sukajan, navy yukata, haori/hakama, gym tank/shorts and teal swim shorts. Ivan gained thirteen looks: two gym, three high-fashion, three idol, four streetwear and one beach outfit. The reports record wardrobe/Camera registration, transparency checks and saved prompts.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-06T21:37:24+10:00 · 01a1b09d-ed27-7fc2-9595-60b264b76501
- 2026-11-06T21:38:35+10:00 · 01a1b0a6-3334-7d80-a607-997755d92d2a
- 2026-11-06T21:40:47+10:00 · 01a1b0a8-423b-7fa2-81d0-63f661e747a7
- 2026-11-06T21:46:59+10:00 · 01a1b0aa-3a71-7123-a2ac-1de64ad85973
- 2026-11-06T22:01:22+10:00 · 01a1b0b1-7f04-7e32-98c5-51cc9c939618

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add Rei outfit variants. All available root-session completion events scanned. 5 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# April outfit request: recovered interrupted work

recovered-01a1b0a5-4deb-7571-930a-f4a702d4f276 | Retrospective | Development history
Date: Unknown — reconstructed history

The root turn was interrupted after setup and planning, with no completion report.

## Details

The root turn was interrupted after setup and planning, with no completion report. It proposed eight distinct April looks matching her established design and intended to add them to the gallery. Current April outfit manifests exist, but they do not prove completion of this particular interrupted request. The archive preserves the interruption instead of inventing a completed release or a validation result.

Recovered reports (chat-completion dates, not release dates):
- No completed report. The source records an interrupted root turn.

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Create eight April outfits. All available root-session completion events scanned. 0 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Expanded Garrett, Ivan, Minsu and Emily group photos

recovered-01a1afe7-fa25-75c1-8da9-9ae7eea19324 | Retrospective | Art & media
Date: Unknown — reconstructed history

Garrett received nine photos: three friendly Rei scenes, two Rei modelling shoots, three April scenes and one larger friend group.

## Details

Garrett received nine photos: three friendly Rei scenes, two Rei modelling shoots, three April scenes and one larger friend group. Ivan received ten: three with Valentina, three solo modelling, two with producers and two with idols. Minsu received nine split between Amy, Sophie and all three together. Emily received nine split between Rei, Sophie and all three together. Each completed batch reports captions, comments, existing-save support and its own historical checks.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-06T18:31:34+10:00 · 01a1afe8-aeb7-7323-8f11-470ba10deb4f
- 2026-11-06T18:54:26+10:00 · 01a1b007-d71d-7c22-bdf8-af2295a4eb40
- 2026-11-06T20:08:39+10:00 · 01a1b049-628e-7942-bf43-202634d7fbf4
- 2026-11-06T21:04:14+10:00 · 01a1b076-1892-7b73-b87e-db6f31e7b163

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add Grove gallery photos. All available root-session completion events scanned. 4 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Yuriko, Lena, Naomi, Celeste, Dev and Rosa galleries

recovered-01a1af57-941c-7bf1-a5e8-a1c5e2e3e207 | Retrospective | Art & media
Date: Unknown — reconstructed history

An inventory of eleven missing galleries preceded six completed eight-photo additions.

## Details

An inventory of eleven missing galleries preceded six completed eight-photo additions. Yuriko’s covers selfies, miniature sets, theatre lighting, dinner and sketches; Lena’s covers photography, conservation and paella; Naomi’s covers bicycle repair, a handmade mug, riding and dinner. Celeste’s includes the planetarium, birds, sourdough and piano. Dev’s includes radios, tabletop games, photography and chai. Rosa’s includes community lunch, gardening, skates and reading. The additions include captions, comments and automatic existing-save upgrades. The old inventory is historical, not a statement that those galleries remain missing.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-06T15:32:28+10:00 · 01a1af57-abd6-74c1-b7bf-d8fa40999686
- 2026-11-06T15:43:35+10:00 · 01a1af5e-7975-7241-9708-f81c1dd1dd90
- 2026-11-06T15:50:19+10:00 · 01a1af62-6a04-7041-b684-5a09ce63f197
- 2026-11-06T15:57:49+10:00 · 01a1af69-2d9d-72f2-a77d-e7725968f98a
- 2026-11-06T16:07:29+10:00 · 01a1af72-6f70-7613-a87d-1394c2145628
- 2026-11-06T16:15:06+10:00 · 01a1af78-c214-7ce3-9539-bd584e650759
- 2026-11-06T17:45:19+10:00 · 01a1afc6-d24e-7062-9994-d9ad1a266749

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Find missing Grove galleries. All available root-session completion events scanned. 7 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Emily’s first Grove gallery and comment counts

recovered-01a1aeeb-7286-7f32-a33a-fab021246e24 | Retrospective | Art & media
Date: Unknown — reconstructed history

The first completed Emily gallery release added two photos with dated captions, likes and four friend comments.

## Details

The first completed Emily gallery release added two photos with dated captions, likes and four friend comments. Gallery cards gained comment counts, and existing saves received the posts automatically. The report cites seventeen tests and a UI smoke check at that time. A later interrupted turn in the same chat has no completion report; subsequent Emily expansions are recorded separately.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-06T13:35:56+10:00 · 01a1aeeb-ae92-7661-ba61-cc741b2e5e5b

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Create Emily’s grove gallery. All available root-session completion events scanned. 1 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Vendetta adaptation and the first Find Charles lead

recovered-01a1a90f-188f-7fd3-9456-046c03b41a8f | Retrospective | World & story
Date: Unknown — reconstructed history

The game guide adopted Vendetta as a source while explicitly excluding Awakened from Mysterious Hearts.

## Details

The game guide adopted Vendetta as a source while explicitly excluding Awakened from Mysterious Hearts. The initial adaptation left some timeline questions open; this is an earlier design stage. A later completed update established Charles’s undercover Syndicate role as writer-only knowledge and kept it out of Garrett’s prompts. Find Charles introduced Mei’s delivery slip dated eleven days after Charles left work, followed by a receiving copy identifying West Pier Cold Storage without a driver signature. The report records both steps, reload persistence and support for existing Garrett saves. A separate interrupted turn is not treated as an additional completed update.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-05T10:16:01+10:00 · 01a1a90f-1b88-7aa1-b8e7-e87debf55f50
- 2026-11-05T10:17:49+10:00 · 01a1a910-21d6-7ce2-948e-d2be9eab6701

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Use Vendetta for world-building. All available root-session completion events scanned. 2 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Source-world lore, resident portraits and character tiers

recovered-01a1b380-8a51-7c92-bca7-f0cc55275a57 | Retrospective | World & story
Date: Unknown — reconstructed history

The first three recovered completions concern external Vendetta reference documents: the Blisk empire and 2023–2036 war, expanded Sylvanis/Ivan history, and Billy Stevens/Alice Granger profiles.

## Details

The first three recovered completions concern external Vendetta reference documents: the Blisk empire and 2023–2036 war, expanded Sylvanis/Ivan history, and Billy Stevens/Alice Granger profiles. They are source-world edits, not proof every detail shipped into Mysterious Hearts. Three subsequent completions concern the game: twelve local residents with routines and tastes; twelve portraits integrated into conversations, Contacts and Messages; and a split between major characters and simpler town NPCs. Major characters retain full systems; locals use familiarity and conversations without romance, Grove or Meet-Cute. Existing NPC conversations remain while obsolete romance progression is archived. Interrupted and in-progress turns at the recovery snapshot are excluded. Historical reports preserve the stated unrelated test failures.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-07T10:56:24+10:00 · 01a1b381-4875-7903-ba01-04ceec8a3a55
- 2026-11-07T11:01:18+10:00 · 01a1b382-9134-7410-8b58-300d0325a6a3
- 2026-11-07T11:07:39+10:00 · 01a1b388-cbb8-7da3-9543-2274ecd92b7c
- 2026-11-07T11:14:56+10:00 · 01a1b38d-ae8c-7023-94b8-c8fa72a36757
- 2026-11-07T11:26:30+10:00 · 01a1b394-04b6-77a0-8306-4fc4cc6ec36d
- 2026-11-07T11:36:28+10:00 · 01a1b39f-2036-7f53-8704-d9ccb56b3eac

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add Blisk to the lore. All available root-session completion events scanned. 6 completed turns; 2 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Rei group photos and tattoo continuity fixes

recovered-01a1af65-5ed7-71c3-bae5-6f589f6c43ca | Retrospective | Art & media
Date: Unknown — reconstructed history

Sixteen Rei group photos were added with captions, comments and save support.

## Details

Sixteen Rei group photos were added with captions, comments and save support. Four additional Rei/Garrett modelling editorials followed, alongside a missing tattoo-sleeve fix for a basketball image. Fifteen original group photos were corrected so exposed forearms and wrists match Rei’s tattoos, preserving engagement and captions. Garrett’s white-tee editorial was also corrected with tattoos on both exposed arms. Each correction remains distinct from new-photo additions.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-06T16:06:30+10:00 · 01a1af66-01d2-7430-9b6b-e9d77b07fec9
- 2026-11-06T16:15:53+10:00 · 01a1af77-40c3-79b3-8234-97c96a5516db
- 2026-11-06T16:46:55+10:00 · 01a1af7f-d5af-7410-b290-930251c165d2
- 2026-11-06T17:39:32+10:00 · 01a1afc7-7138-7e10-94a5-be232585880e

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add group photos to Grove gallery. All available root-session completion events scanned. 4 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Early protagonist Grove artwork batches

recovered-01a1ae49-1819-7e70-a833-e7329c23d5f6 | Retrospective | Art & media
Date: Unknown — reconstructed history

Garrett’s first four generated images covered cooking, noodles, training and eveningwear; the first report explicitly said UI integration was pending.

## Details

Garrett’s first four generated images covered cooking, noodles, training and eveningwear; the first report explicitly said UI integration was pending. Four further photos brought that asset batch to eight. Seven portraits were corrected for dragon sleeves, chest/neck tattoos and a leaner build, leaving the noodle image unchanged. Separate completed batches created nine Rei images (modelling, artistic selfies and artwork), ten Ivan performance/fashion images, and eight Minsu medical-study, food-review, taekwondo and selfie images. These asset-creation reports are not retroactively presented as completed UI integration. One interrupted turn remains excluded.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-06T10:40:09+10:00 · 01a1ae49-1b21-7791-adc9-a6663355f95d
- 2026-11-06T10:44:20+10:00 · 01a1ae4d-530d-7322-b0c6-309d6f134741
- 2026-11-06T10:54:00+10:00 · 01a1ae50-535a-7022-b54d-080b0389921a
- 2026-11-06T11:06:49+10:00 · 01a1ae5a-8289-7b12-99fb-9e3d8cdddf91
- 2026-11-06T11:21:44+10:00 · 01a1ae66-1029-7492-a3d3-dbb982a65032
- 2026-11-06T11:33:55+10:00 · 01a1ae73-a0e7-7c33-9b39-7224f6cbff03

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Generate Garrett gallery images. All available root-session completion events scanned. 6 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Portrait alignment audit: interrupted before completion

recovered-01a1a918-d3c4-7131-8687-64bc9facc63d | Retrospective | Development history
Date: Unknown — reconstructed history

The recovered root turn ended by interruption without a completion report.

## Details

The recovered root turn ended by interruption without a completion report. Its inspection identified inconsistent realistic shading and fabric texture in supporting portraits and an initials placeholder for Valentina. It proposed comparing supplied references, correcting portraits and writing an art guide. No completed alignment pass or finished guide is certified from this chat.

Recovered reports (chat-completion dates, not release dates):
- No completed report. The source records an interrupted root turn.

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Align portraits and add art guide. All available root-session completion events scanned. 0 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Text audio, typing indicators and chat bubbles

recovered-01a1ab33-ec47-7a31-90e4-8c136de39266 | Retrospective | Phone & social
Date: Unknown — reconstructed history

Sent/received MP3 effects were added for direct and group texts with a sound toggle, while in-person dialogue remained silent.

## Details

Sent/received MP3 effects were added for direct and group texts with a sound toggle, while in-person dialogue remained silent. A looping typing sound followed, stopping on completion/error and respecting mute. The next update added a three-dot animated typing bubble with the character name. Another added right-aligned blue outgoing bubbles, left-aligned grey incoming bubbles and group sender names, while preserving the in-person layout. A fifth interrupted turn has no completed update. Audio and layout checks quoted in original reports are historical claims, not new checks performed by this recovery.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-05T20:17:23+10:00 · 01a1ab34-742d-7190-a879-e4dfed8f8dbf
- 2026-11-05T20:18:36+10:00 · 01a1ab36-efb0-7da2-81fa-c165c8835f11
- 2026-11-05T20:23:31+10:00 · 01a1ab3b-57d5-7153-be94-39e102be61b4
- 2026-11-05T20:26:47+10:00 · 01a1ab3c-fe92-76a2-9973-0a0b795a31fe

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add texting notification sounds. All available root-session completion events scanned. 4 completed turns; 1 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Home and sleep portraits, gallery browsing and locks

recovered-01a1a5f5-13ae-7d70-98bb-31b30a320696 | Retrospective | Art & media
Date: Unknown — reconstructed history

Minsu, Rei and Garrett gained home-specific portraits and chat location/travel labels.

## Details

Minsu, Rei and Garrett gained home-specific portraits and chat location/travel labels. Sleep portraits followed for those three, then for Amy, April, Emily, Samantha and Sophie. Ten casual/evening portraits introduced the Portrait gallery with character filters, previous/next navigation and full-resolution drag-to-pan. Five later completions each added six pictures to one love interest’s gallery, bringing each to eight at that stage. Bedroom photos were then gated on an official relationship with that specific character; casual/evening photos remained available. Early sleep-hour descriptions are historical and do not override current schedule logic.

Recovered reports (chat-completion dates, not release dates):
- 2026-11-04T19:50:23+10:00 · 01a1a5f5-c493-7773-9e02-c4b65ea67408
- 2026-11-04T19:55:30+10:00 · 01a1a5fb-7ddb-7c72-9ec7-0251660c0e42
- 2026-11-04T19:58:18+10:00 · 01a1a5fe-3f40-7bc2-a35b-9e2371d358db
- 2026-11-04T20:16:10+10:00 · 01a1a607-1868-7de1-9d6c-179d73b4c71d
- 2026-11-04T20:17:25+10:00 · 01a1a60f-c63b-76f0-9ea0-9cfb5e512810
- 2026-11-04T20:25:13+10:00 · 01a1a616-ff2a-78d2-9f34-2af974b57dd9
- 2026-11-04T20:45:41+10:00 · 01a1a629-c3da-7441-8c21-4bc8bf57c7f1
- 2026-11-04T20:46:10+10:00 · 01a1a62a-2ff3-7e12-879b-9d1d263c5bc3
- 2026-11-04T21:31:43+10:00 · 01a1a652-950f-7830-8178-69487ba89598
- 2026-11-04T21:34:16+10:00 · 01a1a654-4780-79f0-8e2d-39a67f99b392

## Save compatibility

Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.

## Evidence and historical limits

Source chat: Add at-home character portraits. All available root-session completion events scanned. 10 completed turns; 0 unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.

- patch_notes/recovered_history.json
- patch_notes/RECOVERY.md


---

# Town NPC regression checks aligned with character rules

release-2026-11-07-local-character-test-alignment | Release | Relationships
Date: 2026-11-07

Resolved the two legacy local-character test conflicts reported with personality-led flirting and refusals.

## Details

Fixed

Verified the updated Theo dating regression: town NPCs cannot unlock romance through returned flirting, start a date or commit a date invitation. The old local romance expectation no longer applies under the major-character and town-NPC rules.

Updated the Maya reaction regression to use the smaller town-conversation response schema. It checks that the selected reply reaches the conversation without the major-character submitted-tone payload, suggestions are deferred, and generated emotions are preserved instead of overwritten by major-character tone effects. Committing the exchange creates ordinary familiarity without relationship or advanced relationship-dynamics progression.

These checks resolve the two legacy conflicts recorded in the Personality-led flirting and clear refusals entry. This update changes regression coverage and documentation; it does not change character eligibility or dialogue behavior.

Validation

All 63 tests passed across dating, reactions, character types, romantic voices, sexuality, Meet-Cute and familiar conversations. Provider settings were mocked for this offline run. The full game suite and live model dialogue quality were not evaluated.

## Save compatibility

No save migration, story reset or game restart is needed for these test and documentation changes. Existing major-character and town-NPC behavior is unchanged.

## Evidence and historical limits

Recorded on 7 November 2026 (Australia/Brisbane). The Theo regression was already updated in the workspace and was verified here; the Maya regression was updated here. The 63-test focused run passed in this update. Earlier test results remain historical.

- tests/test_dating.py
- tests/test_reactions.py
- tests/test_character_types.py
- town_npc_system.py
- character_types.py


---

# Major characters and town NPCs

release-2026-11-07-major-characters-and-town-npcs | Release | Relationships
Date: 2026-11-07

Two character types distinguish the full major-character experience from simpler, strictly platonic town conversations.

## Details

Changed

Starting characters and every hidden interest are major characters, including platonic interests, Neo and Alyssa. They retain their full character systems. Major status does not automatically make someone romanceable: existing orientation, family and story boundaries still apply.

All older town NPCs, venue staff and the twelve recently added Winterfield residents use the town NPC system. Town NPCs cannot be romanced, added on Grove or discovered on Meet-Cute. This also removes the former local romance paths for Theo, Noah and Leo. Ordinary phone contacts and direct messages remain available through the existing number-exchange system.

Visit residents at their usual town locations to talk, or open Messages for an already saved local contact. Their conversations retain individual backgrounds, interests, recent exchanges and emotions, with simple familiarity instead of attraction, jealousy, dating goals or advanced relationship progression. Conversations on three separate story days establish a familiar face.

Interface

Town conversations show the Town NPC label and familiarity instead of relationship bars. Personal-talk controls and personal-mode message suggestions are unavailable for local-only conversations. Ordinary conversation suggestions remain available. Local phone contacts are identified as town NPCs; major-character contacts use the major-character label.

Save compatibility

Older local conversations and ordinary phone contacts remain available. Obsolete town relationship progression, active local dates and Meet-Cute matches or likes are archived rather than retained as active romance. Scheduled dates associated with removed matches are cancelled. Old local Grove posts are hidden and pending local Grove generation is removed.

Validation

Focused character-type, town-resident, town, dating, relationship-dynamics, Meet-Cute, sexuality, lore, phone-number, messaging, familiar-conversation and inbox-order checks passed during implementation. The character-type UI smoke check and dark-theme smoke across 32 phone pages passed; local conversation and messaging screenshots were inspected.

Known limitations

One separate social-world test had an outdated exact demographic expectation that omitted the sexuality field added by another update. That failure was reported rather than counted as passing. The entire game test suite was not rerun for this change.

## Save compatibility

Restart the game to load the changed code. Existing stories remain usable; migration runs automatically and preserves local chat history while archiving obsolete town romance data. No story reset or manual migration is required. Major-character relationship rules and progress remain in place.

## Evidence and historical limits

Recorded on 7 November 2026 from the character-type implementation and its completed checks in this chat. Validation above describes those implementation checks, not a new full-suite run when publishing this note. Historical entries remain unchanged.

- character_types.py
- town_npc_system.py
- town.py
- groups.py
- phone_apps.py
- meet_cute.py
- relationship_dynamics.py
- game.py
- town_ui.py
- phone_chat.py
- phone_numbers_ui.py
- phone_ui.py
- conversation_lore.py
- Mysterious Hearts - Character References.md
- tests/test_character_types.py
- tests/test_dating.py
- tests/character_types_ui_smoke.py
- tests/phone_dark_theme_smoke.py


---

# Detailed physical types and character appearance references

release-2026-11-07-detailed-physical-types | Release | Relationships
Date: 2026-11-07

Hair, eyes, facial features and body type now shape each character’s physical preferences, with a shared appearance document used in dialogue.

## Details

Added

All 25 orientation-defined characters now have individual hair, eye, facial-feature and body-type preferences alongside height, overall appearance and usual fashion. Each list contains alternatives: a partner need not match every listed trait. Physical matching considers seven equally weighted dimensions; unknown details count as neutral. Hair preferences may concern colour or styling, and eye preferences may concern colour or shape.

Changed

The added details influence new stranger attraction, emerging NPC chemistry and the private guidance used for early romantic reciprocation. Personality-based long-term growth is unchanged. Preferences remain tendencies rather than gates, and never override consent, orientations, family boundaries or existing relationship history.

Character appearance document

Mysterious Hearts - Character Appearances.md records recognisable features, usual portrait clothing and structured matching descriptors. Dialogue now reads its descriptions for the speaker, listeners and other people already known by sight under the existing visibility rules. Texting does not establish a live view. Current scene outfits override reference styling. Unspecified eye colours, builds or facial details are left unknown rather than invented. The document preserves the authored descriptions for all 44 characters with appearance references.

New preference details

| Character | Hair alternatives | Eye alternatives | Facial features | Body type |
| --- | --- | --- | --- | --- |
| Rei | blonde, long, wavy | blue, hazel | delicate, fine features | petite, slim |
| Garrett | dark-brown, straight, shoulder-length | brown, dark | delicate, fine features | petite, slim |
| Minsu | brunette, ponytail, bob | green, hazel | strong brows, expressive | athletic, lean |
| Ivan | black, dark-brown, wavy | dark, grey-green | angular, strong brows | lean, broad shoulders |
| Emily | black, layered, shaggy | dark | angular, sharp jaw | lean, defined shoulders |
| Sophie | black, short, tousled | dark, green | soft contours, strong brows | athletic, muscular |
| Amy | black, curly, wavy | dark, hazel | soft contours, delicate | lean, slim |
| Samantha | blond, black, short | golden, dark | angular, strong brows | muscular, broad shoulders |
| April | blond, ash-brown, tousled | golden, brown | angular, strong brows | athletic, broad shoulders |
| Yuriko | black, tousled, curly | dark, brown | soft contours, expressive | lean, slim |
| Lena | dark-brown, auburn, curly | hazel, green | angular, fine features | lean, slender |
| Naomi | black, short, bob | dark, brown | strong brows, fine features | athletic, lean |
| Celeste | black, layered, wavy | dark, hazel | delicate, soft contours | lean, slim |
| Valentina | sandy-blond, silver-grey, short | green, grey-green | strong brows, angular | athletic, muscular |
| Dev | dark, curly, bob | dark, brown | soft contours, rectangular glasses | slim, curvy |
| Elliot | black, dark-brown, tousled | dark, green | strong brows, clean-shaven | lean, athletic |
| Tyler | black, short, locs | dark, hazel | strong brows, angular | athletic, muscular |
| Daniel | black, layered, wavy | dark, grey-green | angular, sharp jaw | lean, broad shoulders |
| Rosa | dark, curly, tousled | brown, dark | soft contours, moustache | broad shoulders, curvy |
| Neo | near-black, long, wavy | purple, dark | fine features, elongated ears | slim, slender |
| Alyssa | black, tousled, short | grey-green, dark | angular, strong brows | lean, muscular |
| Sylvanis | black, long, straight | dark, green | angular, fine features | slender, lean |
| Theo | auburn, dark-brown, wavy | hazel, dark | delicate, rectangular glasses | slim, lean |
| Noah | dark, short, curly | dark, brown | soft contours, expressive | lean, curvy |
| Leo | brunette, ponytail, short | green, dark | strong brows, expressive | athletic, lean |

Validation

88 focused tests ran: 86 passed, including all eight romantic-type tests. Two unrelated failures also reproduce with the new physical dimensions and document lookup disabled: the local-romance conversation fixture lacks required emotion data, and the profile-demographics assertion does not expect the existing Sexuality field. No phone UI surfaces changed.

## Save compatibility

Existing saves need no reset or migration. Restart the running game to load the new code and cached appearance reference. Existing attraction, established crushes and relationship history remain intact; future physical matching uses the expanded preferences.

## Evidence and historical limits

Implemented in this chat on 7 November 2026. Actual appearance descriptions preserve the existing Character References canon; new preferences are authored independently. Test counts record the focused run for this update, including the two reproduced unrelated failures.

- romantic_types.py
- character_appearance.py
- Mysterious Hearts - Character Appearances.md
- social_world.py
- tests/test_romantic_types.py
- tests/test_social_world.py
- tests/test_conversation_lore.py


---

# Personality-led flirting and clear refusals

release-2026-11-07-individual-romantic-voices | Release | Relationships
Date: 2026-11-07

Characters flirt and turn down advances in their own voices while respecting sexuality, consent and relationship boundaries.

## Details

Added

Individual flirting and refusal guidance for all 25 characters with canonical orientations. Rei uses spare, deadpan warmth; Garrett brings confident, cheeky banter; Emily can be shy without making her answer ambiguous; Samantha is frank; April is precise and restrained. Other characters retain their own pacing, humour and ways of expressing interest. Platonic and committed characters keep their existing route boundaries.

Where to find it

The guidance applies automatically to ordinary conversations, private and group texts, on-demand player suggestions, date-invitation replies and Meet-Cute chats. Open Meet-Cute on the phone to see character-specific readiness refusals when asking for numbers, a date or exclusivity. No new setting is required.

Changed

Generated responses distinguish orientation incompatibility, lack of interest, unreadiness and scheduling conflicts. Humour, pauses and nervousness must not obscure a clear answer. Repeated pressure calls for a firmer boundary, not escalating flirtation. Delivery guidance encourages fresh wording grounded in the actual exchange instead of repeated apologies, hobby metaphors or stock pickup lines. The player's voice guidance applies to unsent suggestions, not rewrites of their submitted words.

Meet-Cute's shared readiness-refusal lines are replaced with authored responses for each participating character. Existing acceptance criteria, scheduling checks, orientation eligibility and consent rules remain authoritative. Dev and Elliot's older blanket platonic dialogue instructions now allow reciprocation only when their canonical orientations, current interest and route boundaries permit it.

Validation and known limitations

44 focused tests passed across romantic voice, sexuality, Meet-Cute and familiar-conversation suites. Checks cover cast guidance, prompt integration, incompatible-pair restrictions, state preservation during generation, and character-specific readiness refusals that still decline the request. No live model quality evaluation or UI layout change was part of this update; generated wording remains model-dependent, while the offline readiness replies are authored lines.

A broader check also encountered two existing local-character test conflicts: a Theo dating test assumes a local romance route, and a Maya reaction test expects the older generated local-conversation tone payload. The workspace's newer major/minor-character behavior differs from those assumptions; this entry does not claim those tests passed.

## Save compatibility

Existing saves remain compatible. Restart the running game to load the updated dialogue guidance. Stored conversations and past replies are retained; future generated replies and new Meet-Cute readiness refusals use the new wording. This update does not change canonical sexuality, romance eligibility or relationship thresholds.

## Evidence and historical limits

Implemented in the preceding update in this chat and recorded on 7 November 2026 (Australia/Brisbane). The 44-test passing run and two broader legacy local-character failures were observed in that update; historical results are not represented as a new full-suite run.

- romantic_voice.py
- sexuality.py
- meet_cute.py
- dialogue_styles.json
- tests/test_romantic_voice.py
- tests/test_sexuality.py
- tests/test_meet_cute.py
- tests/test_familiar_conversations.py
- tests/test_dating.py
- tests/test_reactions.py


---

# Canonical romantic type preferences

release-2026-11-07-romantic-types | Release | Relationships
Date: 2026-11-07

Characters have individual physical and personality types that influence initial attraction and lasting affection.

## Details

Added

All 25 characters with defined orientations now have canonical romantic preferences. These work automatically in romance dialogue and relationship simulation; there is no new settings screen. Physical type covers height, appearance and usual fashion. Personality type covers interests, introversion/extroversion and lifestyle.

Changed

Physical fit influences new stranger attraction and emerging NPC chemistry, and guides early reciprocation in generated dialogue. Personality fit determines the chance of positive long-term feeling growth during hourly simulation updates: 15% for a complete mismatch, 85% for a full match, with partial matches in between. Exceptions remain possible. Negative feeling changes, friendship, trust, orientation, family boundaries and consent keep their existing rules.

Canonical preferences

These describe the preferred partner, not the character’s own traits.

| Character | Height (cm) | Appearance | Fashion | Interests | Sociability | Lifestyle |
| --- | --- | --- | --- | --- | --- | --- |
| Rei | 150–175 | Soft | Casual | Crafts | Introvert | Quiet |
| Garrett | 145–172 | Delicate | Classic | Science | Introvert | Structured |
| Minsu | 155–178 | Athletic | Sporty | Sports | Extrovert | Active |
| Ivan | 165–190 | Striking | Artistic | Music | Introvert | Creative |
| Emily | 178–195 | Delicate | Artistic | Art | Introvert | Creative |
| Sophie | 170–193 | Athletic | Streetwear | Sports | Extrovert | Active |
| Amy | 170–190 | Soft | Artistic | Art | Introvert | Creative |
| Samantha | 178–198 | Athletic | Bold | Sports | Extrovert | Active |
| April | 175–193 | Athletic | Classic | Cooking | Extrovert | Structured |
| Yuriko | 170–188 | Soft | Casual | Crafts | Extrovert | Creative |
| Lena | 165–190 | Striking | Artistic | Photography | Introvert | Adventurous |
| Naomi | 160–185 | Athletic | Practical | Outdoors | Introvert | Active |
| Celeste | 170–195 | Delicate | Artistic | Music | Introvert | Quiet |
| Valentina | 170–195 | Athletic | Casual | Outdoors | Extrovert | Adventurous |
| Dev | 160–190 | Soft | Practical | Science | Introvert | Creative |
| Elliot | 170–195 | Athletic | Casual | Outdoors | Introvert | Quiet |
| Tyler | 165–193 | Athletic | Sporty | Sports | Extrovert | Active |
| Daniel | 175–195 | Striking | Artistic | Art | Introvert | Creative |
| Rosa | 170–190 | Soft | Practical | Cooking | Extrovert | Social |
| Neo | 155–178 | Soft | Artistic | Crafts | Introvert | Quiet |
| Alyssa | 175–190 | Athletic | Practical | Science | Introvert | Quiet |
| Sylvanis | 165–185 | Striking | Tailored | Art | Extrovert | Social |
| Theo | 170–195 | Delicate | Artistic | Books | Introvert | Quiet |
| Noah | 160–190 | Soft | Streetwear | Gaming | Extrovert | Social |
| Leo | 155–180 | Athletic | Sporty | Outdoors | Extrovert | Adventurous |

Known limitations

Appearance and interests currently use broad tags, not detailed hair, eye or facial-feature preferences. Fashion means usual presentation, not a live outfit check. Dialogue probabilities are guidance to the dialogue generator, while long-term growth uses an actual probability roll.

Validation

53 tests passed across romantic types, mysterious hearts, sexuality, dating, social events and relationship dynamics. Save-related tests used a workspace temporary directory. No phone UI surfaces changed.

## Save compatibility

Existing saves remain compatible; no reset or manual migration is required. Restart the running game to load the changed Python code. Saved attraction, established relationship history and Emily’s authored crush are retained. Future affection growth uses the new preferences.

## Evidence and historical limits

Implemented and verified in this chat on 7 November 2026. Preferences are taken directly from romantic_types.CANON; validation records the 53-test combined run completed before publication.

- romantic_types.py
- town.py
- sexuality.py
- mysterious_hearts.py
- tests/test_romantic_types.py
- tests/test_mysterious_hearts.py
- tests/test_sexuality.py
- tests/test_dating.py
- tests/test_social_events.py
- tests/test_relationship_dynamics.py


---

# A permanent update archive

release-2026-11-07-patch-notes | Release | Interface
Date: 2026-11-07

Searchable patch notes, a detailed retrospective and original development reports.

## Details

Added a dark desktop patch notes reader from the start screen and Tools menu. Search titles, details and sources; filter category, entry type, unread and bookmarks; sort by catalogue order, title or documented date.

Read status is explicit and revision-aware: edited entries become unread again. Bookmarks and read state live outside story saves. Export the selected note or current filtered results to Markdown.

The archive preserves README sections and recovered completed development reports. Original reports are optional in the viewer because they include advice and obsolete behavior. Unknown release dates and missing oversized chat records are disclosed.

Future updates use stable IDs, source references, compatibility notes and schema validation. The first archive does not assign fictional version numbers to older work.

Validation: catalogue validation, six focused unit tests, patch-reader interaction/layout smoke, start-screen smoke and dark-theme smoke across 32 phone pages passed. Rendered layouts were inspected. Historical features were not all rerun; see the validation record for scope and sound warnings.

Recovery follow-up: the 17 oversized-chat retrieval gaps described above were subsequently resolved from local logs. See Recovered the 17 oversized development chats and patch_notes/RECOVERY.md. Interrupted work remains labelled.

## Save compatibility

No story reset or save migration. Reader preferences are separate from stories.

## Evidence and historical limits

First dedicated patch notes release, authored in this change. Automated validation is documented separately from historical test claims.

- patch_notes.py
- patch_notes_ui.py
- patch_notes/AUTHORING.md
- patch_notes/VALIDATION.md


---

# More Winterfield neighbours

history-more-winterfield-neighbours | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: More Winterfield neighbours.

## Details

All twelve residents have individual transparent manhwa portraits in `assets/portraits/<name>-selection.png`. They appear in local conversations, saved local contacts, and direct-message headers and bubbles. Built-in image-generation prompts and appearance references are preserved in `assets/portraits/town-residents-manifest.json`. Run `python tests/town_portraits_smoke.py` to verify the assets and their actual Tk loaders without AI requests or save writes.

Twelve additional adult locals now appear in the existing town encounter list: Priya the librarian, Otis the retired mechanic, Nadia the shuttle driver, Ben the bowling technician, Tess the projectionist, Farah the tailor, Gabe the bicycle repairer, Wren the animation student, Celia the nurse, Arthur the history volunteer, Luz the gardener and Samir the bakery driver.

Visit the library, shops, downtown, parks and leisure venues to meet them. Their public routines change at 08:00, noon, 17:00 and 22:00, with different weekend stops; rain moves exposed outdoor visits into the library. Their routines continue while you wait. Each has personal interests, connections to other residents and rotating conversation topics. They use the existing local conversation, history and phone-contact systems, without adding romance routes or automatically revealing everyone's number. Existing saves receive the roster when loaded; restart the game to load the updated code.

These are background routines rather than simulated driving journeys. Their personal projects are conversation material, not automatically completed quests or player memories. Focused checks: `python -m unittest discover -s tests -p test_town_residents.py -v`.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — More Winterfield neighbours


---

# Phone numbers and adding contacts

history-phone-numbers-and-adding-contacts | Retrospective | Phone & social
Date: Unknown — reconstructed history

Preserved update documentation: Phone numbers and adding contacts.

## Details

Every named, contactable resident has a stable fictional number, including the protagonists, hidden cast, local residents and venue staff. Your own number and saved contacts' numbers appear in **Phone → Contacts**. Use **Add a contact by phone number** to save someone using their full number; spaces, parentheses, hyphens and an optional `+1` are accepted. Adding an existing contact does not duplicate it. Invalid and unassigned numbers show an inline error.

When a Meet-Cute match agrees to exchange numbers, their reply includes the actual number and saves it in Contacts. The match screen shows the saved number and provides **View saved contact** and **Open Messages**. Adding a hidden resident by number records an online introduction, without marking a physical meeting or revealing a home address. Existing saves keep their contacts and receive assigned numbers automatically; undiscovered numbers are not shown as a public directory.

Meet-Cute remains a screen inside the phone, including validation messages and unmatch/block confirmations. Its contact links navigate within the same phone. Regression checks: `python -m unittest discover -s tests -p test_phone_numbers.py -v` and `python tests/meet_cute_ui_smoke.py`; the latter verifies that these interactions create no additional top-level windows.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Phone numbers and adding contacts


---

# Meet-Cute dating app

history-meet-cute-dating-app | Retrospective | Relationships
Date: Unknown — reconstructed history

Preserved update documentation: Meet-Cute dating app.

## Details

Open **Phone → Meet-Cute → Profile** to publish a dating profile. Choose up to three photos from your signature portrait, Camera Gallery or saved Wardrobe designs, add a bio, and answer three prompts. Age and identity come from the protagonist's canon; occupation visibility is optional. Interest fields are read-only dropdowns backed by the same whitelist used when saving:

| Protagonist | Selectable canon interests |
| --- | --- |
| Garrett | Cooking, Jeet Kune Do, Sanda |
| Rei | Drawing, Poetry, Cooking |
| Minsu | Science, Video games, Anime, Taekwondo, Reviewing food |
| Ivan | Singing, Piano, Music, Modelling |

**Preferences** controls adult age range, gender, relationship intentions, a shared canon interest and approximate neighbourhood. Age and gender always filter. The other settings can be required or preferred. These neighbourhoods are profile information, not live tracking. **Discover** offers at most five profiles per game day for the current preferences. A pass lasts that day; some residents join after later days, and profile prompts occasionally change. Family, the player themself, Rosa's platonic route and Sylvanis are excluded.

Like a particular photo or prompt and include a message. Character compatibility, established relationships, interests and opening style influence whether an outgoing like becomes a match. NPCs can also send likes commenting on your published profile. These authored app decisions use story time, respect sleep, and do not require AI calls. **Likes** lets you accept or decline; **Matches** includes unread counts and “Your turn.” Matched chat replies use the game's configured dialogue provider, run in the background after a character-specific delay, and offer a manual retry on failure. No substitute reply is invented when generation fails.

Hidden cast can be discovered and matched entirely inside the app. A match does not reveal private biography, a home address, a live location or a phone contact. An accepted number-exchange request unlocks ordinary Messages and records an online introduction without marking an in-person meeting. Profile snapshots and private chat history provide continuity for that participant's later conversations. Unrelated characters do not receive those records.

Propose a public first date from the match conversation. It appears in Calendar only after the match agrees, considering familiarity, availability and conflicting appointments. Dates can happen before numbers are exchanged. Travel to the venue and use **Join date** during the agreed time; actual co-presence establishes the first meeting. You can cancel an agreed date, pause discovery, unmatch or block. Unmatching also cancels future Meet-Cute dates; it does not silently break up an established relationship. Exclusivity discussions use the existing relationship requirements and pause discovery when accepted.

Profiles, preferences, drafts, likes, matches, pending replies and dates persist with each story. Older saves remain compatible and have no dating-app activity until a profile is published. Focused checks: `python -m unittest discover -s tests -p test_meet_cute.py -v` and `python tests/meet_cute_ui_smoke.py`. The UI check exercises all protagonist dropdowns, hidden matching, draft preservation, generated-chat delivery and failure/retry with a mocked provider.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Meet-Cute dating app


---

# More phone apps and outfit design

history-more-phone-apps-and-outfit-design | Retrospective | Phone & social
Date: Unknown — reconstructed history

Preserved update documentation: More phone apps and outfit design.

## Details

Swipe through the phone home pages to find eight additional apps. Their records and form drafts belong to the current story save, including older saves opened after this update.

- **Mixtape:** save playlists with song titles, artists and a dedication or memory; share a snapshot privately with a contact. This is an in-world playlist notebook, without audio streaming.
- **Wardrobe:** preview and wear existing looks or generated designs. **Design outfit** takes a name and clothing description, uses the player's portrait as a likeness reference, and calls the same Codex built-in image-generation bridge as Camera. A completed design becomes a wardrobe option, a player portrait, and a Camera clothing reference.
- **Out & About:** book cinema, dinner, bowling or a creative workshop with a contact. Prices are charged immediately, appointments appear in Calendar, and cancellation before the start refunds once. These follow the existing Calendar rule that scheduled guests attend automatically.
- **Pocket Wallet:** see the current balance, app purchase receipts and refunds, or pay your rounded-up share of a new bill. Splitting does not invent payments from other characters or amend earlier purchases.
- **Winterfield Exchange:** purchase daily secondhand listings and collect them at the named venue. Known characters can list items through community stalls. Collected finds enter inventory and are available as gifts.
- **Recipe Box:** save recipes, share them privately, buy ingredients and cook in a home kitchen. Cooked meals become recent Camera activity; use Calendar to arrange cooking nights.
- **Postcards:** choose a Gallery photo, write a message and send it to a contact. The card is retained in the app and appears as an outgoing photo in Messages.
- **Campus Portal:** enroll in community courses, submit weekly written assignments, join clubs and complete daily practice at their venues. Courses are available to residents as well as students; study sessions use Calendar.

Outfit generation uses the existing Codex ChatGPT login and plan allowance, with no API-key fallback. Switching phone apps does not interrupt it. Cancel stops the request; failures preserve the description for a manual retry. Closing the game cancels active generation. Generated assets remain under `assets/generated/`; keep that folder when transferring saves. A result from an earlier story is not inserted into a different loaded story.

Focused validation: `python -m unittest discover -s tests -p test_lifestyle_apps.py -v` and `python tests/lifestyle_ui_smoke.py`. The UI smoke test mocks image generation, exercises all eight screens, and covers saved drafts, switching apps during a job, failure, cancellation, preview and wearing a design. It does not consume generation allowance.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — More phone apps and outfit design


---

# Sending photos in Messages

history-sending-photos-in-messages | Retrospective | Phone & social
Date: Unknown — reconstructed history

Preserved update documentation: Sending photos in Messages.

## Details

In a chat, tap **+ → Attach photo from Gallery**, choose a photo, optionally type a caption, then tap **Send**. Direct and group chats support photos. Take photos in Camera to add them to the Gallery. Attachments and unsent photo selections stay with the save. Tap a sent photo bubble and choose **View photo** to open it. Characters receive the photo’s recorded type and location as text context; the image itself is not sent to the dialogue model.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Sending photos in Messages


---

# Personal phones and pinned messages

history-personal-phones-and-pinned-messages | Retrospective | Phone & social
Date: Unknown — reconstructed history

Preserved update documentation: Personal phones and pinned messages.

## Details

Open **Phone → Settings → Personalise phone & controls**. Phone mode keeps a fixed **9:16** portrait window; tablet mode keeps **3:4** proportions. Choose a scale or **Fit to screen**. Message text size is independent of device size.

The home screen uses iPhone-style app pages instead of a scrolling grid: swipe/drag left or right, click the page dots or arrows, or use the arrow keys while the home screen is focused. Messages, Camera and Contacts stay in the dock on every page. Your last page is remembered. Chats use a centred contact header, blue outgoing/grey incoming bubbles, a fixed bottom composer and a home indicator. Tap **+** or **•••** for the options view containing suggestions, emoji, retry, wait and other controls. App content and message history retain vertical scrolling where appropriate.

**Tap or right-click any delivered message bubble** to pin/unpin it or copy its text. Keyboard users can focus the history, choose messages with Up/Down and open the menu with Enter. The three-message limit is shared across chats. Pinned bubbles display a badge; the pinned-message bar opens a list that jumps to the selected message. Earlier starter texts and group messages support the same controls; unfinished messages cannot be pinned. The Messages inbox shows avatars, latest-text previews and the latest message’s story time (with a date for older messages), ordered newest first beneath pinned chats; right-click a row (or focus it and press Space) to pin/unpin the conversation separately.

Garrett, Rei, Minsu and Ivan each start with their own generated wallpaper, home accent, app order, contact names, favourites, an earlier saved image, a personal note and three earlier messages. Earlier messages are clearly labelled and kept outside AI conversation history; they do not award relationship progress. Opening the phone adds these defaults to older saves without resetting progress, existing phone customisations or legacy contact aliases.

- **Contacts:** edit phone-only names, favourite contacts, choose contact photos from this story’s Camera Gallery, and select Default, Chime, Soft or Silent notification tones. Names affect phone headers, search and lock-screen notifications; character IDs, spoken dialogue and public Grove identities stay separate.
- **Messages → Pinned messages / Search:** pin up to **three individual messages across the phone**, including group messages. Each protagonist has a different starting set. Unpin one before adding a fourth. Search delivered texts by contact name or words; spoken conversations and undiscovered contacts are excluded. Pinned chats are separate and do not use message-pin slots. An unread-only filter is available in Messages.
- **Notes:** write private theories and reminders beneath the protagonist’s starting note. Notes save when leaving the screen or closing the phone and are not sent to characters.
- **Gallery:** view the protagonist’s earlier saved image. New Camera Gallery photos become available as wallpapers and contact pictures. Wallpaper selection has a preview and an Apply button. Restore protagonist appearance resets cosmetics while retaining notes, pins and story progress.
- **Lock:** show full previews, sender names only, or generic new-message notices. This is a cosmetic lock screen, not a security lock.
- **Controls:** Escape or Alt+Left goes back; Ctrl+H opens Home; Ctrl+F opens message search. Home remains available at the bottom. Drafts and conversation scroll positions persist; **Latest** jumps to the newest message. Optional reply confirmation shows the exact response before sending.
- **Comfort:** choose instant, fast or gentle text reveal, hide the typing indicator, reduce animation, independently adjust notifications/typing/voicemail volume, and hide relationship meters in phone contact profiles. These presentation controls do not bypass character availability or AI generation time.

Cosmetics, notes, pins and contact preferences belong to each save. Device sizing and accessibility settings are shared through the ignored local `phone_preferences.json`. Wallpaper assets are `assets/ui/phone-wallpaper-{garrett,rei,minsu,ivan}.png`; built-in image-generation prompts are recorded in `assets/ui/phone-wallpapers-prompts.txt`. The two additional notification tones are locally synthesized WAV assets.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Personal phones and pinned messages


---

# Contact profiles and anonymous notes

history-contact-profiles-and-anonymous-notes | Retrospective | Phone & social
Date: Unknown — reconstructed history

Preserved update documentation: Contact profiles and anonymous notes.

## Details

Restart the game to load these additions; existing stories gain their state automatically.

**Phone → Contacts → Full profile & shared history** now includes attraction, trust and closeness, public About Me and favourites, communication preferences, likes, dislikes and boundaries. Personal facts learned in delivered conversations stay attributed in the private notebook; explicit favourite-food/movie/music statements also populate the discovered favourites display. Unknown preferences remain unknown. Shared memories, promises, relationship milestones and Gallery access sit alongside private questions, keepsakes and plans. Pin notebook entries and mark your own plans complete; these personal annotations do not claim that an NPC witnessed or agreed to them.

Open your own contact to edit profile fields, select an available portrait outfit, and choose public, private or selected-contact visibility for each field. Visible fields are included in character conversation context, so characters can respond to your interests. NPC statuses follow their daily activities. Private notebooks never enter another character's dialogue context.

Characters who begin as close friends or siblings already know each other's everyday favourites from the character reference tables. Contacts label these as known from shared history, including meals, drinks, TV shows, movies, books and authors. This also applies to NPC knowledge and existing saves; later relationship damage does not erase established knowledge. New closeness alone does not invent a disclosure, and unspecified tastes remain unknown. Your own contact shows your established tastes while retaining any profile edits.

Your own contact has no discovery requirements. Its private personal-reference panel includes your established background, personal and private history, experience, appearance and tastes from the reference tables. The profile editor starts with your known preferences; unassigned preferences say “Not set” rather than “Not shared.” This does not publish your private history or fill in any memory gaps explicitly left unresolved in canon.

Established favourites and shared history also feed direct texts, in-person conversations, queued group texts and manual player suggestions. Dialogue instructions ask characters to build on what they already know rather than ask introductory questions again. A delivered change of preference updates only the people who heard it; group references retain audience privacy. Prompt regression tests cover these paths without making live AI requests; wording still depends on the selected model.

Newly delivered self-disclosures automatically update observer-specific contacts and future conversation context. This includes favourite meals, drinks, TV shows, books and authors, plus explicit hobbies, likes, dislikes, allergies, hometowns, work, studies and boundaries. Multiple hobbies are retained; newer favourite values replace older values only for listeners who heard the update. Broader personal details are saved as exact, attributed quotes when the conversation model identifies them, including asynchronous text replies. Notes identify hearsay separately, and unspoken model notes are rejected. Parsing is conservative: questions, hypotheticals and ambiguous wording do not establish a new profile value. Existing recorded utterances remain usable without replaying conversations.

**Phone → Mysterious Hearts** supports anonymous notes to contacts, incoming notes, anonymous replies, identity reveals, closed conversations and sender blocking. Choose a note's intention when composing. Draft text and thread history persist with the story. The app icon shows unread notes. Blocking also prevents the same sender opening another thread to bypass the boundary.

Within a thread, compare its wording with your own shared memories, record supporting or conflicting clues, choose a suspect, ask directly, approach them warmly, accuse them, share a copy with a friend, or leave the mystery alone. Suspicions are separate from confirmed identities. Accusations can reduce the accused person's trust; acting warmly on a mistaken theory changes expectations in one direction. Enjoying an anonymous conversation builds an attachment to the thread, which does not automatically transfer to a person at reveal. Friends receive snapshots of shared messages, never access to future replies or later reveals.

NPCs also send notes to one another and investigate using their own memories, relationships and personality. These actions run on story time without extra AI requests. Authored notes and replies currently provide the autonomous message text; ordinary generated conversations receive only the relevant speaker's app knowledge and current feelings. Free-form dialogue adherence remains dependent on the selected model.

Emily begins with Rei as her canonical crush. Unchanged relationships preserve that starting feeling; hurt and changing chemistry can alter it. Other romantic recipients require sustained interest, rather than a single friendly exchange. Notes can become more personal, pause, stop, or receive a closure message. Earlier confessions remain sincere historical messages even after feelings change. Emily's automatic enthusiasm for Rei's date invitations now depends on her current feelings.

Focused checks: `python -m unittest discover -s tests -p test_mysterious_hearts.py -v` and `python tests/hearts_ui_smoke.py`. The latter opens mocked phone screens without generating dialogue or saving a player story.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Contact profiles and anonymous notes


---

# ChatGPT sign-in option

history-chatgpt-sign-in-option | Retrospective | AI & platform
Date: Unknown — reconstructed history

Preserved update documentation: ChatGPT sign-in option.

## Details

Open **AI & account** from the main menu or conversation sidebar. Choose **Continue with ChatGPT**, finish sign-in in your browser and approve ChatGPT plan usage. Refresh the connection if necessary, select one of the models returned for your account, and click **Use selected ChatGPT model**. Use **Use local Qwen 3.5 9B Abliterated** to switch back. The game never silently falls back between providers.

ChatGPT mode sends story context and conversation text to OpenAI, using eligible plan allowance or available credits. **Manage ChatGPT usage** opens your usage settings. **Disconnect** removes this game's local credentials and attempts remote revocation. This does not sign you out of other OpenAI applications. No API key is needed; the game does not read Codex or browser credentials. Your password stays in the browser. The official SDK verifies identity, handles refresh and stores tokens under `.chatgpt/`, encrypted through Windows DPAPI for your Windows account. Non-secret provider preferences are in `ai_settings.json`; both paths are git-ignored.

Sign-in and live ChatGPT inference require your browser authorization and an eligible account. Automated tests use mocks; a disconnected SDK status check is not proof of a successful account connection.

Official integration documentation: [Sign in with ChatGPT](https://developers.openai.com/cookbook/articles/sign-in-with-chatgpt). The vendored official SDK is retained in `vendor/sign-in-with-chatgpt-devkit` with its license and notices. Its noncommercial license applies to this personal local integration; review that license before commercial distribution.

For another machine, install Node.js 22.12+ and the dependencies from `package.json` (`npm install` or `pnpm install`), then run `npm run build:signin`. Keep the vendor SDK directory and its license files. Python/Tk still runs the game; Node runs the private sign-in bridge. The SDK source revision is recorded in the vendored repository.

Double-click **Launch Mysterious Hearts.cmd**. Choose Garrett, Rei, or Minsu, then select a love interest to receive her opening text. Character responses arrive before any suggestions. Type a custom response and press Enter or click Send, or click **Suggest replies** to generate four optional choices. Both portraits appear above the dialogue.

New conversations now begin automatically with an incoming text from the selected love interest. Wait for her first message, then type your own reply or click **Suggest replies**. Each woman has an individual texting style. Messages remain remote exchanges; invitations do not automatically move the characters into a meeting. Already-started conversations in older saves retain their previous mode; untouched contacts start by text. Failed opening requests can be retried without sending a fabricated player message.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — ChatGPT sign-in option


---

# Subscription-only image generation

history-subscription-only-image-generation | Retrospective | AI & platform
Date: Unknown — reconstructed history

Preserved update documentation: Subscription-only image generation.

## Details

Open **Portrait gallery → Image studio · Generate**, describe an image and click **Generate image**. The game runs the installed Codex CLI in the background and automatically imports and displays the resulting PNG. Completed images and their prompts persist under `assets/generated/` and appear in the studio when reopened. Existing character portraits and backgrounds are not overwritten.

Images use **Codex's ChatGPT login**, independently of the game's dialogue sign-in. Open Codex and sign in with ChatGPT (or run `codex login`) first. API-key logins are rejected. The bridge forces ChatGPT authentication, removes API-key environment variables, ignores user CLI configuration, disables shell tools and external integrations, and has no paid API fallback or automatic retry. Usage counts against the ChatGPT/Codex plan and its limits; included allowances and any account-level credits remain governed by OpenAI's account settings.

Generation can take several minutes. Cancel stops the local job; usage already incurred may still count. Closing the studio cancels its pending request. If login, generation, or usage limits fail, the studio displays an error. The bridge requires a Codex CLI with built-in image generation; this workflow was verified with `0.166.0-alpha.6`. Local failure diagnostics are stored in the failed job folder.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Subscription-only image generation


---

# Phone Camera and Gallery

history-phone-camera-and-gallery | Retrospective | Phone & social
Date: Unknown — reconstructed history

Preserved update documentation: Phone Camera and Gallery.

## Details

Known contacts post their own Grove photos on randomized, character-specific schedules measured in story time. Frequent posters such as Sophie post every 4–12 hours; quieter accounts such as April can wait 2–5 days. The configured dialogue provider writes the photo concept and caption, then the same Codex ChatGPT image generator used by Camera creates the image, with character portraits as selfie references. Photos appear in the feed and character profiles, and follower-scaled likes accumulate over the first day. Schedules persist with the save; time skips queue at most one photo per contact. Image generation runs separately from text comments, waits for active Camera jobs, and offers **Retry character photos** in Grove after failures. Automatic character photos use the same Codex plan allowance as Camera.

To edit or delete custom camera presets, open **Custom… → Manage saved descriptions** in a wheel, or **Choose outfits → Manage saved outfits** for a person. Select a saved description, edit it and click **Save changes**, or choose **Delete saved**. Active selections follow edits and return to a default when deleted; existing photos keep their original details. Outfit management is specific to the selected character.

Use **Custom…** in the expression, pose or group-pose wheel to type a description or choose a previously saved one, then **Save & use**. Descriptions support 1–500 characters and persist with the save, independently for each category. Saved custom choices also appear in the wheels and can be reused for the player or companions. Group descriptions can specify each person's pose.

The expression and pose wheels include stoic, smoulder, smirks, shy smiles, intense gazes, casual stances, seated poses, and more group and romance poses. Use **Previous set / Next set** to browse eight choices at a time. Visiting the **Downtown modelling studio** adds editorial, runway, commercial and beauty expressions and poses. Choose **Modelling portrait** for a photographer-framed shot with studio lighting and framing suited to the pose. Studio-only choices reset when you leave; photos still save to the dated Gallery.

Open the phone's **Camera** to take photos using the subscription-only Image Studio bridge. At home, choose **Selfie**, **Mirror selfie**, or **Photo of hobby**. Elsewhere choose **Selfie** or **Photo of environment**; **Photo of activity** appears when there is a recent recorded activity/meal or you describe what is in front of you. The hobby field offers the player's home activities and also accepts free text. Recent meals and activities expire from camera context after one in-game hour or when you leave the location.

During a hangout, **Group selfie** and **Group photo** include the player and companions actually present. Select a person to use their **Expression wheel** and **Pose wheel**. **Group pose wheel** includes friendship poses and named romance poses for present dating/official partners without unresolved harm. Rotate with arrows or mouse wheel, or click a choice, then **Choose**. Availability is checked again when you press **Take photo**.

**Choose outfits** offers each person's saved wardrobe and gallery looks, or **Custom** clothing you describe. Custom outfit descriptions are saved for reuse. Existing gallery unlocks also apply to bedroom outfits. Outfit choices apply to the photo; character portraits are attached as likeness and clothing references.

The phone's **Gallery** contains this save's camera photos, grouped by in-game date, newest first, with capture times and locations. Open a photo for a larger view. Photos retain the scene and time from the shutter press, even if the world changes during generation. You can switch apps or close the phone while a photo develops; it loads into Gallery automatically. Closing the game cancels a pending request. Albums are stored under `assets/generated/camera-albums/`, with the album ID in the save; keep those assets when transferring saves. Camera generation retains ChatGPT-only authentication, with no paid API fallback.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Phone Camera and Gallery


---

# Local AI setup

history-local-ai-setup | Retrospective | AI & platform
Date: Unknown — reconstructed history

Preserved update documentation: Local AI setup.

## Details

The game now uses the installed Qwen 3.5 9B Abliterated model. Both AI stages request non-thinking output and allow up to five minutes per request; the first long-context request can be slow. Saves and portrait assets are unchanged.

For local mode, open **Locally Uncensored** and load `Qwen3.5-9B-abliterated.Q4_K_M.gguf` with LU Engine. This model is already installed on this computer; no Ollama download is required.

One-time connection setup:
1. In Locally Uncensored, open **Settings > Voice & Remote > Local API**.
2. Generate and copy a token, then start the API on port **8129**. Leave network access off for this computer only. Optionally enable **Start with LU**.
3. Restart the game, open **AI & account > Set LU API token**, and paste the token. The game saves it using Windows user encryption, separately from story saves.
4. Choose **Use local Qwen 3.5 9B Abliterated · LU Engine**.

The game uses the Local API at `http://127.0.0.1:8129` and checks that the requested 9B model is available before each generation. Both scene and player-choice passes use structured JSON output. The private engine port 8127 is not the external integration endpoint. For a custom local API port, set `LU_ENGINE_URL` before launching. `LU_API_TOKEN` can alternatively supply the token through the environment.

Keep Locally Uncensored and its Local API running during play. If generation fails, use Retry response; the unfinished turn does not change your save. The model's adherence to character canon and quality can vary.

[Locally Uncensored Local API documentation](https://locallyuncensored.com/guide/settings-and-troubleshooting/).

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Local AI setup


---

# Game features

history-game-features | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Game features.

## Details

- Interactive phone Maps app with switchable Map and Satellite views: a street map and a simulated aerial view of fictional Winterfield with terrain, trees, roofs and shadows. Both support location search, food/outdoor/home filters, clickable places with live presence and incoming travellers, drive/arrival actions, your location, drag and arrow-button panning, and cursor-centred wheel zoom. Undiscovered private locations stay hidden. View mode, map position and selected place are remembered while the phone is open.
- Phone Mini Games app with 13 games: Connect 4, Tetris, Blackjack, Snake, Pong, 2048, Memory Match, Minesweeper, Breakout, Match-3, Word Search, Simon Says, and draw-one Klondike Solitaire. Scroll the game list to see them all. Games have canvas animations and original sound effects; the SFX button mutes arcade audio, and phone sound/volume and reduced-motion settings are respected. Each game shows its mouse, touch-style button, or keyboard controls. Minesweeper has three difficulties and a safe first reveal; Match-3 offers 30 moves and cascading combos; Simon uses both lights and tones. Solitaire supports click-to-move and dragging. Connect 4 and Pong have computer opponents; Blackjack is a practice table with no wagers. Games resume while the phone stays open, and timed games pause when you leave them. Closing the phone clears arcade progress.
- Two playable men and five adult romance interests, with seven transparent portraits.
- Character canon loaded from `Mysterious Hearts - RPG Game.md`.
- Custom input on every successful turn; four optional replies generated only by clicking **Suggest replies**.
- Separate conversation history and cumulative AI memory for each relationship.
- Conversation headers show each participant’s current feeling across texts, group chats, and town encounters. Characters start Content. Their responses to friendly, sincere, funny, and flirtatious replies or gestures depend on their mood and relationship. When Rei flirts with Emily in a comfortable moment, she gets Flustered. Over text that might come through in a shy comeback. In person she might lose her place mid-sentence.
- Laughter can be a whole reply. Sophie might text “LMAO” at a joke that really lands or send an ecstatic message in capitals after a win. Emily leans toward a small “haha.” In person, a character can laugh aloud, interrupt their own sentence, or answer the joke with a gesture.
- Day and time progression after successful turns; a complete conversation journal.
- The active autosave is `saves/story.json`. Each playthrough also has its own autosave, named copies, and recovery history under `saves/stories/`. Open **Saved stories & backups** or **Tools → Saves & recovery** to manage them. Starting a new game preserves the previous playthrough.
- Responsive background AI requests; readable connection and validation errors.
- Named conversation transcript: your exact reply, separately labelled narration, and the love interest's answer. Pending replies remain visible. The response area names the player who will speak; scene controls are labelled separately. AI speaker/addressee fields are checked before a response is shown. Older saves remain compatible.

Locations such as Petal & Stem and the chess café are initial gameplay settings, not additions to confirmed character canon. The clock tracks game minutes, character schedules and persistent journeys. Free roam uses drive controls rather than a continuous movement map. Combat and authored endings are not implemented. Find Charles includes an authored document investigation and three follow-up enquiries in the Winterfield phone app.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Game features


---

# Runtime and development

history-runtime-and-development | Retrospective | AI & platform
Date: Unknown — reconstructed history

Preserved update documentation: Runtime and development.

## Details

Native Python/Tk desktop app, not a browser window. The launcher uses this computer's bundled Python runtime if available, otherwise `pythonw.exe` on PATH. On another Windows computer install Python 3.12+ with Tk support and run `python -m pip install -r requirements.txt`, then `python game.py`.

Run tests with `python -m unittest discover -s tests -v`. Tests use a local fake HTTP service; they do not require model generation. `python tests/live_smoke.py` makes one real model request and checks the response without modifying your save.

Portrait assets and the prompts used to generate them are in `assets/portraits/`.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Runtime and development


---

# AI direction

history-ai-direction | Retrospective | AI & platform
Date: Unknown — reconstructed history

Preserved update documentation: AI direction.

## Details

Character conversation references live in `Mysterious Hearts - Character References.md`. The game selects public, familiar, personal and confidence material using both trust and closeness. Existing shared history remains available to the people involved. The world reference supplies common recognition and occupation-specific knowledge when an organisation comes up.

Joseph, Sylvanis and Valentina have full tables. Relationship evidence distinguishes public family ties, firsthand history, delivered disclosures and observations. Companions present for Rei's encounter with Joseph can remember what they heard. Other residents need their own source.

The four disclosure bands use the lower of trust and closeness plus 18, with boundaries at 40, 58 and 78. These are tunable gameplay choices. Group disclosure considers every listener. Short, authored repair lines handle a few direct story questions when a generated reply misses the supplied facts. Restart the game after changing Python code or the cached character and world tables.

Player suggestions use the selected protagonist's voice guide and the current scene, in a separate **manual** request. Character responses do not generate choices or run a second suggestion pass. Click **Suggest replies**, **Suggest personal replies**, or **Suggest actions** to request only that set. Custom input stays available while suggestions generate. Suggestion requests never replay the character response, advance game time, change relationships, or rewrite your custom input. Cancelled or stale suggestions are discarded.

`ai_directions.txt` supplies shared narrative rules on every generation: continuity, player agency, knowledge limits, gradual romance, meaningful choices and factual relationship memory. `dialogue_styles.json` supplies individual voices. Both files are read for each new request, so edits to their contents apply on the next turn. Restart the game after Python code updates. These are model instructions rather than a deterministic romance simulation; factual and stylistic adherence can still vary. Speaker IDs and response structure are validated separately in code.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — AI direction


---

# Town, money and relationships

history-town-money-and-relationships | Retrospective | Relationships
Date: Unknown — reconstructed history

Preserved update documentation: Town, money and relationships.

## Details

Restart the game and choose **Continue saved story**, then **Town · Free roam** in the sidebar. Existing saves gain the new systems without losing conversations. Both Garrett and Rei are wealthy; each new or upgraded story starts with $100,000 in spending money. The other protagonist is available as a phone contact or at the town square.

Explore workplaces, public spaces and all seven character homes. Use **Meet** when a character shares your current location. Sidebar contacts retain their actual conversation mode. Travel is instant for you, your party and scheduled NPC movement. The world runs on an active-play clock: one full day takes two real hours by default. Use the toolbar **Time** menu for **Fast · 40-minute day**, **Faster · 15-minute day**, or **Paused**. Rest at home begins sleep without skipping time. Talk to a townsperson for an ongoing conversation using your selected AI provider. Choose a suggested reply or write your own. The conversation resumes when you meet them again.

Optional jobs at the campus café, flower shop, university track and chess café pay $180–$400, limited to one shift per day. Visit the gift boutique to buy six kinds of gifts; give them in person at each woman's usual location. Gifts matching her interests increase attraction more. Purchases, inventory, earnings and social events autosave.

Use **Personal talk ›** in the corner of the dialogue box to select personal talk, then click **Suggest personal replies** when you want four options. **Inquisitive** asks about their day, **Connection** explores something about them, **Open** shares something about your protagonist, and **Emotional** invites a heart-to-heart. Switch back with **‹ Main replies**. Both sets follow the current conversation.

In **Town · Free roam → Relationships**, **Ask on a date** and **Ask to be official** each send a private text and show the character’s answer. Each row lists that pairing’s minimum closeness, trust and attraction. Samantha is open to dates and takes longer to commit. April warms up sooner with Garrett. Emily always accepts a date with Rei and has lower exclusivity requirements with him. Completing a date unlocks the option to become official once the character’s other requirements are met.

Meet your date partner in a private hangout. The $150 date cost applies once, when the date starts. **Date goals** shows a generated conversation topic, a shared activity, and your first mutual kiss. A first kiss you’ve already shared starts checked. Use dialogue or actions to pursue the goals. Progress carries over when you leave or reload. Completing all three ends the date and awards 15 attraction and 10 closeness. You can also cancel a planned or ongoing date in Relationships.

Dating or becoming official with another person while an official relationship is active (including a strained relationship) records a betrayal. The participant learns immediately; physical acts can be witnessed by people present. Other contacts learn through an explicit disclosure in Phone → Winterfield. Trust loss and relationship tension apply when the person learns, once per event. The AI also reports actual mutual romantic acts in conversations; those reports trigger the same consequences, though interpretation of free-form dialogue depends on the model. Conversation context limits new private relationship and betrayal knowledge to participants, witnesses and recipients of disclosures. Existing knowledge in older saves is preserved. Breaking up before pursuing someone else avoids a new betrayal. Amends restore trust gradually, once per woman per day; gifts cannot erase betrayal. The Town & social journal shows events and bonds between the girls.

Verification: `python -m unittest discover -s tests -v` covers economy guards, save upgrades, male contacts and cheating consequences. `python tests/ui_smoke.py` checks desktop controls using mocked generation without modifying the player's save.

Character panels show trust, closeness and attraction out of 100. The first ordinary exchange of the day gives each participant 2 closeness and 1 trust. The existing 3-trust gain applies while befriending Tyler, Daniel and Valentina. Up to three meaningful moments per person each game day earn additional points. Learning something personal adds 2 trust and 2 closeness, accepted support adds 2 trust and 1 closeness, and a shared laugh adds 1 closeness. A personal discovery with mutual romantic chemistry can also add 1 attraction.

On eligible routes, a clearly welcomed flirt adds 2 attraction and a returned flirt adds 3. Either can also earn 1 closeness as a daily bonus when the exchange has no other bonding moment. The established male romance routes retain their 10-point gain for a returned flirt. Chemistry and flirting give at most one attraction award per exchange. Siblings and strictly platonic contacts build trust and closeness, and their attraction meter shows N/A. Setbacks and unresolved harm block conversation gains.

Gifts add 5 closeness, dates and becoming official each add 10, and amends add 3. Breakups reduce closeness by 15. Betrayal reduces closeness by 25 for the committed partner and 5 for the other women. Old affection scores migrate to attraction, and existing relationship progress carries forward.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Town, money and relationships


---

# Starting relationships

history-starting-relationships | Retrospective | Relationships
Date: Unknown — reconstructed history

Preserved update documentation: Starting relationships.

## Details

New stories use protagonist-specific starting relationships. Existing saved stats and relationship statuses are preserved. These numbers are gameplay tuning based on established familiarity. All romance routes start outside a dating relationship. Garrett and Rei start as best friends with 95 trust and 90 closeness and can develop attraction through mutual interest.

| Contact | Garrett attraction | Rei attraction |
| --- | --- | --- |
| Emily | 8 | 58 |
| Sophie | 22 | 32 |
| Amy | 24 | 28 |
| Samantha | 38 | 42 |
| April | 8 | 6 |

Emily's secret crush on Rei is established character canon. He does not automatically know about it. Attraction does not imply dating or consent. Existing saves retain earned stats; new stories use the revised starting attractions.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Starting relationships


---

# Living world, drives and unanswered texts

history-living-world-drives-and-unanswered-texts | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Living world, drives and unanswered texts.

## Details

Use **Choose hangout companions** in the in-person view to select one person for a private hangout or several for a group. Current companions are preselected; uncheck anyone you want to leave out. Only selected companions join your conversation and travel with you; nearby contacts never join automatically. You can also change the selection under **Town → Groups**.

Open **Town · Free roam** or **Maps** to travel instantly. Your party arrives with you. Vehicle selection, chauffeur details, passengers, arrival observations and journey history are retained. Saved journeys from older versions finish on load without charging time. Leaving separately or a scheduled departure ends the hangout and restores phone texts.

All eight characters have daily routines. The selected protagonist remains player-controlled; the other protagonist and five love interests move through their routines, including tracked commutes. Occupation locations are separate from homes. **Homes & routines** lists each designed home, the daily activities and current whereabouts. **Travel & texts** shows transit and message history. These are authored gameplay routines/designs, not assertions of additional historical biography.

By default, the clock advances one game minute every five real seconds (two real hours per full day), including while reading, typing or waiting for AI. The toolbar **Time** menu offers **Normal · 2-hour day** (1×), **Fast · 40-minute day** (3×), **Faster · 15-minute day** (8×), and **Paused**. Select any speed to resume. The selected mode is saved; paused time never accumulates for later catch-up. Pause freezes automatic world time, including sleep, while menus and conversations remain usable. Dialogue and actions add no fixed time cost. Each minute processes schedules, needs, appointments, message queues, Grove posts, photos and replies in order. Midnight rolls directly from 23:59 to 00:00; there is no Finish day control. Menus and closed-app time do not advance the simulation. Fractional minutes are preserved in saves. New games begin at 08:00 on New Year’s Day.

Contacts make dynamic follow-up decisions using personality variation, social energy, elapsed game time and unanswered-message limits. Follow-up wording is AI-generated using the current provider, not a fixed template. Sleep and driving prevent reading or replying; work and social activities limit phone checks. Opening a chat clears your unread badge without counting as a reply. Real-world idle time does not advance availability. Delivered messages persist independently of AI generation; failures can be retried per chat.

**Relationships** shows player bonds, stats, story summaries and milestones. **Bonds** covers all ten pairs of women with individual history, trust, closeness, tension and recent events. Shared scheduled locations can build familiarity once per pair per day after fifteen minutes together. Betrayals and dating overlaps add persistent tension and events; time together does not erase them. The AI receives a bounded recent snapshot of this state, while full journals remain saved locally.

Legacy saves gain the world clock, cast state and bond details on load without resetting stats or relationships. Existing in-person pairs are kept together when the location system is first added. Historical invented travel in old AI prose is not retroactively converted into trips; new movement uses the explicit travel controls.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Living world, drives and unanswered texts


---

# Careers, home actions and groups

history-careers-home-actions-and-groups | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Careers, home actions and groups.

## Details

**Careers** contains two protagonist-specific paid roles. Each is a 45-minute booking, available once per role per day, and must finish within its hours:

| Player | Daytime · 09:00–18:00 | Night · 20:00–24:00 |
| --- | --- | --- |
| Rei | Modelling at the downtown studio · $4,000 | Prize fighting at the Iron Circle · $8,000 |
| Garrett | Golden Dragon noodle shop · $1,500 | Red Dragons business at their private lounge · $5,000 |

The Iron Circle is a separate underground venue that opens at 20:00. The old arena remains available for daytime training. Crime-boss work is an abstract fictional activity, not an operational simulation.

Arriving at your own home opens **Home · Self actions**, also available from the sidebar. Rei can paint, journal, cook or read; Garrett can experiment with noodles, train, relax or review personal business. Four choices and a fifth custom action record personal activity in a saved home journal. Home actions take twenty minutes; custom prose cannot grant money or change locations.

Under **Groups**, select contacts currently at your location and form a party. The party travels with you. Arriving with one companion where another contact is present automatically creates a group chat in a separate window, with individually named responses, custom input, and four replies available through **Suggest replies**. Group histories remain separate from private chats and can be reopened from the Groups tab. People who join the group join the travel party; the drive button switches to a Mercedes-Benz Sprinter when the selected car has too few seats for the party. Scheduled departures update membership and close or replace the affected chat. Disbanding the party stops shared travel. Ending the day closes the outing.

Phone texts show messages and status updates without a narrator. In-person private and group chats retain narration.


Minsu Park is the third playable protagonist: Korean American, 177 cm, ESFP, a taekwondo national gold medalist and black belt studying medicine at Amy’s university. He lives one dorm away from Amy and starts as close friends with Amy and Sophie (through the sports club). His starting friendship values are gameplay tuning, with no assumed attraction or dating. His routine and home activities support medical study and training; he has no authored paid career yet. His portrait is a generated transparent illustration with light skin, clean-shaven features, middle-part hair and Korean streetwear. He is 19, born May 2, and enjoys science, video games, anime, taekwondo and reviewing food. Outside Amy and Sophie, everyone starts with zero closeness: he met Rei and Garrett through Sophie at a party, Emily at the café (and got her number), Samantha at the gym, and April at the library. Existing saves gain Minsu as a contact without resetting progress.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Careers, home actions and groups


---

# Illustrated interface and backgrounds

history-illustrated-interface-and-backgrounds | Retrospective | Interface
Date: Unknown — reconstructed history

Preserved update documentation: Illustrated interface and backgrounds.

## Details

Generated artwork is stored in `assets/ui/`, with the exact built-in image generation prompts alongside each PNG. The menu uses Winterfield at dusk and a navy-and-gold decorative title header. In-person conversations and the Town view show university artwork for campus/track, café artwork for the café, and town-square artwork for the square. Phone conversations and locations without their own illustration use the abstract UI artwork. Scene illustrations now use dawn, day, dusk and night lighting from the story clock. Rain and snow appear over supported exterior scenes; text conversations retain their neutral backdrop. Portraits render over the backgrounds with their relative height scaling preserved. Labels, buttons and dialogue remain live, readable controls. Missing artwork falls back to the existing dark theme.

The selection screen also uses `title-logo.png`, `selection-frame.png`, and `selection-nameplate.png` from `assets/ui/`. The title is generated lettering; character names, role labels and keyboard-focusable Begin buttons stay live. The original portrait assets and relative protagonist height scaling are preserved. Generation prompts are saved beside the images.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Illustrated interface and backgrounds


---

# Hidden residents

history-hidden-residents | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Hidden residents.

## Details

Six adult residents can be met at the archive, cycle workshop, planetarium, makerspace, community market and wetland boardwalk. They work from 09:00 to 17:00, then follow individual errands or quiet evenings at home. Weekends have later starts and individual outings. Rain moves outdoor leisure to varied indoor venues that suit each character. Use Town → Meet when nearby. Town → Discoveries shows profiles after meeting, lets you add their phone contact, and reveals a home address after 6 closeness (daily conversations grant 2). Discoveries persist in existing saves. Friends remain platonic; attraction represents initial potential, not consent. All six hidden residents have transparent anime/manhwa portraits in assets/portraits, with their built-in image_gen prompts saved beside each PNG.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Hidden residents


---

# Convenience tools and scheduled events

history-convenience-tools-and-scheduled-events | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Convenience tools and scheduled events.

## Details

Restart the game to use these changes; existing stories are supported.

- **Tools → Saves & recovery** saves named copies, renames slots, loads other playthroughs, and restores recent backups. Starting a new story preserves the previous playthrough and its independent recovery history. Continue still opens the active autosave.
- Continuing a story shows a factual recap with your last conversation, location, recent events, upcoming appointments, and date goals.
- AI responses show an elapsed timer. The completed character response is displayed and saved before optional reply suggestions are requested. **Cancel response** discards the unfinished turn and ignores late results. The provider may keep processing an already submitted request.
- Phone drafts are kept separately for each contact or group across navigation and restarts. Conversation scroll positions are remembered; new messages do not pull you away from older messages you are reading.
- **Tools → Search conversations** searches text and hangout histories by phrase, conversation, and recorded date. Select a result to see it highlighted in its original thread; bookmark messages and filter to bookmarks. Older messages without a recorded timestamp appear as Earlier.
- Town travel controls show travel duration, arrival time and expected contacts using a simulated copy of the current schedule. Use Go home and favourite destinations for shortcuts. The controls scroll when space is limited.
- Reply, activity, travel and career controls explain time or money costs. Career controls explain whether the booking is completed, outside its hours, or requires visiting the workplace.
- Relationship changes appear after exchanges and town actions. Toggle them in **Phone → Settings → Show relationship changes**.
- **Tools → Daily agenda** combines today's occasions, upcoming appointments, unfinished date goals and career availability. Calendar reminders run as the live clock reaches each appointment.

Open **Calendar → Plan an event** (also accessible from the phone calendar). Enter a title, game-world date, start time, discovered venue, duration, and one or more contacts. Conflicting appointments are rejected. Calendar markers and the agenda include saved events. **Cancel event** withdraws an appointment; **Join event** starts a hangout with the selected guests once you are at the venue during its scheduled time.

Reminders appear at **60 and 15 in-game minutes before** the start, plus an arrival notice. If a time-consuming action crosses a reminder, it is displayed when that action finishes. Only future reminder thresholds can fire: planning less than an hour ahead cannot generate an earlier one-hour reminder. Guests automatically attend at the chosen time and stay at the venue for the event duration, overriding their usual routines. You still travel to the venue yourself. Events, reminders already sent, and attendance survive saving and loading. These are game-clock appointments; real-world time while the game is closed does not advance them.

Verification: `python -m unittest discover -s tests -q` includes event timing, cancellation, guest selection, save recovery and persistence. `python tests/qol_ui_smoke.py` exercises the actual Tk planner, drafts, cancellation, search, agenda and saves using fresh in-memory state and mocked saves; it does not contact the AI or overwrite the player's story.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Convenience tools and scheduled events


---

# Source-backed character and event memory

history-source-backed-character-and-event-memory | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Source-backed character and event memory.

## Details

Existing saves are upgraded additively on load. Original transcripts, cumulative prose memories, relationship milestones, group and hangout histories, profile notes, shared events, and scheduled events remain in place. A versioned `memory_store` adds permanent source references, character-specific knowledge ownership, timestamps where available, certainty labels, and searchable topic indexes. Migration makes no AI requests. Existing prose summaries remain archived as historical evidence; they are no longer rewritten every turn or treated as stronger evidence than canon and current game state.

The ledger separates experiences, reported facts/preferences, beliefs, commitments, and legacy summaries. Quoted preferences remain self-reports; rumours remain unverified claims. Explicit promises/proposals are retained as unresolved statements unless there is separate evidence of their outcome. Existing agreed-meeting records and cancellations have an auditable history. A subsequent meeting does not prove an unspecified planned activity was completed. Exact preference-slot updates and explicit corrections can supersede an older record for the people who learned the update, without deleting the earlier evidence or informing other characters automatically.

Recall combines the current exchange and location with indexed topics, importance, open commitments, milestones, and recent dialogue. Only records owned by the character are eligible. Relationship overviews and invitation context use a disposable, source-linked extractive summary, rather than replacing historical prose. Canon and authoritative game state still take precedence over statements and summaries.

New calendar events record planned, attended, completed, cancelled, or player-missed states. Attendance is recorded from actual presence during the event; inviting someone is not itself a shared experience. If an old saved appointment has no attendance evidence, the system explicitly retains unknown attendance rather than inventing a visit. Guest attendance and the player's attendance are separate.

Verification: memory migration and manual-suggestion regressions are in `tests/test_memory_store.py`. `python tests/manual_suggestions_smoke.py` checks response-first delivery, personal-only generation, continued custom typing, cancellation, and in-person choice selection with mocked AI and saves. The existing player save files are not modified by these tests.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Source-backed character and event memory


---

# Winterfield immersion update

history-winterfield-immersion-update | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Winterfield immersion update.

## Details

Restart the game, continue your story, and open **Phone → Weather** or **Phone → Winterfield**. Town also has a **Life in Winterfield** shortcut. Existing saves gain these systems without resetting progress; the update does not invent earlier visits, help or discoveries.

**Weather** has an iPhone-inspired large temperature display, rounded forecast cards, a horizontally scrollable 24-hour forecast, ten daily temperature bars, and wind, humidity, sunrise/sunset, UV, visibility and feels-like readings. It follows the fictional 2050 calendar, with seasonal temperatures and deterministic forecasts. It is not an internet weather service. Celsius is used throughout. Town scenes and Maps display the same conditions. Sheltered boathouse activities and residents’ outdoor leisure respond to rain; bookings and player travel are never silently cancelled.

**Winterfield** gathers attributed local bulletins, festival preparations and aftermath, a rotating cinema programme, and practical details of life in 2050. Nine characters have authored projects that now progress through time spent at their project venue, independently of player participation. Already-reached stages are preserved during migration. Meet a character to help once for twenty minutes. Only completed help becomes a shared memory; completed projects remain available for conversation.

Repeatable café, pizza, cinema, flower-shop and boathouse activities take ten minutes and are limited to once per place per story day. Paid orders show their cost. Regulars remember recorded orders, lobby sketches persist, and three visits on separate days with the same companion establish a shared ritual. The Follow through section surfaces recorded promises and proposals and links back to the relevant conversation; it does not claim a proposal was accepted or a promise fulfilled.

Garrett can continue **Find Charles** after reading the receiving copy. Three enquiries at the archive, Interpol desk and Golden Dragon each take twenty minutes, with at least one story day between enquiries. The episode resolves the crate-count discrepancy and the meaning of the receiving stamp, then identifies a missing authorisation page as the next lead. It does not reveal Charles’s location, allegiance or fate.

New betrayals are private records until witnessed or disclosed. Use **Winterfield → Tell someone what happened** to send an explicit disclosure. Consequences apply once to each informed person; relationship tension requires both people to know. Legacy knowledge remains intact. AI interpretation of free-form romantic actions still depends on the model.

Verification: `tests/test_living_world.py` covers forecast consistency, additive migration, projects, actual shared visits, mystery gates, knowledge boundaries, routines and news. `tests/living_world_smoke.py` exercises Weather at both supported phone sizes, day/night views, Winterfield, Maps and Home with mocked AI and saves.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Winterfield immersion update


---

# Autonomous life and asynchronous messages

history-autonomous-life-and-asynchronous-messages | Retrospective | Simulation
Date: Unknown — reconstructed history

Preserved update documentation: Autonomous life and asynchronous messages.

## Details

Restart the game. **Tools → Life & availability** (also linked from Messages, Town and Home) shows player Energy, Social battery and Happiness, usual sleep schedules, pending invitations and shared life events. Existing stories gain these records without resetting relationships or histories.

- Time passes automatically while playing. At home, **Nap** sets one hour of sleep and **Sleep** sets eight hours; both recover needs over the running game clock. While asleep, choose **Normal · 1×**, **Fast · 4×**, **Faster · 12×**, or **Skip to waking** in Life & availability (also accessible from Home activities and the sleeping presence view). Skipping processes every world tick. Sleep acceleration multiplies the selected Time speed and stops while time is paused. The sleep multiplier returns to 1× upon waking, preserving your selected Time speed; **Wake up** ends sleep early.
- Needs update every five game minutes. Characters reconsider optional plans every 15–30 minutes, retain chosen intentions, seek rest, work on personal projects, arrange company and make invitations. Familiar contacts may travel to your door; welcoming them remains your decision. Invitations can be accepted, declined or deferred in Life & availability. No relationship penalty applies just for declining.
- Sleep schedules allow a bounded late-night extension for comfortable company. Characters wind down, leave through tracked journeys, or request a separate sleeping place at your home. Accepted overnight stays preserve their location through sleep and end with morning departure. Staying overnight never establishes intimacy.
- Sustained public encounters create directional NPC acquaintances, including pairs outside the original five-woman bond table. Established acquaintances can deliberately meet again. Their own memories include those encounters; other people do not learn them automatically. Small work/study events, remembered activities and project progress supply conversation context.
- Send several texts, switch to another contact or group, and keep playing while replies generate. Outgoing bubbles show **Delivered** and then **Read** (or partial group readership). Each recipient reads and answers according to availability. Sending another text while a reply is being generated queues it for the next exchange; it does not rewrite the response already underway.
- NPC replies contain one to three generated bubbles. Follow-ups can add a thought or start another topic. Prompts explicitly reject stock apologies, repetitive reminders and assumptions about why the player has not replied. No automatic reply is sent while a character sleeps or drives. The worker processes one messaging request at a time without locking the interface.
- **Pause reply** preserves delivered messages; **Continue / retry** resumes the chat after a generation failure or pause. Pending messages survive saving and reloading. Character generation uses the selected AI provider and therefore its normal usage allowance. Simulating needs, travel and decisions requires no AI requests.

Validation: `tests/test_autonomy.py` covers sleep, needs, receipts, independent queues, stale-response protection, acquaintances, overnight stays and migration. `tests/autonomy_ui_smoke.py` exercises the native phone and needs window using mocked AI and saves. No player save is modified by these checks.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Autonomous life and asynchronous messages


---

# Autonomy integration audit and reply timing — November 6, 2026

history-autonomy-integration-audit-and-reply-timing-november-6-2026 | Retrospective | Simulation
Date: 2026-11-06

Preserved update documentation: Autonomy integration audit and reply timing — November 6, 2026.

## Details

The audit found real integration defects, not just slow tuning. Read messages were re-gated by narrow clock windows after long waits; every new bubble could postpone a whole chat; unsolicited messages could precede unanswered player messages; and a completed response from an unavailable character could hold the shared worker. These paths now use independent message deadlines, relationship-based attention, player-message priority and per-chat prepared responses. Existing pending messages migrate without deletion or resending. Sleep, driving and an ongoing face-to-face conversation still prevent that character from texting.

Dialogue, texts, dating invitations and physical actions never add a fixed time cost. The response headings show **Time passes naturally**. The active-play clock continues while the AI writes; the phone shows availability and an elapsed writing indicator.

Closeness, trust and attraction affect notice/reply delays, follow-up timing and initiation likelihood. Emily has an authored preference for replying to Rei promptly, unless their relationship is strained or has unresolved harm. In ordinary free time she can start replying to Rei immediately; an unfamiliar Minsu usually waits about five minutes for reading and two more for composing. Work, social activity and low energy can add a short delay. A second unanswered text shortens the remaining notice/composition delay; it never restarts the wait or wakes a sleeping driver/recipient. These are eligibility times, not promises about provider latency.

| Discussed feature | Integration checked |
| --- | --- |
| Fixed simulation, persistent intentions, needs-driven priorities | Five-minute needs updates; saved plans and 15–30-minute decisions in `autonomy.py`; minute-based journeys and event boundaries remain in `world_loop.py`. |
| Spontaneous visits, NPC invitations and leaving naturally | Invitations, welcome/decline/defer controls, real journeys and visit deadlines. Starting an in-person hangout now preserves the accepted visit's deadline. |
| Flexible bedtime, overnight stays and morning departure | Individual schedules, limited bedtime grace, separate sleeping arrangements and tracked departures. Starting an overnight stay before bedtime no longer loses its plan on the next tick. |
| Player waits, naps, eight-hour sleep and meters | Tools, Home, Town and phone links; midnight crossing, distinct rest recovery and time-skip warnings. |
| Activity-dependent messaging and delivery/read receipts | Sleep/driving restrictions, short busy delays, per-recipient group readership and visible availability. Legacy town phone contacts also work through the queue. |
| Double texts, bursts, simultaneous chats and dynamic follow-ups | Immediate outgoing saves; one-to-three generated bubbles; independent queues; relationship-based follow-ups; later texts remain separate from a response already being composed. |
| Projects that progress independently and remember help | Actual work time and completion events; helping now preserves accumulated progress instead of replacing the project record. |
| New acquaintances, directional bonds and NPC social lives | Sustained public encounters, deliberate peer outings and player-approved friend introductions. Small outing disagreements and their repair are tracked separately from serious unresolved harm. |
| Different kinds of company, rewarding interaction and rituals | Familiar quiet company can restore social battery; meaningful exchanges change wellbeing/closeness; remembered activities and actual shared rituals influence later invitations and dialogue. |
| Circumstantial changes and fallback plans | Outdoor peer/project plans can move under shelter through actual travel. A player-agreed outdoor outing requires a new accepted proposal to change venue. |
| Emotion causes, private events and gradual recovery | Message-specific causes, owned work/study events, slower wellbeing and limited mood recovery; relationship harm is not erased by ordinary time together. |
| Promises and follow-through | Explicit proposals and promises, owner-specific recall and reminders. Explicit agreement, cancellation or reported completion in a reply can supersede a commitment for the people who heard it; the supplied quotation is checked against the actual player message. |

Scope remains bounded: projects use authored stages, social disagreements concern small everyday plans, and reported completion of a promise is distinguished from independently verified physical completion. Full spatial autonomy and individual meters belong to the scheduled cast; older incidental town contacts have default phone availability rather than newly invented homes and complete lives. Sending is an immediate local delivery, so there is no fabricated network-transit delay. Those distinctions are intentional and should not be described as a fully unconstrained simulation.

Regression coverage is in `tests/test_message_timing.py` alongside the existing autonomy, world, dates, memory and group tests. `tests/message_timing_ui_smoke.py` holds a mocked response in progress while sending extra texts, switching chats and checking that the clock stays unchanged. The live player's save was inspected read-only to reproduce the backlog; no test rewrites it.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Autonomy integration audit and reply timing — November 6, 2026


---

# Varied character outings

history-varied-character-outings | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: Varied character outings.

## Details

Free-day routines rotate through late-morning, afternoon and evening destinations. Weekday work and sleep schedules remain intact, while meal breaks and leisure stops vary by character and day. Public hangout invitations and peer plans use character interests, shared interests, recent visited locations and current crowds; the café is one option among many. Peer partners share the same destination and activity. Rain chooses suitable indoor alternatives instead of sending everyone to the café. Agreed player outings keep their location unless the player accepts a proposed change. Recent destinations persist in saves.

`tests/test_leisure.py` checks destination diversity, public access, weather alternatives, repeat avoidance, shared peer plans, actual free-day movement and schedule priorities.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Varied character outings


---

# More places around Winterfield

history-more-places-around-winterfield | Retrospective | World & story
Date: Unknown — reconstructed history

Preserved update documentation: More places around Winterfield.

## Details

The map and travel picker now include Winterfield Lanes (bowling), Pixel Pier (arcade), Afterglow (nightclub), the Copper Lantern (bar), Winterfield Commons (public park), Silver Sands (beach), the Public Library and Winterfield Galleria (shopping mall). Riverside Park remains available. Each destination supports calendar invitations, shared travel, encounters and a daily activity through the living-world panel. Paid activities deduct their displayed cost; visits record memories and shared rituals and supply camera activity context.

Characters choose these places according to their interests, recent visits, crowds and weather. Rain and snow redirect autonomous outdoor outings indoors. Bar outings begin at 17:00 and nightclub outings at 20:00; sociable characters can take evening outings on free days before returning home. These are activity hours; players can visit the locations at any time. Travel keeps the game's existing instant-arrival behavior. Existing saves need no reset. Each new venue has a distinct illustrated background; park and beach scenes also receive outdoor weather effects.

Downtown is a visitable metropolitan district with a free boulevard walk, generated scene artwork, calendar meetups and interest-led autonomous outings. It uses outdoor weather rules. Both map layers now continue into dense city blocks beyond the playable destinations, with no empty texture edge when zoomed out.

Map geography now uses continuous curved streets, uneven block spacing, T-junctions, diagonal arterial roads, rounded park boundaries and road-aligned building footprints. Downtown has denser, larger buildings; neighbourhood streets continue beyond the playable area in both map layers.

Unanswered text follow-ups use the contact friendship thresholds: acquaintances wait four times the previous delay, friends (trust 50+, closeness 25+) wait twice as long, and close friends (trust 70+, closeness 55+) or above retain the previous pace. Existing availability, requested pauses and increasing delays for repeated unanswered follow-ups still apply.

Characters can also send newly generated private photos through the existing Codex ChatGPT image connection. Eligible direct replies have a 4% chance for acquaintances, 12% for friends and 25% for close friends or above, with minimum gaps of three story days, one day and twelve hours respectively. Photos develop in the background and appear inline when the sender is available. Silence follow-ups, setbacks and requests to pause do not trigger photos. Pending jobs survive saves; failed jobs can be retried with **Chat options → Retry incoming photos**. These images are generated specifically for the message, not taken from Camera or Grove galleries.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — More places around Winterfield


---

# Relationship development

history-relationship-development | Retrospective | Relationships
Date: Unknown — reconstructed history

Preserved update documentation: Relationship development.

## Details

Conversations can record concrete player promises, individually expressed boundaries, loyalty conflicts, and character-initiated dates, introductions or relationship talks. These appear in Character profiles → Your notebook and persist in saves. Only delivered words or submitted actions count; suggestions and hypothetical plans do not.

An explicitly agreed promise deadline uses story time. Missing it marks the promise overdue; following through later does not erase the original hurt. Respecting boundaries and keeping promises build trust. Crossing boundaries and breaking promises damage it. Repeating the same recorded outcome cannot repeatedly earn trust.

Rei protects Yuriko and Emily, Garrett protects April, and Ivan protects Valentina with additional disapproval. Their approval changes with conduct they actually witness; private actions are not automatically shared. Characters can voice competing loyalties, and the person being protected can challenge intrusive behaviour.

Repairing unresolved harm now requires acknowledging the specific hurt, corrective conduct on a later story day, and freely offered forgiveness. The Make amends button cannot bypass that process. Established betrayal memories remain. Characters with sufficient trust and closeness may initiate a milestone conversation; accepting a proposed date still uses the normal date eligibility and goals. Declined invitations have a three-story-day cooldown.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Relationship development


---

# Story saves and portable backups

history-story-saves-and-portable-backups | Retrospective | Saves
Date: Unknown — reconstructed history

Preserved update documentation: Story saves and portable backups.

## Details

Each playthrough has a stable story ID and an independent autosave. `saves/story.json` remains the Continue entry; switching stories does not mix their recovery histories. Existing saves gain their story ID when saved.

Recovery retains up to 12 checkpoints spaced at least five real minutes apart and 14 daily checkpoints (local calendar days). These capture the previous saved state before a later write. Named copies remain until their story is deleted. Legacy rotating backups remain available. Writes use unique temporary files, flush data before replacement, and serialize through a process/thread lock.

The save library displays protagonist, story date/time, location, save type, and local save timestamp. Malformed files are shown as damaged instead of disappearing. If Continue fails, the game offers the newest loadable recovery entry; if the damaged file cannot identify its story, the candidate may be another playthrough and is named in the prompt.

**Delete selected story** removes all saves and checkpoints with that story ID; **Clear all saves** removes every saved story. Both require confirmation. Deleting the active story returns to the menu and clears its in-memory state. Generated pictures, account credentials, and device preferences are retained. Legacy files without story IDs are deleted individually.

**Export with photos** creates a ZIP containing the selected saved state, referenced generated media, and its camera album manifest. **Import** validates the save and archive paths and creates a separate playthrough. Missing source images cannot be included; conflicting existing media causes import to stop without overwriting it. Bundles have a 1 GiB uncompressed size limit. Exported stories include conversation history and personal notes, so share them deliberately.

Validation: `tests/test_save_system.py` covers independent histories, checkpoint spacing, deletion, atomic-write failure, photo/album transfer, damaged-save visibility and archive traversal. `tests/save_library_smoke.py` exercises named saves and clearing an active story in Tk using isolated temporary storage.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Story saves and portable backups


---

# Start screen

history-start-screen | Retrospective | Interface
Date: Unknown — reconstructed history

Preserved update documentation: Start screen.

## Details

The main menu uses a split layout: story navigation and account/sound controls on the left, a large Winterfield character preview on the right. Select Garrett, Rei, Minsu or Ivan to preview their portrait and introduction, then choose **Begin as …** to start. Selection alone does not create a save. Continue is disabled until an active save exists; named stories and recovery remain accessible through **Story library & backups**. The layout supports the default 1220×940 window and the 1000×800 minimum. `tests/start_ui_smoke.py` checks all four selections, the start action, and both layouts without writing player saves or contacting AI.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/README-at-archive.md — Start screen


---

# From design to the first playable game

history-foundations | Retrospective | World & story
Date: Unknown — reconstructed history

The first desktop build offered Garrett or Rei, five love interests, portraits, local AI conversations, four generated choices, custom replies, autosave and separate relationship histories. Initial development reports also record character design and portrait creation. Combat and scripted quests were not part of that first playable build.

## Details

The first desktop build offered Garrett or Rei, five love interests, portraits, local AI conversations, four generated choices, custom replies, autosave and separate relationship histories. Initial development reports also record character design and portrait creation. Combat and scripted quests were not part of that first playable build.

Early follow-ups added individual voices, labelled player/narrator/character dialogue, speaker checks, gradual-romance and knowledge instructions, protagonist-specific replies and automatic incoming opening texts. The local provider moved from Librellama Gemma E2B to Gemma 12B, then later Qwen; automatic suggestions were later replaced by manual requests. See the dated development reports for those intermediate states.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- patch_notes/development_records.json
- game_core.py
- ai_directions.txt


---

# Canonical attraction and legacy romance reconciliation

history-sexuality | Retrospective | Relationships
Date: Unknown — reconstructed history

Canonical orientations now gate both sides of romantic compatibility across Meet-Cute discovery, likes, matching, date acceptance, flirt choices and anonymous feelings. Friendship is still available. Persistence and affection scores do not override orientation, and attraction is not consent.

## Details

Canonical orientations now gate both sides of romantic compatibility across Meet-Cute discovery, likes, matching, date acceptance, flirt choices and anonymous feelings. Friendship is still available. Persistence and affection scores do not override orientation, and attraction is not consent.

Older incompatible romance states become friendships while retaining trust, closeness and history. Incompatible dating-app matches close without deleting messages; pending romantic replies and future dates are cancelled. Incompatible active date sessions are retained as historical records.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- sexuality.py
- tests/test_sexuality.py


---

# Editable app pages and dock

history-home-layout | Retrospective | Phone & social
Date: Unknown — reconstructed history

The phone home screen supports choosing an app and placing it into an explicit empty position on another page, swapping apps into the dock, and dragging dock apps back to the page. Empty positions are preserved. Editing does not launch apps. Layouts survive save round-trips, rebuilding the home screen and resizing.

## Details

The phone home screen supports choosing an app and placing it into an explicit empty position on another page, swapping apps into the dock, and dragging dock apps back to the page. Empty positions are preserved. Editing does not launch apps. Layouts survive save round-trips, rebuilding the home screen and resizing.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- phone_home.py
- phone_personalization.py
- tests/phone_home_smoke.py


---

# Neo Ishida joins the hidden cast

history-neo | Retrospective | World & story
Date: Unknown — reconstructed history

Neo has a discoverable profile, portrait, Grove identity, daily schedule and home. His established connections to Tyler and Daniel inform shared memories. Neo is in a committed relationship with Alyssa and remains a platonic contact rather than a dating-app candidate. Meeting him does not automatically introduce Alyssa. His home requires the normal discovery threshold. Existing saves add his records without overwriting existing bond progress.

## Details

Neo has a discoverable profile, portrait, Grove identity, daily schedule and home. His established connections to Tyler and Daniel inform shared memories. Neo is in a committed relationship with Alyssa and remains a platonic contact rather than a dating-app candidate. Meeting him does not automatically introduce Alyssa. His home requires the normal discovery threshold. Existing saves add his records without overwriting existing bond progress.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- hidden_cast.py
- tests/test_neo.py


---

# Alyssa and the shared household

history-alyssa | Retrospective | World & story
Date: Unknown — reconstructed history

Alyssa joins the discoverable cast with personal references, a Grove identity and bookbinding interests. She and Neo share one home and a committed partnership. Discovering one partner does not silently introduce the other. Both remain unavailable as player romance routes. Save migration preserves prior discoveries and relationship progress.

## Details

Alyssa joins the discoverable cast with personal references, a Grove identity and bookbinding interests. She and Neo share one home and a committed partnership. Discovering one partner does not silently introduce the other. Both remain unavailable as player romance routes. Save migration preserves prior discoveries and relationship progress.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- hidden_cast.py
- tests/test_alyssa.py


---

# Neo and Alyssa photo archives

history-couple-gallery | Retrospective | Art & media
Date: Unknown — reconstructed history

Added eight distinct square Grove photos each for Neo and Alyssa, with authored captions and comments. The gallery upgrade preserves existing likes, replies and live posts and does not duplicate the imported archive on repeated loads. Image generation prompts are retained with the assets.

## Details

Added eight distinct square Grove photos each for Neo and Alyssa, with authored captions and comments. The gallery upgrade preserves existing likes, replies and live posts and does not duplicate the imported archive on repeated loads. Image generation prompts are retained with the assets.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- tests/test_neo_alyssa_galleries.py
- assets/grove/neo/generation-prompts.json
- assets/grove/alyssa/generation-prompts.json


---

# Grove, Supafast and Doober Eats

history-grove | Retrospective | Phone & social
Date: Unknown — reconstructed history

Added social posts and replies through Grove, daily shopping through Supafast, and food menus and deliveries through Doober Eats. Character follower counts and known profiles shape the social presentation. Later updates added publishing Gallery photos with captions, generated character comments and follower-based engagement.

## Details

Added social posts and replies through Grove, daily shopping through Supafast, and food menus and deliveries through Doober Eats. Character follower counts and known profiles shape the social presentation. Later updates added publishing Gallery photos with captions, generated character comments and follower-based engagement.

Conversation context includes actual posts and relevant orders; merely discussing a purchase does not place an order or spend money. Private deliveries are not automatically shared with unrelated characters.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- phone_apps.py
- grove_photos.py
- grove_reactions.py
- tests/test_phone_apps.py
- tests/test_grove_photos.py
- tests/test_encounter_context.py


---

# Character galleries and group photo expansion

history-grove-art | Retrospective | Art & media
Date: Unknown — reconstructed history

Grove gained authored photo archives, dates, captions, likes and comments for its character profiles. Subsequent artwork expanded individual and group scenes, including Rei, Garrett and Yuriko with their established friends. Gallery tooling also covers Valentina, Sylvanis, Tyler, Elliot and Daniel.

## Details

Grove gained authored photo archives, dates, captions, likes and comments for its character profiles. Subsequent artwork expanded individual and group scenes, including Rei, Garrett and Yuriko with their established friends. Gallery tooling also covers Valentina, Sylvanis, Tyler, Elliot and Daniel.

Photo archives and live posts coexist. These are authored in-world records; importing artwork is not evidence that a player performed the depicted activity. Available original reports remain in the optional development archive; some image-heavy chats exceeded the retrieval limit.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- grove_gallery.py
- tests/test_grove_gallery.py
- tools/add_daniel_gallery.py
- tools/add_elliot_gallery.py
- tools/add_sylvanis_gallery.py
- tools/add_tyler_gallery.py
- tools/add_valentina_gallery.py


---

# Arcade expansion, sound and animation

history-arcade | Retrospective | Phone & social
Date: Unknown — reconstructed history

The initial phone arcade included Connect 4, Tetris, Blackjack, Snake, Pong and 2048. It expanded with Minesweeper, Breakout, Memory Pairs, Match-3, Simon and draw-one Klondike Solitaire.

## Details

The initial phone arcade included Connect 4, Tetris, Blackjack, Snake, Pong and 2048. It expanded with Minesweeper, Breakout, Memory Pairs, Match-3, Simon and draw-one Klondike Solitaire.

Games gained canvas animation, including sliding tiles, and sound effects. Reduced-motion and phone audio preferences are respected. Minesweeper has difficulty choices and a safe opening; Match-3 uses cascading combos; Solitaire supports click and drag moves. Timed games pause away from the screen. Progress lasts while the phone stays open; Blackjack is practice without wagers.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- mini_games.py
- arcade_games.py
- tests/test_mini_games_animation.py
- tests/test_arcade_games.py


---

# Message and Grove notification popups

history-notifications | Retrospective | Phone & social
Date: Unknown — reconstructed history

Notifications cover incoming messages and Grove interactions, including comments and replies. The UI provides navigation to the relevant activity and respects privacy settings. Notification regression checks cover routing and avoiding duplicate delivery. Earlier audio work added separate sent/received text sounds and controls, without treating in-person speech as a text notification.

## Details

Notifications cover incoming messages and Grove interactions, including comments and replies. The UI provides navigation to the relevant activity and respects privacy settings. Notification regression checks cover routing and avoiding duplicate delivery. Earlier audio work added separate sent/received text sounds and controls, without treating in-person speech as a text notification.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- notifications_ui.py
- tests/test_notifications.py
- sound.py
- tests/test_sound.py


---

# Dark phone surfaces and embedded prompts

history-dark-phone | Retrospective | Interface
Date: Unknown — reconstructed history

Phone prompts and confirmations use embedded dialog wrappers so navigation stays in the phone. Dark slate styling covers entries, combobox popups, scrollbars, selected and disabled states, and arcade screens. Theme checks guard against native light controls. Navigation checks cover leaving and reopening active conversations, drafts and in-phone routes.

## Details

Phone prompts and confirmations use embedded dialog wrappers so navigation stays in the phone. Dark slate styling covers entries, combobox popups, scrollbars, selected and disabled states, and arcade screens. Theme checks guard against native light controls. Navigation checks cover leaving and reopening active conversations, drafts and in-phone routes.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- phone_dialogs.py
- phone_theme.py
- tests/phone_dark_theme_smoke.py
- tests/phone_dialogs_smoke.py
- tests/phone_navigation_smoke.py


---

# Witnessed romance and protective reactions

history-protection | Retrospective | Relationships
Date: Unknown — reconstructed history

Protective reactions respond to actual witnessed romantic conduct involving established close ties. Rei, Garrett and Ivan have distinct motivations; the reaction is not automatically romantic jealousy. Private romance and ordinary friendly events do not trigger an uninformed protector. Repeated observations are deduplicated, and the player does not react to himself as a separate NPC.

## Details

Protective reactions respond to actual witnessed romantic conduct involving established close ties. Rei, Garrett and Ivan have distinct motivations; the reaction is not automatically romantic jealousy. Private romance and ordinary friendly events do not trigger an uninformed protector. Repeated observations are deduplicated, and the player does not react to himself as a separate NPC.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- protectiveness.py
- tests/test_protectiveness.py


---

# Persistent hangouts and accurate encounter context

history-hangouts | Retrospective | Phone & social
Date: Unknown — reconstructed history

In-person hangouts retain their own history and distinguish spontaneous visits, arranged meetings and summoned visitors. Groups keep participant-specific knowledge. Later controls allow selecting whom to hang out with instead of assuming everyone nearby is part of the conversation.

## Details

In-person hangouts retain their own history and distinguish spontaneous visits, arranged meetings and summoned visitors. Groups keep participant-specific knowledge. Later controls allow selecting whom to hang out with instead of assuming everyone nearby is part of the conversation.

You cannot text someone in your active hangout, including through a group chat. Texting resumes after the hangout ends. Phone navigation allows reopening a conversation while its reply is in progress.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- encounter_context.py
- tests/test_hangout_journal.py
- tests/test_hangout_texting.py
- tests/test_encounter_context.py


---

# Portrait consistency and alternate outfits

history-portraits | Retrospective | Art & media
Date: Unknown — reconstructed history

Character artwork gained consistent portrait presentation and saved generation prompts. Alternate outfit assets expanded the visual wardrobe, including additional Garrett, Rei, Emily and April looks. Portrait and clothing references feed Camera and later generated Wardrobe designs. Original image-heavy chat reports were not all recoverable; the archive does not invent their individual completion dates.

## Details

Character artwork gained consistent portrait presentation and saved generation prompts. Alternate outfit assets expanded the visual wardrobe, including additional Garrett, Rei, Emily and April looks. Portrait and clothing references feed Camera and later generated Wardrobe designs. Original image-heavy chat reports were not all recoverable; the archive does not invent their individual completion dates.

Earlier portrait work added casual, evening and bedroom gallery variants. Bedroom photos unlock only when the relationship with the specific character is official; otherwise the gallery displays a locked message. Casual and evening portraits remain available.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- assets/portraits
- camera.py
- lifestyle_apps.py
- gallery_ui.py


---

# Expanded protagonists, family and hidden cast

history-cast | Retrospective | World & story
Date: Unknown — reconstructed history

The original Garrett/Rei choice expanded to Minsu and Ivan. Minsu has authored university friendships, a dorm, medical study and taekwondo interests. Yuriko is Rei’s platonic sibling contact. Hidden residents gained gated profiles, home discovery, contacts and persistent schedules. Later additions include Valentina, Sylvanis, Neo and Alyssa.

## Details

The original Garrett/Rei choice expanded to Minsu and Ivan. Minsu has authored university friendships, a dorm, medical study and taekwondo interests. Yuriko is Rei’s platonic sibling contact. Hidden residents gained gated profiles, home discovery, contacts and persistent schedules. Later additions include Valentina, Sylvanis, Neo and Alyssa.

Private lore is revealed through familiarity and evidence rather than a public directory. Sylvanis has special headquarters access rules; Ivan starts with an existing connection. Daniel and Tyler are 21 in the current cast records.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- game_core.py
- hidden_cast.py
- tests/test_minsu.py
- tests/test_hidden_cast.py
- Mysterious Hearts - Character References.md


---

# Emotions, dialogue tone and social reactions

history-emotions | Retrospective | Relationships
Date: Unknown — reconstructed history

Conversation headers show participant emotions. Friendly, sincere, funny and flirtatious exchanges interact with mood and relationships. Character voice guidance supports distinctive laughter, stutters, exuberance and quiet reactions; physical action suggestions follow the conversation’s tone. Family and platonic boundaries remain enforced.

## Details

Conversation headers show participant emotions. Friendly, sincere, funny and flirtatious exchanges interact with mood and relationships. Character voice guidance supports distinctive laughter, stutters, exuberance and quiet reactions; physical action suggestions follow the conversation’s tone. Family and platonic boundaries remain enforced.

## Save compatibility

See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.

## Evidence and historical limits

Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.

- emotions.py
- dialogue_styles.json
- tests/test_reactions.py
- tests/test_conversation_growth.py
