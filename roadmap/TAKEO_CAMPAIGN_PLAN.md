# MH-018 — Takeo Mishima: Empire of One

**Editorial development, 2026-11-11:** [MH-019](CAMPAIGN_REVISION_PLAN.md) strengthens concrete command costs, distinct historical motives, independent opposition and era continuity while preserving this confirmed treatment and single ending. It does not reopen the superseded alternate endings, change Takeo's authoritarian character, add a Neo reunion or assign an implementation slot.

**Status:** Planned — campaign treatment confirmed by the user on 2026-11-11, with **Empire of One** as the title and the recommended ending selected. No runtime implementation.  
**Recorded:** 2026-11-11.  
**Tracking:** [Roadmap MH-018](../ROADMAP.md#mh-018-takeo-mishima-playable-campaign).  
**Sequence:** Not assigned. Preserve the approved interiors → MH-016 → Mavis → Martos → Elias → Camila → Sylvanis implementation order. This planning work does not add a fifth approved slot or resume paused artwork.  
**Scope:** Playable Takeo, no Grove, three starting contacts, his historical rise, and a complete present-day expansion story with a playable climax and settled aftermath.

**Confirmation — 2026-11-11:** The user approved these campaign ideas as the confirmed plan. The fourteen-chapter story, eight historical sequences, American expansion, Crow betrayal, former Directive 0 deputy, command relationships and headquarters aftermath are accepted scope. The completed campaign has one confirmed ending: Takeo preserves the bridgehead and Thirteen's command, then personally destroys the contested programme archive. Alternate titles and the two alternative endings from the initial brainstorm are superseded and are not queued features. Exact manuscript wording, unnamed supporting characters' personal details, fine chronology, final room layouts and combat tuning remain authoring work. Approval of the plan does not mark it implemented or change the existing release order.

## Plugin task assignments

**Assigned:** 2026-11-11. Planned; implementation slot remains unassigned. Empire of One and its single confirmed ending are not reopened.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Steps 1, 3–4: chronology, fourteen chapters and eight historical sequences | Story Skills + Writer's Loop | Reconcile roughly-56 age/slow ageing and private knowledge; preserve authoritarian character, the confirmed treatment, no Neo reunion and the distinction from Sylvanis's arena story. |
| Step 2: playable start, exactly three contacts and no Grove | falsegreen-skill | Review assertions across new game, registration, navigation and load; pair suppression checks with valid unaffected starts, intended contacts and actual leader access. |
| Steps 5–7: objectives, confirmed finale, visits and persistent aftermath | Story Skills (interactive-fiction) + falsegreen-skill | Map supported tactical choices within the one ending; test retries, archived/destroyed resources, one-time rewards, historical isolation and no cross-protagonist mutation. |
| Historical portraits and room-dependent scene art | Story Skills for era briefs; Bulk BG Remove only for portrait isolation | Keep identity/age references independent, wait for stable rooms and use existing art/presentation contracts. Inspect in-person scenes and every changed dark phone state. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Confirmed requirements and history

The following facts come from the user's original campaign request and age clarification. The present-day treatment below was subsequently confirmed as the campaign plan:

1. Takeo Mishima becomes a playable character. He has **no Grove account**. His starting contacts are **Sylvanis, Number Thirteen and Keisuke Hachimura**.
2. He is **roughly 56 in the present day**. His Awakening means he does not visibly age much. The current age of 42 is superseded for future implementation; no new birthday, exact birth date, immortality or regeneration mechanism is established.
3. He was a special-forces operator and captain of **Directive 0**, a United Nations top-secret black-operations death squad.
4. Directive 0 was disbanded because of ethical concerns. Takeo subsequently chose to join **Onami**, a Japanese militant terrorist organisation.
5. He helped Onami conquer Japan in **2024**. He respected the absolute power and strength of its leader, **Shinzo Kazama**, and Kazama's ambition to subjugate the world and obtain power at all costs. Takeo became Onami's military commander.
6. His **Nanoengine** powers provided the baseline for Onami's **Shinigami Protocol** experiments to create supersoldiers.
7. The United Nations Military defeated Onami in **2027**, and Shinzo Kazama was killed. Takeo founded the **Shinokami** from Onami's remnants.
8. He continued Shinigami Protocol experimentation, including on his own son. He gave his son no name, only the designation **One**; the boy later became **Neo Ishida**.
9. After the raid in which Neo escaped, Takeo groomed **Thirteen** into his latest and only success. He formulated an expansion into the Americas and began working with Sylvanis, begrudgingly.

Keep Takeo's deliberate choices legible. Directive 0's dissolution did not force him into terrorism. Admiration for Kazama did not remove his responsibility. He treated his son as a subject because of his own convictions, not because he secretly lacked permission to love him.

## Central dramatic idea

**Takeo can overpower an army. Can he build an empire that does not depend on his standing in every room?**

His history runs through three forms of authority: the institution that licensed his violence, the conqueror whose strength he willingly served, and the organisation he now commands. The present campaign asks what survives when fear produces dishonest reports, a commercial partner withholds cooperation, and his most prized subordinate begins making decisions of his own.

Confirmed title: **Empire of One**. It refers to his isolation at the top and echoes the number he gave his son. Do not imply Neo wants to inherit the Shinokami.

Confirmed character direction: retain the severe, deliberate authoritarian established in [takeo.py](../takeo.py). His development concerns the limits of command and his response to them, rather than an automatic redemption. He may revise a strategy and recognise a subordinate's usefulness without becoming kind. His view that superior strength grants the right to rule remains his belief, not the narrator's verdict.

## Chronology and source reconciliation

The [game calendar](../story_calendar.py) starts in **2050**. At roughly 56, Takeo is approximately 30 in 2024 and 33 in 2027; exact ages depend on a still-unspecified birthday. This permits an adult special-forces career and captaincy before Onami. His appearance should remain recognisably the established 211 cm Human Siege Engine: the age correction does not call for an elderly redesign. Slow visible ageing does not establish invulnerability, eternal life or a new combat power.

| Topic | Current source / issue | Treatment for future implementation |
| --- | --- | --- |
| Playability and age | [playable_cast.py](../playable_cast.py) excludes `takeo`; [takeo.py](../takeo.py) lists 42 and leaves his defection unresolved. | Add the requested protagonist and roughly-56 history deliberately, including selection, profile and contextual references. Planning changes none of those files. |
| Historic expansion versus current US command | [thirteen.py](../thirteen.py) already makes Thirteen commander of US operations at Pacific Relay Depot. | Show the first American expansion decision in history. The present story expands an existing foothold into a self-sufficient regional command; it is not his first arrival in America. |
| Shinigami Protocol | Older [worldbuilding](../Mysterious%20Hearts%20-%20Worldbuilding.md) describes conditioning without a named Trait; [vendetta_lore.py](../vendetta_lore.py) now names Shinigami Protocol for Neo and Thirteen. | Reconcile those sources to the new Nanoengine-baseline experiment history. A baseline is not proof that either subject has Takeo's Nanoengine, a neural HUD, implants, a remote-control switch or identical abilities. Exact experimental mechanism remains undecided. |
| One and the only success | Existing lore says One excelled and Thirteen was once the weakest child. | Preserve both. Thirteen is Takeo's latest and only retained success after the raid, according to the new premise; One remains an exceptional escaped survivor. Do not rewrite One as weak, Thirteen as a defective copy, or imply no earlier subject ever performed well. |
| The raid | Existing Thirteen lore identifies an Interpol raid, the other subjects' deaths and an unspecified killer. | Preserve that bounded history. Do not assign the deaths to Neo, invent a childhood promise, or claim he could have saved everyone. Dates and historical ages need a shared chronology pass. |
| Movement | NPC Takeo currently stays permanently at Kestrel Operations Centre. | Confirmed protagonist-only campaign travel exception. Other protagonists retain his existing NPC appointment rules; authored absences must be explicit. Do not silently make him a casual outing companion. |
| Syndicate relationship | [criminal_dynamics.py](../criminal_dynamics.py) already proposes a future Crow betrayal of dependent Shinokami expansion. | That plan becomes the present conflict of this route. It is not a completed event until authored gameplay resolves it. Takeo learns only what he actually discovers. |
| Sylvanis route | [MH-014](SYLVANIS_CAMPAIGN_UPDATE_PLAN.md) ends its arena crisis while leaving the territorial betrayal unresolved. | The later expansion crisis is a separate campaign episode. Playing Sylvanis first is not a prerequisite; a new Takeo save starts with the baseline deal. Cross-route shared-save support needs explicit chronology and outcome rules before implementation. |

No exact dates are assigned to Directive 0's dissolution, One's birth, the raid, Thirteen's grooming or the first supply agreement. Do not compress all of them into 2027. Other characters' private knowledge, civil identities and unplayed story outcomes remain compartmentalised.

## Playable starting state

- **Protagonist:** Takeo Mishima, supreme leader of the Shinokami, with his established Nanoengine and military expertise available from the start. He does not begin as a recruit or unlock his canonical strength through ordinary training.
- **Starting place:** Kestrel Operations Centre, command-room opening. Thirteen is at the existing Pacific Relay Depot US command; Keisuke remains its recruitment/enforcement liaison.
- **Starting contacts:** exactly Sylvanis, Number Thirteen and Keisuke Hachimura as the intended seeded personal contact set. This does not require his supreme leader to earn subordinate recruitment ranks. Identity-specific access must survive contact refresh, loading and suspension checks without changing other protagonists' gates.
- **No Grove:** no seeded account, profile, feed, suggested registration, creation prompt or recreated account on load. Check global social-account initialisers as well as the visible app. Other communication tools can remain available according to their existing rules.
- **Campaign access:** future character selection → Takeo → the in-person **Stories, guards & gang properties → Story** objective view. Destination selection/travel follows **Maps** under [MH-016](CAMPAIGN_PRESENTATION_UPDATE_PLAN.md). Meetings, command decisions, historical visits and combat occur in the **in-person window**.
- **Between chapters:** private reports, an armoury inspection, a supervised training observation and command conversations. These express his position without ordinary job applications, dating assumptions or a friendly Grove persona. His private money, faction resources and starting equipment still need balance design; do not invent a spendable empire-sized balance.

## Confirmed present-day story

### Act I — An empire on borrowed ground

Takeo decides the Pacific Relay foothold has reached its limit. He plans a regional command and research centre capable of supporting broader American expansion: the **Meridian complex**. This is a new fictional campaign location, not an already-owned site or an instruction to seize a real place.

Thirteen will command it, Keisuke will oversee local enforcement and recruitment, and Sylvanis will supply Red Magic and Blue Magic through the Syndicate. Takeo dislikes relying on him, but recognises the immediate value. The Crow's role is understood through the liaison and actual agreements, not a new face-to-face introduction.

The first action sequence establishes Takeo's power: he personally ends a challenge at an authorised campaign site. Then he receives three conflicting reports about whether the resulting foothold is usable. He can win the fight; intimidation alone cannot tell him which account is true.

### Act II — The cost of obedience

An inspection reveals that the supposed expansion success depends on Syndicate-controlled services, frightened local officers and an exaggerated research forecast. The soldiers are real; the claims that they can become a reliably reproducible Shinigami force are not proven.

Keisuke has punished bad news and passed reassuring reports upward. He remains a capable, dangerous enforcer, not comic relief. Thirteen has concealed one withdrawal decision because admitting an order failed would expose him to Takeo's judgement. His decision kept an existing unit functional; the lie still had consequences. Neither subplot automatically establishes a conspiracy between them.

Sylvanis admits that temporary drug effects cannot simply replace the years and conditions behind Thirteen's development. He is amused by Takeo's desire for consistency. He does not become remorseful, secretly loyal or susceptible to a threat that makes him obedient.

### Act III — The captain who would not stand down

A **former Directive 0 deputy**, now part of an authorised UN operation, identifies the expansion. This character's role is confirmed; name, age, present rank and institutional appointment remain to be authored. This is a former subordinate who rejected Takeo's later choices, not a hidden mastermind who caused his downfall.

The deputy's aim is to stop the new regional programme and secure its records, not prove personal physical superiority. They recognise the Human Siege Engine's danger and conduct the conflict around bounded objectives. Give them credible concerns and accountability for their own classified past; do not imply every UN official is either secretly corrupt or morally spotless.

Their challenge is personal: Directive 0 ended, but Takeo never accepted that anyone had the authority to tell him to stop. Parallel memories show that he nevertheless chose to serve Kazama. He accepted a superior when he admired that superior's strength; he now treats the same choice in others as disloyalty.

Takeo discovers concrete evidence that the Syndicate's assistance has made the new complex dependent on resources it can withdraw. He suspects a takeover only after those findings. He cannot read the Crow's private plan from the player's prior knowledge.

### Act IV — An order that cannot be obeyed

The Crow activates the local takeover: support is withdrawn and Syndicate personnel contest the new complex and its research assets. The UN operation acts on separately established evidence of the expansion. Their overlapping objectives create a three-sided crisis; they are not secretly one faction, and the Crow does not control every response.

Thirteen receives mutually incompatible demands: hold the relay, preserve the research transfer and reinforce Takeo. He cannot satisfy all three. His first significant assertion is professional and personal: **“Name the objective. I cannot hold three positions.”**

Takeo must decide what matters before force can serve it. Sylvanis states plainly that their commercial bargain never made him a subordinate. His participation or withdrawal is his own chosen amusement or interest; Takeo neither tricks nor coerces him into helping.

### Act V — Empire of One

The expansion crisis culminates inside the Meridian complex. Takeo breaks through an attack meant to isolate his command. Meanwhile, the UN deputy pursues the programme records, the Syndicate pursues the local assets, and Thirteen tries to keep his command intact.

The climax resolves the specific expansion attempt and contested records. It does not require the death of the Crow, Sylvanis, an Ace, Thirteen or Neo, the conquest of an entire continent, or a newly invented fighter stronger than everyone else.

## Fourteen-chapter outline

| ID / title | Present action | Memory or dramatic payoff |
| --- | --- | --- |
| TK-01 — State the Result | Open at Kestrel with the three contacts' incompatible reports; approve the Meridian objective. | Establish supreme command, starting access, current US foothold and actual success conditions. |
| TK-02 — Directive 0 | Respond to the first challenge and examine a reference to his former unit. | TK-F01 shows his captaincy and squad; TK-F02 shows ethical dissolution and his deliberate rejection of its judgement. |
| TK-03 — A Man Worth Following | Negotiate the first concrete expansion terms with Sylvanis. | TK-F03 introduces Kazama, Takeo's chosen service and the 2024 conquest. Clarify why he once obeyed another man. |
| TK-04 — The Original Weapon | Inspect the programme's claims against its actual results. | TK-F04 shows Nanoengine becoming Onami's experimental baseline. A research aspiration is not a proven production method. |
| TK-05 — What Survived | Resolve an early dispute over which personnel and assets can sustain the new site. | TK-F05 covers the 2027 defeat, Kazama's death and Takeo gathering the remnants into Shinokami. Do not invent the killer. |
| TK-06 — One | A private review exposes the difference between a numbered inventory and a person. | TK-F06 establishes his nameless son and continued experimentation. No forced present-day reunion or disclosure to outsiders. |
| TK-07 — The Remaining Shinigami | Thirteen's private report contradicts the official account of a withdrawal. | TK-F07 covers the raid and subsequent grooming, preserving the unspecified killer and Thirteen's survival. |
| TK-08 — Across the Pacific | Inspect Pacific Relay and its connection to the Meridian complex. | TK-F08 shows the original American ambition and first begrudging Sylvanis agreement. Return to their accumulated dependence. |
| TK-09 — The Last Captain | Receive the former deputy's authenticated demand and respond to the UN operation's first bounded intervention. | The past returns through a person who remembers Takeo's choices. No automatic surrender or scripted bodily defeat. |
| TK-10 — Good News Only | Compare Keisuke's reports, research results and Thirteen's account in separate in-person scenes. | Reveal how punishment distorted information. Takeo can change reporting demands without becoming compassionate. |
| TK-11 — Borrowed Ground | Discover the concrete dependency and resolve a contested supply/command objective. | The Crow's local takeover becomes evidenced action, not an omniscient narrator's instruction. |
| TK-12 — Name the Objective | Hold the final command meeting; establish preservation of the regional force as the priority, assign responsibilities and define retreat conditions. | Thirteen requires a feasible order. Keisuke's accountability and Sylvanis's stated position receive explicit consequences. |
| TK-13 — The Human Siege Engine | Play the continuous Meridian gauntlet and competing extraction/denial objectives. | Resolve combat, local control and custody of the records through actual encounter results. |
| TK-14 — Empire of One | Return to headquarters for the command settlement, contact scenes and final private reflection. | Confirm the expansion outcome, programme status, surviving command and changed business terms. Campaign complete. |

Eight stable historical sequence IDs are confirmed: **TK-F01** captaincy; **TK-F02** dissolution; **TK-F03** Kazama/2024; **TK-F04** Onami research; **TK-F05** 2027/founding; **TK-F06** One; **TK-F07** raid/Thirteen; **TK-F08** Americas/deal. Several span more than one shot or scene. They are not eight mandatory uninterrupted exposition dumps.

Historical atrocities are fixed wrongdoing, not an opportunity to rewrite Takeo as innocent. Use consequence, testimony and his decisions to establish them without turning child abuse into a scored activity. His son's experimentation and Thirteen's grooming need non-graphic, character-focused scenes. Present control belongs to authored fictional encounters and the decisions the campaign actually supports.

## Climax design

The arena crisis in Sylvanis's proposed route concerns his appetite for spectacle. This climax concerns Takeo's inability to personally secure every part of an organisation. Keep those dramatic purposes distinct.

1. **Breach:** Takeo enters the contested Meridian complex and demonstrates his established ability to break fortified resistance. Preserve the same building and encounter state between waves under MH-016. A normal guard does not become an equal merely because this is the finale.
2. **Divided command:** reports establish what Thirteen, Keisuke and the hostile forces actually control. Previously accepted responsibilities affect available options. Show the real state; do not award objectives because dialogue claims subordinates completed them.
3. **Last confrontation:** the former Directive 0 deputy confronts Takeo within the operation to secure the records. Their challenge is whether he can complete his declared objective before the competing operation does. Their equipment, support and escape limits require combat design; no invented Nanoengine shutdown, magic countermeasure or convenient new weakness.
4. **Irreversible priority:** Takeo commits to preserving the regional command and surviving force at the cost of recovering the unique programme archive. This is his confirmed authored decision, not an alternate-ending selector. Preliminary chapters establish that there is no complete backup, and that the opponent's action has already made saving both infeasible. The player executes the preservation and archive-denial objectives; do not introduce an unexplained final-button dilemma after flawless play.
5. **Resolution:** actually settle the site's control, record custody or destruction, withdrawal and opponent outcome. Taking down a squad is not automatically a strategic victory. Settle the local Syndicate takeover here; do not require a sequel to know whether this campaign's goal was achieved.

**Confirmed ending — Empire of One:** Takeo preserves the bridgehead and Thirteen's command, then personally destroys the contested archive rather than let it pass into another faction's hands. The destruction is an authored consequence of his priority and control doctrine. His army survives; his immediate path to a reproducible Shinigami force does not. His natural power is unaffected, and this destroys the local campaign archive, not every historical trace worldwide.

This is a material victory with a lasting cost. He can call it a calculated sacrifice. The player can see that the man who numbered his children has chosen a living, capable command over an imagined obedient army, without being required to read that as love or redemption.

## Confirmed finale and gameplay consequences

TK-14 must be a playable aftermath chapter, not only a title card or another cliffhanger.

- **Headquarters settlement:** a concrete report states which regional assets remain, what the UN obtained, which takeover attempt ended and what became of the local archive. The deputy may survive the operation's withdrawal; survival does not erase the resolution of their immediate objective.
- **Keisuke:** Takeo confronts the inaccurate reports and restricts his discretion. Supervised reporting and a narrower enforcement role reflect the actual campaign record. Do not force his death or erase his established liaison function without a separately authored replacement.
- **Sylvanis:** a last private exchange closes the failed agreement or sets limited replacement terms. Takeo understands that commercial cooperation never gave him command. Sylvanis remains amused, autonomous and evil; no friendship reward cures either man.
- **Thirteen:** he asks what the next order requires of him and states a practical limit. Takeo names him commander of the surviving regional operation rather than calling him a replacement One. This acknowledges an existing role; it is not a new promotion from recruit. Thirteen stays alive and retains his unresolved self-worth, cruelty and capacity for future agency.
- **Private final image:** Takeo reviews a retained high-level index of programme designations, not a backup of the destroyed experimental archive. One's entry still reads **escaped**, Thirteen's **active**. He closes it and calls for the current command map. His son's life remains outside his ownership, and he turns back to the empire he can still command.

| Confirmed ending | Required achieved outcome | Settled consequence |
| --- | --- | --- |
| **Empire of One** | Preserve the bridgehead and Thirteen's command; Takeo personally destroys the contested archive. | Local expansion survives under harsher independent terms. The immediate replication project is lost, the takeover is repelled at this site, and Thirteen remains a person on whom Takeo depends. |

The previously suggested **The Unfinished Army** and **A Throne Across the Sea** endings are superseded by the user's selection and excluded from implementation scope. Tactical and dialogue choices still change supported losses, custody outcomes, reporting arrangements and the cost of preserving the command; they do not restore the archive or replace the confirmed conclusion. Failure of a required finale objective uses checkpoints/retry rather than awarding the ending without achievement. Thirteen's disagreement remains his own decision and does not require his death. No end card schedules an unplayed Neo abduction, destroys his home or kills his friends.

## Relationships and dialogue anchors

The relationship arcs and dramatic beats are confirmed. These illustrative lines guide the manuscript; exact wording remains open to drafting, and none is an existing released quotation.

| Relationship | What the campaign explores | Proposed anchor |
| --- | --- | --- |
| Kazama / Takeo | A younger Takeo sincerely admired and served overwhelming ambition. Why was that obedience acceptable to him? | Takeo, recalling him: “He did not apologise for wanting the world.” |
| Takeo / Sylvanis | Discipline meets freely chosen chaos. They are useful partners and incompatible masters. | Takeo: “We had an agreement.” Sylvanis: “We still do. You keep mistaking it for an order.” |
| Takeo / Thirteen | Grooming has produced formidable capability without guaranteed obedience. Do not flatten him into either a grateful son or a repaired victim. | Thirteen: “You taught me to survive. Do not call it failure when I do.” |
| Takeo / Keisuke | The subordinate imitates his contempt for weakness and teaches others to conceal it. | Takeo: “I asked how many could fight. You told me how many were afraid to refuse.” |
| Takeo / former deputy | Someone who served under him refuses to accept his claim that command absolves conduct. | Deputy: “The unit was disbanded. You were not ordered to become this.” |
| Takeo / One | The absent son exposes the difference between making a weapon and owning a life. | Takeo's historical instruction: “One. That is sufficient.” The present narrative leaves Neo's chosen name and ordinary life intact. |

Neo need not appear physically for his absence to matter. An optional future encounter is a separate proposal requiring a credible discovery route, his own agency and protection of existing relationships. Do not place his address or chosen identity in Takeo's opening contacts, public dossiers or research reports by default.

## Repeatable historical area

Apply the every-campaign visit requirement from [MH-017](CAMPAIGN_FLASHBACK_AREAS_PLAN.md). Planned area ID: `takeo-command-history`, displayed as **Before the Orders Ended**. Open through **Visit flashback area** in the main in-person window after the corresponding mandatory memory. Keep present time paused, historical chats local, and an explicit return restoring present state.

| Period | Planned rooms / talkable cast | Conversation purpose and boundary |
| --- | --- | --- |
| Directive 0, before dissolution | Briefing room, equipment room, mess; former deputy and an unnamed squad medic. | Discuss captaincy, responsibility, competing accounts and the people behind the unit. These historical versions do not know Onami's future or the present investigation. |
| Onami, after 2024 and before 2027 | Command hall, courtyard, authorised research observation room; Kazama and a research supervisor. | Explore chosen allegiance, ambition and research claims. Kazama is alive only in this period; no playable cruelty activity or real experimental procedure. |
| Early Shinokami | Reconstituted command room, archive and training observation gallery; a remnant officer and research supervisor. | Discuss the cost of rebuilding, obedience and what the records omit. Childhood subjects are not social contacts; any authored appearances use independent age-appropriate references. |
| After the raid / first supply agreement | Kestrel command room and private reception; period-appropriate Thirteen and Sylvanis in separately gated scenes. | Thirteen's surviving status and the bargain's actual terms; no present command knowledge before it exists, no Crow presence inferred from the liaison. |

Proposed historical conversation openings: the deputy asks, “Does an order remain valid when the people who gave it refuse to own it?”; the remnant officer asks, “Are we rebuilding Onami, or following you?”; the research supervisor asks what counts as a success; Sylvanis asks what result Takeo expects to buy. These are topics for authored history, not opportunities to overwrite fixed events or learn future secrets.

The historical periods, supporting roles and room functions are accepted planning scope. Personal names/details, final connected layouts, appearance references and fine period dates remain authoring work. Optional visits cannot grant present contacts, resurrect Kazama, duplicate rewards, prevent the raid or expose private identities to a present listener.

## Implementation, saves and verification plan

Dependencies: [interiors](INTERIORS_UPDATE_PLAN.md), [MH-016 presentation](CAMPAIGN_PRESENTATION_UPDATE_PLAN.md), [historical areas](CAMPAIGN_FLASHBACK_AREAS_PLAN.md), protagonist selection/starts, private contact access, Grove account suppression, authoritative combat objectives, isolated history and [combat lore](COMBAT_CHARACTER_LORE.md).

1. Reconcile confirmed history, roughly-56 age and slow visible ageing across sources. Lock the period sequence and distinguish research inspiration from subjects' actual abilities.
2. Add the playable start, stable `takeo` identity, exactly three seeded contacts, no Grove, appropriate command access and protagonist-scoped travel. Preserve his NPC behaviour for other stories.
3. Develop the confirmed treatment into a manuscript: settle the deputy's personal details, fine chronology, location staging, supported tactical choices and combat tuning. The title, story direction and Empire of One ending were approved on 2026-11-11; they do not need approval again.
4. Draft the fourteen chapters and eight historical sequences, then integrate period-specific visits. Maintain private-knowledge disclosure and age-appropriate references.
5. Implement locations, objective state, save/resume and persistent aftermath using the completed shared systems. Produce room-dependent scene art only after layouts are stable.
6. Verify new-game access; no Grove across registration, navigation and load; exactly the intended starting contacts and no leakage into other starts; direct leader access without recruit ranks; travel and NPC availability; full route, tactical/dialogue consequences, failure/retry and the confirmed ending/aftermath; historical isolation; no duplicate rewards or restored destroyed archives.
7. Run relevant protagonist, major-campaign, conversation/flashback lore, combat-objective, save and patch-note checks. Phone changes require `tests/phone_dark_theme_smoke.py`, relevant feature smokes and rendered inspection of normal, hover, disabled, loading/error and resumed states. In-person layouts and scene transitions also require rendered inspection. List actual executed commands and results when implementation occurs.

**Save impact:** none from this plan. Future additive protagonist-scoped campaign, knowledge, objective, contact and historical state must preserve other stories. Do not retroactively turn every existing save into an active war, add Takeo as a contact elsewhere, replay completed history or mutate historical chat transcripts to his new age. Assess missing-start and migration rules before claiming compatibility. Canon reference corrections may affect newly generated dialogue after release; that does not rewrite previous events.

**Verification performed for planning:** inspected the roadmap/template, patch-note authoring rules, Takeo/Thirteen/Keisuke sources, playable roster, game calendar, criminal dynamics, relevant worldbuilding/combat references, Sylvanis treatment and historical-area plan. Documentation/catalogue verification results are recorded below after execution. No runtime code, art, saves, gameplay tests, rendered screens or live model calls are changed or verified by this planning task.

**Planning check results (2026-11-11):**

- Documentation checks passed for all 16 local links, fourteen ordered chapter IDs, eight historical sequence IDs, Markdown table structure, UTF-8 integrity, the single MH-018 roadmap section/row, the age clarification and retained approved sequence/artwork pause.
- Compared canonical JSON fingerprints: all 493 earlier catalogue entries are unchanged; only `plan-2026-11-11-takeo-campaign` was added as a Development report.
- `python patch_notes.py validate` passed with 494 entries.
- `python -m unittest discover -s tests -p test_patch_notes.py -v`: five passed; the existing archive-source check failed because `tests/screenshots/mixtape-art-review-0.jpg` is missing. This is the same pre-existing failure documented by preceding planning updates; no substitute screenshot or changed historical evidence was created.
- `python patch_notes.py export` completed and refreshed `patch_notes/PATCH_NOTES.md`. Planning reports remain distinct from gameplay releases.
- Runtime, artwork, gameplay/save tests and rendered UI inspection were not performed for this documentation-only task. The playable character, age/source reconciliation and campaign remain future work.

**Confirmation check results (2026-11-11):**

- Confirmed title, treatment, single ending and completed approval milestone agree between this plan and MH-018. Both alternate endings are explicitly superseded; the fourteen ordered chapter IDs and eight historical IDs remain unchanged. Tactical consequences and checkpoint/retry remain compatible with the fixed conclusion.
- All 16 local links, Markdown tables, UTF-8 integrity, roughly-56 age, no-Grove start and unchanged implementation order/artwork pause passed documentation checks.
- Canonical JSON fingerprints confirm all 495 prior catalogue records are unchanged, including the initial proposal and the intervening era-specific flashback reference report. Added only `plan-2026-11-11-takeo-campaign-confirmed`. The roadmap outside MH-018's row and section is unchanged.
- `python patch_notes.py validate` passed with 496 entries. `python -m unittest discover -s tests -p test_patch_notes.py -v` again had five passes and the existing missing `tests/screenshots/mixtape-art-review-0.jpg` archive-source failure. `python patch_notes.py export` completed.
- Planning confirmation only: no runtime, artwork, saves, gameplay tests or rendered UI changes. Detailed authoring and implementation remain pending; the approved story and ending do not require renewed approval.
