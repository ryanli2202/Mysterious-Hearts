import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import uuid
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PIL import Image
import codex_images as bridge


class ImageBridgeTests(unittest.TestCase):
    def setUp(self):
        temporary_root = bridge.ROOT / '.test-tmp'
        temporary_root.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=temporary_root)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.store_patch = patch.object(bridge, 'STORE', self.root / 'library')
        self.store_patch.start()
        self.addCleanup(self.store_patch.stop)
        self.env_patch = patch.dict(os.environ, {'CODEX_HOME': str(self.root / 'codex')})
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

    def image_result(self, folder, valid=True):
        thread_id = str(uuid.uuid4())
        source = self.root / 'codex' / 'generated_images' / thread_id / 'original.png'
        source.parent.mkdir(parents=True)
        if valid:
            Image.new('RGB', (32, 32), 'blue').save(source)
        else:
            source.write_text('not an image')
        (folder / 'result.json').write_text(json.dumps(dict(status='complete', path=str(source), error='')))
        output = json.dumps({'type': 'thread.started', 'thread_id': thread_id})
        return output, source

    def test_environment_removes_keys_without_changing_parent(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'secret', 'CODEX_API_KEY': 'secret',
                                     'OPENAI_BASE_URL': 'https://other', 'OTHER_API_KEY': 'secret'}):
            env = bridge.subscription_env()
            self.assertNotIn('OPENAI_API_KEY', env)
            self.assertNotIn('CODEX_API_KEY', env)
            self.assertNotIn('OPENAI_BASE_URL', env)
            self.assertNotIn('OTHER_API_KEY', env)
            self.assertEqual(os.environ['OPENAI_API_KEY'], 'secret')

    def test_rejects_api_login(self):
        with patch.object(bridge.subprocess, 'run', return_value=Mock(
                returncode=0, stdout='', stderr='Logged in using an API key')):
            with self.assertRaisesRegex(bridge.ImageJobError, 'API-key login is not accepted'):
                bridge.check_login('codex')

    def test_accepts_chatgpt_login(self):
        with patch.object(bridge.subprocess, 'run', return_value=Mock(
                returncode=0, stdout='', stderr='Logged in using ChatGPT')):
            self.assertEqual(bridge.check_login('codex'), 'codex')

    def test_command_enforces_subscription_and_disables_shell(self):
        args = bridge.command('codex', self.root)
        self.assertIn('forced_login_method="chatgpt"', args)
        self.assertIn('--ignore-user-config', args)
        for feature in ('shell_tool', 'apps', 'plugins', 'hooks', 'multi_agent'):
            i = args.index(feature)
            self.assertEqual(args[i - 1], '--disable')
        self.assertEqual(args[args.index('--sandbox') + 1], 'read-only')

    def test_import_decodes_current_job_image(self):
        output, source = self.image_result(self.root)
        path = bridge.import_result(self.root, output, time.time() - 1)
        self.assertTrue(source.exists())
        with Image.open(path) as im:
            self.assertEqual(im.size, (32, 32))
            self.assertEqual(im.format, 'PNG')

    def test_rejects_image_from_another_job(self):
        output, _ = self.image_result(self.root)
        output = json.dumps({'type': 'thread.started', 'thread_id': str(uuid.uuid4())})
        with self.assertRaisesRegex(bridge.ImageJobError, 'outside this request'):
            bridge.import_result(self.root, output, time.time() - 1)

    def test_rejects_invalid_and_stale_images(self):
        output, source = self.image_result(self.root, valid=False)
        with self.assertRaises(OSError):
            bridge.import_result(self.root, output, time.time() - 1)
        Image.new('RGB', (32, 32)).save(source)
        os.utime(source, (10, 10))
        with self.assertRaisesRegex(bridge.ImageJobError, 'stale'):
            bridge.import_result(self.root, output, time.time())

    def test_generation_imports_and_persists_without_retry(self):
        proc = Mock(returncode=0)
        proc.poll.return_value = 0
        def launch(args, **kwargs):
            folder = Path(args[args.index('-C') + 1])
            output, _ = self.image_result(folder)
            proc.communicate.return_value = (output, '')
            return proc
        with patch.object(bridge, 'check_login', return_value='codex'), patch.object(
                bridge.subprocess, 'Popen', side_effect=launch) as run:
            item = bridge.generate('A blue mug')
        self.assertEqual(item['status'], 'complete')
        self.assertTrue(Path(item['path']).exists())
        self.assertEqual(bridge.library()[0]['prompt'], 'A blue mug')
        self.assertEqual(run.call_count, 1)

    def test_failure_never_retries_or_imports(self):
        proc = Mock(returncode=1)
        proc.poll.return_value = 1
        proc.communicate.return_value = ('', 'usage limit')
        with patch.object(bridge, 'check_login', return_value='codex'), patch.object(
                bridge.subprocess, 'Popen', return_value=proc) as run:
            with self.assertRaisesRegex(bridge.ImageJobError, 'No paid API fallback'):
                bridge.generate('A blue mug')
        self.assertEqual(run.call_count, 1)
        self.assertEqual(bridge.library(), [])
        record = json.loads(next(bridge.STORE.glob('*/job.json')).read_text())
        self.assertEqual(record['status'], 'failed')

    def test_cancel_stops_worker_and_releases_lock(self):
        cancel = threading.Event()
        proc = Mock()
        def waiting(*args, **kwargs):
            cancel.set()
            raise subprocess.TimeoutExpired('codex', 0.5)
        proc.communicate.side_effect = waiting
        with patch.object(bridge, 'check_login', return_value='codex'), patch.object(
                bridge.subprocess, 'Popen', return_value=proc), patch.object(bridge, 'stop_process') as stop:
            with self.assertRaisesRegex(bridge.ImageJobError, 'cancelled'):
                bridge.generate('A blue mug', cancel)
        stop.assert_called_once_with(proc)
        self.assertFalse(bridge._generation_lock.locked())

    def test_rejects_duplicate_and_empty_requests(self):
        with self.assertRaises(bridge.ImageJobError):
            bridge.generate(' ')
        bridge._generation_lock.acquire()
        try:
            with self.assertRaisesRegex(bridge.ImageJobError, 'already generating'):
                bridge.generate('A mug')
        finally:
            bridge._generation_lock.release()


if __name__ == '__main__':
    unittest.main()
