"""Recover completed project reports from local rollouts, excluding media/tool/user data."""
import json
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def extract(path, thread, title, project=ROOT):
    records, started, completed, interrupted = [], set(), set(), set()
    malformed = 0
    with Path(path).open(encoding='utf-8') as stream:
        first = json.loads(next(stream))
        metadata = first.get('payload', {})
        if first.get('type') != 'session_meta' or Path(metadata.get('cwd', '')).resolve() != project.resolve():
            raise ValueError('Rollout does not belong to the requested project')
        if metadata.get('id') != thread:
            raise ValueError('Rollout thread ID mismatch')
        for line in stream:
            # Media-heavy tool responses can be enormous. Decode only small event records.
            prefix = line[:500]
            if '"event_msg"' not in prefix: continue
            if not any('"'+kind+'"' in prefix for kind in ('task_started','task_complete','turn_aborted')): continue
            try: event = json.loads(line)
            except ValueError:
                malformed += 1; continue
            payload = event.get('payload', {})
            turn = payload.get('turn_id') or payload.get('turn_attribution', {}).get('turn_id')
            if not turn: continue
            if payload.get('type') == 'task_started': started.add(turn)
            elif payload.get('type') == 'turn_aborted': interrupted.add(turn)
            elif payload.get('type') == 'task_complete':
                completed.add(turn)
                message = payload.get('last_agent_message')
                if isinstance(message, str) and message.strip():
                    records.append(dict(thread=thread,turn=turn,title=title,
                                        completed_at=datetime.fromisoformat(event['timestamp'].replace('Z','+00:00')).timestamp(),
                                        text=message,source='local rollout task_complete',
                                        source_file=Path(path).name,source_ordinal=event.get('ordinal')))
    return records, dict(started_turns=len(started),completed_turns=len(completed),
                         completed_without_report=len(completed-{r['turn'] for r in records}),
                         unfinished_turns=sorted(started-completed), interrupted_turns=sorted(interrupted),
                         malformed_events=malformed)


def main():
    archive=ROOT/'patch_notes'
    previous=json.loads((archive/'development_records.json').read_text(encoding='utf-8'))
    gaps=previous['gaps']
    if not gaps:
        raise SystemExit('No open retrieval gaps. Existing recovery evidence was left unchanged.')
    home=Path.home()/'.codex'
    targets={}
    for line in (home/'session_index.jsonl').open(encoding='utf-8'):
        record=json.loads(line)
        if record.get('thread_name') in gaps: targets[record['thread_name']]=record['id']
    paths=[p for folder in ('sessions','archived_sessions') for p in (home/folder).rglob('*.jsonl')]
    records=[]; manifest=[]
    for title in gaps:
        thread=targets.get(title)
        matches=[p for p in paths if thread and p.name.endswith('-'+thread+'.jsonl')]
        if len(matches)!=1: raise ValueError(f'Expected one rollout for {title}; found {len(matches)}')
        found,stats=extract(matches[0],thread,title)
        records.extend(found)
        manifest.append(dict(title=title,thread=thread,source_file=matches[0].name,**stats))
    known={(r['turn'],r['text']) for r in previous['records']}
    added=[r for r in records if (r['turn'],r['text']) not in known]
    result=dict(recovered_on='2026-11-07',scope='The 17 previously oversized project chats; complete local event scan. Only completed assistant reports extracted. No images, tool output, credentials or user messages copied.',
                chats=manifest,records=records,new_report_count=len(added))
    (archive/'recovered_history.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(chats=len(manifest),reports=len(records),new_reports=len(added),coverage=manifest),ensure_ascii=True))
    for r in added:
        print(json.dumps(dict(title=r['title'],turn=r['turn'],text=r['text']),ensure_ascii=True))


if __name__=='__main__': main()
