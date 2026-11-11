"""Richter's revealed powered frame: committed attacks and punishable recovery."""
import combat_moves as moves


def install(p):
    p['boss']='richter'; p['combat_id']='richter:enhanced'; p['combat_band']='Low A'
    p['stats'].update(awakened_power=76,martial_skill=84,fight_iq=86)
    p['trait']=None
    attacks=[]
    for ident,name,role,cost,force,tags,reach in (
        ('target','Targeting sweep','setup',6,.0,('precision',),4),
        ('burst','Committed weapon burst','attack',18,2.20,('reach','stagger'),4),
        ('recover','Frame recovery','recovery',0,0,(),0),
        ('ram','Powered frame ram','break',22,2.10,('breach','knockback'),1)):
        m=moves.spec('boss:richter:'+ident,name,
            'Targeting precedes the burst; evade or use cover. The following recovery exposes the frame.' if ident!='ram' else 'A committed close ram; create distance or counter its recovery.',
            role,'unique','equipment',tags=tags)
        m.update(stamina=cost,mana=0,force=force,range=reach); attacks.append(m)
    p['equipment_moves']=attacks
    p['moveset']['unique']=[]
    return p


def intent(p,f):
    if p.get('boss')!='richter': return None
    return ('target','burst','recover','ram','recover')[f['turn']%5]
