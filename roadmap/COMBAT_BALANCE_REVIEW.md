# Part 2 implementation and balance review — 2026-11-10

**Superseded status:** The initial limitations below are closed or explicitly assigned to Part 1/MH-002 by the [Part 2 completion record](COMBAT_PART_TWO_COMPLETION.md). This document preserves the first systems-release evidence.

Tracked under MH-001. This records implemented behavior; the design documents retain broader acceptance requirements. Part 1 animations and the separate MH-007 interface revamp are not included.

## Implemented behavior and access

Open Combat in the in-person window. The encounter screen uses location art behind opposing portraits, resource bars, authoritative state counters, opponent intent, move costs, target selection and scrollable narration. Ability details opens a source-linked dossier. The combat hub offers Guided, Standard and Minimal explanations without changing enemy strength.

Neo and Thirteen build Shinigami readiness through varied meaningful exchanges against credible opposition (four normally, three below 60% health). Activation costs 20 stamina for four exchanges, once per encounter, with normal action costs and two exchanges of recovery strain. Repeated identical exchanges do not farm readiness. The AI uses revealed observations and feasible responses, not the player's next selection. Active pressure is multiplied by 1.35; feasible reactive blocks reduce incoming damage to 60%, subject to an opposing-force check. A one-hour recovery action resets the player's spent state; changing encounters alone does not.

Daniel gains up to three War God momentum levels from varied successful contact. Each gives 6% pressure; combos spend three extra stamina. A break/counter finisher at level three spends ten extra stamina, gains 30% force and consumes momentum. Disruption/separation erodes it.

True Sight lowers prepared mana costs to 65% with a minimum cost of one and improves precision and application of force. Analysis uses observed moves. Conduit channels cost eight mana to switch and four per action: red lightning increases force, blue lightning increases speed, Fire increases force and breach, Ice removes reaction latency but not travel time, and Wind applies a 22% soul component. Valentina shares wind/soul mechanics. Misanthropy costs 18 mana, lasts four exchanges and provides a finite 18%-health endurance reserve. It records injury debt, never heals; exhausting the reserve or ending the state while carrying lethal debt causes collapse. Robots do not take soul injury.

Canonical combat expressions separately adjust force, endurance, tempo and precision. Damage pacing is 60% of the prior raw result; sparring applies a further 55% restraint factor. Repeated control effects have an immunity window and reflected force is capped. April remains physically vulnerable; the support resolver can grant an observed opening after two exchanges, at a seven-stamina cost. This hook does not add a new companion-recruitment route.

Iron Circle generated opponents use D 450–301, C 300–101, B 100–11 and low A 10–2. Style previews expose counterplay before entry. Ordinary ladder wins stop at #2; promotion requires defeating the actual current champion, initially Rei. Defeat on title defense installs the challenger as champion while preserving earned-title history. A legacy #1 save keeps its title. Competitive position does not rewrite the entrant's stats.

Enhanced Richter uses a targeting/burst/recovery/ram/recovery sequence and takes 30% more damage in exposed recovery. His civilian identity remains unranked. Existing solo access and mission victory gates remain authoritative. **The Crow containment campaign deliberately still forces defeat after four exchanges; finishing it through another result cannot capture him or bypass the authored retreat.** This is an explicit campaign exception to ordinary resolved combat.

Ordinary encounters offer survival, delay and escape objectives; rescue is available with an existing ally. Success is recorded separately from a duel victory and does not clear victory-gated campaigns. Rescue checks the ally remains alive and the player meets escape positioning; it does not simulate a separate escort position.

Spar, fight and lesson requests now generate the protagonist's line before the recipient's response. The exact line is validated and retained through display and history. Selected intent/art, eligibility, stale-result rejection and once-only commitment remain authoritative. Three actual provider samples are saved in `combat-dialogue-samples.json`; canonical and custom mock regression checks cover failure and persistence. A custom protagonist live-provider sample is not part of this evidence.

The exported `COMBAT_IDENTITY_SHEETS.json` contains 104 source-linked records, including unknown/unranked people and combat archetypes. Public title disclosure requires audience recognition; observing a technique does not reveal civilian identity. This conservative default is not a new discovery quest system.

## Balance evidence

`tools/combat_balance_matrix.py` runs exploratory seeds 0–5 on both sides. `tools/combat_balance_acceptance.py` declares acceptance ranges separately and runs previously unused seeds 100–111 on both sides. Both exercise the resolver without providers, world rewards or persistent story saves. Baseline comparisons suppress advanced forms; state comparisons enable them. A 50-exchange cap decides by remaining health fraction, so these statistics include timeout decisions, not only knockouts. They measure automatic policies, not universal player win probabilities.

The holdout passed all ten groups: S+/S 89.6%, S/A+ 89.6%, A+/A 79.2%, A/B 95.8%, apex/B 100%, B/C 100%, C/D 100%, Rei/enhanced Richter 75%, Rei/contender 100%, and adjacent arena boundaries 52.8%. Both Protocol comparisons activated in every sample; active-window dealt/received damage ratios were 1.87 for Neo/Ivan and 1.19 for Thirteen/Charles. Temporary competitiveness does not guarantee winning the whole fight. Full criteria and individual pair results are in `combat-holdout-results.json`.

Generated skills receive structural balance-review metadata without changing stable fingerprints. Path transitions record before/after review data. These are bounded structural checks, not individual matchup simulations of every generated move.

## Save impact

Restart the application to load Python changes; no new story is required. Additive defaults retain active resources, stable learned/signature IDs, earned refinement and Path history. Canonical lore revisions reconcile old descriptions without renaming custom Traits. Custom naming alone cannot grant a canonical ability. Existing arena snapshots retain their stats; new candidates use the tuned scale. Revealed active enhanced-Richter snapshots receive the boss move set without resetting resources. New state, recognition and championship fields are save-owned. Historical dialogue and campaign progress remain intact.

## Verification and remaining acceptance

Passed: 78 combat tests, 23 enhanced-combat tests and 18 Interpol tests, including the authored Crow outcome. Also passed during implementation: major campaigns (9), campaign dialogue (8), guard portraits (4), Four Aces (4), custom protagonists (11), Vendetta lore (5). Compact Part 2, opponent, dialogue and enhanced-combat UI smoke checks passed. Rendered compact HUDs and ability dossiers reviewed. Dark-theme smoke passed across 34 phone pages and embedded controls. No animation production or playback files changed.

Release checks: patch-note catalogue validation and export passed (465 entries); patch-note UI smoke passed including error/empty states and two sizes; start-screen smoke passed with 28 previews and minimum/default layouts. Patch-note unit tests: five passed, one failed on the missing historical screenshot below.

The broader plan remains in progress for full group-coordination/ally-state parity and specialist scenario coverage, depleted-entry boss balance evidence, exhaustive combinations/progression simulations, additional recognition/disclosure coverage, live custom-dialogue review and Part 1 visual integration. `starting_scale()` is a shared numeric handoff to MH-002, not a completed custom-character creator/kit implementation. Do not mark these as verified releases. The unrelated story-expansion suite has a reunion-location expectation mismatch (Garrett's home versus noodle shop); no unrelated story logic was changed for it. Patch-note archive tests also expose a missing historical `crow-contact.png`; preserve historical evidence rather than fabricate it.
