# Maintaining Mysterious Hearts patch notes

The source of truth is `patch_notes/catalog.json`. The desktop reader and command-line export both use it. `PATCH_NOTES.md` is a generated, portable copy of the curated entries. Original development reports are available by enabling **Include original chat reports**; they deliberately include advice and superseded implementations, not just shipped work.

## Recording the next update

1. Add one entry at the beginning of `releases` with a permanent, unique ID, such as `release-2026-11-08-feature-name`. Never renumber existing IDs.
2. Set `kind` to `Release`, supply the actual publication date as `YYYY-MM-DD`, and select a useful category. Do not create a game version number unless the game adopts that version explicitly.
3. Write a short player-facing summary. In `body`, group substantial work under Added, Changed, Fixed and Known limitations as appropriate. Include where to find the feature, before/after behavior, important rules and the checks actually performed. Do not claim a test passed merely because a test file exists.
4. Write explicit `save_impact`: whether a restart or migration is required, what existing saves retain, and any intentional behavior changes. Provide file/test/document references in `sources` and explain the evidence in `provenance`.
5. Run `python patch_notes.py validate`, `python -m unittest discover -s tests -p test_patch_notes.py -v`, then `python patch_notes.py export`. UI changes also need the patch notes and start-screen smoke checks. Use the bundled Python executable when `python` is unavailable.
6. Keep entries immutable for history except factual corrections. A content correction changes the entry fingerprint and makes it unread again. Reader state belongs in the ignored `patch_notes_preferences.json`, never in a story save.

Required entry shape:

```json
{
  "id": "release-YYYY-MM-DD-short-name",
  "title": "A concise update title",
  "category": "Interface",
  "kind": "Release",
  "date": "2026-11-07",
  "summary": "What the player gains.",
  "body": "Added\n\nDetailed behavior and access instructions.\n\nValidation\n\nChecks actually run and any remaining limits.",
  "save_impact": "Existing stories remain compatible; restart to load changed Python code.",
  "sources": ["source_file.py", "tests/relevant_test.py"],
  "provenance": "Implemented and verified in this update."
}
```

## Historical accuracy and coverage

The initial archive was reconstructed on 7 November 2026. The repository had no commits or release ledger. Every pre-archive README section is preserved in `README-at-archive.md` and represented in the curated catalogue. Additional notes cover code/test-supported changes absent from those sections. `development_records.json` preserves 284 retrieved completed reports from project chats, including the initial design and first playable build. Reports from the same turn share one catalogue entry.

Chat completion dates are displayed in Australia/Brisbane and are **not release dates**. Retrospective topics have unknown dates unless documentation explicitly dates them. Catalogue order groups readable topics and does not assert a historical sequence. Original README paragraphs sometimes retain obsolete values, roster sizes, travel rules or suggestion behavior; newer implementation takes precedence. The original reports explain several intermediate designs, such as model switches and automatic suggestions later becoming manual.

The 17 former retrieval gaps (including one archived chat) were resolved by reading local root-session logs. `recovered_history.json` preserves 66 completed reports with source ordinals, timestamps and a per-chat audit; 59 reports were missing from the initial extraction. `gaps` is now empty and `resolved_gaps` records each resolution. Three chats have no completion report because their turns were interrupted. Other interrupted or still-active turns remain excluded. See `RECOVERY.md` for exact coverage. This closes retrieval gaps, not unrecorded work or a missing Git history. Historical tests remain attributed reports, not freshly certified results.

`tools/build_patch_history.py` is a one-time importer, intentionally refusing to overwrite an existing catalogue. It is not a release publisher. Add future updates directly instead of rerunning it.

## Reader behavior

- Open **Patch notes & update history** on the start screen or in **Tools** while playing.
- Search matches all typed words across title, summary, full details and sources, without case sensitivity.
- Filters combine category, record type, unread/bookmarked status and optional original reports. **Dated first** puts unknown dates last; it does not invent chronology.
- Reading a note does not automatically mark it read. Use **Mark read** explicitly; corrections make it unread again.
- Export selected notes or filtered results without overwriting earlier exports. The status line gives the output path under `patch_notes/exports/`. **Copy note** copies Markdown.
- Missing or malformed catalogue files produce an inline error. Damaged reader preferences reset to defaults. Export and preference write errors remain in the viewer.
- No network requests, AI calls, credential access or story mutations are involved.
