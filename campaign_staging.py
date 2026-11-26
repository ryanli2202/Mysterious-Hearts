"""Explicit reviewed authoring metadata, separate from the compiled manuscript.

Old saved beats are not rewritten. New pages bind reviewed source spans and
selected core inserts to their original text/condition/era before playback.
"""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def catalogue():
    return json.loads((ROOT/'campaign_prose/staging.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def cores():
    selection=json.loads((ROOT/'assets/campaigns/core/catalog.json').read_text(encoding='utf-8'))
    return {(b['scene_id'],b['source_element']-1):(c['id'],b) for c in selection['core_shots'] for b in c['bindings']}


def segments(key,index,element,mode):
    text=element['text'];entry=catalogue()['scenes'].get(key,{}).get('elements',{}).get(str(index))
    if entry and entry['source_sha256']!=hashlib.sha256(text.encode()).hexdigest():
        raise ValueError('Campaign staging is out of date for '+key+'. Restore matching manuscript/staging files.')
    original_index=element.get('legacy_element',index)
    core=None if element.get('authored') else cores().get((key,original_index))
    if core and core[1]['anchor_text'] not in text:
        raise ValueError('Core-shot source no longer matches '+key+'. Restore the matching campaign files.')
    shot=key+':'+mode
    core_id=element.get('core_id') or (core[0] if core else None)
    visual=__import__('campaign_scene_staging').visual(key,original_index,mode)
    visual.update({k:element[k] for k in ('background','portraits') if k in element})
    shot=visual.pop('shot_id',shot)
    if core_id:shot=(core[1].get('legacy_rei_shot_id') if core else None) or key+':'+core_id
    parts=entry['parts'] if entry else [dict(phase='prose',start=0,end=len(text))]
    if mode=='memory':
        for part in parts:
            if part.get('speaker'):__import__('campaign_eras').validate(key,part['speaker'])
    return [dict(phase=p['phase'],speaker=p.get('speaker'),text=text[p['start']:p['end']],
                 source_element=index,source_start=p['start'],source_end=p['end'],shot_id=shot,core_id=core_id,
                 **({'fox_voice_when':element['when']} if p.get('speaker')=='fox' and element.get('when') else {}),
                 **visual)
            for p in parts]


def deduplicate_core_inserts(lines):
    first={}
    for beat in lines:
        for segment in beat.get('stage_segments',[]):
            core=segment.get('core_id')
            if not core:continue
            source=(beat.get('scene_id'),segment.get('source_element'))
            if first.setdefault(core,source)!=source:
                segment['core_id']=None
                segment['shot_id']=str(beat.get('scene_id'))+':'+beat.get('mode','present')
    return lines
