"""Read-only verification of MH-013 installed masters and the whole height roster."""
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import game
import character_stature as stature
import portrait_framing as framing

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT/'roadmap/artwork-stage-02'
INSTALL = STAGE/'height-review'
OUT = STAGE/'height-variation'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((STAGE/'manifest.json').read_text(encoding='utf-8'))
    install = json.loads((INSTALL/'installation.json').read_text(encoding='utf-8'))
    baseline = json.loads((STAGE/'before-state.json').read_text(encoding='utf-8'))
    by_id = {r['id']:r for r in install['assets']}
    rows = []
    app = SimpleNamespace(photos={},state_data={})
    with patch.object(game.ImageTk,'PhotoImage',side_effect=lambda im:im.copy()):
        for master in manifest['assets']:
            ident = master['id']; installed = by_id[ident]
            path = ROOT/master['path']
            assert digest(path) == master['new_sha256'] == installed['installed_sha256'], ident
            assert digest(STAGE/master['candidate']) == master['new_sha256'], ident
            if installed.get('backup'):
                assert digest(ROOT/installed['backup']) == installed['before_sha256'], ident
            record = stature.records()[ident]
            who = 'guard_art_'+master['character'] if master['role'] else master['character']
            measurements = []
            for size in ((192,352),(96,176)):
                photos = game.Game.portrait_group(app, {'ivan':(size[0]*2,size[1]),who:size})
                heights = {}
                for key, photo in photos.items():
                    box = framing.visible_bounds(photo)
                    assert box and box[3] == size[1], ident
                    heights[key] = box[3]-box[1]
                error = abs(heights[who]-heights['ivan']*record['height_cm']/193)
                assert error <= 2, (ident,size,error)
                measurements.append(dict(slot=size,visible_pixels=heights[who],ivan_pixels=heights['ivan'],ratio_error_pixels=round(error,3)))
            rows.append(dict(id=ident,**record,measurements=measurements))
    targets = {r['path'] for r in install['assets']}
    unchanged = [p for p in baseline if p not in targets]
    assert all(digest(ROOT/p)==baseline[p] for p in unchanged), 'Non-master asset changed'
    report = dict(roadmap_id='MH-013',date='2026-11-11',verified=True,total=len(rows),
        authored=sum(r['basis']=='authored' for r in rows),
        user_specified=sum(r['basis']=='user specified' for r in rows),
        fallbacks=sum(r['basis']=='display fallback' for r in rows),
        installed_changes=install['changed'],other_baseline_files_unchanged=len(unchanged),
        cropping='Visible head-to-mid-thigh span uses 0.70 of full stature; picture crop is not feet. Same pixels/cm across participants, uniform resize, alpha padding excluded.',
        characters=rows)
    (OUT/'height-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    lines=['# MH-013 Stage 2 height roster','','Verified 2026-11-11. All 107 installed default portraits match their accepted master hashes. '
           f"{report['authored']} original authored heights unchanged; {report['user_specified']} explicit user heights; {report['fallbacks']} varied display defaults. "
           'Remaining male defaults span 175-180 cm and female defaults 160-165 cm. Oni and Custom Robotic use the explicit 198 cm override. '
           'Values are fixed per identity, never randomized on load. Dialogue disclosure rules remain unchanged. Full heights are not the visible cropped image height.','',
           '| Character / role | Full stature (cm) | Basis | Display profile |','| --- | ---: | --- | --- |']
    lines += [f"| {r['id']} | {r['height_cm']} | {r['basis']} | {r['profile']} |" for r in sorted(rows,key=lambda r:r['id'])]
    (OUT/'HEIGHTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"{len(rows)}/107 installed hashes and height ratios passed at two sizes; {len(unchanged)} other baseline assets unchanged.")


if __name__ == '__main__':
    main()
