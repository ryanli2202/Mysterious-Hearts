import copy
from pathlib import Path
import tempfile
import unittest

import game_core as core
import groups
import story_calendar as dates
import town
from date_fixtures import finish_date, invite


class MemoryTests(unittest.TestCase):
    def test_hangout_kiss_and_witness_memories(self):
        s = core.fresh('rei')
        town.summon(s, 'emily'); town.summon(s, 'sophie')
        gid = s['active_group']
        members = s['groups'][gid]['members']
        scene = dict(narration='Emily and Rei share a kiss under the lanterns.',
                     choices=['Stay?', 'Coffee?', 'Ready?', 'Thanks.'], kissed_contact='emily',
                     lines=[dict(speaker=core.CONTACTS[m][0],text='Hey.') for m in members])
        groups.commit(s,gid,'I lean closer.',scene)
        self.assertIn('kiss', s['relationships']['emily']['firsts'])
        groups.disband(s)
        for who in ('emily','sophie','amy'):
            s['active'] = who
            system = core.build_messages(s, 'Remember the lanterns?')[0]['content']
            self.assertEqual('share a kiss under the lanterns' in system, who in members)

    def test_solo_text_recalls_only_participating_groups_and_events(self):
        s = core.fresh('rei')
        gid = groups.create_text(s, 'Weekend plans', ['emily', 'sophie'])
        data = dict(narration='A message arrives.', choices=['Yes.', 'Maybe.', 'When?', 'Where?'],
                    lines=[dict(speaker='Emily Fields',text='Bring the blue origami crane.'),
                           dict(speaker='Sophie Parker',text='I’ll bring paper.')])
        groups.commit(s, gid, 'What should I bring?', data)
        s['world']['party'] = ['emily']
        dates.celebrate(s, 'New Year’s Day')
        for who, crane, celebration in [('emily', True, True), ('sophie', True, False), ('amy', False, False)]:
            s['active'] = who
            system = core.build_messages(s, 'What did we plan?')[0]['content']
            self.assertEqual('blue origami crane' in system, crane)
            self.assertEqual('wish cards flutter' in system, celebration)

    def test_firsts_survive_repetition_and_reload(self):
        s = core.fresh('rei')
        town.travel(s, 'flowers'); town.finish_drive(s); town.meet(s, 'emily')
        finish_date(s, 'emily')
        first_date = s['relationships']['emily']['firsts']['date']
        finish_date(s, 'emily')
        invite(s, 'emily', 'official')
        scene = dict(narration='They kiss.', dialogue='Hey.', memory='A shared kiss.',
                     choices=['Hi.', 'Want to stay?', 'Okay.', 'Coffee?'], romance_event='kiss')
        core.commit(s,'I lean closer.',scene)
        firsts = copy.deepcopy(s['relationships']['emily']['firsts'])
        core.commit(s,'One more?',scene)
        self.assertEqual(firsts['date'], first_date)
        self.assertEqual(set(firsts), {'date','kiss','official'})
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'game.json'
            core.save(s,path)
            self.assertEqual(core.load(path)['relationships']['emily']['firsts'], firsts)
        other = core.fresh('rei')
        core.commit(other, 'Sending a kiss emoji.', scene)
        self.assertNotIn('firsts',other['relationships']['emily'])
