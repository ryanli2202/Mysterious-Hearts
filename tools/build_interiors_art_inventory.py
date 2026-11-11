"""Authored planning inventory; generates documentation only, never game assets."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'roadmap'
existing_inventory = OUT / 'INTERIORS_IMAGE_INVENTORY.json'
if existing_inventory.exists():
    existing = json.loads(existing_inventory.read_text(encoding='utf-8'))
    if existing.get('production_status') or any(
        view.get('generation_status', 'not_started') != 'not_started'
        for building in existing.get('buildings', []) for view in building.get('views', [])
    ):
        raise SystemExit('Refusing to overwrite interiors production records; revise the existing inventory explicitly.')
# section | building ID | name | semicolon-separated image views | reuse assignments
# @ outdoor/sheltered view; ? unresolved optional layout (not in firm image total).
# Each unmarked entry is one distinct interior image, including explicit zone views.
DATA = r'''
Homes|rei_home|Rei and Yuriko's penthouse|Entrance;Living space;Kitchen and dining;Library;Art space;Hallway;Rei bedroom;Yuriko bedroom;Bathroom|Living space=rei_home
Homes|emily_home|Emily's garden apartment|Entrance;Living room;Kitchen;LEGO workroom;Hall;Bedroom;Bathroom;@Flower balcony|Bedroom=emily_home
Homes|sophie_home|Sophie's trackside loft|Entrance;Open living kitchen;Stretching zone view;Stairway;Sleeping loft;Bathroom;@Balcony|Open living kitchen=sophie_home
Homes|amy_home|Amy's dorm|Dorm room;?Bathroom|Dorm room=amy_home
Homes|nest_dorm_corridor|Amy and Minsu's shared building access|Public dorm corridor|
Homes|minsu_home|Minsu's dorm|Dorm room;?Bathroom|Dorm room=minsu_home
Homes|samantha_home|Samantha's garage flat|Street-entry vestibule;Garage workbench;Heavy-bag zone view;Stairway;Living kitchen;Bedroom;Bathroom|Living kitchen=samantha_home
Homes|april_home|April's observatory townhouse|Entrance;Sitting chess room;Kitchen;Hall;Study lab desk;Bathroom;Stairway;Upper landing;Bedroom;Roof access;@Telescope terrace|Sitting chess room=april_home
Homes|garrett_home|Garrett's hillside estate|Foyer;Living room;Dining room;Noodle kitchen;Stairway;Landing;Garage passage;Garage;Bedroom;Bathroom;@Terrace|Living room=garrett_home
Homes|valentina_home|Yeuns' Ferry Signal House|Entrance;Harbour living room;Kitchen dining;Piano alcove view;Sail workroom;Mezzanine stairway;Reading mezzanine;Ivan bedroom;Valentina bedroom;Bathroom|Harbour living room=valentina_home
Homes|neo_home|Neo and Alyssa's station apartment|Entrance;Living room;Kitchen dining;Hall;Shared bedroom;Bathroom;@Herb balcony|Living room=neo_home
Homes|tyler_home|Tyler's East Ward duplex|Entry living room;Kitchen dining;Level hall;Tyler bedroom;Father bedroom;Accessible bathroom;@Accessible porch|Entry living room=tyler_home
Homes|lena_home|Lena's clocktower flat|Entrance;Living record room;Kitchen;Photo workroom;Hall;Bedroom;Bathroom|Living record room=lena_home
Homes|naomi_home|Naomi's riverside maisonette|Entrance;Living room;Kitchen;Stairway;Landing;Bedroom;Bathroom;@Balcony|Living room=naomi_home
Homes|celeste_home|Celeste's blue-door cottage|Entrance;Piano sitting room;Kitchen dining;Hall;Bedroom;Bathroom|Piano sitting room=celeste_home
Homes|dev_home|Dev's station studio|Entrance;Studio room;Bathroom|Studio room=dev_home
Homes|rosa_home|Rosa's market terrace|Entrance;Sitting room;Communal dining room;Kitchen;Stairway;Landing;Bedroom;Bathroom;@Shared courtyard|Communal dining room=rosa_home
Homes|elliot_home|Elliot's willow cabin|Living workroom;Kitchenette;Bedroom;Bathroom;@Covered porch|Living workroom=elliot_home
Homes|daniel_home|Daniel's flat above the Bijou|Stair entrance;Poster hall;Living drawing room;Kitchen;Bedroom;Bathroom|Poster hall=daniel_home
Homes|fox_home|Fox's Blackhaven hideout|Entrance;Living kettle room;Equipment workshop;Private evidence room;Hall;Bedroom;Bathroom|Equipment workshop=fox_home
Homes|gordon_home|Gordon's Civic Court apartment|Entrance uniform locker;Living reading room;Kitchen;Hall;Bedroom;Bathroom|Living reading room=gordon_home
Homes|sylvanis_home|Sylvanis's shuttered flat|Bell entrance;Bare sitting room;Kitchen;Private notes room;Bedroom;Bathroom|Bare sitting room=sylvanis_home
Homes|martos_home|Martos's apartment|Entrance;Living room;Kitchen;Watch workroom;Hall;Bedroom;Bathroom|Living room=martos_home
Homes|elias_home|Elias's penthouse|Entrance;Sitting rehearsal room;Kitchen;Script study;Hall;Bedroom;Bathroom|Sitting rehearsal room=elias_home
Homes|mavis_home|Mavis's private room|Private room|Private room=mavis_home
Homes|camila_home|Camila's apartment|Entrance;Living chess room;Kitchen;Private study;Hall;Bedroom;Bathroom|Living chess room=camila_home
Custom homes|vacant_downtown_home|Downtown apartment|Entrance;Open living kitchen;Hall;Bedroom;Bathroom|Open living kitchen=vacant_downtown_home
Custom homes|vacant_suburbs_home|Suburban house|Entrance;Living room;Kitchen;Hall;Bedroom 1;Bedroom 2;Bathroom;@Garden|Living room=vacant_suburbs_home
Custom homes|vacant_beach_home|Beach cottage|Entrance;Living room;Kitchen;Hall;Bedroom;Bathroom;@Dune deck|Living room=vacant_beach_home
Custom homes|vacant_university_home|University apartment|Entrance;Living study kitchenette;Bedroom;Bathroom|Living study kitchenette=vacant_university_home
Public and work|cafe|Campus café|Entrance;Counter seating room;Quiet study room;Staff kitchen;Staff office;Service corridor;Restroom|Counter seating room=../cafe-evening
Public and work|noodle_shop|Golden Dragon|Entrance;Dining room;Service counter view;Kitchen;Staff office store;Restroom|Dining room=noodle_shop
Public and work|marios_pizza|Mario's Pizza|Entrance;Dining counter room;Staff kitchen store;Restroom|Dining counter room=marios_pizza
Public and work|chess|Chess café|Entrance;Café room;Playing room;Lesson alcove view;Restroom|Playing room=chess
Public and work|flowers|Petal & Stem|Entrance;Shop floor;Arrangement workroom;Stockroom;Restroom|Shop floor=flowers
Public and work|boutique|Gift boutique|Entrance;Display counter room;Staff store;Restroom|Display counter room=boutique
Public and work|shopping_mall|Winterfield Galleria and JobSeek tenant|Concourse;Food seating view;Customer service room;JobSeek tenant shop floor;Tenant receiving room;Tenant staff office;Tenant store;Restroom|
Public and work|campus|Winterfield University|Main lobby;Teaching corridor;Lecture room;Seminar room;Study room;Theatre workshop;Rehearsal room;Restroom|
Public and work|track|University track pavilion|Pavilion lobby;Changing room;Coaching room;Restroom|
Public and work|studio|Downtown modelling and recording studio|Reception;Corridor;Photo studio;Dressing fitting room;Recording booth;Choreography room;Review room;Restroom|Photo studio=studio
Public and work|arena|Arena lounge and training|Entrance;Lounge;Training hall;Coach review room;Changing room;Restroom|Lounge=arena
Public and work|boxing_club|East Ward Boxing Club|Entrance;Reception lounge;Training hall;Equipment room;Changing room;Restroom|Training hall=boxing_club
Public and work|iron_circle|Iron Circle|Controlled entrance;Spectator lounge;Ring hall;Fighter preparation room;Recovery room;Restroom|Ring hall=iron_circle
Public and work|library|Public library|Lobby desk;Reading room;Stacks;Reservable study room;Staff catalogue office;Desk corridor;Restroom|
Public and work|archive|Old town archive|Public desk;Reading records room;Conservation workshop;Restricted storage;Restroom|Reading records room=archive
Public and work|makerspace|Station makerspace|Welcome room;Shared workshop;Electronics room;Tool store;Restroom|Shared workshop=makerspace
Public and work|cycle_shop|Riverside cycle workshop|Customer counter room;Repair room;Parts store;Restroom|Customer counter room=cycle_shop
Public and work|planetarium|Hilltop planetarium|Lobby exhibits;Dome theatre;Staff corridor;Preparation room;Restroom|Lobby exhibits=planetarium
Public and work|cinema|Bijou cinema|Ticket foyer;Auditorium;Staff corridor;Projection room;Staff office;Restroom|Ticket foyer=cinema
Public and work|sailing_club|Municipal boathouse|Reception;Rigging workshop;Equipment store;Restroom;@Launch|Reception=sailing_club
Public and work|market|Lantern community market|Community dining room;Staff kitchen store;Restroom;@Public stalls|@Public stalls=market
Public and work|bowling_alley|Winterfield Lanes|Reception;Lane hall;Lounge;Restroom|
Public and work|arcade|Pixel Pier|Counter room;Cabinet floor;Seating view;Staff repair room;Staff office;Service corridor;Restroom|
Public and work|nightclub|Afterglow|Entrance;Dance hall;Lounge;Service room;Staff corridor;Restroom|
Public and work|bar|Copper Lantern|Entrance;Bar seating room;Service room;Staff office;Restroom|
Public and work|public_park_pavilion|Commons gardener pavilion|Tool store;Supervisor office;Restroom|
Outdoor placeholder replacement|beach|Silver Sands beach|@Shoreline beach scene|
Outskirts|hill_tea_room|Hillside Tea Room|Entrance counter view;Tea room;Staff kitchen;Restroom|Tea room=hill_tea_room
Outskirts|farm_shop|Westbrook farm shop|Entrance;Produce counter hall;Staff store;Restroom|Produce counter hall=farm_shop
Outskirts|pottery_studio|Old Mill pottery studio|Entrance display room;Pottery workshop;Kiln room;Restroom|Pottery workshop=pottery_studio
Outskirts|marine_centre|Marine discovery centre|Lobby;Exhibit hall;Education room;Staff service room;Restroom|Exhibit hall=marine_centre
Outskirts|harbour_market|South Harbour covered market|Vendor storage;Restroom;@Sheltered entrance;@Stall aisles;@Public seating|@Stall aisles=harbour_market
Outskirts|railway_museum|Railway museum|Ticket lobby;Collection hall;Archive education room;Restroom|Collection hall=railway_museum
Outskirts|southbank_diner|Riverside diner|Entrance;Dining counter room;Staff kitchen;Restroom|Dining counter room=southbank_diner
Headquarters|syndicate_office|Waterfront executive offices|Public lobby;Appointment room;Guarded access passage;Restroom|Appointment room=syndicate_office
Headquarters|syndicate_hq|Syndicate underground HQ|Security foyer;Internal corridor;Council chamber;Executive meeting room;Cross-branch operations room;Members lounge;Restroom|Council chamber=syndicate_hq
Headquarters|syndicate|Red Dragons lounge|Entrance;Members lounge;Council meeting room;Community liaison room;Office;Restroom|Members lounge=syndicate
Headquarters|site_01|Kestrel Operations Centre|Reception;Secure corridor;Briefing room;Operations office;Guarded service room;Restroom|Reception=site_01_reception;Briefing room=site_01_briefing
Headquarters|site_02|Pacific Relay Depot|Reception;Secure corridor;Briefing room;Dispatch room;Warehouse;Restroom|Reception=site_02_reception;Briefing room=site_02_briefing
Headquarters|site_03|Stillwater Research Annex|Reception;Secure corridor;Briefing room;Research office;Restricted laboratory;Restroom|Reception=site_03_reception;Briefing room=site_03_briefing
Headquarters|site_04|Breakwater Security Depot|Reception;Secure corridor;Briefing room;Equipment room;Maintenance bay;Restroom|Reception=site_04_reception;Briefing room=site_04_briefing
Headquarters|site_05|Aster Media House|Reception;Secure corridor;Briefing room;Production room;Editing room;Restroom|Reception=site_05_reception;Briefing room=site_05_briefing
Headquarters|site_06|Meridian Capital Offices|Reception;Secure corridor;Briefing room;Accounts office;Restricted records room;Restroom|Reception=site_06_reception;Briefing room=site_06_briefing
Headquarters|site_07|Oculus Winterfield Campus|Reception public displays;Controlled corridor;Briefing room;Corporate office;Data wing;Security room;Public-service supervisor room;Restroom|Reception public displays=site_07_reception;Briefing room=site_07_briefing
Headquarters|site_08|Greyglass Service House|Reception;Secure corridor;Briefing room;Equipment workshop;Restricted store;Restroom|Reception=site_08_reception;Briefing room=site_08_briefing
Headquarters|glasshouse_lab|Glasshouse|Cleared entrance;Internal corridor;Laboratory workroom;Private review reunion room;Records room;Rest room;Restroom|Laboratory workroom=glasshouse_lab
Headquarters|interpol_hq|Interpol Regional HQ|Public lobby verification desk;Secure corridor;Awakened Operations briefing room;Controlled training hall;Interview containment wing;Case office;Restroom|Public lobby verification desk=interpol_hq;Awakened Operations briefing room=interpol_briefing;Controlled training hall=interpol_training;Interview containment wing=interpol_containment
Headquarters|blackstone_hq|Blackstone Headquarters|Reception security;Controlled corridor;Research records;Experimental wing;Executive command;Restroom;@Loading compound|Reception security=blackstone_hq;Research records=blackstone_records;Experimental wing=blackstone_lab;Executive command=blackstone_command;@Loading compound=blackstone_loading
Smaller factions|lantern_house|Lantern House|Entrance;Waiting room;Meeting room;Office;Stairway;Private flat living repair room;Private bedroom;Private bathroom;Visitor restroom|Meeting room=lantern_house
Smaller factions|saints_depot|Saints Rail Depot|Entrance;Waiting room;Meeting room;Dispatch workshop;Private converted office living sleeping room;Private bathroom;Visitor restroom|Meeting room=saints_depot
Smaller factions|purple_clubhouse|Purple Skulls clubhouse|Entrance;Waiting room;Meeting room;Members lounge;Garage;Stairway;Private residence living room;Private bedroom;Private bathroom;Visitor restroom|Meeting room=purple_clubhouse
Smaller factions|hamayashi_house|Kurose House|Entrance;Reception waiting hall;Meeting room;Records room;Rear residence living room;Private bedroom;Private bathroom;Visitor restroom;@Bonsai courtyard|Meeting room=hamayashi_house
Smaller factions|rojos_courtyard|Los Rojos base|Entrance;Waiting room;Meeting room;Office;Stairway;Upstairs living guitar room;Private bedroom;Private bathroom;Visitor restroom;@Courtyard|Meeting room=rojos_courtyard
Smaller factions|consortium_house|Waterfront Consortium House|Entrance;Waiting room;Boardroom;Office;Stairway;Upper apartment living chart room;Private bedroom;Private bathroom;Visitor restroom|Boardroom=consortium_house
Smaller factions|hamayashi_annex|Hamayashi riverside annex|Entrance;Meeting office room;Restroom|Meeting office room=hamayashi_annex
Smaller factions|hamayashi_store|Hamayashi supply house|Entrance;Stock hall;Office;Restroom|Stock hall=hamayashi_store
Owned properties|crew_lot_west|West workshop|Entry;Workshop;Office;Restroom|
Owned properties|crew_lot_docks|Dock warehouse|Entry;Warehouse;Meeting office;Restroom|
Owned properties|crew_lot_north|Northern offices|Reception;Meeting room;Workroom;Restroom|
Owned properties|crew_lot_south|South garage|Entry;Garage;Office;Restroom|
'''

def slug(s):
    return re.sub('[^a-z0-9]+', '_', s.lower()).strip('_')

buildings = []
used = set()
for line in DATA.strip().splitlines():
    group, bid, name, raw, reuse_text = line.split('|')
    reuse = dict(x.split('=', 1) for x in reuse_text.split(';') if x)
    rows = []
    for item in raw.split(';'):
        kind = 'outdoor' if item.startswith('@') else 'conditional' if item.startswith('?') else 'interior'
        room = item.lstrip('@?')
        rid = bid + '__' + slug(room)
        existing = None
        if item in reuse:
            p = (ROOT / 'assets/ui/locations' / (reuse[item]+'.png')).resolve()
            assert p.is_file(), p
            existing = p.relative_to(ROOT).as_posix()
            assert existing not in used, existing
            used.add(existing)
        row = dict(id=rid, room=room, kind=kind, status='reuse_candidate' if existing else 'layout_decision' if kind=='conditional' else 'new_image', existing=existing,
                   target=existing or f'assets/ui/locations/interiors/{bid}/{slug(room)}.png')
        if existing:
            with Image.open(ROOT / existing) as im: row['dimensions']=list(im.size)
            row['sha256']=hashlib.sha256((ROOT/existing).read_bytes()).hexdigest()
            row['review']='Contact-sheet visual match; full-resolution and in-game framing approval pending.'
        rows.append(row)
    buildings.append(dict(id=bid, name=name, group=group, views=rows))

allrows=[r for b in buildings for r in b['views']]
counts=Counter((r['kind'], r['status']) for r in allrows)
hashes=[r['sha256'] for r in allrows if r.get('sha256')]
assert len(hashes)==len(set(hashes)), 'Duplicate reuse image content'
assert len({r['id'] for r in allrows})==len(allrows)

notes = {
 'emily_home':'Existing image shows a bed, so allocate it to the bedroom, not the proposed separate living room.',
 'nest_dorm_corridor':'Proposed planning-only building/view key; not a current runtime location. Keep separate dorm entry gates.',
 'amy_home':'Bathroom configuration is unresolved; do not generate bathroom art until the dorm layout is settled.',
 'minsu_home':'Bathroom configuration is unresolved; do not generate bathroom art until the dorm layout is settled.',
 'valentina_home':'Use the current shared signal-house art. Legacy ivan_home.png depicts the older home and is not a second room of this building.',
 'mavis_home':'Threshold is a doorway action within this single-room view, not an invented lobby. No address or additional private rooms are established.',
 'planetarium':'Existing artwork reads as the exhibit lobby/entrance to the dome, not the auditorium itself.',
 'pottery_studio':'Existing art contains worktables and ceramics equipment; allocate it to the workshop, not both display room and workshop.',
 'shopping_mall':'Existing shopping_mall.png is flat placeholder art. One JobSeek tenant is budgeted; additional named tenant units require additional rows if enabled.',
 'public_park_pavilion':'Proposed support building for the existing gardener job; not an established runtime building ID.',
 'glasshouse_lab':'Private review/reunion room is one reservable room used at different times; no simultaneous incompatible private scenes.',
 'interpol_hq':'Containment wing is one initial scene. If subdivided into interview rooms or cells, each new navigable room needs another image.',
 'blackstone_hq':'Loading compound is an existing exterior view, not an indoor room. Keep its authored campaign location outdoors.',
 'beach':'Replace assets/ui/locations/beach.png: current simple geometric placeholder. Keep the beach outdoors and preserve weather, travel and beach-outfit context. This is one additional image, not an interior room.',
 'rojos_courtyard':'Despite its filename, the current picture depicts a covered indoor meeting setting; use for meeting room, not the separate open courtyard.',
}
for key in ['arcade','bar','bowling_alley','library','nightclub']:
    notes[key]='Existing base image is simple flat placeholder art; replace with new finished room-specific artwork.'
for b in buildings:
    if b['group']=='Smaller factions' and b['id'] not in ('hamayashi_annex','hamayashi_store'):
        notes[b['id']]=notes.get(b['id'],'')+' Leader-residence subdivision is a proposed production layout, not established detailed canon; review before generation.'

doc = ['# Interiors room and image inventory', '', '**Status:** Proposed production inventory; no images generated or runtime mappings changed.',
       '**Source:** All three interiors plan documents plus current location assets and selected campaign sources.', '',
       '**Production grouping:** [Ten generation batches](INTERIORS_GENERATION_BATCHES.md), with per-image Markdown and JSON manifests. Rebuild batches after changing this inventory.', '',
       '## Totals', '', '| Scope | Views | Reuse candidates | New images | Layout decisions |', '| --- | ---: | ---: | ---: | ---: |']
for kind in ('interior','outdoor','conditional'):
    c=Counter(r['status'] for r in allrows if r['kind']==kind)
    doc.append(f"| {kind.title()} | {sum(c.values())} | {c['reuse_candidate']} | {c['new_image']} | {c['layout_decision']} |")
doc += ['', f"**{len(buildings)} building/group entries.** Each listed room/view has one image slot. Outdoor views and unresolved dorm bathrooms are separated from the firm interior count.", '',
        'Reuse means a visually matching candidate identified in the contact-sheet audit, not a final in-game approval. Every candidate has a real path, dimensions and SHA-256 in the JSON companion; none is assigned to two views or has identical bytes to another selected candidate. Full-resolution detail, art continuity, door positions and character framing still need final review. Budget new artwork for every New row; replacement of a rejected candidate would increase that budget.', '',
        '## Scope and counting decisions', '',
        '- This is the complete enumerated production baseline for the currently specified layouts, including the integration review\'s missing JobSeek staff rooms. It is not proof that every future campaign scene has been implemented or that no later design change can add rooms.',
        '- Each semicolon-separated space in the authored data is a separate image/view. Explicit navigable alcoves, counters and seating views receive their own image even when they share a physical room. Ordinary clickable hotspots (a chair, sink or desk) do not get extra images. Open zones retain shared witnesses.',
        '- Named entrances and stairways are budgeted as separate views unless the plan explicitly makes them a doorway action (Mavis and the dorm thresholds). Outdoor frontages already used for travel remain separate assets, not new indoor lobbies.',
        '- One restroom scene per public/working building is budgeted to close the plans\' general bathroom requirement. Private/public boundaries must remain separate. Leader bases include a visitor restroom and private bathroom. These are proposed service-layout details; extra cubicles are not individually navigable.',
        '- Dorm bathrooms remain conditional. Generic labels such as shop units resolve to one JobSeek tenant and its support rooms for this baseline, not an unlimited mall. Generic residential areas at six gang bases are expanded into bounded proposed rooms below.',
        '- Existing home images often show adjoining open-plan areas. Reuse is allocated to one primary room only; new views must preserve visual continuity. A reused image may show a doorway but cannot act as the image for every room behind it.',
        '- One guard post does not require one background: guards overlay their assigned room/view. Neither NPCs nor automatic outfits are baked into the art. New enclosed guardrooms require new inventory entries.',
        '- Historical flashbacks, unspecified new venues and future campaign-specific spaces are not silently invented or assigned arbitrary room counts; see the coverage notes below.', '',
        '## Building summary', '', '| Building | Interior | Outdoor | Conditional | Reuse candidates |', '| --- | ---: | ---: | ---: | ---: |']
for b in buildings:
    c=Counter(r['kind'] for r in b['views'])
    doc.append(f"| [{b['name']}](#{b['id'].replace('_','-')}) | {c['interior']} | {c['outdoor']} | {c['conditional']} | {sum(r['status']=='reuse_candidate' for r in b['views'])} |")
last=None
for b in buildings:
    if b['group']!=last:
        doc += ['', '## '+b['group']]; last=b['group']
    doc += ['', f"### {b['id'].replace('_','-')}", '', f"**{b['name']}** — planning key `{b['id']}`."]
    if notes.get(b['id']): doc += ['', notes[b['id']].strip()]
    doc += ['', '| Room / image view | Type | Art action | Existing image or proposed new target |', '| --- | --- | --- | --- |']
    for r in b['views']:
        action={'reuse_candidate':'Reuse candidate','new_image':'New','layout_decision':'Hold: layout decision'}[r['status']]
        path=r['target']
        link=f'[{Path(path).name}](../{path})' if r['existing'] else f'`{path}`'
        doc.append(f"| {r['room']} | {r['kind']} | {action} | {link} |")

doc += ['', '## Existing art not allocated to an interior', '',
        '| Existing asset group | Decision |', '| --- | --- |',
        '| `site_01.png`–`site_08.png` | Keep as exterior frontages; do not count as room images. |',
        '| `site_01_interior.png`–`site_08_interior.png` | Older reception-like alternates. Do not allocate to secure corridors or additional rooms just to reduce new-art count. Newer dedicated reception/briefing files are selected. |',
        '| `crew_lot_*.png` | Keep as exteriors; all property interiors require new artwork. |',
        '| `ivan_home.png` | Legacy home art; current shared home is `valentina_home`. Do not invent a room to reuse it. |',
        '| `arcade.png`, `bar.png`, `bowling_alley.png`, `library.png`, `nightclub.png`, `shopping_mall.png` | Existing flat placeholder artwork; replacement required for finished interiors. |',
        '| `campus-day.png`, `track.png`, `fox_hideout.png`, `gordon_apartments.png` | Exterior/arrival views. New campus/pavilion interiors are separate. Fox/Gordon residence interiors use their actual home files. |',
        '| `beach.png` | Simple outdoor placeholder: replacement is required and budgeted in the Silver Sands entry. |',
        '| Parks, wetlands, downtown, Blackhaven, trails, orchard, pier, lookout, lighthouse walk | Existing illustrated outdoor destinations; retain unless a later audit identifies a placeholder or incompatible view. Outdoor placeholder replacement is in scope, but these images are not all automatically regenerated. |',
        '| `garrett-hong-kong-school.png`, `rei-high-school.png` | Existing historical exterior views. Preserve for supported flashbacks; not present-day university rooms. |',
        '| `transit.png`, `motorcycle.png`, phone wallpapers, UI frames and portrait/gallery art | Not reusable as empty architectural room backgrounds. |', '',
        '## Placeholder replacement requirements', '',
        'The update must replace simple placeholder location art wherever used, including outdoor destinations. The current visual audit identifies seven active files: `arcade.png`, `bar.png`, `bowling_alley.png`, `library.png`, `nightclub.png`, `shopping_mall.png` and `beach.png`. The six interior replacements are already covered by New rows for cabinet floor, bar/seating room, lane hall, reading room, dance hall and mall concourse respectively; do not count them twice. Silver Sands adds one outdoor image.', '',
        'Each replacement must be a finished, distinct architectural/environment illustration consistent with the existing game artwork, with clear space for live character overlays. Preserve original venue IDs, activity access, fees, schedules and indoor/outdoor weather behaviour. Update the actual scene lookup and any Maps/arrival/preview consumers so the old placeholder cannot remain visible through an alternate path.', '',
        'Audit every enabled location/view, including missing-file fallbacks, before release. Any further simple placeholder must be added as an explicit replacement row. Archived placeholders, such as the old public-park file, are not active replacement work unless still referenced. Existing finished public-park artwork should be retained.', '',
        'Inspect `tools/build_venue_art.py` before production: its bulk primitive renderer can overwrite venue PNGs, including finished assets. Add overwrite protection or retire that production path when implementing the update; do not run it to create the new art. Verify all seven replacements at full size and in actual rendered scenes, and record source/prompt provenance. No replacement has been generated or installed by this planning change.', '',
        '## Campaign, meeting and wardrobe coverage', '',
        '- Council uses Syndicate council chamber; diplomacy uses assigned meeting/boardrooms; JobSeek uses the listed staff areas and named tenant. No extra image is needed per event when events occupy the same physical room at different times.',
        '- Glasshouse review/reunion, archive records, Kurose testimony/records, Blackstone records/lab/command and Interpol briefing/training/containment all have dedicated rows. Garrett\'s home dining and noodle-shop aftermath have dedicated views. Subsequent indoor campaign stages must resolve to these rows or add an explicit new row before being enabled.',
        '- Reviewed Charles search/extended Garrett chapters and repeatable post-story destinations: Blackhaven, public market and waterfront outdoor handovers remain outdoor where authored. Do not build a fictitious indoor market room solely for a combat objective.',
        '- Fixed-domain characters do not receive invented private houses: Crow uses HQ, Takeo/Thirteen existing briefing rooms, Charles Glasshouse rest/review/work rooms.',
        '- Newer campaigns and historical scenes still require the integration plan\'s exhaustive stage-to-room audit. This is a release gate, not a hidden unbudgeted assumption: an unmapped indoor stage cannot ship until added here. Unspecified Bubblegram district venues stay blocked for indoor production until an actual building is selected; outdoor contracts stay outside.',
        '- Beach/gym/formal/home outfit switching reuses scene images; it adds wardrobe assets only if separately requested. Listed dressing/changing rooms already cover the architectural requirement. No per-outfit or per-character background variants.', '',
        '## Audit and maintenance', '',
        '- Visually reviewed contact sheets 01–06 covering all current location PNGs plus café/campus art. Sheets 07–08 contain remaining UI/wallpaper assets and are not location-reuse evidence.',
        '- Checked selected asset existence, dimensions, hashes, unique IDs and one-to-one reuse assignment when generating this inventory. No new art, runtime integration or in-game render test was performed.',
        '- Contact-sheet matches are provisional production reuse recommendations. Inspect full-size candidates before final installation; reject unwanted baked-in signage, incompatible room geometry, bad crop or missing foreground space.',
        '- Source data and reproducible renderer: `tools/build_interiors_art_inventory.py`. Machine-readable companion: [INTERIORS_IMAGE_INVENTORY.json](INTERIORS_IMAGE_INVENTORY.json). Contact sheets: [audit directory](interiors-art-audit/).',
        '- Proposed new paths are reserved planning targets, not existing files. Do not generate art for unresolved layouts. Preserve stable row IDs when modifying the plan; add newly navigable spaces rather than hiding them under an existing room.', '']
(OUT/'INTERIORS_IMAGE_INVENTORY.md').write_text('\n'.join(doc),encoding='utf-8')
(OUT/'INTERIORS_IMAGE_INVENTORY.json').write_text(json.dumps(dict(schema_version=1,status='proposed',scope='Current specified interiors production baseline',buildings=buildings),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(buildings=len(buildings),counts={str(k):v for k,v in counts.items()},selected_assets=len(used)),indent=2))
