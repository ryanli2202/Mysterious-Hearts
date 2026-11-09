import json
import unittest
from unittest.mock import patch
import game_core as core
import lu_provider as lu


class LUIntegrationTests(unittest.TestCase):
    def test_response_and_manual_suggestions_route_to_lu(self):
        from test_game import SCENE
        replies = {'choices_speaker': 'Garrett Han', 'choices': SCENE['choices']}
        replies['personal_choices'] = core.personal_choices(core.fresh(), {})
        scene = dict(SCENE, input_tone='Friendly', emotions={'garrett':'content', 'emily':'happy'}, bond_moments={'emily':'none'})
        with patch.object(core.chatgpt_provider, 'settings', return_value={'provider': 'lu', 'model': ''}), patch.object(lu, 'generate', side_effect=[
            {'message': {'content': json.dumps(scene)}},
            {'message': {'content': json.dumps(replies)}},
        ]) as generate:
            state=core.fresh()
            result=core.generate(state, 'Hello')
            self.assertEqual(result['dialogue'], SCENE['dialogue'])
            self.assertEqual(generate.call_count,1)
            core.commit(state,'Hello',result)
            import suggestions
            self.assertEqual(suggestions.generate(state,('route','emily')),SCENE['choices'])
            self.assertEqual(generate.call_count, 2)

    def test_rejects_other_loaded_model(self):
        with patch.object(lu, 'request', return_value={'data': [{'id': 'Qwen3.5-27B-abliterated.Q4_K_M.gguf'}]}):
            with self.assertRaisesRegex(RuntimeError, 'Load Qwen3.5-9B'):
                lu.check_model()

    def test_openai_compatible_schema_and_response(self):
        model = 'C:\\models\\' + lu.MODEL_FILE
        with patch.object(lu, 'request', side_effect=[
            {'data': [{'id': model}]},
            {'choices': [{'message': {'content': '{"ok":true}'}}]},
        ]) as request:
            result = lu.generate({'messages': [], 'format': {'type': 'object'}, 'options': {'temperature': 0.3, 'num_predict': 1500}})
            self.assertEqual(result['message']['content'], '{"ok":true}')
            path, body = request.call_args.args
            self.assertEqual(path, '/v1/chat/completions')
            self.assertEqual(body['model'], model)
            self.assertEqual(body['max_tokens'], 1500)
            self.assertFalse(body['chat_template_kwargs']['enable_thinking'])
            self.assertEqual(body['response_format']['json_schema']['schema'], {'type': 'object'})

    def test_token_protected_roundtrip(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory, patch.object(lu, 'TOKEN_FILE', Path(directory) / '.lu-token'), patch.dict(lu.os.environ, {'LU_API_TOKEN': ''}):
            lu.save_token('test-only-lu-token')
            self.assertNotIn(b'test-only-lu-token', lu.TOKEN_FILE.read_bytes())
            self.assertEqual(lu.get_token(), 'test-only-lu-token')
