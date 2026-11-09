# Patch notes system validation — 7 November 2026

Checks performed for this change (not a recertification of earlier game features):

- Initial catalogue validation (before historical recovery): 269 unique entries, comprising 48 curated notes and 221 original report entries.
- Six focused unit tests passed: preserved-section/source coverage, invalid schema/duplicate/date rejection, combined filtering and date ordering, preference persistence and revision-aware unread state, atomic-write failure preservation, and selective export with provenance.
- Patch notes UI smoke passed: real Tk search, bookmark/read controls, filtered empty state, report visibility, Markdown export, inline corrupt-catalogue error, and 1100×760 / 850×600 layouts. Preferences and exports used isolated temporary storage.
- Start-screen smoke passed: four protagonist previews, explicit Begin action and 1220×940 / 1000×800 layouts. The new patch notes entry is visible in the minimum layout.
- Phone dark-theme smoke passed across 32 phone pages, chat, contact details and embedded controls.
- Rendered screenshots of the patch reader and minimum start-screen layout were inspected. A footer/action layout overflow found during the first check was corrected before the successful run.

The initial unit-test attempt used the system temporary directory and failed/stalled under the filesystem restrictions. It was stopped; the successful run used the workspace `.test-tmp` directory. Smoke tests emitted existing sound-loading warnings; audio was not changed or validated by this work. No live AI generation was used. Player story writes were mocked in game smoke tests; patch-reader state and exports were isolated.

Focused smoke screenshots are generated under `tests/screenshots/` and are not part of the distributed history.

## Historical recovery follow-up

All eight patch/archive tests passed after importing the recovered reports, including exact text coverage for all 66 reports, all 17 chat chapters and exclusion of interrupted turns. Catalogue validation passed. See `RECOVERY.md` for scope.
