# Expanded combat Traits and abilities

Parent: [MH-001](../ROADMAP.md#mh-001-combat-window-redesign-and-animated-attacks) · [Part 2 — lore, HUD and systems](../COMBAT_WINDOW_UPDATE_PLAN.md)

Created 2026-11-10. Status: authored design reference; runtime integration and gameplay verification pending. Established powers and explicit user revisions are distinguished from proposed mechanics. The Shinigami activation/duration/cost/power specification and War God mechanics were confirmed on 2026-11-10. The same confirmation revises True Sight, Analysis, Conduit and Deathwind as detailed below; these revisions supersede older narrower definitions.

Companion: [character identity, reputation and combat presence](COMBAT_CHARACTER_LORE.md), covering the Crazed Demon, the unidentified Crow, the Human Siege Engine and roster-specific integration.

## Definition and presentation rules

A **Trait** is an individual Awakened capability. **Awakened physical development** supports strength, reactions and endurance without automatically providing a rare Trait. A **technique** is a learned application; a **signature** is a character-specific technique, not necessarily another power. **Amplification** applies an existing ability to a compatible action. A **form or trump-card state** changes ability operation under defined conditions. Identify equipment and cybernetic systems separately.

Power, refinement, martial skill, perception and judgement remain distinct. Recognising the correct response does not supply the speed, range or leverage to execute it. A shared Trait name does not imply identical mastery. Tier measures overall effectiveness, not a uniform multiplier on every attribute.

Each entry provides an expanded description, combat applications and boundaries. Existing signatures illustrate applications rather than automatic outcomes. Exact ranges, costs, durations and damage remain per-action implementation data unless explicitly established. New speculative mechanics are labelled **Proposed**; no generic resource rule creates an unsupported weakness for Takeo or another character.

Use these descriptions in identity sheets, learned-ability detail panels, move previews and generation context. Show a short summary first and expandable details second. Preserve discovery and privacy boundaries: author-facing knowledge must not leak through ordinary dialogue or undiscovered opponent previews. Combat remains in person; any phone presentation must use existing dark styles and embedded dialogs.

## Shared perceptual and analytical powers

### True Sight — Garrett, Sylvanis and Charles

**Confirmed definition:** True Sight perceives the world through pure mana and magical flow. Its primary function is near-perfect efficiency in Awakened application, rather than merely heightened immediate combat observation. Reading and applying that flow produces precognition as a side effect, heightened combat perception and reflexes, significantly enhanced application of speed and strength through Awakened energy, and lower mana drainage.

**Expression:** The user perceives how mana moves and channels their own Awakened energy with exceptionally little waste. Precognitive information informs response timing, while efficient energy application materially improves speed and strength. It must therefore affect resource use and physical amplification as well as targeting or prediction. Garrett combines it with Golden Flame and Fa Jin, Sylvanis with Polymath and Umbrakinesis, and Charles with White Flame Tiger and refined martial technique. Charles possessing True Sight is now explicit confirmed lore.

**Boundaries and implementation:** Preserve actual precognition; do not reduce it to ordinary body-language analysis. Near-perfect efficiency and lower drainage do not mean infinite mana or zero-cost actions. Precognitive horizon, mana-flow detection range, amplification values, concealment interactions and cost-reduction stacking need design and testing. Perception/reflex improvements do not automatically guarantee every evasion or physical outcome, and the Trait does not establish mind-reading or identity proof. Source: explicit user revision, superseding earlier profile/catalogue descriptions.

### Polymath — Sylvanis, The Crow and April

**Definition:** Exceptional comprehension, learning and synthesis of available information. Polymath recognises relationships between observed techniques, recurring choices and changing circumstances, enabling an unusually effective understanding of an opponent or problem.

**Expression by user:** Sylvanis integrates analysis with True Sight, martial mastery and shadows. The Crow translates it through his extensive learned repertoire and formidable Awakened body. April uses it for reasoning, pattern recognition and tactical planning; she does not gain their physical ability or martial experience.

**Boundaries:** Requires evidence; it cannot reveal unseen plans, read minds or automatically solve an investigation. Understanding a technique does not grant its supernatural source or instant physical mastery. April remains a specialist. **Proposed implementation:** develop pattern knowledge through meaningful observations, separating inferred openings from guaranteed success. Sources: profiles/catalogue, existing cognition lore and explicit April revision.

### Analysis — Camila

**Confirmed definition:** Analysis allows the viewer to see and perceive minuscule changes and microscopic details, and visualise branching paths. Camila combines this exceptional observational resolution with accelerated recognition of patterns, trajectories and structural relationships to evaluate how an exchange or system might develop.

**Expression:** Subtle changes and tiny visible details inform possible branches of action and response. Pattern Lock develops a reading of repeated behaviour; Tempo Theft acts on a minute timing change; Cascade Reversal executes a selected branch through physical technique. Branch visualisation must be represented as a meaningful analytical capability, not merely decorative lines.

**Boundaries:** Branches represent possible developments rather than guaranteed outcomes. Microscopic perception does not itself establish unlimited range, sight through every obstruction or knowledge of unseen facts. An identified response still needs a physically feasible action. Exact observation range, branch resolution and gameplay representation remain design work. Distinguish Analysis's fine-detail observation/branch visualisation from True Sight's mana-flow perception and precognition and Polymath's comprehension/synthesis. Source: explicit user revision plus existing Four Aces lore.

## Apex and exceptional combatants

### Sylvanis — Umbrakinesis and integrated mastery

**Description:** Sylvanis shapes shadows into physical offensive and defensive constructs, combining their reach and geometry with True Sight and Polymath. He can read an opening, analyse likely responses and place pressure where an opponent has limited room to answer.

**Applications:** Striking masses, restraints, barriers and multi-directional pressure. Nightfall Hammer concentrates impact; Midnight Coil contests restraint; Eclipse Convergence narrows available routes. Constructs interact with actual targets and resolved positions rather than guaranteeing contact through visual spectacle.

**Peak:** Second-stage Transcendence supports corrosive, burning, explosive or piercing shadows even in absolute light. These advanced properties are not shared automatically by every shadow user. Existing Path metadata names his trump card Black-eyed Shadow Dominion; reconcile naming and activation rather than duplicating the form.

**Limits:** S+ overall, not omniscient or invulnerable. Separate baseline constructs from active advanced properties and record expenditure per action. Bright surroundings must not disable the explicitly light-independent advanced state. Sources: profiles, catalogue, Path and approved hierarchy.

### Takeo Mishima — Nanoengine

**Description:** Takeo generates and controls nanomachines within his body. They reinforce muscle, bone, joints, skin and nervous tissue, making him a heavily protected adaptive weapons platform. Weapons emerge and reshape internally; removing a carried weapon does not disarm him.

**Applications:** Extreme reinforced strikes, destructive charges, adaptive armour and transformed striking/cutting surfaces, with ranged weapon capability. His dossier establishes breaching reinforced tank hulls and fortifications and surviving conditions lethal to most Awakened. Siege Fist, Adaptive Bulwark and Monolith Blade apply the same internal system differently.

**Limits:** Exceptional protection and structural recovery are not infinite regeneration. Conventional firearms are largely ineffective; specialised ammunition or traps offer no guaranteed answer. Do not invent convenient overheating, fuel exhaustion, hacking access or short cooldown weaknesses. Preserve military tactical competence. S-tier threat; Richter's cybernetics do not make him comparable. Sources: `takeo.py`, profiles and catalogue.

### The Crow — Polymath in martial combat

**Description:** The Crow uses Polymath to direct a vast learned martial repertoire. He identifies patterns, selects compatible techniques and adjusts sequences to actual responses. Analysis is backed by the physical ability and experience needed to exploit it.

**Applications:** Perfect Counter selects a feasible returning action; Hundred-Style Sequence changes rhythm and method; Checkmate Sequence constrains options through successive physical exchanges. Chess imagery is a metaphor, not summoned pieces or control of another person's decisions.

**Limits:** Requires information and an executable response. Correct analysis does not make impossible actions possible. Preserve S-tier effectiveness without hidden guaranteed wins. Syndicate authority is not why his attacks succeed. Sources: shared Polymath definition, profiles and catalogue.

### Ivan Yeun — Conduit

**Confirmed definition:** Conduit channels elements and physically amplifies Ivan's stats when he uses them. Each channel has a specific additional effect; they are not interchangeable elemental damage colours.

| Channel | Confirmed effect |
| --- | --- |
| Red lightning | Enhances attack power. |
| Blue lightning | Dramatically enhances speed. |
| Wind | Deals soul damage. |
| Fire | Generates strength. |
| Ice | Enhances reflexes and reaction time. |

**Applications:** Retain elemental attacks and the existing physical amplification while expressing these channel-specific benefits. Red lightning's attack-power increase and fire's strength increase require distinct implementation definitions. Blue lightning movement speed differs from ice's response timing. Wind's soul damage requires an explicit damage category and interaction rules, rather than ordinary physical damage with a renamed effect. Existing fire, wind, ice and lightning signatures remain eligible applications subject to action mapping and cost review.

**Tranquility — ice-derived bonus:** Grants instant reaction speeds and perception and a constant flow state. Preserve that stated capability rather than substituting a small reaction-stat buff. Distinguish reaction/perception latency from the travel time and physical reach of a chosen action; an instant reaction does not automatically place Ivan at a distant target. Activation/access conditions, duration, resource use and interactions with other states require specification. Do not assume the bonus expires between exchanges or invent a duration from its name.

**Misanthropy — wind-derived bonus:** Allows Ivan to suffer more damage and remain standing. This is increased capacity to keep functioning under damage, not merely a cosmetic refusal to fall. It does not establish regeneration, damage cancellation or immunity to all incapacitation. Health/functional thresholds, accumulated damage, active/exit behaviour and costs require design. Valentina also has access through Deathwind's origin as an extension of Ivan's wind power.

**Full Conduit State:** Retain the established five-minute duration and once-per-twenty-four-hours availability across restarts and saves. Do not automatically apply this timer to all ordinary channel use, Tranquility or Misanthropy without a separate specification. Channel combinations, switching costs, stat stacking, soul-damage defences and bonus interactions remain to be designed and tested.

**Balance:** A+ baseline is unchanged. No automatic soul destruction, possession, unbounded weather or blanket defence bypass is established by soul damage. The detailed soul-damage model must preserve its distinct lore effect. Source: explicit user revision plus established Conduit state lore.

### Charles Han — White Flame Tiger and True Sight

**Description:** Charles possesses True Sight alongside White Flame Tiger. Mana-flow perception, precognition and near-perfect Awakened efficiency reinforce his speed/strength application and lower mana drainage. A Transcendent white-flame manifestation reinforces highly refined martial pressure. Flame strengthens strikes and movement, while tiger-shaped expressions communicate pouncing, driving and intercepting force.

**Applications:** White Tiger Pounce closes distance; Fangbreaker Fist concentrates a strike; Snowfire Mantle supports guarded advance. Sanda, Jeet Kune Do and Wing Chun provide different means of reaching an opening.

**Limits:** Tiger imagery does not establish a separately conscious summon or unrestricted shapeshifting. Knowing Transcendence does not mean it is always active. White flame does not imply healing, purification or immunity to all fire. A+ overall; document manifestation state and expenditure separately. Sources: Charles's lore, profiles, Path and catalogue.

## High-elite fighters

### Garrett Han — Golden Flame, True Sight and Fa Jin

**Description:** Golden Flame reinforces martial striking, defensive pressure and mobility. True Sight perceives mana/magical flow, improves Awakened efficiency and speed/strength application, lowers mana drainage and supplies precognition, combat perception and reflexes. Fa Jin is trained force delivery, not another fire power. Their combination lets Garrett recognise an opening and deliver concentrated pressure through practiced movement.

**Applications:** Preserve a technique's movement when amplified: flame reinforces contact or motion, True Sight improves flow efficiency, amplification and precognitive timing, and Fa Jin remains tied to physical execution. Established Transcendence is a distinct peak, not permanent maximum amplification.

**Limits:** No healing, mind-reading or guaranteed execution. Costs and state availability must be explicit; do not stack every enhancement for free. Baseline A, active-form comparisons separate. Sources: profiles, Vendetta lore, Path and catalogue.

### Rei Takamura — Flowing Tempest

**Description:** Flowing Tempest redirects kinetic force and develops speed and power through sustained movement. Wind and green lightning are established expressions. Its identity is continuity: movement, redirection and the next action reinforce one another while Rei controls the exchange.

**Applications:** Footwork, throws and strikes turn incoming pressure into better position. Tempest Mantle retains momentum defensively; Cyclone Crash combines a throw with controlled motion; Storm Rail expresses a rapid amplified approach. Wind, lightning and redirection are distinct applications.

**Limits:** Disruption, fatigue and injury matter. Accumulation is bounded; harmless repeated movement must not create infinite force. Redirection needs a feasible response and cannot automatically return every impact. A-tier starting champion; identify momentum state when comparing him with contenders or Richter. Sources: profiles, Vendetta lore and catalogue.

### Neo and Thirteen — Shinigami Protocol

**Confirmed definition:** Both possess Shinigami Protocol and an ultra-instinct trump-card state. They reactively respond, adapt to opponents and make the best possible combat choices. This supersedes older traitless descriptions.

**Expanded design interpretation:** The Trait integrates perception, combat processing and trained execution. The trump card minimises hesitation and coordinates the best feasible response to available information: interception, evasion, pressure, repositioning or a necessary trade. Adaptation concerns observed opponents and usable techniques, not acquisition of their supernatural powers.

**Limits:** No automatic dodge of unavoidable attacks, omniscience, Nanoengine, implanted HUD or invented programme history. Correct decisions can lose against overwhelming force. Shared naming does not settle Neo versus Thirteen. Baseline A is confirmed; the active trump-card state has confirmed temporary A+ combat effectiveness, driven mainly by execution, reactions and adaptation rather than an equal increase in every physical statistic.

**Confirmed differentiation:** Neo emphasises efficient interception, precision and tactical switching. Thirteen emphasises close suppression and restricting exits, spending more stamina when sustaining pressure. Neither version is inherently defective. Players choose intention/technique while the state improves execution rather than removing control.

**Confirmed activation, duration and costs:** Deliberate activation after sufficient combat pressure/readiness, normally 3–5 meaningful exchanges against a credible opponent. Meaningful attacking, defending, countering and observation build readiness; taking damage is not required, and idle guarding/harmless repeated actions cannot farm it. The state lasts four full exchanges, visibly counted; multi-hit actions do not consume multiple exchanges. Activation costs approximately 20% of maximum stamina and requires enough stamina to pay; ordinary action costs continue. Follow with two exchanges of recovery strain with reduced stamina recovery, no immediate reactivation and no automatic collapse or helpless stun.

**Confirmed reuse and power:** Initially once per encounter, resetting only after genuine recovery; fleeing/restarting or save/load must not refresh it. Preserve expenditure and remaining duration in saved encounters. Temporary A+ effectiveness allows a credible contest with Ivan/Charles during the window without guaranteeing victory; S/S+ opponents retain their overall advantage. Both player and NPC versions use the same readiness requirements. Exact readiness formula, stamina rounding, genuine-recovery criterion, reduction magnitude and adaptation persistence are implementation details still to define, not grounds to reopen the approved four-exchange/two-exchange structure.

**Signatures:** Neo's Adaptive Intercept and Thirteen's Suppression Rush express different applications. Preserve stable moves and separate baseline signatures from active-state enhancements. Source: explicit user revision; obsolete profile/catalogue labels require migration.

### Daniel Stevens — War God

**Confirmed foundation:** Daniel's Trait is War God, like his father's. Existing lore establishes enhanced physical capacity, reflexes and instinctive battle aptitude. The following detailed mechanics were confirmed on 2026-11-10. They define Daniel's implementation without inventing his father's entire repertoire or biography.

**Confirmed definition:** War God integrates power, balance and learned martial skills into exceptionally fluent combat. Daniel recognises how one exchange becomes the next: striking into clinching, pressure into a takedown, or an opponent's commitment into a reversal. Its identity is connected physical pressure, distinct from Polymath's analysis and the Shinigami trump card.

**Confirmed applications:** Whole-body coordination improves force delivery and stance recovery; close-contact reading detects leverage and weight shifts; instinctive transitions apply trained techniques when position permits. Perfect Transition, Concrete Driver and Instinctive Reversal provide existing signature anchors.

**Confirmed momentum:** Three bounded levels—Engaged, Flowing, Dominant—earned through successful varied exchanges. Higher levels improve transitions and pressure; a costly finisher/reversal consumes momentum. Lost engagement or decisive disruption causes decay. Ineffective repetition does not build it; one mistake need not disable the entire Trait.

**Costs and limits:** Reinforced combinations and finishers spend stamina; exact action costs and momentum thresholds require tuning. No automatic takedowns, unlimited strength, distant mind-reading or inheritance of every paternal technique. Baseline A remains confirmed; no extra A+ transformation is established. Father and son may differ in mastery and expression. Sources: user revision and physical-combat profile; momentum mechanics are confirmed; numerical tuning and testing remain pending.

### Martos Cabrera — Rage

**Description:** Battle pressure increases strength, durability and physical mutation, expanding Martos's capacity for direct suppression, reinforced collisions and close control.

**Applications:** Juggernaut Charge drives into contested space; Colossus Grip applies force after securing a grip; Siege Reversal turns a braced exchange into a return. Direct pressure does not automatically grant greater speed or precision.

**Limits:** Overmutation sacrifices control, coordination and judgement. Greater output is not a free improvement to every statistic. Injury matters; no infinite growth or regeneration. Define accumulation without making deliberate self-harm the only viable activation method. Sources: Four Aces lore, profiles and catalogue.

### Elias Braun — Pyromovement

**Description:** Movement accumulates heat released through strikes and burning trails. Maintaining useful rhythm prepares stronger releases; restrained motion limits accumulation.

**Applications:** Heatstep Engine develops heat through footwork; Ignition Carousel converts movement into a sweeping heated attack; Ember Encore links rhythm and release. Martial training determines how the attack reaches its target.

**Limits:** Not free unlimited fire generation. Track accumulated and spent output, with terrain effects only where resolved. **Proposed implementation:** distinguish heat reserves from stamina and prevent harmless repeated movement creating unlimited pre-fight output. Sources: Four Aces lore, profiles and catalogue.

### Mavis Kuro — Mist

**Description:** Mavis disperses into dark vapour for evasion/infiltration and returns to deliver physical force. Concealment and bodily dispersal complicate targeting, especially in low light.

**Applications:** Black-Vapour Slip moves around an incoming line; Hollow Counter pairs evasion and return; Smokebreak Traverse uses a real opening. Lost visual contact does not itself prove displacement or a successful strike.

**Limits:** Bright light limits concealment and dispersal is finite. No instant defeat under a light, limitless intangibility, teleportation or passage through every sealed barrier. Reformation, duration and traversal need explicit rules; visual effects do not establish universal weaknesses. Sources: Four Aces lore, profiles and catalogue.

### Edward Fox — Eight Senses

**Description:** Sound, scent, heartbeat, vibration and air displacement inform a detailed physical reading of nearby activity. Fox can use available signals when sight is obstructed to detect an approach, track movement or orient a counter.

**Applications:** Pulse Hunter tracks detectable movement; Shockline Read uses developing cues; Blindside Verdict answers a sensed approach. Military training supplies the physical response. Do not invent a definitive eight-item taxonomy where sources do not provide one.

**Limits:** No mind-reading, universal wall vision or automatic identity proof. Detection requires signals; sensing Takeo does not make Fox able to withstand his force. Signal-based counterplay needs authored rules, not an invented universal noise weakness. Sources: profiles, Interpol references and catalogue.

### Jeremy Gordon — Biocreation

**Description:** Gordon grows biological firearms, firing channels, high-impact rounds and adaptive components from his Awakened physiology. His body supplies the weapon system without dependence on external ammunition.

**Applications:** Living Cannon concentrates fire; Hydra Burst distributes a finite sequence; Adaptive Breach adjusts a component for an obstacle; Bone Bulwark provides protective growth. Regrowth Reload restores the weapon mechanism, not unrestricted bodily healing.

**Limits:** Powerful fire uses finite mana. No guaranteed hits, infinite simultaneous weapons, universal armour penetration or limitless regeneration. Adaptation remains within authored options. Relevant firepower does not erase a superior opponent's advantage. Sources: profiles, Interpol references and catalogue.

## B-tier Traits and physical abilities

### Tyler Harding — Impact storage

**Description:** Tyler stores a finite portion of absorbed impact and releases it through strikes. Surviving pressure creates an opportunity to return concentrated force through his boxing.

**Applications:** Breakwater Guard combines defence and partial storage; Debt Collector spends reserve in a punch; Redline Barrage divides it across separate impacts. One reserve cannot power every hit at full value.

**Limits:** Absorption does not cancel injury. Reserves are finite; durability determines whether Tyler survives the incoming blow. Define eligible impact sources rather than assuming all damage can be stored. Prevent self-sustaining rebound loops. Impact storage remains a descriptive label, not a newly established formal name. Sources: profiles, Vendetta lore and catalogue.

### Samantha Kim — Hemokinesis

**Description:** Samantha shapes her own and accessible blood into controlled external weapons/structures. Fluid material becomes a lance, cutting edge, restraint or barrier, supporting flexible attack and defence.

**Applications:** Crimson Lance concentrates a projectile; Red-Thread Snare contests external restraint; Coagulated Aegis forms a barrier. Available material, an eligible target and a successful action are separate requirements.

**Limits:** Own-blood use costs health; blood loss remains dangerous. No automatic control of intact bodies, instant internal killing, limitless supply or free healing by reclaiming blood. Specify material availability/recovery and avoid duplicating consumed sources. Sources: profiles, Vendetta lore and catalogue.

### Minsu Park — Speed and reflexes

**Description:** Short bursts of enhanced movement, reaction and coordination reinforce trained taekwondo. Minsu seizes brief openings, intercepts approaches and disengages through speed.

**Applications:** Vanishing Kick rapidly enters range; Hundred-Frame Step changes position; Racing Intercept reaches a viable interception point. Afterimages depict motion, not clones or independent attackers.

**Limits:** No time stop, teleportation or limitless sustained speed. A fast committed kick can be badly positioned or intercepted. Preserve fatigue, range and training; speed is not automatically the highest impact power. Formal Trait name remains unestablished. Sources: profiles, Vendetta lore and catalogue.

### Valentina Yeun — Deathwind and Misanthropy

**Confirmed origin and definition:** Ivan provided Deathwind to Valentina as an extension of his wind power. It remains her established cutting-wind/controlled-gust ability, now with an explicit shared origin, inherited soul damage and access to the wind-derived Misanthropy bonus. Do not invent the transfer's date, ritual or circumstances, or a general ability to grant Traits to anyone.

**Applications:** Horizon Sever creates a cutting line; Pressure Coffin applies contested pressure; Gale Reversal redirects an approach where feasible. Misanthropy allows Valentina to suffer more damage and remain standing, requiring real functional endurance mechanics rather than only descriptive narration.

**Boundaries and open design:** Misanthropy does not grant regeneration or automatic immunity. Specify its thresholds, access, duration, cost and accumulated-damage/exit rules consistently with Ivan. Deathwind explicitly inherits wind's soul damage because it comes from the same source, as confirmed by the user. Its offensive wind applications must use the shared soul-damage rules; the inherited bonus is Misanthropy. Define per-action damage amounts and defence interactions without stripping out the inherited soul effect. The origin does not grant fire, ice, lightning, Tranquility or the full Conduit State. No automatic death, soul control or limitless weather. Valentina remains B-tier. Source: explicit user revision plus existing Deathwind applications.

### Emily Fields — Critical Hit

**Description:** Critical Hit creates weak points for precise follow-up exploitation. Pain immunity lets Emily continue without normal pain response but does not prevent structural injury or damage-induced unconsciousness.

**Applications:** Fracture Point establishes an opportunity; Shatter Touch exploits one; Critical Verdict consumes an established opening for a stronger resolved effect. Creating a mark, reaching it and exploiting it are distinct steps.

**Limits:** Not instant death, automatic defence bypass, regeneration or immunity to physical incapacitation. Mark duration, stacking, valid surfaces, consumption and resistance require tuning. Emily starts awakened under the approved MH-002 correction; stale inactive-future-potential descriptions are superseded for this update. Sources: profiles, catalogue and approved correction.

### Alyssa — Umbrakinesis

**Description:** Alyssa shapes shadows into external pressure, defence and restraint, supported by enhanced speed/reflexes. It is her own ability, not inheritance of Sylvanis's complete arsenal.

**Applications:** Dusk Hammer shapes a striking mass; Black-Ribbon Bind contests restraint; Shade Mantle provides layered defence. Twilight Step conceals/accompanies movement without establishing teleportation. Ribbon imagery distinguishes her style without implying an arbitrary weakness.

**Limits:** No automatic intangibility, True Sight, Polymath or second-stage corrosive/explosive shadows. Define her own reach, construct durability and expenditure; do not copy Sylvanis or invent a daylight-disable rule. Sources: profiles, Vendetta lore and catalogue.

### Keisuke Hachimura — Awakened physical combat

**Description:** Awakened power supports Kyokushin and Japanese Jujutsu, making Keisuke dangerous through body strikes, pressure and throwing technique without a currently established named Trait.

**Applications:** Crushing Body Blow concentrates a strike; Groundsplitter Throw requires a grip and resolved landing; Relentless Storm sustains close pressure. Destructive names do not grant elemental attacks or automatic terrain damage.

**Limits:** Position, leverage, stamina and responses matter. Do not invent a Trait to fill an empty field. His clear inferiority to Thirteen remains; personality makes him neither harmless nor automatically irrational. Sources: profiles, catalogue, Keisuke and Thirteen lore.

## Technology, ordinary capabilities and forms

### Joseph Richter — Cybernetic boss enhancement

**Description:** Reinforced arms, a powered spinal frame, targeting systems and weapons create a low-A boss configuration. It is cybernetic enhancement, not a newly declared Awakened Trait. Civilian Richter remains unranked.

**Applications:** Confirmed design uses weapon pressure, momentum interruption, readable committed attacks and punishable recovery. Challenge comes from the functioning system rather than invented lifelong martial mastery. Reveal the enhanced form only in appropriate story context.

**Limits:** Moderately below Rei at comparable readiness. No Nanoengine, hidden second transformation or reinforcements by analogy with other bosses. Guard attrition is separate from full-health strength. Preserve the solo confrontation and actual victory requirement. Sources: `rei_story.py`, campaign dialogue and approved boss plan.

### Unawakened characters, guards and custom abilities

Yuriko, Sophie, Amy, Lena, Naomi, Celeste, Dev, Rosa and Elliot currently have no established Trait in the catalogue. Ordinary training, conditioning, equipment and defence remain meaningful. Absence of a Trait is not helplessness or permission to invent one. Treat other unranked characters on the same evidence-based basis.

Guard archetypes identify whether capabilities come from awakening, training, robotics, cybernetics or equipment. Iron Circle rank does not automatically confer a Trait. Custom abilities need the same definition, range/target, activation, cost, limitations and interaction fields plus bounded mechanical validation. Prose cannot author arbitrary effects.

### Transcendence, amplification and trump cards

Transcendence is a rare Path breakthrough associated with an established temporary, mana-intensive manifestation. Progression stage and active manifestation are different states. Garrett, Charles and Sylvanis require baseline/active descriptions. Ivan has his own established timing. Calling Shinigami a trump card must not automatically change Neo or Thirteen's Path stage.

Amplification preserves the underlying technique while applying a compatible effect. Range, action count, damage, resource use and statuses come from resolution, not extravagant description. Enhancements cannot spend the same reserve twice or silently stack into immunity. Martial schools retain their training and leverage requirements; master-move names do not create elemental powers.

## Required move-level description contract

These Trait definitions do not replace detailed descriptions for every existing/future move. During integration, give each action a summary and details stating: what the user does; target and range; prerequisites/setup; costs; normal outcome; miss/block/resisted behaviour; duration and stacking/consumption; eligible amplification and state changes; limitations; stable source/action IDs. Display verified mechanical values, never invented AI-prose numbers.

For example, Critical Verdict exploits an established eligible weak point. Its preview must specify required mark, actual range/cost, consumption timing and miss/resistance rules. Those values remain to be authored and tested; no instant-victory promise. Adaptive Intercept must distinguish baseline from active Shinigami execution and show whether a feasible reaction is available, rather than promising a counter to everything.

## Integration, review and evidence

- Reconcile `combat_profiles.py`, `combat_catalogue/traits.json`, `combat_path.py`, lore modules and character references with explicit approved changes. Preserve stable IDs/learned skills and migrate conflicting traitless labels for Neo, Thirteen, Daniel and April.
- These entries supply the ability component of identity sheets; they do not claim every complete character sheet or every move specification is finished. Add source-linked AI, matchup and state details during implementation.
- Preserve discovery boundaries. Renaming lore must not secretly grant numerical boosts or rewrite old stories. Document save migration separately.
- Before release, review descriptions against mechanics and new-move/progression requirements. Test applicable interactions, resources, state transitions, saves and player/opponent symmetry. Inspect expanded panels, keyboard access and hidden/unknown states; run phone theme checks if phone surfaces change.
- Authoring evidence: read profiles, Trait catalogue, Path, Takeo/Four Aces descriptions and approved plan. No runtime code, saves or gameplay balance changed; no gameplay/UI test claimed. Shinigami timing/cost/power and War God mechanics are now confirmed scope; remaining numeric detail and the new lore interactions still require implementation and verification.
- Record implemented behaviour and actual checks in release patch notes when integrated. This reference is planning material, not a gameplay release.
