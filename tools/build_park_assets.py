"""Export the code-native park planes as reusable PNG assets."""
import json
import sys
import os
import subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from park_scene import ROOT, layers

folder=ROOT/'assets/world/park'
folder.mkdir(parents=True,exist_ok=True)
if (folder/'source/props-atlas.png').exists():
    node=Path(os.environ['USERPROFILE'])/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
    subprocess.run([str(node),str(ROOT/'tools/build_park_polish.cjs')],cwd=ROOT,check=True)
    sys.exit(0)
manifest=[]
for name,parallax,image in layers():
    image.save(folder/f'{name}.png')
    manifest.append(dict(name=name,file=f'{name}.png',parallax=parallax,size=list(image.size)))
(folder/'layers.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(f'Exported {len(manifest)} park layers to {folder}')
