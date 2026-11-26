"""Offline, source-checked speech bindings and transient reader playback.

Packages can add other speakers without changing the reader or sound system.
Unrecognised source adapters or stale snapshots remain text-only.
"""
import hashlib
import json
import logging
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets/sounds/campaigns'


def sha(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()


@lru_cache(maxsize=1)
def manifest():
    try:
        data=json.loads((ASSETS/'manifest.json').read_text(encoding='utf-8'))
        if not isinstance(data,dict) or data.get('version')!=1 or not isinstance(data.get('lines'),list):return []
        strings=('id','campaign','scene','speaker','era','source_sha256','subtitle','file','sha256')
        return [r for r in data['lines'] if isinstance(r,dict) and r.get('accepted') is True
                and all(isinstance(r.get(k),str) for k in strings)
                and all(type(r.get(k)) is int for k in ('source_start','source_end'))
                and isinstance(r.get('when',{}),dict) and isinstance(r.get('access_conditions',{}),dict)
                and (not r.get('source_symbol') or r.get('adapter')=='fixed_fox'
                     or 'reflection_value' in r.get('access_conditions',{}))]
    except (OSError,ValueError,KeyError,TypeError):
        logging.warning('Campaign voice manifest unavailable; using captions.')
        return []


@lru_cache(maxsize=512)
def _file_valid(path,modified,size,expected):
    try:return hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected
    except OSError:return False


def audio_path(record,pcm=False):
    try:
        path=(ASSETS/record['pcm_file' if pcm else 'file']).resolve()
        if not path.is_relative_to(ASSETS.resolve()) or path.suffix.lower()!=('.wav' if pcm else '.mp3'):return None
        info=path.stat()
        return path if _file_valid(str(path),info.st_mtime_ns,info.st_size,record['pcm_sha256' if pcm else 'sha256']) else None
    except (OSError,KeyError,TypeError,ValueError):return None


def playable(row):
    path=audio_path(row)
    pcm=audio_path(row,pcm=True)
    return dict(row,path=path or pcm,pcm_path=pcm) if path or pcm else None


def fixed_binding(scene, source, speaker='fox'):
    """Bind an explicitly authored callback to its recorded source literal."""
    for row in manifest():
        if (row.get('adapter'),row['scene'],row['speaker'],row['source_sha256'])==(
                'fixed_fox',scene,speaker,sha(source)):
            return dict(scene=scene,source=source)
    return None


def fixed_record(binding, player, era, displayed):
    if not isinstance(binding,dict) or not isinstance(binding.get('source'),str):
        return None
    source=binding['source']
    for row in manifest():
        if (row.get('adapter')=='fixed_fox' and row['scene']==binding.get('scene')
                and row['era']==era and player in row.get('viewpoints',[])
                and row['source_sha256']==sha(source)
                and source[row['source_start']:row['source_end']]==displayed==row['subtitle']):
            return playable(row)
    return None


def fixed_page(beat, scene, source):
    """Split the exact authored quotation from its surrounding prose."""
    binding=fixed_binding(scene,source)
    if not binding:return beat
    row=next(r for r in manifest() if r['scene']==scene and r.get('adapter')=='fixed_fox')
    caption=beat['narration']
    quote='“'+row['subtitle']+'”'
    start=caption.find(quote)
    if start<0 or caption.count(quote)!=1:return beat
    pieces=[]
    if caption[:start].strip():pieces.append(dict(phase='prose',text=caption[:start]))
    pieces.append(dict(phase='dialogue',speaker='fox',text=quote,fixed_voice=binding))
    if caption[start+len(quote):].strip():pieces.append(dict(phase='prose',text=caption[start+len(quote):]))
    beat.update(stage_segments=pieces,fixed_voice_caption_hash=sha(caption))
    return beat


def sync_fixed(playback, state, token, record):
    import campaign_prose
    preferences=campaign_prose.read(state).get('preferences',{})
    playback.configure(preferences.get('voice_enabled',True),preferences.get('voice_volume',70))
    playback.enter(token,record)


def fixed_exchange(beat, player, scenes):
    lines=[(player,beat['player'])] if beat['player'] else []
    lines.extend(beat['speeches'])
    parts=[]
    for speaker,text in lines:
        part=dict(phase='dialogue',speaker=speaker,text=text)
        binding=fixed_binding(scenes[speaker],text,speaker) if speaker in scenes else None
        if binding:part['fixed_voice']=binding
        parts.append(part)
    if beat['narration']:parts.append(dict(phase='prose',text=beat['narration']))
    beat.update(stage_segments=parts,fixed_voice_caption_hash=sha(beat['narration']))


def reaction_record(state, fight):
    if not fight or fight.get('kind')!='interpol' or fight.get('status')!='active':return None
    event=fight.get('fox_reaction_voice')
    if not isinstance(event,dict) or event.get('exchange')!=len(fight.get('exchanges',[])):return None
    index=event.get('log_index')
    log=fight.get('log',[])
    binding=event.get('binding')
    if type(index) is not int or not 0<=index<len(log) or not isinstance(binding,dict):return None
    source=log[index]
    if source!=binding.get('source') or 'Fox: “' not in source:return None
    caption=source.split('Fox: “',1)[1].split('”',1)[0]
    return fixed_record(binding,state.get('player'),'present',caption)


def resolve(beat,unit,player):
    """Match the actually displayed frozen segment, never its quotation alone."""
    if unit.get('phase')!='dialogue':return None
    parts=beat.get('stage_segments',[])
    index=unit.get('segment',-1)
    if not isinstance(index,int) or not 0<=index<len(parts):return None
    part=parts[index]
    if part.get('phase')!='dialogue' or part.get('speaker')!=unit.get('speaker'):return None
    import campaign_presentation
    displayed=campaign_presentation.passages(part.get('text',''))
    page=unit.get('page',0)
    if type(page) is not int or not 0<=page<len(displayed) or unit.get('text')!=displayed[page]:return None
    if 'voice_source_text' in part and part['text'] not in campaign_presentation.passages(part['voice_source_text']):return None
    if part.get('fixed_voice') and part.get('speaker')=='fox' and beat.get('mode')!='memory':
        if beat.get('fixed_voice_caption_hash')!=sha(beat.get('narration','')):return None
        return fixed_record(part['fixed_voice'],player,'present',
                            part.get('voice_source_text',part['text']).strip('“”'))
    era=beat.get('era_id') if beat.get('mode')=='memory' else 'present'
    if beat.get('mode')=='memory':
        import campaign_eras
        actual=campaign_eras.SCENES.get(beat.get('scene_id'))
        if era is None:era=actual
        if era!=actual:return None
    for row in manifest():
        if (row.get('scene'),row.get('speaker'),row.get('era'))!=(beat.get('scene_id'),unit.get('speaker'),era):continue
        if player not in row.get('viewpoints',[row.get('campaign')]):continue
        text=part.get('voice_source_text',part.get('text'))
        if text!=row.get('subtitle'):continue
        if row.get('source_symbol'):
            import campaign_prose
            binding=beat.get('voice_reflection',{})
            if binding!={'id':row['scene'],'value':row['access_conditions']['reflection_value']}:continue
            options=campaign_prose.REFLECTIONS.get(row['scene'],('',[]))[1]
            response=next((o[2] for o in options if o[0]==binding['value']),None)
            if response is None or sha(response)!=row['source_sha256'] or beat.get('narration')!=response:continue
            if part.get('source_start')!=row['source_start'] or part.get('source_end')!=row['source_end']:continue
        else:
            if row['speaker']=='fox' and row.get('when') and part.get('fox_voice_when')!=row['when']:continue
            keys=('source_element','source_start','source_end')
            if any(part.get(k)!=row.get(k) for k in keys):continue
            import campaign_prose
            try:element=campaign_prose.library()[row['scene']]['elements'][row['source_element']]
            except (KeyError,IndexError,TypeError):continue
            if sha(element['text'])!=row['source_sha256'] or element.get('when',{})!=row.get('when',{}):continue
            if element['text'][row['source_start']:row['source_end']]!=text:continue
            import campaign_staging
            current_parts=campaign_staging.catalogue().get('scenes',{}).get(row['scene'],{}).get('elements',{}).get(str(row['source_element']),{}).get('parts',[])
            if not any(p.get('speaker')==row['speaker'] and p.get('phase')=='dialogue' and p.get('start')==row['source_start'] and p.get('end')==row['source_end'] for p in current_parts):continue
        return playable(row)
    return None


def reflection_page(page,key,value):
    """Add explicit speech only from an approved reflection source binding."""
    for row in manifest():
        if row.get('source_symbol') and row['scene']==key and row.get('access_conditions',{}).get('reflection_value')==value:
            text=page['narration'];start,end=row['source_start'],row['source_end']
            if sha(text)!=row['source_sha256'] or text[start:end]!=row['subtitle']:continue
            page['voice_reflection']=dict(id=key,value=value)
            page['stage_segments']=[dict(phase='dialogue',speaker=row['speaker'],text=text[start:end],source_element='reflection:'+value,source_start=start,source_end=end),
                                    dict(phase='prose',text=text[end:],source_element='reflection:'+value)]
            return page
    return page


class Playback:
    """No story callbacks, save data, timers or provider requests live here."""
    def __init__(self,sounds):
        self.sounds=sounds;self.token=None;self.record=None;self.enabled=True;self.volume=70;self.error=''

    def enter(self,token,record,autoplay=True):
        if token==self.token and (record or {}).get('id')==(self.record or {}).get('id'):return
        self.stop();self.token=token;self.record=record;self.error=''
        if autoplay:self.replay()

    def replay(self):
        self.stop();self.error=''
        if not self.record or not self.enabled:return False
        try:return self.sounds.play_campaign_voice(self.record['path'],self.volume,self.record.get('pcm_path'))
        except (OSError,ValueError) as exc:self.error=str(exc);return False

    def stop(self):self.sounds.stop_campaign_voice()

    def configure(self,enabled,volume):
        self.enabled=bool(enabled);self.volume=max(0,min(100,int(float(volume))))
        if not self.enabled:self.stop()
        else:
            try:self.sounds.set_campaign_volume(self.volume)
            except (OSError,ValueError) as exc:self.error=str(exc);self.stop()
