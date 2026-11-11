# MH-002: RPG main menu and character selection

Status: **Released**. Added: **2026-11-10**. Parent: [Roadmap](../ROADMAP.md#mh-002-rpg-main-menu-and-character-selection).

Implementation completed 2026-11-10; see [completion evidence and verification limits](CHARACTER_SELECTION_COMPLETION.md). Earlier planning/implementation statements below are retained as scope and historical evidence. This document retains the full requested major-update scope. Release date: 2026-11-10; no game version number is assigned. The confirmed core is an RPG-style main menu, selectable character dossiers, integrated custom creation and the supporting editing, recovery, identity and portability features specified below. Layout and interaction choices below are the recommended design; optional extensions are explicitly separated.

## Plugin task assignments

**Assigned:** 2026-11-11. MH-002 is Released; assignments apply only to requested maintenance or future extensions.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Dossiers, public/private biography and custom background wording | Story Skills + Writer's Loop | Preserve identity-specific facts, knowledge boundaries and established starts; route substantive appearance changes through MH-013. |
| Needed local icons/frame assets or user-supplied portrait cutouts | prompt-to-asset; Bulk BG Remove only for requested isolation | Validate/export compatible local assets; retain dark panels, height fitting, missing-art recovery and original user files. |
| Selection, drafts, recovery, portability and starting-state changes | falsegreen-skill | Review tests for actual profile/story independence, duplicate identities, failed-start retention, history restore and private data boundaries; run creator/selection/save suites plus UI smokes. |
| Starting background and combat package changes | Story Skills + falsegreen-skill | Follow the two linked custom-start specifications and MH-001 balance contracts; verify permitted roles, learned-move caps and unaffected canonical starts. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Experience and visual direction

Make choosing a protagonist feel like choosing whose life to inhabit. Combine a cinematic Winterfield backdrop, large character artwork, restrained gold framing, dark slate panels and each character's accent colour. Keep the social/life-simulation identity alongside combat information; an unawakened character should feel like a complete choice.

Use three main areas on a wide window:

| Area | Contents |
| --- | --- |
| Left navigation | Continue, New Story, Story Library, character creation/library, gallery, patch notes and settings/account/audio access |
| Centre stage | Selected character artwork, full name, epithet and short story hook; a portrait roster along the bottom |
| Right dossier | Overview, Backstory, Details and Awakened tabs; persistent Begin as [name] action |

The initial menu prioritises Continue when a readable save exists and New Story otherwise. New Story opens the roster without creating a save. Selecting a portrait updates the stage and dossier only. Begin starts the selected protagonist through the existing start flow, preserving its save-protection behaviour. Continue always resumes the intended save, independently of the roster selection.

For smaller windows, use a compact navigation strip and place the dossier below or alongside a smaller portrait, with scrolling inside the content area. Keep the selected name and Begin action visible. Choose breakpoints after inspecting the game's supported window sizes and Windows scaling; do not shrink text until it is unreadable.

## Character dossier

Confirmed follow-up (2026-11-10): all canonical playable characters need two-paragraph biographies grounded in their lore/story. Details must reuse established age, occupation, birthday, height and MBTI rather than blanket placeholders, and include Garrett's triad leadership, Rei's underground championship and Ivan's Syndicate executive role alongside their public work. These owner-facing details do not disclose secrets to NPCs. Unestablished dates/measurements remain honestly unknown; newly authored MBTI interpretations are labelled. Implemented scope and checks are in [the follow-up evidence](CHARACTER_SELECTION_IMPLEMENTATION.md#biography-details-and-revision-follow-up--2026-11-10).

Further confirmed correction (2026-11-10): include the Four Aces' Syndicate status in their occupation panels alongside civilian work. They serve the Cardmaster directly as Ace specialists; their titles do not imply Suit command or disclose their identities to NPCs. Implemented with the [staged creator/profile follow-up](CHARACTER_SELECTION_IMPLEMENTATION.md#staged-creator-profile-editing-and-saved-previews--2026-11-10).

| Tab | Recommended contents and boundaries |
| --- | --- |
| Overview | Name, portrait, epithet, short introduction, interests, broad playstyle and starting-life summary. Describe opportunities rather than promising exclusive campaigns that do not exist. |
| Backstory | Authored opening biography and relevant background, with a short default summary and expandable sections. Public/setup information is visible; hidden identities, future events and another character's secrets remain protected. |
| Details | Authored age, birthday, height, occupation/studies, personality, hobbies and known affiliations where supported. Show starting home, funds and work from actual start configuration where available; distinguish gameplay balance from canonical biography. Missing facts remain unspecified. |
| Awakened | Actual starting awakened state and Path stage, Trait name and bounded description, martial arts, available skills/forms and four labelled ratings: awakened power, Trait refinement, martial skill and fight IQ. Explain resource costs and limitations. Awakened without a named Trait and unawakened are valid, distinct states. |

Keep stat bars accompanied by readable numbers and explanations. Do not turn combat ratings into overall character quality or fabricate difficulty rankings. Use concise ability descriptions with expandable detail so long custom Traits remain usable.

Label the new-story preview **Starting profile**. Any saved-story preview belongs to a specifically selected save and is labelled **Saved progress** with the character and save identity. Never borrow progression from one save to decorate another character's starting preview.

The Path integration should distinguish current stage, earned abilities and future progression. Unavailable forms cannot appear equipped or usable. A possible future awakening is neither a starting power nor a guaranteed unlock. Do not imply that conversation or romance unlocks awakening or that every character can reach Transcendence.

## Roster and custom characters

- Use portrait tiles with full-name labels, a clear selection outline and keyboard focus. Retain every currently playable character and stable character ID; this update does not make excluded NPCs playable.
- Approved scope clarification (2026-11-10): completed characters made with the existing custom character creation system appear directly in the main character-selection roster alongside the canonical cast. Include previously saved profiles, not just characters created after this update. They must not require opening a separate Saved characters dialog to select or preview them.
- Provide name search and All / Canonical / My Characters filters, with All as the initial view. Mark custom entries with a small Custom badge. Preserve the current selection across dossier tabs; when a filter hides it, clearly retain or clear selection rather than showing a mismatched portrait and Begin action. Empty search results and an empty custom library need clear recovery actions.
- Saved custom characters receive the same dossier treatment using their stored biography, details, portrait and accepted Trait information. Selecting one must not regenerate artwork, evaluate a Trait, spend credits or start a playthrough.
- Keep Create your own accessible and return to the appropriate roster entry after successful creation. Distinguish reusable character profiles from saved stories: a profile begins a new playthrough; a story save resumes one.
- Refresh the roster after the creator successfully saves a reusable profile; cancellation adds nothing. Final Review offers Save character (return to the selected roster entry) and Save & begin (explicitly save, then start through existing save-protection checks). If starting fails, retain the successfully saved reusable profile. Neither autosave nor Save draft starts a story. Preserve profiles after story-save deletion and across app restarts. Duplicate names must remain distinct choices, using stable profile identity and a useful secondary label rather than name-based deduplication.
- Missing artwork uses a styled silhouette or initials. Invalid custom profiles and unreadable saves show an inline explanation and preserve access to library/recovery controls.

## Data integration and correctness

### Integrated character creation: expanded scope

Requested on 2026-11-10: MH-002 also improves character creation with combat, JobSeek, Bubblegram and backstory integration. These areas and the linked background/rank catalogue are committed scope; numeric starting balance remains design work; Path/style/move allocations are confirmed. Retain the existing selection and Emily scope.

Recommended flow: **Identity & Appearance → Backstory → Combat → Career → Underworld → Review**. Provide defaults and optional advanced sections, with a live dossier preview matching character selection. Back/Next preserves inputs; errors identify the relevant field. Separate saving a completed reusable character from explicitly beginning a story.

| System | Recommended integration | Starting-state rules |
| --- | --- | --- |
| Combat | Awakened/unawakened choice, supported martial arts and training background, reviewed Trait/amplifications, ratings, available moves and resource limits. | Resolve starting combat stats from recognised career/backstory/training experience using the progressive starting packages and MH-001 balance scale; assign compatible Path stages explicitly. Distinguish granted moves from future training. Free-written power claims do not grant mechanics. |
| JobSeek | Choose looking for work, a career interest or a supported starting job; preview workplace, entry role, hours and pay. Retain descriptive occupation for unsupported professions. | A supported starting job seeds real employment once when creating a story. An interest only guides suggestions. Label descriptive occupation separately from mechanical employment. Advanced ranks and certificates require explicit starting rules. |
| Bubblegram | Alias, private underworld history, criminal career direction and selectable established criminal backgrounds; preview actual starting standing and opportunities. | Support both newcomer and established starts. Approved background presets seed real reputation, applicable membership/rank, heat, access and obligations once. The linked background catalogue defines approved presets/ranks; numeric values need balance design; free text alone does not grant authority or completed contracts. |
| Backstory | Hometown, prior work/training, reason for moving, formative events, motivations, goals and optional private history, plus free-written biography. | Feed accepted facts into the dossier and relevant dialogue context. Separate past facts, present state and aspirations. Do not automatically create local acquaintances, romances, NPC memories or completed quests. |

Replace the fixed newcomer biography with a builder that incorporates authored history, retaining newcomer/no-local-ties as the default. Separate public biography from private history: public profiles must not publish secrets, and NPC knowledge follows existing disclosure rules. Do not infer history or behaviour from gender or MBTI. Flag conflicting choices with editable explanations without discarding text. “Join the Syndicate” is a goal, not current membership. Civilian career progression remains independent of crime, and reserved canonical faction roles remain reserved unless explicitly scoped otherwise.

The final Review page shows identity and biography, home and funds, actual employment, awakened state and Path stage, available moves and Trait limits, public/private information and actual affiliations versus interests. Every choice should clearly indicate whether it changes gameplay, adds descriptive history or sets a future goal. Career/backstory experience now affects starting power, Trait refinement, martial skill and fight IQ through multiple noticeable steps. Show each source contribution and final stats, avoid counting the same experience twice, and keep awakened/learned-skill eligibility explicit. Use the [progressive starting-power specification](CUSTOM_STARTING_BACKGROUNDS.md#progressive-starting-combat-power-confirmed-scope) and [MH-001 balance authority](../COMBAT_WINDOW_UPDATE_PLAN.md#lore-based-balancing-and-character-power); do not implement a competing legacy-scale curve.

#### Confirmed creator features (2026-11-10)

Confirmed follow-up: [Custom career and criminal starting backgrounds](CUSTOM_STARTING_BACKGROUNDS.md) defines the approved narrative backgrounds, JobSeek ranks 0–3 and established crew/faction starting ranks. Advanced starts are freely selectable. A dedicated dark options window provides cards, category filters, rank selection and effect previews with Apply/Cancel. Numeric balance remains to be finalised.

Confirmed hierarchy follow-up (2026-11-10): the catalogue defines seven starting-experience placements: lower D → upper D → lower C → upper C → lower/mid B → upper B → low A. The user approved the Syndicate, Shinokami, street-crew and experienced-civilian mappings and Exceptional Veteran — low A as freely selectable without unlocks. Exceptional experience can accompany civilian, independent or faction roles without granting higher organisational rank, arena titles or canonical powers. Exact stats and matchup verification remain pending under MH-001; low-A customs remain below Rei under comparable conditions.

The user explicitly added draft saving, meaningful career choices, backstory-aware dialogue, established Bubblegram criminal backgrounds and AI expansion of player-written text. These are required MH-002 scope, not optional suggestions.

**Draft saving.** Provide Save draft and Resume draft, supporting incomplete fields independently of final playable-profile validation. Persist the current step, text, selections, portrait references and accepted Trait-review data with its input signature. Drafts survive restart and appear in a clearly labelled draft list, not as playable characters. Resuming never automatically starts generation or re-evaluation; changed inputs invalidate only affected approvals. Use atomic writes, recoverable errors and versioned defaults. Keep the last saved draft if a save fails, and warn before discarding unsaved edits. Completing a draft creates or updates its intended reusable profile without duplicate roster entries.

**Meaningful career choices.** Supported job choices establish actual JobSeek employment with the displayed workplace, role, pay, schedule and available work actions. Looking for work remains a valid start; a career interest points toward relevant listings. Descriptive occupation stays available for professions without implemented work. Any experienced-career presets must define the rank, skills and qualifications they grant explicitly. Show material consequences in Review and initialise employment exactly once; changing a creator profile never changes an existing story's job. Include career facts in suitable dialogue without implying coworkers already know the protagonist.

**Backstory-aware dialogue.** Persist an accepted structured background and biography as story-owned facts. Use relevant past work, hometown, motivations and disclosed history in dialogue and memory context rather than falling back to a generic newcomer description. Keep private facts separate from what each NPC knows; awareness must follow existing disclosure or explicit starting-role knowledge. Preserve distinctions between lived history, current commitments and aspirations. Later playthrough facts take precedence over stale starting descriptions, and backstory never dictates the player's present emotions or actions. Test public discussion, private secrets, subsequent disclosures, changed jobs and conflicting goals across save/reload.

**Established Bubblegram backgrounds.** Custom characters can begin with a real established criminal position, not merely a written aspiration. Design supported presets covering meaningful differences in experience and affiliation; candidate concepts include an independent operator, an established crew member and an experienced faction operative. The linked background catalogue now defines the approved choices and starting ranks; advanced options require no prior unlocks. Define each preset's reputation, heat, affiliation/rank, accessible work and locations, obligations, and any starting resources. Expose these effects before acceptance. Preserve canonical reserved roles and distinguish professional recognition from personal friendship or secret knowledge. Seed only the selected starting role; bypass newcomer onboarding only where that role warrants it. Avoid replaying invitation, trial or reward logic to manufacture fake completed missions. Make later progression and loss of standing work normally. Keep civilian employment and criminal role separate, and verify compatibility if both are selected. Canonical-only role registries must not be globally overwritten to implement custom roles.

**AI Expand / Rewrite / Format.** Add an explicit text-assistance action beside suitable free-text creator fields, including biography, formative history, motivations, appearance and Trait description. Let the player choose expansion, rewriting or formatting and optionally provide tone/length guidance. Preserve original meaning, names and accepted character facts while elaborating the writing. Formatting mode changes presentation without adding facts. Expansion may propose new narrative detail, clearly presented for review, but cannot silently change structured identity, grant powers or ranks, invent ties to canonical characters or convert goals into accomplishments.

Show the original and suggested text with Apply, edit, retry and discard controls; keep undo available after applying. Generated content remains a proposal until accepted. A request uses a snapshot of its target field and relevant creator context: if the player edits or switches drafts before completion, never overwrite newer text or apply the response to another character. Handle cancellation, unavailable AI, failure and overlength output inline while preserving the player's writing. Only explicit requests invoke the configured AI provider; browsing, typing and resuming drafts do not. Manual creation and draft saving remain usable when AI is unavailable. Applying a changed Trait description invalidates its earlier mechanical review and requires the existing evaluation/acceptance flow; expanding appearance only marks an existing portrait as potentially out of date, never silently regenerates it. No additional AI provider or credential changes are authorised by this planning entry.

#### Locked facts and draft revision history: confirmed scope

Approved on 2026-11-10; these replace the earlier optional suggestions.

**Locked facts for AI text assistance.** Let players pin structured facts and selected narrative facts that AI expansion/rewrite must preserve, such as name, age, hometown, key events, motivations, ability limits and chosen career. Display the active locks before requesting assistance. Distinguish exact wording locks from facts whose wording may be polished without changing meaning. Persist locks with the draft and include them in the request snapshot. AI-generated text cannot edit structured fields or remove locks. Tone preferences guide style but do not override pinned facts.

Keep generated output in the review area until accepted. Check exact locks and structured contradictions before application, and highlight potential narrative conflicts for correction rather than claiming semantic checks are infallible. Reject application of a known conflicting suggestion until corrected or until the player explicitly changes the relevant lock. A changed lock or source field while a request is running makes its response stale. Unlocking/editing is an explicit player action; expansion never does it automatically. Allow acceptance of useful edits without the conflicting passages. Manual writing and drafting work without AI.

**Draft revision history.** Store persistent, timestamped revisions with understandable labels: manual save, before AI apply, before preset replacement and before restore. Include creator text, structured choices, locked facts, selected assets and Trait-review signatures in each snapshot. Keep history per stable draft ID so duplicate names cannot mix records. Avoid a revision for every keystroke; use meaningful checkpoints, deduplicate unchanged snapshots and define bounded retention without silently removing named/pinned checkpoints.

Provide a dark revision browser with preview, change comparison and Restore. Restoration creates a new current revision and preserves the state being replaced, so restoring is reversible. It affects the draft only, never existing stories or a published reusable profile without a separate explicit save. Do not duplicate portrait assets per revision; preserve referenced files or clearly report missing assets. Revalidate restored schema, field choices and Trait-review signatures under current rules; do not revive obsolete approval or automatically run paid generation. Treat in-flight AI responses as stale after restoration. Preserve the last valid history on interrupted or failed writes and make errors recoverable.

Acceptance checks: locks persist across restart and restore; exact locked wording is preserved; changed locks invalidate pending responses; conflicts remain reviewable without losing original text; restores are reversible; history stays isolated between drafts; missing artwork and old schemas are handled; restored Traits require current valid approval; no history action changes existing playthroughs or invokes AI automatically.

#### Persistence implementation

Source inspection found that `custom_protagonist.validate` whitelists profile fields, `background` hard-codes a newcomer and `install` supplies an empty career list. The creator already supports portrait generation and reviewed Trait amplifications. Employment and criminal state live in `job_apps.py`, with separate rules in `jobseek_progression.py`, `bubblegram_progression.py` and `bubblegram_roles.py`. Extend these data contracts rather than adding UI fields that disappear on validation/reload.

Add optional, versioned profile fields with legacy defaults. Preserve stable profile identity independently of edits, accounting for current content-hash library filenames. New stories receive their own profile snapshots; changing a reusable character must not rewrite an ongoing playthrough.

Resolve starting choices through one validated creation path, seeding each system once. Preview uses isolated data from the same rules. Loading an existing story cannot reapply presets, duplicate funds, overwrite employment, reset heat or replace earned progression. Unsupported choices need a clear explanation rather than silent deletion.

Keep portrait generation and Trait review explicit. Career or biography edits should not regenerate portraits; changed Trait inputs invalidate only the affected review. Preserve accepted work through recoverable failures. Creator surfaces, popup listboxes and all interactive states remain dark using shared themes and embedded dialogs. Training, work and criminal operations take place in the in-person window.

#### Creator acceptance checks

- Fresh awakened, unawakened, job-seeking and supported employed characters match the reviewed starting state.
- Established criminal presets produce the reviewed Bubblegram standing, access and obligations, progress correctly and do not replay newcomer trials or duplicate resources on load.
- Incomplete drafts survive restart with text and valid accepted assets intact; failed saves preserve the previous draft; completion creates the intended single profile.
- AI text edits require acceptance, preserve originals/undo and cannot overwrite newer edits or another draft; failures and cancellation leave manual creation usable. Formatting adds no facts, and changed Trait text invalidates prior review.
- Backstory, privacy distinctions, career choices and accepted abilities survive validation, library save, story creation and reload.
- Free-written biography cannot bypass the approved starting rules for skills, wages, faction authority or accomplishments.
- Public displays and NPC knowledge respect private history; aspirations are not remembered as completed events.
- Old custom profiles load; profile edits leave existing stories intact; multiple stories do not share progression.
- Repeated loads never duplicate setup rewards or reapply starting employment/affiliations. Cancellation and preview do not mutate gameplay.
- Run relevant custom creator/library/protagonist, combat, JobSeek and Bubblegram checks, plus `tests/phone_dark_theme_smoke.py` and rendered inspection of every new creator step and interactive/error state. Record actual checks during implementation.

#### Creator convenience features: confirmed scope

- **Autosave recovery:** save a debounced working copy per draft, including incomplete text and current selections, with Saving / Saved / Unsaved changes / Save failed status. Keep explicit saves and meaningful revisions distinct from autosave. Use atomic writes and recover the last valid copy after interruption; offer a recovery preview rather than silently replacing a newer manual revision. Restoring or explicitly discarding a draft must not resurrect superseded autosaves. Never save secrets from provider configuration or trigger AI on recovery.
- **Optional writing prompts:** provide skippable, editable questions for history, hometown, motivations and formative events. Offer prompts relevant to selected backgrounds without assuming answers. Unanswered prompts do not block completion and are not character facts. Answers enter only their intended fields; AI expansion remains an explicit action.
- **Section completion checklist:** show each creator section's required omissions, validation problems and optional additions separately. Link each issue to its control and preserve the current draft when navigating. Derive readiness from the same validation used at final creation, including valid Trait review and assets. A skipped optional backstory answer must not appear as an error.
- **Selective randomisation:** let players choose which supported fields to randomise, preview the changes and explicitly apply or discard them. Preserve pinned facts and all unselected fields. Use valid local option pools for ordinary randomisation; prose generation, portrait generation and AI evaluation remain separate explicit actions. Respect compatible job/role combinations and accepted starting ranges; if no compatible result exists, explain without changing anything. Changed Trait inputs invalidate the relevant review. Applying a result records a reversible revision and never alters a live story.
- **Inspiration bookmarks:** save alternative AI passages or player-written ideas with a label and source field in a separate per-draft ideas collection. Support edit, remove, preview and explicit insertion with revision/undo. Ideas are excluded from accepted biography, gameplay setup and dialogue/memory context until deliberately applied. Applied ideas pass the normal field validation, lock and Trait-review rules; applying one does not erase the saved idea automatically. Preserve bookmarks across restart and keep them isolated between drafts.

Acceptance: test interrupted/failed autosaves and recovery conflicts; optional prompt skipping; checklist navigation and agreement with final validation; locked/unselected fields surviving randomisation; incompatible option handling; undo after application; bookmarks persisting without leaking into dialogue; all states rendered dark with keyboard access. No implementation or runtime verification has occurred yet.

#### Portability, dialogue preview and help: confirmed scope

Approved on 2026-11-10: all three features below are required MH-002 scope.

**Character export/import.** Export a versioned portable package containing the accepted profile and portrait assets, with a preview of included content and explicit controls for private biography. Exclude provider credentials, story saves, draft revisions, unused inspiration and preview conversations. Imports show character identity, source format, included assets and compatibility problems before acceptance. Validate schema, file sizes and asset types; reject unsafe paths, executable content and malformed packages without changing the library. Import as a separate character by default; never overwrite a same-name profile or existing story automatically. Provide explicit duplicate/conflict handling and retain provenance without trusting imported approval flags. Revalidate starting presets and Trait data under current rules, requiring a fresh review where existing approval cannot be verified. Missing assets or unsupported versions need an actionable explanation. Exporting never edits the source profile or publishes anything externally.

**Dialogue preview.** Offer a short, explicitly non-canonical conversation based on the accepted or currently reviewed creator snapshot. Use a neutral sample interlocutor with a defined knowledge scope; public facts may inform their responses, while private history stays undisclosed unless shared within this sample. The player writes their own replies. Display which background version the sample uses and make restart/clear available after edits. Invoke AI only through explicit preview actions and handle cancellation/provider errors without losing the draft. Keep sample messages in isolated preview state, excluded from world time, story saves, relationship scores, quest flags, phone messages, character memory and future dialogue retrieval. Label the sample as illustrative rather than a guarantee of exact future responses. Only explicit copying into a creator field can turn suggested prose into accepted character content, with normal locks, validation and revision handling.

**Field explanations and examples.** Add concise inline help and expandable examples beside complex fields, particularly Trait costs/limits, Path stage, job experience, criminal reputation versus rank, and public/private backstory. Derive numeric effects and available choices from the same rules used by the picker. Keep examples clearly labelled, optional and separate from saved facts unless deliberately inserted. Explain unfamiliar terms in plain language and support keyboard access and text scaling. Use dark embedded help surfaces, including hover/focus and empty/error states.

Acceptance: export/import round trips preserve intended fields and artwork; private-content controls are honoured; duplicate names, corrupt/oversized packages, unsafe paths, missing assets and old versions cannot damage existing profiles or saves. Imported approval is checked rather than trusted. Dialogue previews respect knowledge boundaries and leave all gameplay/memory state unchanged, including after cancellation and restart. Help matches actual preset effects, is accessible without a mouse and never silently inserts examples. Required runtime and rendered checks remain pending implementation.

#### Editing, identity and usability: confirmed scope

Approved on 2026-11-10: all four refinements are required.

- **Session undo/redo:** group ordinary typing into useful undo steps and treat applied presets, AI edits and randomisation as single reversible operations. Revalidate affected fields/assets/Traits and invalidate pending responses after undo/redo. Do not undo external AI jobs, charge refunds or gameplay actions. A new edit after undo clears the redo branch; persistent revisions preserve major checkpoints separately.
- **Preferred address and pronunciation:** optional preferred name, nickname and pronunciation guidance, with canonical name as a safe default for old profiles. Use guidance in appropriate dialogue/presentation; no new speech engine is implied. These fields participate in locks, revisions, import/export and story snapshots. NPC familiarity still determines whether an intimate nickname is appropriate.
- **Identity visibility:** distinguish creator-facing identity, public/preferred name and underworld alias. Configure which identity is public and which contexts or known disclosures allow a private identity. Use one knowledge resolver for dialogue, Bubblegram labels, public profiles and preview conversations. Faction rank can grant role recognition, not automatic legal-name/alias linkage. Players can inspect their own complete profile in the creator/dossier, while public surfaces and NPC context receive only permitted facts. Exports preview included private identities and preserve visibility metadata; imported text cannot establish another NPC's knowledge.
- **Creator usability pass:** review blank/newcomer, advanced civilian-plus-criminal, restored draft, legacy profile and long imported biography flows. Keep optional/advanced content collapsed initially but reachable, and preserve free access to every approved advanced start. Check keyboard-only use, text scaling, small windows, long names, field errors and focus restoration from option/history windows. Verify that simple creation does not require filling optional histories, using AI text tools or opening every section.

Acceptance: ordinary edits and grouped operations undo/redo correctly; all restore paths invalidate stale asynchronous responses; aliases and preferred-address rules survive restart/import; undisclosed identity links remain absent from NPC/public context; completed usability scenarios have rendered evidence. Undo/history/recovery never change active playthroughs.

#### Earlier optional suggestions

- **Choice impact summary:** show what changed in starting employment, access and responsibilities when switching a preset, before applying it.
- **Starting character sheet:** offer a readable final sheet containing identity, biography, career, criminal role and combat profile for review.
- **Explain remaining progression:** show the next available career or faction milestone for an advanced start, so players know what remains to work toward.


- **Quick Start and Advanced creation:** editable templates using the same visible starting rules as manual creation.
- **Personal goals and journal prompts:** carry chosen ambitions into the opening journal with relevant existing activities, without fabricating quests or rewards.
- **Backstory timeline:** organise formative events and flag age/order conflicts without inventing dates or relationships.
- **Optional arrival prologue:** reflect the accepted background in a skippable in-person scene; skipping never loses resources or applies setup twice.

### Selection preview data

Combat-kit design follow-up: [Starting Path stages, martial arts and learned moves](CUSTOM_STARTING_COMBAT_KITS.md) records the approved Awakening/Ascension/Totality origin stages and progressively broader style and learned-technique selections, thematic editable defaults and a full low-A Exceptional Veteran example. The shared resolver must seed exactly the selected movebook rather than accidentally granting every eligible catalogue move. The user approved these allocations; implementation and MH-001 calibration remain pending. All six subsequent Trait/package enhancements are now confirmed: structured Trait builder, tier-aware preview, specialisation, one reviewed starting signature for eligible Veteran-and-higher characters, kit review and isolated in-person practice. The four further custom-Trait features are also confirmed: signature intent controls, interaction explanations, authored non-combat uses in work/exploration and Trait change comparison. Details and acceptance checks are in the linked combat-kit plan.

`start_ui.py` currently provides a cinematic preview, four-name roster pages and separate Begin/Continue actions. Its preview primarily contains an epithet, mood and interests. Extend or extract that presentation rather than creating a second roster with divergent IDs.

Create a read-only preview adapter with explicit inputs for canonical starting profiles, reusable custom profiles and saved-story snapshots. Use authoritative start/profile data and a small authored presentation layer for summaries, display order and spoiler visibility. Keep provenance for authored facts so contradictions can be audited.

Candidate sources to reconcile during implementation:

- `game_core.py`, `playable_cast.py` and character reference documents for roster identity and starting life.
- `contact_profiles.py`, character lore modules and references for backstory and personal facts, respecting disclosure boundaries. Do not expose raw internal lore or dynamically learned personal details in a fresh-story preview.
- `combat_profiles.py`, `combat_path.py` and `combat_moves.py` for actual combat capability, Path stage and moves.
- `custom_protagonist.py`, `custom_library.py` and `custom_creator_ui.py` for reusable custom character data and accepted Traits.
- Existing save-library code for validated save identity and summaries.

Approved scope decision (2026-11-10): Emily starts awakened, with matching lore, as part of MH-002. `vendetta_lore.py` currently describes Critical Hit as only a future possibility, while `combat_profiles.py` already supplies awakened ratings and Critical Hit, and `combat_path.py` seeds Ascension. Update her lore to agree with her starting abilities rather than removing those abilities.

### Emily: starting awakened abilities and lore

- Establish Critical Hit as an active starting Trait: creating weak points and suppressing pain. Pain suppression does not prevent injury, damage or knockout; abilities retain their existing costs and combat limits.
- Retain the current Ascension starting stage and existing combat ratings as the implementation baseline; this decision does not request additional stat boosts, new forms or new skills.
- Update character-selection copy, backstory references, current lore and dialogue context consistently for Emily as both protagonist and NPC. Preserve her gentle personality, floristry and everyday interests; combat power does not replace her personal identity.
- Remove present-day claims that she is unawakened or that Critical Hit is merely hypothetical. Preserve genuinely historical pre-awakening scenes with explicit context. Do not invent an awakening date, cause, Blackstone encounter, Iron Circle history or campaign victories to explain the change. A detailed origin story remains a separate writing decision.
- Existing saves must retain earned progression, learned moves, relationships and story history. Audit stored Emily profiles before deciding whether migration is needed; do not reset profiles or downgrade progressed stages to Ascension. If older saves require a correction, implement and test an idempotent compatibility path during normal loading, never during menu preview. Document the actual effect on existing stories, including updated dialogue lore; do not rewrite historical chat logs.
- Acceptance: fresh protagonist and NPC Emily profiles, selection details and dialogue context agree that her ability is active; no future-only disclaimer survives in present-day context; pain suppression cannot be presented as invulnerability. Test representative existing saves and any compatibility correction separately from new-game defaults.

Avoid invoking stateful gameplay profile helpers on live saves while browsing: `combat_profiles.profile` uses `setdefault` and initialisation. Construct isolated starting data or read a copied, validated snapshot. Opening a menu must not advance time, initialise live progression, unlock skills, alter relationships, write story data or make AI/network requests.

Custom library integration caveat: `custom_library.profiles` currently recovers profiles from saves by calling `remember`, which writes reusable profile files, and silently skips some invalid profiles. Separate read-only enumeration from legacy recovery for the new roster. Make any needed recovery an explicit, idempotent library/load step outside preview rendering, preserving story saves. Inventory stable identity carefully: existing library filenames are content hashes, so a name alone is not a profile key. Surface recoverable invalid-profile information rather than silently making a user's character disappear.

## Presentation, accessibility and boundaries

Reuse `winterfield_ui.py` and existing visual assets where appropriate. Phone integration, if later added, must use `phone_theme.py`, embedded `phone_dialogs` and dark control states throughout. The menu is a pre-game surface; actual combat, training, demonstrations or other in-person activities belong in the in-person window.

Support keyboard roster navigation, Tab focus, explicit activation and Escape/back. Changing selection must not launch a story. Keep focus visible independently of colour, support long names and text scaling, and provide text equivalents for badges and stat bars. Cancel pending render callbacks when navigating away and cache appropriately sized portraits to keep roster browsing responsive.

Any decorative motion should be subtle, skippable and disabled by Reduced Motion. Static artwork is sufficient for the initial implementation; animated character assets are not a prerequisite.

## Additional suggestions, not committed scope

1. **Compare two protagonists:** a compact side-by-side view of starting life, interests and abilities. Especially useful for choosing between social and combat-oriented playstyles.
2. **Story tone tags:** authored descriptors such as quiet everyday life, investigation or martial arts, grounded in available content. Avoid implying a locked class or a guaranteed story outcome.
3. **Character-specific backdrops and ambient cues:** reuse suitable homes or locations, with sound controlled by the existing audio setting and motion by accessibility preferences.
4. **Spoiler-controlled character codex:** optionally revisit biographies and discovered information from a particular save. Discovery must stay scoped to that save rather than leaking across stories.
5. **Favourites and recently played:** shortcuts for a growing roster, stored as menu preferences rather than gameplay changes.
6. **Awakened portrait preview:** toggle between existing ordinary and applicable awakened artwork, clearly labelled as artwork. A preview never grants a form or initiates combat.
7. **Starting connections:** a small relationship diagram showing established family, friends and known affiliations. Use only opening knowledge, distinguish friendship from romance and conceal secret connections. This gives a social RPG choice as much weight as combat stats.
8. **First-day opportunities:** show two or three concrete activities available from that character's real starting situation, with a brief explanation of where to find them. These are suggestions, not auto-started quests or promises of exclusive content.
9. **Strengths and trade-offs:** pair each major ability with a concise limitation and show non-combat strengths alongside it. For Emily, explain that suppressing pain does not stop injury. Avoid invented weaknesses or an overall power ranking.
10. **Find my protagonist:** optional filters for interests, starting lifestyle and combat approach that narrow the roster using authored metadata. Explain matches and allow instant reset; no AI request or personality inference is needed.
11. **Opening situation preview:** show the actual starting location, home and work/study context together in a compact card, optionally with existing location artwork. Clearly distinguish new-story conditions from a Continue summary.
12. **Remember browsing position:** retain the chosen tab, search and roster position when returning from a biography, gallery or creator. Keep focus on the selected character and store any persistent preference outside story saves.
13. **Custom character identity card:** optionally let players choose a short epithet and accent colour in the creator, then reuse them in the roster and dossier. These are presentation fields, not new abilities; existing profiles receive neutral defaults.
14. **Related playthroughs:** from a selected reusable character, show explicitly associated saved stories with separate New story and Continue actions. Match by reliable profile/save identity, never just a shared name; allow multiple playthroughs without mixing their progression.
15. **Duplicate as a new character:** create a separate editable draft from a saved custom profile for alternate concepts. Keep the original and its existing saves intact; changed awakened Traits still pass the creator's existing review process before use.
16. **Standalone ability glossary:** a browsable reference remains optional; contextual explanations of Trait, amplification and Path stages are already required by field help.
17. **Portrait framing controls:** optional crop/position adjustment for roster thumbnails and the large preview, without modifying the original portrait asset. This helps differently proportioned custom artwork fit the same layout.

Prioritise the complete dossier, Emily's lore alignment and accurate starting information before adding these extensions. Of the new suggestions, starting connections, first-day opportunities and strengths/trade-offs provide the most useful information for choosing a protagonist.

## Full-plan integration review — 2026-11-10

Reviewed the complete selection/creation specification, approved starting-background catalogue and MH-002 roadmap entry. All confirmed additions remain required. Earlier suggestions not explicitly accepted remain in the optional lists; they are not release blockers. This is a design review, not evidence that runtime behaviour works.

Documentation verification passed: local link existence across all three planning documents, presence of the four confirmed additions and review sections, and checks for superseded optional/start-flow wording. `patch_notes.py validate` passed with 461 entries and `patch_notes.py export` refreshed the generated notes. No release entry was added for planning; gameplay tests and rendered UI inspection remain pending implementation.

### Shared data and lifecycle

| Object | Owns | Must not own or change |
| --- | --- | --- |
| Draft | Editable fields, stable draft ID, choices, locks, ideas and asset references | Active story progression |
| Undo stack | Short-lived edit operations for the current session | Durable recovery or external AI side effects |
| Autosave | Latest recoverable working copy, including incomplete input | Automatic replacement of a newer manual restore |
| Revision history | Meaningful durable draft checkpoints | Reapplication of old approval without revalidation |
| Reusable character | Validated versioned starting profile with stable profile ID | Current job/heat/relationships from a playthrough |
| Story snapshot | Resolved starting choices and evolving save-local progression/knowledge | Automatic propagation of later creator edits |
| Preview | Read-only derived dossier or isolated sample dialogue | World events, NPC memories or save mutation |

Use one validation/starting-state resolver for the picker, completion checklist, Review, roster and new-story initialisation. Keep approved narrative, structured mechanical choices, private facts, aspirations and unused ideas separately typed. Preview adapters cannot call live gameplay initialisers. One knowledge/identity resolver supplies appropriate public or NPC-facing data; AI prompts should receive only relevant allowed context, not secret text with a request to ignore it.

Creation lifecycle: New/Resume draft → edit/review → Save character → roster selection → Begin. Save & begin is an explicit shortcut through the same save and start checks. Save character never starts a story; failed start preserves the saved profile. Cancelling creation adds no completed profile, though an autosaved draft may remain available until explicitly discarded. Draft edits and revisions do not change a reusable profile until Save character, and never update existing stories.

Import lifecycle: inspect package → validate/review in a draft → Save character. Compatible complete imports may use an explicit save action after review; invalid imports stay out of the playable roster. Export only accepted reusable data and chosen private content, not unsaved working edits. Library recovery/migration happens outside rendering and must preserve legacy IDs and story links.

### Resolved overlaps and conflicts

- Approved creator features no longer sit under optional headings. The in-creator Review summary and contextual term help are required; a separate exportable character sheet, detailed comparison tool and standalone glossary remain optional.
- Free advanced starts bypass origin discovery/onboarding gates only for their selected approved role. They do not reveal unrelated secrets, replace canonical leaders or unlock every organisation. This supersedes the earlier ambiguous picker discovery restriction.
- Newcomer/no-acquaintance defaults coexist with established careers/criminal backgrounds: prior experience and limited role recognition are explicit origin facts; personal bonds and unrelated local memories are not manufactured.
- Undo, history and autosave have separate responsibilities. Restores and undo invalidate pending AI responses using draft identity plus revision/field signatures, even when the text happens to return to an older value.
- Roster/dossier previews make no network requests. AI dialogue previews are a separately labelled, explicitly requested simulation. Passive previews do not save anything; autosave writes draft state only during editing.
- Appearance edits do not silently regenerate artwork. Track portrait compatibility separately from Trait approval. Final validation must follow the actual creator's accepted-portrait rules and explain any necessary explicit action. AI writing is optional, but existing portrait-generation and Trait-evaluation dependencies are not silently replaced with a promise of fully offline completion.
- Creator/dossier access to a player's own private history is distinct from NPC/public access. Public names, underworld aliases and private identity links use the same visibility contract across dialogue, profiles, import/export and sample conversations.
- Existing saves retain their current progression. Emily's explicitly scoped lore/profile compatibility correction is separately tested and does not justify reseeding other characters or resetting earned stages.
- Starting combat stats now use progressive career/backstory contributions, superseding any earlier assumption that career and combat stats are independent. MH-001 owns future numerical scale, effective-strength calibration and migration. Creator packages now have confirmed target hierarchy placements, including low-A Exceptional Veteran; reaching those targets through coherent stats/abilities depends on that shared contract. UI/data work can proceed before final calibration.
- Approved preset/rank names are fixed scope. Reputation, heat, prior-experience credits, qualifications, resources and detailed combat packages still need a documented balance pass; proposed numbers are never presented as verified gameplay.

### Implementation sequence and exit criteria

| Stage | Work | Exit evidence |
| --- | --- | --- |
| 1. Contracts and balance | Versioned profiles/IDs, legacy migration, private identity/knowledge fields, accepted preset catalogue, origin experience and combat defaults | Reviewed field mappings and balance tables; legacy fixtures and pure resolver checks |
| 2. Persistence and editor | Drafts, autosave, revisions, undo/redo, locks, ideas, import validation | Recovery/failure tests and no cross-draft/story changes |
| 3. Creator and picker | Staged form, all career/crime options, preview, prompts, checklist, randomisation, help and identity controls | Every option maps to valid reviewed state; new players can select all advanced starts |
| 4. AI and dialogue | Text assistance, stale-result handling, locked-fact review, backstory/identity context and isolated dialogue preview | Conflict/cancellation tests, visibility tests and no leaked preview memories |
| 5. Menu and gameplay wiring | RPG layout, shared dossier, canonical/custom roster, save/start/Continue, once-only career/crime/combat setup, Emily lore alignment, export | Preview/start parity and compatible existing saves; all current entry points reachable |
| 6. Integrated QA and release record | Usability pass, dark-theme states, scaled layouts, regressions and actual patch notes | Required checks and rendered evidence recorded, catalogue validated/exported |

Stages order implementation dependencies; they do not remove approved features or promise separate releases. Reuse existing creator capabilities while replacing their flows deliberately. Finish the entire confirmed scope and required checks before marking MH-002 ready for release.

### End-to-end acceptance scenarios

1. New player makes an ordinary unawakened job-seeker with minimal text, skips optional sections, saves and starts. Roster, Review and initial story agree.
2. New player freely chooses a senior/manager career and established faction role, with combat training combined with career/background experience. Correct authority, pay, commitments and knowledge appear; reloading awards nothing twice and later progression works.
3. Player drafts privately linked public/underworld identities, locks key facts, expands text, bookmarks an alternative, randomises selected fields, then undo/redoes and restores. No locks, ideas, identities or obsolete approvals leak or change silently.
4. Interrupted autosave and restart recover the right draft; duplicate-name drafts and profiles remain isolated. Missing artwork, incomplete fields and errors preserve work and provide recovery.
5. Export/import with private content included and excluded produces correct previews; edited/untrusted approval flags, unsupported versions and malformed assets are handled before entering the playable roster.
6. Dialogue preview uses permitted backstory and identity only. Disclosing a secret in the preview affects that sample only; no actual NPC learns it. Editing the draft marks the sample stale and supports restart.
7. Existing canonical/custom saves and reusable legacy profiles load normally; custom characters appear in the shared roster; Emily's current lore agrees with her awakened state while preserving earned progression and historical logs.
8. A new player with no prior saves selects Exceptional Veteran with civilian, independent and faction origins. All resolve to the calibrated low-A target without unintended rank, title, secret-identity or form grants; save/reload and changing background preserve the accepted origin rules.
9. Keyboard-only and scaled-window review covers roster, creator, picker, history, AI review, help, import and errors. Dark surfaces persist in every state; actual activities continue in the in-person window.

### Remaining implementation decisions

No further scope approval is needed for confirmed features. Finalise balance tables, exact field/schema mappings, local retention/package limits, compatible origin credentials/portfolio gates and responsive breakpoints during implementation, then record concrete evidence. Do not silently resolve a balance decision by inventing completed missions, relationships or rank rewards. Tests for the pure data layer should precede UI wiring; rendered checks must inspect the actual completed screens.

## Release verification

Implement in the dependency order specified in the integration review above. All confirmed features remain in MH-002 scope; stages are implementation milestones, not separate promised releases.

Verify before recording any release:
- Every current canonical and valid saved custom character is reachable and previews the correct identity.
- All includes existing and newly created custom profiles; My Characters filters correctly; duplicate names select the correct profile; cancelled creation adds nothing; restarting or deleting a story does not remove its reusable profile. Verify legacy recovery separately from read-only browsing.
- Preview fields match actual new-story data; saved previews match their selected save. Resolve or explicitly block contradictory data before acceptance.
- Browsing, filtering, tabs and closing/reopening do not mutate saves, award progression or trigger AI/artwork requests.
- Begin launches the selected character; Continue remains tied to its save. Existing save protection and recovery paths still work.
- Unknown facts, secret lore, future Traits and unearned forms are represented honestly.
- Inspect wide and compact layouts, Windows scaling, keyboard focus, hover/pressed/disabled states, long custom biographies, absent artwork, empty rosters and unreadable saves.
- Run relevant existing checks including `tests/start_ui_smoke.py`, `tests/playable_cast_ui_smoke.py`, custom creator/library checks and combat Path tests; add focused checks for preview isolation and source/selection correctness.
- If phone surfaces change, also run `tests/phone_dark_theme_smoke.py` and relevant feature smoke checks, with rendered inspection.
- Record actual save impact and player access in `patch_notes/catalog.json` following `patch_notes/AUTHORING.md`, run patch-note validation and required checks, then export `patch_notes/PATCH_NOTES.md`.

Planning evidence: source inspection only on 2026-11-10. Runtime tests and rendered UI checks are pending implementation. This document is not a released feature or a patch-note release entry.
