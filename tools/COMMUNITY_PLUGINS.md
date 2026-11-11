# Community plugins for Mysterious Hearts

Installed 2026-11-11 using the native Codex plugin CLI. These are development
tools, not a gameplay release. No runtime code, player saves, existing campaign
prose, artwork, or audio was changed by setup.

## Installed packages

| Plugin | Version | Project use |
| --- | --- | --- |
| [Story Skills](https://github.com/danjdewhurst/story-skills) | 0.24.1 | 24 fiction and continuity skills plus the bundled Node CLI |
| [Context Guard](https://github.com/GreenLv/codex-context-guard) | 0.17.2 | Nine trusted lifecycle hooks; automatic protection for complex work and recovery after compaction/resume |
| [falsegreen-skill](https://github.com/vinicq/falsegreen-skill) | 0.8.2 | Focused Python regression-test review using the existing Codex session |
| [Writer's Loop](https://github.com/xxsang/writers-loop) | 0.1.0 | Requested prose critique/revision; preference storage remains off |
| [SFXMint](https://github.com/sfxmint/sfxmint-mcp) | 1.0.9 | Hosted, unauthenticated sound-library MCP and sound-selection skill |

Exact upstream commits, the Context Guard release digest, source directories,
installed cache paths, and manifest hashes are recorded in
[community_plugins.lock.json](community_plugins.lock.json).

The local marketplace is `mysterious-hearts-tools`, stored under
`C:/Users/ryanl/.codex/community-sources/mysterious-hearts/`. Complete plugin
packages were installed into Codex's cache, retaining supporting references and
scripts. This avoids falsegreen's documented root-marketplace layout issue and
keeps the original project AGENTS.md intact.

The packages are enabled by [the project config](../.codex/config.toml). Their user
defaults are disabled, so other projects do not automatically inherit them.
The project must remain trusted for its Codex configuration to load. Installed
versions are pinned snapshots; there is no automatic upstream update job.

Five additional free media plugins (Bulk BG Remove, Pro Motion, DESIGN:OS SVG
Animation, launch-film and prompt-to-asset) are installed with the same project
scope. Their restrictions, commands and actual verification results are in
[FREE_MEDIA_PLUGINS.md](FREE_MEDIA_PLUGINS.md). Prompt-to-asset is deliberately
restricted to local tools; do not use its upstream paid/API workflows.

## Automatic workflow

The user authorised activation and automatic workflow integration on 2026-11-11.
[AGENTS.md](../AGENTS.md) now instructs Codex to select the relevant installed
skills from ordinary requests. This now covers all ten project plugins in the
lock file, including the five media plugins. Plugin names, slash commands,
terminal commands and repeated activation prompts are not required from the
user. Codex selects the tools, runs their prepared launchers, combines the
necessary stages and verifies the result. Read only the skills relevant to the
task. The complete standing routing policy is in [AGENTS.md](../AGENTS.md).

Task-level roadmap allocations and the capability assessment are maintained in
[roadmap/PLUGIN_ASSIGNMENTS.md](../roadmap/PLUGIN_ASSIGNMENTS.md) and each linked
plan's Plugin task assignments section. The user requested on 2026-11-11 that
future update plans receive these assignments automatically. Use
[the update template](../roadmap/UPDATE_TEMPLATE.md) for concrete tasks, outputs,
checks and conditional/dependency gates; update child plans as scope changes.
Assignments do not resume paused work, reopen releases or establish that a plugin
performed historical work. Sound/trailer routes remain conditional when outside
the update's scope, and the restricted media setup is not a raster painting
generator.

| Ordinary request | Automatic workflow |
| --- | --- |
| Plan a campaign, check lore, develop a character or flashback | Story Skills; read the source map and protect branch/era knowledge |
| Draft, critique, or revise substantial prose | Writer's Loop; combine with Story Skills for campaign canon and continuity |
| Add/change regression tests or fix a bug with tests | falsegreen-skill review plus the actual relevant tests |
| Add a UI click, alert or synthetic effect | Pro Motion's local WAV synthesis and in-game playback checks |
| Find a library sound or realistic effect | SFXMint's explicitly free downloads; local synthesis/existing assets if a paid format, account or allowance blocks access |
| Remove backgrounds or prepare transparent cutouts | Bulk BG Remove, with its memory planner and output review |
| Create icons, SVG assets, sprite sheets or nine-slice assets | prompt-to-asset's restricted local authoring/validation/export tools |
| Animate SVG or line art | DESIGN:OS SVG Animation and a suitable local export path |
| Create bespoke motion graphics or process local audio | Pro Motion |
| Make a trailer from game assets, a brand kit or a public website | launch-film; combine writing, animation and sound workflows when needed |
| Complex or resumed multi-step work | Context Guard lifecycle protection and recovery |

The free-only/no-external-sign-in rule applies to every selected media step and
fallback. Existing scope and approvals carry across the workflow. Tool setup or
selection alone does not authorise an unrelated asset change, paid service,
publication or new account connection. Commands below are reference material for
Codex to execute; they are not required user activation steps.

Context Guard's exact installed release and hook definitions were reviewed, then
trusted through Codex's native configuration API at the user's explicit request.
Native readback reports all nine hooks enabled and trusted. Trust is stored in the
user config because that API permits writes there; plugin enablement remains
project-specific. No trust-bypass flag or plugin-source modification was used.
Future changed package contents require a new review under
[Codex's hook trust rules](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).

The plugin automatically enables standard full protection when its built-in
complexity/acceptance/requirement thresholds are met, and on first compaction
unless explicitly turned off. Simple requests can use lightweight prompt
journaling. No strict/release contract or publication authority was adopted.
An isolated Windows hook replay confirmed automatic activation on an ordinary
complex request and requirement recovery after simulated compaction/resume.
This verifies the handlers, not a full live-model compaction session.

The initial five-plugin installation exposed 28 skills; the five media plugins
added 21. Fresh discovery for the complete set is recorded in
[COMMUNITY_PLUGINS_VERIFICATION.md](COMMUNITY_PLUGINS_VERIFICATION.md). Already-open
chats may retain their previously loaded hook set until their next refresh or
restart; if that happens, report the loading limitation rather than asking the
user to type plugin activation commands. Read installed skills from the lock-file
paths when skill discovery is stale.

## Project workflows

### Story Skills and Writer's Loop

Read [writing/SOURCE_MAP.md](../writing/SOURCE_MAP.md) first. The structured starter
is [writing/story-skills/story.md](../writing/story-skills/story.md), with a style
sheet and empty character, scene, chapter, and continuity registries. It is ready
for scoped editorial work, but existing game content has not been imported.
Starter validation is not a continuity review of the game.

Example requests (plugin names are optional):

- "Continuity-check Garrett's reunion against the source map."
- "Critique this Rei scene while preserving all outcomes."
- "Model this campaign's branches."

Writer's Loop uses the existing Codex session; no API key or external paid model
was configured. Its standard writing workflow includes plan and revision
checkpoints. Respect approvals already provided in the conversation and the user's
requested scope. Do not collect a persistent preference journal or style pack
unless the user explicitly enables it. No `.writers-loop` storage was created.

Run the bundled CLI from the game root in PowerShell:

```powershell
& .\tools\story.ps1 reindex .\writing\story-skills
& .\tools\story.ps1 wordcount .\writing\story-skills --write
& .\tools\story.ps1 check .\writing\story-skills
```

The wrapper resolves the version recorded in the lock file. It does not add
dependencies to the game or generate runtime prose. Characters and scenes must
be represented explicitly before the checker can assess their continuity.

### falsegreen-skill

Use the installed skill for test quality analysis; no standalone API-backed CLI
or extra model account is necessary. For example:

"Review tests/test_campaign_flashbacks.py for assertions
that would still pass if historical knowledge leaked into the present."

High-value targets include `tests/test_save_system.py`,
`tests/test_campaign_prose.py`, `tests/test_campaign_dialogue.py`,
`tests/test_flashback_visits.py`, and `tests/phone_dark_theme_smoke.py`.
Load the Python and semantic definitions as the skill directs. Test analysis
must cite the faulty assertion and a plausible broken behaviour; it is not a
replacement for running feature tests or inspecting dark-phone interactive states.
No full regression-test audit was performed as part of installation.

### Context Guard diagnostics

```powershell
& .\tools\context-guard.ps1 self-test
& .\tools\context-guard.ps1 status
& .\tools\context-guard.ps1 diagnose
```

The Windows launcher has a verified Python 3.12 interpreter binding in the user's
Codex configuration directory. Private task state stays outside version control.
Use the installed version's supported retention controls if changing retention;
do not manually edit its private ledger or claim its hooks ran from a self-test.

### SFXMint

The plugin declares `https://sfxmint.com/mcp?ref=codex-plugin`; no API key was
added. The setup connection returned `search_sounds`, `get_role_sound`,
`get_sound`, and `get_sound_set`. Server access has daily free allowances.
The live server currently identifies free downloads as MP3 and WAV downloads
as requiring a paid pack. Do not infer free WAV entitlement from a returned URL.

For later requested sound work, use `sound.py` and `assets/sounds/`, preserve
nonblocking playback and mute/volume settings, and keep accepted assets local
for offline play. Add a `SOUNDS.md` record with each asset's stable page URL,
license, AI/synthesis provenance, original SHA-256, processing recipe if any,
and listening/format/playback checks actually performed. No sound downloads,
paid actions, or audio replacements were performed during setup.

## Maintenance and rollback

- Check installation with `codex plugin list --marketplace mysterious-hearts-tools --json` from this project.
- Disable a package for this project by setting its `enabled` entry to `false`
  in `.codex/config.toml`. This preserves source packages and task state.
- Updates should be explicit: inspect the new upstream release, update the local
  source, reinstall the selected package using `codex plugin add`, update the
  version lock, rerun checks, and review any changed hooks. Finish active guarded
  tasks before upgrading Context Guard.
- A plugin reinstall can change its user-level enabled flag; keep the installed
  user-level defaults disabled when retaining project-only use.
- Restore on another machine by cloning the recorded revisions and obtaining
  Context Guard's recorded release, registering the same local marketplace, and
  installing the required entries. Regenerate machine-specific paths in the lock;
  the lock is an installation record, not a portable installer.
- The pre-install user config backup is under the marketplace's
  `backups/config.before-install.toml`. Do not overwrite a later config wholesale
  with that backup; it may contain unrelated newer settings.

## Verification evidence

See [COMMUNITY_PLUGINS_VERIFICATION.md](COMMUNITY_PLUGINS_VERIFICATION.md) for
installation, trust, discovery, and automatic-activation checks.
