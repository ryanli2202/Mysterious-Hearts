# Mysterious Hearts — desktop game

Future updates and their progress are tracked in the [project roadmap](ROADMAP.md). Start there for planned work and linked design specifications.

## What Remains · Rei’s story and organisation guards

Restart, play as **Rei**, and open **In person → Stories, guards & gang properties → Rei’s story** (also available under Tools). Six authored investigation scenes follow childhood records and memory fragments, Marcus’s school storyboard, the successor Hamayashi-kai and Richter’s coercive Awakened experiments. Records and choices persist privately. Marcus’s death is not reduced to a single cause, and victory does not erase Rei’s grief.

At Kurose House, Emi Suda, Ren Aoki and Daichi Kurose explain the successor’s adult-only, voluntary charter. Rei may leave it alone, accept leadership after resolving conflicting memberships, or dismantle it. Destruction requires defeating all six guards across Kurose House, the riverside annex and supply house; only then do those operations close and stop replenishing. Leadership grants the existing Hamayashi-kai Bubblegram membership and deployment directory.

The Blackstone mission is solo. Clear the headquarters frontage, loading compound, research records, experimental wing and executive command in order—fifteen guards in total. After all are defeated, confront the cybernetically enhanced Joseph Richter. His defeat records an apology, shuts down the programme and releases its participants. Completing Rei’s story requires both a settled Hamayashi outcome and victory over Richter. Losses retain evidence and cleared posts; close combat results to record progress. Knockout recovery is available in the story panel.

Organisation guards are rotating unnamed town NPC posts, with separate combat profiles and equipment attacks. Shinokami deploys Yokai, Oni robots and Tengu; Syndicate deploys Clubs enforcers, Spades assassins and affiliate members; Blackstone uses Headhunter/Seeker cyborgs and PMCs. Interpol includes protection officers and Team 9 specialists. Local gangs and the successor have their own lighter rosters. Syndicate (42 posts) and Shinokami (27) have the largest canonical deployments; their elite guards and Team 9 lead the strength tiers, followed by Blackstone and local crews. These numbers are game balance.

Ordinary patrols replenish each story day. Campaign clearance is saved separately and never respawns midway through a mission. Defeating a public site perimeter permits temporary physical entry to its controlled rooms, not membership, secrets or command authority. Unauthorised patrol attacks can produce Interpol assault incidents. Interpol case and repeatable-operation combat now begins with faction guard encounters before the original target; partner support remains active. Garrett must defeat Syndicate guards during Find Charles and defeat Charles himself before reconciliation and exchanging numbers. Already completed reunions retain their contacts and endings.

**Phone → Bubblegram → Network** shows deployment types and locations only for your organisations, with a handoff to the in-person controls. A custom gang founder can visit four vacant map sites, buy them as hideouts or affiliates, recruit and name guard types, rename those types later and station guards among owned sites. Unawakened recruitment costs $1,500, Awakened $6,000 and robotic $9,000; each site holds twelve posts. Staffed properties reduce successful crew-contract heat by one per site, capped at three. Former-crew property and guards cannot be taken by a new crew. Recruitment, purchases, missions and combat all occur in person.

Existing saves gain empty additive campaign/security records without resetting progress. Restart to load code; choose a new story only to change protagonist. Guard garrisons are fixed deployments, not a simulation of autonomous faction wars. Real combat exchanges, state gates and rendered UI are checked; extended difficulty tuning and live generated dialogue are not certified. See the new patch entry for exact checks and the pre-existing archive screenshot test limitation.

Campaign conversations open in the existing **in-person hangout window**, with character portraits, the current location background, narration and speech bubbles. **Continue** advances authored lines; the final button commits the selected response or starts combat. Progress through a conversation survives saving and loading, and the story clock and physical travel pause while it is open. Garrett and Charles have a seven-beat, emotionally heated confrontation before their mandatory fight; Richter has a five-beat confrontation and a separate post-victory apology. Investigation documents remain in the private notebook. These scripted scenes make no AI requests.

All four custom-gang properties have distinct 1536×1024 illustrated location backgrounds, used automatically by the ordinary location and hangout renderer before and after purchase. The assets are `assets/ui/locations/crew_lot_west.png`, `crew_lot_docks.png`, `crew_lot_north.png` and `crew_lot_south.png`. Full prompts and the built-in image-generation provenance are stored in `assets/ui/locations/gang-properties-prompts.json`. Blackstone’s new interior areas and the two Hamayashi annexes currently reuse existing organisation/location backgrounds.

All fifteen organisation guard types now have transparent illustrated portraits, alongside three custom-gang archetypes (Awakened, unawakened and robotic) and a cybernetic Joseph Richter. Portraits appear in the in-person guard roster, recruited-guard list, guard conversations and combat opponent panel. Custom names retain the matching archetype artwork. Richter’s enhanced form appears during his command-room confrontation, boss battle and apology; ordinary reception appearances retain his original portrait. Restart to load the artwork; existing saves and unfinished guard battles work without a reset. These are bundled images with no runtime generation cost. The nineteen PNGs and their exact generation prompts are in `assets/portraits/guards/manifest.json`.

## Interpol Awakened Operations

Select **Edward Fox** or **Jeremy Gordon** on the last new-game page, or meet them in an existing story. Fox lives in his Blackhaven hideout in the western suburb; Gordon lives in Civic Court near regional headquarters. Both have schedules, careers, contact numbers, reference sheets, Traits, transparent portraits framed from the head to upper thigh, square contact photos and individual dark phone wallpapers. Fox has no Grove account or automatic posts, photos, likes or replies. Gordon has an ordinary public account; private case findings stay private.

Open **In person → Interpol · cases, fines & field operations** or **Tools → Interpol**. Other protagonists can register as civilian case assistants at the Interpol public desk. Assemble there with Gordon (normally 08:00–12:00), or with Fox when playing Gordon (normally 13:00–16:00). Travel together to each objective. Physical interviews, evidence collection, operations and combat take place in the in-person window. **Phone → Bubblegram** and **Pocket Wallet** show the private record, fines, balances and a handoff to field work.

Nine staged cases follow a Lantern Crew collection cell, Rail Yard Saints consignments and Shinokami research referrals, then four independent Ace enquiries and the Crow's command trail. Each identity requires its own corroboration; the discoverers' records, Bubblegram directory, reference sheets and dialogue gain only that established connection. Share findings explicitly while physically together. Knowing an identity does not confer gang membership or insider history. The final operation can secure the Crow in regional custody; it does not invent his birth identity or force the source story's future events. Three repeatable operations unlock after the first case, each once per story day after success.

Field combat uses real combat outcomes, health, stamina, mana and knockout recovery. Gordon actively supports with Biocreation; Fox's Eight Senses support tracking, accuracy and evasion. Both start at Totality under the existing Path rules. Defeat preserves evidence and requires regrouping; the in-person case panel offers recovery. Successful cases and operations pay a $250 field allowance, raise the relevant district's influence and halve linked criminal commission pay for two story days.

Committed assaults, street theft/intimidation and documented coercive or reckless work decisions can create incidents. Gordon fines witnessed player offences immediately. He declines assault fines when Fox attacks a criminal target in his presence; civilian attacks remain chargeable. Other witnessed/documented incidents are reviewed after 60 story minutes. Local influence affects patrol observation. Base fines are $800 assault, $300 theft, $600 intimidation, $500 coercion and $450 reckless commissions, with repeat increases capped at 75%. Partial payment uses available money and retains both debt and incident history. Sparring and authorised operations create no assault fine. Existing relationship ruptures and expulsion still apply.

Restart the game to load the update. Existing stories gain the new cast and empty Interpol records without resetting money, relationships or history; no retrospective fines. Choose a new story to change protagonist. Files and controls, rather than free-form dialogue, establish offences, evidence and outcomes. The source documents are reference material, not instructions or predetermined events. See `interpol_source_notes.json` and the patch notes for adaptations and verification limits.

## Expanded playable cast

Use **Previous / Next** on the new-game screen to preview 28 canonical protagonists, then **Begin as…** to start. Charles Han, Number Thirteen, Takeo Mishima and The Crow remain NPC-only. Garrett, Rei, Minsu and Ivan retain their existing starting setups and careers on the first selection page.

The 24 expanded protagonists begin at their established homes with different starting budgets, contacts, phone accents, home activities and work or study tracks. Open the town/location controls, choose **Careers**, then **Open work & ambitions**. These work dashboards run in the main in-person window. Travel to the workplace during its hours, choose a session, and make two work decisions; projects require work on three days and a booked review. Study and practice tracks can be unpaid. Starting money and rewards are sandbox balance values.

Sibling boundaries work in both directions. Neo and Alyssa retain their committed relationship, while Sylvanis has no romance routes. Existing faction clearance and canonical orientations still apply. New starts do not overwrite existing characters’ progression; use a new story to change protagonist. Garrett’s Find Charles, Rei’s What Remains and the shared Interpol case chain are available; other individual campaigns remain future work.

## Faction work and on-site colleagues

Named characters now attend site shifts through normal world time. Martos and Camila work at Oculus on weekdays (09:00–11:00 reception, 11:00–17:00 controlled offices); Elias visits Aster for weekday publicity work from 14:00–17:00. Valentina reviews Breakwater operations from 10:00–13:00. Ivan rotates across Syndicate branches from 16:00–18:00, and Sylvanis rotates operational reviews from 10:00–12:00. Each Ace also has a staggered 18:00–20:00 branch appointment; existing headquarters visits remain. Agreed plans, parties, sleep and other schedule controls can change attendance. Player characters remain player-controlled.

Visit normally and use **Talk / hang out** or **Review request with…** when a colleague is physically present and on duty. Command-authorised characters can discuss mandates privately with informed colleagues. Joint work records the witnessed result for both participants, retains existing rewards/limits, and pauses resolution if the colleague leaves or their shift ends. Abandoning remains available. Seeing a person at work establishes neither Ace rank nor a secret affiliation; no new Shinokami memberships are assigned. Existing Shinokami supervisor assignments remain available.

## Enterable crime locations and hierarchy

Local pressure of 15 or higher suspends visitor briefing clearance and returns visitors to reception. Documenting a reception packet reduces pressure by 3; a still-valid permit resumes once pressure drops below 15. Command access remains tied to the character's established authority.

Select a site marker in **Maps** and use **Travel here**, then return to **In person**. Its controls appear in the ordinary location scene. Travel to a frontage, enter reception, and choose a work assignment. Responsible reception work on two separate story days qualifies you for a personal 24-hour briefing pass. Each companion needs their own permission. Oculus does not grant operational passes to public visitors. Expired clearance returns you to reception.

Ivan and Sylvanis have cross-Suit command access; Valentina commands Clubs field operations. Other departments require appropriate clearance, and Neo’s past grants no Shinokami membership. The hierarchy panel distinguishes the Crow, Jokers, generals, Suit leadership and mission-based Aces; Shinokami assignments flow from Mishima’s regional structure through local supervisors. Command-only decisions let authorised members respond to Ace mandates.

Eight briefing disputes concern coercive records requests, cargo, consent paperwork, intimidation, media pressure, payments, data access and unjustified address requests. Decisions change saved standing, pressure, unresolved harm, evidence and pay. One completion per site per story day; no automatic promotions. Eight generated interior illustrations appear in reception and briefing scenes. Restart to load the update; existing saves remain compatible. Full generation prompts are in `assets/ui/locations/crime-interiors-prompts.json`.

## City-site artwork

All eight new city sites have individual generated 1536×1024 exterior backgrounds in `assets/ui/locations/site_01.png` through `site_08.png`. They appear in ordinary location scenes while visiting the site. Remote unknown sites retain their concealed identity. Game scenes use existing time/weather treatments; notebook artwork is a static illustration. Full built-in image-generation prompts are retained in `assets/ui/locations/crime-sites-prompts.json`. Restart to load the artwork.

## Unlabelled city sites and criminal fronts

Use ordinary **Maps** markers or Winterfield destination controls to visit these locations. Eight new markers cover a Shinokami headquarters frontage, supply depot and research front, four Syndicate side bases/fronts, and Oculus’s Winterfield campus. Unknown buildings use numbered unlabelled markers until inspected. Their map names become public business names, not faction labels.

Travel to a site and **Inspect exterior**. At the **Old town archive**, read its public operator record. At **Interpol’s public desk**, verify the matching published exhibit to establish one of seven local affiliations. Each step requires travel and earlier evidence; records persist privately with the protagonist. Oculus’s filings never prove its Syndicate affiliation: only Ivan, Valentina and Sylvanis know it initially. Their existing insider knowledge does not spread to friends or companions automatically.

The established Syndicate headquarters requires established membership; Valentina now has member access as a general. Every passenger requires their own access. Knowing Sylvanis does not grant HQ entry; old automatic guest passes are revoked and unauthorised saved occupants return to the public waterfront offices. New sites offer reception and controlled briefing interiors. Use the current location scene to enter, work, request clearance and review the hierarchy. Research records at the archive and verify exhibits at Interpol. Combat encounters are not added. Restart to load the update. Existing saves retain their current stories, invitations, relationships and money; no reset is required.

## Vendetta lore integration

Mysterious Hearts now includes Awakening, rare Traits, a unified United Nations government and Interpol’s Awakened Operations Division while retaining its independent relationships and story outcomes. Twelve named characters are Awakened; Emily’s Critical Hit remains a possible future awakening, with no automatic unlock. Alyssa and Sylvanis remain Blisk. Valentina is Ivan’s general, the Queen of Wind, with Deathwind, alongside her sailing work; Minsu has a speed-and-reflexes Trait. Private abilities and affiliations are not a public character directory.

Open **Winterfield → Careers → Open work & ambitions → Work** as Garrett, Ivan or Rei for nine rotating crime-related situations across Red Dragons, Joker Card and Iron Circle work. Complete the two decisions to retain their exact wording and numerical career effects in private **History**. Existing explicit sharing controls disclose only the chosen record. These decisions cover community debt, witnesses, shipment verification, branch accounts, publicity, recruitment, dangerous match offers and injury concealment. They do not automatically resolve investigations or spawn attacks.

Restart the game to load the new canon and code. Existing saves retain bonds, discoveries, bookings and money; already active work sessions retain their original situations. Powers are lore and dialogue context, not a new tactical combat engine. Emily’s future awakening and source-story outcomes are not playable events in this update. See `Mysterious Hearts - Worldbuilding.md` and `vendetta_lore.py` for AU rules and limits.

## Work and ambitions

Open **Winterfield → Careers → Open work & ambitions**. The same dark dashboard opens inside the phone, and Calendar links to accepted work bookings. Each protagonist has two persistent paths:

- **Garrett:** Golden Dragon service and tasting projects; Red Dragons leadership, mediation, direction and delegated reviews.
- **Rei:** modelling campaigns; Iron Circle preparation, title defences, rival-specific plans and comeback camps. He starts at rank #1. Preparation is unpaid; winning a scheduled bout earns the prize.
- **Ivan:** recordings and creative ownership; private Joker Card cross-branch responsibilities, delegation and independence decisions. He begins as an established executive, not a new recruit.
- **Minsu:** unpaid medical learning portfolios; a fictional future taekwondo pathway from local competition through selection to an Olympic tournament. There is no licensed medical work or automatic selection. After earning a medal, further competitions are post-Games invitationals, not additional Olympic medals every week.

**Work** offers 60/120-minute sessions with two decisions, or a 60-minute quick routine. Each career allows one work session per story day. Decisions build craft, workplace trust, reputation or autonomy, with different fatigue costs; matching the project's selected direction adds quality. Established characters begin with existing craft. Local café, flower, coaching and tutoring shifts also take 60 minutes, operate 08:00–20:00 and build workplace reliability, with a $20 pay increase every three completed shifts up to $100 extra.

**Project** starts a seven-day project. Work on three separate days, then book a finale in **Schedule**. Reputation 75 after a completed project unlocks an advanced brief. One three-day extension costs two reliability; an overdue project loses five reliability once and can still be completed with a lower review score. Successful projects create keepsakes in History and the home journal. Competitive finales additionally need two preparations and seven days between competitions. Rei's first camp starts a fourteen-day defence deadline; missing it drops him to #2 and leaves a comeback available. Rival style and the chosen match plan affect his result. Outcomes are deterministic from recorded preparation, quality, craft, fatigue and reliability; leadership pressure also matters.

**Schedule** supports future bookings, cancellations and rescheduling. Bookings conflict with each other and ordinary Calendar events. Arrive at the venue within fifteen minutes of the start; accepted work ends at the booked end. Reminders appear sixty and fifteen minutes before, and at the start. Cancel ahead of time without penalty; late cancellation loses three reliability and missing a booking loses five, plus workplace trust. Unfinished sessions expire when their allotted time runs out without awarding pay. Waiting for a booking is explicit and limited to two days per action. Travel is still required.

**People** shows recurring workplace roles and saved trust/experience. Red Dragons and Joker Card projects support thirty-minute delegation and report reviews, available the following day. Leaving reports unreviewed increases unresolved pressure. These roles are authored workplace records, not new conversational NPCs or romance routes. Preparation and home recovery each take sixty minutes and are limited daily per career; daytime martial-arts preparation takes place at the arena lounge. Fatigue also eases across story days.

**History** retains outcomes and earned keepsakes. Sharing the latest recorded update explicitly gives one known contact that information, including a private career if selected; no reply or romantic progress is invented. Unshared career records are private. The careers are finite authored situations and numerical progression, not an unlimited generated workplace simulation, real qualification rules or a complete simulation of a criminal organisation. An independence direction does not itself declare Ivan free of the Syndicate.

Existing saves receive additive career records when opened through this feature; money, relationships, earlier work and story history remain intact. Old daily career locks are honoured. No title deadline is imposed until the player starts Rei's first camp. Restart to load the code. Focused checks: `python -m unittest discover -s tests -p test_careers.py -v` and `python tests/careers_ui_smoke.py`.

## Character types

There are two character types. **Major characters** are the starting cast and every hidden character, including platonic interests, Neo and Alyssa. They retain the full personality, memory, relationship, schedule and social-app systems. Being major does not automatically make someone romanceable: existing family, orientation and relationship boundaries still apply.

**Town NPCs** are Maya, Theo, June, Noah, Iris, Leo, Mario Romano, Robin Vale, Dana Lin, Joseph Richter and the twelve additional town residents. They have portraits, public routines or venue appearances, ordinary conversation and phone chats. They never become romantic partners, receive Grove accounts or appear on Meet-Cute. Their smaller conversation system uses authored personality, recent exchanges, current mood and familiarity; conversations on three separate story days make them a familiar face. They do not accumulate attraction, jealousy, dating goals or the major cast's detailed relationship events.

Old saves keep their NPC chats and phone numbers. Obsolete NPC romance, dating-app and detailed relationship records are archived as inactive legacy data; active NPC dates are removed and associated Meet-Cute appointments cancelled. Restart the game to load these rules. Classification is centralised in `character_types.py`; background conversations live in `town_npc_system.py`.

## Patch notes and update history

Open **Patch notes & update history** from the start screen or **Tools** while playing. The dark reader supports full-text search, category/type filters, unread entries, bookmarks, sorting, copying and Markdown export. Read status and bookmarks persist separately from story saves; corrected entries become unread again.

The archive includes detailed curated history and original development reports back to game creation. Enable **Include original chat reports** for original design discussions, intermediate implementations and advice. All 17 formerly oversized chats have now been recovered from local logs, adding 59 missing completion reports and 17 detailed historical chapters. Three chats had no completed turn; their interrupted work is explicitly labelled. Unknown release dates remain unknown; report dates indicate chat completion, not releases. See [recovery coverage](patch_notes/RECOVERY.md).

The portable archive is [Patch notes](patch_notes/PATCH_NOTES.md); [authoring instructions](patch_notes/AUTHORING.md) explain how to record future updates. `python patch_notes.py validate` validates the catalogue; `python patch_notes.py export` refreshes the portable copy. Viewing notes does not call AI or change story progress. Restart the game to load the new menu links.

## More Winterfield neighbours

All twelve residents have individual transparent manhwa portraits in `assets/portraits/<name>-selection.png`. They appear in local conversations, saved local contacts, and direct-message headers and bubbles. Built-in image-generation prompts and appearance references are preserved in `assets/portraits/town-residents-manifest.json`. Run `python tests/town_portraits_smoke.py` to verify the assets and their actual Tk loaders without AI requests or save writes.

Twelve additional adult locals now appear in the existing town encounter list: Priya the librarian, Otis the retired mechanic, Nadia the shuttle driver, Ben the bowling technician, Tess the projectionist, Farah the tailor, Gabe the bicycle repairer, Wren the animation student, Celia the nurse, Arthur the history volunteer, Luz the gardener and Samir the bakery driver.

Visit the library, shops, downtown, parks and leisure venues to meet them. Their public routines change at 08:00, noon, 17:00 and 22:00, with different weekend stops; rain moves exposed outdoor visits into the library. Their routines continue while you wait. Each has personal interests, connections to other residents and rotating conversation topics. They use the existing local conversation, history and phone-contact systems, without adding romance routes or automatically revealing everyone's number. Existing saves receive the roster when loaded; restart the game to load the updated code.

These are background routines rather than simulated driving journeys. Their personal projects are conversation material, not automatically completed quests or player memories. Focused checks: `python -m unittest discover -s tests -p test_town_residents.py -v`.

## Phone numbers and adding contacts

Every named, contactable resident has a stable fictional number, including the protagonists, hidden cast, local residents and venue staff. Your own number and saved contacts' numbers appear in **Phone → Contacts**. Use **Add a contact by phone number** to save someone using their full number; spaces, parentheses, hyphens and an optional `+1` are accepted. Adding an existing contact does not duplicate it. Invalid and unassigned numbers show an inline error.

When a Meet-Cute match agrees to exchange numbers, their reply includes the actual number and saves it in Contacts. The match screen shows the saved number and provides **View saved contact** and **Open Messages**. Adding a hidden resident by number records an online introduction, without marking a physical meeting or revealing a home address. Existing saves keep their contacts and receive assigned numbers automatically; undiscovered numbers are not shown as a public directory.

Meet-Cute remains a screen inside the phone, including validation messages and unmatch/block confirmations. Its contact links navigate within the same phone. Regression checks: `python -m unittest discover -s tests -p test_phone_numbers.py -v` and `python tests/meet_cute_ui_smoke.py`; the latter verifies that these interactions create no additional top-level windows.

## Meet-Cute dating app

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

## More phone apps and outfit design

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

## Sending photos in Messages

In a chat, tap **+ → Attach photo from Gallery**, choose a photo, optionally type a caption, then tap **Send**. Direct and group chats support photos. Take photos in Camera to add them to the Gallery. Attachments and unsent photo selections stay with the save. Tap a sent photo bubble and choose **View photo** to open it. Characters receive the photo’s recorded type and location as text context; the image itself is not sent to the dialogue model.

## Personal phones and pinned messages

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

## Contact profiles and anonymous notes

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

## ChatGPT sign-in option

Open **AI & account** from the main menu or conversation sidebar. Choose **Continue with ChatGPT**, finish sign-in in your browser and approve ChatGPT plan usage. Refresh the connection if necessary, select one of the models returned for your account, and click **Use selected ChatGPT model**. Use **Use local Qwen 3.5 9B Abliterated** to switch back. The game never silently falls back between providers.

ChatGPT mode sends story context and conversation text to OpenAI, using eligible plan allowance or available credits. **Manage ChatGPT usage** opens your usage settings. **Disconnect** removes this game's local credentials and attempts remote revocation. This does not sign you out of other OpenAI applications. No API key is needed; the game does not read Codex or browser credentials. Your password stays in the browser. The official SDK verifies identity, handles refresh and stores tokens under `.chatgpt/`, encrypted through Windows DPAPI for your Windows account. Non-secret provider preferences are in `ai_settings.json`; both paths are git-ignored.

Sign-in and live ChatGPT inference require your browser authorization and an eligible account. Automated tests use mocks; a disconnected SDK status check is not proof of a successful account connection.

Official integration documentation: [Sign in with ChatGPT](https://developers.openai.com/cookbook/articles/sign-in-with-chatgpt). The vendored official SDK is retained in `vendor/sign-in-with-chatgpt-devkit` with its license and notices. Its noncommercial license applies to this personal local integration; review that license before commercial distribution.

For another machine, install Node.js 22.12+ and the dependencies from `package.json` (`npm install` or `pnpm install`), then run `npm run build:signin`. Keep the vendor SDK directory and its license files. Python/Tk still runs the game; Node runs the private sign-in bridge. The SDK source revision is recorded in the vendored repository.

Double-click **Launch Mysterious Hearts.cmd**. Choose Garrett, Rei, or Minsu, then select a love interest to receive her opening text. Character responses arrive before any suggestions. Type a custom response and press Enter or click Send, or click **Suggest replies** to generate four optional choices. Both portraits appear above the dialogue.

New conversations now begin automatically with an incoming text from the selected love interest. Wait for her first message, then type your own reply or click **Suggest replies**. Each woman has an individual texting style. Messages remain remote exchanges; invitations do not automatically move the characters into a meeting. Already-started conversations in older saves retain their previous mode; untouched contacts start by text. Failed opening requests can be retried without sending a fabricated player message.

## Subscription-only image generation

Open **Portrait gallery → Image studio · Generate**, describe an image and click **Generate image**. The game runs the installed Codex CLI in the background and automatically imports and displays the resulting PNG. Completed images and their prompts persist under `assets/generated/` and appear in the studio when reopened. Existing character portraits and backgrounds are not overwritten.

Images use **Codex's ChatGPT login**, independently of the game's dialogue sign-in. Open Codex and sign in with ChatGPT (or run `codex login`) first. API-key logins are rejected. The bridge forces ChatGPT authentication, removes API-key environment variables, ignores user CLI configuration, disables shell tools and external integrations, and has no paid API fallback or automatic retry. Usage counts against the ChatGPT/Codex plan and its limits; included allowances and any account-level credits remain governed by OpenAI's account settings.

Generation can take several minutes. Cancel stops the local job; usage already incurred may still count. Closing the studio cancels its pending request. If login, generation, or usage limits fail, the studio displays an error. The bridge requires a Codex CLI with built-in image generation; this workflow was verified with `0.166.0-alpha.6`. Local failure diagnostics are stored in the failed job folder.

## Phone Camera and Gallery

Known contacts post their own Grove photos on randomized, character-specific schedules measured in story time. Frequent posters such as Sophie post every 4–12 hours; quieter accounts such as April can wait 2–5 days. The configured dialogue provider writes the photo concept and caption, then the same Codex ChatGPT image generator used by Camera creates the image, with character portraits as selfie references. Photos appear in the feed and character profiles, and follower-scaled likes accumulate over the first day. Schedules persist with the save; time skips queue at most one photo per contact. Image generation runs separately from text comments, waits for active Camera jobs, and offers **Retry character photos** in Grove after failures. Automatic character photos use the same Codex plan allowance as Camera.

To edit or delete custom camera presets, open **Custom… → Manage saved descriptions** in a wheel, or **Choose outfits → Manage saved outfits** for a person. Select a saved description, edit it and click **Save changes**, or choose **Delete saved**. Active selections follow edits and return to a default when deleted; existing photos keep their original details. Outfit management is specific to the selected character.

Use **Custom…** in the expression, pose or group-pose wheel to type a description or choose a previously saved one, then **Save & use**. Descriptions support 1–500 characters and persist with the save, independently for each category. Saved custom choices also appear in the wheels and can be reused for the player or companions. Group descriptions can specify each person's pose.

The expression and pose wheels include stoic, smoulder, smirks, shy smiles, intense gazes, casual stances, seated poses, and more group and romance poses. Use **Previous set / Next set** to browse eight choices at a time. Visiting the **Downtown modelling studio** adds editorial, runway, commercial and beauty expressions and poses. Choose **Modelling portrait** for a photographer-framed shot with studio lighting and framing suited to the pose. Studio-only choices reset when you leave; photos still save to the dated Gallery.

Open the phone's **Camera** to take photos using the subscription-only Image Studio bridge. At home, choose **Selfie**, **Mirror selfie**, or **Photo of hobby**. Elsewhere choose **Selfie** or **Photo of environment**; **Photo of activity** appears when there is a recent recorded activity/meal or you describe what is in front of you. The hobby field offers the player's home activities and also accepts free text. Recent meals and activities expire from camera context after one in-game hour or when you leave the location.

During a hangout, **Group selfie** and **Group photo** include the player and companions actually present. Select a person to use their **Expression wheel** and **Pose wheel**. **Group pose wheel** includes friendship poses and named romance poses for present dating/official partners without unresolved harm. Rotate with arrows or mouse wheel, or click a choice, then **Choose**. Availability is checked again when you press **Take photo**.

**Choose outfits** offers each person's saved wardrobe and gallery looks, or **Custom** clothing you describe. Custom outfit descriptions are saved for reuse. Existing gallery unlocks also apply to bedroom outfits. Outfit choices apply to the photo; character portraits are attached as likeness and clothing references.

The phone's **Gallery** contains this save's camera photos, grouped by in-game date, newest first, with capture times and locations. Open a photo for a larger view. Photos retain the scene and time from the shutter press, even if the world changes during generation. You can switch apps or close the phone while a photo develops; it loads into Gallery automatically. Closing the game cancels a pending request. Albums are stored under `assets/generated/camera-albums/`, with the album ID in the save; keep those assets when transferring saves. Camera generation retains ChatGPT-only authentication, with no paid API fallback.

## Local AI setup

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

## Game features

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

## Runtime and development

Native Python/Tk desktop app, not a browser window. The launcher uses this computer's bundled Python runtime if available, otherwise `pythonw.exe` on PATH. On another Windows computer install Python 3.12+ with Tk support and run `python -m pip install -r requirements.txt`, then `python game.py`.

Run tests with `python -m unittest discover -s tests -v`. Tests use a local fake HTTP service; they do not require model generation. `python tests/live_smoke.py` makes one real model request and checks the response without modifying your save.

Portrait assets and the prompts used to generate them are in `assets/portraits/`.

## AI direction

Character conversation references live in `Mysterious Hearts - Character References.md`. The game selects public, familiar, personal and confidence material using both trust and closeness. Existing shared history remains available to the people involved. The world reference supplies common recognition and occupation-specific knowledge when an organisation comes up.

Joseph, Sylvanis and Valentina have full tables. Relationship evidence distinguishes public family ties, firsthand history, delivered disclosures and observations. Companions present for Rei's encounter with Joseph can remember what they heard. Other residents need their own source.

The four disclosure bands use the lower of trust and closeness plus 18, with boundaries at 40, 58 and 78. These are tunable gameplay choices. Group disclosure considers every listener. Short, authored repair lines handle a few direct story questions when a generated reply misses the supplied facts. Restart the game after changing Python code or the cached character and world tables.

Player suggestions use the selected protagonist's voice guide and the current scene, in a separate **manual** request. Character responses do not generate choices or run a second suggestion pass. Click **Suggest replies**, **Suggest personal replies**, or **Suggest actions** to request only that set. Custom input stays available while suggestions generate. Suggestion requests never replay the character response, advance game time, change relationships, or rewrite your custom input. Cancelled or stale suggestions are discarded.

`ai_directions.txt` supplies shared narrative rules on every generation: continuity, player agency, knowledge limits, gradual romance, meaningful choices and factual relationship memory. `dialogue_styles.json` supplies individual voices. Both files are read for each new request, so edits to their contents apply on the next turn. Restart the game after Python code updates. These are model instructions rather than a deterministic romance simulation; factual and stylistic adherence can still vary. Speaker IDs and response structure are validated separately in code.

## Town, money and relationships

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

## Starting relationships

New stories use protagonist-specific starting relationships. Existing saved stats and relationship statuses are preserved. These numbers are gameplay tuning based on established familiarity. All romance routes start outside a dating relationship. Garrett and Rei start as best friends with 95 trust and 90 closeness and can develop attraction through mutual interest.

| Contact | Garrett attraction | Rei attraction |
| --- | --- | --- |
| Emily | 8 | 58 |
| Sophie | 22 | 32 |
| Amy | 24 | 28 |
| Samantha | 38 | 42 |
| April | 8 | 6 |

Emily's secret crush on Rei is established character canon. He does not automatically know about it. Attraction does not imply dating or consent. Existing saves retain earned stats; new stories use the revised starting attractions.

## Living world, drives and unanswered texts

Use **Choose hangout companions** in the in-person view to select one person for a private hangout or several for a group. Current companions are preselected; uncheck anyone you want to leave out. Only selected companions join your conversation and travel with you; nearby contacts never join automatically. You can also change the selection under **Town → Groups**.

Open **Town · Free roam** or **Maps** to travel instantly. Your party arrives with you. Vehicle selection, chauffeur details, passengers, arrival observations and journey history are retained. Saved journeys from older versions finish on load without charging time. Leaving separately or a scheduled departure ends the hangout and restores phone texts.

All eight characters have daily routines. The selected protagonist remains player-controlled; the other protagonist and five love interests move through their routines, including tracked commutes. Occupation locations are separate from homes. **Homes & routines** lists each designed home, the daily activities and current whereabouts. **Travel & texts** shows transit and message history. These are authored gameplay routines/designs, not assertions of additional historical biography.

By default, the clock advances one game minute every five real seconds (two real hours per full day), including while reading, typing or waiting for AI. The toolbar **Time** menu offers **Normal · 2-hour day** (1×), **Fast · 40-minute day** (3×), **Faster · 15-minute day** (8×), and **Paused**. Select any speed to resume. The selected mode is saved; paused time never accumulates for later catch-up. Pause freezes automatic world time, including sleep, while menus and conversations remain usable. Dialogue and actions add no fixed time cost. Each minute processes schedules, needs, appointments, message queues, Grove posts, photos and replies in order. Midnight rolls directly from 23:59 to 00:00; there is no Finish day control. Menus and closed-app time do not advance the simulation. Fractional minutes are preserved in saves. New games begin at 08:00 on New Year’s Day.

Contacts make dynamic follow-up decisions using personality variation, social energy, elapsed game time and unanswered-message limits. Follow-up wording is AI-generated using the current provider, not a fixed template. Sleep and driving prevent reading or replying; work and social activities limit phone checks. Opening a chat clears your unread badge without counting as a reply. Real-world idle time does not advance availability. Delivered messages persist independently of AI generation; failures can be retried per chat.

**Relationships** shows player bonds, stats, story summaries and milestones. **Bonds** covers all ten pairs of women with individual history, trust, closeness, tension and recent events. Shared scheduled locations can build familiarity once per pair per day after fifteen minutes together. Betrayals and dating overlaps add persistent tension and events; time together does not erase them. The AI receives a bounded recent snapshot of this state, while full journals remain saved locally.

Legacy saves gain the world clock, cast state and bond details on load without resetting stats or relationships. Existing in-person pairs are kept together when the location system is first added. Historical invented travel in old AI prose is not retroactively converted into trips; new movement uses the explicit travel controls.


## Careers, home actions and groups

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


## Illustrated interface and backgrounds

Generated artwork is stored in `assets/ui/`, with the exact built-in image generation prompts alongside each PNG. The menu uses Winterfield at dusk and a navy-and-gold decorative title header. In-person conversations and the Town view show university artwork for campus/track, café artwork for the café, and town-square artwork for the square. Phone conversations and locations without their own illustration use the abstract UI artwork. Scene illustrations now use dawn, day, dusk and night lighting from the story clock. Rain and snow appear over supported exterior scenes; text conversations retain their neutral backdrop. Portraits render over the backgrounds with their relative height scaling preserved. Labels, buttons and dialogue remain live, readable controls. Missing artwork falls back to the existing dark theme.

The selection screen also uses `title-logo.png`, `selection-frame.png`, and `selection-nameplate.png` from `assets/ui/`. The title is generated lettering; character names, role labels and keyboard-focusable Begin buttons stay live. The original portrait assets and relative protagonist height scaling are preserved. Generation prompts are saved beside the images.

## Hidden residents

Six adult residents can be met at the archive, cycle workshop, planetarium, makerspace, community market and wetland boardwalk. They work from 09:00 to 17:00, then follow individual errands or quiet evenings at home. Weekends have later starts and individual outings. Rain moves outdoor leisure to varied indoor venues that suit each character. Use Town → Meet when nearby. Town → Discoveries shows profiles after meeting, lets you add their phone contact, and reveals a home address after 6 closeness (daily conversations grant 2). Discoveries persist in existing saves. Friends remain platonic; attraction represents initial potential, not consent. All six hidden residents have transparent anime/manhwa portraits in assets/portraits, with their built-in image_gen prompts saved beside each PNG.

## Convenience tools and scheduled events

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


## Source-backed character and event memory

Existing saves are upgraded additively on load. Original transcripts, cumulative prose memories, relationship milestones, group and hangout histories, profile notes, shared events, and scheduled events remain in place. A versioned `memory_store` adds permanent source references, character-specific knowledge ownership, timestamps where available, certainty labels, and searchable topic indexes. Migration makes no AI requests. Existing prose summaries remain archived as historical evidence; they are no longer rewritten every turn or treated as stronger evidence than canon and current game state.

The ledger separates experiences, reported facts/preferences, beliefs, commitments, and legacy summaries. Quoted preferences remain self-reports; rumours remain unverified claims. Explicit promises/proposals are retained as unresolved statements unless there is separate evidence of their outcome. Existing agreed-meeting records and cancellations have an auditable history. A subsequent meeting does not prove an unspecified planned activity was completed. Exact preference-slot updates and explicit corrections can supersede an older record for the people who learned the update, without deleting the earlier evidence or informing other characters automatically.

Recall combines the current exchange and location with indexed topics, importance, open commitments, milestones, and recent dialogue. Only records owned by the character are eligible. Relationship overviews and invitation context use a disposable, source-linked extractive summary, rather than replacing historical prose. Canon and authoritative game state still take precedence over statements and summaries.

New calendar events record planned, attended, completed, cancelled, or player-missed states. Attendance is recorded from actual presence during the event; inviting someone is not itself a shared experience. If an old saved appointment has no attendance evidence, the system explicitly retains unknown attendance rather than inventing a visit. Guest attendance and the player's attendance are separate.

Verification: memory migration and manual-suggestion regressions are in `tests/test_memory_store.py`. `python tests/manual_suggestions_smoke.py` checks response-first delivery, personal-only generation, continued custom typing, cancellation, and in-person choice selection with mocked AI and saves. The existing player save files are not modified by these tests.


## Winterfield immersion update

Restart the game, continue your story, and open **Phone → Weather** or **Phone → Winterfield**. Town also has a **Life in Winterfield** shortcut. Existing saves gain these systems without resetting progress; the update does not invent earlier visits, help or discoveries.

**Weather** has an iPhone-inspired large temperature display, rounded forecast cards, a horizontally scrollable 24-hour forecast, ten daily temperature bars, and wind, humidity, sunrise/sunset, UV, visibility and feels-like readings. It follows the fictional 2050 calendar, with seasonal temperatures and deterministic forecasts. It is not an internet weather service. Celsius is used throughout. Town scenes and Maps display the same conditions. Sheltered boathouse activities and residents’ outdoor leisure respond to rain; bookings and player travel are never silently cancelled.

**Winterfield** gathers attributed local bulletins, festival preparations and aftermath, a rotating cinema programme, and practical details of life in 2050. Nine characters have authored projects that now progress through time spent at their project venue, independently of player participation. Already-reached stages are preserved during migration. Meet a character to help once for twenty minutes. Only completed help becomes a shared memory; completed projects remain available for conversation.

Repeatable café, pizza, cinema, flower-shop and boathouse activities take ten minutes and are limited to once per place per story day. Paid orders show their cost. Regulars remember recorded orders, lobby sketches persist, and three visits on separate days with the same companion establish a shared ritual. The Follow through section surfaces recorded promises and proposals and links back to the relevant conversation; it does not claim a proposal was accepted or a promise fulfilled.

Garrett can continue **Find Charles** after reading the receiving copy. Three enquiries at the archive, Interpol desk and Golden Dragon each take twenty minutes, with at least one story day between enquiries. The episode resolves the crate-count discrepancy and the meaning of the receiving stamp, then identifies a missing authorisation page as the next lead. It does not reveal Charles’s location, allegiance or fate.

New betrayals are private records until witnessed or disclosed. Use **Winterfield → Tell someone what happened** to send an explicit disclosure. Consequences apply once to each informed person; relationship tension requires both people to know. Legacy knowledge remains intact. AI interpretation of free-form romantic actions still depends on the model.

Verification: `tests/test_living_world.py` covers forecast consistency, additive migration, projects, actual shared visits, mystery gates, knowledge boundaries, routines and news. `tests/living_world_smoke.py` exercises Weather at both supported phone sizes, day/night views, Winterfield, Maps and Home with mocked AI and saves.


## Autonomous life and asynchronous messages

Restart the game. **Tools → Life & availability** (also linked from Messages, Town and Home) shows player Energy, Social battery and Happiness, usual sleep schedules, pending invitations and shared life events. Existing stories gain these records without resetting relationships or histories.

- Time passes automatically while playing. At home, **Nap** sets one hour of sleep and **Sleep** sets eight hours; both recover needs over the running game clock. While asleep, choose **Normal · 1×**, **Fast · 4×**, **Faster · 12×**, or **Skip to waking** in Life & availability (also accessible from Home activities and the sleeping presence view). Skipping processes every world tick. Sleep acceleration multiplies the selected Time speed and stops while time is paused. The sleep multiplier returns to 1× upon waking, preserving your selected Time speed; **Wake up** ends sleep early.
- Needs update every five game minutes. Characters reconsider optional plans every 15–30 minutes, retain chosen intentions, seek rest, work on personal projects, arrange company and make invitations. Familiar contacts may travel to your door; welcoming them remains your decision. Invitations can be accepted, declined or deferred in Life & availability. No relationship penalty applies just for declining.
- Sleep schedules allow a bounded late-night extension for comfortable company. Characters wind down, leave through tracked journeys, or request a separate sleeping place at your home. Accepted overnight stays preserve their location through sleep and end with morning departure. Staying overnight never establishes intimacy.
- Sustained public encounters create directional NPC acquaintances, including pairs outside the original five-woman bond table. Established acquaintances can deliberately meet again. Their own memories include those encounters; other people do not learn them automatically. Small work/study events, remembered activities and project progress supply conversation context.
- Send several texts, switch to another contact or group, and keep playing while replies generate. Outgoing bubbles show **Delivered** and then **Read** (or partial group readership). Each recipient reads and answers according to availability. Sending another text while a reply is being generated queues it for the next exchange; it does not rewrite the response already underway.
- NPC replies contain one to three generated bubbles. Follow-ups can add a thought or start another topic. Prompts explicitly reject stock apologies, repetitive reminders and assumptions about why the player has not replied. No automatic reply is sent while a character sleeps or drives. The worker processes one messaging request at a time without locking the interface.
- **Pause reply** preserves delivered messages; **Continue / retry** resumes the chat after a generation failure or pause. Pending messages survive saving and reloading. Character generation uses the selected AI provider and therefore its normal usage allowance. Simulating needs, travel and decisions requires no AI requests.

Validation: `tests/test_autonomy.py` covers sleep, needs, receipts, independent queues, stale-response protection, acquaintances, overnight stays and migration. `tests/autonomy_ui_smoke.py` exercises the native phone and needs window using mocked AI and saves. No player save is modified by these checks.

## Autonomy integration audit and reply timing — November 6, 2026

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


### Varied character outings

Free-day routines rotate through late-morning, afternoon and evening destinations. Weekday work and sleep schedules remain intact, while meal breaks and leisure stops vary by character and day. Public hangout invitations and peer plans use character interests, shared interests, recent visited locations and current crowds; the café is one option among many. Peer partners share the same destination and activity. Rain chooses suitable indoor alternatives instead of sending everyone to the café. Agreed player outings keep their location unless the player accepts a proposed change. Recent destinations persist in saves.

`tests/test_leisure.py` checks destination diversity, public access, weather alternatives, repeat avoidance, shared peer plans, actual free-day movement and schedule priorities.


## More places around Winterfield

The map and travel picker now include Winterfield Lanes (bowling), Pixel Pier (arcade), Afterglow (nightclub), the Copper Lantern (bar), Winterfield Commons (public park), Silver Sands (beach), the Public Library and Winterfield Galleria (shopping mall). Riverside Park remains available. Each destination supports calendar invitations, shared travel, encounters and a daily activity through the living-world panel. Paid activities deduct their displayed cost; visits record memories and shared rituals and supply camera activity context.

Characters choose these places according to their interests, recent visits, crowds and weather. Rain and snow redirect autonomous outdoor outings indoors. Bar outings begin at 17:00 and nightclub outings at 20:00; sociable characters can take evening outings on free days before returning home. These are activity hours; players can visit the locations at any time. Travel keeps the game's existing instant-arrival behavior. Existing saves need no reset. Each new venue has a distinct illustrated background; park and beach scenes also receive outdoor weather effects.

Downtown is a visitable metropolitan district with a free boulevard walk, generated scene artwork, calendar meetups and interest-led autonomous outings. It uses outdoor weather rules. Both map layers now continue into dense city blocks beyond the playable destinations, with no empty texture edge when zoomed out.

Map geography now uses continuous curved streets, uneven block spacing, T-junctions, diagonal arterial roads, rounded park boundaries and road-aligned building footprints. Downtown has denser, larger buildings; neighbourhood streets continue beyond the playable area in both map layers.

Unanswered text follow-ups use the contact friendship thresholds: acquaintances wait four times the previous delay, friends (trust 50+, closeness 25+) wait twice as long, and close friends (trust 70+, closeness 55+) or above retain the previous pace. Existing availability, requested pauses and increasing delays for repeated unanswered follow-ups still apply.

Characters can also send newly generated private photos through the existing Codex ChatGPT image connection. Eligible direct replies have a 4% chance for acquaintances, 12% for friends and 25% for close friends or above, with minimum gaps of three story days, one day and twelve hours respectively. Photos develop in the background and appear inline when the sender is available. Silence follow-ups, setbacks and requests to pause do not trigger photos. Pending jobs survive saves; failed jobs can be retried with **Chat options → Retry incoming photos**. These images are generated specifically for the message, not taken from Camera or Grove galleries.


### Relationship development

Conversations can record concrete player promises, individually expressed boundaries, loyalty conflicts, and character-initiated dates, introductions or relationship talks. These appear in Character profiles → Your notebook and persist in saves. Only delivered words or submitted actions count; suggestions and hypothetical plans do not.

An explicitly agreed promise deadline uses story time. Missing it marks the promise overdue; following through later does not erase the original hurt. Respecting boundaries and keeping promises build trust. Crossing boundaries and breaking promises damage it. Repeating the same recorded outcome cannot repeatedly earn trust.

Rei protects Yuriko and Emily, Garrett protects April, and Ivan protects Valentina with additional disapproval. Their approval changes with conduct they actually witness; private actions are not automatically shared. Characters can voice competing loyalties, and the person being protected can challenge intrusive behaviour.

Repairing unresolved harm now requires acknowledging the specific hurt, corrective conduct on a later story day, and freely offered forgiveness. The Make amends button cannot bypass that process. Established betrayal memories remain. Characters with sufficient trust and closeness may initiate a milestone conversation; accepting a proposed date still uses the normal date eligibility and goals. Declined invitations have a three-story-day cooldown.

### Story saves and portable backups

Each playthrough has a stable story ID and an independent autosave. `saves/story.json` remains the Continue entry; switching stories does not mix their recovery histories. Existing saves gain their story ID when saved.

Recovery retains up to 12 checkpoints spaced at least five real minutes apart and 14 daily checkpoints (local calendar days). These capture the previous saved state before a later write. Named copies remain until their story is deleted. Legacy rotating backups remain available. Writes use unique temporary files, flush data before replacement, and serialize through a process/thread lock.

The save library displays protagonist, story date/time, location, save type, and local save timestamp. Malformed files are shown as damaged instead of disappearing. If Continue fails, the game offers the newest loadable recovery entry; if the damaged file cannot identify its story, the candidate may be another playthrough and is named in the prompt.

**Delete selected story** removes all saves and checkpoints with that story ID; **Clear all saves** removes every saved story. Both require confirmation. Deleting the active story returns to the menu and clears its in-memory state. Generated pictures, account credentials, and device preferences are retained. Legacy files without story IDs are deleted individually.

**Export with photos** creates a ZIP containing the selected saved state, referenced generated media, and its camera album manifest. **Import** validates the save and archive paths and creates a separate playthrough. Missing source images cannot be included; conflicting existing media causes import to stop without overwriting it. Bundles have a 1 GiB uncompressed size limit. Exported stories include conversation history and personal notes, so share them deliberately.

Validation: `tests/test_save_system.py` covers independent histories, checkpoint spacing, deletion, atomic-write failure, photo/album transfer, damaged-save visibility and archive traversal. `tests/save_library_smoke.py` exercises named saves and clearing an active story in Tk using isolated temporary storage.


### Start screen

The main menu uses a split layout: story navigation and account/sound controls on the left, a large Winterfield character preview on the right. Select Garrett, Rei, Minsu or Ivan to preview their portrait and introduction, then choose **Begin as …** to start. Selection alone does not create a save. Continue is disabled until an active save exists; named stories and recovery remain accessible through **Story library & backups**. The layout supports the default 1220×940 window and the 1000×800 minimum. `tests/start_ui_smoke.py` checks all four selections, the start action, and both layouts without writing player saves or contacting AI.


### Canonical romantic types

`romantic_types.py` authors physical and personality preferences for all 25 orientation-defined characters. Physical fit considers preferred height range, appearance and usual fashion; personality fit considers multiple interests, character traits, lifestyle facets and sociability through `personality_types.py`. These are directional preferences, not universal beauty rankings. Unknown traits count as neutral.

New stranger attraction and emerging NPC chemistry use physical fit. Dialogue receives each speaker's private type and reciprocation tendency. Positive long-term feeling growth rolls against personality fit each simulation hour: 15% for no match, 85% for a full match, interpolated for partial matches. Negative feeling changes are unaffected. Friendship, trust, consent, orientations and family boundaries retain their existing rules. Saved attraction, established history and Emily's authored crush are preserved; preferences never retroactively erase them. Usual fashion tags do not establish today's outfit.


### Detailed appearance references

`Mysterious Hearts - Character Appearances.md` supplies detailed appearance descriptions to dialogue through `character_appearance.py`. It preserves existing portrait features and usual styling, with structured hair, eye, facial-feature and body-type descriptors for romantic matching. Unknown details stay neutral. Edit the dedicated document when updating these runtime references; restart the game to reload cached records. The original character conversation tables remain historical source descriptions.

Each character’s physical type in `romantic_types.py` now includes those four dimensions alongside height, overall appearance and fashion. Alternatives within a dimension are equally acceptable; physical dimensions have equal weight. Personality matching uses the expanded profiles described below.


### Expanded personality compatibility

`personality_types.py` records multiple authored interests, everyday character traits and lifestyle facets for all 25 romantic-type profiles, separately from their preferred partner traits. Hidden-cast hobbies are included directly from `hidden_cast.CAST`. Existing route eligibility still decides who can be romanced.

Long-term fit weights character traits at 35%, interests at 30%, lifestyle at 25% and sociability at 10%. Each category scores the proportion of preferred facets present in the other person. Related hobbies can count in a shared domain, while exact hobbies stay distinct. Extra hobbies never reduce fit, duplicate tags cannot inflate it, and unknown categories count as neutral. Scores remain directional and feed the existing 15–85% positive-affection growth chance. Physical attraction and negative affection changes are unchanged.

Restart to load the profiles. No save migration is needed; accumulated feelings and history remain intact while future growth uses the expanded compatibility. Dialogue uses category-level fit privately without learning undisclosed biography from the scoring data.

## Supafast daily AI catalogue

The game automatically prepares Supafast's current-day selection through the provider selected in **AI & account**. Open **Phone → Supafast** to browse it. Twelve new product names, descriptions, categories and whole-dollar prices are generated together; there is no fixed production item roster. The shop saves an accepted selection, so reopening it or reloading the story does not reroll prices or products. Stock changes at 00:00 in-game time. The game clock starts the new catalogue in the background even when Supafast and the phone are closed; product photos queue after the catalogue is ready. Skipped days are not backfilled.

Generation runs in the background. If the provider fails or returns invalid listings, use **Retry daily selection**. The shop does not substitute canned products or offer yesterday's stock for purchase. Recent exact product names are rejected, and the prompt requests genuinely different goods rather than recolours. Search includes descriptions as well as names and categories. Purchasing and gifting retain the existing instant-delivery behavior. Generated descriptions are flavour, not new mechanical item effects.

Existing purchased items, inventory IDs and order history remain intact, including items from the earlier fixed catalogue. Restart the game to load this update; no story reset or manual migration is required. Generation uses the selected provider's normal connection and usage allowance. Checks: `tests/test_supafast.py` and `tests/supafast_ui_smoke.py` mock the provider and do not make live AI requests.

Supafast listings also generate one product photo per item through the existing **Codex ChatGPT image connection**. Photos use your ChatGPT plan allowance and run sequentially in the background; a new twelve-item selection can request twelve photos. Listings remain purchasable while photos load. Images are prompted as isolated studio product photographs on a dark slate background, based on each item's name, description and category. Compact previews preserve the full image rather than cropping the product. Generated file references are saved with the product and reused on reopening or reloading. Missing photos for the current selection are queued automatically while the story is running, even with the phone closed.

If photography fails (including another image job already running), the remaining queue pauses. **Retry product photos** resumes missing photos without rerolling stock or replacing successful pictures. Missing files can be regenerated; corrupt previews offer a retry. Leaving the phone allows the current day's queue to continue, while changing the day or loading another story cancels outdated work and discards late results. Already-incurred provider usage may still count. Retained product files live under `assets/generated`; keep those files with the save. Verification uses mocked image generation and local fixture pictures rather than spending plan allowance.

## Doober Eats food photography

Open **Phone → Doober Eats** and choose a restaurant to generate food photos for its menu through the existing Codex ChatGPT image connection. Each dish or drink receives a separate photograph based on the restaurant, item name and category, with natural food styling on a dark slate tabletop. Photos appear above menu names and prices. The menu's items, prices, ordering and delivery behavior are unchanged.

Photos load sequentially in the background using your ChatGPT plan allowance; a restaurant has twenty menu items. Ordering remains available while photos load. Successful images are saved per restaurant and item, reused across days and save reloads, and kept separate from the player’s Camera album. Opening another restaurant cancels unfinished work for the previous menu; returning resumes missing photos. Switching saves or closing the game cancels obsolete work. Already-incurred usage may still count.

If generation fails or another image job is running, **Retry food photos** resumes missing photos without replacing completed ones. Missing files regenerate, and corrupt previews offer retry. Keep `assets/generated` with the game/save. No manual migration is needed; old saves gain photo records when menus are opened. Tests use mocked generation and fixture images; they do not verify live model food accuracy.


## Protagonist phone artwork, vehicles and Bubblegram desks

All 28 protagonists have individual dark phone wallpapers. Default wallpapers update automatically; custom photo selections remain selected. Charles, Fox and Gordon have dedicated contact photos in messaging and contact details, subject to existing contact access.

Under **Town → Plan a drive**, choose from your protagonist’s named car models. Single-car garages show their model directly. Choices persist in saves and trip history; larger parties use the existing passenger van. The original four keep their existing garages.

Sylvanis, Valentina and the four Aces have established desks under **Phone → Bubblegram → Contracts / Network → Leadership**, with role-specific commissions, operating funds and diplomacy. Aces remain mission specialists, not Suit commanders. Physical contract work and deal settlement open in the main in-person window; travel to the listed venue before completing work. These roles migrate once while retaining earned reputation, heat and operating results. Individual story arcs remain separate future work.
