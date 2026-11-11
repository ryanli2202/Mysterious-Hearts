"""Bounded, non-executable portable character packages. Never extracts zip paths."""
import copy
import io
import hashlib
import json
import os
from pathlib import Path
import uuid
import zipfile
from PIL import Image
import custom_protagonist as custom

MAX_PACKAGE = 12 * 1024 * 1024


def export(profile, destination, private=False):
    p = custom.validate(profile)
    if not private:
        p.pop('private_history', None)
        ident = p.get('identity', {})
        if not ident.get('legal_public', True):
            p['name'] = ident.get('public_name') or p.get('preferred_name') or 'New arrival'
        p['identity'] = dict(public_name=ident.get('public_name',''), legal_public=True)
    p.pop('profile_id', None)
    portrait = custom.portrait_path(profile).read_bytes()
    if len(portrait)>MAX_PACKAGE: raise ValueError('Portrait exceeds package limit.')
    destination=Path(destination)
    temp=destination.with_name(destination.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
            z.writestr('character.json',json.dumps(dict(format='MH-character',version=1,private=private,profile=p)))
            z.writestr('portrait.png',portrait)
        if temp.stat().st_size>MAX_PACKAGE: raise ValueError('Package exceeds 12 MB.')
        # Explicit path, but never silently replace an existing export.
        with destination.open('xb') as output: output.write(temp.read_bytes())
    finally:
        temp.unlink(missing_ok=True)
    return destination


def inspect(path):
    path=Path(path)
    if path.stat().st_size>MAX_PACKAGE: raise ValueError('Package exceeds 12 MB.')
    try:
        with zipfile.ZipFile(path) as z:
            info=z.infolist()
            if len(info)!=2 or {x.filename for x in info}!={'character.json','portrait.png'}:
                raise ValueError('Package must contain only character.json and portrait.png; paths and extra files are rejected.')
            if sum(x.file_size for x in info)>MAX_PACKAGE or any(x.flag_bits&1 for x in info):
                raise ValueError('Expanded or encrypted package is unsupported.')
            manifest=json.loads(z.read('character.json'))
            if not isinstance(manifest,dict) or manifest.get('format')!='MH-character' or type(manifest.get('version')) is not int or manifest['version']!=1:
                raise ValueError('Unsupported package format or version.')
            p=custom.validate(manifest['profile'])
            p.pop('profile_id',None)
            # External claims never establish acceptance or a learned signature.
            p.pop('trait_amplifications',None)
            p.pop('starting_signature',None)
            p.pop('specialisation',None)
            p['import_provenance']=dict(format='MH-character v1',digest=hashlib.sha256(path.read_bytes()).hexdigest())
            picture=z.read('portrait.png')
            with Image.open(io.BytesIO(picture)) as image:
                if image.format!='PNG' or image.width>4096 or image.height>4096 or image.mode!='RGBA':
                    raise ValueError('Use a transparent RGBA PNG no larger than 4096 × 4096.')
                image.verify()
            with Image.open(io.BytesIO(picture)) as image:
                low,high=image.getchannel('A').getextrema()
                if low!=0 or high==0: raise ValueError('Portrait must have both a transparent background and visible character pixels.')
            return dict(profile=p,portrait=picture,source_format='MH-character v1',
                        warning='Imported Traits require fresh evaluation and acceptance. Review identity, text and starting choices.')
    except (zipfile.BadZipFile,KeyError,TypeError,json.JSONDecodeError,OSError,NotImplementedError,RuntimeError,Image.DecompressionBombError) as exc:
        raise ValueError('Unreadable character package: '+str(exc)) from exc


def draft_snapshot(package, base):
    """Explicit import acceptance stores a safe new asset and independent draft."""
    p=package['profile']; result=copy.deepcopy(base)
    root=custom.ROOT/'assets'/'generated'; root.mkdir(parents=True,exist_ok=True)
    path=root/('import-'+uuid.uuid4().hex+'.png')
    with path.open('xb') as output: output.write(package['portrait'])
    result['values'].update({k:', '.join(p[k]) if isinstance(p[k],list) else str(p[k]) for k in result['values'] if k in p})
    result.update(appearance=p['appearance'],awakened=p['awakened'],trait_enabled=p.get('trait_enabled',True),awakening_description=p.get('awakening_description',''),
                  mana_potential=p.get('mana_potential',True),
                  extra={k:p.get(k,'') for k in result.get('extra',{})},origin=p.get('origin',{}),identity=p.get('identity',{}),
                  portrait=path.relative_to(custom.ROOT).as_posix(),
                  generated_signature=[str(p[k]) for k in ('gender','age','height','hairstyle')]+[p['appearance']],
                  trait_amplifications=[],trait_signature=None,trait_reviewed=False,writing={},
                  specialisation='',starting_signature=None,
                  import_provenance=p.get('import_provenance'),
                  edit_profile_id=None,edit_profile_baseline=None)
    import vacant_homes
    result['home_choice']=vacant_homes.HOMES[p['home']]['name']
    return result
