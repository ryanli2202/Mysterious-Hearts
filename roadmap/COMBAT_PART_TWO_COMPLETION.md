# MH-001 Part 2 completion — 2026-11-10

Part 2's non-animation implementation and relevant gameplay/UI verification are complete. MH-001 as a whole remains in progress because Part 1 owns animation production and combined visual timing/lifecycle verification. The character-creator UI/starting-kit work belongs to MH-002; the later large-portrait redesign belongs to MH-007. Neither is silently included in this release.

## Final implementation

- Partners now use the same form/channel/Protocol/endurance activation and adjusted-cost rules as opponents. Their state clocks advance once per exchange, without double-ticking the opponent. Recovery, saved expenditure and Conduit cooldowns persist. Support actions have saved resolved records and contribute their actual damage to encounter scores.
- In Stories & organisations → Guards, a companion from the current in-person group may support an ordinary patrol encounter when physically present, recovered and at trust 60 or higher. The companion cannot belong to the defending faction. Crow, Sylvanis, Takeo and Thirteen do not volunteer through this generic route. Eligibility is checked again on entry. This does not recruit partners into authored solo missions, Richter or the Crow campaign.
- April uses two exchanges of observed patterns before spending seven stamina to provide a bounded focus opening; guarding restores five stamina under ordinary conditions. She remains vulnerable to retaliation and physically weaker than combat specialists. This is an accessible tactical contribution, not a duel-tier promotion.
- Rescue has a separate saved ally position. An escort guards and follows one space per exchange, cannot follow while restrained, and must reach the same edge alive and unrestrained. Player-only escape no longer awards rescue. The compact HUD displays partner resources/state/position. Revealed Richter has explicit boss framing and low-A equipped assessment.
- Known operational titles are stored separately from civilian identity links. Earned Interpol disclosures now supply non-Ace identities as well as Ace identities. Mixed audiences receive only mutually known title context. Move observation never supplies secret identities. Rei's ring reputation is recognised at the Iron Circle without disclosing private clan history.
- Generated-skill reviews now include the prepared cost, current-profile raw-force forecast and affordability, in addition to structural constraints and progression review records. The forecast is explicitly pre-defence force, not guaranteed damage or win probability.
- The Crow containment confrontation still forces defeat after four exchanges and cannot be converted into capture by an early knockout, alternative objective or externally supplied victory result. Animations/playback assets were not edited.

## Acceptance evidence

Current checks passed:

- 92 combat tests, including 14 focused completion regressions: partner state duration/resources, April's bounded contribution, escort movement, identity/title separation, stale partner eligibility, control immunity, reflection/storage caps, recovery caps, generated-force review and an explicit four-exchange Crow defeat.
- 23 enhanced-combat, 18 Interpol, 9 major-campaign, 8 campaign-dialogue, 5 Vendetta-lore, 4 Four-Aces and 11 custom-protagonist tests.
- `tools/combat_part_two_acceptance.py`: 41,040 finite action/amplification/progression stress combinations across twelve representative profiles and five awakened stages. No non-finite force or negative paid resources. Existing reflected-force/control/recovery regressions test actual defensive behavior, rather than treating this force sweep as proof of all outcomes.
- Same-seed Richter attrition comparison, seeds 200–211: Rei won 9/12 from full resources and 3/12 at 60% health, 50% stamina and 50% mana. The boss was unchanged. This complements the earlier side-swapped tier benchmark (75% Rei wins) and campaign access/victory/retry regressions.
- Live custom-protagonist provider sample: Alex Rivers invited Rei to a friendly practice spar; Rei accepted light contact and either participant's right to stop. No invented history, private lore or completed activity. First attempt had a provider connection error; retry succeeded. Neither attempt committed a story save. See `combat-custom-dialogue-sample.json`.
- Compact state/dossier/escort smoke, actual trusted-patrol entry and partner HUD smoke, revealed-boss smoke, dialogue UI smoke, major-campaign UI smoke, Interpol UI smoke and 34-page dark-phone smoke passed. Rendered entry, partner/escort and boss screens reviewed at 1000×800. The Crow contact smoke also passed and produced a fresh screenshot, not a reconstructed historical capture.

Earlier baseline evidence remains in `combat-holdout-results.json`: ten matchup groups and both Protocol active-window criteria passed. The final changes do not alter solo damage formulas or those matchup policies. `COMBAT_IDENTITY_SHEETS.json` contains 104 source-linked records with display names and explicit unknown/unranked cases.

## Verification bounds and compatibility

This is a finite, reproducible acceptance matrix, not an exhaustive proof for unlimited future generated content or every human tactic. Future skill/progression changes keep the review hooks and must rerun relevant checks. Part 1 must verify its effects against the saved authoritative records; no animation readiness is claimed here.

Existing stories remain compatible. New ally positions default to the existing player position when loading a legacy encounter, state/recognition/review fields are additive, and earned ranks, titles, Path history, learned IDs, current resources and campaign progress remain intact. Restart the application to load the changed Python code.

Release checks passed: catalogue validation/export (466 entries), patch-note UI including empty/error states and two sizes, start UI with 28 previews and minimum/default layouts, and compilation of the changed runtime modules.

An unrelated archive-source test still fails: the current first missing source is `tests/screenshots/mixtape-art-review-0.jpg`. Five other patch-note tests pass. The previously reported Crow screenshot now exists from the fresh smoke run; historical releases were not rewritten. The previously reported story-expansion reunion-location expectation mismatch is outside this combat change and that suite was not rerun in this pass. These are repository verification exceptions, not unimplemented Part 2 mechanics.
