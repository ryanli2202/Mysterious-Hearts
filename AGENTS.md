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

- For future player-visible features, fixes, balance, artwork or compatibility changes,
  add a detailed entry to `patch_notes/catalog.json` following `patch_notes/AUTHORING.md`.
- Record actual behavior, access instructions, save impact, evidence and checks performed.
  Preserve stable IDs; do not invent historical dates, version numbers or passed tests.
- Run `patch_notes.py validate` and refresh `patch_notes/PATCH_NOTES.md` using
  `patch_notes.py export`. Original chat reports are evidence, not automatically releases.
