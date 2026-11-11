# In-person activity requirements

- In-person activities must be performed in the in-person window, rather than
  in the phone window. Apply this rule to all future features and changes.

# Phone UI requirements

- The phone UI must remain dark throughout. Do not introduce white, off-white,
  pale neutral, or native Windows light surfaces in any phone feature.
- This applies to app pages, mini games, headers, cards, menus, dropdown popups,
  scrollbars, entries, dialogs, empty/loading/error states, and hover, focus,
  pressed, selected, readonly, and disabled control states.
- Reuse `winterfield_ui.py`, `phone_theme.py`, and the existing phone/arcade
  styles. Use dark slate backgrounds and coloured accents. Readable muted light
  text is allowed; photographs and other user/content images keep their colours.
- Use the embedded `phone_dialogs` wrappers for phone prompts. Avoid new native
  light dialogs or unstyled Tk/ttk widgets. Configure combobox popup listboxes as
  well as the closed control. Preserve themed styles when resizing or navigating.
- When changing phone surfaces, run `tests/phone_dark_theme_smoke.py` and the
  relevant feature smoke checks. Inspect rendered screens for new layouts and
  interactive states. This rule applies to all future phone features.

# Patch notes requirements

- Track requested future updates in `ROADMAP.md` using its status workflow and
  `roadmap/UPDATE_TEMPLATE.md`. Preserve stable roadmap IDs, link detailed plans,
  and keep statuses, milestones and actual verification evidence current when
  working on a tracked update. Planning entries are not released features.

- For every new or materially revised update plan, automatically assign relevant
  project plugins to specific milestones/tasks using
  `roadmap/PLUGIN_ASSIGNMENTS.md` and the template's Plugin task assignments
  section. Do this in each separately maintained child plan as well as its parent.
  Name the plugin/skill, concrete deliverable, required checks, dependency or pause
  gate, and whether use is required, conditional, future maintenance only, or not
  applicable. Explain conditional triggers and capability gaps; do not force all
  ten plugins into every task or add unrelated media work. Preserve assignments
  when regenerating planning documents. Keep assignment, actual execution,
  verification and release evidence separate; never retroactively claim plugin
  use for completed work. Update assignments as scope changes without altering
  approved order, stable IDs, paused work or existing authorisation.

- For future player-visible features, fixes, balance, artwork or compatibility changes,
  add a detailed entry to `patch_notes/catalog.json` following `patch_notes/AUTHORING.md`.
- Record actual behavior, access instructions, save impact, evidence and checks performed.
  Preserve stable IDs; do not invent historical dates, version numbers or passed tests.
- Run `patch_notes.py validate` and refresh `patch_notes/PATCH_NOTES.md` using
  `patch_notes.py export`. Original chat reports are evidence, not automatically releases.

# Project community plugins

- Automatically select and use all ten project plugins recorded in
  `tools/community_plugins.lock.json` according to the task. This is standing
  authorisation for future requests in this project: ordinary language is enough.
  Codex owns plugin selection, invocation, command execution and verification;
  do not ask the user to name plugins, type slash commands, run setup/activation
  commands, or repeat permission already supplied for the requested work.
  Read the applicable installed SKILL.md before using it. Resolve installed paths
  through `tools/community_plugins.lock.json` if discovery has not refreshed.
  Load only skills relevant to the current request, not every plugin on every turn.
- Use this routing table for ordinary requests and combine relevant workflows
  when the requested deliverable needs several stages:

| Task or required step | Automatic plugin selection |
| --- | --- |
| Campaign, lore, character, era, branch or continuity work | Story Skills |
| Substantial prose drafting, critique or revision | Writer's Loop, with Story Skills for game canon |
| Regression-test creation, modification or review | falsegreen-skill, plus actual relevant tests |
| Long, complex, resumed or compacted work | Context Guard's existing lifecycle hooks |
| Library sound search or realistic/recorded effects | SFXMint's verified free, no-sign-in assets only |
| Background removal, transparent cutouts or batch isolation | Bulk BG Remove |
| Bespoke motion graphics, local MP4/stills, synthetic effects or audio processing | Pro Motion |
| SVG, line-art or vector animation | DESIGN:OS SVG Animation |
| Trailer or launch video from existing game assets, a brand kit or a public website | launch-film |
| Local SVG/icon authoring, validation, sprite sheets, nine-slice assets or platform export | prompt-to-asset's restricted local tools |

- For simple UI clicks, alerts and other synthetic effects, use Pro Motion's
  local synthesis first. Use SFXMint when a library sound better fits the request;
  choose only downloads explicitly marked free. If an allowance, login or paid
  format blocks it, use local synthesis or an existing suitable local asset.
  Never purchase access or treat a returned paid WAV URL as free entitlement.
- For a combined media request, carry the asset through the needed stages:
  author/export with prompt-to-asset, cut out with Bulk BG Remove when relevant,
  animate with DESIGN:OS or Pro Motion, assemble with launch-film when appropriate,
  and verify the resulting files and their use in the game. Select stages from
  the actual request; do not generate unrelated art, sound or videos.
- Run the prepared project launchers yourself. Prefer the restricted native
  prompt-to-asset MCP when available; if tool discovery is stale, use its same
  configured restricted local stdio server through an available process tool.
  Do not replace it with the unrestricted CLI. Report a genuine host limitation
  only after checking the installed paths and available local invocation options.
- Keep the free-feature/no-external-sign-in constraint throughout automatic
  selection and fallback. Automatic workflow use does not expand the requested
  scope, allow paid services, or authorise publishing, sending messages or new
  provider connections. Ask only for missing decisions that affect the work.
- For campaign prose, combine Story Skills and Writer's Loop: establish canon and
  branch/era boundaries, draft or revise within the authorised scope, then review
  prose and continuity. Run the appropriate checks as part of delivery.
- Context Guard's nine installed lifecycle hooks are trusted for this reviewed
  package. Let its built-in automatic activation protect complex work and its
  recovery hooks preserve active work across compaction/resume. Do not ask the
  user to type `context-guard on` for normal work. Simple requests can remain in
  the plugin's lightweight journaling mode. Do not fabricate user control prompts,
  edit private guard state, or claim protection is active without hook evidence.
- Setup, source locations, commands, and verification are documented in
  `tools/COMMUNITY_PLUGINS.md`; pinned installs are in `tools/community_plugins.lock.json`.
- Use Story Skills for substantial campaign planning, scene writing, character/era
  continuity, and editorial review. Its workspace is `writing/story-skills/`.
  Read `writing/SOURCE_MAP.md` first. The existing game sources, confirmed user
  decisions, and `ROADMAP.md` remain authoritative. The starter workspace is not
  an imported manuscript or proof that the game's continuity has passed.
- Use Writer's Loop for substantial requested prose drafting, critique and revision.
  Preserve character-specific voices, protected outcomes, historical knowledge,
  and the requested scope. Existing user approvals remain valid. Do not treat
  generated drafts as approved canon or infer standing preferences from them.
  Preference learning is session-only unless the user explicitly enables storage.
- Use falsegreen-skill for focused review of regression tests being added or
  changed, especially save state, campaign outcomes, knowledge isolation, and
  phone styling. Load its detailed catalog only as needed. Preserve this file;
  never replace it with a plugin's example AGENTS.md. Findings require evidence;
  test review does not replace running relevant tests or inspecting rendered UI.
- Use Context Guard's standard protection for long or resumed multi-step tasks.
  Preserve the existing task scope, approval order,
  paused work, and actual verification evidence. Installation does not adopt
  strict/release contracts or authorize publication. If hooks are unavailable,
  report that limitation and continue using the existing project records.
- Existing user authorisation carries through the selected plugin workflows.
  Do not re-request approval for work already authorised in the chat. Ask only
  for genuinely missing decisions, expanded scope, or a required host trust
  review after plugin contents change; never silently trust an updated package.
- Use SFXMint for library sound-effect work under the free-only routing above.
  Keep audio local for offline play,
  use `sound.py` and existing mute/volume controls, and record each new asset's
  stable source page, CC0 license, AI/synthesis origin, and SHA-256 in SOUNDS.md.
  Preview sound in context before accepting it. Setup alone does not authorize
  paid downloads, replacement of existing audio, or a game audio redesign.

# Free media plugin workflow

- The five additional media plugins are enabled only for this project. Read
  `tools/FREE_MEDIA_PLUGINS.md` and the relevant installed skill before use.
  Use `python tools/media_tools.py` for the prepared Windows runtimes. Do not run
  upstream global installers or bypass the project launcher with the unrestricted
  prompt-to-asset CLI.
- Route requested background cutouts to Bulk BG Remove; local motion graphics
  and synthesised WAV effects to Pro Motion; SVG/line-art animation to DESIGN:OS;
  requested trailers using existing art or a public website to launch-film;
  local SVG/icon authoring, validation, sprite sheets and export to prompt-to-asset.
- Only fully free features requiring no external sign-in are authorised. Do not
  initiate provider login, API-key setup, paid credits, trials, hosted generation,
  Suno/Udio/ElevenLabs music, purchases, publication or deployment. Use local art,
  local synthesis and local rendering. Public dependency/model downloads need no
  account; do not bypass Bulk BG Remove's memory checks. Check asset/model licences
  for the actual intended use rather than treating free access as public domain.
- Prompt-to-asset is deliberately local-only: ten approved tools, inline_svg mode,
  no provider-credential loading and no HTTP generation. Keep that restriction
  when updating it. Run `node tools/verify_free_media.mjs` after changing its adapter.
- Draft outputs belong in `media-workspace/`; installation tests in `.test-tmp/media/`.
  Installing tools does not approve new production assets or gameplay changes.
  When later asked to integrate art/audio, preserve the phone/in-person rules,
  provenance, patch-note requirements and relevant visual/playback verification.
