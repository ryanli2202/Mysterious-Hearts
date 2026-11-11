"""Project-scoped, free-only launchers for the installed media plugins."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def configuration():
    return json.loads((ROOT / 'tools/media_plugins.runtime.json').read_text(encoding='utf-8'))


def environment(config):
    # Never pass provider credentials or remote generation overrides to media tools.
    denied = ('API_KEY', 'API_TOKEN', 'ACCESS_TOKEN', 'SECRET', 'PASSWORD',
              'SUBSCRIPTION_KEY', 'BASE_URL', 'MODAL_COMFYUI', 'P2A_', 'PROMPT_TO_BUNDLE_')
    env = {k: v for k, v in os.environ.items()
           if not any(part in k.upper() for part in denied)
           and k.upper() not in {'FAL_KEY', 'HF_TOKEN', 'NIM_API_KEY', 'NODE_OPTIONS',
                                'CLOUDFLARE_ACCOUNT_ID', 'HUGGING_FACE_HUB_TOKEN'}}
    env.update({
        'PATH': str(Path(config['ffmpeg']).parent) + os.pathsep
                + str(Path(config['python']).parent) + os.pathsep + env.get('PATH', ''),
        'CHROME': config['chrome'], 'CHROME_PATH': config['chrome'],
        'LAUNCH_FILM_CHROME': config['chrome'], 'LAUNCH_FILM_FFMPEG': config['ffmpeg'],
        'LAUNCH_FILM_FFPROBE': config['ffprobe'],
        'LAUNCH_FILM_EASYBRANDKIT': str(Path(config['node_modules']) / 'easybrandkit/skills/easybrandkit/scripts/easybrandkit.js'),
        'MH_FFMPEG': config['ffmpeg'], 'MH_FFPROBE': config['ffprobe'],
        'MH_MEDIA_FREE_ONLY': '1', 'PUPPETEER_SKIP_DOWNLOAD': '1',
        'NODE_PATH': config['node_modules'],
        'U2NET_HOME': config['models'],
        'PROMPT_TO_BUNDLE_OUTPUT_DIR': str(ROOT / 'media-workspace/prompt-to-asset'),
        'PROMPT_TO_BUNDLE_CACHE_DIR': str(ROOT / '.test-tmp/media/asset-cache'),
        'PROMPT_TO_BUNDLE_TRANSPORT': 'stdio', 'P2A_MAX_SPEND_USD_PER_RUN': '0',
    })
    return env


def run(command, config, cwd=ROOT):
    return subprocess.call([str(p) for p in command], cwd=cwd, env=environment(config))


def main():
    config = configuration()
    if len(sys.argv) < 2:
        print('Commands: doctor, bulk-bg-remove, sfx, audio, launch-film, p2a, pro-init, pro-render, design')
        return 0
    name, *args = sys.argv[1:]
    packages = config['packages']
    pro = Path(packages['pro-motion']) / 'skills/pro-motion'
    if name == 'doctor':
        checks = {key: Path(config[key]).is_file() for key in ('python', 'node', 'chrome', 'ffmpeg', 'ffprobe')}
        checks.update({key: Path(value).is_dir() for key, value in packages.items()})
        checks.update({
            'background_remover_cli': (Path(config['python']).parent / 'bulk-bg-remove.exe').is_file(),
            'prompt_mcp_build': (Path(config['prompt_runtime']) / 'dist/index.js').is_file(),
            'puppeteer': (Path(config['node_modules']) / 'puppeteer/package.json').is_file(),
            'easybrandkit': Path(environment(config)['LAUNCH_FILM_EASYBRANDKIT']).is_file(),
        })
        print(json.dumps({'ready': all(checks.values()), 'checks': checks, 'policy': 'free-only; no external sign-in'}, indent=2))
        return 0 if all(checks.values()) else 1
    if name == 'bulk-bg-remove':
        return run([Path(config['python']).parent / 'bulk-bg-remove.exe', *args], config)
    if name in {'sfx', 'audio'}:
        if name == 'sfx' and (not args or args == ['--help']):
            print('sfx <bubble|punch|metal|rip|click|riser|impact|sparkle> <output.wav> [--note A4] [--dur 0.6]')
            return 0
        return run([config['python'], pro / 'scripts/audio_post.py', *(['sfx'] if name == 'sfx' else []), *args], config)
    if name == 'launch-film':
        return run([config['node'], Path(packages[name]) / 'bin/launch-film.js', *args], config)
    if name == 'p2a':
        if args:
            raise SystemExit('Only the restricted MCP server is exposed. Provider config/login/API CLI commands are disabled.')
        return run([config['node'], '--import', (ROOT / 'tools/prompt_to_asset_free_only.mjs').as_uri(),
                    Path(config['prompt_runtime']) / 'dist/index.js'], config)
    if name == 'pro-init':
        if len(args) != 1:
            raise SystemExit('Usage: pro-init <new project subdirectory>')
        destination = (ROOT / args[0]).resolve()
        if not destination.is_relative_to(ROOT) or destination.exists():
            raise SystemExit('Choose a new directory inside this project.')
        shutil.copytree(pro / 'assets/template', destination)
        shutil.copytree(pro / 'scripts', destination / 'tools')
        for folder in ('music', 'out', 'stills'):
            (destination / folder).mkdir(exist_ok=True)
        # The game root is ESM; the upstream renderer is CommonJS.
        (destination / 'package.json').write_text('{"private":true,"type":"commonjs"}\n', encoding='utf-8')
        print(destination)
        return 0
    if name == 'pro-render':
        if len(args) < 3:
            raise SystemExit('Usage: pro-render <project subdirectory> <page.html> <output.mp4> [renderer options]')
        destination = (ROOT / args[0]).resolve()
        if not destination.is_relative_to(ROOT):
            raise SystemExit('Render directory must be inside this project.')
        return run([config['node'], destination / 'tools/render-fast.js', *args[1:]], config, destination)
    if name == 'design':
        allowed = {'export-player-deliverable.mjs', 'export-60fps-video.mjs',
                   'dev-server.mjs', 'motion-ir-compiler-demo.ts', 'new-line-art-case.mjs'}
        if not args or args[0] not in allowed:
            raise SystemExit('Choose a local design script: ' + ', '.join(sorted(allowed)))
        package = Path(packages['design-os-svg-animation'])
        script = package / 'scripts' / args[0]
        prefix = [package / 'node_modules/tsx/dist/cli.mjs'] if script.suffix == '.ts' else []
        return run([config['node'], *prefix, script, *args[1:]], config)
    raise SystemExit(f'Unknown media command: {name}')


if __name__ == '__main__':
    raise SystemExit(main())
