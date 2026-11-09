# Recovery of the 17 oversized development chats

Recovered on 7 November 2026 from local session logs after the chat tool could not read image-heavy turns. Only completed assistant reports were extracted; images, tool output, user messages and credentials were not copied. Local logs were read without modification.

## Results

- All 17 root-session logs were found and scanned, including the archived portrait chat.
- 66 completed reports were recovered; 59 were absent from the previous extraction.
- Every completed turn in this snapshot has a report; no selected event failed JSON parsing.
- Three chats contain only interrupted work and no completion report. They receive explicit historical audit entries, not invented completed releases.
- Some other chats also contain interrupted or still-active turns. Those remain excluded from completed update records.
- Original timestamps, log basenames, event ordinals and turn IDs are retained in `recovered_history.json`. Brisbane dates are chat-completion dates, not release dates.

## Coverage

| Original chat | Completed reports | Unfinished at snapshot |
| --- | ---: | ---: |
| Add Neo Ishida as cast member | 4 | 0 |
| Add photos to Yuriko’s grove gallery | 3 | 1 |
| Find missing grove galleries | 6 | 0 |
| Create 8 Garrett outfit variants | 0 | 1 |
| Create 8 Emily outfit variants | 4 | 0 |
| Add Rei outfit variants | 5 | 0 |
| Create eight April outfits | 0 | 1 |
| Add Grove gallery photos | 4 | 0 |
| Find missing Grove galleries | 7 | 0 |
| Create Emily’s grove gallery | 1 | 1 |
| Use Vendetta for world-building | 2 | 1 |
| Add Blisk to the lore | 6 | 2 |
| Add group photos to Grove gallery | 4 | 0 |
| Generate Garrett gallery images | 6 | 1 |
| Align portraits and add art guide | 0 | 1 |
| Add texting notification sounds | 4 | 1 |
| Add at-home character portraits | 10 | 0 |

The former retrieval gaps are resolved. This does not turn interrupted work into completed work, prove all historical test claims, or create a missing Git history. An active chat can produce further updates after this fixed snapshot.

## Important distinctions

- **Create 8 Garrett outfit variants**, **Create eight April outfits**, and **Align portraits and add art guide** have no root-turn completion. Current outfit manifests are not proof those requests finished. Their planning and interruption are labelled in the curated entries.
- Early Garrett Grove reports explicitly describe generated assets awaiting UI integration; those steps are preserved separately.
- **Add Blisk to the lore** includes changes to external Vendetta references. These are source-world history, not an automatic release of every lore fact into this game. Its completed resident, portrait and character-tier changes are separately identified.
- Past failures and blocked checks remain visible in original reports. This recovery does not silently rewrite them as successful tests.

## Verification

Run `python -m unittest discover -s tests -p test_patch*py -v` and `python patch_notes.py validate`. Recovery checks assert all 66 report texts are represented, all 17 chats have historical entries, interrupted turns are excluded from completed reports, and extraction rejects another project/thread. The standard catalogue tests cover filtering, sources, exports and reader persistence.

This update changes only archive content, recovery tooling and the archive notice. No game feature, media asset, or story save is modified.

Verification completed: all eight patch/archive tests and catalogue validation passed. The patch notes UI smoke passed at both supported sizes; the rendered minimum-size screen was inspected. A search-test assumption that only one entry matched was updated to select the intended result explicitly.
