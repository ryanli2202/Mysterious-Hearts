import copy
import json
import unittest
from unittest.mock import patch

import dating
import game_core as core
import meet_cute as mc
import messaging
import romantic_voice as voice
import sexuality
import suggestions


class RomanticVoiceTests(unittest.TestCase):
    def setUp(self):
        provider=patch.object(core.chatgpt_provider,'settings',return_value={'provider':'ollama','model':''})
        provider.start();self.addCleanup(provider.stop)

    def test_whole_canonical_cast_has_distinct_voice_and_boundaries(self):
        self.assertEqual(set(voice.VOICES),set(sexuality.CANON))
        self.assertEqual(set(voice._DECLINES),set(mc.HOOKS))
        s=core.fresh('rei')
        for who in sexuality.CANON:
            with self.subTest(who=who):
                guide=dating.romantic_voice(s,who)
                self.assertIn(voice.VOICES[who][1],guide)
                self.assertIn('Sexuality, family boundaries, commitments, consent',guide)
                self.assertIn('Do not use flirt guidance for an incompatible pairing',guide)
                self.assertIn('not lines to recite',guide)
        self.assertIn('Keep sibling love familial',dating.romantic_voice(s,'yuriko'))

    def test_texts_and_suggestions_receive_participant_specific_guidance(self):
        s=core.fresh('rei');s['active']='garrett'
        s['routes']['garrett']['dialogue']='How was your day?'
        result=dict(choices_speaker=core.PLAYERS['rei'],choices=['Hello.','How are you?','Good to see you.','Coffee later?'])
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(result)}}) as request:
            suggestions.generate(s,('route','garrett'))
        prompt=request.call_args.args[1]['messages'][0]['content']
        self.assertIn(voice.VOICES['garrett'][1],prompt)
        self.assertIn('garrett: straight',prompt)
        self.assertIn('boundaries: []',prompt)
        s['groups']['test']=dict(channel='text',name='Friends',members=['garrett','amy'],history=[])
        job=dict(who='garrett',group=True,key='test',text='Want to date me?',ids=[],reason=None)
        with patch.object(core,'request',side_effect=RuntimeError('capture')) as request:
            with self.assertRaisesRegex(RuntimeError,'capture'):messaging.generate(s,job)
        prompt=request.call_args.args[1]['messages'][0]['content']
        self.assertIn(voice.VOICES['garrett'][1],prompt)
        self.assertIn(voice.VOICES['amy'][0],prompt)

    def test_meet_cute_free_replies_get_voice_without_changing_state(self):
        s=core.fresh('rei');s['world']['minute']=5000
        mc.publish(s,'Hello',['Drawing'],['A','B','C'],['portrait'],'Open to either','Evenings')
        m=mc._match(s,'lena','Hello',mc.ensure(s)['profile'])
        mc.send(s,'lena','Was that flirting?')
        before=copy.deepcopy(s)
        with patch.object(core,'request',return_value={'message':{'content':json.dumps({'text':'You noticed.'})}}) as request:
            self.assertEqual(mc.generate(s,'lena',m['pending']['id']),'You noticed.')
        prompt=request.call_args.args[1]['messages'][0]['content']
        self.assertIn(voice.VOICES['lena'][0],prompt)
        self.assertIn(voice.VOICES['lena'][1],prompt)
        self.assertIn('Repeated pressure warrants a firmer',prompt)
        self.assertEqual(s,before)

    def test_readiness_refusals_are_authored_and_still_decline(self):
        lines=[]
        for who in ('emily','samantha','april','lena'):
            s=core.fresh('rei');s['world']['minute']=5000
            mc.publish(s,'Hello',['Drawing'],['A','B','C'],['portrait'],'Open to either','Evenings')
            m=mc._match(s,who,'Hello',mc.ensure(s)['profile'])
            m['numbers']=False  # Exercise readiness even for initially known contacts.
            mc.request_numbers(s,who)
            mc.answer_proposal(s,m)
            self.assertEqual(m['proposal']['status'],'declined')
            self.assertFalse(m['numbers'])
            self.assertEqual(m['messages'][-1]['text'],voice.readiness_reply(who,'numbers'))
            lines.append(m['messages'][-1]['text'])
            m['proposal']=dict(kind='date',status='pending',start=6000)
            mc.answer_proposal(s,m)
            self.assertEqual(m['proposal']['status'],'declined')
            self.assertEqual(m['messages'][-1]['text'],voice.readiness_reply(who,'date'))
            self.assertFalse(m['dates'])
        self.assertEqual(len(set(lines)),len(lines))


if __name__=='__main__':unittest.main()
