# Combat update — Part 1: animations and effects

Roadmap: [MH-001](ROADMAP.md#mh-001-combat-window-redesign-and-animated-attacks). Companion: [Part 2 — lore, HUD, systems and all other changes](COMBAT_WINDOW_UPDATE_PLAN.md).

**Status:** In progress — asset production; runtime integration and rendered gameplay verification pending. Split into two implementation parts on 2026-11-10 without changing approved scope, roadmap ID or release status. Part numbers organise scope; they do not prescribe delivery order.

**Scope:** Animated attack effects, ordinary/reaction/status/movement effects, master/character signatures, form and amplification visual treatments, generated-skill visual recipes, GIF production, animation sequencing, compositing, mirroring, Reduced Motion and Fast Combat presentation.

**Boundary:** Part 2 owns lore, abilities and their mechanics, balance, AI/dialogue, progression, encounter rules, HUD/layout, descriptions and save migrations for those systems. Part 1 visualises resolved events and never determines damage, costs or outcomes. Static portrait/location artwork selection and HUD arrangement belong to Part 2; animated overlays and their sequencing belong here.

**Asset production:** [Batch schedule, manifests, coverage and acceptance](roadmap/COMBAT_GIF_BATCHES.md) is the maintained source for batch progress. The evidence below is preserved from the roadmap at this split; do not infer that produced assets are integrated gameplay.

**Progress and evidence:** GIF asset production started on 2026-11-10. [Batch schedule and coverage](roadmap/COMBAT_GIF_BATCHES.md) preserves the 32-batch schedule and earlier blocked direct-GIF attempt. Batches 01–10 and 12 now contain 86 local 1536x1024 sprite sheets and 512x512 GIFs. The latest [batch 12 manifest](assets/combat/animations/batch-12/manifest.json) records eight Japanese Jujutsu/Wing Chun signatures and full prompts. `python tools/build_combat_batch_gifs.py --batch 12` passed decoding, frame-count, size, duration and loop checks: 900ms action plus 720ms review rest. Its combined preview passed decoding and timing checks. All eight source sheets and the assembled contact image were visually inspected. Exact built-in generator model identity is unconfirmed. Batch 11 remains planned. Patch-note validation passed with 462 entries and export refreshed; no unintegrated assets were labelled as a gameplay release. Runtime action-ID mapping, integration, in-game rendered review, outcome variants, compositing, accessibility and combat checks remain pending.

## Plugin task assignments

**Assigned:** 2026-11-11. Remaining Part 1 work only; existing batches and Part 2 completion retain their recorded status.

Follow the [shared plugin workflow and evidence rules](roadmap/PLUGIN_ASSIGNMENTS.md). Context Guard applies across complex/resumed work; use hook evidence or report its absence. These are future task allocations, not claims that plugins performed earlier work.

| Specific task in this plan | Assigned plugin / workflow | Required output and verification |
| --- | --- | --- |
| Stages 1–2: reconcile stable action IDs and the 32-batch catalogue | Story Skills + Writer's Loop | Check character powers, Trait/form identity and descriptions against Part 2; produce an action-to-visual brief without changing mechanics. |
| Stages 2, 4–5: author trails, impact shapes, seals and form overlays | prompt-to-asset → DESIGN:OS SVG Animation | Author/validate local SVG elements; animate only suitable vector/line-art effects with deterministic timing. Inspect rest poses, mirrored variants and exported frames before runtime conversion. |
| Stages 2–5: composite effects and export review assets | Pro Motion; prompt-to-asset for sprite sheets; Bulk BG Remove only for source cutouts | Use local rendering and the existing GIF builder/manifest contract; verify alpha, dimensions, frame counts, action/rest duration and stable action mapping. A rendered MP4 is not a Tk combat animation. |
| Stages 3 and 6: resolved-event integration and accessibility | falsegreen-skill | Review tests for invented hits, duplicate costs, interrupted sequences, stale callbacks, save/reload and Reduced Motion/Fast Combat. Run relevant combat suites and inspect the actual in-person arena. |
| Only if a later request includes combat sound cues | Pro Motion first; SFXMint for suitable explicitly free library effects | Conditional: sound is not added by this allocation. Preserve sound.py controls; record provenance and listen in context before acceptance. |

Execution evidence is pending for these assignments. Record actual commands, outputs, review findings and limitations with the existing task evidence when work runs. Other plugins are unassigned unless the task meets a conditional route in the shared workflow.

## Animation requirements

Ordinary attacks should take approximately half a second. Start with slash, blunt impact, projectile, magic, heal, and shield effects. Include weapon-specific trails, target recoil, restrained impact shake, casting glows, buff particles, block flashes, dodge movement, critical impact emphasis, and subtle status loops.

Every master move and Trait-exclusive skill needs a distinct signature beyond a shared effect recolour. Give defensive, healing, and utility skills the same attention as attacks. Master introductions may briefly dim the arena, display the move name, and highlight the attacker before the signature action. Keep status panels and narration readable.

Synchronise displayed damage, health bars, status changes, and narration with resolved impact beats. The combat engine remains authoritative: presentation must never reroll an exchange, charge resources twice, invent hits, or create terrain destruction absent from the result. Mirror all effects for opponents. Provide Reduced Motion and Fast Combat settings, with recognisable shortened signatures and no unnecessary control blocking.

## Implementation stages

1. Inventory stable action IDs and the original 88 master, 124 Trait and 15 awakened-signature designs. Reconcile changed Trait classifications and additional confirmed state cues against Part 2; preserve original coverage rather than silently dropping actions.
2. Continue the linked GIF batch schedule and visual asset review. Preserve manifests and actual production evidence; do not label unintegrated assets released.
3. Integrate a nonblocking sequence driven by resolved events into Part 2's arena surface. Implement ordinary effects and presentation settings first, with cancellation on navigation, closure and encounter completion.
4. Implement master, Trait and awakened signatures below, tracking player/opponent mirroring and miss, block, partial and resisted variants by stable ID.
5. Layer compatible amplification and active forms over recognisable base animations. Cover Shinigami activation/active/exit cues and newly confirmed ability effects. Persist stable generated-skill visual recipes with deterministic defaults for old saves, without changing their mechanics.
6. Review rendered effects, Reduced Motion, Fast Combat, sequencing, cleanup and restoration. Record implemented behaviour, actual checks and release evidence.

## Acceptance and validation

- Effects stay in the in-person arena and remain clear at normal/small sizes without obscuring Part 2's HUD, controls or narration.
- Verify attacks, multi-hit sequences, counters, misses, blocks, restraints, healing, buffs, terrain collisions and state transitions against resolved events. No invented hits, destruction, rerolls or duplicate resource costs.
- Verify player/opponent mirroring, interruption/cancellation, closing/navigation cleanup, save/load during presentation, stable visual recipes and repeated-input protection at the integration boundary.
- Inspect Reduced Motion/Fast Combat, safe flashes/shake, impact timing and fallback artwork. Run relevant combat/effect/UI smoke checks; record actual commands and results during implementation.
- Apply phone dark-theme requirements if any phone controls change. Animated presentation never moves an in-person activity into the phone.
- Follow patch-note authoring requirements for shipped player-visible changes, validate and export. Existing production evidence is not proof of runtime integration or a gameplay release.

## Animation design catalogue

The following treatments preserve the supplied move-by-move designs. They describe presentation, not additional powers or guaranteed combat outcomes.

## Overall visual direction

Keep the portraits anchored at opposite sides of the arena. Animate attacks through portrait movement, brief action silhouettes, attack trails, particles, and impact effects between them. Throws and grapples particularly benefit from silhouettes; rotating an entire portrait card would look awkward.
- Martial masters: air distortion, motion trails, dust, shock rings, and physical impact. Names such as “Thunder” or “Phantom” don’t automatically mean lightning or supernatural ghosts.
- Trait skills: distinctive supernatural materials and motion appropriate to that character.
- Timing: approximately 0.7–1.1 seconds for masters; 0.9–1.5 seconds for signature skills. Reserve longer sequences for exceptional finishers.
- Outcome accuracy: misses pass the target, blocks meet the guard, successful restraints close, and resisted restraints tear apart. Debris and craters appear only when the resolved action actually causes destruction.
- Readability: effects stay inside the arena, away from status panels and narration. Enemy effects mirror correctly.
- Accessibility: reduced-motion versions retain signature shapes without shake, rapid flashes, or large portrait movement.
The visual motifs below are presentation effects—not new powers or guaranteed combat outcomes.

## Martial master moves

### Boxing — compact impacts, rhythm, and precise footwork
| Move | Proposed animation |
| --- | --- |
| Hurricane punches | A tightening spiral of fist silhouettes becomes a rapid, finite barrage of compact impact rings. |
| Ghost step | The portrait compresses into a narrow motion smear; a floor-level dust streak traces the approach. |
| Unseen spectre | Afterimages circle the target, with successive strikes emerging from different positions before the images reunite. |
| Power-breaker | A drawn-back fist silhouette launches one thick pressure cone; the guard buckles at the contact point. |
| Phantom cadence | Two quick impacts, a deliberate pause, then an unexpected burst using differently spaced trails. |
| Thunderclap counter | The incoming trail slips past; one returning punch produces an expanding air ring at contact. |
| Iron constellation | Body and head impacts leave brief points of light connected into a constellation-like strike pattern. |
| Vanishing bell | A sharp sideways afterimage evades the attack; a hooked return lands with a bell-shaped shock ring. |

### Taekwondo — long arcs and aerial movement
| Move | Proposed animation |
| --- | --- |
| Skywheel barrage | An airborne silhouette rotates above the engagement, tracing several overlapping kick crescents. |
| Horizon step | A low horizontal streak crosses the arena and rises into a poised kicking silhouette. |
| Falling star | A silhouette climbs briefly, then a heel-shaped streak drops steeply into a concentrated ground impact. |
| Mirage wheel | Kick afterimages alternate high and low around the target, resolving into one clear finishing arc. |

### Judo — weight, balance, and rotation
| Move | Proposed animation |
| --- | --- |
| World-turner | Two contact silhouettes rotate around a shared centre before the target follows a broad throwing arc. |
| Falling mountain | The attacker settles low; the target silhouette drops heavily with a wide, grounded dust burst. |
| Zero-point reversal | The apparent throw briefly hangs at its balance point, then reverses direction into the counterthrow. |
| Iron orbit | Small circular trails repeatedly tilt the target’s balance, keeping them moving around the attacker’s centre. |

### Kyokushin — rooted force and relentless contact
| Move | Proposed animation |
| --- | --- |
| Mountain-splitter | A planted stance sends a wedge-shaped pressure trail into the guard, splitting the impact graphic vertically. |
| Adamant advance | The portrait advances in firm increments while incoming impacts visibly strike its braced silhouette. |
| Hundred-beat barrage | Alternating body impacts and low kick sweeps build a dense, percussive pattern. |
| Thunder heel | A high heel silhouette falls in a nearly vertical line, ending in a compact circular shockwave. |

### MMA — transitions between combat phases
| Move | Proposed animation |
| --- | --- |
| Apex chain | Punch trails lead into a level change, a takedown arc, and a final ground-control silhouette. |
| Predator switch | An attack begins on one line, then abruptly changes height and direction as the opponent defends. |
| Gravity crash | A low entry pulls both silhouettes toward a single heavy landing point. |
| Total control | Overlapping positional silhouettes transition around the target, with pressure markers shifting between contested holds. |

### Muay Thai — elbows, knees, and close-range power
| Move | Proposed animation |
| --- | --- |
| Eight-limbed tempest | Distinct punch lines, elbow wedges, knee bursts, and kick arcs alternate in a tight sequence. |
| Meteor knee | A rising knee silhouette surges diagonally forward behind a dense, tapered air trail. |
| Titan clinch | Paired contact brackets close around the upper silhouette; short pulses show contested posture pressure. |
| Thunder pillar | A broad roundhouse trail strikes the guard like a horizontal column of compressed air. |

### Streetfighting — irregular and abrasive
| Move | Proposed animation |
| --- | --- |
| Riot engine | Uneven punch trails and abrupt lunges build into an untidy burst of heavy impacts. |
| Backstreet phantom | Jagged footwork afterimages jump between unexpected approach angles, connected by visible movement trails. |
| Concrete verdict | One blunt straight-punch silhouette lands with a square-edged compression burst and appropriate surface debris. |
| Chaos rhythm | Trails stall abruptly, then restart at different speeds and heights around the target’s defence. |

### Sanda — striking flowing into throws
| Move | Proposed animation |
| --- | --- |
| Storm bridge | A long strike trail bridges the gap, curls into a grip, then becomes a throwing arc. |
| Sky-catch reversal | An incoming aerial silhouette is caught; its existing trajectory bends into a forceful downward throw. |
| Horizon breaker | A side-kick silhouette drives a broad horizontal pressure front into the guard. |
| Cyclone sweep | A low circular trail gathers around the target’s feet and carries their silhouette into a tumbling fall. |

### Jeet Kune Do — minimal motion and interception
| Move | Proposed animation |
| --- | --- |
| Stillpoint intercept | A tiny contact point appears directly on the incoming attack line before either trail fully extends. |
| Vanishing line | One clean diagonal afterimage exits the attack corridor, leaving the incoming strike to pass through. |
| One-beat thunder | Almost no windup: a short line snaps outward and becomes a disproportionately strong contact ring. |
| Empty rhythm | Sparse attack trails alternate with conspicuous gaps, landing between the opponent’s defensive movements. |

### Military CQC — economical and controlled
| Move | Proposed animation |
| --- | --- |
| Breach sequence | A narrow entry streak leads into a disruption impact and sharply defined positional-control silhouettes. |
| Lockdown engine | Contact markers transfer rapidly between holds, tightening only when the corresponding control succeeds. |
| Silent vector | A subdued, low trail crosses the gap with minimal particles and a crisp arrival silhouette. |
| Titan restraint | Heavy contact brackets brace around the target while opposing tension lines show the struggle. |

### Kickboxing — alternating hands and feet
| Move | Proposed animation |
| --- | --- |
| Tempest circuit | Straight punch trails and broad kick crescents form a repeating circuit around the engagement. |
| Sonic crescent | A thin kick arc arrives first, followed a moment later by its wider air-distortion wake. |
| Iron comet | A concentrated punch impact leads immediately into a heavier driving kick and elongated shock cone. |
| Phantom relay | Afterimages alternate between close punching range and longer kicking range, passing the attack between positions. |

### Silat — low angles and deceptive direction changes
| Move | Proposed animation |
| --- | --- |
| Serpent lattice | Curving contact trails weave around the guard into a shifting lattice of restricted angles. |
| Phantom crescent | A faint upper afterimage distracts while a sharp low crescent sweeps beneath the target. |
| Falling canopy | The attacker silhouette dips under a strike, rises inside the guard, and folds into a close throw. |
| Mirror snare | A mirrored pair of trails suggests one direction, then the actual reversal snaps along the other. |

### Aikido — continuous redirection
| Move | Proposed animation |
| --- | --- |
| Still-water reversal | The incoming line becomes a smooth circular ripple and curves back through a close-range reversal. |
| World-axis turn | A clear pivot point anchors a rapid rotation, sending the target through a wide throwing arc. |
| Orbit of silence | Thin, uninterrupted circular trails show continuous balance pressure without explosive impact flashes. |
| Returning mountain | The incoming rush compresses against a rooted silhouette, then rolls back into a heavy grounded throw. |

### Taido — unusual body axes
| Move | Proposed animation |
| --- | --- |
| Axis phantom | A silhouette rotates between upright, tilted, and inverted orientations while leaving the expected attack line. |
| Sky spiral | A rising corkscrew of kick trails wraps around an airborne silhouette. |
| Inverted comet | An inverted silhouette delivers a steep diagonal kick, with its trail clearly following the changed body axis. |
| Nine-angle mirage | Afterimages occupy changing heights and angles; only resolved strikes receive contact effects. |

### Lethwei — dense, forceful close exchanges
| Move | Proposed animation |
| --- | --- |
| Nine-limbed thunder | Tight elbow, knee, fist, kick, and head-strike silhouettes combine into a compact collision sequence. |
| Iron monsoon | Repeated heavy impacts crowd the engagement while visible returning hits preserve the sense of risk. |
| Falling bell | A short close-range collision produces a heavy bell-shaped compression wave and pronounced recovery beat. |
| Unbroken advance | The attacker keeps stepping forward through visible impact jolts, maintaining pressure without suggesting invulnerability. |

### Japanese Jujutsu — linked grips and positional traps
| Move | Proposed animation |
| --- | --- |
| Thousand-link bind | A chain of contact markers transfers rapidly between holds around paired silhouettes. |
| Earthfall reversal | The incoming commitment tips past its balance point and drops into a hard counterthrow. |
| Iron labyrinth | Angular positional paths repeatedly close around the opponent’s attempted escape routes. |
| Silent avalanche | A subdued entry flows directly into a sudden throw and a compact restraint finish. |

### Wing Chun — centre-line speed
| Move | Proposed animation |
| --- | --- |
| Thousand-point rain | Closely packed straight punches form a narrow stream of small, rapid contact bursts. |
| Centre-line collapse | Parallel guard lines compress inward as a concentrated straight attack contests the central opening. |
| Mirror hands | Paired hand trails deflect incoming lines outward while short returning strikes travel through the middle. |
| Inch thunder | A tiny gap separates fist and target; a minimal movement creates a large local compression ring. |

### Shinokami martial arts — restrained precision
| Move | Proposed animation |
| --- | --- |
| Eclipse intercept | The incoming and intercepting trails overlap briefly, forming an eclipse-shaped contact ring. |
| Null cadence | The opponent’s rhythmic motion trails are interrupted by deliberately mistimed physical pressure beats. |
| Shinigami crossing | Two sharp movement lines cross; the attacker emerges at a new angle beyond the expected strike. |
| Iron eclipse | Small interception rings alternate with dense returning impacts, using very little excess movement. |

### Krav Maga — abrupt responses and escape
| Move | Proposed animation |
| --- | --- |
| Zero-window response | Defensive contact and the returning strike occur almost together in one abrupt visual beat. |
| Breakout surge | Close pressure markers separate as a forceful movement trail pushes toward the available escape route. |
| Iron corridor | Protective forearm silhouettes frame a narrow advancing route punctuated by short counterstrikes. |
| Last-light reversal | A narrowly deflected attack skims past before both silhouettes sharply exchange positional advantage. |

### Systema — relaxed movement, sudden force
| Move | Proposed animation |
| --- | --- |
| Quiet thunder | A relaxed silhouette makes a small movement; the impact expands unexpectedly after contact. |
| Flowing void | Soft, continuous body afterimages bend around incoming trajectories, with hits shown whenever evasion fails. |
| Pulse cascade | Compact circular impacts travel across the target in an uneven, accelerating rhythm. |
| Unbroken current | One continuous curved trail connects evasion, repositioning, and the returning strike. |

### Kudo — compact mixed combat
| Move | Proposed animation |
| --- | --- |
| Tempest clinch | Short impact wedges fold inward into gripping silhouettes, followed by a quick throwing entry. |
| Meteor wheel | Secured contact becomes a tight rotating arc ending in a heavy diagonal landing. |
| Crashing tide | Repeated broad pressure waves alternate with close-grip tension, suggesting sustained mixed offence. |
| Seamless storm | A single flowing trail changes from strike lines to clinch circles to a final throwing arc. |

## Trait-exclusive skills

Each character should have a recognisable visual language even before their move name appears.

### Garrett Han — golden flame, dragon-like curves, precise gold sight lines
| Skill | Proposed animation |
| --- | --- |
| Dragon Kick | Golden flame erupts behind a flying kick, forming a dragon-head impression at the explosive impact. |
| Sunbreaker Fist | Gold light compresses around a fist, then punches forward as a short, intensely focused flame core. |
| Golden Dragon Spiral | Two rising flame coils follow the rotating kicks, lifting debris only where the impacts break terrain. |
| Solar Wake | A blazing movement streak crosses the arena, leaving a low burning wake behind the finishing impact. |
| True-Sight Reversal | A fine gold line identifies the incoming trajectory; Garrett slips aside and strikes along a newly revealed opening. |
| Dragon’s Descent | A rising flame column curls overhead before a dragon-shaped plunge ends in a radial golden blast. |
| Phoenix Wheel | A broad, feather-like wheel of fire sweeps through the engagement and carries displaced debris outward. |
| Dawnfall Breaker | A tiny gold targeting glint precedes a narrow penetrating strike; flame blooms outward after contact. |

### Rei Takamura — emerald electricity, pale wind ribbons, continuous momentum
| Skill | Proposed animation |
| --- | --- |
| Descending Tempest | A green lightning trail rises, then an axe-kick silhouette drops through a funnel of wind into impact. |
| Flowing Stream | Curved wind ribbons catch the incoming effect and redirect it toward its source, partially or fully according to resolution. |
| Thousand Sparks | Green movement trails loop faster around the arena, condense into a spinning kick, and release their stored momentum. |
| Emerald Rift | A thin green wind crescent tears across the arena, leaving a brief split-air distortion behind it. |
| Cyclone Crash | A throwing silhouette winds the opponent into a compact cyclone before driving them into the resolved collision surface. |
| Storm Rail | Two narrow green rails frame an almost instantaneous dash, ending in one concentrated electrical impact. |
| Tempest Mantle | Wind ribbons orbit the guard, catching incoming pressure and tightening into a visible retained-momentum accent. |
| Eye of the Tempest | A calm centre forms around Rei while wind, sparks, and available debris circulate, then sweep outward. |

### Ivan Yeun — clearly separated elemental channels

Red lightning should feel heavy and explosive; blue lightning should feel thin, fast, and precise.
| Skill | Proposed animation |
| --- | --- |
| Furnace Knee | Fire gathers tightly around a knee silhouette, then vents downward and outward through the impact. |
| Whiteout Crash | Frost plates build over a charging shoulder; contact bursts into angular ice shards and a cold mist wake. |
| Gale Cutter | A nearly transparent blade of wind crosses the arena with sharp edge glints and displaced dust. |
| Crimson Break | Thick red lightning branches converge at contact, then erupt outward in a heavy knockback burst. |
| Azure Blink | A hair-thin blue trail traces the actual movement route before a small, precise blue contact flash. |
| Flashfreeze Snare | Frost races across the ground and grows into ice teeth around the target’s movement path. |
| Thunderhead Drop | An upward gust lifts the silhouette; red lightning gathers below it before the descending collision. |
| Winterstorm Ring | Ice shards orbit inside a horizontal wind ring, then scatter across the affected ground. |
| Arc Split | A blue arc carries Ivan around the guard; a distinctly heavier red burst marks the finishing blow. |
| Fivefold Ruin | Fire, wind, ice, blue movement, and red impact appear in a readable sequence, culminating in a combined collision. |

### Sylvanis — dense black-violet constructs, sharp sight lines, deliberate geometry
| Skill | Proposed animation |
| --- | --- |
| Nightfall Hammer | A huge shadow fist grows behind the physical strike and overtakes it at contact. |
| Midnight Coil | Thick shadow bands close in layered spirals, tightening or breaking according to the restraint contest. |
| Umbral Rush | A low shadow veil conceals a visible movement streak; a reinforced silhouette emerges at the impact. |
| True-Sight Intercept | One pale violet prediction line finds the attack’s opening; a narrow counter cuts directly through it. |
| Polymath Rupture | Several schematic strike patterns appear briefly, then one changes rhythm and breaks through the observed weak opening. |
| Eclipse Convergence | Distinct shadow constructs attack from separate directions, visually narrowing the target’s available space. |
| Black Sun Collapse | A dense, dark orb with a violet rim descends and flattens into a crushing radial impact. |
| Shadow Requiem | Shadow barriers cut across predicted escape routes before a rapid, precisely spaced finishing sequence. |

### Charles Han — white flame with cool blue edges and tiger-shaped accents

The white belongs to the flame artwork, not the interface panels.
| Skill | Proposed animation |
| --- | --- |
| White Tiger Pounce | A white-flame tiger outline accompanies a short pouncing arc and bursts apart at contact. |
| Fangbreaker Fist | Two narrow fang-shaped flame wedges close around the punch’s concentrated impact point. |
| Tiger Wheel | White claw-like arcs rotate around the engagement before sweeping outward. |
| White-Flame Roar | A tiger-jaw impression opens within a short, broad forward flame burst. |
| Twin-Fang Return | A defensive flame curl becomes two sharp returning fang-shaped impacts on different guard lines. |
| Snowfire Mantle | Close-fitting white flame streams backward during the guarded advance, then surges through the returning strike. |

### Takeo Mishima — graphite armour, mechanical assembly, amber engine light
| Skill | Proposed animation |
| --- | --- |
| Siege Fist | Small metallic segments assemble into a reinforced fist silhouette before a broad battering impact. |
| Bunker Rush | Armour plates lock across a charging silhouette, leaving a heavy dust wake and displaced fragments. |
| Adaptive Bulwark | Hexagonal plates slide toward the incoming contact point and visibly flex, hold, or fracture. |
| Monolith Blade | A segmented arm blade extends outward, locks into shape, and sweeps through a single heavy cutting arc. |
| Engine Overdrive | Amber seams brighten in sequence; a dense acceleration trail ends in a piston-like impact. |
| Iron Meteor | Armour segments compress around an airborne silhouette before a heavy descent and low radial debris burst. |

### The Crow — monochrome analysis, chess-like composition, precise physical attacks

Chess imagery should be a subtle visual metaphor, not summoned pieces.
| Skill | Proposed animation |
| --- | --- |
| Checkmate Sequence | Faint route lines close off escape options as successive physical impacts guide the target toward the finishing position. |
| Perfect Counter | Several faint possible trajectories disappear, leaving one clean returning line and a precise contact flash. |
| Black Rook Breach | Rectangular structural outlines identify a weak section; a straight impact drives through its centre. |
| Hundred-Style Sequence | Distinct striking and grappling silhouettes replace one another rapidly, each with a different rhythm and range. |
| Queen’s Gambit | An inviting opening is briefly outlined; the opponent’s commitment triggers a returning sequence around it. |
| King in Motion | Predicted attack lanes appear faintly while the movement silhouette follows a narrow safe route between them. |

### Martos Cabrera — deep crimson pressure, heavy mass, rough impacts
| Skill | Proposed animation |
| --- | --- |
| Juggernaut Charge | A broad rushing silhouette pushes a bow wave of dust and actual broken obstacles ahead of it. |
| Ruin Hammer | A massive downward strike produces a compressed impact disc followed by outward-running ground fractures. |
| Colossus Grip | Large gripping silhouettes close around the target, with visible tension before the resolved crush or throw. |
| Aftershock Stamp | A heel stamp sends successive low shock rings through the ground, lifting nearby loose rubble. |
| Redline Surge | Crimson pulses accelerate around the portrait while oversized, increasingly rough strike trails batter the target. |
| Siege Reversal | Incoming force visibly compresses his braced stance, then releases through a thick returning impact cone. |

### Elias Braun — orange heat, ember trails, dance-like rhythm
| Skill | Proposed animation |
| --- | --- |
| Heatstep Engine | Alternating footfall sparks grow into glowing trails and heat shimmer as movement accelerates. |
| Ignition Carousel | A rotating kick pulls accumulated embers into a wide blazing carousel arc. |
| Cinder Rail | A narrow heated movement line brightens into a straight rushing strike and a fiery contact burst. |
| Ember Encore | Successive kick arcs increase in ember density and intensity as heat builds through the sequence. |
| Scorched Stage | Crossing movement trails remain as glowing ground paths, clearly marking the affected routes. |
| Curtainfall Kick | Heat trails rise behind the airborne silhouette, then fall like a fiery curtain around the descending kick. |

### Mavis Kuro — charcoal vapour with silver edges
| Skill | Proposed animation |
| --- | --- |
| Black-Vapour Slip | Her silhouette breaks into wisps around the incoming attack and reforms visibly off its line. |
| Hollow Counter | The struck silhouette caves into smoke; a new silhouette reforms beside it and delivers the return. |
| Veilbreaker Palm | A hand condenses from mist immediately before contact, producing a dense palm-shaped pressure burst. |
| Shrouded Sweep | Low vapour obscures the feet while a silver-edged sweep cuts through the target’s footing. |
| Smokebreak Traverse | Mist threads through a real opening in broken cover and gathers into her silhouette beyond it. |
| Midnight Curtain | A broad sheet of dark vapour rolls across the arena as her position changes behind it. |

### Camila Lopez — teal analytical lines, structural diagrams, controlled movement
| Skill | Proposed animation |
| --- | --- |
| Faultline Palm | Fine teal lines trace the barrier’s weakness before a palm impact breaks along the identified structure. |
| Pattern Lock | Ghosted repetitions of an observed movement overlap until one recurring opening receives a clear timing marker. |
| Checkmate Turn | A curved trajectory diagram appears around the incoming entry, then becomes the actual reversal and throw. |
| Tempo Theft | A small timing pulse marks the opponent’s weight shift; Camila’s movement cuts into that exact beat. |
| Glassboard Feint | A translucent outlined opening draws the attack, then the diagram pivots into the returning strike path. |
| Cascade Reversal | Linked grip markers and directional arrows flow through successive turns into one heavy throwing finish. |

### Samantha Kim — glossy crimson forms with dark red shadows

Keep blood effects stylised and externally controlled.
| Skill | Proposed animation |
| --- | --- |
| Crimson Lance | Crimson droplets gather into a long rigid lance, which fires with a thin trailing filament. |
| Red-Thread Snare | Fine red strands travel around the target externally, tighten, and pull along the resolved restraint direction. |
| Scarlet Crescent | A liquid ribbon hardens into a broad crescent as it sweeps across the engagement. |
| Bloodbloom Burst | A compact blood mass unfolds into striking petal-like forms that hit from several short-range angles. |
| Coagulated Aegis | Overlapping dark-crimson plates assemble into a shield and visibly crack under sufficient incoming force. |
| Returning Fang | A hooked blood projectile crosses the target, curves around, and returns along a visibly different route. |

### Tyler Harding — compressed impact rings and visible force reserves
| Skill | Proposed animation |
| --- | --- |
| Debt Collector | Stored rings around the attacking arm collapse into one punch, then expand violently at the target. |
| Rebound Crash | An incoming impact compresses a circular reserve graphic; its energy immediately reverses through the returning punch. |
| Breakwater Guard | A broad impact washes over a braced guard while part of the shockwave coils into stored rings. |
| Avalanche Hook | Several dense reserve bands unwind through a sweeping hook and become a broad displacement wave. |
| Redline Barrage | Separate reserve segments discharge one by one, each feeding a distinct punch impact. |
| Aftershock Uppercut | Compressed rings launch upward with the punch; a second impact marks the target’s resolved landing. |

### Minsu Park — silver-blue speed trails and crisp afterimages
| Skill | Proposed animation |
| --- | --- |
| Vanishing Kick | A thin movement streak reaches the opponent before the trailing kick afterimage catches up. |
| Hundred-Frame Step | A fan of closely spaced afterimages bends around the incoming trajectory and resolves at the new position. |
| Blink Chain | Kick traces alternate high and low in sharply separated beats, preserving the number of resolved hits. |
| Racing Intercept | Two movement lines cross at a clearly marked interception point where the stopping kick lands. |
| Comet Run | A lengthening speed trail builds behind the run-up, then funnels into the driving kick. |
| Afterimage Relay | Short movement bursts pass around the guard in sequence before one solid silhouette delivers the final kick. |

### Valentina Yeun — blade-like grey-green wind and severe pressure distortion
| Skill | Proposed animation |
| --- | --- |
| Guillotine Gale | A tall, thin cutting gust drops across the target like an angled guillotine blade. |
| Cyclone Vault | A rising corkscrew gust lifts the silhouette before unfurling around the returning acrobatic kick. |
| Pressure Coffin | Opposing translucent wind planes compress around the target, distorting the background inside the contested zone. |
| Horizon Sever | A long, low wind crescent cuts across the arena, leaving a sharp horizontal distortion seam. |
| Gale Reversal | An opposing gust bends the incoming trajectory aside, then opens into the returning attack. |
| Seventh Squall | Successive gusts strike from changing directions, with debris following each resolved displacement. |

### Emily Fields — precise magenta weak-point marks and fracture patterns
| Skill | Proposed animation |
| --- | --- |
| Fracture Point | A small contact pulse leaves a distinctive diamond-shaped weak-point marker on the chosen target. |
| Shatter Touch | A precise touch activates the existing marker and sends sharp fractures through the affected surface. |
| Faultline Rush | A narrow rushing trail converges on a newly highlighted opening, ending in a tightly focused impact. |
| Painless Advance | A steady outline holds around her advancing portrait while damage effects and health loss remain visible. |
| Chain Fracture | Successive marks appear and rupture in sequence, forming a growing chain of local fractures. |
| Critical Verdict | The established marker contracts to a point, then bursts into a large radial fracture pattern as it is consumed. |

### Alyssa — flowing violet-black ribbons and softer-edged shadow constructs

This distinguishes her from Sylvanis’s dense, geometric shadows.
| Skill | Proposed animation |
| --- | --- |
| Dusk Hammer | Flowing shadow gathers into a rounded striking mass that follows the physical blow into contact. |
| Black-Ribbon Bind | Long violet-edged ribbons weave around the target and pull taut along the restraint direction. |
| Shade Mantle | Overlapping translucent shadow layers meet the incoming attack, peeling away when damaged or broken. |
| Twilight Step | A curtain-like shadow fold conceals the movement trail before opening around the returning strike. |
| Midnight Sweep | A broad, low shadow ribbon rolls across the ground, carrying displaced loose objects sideways. |
| Falling Shade | Hanging shadow strands gather into a heavy overhead form and drop onto the selected area. |

### Edward Fox — amber sensory rings, vibration traces, understated physical force
| Skill | Proposed animation |
| --- | --- |
| Blindside Verdict | An amber sensory ripple reveals the concealed attack’s direction before a sharply angled returning strike. |
| Pulse Hunter | Small heartbeat and displacement pulses briefly mark the detected route through visual obstruction. |
| Zero-Noise Rush | Ground-level sensory traces identify a quiet route; a subdued movement silhouette follows it into close range. |
| Shockline Read | Vibration ripples travel along the ground and air before the incoming attack; Fox moves off their convergence. |
| Eightfold Intercept | Several distinct sensory traces converge on one interception point, followed by a precise physical impact. |
| Blackhaven Breaker | Contact sends amber vibration lines through a barrier, revealing a weak structure before the breaching strike. |

### Jeremy Gordon — ivory biological armour, dark tissue, purposeful growth
| Skill | Proposed animation |
| --- | --- |
| Living Cannon | Ribbed biological segments grow into a firing channel, brace, and discharge a heavy concentrated round. |
| Hydra Burst | Several smaller firing channels unfold in different directions and deliver a clearly finite sequence of shots. |
| Adaptive Breach | The firing component visibly changes shape to suit the obstacle before releasing its specialised impact round. |
| Bone Bulwark | Interlocking ivory plates grow across the defensive line and fracture individually under incoming force. |
| Regrowth Reload | Spent components retract or shed; fresh tissue and armour assemble into a restored firing mechanism. |
| Siege Lance | A long rifle-like growth locks into alignment and fires one narrow, forceful shot through the selected line. |

## Awakened signatures and revised Trait assignments

The original catalogue contains these 15 signatures, previously grouped as lacking Traits. The confirmed lore revision assigns Neo and Thirteen to Shinigami Protocol, Daniel to War God and April to Polymath; Keisuke's Trait status is unchanged. Preserve these individual animations and stable action IDs while reconciling classification. This rename does not add elemental powers or fully specify the Shinigami trump-card state effects.
| Character / skill | Proposed animation |
| --- | --- |
| Neo — Shinigami Vector | A precise diagonal movement streak crosses the engagement and ends in one compact CQC impact. |
| Neo — Breakpoint Drive | A braced close strike produces a dense pressure cone and debris from the actual collision surface. |
| Neo — Adaptive Intercept | Several faint response silhouettes collapse into the chosen learned counter as the incoming attack changes. |
| Daniel — Perfect Transition | A striking silhouette drops seamlessly into a takedown, carrying the target into the resolved collision. |
| Daniel — Concrete Driver | A heavy close-contact silhouette drives force into the landing surface with a broad dust burst. |
| Daniel — Instinctive Reversal | Contact pressure bends one way, abruptly reverses, and carries the counter along a short curved trail. |
| April — Accelerated Calculation | Observed attack trajectories briefly separate into clear alternatives before the selected defensive line brightens. |
| April — Pattern Map | Repeated movement traces overlap into a compact map, highlighting probable routes without implying certainty. |
| April — Predictive Escape | A narrowing gap receives a subtle outline; her movement trail passes through before the pressure closes. |
| Thirteen — Suppression Rush | A tight approach streak leads into successive short impacts that maintain continuous positional pressure. |
| Thirteen — Iron Reversal | A braced contact silhouette absorbs the collision’s direction and folds it into a powerful return. |
| Thirteen — Vanishing Entry | A sudden lateral burst crosses the expected attack line and resolves into a close striking stance. |
| Keisuke — Crushing Body Blow | A dense body-level impact compresses the target silhouette before any resolved backward collision. |
| Keisuke — Groundsplitter Throw | A secure grip leads into a strong throwing arc, with ground fractures appearing at the actual landing. |
| Keisuke — Relentless Storm | Body punches, kicks, and control silhouettes alternate in a sustained sequence with distinct defensive-response beats. |

## How amplification and forms should affect these animations

A martial master’s movement pattern should remain recognisable when amplified. For example, Hurricane punches with Golden Fire keeps its spiralling punch barrage but gains flame trails; True Sight adds mana-flow perception and efficient energy-channel cues with precognitive opening markers; visible speed/strength amplification and resource changes must match resolution. This preserves both the move’s identity and the character’s Trait.

Advanced forms should intensify the same signature through richer materials, stronger trails, or additional background accents. They shouldn’t make the base skill look unfinished.

For generated custom skills, assign a stable visual recipe when the skill is accepted: casting cue, movement path, effect material, impact shape, and lingering effect. Save that recipe with the skill so its appearance remains consistent.
