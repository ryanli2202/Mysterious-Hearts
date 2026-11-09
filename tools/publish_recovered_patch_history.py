"""Publish the reviewed recovery without duplicating existing report or topic IDs."""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import patch_notes as notes

SUMMARIES = {
 'Add Neo Ishida as cast member': ('Neo, Alyssa and their shared home', 'World & story',
  'Neo joined as a hidden, platonic cast member with personal references, a schedule, an apartment and established friendships with Tyler and Daniel. A transparent scene portrait and apartment illustration followed. Alyssa subsequently became a discoverable character with her own archive job, routines, profile and artwork, superseding the earlier off-screen description. Eight Grove photos each then added their hobbies, shared home life and Neo’s friendships. Existing-save migration and engagement preservation were reported.'),
 'Add photos to Yuriko’s grove gallery': ('Yuriko, Sophie and high-school photo memories', 'Art & media',
  'Seven Yuriko group photos added playful memories involving Rei, including cat ears, flour, a crown and a parasol. Eight Sophie photos followed, including school memories dated 2046–2047. High-school reference portraits were created for Rei, Sophie, Emily and Marcus. Another eight school photos were split between Rei and Emily; Rei is deliberately tattoo-free in these earlier memories. Captions, comments and save upgrades were included. One interrupted turn has no completion report and is not counted as another photo release.'),
 'Find missing grove galleries': ('Elliot, Tyler, Valentina, Daniel and Sylvanis galleries', 'Art & media',
  'An initial inventory identified five missing galleries; five later completion reports added eight photos for each character. Elliot’s posts include Ivan comments. Tyler’s cover boxing, dominoes, supper and his father. Valentina’s include three Ivan sibling scenes: sail repairs, karaoke and supper. Daniel’s cover cinema work, drawings, judo and home life. Sylvanis’s use crime-themed scenes and tense replies from Ivan. Save upgrades were reported. The original reports retain temporary unrelated gallery-test failures rather than rewriting them as clean runs.'),
 'Create 8 Garrett outfit variants': ('Garrett outfit request: recovered interrupted work', 'Development history',
  'The root turn was interrupted and has no completion report. It planned eight looks: burgundy velvet, emerald silk, leather biker jacket, camel coat, denim, knit polo, satin bomber and navy waistcoat. These plans are not proof of a completed eight-outfit update. A Garrett alternate-outfit manifest exists in the current project, but that does not establish that this interrupted turn completed or published every requested look. No release date or passed test is assigned to the request.'),
 'Create 8 Emily outfit variants': ('Emily, Sophie and Amy wardrobe expansions', 'Art & media',
  'Emily received eight everyday and occasion looks: florist workwear, café cardigan, spring picnic, rainy day, winter coat, art workshop, garden party and evening velvet. Five more added a navy satin gown, ivory tailored suit, blue floral bikini, teal one-piece and lavender gym set. Sophie then gained thirteen outfits: three bikinis, two gym looks and eight casual/formal options. Amy gained thirteen: three bikinis, two gym looks and eight artistic, casual and formal options. Reports describe transparent PNGs registered in the gallery and Camera outfit chooser, with prompts retained.'),
 'Add Rei outfit variants': ('Rei and Ivan outfits, plus hoodie corrections', 'Art & media',
  'Rei gained eight additional outfits including his black sweater. His charcoal-hoodie shoulders were first broadened, then adjusted to a narrower, softer slope. Six later choices added Japanese techwear, a green-and-ivory sukajan, navy yukata, haori/hakama, gym tank/shorts and teal swim shorts. Ivan gained thirteen looks: two gym, three high-fashion, three idol, four streetwear and one beach outfit. The reports record wardrobe/Camera registration, transparency checks and saved prompts.'),
 'Create eight April outfits': ('April outfit request: recovered interrupted work', 'Development history',
  'The root turn was interrupted after setup and planning, with no completion report. It proposed eight distinct April looks matching her established design and intended to add them to the gallery. Current April outfit manifests exist, but they do not prove completion of this particular interrupted request. The archive preserves the interruption instead of inventing a completed release or a validation result.'),
 'Add Grove gallery photos': ('Expanded Garrett, Ivan, Minsu and Emily group photos', 'Art & media',
  'Garrett received nine photos: three friendly Rei scenes, two Rei modelling shoots, three April scenes and one larger friend group. Ivan received ten: three with Valentina, three solo modelling, two with producers and two with idols. Minsu received nine split between Amy, Sophie and all three together. Emily received nine split between Rei, Sophie and all three together. Each completed batch reports captions, comments, existing-save support and its own historical checks.'),
 'Find missing Grove galleries': ('Yuriko, Lena, Naomi, Celeste, Dev and Rosa galleries', 'Art & media',
  'An inventory of eleven missing galleries preceded six completed eight-photo additions. Yuriko’s covers selfies, miniature sets, theatre lighting, dinner and sketches; Lena’s covers photography, conservation and paella; Naomi’s covers bicycle repair, a handmade mug, riding and dinner. Celeste’s includes the planetarium, birds, sourdough and piano. Dev’s includes radios, tabletop games, photography and chai. Rosa’s includes community lunch, gardening, skates and reading. The additions include captions, comments and automatic existing-save upgrades. The old inventory is historical, not a statement that those galleries remain missing.'),
 'Create Emily’s grove gallery': ('Emily’s first Grove gallery and comment counts', 'Art & media',
  'The first completed Emily gallery release added two photos with dated captions, likes and four friend comments. Gallery cards gained comment counts, and existing saves received the posts automatically. The report cites seventeen tests and a UI smoke check at that time. A later interrupted turn in the same chat has no completion report; subsequent Emily expansions are recorded separately.'),
 'Use Vendetta for world-building': ('Vendetta adaptation and the first Find Charles lead', 'World & story',
  'The game guide adopted Vendetta as a source while explicitly excluding Awakened from Mysterious Hearts. The initial adaptation left some timeline questions open; this is an earlier design stage. A later completed update established Charles’s undercover Syndicate role as writer-only knowledge and kept it out of Garrett’s prompts. Find Charles introduced Mei’s delivery slip dated eleven days after Charles left work, followed by a receiving copy identifying West Pier Cold Storage without a driver signature. The report records both steps, reload persistence and support for existing Garrett saves. A separate interrupted turn is not treated as an additional completed update.'),
 'Add Blisk to the lore': ('Source-world lore, resident portraits and character tiers', 'World & story',
  'The first three recovered completions concern external Vendetta reference documents: the Blisk empire and 2023–2036 war, expanded Sylvanis/Ivan history, and Billy Stevens/Alice Granger profiles. They are source-world edits, not proof every detail shipped into Mysterious Hearts. Three subsequent completions concern the game: twelve local residents with routines and tastes; twelve portraits integrated into conversations, Contacts and Messages; and a split between major characters and simpler town NPCs. Major characters retain full systems; locals use familiarity and conversations without romance, Grove or Meet-Cute. Existing NPC conversations remain while obsolete romance progression is archived. Interrupted and in-progress turns at the recovery snapshot are excluded. Historical reports preserve the stated unrelated test failures.'),
 'Add group photos to Grove gallery': ('Rei group photos and tattoo continuity fixes', 'Art & media',
  'Sixteen Rei group photos were added with captions, comments and save support. Four additional Rei/Garrett modelling editorials followed, alongside a missing tattoo-sleeve fix for a basketball image. Fifteen original group photos were corrected so exposed forearms and wrists match Rei’s tattoos, preserving engagement and captions. Garrett’s white-tee editorial was also corrected with tattoos on both exposed arms. Each correction remains distinct from new-photo additions.'),
 'Generate Garrett gallery images': ('Early protagonist Grove artwork batches', 'Art & media',
  'Garrett’s first four generated images covered cooking, noodles, training and eveningwear; the first report explicitly said UI integration was pending. Four further photos brought that asset batch to eight. Seven portraits were corrected for dragon sleeves, chest/neck tattoos and a leaner build, leaving the noodle image unchanged. Separate completed batches created nine Rei images (modelling, artistic selfies and artwork), ten Ivan performance/fashion images, and eight Minsu medical-study, food-review, taekwondo and selfie images. These asset-creation reports are not retroactively presented as completed UI integration. One interrupted turn remains excluded.'),
 'Align portraits and add art guide': ('Portrait alignment audit: interrupted before completion', 'Development history',
  'The recovered root turn ended by interruption without a completion report. Its inspection identified inconsistent realistic shading and fabric texture in supporting portraits and an initials placeholder for Valentina. It proposed comparing supplied references, correcting portraits and writing an art guide. No completed alignment pass or finished guide is certified from this chat.'),
 'Add texting notification sounds': ('Text audio, typing indicators and chat bubbles', 'Phone & social',
  'Sent/received MP3 effects were added for direct and group texts with a sound toggle, while in-person dialogue remained silent. A looping typing sound followed, stopping on completion/error and respecting mute. The next update added a three-dot animated typing bubble with the character name. Another added right-aligned blue outgoing bubbles, left-aligned grey incoming bubbles and group sender names, while preserving the in-person layout. A fifth interrupted turn has no completed update. Audio and layout checks quoted in original reports are historical claims, not new checks performed by this recovery.'),
 'Add at-home character portraits': ('Home and sleep portraits, gallery browsing and locks', 'Art & media',
  'Minsu, Rei and Garrett gained home-specific portraits and chat location/travel labels. Sleep portraits followed for those three, then for Amy, April, Emily, Samantha and Sophie. Ten casual/evening portraits introduced the Portrait gallery with character filters, previous/next navigation and full-resolution drag-to-pan. Five later completions each added six pictures to one love interest’s gallery, bringing each to eight at that stage. Bedroom photos were then gated on an official relationship with that specific character; casual/evening photos remained available. Early sleep-hour descriptions are historical and do not override current schedule logic.'),
}


def main():
    archive=notes.ROOT/'patch_notes'
    recovered=json.loads((archive/'recovered_history.json').read_text(encoding='utf-8'))
    old=json.loads((archive/'development_records.json').read_text(encoding='utf-8'))
    data=json.loads(notes.CATALOG.read_text(encoding='utf-8'))
    entries=data['releases']; ids={r['id'] for r in entries}
    known={(r['turn'],r['text']) for r in old['records']}
    added=0
    for r in recovered['records']:
        if (r['turn'],r['text']) not in known:
            old['records'].append(r); known.add((r['turn'],r['text']))
        key='report-'+r['turn']
        if key in ids:continue
        ids.add(key);added+=1
        entries.append(dict(id=key,title=r['title'],kind='Development report',category='Original reports',
            date=datetime.fromtimestamp(r['completed_at'],timezone(timedelta(hours=10))).date().isoformat(),
            summary='Recovered original completion report from a previously oversized chat.',body=r['text'],
            save_impact='Historical report; consult the current feature notes for compatibility.',
            provenance='Recovered from local task_complete event. Date is chat completion in Australia/Brisbane, not a release date. Historical validation claims remain attributed to the original report.',
            sources=['patch_notes/recovered_history.json',r['source_file']+' — ordinal '+str(r['source_ordinal']),'Turn: '+r['turn']]))
    chapters=[]
    for chat in recovered['chats']:
        title,category,body=SUMMARIES[chat['title']]
        key='recovered-'+chat['thread']
        records=[r for r in recovered['records'] if r['thread']==chat['thread']]
        evidence='\n\nRecovered reports (chat-completion dates, not release dates):\n'+('\n'.join('- '+datetime.fromtimestamp(r['completed_at'],timezone(timedelta(hours=10))).isoformat(timespec='seconds')+' · '+r['turn'] for r in records) if records else '- No completed report. The source records an interrupted root turn.')
        item=dict(id=key,title=title,kind='Retrospective',category=category,date=None,
            summary=body.split('. ')[0]+'.',body=body+evidence,
            save_impact='Archive-only recovery changes no game state. Historical migration statements are retained as reports, not newly executed migrations.',
            provenance='Source chat: '+chat['title']+'. All available root-session completion events scanned. '+str(chat['completed_turns'])+' completed turns; '+str(len(chat['unfinished_turns']))+' unfinished/interrupted turns at the recovery snapshot. Source-world changes, asset-only work and interrupted requests are distinguished from completed game updates.',
            sources=['patch_notes/recovered_history.json','patch_notes/RECOVERY.md'])
        if key not in ids: chapters.append(item); ids.add(key)
    release=dict(id='release-2026-11-07-history-recovery',title='Recovered the 17 oversized development chats',kind='Release',category='Interface',date='2026-11-07',
        summary='Restored missing historical reports and detailed notes from local session logs.',
        body='Scanned all 17 formerly inaccessible root-session logs. Recovered 66 completed reports, including 59 previously absent reports. Added one detailed historical chapter per chat, including explicit interrupted-work records for the three chats without completed reports. Retained original timestamps, source file names, event ordinals and turn IDs.\n\nExternal Vendetta lore edits, generated assets awaiting integration, superseded behavior and unfinished requests are labelled. The old oversized-chat retrieval gaps are resolved; unfinished work is not relabelled as shipped. No game feature, artwork or story save is changed by this archive update.',
        save_impact='No save migration or story reset. Reopen the patch notes viewer to load the updated catalogue.',
        provenance='Local log recovery performed on 7 November 2026. Historical tests are not recertified. Recovery verification is recorded in patch_notes/RECOVERY.md.',
        sources=['patch_notes/recovered_history.json','patch_notes/RECOVERY.md','tools/recover_patch_history.py'])
    if release['id'] not in ids: chapters.insert(0,release)
    entries[:0]=chapters
    old['resolved_gaps']=[dict(title=c['title'],thread=c['thread'],resolution='Local root-session log scanned',completed_reports=c['completed_turns'],unfinished_turns=c['unfinished_turns']) for c in recovered['chats']]
    old['gaps']=[]
    notes.validate(data)
    notes.atomic_write(archive/'development_records.json',json.dumps(old,ensure_ascii=False,indent=2))
    notes.atomic_write(notes.CATALOG,json.dumps(data,ensure_ascii=False,indent=2))
    notes.export(notes.select(entries),archive/'PATCH_NOTES.md')
    print(f'Added {added} reports and {len(chapters)} curated entries; total {len(entries)} entries, {len(notes.select(entries))} curated.')


if __name__=='__main__':main()
