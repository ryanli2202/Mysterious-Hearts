import copy, json, threading, unittest
from pathlib import Path
from unittest.mock import patch
import autonomy, camera, codex_images, game_core as core, grove_photos, message_photos as photos
from messages_ui import text_messages

class IncomingPhotoTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei'); self.s['active']='emily'
        self.job=dict(who='emily',key='emily',group=False,reason=None)
        self.result=dict(moment='none',pause_minutes=0)

    def test_frequency_and_persistent_cooldown(self):
        bond=self.s['relationships']['emily']
        for trust,close,expected in [(35,0,(.04,4320)),(50,25,(.12,1440)),(70,55,(.25,720))]:
            bond.update(trust=trust,closeness=close)
            self.assertEqual(photos.frequency(self.s,'emily'),expected)
        with patch.object(autonomy,'chance',return_value=0):
            photos.schedule(self.s,self.job,self.result)
            photos.schedule(self.s,self.job,self.result)
        data=photos.ensure(self.s); self.assertEqual(len(data['pending']),1)
        restored=json.loads(json.dumps(self.s)); photos.ensure(restored)['pending'].clear()
        with patch.object(autonomy,'chance',return_value=0): photos.schedule(restored,self.job,self.result)
        self.assertFalse(photos.ensure(restored)['pending'])

    def test_silence_pause_and_setback_never_schedule(self):
        with patch.object(autonomy,'chance',return_value=0):
            for job,result in [(dict(self.job,reason={'kind':'silence'}),self.result),
                               (self.job,dict(self.result,pause_minutes=60)),
                               (self.job,dict(self.result,moment='setback'))]:
                photos.schedule(self.s,job,result)
        self.assertFalse(photos.ensure(self.s)['pending'])

    def test_worker_errors_wait_for_retry_and_old_save_results_are_ignored(self):
        from types import SimpleNamespace
        with patch.object(autonomy,'chance',return_value=0): photos.schedule(self.s,self.job,self.result)
        job=photos.ensure(self.s)['pending'][0]
        game=SimpleNamespace(state_data=self.s,in_game=True,bind=lambda *a,**kw:None,
                             persist=lambda:None,render=lambda:None)
        pump=photos.PhotoPump(game)
        pump.running=(self.s,job['id'],threading.Event())
        pump.results.put((self.s,job['id'],None,'failed'))
        with patch.object(grove_photos,'generate') as generate:
            pump.tick(); pump.tick()
            generate.assert_not_called()
        self.assertIn('error',job)
        pump.retry(); self.assertNotIn('error',job)
        old=self.s; game.state_data=core.fresh('rei')
        pump.running=(old,job['id'],threading.Event())
        pump.results.put((old,job['id'],{'text':'stale'},None))
        pump.tick()
        self.assertFalse(photos.ensure(game.state_data)['pending'])
        self.assertNotIn('result',job)

    def test_codex_generation_and_attachment_delivery(self):
        with patch.object(autonomy,'chance',return_value=0): photos.schedule(self.s,self.job,self.result)
        job=photos.ensure(self.s)['pending'][0]
        plan=dict(caption='look at this',scene='A blue ceramic cup on a table.',selfie=False)
        path=codex_images.STORE/'test-message-photo.png'
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(plan)}}) as request, \
             patch.object(codex_images,'generate',return_value={'path':str(path)}) as generate, \
             patch.object(Path,'is_file',return_value=True):
            result=grove_photos.generate(self.s,job,threading.Event())
        generate.assert_called_once()
        self.assertIn('privately',request.call_args.args[1]['messages'][0]['content'])
        self.assertNotIn('public Grove photo',request.call_args.args[1]['messages'][0]['content'])
        with patch('PIL.Image.open'):
            self.assertTrue(photos.commit(self.s,job,result))
            self.assertFalse(photos.commit(self.s,job,result))
        saved=json.loads(json.dumps(self.s))
        message=text_messages(saved)[-1]
        self.assertEqual(message[2],'in')
        self.assertEqual(message[6]['path'],result['image'])
        self.assertIn(plan['scene'],message[1])
        self.assertEqual(saved['routes']['emily']['unread'],1)
        self.assertFalse(photos.ensure(saved)['pending'])

if __name__=='__main__': unittest.main()
