# MH-002: custom career and criminal starting backgrounds

Current status: implemented in MH-002 on 2026-11-10. [Final behaviour, numerical choices, tests and limits](CHARACTER_SELECTION_COMPLETION.md) supersede the planning-only implementation statements retained below.

Planned scope confirmed 2026-11-10. Parent: [Character selection and creation plan](CHARACTER_SELECTION_UPDATE_PLAN.md). The user approved the listed backgrounds, careers and starting ranks, freely selectable advanced starts and a simple options-selection window. Exact reputation/heat values, funds and other numeric balance remain proposals. Nothing here is implemented or released.

## Plugin task assignments

**Assigned:** 2026-11-11. Implemented under MH-002. Future requested maintenance only; final completion evidence still supersedes historical planning text.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Career/criminal background and rank descriptions | Story Skills + Writer's Loop | Separate reputation from membership/authority, preserve public/private biography and compatible work/faction choices. |
| Preset application, save/load and boundary regressions | falsegreen-skill | Review independent expected-state assertions and invalid combinations; run affected custom-protagonist, creator, selection and combat tests, and inspect the dark picker states. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Model: background, current role and experience

Choose narrative background, civilian employment and criminal affiliation independently where compatible. Their recognised experience contributes to one combined starting combat profile, alongside explicit training and awakened status. A former criminal can have a legitimate job without active faction access; an experienced photographer can be newly hired locally. Higher combat-relevant career/background tiers provide progressively stronger starting stats, rather than every custom character sharing novice values. Awakening and named Traits remain explicit character choices.

Permit one active JobSeek job and one compatible active criminal arrangement, following current state constraints. Day job plus criminal role is allowed; actual work still observes time, travel and scheduling conflicts. Explain exclusions rather than silently replacing a selection. Support career-only and crime-only characters fully.

## Bubblegram starting presets

Suggested reputation and heat values below are game balance proposals on the existing scales. Reputation determines visibility, while membership/rank and other requirements determine access; reputation alone grants no command authority. Heat represents current attention, not the number of crimes in a biography.

| Preset | Starting role | Suggested reputation / heat | Starting experience |
| --- | --- | --- | --- |
| Clean slate | No criminal role | 0 / 0 | Discover Bubblegram and build connections through play. |
| Former underworld worker | No active membership | 20 / 0 | Past experience acknowledged; no current faction clearance or fabricated hostility. |
| Independent operator | Unaffiliated contractor | 20 / 5 | Established small-time work without a gang command role. |
| Connected freelancer | Unaffiliated contractor | 40 / 10 | Wider recognition; invitations still follow appropriate access rules. |
| Trusted crew member | Trusted member, gang rank index 1 | 30 / 5 | Recognised member of one supported crew, with normal crew work. |
| Crew lieutenant | Lieutenant, gang rank index 2 | 50 / 10 | Established local responsibility and higher standing. |
| Crew captain | Captain, gang rank index 3 | 65 / 15 | Advanced start at the existing gang-rank ceiling, with normal consequences and remaining faction progression. |
| Small-crew founder | Founder of a custom crew, initial network tier | 25 / 5 | Own a modest new organisation using the custom-gang system, not command of a canonical gang. |
| Established faction member | Syndicate rank index 1 or Shinokami Member | 40 / 5 | Already sponsored/inducted, with access appropriate to the selected role. |
| Faction specialist | Syndicate rank index 2 or Shinokami Squad leader | 50 / 10 | Experienced branch work with limited authority. |
| Faction field leader | Syndicate rank index 3 or Shinokami Unit captain | 60 / 15 | Advanced operational role, below faction executive leadership. |

Confirmed: ordinary and advanced starts are freely selectable without achievements, prior playthroughs, currency costs or unlock requirements. Clearly label advanced starts as skipping early progression and keep newcomer as the default. The approved starting range leaves Syndicate Lieutenant and higher, and Shinokami Executive and higher, for in-story progression in this update. These are creator scope limits, not universal lore restrictions. Named canonical positions such as Cardmaster, Jokers, Aces and Takeo's Supreme Commander are not selectable replacements.

Existing street-crew choices include Lantern Crew, Rail Yard Saints, Purple Skulls, Hamayashi-kai, Los Rojos and Waterfront Consortium. Map eligible presets to each organisation explicitly: a trusted member in a high-profile organisation may need a higher starting reputation than the base table. The approved creator presets are selectable without in-story discovery requirements. Choosing an established affiliation seeds only the role knowledge needed for that start. Use spoiler-light organisation summaries in the picker; hide unrelated secret identities and events. In-story discovery gates continue to apply to unselected affiliations and unrelated secrets.

### Faction rank mapping

These titles come from the current `job_apps.BRANCHES` catalogue; displayed levels are human-readable, while saved rank indexes are zero-based.

| Branch | Member start (index 1) | Specialist start (index 2) | Field leader start (index 3) |
| --- | --- | --- | --- |
| Syndicate Clubs | Clubs operative | Clubs specialist | Clubs team leader |
| Syndicate Hearts | Hearts operative | Hearts coordinator | Hearts producer |
| Syndicate Diamonds | Diamonds clerk | Diamonds analyst | Diamonds controller |
| Syndicate Spades | Spades operative | Spades specialist | Spades handler |
| Shinokami | Member | Squad leader | Unit captain |

Treat branch selection as work identity, not automatic control of another branch. Established membership bypasses its initial sponsorship trials but does not create historical mission completions. Define standing, sponsor/affiliation representation and recognised prior experience per preset. Verify later promotion checks, invitations, resignations, expulsions and lost reputation operate normally. An affiliation may establish role recognition without creating friendships with named NPCs or revealing confidential identities beyond clearance. Apply the shared identity-visibility rules to alias recognition and legal-name linkage.

Confirmed narrative backgrounds: former courier, street survivor, freelance fixer, former crew member, faction transfer, underground fighter, numbers specialist and small-crew founder. Select recognised experience/training alongside these backgrounds so supported history can affect starting combat stats. Free prose alone does not set arbitrary ratings. No background promises unimplemented activities. “Former” membership grants neither current clearance nor automatic enemies, but accepted prior training may retain its combat contribution.

## JobSeek experience tiers

Use the existing job ladder rather than inventing a separate creator-only ranking system.

| Starting option | Saved rank | Intended experience |
| --- | --- | --- |
| Looking for work | No employment | Choose career interests and explore listings. |
| New hire / trainee | 0 | First job or career change, full early progression. |
| Experienced worker | 1 | Credible prior work; starts in the second existing job title. |
| Senior professional | 2 | Skilled practitioner with the third existing job title. |
| Manager / lead | 3 | Advanced start at the fourth existing job title; retain higher career progression. |
| Returning professional | No active employment, chosen prior career experience | Keeps an explicitly declared prior-career profile for re-entry, without current wages or workplace authority. |

Confirmed: ranks 0–3 are freely selectable, with Department lead, Regional coordinator, Regional director and Career fellow earned in play for this update. An advanced title must work mechanically: audit management/project/qualification gates rather than merely displaying a manager label. Either represent recognised prior credentials/portfolio explicitly or state which local requirements still need fulfilling. Do not equate a job title such as Café manager with ownership of the venue.

### Starting careers supported by current JobSeek

| Career | New hire | Experienced | Senior | Manager / lead |
| --- | --- | --- | --- | --- |
| Photography | Assistant photographer | Photographer | Senior photographer | Photography director |
| Modelling | Junior model | Booked model | Campaign model | Lead model |
| Library | Library assistant | Librarian | Senior librarian | Library manager |
| Oculus reception | Reception assistant | Receptionist | Senior receptionist | Front desk manager |
| Cinema | Cinema attendant | Projection assistant | Shift supervisor | Cinema manager |
| Café | Café assistant | Barista | Shift lead | Café manager |
| Floristry | Flower assistant | Florist | Senior florist | Shop manager |
| Kitchen | Kitchen assistant | Line cook | Sous chef | Head chef |
| Retail | Sales assistant | Sales specialist | Team lead | Store manager |
| Arcade | Arcade attendant | Cabinet technician | Floor supervisor | Arcade manager |
| Gardening | Grounds assistant | Gardener | Senior gardener | Grounds supervisor |
| Bar | Bar assistant | Bartender | Shift supervisor | Bar manager |

Review displays actual current pay and hours from the job catalogue, not copied amounts in preset text. Workplace employment, including Oculus reception, grants only the job's intended access and no automatic security clearance or relationships.

### Civilian narrative backgrounds

- **First job:** new hire or unemployed; useful for a simple start without invented qualifications.
- **Career changer:** prior work in another field, starting fresh in the selected job. No automatic transfer of all ranks or skills.
- **Transferred professional:** experienced or senior worker moving to Winterfield; recognised work history without established local friendships.
- **Returning to work:** choose previous career experience and current employment separately; personal reasons remain player-authored.
- **Creative practitioner:** photography, modelling or other descriptive creative work, with supported portfolio facts where implemented.
- **Vocational specialist:** practical training suited to kitchen, floristry, arcade or gardening work; only supported credentials have mechanical effects.
- **Experienced supervisor:** a manager/lead start with explicit leadership capability and responsibilities.
- **Student / recent graduate:** narrative education and an optional part-time-compatible career choice. Do not imply a new university/degree simulation or arbitrary credentials.

Unsupported professions remain valid descriptive biography with clear “no playable career track yet” labelling. Do not present doctor, lawyer or other new careers as implemented simply because the player types them.

## Progression and compatibility design

### Progressive starting combat power: confirmed scope

User decision on 2026-11-10: backstory and career experience must affect starting combat power, including awakened power and Trait refinement. Improvements must be noticeable across multiple tiers, not a novice/advanced binary. In particular, Syndicate field leaders and Shinokami unit captains start stronger than specialists, who start stronger than ordinary members. This supersedes the earlier separation of career seniority from combat starting stats.

**Stat-scale authority:** use [MH-001 lore-based balancing and character power](../COMBAT_WINDOW_UPDATE_PLAN.md#lore-based-balancing-and-character-power) for future stat representation, numerical thresholds, effective-strength gaps and progression. Its confirmed hierarchy is S+/S/A+/A/low A/B/C/D, with April assessed separately. Exact numeric thresholds remain undesigned. The earlier provisional 0–100 creator table is withdrawn; do not implement it as a second scale or assume a permanent 100 cap.

The following seven starting-experience steps and their hierarchy placements are confirmed scope. These are creator experience labels mapped to the existing MH-001 hierarchy, not a separate combat scale. Resolve final stats through MH-001’s shared balance rules and verify the approved target placements there.

| Experience step | Typical combat-relevant background | Required relative effect |
| --- | --- | --- |
| 0 — Newcomer | No relevant prior combat experience | Entry baseline under the shared balance scale. |
| 1 — Trained | Regular training, street experience, trusted crew member | Noticeable improvement over newcomer in relevant capability/control. |
| 2 — Practised | Independent operator, established faction member | Stronger practical skill and, where awakened, power/refinement than trained starts. |
| 3 — Veteran | Crew lieutenant, faction specialist or squad leader | Clear improvement over ordinary members without jumping directly to elite lore status. |
| 4 — Field leader | Crew captain, Syndicate field leader or Shinokami unit captain | Noticeably greater combat capability, Trait control and tactical experience than specialists. |
| 5 — Seasoned field leader | Step-4 role plus separately confirmed extensive combat/awakened history | A further meaningful increase into upper B. |
| 6 — Exceptional veteran | Exceptional civilian, independent or faction combat history | Freely selectable low-A start, below Rei under comparable conditions. |

Steps 5 and 6 are experience options, not newly selectable faction ranks; advanced choices remain freely available. Awakened power gains require an awakened start; Trait-refinement gains apply to a supported accepted Trait. Unawakened veterans still gain martial/tactical competence and must not automatically be classified as D solely for being unawakened. Do not invent a numeric ceiling or a specific named-character matchup from job title alone. Establish custom-origin placements and specialist stat distributions during MH-001 calibration, respecting the confirmed lore gaps and unique character capabilities.

All eligible branches receive tier progression, including Hearts, Diamonds and Spades. Branch/background emphasis may redistribute a small, documented amount between stats: physical fieldwork can favour martial skill, analysis can favour fight IQ, and sustained ability practice can favour refinement. Such variation must not erase the noticeable increase between corresponding role tiers or make every non-Clubs member a novice.

### Confirmed placement in the MH-001 combat hierarchy

Approved on 2026-11-10: the user confirmed these placements and added Exceptional Veteran at low A as a freely selectable start. Exact numerical balance and measured outcomes remain pending. MH-001 remains authoritative. “Lower/upper” describes position within an existing band, not a new tier. Compare healthy, ready characters with their accepted abilities and ordinary role equipment, without exceptional preparation or temporary peak forms. No package inherits a canonical character's unique abilities.

| Starting experience | Confirmed target placement | What the player should feel |
| --- | --- | --- |
| Newcomer | D, lower end; an untrained civilian may sit below the trained-guard benchmark | Inexperienced; even ordinary combat personnel are dangerous. Awakening alone does not establish fighting competence. |
| Trained | D, upper end | Noticeably more capable than a newcomer, but still below established elite personnel. |
| Practised | C, lower end | Credible professional fighter/operator with a large advantage over ordinary low-D opponents. |
| Veteran | C, upper end | Strong specialist or experienced squad-level fighter, noticeably above routine C opponents. |
| Field leader | B, lower-to-middle portion | A dangerous established fighter in the broad band containing Emily, Minsu and other named B combatants; no guaranteed victory over any named character. |
| Seasoned field leader | B, upper portion | Strong advanced start approaching contender territory. |
| Exceptional veteran | Low A | Contender-level starting combat capability, below Rei at comparable readiness; no automatic arena rank or title. |

Confirmed: **Exceptional Veteran — low A** is the strongest approved starting package in this update and is freely selectable without achievements, previous saves, completion gates, currency costs or unlock requirements. It is available to civilian, independent and faction backgrounds, not only faction leaders. Selecting the package explicitly establishes the required exceptional combat history; do not require an AI biography to prove eligibility or silently downgrade it to upper B. The creator must offer compatible, reviewed abilities/training and show the resolved low-A profile before starting.

Low-A capability does not award a new faction rank, elite canonical abilities, Transcendence, Iron Circle placement, title or recorded victories. A civilian may remain a florist or unemployed; a faction member retains the selected approved organisational rank. Main A, A+, S and S+ are not starting packages. Later advancement follows MH-001's authored progression decisions. Low-A customs remain below Rei under comparable conditions, with matchups against other contenders and enhanced Richter assessed individually rather than guaranteed. Preserve smooth transitions from upper B into low A and room for later growth.

#### Syndicate and Shinokami mappings

These packages include relevant prior training and operational experience; rank contributes real combat starting power through that package. Clerical title alone is not proof of skill, and a player's explicit stronger civilian/training history may raise the combined result without adding complete profiles together.

| Syndicate branch | Member start: lower C | Specialist start: upper C | Field-leader start: lower/mid B | Seasoned leader: upper B |
| --- | --- | --- | --- | --- |
| Clubs | Operative | Specialist | Team leader | Team leader + seasoned history |
| Hearts | Operative | Coordinator | Producer | Producer + seasoned history |
| Diamonds | Clerk | Analyst | Controller | Controller + seasoned history |
| Spades | Operative | Specialist | Handler | Handler + seasoned history |
| Shinokami | Member | Squad leader | Unit captain | Unit captain + seasoned history |

The seasoned column changes experience, not the selected organisational rank. Every approved branch can also pair its selected role with the freely selectable Exceptional Veteran package for low-A capability; this does not promote the role to Lieutenant or Executive. Lieutenant/executive and higher roles remain outside the approved starting-rank range. Their eventual combat placement needs authored experience and cannot be extrapolated automatically into A/S. Probationary associate and Shinokami Apprentice remain entry progression roles rather than additional established-start presets; where used in gameplay, upper D is a proposed baseline for a trained recruit, with stronger prior origins retained.

Suggested stat emphases: Clubs physical offence and martial technique; Hearts controlled ability use and adaptable positioning; Diamonds tactical judgement and precision; Spades mobility, precision and ambush capability; Shinokami disciplined martial technique and coordinated combat. These are proposed package styles, not new supernatural powers or mandatory Traits. Every branch receives progressive power/refinement when awakened and meaningful martial/tactical gains. Assess open duels separately from prepared or team encounters, particularly for support-oriented builds. Do not rank a custom Diamonds analyst as April's equivalent merely because both are analytical.

#### Street crews and independent backgrounds

| Background | Confirmed standard placement | Qualification |
| --- | --- | --- |
| Clean slate | Lower D | Unless an independent accepted training history raises it. |
| Former underworld worker | Retained prior experience step | Losing affiliation does not erase skills; do not add current access. |
| Independent operator | Lower C | Includes the practised operational history in the approved package. |
| Connected freelancer | Lower C by default | Contacts alone do not add combat power; veteran training can raise it to upper C. |
| Trusted crew member | Upper D | Trained baseline; stronger independent background can raise it. |
| Crew lieutenant | Upper C | Veteran combat/command package. |
| Crew captain | Lower/mid B | Field-leader package; seasoned history may raise it to upper B. |
| Small-crew founder | Upper D by default | Founder is ownership, not mastery; select practised/veteran/seasoned history separately. |

#### Experienced civilian backgrounds

Civilian occupation and experience must matter, but professional seniority alone does not equal combat seniority. Four JobSeek ranks provide progressive relevant contributions inside the current band. Crossing into C or B requires the corresponding accepted training/awakened-use history, selectable just as freely as criminal advanced starts.

| Civilian history | Confirmed target placement | Suitable interpretation |
| --- | --- | --- |
| First job / untrained newcomer | Lower D | Minimal combat exposure regardless of occupation. |
| Experienced practical worker or regular self-defence trainee | Middle-to-upper D | More conditioning, control or tactical awareness; no assumed elite combat training. |
| Senior professional with sustained martial/awakened practice | Lower C | Practised fighter who happens to work a civilian job. |
| Veteran civilian practitioner / former professional combatant | Upper C | Substantial accepted prior training, independent of current employment. |
| Experienced instructor or serious combat competitor | Lower/mid B | Field-leader-equivalent combat experience without faction membership. The history is supported combat background, not a newly implemented JobSeek profession. |
| Seasoned civilian expert with extensive combat/awakened history | Upper B | Same upper-B opportunity as a seasoned faction leader. |
| Exceptional civilian veteran | Low A | Freely selectable exceptional combat-history package, independent of employment or faction membership. |

A manager with no combat history stays in D with meaningful relevant gains over an equivalent novice, rather than automatically matching an elite guard. An unemployed former veteran can remain C/B without wages. Career changers retain established combat experience. For example, senior florist + regular self-defence is upper D, senior florist + practised awakened combat is lower C, and florist + seasoned combat-expert history can be upper B. The job adds its bounded contributions in each case; it does not replace the selected history.

#### Unawakened and specialist handling

Do not implement a single “unawakened = D” rule. Upper-D trained and C-tier veteran unawakened packages are valid calibration targets; evaluate an exceptional unawakened B proposal from actual skills/equipment rather than granting fake mana or blocking it solely for lacking Awakening. The highest reference packages assume capabilities sufficient for their target, not that all combinations can reach B by raising fight IQ alone. Preview any capability shortfall and explain the actual placement before acceptance. A tactical/support profile can have high fight IQ or refinement yet a lower direct-duel assessment; show that distinction rather than mislabelling it B in all circumstances.

Record overall target band separately from per-stat values and never force all stats into the same ordinal ranking. Balance checks must preserve meaningful improvements for each step of the same viable package and branch. Different branches, Traits and equipment may overlap or reverse specific matchups.

#### Calibration examples and acceptance

Compare newcomer/trained packages against ordinary guards, practised/veteran packages against individual elite personnel and mid-ranked arena fighters, and field/seasoned packages against multiple B references with distinct styles (including Emily, Minsu and Valentina). Test Exceptional Veteran directly against low-A contenders and enhanced Richter, with Rei as the stronger A benchmark; do not assume identical results across these matchups. Do not target identical win rates versus every named character. Test ordinary and prepared conditions separately and retain overwhelming apex gaps where required by MH-001. Verify all career ranks create visible stat contributions without exploiting combined backgrounds to exceed the selected package into main A or bypass authored progression. Show both experience step and calibrated combat assessment in Review, with numbers coming from MH-001's eventual shared scale.

### Civilian stat contributions

Civilian experience also contributes, with gains scaled to the relevance of the work rather than granting all managers field-leader combat power. Use four distinct increasing contribution levels for new hire / experienced / senior / manager, expressed in MH-001-calibrated values rather than fixed legacy-scale point bonuses. Distribute contributions using an authored relevance map, not a blanket increase to every stat. Physical/practical backgrounds can contribute martial skill; observational or supervisory work can contribute tactical judgement; explicit accepted awakened practice associated with the background can contribute power/refinement. Validate the mappings against what the stats actually mean. Profession, gender or MBTI alone never implies awakening or martial mastery.

Every supported career/rank combination must have a visible contribution or a clear explanation of the relevant recognised background needed; do not silently advertise combat bonuses that resolve to zero. Looking for work can retain approved prior-career/training experience without gaining employment or income. A purely descriptive unsupported profession can still pair with an explicit supported training/history choice.

Examples: a senior gardener with long-term physical training can start stronger physically than an otherwise equivalent novice; a manager with tactical training can have greater fight IQ; an awakened professional with years of accepted Trait practice can have higher refinement without criminal membership. A civilian can reach an experienced combat tier through confirmed training history rather than being forced into a criminal career.

### Resolve once, explain every contribution

Confirmed combat kits: [Starting Path stages, martial arts and learned moves](CUSTOM_STARTING_COMBAT_KITS.md) maps all seven experience tiers to approved Path stages, style slots and learned-technique allocations, with catalogue examples and the low-A Exceptional Veteran kit. Exact numeric thresholds and matchup validation remain under MH-001. The six Trait/package enhancements are now approved, including one reviewed origin signature for eligible Veteran-and-higher builds; signature intent controls, interaction explanations, supported non-combat uses and Trait change comparison are also confirmed.

Determine the strongest applicable combat-experience tier from current role and recognised prior training, then apply bounded, non-duplicated career/background adjustments. Do not sum complete tier profiles for job + faction + biography. Track the same underlying experience once; describe how career bonuses and branch emphasis are capped before implementation. Avoid reducing stats when adding a compatible stronger experience choice. Show tier baseline, each adjustment and final ratings in Combat, the options window and Review; the roster must show the same final starting profile.

Recognised prior experience is selected/confirmed through structured choices derived from the written background. AI expansion can suggest such a choice for review, but cannot silently award ratings by writing more impressive prose. Changing a career/background recalculates the preview and records a reversible edit; it never changes an existing playthrough. Locks on accepted narrative facts should flag contradictory preset changes for resolution rather than silently changing the biography.

Keep Path stage, known skills and rated competence coherent. Decide a compatible starting Path stage for each approved awakened-experience package during the balance pass; do not label a career rank as a Path stage or automatically grant Transcendence. Seed final ratings once without replaying historical stage-transition boosts. Explicitly map starting learned moves/styles, including any advanced/master eligibility reached by the strongest starting package under the new balance rules; stats alone do not grant every move, a unique canonical skill or an unrelated form. Preserve the existing reviewed custom Trait pipeline.

Acceptance: compare all adjacent tiers under the same branch, Trait and training assumptions; verify noticeable monotonic stat changes, no duplicate experience stacking, and preview/new-story equality. Check all civilian ranks, unawakened variants, retained prior experience, combined careers, highest-tier move eligibility and Path-stage consistency. Simulated representative encounters should confirm improved performance without promising guaranteed wins; document actual resource-cost, damage and progression effects. Existing saves retain current stats and are never reseeded on reload. No separate numeric creator curve is approved. Calibrate the final mappings alongside the MH-001 matchup matrix, using fixed seeds, both sides, comparable ability/form states and measured fight/resource outcomes. Social rank supplies recognised experience, not proof of superiority over every lore character.

### Simple options-selection window

Provide a dedicated dark, themed selection window opened by Choose background, Choose career or Choose criminal start in the creator. Reuse one consistent picker design with category tabs, search/filter controls, readable option cards and a detail preview. Use the existing embedded window/dialog wrappers and shared theme; all popup and interactive states remain dark.

For careers, choose a career card and then a clearly labelled experience level showing the actual job title. For criminal starts, choose a background/role, compatible organisation or branch where applicable, then rank. Narrative background has its own selection and editable text. Include Exceptional Veteran — low A in the experience selector for all compatible background categories, with no prior-playthrough lock. Show All / Standard / Advanced filters with All initially selected; Advanced is a descriptive badge, not a lock or separate game mode. Never require users to type internal IDs or rank numbers.

The detail panel explains the role, pay/hours or standing/access, responsibilities, starting benefits and remaining progression. Display unresolved draft choices clearly. Apply updates the creator draft only; Cancel/Escape preserves prior selections. On reopen, highlight the current choice. Changing category must not silently discard selections elsewhere. Incompatible combinations include a plain-language explanation and an explicit replacement choice. Include None / Looking for work where appropriate.

Support keyboard navigation, visible focus, scrolling and smaller windows. Test novice and advanced choices, every career/rank mapping, organisation compatibility, cancellation, restored drafts and all dark interactive states. Confirm an entirely new player can select every approved advanced start without any existing save or unlock data. Final review must match both the picker summary and actual new-story setup.

### Progression rules

Store recognised pre-story experience separately from completed in-story shifts, missions, projects, earnings and historical event logs. Promotion eligibility may combine validated origin experience and earned progress where appropriate, while next-tier requirements remain unmet at creation. Never fabricate completed quests or backdated wages to seed a senior rank. Audit every relevant promotion gate for this distinction, including gang standing, faction assignments and civilian qualifications/portfolio.

Preview and new-story setup use the same preset resolver. Persist preset ID/version and a resolved origin snapshot; applying it is once-only. Existing stories do not reapply changed balance, restore lost ranks or accrue starting money again. Preserve role identity and player-authored biography through draft, library and story round trips. Draft selection and AI expansion cannot apply actual employment or criminal state.

Funds, organisation budgets, assets, qualifications and exact standing values require a balance table during implementation. Keep personal money separate from operational budgets. No preset creates future victory flags, named NPC bonds or access outside its role. Verify combined civilian/criminal starts, former-member starts, job changes, invitations, promotion eligibility, expulsion and save reload.

## Suggested example builds

- Transferred florist: experienced Florist, no criminal role, private family history and a goal to open a shop someday.
- Night-shift bartender: Bartender plus independent operator, with work and criminal commitments respecting schedule conflicts.
- Numbers specialist: senior civilian role of choice plus Diamonds analyst; the biography describes prior numerical work without inventing an unsupported finance job.
- Returning former crew member: currently job-seeking with prior career experience and former underworld background, no active gang access.
- Established fighter: Clubs specialist plus separately selected combat training; criminal rank does not itself grant Awakening.

Evidence: inspected `job_apps.py`, `jobseek_progression.py` and `bubblegram_progression.py` on 2026-11-10. Rank names reflect existing catalogues. The user subsequently approved the backgrounds and starting ranks, free selection of advanced starts and an options window. The user additionally confirmed all hierarchy placements and the freely selectable low-A Exceptional Veteran option. Numeric balance remains pending under MH-001. No implementation or gameplay verification has been performed.
