# Interiors integration review and implementation contract

**Parent:** [Lived-In Interiors](INTERIORS_UPDATE_PLAN.md)  
**Detailed layouts:** [Public buildings and faction rooms](INTERIORS_PUBLIC_AND_FACTION_PLAN.md)  
**Review date:** 2026-11-11  
**Status:** Proposed design reviewed; implementation and runtime verification pending

**Image inventory:** [Room-by-room production list](INTERIORS_IMAGE_INVENTORY.md) and [JSON manifest](INTERIORS_IMAGE_INVENTORY.json) provide the current authored baseline, proposed target paths and visually reviewed reuse candidates. Runtime IDs and final render approval are still pending; planning keys do not change game locations.

This document resolves integration ambiguities in the two layout plans. Its contracts take precedence over earlier tentative wording about representation, movement, scheduling, work access and migration. It does not change established character canon, event outcomes or authorize implementation. Numerical guard deployments and room artwork remain subject to implementation validation.

## Plugin task assignments

**Assigned:** 2026-11-11. Implementation contract under interiors; assignments do not change the resolved contracts or activate proposed rooms.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| One location model; campaigns, meetings, privacy and wardrobe contracts | Story Skills + Writer's Loop | Review room/building/zone wording, character-specific constraints and wardrobe precedence so implementation tasks have one authoritative contract. |
| End-to-end acceptance scenarios and staged activation gates | falsegreen-skill | Review behavioural tests for actual movement/attendance, adjacent travel cost, fixed characters, guards, work permissions, outfit restoration and idempotent migration; reject mocked-state-only evidence. |
| Artwork activation gates | Bulk BG Remove only for portrait layers; no plugin for full room painting | Verify unique room-image coverage, routing and in-person rendering separately from image preparation. Preserve the Garrett living-room replacement gap until an explicit inventory revision resolves it. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Findings resolved in the design

| Gap found | Resolution |
| --- | --- |
| Existing code compares a single location string for travel, work, witnesses and attendance. | Normalize through one location registry with separate building, room and zone semantics. Never globally replace every equality check with a building comparison. |
| `world_loop.ensure` and `advance` pin Crow, Takeo, Thirteen and Charles before ordinary invitations can run. | Treat these as permitted-location constraints, not unconditional per-tick relocation. Resolve authorized same-building events within those constraints. |
| Scheduled invitations currently assign NPCs directly to the venue, clearing journeys. | Schedule travel and interior routing before the event; arrival and attendance follow actual presence. Do not silently rewrite existing event start/end times. |
| Room wandering could compete with obligations, conversations or the active player's movement. | Use the explicit intent priority and commitment rules below; room preferences are the final fallback. |
| JobSeek has 12 distinct job keys and progression actions beyond shifts; several proposed layouts lack staff review/work areas. | Map all 12 jobs and add the minimal connected staff spaces below. Shared task access is scoped and never faction clearance. |
| Room guards would change index-based IDs and building-wide clearance checks. | Preserve legacy IDs with a mapping; use stable post/slot IDs for additions and versioned mission encounter sets. Separate physical post presence from mission-required enemies. |
| Private Charles scenes currently check the whole lab for bystanders; room separation alone could bypass authorial restrictions. | Use explicit room-local privacy while retaining mission/party/disclosure prerequisites and secure building clearance. A guard outside a closed door is not a witness; anyone inside is. |
| Plans mixed no automatic relocation with active-save room migration. | Only migration may place already-present participants into the compatible room of their active scene. This is a one-time restoration, never new travel or a general access bypass. |
| A closed/occupied room could make a job or story permanently impossible. | Require an authored accessible route, waiting state and interruption/resume rule for every activity; no hidden deadline extensions or reward replay. |

## One location model

Define one authored registry and save contract before adding room UI. Suggested module names are implementation choices; the following meanings are required.

| Record | Required information |
| --- | --- |
| Building | Stable existing ID, public/map label, discovery rule, exterior/entry point, default arrival, room list and legacy aliases. |
| Room | Stable ID, parent building, display/discovery label, connected edges, enclosure, weather exposure, access policy, capacity/reservation policy, supported activity tags, art and safe exit. |
| Zone | Stable local label within a room, e.g. sofa/counter/ring. Zones share room presence and witnesses unless a separately authored scene rule says otherwise. |
| Edge | Origin/destination, door or open connection, access test, accessible route information and movement cost; outward safe exit must not depend on permission to enter another secure room. |
| Actor | Current canonical location/room, optional zone, activity, availability/commitment, pending route, journey and room-history state. One authoritative room; player/world mirrors are updated atomically. |
| Activity/event stage | Stable ID and schema version, assigned room/zone, participant requirements, start/end or work duration, room reservation, access grants if supported, witness/privacy rule, interruption/resume and idempotent outcome. |
| Security post | Stable post and guard-slot IDs, room/edge, duty hours, faction/authority, count, encounter set and replenishment policy. |

Keep existing `site_01_briefing`, other site reception/briefing IDs and named Interpol/Blackstone locations resolvable. New identifiers can use a building-qualified form, but display labels must never be save keys. Home aliases (Ivan/Valentina, Neo/Alyssa, Rei/Yuriko) resolve to one building with distinct bedroom permissions. Retain separate building travel records and existing map pins; indoor room coordinates inherit the building position.

Use semantic helpers throughout the code: same building for map/search and broad workplace identity; same room and available for conversation, attendance, shared minutes and physical tasks; valid route and access for movement. Trips are not room occupancy. Legacy unexpanded buildings resolve to a single default scene until their entire integration batch is ready.

## Connected layouts, movement and exits

Every supported activity must have a route from its authorized arrival point. Validate graphs for orphan rooms, protected rooms reached through public shortcuts and inaccessible exits. Secure corridors belong between reception and controlled rooms; public bathrooms must not require entering staff workrooms. Unknown room names stay hidden until legitimately discovered.

Proposed baseline: adjacent-room movement commits immediately and adds no extra story minutes; existing actions continue to advance time normally. This avoids making a previously valid one-hour shift run past closing merely because it now has several workrooms. It still checks each traversed edge. A multi-room Go to room action follows those edges and stops at a blocked door, scene trigger or encounter; it is not a teleport. Large timed routes may be authored explicitly, with booking/travel estimates updated accordingly. Waiting advances time only through an explicit existing wait/time action.

Time-driven NPC room choices occur on story-clock ticks, not UI renders. Retain proposed 20–60-minute leisure dwell periods with persisted choices; scheduled transitions can occur sooner. Door positions do not themselves simulate hearing through walls. Open zones use one room; an enclosed room uses its own co-presence set. Do not add complex acoustic simulation as an implicit dependency.

Add common access outcomes: allowed, knock/request, wait, denied, temporarily unavailable, and safe exit. Each shows the actual next step without leaking hidden occupants. If permission expires or closing occurs, finish only an already-authorized atomic action where existing rules allow, then exit to the designated safe area. Combat/custody follow their authored resolution; nobody is ejected mid-combat into a contradictory scene. Expiry cannot be extended by refreshing or talking indefinitely.

Companions check every edge independently. Offer entering alone with companions waiting in a permitted room, choosing a different destination or leaving together. Party membership can persist while separated, but co-presence, dialogue, shared minutes and combat support cannot. Do not strand a companion behind a locked route or summon them through a private door. Reunion uses explicit room routing.

## Scheduling and availability

Resolve NPC intent in this order:

1. Active combat, custody, knockout/recovery and explicit campaign scene locks, honoring their own established rules.
2. An already-running noninterruptible event/work stage; resolve conflict through that activity's interruption policy rather than duplicating the actor.
3. Accepted timed events and mandatory authored meetings, using existing event-provider ordering and a central conflict check. Retain council precedence over casual plans. Do not accept a new overlapping booking that cannot be honoured.
4. Existing approved companion/hangout commitments until their end or next hard obligation. A hard deadline prompts a visible wrap-up; casual conversation cannot hold an NPC indefinitely.
5. Faction shifts and normal work/sleep/building appointments, retaining existing precedence such as the 17:00 laboratory review overriding overlapping routine work.
6. Optional leisure building choice, then room/activity preferences and dwell time.

Fixed characters retain their existing allowed domain: Crow inside Syndicate HQ, Charles inside Glasshouse, Takeo in his established briefing room and Thirteen in his established briefing room unless a later explicit story change authorizes otherwise. Crow can attend the council chamber or executive room without leaving HQ; Charles can move between authorized lab rooms without leaving Glasshouse. Initialization/load must not reset these actors to the building default every time state is read. Active-player choices remain exempt from NPC scheduling; fixed-location player restrictions apply only where existing gameplay explicitly requires them.

Plan NPC travel ahead of a booked start when possible; preserve external travel rules and complete interior routing on arrival. A delayed guest is visibly late/absent, not teleported. Do not start a reward-bearing stage without its required attendees. Optional audience roles need not block the event. Event notifications distinguish starting time, participant arrival and player attendance; never announce that everyone arrived solely because the clock reached the start.

On large time advances, process obligation boundaries, arrivals, expiries, stage completion and closing in order rather than sampling only the final room. Advance once, resolve outcomes once. Load restores state without advancing time. Catch-up does not fabricate unobserved conversations, evidence or missed mandatory attendance.

## Complete JobSeek room mapping

These additions extend the public layout graphs; all added architecture is proposed. Preserve existing hours, rank checks, pay and task durations. Every progression action in `jobseek_progression.py` must be classified as online, physical or authored abstract work before routing; do not turn online administration into an unnecessary physical visit.

| Job key | Physical task rooms | Added connected support space / review |
| --- | --- | --- |
| `photographer` | Studio photo room; equipment preparation and client selection in review room. | Existing proposed studio review room serves producer meetings. |
| `model` | Studio photo room and private dressing/fitting room. | Review room for booking/portfolio review; changing is not public dialogue. |
| `librarian` | Library desk, stacks, reading room and booked study room. | Add staff catalogue office off desk corridor; promotion review there. |
| `oculus` | Existing public reception and desk service zones. | Add public-service supervisor room off reception, outside secure corridor. Civilian rank never grants briefing/data-wing or Syndicate access. |
| `cinema` | Ticket foyer; projection room only for eligible assignment/rank. | Add staff office off staff corridor for festival planning/reviews. |
| `barista` | Café counter and staff preparation/kitchen. | Add staff office off kitchen/service corridor; meetings never require passing through a private customer booking. |
| `florist` | Shop, arrangement workroom and authorized stockroom. | Workroom's review table is a zone; use a scheduled quiet review, not fictional soundproofing. |
| `chef` | Golden Dragon kitchen and assigned service areas. | Existing proposed staff office for reviews. |
| `retail` | A specific authored Galleria tenant unit, its shop floor and receiving room. | Add that unit's staff office/store; do not treat the entire mall as the player's employer. Choose a neutral workplace label until an existing retailer is verified. |
| `arcade` | Counter/cabinet floor; repairs at a safely unavailable cabinet or service bench. | Add staff repair room and office off service corridor. Tournament customers do not stand in a repair-only room. |
| `gardener` | Existing outdoor garden/path work zones. | Add proposed park pavilion tool store and supervisor office for physical briefings; gardening remains outdoors and retains weather checks. |
| `bartender` | Bar counter and service room. | Add staff office off service room for reviews; maintain 17:00 opening and existing hours. |

A physical assignment grants only the minimum supported work access for its duration; it is not an invented security credential. Validate required access before accepting/starting work and again at entry. Colleagues/mentors use stable workplace-role records when no named cast member exists; do not create personal contacts or phantom named attendees. A scene requiring an abstract supervisor must have an explicit local role present for that scene, not wait forever for an NPC absent from the cast registry.

Bubblegram district-level jobs need an explicit classification: outdoor meeting/handover point, already-established building room, or a newly authored neutral meeting venue. Do not pick a random building on every visit or reveal an unknown faction base. Snapshot the destination with the accepted assignment. Leadership meetings use the existing diplomacy mapping and all current authority checks.

## Campaigns, meetings and privacy

The implementation inventory must include `charles_quest.py`, `charles_disclosure.py`, `rei_story.py`, `interpol.py`, `interpol_cases.py`, `post_story.py`, `laboratory_missions.py`, campaign prose/dialogue/flashback catalogues, and any newer campaign modules discovered at implementation. Map each branch and repeatable operation, not just campaign titles. Include guards, combat and aftermath, even when all occur inside one building.

Use authored per-stage destinations for missions/work; a generic public-room fallback is allowed only for a casual event with genuinely unspecified intent. Unmapped campaign or restricted-work stages are validation failures, not invitations to execute in reception. Historical flashbacks keep their own historical scene space and cannot relocate the live cast or award present-day discoveries.

Bookings validate required participants and room capacity, including companions and guards physically inside. Meetings reserve an enclosed room when their existing privacy requirement demands one. A guard stationed outside the council door does not consume a chamber seat or hear its agenda; an inside guard is a real witness and must satisfy the scene's disclosure rule. An unavailable private room cannot silently become an open café table.

Separate arrival, joined, participating, temporarily away and completed/missed states. Existing attendance rules remain authoritative: council minutes count only while joined, awake, eligible and in the chamber; leaving pauses accrual. A conversation lock cannot extend the booked end. Missing a room due to an implementation-only migration obstruction must be recoverable without inventing player attendance or blaming the player for an impossible route.

Charles-specific acceptance: Garrett must complete the authored approach/guard/victory steps, reach the assigned private reunion room and satisfy existing solo/privacy rules. Charles must actually be there. Sylvanis or other personnel in another lab room neither block a private conversation solely through building equality nor learn its contents. Unauthorized room occupants still block it; moving the party to the hall is allowed only if the existing mission's solo/party rule permits that, not as a bypass. Preserve all disclosure and reunion flags.

## Guard allocation and encounter compatibility

The staffing table is a planning baseline, not a rule to shrink a site with a larger existing deployment. Expanded sites require an explicit before/after manifest, retaining existing guards and adding slots where room coverage needs them. Guard counts must represent actual actors, not a static label plus an unrelated combat roster. Off-duty, disabled, defeated or redeployed guards cannot appear at two posts.

Existing built-in IDs are `venue:index` from `organisation_guards.slots`. Do not reorder `DEPLOYMENTS` and reinterpret saved victories. Freeze old IDs and map each to a new post; new IDs use stable building/post/slot identifiers. Preserve custom recruited guard IDs, type, cost and ownership; stationing selects a room/post within an owned permitted property.

Separate three concepts: guards physically present at a post, enemies required by a particular mission/version, and site permission/breach state. Campaign `cleared()` must evaluate its snapshotted required encounter set, not every guard added to the building later. Patrol victory remains subject to existing day-based replenishment; campaign victory does not. Do not make a local post victory imply that all rooms or confidential records are authorized. Existing earned broader clearance receives an explicit compatibility rule, not silent removal.

For an active legacy campaign, preserve defeated IDs and remaining original required IDs. Additional security posts must have an authored passage reason or stay outside that mission's critical route; do not silently turn hostile guards friendly. New mission instances can use a balanced expanded roster. Completed campaigns remain completed; ordinary future patrols can still obey their separate rules without replaying the campaign.

Do not add automatic reinforcements in the first interior release unless separately implemented and tested. Local post encounters suffice. Guard dialogue, command exceptions and access tests apply before combat; feared/recognized visitors are not automatically commanders. New room security must respect established absolute-command exceptions and the Aces' specialist status.

## Wardrobe and location resolution

Automatic location/activity outfits are required scope; see the [wardrobe specification](INTERIORS_UPDATE_PLAN.md#automatic-location-appropriate-wardrobes--required-scope). Add an appearance resolver downstream of location, activity and scene resolution. It must consume the selected room/activity; it must never move an actor, choose their schedule, grant access or complete an event to justify clothing.

Save stable baseline outfit, effective automatic choice, active context identity, manual visit override and schema version per actor. Keep category metadata in the shared wardrobe registry and preserve existing availability/unlock rules. Do not create a second independent outfit list for interiors. Context identity represents a beach/gym/home visit or specific event, not each screen render or adjacent room. Entering a higher-priority event temporarily overrides a building category; leaving recomputes from the current context rather than blindly restoring a stale stack.

All live appearance consumers must read the same effective outfit: in-person portraits, appropriate combat rendering, current-scene dialogue context and camera default selection. Preserve camera's separately selected staged clothing and the appearance snapshots of already-started authored scenes where those are required. An appearance change never changes a character's physical identity, powers or equipment mechanics; required faction masks and story disguises remain authoritative.

Initialization migrates existing player wardrobe choices as baseline, never as an inferred permanent lock. NPCs without saved appearance state use their valid canonical baseline. Load preserves a valid context choice without rerolling; missing/unavailable assets use a safe eligible fallback. No new unlocks, free wardrobe generation or retroactive changes to photos/history. Active scene appearance locks release only at their authored boundary; queued room changes apply afterwards.

Extend the activity inventory with optional dress category/required appearance and the room registry with optional dress context. Validate that an event's dress rule, work uniform and current disguise do not conflict. Conflicts must be resolved in authored data rather than allowing random wardrobe selection to break a campaign. Formal tags describe specific venues/events; ordinary presence at a faction building is not sufficient.

## Migration, artwork and delivery gates (implementation)

Use one versioned migration transaction for actor rooms, active/pending events, work assignments, groups, guards and scene context. Create/validate references first, then update mirrored state together. Preserve original fields needed for legacy consumers until those consumers are converted. Invalid references use a safe same-building arrival only for idle actors; active mission/work records require their authored repair mapping. Never discard progress to hide a migration error.

No old transcript or completed event acquires a newly invented exact room. A mid-scene compatible restoration may place participants together only when the saved activity already establishes their participation. An unrelated person merely standing in the same building must not be pulled into the scene. Repeated loads do not reposition settled actors again or reset dwell timers, occupancy reservations or rewards.

Complete one vertical integration slice before rolling out room graphs everywhere: penthouse routines/companions; public café job/event; secure council/laboratory with guards; then remaining buildings. This is a dependency order, not a change in update priority. Activate a building only when its scheduled actors, work, campaigns, events, access and legacy mappings are covered. Otherwise keep its legacy single-scene behaviour; do not ship half-converted equality checks.

Every distinct explorable interior space requires its own dedicated image, as explicitly requested by the user. This includes halls, entrances, bedrooms, workplaces, meeting rooms, secure rooms and campaign interiors, not just major destinations. A separately displayed/navigable open-plan zone also requires its own view; a non-navigable activity hotspot within the same room can remain on that room's image. Separate rooms cannot share a generic building background or the same image under different filenames.

Art manifest entries need building/room or view ID, unique asset path, source/prompt provenance, dimensions, indoor/outdoor treatment and character-safe framing. Existing art can satisfy one matching space after visual review; shared reception/briefing art cannot satisfy both. Each image must depict its own layout, doors and room purpose while maintaining visual continuity with the building. Backgrounds must not bake in transient characters, guards or outfits that conflict with live occupancy or wardrobe switching.

Validate complete image coverage against the enabled room/view registry, file existence and duplicate image content; visually inspect distinctness as well as technical checks. Temporary generic backgrounds are development-only. Missing art blocks that space's release readiness; a graceful runtime error fallback does not count as completed artwork. Inspect empty, occupied, denied, waiting, compact and reopened-phone states. Art generation must not dictate access or invent occupants.

## End-to-end acceptance scenarios

Placeholder correction is part of release acceptance: the seven identified placeholder venues in the image inventory must render finished replacement art through in-person, arrival and preview routes. Include outdoor Silver Sands, retain its weather/wardrobe rules, and avoid double-counting six replacements already budgeted as new interior views. Audit missing-file fallbacks and protect generated art from the existing bulk primitive renderer. No active venue may retain a known simple placeholder at release.

| Scenario | Required observable result |
| --- | --- |
| Rei returns while Yuriko is home | Separate room activities, no cross-room chat/witnesses, knock/privacy works, household alias and save/load consistent. |
| Café shift plus a customer date | Worker has scoped kitchen access, date uses its reserved public/quiet space, no unintended shared attendance, work pays once and ends within existing hours. |
| Civilian Oculus promotion | Supervisor meeting reachable from reception; no criminal membership, secure-room or confidential identity access granted. |
| Crow and Ivan at Sunday council | Both route into chamber within allowed HQ domain; correct roster, eligibility, duration and attendance accounting; foyer guards cannot hear proceedings. |
| Takeo/Thirteen appointment | Existing briefing room IDs and fixed-location rules remain valid; wrong room cannot join; permitted visitors can reach the room. |
| Garrett's active legacy search | Old victories survive, new posts do not relock the critical route, private Charles encounter remains gated, loading cannot repeat rewards/disclosures. |
| Rei/Interpol/post-story mission | Stage-specific rooms, guard encounters, custody/solo restrictions and aftermath all resolve coherently; a neighbouring room cannot satisfy an objective. |
| Bubblegram accepted contract | Destination persists through save/load; phone directs physical work to in-person; outdoor assignments remain outdoors; access and payout unchanged. |
| NPC late or room unavailable | Honest status, accessible waiting/reschedule path, no teleportation, false attendance, silent venue switch or duplicated participants. |
| Permit expires with separated party | Correct safe reception/exit for each actor, no locked-in companion, no stolen command authority, existing work remains resumable as allowed. |
| Midnight / long time advance | Patrol replenishment stays distinct from mission clearance, scheduled departures and expiries execute in order, no duplicate event completion. |
| Custom protagonist and crew property | Player is never moved by NPC preferences; unowned property has no free guards; owned guard posts preserve paid roster identities and costs. |

All supported JobSeek physical action types and all campaign branches need inventory-driven validation, not just the representative UI scenarios. Release requires zero unmapped indoor activity entries, coherent access paths and documented actual regression/UI results. No gameplay pass is claimed by this design review.

## Review evidence and remaining implementation work

Reviewed both complete design documents and inspected current job catalogues, progression availability checks, world-loop initialization/advancement and co-presence, guard IDs/clearance, Charles quest privacy and guard prerequisites, and repeatable post-story mission routing. The findings above are source-supported design risks, not runtime reproductions. Checked document formatting and internal links after editing.

Still required during implementation: exhaustive source/catalogue inventory; actual schema/helper implementation; room/guard manifests and capacity values; migration fixtures; per-site difficulty calibration; generated/reused art review; runtime tests and rendered checks. Unestablished details such as dorm bathroom configuration can remain non-interactive/unspecified until resolved; they must not block a required route or be invented as historical canon.
