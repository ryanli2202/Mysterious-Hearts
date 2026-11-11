"""Reproducible Rei campaign artwork inventory and production bookkeeping.

Does not modify gameplay or player saves. Generation uses the built-in image tool.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import itertools
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import campaign_prose as prose

BASE = ROOT / 'assets/campaigns/rei'
MANIFEST = BASE / 'manifest.json'
WORK = ROOT / 'roadmap/rei-campaign-artwork'
REFS = WORK / 'references'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(data):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def read():
    return json.loads(MANIFEST.read_text(encoding='utf-8'))


CAST = {
 'rei': ('rei-selection.png', 'Adult Rei Takamura, Japanese, 21, 184 cm, lean, shaggy layered black hair, grey-dark eyes, paired silver lip piercings and ear piercings. Black open-collar shirt, black trousers. Detailed black dragon/floral/thorn tattoo work on neck, upper chest AND BOTH ARMS down to the wrists; preserve ALL exposed arm ink, including forearms when sleeves are rolled. Skin only, not fabric or hands. Reference tattoo body image defines the actual design; do not make him shirtless.'),
 'rei_school': ('rei-high-school.png', 'Rei at 17: shaggy black hair, grey eyes, small silver earrings and paired lip piercings, charcoal T-shirt, blue-grey overshirt, dark jeans. NO TATTOOS ANYWHERE in this school era.'),
 'garrett': ('garrett-home.png', 'Adult Garrett Han, tall athletic Chinese man, tousled golden-blond hair, golden eyes, neck/chest tattoos, gold earrings; light open-collar shirt and dark trousers, apron when cooking. Use his own identity reference, not Rei\'s face.'),
 'yuriko': ('yuriko-selection.png', 'Adult Yuriko Takamura, short dark wavy bob, warm dark eyes, amber hair clip, olive overshirt over modest light shirt, dark trousers. Rei\'s sister; sibling familiarity, never romance.'),
 'emily': ('emily-selection.png', 'Adult Emily Fields, long blonde hair and blunt fringe, blue eyes, round glasses, modest light blouse and navy pinafore. Soft, thoughtful expression; natural adult proportions.'),
 'sophie': ('sophie-selection.png', 'Adult Sophie Lane, athletic woman, long brown hair in high ponytail, green eyes, green track jacket and casual trousers; attentive, direct, warm.'),
 'emily_school': ('emily-high-school.png', 'School-era Emily, 16, long blonde hair and fringe, blue eyes, round glasses, modest blouse and dusty-blue pinafore. Age-appropriate school clothes.'),
 'sophie_school': ('sophie-high-school.png', 'School-era Sophie, 17, brown ponytail, green eyes, age-appropriate green school sports jacket and casual trousers.'),
 'marcus': ('marcus-high-school.png', 'Marcus, slim schoolboy, tousled short auburn hair with cowlick, hazel eyes, warm fair skin and subtle freckles, mustard cardigan over muted teal shirt, dark trousers. Wry shy smile. No tattoos or piercings. A living historical friend in filmmaking scenes ONLY.'),
 'joseph_school': ('joseph-richter-high-school.png', 'School-era Joseph Richter. Use supplied youthful face and school clothing. No cybernetics, no adult executive armour.'),
 'joseph': ('joseph-richter-selection.png', 'Adult Joseph Richter, Blackstone executive; preserve reference face, hair and dark executive clothing.'),
 'richter_combat': ('guards/richter_cybernetic.png', 'Adult Joseph Richter with the established powered spinal frame and reinforced cybernetic arms. Match reference equipment; restrained targeting lights, no arbitrary powers.'),
 'emi': ('emi-suda-selection.png', 'Emi Suda, current adult successor administrator; identity and outfit from reference.'),
 'ren': ('ren-aoki-selection.png', 'Ren Aoki, current adult successor administrator; identity and outfit from reference.'),
 'daichi': ('daichi-kurose-selection.png', 'Daichi Kurose, current adult successor leader; identity and outfit from reference, measured manner.'),
 'robin': ('robin-vale-selection.png', 'Robin Vale, public Blackstone reception clerk; identity and attire from reference. Supplying a public form, not confessing or granting private records.'),
}
VENUES = {
 'rei_home':'Rei\'s present-day apartment, quiet drawing table, papers, pencil, lived-in shelves, subdued daylight. Use the location reference for environment only.',
 'noodle_shop':'Golden Dragon noodle shop: warm familiar modest Chinese restaurant, wooden tables and service counter, bowls and dumplings; follow location reference.',
 'square':'Winterfield town square, quiet outdoor seating/work table, ordinary daytime social visit.',
 'park':'Winterfield park, leafy walking path and seating, natural daylight; no school campus.',
 'archive':'Public archive reading room, orderly files, long reading table, documents with indistinct marks; no invented legible evidence.',
 'hamayashi_house':'Kurose House, present-day Hamayashi-kai successor meeting room or its exterior when the passage says outside. No childhood clan members.',
 'blackstone_hq':'Blackstone public reception and entrance, contemporary restrained corporate architecture.',
 'blackstone_command':'Blackstone executive command, secured modern office and machinery, restrained clinical light.',
 'rei-high-school':'Historical school in 2046–2047, ordinary school courtyard/bench or classroom film-work table, following the passage. All students in historical references; no adult tattoos.',
}


def source_ref(relative, label, refs):
    source=ROOT/relative
    if not source.exists():
        raise FileNotFoundError(source)
    digest=sha(source)
    dest=REFS/(source.stem+'-'+digest[:10]+source.suffix)
    REFS.mkdir(parents=True, exist_ok=True)
    if not dest.exists():shutil.copy2(source,dest)
    if sha(dest)!=digest:raise ValueError('Reference snapshot mismatch')
    refs[str(dest.relative_to(ROOT))]=dict(source=relative,sha256=digest,role=label)
    return str(dest)


def configuration(key, mode, ctx, text):
    n=int(key[2:]) if key.startswith('RD') else 0
    venue='rei_home';cast=['rei']
    if n in (3,4,8,14,22,28,34):venue='noodle_shop';cast=['rei','garrett']
    elif n in (2,6,18):cast=['rei','yuriko']
    elif n==7:venue='square';cast=['rei','emily']
    elif n==10:venue='square';cast=['rei','emily','sophie']
    elif n==12:venue='park';cast=['rei','sophie']
    elif n in (5,17):venue='archive'
    elif n in (19,23,24,25):venue='hamayashi_house';cast=['rei','emi','ren','daichi']
    elif n==20:venue='hamayashi_house'
    elif n==21:venue='square';cast=['rei',ctx.get('visitor','emily')]
    elif n==27:venue='square';cast=['rei','emily','sophie']
    elif n==16:venue='blackstone_hq';cast=['rei','robin']
    elif n==29:venue='blackstone_hq'
    elif n in (30,31):venue='blackstone_command';cast=['rei','richter_combat']
    elif n==32:venue='park';cast=['rei','sophie']
    elif n==35:cast=['rei','yuriko','emily','sophie']
    if mode=='memory' and n in (9,11,13):
        venue='rei-high-school'
        cast=['rei_school']+{9:['marcus'],11:['emily_school','sophie_school'],13:['joseph_school']}[n]
    if n==25 and ctx.get('phase')=='after':cast=['rei'];venue='hamayashi_house'
    if n==31 and ctx.get('phase')=='failure':cast=['rei']
    return venue,cast


def build():
    if MANIFEST.exists():raise RuntimeError('Manifest already exists; preserve stable IDs and production records.')
    scenes=prose.library(); shots=[];refs={};routes={}
    def add(key,text,mode='present',ctx=None,cast=None,venue=None,origin='compiled-page',bindings=None):
        ctx=ctx or {}
        default_venue,default_cast=configuration(key,mode,ctx,text)
        cast=cast if cast is not None else default_cast
        venue=venue or default_venue
        fingerprint=hashlib.sha256(json.dumps([key,text,mode,cast,venue],ensure_ascii=False).encode()).hexdigest()
        prior=next((x for x in shots if x['source_fingerprint']==fingerprint),None)
        if prior:
            if bindings and bindings not in prior['bindings']:prior['bindings'].append(bindings)
            return prior['id']
        number=1+sum(x['scene_id']==key for x in shots)
        ident=f'{key}-S{number:02}'
        reference_paths=[];roles=[]
        for who in cast:
            filename,description=CAST[who]
            reference_paths.append(source_ref('assets/portraits/'+filename,who,refs))
            roles.append(f'Image {len(reference_paths)}: {who}, identity/age/clothing reference. {description}')
        if 'rei' in cast:
            reference_paths.append(source_ref('assets/portraits/rei-beach.png','Rei exposed arm/chest/neck tattoo placement only',refs))
            roles.append(f'Image {len(reference_paths)}: Rei\'s detailed body tattoo reference ONLY. Do not copy bare torso, shorts, pose or background. Preserve BOTH tattooed arms wherever skin is visible.')
        locpath='assets/ui/locations/'+venue+'.png'
        if (ROOT/locpath).exists():
            reference_paths.append(source_ref(locpath,'location environment only',refs))
            roles.append(f'Image {len(reference_paths)}: environment/location reference only, adapted to this shot\'s framing.')
        framing=['medium-wide establishing view with characters doing the passage\'s physical action','three-quarter medium shot with natural interaction and readable hands','closer emotional shot, maintaining enough environment and props to identify the action','over-shoulder shot focusing on the meaningful physical object/action','side-angle two/three-person composition; if solo, intimate side profile'][((number-1)%5)]
        prompt=(f'Use case: illustration-story. Asset: ONE standalone landscape 16:9 visual-novel shot for Mysterious Hearts, Rei campaign, {ident}, {scenes.get(key,{}).get("title",key)}. '
          'Create a new complete scene using reference images for identity and environment; they are not edit targets.\n'
          +'\n'.join(roles)+'\n'
          +f'Era: {mode}. Setting: {VENUES.get(venue,venue)}. '
          +f'Composition: {framing}. Depict one specific physical moment actually supported by the selected passage below. Follow explicit room/era/solitude transitions. Do not illustrate figurative language literally. '
          +'Preserve the named cast only when physically present. A person mentioned or remembered is not automatically present. No ghost Marcus, no montage, no extra panels. '
          +'For school loss scenes, show the friends receiving/supporting grief only: no body, self-harm imagery, method, final note, imagined final moments, or invented explanation. For school conflict, non-graphic confrontation with no blood or severe injury, and no triumphant glorification. '
          +'Style: cohesive polished semi-realistic illustrated manhwa, dimensional faces with restrained eyes, clean tapered contours, designed shadows with soft transitions, detailed layered hair, believable anatomy/hands, painted environment depth. Not photo, not 3D. '
          +'Keep character identity, piercings and era accurate. CRITICAL: adult Rei has intricate winding black dragon/floral/thorn tattoos over BOTH arms, including exposed forearms, plus neck/chest, matching tattoo reference. NEVER leave exposed adult forearms blank, never paint ink through fabric. School Rei has NO tattoos. '
          +'Wide horizontal full scenic opaque image, important faces/action above bottom 18% with quieter lower area for later narration. No text, captions, UI, logos, signature, watermark, borders or comic panels. Paper writing is indistinct marks, not invented legible facts. One image, not a contact sheet.\n'
          +'SELECTED AUTHORED PASSAGE (context only; never render these words in the image):\n'+text)
        shots.append(dict(id=ident,scene_id=key,scene_title=scenes.get(key,{}).get('title',key),origin=origin,mode=mode,venue=venue,cast=cast,narration=text,bindings=[bindings] if bindings else [],source_fingerprint=fingerprint,reference_paths=reference_paths,prompt=prompt,path=f'assets/campaigns/rei/shots/{ident.lower()}.png',status='pending',review=None))
        return ident

    for key,spec in scenes.items():
        if not key.startswith('RD'):continue
        fields={}
        for e in spec['elements']:
            for field,value in e.get('when',{}).items():
                values=fields.setdefault(field,[])
                if value not in values:values.append(value)
        if 'disclosure'in fields and 'private'not in fields['disclosure']:fields['disclosure'].append('private')
        routes[key]=[]
        for values in itertools.product(*fields.values()):
            ctx=dict(player='rei',choice=0,phase='before',disclosure='share',support='help',richter=False,ending=None,visitor='emily')|dict(zip(fields,values))
            ids=[]
            for index,page in enumerate(prose.pages(key,ctx)):
                binding=dict(context=dict(zip(fields,values)),page_index=index)
                ids.append(add(key,page['narration'],page.get('mode','present'),ctx,bindings=binding))
            if ids:routes[key].append(dict(context=dict(zip(fields,values)),shots=ids))

    # Authored pages added by Python assembly, in addition to the 35 catalogue scenes.
    add('RD01','Rei had kept this book for years. Today he chose to open it. Yuriko had memories of her own; Garrett knew some of the broad history Rei had trusted him with. Neither could complete the gaps for him. He could ask for company later, or keep the page private. For now, he wanted to know what was actually there.',origin='action_pages opening')
    for key in ('RD01','RD20','RD31'):
        question,options=prose.REFLECTIONS[key]
        add(key,question+' Rei pauses in the current room to reflect, before choosing.',origin='reflection question',cast=['rei'])
        for value,label,response in options:add(key,response,origin='reflection response',cast=['rei'],bindings={'reflection':value})
    for key in ('RD09','RD11','RD13'):
        add(key,'Back in the present, adult Rei considers what to do with the storyboard page at his own table.',origin='memory return reflection',cast=['rei'],venue='rei_home')
        for value,text in [('pause','Rei put the page down. He noticed the table beneath his hands and the room around it. The memory could remain true without filling every moment of the present.'),('keep','He left the page where he could see it. He did not ask the memory to answer another question before he was ready.')]:
            add(key,text,origin='memory return response',cast=['rei'],venue='rei_home',bindings={'reflection':value})
    for key in ('RD22','RD28'):
        add(key,'Rei kept the details to himself. “I can’t give you the whole account,” he said. “Then don’t,” Garrett answered. “I can offer you a seat without asking for the file.” Rei accepted the company. His decision and his next steps remained his own.',origin='private social override',bindings={'disclosure':'private'})
    for who in ('emily','sophie'):
        for page in prose.pre_mission_visit({},[who],{}):add('RD27',page['narration'],cast=['rei',who],origin='single friend availability',bindings={'attending':[who]})
    for count in range(3):
        for cast in itertools.combinations(('yuriko','emily','sophie'),count):
            for index,page in enumerate(prose.ending_visit({},list(cast))):
                shotcast=['rei']+list(cast) if index==0 else ['rei',cast[index-1]]
                add('RD35',page['narration'],cast=shotcast,origin='ending availability',bindings={'attending':list(cast),'page_index':index})
    add('RD22','Rei had decided he needed a boundary before an answer. Garrett could ask him a question without being allowed to choose the answer for him.',origin='continuity flag',bindings={'RD20':'boundary'})
    add('RD33','He had left the first gaps visible. Finishing the investigation did not require him to fill them now.',origin='continuity flag',bindings={'RD01':'gaps'})
    add('RD30','The executive objective remained unresolved. Rei checked what he could do now, without pretending the previous attempt had supplied an apology or stopped the programme.',cast=['rei'],origin='confrontation retry')
    add('RX01','The mission remained unresolved. Rei kept the evidence already secured. Resting and reassessing would not undo it; neither would pretending this attempt had finished the work.',cast=['rei'],venue='rei_home',origin='generic failed mission aftermath')
    # Optional response-confirmation pages are UI overlays on the current shot, not new scenes.
    # Combat is dynamic; these eight site shots cover authored destination transitions.
    import organisation_guards as guards
    for i,venue in enumerate((*guards.HAMAYASHI,*guards.BLACKSTONE),1):
        add('RC'+str(i).zfill(2),f'Rei approaches {venue.replace("_"," ")}, alone, at the beginning of the authored campaign encounter. He checks the immediate entrance and keeps the retained evidence secure. No victory is implied. Show the location and Rei preparing to enter, without generic crowds or an invented fight outcome.',cast=['rei'],venue=venue,origin='campaign encounter site establishing shot')
    data=dict(schema_version=1,roadmap_id='MH-016',recorded='2026-11-11',status='in production',runtime_installed=False,scope='All 35 existing Rei compiled scenes, conditional narrative pages and Python-authored reflection/availability/retry pages, plus eight encounter-site establishing shots. Response confirmation controls retain the current shot; dynamic turn-by-turn combat is not fixed scripted art.',tattoo_rule='Adult Rei: both arms, forearms, neck/chest wherever exposed, source-matched. School Rei: no tattoos.',source_files={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'campaign_prose/catalog.json',ROOT/'campaign_prose.py',ROOT/'rei_story.py',ROOT/'campaign_flashbacks.py']},references=refs,routes=routes,shots=shots)
    write(data)
    print(json.dumps({'scenes':len(routes),'shots':len(shots),'references':len(refs)},ensure_ascii=False))


def record(ident,source):
    from PIL import Image
    data=read();shot=next(s for s in data['shots'] if s['id']==ident)
    src=Path(source);dest=ROOT/shot['path'];dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():raise RuntimeError('Do not overwrite generated final: '+str(dest))
    with Image.open(src) as im:im.verify()
    shutil.copy2(src,dest)
    with Image.open(dest) as im:metadata=dict(size=list(im.size),mode=im.mode,format=im.format)
    shot.update(status='generated',generated_source=str(src),sha256=sha(dest),metadata=metadata)
    write(data)
    print(ident+' saved '+str(dest))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['build','next','record','status','review','sheets','validate']);parser.add_argument('args',nargs='*');args=parser.parse_args()
    if args.action=='build':build();return
    if args.action=='record':record(*args.args);return
    data=read()
    if args.action=='next':print(json.dumps([s for s in data['shots'] if s['status']=='pending'][:int(args.args[0] if args.args else 4)],ensure_ascii=False));return
    if args.action=='review':
        ids=args.args[0].split(',');note=args.args[1]
        for shot in data['shots']:
            if shot['id'] in ids:
                assert shot['status']!='pending'
                shot['review']=dict(status='accepted',note=note);shot['status']='accepted'
        write(data);print('Reviewed '+str(len(ids))+' shots.');return
    if args.action=='status':
        from collections import Counter
        print(json.dumps(dict(total=len(data['shots']),status=dict(Counter(s['status'] for s in data['shots'])))));return
    if args.action=='validate':
        from PIL import Image
        assert len(set(s['id'] for s in data['shots']))==len(data['shots'])
        assert len(set(s['path'] for s in data['shots']))==len(data['shots'])
        for filename,digest in data['source_files'].items():assert sha(ROOT/filename)==digest,filename+' source changed'
        for filename,info in data['references'].items():assert sha(ROOT/filename)==info['sha256']
        found=set()
        for shot in data['shots']:
            if shot['status']=='pending':continue
            path=ROOT/shot['path'];assert path.exists(),shot['id']
            assert sha(path)==shot['sha256'];assert shot['sha256']not in found,'Duplicate image';found.add(shot['sha256'])
            with Image.open(path) as im:
                assert im.width>im.height and im.width>=1280 and im.height>=720,(shot['id'],im.size)
            if 'rei_school'in shot['cast']:assert not any('rei-beach'in p for p in shot['reference_paths'])
            if 'rei'in shot['cast']:assert any('rei-beach'in p for p in shot['reference_paths'])
        print(f'Validated {len(data["shots"])} unique shot records, {len(found)} generated images, reference/source hashes and tattoo-era reference rules.');return
    if args.action=='sheets':
        from PIL import Image,ImageOps,ImageDraw
        selected=[s for s in data['shots'] if s['status']!='pending']
        dest=WORK/'review';dest.mkdir(exist_ok=True)
        for start in range(0,len(selected),12):
            group=selected[start:start+12];sheet=Image.new('RGB',(1440,4*300),'#172231');draw=ImageDraw.Draw(sheet)
            for i,shot in enumerate(group):
                im=Image.open(ROOT/shot['path']).convert('RGB');im=ImageOps.contain(im,(468,264));x=(i%3)*480+(480-im.width)//2;y=(i//3)*300
                sheet.paste(im,(x,y));draw.text(((i%3)*480+10,y+270),shot['id']+' '+shot['mode'],fill='#e1e8ed')
            sheet.save(dest/f'sheet-{start//12+1:02}.jpg',quality=92)
        print(str(dest))


if __name__=='__main__':main()
