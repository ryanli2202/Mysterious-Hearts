import json
import tempfile
import unittest
from pathlib import Path
from tools.recover_patch_history import extract
import patch_notes as notes


class RecoveryTests(unittest.TestCase):
    def test_completion_only_excludes_user_media_and_interrupted_work(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); path=root/'log.jsonl'
            rows=[
                dict(type='session_meta',payload=dict(id='thread',cwd=str(root))),
                dict(type='event_msg',payload=dict(type='task_started',turn_id='done')),
                dict(type='response_item',payload=dict(type='message',role='user',content='private user data')),
                dict(type='response_item',payload=dict(type='function_call_output',output='binary media'*1000)),
                dict(type='event_msg',timestamp='2026-11-06T23:00:00Z',ordinal=8,payload=dict(type='task_complete',turn_id='done',last_agent_message='Completed feature.')),
                dict(type='event_msg',payload=dict(type='task_started',turn_id='stopped')),
                dict(type='event_msg',payload=dict(type='turn_aborted',turn_id='stopped')),
                dict(type='event_msg',payload=dict(type='task_started',turn_id='active')),
            ]
            path.write_text('\n'.join(json.dumps(r) for r in rows),encoding='utf-8')
            records,stats=extract(path,'thread','Example',root)
            self.assertEqual(len(records),1)
            self.assertEqual(records[0]['text'],'Completed feature.')
            self.assertEqual(records[0]['source_ordinal'],8)
            self.assertEqual(stats['unfinished_turns'],['active','stopped'])
            self.assertEqual(stats['interrupted_turns'],['stopped'])
            self.assertNotIn('private user data',json.dumps(records))
            with self.assertRaises(ValueError): extract(path,'other','Example',root)
            with self.assertRaises(ValueError): extract(path,'thread','Example',root/'other')

    def test_all_recovered_reports_and_chats_are_published(self):
        archive=notes.ROOT/'patch_notes'
        source=json.loads((archive/'recovered_history.json').read_text(encoding='utf-8'))
        raw=json.loads((archive/'development_records.json').read_text(encoding='utf-8'))
        entries={r['id']:r for r in notes.load()}
        self.assertEqual(len(source['chats']),17)
        self.assertEqual(len(source['records']),66)
        self.assertEqual(raw['gaps'],[])
        self.assertEqual(len(raw['resolved_gaps']),17)
        for report in source['records']:
            entry=entries['report-'+report['turn']]
            self.assertEqual(entry['body'],report['text'])
            self.assertEqual(entry['kind'],'Development report')
        for chat in source['chats']:
            self.assertIn('recovered-'+chat['thread'],entries)
            self.assertEqual(chat['malformed_events'],0)
            self.assertEqual(chat['completed_without_report'],0)
            for turn in chat['unfinished_turns']:
                self.assertNotIn('report-'+turn,entries)
        self.assertEqual(sum(c['completed_turns']==0 for c in source['chats']),3)


if __name__=='__main__':unittest.main()
