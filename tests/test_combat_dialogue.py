import copy
import unittest
from unittest.mock import patch
import game_core as core
import combat
import combat_dialogue as dialogue


class DialogueTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('garrett')
        self.s['world']['location']='park'
        for who in ('garrett','rei','emily','samantha'):
            self.s['world']['cast'][who].update(location='park',journey=None)

    def reply(self,who,kind,accepted=True,art=None):
        with patch.object(combat,'ask_ai',return_value=dict(dialogue='Stay back.' if kind=='attack' else 'All right.',narration='She steps back.',accepted=accepted)):
            return dialogue.generate(copy.deepcopy(self.s),who,kind,art)

    def test_acceptance_then_fight(self):
        result=self.reply('rei','spar')
        self.assertIsNone(combat.active(self.s))
        dialogue.commit(self.s,result)
        self.assertEqual(combat.active(self.s)['kind'],'spar')

    def test_dynamic_refusal(self):
        dialogue.commit(self.s,self.reply('rei','spar',False))
        self.assertIsNone(combat.active(self.s))
        self.assertNotIn('rei',combat.ensure(self.s)['ruptures'])

    def test_emily_flees_and_breaks_up(self):
        self.s['relationships']['emily']['status']='official'
        dialogue.commit(self.s,self.reply('emily','attack'))
        self.assertIsNone(combat.active(self.s))
        self.assertFalse(combat.present(self.s,'emily'))
        self.assertEqual(self.s['relationships']['emily']['status'],'exes')
        self.assertEqual(self.s['relationships']['emily']['trust'],0)
        self.assertTrue(self.s['relationships']['emily']['breakups'])

    def test_samantha_fights_and_loses_trust(self):
        dialogue.commit(self.s,self.reply('samantha','attack'))
        self.assertEqual(combat.active(self.s)['opponent'],'samantha')
        self.assertIn('samantha',combat.ensure(self.s)['ruptures'])

    def test_lesson(self):
        minute=self.s['world']['minute']
        dialogue.commit(self.s,self.reply('rei','learn',art='Judo'))
        self.assertEqual(self.s['world']['minute'],minute+30)
        self.assertEqual(combat.profile(self.s,'garrett')['arts']['Judo'],3)

    def test_remote_and_stale_response(self):
        result=self.reply('rei','spar')
        self.s['world']['cast']['rei']['location']='cafe'
        with self.assertRaises(ValueError): dialogue.commit(self.s,result)
        with self.assertRaises(ValueError): self.reply('rei','attack')
        self.assertIsNone(combat.active(self.s))

    def test_invalid_ai_has_no_consequences(self):
        with self.assertRaises(ValueError): self.reply('emily','challenge')
        with patch.object(combat,'ask_ai',return_value={'accepted':'yes'}):
            with self.assertRaises(ValueError): dialogue.generate(self.s,'rei','spar')
        self.assertFalse(combat.ensure(self.s)['ruptures'])

    def test_response_cannot_apply_twice(self):
        result=self.reply('rei','spar',False)
        dialogue.commit(self.s,result)
        with self.assertRaises(ValueError): dialogue.commit(self.s,result)
        self.assertEqual(len(self.s['combat']['dialogue']),1)

    def test_failed_provider_does_not_attack(self):
        before=copy.deepcopy(self.s)
        with patch.object(combat,'ask_ai',side_effect=RuntimeError('offline')):
            with self.assertRaises(RuntimeError): dialogue.generate(copy.deepcopy(self.s),'emily','attack')
        self.assertEqual(self.s,before)

    def test_flee_closes_and_archives_dialogue(self):
        self.s['groups']['test']=dict(members=['emily'],history=[],open=True,channel='in_person')
        self.s['active_group']='test'
        dialogue.commit(self.s,self.reply('emily','attack'))
        self.assertIsNone(self.s['active_group'])
        self.assertFalse(self.s['groups']['test']['open'])
        self.assertTrue(any(row.get('text')=='Stay back.' for row in self.s['hangout_journal'][-1]['history']))

if __name__=='__main__': unittest.main()
