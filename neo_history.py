"""Three earned historical areas, with exact-age rooms and isolation."""
TITLES={'neo-school':'A Seat Saved for You','neo-adoptive-home':'Learning to Be Home','neo-shinigami-facility':'Before We Had Names'}
PERIODS={'neo-school':(('SCHOOL','School - age sixteen',None),),'neo-adoptive-home':(('HOME-A','Early home - age twelve','NE-M01'),('HOME-B','Settled home - age sixteen','NE-M03')),'neo-shinigami-facility':(('FACILITY','Before the raid - age ten','NE-M05'),)}
ERAS={'SCHOOL':'neo_school16','HOME-A':'neo_home12','HOME-B':'neo_home16','FACILITY':'neo_facility10'}
def rows(prefix,items):
 return {prefix+key:(title,'locations/campaign/neo/'+art,tuple(prefix+v for v in links),cast) for key,title,art,links,cast in items}
ROOMS={
 'neo-school':rows('NS',[('1','Gym','school_gym',('2',),('neo','tyler','daniel')),('2','Corridor','school_corridor',('1','3'),('neo','tyler','daniel')),('3','Lunch courtyard','school_courtyard',('2','4'),('neo','tyler','daniel')),('4','School gate','school_gate',('3',),('neo','tyler','daniel'))]),
 'neo-adoptive-home':rows('NH',[('1','Kitchen','home_kitchen',('2','3'),('neo','mariko')),('2','Living room','home_living',('1','3','5'),('neo','mariko')),('3','Hall','home_hall',('1','2','4'),('neo','mariko')),('4','Bedroom - privacy respected','home_bedroom',('3',),('neo',)),('5','Garden porch','home_garden',('2',),('neo','mariko'))]),
 'neo-shinigami-facility':rows('NF',[('1','Trainee dormitory','facility_dorm',('2',),('neo','thirteen','trainee')),('2','Dining room','facility_dining',('1','3'),('neo','thirteen','trainee')),('3','Supervised courtyard','facility_courtyard',('2','4'),('neo','thirteen','trainee')),('4','Training hall','facility_hall',('3',),('neo','thirteen','trainee'))])}
def locked(s,area):
 d=s.get('neo_campaign',{})
 if s.get('player')!='neo' or not d.get('started'):return 'Start the campaign explicitly.'
 if area not in PERIODS:return 'Unknown historical area.'
 if not any(gate is None or gate in d.get('memories',[]) for _,_,gate in PERIODS[area]):return 'Complete the corresponding authored memory first.'
 return ''
def choose(s,key):
 if s.get('flashback_visit') or s.get('campaign_dialogue') or s.get('neo_campaign',{}).get('session'):raise ValueError('Return from the current scene first.')
 reason=locked(s,key)
 if reason:raise ValueError(reason)
 __import__('neo_campaigns').data(s)['visit_area']=key
 return key
def area(s):return (s.get('flashback_visit') or {}).get('area') or s.get('neo_campaign',{}).get('visit_area','neo-school')
def activities(s):
 key=(s.get('flashback_visit') or {}).get('area')
 if key=='neo-adoptive-home':return ('Share an ordinary meal','Try a harmless radio repair','Choose where to keep an ordinary possession','Sit quietly together')
 if key=='neo-school':return ('Share lunch','Discuss a film','Try controlled practice','Wait at the gate')
 return ('Share food','Discuss the supplied training day','Spend a supervised quiet interval')
def opening(s,members):
 import campaign_memory_areas as spaces,flashback_lore
 era=spaces.reference_era(s,area(s));who=members[0] if members else None
 text={'mariko':'Dinner first. The radio can wait.' if era=='neo_home16' else 'You can leave it there. We will look tomorrow.','tyler':'Saved you a seat.','daniel':'I chose the film. You can come.','thirteen':'There is still room here.','trainee':'Move the bowl a little.'}.get(who,'')
 return dict(player='',narration=flashback_lore.era(era)['setting'],lines=[dict(speaker=who,text=text)] if who else [])
