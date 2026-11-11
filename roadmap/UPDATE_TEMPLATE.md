# Future update entry template

Copy this structure into `ROADMAP.md` for each new update, replace placeholders, and add its summary row. Keep detailed designs in a linked plan when they are too long for the roadmap. Automatically assign relevant plugins to concrete tasks using [the plugin assessment and workflow](PLUGIN_ASSIGNMENTS.md), the project routing rules and the pinned lock. Every separately maintained child plan needs its own task assignments; a list of plugin names alone is insufficient. Adjust relative links for the destination document when copying the template.

## MH-NNN Update title

**Status:** Proposed or Planned  
**Added:** Actual date recorded  
**Area:** Affected game area  
**Detailed specification:** Link to plan, or describe the scope here

Describe the player-visible outcome and how players will access it.

### Milestones

- [ ] Confirm scope and dependencies.
- [ ] Assign relevant plugins to specific tasks, including outputs, checks and dependency/pause gates.
- [ ] Implement the agreed behaviour.
- [ ] Run relevant checks and inspect new UI states.
- [ ] Document save impact and release evidence; validate and export patch notes where required.

### Plugin task assignments

| Milestone / specific task | Plugin and relevant skill / ordinary tools | Concrete output | Required verification | Use / dependency gate | Execution evidence |
| --- | --- | --- | --- | --- | --- |
| Replace with a scoped task from this plan | Select the relevant installed plugin/skill, or explain why ordinary implementation tools are sufficient | Name the artifact or behaviour | Name meaningful tests/reviews/render/playback checks | Required when task runs; Conditional with trigger; Future maintenance only; or Not applicable with reason | Pending until actually executed; then link commands, results and limitations |

Break mixed tasks into separate rows where writing, media preparation, integration and verification have different outputs. Assess the ten project routes against actual scope: Story Skills for canon/branches/eras; Writer's Loop for substantial prose/specification review; Context Guard for complex/resumed work; falsegreen-skill for substantive regression-test work; Bulk BG Remove for cutouts; prompt-to-asset for restricted local SVG/export; DESIGN:OS for suitable vector motion; Pro Motion for local compositing/synthetic effects; SFXMint for explicitly free library sounds; launch-film for a requested trailer. Record unneeded routes as not applicable in a short note rather than creating work to use them.

**Conditional use / exclusions / capability gaps:** State actual triggers, omitted workflows and any unmet need. The restricted media plugins do not generate detailed raster portraits, room paintings or scene illustrations. Keep a separate permitted production task when needed. Sound or trailer work is conditional unless requested in scope.

**Shared execution rules:** Read applicable installed skills at execution, resolve paths through `tools/community_plugins.lock.json`, and run prepared launchers automatically. Preserve free/no-sign-in limits, source/provenance, dark phone styling, in-person routing, approved order and pauses. Context Guard requires actual hook/session evidence; report absence without editing private state. Existing authorisation carries across selected workflows. Assignments are not completed milestones or proof of prior plugin use.

**Dependencies:** Required systems, assets, or preceding updates.

**Completion criteria:** Observable outcomes and required checks.

**Save impact:** Known impact or what must be assessed.

**Progress and evidence:** Actual completed work and checks, or implementation pending.

**Blocker and next action:** Include only when blocked.

**Release record:** Add the patch-note link and actual release details when released.
