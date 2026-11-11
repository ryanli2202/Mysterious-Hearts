# Lived-In Interiors — public buildings, headquarters and events

**Parent:** [Interiors update plan](INTERIORS_UPDATE_PLAN.md)  
**Status:** Proposed; event room-assignment requirement requested by the user  
**Added:** 2026-11-11

**Cross-system review:** [Interiors integration review](INTERIORS_INTEGRATION_REVIEW.md). Its shared contracts resolve earlier tentative wording here, including added JobSeek staff rooms, fixed-character meeting attendance, local guard encounters and legacy migration. Read both documents before implementation.

**Production inventory:** [All room/image slots grouped by building](INTERIORS_IMAGE_INVENTORY.md) includes these graphs, required JobSeek support rooms, visitor restrooms and proposed bounded leader-residence subdivisions. Existing image reuse recommendations are provisional until full-size/render inspection; every new navigable space must receive its own row.

## Plugin task assignments

**Assigned:** 2026-11-11. Subplan of interiors; proposed layouts retain their decision status and runtime work remains pending.

Follow the [shared plugin workflow and evidence rules](PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Public/workplace and headquarters room graphs; event mappings | Story Skills + Writer's Loop | Review all twelve JobSeek roles, Bubblegram meetings, councils, laboratories and campaign venues against actual roles, chronology, privacy and permitted occupants. |
| Room-local security, schedules and meeting attendance | falsegreen-skill | Review assertions for actual room presence, stable legacy guard IDs, mission-versioned clearance, restricted leader movement and safe appointment migration; execute tests during implementation. |
| Room signs/access symbols and transparent character/prop layers | prompt-to-asset; Bulk BG Remove only where isolation is needed | Export only required local assets; check dark-phone handoffs and in-person room rendering. Dedicated full room illustrations remain a separate art-production task. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Required outcome

Public buildings and faction headquarters gain connected rooms, with characters working, relaxing and attending meetings in appropriate spaces. Previously established events and meetings that take place inside buildings must occur in specific rooms. All physical exploration, attendance, work and interaction stays in the in-person window.

Room assignments change where an established activity happens, not its participants, purpose, schedule, cost, prerequisites, disclosure permissions or outcomes. Existing named rooms retain their identities. The layouts below are proposed additions rather than claims that these rooms already exist in the game. Do not infer implementation approval from this specification.

## Layout and routine rules

Every distinct explorable interior space in these layouts requires its own dedicated image before release, including corridors, staff rooms, guard-post rooms and campaign/meeting spaces. Follow the parent plan and integration review's full image-coverage requirements; a shared building background is not sufficient.

`A ↔ B` is a bidirectional connection; braces indicate separate branches. Staff-only and secure branches require explicit permission. An open counter, dance floor or workbench can be a zone within one room: zones do not create artificial soundproofing or separate witnesses. Include appropriate bathroom access without using bathrooms as social or event destinations.

Resolve existing building schedules first, then room activities. Employment, faction shifts, booked meetings and campaign scenes take priority over optional room wandering. Active participants stay for their scene unless its existing rules allow interruption. Movement between rooms never rerolls attendance, consumes rewards or spawns encounters. NPCs must be physically present and available; staff labels do not automatically create new named characters or contacts.

Keep outdoor destinations outdoors. A park meeting, public frontage inspection, pier walk or courtyard scene must not be moved indoors merely to fit the room system. Covered markets use sheltered public zones; balconies and outdoor courts retain weather rules.

## Public and workplace layouts

| Building | Proposed room graph | Character placement and activity |
| --- | --- | --- |
| Campus café (`cafe`) | Entrance ↔ counter/seating room ↔ {quiet study room, staff kitchen}. | Maya serves at counter when scheduled; lunch visitors use seating, study visits use study room. Kitchen is staff-only. Agreed dates use an assigned seating area or quiet room, without assuming privacy in public seating. |
| Golden Dragon (`noodle_shop`) | Entrance ↔ dining room ↔ {service counter, kitchen}; kitchen ↔ staff office/store. | Garrett's existing shop shift uses kitchen and counter; customer conversations occur in dining room. Leadership business stays at the Red Dragons base. |
| Mario's Pizza (`marios_pizza`) | Entrance ↔ dining room/counter ↔ staff kitchen/store. | Food outings and existing visits use dining room; staff work behind the counter. No new named employees implied. |
| Chess café (`chess`) | Entrance ↔ café room ↔ playing room ↔ lesson alcove. | April's scheduled practice uses playing room; booked tutoring uses lesson alcove. A lesson alcove shares witnesses unless enclosed in the final design. |
| Petal & Stem (`flowers`) | Entrance ↔ shop floor ↔ arrangement workroom ↔ stockroom. | Emily's shift alternates serving and arranging; deliveries depart from workroom. Casual shoppers cannot follow her into stock storage. |
| Gift boutique (`boutique`) and mall (`shopping_mall`) | Boutique: entrance ↔ display/counter room ↔ staff store. Mall: concourse ↔ {shop units, food seating, customer service}. | Shopping visits stay in public areas; retain existing local routines and named retailers. Mall navigation must not invent purchases or shop ownership. |
| University (`campus`) | Main lobby ↔ teaching corridor ↔ {lecture room, seminar room, study room, theatre workshop}; theatre workshop ↔ rehearsal room. | Minsu's classes use lecture room; Amy's philosophy seminars use seminar room; April's research uses study room; Yuriko's lectures/workshop/rehearsal use the corresponding spaces. Preserve exact existing class times. Distinct classes can share a room only when their schedules permit. |
| Track (`track`) | Outdoor track ↔ pavilion lobby ↔ {changing facilities, coaching room}. | Sophie trains on the outdoor track, with review sessions in coaching room only when appropriate. Do not turn running into an indoor event. |
| Downtown studio (`studio`) | Reception ↔ corridor ↔ {photo studio, dressing room, recording booth, choreography room, review room}. | Rei's modelling uses photo studio/dressing room; Ivan's vocals, recording and choreography use corresponding workrooms. Publicity discussions use review room. Shared destination does not make every worker witness every session. |
| Arena lounge (`arena`) | Entrance ↔ lounge ↔ {training hall, coach review room, changing facilities}. | Samantha's training/sparring and Minsu's competition preparation use training hall; Sylvanis watches only when his current schedule places him there. Coaching reviews use review room. |
| East Ward Boxing Club (`boxing_club`) | Entrance ↔ reception/lounge ↔ training hall ↔ {equipment room, changing facilities}. | Tyler teaches and Neo attends controlled drills in training hall; glove repairs use equipment area. Training partners must actually be present. |
| Iron Circle (`iron_circle`) | Controlled entrance ↔ spectator lounge ↔ ring hall ↔ {fighter preparation room, recovery room}. | Rei/Samantha's authored bouts occur in ring hall; preparation and coaching use fighter room. Preserve 20:00 opening, fighter eligibility, champion state and all combat outcomes. Spectators do not gain backstage access. |
| Public library (`library`) | Lobby/desk ↔ {reading room, stacks, reservable study room}. | Reading visits use reading room; existing research goes to the relevant desk/stacks. Quiet meetings use study room when available. |
| Old town archive (`archive`) | Public desk ↔ reading/records room; staff door ↔ conservation workshop ↔ restricted storage. | Lena restores photographs and Alyssa repairs books in workshop; public city-site research occurs in records room. Neither public access nor friendship unlocks restricted documents. |
| Station makerspace (`makerspace`) | Welcome room ↔ shared workshop ↔ {electronics room, tool store}. | Dev hosts repair sessions and Neo repairs electronics in appropriate workshop zones. Tool-store permissions remain distinct from attending a session. |
| Riverside cycle workshop (`cycle_shop`) | Customer counter ↔ repair room ↔ parts store. | Naomi serves customers at counter and repairs bicycles in repair room. Visitors wait in the customer area unless invited. |
| Hilltop planetarium (`planetarium`) | Lobby/exhibits ↔ dome theatre; staff corridor ↔ preparation room. | Celeste prepares demonstrations in preparation room, presents in dome and answers visitors in lobby. A room change does not invent a scheduled public show. |
| Bijou cinema (`cinema`) | Ticket foyer ↔ auditorium; staff corridor ↔ projection room. | Daniel works in projection room and meets friends in foyer when free. Film outings use auditorium; conversation does not grant projection access. Preserve existing screenings/activities rather than adding a timetable here. |
| Municipal boathouse (`sailing_club`) | Reception ↔ rigging workshop ↔ equipment store; reception ↔ outdoor launch. | Valentina prepares boats in workshop and teaches at the launch/water where existing activities require. Preserve faction-work overrides rather than duplicating her at the boathouse. |
| Lantern market (`market`) | Public stall area ↔ community dining room ↔ staff kitchen/store. | Rosa coordinates the community kitchen, shoppers visit stalls, meals use dining room. Keep outdoor stall conditions where applicable. |
| Bowling alley (`bowling_alley`) | Reception ↔ lane hall ↔ lounge. | Existing bowling action belongs to a lane zone; waiting companions use lounge. Preserve existing fees and outcomes. |
| Arcade (`arcade`) | Counter ↔ cabinet floor ↔ seating area. | Cabinet play uses cabinet zones; companions can wait nearby. Physical arcade play remains in person, with existing game state preserved. |
| Afterglow (`nightclub`) | Entrance ↔ dance hall ↔ lounge; staff branch ↔ service room. | Dance outings use dance floor; conversation uses lounge. Preserve opening-time rules and admission costs. |
| Copper Lantern (`bar`) | Entrance ↔ bar/seating room ↔ staff service room. | Ordering and drinks use counter/table zones. No private room or secrecy inferred from sitting at a table. |

### Outskirts buildings

| Venue | Proposed graph and routine placement |
| --- | --- |
| Hillside Tea Room (`hill_tea_room`) | Entrance/counter ↔ tea room ↔ staff kitchen. Euan's existing service presence stays here; tea visits use tables. |
| Farm shop (`farm_shop`) | Entrance ↔ produce hall/counter ↔ staff store. Existing staff and juice action use counter; browsing uses produce zone. |
| Old Mill pottery studio (`pottery_studio`) | Entrance/display room ↔ pottery workshop ↔ restricted kiln room. Jonah's work uses workshop; the existing display visit stays in display room, not a newly invented class. |
| Marine discovery centre (`marine_centre`) | Lobby ↔ exhibit hall ↔ education room; staff service branch remains restricted. Existing exhibit visits stay in hall; education-room sessions require an actual authored event. |
| South Harbour covered market (`harbour_market`) | Sheltered entrance ↔ stall aisles ↔ public seating; vendor storage restricted. Preserve existing vendor/local schedules and sheltered conditions. |
| Railway museum (`railway_museum`) | Ticket lobby ↔ collection hall ↔ archive/education room. Existing collection visit stays in hall; archive access is separately controlled. |
| Riverside diner (`southbank_diner`) | Entrance ↔ dining room/counter ↔ staff kitchen. Existing sandwich and shared lunch use dining room. |

## Faction headquarters and controlled sites

Room labels visible to visitors must follow existing discovery rules. Public reception does not expose secret affiliation, occupants or restricted room names. Keep map travel targeted at the building or existing authorized entry point; a scheduled room is not a fast-travel bypass.

| Building | Proposed graph | Routine and meeting placement |
| --- | --- | --- |
| Waterfront executive offices (`syndicate_office`) | Public lobby ↔ appointment room; guarded route ↔ existing underground HQ entrance. | Ivan's Joker-network diplomacy uses appointment room. Public transfer-record enquiries remain at public desk/frontage as authored. HQ remains a separate controlled destination. |
| Syndicate underground HQ (`syndicate_hq`) | Security foyer ↔ internal corridor ↔ {council chamber, executive meeting room, cross-branch operations room, members' lounge}. | Weekly face-card council uses council chamber; Crow diplomacy uses executive meeting room; Ivan's ordinary cross-branch work uses operations room. Aces' staggered appointments use executive/operations room according to appointment type. The Crow remains within HQ; no residence or routine trips are invented. |
| Red Dragons lounge (`syndicate`) | Entrance ↔ members' lounge ↔ {council/meeting room, community liaison room, office}. | Garrett's 20:00 leadership work and diplomacy use meeting room; civilian grievances use liaison room when the authored work calls for a private hearing. Preserve refusal of narcotics revenue and existing membership rules. |
| Kestrel (`site_01`) | Frontage ↔ existing reception ↔ secure corridor ↔ {existing briefing room, operations office, guarded service area}. | Takeo remains assigned to `site_01_briefing`, including leadership meetings. Reception work stays in reception. New offices do not relocate him or create additional command rights. |
| Pacific Relay (`site_02`) | Frontage ↔ existing reception ↔ secure corridor ↔ {existing briefing room, dispatch room, warehouse}. | Thirteen remains at `site_02_briefing`; logistics staff use dispatch/warehouse only where actual roster and duties permit. No forced home/outings schedule. |
| Stillwater (`site_03`) | Frontage ↔ reception ↔ secure corridor ↔ {briefing room, research office, restricted laboratory}. | Existing assignments stay in reception/briefing. Research-room presence grants no new experiment, captive or evidence discovery. |
| Breakwater (`site_04`) | Frontage ↔ reception ↔ secure corridor ↔ {briefing room, equipment room, maintenance bay}. | Valentina's 10:00–13:00 operations review, Ivan's rotation and Martos's appointed work retain the existing briefing destination. |
| Aster (`site_05`) | Frontage ↔ reception ↔ secure corridor ↔ {briefing room, production room, editing room}. | Elias's public 14:00–17:00 appointment stays at reception as currently authored; private operational appointments use briefing. Do not silently move established public work behind a locked door. |
| Meridian (`site_06`) | Frontage ↔ reception ↔ secure corridor ↔ {briefing room, accounts office, restricted records room}. | Camila's and Ivan's site appointments use existing briefing. Accounting staff may work in accounts office; records remain permission-gated. |
| Oculus (`site_07`) | Frontage ↔ reception/public display room ↔ controlled corridor ↔ {briefing room, corporate office, data wing, security room}. | Preserve Martos/Camila weekday 09:00–11:00 reception work and 11:00–17:00 briefing assignment. Later room specialisation requires an explicit schedule revision, not an accidental migration. No visitor-pass route into operations. |
| Greyglass (`site_08`) | Frontage ↔ reception ↔ secure corridor ↔ {briefing room, equipment workshop, restricted store}. | Mavis's existing private appointments use briefing; generic servicing uses workshop when authorized. No civilian-identity or assassination information leaks through room names. |
| Glasshouse (`glasshouse_lab`) | Cleared entrance ↔ internal corridor ↔ {laboratory workroom, private review room, records room, rest room}. | Sylvanis's research uses workroom; existing laboratory reviews use private review room. Charles remains within the Glasshouse, with rest permitted only inside it. Record access, private reunion and research reviews retain their separate story and knowledge gates. |
| Interpol regional HQ (`interpol_hq`) | Public lobby/verification desk ↔ secure corridor ↔ {existing `interpol_briefing`, `interpol_training`, `interpol_containment`, case office}. | Gordon receives reports in case office, trains in existing hall and reviews cases in existing briefing room. Fox's liaison uses case office or a booked briefing. Public exhibit verification and repeatable-operation intake remain at public desk. No change to Geneva's global-HQ role. |
| Blackstone (`blackstone_hq` plus existing wings) | HQ reception/security ↔ controlled corridor ↔ {`blackstone_loading`, `blackstone_records`, `blackstone_lab`, `blackstone_command`}. | Keep existing wing identities and authored campaign order. Record recovery uses records; laboratory scenes use experimental wing; Richter command confrontation uses command where the existing stage specifies it. Do not bypass guard encounters or solo requirements through new corridors. |

Guards occupy specific door posts or patrol routes. The user's follow-up requires expanded guard rosters across interior rooms, not merely redistribution of existing guards. Add explicit new deployment slots under the rules below; moving an existing guard must not duplicate that guard, respawn a defeated campaign guard, remove a required encounter or grant authority. Coordinate command rules with the guard plan; ordinary briefing permission and command authority remain distinct. Existing permit expiration/pressure suspension returns occupants to the correct reception without losing assignments.

### Smaller faction bases and owned properties

Each base has entrance ↔ public waiting space ↔ controlled meeting room. Add the following branches, retaining existing leader residence facts and invitations:

| Base | Proposed branches and routine |
| --- | --- |
| Lantern House (`lantern_house`) | Office and stairs to Mara's private flat; she receives appointments in meeting room and repairs radios privately when off duty. |
| Saints Rail Depot (`saints_depot`) | Dispatch/workshop and Darius's converted office residence; meetings in meeting room, clock restoration in private work area. |
| Purple Skulls (`purple_clubhouse`) | Members' lounge, garage and Rafe's upstairs residence; maintenance in garage, negotiations in meeting room. |
| Kurose House (`hamayashi_house`) | Reception hall, meeting room, records room, bonsai courtyard and private rear residence; Daichi's visitors and authored testimony use meeting room, record inspection uses records room only when authorized. |
| Los Rojos (`rojos_courtyard`) | Outdoor courtyard, offices/meeting room and Isabel's upstairs residence; meetings indoors unless explicitly authored for courtyard, guitar practice remains private. |
| Waterfront Consortium (`consortium_house`) | Waiting room, boardroom, office and private residential area; Evelyn's leadership meetings use boardroom. Detailed residential layout needs a separate source review. |
| Hamayashi annex/supply house | Preserve `hamayashi_annex` and `hamayashi_store` as existing sites. Annex: entrance ↔ meeting/office room; supply house: entrance ↔ stock hall ↔ office. Campaign clearance remains site-specific. |
| Four purchasable crew properties | West workshop: entry ↔ workshop ↔ office; dock warehouse: entry ↔ warehouse ↔ meeting office; northern offices: reception ↔ meeting room ↔ workroom; south garage: entry ↔ garage ↔ office. Owned use determines allowed activities; unowned properties do not gain a leader, gang or staff automatically. |

## Established events: explicit room assignments

These are proposed destination mappings for existing activities, not newly created meetings. Preserve existing named-room destinations verbatim. Inventory all additional event producers before release; this reviewed table is a starting migration catalogue, not a claim that every campaign stage was audited.

| Existing event or activity / source | Assigned room and preserved conditions |
| --- | --- |
| Weekly face-card council (`syndicate_council.py`) | HQ council chamber. Preserve Sunday 20:00–21:00, roster, Jack-and-above eligibility, Ivan's mandatory attendance, 45-minute attendance threshold and once-only resolution. Time in foyer/lounge does not count. |
| Leadership negotiations (`crime_diplomacy.py`) | Red Dragons meeting room; Joker-network waterfront appointment room; Crow's HQ executive meeting room; Takeo's existing `site_01_briefing`; other leaders' base meeting rooms/boardroom. Keep attendee, agenda, deal state and booked time. |
| Player appointments and Meet-Cute dates (`scheduled_events.py`) | Assign a room compatible with activity and current access: café seating, library study room, cinema auditorium for viewing, home living room for an ordinary home visit. Explicit existing room wins. Unknown free-text intent defaults to an appropriate public/shared meeting room, never a bedroom, secure lab or inferred private date. Preserve mutually accepted venue and guests. |
| Careers and booked shifts (`careers.py`) | Modelling/photo studio, vocals/recording booth, choreography room, noodle kitchen, Iron Circle preparation/ring rooms, arena training hall, Red Dragons meeting/liaison room, HQ cross-branch operations room. Multi-stage activities explicitly change rooms at stage boundaries without duplicating pay or time. |
| Faction cover/operational appointments (`faction_work.py`) | Keep all existing `site_*_reception` and `site_*_briefing` assignments. Glasshouse reviews use private review room; staggered HQ appointments use appropriate executive/operations room. Preserve precedence where shifts overlap. |
| Reception packets and briefing disputes (`crime_operations.py`) | Existing reception/briefing rooms remain authoritative, including permit expiry, pending choices, rewards and branch authority. |
| Public record research and exhibit verification (`crime_sites.py`) | Archive records room and Interpol public verification desk respectively. Exterior site inspection stays outside. No secret evidence appears merely from entering an archive. |
| Glasshouse research/supply brief and specialist reviews (`criminal_dynamics.py`, `laboratory_missions.py`) | Private review room, with required people and disclosure clearance checked in that room. Outer building clearance still applies to everyone. Unseen people elsewhere neither hear the briefing nor acquire its secrets. |
| Charles reunion and related campaign scenes | Explicit private Glasshouse room for the reunion, chosen by the authored stage; combat stays in its stage-assigned encounter room. Preserve discovery, prerequisite victories, solo/party rules, disclosures and completed reunion state. Presence in Charles's workroom cannot trigger an unearned reunion. |
| Rei's What Remains (`rei_story.py`) | Home sketchbook scene in Rei's art space; Kurose House testimony in meeting room and actual document inspection in records room; Blackstone stages retain their corresponding wing/room. Other scene destinations require per-stage review before migration. |
| Interpol cases (`interpol_cases.py`) | Existing `interpol_briefing` reviews stay there; public intake at HQ desk; field investigations and encounters remain at their authored destination, with a specific room where indoors. An outdoor transfer verification remains outside. |
| Existing home hangouts, lessons and shared meals | Living room for ordinary conversation, kitchen/dining room for meals, appropriate workspace for a supported lesson. Private bedroom access is never inferred from a generic home invitation. |
| Flashbacks and authored past scenes | Assign rooms within the historical scene's own setting only when supported. Do not move present-day NPCs, rewrite historical text to claim an unestablished room, or turn a flashback into a present appointment. |

## Event records, navigation and compatibility

Use the integration review's canonical building/room/zone registry and versioned event-room references. Exact field names remain an implementation decision. Event identity remains stable. Room references must resolve through the same room registry used by characters, access and UI.

For new events, resolve and save the room at booking/scene creation, validate venue membership and guest access, and show Building › Room in confirmations/reminders. Building travel arrives at the entry, followed by in-person directions. Attendance begins only after actual room arrival and the existing join conditions; nobody gains attendance credit for standing in reception. Invitations are not credentials. Locked or occupied destinations produce a clear wait/reschedule path without silent relocation or rewritten consent.

Use existing schedule precedence for conflicts. Exclusive rooms such as council/private interview rooms can be reserved; public cafés can hold separate groups but groups do not automatically merge. Waiting participants do not leak meeting contents to bystanders. Any change to an agreed room must be visible to participants and recheck access. Never silently change the building or event time.

Legacy migration rules:

- Preserve event IDs, times, guests, cancellation, attendance totals, pending choices, outcome flags and memory records. Add room metadata idempotently; do not recreate events.
- Preserve an existing room ID. Resolve building-only pending events through an authored event-type mapping. Only generic casual events may fall back to an appropriate shared room; campaign/work stages require explicit mappings. Unresolvable/removed rooms require explicit repair, not restricted access or dropped events.
- Active scenes receive a compatible room and consistent saved-participant positions atomically during versioned migration, preserving accrued attendance and progress. This restores an already-running scene; it never recruits bystanders or performs new travel. Do not replay entry combat, rewards, dialogue, reunions or membership grants. Revalidate access under existing story-authorized exceptions.
- Completed/cancelled events remain historical facts. Do not rewrite transcript text or assert an exact historical room without evidence; a compatibility mapping for future mechanics must not fabricate old knowledge. Upcoming occurrences use the new room normally.
- Mid-journey saves retain their destination building and continue to its normal arrival point. Remember the event room for subsequent navigation without teleporting through guards.
- Update all venue equality checks deliberately: building-level discovery/travel and room-level interaction/attendance are different requirements. Audit player, NPC, companion, group, calendar, career, dialogue, memory, witness, scene-art and map code together.

## Required integration extension — 2026-11-11

The user explicitly requires campaign buildings/rooms, Bubblegram meetings, JobSeek jobs and related activities to use the interiors system; character schedules and preferred places must reflect it; more guards must be stationed across different rooms. These are required parts of the planned update, not optional polish. The overall update remains Proposed and no implementation is claimed.

### Campaign, Bubblegram and JobSeek coverage

The event inventory must cover every campaign stage and branch, repeatable mission, career, app-originated physical assignment, interview, project, meeting, training session, date and hangout. Include both existing records and events generated after the update, with canonical and custom protagonists. Do not limit room support to calendar appointments or the sample mappings above.

| Integration | Required room behaviour and preserved state |
| --- | --- |
| Campaigns | Map each indoor stage's entry, dialogue, evidence, encounter and aftermath to explicit rooms. Multi-room missions follow connected routes with stage-specific gates. Review all campaign implementations and scene catalogues, not only Rei/Interpol examples. Preserve objective order, solo/party restrictions, required battles, named participants, outcomes and completion flags. A mission cannot be completed by standing elsewhere in its building. |
| Bubblegram contracts and workplace actions | Audit `job_apps.py`, `bubblegram_roles.py`, `bubblegram_progression.py`, `bubblegram_workplace_ui.py` and diplomacy integration. Existing briefing-room mandates retain those rooms; HQ work uses operations/meeting rooms. Negotiations use the leader's assigned meeting room. Physical handovers/reviews must have an explicit interaction location. Keep genuinely outdoor downtown/market assignments outdoors; a district-only indoor assignment needs an authored building and room, never an arbitrary hidden HQ. |
| JobSeek shifts and progression | Audit `job_apps.py`, `jobseek_progression.py`, `jobseek_workplace_ui.py`, `job_apps_ui.py` and career booking integration. Assign each job's actual tasks to its workplace rooms, including supported interviews, projects and promotion reviews. A café shift may move between service and staff kitchen while review occurs in an appropriate staff room. Job-specific access is scoped to the shift/task and does not grant unrelated restricted access. |
| App-to-world handoff | Phone apps may advertise, accept, schedule and show directions. Starting/performing physical work or attending a meeting opens the in-person flow and requires actual arrival in its room. Preserve online-only actions as online. Buttons cannot finish physical tasks remotely or teleport through controlled doors. |
| Pending work and rewards | Save the assigned room(s), stage and required attendees alongside stable assignment identifiers. Preserve deadline, pay, experience, promotion, reputation, budgets, pending choices and once-only completion. Reload or walking between task rooms cannot reset work, multiply payouts or extend deadlines. |

For each catalogue entry, record source module and stable activity ID, building, room(s), activity stage, access/participants, scheduling producer, completion consumer and legacy-save mapping. Audit UI shortcuts and generated prose against the same mapping. Dialogue may describe the current room but cannot invent a move, witness, access grant or completed objective.

### Schedules and preferred places

Extend `world_loop.py`, `leisure.py`, public venue suitability, faction-work appointments, local resident routines and agreed peer plans to resolve both a building and a room/activity preference. Preserve the character's established interests rather than assigning every idle NPC to reception.

- Resolve campaign/active event obligations, work shifts, travel and existing schedule precedence before leisure. Home-room preferences from the parent plan apply whenever the character is at home.
- Give preferences room/activity targets: April favours chess playing/study spaces; Amy favours suitable painting/study areas; Yuriko alternates model-work and bedroom/living-space downtime; Neo favours repair work and home co-op space; a guard favours an assigned duty post rather than civilian leisure rooms while on duty.
- Retain building-level variety and add room-level recent visits, dwell time and availability. A new room must not erase established favourite venues or make characters remain indoors all day.
- Filter room choices by opening hours, access, weather, activity suitability, appointments and actual capacity. No preference grants a key, reveals a hidden site or overrides a private booking.
- Compute crowds both by building and by room as appropriate. Characters in different rooms are not automatically together. Peer plans choose a shared accessible room and coordinate arrival; household members retain independent activity choices.
- Persist chosen room/activity and relevant recent-room history so refresh/load does not reroll occupants. Use safe defaults for older saves. Occupancy shown to the player remains constrained by observation/knowledge, not the scheduler's omniscient data.
- NPC moves use real connections with meaningful dwell periods. Wrap up an interruptible interaction before leaving; preserve active-player control and scripted scene locks. Travel remains a distinct state, with no simultaneous occupancy at both ends.

### Expanded interior security rosters

Author a deployment manifest per guarded building: stable post ID, room/door, guard type, explicit headcount, duty window, authority, patrol connections (if any), visibility, encounter participation and respawn policy. New guards are distinct saved entities/slots. Existing portraits/types can be reused without cloning an existing guard's identity or encounter state.

Proposed starting allocation for review; exact numbers need per-site balance checks. This is not a ceiling or permission to reduce existing larger deployments. The integration review requires a before/after manifest preserving existing identities and adding the necessary room posts:

| Building scale | Proposed staffed posts |
| --- | --- |
| Major faction headquarters | 2 at entrance/security, 2 at the principal secure corridor, 2 outside command/council access, 1 at each separately protected records/lab wing, and a 2-person reserve/patrol if the authored layout supports it. Populate only actual rooms; some posts can cover multiple adjacent doors. |
| Branch depot, research or corporate site | 1–2 at entry, 1–2 at controlled corridor, 1 outside briefing/command and 1 at each sensitive storage/data/research branch. Use that organisation's established guard types. |
| Smaller gang base | 1 lookout at entry, 1–2 guards at meeting-room approach, and 1 at a separately protected store/residential boundary when justified. Do not occupy private bedrooms as ordinary posts. |
| Interpol and Blackstone | Explicit manifests using their existing organisations' types and authority rules; protect interview/containment, records, lab and command boundaries as appropriate. Guards at separate posts are not automatically one encounter. |
| Owned crew property | Scale posts to purchased property, actual ownership and supported staffing rules. Do not create free guards at an unowned/vacant property or bypass recruitment/cost limits. |

Expand rosters where the new layout needs coverage, and record the actual old/new counts when implemented. Avoid a full combat gauntlet at every door: authorized movement passes posts normally. Discovery, greetings, warnings and challenges depend on the particular guard's knowledge and assigned boundary, with MH-003 command exceptions preserved.

Define local encounter scope explicitly. Only guards at the encountered post and authored reinforcements participate; no whole-building omniscient aggro or automatic attacks from unseen rooms. If reinforcement is supported, its route, trigger and arrival must be authored and visible in gameplay. Doorway guards cannot hear all conversations throughout the building.

Save migration must preserve defeated existing guard IDs and campaign clearance. Do not relock completed missions by adding new mandatory enemies behind the player. Pending missions need a versioned roster decision that preserves already earned progress; proposed default is to retain their required encounter set, with additional posts non-blocking until a future eligible encounter. New encounters use the expanded balanced roster. Keep ordinary patrol replenishment distinct from non-respawning campaign guards and avoid repeated rewards from room changes.

### Added acceptance requirements

- Every indoor campaign/Bubblegram/JobSeek catalogue entry has a validated building/room mapping and a real in-person completion path; explicit outdoor exceptions stay outdoors.
- Test one multi-room campaign, one Bubblegram meeting/contract and each distinct JobSeek task flow, including wrong-room attempts, unavailable participants, restricted doors, deadline expiry and reload during active work.
- Verify unchanged payouts, promotions, reputation, budgets, victories and completed story flags after migration and repeated room transitions.
- Verify favourite building/room selection, weekday/free-day behaviour, peer meetings, unavailable-room fallback and stable save/load occupancy without dragging the active player around.
- Verify per-room guard headcounts, unique IDs, duty changes, local encounters, permitted passage, expired clearance, campaign-clearance migration and no respawn/reward farming by changing rooms.
- Review difficulty for expanded security before releasing: additional stationed guards must not silently invalidate existing campaign balance or authored outcomes.
- Run relevant JobSeek, Bubblegram, campaign, guard, leisure, world-loop, save and workplace UI checks alongside the parent plan's checks. Phone changes require dark-theme smoke and visual inspection. No checks are marked passed during planning.

**Additional evidence:** Inspected Bubblegram role venues and progression, JobSeek workplace progression and `job_apps.py` assignment/location guards, plus `leisure.py` venue filtering, crowd counting and recent-place logic. The current plan's earlier guard-redistribution wording has been superseded by explicit roster expansion. Full call-site/catalogue audit and numerical deployment balance remain pending.

## Milestones and acceptance (implementation)

- [x] Review public venue, faction site, shift, council, diplomacy, scheduled-event and selected campaign sources; draft layouts and mappings.
- [ ] Complete a machine-readable inventory of every indoor event/scene/meeting producer, existing location, destination room, access rule and save migration. Include other campaigns and dynamic activities not individually reviewed here.
- [ ] Implement shared room navigation, worker routines, guard posts and event-room records.
- [ ] Migrate old scheduled/active events and update every join/attendance/interaction check.
- [ ] Produce room artwork and inspect public, secure, occupied, waiting and denied states.
- [ ] Verify all existing event outcomes and saved progress; publish evidence only after checks run.

Required checks include: council foyer versus chamber attendance and no duplicate resolution; each diplomacy target; preserved existing named-room meetings; public appointments without secure-room access; arrival without teleportation; companions with differing permissions; private brief witnesses; same-building different-room NPC conversations; staff departures; existing shift overrides; guard/campaign progress; repeat load during an active event; old completed-event history unchanged; outdoor events unchanged; custom protagonists and player-controlled movement; all indoor inventory entries mapped or explicitly blocked with a documented reason.

Run relevant existing council, scheduled-event, diplomacy, career, crime-site/operations, laboratory, campaign, world-loop and save tests plus new room-integration checks. Inspect the new layouts and event states in person. Calendar/reminder/Maps changes must retain dark phone controls and pass `tests/phone_dark_theme_smoke.py` and relevant feature smokes. Delivered changes require detailed patch-note evidence, validation and export under the parent plan. Planning alone is not a release.

**Evidence (2026-11-11):** Source inspection only: `town.py`, `public_venues.py`, `outskirts.py`, `crime_sites.py`, `organisation_guards.py`, `gang_leaders.py`, `faction_work.py`, `scheduled_events.py`, `syndicate_council.py`, `crime_diplomacy.py`, `careers.py`, `criminal_dynamics.py`, `laboratory_missions.py`, `charles_han.py`, `rei_story.py` and Interpol definitions/cases. No runtime changes, art generation, event migration, gameplay tests or rendered UI checks performed. Full campaign/event inventory remains pending.
