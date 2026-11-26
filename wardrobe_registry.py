"""Reviewed category metadata over the existing eligible wardrobe catalogue.

This table does not make a look eligible. camera.outfits remains the authority
for ownership, relationship gates, custom designs, file existence and identity.
Unlisted/custom art is everyday clothing until explicitly tagged.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CATEGORIES={}
# These alternate sprites already have live location selection in game.py.
# Sharing them with camera/automatic appearance removes divergent selectors;
# it introduces no relationship-gated gallery looks or generated designs.
OPTIONS={
 'yuriko':{'Teal sporty bikini':'bikini-teal','Coral floral bikini':'bikini-floral','Navy high-waisted bikini':'bikini-navy',
           'Sage gym set':'gym-sage','Lavender gym layers':'gym-lavender','Theatre workshop overalls':'theatre-overalls','Burgundy evening dress':'evening-dress'},
 'april':{'Beach bikini':'beach-bikini','Beach swimsuit':'beach-swimsuit','Plum training outfit':'gym-plum',
          'Ivory formal suit':'formal-ivory-suit','Emerald evening dress':'formal-emerald'},
 'samantha':{'Black sport bikini':'beach-black-bikini','Crimson bikini':'beach-red-bikini','Teal bikini':'beach-teal-bikini',
             'Charcoal gym set':'gym-charcoal','Olive training set':'gym-olive','Black evening suit':'formal-black-suit','Burgundy evening dress':'formal-burgundy-dress'},
}


def assign(who,category,slugs):
    for slug in slugs:
        CATEGORIES['assets/portraits/'+who+'-'+slug+'.png']=category


for _who in ('rei','garrett','minsu','ivan','yuriko','emily','sophie','amy','samantha','april',
             'valentina','neo','alyssa','tyler','lena','naomi','celeste','dev','rosa','elliot','daniel',
             'fox','gordon','sylvanis','martos','elias','mavis','camila','charles','takeo','thirteen','crow'):
    assign(_who,'home',('home',))
    assign(_who,'sleep',('sleep',))
assign('rei','beach',('beach',));assign('rei','gym',('gym',))
assign('rei','formal',('selection','tailored-waistcoat'))
assign('garrett','beach',('beach-shorts',));assign('garrett','gym',('gym-tank','gym-compression'))
assign('garrett','formal',('formal-tuxedo','formal-burgundy'))
assign('minsu','beach',('beach-shorts',));assign('minsu','gym',('gym-tank','gym-compression'))
assign('ivan','beach',('beach',));assign('ivan','gym',('gym-tank','gym-training'))
assign('ivan','stage',('idol-midnight','idol-white','idol-crimson'))
assign('ivan','formal',('fashion-ivory',))
assign('emily','beach',('beach-bikini','beach-swimsuit'));assign('emily','gym',('gym',))
assign('emily','formal',('formal-satin','formal-tailoring'));assign('emily','florist',('florist',))
assign('sophie','beach',('beach-coral','beach-tropical','beach-cobalt'))
assign('sophie','gym',('gym-strength','gym-cardio'));assign('sophie','formal',('formal-emerald','formal-suit'))
assign('amy','beach',('beach-sage','beach-daisy','beach-terracotta'))
assign('amy','gym',('gym-yoga','gym-training'));assign('amy','formal',('formal-plum','formal-tweed'))
assign('samantha','beach',('beach-black-bikini','beach-red-bikini','beach-teal-bikini'))
assign('samantha','gym',('gym-charcoal','gym-olive'));assign('samantha','formal',('formal-black-suit','formal-burgundy-dress'))
assign('april','beach',('beach-bikini','beach-swimsuit'));assign('april','gym',('gym-plum',))
assign('april','formal',('formal-ivory-suit','formal-emerald'))
assign('yuriko','beach',('bikini-teal','bikini-floral','bikini-navy'))
assign('yuriko','gym',('gym-sage','gym-lavender'));assign('yuriko','formal',('evening-dress',))
assign('yuriko','theatre',('theatre-overalls',))
for _who in ('crow','ivan','sylvanis','martos','elias','mavis','camila'):
    assign(_who,'required',('syndicate',))
    CATEGORIES['assets/portraits/combat/'+_who+'.png']='required'


def category(path):
    try:
        absolute=Path(path).resolve()
        relative=absolute.relative_to(ROOT).as_posix()
    except (ValueError,TypeError,OSError):return 'baseline'
    return CATEGORIES.get(relative,'baseline')


def options(who):
    return {label:str(ROOT/'assets/portraits'/(who+'-'+slug+'.png'))
            for label,slug in OPTIONS.get(who,{}).items() if (ROOT/'assets/portraits'/(who+'-'+slug+'.png')).is_file()}


def required_combat(s,who):
    """Existing masked combat art outranks optional visit clothes and snapshots."""
    fight=s.get('combat',{}).get('active') or {}
    if who not in ('martos','elias','camila','mavis','crow','ivan','sylvanis'):return None
    if who not in (s.get('player'),fight.get('opponent'),fight.get('ally')) or not fight:return None
    path=ROOT/'assets/portraits/combat'/(who+'.png')
    return str(path) if path.is_file() else None
