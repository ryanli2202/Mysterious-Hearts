"""One-time retrospective importer. Does not overwrite an existing catalogue."""
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import patch_notes as notes


def build():
    if notes.CATALOG.exists():
        raise SystemExit('Catalogue already exists. Edit it directly; do not regenerate historical snapshots.')
    archive = notes.ROOT/'patch_notes'
    original = (notes.ROOT/'README.md').read_text(encoding='utf-8')
    (archive/'README-at-archive.md').write_text(original, encoding='utf-8')
    entries = []

    def add(key, title, category, summary, body, sources, impact=None, kind='Retrospective', when=None, provenance=None):
        entries.append(dict(id=key, title=title, category=category, kind=kind, date=when,
                            summary=summary, body=body, sources=sources,
                            save_impact=impact or 'See the preserved detail for documented migration behavior. No additional migration is performed by viewing these notes.',
                            provenance=provenance or 'Reconstructed on 7 November 2026 from the cited local evidence. Original release date and exact sequence are not established. This describes the recoverable feature history, not a claim that every paragraph shipped together.'))

    add('release-2026-11-07-patch-notes', 'A permanent update archive', 'Interface',
        'Searchable patch notes, a detailed retrospective and original development reports.',
        'Added a dark desktop patch notes reader from the start screen and Tools menu. Search titles, details and sources; filter category, entry type, unread and bookmarks; sort by catalogue order, title or documented date.\n\nRead status is explicit and revision-aware: edited entries become unread again. Bookmarks and read state live outside story saves. Export the selected note or current filtered results to Markdown.\n\nThe archive preserves README sections and recovered completed development reports. Original reports are optional in the viewer because they include advice and obsolete behavior. Unknown release dates and missing oversized chat records are disclosed.\n\nFuture updates use stable IDs, source references, compatibility notes and schema validation. The first archive does not assign fictional version numbers to older work.',
        ['patch_notes.py', 'patch_notes_ui.py', 'patch_notes/AUTHORING.md'],
        'No story reset or save migration. Reader preferences are separate from stories.', kind='Release', when='2026-11-07',
        provenance='First dedicated patch notes release, authored in this change. Automated validation is documented separately from historical test claims.')

    # Preserve every prior documentation section in full, including historical limitations.
    sections = re.split(r'^#{2,3} (.+)\n', original, flags=re.M)
    for index in range(1, len(sections), 2):
        title, body = sections[index].strip(), sections[index+1].strip()
        category = 'World & story'
        for words, value in [(['phone','contact','messages','camera','meet-cute'], 'Phone & social'),
                             (['relationship','dating'], 'Relationships'),
                             (['ai','sign-in','generation','runtime'], 'AI & platform'),
                             (['save','backup'], 'Saves'), (['interface','start screen'], 'Interface'),
                             (['autonomy','autonomous','clock'], 'Simulation')]:
            if any(w in title.lower() for w in words): category = value
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        add('history-'+slug, title, category,
            'Preserved update documentation: '+title+'.', body,
            ['patch_notes/README-at-archive.md — '+title],
            when='2026-11-06' if title.startswith('Autonomy integration audit') else None)

    additions = [
      ('foundations', 'From design to the first playable game', 'World & story',
       'The first desktop build offered Garrett or Rei, five love interests, portraits, local AI conversations, four generated choices, custom replies, autosave and separate relationship histories. Initial development reports also record character design and portrait creation. Combat and scripted quests were not part of that first playable build.\n\nEarly follow-ups added individual voices, labelled player/narrator/character dialogue, speaker checks, gradual-romance and knowledge instructions, protagonist-specific replies and automatic incoming opening texts. The local provider moved from Librellama Gemma E2B to Gemma 12B, then later Qwen; automatic suggestions were later replaced by manual requests. See the dated development reports for those intermediate states.', ['patch_notes/development_records.json','game_core.py','ai_directions.txt']),
      ('sexuality','Canonical attraction and legacy romance reconciliation','Relationships',
       'Canonical orientations now gate both sides of romantic compatibility across Meet-Cute discovery, likes, matching, date acceptance, flirt choices and anonymous feelings. Friendship is still available. Persistence and affection scores do not override orientation, and attraction is not consent.\n\nOlder incompatible romance states become friendships while retaining trust, closeness and history. Incompatible dating-app matches close without deleting messages; pending romantic replies and future dates are cancelled. Incompatible active date sessions are retained as historical records.', ['sexuality.py','tests/test_sexuality.py']),
      ('home-layout','Editable app pages and dock','Phone & social',
       'The phone home screen supports choosing an app and placing it into an explicit empty position on another page, swapping apps into the dock, and dragging dock apps back to the page. Empty positions are preserved. Editing does not launch apps. Layouts survive save round-trips, rebuilding the home screen and resizing.', ['phone_home.py','phone_personalization.py','tests/phone_home_smoke.py']),
      ('neo','Neo Ishida joins the hidden cast','World & story',
       'Neo has a discoverable profile, portrait, Grove identity, daily schedule and home. His established connections to Tyler and Daniel inform shared memories. Neo is in a committed relationship with Alyssa and remains a platonic contact rather than a dating-app candidate. Meeting him does not automatically introduce Alyssa. His home requires the normal discovery threshold. Existing saves add his records without overwriting existing bond progress.', ['hidden_cast.py','tests/test_neo.py']),
      ('alyssa','Alyssa and the shared household','World & story',
       'Alyssa joins the discoverable cast with personal references, a Grove identity and bookbinding interests. She and Neo share one home and a committed partnership. Discovering one partner does not silently introduce the other. Both remain unavailable as player romance routes. Save migration preserves prior discoveries and relationship progress.', ['hidden_cast.py','tests/test_alyssa.py']),
      ('couple-gallery','Neo and Alyssa photo archives','Art & media',
       'Added eight distinct square Grove photos each for Neo and Alyssa, with authored captions and comments. The gallery upgrade preserves existing likes, replies and live posts and does not duplicate the imported archive on repeated loads. Image generation prompts are retained with the assets.', ['tests/test_neo_alyssa_galleries.py','assets/grove/neo/generation-prompts.json','assets/grove/alyssa/generation-prompts.json']),
      ('grove','Grove, Supafast and Doober Eats','Phone & social',
       'Added social posts and replies through Grove, daily shopping through Supafast, and food menus and deliveries through Doober Eats. Character follower counts and known profiles shape the social presentation. Later updates added publishing Gallery photos with captions, generated character comments and follower-based engagement.\n\nConversation context includes actual posts and relevant orders; merely discussing a purchase does not place an order or spend money. Private deliveries are not automatically shared with unrelated characters.', ['phone_apps.py','grove_photos.py','grove_reactions.py','tests/test_phone_apps.py','tests/test_grove_photos.py','tests/test_encounter_context.py']),
      ('grove-art','Character galleries and group photo expansion','Art & media',
       'Grove gained authored photo archives, dates, captions, likes and comments for its character profiles. Subsequent artwork expanded individual and group scenes, including Rei, Garrett and Yuriko with their established friends. Gallery tooling also covers Valentina, Sylvanis, Tyler, Elliot and Daniel.\n\nPhoto archives and live posts coexist. These are authored in-world records; importing artwork is not evidence that a player performed the depicted activity. Available original reports remain in the optional development archive; some image-heavy chats exceeded the retrieval limit.', ['grove_gallery.py','tests/test_grove_gallery.py','tools/add_daniel_gallery.py','tools/add_elliot_gallery.py','tools/add_sylvanis_gallery.py','tools/add_tyler_gallery.py','tools/add_valentina_gallery.py']),
      ('arcade','Arcade expansion, sound and animation','Phone & social',
       'The initial phone arcade included Connect 4, Tetris, Blackjack, Snake, Pong and 2048. It expanded with Minesweeper, Breakout, Memory Pairs, Match-3, Simon and draw-one Klondike Solitaire.\n\nGames gained canvas animation, including sliding tiles, and sound effects. Reduced-motion and phone audio preferences are respected. Minesweeper has difficulty choices and a safe opening; Match-3 uses cascading combos; Solitaire supports click and drag moves. Timed games pause away from the screen. Progress lasts while the phone stays open; Blackjack is practice without wagers.', ['mini_games.py','arcade_games.py','tests/test_mini_games_animation.py','tests/test_arcade_games.py']),
      ('notifications','Message and Grove notification popups','Phone & social',
       'Notifications cover incoming messages and Grove interactions, including comments and replies. The UI provides navigation to the relevant activity and respects privacy settings. Notification regression checks cover routing and avoiding duplicate delivery. Earlier audio work added separate sent/received text sounds and controls, without treating in-person speech as a text notification.', ['notifications_ui.py','tests/test_notifications.py','sound.py','tests/test_sound.py']),
      ('dark-phone','Dark phone surfaces and embedded prompts','Interface',
       'Phone prompts and confirmations use embedded dialog wrappers so navigation stays in the phone. Dark slate styling covers entries, combobox popups, scrollbars, selected and disabled states, and arcade screens. Theme checks guard against native light controls. Navigation checks cover leaving and reopening active conversations, drafts and in-phone routes.', ['phone_dialogs.py','phone_theme.py','tests/phone_dark_theme_smoke.py','tests/phone_dialogs_smoke.py','tests/phone_navigation_smoke.py']),
      ('protection','Witnessed romance and protective reactions','Relationships',
       'Protective reactions respond to actual witnessed romantic conduct involving established close ties. Rei, Garrett and Ivan have distinct motivations; the reaction is not automatically romantic jealousy. Private romance and ordinary friendly events do not trigger an uninformed protector. Repeated observations are deduplicated, and the player does not react to himself as a separate NPC.', ['protectiveness.py','tests/test_protectiveness.py']),
      ('hangouts','Persistent hangouts and accurate encounter context','Phone & social',
       'In-person hangouts retain their own history and distinguish spontaneous visits, arranged meetings and summoned visitors. Groups keep participant-specific knowledge. Later controls allow selecting whom to hang out with instead of assuming everyone nearby is part of the conversation.\n\nYou cannot text someone in your active hangout, including through a group chat. Texting resumes after the hangout ends. Phone navigation allows reopening a conversation while its reply is in progress.', ['encounter_context.py','tests/test_hangout_journal.py','tests/test_hangout_texting.py','tests/test_encounter_context.py']),
      ('portraits','Portrait consistency and alternate outfits','Art & media',
       'Character artwork gained consistent portrait presentation and saved generation prompts. Alternate outfit assets expanded the visual wardrobe, including additional Garrett, Rei, Emily and April looks. Portrait and clothing references feed Camera and later generated Wardrobe designs. Original image-heavy chat reports were not all recoverable; the archive does not invent their individual completion dates.', ['assets/portraits','camera.py','lifestyle_apps.py']),
      ('cast','Expanded protagonists, family and hidden cast','World & story',
       'The original Garrett/Rei choice expanded to Minsu and Ivan. Minsu has authored university friendships, a dorm, medical study and taekwondo interests. Yuriko is Rei’s platonic sibling contact. Hidden residents gained gated profiles, home discovery, contacts and persistent schedules. Later additions include Valentina, Sylvanis, Neo and Alyssa.\n\nPrivate lore is revealed through familiarity and evidence rather than a public directory. Sylvanis has special headquarters access rules; Ivan starts with an existing connection. Daniel and Tyler are 21 in the current cast records.', ['game_core.py','hidden_cast.py','tests/test_minsu.py','tests/test_hidden_cast.py','Mysterious Hearts - Character References.md']),
      ('emotions','Emotions, dialogue tone and social reactions','Relationships',
       'Conversation headers show participant emotions. Friendly, sincere, funny and flirtatious exchanges interact with mood and relationships. Character voice guidance supports distinctive laughter, stutters, exuberance and quiet reactions; physical action suggestions follow the conversation’s tone. Family and platonic boundaries remain enforced.', ['emotions.py','dialogue_styles.json','tests/test_reactions.py','tests/test_conversation_growth.py']),
    ]
    for key,title,category,body,sources in additions:
        add('history-'+key,title,category,body.split('\n\n')[0],body,sources)

    records = json.loads((archive/'development_records.json').read_text(encoding='utf-8'))
    for record in sorted(records['records'], key=lambda r:r.get('completed_at') or 0, reverse=True):
        when = datetime.fromtimestamp(record['completed_at'], timezone(timedelta(hours=10))).date().isoformat() if record.get('completed_at') else None
        add('report-'+record['turn'],record['title'],'Original reports',
            'Original completed development-chat report. May describe implementation, design or advice.',record['text'],
            ['Development chat: '+record['thread'], 'Turn: '+record['turn']],
            'Use the curated notes and current game documentation for compatibility. This report records what was stated at the time.',
            kind='Development report',when=when,
            provenance='Date is chat completion in Australia/Brisbane, not a release date. Preserved source report; implementation and historical test claims have not been independently reverified for this archive.')
    # A turn can contain multiple final reports; keep stable unique IDs.
    seen = set(); unique = []
    for entry in entries:
        if entry['id'] not in seen: unique.append(entry); seen.add(entry['id'])
    data = dict(schema_version=1, reconstructed_on='2026-11-07', releases=unique)
    notes.validate(data)
    notes.atomic_write(notes.CATALOG,json.dumps(data,ensure_ascii=False,indent=2))
    notes.export(notes.select(unique),archive/'PATCH_NOTES.md')
    print(f'Created {len(unique)} entries; {len(notes.select(unique))} curated notes; {len(records["gaps"])} source gaps.')


if __name__ == '__main__': build()
