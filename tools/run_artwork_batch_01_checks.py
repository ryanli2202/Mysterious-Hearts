"""Record actual offline unit/smoke outcomes for the MH-013 pilot."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'roadmap/artwork-batch-01/checks'
UNITS = ('portrait_framing', 'combat_portraits', 'guard_portraits', 'character_selection',
         'campaign_flashbacks', 'flashback_visits', 'syndicate_cast', 'hangout_scene', 'camera')
SMOKES = ('artwork_batch_01_ui', 'character_selection_ui', 'start_ui', 'town_portraits',
          'combat_portraits_ui', 'guard_portraits_ui', 'syndicate_uniform',
          'syndicate_guard_encounters', 'campaign_flashbacks_ui', 'flashback_visits_ui',
          'camera', 'phone_dark_theme', 'patch_notes_ui')


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser()
    parser.add_argument('kind', choices=('units','smokes','patch_notes'))
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    checks = ([(f'test_{name}', ['-m','unittest','discover','-s','tests','-p',f'test_{name}.py','-v']) for name in UNITS]
              if args.kind == 'units' else
              [(f'{name}_smoke', [f'tests/{name}_smoke.py']) for name in SMOKES]
              if args.kind == 'smokes' else
              [('patch_notes_validate',['patch_notes.py','validate']),
               ('test_patch_notes',['-m','unittest','discover','-s','tests','-p','test_patch_notes.py','-v']),
               ('patch_notes_export',['patch_notes.py','export'])])
    results = []
    for name, command in checks:
        run = subprocess.run([sys.executable,*command],cwd=ROOT,capture_output=True,text=True,
                             encoding='utf-8',errors='replace',
                             env={**os.environ,'PYTHONIOENCODING':'utf-8'})
        (OUT/f'{name}.txt').write_text(run.stdout+run.stderr,encoding='utf-8')
        results.append(dict(check=name,command='python '+' '.join(command),returncode=run.returncode,log=f'checks/{name}.txt'))
        print(f'{name}: {"PASS" if run.returncode == 0 else "FAIL"}',flush=True)
        if run.returncode:
            print((run.stdout+run.stderr)[-2200:],flush=True)
        (OUT/f'{args.kind}.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    return int(any(row['returncode'] for row in results))


if __name__ == '__main__':
    sys.exit(main())
