import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import chatgpt_provider as p
import game_core as c

class AccountTests(unittest.TestCase):
    def test_settings_default_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(p,'SETTINGS',Path(folder)/'settings.json'):
                self.assertEqual(p.settings()['provider'],'lu')
                p.save_settings('chatgpt','available-model')
                self.assertEqual(p.settings(),{'provider':'chatgpt','model':'available-model'})
                p.save_settings('ollama')
                self.assertEqual(p.settings()['provider'],'ollama')

    def test_chatgpt_routes_without_ollama_or_key(self):
        body={'messages':[{'role':'system','content':'story'}],'format':{'type':'object'}}
        with patch.object(p,'settings',return_value={'provider':'chatgpt','model':'chosen-model'}), patch.object(p.bridge,'call',return_value={'text':'{"dialogue":"hello"}'}) as rpc:
            result=c.request('/api/chat',body)
            self.assertEqual(result['message']['content'],'{"dialogue":"hello"}')
            self.assertEqual(rpc.call_args.args[1]['model'],'chosen-model')
            self.assertEqual(rpc.call_args.args[1]['messages'],body['messages'])

    def test_sign_in_alone_does_not_enable_generation(self):
        with patch.object(p,'settings',return_value={'provider':'chatgpt','model':'chosen-model'}), patch.object(p.bridge,'call',return_value={'status':'connected','sharing':False}):
            with self.assertRaisesRegex(RuntimeError,'enable plan usage'): c.check_model()

    def test_cloud_error_does_not_fall_back(self):
        with patch.object(p,'settings',return_value={'provider':'chatgpt','model':'chosen-model'}), patch.object(p.bridge,'call',side_effect=RuntimeError('Usage limit reached')):
            with self.assertRaisesRegex(RuntimeError,'Usage limit'): c.request('/api/chat',{'messages':[],'format':{}})

    def test_generation_retries_a_busy_credential_store_once(self):
        with patch.object(p, 'settings', return_value={'model': 'chosen-model'}), patch.object(
                p.bridge, 'call', side_effect=[p.StorageBusy('busy'), {'text':'ready'}]) as rpc:
            result = p.generate({'messages': [], 'format': {}})
        self.assertEqual(result['message']['content'], 'ready')
        self.assertEqual(rpc.call_args_list, [rpc.call_args, rpc.call_args])

if __name__=='__main__': unittest.main()
