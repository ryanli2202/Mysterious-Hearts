import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as core
import town
import groups
import job_apps as jobs
import gang_leaders as leaders
import crime_diplomacy as dip
import criminal_reputation as rep
import phone_numbers
import character_types
import town_npc_system
from test_crime_diplomacy import place, attend


class GangLeaderTests(unittest.TestCase):
    def test_reputation_and_ivan_dual_affiliation(self):
        for who,value in rep.SCORES.items():
            self.assertEqual(jobs.progression.ESTABLISHED[who][0],value)
        for who in ('garrett','ivan'):
            s=core.fresh(who); d=jobs.ensure(s)
            self.assertEqual(d['reputation'],rep.SCORES[who])
            d['reputation']=70; jobs.ensure(s); self.assertEqual(d['reputation'],70)
        self.assertEqual(d['affiliations'],['Syndicate','Black and White Joker network'])
        self.assertEqual(d['syndicate_role'],'Black and White Joker')
        rows=jobs.progression.directory(s)
        self.assertIn('Crazed Demon',rows[0]); self.assertIn('Crow',rows[1])

    def test_all_joining_contacts_and_resident_bases(self):
        import phone_map
        for key,p in leaders.LEADERS.items():
            s=core.fresh('minsu'); d=jobs.ensure(s); d.update(reputation=60,completed=12)
            with self.assertRaises(ValueError): phone_numbers.add(s,phone_numbers.NUMBERS[p['name']])
            jobs.progression.join(s,key)
            self.assertTrue(phone_numbers.saved_number(s,p['name']))
            history=copy.deepcopy(s['npc_chats'][p['name']]['history']); leaders.ensure(s)
            self.assertEqual(history,s['npc_chats'][p['name']]['history'])
            town.travel(s,p['base'])
            import gang_members
            self.assertEqual(s['world']['npcs'],[p['name'], *gang_members.coworkers(s)])
            self.assertIn(p['base'],phone_map.POINTS)
            self.assertEqual(character_types.kind(p['name']),character_types.TOWN)
            self.assertNotIn(p['name'],s['routes'])
            gid=groups.open_local(s,p['name']); self.assertEqual(s['groups'][gid]['local'],p['name'])
            groups.close_active(s,'Leaving'); town.travel(s,'square')
            self.assertNotIn(p['name'],s['world']['npcs'])

    def test_named_cast_meetings_physical_presence_and_clearance(self):
        s=core.fresh('ivan'); m=dip.book(s,'dragons',2520)
        self.assertEqual(m['attendee'],'garrett'); self.assertEqual(m['venue'],'syndicate')
        place(s,m['venue'],2519); town.loop.advance(s,1)
        self.assertEqual(s['world']['cast']['garrett']['location'],m['venue'])
        gid=dip.begin(s,m['id']); self.assertEqual(s['groups'][gid]['members'],['garrett'])
        from hangout_ui import current_exchange
        self.assertEqual(current_exchange(s,s['groups'][gid]).speeches[0][0],'garrett')
        with self.assertRaises(ValueError): dip.conclude(s,m['id'],'measured')
        for _ in range(3): dip.discuss(s,m['id'])
        self.assertEqual(m['agenda_index'],3)
        dip.conclude(s,m['id'],'relations'); self.assertEqual(m['status'],'completed')
        self.assertEqual(dip.book(s,'syndicate',3960)['attendee'],'crow')
        outsider=core.fresh('garrett')
        for target in ('syndicate','shinokami'):
            with self.assertRaises(ValueError): dip.book(outsider,target,2520)
        with self.assertRaises(ValueError): dip.book(s,'syndicate',2640) # Sunday council

    def test_timer_departure_and_save_resume(self):
        s=core.fresh('garrett'); m=dip.book(s,'purple',2520)
        place(s,m['venue'],2520); dip.begin(s,m['id']); dip.discuss(s,m['id'])
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'meeting.json'; core.save(s,path); s=core.load(path)
        m=dip.commitments(s)[0]
        self.assertEqual(m['agenda_index'],1); dip.discuss(s,m['id'])
        groups.close_active(s,'Left meeting')
        with self.assertRaises(ValueError): dip.discuss(s,m['id'])
        s['world']['minute']=m['end']; dip.tick(s)
        self.assertEqual(m['status'],'missed')
        before=copy.deepcopy(s['crime_diplomacy']); dip.tick(s)
        self.assertEqual(before,s['crime_diplomacy'])

    def test_takeo_receives_meeting_at_hq_without_number_leak(self):
        import crime_operations, takeo
        s=core.fresh('garrett')
        crime_operations.data(s)['permits']['site_01']={'until':4000}
        m=dip.book(s,'shinokami',2520)
        self.assertEqual(m['attendee'],'takeo')
        jobs.travel(s,m['venue']); self.assertEqual(s['world']['location'],'site_01')
        jobs.travel(s,m['venue']); self.assertEqual(s['world']['location'],'site_01_reception')
        jobs.travel(s,m['venue']); self.assertEqual(s['world']['location'],takeo.HQ)
        s['world']['minute']=2519; town.loop.advance(s,1)
        gid=dip.begin(s,m['id'])
        self.assertEqual(s['groups'][gid]['members'],['takeo'])
        self.assertFalse(phone_numbers.saved_number(s,'takeo'))
        self.assertEqual(s['world']['cast']['takeo']['location'],takeo.HQ)

    def test_town_dialogue_reputation_and_agenda_context(self):
        s=core.fresh('garrett'); m=dip.book(s,'lantern',2520)
        place(s,m['venue'],2520); dip.begin(s,m['id']); name=m['attendee']
        result=dict(narration='The meeting continues.',lines=[dict(speaker=name,text='We should leave him out of this.')],
                    emotions={'garrett':'content',name:'guarded'})
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(result)}}) as request:
            town_npc_system.generate(s,[name],{'player_reply':'What about Sylvanis?'})
        payload=json.loads(request.call_args.args[1]['messages'][1]['content'])
        profile=payload['residents'][name]
        self.assertIn('most dangerous man',profile['Underworld reputation'])
        self.assertEqual(profile['Gang leadership']['meeting']['agenda'],m['agenda'])

    def test_legacy_meeting_migration_preserves_date(self):
        s=core.fresh('garrett'); b=dip.ensure(s)
        m=dict(id='legacy',target='rojos',start=2520,end=2580,venue='market',representative='anonymous executive',
               leader=False,status='booked',reminded=False,title='Private leadership appointment')
        b['meetings'].append(m); dip.tick(s)
        self.assertEqual(m['attendee'],'Isabel Vega'); self.assertEqual(m['start'],2520)
        self.assertEqual(m['venue'],'rojos_courtyard'); self.assertEqual(len(m['agenda']),3)


if __name__=='__main__': unittest.main()
