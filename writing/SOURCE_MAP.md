# Mysterious Hearts editorial source map

Created 2026-11-11 for the community-plugin setup. This is a navigation guide,
not a new campaign plan, manuscript import, or continuity certification.

## Authority and status

Read [AGENTS.md](../AGENTS.md), the [roadmap](../ROADMAP.md), and the relevant
confirmed user decisions before writing. Preserve distinctions between confirmed
history, implemented conditional outcomes, confirmed future premises, and proposed
scenes/details. Do not promote proposals into canon. Follow the existing production
order and pauses. In-person scenes belong in the in-person window.

The shared [campaign revision plan](../roadmap/CAMPAIGN_REVISION_PLAN.md) records
protected outcomes and the Garrett/Charles canon decision. Consult its current
version instead of creating competing copies of those decisions here.

## Campaign sources

| Route | Primary implementation or plan |
| --- | --- |
| Garrett | [Chapters](../garrett_chapters.py), [Charles quest](../charles_quest.py), shared revision plan |
| Rei | [Campaign](../rei_story.py), [presentation plan](../roadmap/CAMPAIGN_PRESENTATION_UPDATE_PLAN.md) |
| Fox / Gordon | [Interpol](../interpol.py), [cases](../interpol_cases.py), shared revision plan; retain distinct viewpoints |
| Mavis | [Campaign plan](../roadmap/MAVIS_CAMPAIGN_PLAN.md) |
| Martos | [Campaign plan](../roadmap/MARTOS_CAMPAIGN_PLAN.md) |
| Elias | [Campaign plan](../roadmap/ELIAS_CAMPAIGN_PLAN.md) |
| Camila | [Campaign plan](../roadmap/CAMILA_CAMPAIGN_PLAN.md) |
| Sylvanis | [Campaign plan](../roadmap/SYLVANIS_CAMPAIGN_UPDATE_PLAN.md) |
| Takeo | [Confirmed campaign plan](../roadmap/TAKEO_CAMPAIGN_PLAN.md) |

Shared prose lives in [the prose catalogue](../campaign_prose/catalog.json) and
[compiler](../campaign_prose.py). Authored dialogue and flashback integration live in
[campaign_dialogue.py](../campaign_dialogue.py) and
[campaign_flashbacks.py](../campaign_flashbacks.py). Runtime IDs, branches, save
snapshots, progress, private disclosures, and one-time effects must survive edits.

## Character, era, and voice references

- [Character references](../Mysterious%20Hearts%20-%20Character%20References.md)
- [Character appearances](../Mysterious%20Hearts%20-%20Character%20Appearances.md)
- [Worldbuilding](../Mysterious%20Hearts%20-%20Worldbuilding.md)
- [Dialogue styles](../dialogue_styles.json)
- [Historical reference sheets](../flashback_character_references.json)
- [Historical dialogue guides](../flashback_dialogue_guides.json)
- [Historical area and cast requirements](../roadmap/CAMPAIGN_FLASHBACK_AREAS_PLAN.md)

Do not use present-day profiles or later knowledge for an earlier era. A missing
historical profile is an authoring gap, not permission to invent a fallback.

## Using the Story Skills workspace

[story-skills/story.md](story-skills/story.md) is a valid editorial starter.
No chapters, characters, or knowledge records have been imported yet. A clean
starter check only establishes that the scaffold is valid.

For a requested campaign edit, identify the route and branch first. Read the
source scene and protected outcomes, then author structured scene/character/era
records and working prose for that scope. Keep branch identity and reveal timing
explicit; do not flatten mutually exclusive outcomes into one chronology. Retain
game IDs in source notes rather than renumbering runtime records to match Story
Skills' chapter IDs. Story Skills checks cover only the material represented in
its workspace. Use the installed interactive-fiction skill when modelling branches.

After editing structured story files, run the installed CLI through
`tools/story.ps1`: `reindex`, `wordcount --write`, and `check`, in that order.
Runtime integration still requires the relevant Python tests and rendered UI
checks. Editorial drafts alone do not complete MH-019 or any parent campaign.
