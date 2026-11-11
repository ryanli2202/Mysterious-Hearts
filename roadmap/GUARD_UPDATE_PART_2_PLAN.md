# Guard update Part 2 — conversations, authority and recognition

**Roadmap ID:** MH-003  
**Status:** Released  
**Added:** 2026-11-10  
**Area:** In-person guard interactions, dialogue context, contact eligibility and save compatibility

Implemented and available after restarting the game on 2026-11-10. Release record: `release-2026-11-10-guard-dialogue-and-authority` in [the patch-note catalogue](../patch_notes/catalog.json). The specification below preserves the approved scope; actual behaviour and verification limits are recorded in the implementation evidence. Part 2 follows the existing guard/portrait work recorded as `release-2026-11-10-guard-portraits-and-cybernetic-richter`; it does not rename that release or claim a previously tracked Part 1 roadmap entry.

## Plugin task assignments

**Assigned:** 2026-11-11. MH-003 is Released. Apply during requested maintenance and interiors integration without reopening the release.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Guard voice, role/recognition guides and campaign context | Story Skills + Writer's Loop | Review visible vs concealed identity, earned recognition, rank/command and disclosure audiences; retain campaign-specific outcomes and physical in-person dialogue. |
| Contact restrictions, authority and saved guard compatibility | falsegreen-skill | Review tests that distinguish legitimate recognition from illicit contact access, preserve legacy IDs and campaign clearance, and verify saved dialogue/profile routing. |
| Later guard portrait refinements | Bulk BG Remove only for cutouts; Story Skills for appearance continuity | Follow MH-010/MH-011 designs and MH-013 production gates; inspect actual conversations/combat and dark phone surfaces if affected. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Confirmed scope and access

Players can approach and talk to a present guard in the **in-person window**, including from the nearby-person interaction and guard roster. Opening a conversation must be a clear, non-combat action. Keep existing combat/campaign gates intact. Guards remain on duty: talking does not recruit them into a travelling party or grant access to their post.

Every guard type needs its own dialogue guide. Guards recognise the player's and other characters' organisational rank and role when that information is available to them, and react appropriately to their own members, outside members, outside leaders and civilians. This applies to canonical and custom protagonists, present companions and relevant people discussed in conversation.

Guards never become personal phone contacts from talking, starting a hangout, or completing an encounter. Existing accidental guard contacts need safe cleanup. Named story characters remain distinct from rotating guard posts.

## Dialogue-guide catalogue

These voice treatments and all six additional refinements below are confirmed planned scope; they add no new faction history, powers or character relationships. Each implementation guide must include voice, duties, allowed knowledge, forms of address, reactions to each audience category, refusal/escalation examples and a deterministic fallback. Examples below illustrate tone toward ordinary or unverified visitors, not mandatory repeated lines. The authority matrix overrides visitor scripts for recognised commanders: never tell Ivan or Sylvanis to wait for Syndicate clearance, or Richter to obtain Blackstone authorisation. Fearful, deeply respectful Ace reactions are separately required.

| Type key | Voice and conversational focus | Boundaries and illustrative line |
| --- | --- | --- |
| `yokai` | Disciplined assault specialist; direct, confident, operational language. | Recognises Shinokami command without treating every member as an assault commander. “State your business. I’ll check who can clear it.” |
| `oni` | Robotic security; concise, literal, procedural acknowledgement. | No invented human biography or omniscient scans. “Identity requires verification. State your purpose.” |
| `tengu` | Alert perimeter professional; practical questions about arrival, destination and clearance. | Shares directions appropriate to access, not deployment weaknesses. “Who are you here to see?” |
| `clubs` | Firm protection/enforcement voice; prioritises the protected person and site. | Respect for Syndicate hierarchy does not expose protected movements. “I can pass the request up. You wait here.” |
| `spades` | Restrained, precise, sparing speech; observant without constant theatrical threats. | No assassin identities, targets or covert methods disclosed. “You can leave the message with me.” |
| `affiliate` | Practical perimeter worker; less inner-circle familiarity, follows assigned remit. | Does not pretend to know secret suit business. “That’s above my clearance. I can ask.” |
| `headhunter` | Controlled cyborg interception specialist; decisive security language. | Cybernetics do not erase personhood or grant unlimited tracking. “Stop there. Tell me why you need entry.” |
| `seeker` | Watchful surveillance specialist; specific clarifying questions. | Refers only to observed or authorised information, not private thoughts. “Which entrance did you come through?” |
| `pmc` | Contract-security professionalism; plain instructions and assignment limits. | Absolute obedience to Richter is required; personal warmth may vary. “Authorisation first. Then I can escort you.” |
| `team9` | Controlled Awakened-response specialist; containment, field support and safety. | Recognises Gordon's established command and others' actual remit; avoids treating all Awakened civilians as offenders. “Tell me what happened, then give us room.” |
| `interpol` | Clear public-facing officer; courteous, procedural and accountable. | Distinguishes public assistance from custody/security permissions. “I can help at the public desk. That area is restricted.” |
| `kai_sentinel` | Formal, composed specialist; house security and current leadership. | Uses the saved successor/leadership outcome; cannot revive a dissolved faction. “I’ll take your request to the person responsible.” |
| `kai_guard` | Respectful house-duty voice; visitors, deliveries and ordinary directions. | No automatic access through personal familiarity or claims of seniority. “Please wait here while I confirm your visit.” |
| `lookout` | Brief, locally grounded and watchful; knows the immediate street/post. | Vocabulary follows the actual crew; no universal gang caricature or invented intelligence network. “You looking for someone here?” |
| `crew_enforcer` | Firm, territorial, practical; protects the crew's assigned interests. | Crew policy and saved diplomacy determine hostility, not the archetype alone. “Say what you need. Keep the entrance clear.” |
| Custom Awakened | Professional guard voice with approved crew flavour and relevant ability category. | No invented Trait, rank or loyalty beyond the saved assignment. “I can check that with the crew.” |
| Custom unawakened | Grounded site-security voice, relying on training and procedure. | No fabricated powers or assumption of cowardice. “Let me verify that before you go through.” |
| Custom robotic | Procedural, concise; uses saved ownership and assigned access rules. | No fabricated feelings or private records; obey the established owner/command hierarchy. “Request received. Checking assigned permissions.” |

Custom named types inherit the appropriate category guide plus explicit type/crew overrides. Renaming a type changes its label, not its identity or permissions. Require coverage checks for every `organisation_guards.TYPES` entry and every supported custom category; unknown legacy types receive a neutral, restricted-duty fallback.

## Rank, role and recognition contract

Build a structured context resolver shared by guard dialogue and its action validation. Resolve each subject separately: identity, organisation, current rank/title, operational role, command scope, membership status, source of recognition and what this guard is allowed to know. Use current saved membership, promotions, leadership, expulsions, crew ownership and campaign outcomes before static defaults. Inventory `combat.affiliation`, membership/career records, gang leadership, Interpol and Rei's ending state before choosing the authoritative precedence; do not use combat's numeric rank as a complete dialogue title or permission system.

Rank, role, combat strength, notoriety and access clearance are different fields. Established high command carries **absolute authority over its defined subordinates**, across local posts and ordinary duty assignments. Guards must not invent clearance checks, supervisor referrals or personal discretion to obstruct a recognised absolute commander. A post's routine orders do not override that commander's instructions. Combat strength or reputation alone does not grant command; a civilian may be formidable without being an organisational leader.

### Confirmed command hierarchy clarification — 2026-11-10

- **Ivan and Sylvanis:** each can freely command any Syndicate member **apart from the Four Aces**. This covers ordinary guards, specialists, affiliates and other non-Ace members, not just a personal detail or local department. Implement the named exception explicitly; do not infer command over an Ace from a numeric rank comparison.
- **The Four Aces:** do **not** command guards. Guards nevertheless fear them and show undying respect. Convey this through immediate attentiveness, careful address, tension and exceptional deference, without turning fear or respect into formal command authority. They must never receive the ordinary junior-member treatment simply because they lack guard command.
- **Joseph Richter:** retains **absolute control over Blackstone**, including its PMC, Seeker and Headhunter personnel. Contract status, departmental boundaries and routine security procedure cannot be used to deny his authority. His control does not depend on whether he is currently depicted in ordinary or cybernetic form. Preserve resolved campaign outcomes and disabled deployments; authority does not resurrect defeated personnel or reopen a completed story.
- **Organisation-wide application:** these are examples of a general hierarchy requirement, not three isolated dialogue exceptions. Author an explicit command/exception matrix for every organisation and custom crew using established leadership lore and current legitimate saved leadership. Clearly established top command has absolute authority over its subordinates; actual exceptions such as the Aces remain explicit. Ordinary seniors have their authored authority, and outsiders gain no authority merely from their rank elsewhere. Do not invent additional canonical hierarchy relationships where evidence is missing.

Represent `can_command`, scope, explicit exceptions, fear and respect separately. Apply the same matrix to the player and NPCs. Known commanders are recognised without repetitive proof requests; identity verification is for genuinely unknown or disputed identities, not a routine obstacle to leadership. A recognised commander may authorise a visitor or escort, with the resulting permission recorded by a supported action rather than inferred from mere proximity.

Resolve conflicting orders using the established hierarchy and any authored precedence. Do not invent precedence between Ivan and Sylvanis, or let the model silently choose a superior where lore has not established one; identify such gaps during the hierarchy inventory. Generation must express the resolved authority faithfully. A missing gameplay action is an implementation limitation, never an in-world claim that a guard can overrule absolute command.

| Audience | Expected response |
| --- | --- |
| Own absolute commander | Immediate acknowledgement and obedience across posts and departments; no invented local-clearance veto. Apply explicit hierarchy exceptions and execute supported orders through game actions. |
| Own authorised operational commander | Follow their established command scope; do not confuse this narrower role with absolute high command. |
| Four Aces addressing Syndicate guards | Fear and undying respect, with no guard command authority; deferential speech must not fabricate a chain of command. |
| Own senior member outside direct remit | Professional deference, verification or referral for orders beyond their authority. |
| Own peer / junior member | Collegial or instructive tone appropriate to the type; no invented familiarity or bullying. |
| Member of another organisation | Apply current diplomatic/security context; distinguish approved visitors, neutral outsiders and known hostiles. Membership alone is not an attack trigger. |
| Leader of another organisation | Recognise known status and diplomatic significance; measured respect, caution or hostility consistent with relations, with no transfer of command or automatic clearance. |
| Civilian / unaffiliated visitor | Type- and site-appropriate assistance, directions or refusal; no invented affiliation or criminal status. |
| Unknown / disputed identity | Ask purpose or verify credentials without pretending recognition is certain. Spoken claims alone cannot change saved status. |

Evaluate other characters with the same rules, including NPC-to-NPC address in mixed groups and references to absent people. Do not attribute a companion's clearance to everyone accompanying them automatically; honour explicit authorisation from a commander with the authority to grant it. Avoid disclosing confidential titles merely because the internal resolver knows them. In particular, preserve The Crow's anonymity and concealed civilian identities behind operational titles. Internal hierarchy knowledge may be complete for a relevant known command role while recognition of an unintroduced face remains uncertain.

Re-resolve after promotions, demotions, defections, expulsions, ownership changes and story outcomes. Generation receives a knowledge-filtered snapshot; it cannot award membership, clearance, money, victories or authority through prose. Revalidate presence, post identity and relevant state before committing a delayed reply.

## Contact bug and save compatibility

Observed source path: `groups.open_local` creates `npc_chats[name]` and calls `groups.sync_contacts`; syncing creates a direct text group for every NPC chat. `town.commit_npc` also syncs contacts. `organisation_guards.npc_detail` already says guards have no personal number, but prose cannot enforce this.

Implement a shared contact-eligibility rule and use it at all contact-list, direct-text, group-text, number-exchange and load/sync entry points. Give guards structured entity metadata; do not rely solely on display labels. Preserve ordinary resident contact behaviour and named-character exceptions.

Keep guard conversations as in-person records separate from phone eligibility. Use stable post/type/faction/venue identifiers rather than `Post guard` labels, which can collide across locations and renumber when deployments change. Rotating posts are not permanent individual friends: do not transfer personal memories from one replacement to another. Define encounter/shift scope before introducing persistent individual memory.

Add an idempotent, versioned migration for existing accidental guard contacts: remove their active phone eligibility, archive relevant history, and repair stale active-thread references. Inspect affected legacy group texts and number-book data as well as direct threads; preserve legitimate members and readable historical messages while preventing new guard texting. Match legacy guard records conservatively using known metadata and the reserved legacy format; ambiguous records must not cause deletion of legitimate contacts. Preserve recruitment, assignments, portraits, campaign victories, faction relations and normal NPC histories. Assess old saves containing only labels without venue metadata explicitly; do not guess an individual guard identity.

## Implementation milestones

- [x] Inspect current guard catalogue, local hangout/contact syncing, dialogue hook and affiliation helper; record the reported defect and planning evidence.
- [x] Draft per-type dialogue directions and audience rules for review.
- [x] Inventory authoritative rank/role/knowledge sources and all guard/contact entry points.
- [x] Implement stable guard interaction identities, in-person conversation routing and contact exclusion.
- [x] Implement guarded legacy cleanup and save/load compatibility.
- [x] Implement complete type guides, structured recognition context, explicit command/exception matrices and safe fallback dialogue.
- [x] Implement all six approved refinements: duty topics, warning ladder, visitor credentials, post memory, individual variation and supported command menus.
- [x] Verify deterministic behaviour, simulated provider success/failure, rendered states and release documentation; live provider prose remains unverified as recorded below.

## Acceptance and verification plan

1. Talk to each of the 15 built-in types and all three custom categories in person; verify guide selection, opening/reply context, respectful refusal, fallback and correct portrait. No guard is added to contacts before or after conversation, save/load or contact sync.
2. Exercise direct text, group text, number exchange and stale phone routes; guards cannot be contacted remotely. Ordinary locals and named characters retain their existing supported behaviour.
3. Test every audience category for player and non-player subjects: own commander, senior/peer/junior, outside member/leader, civilian and unknown. Include canonical/custom characters, mixed organisations, confidential roles and conflicting claimed versus saved ranks.
4. Test promotion, expulsion, defection, new leadership, renamed custom types, duplicate labels across sites, post depletion/rotation, faction dissolution and migration run twice. Preserve legitimate contacts and historical messages.
5. Test conversation during departure, active combat, removed post, state changes during generation, provider failure and duplicate callbacks. No stale reply or prose changes permissions or world state.
6. Inspect the nearby guard action, roster handoff, compact in-person conversation, refusal/error and end-of-conversation states. Run relevant guard, group, NPC, campaign, save and contact tests. If phone contact surfaces change, run `tests/phone_dark_theme_smoke.py` and relevant feature smoke checks, and visually inspect dark phone states.
7. Verify Ivan and Sylvanis can each command every non-Ace Syndicate member across departments; the Four Aces are excluded from their command scope. Verify all Four Aces receive fear and undying respect without guard command authority. Verify Richter's absolute Blackstone control across all three guard types and both appearances, preserving completed campaign outcomes. Extend matrix coverage to every other organisation and custom crew; no generic security script may override established absolute command.
8. Verify duty topics remain knowledge-appropriate; warning stages are readable and do not apply as obstruction to recognised command; visitor credentials and explicit commander authorisations work; post reports survive only their defined scope without fabricated personal memories; personality variations preserve hierarchy; supported commands execute once and have truthful outcomes. Test contradictory orders and unsupported actions without inventing hierarchy or claiming execution.
9. Record actual behaviour, access, migration and evidence in `patch_notes/catalog.json` only when implemented. Follow `patch_notes/AUTHORING.md`, run validation and unit checks, export `patch_notes/PATCH_NOTES.md`, and complete applicable release UI checks.

Initial planning used source inspection only. The following implementation evidence supersedes that initial verification state.

## Additional refinements — confirmed scope (2026-11-10)

All six suggestions are approved for implementation. Authority and dialogue must follow the clarified hierarchy above.

- **Duty-aware topics:** ask directions, who is in charge, visiting procedure or how to report a problem, with answers bounded by clearance.
- **A readable warning ladder:** a guard explains the boundary, warns about continued intrusion, then uses existing escalation mechanics. Do not turn a rude line into unavoidable combat.
- **Credentials and appointments:** let visitors establish a legitimate reason to enter through existing systems, with rank and visitor permission visibly separate. Recognised absolute commanders do not need visitor credentials; their explicit admission orders are honoured.
- **Limited post memory:** guards may refer to a recent warning at that post; label it as a shared security report rather than pretending every replacement personally met the player.
- **Individual variation within each type:** restrained variation in warmth, patience and phrasing while preserving the guide, duty and faction policy.
- **Supported command menu:** where the player has authority, offer executable orders such as status reports, referrals and visitor authorisation. Absolute commanders receive organisation-wide command coverage over their defined subordinates, without artificial local-rank restrictions. The menu is bounded by implemented actions, not diminished lore authority; add and verify handlers for every offered command, and never pretend an unsupported order was executed.


## Implementation evidence — 2026-11-10

**Release:** `release-2026-11-10-guard-dialogue-and-authority` in [catalogue](../patch_notes/catalog.json). Restart and continue the existing story. Access: **In person → Stories, guards & gang properties → Guards**, or approach a nearby guard.

- `guard_dialogue.py` supplies 15 built-in and three custom-category guides, explicit command/exception rules, knowledge-limited generation context, faction relations, per-shift delivery variation and deterministic topic/fallback speech. Rank comes from current membership/branch titles, canonical command roles, gang leadership, custom ownership and Rei's ending; expulsion removes player command. Aces always lack guard command, regardless of numeric rank. Unit/branch command is separate from organisation-wide absolute command.
- All six refinements are implemented through conversation and the in-person guard desk. Directions, leadership and credentials have explicit responses. Visit requests remain pending until a supported authorisation exists; the desk does not pretend to book an external meeting. Written reports are unverified, shared post records. Warnings progress through boundary explanation, repeat warning and recorded refusal without forcing combat. Local visitor authorisation/revocation, status and referral handlers execute separately from prose; they do not invent deployments or bypass campaign rooms. Conflicting Joker orders retain the unresolved precedence boundary.
- Separate guard histories use faction, venue, stable slot/type and story day. Custom type renaming retains identity, while different posts/shifts/owners do not share individual memories. Archived history remains readable. Load/sync migration removes guard phone eligibility and archives old chats, address-book entries and affected pending message work. Legitimate mixed-group recipients and old messages survive. Queued affected phone work is archived rather than replayed. No player save or credentials were touched during verification.
- Actual background-worker snapshot delivery, duplicate/stale replies, rank/post/ownership changes, fallback and real `game_core.load` round trips are covered. Generated prose cannot commit gameplay events. Physical action input retains its action presentation rather than being displayed as speech.

**Checks performed:** 101 passing tests across `test_guard_dialogue.py` (14 tests), `test_guard_portraits.py`, `test_major_campaigns.py`, `test_phone_numbers.py`, `test_character_types.py`, `test_save_system.py`, `test_dialogue_craft.py`, `test_campaign_dialogue.py`, `test_message_timing.py`, `test_hangout_texting.py`, `test_hangout_scene.py` and `test_hangout_journal.py`. Guard-dialogue and guard-portrait UI smoke passed; dark-phone smoke passed on 34 pages plus chat, contact details and embedded controls. Patch-note reader and start-screen smoke passed (28 previews). Catalogue validation/export passed. Patch-note unit checks: five pass; one historical-source failure for missing `tests/screenshots/mixtape-art-review-0.jpg`. This failure is not a guard test failure and was not concealed by changing historical records.

**Rendered review:** inspected `tests/screenshots/guard-part2-commands.png`, `guard-part2-conversation-compact.png` and `phone-dark-theme.png`. Guard desk and conversation use existing dark/in-person presentation; disabled visitor controls and compact conversation remain readable.

**Verification limits:** No live provider dialogue sample was requested. Tests simulate generated replies and provider failures; standard topics and the asynchronous UI turn use local authored responses. Prompted privacy/voice compliance and a small explicit contradiction filter do not establish perfect semantic enforcement for all model wording. The resolver and action handlers, not prose, determine permissions and save changes. Visitor approval applies to the local guard post for the current story day and does not unlock protected campaign areas; referrals and visit requests are recorded requests, not simulated remote responses or guaranteed appointments.


**Guard dialogue correction (2026-11-10):** A live reproduction found valid provider dialogue with empty narration was rejected and replaced by a stock greeting. `guard_dialogue.validate_reply` now permits narration-free speech; conversation topics use AI generation, malformed responses get one repair attempt, and persistent failures surface through the existing retry UI without saving a greeting. Sixteen guard-dialogue, six hangout-scene and three hangout-texting tests passed; asynchronous guard UI smoke passed and compact speech-only rendering was inspected. Two live Fox/Interpol turns produced contextual answers, recorded in `tests/guard_dialogue_live_check.json`; this supersedes the earlier no-live-sample limitation for this specific scenario only. Release: `release-2026-11-10-guard-ai-reply-validation`. Existing saved greetings are retained as history. Initial approach greetings and explicit desk actions remain authored.
