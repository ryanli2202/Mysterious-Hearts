# Combat update — Part 2: lore, HUD, systems and all other changes

Roadmap: [MH-001](ROADMAP.md#mh-001-combat-window-redesign-and-animated-attacks). Companion: [Part 1 — animations and effects](COMBAT_ANIMATIONS_UPDATE_PLAN.md).

**Status:** Part 2 complete — non-animation runtime implementation and relevant verification completed 2026-11-10. See [completion evidence](roadmap/COMBAT_PART_TWO_COMPLETION.md). Part 1 animations and combined visual integration remain separate; MH-001 overall stays In progress. Earlier pending statements below are preserved historical planning context and are superseded by this completion record.

### Completion evidence — 2026-11-10

Closed the remaining partner-state, specialist access, escort positioning, recognition/disclosure, depleted-boss and generated-combination checks. [Full completion record](roadmap/COMBAT_PART_TWO_COMPLETION.md) includes actual commands/results, limitations and save compatibility. 92 combat + 23 enhanced combat + 18 Interpol tests pass; 41,040 finite stress combinations pass. Live custom dialogue and compact partner/boss UI reviewed. The Crow campaign still forces defeat after four exchanges. Release: `release-2026-11-10-combat-part-two-completion`.

### Systems implementation evidence — 2026-11-10

See [implementation, formulas, access, save impact and limits](roadmap/COMBAT_BALANCE_REVIEW.md), [104 identity sheets](roadmap/COMBAT_IDENTITY_SHEETS.json), [fresh-seed acceptance results](roadmap/combat-holdout-results.json), [exploratory results](roadmap/combat-balance-results.json) and [actual dialogue samples](roadmap/combat-dialogue-samples.json).

Implemented state mechanics, hierarchical combat expressions, current-champion bouts, contender previews, enhanced Richter, alternative objectives, generated initiating dialogue, knowledge-sensitive identity dossiers and the location-art HUD. Passed 78 combat, 23 enhanced-combat and 18 Interpol tests; all ten holdout matchup groups and both Protocol active-window criteria passed. Compact Part 2, opponent, dialogue and enhanced-combat UI smoke checks and 34-page dark-phone checks passed. The authored Crow containment encounter still forces defeat after four exchanges, per the user's explicit campaign exception. No Part 1 animations changed.

The review lists remaining full-plan acceptance work; these runtime changes do not imply completion of group scenario coverage, depleted boss comparisons, every generated combination or animation integration. Release record: `release-2026-11-10-combat-part-two-systems`.

### Initial implementation evidence — 2026-11-10

- `combat_profiles.py` now names Neo/Thirteen Shinigami Protocol, Daniel War God and April Polymath. Initial refinement defaults are 94/90/90/85 respectively; these are authored calibration values, not source facts or measured matchup results. April retains power 35, martial skill 38 and fight IQ 99. No physical-tier promotion is implied.
- Version 1 identity migration updates formerly traitless canonical profiles, including the opponent snapshot in an active encounter. Keeps earned refinement above the new baseline, all other stats, Path history, learned/signature IDs and current resources. Adds the existing bounded precision amplification (8 mana) where the legacy movebook had none; it does not generate new signatures. Existing custom Traits remain unchanged. Dialogue uses reconciled copies without mutating story state or exposing other speakers’ private abilities.
- `combat_balance.py` assigns D 450–301, C 300–101, B 100–11 and low A 10–2. The generator and validator share interpolated stats. Adjacent ranks differ by at most one per numeric stat, and contender stats stay below Rei’s current defaults. Generated prose cannot override the assigned stats. This is numeric calibration only: moves, AI, band capability transitions and full outcome distributions still require balance review. Existing active arena opponent stats and ladder records are preserved; newly validated candidates use this scale. Championship routing/title rules remain legacy behaviour and are NOT completed by this slice.
- The in-person HUD now puts the player portrait left and opponent right, with adjacent labelled health/stamina/mana bars and current Path/form state. Narration remains above bottom action controls. This is the first layout slice, not the finished location-art arena or complete responsive/status design. No animation files or playback changed.
- Verified: 63 combat tests (including four new migration/calibration checks), 23 enhanced-combat tests, five Vendetta lore tests and five Thirteen tests. Combat, combat-portrait and enhanced-combat UI smoke checks passed; inspected the 1000×800 rendered HUD after a resolved exchange. Phone dark-theme smoke passed across 34 pages; patch-notes UI smoke passed. Further release checks are recorded in the patch-note entry.
- Release checks: start-screen smoke passed (28 previews); patch-note validation/export passed. Patch-note unit suite: five passed, one failed on a pre-existing missing historical screenshot (`tests/screenshots/crow-contact.png`); history left unchanged. 
- Next: explicit current-champion bouts and contender identities, full character hierarchy/guard/Richter outcome calibration, complete reputation recognition, Shinigami readiness/adaptation/state persistence, War God momentum, revised perception/element mechanics, dialogue requests and final arena artwork/accessibility. Earlier “pending” sections below describe the remaining full acceptance scope; this evidence records only the implemented slice.


**Scope:** All non-animation work: lore/reputation/identity sheets, ability definitions and mechanics, hierarchy/balance, AI and dialogue, training/progression, Iron Circle and boss rules, HUD/layout/controls, static artwork integration, descriptions/previews, accessibility of those controls, persistence and compatibility.

**Boundary:** Part 1 owns animated effects, GIFs, signature animation designs, visual recipes and playback/accessibility behaviour. This part supplies authoritative resolved events, active states and stable action IDs and builds the arena/HUD surface they use. Descriptions of state visuals below are integration dependencies on Part 1, not a second animation implementation backlog.

**Supporting references:** [Abilities](roadmap/COMBAT_ABILITY_DEFINITIONS.md), [character combat lore](roadmap/COMBAT_CHARACTER_LORE.md). Existing links to this file's lore/system sections remain valid.

## Plugin task assignments

**Assigned:** 2026-11-11. Part 2 is complete. These assignments apply only to requested maintenance or interfaces touched by Part 1; they do not reopen completed work.

Follow the [shared plugin workflow and evidence rules](roadmap/PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Lore, ability descriptions and generated combat dialogue maintenance | Story Skills + Writer's Loop | Preserve concealed identities, power limits, forced outcomes and private disclosure audiences; review changed text against authoritative state. |
| HUD or status-symbol asset changes | prompt-to-asset, when a new local vector asset is needed | Validate/export dark-compatible icons or nine-slice framing; reuse combat_style and inspect compact, large-text, disabled and drawer states. |
| Mechanics, balance, partner/boss state and save-boundary changes | falsegreen-skill | Review substantive regression assertions against Part 2 contracts, including depleted bosses, partner state and generated combinations; rerun affected combat suites. Historical test counts are not new results. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Lore-based balancing and character power

Confirmed scope addition, 2026-11-10: characters must have significantly different combat strength that reflects their lore. This is part of MH-001, alongside presentation and animation. Balancing and lore reconciliation are planned; no runtime balance changes have been implemented by this addition.

### Confirmed hierarchy

Revised and approved on 2026-11-10, superseding the earlier broad tiers and April's previous placement. Compare serious fights between healthy characters in comparable, explicitly stated ability/form states, without exceptional preparation. Characters in a shared row are not internally ranked. Overall strength does not require every individual statistic to follow the same ordering.

| Tier | Characters / combatants | Gap to the tier below and intended relationship |
| --- | --- | --- |
| S+ — Strongest overall | Sylvanis | Small–moderate above S. The most complete combatant through prediction, analysis, martial versatility, shadows and second-stage Transcendence; not necessarily the greatest raw physical strength. |
| S — Apex threats | Takeo Mishima, The Crow | Moderate above A+. Almost unbeatable for ordinary lower-tier challengers. Physical reinforcement/adaptive weapons versus analysis/mastery; no fixed Takeo/Crow ordering. |
| A+ — Exceptional masters | Ivan Yeun, Charles Han | Small above A. Elemental versatility and limited Conduit State versus refined martial pressure and Transcendence. |
| A — High elite | Four Aces (Martos Cabrera, Elias Braun, Mavis Kuro, Camila Lopez), Garrett Han, Neo, Daniel, Edward Fox, Jeremy Gordon, Rei, Thirteen | Large overall gap above B, with specialist exceptions and meaningful within-tier differences. |
| Low A — Title contenders and enhanced Richter | Iron Circle number-one contenders; Joseph Richter in his fully active cybernetic boss form | The lower portion of A, below Rei at comparable full-strength states. Richter is moderately below Rei. No fixed ordering between Richter and contenders; contender gaps and the high-B boundary require tuning. |
| B — Dangerous named Awakened / high-ranked arena combatants | Tyler Harding, Samantha Kim, Keisuke Hachimura, Emily Fields, Alyssa, Minsu Park, Valentina Yeun; high-ranked Iron Circle combatants | Moderate above a typical individual C-tier elite guard or mid-ranked arena fighter. Range, training, resources and matchups matter. |
| C — Elite combat personnel / mid-ranked arena combatants | Established elite guards and appropriate specialist archetypes; mid-ranked Iron Circle combatants | Large above ordinary D-tier opponents. Assess coordinated squads separately from individual fighters. |
| D — Lower-level combatants | Unawakened lower-level guards; lower-ranked Iron Circle combatants | Baseline tier. Equipment, positioning and numbers matter. Being unawakened does not automatically put every veteran in D. |
| Specialist — Separate assessment | April | No single duel-tier gap. High tactical contribution through cognition, observation and preparation; substantially weaker direct fighting and vulnerable when isolated. Not automatically above elite guards in a duel. |

Exact numerical thresholds remain to be designed and verified. Minsu and Valentina remain in B. Audit other unassigned roster members against lore; do not infer placements from an earlier “etc.” or organisational rank alone.

### Confirmed gap definitions

These are design requirements, not measured win rates or damage multipliers.

| Gap | Practical meaning |
| --- | --- |
| Small / mild | The stronger fighter is favoured, but a good matchup or better execution can reverse the result. |
| Moderate | A clear advantage; the weaker fighter needs a meaningful tactical edge, preparation or an exploitable circumstance. |
| Large | Normal good play alone rarely closes the difference; teamwork, a major situational advantage or another objective becomes important. |
| Overwhelming | A normal solo victory is implausible; survival, rescue, escape or delay should usually be the achievable objective. |

Gaps are not additive damage multipliers. Apex versus B should generally feel overwhelming, while specialists and temporary forms require explicit matchup assessment. The A-to-B large gap describes the broad groups, not an automatic cliff between a high-B fighter and a low-A contender.

### Confirmed Iron Circle integration

Lower ranks map to D, mid ranks to C, high ranks to B, and number-one contenders to low A, below Rei. Arena combat remains in the in-person window. The rank boundaries and all arena refinements below were confirmed on 2026-11-10. Implementation, numerical combat tuning and verification remain pending.

Current implementation evidence: `combat.py` starts the ledger at rank 450 and uses three generation bands (ranks above 300, above 100, and the remaining top ranks). It has no distinct low-A contender generation band in that function. Opponent generation and validation must both enforce the new mapping, including Traits, effective move strength and tactical competence rather than just generated descriptions. Preserve saved ladder progress and assess stored opponents/active encounters during migration.

Confirmed rank boundaries and required arena refinements:

- Use ranks 450–301 for D, 300–101 for C, 100–11 for B and 10–2 for low-A contenders, with Rei as the starting #1 benchmark. These cutoffs are confirmed planned scope; the existing generator still needs four-band integration. Rank #1 is the championship position, initially held by Rei, rather than another generated contender band.
- Smooth progression within bands so rank 101 versus 100 or 11 versus 10 is a believable step, not a sudden stat wall. Contenders should remain below Rei but provide credible title-fight pressure.
- Keep competitive rank distinct from actual power: an established strong protagonist entering at rank 450 retains their strength. Rank progression does not automatically grant awakening, a Trait or an unexplained power increase.
- Make the title bout an explicit encounter with the actual current champion rather than treating a generated opponent or ordinary rank increment as defeating Rei. Preserve legitimately earned titles in existing saves; Rei is the starting champion benchmark, not permanently guaranteed to win.
- Give contenders distinct, bounded fighting styles and previewable strengths; ring performance and street/group threat should be assessed separately when rules, equipment or objectives differ.

### Joseph Richter boss placement — confirmed

Confirmed on 2026-11-10: **low A for Richter's fully active cybernetically enhanced boss form**, **moderately below Rei** at comparable health and readiness. The user approved this placement and all boss-fight refinements below as required MH-001 scope. Runtime implementation and verification remain pending. Richter's ordinary civilian presentation has no established combat tier and must not inherit the boss rating.

| Comparison | Confirmed relationship |
| --- | --- |
| Richter's active boss form versus Rei | Rei has a moderate overall advantage through refined technique, redirection and sustained momentum; Richter can punish mistakes and interrupt momentum, without a guaranteed scripted result. |
| Versus Iron Circle number-one contenders | Same broad low-A band; no fixed ordering. Weapon-equipped boss combat is not an identical ruleset to an arena bout. |
| Versus B-tier fighters | A meaningful advantage in the equipped encounter, varying by matchup; exact small/moderate gaps require testing, not an automatic large gap over every high-B specialist. |
| Versus individual Blackstone guards | Clearly stronger than ordinary PMC, Seeker and Headhunter opponents; determine exact gaps after assigning those archetypes. Do not infer superiority over an entire coordinated force. |
| Versus A+ and S/S+ | Below the exceptional masters and far below apex threats. Cybernetic enhancement does not imply Takeo's Nanoengine or comparable capabilities. |

**Existing evidence:** `rei_story.confront` builds his boss profile from the Headhunter cyborg archetype, assigns the cybernetic portrait and overrides power/skill/fight IQ to 79/84/88. `RICHTER_DIALOGUE` and `campaign_dialogue.RICHTER_FIGHT` establish reinforced arms, a powered spinal frame, targeting lights and weapons. These numbers establish current implementation only, not a verified tier. The fight is solo, at Blackstone executive command after stage 6 and all five Blackstone areas are cleared. Victory disables the programme and records the existing story resolution.

**Confirmed boss-fight design:** Make the challenge come from his established powered frame, weapons and targeting against Rei's movement/redirection. Implement readable committed attacks, targeting and weapon pressure, momentum interruptions and punishable recovery that give skilled play clear openings. Preserve established capabilities without inventing a new Trait, elite lifelong martial mastery, reinforcements, environmental traps or hidden second transformation. Those additions would require separate design approval. No unenhanced rating is inferred from being wealthy or a boss.

**Encounter and save requirements:** Preserve the solo, in-person confrontation, investigation prerequisites, campaign-scoped guard clearance and victory-based resolution. Survival/escape objectives for apex fights do not substitute for this mission's required victory. Distinguish Richter's full-health matchup from difficulty caused by preceding guard attrition; do not silently weaken Rei or raise Richter's lore tier to compensate. Do not replay resolved campaigns, restore disabled Blackstone sites or expose the hidden boss portrait in ordinary contact views.

**Validation pending:** Compare the enhanced profile against Rei, representative low-A contenders, B-tier specialists and Blackstone guard archetypes using explicit equipment and starting-state assumptions. Check both fresh and depleted campaign entry, meaningful counterplay, defeat/retry, victory persistence and legacy active encounters. Review in-person boss presentation and ensure narration follows actual frame/weapon effects. No balance simulation, boss replay or UI verification was performed for this placement assessment.

### Confirmed Trait lore revisions and Shinigami trump-card state

Approved on 2026-11-10. These explicit lore changes supersede earlier descriptions that leave Neo, Thirteen, Daniel or April without a named Trait. They are required update scope; runtime profiles, lore modules and move catalogues have not yet been changed by this planning entry.

| Character | Confirmed Awakened Trait | Confirmed ability/state direction |
| --- | --- | --- |
| Neo | Shinigami Protocol | Has a trump-card state functioning in “ultra instinct”: reactive responses, adaptation to opponents and selection of the best possible choices in combat. |
| Thirteen | Shinigami Protocol | Has the same named Trait and an ultra-instinct trump-card state with reactive responses, opponent adaptation and best-possible combat choices. Shared Trait/state does not establish identical overall strength or settle his matchup with Neo. |
| Daniel | War God | His Awakened Trait is War God, like his father's. His coordinated physical pressure, instinctive transitions, contact reading and three-level momentum mechanics are now confirmed below; his father's wider biography/repertoire is not established. |
| April | Polymath | Her enhanced cognition, pattern recognition and tactical processing are now identified as Polymath. She remains a separate tactical specialist; sharing a Trait name with another character does not automatically grant their physical ability, experience or full combat effectiveness. |

**Shinigami state implementation requirements:** Treat the trump-card state as a real mechanical state for both Neo and Thirteen, separate from baseline Trait identity. Express its reactive response, adaptation and best-choice behaviour in resolution and tactical decision-making, not just dialogue or animation. Interpret best possible choices relative to the character's available information, physically feasible responses and usable abilities/resources; excellent decisions do not guarantee success against overwhelming force. Preserve the existing distinction between perception and physical response and the prohibition on hidden guaranteed victories. Do not silently dilute the approved reactive/adaptive capability into a cosmetic accuracy buff.

**Confirmed Shinigami state specification (2026-11-10):** Both Neo and Thirteen deliberately activate after sufficient combat readiness, normally 3–5 meaningful exchanges against a credible opponent. Offence, defence, counters and observation build readiness; damage is optional and idle/harmless repetition cannot farm it. Duration is four full exchanges, visibly counted, without multiple decrements for multi-hit attacks. Activation costs approximately 20% maximum stamina, requires sufficient stamina, and does not waive ordinary action costs. Afterward apply two exchanges of reduced stamina recovery, no immediate reactivation and no automatic collapse/stun. Initially allow one activation per encounter, resetting only after genuine recovery; preserve expenditure across saves/resumption and prevent flee/restart resets. Apply the same requirements to NPCs.

**Confirmed power and expression:** Baseline A, temporary A+ combat effectiveness through reactive defence, adaptation, efficient movement, precision and best feasible decisions. This permits contesting Ivan/Charles during the window without guaranteed victory and does not erase S/S+ advantages. Neo emphasises efficient interceptions, precise counters and tactical switching; Thirteen emphasises suppression/closing escape routes with greater expenditure while sustaining pressure. Neither version is inherently defective. Players retain intention/technique selection while the state optimises execution. Formal state naming, exact readiness/rounding/recovery formulas and adaptation persistence still require implementation decisions; approved duration, cost target and power level are no longer merely proposals.

**Confirmed War God mechanics:** Daniel integrates physical power, balance and learned skills through instinctive transitions, whole-body coordination, close-contact reading and reversals. Use three bounded momentum levels—Engaged, Flowing, Dominant—earned by successful varied exchanges, improving stance recovery/transitions, pressure and access to a costly finisher/reversal that consumes momentum. Losing engagement or decisive disruption causes decay; ineffective repeated attacks do not build it, and one mistake need not disable the Trait. Reinforced combinations/finishers consume stamina. Daniel remains A overall, without an additional A+ transformation. No automatic takedowns, unlimited strength, mind-reading or automatic access to his father's full repertoire. Exact thresholds and action costs require tuning.

**Lore and system reconciliation:** Audit `combat_profiles.py`, `vendetta_lore.py`, `thirteen.py`, character references, protagonist previews, identity sheets, dialogue context, progression/form handling, move generation/validation and signature classifications. Replace conflicting “no named Trait” or traitless descriptions for these four characters. Preserve unrelated backstory and privacy boundaries; Shinigami Protocol does not by itself establish hidden implants, a neural HUD, Nanoengine or new programme history. Daniel sharing War God with his father does not author a new paternal biography or establish how inheritance works.

**Skills and presentation:** Preserve stable IDs and learned moves while mapping Neo/Thirteen signatures to Shinigami Protocol, Daniel's signatures to War God and April's signatures to Polymath. Reconcile the original traitless-signature category and catalogue counts rather than duplicating or deleting its existing animations. Define and review recognisable state activation/active/exit cues for both Shinigami users, with Reduced Motion and Fast Combat support. Any new state effects or signatures require their own coverage entries; the original 227 designs are not automatically complete coverage of this new scope.

**Save impact and acceptance:** Plan a versioned additive migration for existing profiles, Trait/refinement fields and active encounters; preserve earned progression, learned skills and history. Reconcile old zero/absent Trait defaults without treating them as evidence the newly confirmed Traits have no refinement. Verify canonical/new-story previews, NPC and player profiles, generated dialogue and saved records agree on names and capabilities. Test baseline versus trump-card response/adaptation/choice quality for both Neo and Thirteen against varied opponents, with feasible-response and information limits. Verify April stays mechanically distinct from The Crow/Sylvanis and Daniel is recognised as War God without unsupported extra powers. Detailed formulas, migration implementation, visual review and gameplay verification remain pending; the state specification and War God mechanics above are confirmed.

### Confirmed mana perception and elemental lore revisions

Confirmed on 2026-11-10; these replace older narrower descriptions in the ability reference and must be reconciled across runtime lore, profiles, move catalogues, AI dialogue, identity sheets and previews during implementation.

- **True Sight:** Perception of the world through pure mana and magical flow enables near-perfect efficiency in Awakened application. Precognition is a side effect, alongside heightened combat perception/reflexes, significantly enhanced speed/strength application using Awakened energy and lower mana drainage. It is not merely immediate body-language perception. Garrett and Sylvanis retain it, and **Charles also possesses True Sight alongside White Flame Tiger**. Near-perfect efficiency is not infinite energy; exact amplification, detection horizon and resource stacking need tuning without discarding the confirmed effects.
- **Analysis:** Allows perception of minuscule changes and microscopic details and visualisation of branching paths. Camila's observation and branching evaluation must be reflected in both mechanics and descriptions. Branches are possibilities; this is distinct from True Sight's actual mana-flow precognition and Polymath's synthesis.
- **Conduit elemental amplification:** Channel use physically amplifies stats: red lightning enhances attack power; blue lightning dramatically enhances speed; wind deals soul damage; fire generates strength; ice enhances reflexes/reaction time. Keep red attack power versus fire strength and blue movement speed versus ice reactions mechanically distinct.
- **Tranquility (Ivan, ice):** Instant reaction speeds and perception and a constant flow state. Preserve instant response as specified, while distinguishing it from physical movement travel time. Access, duration, costs and interactions require design; do not silently reduce it to a minor stat bonus.
- **Misanthropy (wind):** Ivan can suffer more damage and remain standing. Valentina also has access. Implement meaningful continued-function endurance with explicit damage/threshold rules, not invented regeneration or cancellation of injury.
- **Deathwind origin and inheritance:** Ivan provided Valentina's Deathwind as an extension of his wind power. The user explicitly confirmed that **Deathwind inherits wind's soul damage from the same source**, as well as Misanthropy. Preserve her wind techniques and B-tier baseline. Do not invent transfer circumstances or automatically grant other elemental channels, Tranquility or Full Conduit State.

**Integration and unresolved detail:** Define soul damage, eligible targets, defences, damage accounting and interaction with armour/health before implementation; do not relabel ordinary damage without a distinct effect or assume universal defence bypass. Use consistent shared source rules for Ivan and Valentina. Specify Misanthropy's access, accumulated-damage/functional thresholds and exit behaviour and Tranquility's availability/flow persistence. Full Conduit State retains five minutes once per 24 hours; this timer is not automatically the duration of every elemental bonus. Review combined True Sight/element/form amplification and mana efficiency for duplication and unintended tier changes.

**Acceptance evidence required:** Test every elemental channel's distinct effect, Tranquility's reaction/perception versus travel time, Misanthropy on both users, soul damage from both wind sources, Charles's combined Traits and Analysis's fine-detail/branch behaviour. Include state switching, mixed channels, resource stacking, player/NPC symmetry, active-state saves and lore/privacy consistency. Preserve stable move IDs, existing progression and the approved baseline hierarchy; separately verify temporary peaks. No runtime implementation or gameplay verification is claimed by this planning revision.

### Expanded Trait and ability definitions

Confirmed scope addition, 2026-11-10: provide substantially deeper definitions and descriptions for Traits, abilities, forms and individual moves. The authored [expanded combat ability reference](roadmap/COMBAT_ABILITY_DEFINITIONS.md) covers the current Trait roster, revised Shinigami Protocol/War God/Polymath identities, shared-power differences, forms, Richter's enhancement and non-Trait capabilities. Entries explain function, applications, limitations and sources; the move-level contract requires prerequisites, costs, range, outcomes and interactions during integration.

Use the reference in identity sheets, appropriate ability detail panels, move previews and generation context with discovery/privacy boundaries preserved. Descriptions must match verified mechanics, preserve stable skill IDs and work with legacy saves. Shinigami activation/duration/cost/A+ peak and War God momentum are now confirmed scope; implementation and remaining formula-level tuning are pending. These definitions do not complete all identity sheets or each individual move's mechanical specification.

Authoring evidence: the expanded reference was created and reviewed against current profiles/catalogue and approved lore revisions. Runtime integration, per-action reconciliation, gameplay checks and rendered review remain pending.

### Required implementation and lore reconciliation

- Audit `combat_profiles.py`, combat resolution, move effects, AI tactics, progression/forms and `organisation_guards.py` against the character references and character-specific lore modules. Existing peak-source ratings are a starting point, not evidence that the hierarchy already works.
- Make power differences observable through damage, durability, speed, precision, resource efficiency, technique, tactical decisions and appropriate ability interactions. Preserve character identity and established limits: Sylvanis's combined abilities, Takeo's overwhelming physical reinforcement, and The Crow's analysis need different mechanical expressions.
- Reconcile conflicting ratings, encounter descriptions and combat dialogue with the confirmed hierarchy. Keep private power knowledge and unrevealed identities behind their existing discovery boundaries; social rank alone does not determine combat strength.
- Preserve the distinction between overall effectiveness and specialised attributes. Sylvanis being strongest overall does not require him to exceed Takeo's raw physical power in every statistic. April is a separate specialist: implement tactical contribution and vulnerable direct combat without inventing brute force, new powers or guaranteed elite-guard victories.
- Align new-story profiles, NPC opponents, training encounters and saved profiles so character choice does not arbitrarily reverse the lore hierarchy. Coordinate Emily's already-approved awakened starting state with MH-002; her tier does not grant additional powers.
- Define baseline, restrained/sparring and active-form comparisons explicitly. Preserve resource costs, activation conditions, injuries and established limits, including Ivan's five-minute Conduit State once per 24 hours. Almost unbeatable does not mean unconditional invulnerability or unlimited resources.
- Assess additive/versioned balance migration for stored profiles. Preserve earned progression, learned moves, resources, story history and custom-character choices; document how existing encounters and legacy numeric ratings will be handled before implementation. Do not blindly replace a saved profile with a fresh default.

### Confirmed balancing refinements

Approved on 2026-11-10: all refinements below are required MH-001 scope, together with distinct character strengths and specialist treatment described above. Implementation and verification remain pending:

1. **Alternative objectives against the apex tier.** Support clearly communicated survival, escape, rescue or delay objectives where a normal duel would be implausible. A successful retreat should be meaningful without requiring the apex opponent to become weak.
2. **Bounded counterplay and specialist roles.** Allow preparation, terrain, teamwork and ability matchups to matter without a routine lower-tier counter or repeated stun loop erasing a major lore gap. Give April room to excel at tactical support and prediction rather than inflating her physical strength.
3. **Explicit restraint in sparring.** Label an opponent's restrained state and distinguish training success from defeating their full-strength self. Strong characters can teach approachable lessons without contradicting later encounters.
4. **Lore-preserving difficulty options.** Adjust assistance, telegraphs and encounter circumstances rather than automatically scaling every opponent to the player's level. Keep the hierarchy recognisable across difficulty settings.
5. **Separate starting strength from earned progression.** Establish what exceptional training, forms and custom-character progression can eventually achieve, with authored milestones for crossing tiers instead of accidental stat inflation. Progression rules must not remove MH-002's freely selectable advanced backgrounds.

6. **Distinct roles within the Four Aces.** Keep their shared broad tier without forcing equal open-duel performance: Martos specialises in suppression/direct combat, Mavis in infiltration and assassination, Elias in movement-driven pressure, and Camila in analysis. No unsupported exact internal ranking.
7. **Minsu and Valentina's B-tier specialities.** Minsu excels in short exchanges, interception and disengagement through speed and trained taekwondo; Valentina is especially dangerous with range and space for cutting wind. A favourable specialised matchup does not automatically promote either into A.
8. **Assess temporary peaks separately.** Explicitly compare Ivan's five-minute, once-per-day Conduit State, Garrett's Transcendence and Rei's accumulated momentum against equivalent documented states. Do not compare ordinary performance to another character's maximum without labelling the difference.
9. **No invented apex weaknesses.** Do not create unsupported Nanoengine fuel limits or convenient cooldowns to make Takeo beatable. Fox can contribute tracking/evasion/evacuation and Gordon relevant firepower without erasing Takeo's physical advantage. Use alternative objectives and established limits.
10. **Evidence-based comparisons.** Preserve Thirteen's clear advantage over Keisuke. Neo's childhood Number One designation does not settle the present-day Neo/Thirteen matchup. Do not use faction status, childhood labels or planned source-story victories as proof of every current duel result.

### Confirmed combat identity and behavioural balance

Approved on 2026-11-10: all following refinements are required MH-001 scope. These extend the confirmed hierarchy without creating new tiers or rewriting established powers.

- **Power, control and experience:** Model output separately from refinement, efficiency, commitment and combat experience. Comparable overall strength must still permit different resource use, execution and opening creation; do not invent inexperience simply to weaken someone.
- **Perception versus response:** Recognising an attack does not guarantee the speed, position or time needed to evade or counter it. April may identify danger she cannot physically escape; The Crow still needs a feasible response despite understanding an attack.
- **Information-dependent analysis:** Camila and The Crow adapt to observed patterns; unfamiliar techniques initially provide less evidence. Preserve their baseline competence, established prediction abilities and knowledge boundaries. Analysis does not reveal unseen information or grant automatic counters.
- **Burst versus sustained strength:** Assess short peaks and extended encounters separately. Preserve Ivan's Conduit duration/frequency and Minsu's bounded speed bursts; neither implies unlimited sustained output.
- **Distinct defensive mechanisms:** Separate durability, armour, evasion, pain tolerance and recovery. Emily's pain immunity does not prevent injury; Tyler's impact storage does not cancel damage. Avoid treating these as interchangeable damage immunity.
- **Group threat assessment:** Evaluate coordination, space, equipment and ability synergy. Several C-tier fighters are not automatically equivalent to one A-tier fighter; allies may help or obstruct one another. Record individual and group assumptions separately.
- **Character-specific AI priorities:** Express identity in decisions as well as statistics. Analytical fighters punish observed repetition, suppression specialists restrict movement, and competent fighters adapt when an action is ineffective. Respect available information, resources and committed-action rules; do not grant AI hidden knowledge of the player's next choice.
- **Willingness versus capability:** Restraint, protection objectives and collateral concerns affect choices without silently changing intrinsic strength. An unfavourable outcome while protecting someone does not itself demote a character's baseline tier.
- **No forced combat outcomes:** Make the hierarchy emerge from abilities, tactics and circumstances. Do not grant hidden guaranteed-win rules to stronger fighters or unexplained protagonist bonuses to satisfy an expected story result. Existing victory-gated missions, including Richter's confrontation, require an actual resolved victory rather than scripting one.

### Character identity, reputation and combat presence

Confirmed scope addition, 2026-11-10: integrate who each character is into combat, beyond tiers and powers. The [character combat lore reference](roadmap/COMBAT_CHARACTER_LORE.md) provides apex definitions and roster-specific directions. Sylvanis is the Crazed Demon, reputed to be the most feared being on the planet; The Crow is an enigma whose personal identity is unknown; Takeo is the Human Siege Engine, capable of destroying army platoons alone. Preserve these as actual lore, not generic boast lines.

Extend every identity sheet with established titles, reputation, audience recognition, public/private roles, motivations, fighting manner and relationship-sensitive voice. Apply them to introductions, spar/challenge/lesson dialogue, tactics, ability reactions and aftermath while preserving disclosure and resolved-outcome boundaries. The Crow's alias/role does not reveal his identity; Sylvanis's reputation does not force the player's fear; Takeo's capability does not invent completed battles. All titles, scoped reputations and presence directions in the character lore reference are now confirmed (2026-11-10), including Ivan's Fivefold Calamity, Neo's Missing Shinigami and Thirteen's Remaining Shinigami. Use the complete approved roster; additional unsupplied fame or history remains unestablished.

The Syndicate is confirmed as the world's largest and most feared organisation. Ivan and the Four Aces have formidable international reputations in relevant circles. **The Four Aces are considered the best in the world at their respective Syndicate duties:** Clubs in high-risk combat/suppression/bodyguard work; Hearts in influence/psychological operations/spectacle/social destabilisation; Spades in assassination/infiltration/evasion/silent removal; Diamonds in financial warfare/institutional sabotage/strategic calculation. **The Ace of Spades is the world's most feared assassin.** This does not override their confirmed A-tier placement or make every specialty an automatic duel victory.

Implement the approved two-layer recognition model: an operational title may be notorious while its civilian identity remains concealed. Use titles selectively in introductions, informed reactions and dossiers, with behaviour carrying their reputation during exchanges. Missing/Remaining Shinigami expresses shared experimental origins and different histories, not perfect/failed versions. Preserve developing or local recognition for characters without global notoriety.

Verify informed/uninformed and mixed audiences, concealed identities, generated dialogue variety, previews/portraits, save-owned recognition and legacy defaults. No hidden fear debuff, forced surrender, automatic win or bonus tier arises from reputation. Reference authored; runtime integration, generated-sample review and gameplay/UI verification remain pending.

### Combat identity sheets for every character

Create a concise, consistently structured combat identity sheet for every character, indexed by stable character ID. Include named NPCs and noncombatants: record unranked/unknown or no established combat capabilities when appropriate instead of inventing a tier. Distinguish civilian and enhanced forms, especially Richter. Provide corresponding archetype records for guards and generated arena opponents, and a compatible identity record for custom combat profiles. These are design/validation records; private facts must not automatically become public dossier text.

Each sheet must record:

- Baseline tier or specialist/unranked status, relevant peak states, activation conditions and comparison assumptions.
- Exceptional strengths, ordinary limitations, and explicit things the abilities cannot do.
- Preferred range, tactics, character-specific AI priorities, resource demands, burst/sustained performance and distinct defensive mechanisms.
- Favourable and unfavourable matchups, with conditions and uncertainty; separate individual, group, arena and objective-based assessments.
- Restraint and collateral considerations separately from intrinsic capability.
- Established titles/reputation, public/private roles, audience recognition, motivations, fighting manner and relationship-sensitive voice, following the character combat lore reference.
- Exact lore/source references, approved design decisions and unresolved interpretations. Game balance numbers are not independent lore evidence.
- Linked implementation/profile/move IDs and actual verification evidence, with pending work clearly labelled.

Maintain roster coverage and update the sheets when lore, abilities, forms or balance decisions change. Alyssa must not acquire Sylvanis's broader repertoire; Samantha's accessible-blood control must not become unrestricted internal blood control. Reconcile existing contradictions using approved scope, including Emily's awakened state, rather than copying stale descriptions into the sheets.

### Balance reviews for new moves and progression bonuses

Every new or materially changed move, generated custom skill, form modifier or progression bonus requires a recorded balance review before inclusion in the implemented update. Reuse the combat identity sheets and matchup benchmarks; review the resulting build and combinations, not just the isolated effect.

Record affected character/action IDs, intended benefit, costs and limitations, lore compatibility, expected tier/matchup impact, and actual checks/results. Cover repeated restraint/counters, stacked prediction, resource-recovery loops, critical-hit combinations, defensive stacking and burst amplification. Check player/opponent symmetry and short/long encounters. Ensure a lower-tier build cannot routinely erase an apex gap through unintended interactions, while preserving legitimate specialist advantages and approved earned tier progression.

New canonical powers or hierarchy changes must be explicit design decisions, not incidental consequences of a bonus. Generated skills must pass bounded mechanical validation before acceptance; prose alone is not balance evidence. For changed existing bonuses, record save impact and preserve earned progression through an explicit migration assessment rather than silently deleting it. Keep review evidence with the implementation and eventual release record; do not claim unrun tests or simulations.

### Balance acceptance and evidence

**Confirmed custom-start integration (2026-11-10):** MH-002's [starting-background catalogue](roadmap/CUSTOM_STARTING_BACKGROUNDS.md#confirmed-placement-in-the-mh-001-combat-hierarchy) now has approved starting targets from lower D through upper B plus **Exceptional Veteran — low A**, freely selectable without prior unlocks. Calibrate these packages on this plan's shared scale, including civilian, independent and Syndicate/Shinokami backgrounds. Exceptional Veteran grants combat experience, not organisational promotion, arena rank/title, canonical abilities or automatic Transcendence. Low-A customs remain below Rei in comparable states; assess contender/Richter matchups individually. Preserve the approved starting targets while verifying coherent stats, Traits, learned moves, role specialities and later progression. Numerical implementation and matchup evidence remain pending.

- Verify identity-sheet coverage against the complete roster and combat archetypes; check source references, unknown/unranked cases, form separation and private-lore boundaries.
- Verify perception without feasible response, unfamiliar versus observed patterns, burst versus sustained output, distinct defence mechanisms, coordinated versus obstructed groups, character-specific AI and protection/restraint scenarios. Record actual outcomes rather than assuming the design works.
- Verify new move/progression reviews include combination exploits, lore limits, tier impact, generated-skill validation and save compatibility. Confirm combat has no hidden tier-based guaranteed wins or protagonist outcome overrides.
- Verify survival, escape, rescue and delay objectives resolve and report success independently of defeating an apex opponent. Verify clearly labelled restrained sparring, bounded preparation/teamwork counterplay, hierarchy-preserving difficulty settings and authored progression across tiers. Preserve distinct strengths and April's tactical role without inventing physical powers.

- Build a reproducible matchup matrix spanning the ranked characters above, representative guard archetypes and all four Iron Circle bands; assess April separately rather than requiring duel-tier wins, with fixed seeds, both player/opponent sides, equal starting conditions, and distinct baseline/form cases. Record win rates, fight length, damage/resource use and relevant tactical exceptions; define quantitative acceptance bands before tuning rather than inventing passed results now.
- Verify Iron Circle generation and validation enforce D/C/B/low-A placements and full-strength contenders remain below Rei; check saved ranks, stored opponents and encounter restoration. Verify exact boundary ranks 450, 301/300, 101/100, 11/10 and 2/1, smooth adjacent-rank difficulty, distinct contender previews and the actual champion encounter. Ordinary rank increments must not skip the title fight. Verify powerful new entrants retain their abilities and earned titles survive save migration.
- Demonstrate the requested mild, moderate, large and overwhelming gaps in resolved fights, including Sylvanis's overall apex position. Audit within-tier variety and explain specialist matchups rather than forcing identical results for every pair.
- Check critical-hit bursts, restraint/counter loops, impact storage, evasion, armour, healing and resource exhaustion for unintended tier-breaking exploits. Verify ability boundaries remain intact and animations/narration report actual outcomes.
- Review April's direct-combat and tactical contribution separately; verify that information, preparation and allies improve her contribution without granting omniscience or physical dominance.
- Verify new stories, existing saves, earned forms, custom profiles and encounter restoration. Run relevant combat/profile/tactics tests and combat UI smoke checks after implementation; inspect the in-person UI's revised threat and outcome states. Apply phone dark-theme checks if any phone surfaces change.
- Approval evidence (2026-11-10): the user approved the recommended S+/S/A+/A/B/C/D hierarchy, April as a separate specialist, gap definitions and all lore refinements, and specified Iron Circle D/C/B/low-A placements below Rei. The user subsequently confirmed ranks 450–301 D, 300–101 C, 100–11 B, 10–2 low A and Rei as the starting #1 A-tier champion, plus all arena refinements: smooth transitions, rank/strength separation, an explicit title bout, saved-title preservation, distinct contender styles/previews and ruleset-sensitive threat assessment. Implementation and gameplay verification remain pending.
- Further approval (2026-11-10): all combat identity/behaviour refinements, identity sheets for every character and ongoing new-move/progression balance reviews are confirmed. This edit records scope and acceptance criteria only; sheets, mechanics and review tooling are not yet implemented or verified.
- Planning evidence: inspected `combat_profiles.py`, `four_aces.py`, `takeo.py`, `the_crow.py` and character-reference passages. Existing ratings cluster several requested tiers; April's current profile emphasises cognition over physical combat. No numerical rebalance, matchup simulation, gameplay test or UI inspection has been performed for this scope addition.
- Record implemented balance/lore behaviour, access, migration and actual checks in the release catalogue when shipped; this plan addition is not a released balance patch.

## In-character AI-generated sparring, fight and lesson requests

Confirmed scope addition, 2026-11-10: when the player asks someone to spar, challenges them to an agreed fight or asks them to teach a selected martial art, generate the initiating spoken line in the selected protagonist's own voice instead of displaying the same baseline question for everyone. This includes canonical and custom protagonists and both combat-screen and hangout entry points. Invitations, lessons and encounters remain in the in-person window. Lesson requests were explicitly confirmed on 2026-11-10 and must reflect the protagonist's personality and relationship with the teacher.

**Current evidence:** `combat_dialogue.py` currently supplies fixed `LINES` for sparring, challenges and lessons (`Would you teach me {art}?`), generates only the recipient's dialogue/reaction, and writes the fixed line into `record['player_line']` during commit. `combat_ui.py` and `hangout_combat_ui.py` expose the corresponding request controls. This scope addition is planning only; no runtime dialogue changes or tests have been performed.

### Required behaviour

- Generate a brief, natural protagonist invitation using their established voice, personality, speaking style, relationship with the recipient, current location and relevant recent conversation. Custom protagonists use their saved authored identity and voice context. Vary phrasing contextually rather than merely swapping names into a universal sentence; do not promise mathematical uniqueness or caricature every character.
- Preserve the selected intent: a friendly spar remains practice, an agreed-fight challenge requests agreement, and a lesson request asks the selected teacher to teach the selected martial art. Do not turn these requests into an unsolicited attack, threat, wager, romance advance or invented personal grievance.
- Supply protagonist context separately from recipient context and respect who knows each private fact. Do not invent shared history or reveal undisclosed powers, identities or trauma to make a line sound distinctive.
- Generate the recipient's existing in-character response to the actual generated invitation. Keep acceptance, eligibility and encounter outcomes under the existing authoritative rules; persuasive wording does not bypass refusal, unlock a fight or grant a lesson. For lessons, keep the selected teacher/art identifiers authoritative, preserve teaching eligibility and training prerequisites, and respond to the actual generated request. Do not invent prior tuition, mastery or a promise to teach an unavailable art.
- Carry one validated `player_line` through result, review/display, commit, combat dialogue history and active/archived hangout history. The displayed invitation, the line answered by the recipient and the saved utterance must agree. Do not regenerate at commit or overwrite the generated line with `LINES`.
- Retain scene/eligibility revalidation and duplicate-commit protection. Invalid, failed or stale generation must not start combat, apply training, spend lesson time or other resources, spend a turn or record an utterance that was never accepted into the scene. Allow retry through the existing interaction flow; do not silently present a fixed question as successful character-specific generation.
- Preserve older dialogue history containing baseline lines. Use additive data handling and assess compatibility for pending/legacy results without rewriting past conversations. Attack wording remains outside this specific request. Accepted lessons apply existing training effects and time costs once through the authoritative commit path; generated dialogue must not itself award skill or narrate a completed lesson before commitment.

### Acceptance and evidence required

- Verify canonical protagonists with contrasting voices and a custom protagonist, friendly spar versus agreed challenge versus martial-art lesson requests, varied teacher/student relationships, refusals and recent-context references. Inspect actual generated samples for voice, intent and lore boundaries; mock responses alone do not establish dialogue quality.
- Verify lesson requests name or unambiguously refer to the selected art, use the selected teacher, and preserve eligibility/refusal outcomes. Check accepted lessons apply training and time costs exactly once, including repeated commits; unavailable arts, failed generation and stale results grant no training.
- Check combat-screen and hangout entry points, visible review/result states and active/archived history. Confirm the same generated initiating line is used throughout and the recipient responds to it.
- Test invalid/missing generated fields, failed generation, scene changes, changed eligibility and repeated commits; verify no unintended combat start, training award, time cost or duplicate history. Check legacy dialogue records remain readable.
- Run relevant combat dialogue tests and UI smoke checks, and inspect rendered in-person states after implementation. If any phone surface changes, apply the phone dark-theme checks. Record actual commands and results, save impact and release evidence when implemented.

## Window layout

- Left: the player combat portrait, with their status panel immediately toward the centre.
- Right: the opponent combat portrait, with a mirrored status panel toward the centre.
- Arena background: current location artwork with dark translucent information panels and a fallback when artwork is unavailable.
- Bottom centre: narration with the latest action prominent and earlier turns available for review.
- Bottom controls: learned combat moves and options, with clear categories and previews of costs, targets, and effects. Preserve existing Martial, Unique skills, Awakened signatures, Utility, and amplification selection. Attack, Skills, Items, Defend, and Escape groupings are only appropriate where the engine supports them.
- Show turn ownership, opponent intent, numeric health/resource bars, status effects with explanations, and a clear selected target.
- Portraits shrink before narration and controls become cramped. Give dangerous opponents and bosses distinct framing without obscuring information.

## Implementation stages

1. Reconcile approved lore, titles, knowledge boundaries, ability definitions and identity sheets with runtime profiles/catalogues. Define remaining numerical formulas and migration contracts without reopening confirmed scope.
2. Implement and verify the hierarchy, specialised roles, Trait/form mechanics, combat AI and new-move/progression review requirements. Preserve baseline versus active-state distinctions and source evidence.
3. Implement Iron Circle tiers/title encounters, Richter balance, alternative objectives and training/progression rules with save-owned outcomes and compatible legacy data.
4. Implement protagonist-specific spar/challenge/lesson requests and recipient context/history consistency, retaining authoritative eligibility and once-only effects.
5. Build the responsive arena HUD, portrait/location-art arrangement, status and resource displays, move previews, expanded definitions, controls, narration/history and keyboard access. Preserve training, hangout combat, targeting and restoration in the in-person window.
6. Supply resolved-event/state data to Part 1. HUD values, costs and narration use the same result; visuals cannot reroll outcomes. Verify both parts together when integrated.
7. Complete relevant unit/smoke checks and rendered-state review, document actual migrations and player access, then validate/export release patch notes when implemented.

## Acceptance and validation

- Complete the detailed balance, lore, identity, dialogue, arena and boss acceptance criteria above and in linked references. Preserve all approved decisions and explicit unresolved formula details.
- Inspect normal/small windows, resizing, long names, missing static artwork, tooltips, disabled controls, narration history, target selection, expanded ability panels and encounter completion.
- Verify resource/status displays and dialogue follow authoritative results, repeated input cannot duplicate actions, failed/stale AI responses cannot reroll or commit gameplay, and legacy/current saves retain progression and encounter state.
- Run relevant combat/profile/tactics/progression/dialogue tests and combat, enhanced combat, portraits, opponent and dialogue UI smoke checks. Record actual commands/results; no unrun check is claimed passed.
- Combat, training and hangout fights stay in person. If phone surfaces change, retain dark styles and embedded dialogs, run `tests/phone_dark_theme_smoke.py` plus relevant checks and inspect interactive states.
- Integrate with Part 1 to verify HUD/effect timing, safe callback lifecycle and restored presentation; Part 1 owns visual coverage and recipe checks.
- For implemented player-visible changes, follow `patch_notes/AUTHORING.md`, document actual behaviour/access/save impact/evidence, validate and export. Planning documents and the split itself are not gameplay releases.

## Split verification evidence

On 2026-11-10 the existing lore, dialogue and layout sections were retained here and the complete animation catalogue/requirements moved to Part 1. All approved scope remains under MH-001. Existing detailed references and historical production evidence were preserved; no runtime files or saves were changed by this reorganisation.
