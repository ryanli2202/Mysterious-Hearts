"""Apply recorded project adaptations to pinned community plugin sources.

Run only after reviewing the upstream versions. This does not fetch or execute
upstream installers, authenticate, or install global dependencies.
"""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = Path.home() / '.codex/community-sources/mysterious-hearts'


def replace(path, old, new):
    data = path.read_text(encoding='utf-8')
    if new in data:
        return
    if old not in data:
        raise RuntimeError(f'Upstream changed; review required: {path}')
    path.write_text(data.replace(old, new, 1), encoding='utf-8', newline='\n')


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    packages = {
        'bulk-bg-remove': BASE / 'bulk-bg-remove',
        'pro-motion': BASE / 'pro-motion/plugins/pro-motion',
        'design-os-svg-animation': BASE / 'design-os-svg-animation',
        'launch-film': BASE / 'launch-film',
        'prompt-to-asset': BASE / 'prompt-to-asset/plugins/prompt-to-asset',
    }
    backup = BASE / 'backups/media-2026-11-11'
    backup.mkdir(parents=True, exist_ok=True)
    marketplace = BASE / '.agents/plugins/marketplace.json'
    for path in (marketplace, Path.home() / '.codex/config.toml', ROOT / '.codex/config.toml',
                 ROOT / 'tools/community_plugins.lock.json'):
        target = backup / (('project-' if path.is_relative_to(ROOT) else '') + path.name)
        if not target.exists():
            shutil.copy2(path, target)

    pro = packages['pro-motion'] / 'skills/pro-motion/scripts/render-fast.js'
    replace(pro, "ffmpeg = require('ffmpeg-static');", "ffmpeg = process.env.MH_FFMPEG || require('ffmpeg-static');")
    replace(pro, "}).listen(0);", "}).listen(0, '127.0.0.1');")
    # Wait for the asynchronous loopback bind before accessing server.address().
    replace(pro, "  const url = `http://127.0.0.1:", "  if (!srv.listening) await new Promise(resolve => srv.once('listening', resolve));\n  const url = `http://127.0.0.1:")

    exporter = packages['design-os-svg-animation'] / 'scripts/export-60fps-video.mjs'
    replace(exporter, "const CHROME_BIN = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';",
            "const CHROME_BIN = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';")
    replace(exporter, "const FFMPEG_BIN = '/opt/homebrew/bin/ffmpeg';",
            "const FFMPEG_BIN = process.env.MH_FFMPEG || 'ffmpeg';")

    chrome = packages['launch-film'] / 'src/chrome.js'
    replace(chrome, '''      child.kill("SIGKILL");
      setTimeout(() => fs.rmSync(profile, { recursive: true, force: true }), 300).unref();''', '''      // Windows can retain profile locks briefly after Chrome exits.
      const cleanup = () => {
        const target = path.resolve(profile);
        if (!target.startsWith(path.resolve(os.tmpdir()) + path.sep) ||
            !path.basename(target).startsWith("launch-film-chrome-")) return;
        fs.rm(target, { recursive: true, force: true, maxRetries: 20, retryDelay: 100 }, err => {
          if (err) process.stderr.write(`Temporary Chrome profile cleanup: ${err.code}\\n`);
        });
      };
      if (child.exitCode === null) { child.once("close", cleanup); child.kill("SIGKILL"); }
      else cleanup();''')

    p2a = BASE / 'prompt-to-asset/packages/mcp-server'
    replace(p2a / 'src/config.ts', 'hydrateEnv();',
            '// Project policy: never load stored provider credentials.\nif (process.env["MH_MEDIA_FREE_ONLY"] !== "1") hydrateEnv();')
    server = p2a / 'src/server.ts'
    allowed = ['asset_capabilities', 'asset_generate_logo', 'asset_generate_app_icon',
               'asset_generate_favicon', 'asset_save_inline_svg', 'asset_validate',
               'asset_brand_bundle_parse', 'asset_export_bundle', 'asset_sprite_sheet', 'asset_nine_slice']
    filter_code = ('const MH_FREE_TOOLS = new Set(' + json.dumps(allowed) + ');\n'
        '  server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS.filter(t => MH_FREE_TOOLS.has(t.name)).map(t => ({...t, description: "LOCAL FREE-ONLY: no API generation or external sign-in. " + t.description})) }));')
    if 'const MH_FREE_TOOLS' not in server.read_text(encoding='utf-8'):
        replace(server, 'server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));', filter_code)
    old_listing = 'TOOLS.filter(t => MH_FREE_TOOLS.has(t.name)).map(t => ({...t, description: "LOCAL FREE-ONLY: no API generation or external sign-in. " + t.description}))'
    local_listing = '''TOOLS.filter(t => MH_FREE_TOOLS.has(t.name)).map(t => {
      const tool = structuredClone(t);
      if (tool.inputSchema.properties?.mode) tool.inputSchema.properties.mode = {
        type: "string", enum: ["inline_svg"], description: "Local SVG authoring only."
      };
      tool.description = t.name.startsWith("asset_generate_")
        ? "Create a local SVG authoring brief. Use asset_save_inline_svg to write the authored SVG and exports. No hosted generation."
        : "LOCAL FREE-ONLY: no API generation or external sign-in. " + t.description;
      tool.annotations = {...tool.annotations, openWorldHint: false};
      return tool;
    })'''
    replace(server, old_listing, local_listing)
    gate = '''      // Mysterious Hearts: reject paid, account-backed and unlisted routes before dispatch.
      if (!MH_FREE_TOOLS.has(name)) throw new Error("Disabled by project free-only policy: " + name);
      const mhArgs = (args ?? {}) as Record<string, unknown>;
      if (mhArgs["mode"] !== undefined && mhArgs["mode"] !== "inline_svg")
        throw new Error("Only inline_svg mode is enabled; no external generation or sign-in.");
      if (name.startsWith("asset_generate_")) mhArgs["mode"] = "inline_svg";
      if (name === "asset_capabilities") return {content: [{type: "text", text: JSON.stringify({
        policy: "free-only, local-only, no external sign-in", tools: [...MH_FREE_TOOLS], modes: ["inline_svg"]
      })}]};
      let result: unknown;'''
    replace(server, '      let result: unknown;', gate)

    # Upstream Codex manifest's entry is not a complete skill/MCP declaration.
    save(packages['prompt-to-asset'] / '.codex-plugin/plugin.json', {
        'name': 'prompt-to-asset', 'version': '0.1.0',
        'description': 'Project-pinned prompt-to-asset; local SVG, validation and export only.',
        'skills': './skills/', 'mcpServers': './.codex.mcp.json', 'license': 'MIT',
        'repository': 'https://github.com/MohamedAbdallah-14/prompt-to-asset',
        'interface': {'displayName': 'prompt-to-asset (free local features)',
                      'shortDescription': 'Local SVG and game asset exports; no sign-in or paid APIs.'}})
    save(packages['prompt-to-asset'] / '.codex.mcp.json', {'mcpServers': {'prompt-to-asset-free': {
        'command': str(BASE / 'media-runtime/python/Scripts/python.exe'),
        'args': [str(ROOT / 'tools/media_tools.py'), 'p2a'], 'cwd': str(ROOT),
        'startup_timeout_sec': 30, 'tool_timeout_sec': 120}}})

    policy = '''
## Mysterious Hearts installation policy

This reviewed project installation permits only fully free features needing no
external sign-in. Use `python tools/media_tools.py` from the game root and read
`tools/FREE_MEDIA_PLUGINS.md` for the installed commands and limits.
Never start provider login, API-key setup, purchases, paid credits, trials,
Suno/Udio/ElevenLabs generation, hosted rendering, publication or deployment.
Do not load existing provider credentials, run an unpinned npx installer, or
replace the restricted prompt-to-asset server with its unrestricted CLI.
Use existing local art/audio, local synthesis, SVG and local render/export.
For prompt-to-asset, only its advertised local tools and inline_svg mode are
enabled; API/external_prompt_only, model training, network and sign-in are disabled.
Production artwork, audio replacement and gameplay changes require a task that
requests them. Install verification belongs under `.test-tmp/media/`.
Preserve dark phone styles and in-person activity routing. Do not publish.
The user has authorised this installation and its free dependencies already.
Use the prepared isolated runtime instead of global installs or setup.sh.

'''
    for package in packages.values():
        for skill in (package / 'skills').glob('*/SKILL.md'):
            data = skill.read_text(encoding='utf-8')
            if '## Mysterious Hearts installation policy' not in data:
                start = data.find('\n---', 3)
                if not data.startswith('---') or start < 0:
                    raise RuntimeError(f'Unrecognized skill frontmatter: {skill}')
                point = start + 4
                data = data[:point] + policy + data[point:]
            skill.write_text(data, encoding='utf-8', newline='\n')

    data = json.loads(marketplace.read_text(encoding='utf-8'))
    for name, package in packages.items():
        if not any(p['name'] == name for p in data['plugins']):
            data['plugins'].append({'name': name, 'source': {'source': 'local', 'path': './' + package.relative_to(BASE).as_posix()},
                'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Media'})
    save(marketplace, data)
    runtime = BASE / 'media-runtime'
    ffmpeg = next((runtime / 'ffmpeg').glob('*/bin/ffmpeg.exe'))
    save(ROOT / 'tools/media_plugins.runtime.json', {
        'python': str(runtime / 'python/Scripts/python.exe'), 'node': shutil.which('node'),
        'chrome': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
        'ffmpeg': str(ffmpeg), 'ffprobe': str(ffmpeg.with_name('ffprobe.exe')),
        'node_modules': str(runtime / 'node/node_modules'), 'models': str(runtime / 'models'),
        'prompt_runtime': str(p2a), 'packages': {k: str(v) for k, v in packages.items()}})
    save(runtime / 'node/package.json', {'name': 'mysterious-hearts-free-media-runtime', 'private': True,
        'dependencies': {'puppeteer': '24.10.2', 'easybrandkit': '0.4.0'}})
    print('Prepared five pinned local plugin packages, offline MCP restriction, and Windows launchers.')


if __name__ == '__main__':
    main()
