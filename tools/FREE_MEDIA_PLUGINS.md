# Free media tools for Mysterious Hearts

Installed 2026-11-11. All five requested plugins are enabled in this project's
`.codex/config.toml` and disabled by default in the user configuration. No external
account, API key, paid credit, trial, or subscription was configured. Codex itself
continues to use the user's existing access.

| Plugin | Pinned plugin version | Enabled use |
| --- | --- | --- |
| [Bulk BG Remove](https://github.com/Btike/bulk-bg-remove) | 0.1.3 | Local CPU background removal; transparent PNG/WebP and image finishing |
| [Pro Motion](https://github.com/jack-reson8/pro-motion) | 1.3.0 | Local canvas motion graphics, MP4/stills, WAV synthesis and audio processing |
| [DESIGN:OS SVG Animation](https://github.com/jangtrinh/design-os-svg-animation) | 1.0.0 | Local SVG/line-art animation, Motion IR, HTML player compilation and local rendering |
| [launch-film](https://github.com/EminBudak/launch-film) | 0.2.1 | Local trailers from an existing brand kit or public website, with locally generated soundtrack/SFX |
| [prompt-to-asset](https://github.com/MohamedAbdallah-14/prompt-to-asset) | 0.1.0 | Restricted local MCP: SVG authoring briefs, file creation, validation, platform exports, sprite sheets and nine-slice assets |

Prompt-to-asset's plugin manifest is version 0.1.0; its built MCP package is 0.5.1.
Exact commits and installed paths are in `community_plugins.lock.json`.

## Project rules

- Use only fully free features requiring no external sign-in. Use the project
  launcher below; do not use unrestricted provider commands, account setup,
  paid generation, free trials, hosted rendering, Suno/Udio/ElevenLabs, publication
  or deployment. Upstream skills describe broader capabilities than this setup.
- Prompt-to-asset permits exactly `asset_capabilities`, `asset_generate_logo`,
  `asset_generate_app_icon`, `asset_generate_favicon`, `asset_save_inline_svg`,
  `asset_validate`, `asset_brand_bundle_parse`, `asset_export_bundle`,
  `asset_sprite_sheet`, and `asset_nine_slice`. Generation means a local SVG brief
  for Codex to author, followed by local export; it is not hosted image generation.
  Only `inline_svg` mode is advertised/accepted. API/external modes and unlisted
  tools fail before dispatch. Stored-provider credential hydration is disabled,
  inherited provider credentials are removed, and HTTP/fetch are blocked in this
  MCP process. This is an application restriction, not an OS security sandbox.
- Other plugins use local processing. Public website reads, dependency downloads
  and public model downloads need no account. Use local music or synthesised
  audio; do not interpret upstream music-service suggestions as permission.
- Bulk BG Remove caches each model after its first public download. Silueta is
  already cached and tested. The machine had about 4.5 GB free RAM during setup;
  the best large models did not fit. Run its dry-run planner before each batch,
  respect blockers and report fallback quality. Do not lower memory safeguards.
- DESIGN:OS uses **PolyForm Shield**, not MIT, at this pinned revision. Its normal
  use for game assets is free; preserve its licence and review it before any
  redistribution or competing animation-tool product. Other plugin source licences
  and third-party notices remain in their packages. Free access does not make
  every model, font, supplied reference image or generated asset public domain.
- These tools are for requested development work. Drafts go in `media-workspace/`;
  verification fixtures go in `.test-tmp/media/`. Accept production assets only
  within the requested scope and record provenance. Preserve the game's dark
  phone UI, in-person routing, existing audio controls and patch-note workflow.

## Automatic use

The user authorised automatic integration of all project plugins on 2026-11-11.
Future requests can simply say "remove this background", "make a subtle click",
"animate this icon", "make a trailer" or "export a sprite sheet". Codex selects
the relevant skills, runs the prepared commands and checks the outputs. The
standing routing table in `../AGENTS.md` also covers writing, tests and Context
Guard. No plugin names, slash commands, manual activation or terminal typing are
required from the user. Only relevant plugins run for a given task.

For sound, local Pro Motion synthesis is preferred for simple synthetic effects;
SFXMint is used for suitable explicitly free library assets. Its paid formats or
usage limits never trigger a purchase or sign-in. Prompt-to-asset remains local
and restricted even when another plugin's upstream instructions suggest a paid
generation route. Known DESIGN:OS limitations still apply.

## Commands for Codex

Codex runs these from the game root in PowerShell; they are reference commands,
not user activation steps. The launcher selects an isolated Python
3.12 environment, the installed Node and Chrome, and a private FFmpeg installation.
No game runtime dependency was added.

```powershell
python tools/media_tools.py doctor
python tools/media_tools.py bulk-bg-remove "path/to/images" --dry-run --sample-sheet --json
python tools/media_tools.py bulk-bg-remove "path/to/images" --json
python tools/media_tools.py sfx --help
python tools/media_tools.py sfx click "media-workspace/click.wav" --dur 0.2
python tools/media_tools.py pro-init "media-workspace/trailer"
python tools/media_tools.py pro-render "media-workspace/trailer" film.html out/film.mp4 --fps 30 --workers 1
python tools/media_tools.py launch-film doctor
python tools/media_tools.py launch-film --help
python tools/media_tools.py design export-player-deliverable.mjs --spec "media-workspace/animation.json" --out "media-workspace/animation.html"
python tools/media_tools.py design motion-ir-compiler-demo.ts
node tools/verify_free_media.mjs
```

Create output parent folders before synthesising audio. Pro Motion's page must
define `window.READY`, `window.render(t)`, `window.DUR`, and a canvas with `id="c"`.
The scaffold is a starting point, not an authored trailer. The wrapper's `audio`
command exposes the upstream local audio-processing help.

DESIGN's HTML exporter accepts a JSON specification with `canvasHTML`,
`engineScriptContent`, duration and scenes. Its clean export mode uses native
dimensions (1920×1080 for 16:9); render at those dimensions. The bundled
`export-60fps-video.mjs` targets upstream example promos, not arbitrary game
projects. Its Chrome/FFmpeg paths were adapted for Windows. Core HTML/SVG output
was verified; that long example-promo export was not run. Some tutorial helper
scripts still assume macOS; they are not verified Windows workflows.

launch-film has pinned `easybrandkit` 0.4.0 for public website extraction. Its
local brand-kit renderer was tested. No game website was scraped, and extraction
from arbitrary sites is not guaranteed. Browser sessions use temporary profiles.

Prompt-to-asset starts through its installed stdio MCP declaration and
`python tools/media_tools.py p2a`. CLI login/config/generation arguments are
rejected by the wrapper. The MCP package is built from its pinned local source.

## Verification and limits

Actual results on 2026-11-11:

| Check | Result |
| --- | --- |
| Native Codex installation and fresh `skills/list` | Five packages; 21 enabled skills; no discovery errors |
| Runtime doctor | All interpreter, browser, FFmpeg, built MCP and helper paths present |
| Bulk BG Remove | Real 512×512 scikit-image astronaut fixture processed with Silueta; no failures; output has opaque and transparent pixels |
| Pro Motion audio | Real 0.2-second stereo WAV at 48 kHz; 9,600 frames |
| Pro Motion video | Real 320×180 H.264 MP4; four frames at 10 fps, duration 0.4 seconds |
| DESIGN build | TypeScript build passed |
| DESIGN browser smoke | Compiled local HTML, sought to 0.5 seconds, checked rendered magenta pixels on dark slate; remote requests blocked; screenshot inspected |
| DESIGN wider upstream suite | **112 passed, 8 failed, 3 skipped**; six failures use Windows paths as ESM import URLs, one line-width assertion, one slash-separator assertion. Not a fully passing upstream suite |
| launch-film render integration | All three tests passed, including a five-second 1920×1080 film with audio and nonblank frames |
| prompt-to-asset build | TypeScript build passed |
| prompt-to-asset policy/export | MCP handshake and ten-tool allowlist passed; API/external/hidden calls refused; real SVG and 32px PNG export verified for dimensions, colour and transparency; HTTP/fetch guard passed |
| Project patch-note catalogue | Validation passed for 498 existing entries; Markdown export refreshed; no release entry added |

`verify_free_media.mjs` is an integration check against the actual installed
server, with no mocked MCP/provider responses. It passes a fake inherited key,
pairs rejection checks with a successful local export, and verifies file pixels.
`free_media_test_spec.json` records the independent contract. A falsegreen
J1–J6/structural/semantic review found no actionable false-green shape in this
check. This is not a review of the whole upstream test suite.

Install-test artifacts and logs are under `.test-tmp/media/`. No existing game
artwork, audio, saves, phone surfaces or gameplay were changed. Phone/gameplay
smokes are therefore not installation evidence. This development-tool setup is
not a player-visible release or a new roadmap feature.

## Maintenance

Sources and private dependencies are under
`C:/Users/ryanl/.codex/community-sources/mysterious-hearts/`; runtime paths are in
`media_plugins.runtime.json`. Source and dependency records are pinned snapshots,
not an automatic update service. `media-locks/` records the Python packages, three
Node dependency locks, and FFmpeg/model hashes. The runtime file is machine-specific.

`prepare_media_plugins.py` records local adaptations: Windows renderer paths,
Pro Motion loopback serving, launch-film profile cleanup after Chrome exits,
the prompt-to-asset manifest/MCP restriction, and a free-only skill preface.
It expects the reviewed source revisions and installed dependencies; it does not
fetch, authenticate or rebuild them. After changing prompt-to-asset source, rebuild
its MCP package and rerun the policy/export check. Regenerate DESIGN's tutorial
contract if its skill text changes. Keep installed cache copies in sync when
reinstalling and preserve disabled user defaults.

Configuration backups from before this installation are in the marketplace's
`backups/media-2026-11-11/`. Do not restore a whole old configuration over newer
unrelated settings. Disable a selected plugin in `.codex/config.toml` to stop its
project use. Existing chats may need a refresh or a new turn to load newly
installed skills/MCP tools; fresh host discovery was verified.
