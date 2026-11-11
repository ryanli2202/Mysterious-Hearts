"""Authored animation choreography. Tokens are visual beats, never game rules.

Each line matches a catalogue name exactly. '+' layers simultaneous effects;
spaces separate beats; '/material' overrides the character's default material.
"""

MASTER = {
    'Boxing': '''
Hurricane punches|gather orbit flurry burst
Ghost step|crouch dash settle
Unseen spectre|orbit afterimages flurry sweep
Power-breaker|charge punch compress burst
Phantom cadence|jab jab pause flurry
Thunderclap counter|incoming evade punch ring
Iron constellation|jab lowstrike uppercut constellation
Vanishing bell|incoming sidestep hook bell
''',
    'Taekwondo': '''
Skywheel barrage|rise spin kicks descend
Horizon step|crouch dash kick settle
Falling star|rise hang heel quake
Mirage wheel|afterimages highkick lowkick spin
''',
    'Judo': '''
World-turner|grip orbit throw ground
Falling mountain|grip crouch slam ground
Zero-point reversal|incoming grip pause reverse-throw
Iron orbit|grip tilt orbit tilt
''',
    'Kyokushin': '''
Mountain-splitter|brace charge punch fracture
Adamant advance|brace incoming step punch
Hundred-beat barrage|lowstrike jab lowkick flurry
Thunder heel|highkick hang heel ring
''',
    'MMA': '''
Apex chain|jab kick crouch throw grip
Predator switch|jab feint crouch takedown
Gravity crash|crouch dash grip slam
Total control|grip tilt lattice grip
''',
    'Muay Thai': '''
Eight-limbed tempest|jab elbow knee kicks
Meteor knee|crouch rise knee burst
Titan clinch|grip brace compress knee
Thunder pillar|charge kick beam ring
''',
    'Streetfighting': '''
Riot engine|zigzag jab elbow flurry
Backstreet phantom|sidestep zigzag afterimages settle
Concrete verdict|charge dash punch fracture
Chaos rhythm|feint pause jab pause flurry
''',
    'Sanda': '''
Storm bridge|kick dash grip throw
Sky-catch reversal|incoming rise grip reverse-throw
Horizon breaker|brace kick beam burst
Cyclone sweep|crouch spin lowkick takedown
''',
    'Jeet Kune Do': '''
Stillpoint intercept|incoming scan jab ring
Vanishing line|incoming sidestep diagonal settle
One-beat thunder|pause jab compress burst
Empty rhythm|feint jab pause lowstrike
''',
    'Military CQC': '''
Breach sequence|dash elbow grip tilt
Lockdown engine|grip lattice tilt bind
Silent vector|crouch trail dash settle
Titan restraint|brace grip compress bind
''',
    'Kickboxing': '''
Tempest circuit|jab kick orbit flurry
Sonic crescent|kick sweep ring settle
Iron comet|punch dash kick compress
Phantom relay|jab sidestep kick afterimages
''',
    'Silat': '''
Serpent lattice|sweep grip lattice tilt
Phantom crescent|afterimages crouch lowkick takedown
Falling canopy|incoming crouch grip throw
Mirror snare|feint sweep reverse-throw settle
''',
    'Aikido': '''
Still-water reversal|incoming ring redirect throw
World-axis turn|grip pivot orbit throw
Orbit of silence|grip orbit tilt orbit
Returning mountain|incoming brace compress reverse-throw
''',
    'Taido': '''
Axis phantom|tilt invert sidestep afterimages
Sky spiral|rise spin kicks descend
Inverted comet|vault invert diagonal kick
Nine-angle mirage|afterimages highkick sidestep lowkick flurry
''',
    'Lethwei': '''
Nine-limbed thunder|elbow knee headbutt flurry
Iron monsoon|step lowstrike incoming elbow
Falling bell|crouch headbutt bell settle
Unbroken advance|incoming brace step flurry
''',
    'Japanese Jujutsu': '''
Thousand-link bind|grip lattice grip bind
Earthfall reversal|incoming tilt reverse-throw ground
Iron labyrinth|scan lattice tilt grip
Silent avalanche|trail dash throw bind
''',
    'Wing Chun': '''
Thousand-point rain|charge jab flurry beam
Centre-line collapse|compress punch beam fracture
Mirror hands|incoming redirect jab redirect punch
Inch thunder|grip pause jab burst
''',
    'Shinokami martial arts': '''
Eclipse intercept|incoming cross eclipse jab
Null cadence|jab pause elbow pause punch
Shinigami crossing|incoming cross diagonal settle
Iron eclipse|incoming eclipse jab eclipse punch
''',
    'Krav Maga': '''
Zero-window response|incoming+jab elbow burst
Breakout surge|bind compress breakout dash
Iron corridor|shield step jab step elbow
Last-light reversal|incoming evade grip reverse-throw
''',
    'Systema': '''
Quiet thunder|settle pause punch ring
Flowing void|incoming evade incoming sidestep
Pulse cascade|jab pulse lowstrike pulse punch
Unbroken current|incoming redirect pivot punch
''',
    'Kudo': '''
Tempest clinch|elbow knee grip throw
Meteor wheel|grip rise orbit slam
Crashing tide|step punch grip lowstrike
Seamless storm|jab kick grip pivot throw
''',
}

UNIQUE = {
    'garrett': ('gold', '''
Dragon Kick|charge dash kick+dragon burst
Sunbreaker Fist|gather punch beam fracture
Golden Dragon Spiral|rise spin spiral burst
Solar Wake|charge dash trail punch
True-Sight Reversal|incoming scan/gold evade punch/physical
Dragon's Descent|rise dragon drop quake
Phoenix Wheel|spin sweep wings burst
Dawnfall Breaker|scan beam punch bloom
'''),
    'rei': ('green', '''
Descending Tempest|rise/wind hang heel+lightning quake
Flowing Stream|incoming redirect/wind return ring
Thousand Sparks|orbit trail orbit spin+lightning burst
Emerald Rift|kick/wind crescent/wind beam fracture
Cyclone Crash|grip/physical spiral/wind throw ground
Storm Rail|rails dash punch lightning
Tempest Mantle|shield/wind incoming gather orbit
Eye of the Tempest|gather/wind orbit/wind lightning radial/wind
'''),
    'ivan': ('red', '''
Furnace Knee|gather/fire knee/fire bloom/fire quake/fire
Whiteout Crash|plates/ice dash/ice shoulder/ice shards/ice
Gale Cutter|spin/wind kick/wind crescent/wind fracture/wind
Crimson Break|gather/red punch/red lightning/red burst/red
Azure Blink|scan/blue dash/blue jab/blue settle/blue
Flashfreeze Snare|ground/ice trail/ice spikes/ice bind/ice
Thunderhead Drop|rise/wind hang/red drop/red lightning/red+quake/physical
Winterstorm Ring|spin/wind orbit/ice radial/ice ground/ice
Arc Split|sidestep/blue dash/blue punch/red burst/red
Fivefold Ruin|bloom/fire crescent/wind spikes/ice dash/blue punch/red+lightning/red
'''),
    'sylvanis': ('shadow', '''
Nightfall Hammer|gather shadowfist punch slam
Midnight Coil|coil bind compress pulse
Umbral Rush|mist trail dash shadowfist
True-Sight Intercept|incoming/physical scan cross punch
Polymath Rupture|scan lattice jab pause punch
Eclipse Convergence|wall lattice converge compress
Black Sun Collapse|gather eclipse drop radial
Shadow Requiem|scan wall lattice dash flurry
'''),
    'charles': ('white', '''
White Tiger Pounce|crouch tiger dash burst
Fangbreaker Fist|gather fang punch fracture
Tiger Wheel|spin claws orbit radial
White-Flame Roar|charge tiger beam bloom
Twin-Fang Return|incoming/physical shield fang fang
Snowfire Mantle|shield incoming/physical step punch
'''),
    'takeo': ('metal', '''
Siege Fist|plates gather metalfist fracture
Bunker Rush|plates shield dash shoulder
Adaptive Bulwark|incoming/physical plates shield compress
Monolith Blade|plates blade sweep fracture
Engine Overdrive|pulse charge dash metalfist
Iron Meteor|plates rise drop quake
'''),
    'crow': ('analysis', '''
Checkmate Sequence|scan lattice jab kick wall
Perfect Counter|incoming/physical scan cross punch/physical
Black Rook Breach|grid scan beam punch/physical
Hundred-Style Sequence|jab/physical kick/physical elbow/physical throw/physical
Queen's Gambit|feint incoming/physical scan flurry/physical
King in Motion|scan grid sidestep diagonal
'''),
    'martos': ('rage', '''
Juggernaut Charge|brace dash shoulder ground
Ruin Hammer|charge rise slam quake
Colossus Grip|grip compress throw ground
Aftershock Stamp|brace heel ground quake
Redline Surge|pulse pulse dash flurry
Siege Reversal|incoming/physical brace gather punch
'''),
    'elias': ('fire', '''
Heatstep Engine|step trail step dash
Ignition Carousel|gather spin sweep bloom
Cinder Rail|trail rails dash beam
Ember Encore|kick gather kick bloom
Scorched Stage|orbit trail cross ground
Curtainfall Kick|gather rise heel rain
'''),
    'mavis': ('mist', '''
Black-Vapour Slip|incoming/physical mist sidestep reform
Hollow Counter|incoming/physical hollow mist punch/physical
Veilbreaker Palm|mist reform palm/physical burst
Shrouded Sweep|ground mist lowkick/physical sweep
Smokebreak Traverse|wall/physical mist tunnel reform
Midnight Curtain|mist wall sidestep mist
'''),
    'camila': ('teal', '''
Faultline Palm|grid scan palm/physical fracture
Pattern Lock|afterimages scan mark pulse
Checkmate Turn|incoming/physical scan pivot throw/physical
Tempo Theft|scan pulse dash jab/physical
Glassboard Feint|grid feint incoming/physical punch/physical
Cascade Reversal|grip/physical pivot tilt throw/physical
'''),
    'samantha': ('blood', '''
Crimson Lance|gather lance beam burst
Red-Thread Snare|ribbons coil bind pull
Scarlet Crescent|ribbons blade crescent shards
Bloodbloom Burst|gather bloom fang radial
Coagulated Aegis|gather plates shield incoming/physical
Returning Fang|fang projectile curve return
'''),
    'tyler': ('kinetic', '''
Debt Collector|orbit gather punch burst
Rebound Crash|incoming/physical compress gather punch
Breakwater Guard|shield incoming/physical gather coil
Avalanche Hook|coil charge hook radial
Redline Barrage|orbit jab pulse jab pulse flurry
Aftershock Uppercut|gather uppercut rise ground
'''),
    'minsu': ('speed', '''
Vanishing Kick|trail dash kick afterimages
Hundred-Frame Step|incoming/physical afterimages orbit sidestep
Blink Chain|dash highkick lowkick kicks
Racing Intercept|incoming/physical cross dash kick
Comet Run|step trail dash kick+burst
Afterimage Relay|sidestep afterimages orbit highkick
'''),
    'valentina': ('wind', '''
Guillotine Gale|hang blade drop fracture
Cyclone Vault|spiral vault spin kick
Pressure Coffin|wall converge compress bind
Horizon Sever|sweep crescent beam fracture
Gale Reversal|incoming/physical redirect crescent return
Seventh Squall|sweep diagonal radial sweep radial
'''),
    'emily': ('mark', '''
Fracture Point|palm/physical mark pulse settle
Shatter Touch|mark palm/physical fracture shards
Faultline Rush|scan dash mark punch/physical
Painless Advance|incoming/physical brace step punch/physical
Chain Fracture|mark jab/physical fracture mark punch/physical
Critical Verdict|mark compress punch/physical fracture radial
'''),
    'alyssa': ('ribbon', '''
Dusk Hammer|ribbons gather shadowfist burst
Black-Ribbon Bind|ribbons coil bind pull
Shade Mantle|ribbons plates shield incoming/physical
Twilight Step|wall mist sidestep punch
Midnight Sweep|ground ribbons sweep radial
Falling Shade|ribbons gather drop slam
'''),
    'fox': ('sense', '''
Blindside Verdict|incoming/physical pulse scan punch/physical
Pulse Hunter|pulse scan trail dash
Zero-Noise Rush|scan ground trail jab/physical
Shockline Read|ground pulse incoming/physical sidestep punch/physical
Eightfold Intercept|radial scan converge jab/physical
Blackhaven Breaker|palm/physical pulse grid punch/physical
'''),
    'gordon': ('bone', '''
Living Cannon|grow cannon projectile burst
Hydra Burst|grow hydra volley radial
Adaptive Breach|scan grow cannon fracture
Bone Bulwark|grow plates shield incoming/physical
Regrowth Reload|shards retract grow reload
Siege Lance|grow lance beam fracture
'''),
    'neo': ('physical', '''
Shinigami Vector|diagonal dash elbow burst
Breakpoint Drive|brace punch compress fracture
Adaptive Intercept|incoming scan feint elbow
'''),
    'daniel': ('physical', '''
Perfect Transition|jab crouch grip takedown
Concrete Driver|grip charge slam ground
Instinctive Reversal|incoming tilt pivot punch
'''),
    'april': ('analysis', '''
Accelerated Calculation|incoming/physical scan grid shield
Pattern Map|afterimages grid scan mark
Predictive Escape|converge scan tunnel dash/physical
'''),
    'thirteen': ('physical', '''
Suppression Rush|dash elbow jab step punch
Iron Reversal|incoming brace grip reverse-throw
Vanishing Entry|incoming sidestep cross dash
'''),
    'keisuke': ('physical', '''
Crushing Body Blow|charge lowstrike compress ground
Groundsplitter Throw|grip brace throw quake
Relentless Storm|lowstrike knee kick grip elbow
'''),
}

# Shared actions and outcome/status accents are also usable by future custom skills.
COMMON = '''
Direct strike|physical|jab burst
Slash|physical|blade sweep
Heavy impact|physical|charge punch burst
Projectile|physical|projectile burst
Magic impact|blue|gather projectile lightning
Heal|heal|gather bloom pulse
Guard|physical|brace shield
Block|physical|incoming shield ring
Dodge|physical|incoming evade
Miss|physical|incoming sidestep trail
Critical hit|mark|mark punch fracture
Poison|poison|mist rise pulse
Burn|fire|bloom rise ember
Stagger|physical|burst tilt
Weak-point mark|mark|mark pulse
Concealment|mist|mist hollow
Barrier break|blue|shield incoming shards
Recovery|heal|gather pulse settle
Advance|physical|step dash
Retreat|physical|incoming sidestep retreat
Take cover|physical|wall crouch shield
Escape|physical|breakout retreat trail
'''

COLORS = {
 'physical': '#b8d4e5', 'gold':'#ffc343', 'white':'#d6f3ff',
 'green':'#47f6a0','red':'#ff405e','blue':'#39baff','fire':'#ff822f',
 'ice':'#83e4ff','wind':'#a3e7d0','shadow':'#9865ef','metal':'#ecb754',
 'analysis':'#b9c8dd','rage':'#c4515a','mist':'#a9b8cc','teal':'#47ddd0',
 'blood':'#c92f62','kinetic':'#ffc879','speed':'#80c8ef','mark':'#fa75cd',
 'ribbon':'#ba7ef7','sense':'#e5b967','bone':'#d9cfad',
 'heal':'#75e6bb','poison':'#9ccb6a',
}

# Illustrated material atlas, generated with built-in image_gen.
SPRITES = {
 'gold':0,'white':1,'green':2,'red':3,'blue':4,'fire':5,'ice':6,
 'wind':7,'shadow':8,'ribbon':8,'mist':9,'blood':10,'bone':11,
 'metal':12,'kinetic':13,'physical':14,'mark':15,
}
