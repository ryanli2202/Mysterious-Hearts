# Community-plugin setup verification

Recorded 2026-11-11 (Australia/Brisbane).

| Check | Observed result |
| --- | --- |
| Native Codex installation listing inside the project | All five requested plugins installed and enabled at the versions in the lock file |
| Native Codex installation listing from the user home directory | All five installed, disabled outside the project |
| Project and user TOML | Parsed successfully; unrelated user settings preserved when applying project-only enablement |
| Installed manifests | All five SHA-256 hashes match the recorded source manifests |
| Installed skill trees | All 157 skill/support files byte-identical to their source packages; 24 Story Skills plus one entry skill for each other plugin |
| falsegreen supporting files | Root SKILL.md, reference.md, and fragments/precision-rules.md present; original project rules preserved |
| Context Guard release download | SHA-256 matched GitHub's published asset digest: e4640cc14880e88817efef6db9f7d006f64b6281229715f5972d492c84b81230 |
| Context Guard artifact_identity.py --compare-to | Exact release-file parity passed |
| Context Guard self-test, direct and project wrapper | Passed on Python 3.12.10; nine hook events recognised |
| SFXMint live MCP initialize and tools/list | Successful; server reported version 1.12.1 and four tools: search_sounds, get_role_sound, get_sound, get_sound_set |
| Story Skills reindex | Registries up to date |
| Story Skills wordcount --write | Zero manuscript words; no chapters imported |
| Story Skills check | Passed with zero errors and zero warnings after correcting required scaffold metadata; checks cover the starter only |
| Setup documentation links | Local source-map and setup-guide targets resolved |
| python patch_notes.py validate | Passed with 498 existing catalogue entries |
| python patch_notes.py export | Generated patch_notes/PATCH_NOTES.md successfully |

## Hook activation and workflow follow-up

On 2026-11-11 the user explicitly requested Context Guard activation, completion
of hook setup, and automatic use of all five plugins. Reviewed the installed
Windows hook definitions and reconfirmed exact release-file parity. Obtained
each hook's current definition/content hash from the installed Codex host's
`hooks/list` API, persisted those exact approvals through `config/batchWrite`,
and read them back. No bypass flag, guessed hash, private-ledger edit, or plugin
source modification was used. A project-config API write was refused as read-only;
the supported user-config write succeeded, retaining project-only enablement.

| Follow-up check | Observed result |
| --- | --- |
| Native host hooks/list | All nine Context Guard hooks enabled and trusted; no warnings/errors |
| Native host skills/list with forceReload | 28 enabled skills: 24 Story Skills and one each for the other four plugins |
| Exact Windows UserPromptSubmit command, isolated synthetic request | Automatic full activation without a plugin name or control command |
| Exact Windows PreCompact command, isolated synthetic session | Passed and wrote recovery state |
| Exact Windows SessionStart resume command, same synthetic session | Recovered the dark-phone and save-preservation requirements |
| Automatic workflow routing | AGENTS.md maps ordinary task categories to the appropriate plugins and preserves existing authorisation |

The behavioural check used synthetic inputs through the actual installed
Windows hook commands and an isolated temporary data root. It did not simulate
human authorisation in a real task or modify a real session's private state.
It is not a complete live-model compaction test. A fresh ephemeral host startup
had no SessionStart run because the package matches only resume/compact for
that event; the startup result was not counted as hook execution evidence.

Already-open chats may retain their prior hook set until refresh/restart.
The persisted trust and fresh host discovery are verified; loading inside every
pre-existing desktop chat is not claimed. SFXMint's HTTP MCP handshake was
checked independently during installation.

## All-plugin automatic workflow follow-up

On 2026-11-11 the user asked to integrate all installed project plugins into
future work without manual typing. AGENTS.md now gives standing task-based
routing for all ten packages, assigns tool selection and command execution to
Codex, and defines combined writing/media workflows. Simple synthetic sounds
prefer Pro Motion; SFXMint library downloads must be explicitly free, with local
fallbacks when access is limited. Free-only/no-external-sign-in restrictions and
the restricted prompt-to-asset server remain in force.

| Follow-up check | Observed result |
| --- | --- |
| Parsed project and user configuration | All ten project plugins enabled; all ten user defaults disabled |
| Fresh native `skills/list` | 49 enabled skills across all ten packages; no discovery errors |
| Skill counts | Story Skills 24; Context Guard 1; falsegreen 1; Writer's Loop 1; SFXMint 1; Bulk BG Remove 1; Pro Motion 1; DESIGN:OS 5; launch-film 1; prompt-to-asset 13 |
| Native `hooks/list` readback | All nine existing Context Guard hooks enabled and trusted; trust was not changed |
| Media runtime doctor | All configured runtime, helper and built-server paths present |
| Routing review | All ten installed packages mapped to ordinary requests; commands are Codex's responsibility; no user activation step required |
| Patch-note checks | Catalogue valid with 498 entries; Markdown export refreshed; no player-visible release entry added |

The compact native readback is saved in `.test-tmp/plugin_workflow_readback.json`.
This verifies persisted configuration and fresh host discovery. It does not
claim a live hook fired in this chat or guarantee that every existing chat has
refreshed its tool list. Codex should resolve installed skills from the lock file
and use the configured local launchers when discovery is stale. The media
verification and DESIGN:OS limitations recorded in `FREE_MEDIA_PLUGINS.md` remain
unchanged; rendering tests were not repeated for this instruction-only update.

## Scope of checks

This setup did not import or revise the campaign manuscripts, audit the game's
regression suite, download sounds, configure paid services, or run gameplay/UI
smokes. Runtime files, saves, existing assets, approved campaign order, and
existing catalogue records were not edited. No player-visible release entry or
new roadmap implementation slot was created for development-tool installation.
