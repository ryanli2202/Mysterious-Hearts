# MH-002: starting Path stages, martial arts and learned moves

Current status: implemented in MH-002 on 2026-11-10. [Final behaviour, numerical choices, tests and limits](CHARACTER_SELECTION_COMPLETION.md) supersede the planning-only implementation statements retained below.

Confirmed planned scope, 2026-11-10. Parent: [Starting backgrounds and confirmed combat placements](CUSTOM_STARTING_BACKGROUNDS.md). The seven combat placements and freely selectable low-A Exceptional Veteran are confirmed. The user has approved the Path stages, martial-art choices and learned-move allocations below. Implementation and balance verification remain pending. [MH-001](../COMBAT_WINDOW_UPDATE_PLAN.md#lore-based-balancing-and-character-power) owns future stat scaling and effective-strength calibration.

## Plugin task assignments

**Assigned:** 2026-11-11. Implemented under MH-002. Future requested maintenance only; final completion evidence still supersedes historical planning text.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Path-stage, martial-art and learned-move explanations | Story Skills + Writer's Loop | Preserve seven package tiers, actual move catalogues, learned-move caps and the distinction between Path stage and duel strength. |
| Preset application, save/load and boundary regressions | falsegreen-skill | Review independent expected-state assertions and invalid combinations; run affected custom-protagonist, creator, selection and combat tests, and inspect the dark picker states. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Confirmed starting packages

Stage column applies to awakened characters. Counts are maximum distinct starting selections, not arbitrary generated moves. A primary style represents the strongest training; secondary styles provide breadth. All characters receive the existing six utilities: Direct strike, Guard, Recover, Advance, Retreat and Take cover, independently of their learned martial techniques.

| Experience | Confirmed combat target | Starting awakened Path stage | Styles | Learned techniques beyond utilities |
| --- | --- | --- | --- | --- |
| Newcomer | Lower D | Awakening | No formal art by default | Utilities only; selecting regular formal training moves the experience choice to Trained explicitly. |
| Trained | Upper D | Awakening | 1 primary | All basic techniques in that art; no advanced or master moves. |
| Practised | Lower C | Ascension | 1 primary + 1 secondary | Basics in both; choose 2 advanced techniques in the primary art. |
| Veteran | Upper C | Ascension | 1 primary + 1 secondary | Basics in both; choose 4 advanced techniques across them and 1 master in the primary art. |
| Field leader | Lower/middle B | Totality | 1 primary + up to 2 secondary | Basics in selected arts; choose 6 advanced and 2 master techniques, masters in the primary art. |
| Seasoned field leader | Upper B | Totality | 1 primary + up to 2 secondary | Basics in selected arts; choose 8 advanced and 3 master techniques; masters may span primary and one qualified secondary art. |
| Exceptional Veteran | Low A | Totality | 1 primary + up to 3 secondary | Basics in selected arts; choose 10 advanced and 4 master techniques across primary and one qualified secondary art. |

These caps are starting allocations, not permanent limits on learning. Recommend a complete default kit for every package so players need not select every technique manually. Allow optional secondary styles to be omitted without silently converting unspent slots into stat bonuses. The primary art must have at least one learned advanced technique before assigning one of its masters; the same applies to a secondary art. Never select the same stable move ID twice. Martial-arts catalogues vary in size; retain their actual available techniques rather than inventing fillers.

Starting stage does not itself determine duel tier: two Totality characters can differ substantially in power, refinement, technique and experience. A master technique is not a Transcendence form. Veteran's single master is a learned technique supported by its calibrated training, not proof that the character has reached Totality. MH-001 must resolve package prerequisites consistently with the target strength, rather than preserving arbitrary old numerical gates.

## Unawakened, Trait and Path rules

- All unawakened variants remain in Dormancy, with no mana or active Trait effects. They keep relevant martial skill and fight IQ and all permitted basic/advanced allocations. They do not receive or execute the current catalogue's superhuman master moves; show these as unavailable with an explanation, not secretly learned.
- Unawakened experience is not automatically D. Calibrate trained and veteran martial packages on their actual capability. An unawakened variant of an exceptional package needs a separately viable low-A ruleset before it can claim that target; do not quietly downgrade an accepted low-A choice or fabricate awakening/equipment to meet it. Exceptional Veteran itself stays freely selectable; offer a supported low-A kit and clearly show which capability combinations have been validated.
- Awakened custom Traits use the existing explicit author/evaluate/review process. Only accepted amplifications are included, with their real compatible roles and costs. Higher experience increases calibrated potency/control and martial repertoire, not a free copy of canonical Traits.
- Veteran, Field leader, Seasoned field leader and Exceptional Veteran may select one reviewed custom starting signature from three candidates, provided they are awakened with an accepted custom Trait. This approved origin skill is additional to the martial allocations, not a replacement master move. Lower tiers begin with reviewed amplifications and learn unique skills through the existing in-story workshop. Unawakened/Trait-less variants do not receive a fabricated Trait signature. The supported one-skill selection and persistence rules are specified below.
- Totality is the highest approved starting Path stage for all approved packages, including low A. No automatic Transcendence, trump card, Conduit State, Nanoengine, Shinigami Protocol or canonical character signature.
- Initialise the selected stage directly as an origin fact. Never replay stage transitions to stack historical boosts or invent encounter counts, Trait uses, elapsed training months or past breakthroughs. The initial stage-entry clock starts with the story; no immediate retroactive breakthrough eligibility.
- Path advancement and learned-move progression remain independent: later play can add techniques and improve stats even when starting at Totality. Preserve latent-mana choices and established progression rules; unawakened does not promise eventual Awakening.

## Martial-art options and defaults

Use the current catalogue's 21 arts: Boxing, Taekwondo, Judo, Kyokushin, MMA, Muay Thai, Streetfighting, Sanda, Jeet Kune Do, Military CQC, Kickboxing, Silat, Aikido, Taido, Lethwei, Japanese Jujutsu, Wing Chun, Shinokami martial arts, Krav Maga, Systema and Kudo. These are not all automatically learned by a high-tier start. Combat analysis is a training discipline, not a selectable martial art with catalogue techniques.

Offer thematic defaults, freely editable within package compatibility and accepted training history:

| Background | Suggested primary | Suggested secondary choices |
| --- | --- | --- |
| Syndicate Clubs | Military CQC | Kyokushin, MMA, Judo |
| Syndicate Hearts | Kickboxing | Taekwondo, Taido, Boxing |
| Syndicate Diamonds | Aikido | Judo, Wing Chun, Boxing |
| Syndicate Spades | Silat | Krav Maga, Military CQC, Systema |
| Shinokami | Shinokami martial arts | Kyokushin, Japanese Jujutsu, Judo |
| Street crew / independent | Streetfighting | Boxing, MMA, Muay Thai |
| Civilian martial practitioner | Player choice | Complimentary arts within the same slot budget |
| Former service professional | Military CQC or Krav Maga | Boxing, Judo, Systema |

These are recommendations, not canonical mandatory training for every faction member. Shinokami martial arts outside an active Shinokami role requires an explicitly selected compatible prior training background, not a prior-playthrough unlock. Such history grants training only, not membership, secret identities or named NPC mentorship. Civilian employment never forces a fighting style. Keep the same choice depth for equivalent civilian and faction experience.

## Concrete catalogue examples

**Trained boxer, upper D:** Awakening if awakened, one art, all 14 existing Boxing basics (including Jab, Cross, Slip, Parry and Pivot), no advanced or masters. Unlike most arts, Boxing has 14 basics, 10 advanced and 8 masters; do not assume every school has 10/6/4.

**Practised operative, lower C:** Ascension, Military CQC primary and Judo secondary; all their basics; advanced Rush interception and Weapon-hand control. No master moves.

**Veteran Shinokami squad leader, upper C:** Ascension, Shinokami martial arts primary and Judo secondary. Advanced Rush suppression, Rhythm-break combination, False opening → counter, and Judo Counterthrow. Master Eclipse intercept. These examples use existing names; implementation stores their stable catalogue IDs.

**Field-leader Clubs kit, lower/mid B:** Totality, Military CQC primary, Judo and Boxing secondary. Advanced Rush interception, Weapon-hand control, Guard pass → pin, Frame → elbow → trip, Judo Counterthrow and Boxing Slip → cross. Masters Lockdown engine and Breach sequence. Higher potency/refinement and tactical competence distinguish this from a specialist; its rank does not grant unlimited stamina or guaranteed restraint.

**Exceptional Veteran, low-A example:** Totality; Military CQC primary, Judo, Boxing and Silat secondary. Ten advanced selections: all six CQC advanced moves, Judo Counterthrow and Hip throw → pin, Boxing Slip → cross, and Silat Low evasion → rising counter. Four master selections: CQC Breach sequence and Lockdown engine; Judo Zero-point reversal and Iron orbit. This is one recommended build, not compulsory equipment or style choices. Give the other faction styles and civilian routes equally complete valid alternatives. No unique canonical powers are included.

## Picker and state integration

The Combat step displays experience/target band, Path stage, learned style levels and a simple recommended kit. Edit techniques opens the same dark option-picker pattern with art/tier/role filters, descriptions, costs, selected counts and compatible Trait amplifications. Distinguish **Learned now**, **Eligible to learn later** and **Unavailable for this build**. Allow deliberate role coverage (attack, defence/counter, movement and control); utilities ensure a basic functional fallback.

Changing background recalculates the proposed package and highlights any styles/moves no longer covered. Keep the original draft until the player accepts the replacement; undo/history restores it. Preserve valid shared choices when upgrading a package rather than randomly selecting a new loadout. Preview, library snapshot and starting story must resolve the same move IDs and Path stage. No automatic teaching sessions, time charges or relationship creation occur during seeding.

## Required engineering work and checks

Current `combat_moves.initialise` automatically grants all eligible moves from rated arts on a fresh profile and adds all basics when an art is first registered. Custom tier allocations therefore require an explicit, versioned origin movebook path; simply setting high art ratings would overgrant advanced/master moves. Preserve canonical auto-seeding and legacy learned sets where intended. Future lessons must add moves normally without reapplying the starting allocation on every render or reload.

Current advanced/master gates use legacy martial-skill values 60/80, with Awakening required for masters. Replace or map the numeric gates through MH-001's future scale; do not copy those thresholds into the new creator. Validate primary/secondary mastery and resources against the resulting kit. Do not bypass eligibility checks just to make a UI count pass.

Acceptance: all seven recommended kits contain only valid catalogue IDs and the intended counts/roles; no duplicate or accidental all-moves grants; every learned move can execute under its required conditions; unawakened variants cannot use superhuman masters; Path initialisation gives no duplicate boost or fake history; pending AI Trait review cannot grant unaccepted aspects; upgrade/downgrade, undo, import, restart and legacy saves preserve the correct kit. Fixed-seed representative matchups under MH-001 must confirm the approved target bands, including low-A Exceptional Veteran below Rei and meaningful growth between adjacent packages. Inspect the creator picker and in-person execution of representative learned moves. Document actual evidence before release.

Evidence: inspected `combat_path.py`, `combat_profiles.py`, `combat_moves.py` and `combat_catalogue/martial.json`; enumerated current art counts and example move names. Catalogue inspection only; no balance simulations, runtime changes or gameplay tests performed.

## Combat-package and custom-Trait improvements — confirmed scope

Approved on 2026-11-10: all six improvements below are required scope. Practice and signature selection are optional player actions, not optional implementation. The starting signature explicitly extends the previously approved origin kit; ordinary martial allocations remain unchanged.

1. **Structured Trait builder and capability review.** Alongside free text, offer optional prompts for domain, intended effects, activation/setup, range, costs and limits. Present what the engine can execute separately from flavour text and unsupported requests. Show suggested corrections for impossible or contradictory effects without rewriting locked facts automatically. Existing reviewed amplification tags and compatible roles remain authoritative.
2. **Tier-aware Trait preview.** Evaluate the Trait concept independently of career rank, then display how MH-001-calibrated potency/refinement affect damage, resource costs, reach/control where supported and interactions with the selected martial moves. Keep the same Trait identity as the character grows; changing tier should not require regenerating its entire concept or unlock unrelated domains. Final performance must follow engine rules, not AI estimates.
3. **Starting signature skill for experienced packages.** Offer one reviewed custom signature for Veteran and above, chosen from three candidates grounded in accepted Trait aspects and the resolved package. Generate only on explicit request; show mechanics, costs, setup, limits and counters before acceptance. Players can skip selection. Keep one accepted slot even at low A; higher tiers improve its supported performance, not the number of free signatures. Lower tiers retain normal in-story learning. Preserve stable skill IDs/blueprints and once-only origin seeding; the signature is learned at story start without creating a fake workshop absorption event.
4. **Kit coverage and affordability review.** Summarise which learned techniques provide attack, defence/counter, movement and control; show compatible amplifications, actual costs and any unaffordable combinations. Recommend replacements or explain situational costs rather than silently substituting moves. Do not force every style to support every role or turn resource limitations into guaranteed combo outcomes.
5. **Optional practice preview.** Offer a clearly separate disposable training encounter to try the selected kit against a training target. Open actual combat in the in-person window, with no rewards, world-time changes, learning, cooldown consumption or persistent story damage. Use the real resolver and show limitations of a training-target comparison; this is different from the already approved non-canonical dialogue preview.
6. **Trait specialisation choices.** Offer reviewed expressions of the same Trait such as precision, defence, mobility or area control, only where its domain supports them. Show concrete advantages and costs; no universal menu of unrelated powers. A focused Trait can remain competitive with a versatile one through calibrated efficiency/control rather than awarding maximum breadth to every high-tier start.

Source evidence: `combat_workshop.py` currently evaluates 1–6 reviewed amplifications, uses bounded effect tags and compatible roles, and generates three unique-skill candidates through a separate saved learning process. Confirmed additions must extend those contracts deliberately rather than bypassing validation or making AI prose executable.

### Signature, specialisation and preview integration

Treat the signature as prior learning. Recommended initialisation: no creator-generated absorption cooldown; the ordinary first in-story absorption stays available, and each actual absorption then starts the existing 1,440 in-game-minute cooldown. Record the starting signature in a separate origin ledger plus the learned movebook to prevent duplicate learning. Import, recovery, rerolling or editing a reusable profile cannot add skills to an existing story. A new independent story receives its own approved origin skill once. Persist the signature in drafts, revisions, reusable profiles, story snapshots and portable exports, with import revalidation and no trusted external approval flags.

Changing Trait domains/aspects, specialisation, signature mechanics or incompatible package assumptions invalidates the affected acceptance. Pure tier-based stat growth uses the accepted blueprint and shared scaling; it must not generate a new named skill on every stat increase. A downgrade below Veteran parks the candidate as an unused draft idea, never an active learned skill; restoring it requires valid current review. Renaming alone cannot bypass duplicate checks. Preview/loadout actions must use the actual stored, validated blueprint rather than executing generated prose.

Store specialisation as structured, reviewed choices with supported modifiers and costs, not free-form text that silently changes combat. Show compatibility between every accepted amplification and selected move. Supported range, area, resource efficiency or control changes must correspond to implemented effects and preserve the approved combat target; flag unsupported claims for editing. Keep core Trait identity and locked facts stable during all reviews.

Run practice in an isolated temporary combat state in the in-person window. It must not use live-save mutation helpers, update the active story or grant encounter credit, skill absorption, cooldown changes, resources, relationships or knowledge. Keep practice logs separate and disposable. If no story exists, build a sandbox encounter from the reviewed creator snapshot rather than starting a hidden real story. Changed creator data invalidates the practice snapshot. Clearly label target tier and restraint; a training target is not proof of winning a lore matchup.

Acceptance checks: exactly three valid signature candidates and at most one learned origin signature; only Veteran-or-higher accepted custom-Trait builds are eligible; skipping works; same origin cannot seed twice; lower-tier/imported/stale results cannot bypass validation; normal in-story cooldown behaviour remains intact; tier-aware costs/effects match the engine; all specialisations stay within approved domains; practice leaves all real story and workshop state unchanged. Confirmed package bands must still pass MH-001 matchup checks with and without the optional signature.

## Additional custom-Trait features — confirmed scope

Approved on 2026-11-10: all four additions below are required MH-002 scope. Implementation and verification remain pending.

- **Signature intent controls:** let players request a preferred role (counter, defence, mobility, attack or setup) and visual theme before generating the three candidates. Show supported roles from accepted aspects, explain unsupported choices and preserve the request through retries. The validator must check role/domain compatibility, not merely accept the AI's label. Visual theme changes presentation only, never damage types or capabilities. Include intent in the request snapshot so edits invalidate stale candidates; keep the existing one accepted starting-signature slot and eligibility rules.
- **Explain a Trait interaction:** provide an expandable comparison of a selected move with and without its amplification: compatibility reason, affected properties, resource costs after refinement, setup and supported environmental interactions. Read values from the same resolver as actual execution; do not use AI estimates as authoritative numbers. Clearly distinguish fixed changes from situational or probabilistic outcomes. Available from the creator kit review and relevant gameplay move inspection, respecting dark phone surfaces where applicable.
- **Non-combat Trait uses:** implement explicitly authored applications in supported work and exploration contexts, with real costs, prerequisites and consequences. Use a capability/action registry tied to accepted Trait aspects and existing activity handlers. Define each action's valid context, target, range, resource/time costs, outcome bounds and any witness/disclosure effects. Provide reviewed integrations in both work and exploration; examples to assess include compatible precision/control assistance on a work task and perception assistance in an exploration check. Final actions must fit the actual Trait and activity systems. AI descriptions alone cannot unlock actions, reveal secret facts, complete entire quests, award promotions or bypass physical access. Execute in-person actions in the in-person window. Creator previews describe possible uses without running them; ordinary play applies costs and outcomes once through the activity resolver, with save/reload and cancellation protection. Explicitly label unsupported domains/contexts rather than silently promising universal usefulness.
- **Trait change comparison:** before replacing an aspect or specialisation, show old/new supported mechanics, costs, compatible moves, non-combat applications and any signature/skill acceptance invalidated by the edit. Offer Apply or Cancel; applying creates a reversible draft revision and invalidates only genuinely affected review records. Accepted identities, locks and unrelated work remain intact. This operates on draft/reusable-character editing; ongoing story snapshots and learned skills are unchanged. A future in-story respec system is not implied.

Acceptance: intent-selected candidates comply with their requested supported roles and accepted aspects; stale requests cannot replace newer choices; cosmetic themes add no mechanics; explained move changes match actual resolver results under representative stats and conditions. Work and exploration tests cover supported/unsupported aspects, insufficient resources, access restrictions, once-only outcomes, witness knowledge and save/reload. Trait comparisons identify all affected combat and non-combat capabilities, preserve unrelated approvals and cancel without mutation. Inspect all new controls and interaction states in the required dark theme; no actual in-person action runs in a phone or creator preview.
