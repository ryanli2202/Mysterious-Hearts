# MH-005 implementation and verification

Recorded 2026-11-10. Runtime implementation is in `campaign_prose.py`, `campaign_prose_ui.py` and the existing campaign handlers. `campaign_prose/catalog.json` contains the reviewed shipping text; `tools/build_campaign_prose.py` compiles the three draft manuscripts and the four developed sample passages, with explicit editorial corrections and branch conditions. Manuscript directions are not displayed to players.

## Access and reading

Restart the game, select Garrett, Rei, Fox or Gordon, and open **In person → Story**. Existing objective buttons open the corresponding novel scene. Finish the scene to commit the selected action through its original campaign handler. All current campaign and historical scenes run in the in-person window.

**Time with the people in your story** offers optional visits during their chapter windows. The board explains the required venue and unavailable friends, offers normal travel, and supports sharing, privacy and deferral. A visit does not summon cast, give evidence, advance another campaign, or award trust or romance. Existing public-record witnesses and Mei's established supplier role remain authored scene participants; Mei's optional closing visit is limited to the Golden Dragon from 11:00 to 17:00, with no invented surname or new phone contact.

The dark reader displays text immediately, preserves paragraphs, offers 11–24 point type, previous/next controls, required reflection choices, a scrollable page, and saved page/scroll state. It retains historical backgrounds/portraits where verified assets exist and returns to current-day art afterward. At narrow widths the illustration hides to retain readable text and reachable controls. **Story so far** shows earned findings and selected reflections. **Read scene history** reopens completed scene snapshots without dispatching actions or rewards. Reading and archive browsing pause the simulation clock.

An optional Game Master description can be requested on selected action pages. Authored text remains available on failure; requests use the existing configured provider. Navigation and save changes discard stale replies. Generated text cannot mutate story, combat or reward state. Providers were mocked during verification; live model output quality is not certified.

## Coverage

| Route | Integrated scope | Runtime placement |
| --- | --- | --- |
| Garrett | GD01–GD43; ten chapters; G1–G6; GS01–GS10; GR-G01–GR-G06; two shared memories; expanded April and school memories; D02 reunion and D03 dinner | The original 20 steps remain unchanged. Wrong answers retain daily retry gates. Both reconciliation policies, family authentication, legitimate early recognition, real Charles victory, leadership operations, accountability, brother visit and closing meal remain distinct. |
| Rei | RD01–RD35; eight chapters/resolution modules; R1–R6; RS01–RS10; GR-R01–GR-R06; two shared memories; three expanded school memories including D01 Marcus news | Original investigation stages, all three successor decisions and either order of successor/Richter resolution. Destroying the successor requires its real victories. Richter's apology and programme closure require victory; failure retains an unresolved mission. |
| Fox and Gordon | FD01–FD38 and FM01–FM04; twelve chapters; all 36 present-day briefs; four partnership memories; FL01–FL08; six Syndicate guard approaches; four Aces and Crow; D04 aftermath | Both selectable viewpoints; all nine files; all 24 Ace orders; reveals before combat; partial guard progress and retries; current Crow defeat/withdrawal; distinct earned legacy capture; scoped repeatable operations. |

There are 120 authored sections and 28 optional visit entry points. Some visits combine a present scene and its memory; some major sections span a before/after result boundary. These are not 120 extra quests. The existing source outlines retain the detailed brief-to-manuscript mapping. `GARRETT_STEPS`, `REI_STEPS`, `SOCIAL`, `memory_pages` and the Interpol case mapping supply executable placement.

GR-F01 is the split-dumpling receipt; GR-F02 is the development of late visits and ordinary company. Both viewpoints use the same spoken sequence and external events, with distinct interiors. The receipt pinned near the counter remains different from the later drawing in Garrett's till drawer. Completed views record stable shared-event IDs within the current protagonist's narrative state; neither route grants the other's progress or disclosures.

## Voice and chapter review

Garrett notices hands, food, domestic objects and practical work. He reaches for humour or useful activity when waiting is harder, and lets hurt coexist with relief. His later protection choices question whether help creates an obligation. Rei notices framing, pages, gaps and the distinction between a document and a memory. His uncertainty is allowed to remain unresolved; friendship and creative work matter beyond investigation or recovery. Neither voice prescribes forgiveness.

Fox notices routes, physical detail and an action he could take. Impatience can become a demand for certainty, then a willingness to report limits. Gordon notices what a record supports, the cost of a decision to another person and commitments that require follow-through. His precision is a defence as well as a professional strength. Shared dialogue is retained while interior passages select the active protagonist; neither has direct access to the partner's mind.

The implementation review covered the following chapter transitions:

| Chapters | Motivation, pacing and continuity checks |
| --- | --- |
| Garrett 1–2 | Ordinary work and existing friendships establish stakes before the first lead. April's waiting memory stays at the opening; inconclusive records do not become proof. Disappointment gets its own reflection. |
| Garrett 3–4 | Public authorisation, account verification and family authentication remain separate. Wrong answers neither advance the enquiry nor borrow the successful invitation. The cup memory follows the chosen answer and returns to its actual result. |
| Garrett 5 | The school memory is at the laboratory approach. Direct recognition does not acquire letters or invitation knowledge. Reunion dialogue precedes a real fight; disclosure, reconciliation and private reflection follow victory. This is deliberately the longest Garrett chapter. |
| Garrett 6–8 | The civilian question about obligation leads into protection and internal accountability. Guard victories remain scoped. Optional Rei/crew conversations do not decide leadership policy or confer authority. |
| Garrett 9–10 | The brother visit acknowledges guarded reconciliation when chosen. An ordinary shared meal follows larger obligations. April/Mei follow-through and the distinct drawing return to daily life without claiming every threat is over. |
| Rei 1–2 | The chosen drawing and childhood timetable are distinct. Archives corroborate imposed training without restoring missing memory. Yuriko's knowledge depends on disclosure. |
| Rei 3 | Marcus has creative preferences and humour before the developed news scene. No invented last words, method or single cause of death. Each memory has a present-day return and a player-selected pause; no automatic chain starts the next memory. Optional friends remain available between them. This is deliberately the longest Rei chapter. |
| Rei 4–5 | Present withdrawal evidence motivates Blackstone; current successor evidence motivates deliberation without excusing the past or preselecting a branch. Garrett's advice cannot supply undisclosed clan details. |
| Rei resolution modules and ending | All three successor outcomes and both resolution orders remain valid. Loss cannot produce apology, forgiveness or programme closure. A solo final reflection, partial gathering and ordinary friendship scenes avoid summoning unavailable actors. |
| Fox/Gordon 1–4 | Eight Senses does not identify intent or ownership. The cleaner, reused number and date discrepancy each receive a discriminating check. Partnership memories establish consent, follow-through, disagreement and accountability. Interview and frontage corroboration are separate phases. |
| Fox/Gordon 5–8 | Each Ace enquiry stands independently: delivery versus authorship, rumour versus dated presence, routine payment versus authorisation, transferred trace versus personal route. Corrected findings precede the reveal and existing guards. No Ace exposes another case or becomes an informant after defeat. |
| Fox/Gordon 9–10 | A routing label does not name the contact or the Crow. A supported entrance does not imply control. The player is explicitly told that Night Ledger is the established story defeat before choosing combat actions. |
| Fox/Gordon 11–12 | The argument accounts for the living and the failed objective without rewriting earned evidence. Later protection work matters without claiming the Syndicate is destroyed. Legacy capture has separate prose. No pre-fight reflection recurs during post-defeat review. |

Corrections made during review include the two shared first-meeting exchanges, missing D01–D04 prose, private/single-attendee variants, phase-specific contractor/repeatable-operation text, conditional invitation knowledge, viewpoint leakage in legacy closure, period-art transitions, and removal of editorial instructions. Final condition dictionaries are independent copies, checked by regression tests.

### Measured reading inventory

`python tools/report_campaign_prose.py` reproduces `campaign_prose_reading_inventory.json`. The selected normal-route inventory includes all optional social text with one appropriate disclosure/branch variant, each paragraph once. It excludes alternate direct/legacy routes, UI text, combat boilerplate, reflection responses and generated description.

| Viewpoint | Selected prose words | Estimate at 200 words/minute |
| --- | ---: | ---: |
| Garrett | 10,115 | 50.6 minutes |
| Rei | 8,299 | 41.5 minutes |
| Fox | 8,284 | 41.4 minutes |
| Gordon | 7,979 | 39.9 minutes |

These measure comparable reading scale, not identical length or timed gameplay. Rei's Marcus chapter and Garrett's reunion deliberately receive more space. Fox/Gordon additionally retain the many actual encounters and operation transitions; padding each guard with a long speech would reduce rather than improve pacing.

### Source and editorial limits

Existing local character references, campaign rules and approved manuscripts govern the implementation. The two original Vendetta documents and Fox art path recorded in `interpol_source_notes.json` were checked again and remain unavailable. The four undated Fox/Gordon historical incidents therefore remain explicitly authored Winterfield adaptations; no original-source date, prior romance, massacre or future outcome is asserted. Existing installed art is reused.

Chapter review here is an implementation/editorial review. An independent cold read by a person unfamiliar with the external lore has **not** been performed and is not claimed as passed. That review item from the plan remains a validation limitation; automated coverage and prose length do not replace it.

## Save and outcome contract

No numeric campaign step is renumbered and no prior encounter/reward is replayed. New narrative state is additive under `campaign_prose.players[protagonist]`: read sections, reflections, disclosure recipients, deferred visits, shared-event views and type preference. Existing active dialogue snapshots finish as saved. Completed campaigns are not reset or retroactively forced through opening memories. History records experienced scenes; it does not fabricate optional visits that older saves never experienced.

The five established memory IDs are preserved. Garrett's initial April memory gates the opening, and his school memory gates the laboratory stage; Rei's three school memories gate the storyboard stage. A past gate is not imposed on a save already beyond it. Existing open memory snapshots still finish safely. Main action handlers continue to validate actual venue, audience, readiness, clearance, daily limits and prior victories before committing anything. Optional visits reject an already-open scene rather than overwriting its saved position.

Explicit disclosures are saved only after the conversation finishes. Later AI context includes them only for the authorised recipient in an appropriate audience, without supplying Charles's cover, location or number. Combat reactions read actual resolved records, require conscious participants and are emitted at most once per exchange. Ordinary defeat, scripted Crow defeat, legacy capture and repeatable success have distinct aftermath paths.

## Verification record

The final regression run passed **110 tests**: 18 campaign-prose, nine major-campaign, eight dialogue, six flashback, five Charles-quest, 18 Interpol, six story-expansion, 23 enhanced-combat, 14 combat-completion and three Charles-disclosure checks. Full output is in `tests/results/mh005-units.txt`. This includes all 24 Ace orders for each Interpol viewpoint, both reconciliation policies, every Rei ending in both resolution orders, real save-file round trips, older active/completed saves, unavailable friends, private recipients, decline/defer behavior, duplicate-effect protection, independent compiler conditions and optional generation failure/stale replies. Test-provider calls are mocked, and fixtures simulate combat results where the test concerns narrative gating rather than combat balance.

UI smoke checks passed: `campaign_prose_ui_smoke.py`, `campaign_dialogue_ui_smoke.py`, `campaign_flashbacks_ui_smoke.py`, `charles_quest_ui_smoke.py`, `major_campaigns_ui_smoke.py`, `player_story_ui_smoke.py`, `interpol_ui_smoke.py`, `story_expansion_ui_smoke.py` and `phone_dark_theme_smoke.py`. The last checks 34 phone pages plus chat, contact details and embedded controls. An initial story-expansion UI failure exposed an inappropriate pre-fight reflection in the post-defeat review; the runtime condition was corrected and the smoke rerun successfully. An older Charles fixture now completes the school memory at its new contextual gate.

The wider conversation-lore suite passed 29 of 32 tests. The three failures are the previously reported missing Charles TV-show preference, incomplete Garrett audience-reference coverage (this run first reports Yuriko), and missing Nessa Quinn portrait-style data. The earlier `release-2026-11-10-crow-address-canon` entry already records these data-failure categories. The new narrative audience tests pass; unrelated character-source data was not invented to silence the broader checks.

Already inspected renders: pilot April scene, shared first meeting and present return, reflection selection, compact 24-point text, history/recap and optional-visit board. Five historical-scene smoke renders verify the period portrait files, backgrounds, compact controls and restoration. All inspected surfaces use the existing dark palette.

Catalogue validation and Markdown export passed (480 entries at validation). The patch-note reader smoke passed search, filters, reader state, exports, error/empty states and two sizes. The patch-note unit suite passed five of six checks; historical archive-source coverage still fails on the pre-existing missing `tests/screenshots/mixtape-art-review-0.jpg`. No replacement historical screenshot was fabricated.

The start-screen smoke also passed all 28 previews, paging, explicit Begin and default/minimum layouts. This brings the successful UI smoke scripts for this update to eleven. Final follow-up output is appended to `tests/results/mh005-ui.txt`.
