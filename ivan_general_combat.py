"""Five distinct finite kits on the shared resolver; no power transfer simulation."""
KITS={
 'valentina':('Wind','Taido',[
 ('Axis Step','mobility','evade',0),('Spiral Heel','attack','precision',0),('Gale Edge','attack','reach',14),('Crosswind Break','control','knockback',14),('Slipstream Retreat','mobility','retreat evade',10),('Wind Screen','defence','guard',14),('Deathwind Cross','combo','reach',28)]),
 'sowon':('Blue lightning','Taekwondo',[
 ('Checking Side Kick','control','precision',0),('Turning Roundhouse','attack','',0),('Blue Step','mobility','speed evade',12),('Storm Intercept','counter','speed',14),('Tempo Feint','setup','precision',0),('Split-Angle Combination','combo','speed',24),('Crown of Storms','combo','speed precision',30)]),
 'kouji':('Fire','Kickboxing',[
 ('Measuring Jab','setup','precision',0),('Driving Low Kick','attack','stagger',0),('Furnace Clinch','control','restrain stability',14),('Ember Cross','attack','heat',14),('Braced Guard','defence','guard stability',10),('Driving Entry','mobility','advance guard',0),('Kiln Breaker','combo','breach',28)]),
 'paul':('Ice','Judo',[
 ('Grip Check','control','restrain',0),('Outside Reap','throw','knockback',0),('Ice Footing','control','ice',14),('Ice Guard','defence','guard barrier',14),('Cold Counter','counter','ice precision',14),('Release and Reset','mobility','evade',0),('Winter Reversal','counter','ice precision',28)]),
 'somchai':('Red lightning','Streetfighting',[
 ('Hand Check','setup','precision',0),('Driving Body Hook','attack','',0),('Red Pulse','attack','breach',14),('Breach Step','mobility','advance',0),('Red Interruption','counter','knockback',18),('Corner Pressure','control','restrain corner',0),('Red Verdict','attack','breach stagger',30)]),
}
STATES={'valentina':'Misanthropy','sowon':'Lightning Pace','kouji':'Forge Strength','paul':'Tranquility','somchai':'Redline Pressure'}

def install(p,who):
    if who not in KITS:return
    book=p['moveset']
    if book.get('ivan_general_kit_v1'):return
    import combat_moves as moves
    element,art,kit=KITS[who]
    for index,(name,role,tags,mana) in enumerate(kit):
        ident='unique:ivan-general:'+who+':'+moves.slug(name)
        if any(row['id']==ident for row in book['unique']):continue
        row=moves.spec(ident,name,'Bounded '+art+' '+role+('. Uses '+element+' through the shared elemental rules.' if mana else '; physical technique, no free element.'),role,'unique','unique',art,tags.split(),element if mana else '')
        row.update(mana=mana,stamina=22 if index==6 else 10,force=1.4 if index==6 else 1.1,range=4 if 'reach' in tags else 1,hits=2 if role=='combo' else 1)
        if name=='Ice Footing':row.update(tags=['ice','footing'],force=0.,description='Create one short-lived ice patch at a reachable position. Both sides can lose footing; no intact-body freeze or damage.')
        book['unique'].append(row)
    book['ivan_general_kit_v1']=True
