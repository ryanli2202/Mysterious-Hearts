import json
import unittest
from unittest.mock import patch
import game_core as core
import street_recruits as street
import town, town_residents, phone_numbers, custom_gangs as gangs


class StreetRecruitTests(unittest.TestCase):
    def test_roster_references_and_original_recruits_retained(self):
        self.assertEqual(len(street.NAMES),6)
        self.assertEqual(len(gangs.RECRUITS),12)
        self.assertTrue({'Gabe Turner','Ben Okafor','Nadia Flores','Tess Morgan','Wren Park','Farah Haddad'} <= gangs.RECRUITS.keys())
        for name,p in street.RESIDENTS.items():
            self.assertTrue(21 <= p['age'] <= 26)
            self.assertIn(name,phone_numbers.NUMBERS)
            self.assertIn(p['life'],town_residents.profile(name)[2])
            self.assertEqual(town_residents.portrait_reference(name),p['appearance'])
            self.assertEqual(len(street.TASTES[name]),9)
            self.assertIn(street.RECRUITS[name][0],gangs.ROLES)

    def test_all_can_be_met_and_recruited_and_saved(self):
        for name in street.NAMES:
            s=core.fresh('minsu'); d=gangs.jobs.ensure(s); d.update(reputation=40,completed=10)
            gangs.jobs.gang(s,'Street Circle')
            s['world']['minute']=2*1440+600
            venue=gangs.location(s,name)
            s['world']['location']=venue; s['world']['cast']['minsu'].update(location=venue,journey=None)
            town_residents.refresh(s); self.assertIn(name,s['world']['npcs'])
            self.assertIn('trust',gangs.reason(s,name).lower())
            s.setdefault('npc_chats',{})[name]=dict(history=[],connection=dict(status='friends',trust=65))
            with patch.object(gangs.jobs.careers,'spend_time'):
                gangs.recruit(s,name)
            gangs.assign(s,name,street.RECRUITS[name][0])
            restored=json.loads(json.dumps(s))
            self.assertIn(name,gangs.crew(restored)['members'])
            phone_numbers.ensure(restored); self.assertIn(name,restored['phone_numbers']['contacts'])

    def test_routines_and_old_phone_numbers_stay_stable(self):
        start=phone_numbers.RESIDENTS.index(street.NAMES[0])
        old=phone_numbers.RESIDENTS[:start]
        for index,name in enumerate(old): self.assertEqual(phone_numbers.NUMBERS[name],f'1202555{100+index:04d}')
        self.assertEqual(tuple(phone_numbers.RESIDENTS[start:start+len(street.NAMES)]),street.NAMES)
        with patch('town_residents.weather.shelter',return_value=False):
            for name,p in street.RESIDENTS.items():
                for day,field in ((0,'weekend'),(2,'places')):
                    for slot,hour in enumerate((9,14,19)):
                        self.assertEqual(town_residents.routine(name,day*1440+hour*60),p[field][slot])
                self.assertIsNone(town_residents.routine(name,23*60))


if __name__=='__main__': unittest.main()
