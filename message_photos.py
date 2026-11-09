"""Occasional, newly generated private photos; independent of text generation."""
import copy
import json
import queue
import threading


def ensure(s):
    return s.setdefault('message_photos', dict(pending=[], last={}, serial=0))


def frequency(s, who):
    import messaging
    return {4: (.04, 3*1440), 2: (.12, 1440), 1: (.25, 720)}[messaging.followup_spacing(s, who)]


def schedule(s, job, result):
    import autonomy
    import messaging
    import grove
    if job['group'] or (job.get('reason') or {}).get('kind') == 'silence': return
    if result.get('pause_minutes', 0) or result.get('moment') == 'setback': return
    who = job['who']
    if who not in grove.BIOS: return
    data = ensure(s); now = s['world']['minute']
    chance, cooldown = frequency(s, who)
    if len(data['pending']) >= 3 or any(p['author'] == who for p in data['pending']): return
    if now-data['last'].get(who, -10**9) < cooldown: return
    # Stable per delivered reply, so saving/reloading cannot reroll the same exchange.
    history = s['routes'][who]['history']
    if autonomy.chance('message-photo', s['player'], who, now, len(history)) >= chance: return
    data['serial'] += 1
    recent = [line['photo'].get('description', '') for line in history if line.get('photo', {}).get('author') == who][-5:]
    data['pending'].append(dict(id=data['serial'], author=who, private_message=True,
                               conversation=[dict(role=l.get('role'), content=l.get('content')) for l in history[-8:]],
                               recent_photos=recent, minute=now))
    data['last'][who] = now


def commit(s, job, result):
    import camera
    import game_core as core
    import messaging
    import story_calendar
    from PIL import Image
    data = ensure(s)
    pending = next((p for p in data['pending'] if p['id'] == job['id']), None)
    if pending is None: return False
    who = job['author']; now = s['world']['minute']
    record = dict(id=f'message-photo:{job["id"]}', author=who, path=result['image'],
                  minute=job['minute'], date=story_calendar.story_date(job['minute']).isoformat(),
                  mode=result['photo_context']['mode'], location='Shared privately',
                  description=result['photo_context']['detail'])
    with Image.open(camera.photo_path(record)) as image: image.verify()
    text = result['text'] + '\n[Photo: ' + record['description'] + ']'
    route = s['routes'][who]
    route['history'].append(dict(role='assistant', channel='text', minute=now, photo=record,
                                content=json.dumps(dict(dialogue=text, narration='Incoming photo.', memory=route.get('memory',''), choices=[], suggestions_deferred=True), ensure_ascii=False)))
    route['dialogue'] = text
    route['unread'] = route.get('unread', 0)+1
    messaging.mark_inbox_activity(s, route)
    messaging.thread(s, who)['last_reply'] = now
    data['last'][who] = now
    data['pending'].remove(pending)
    return True


class PhotoPump:
    def __init__(self, game):
        self.game = game
        self.results = queue.Queue()
        self.running = None
        game.bind('<Destroy>', self.destroy, add='+')

    def destroy(self, event):
        if event.widget is self.game and self.running: self.running[2].set()

    def retry(self):
        for job in ensure(self.game.state_data)['pending']: job.pop('error', None)
        self.game.persist()

    def tick(self):
        import codex_images
        import grove_photos
        import messaging
        game = self.game; s = game.state_data
        if self.running and (self.running[0] is not s or not game.in_game): self.running[2].set()
        try:
            origin, ident, result, error = self.results.get_nowait()
        except queue.Empty:
            pass
        else:
            cancelled = self.running and self.running[2].is_set()
            self.running = None
            if origin is s and game.in_game and not cancelled:
                job = next((p for p in ensure(s)['pending'] if p['id'] == ident), None)
                if job is not None:
                    if error: job['error'] = 'Photo generation failed. Use Retry incoming photos to try again.'
                    else: job['result'] = result
                    game.persist()
        if not game.in_game or s is None: return
        data = ensure(s)
        for job in list(data['pending']):
            who = job['author']; t = messaging.thread(s, who)
            if job.get('error') or not job.get('result'): continue
            if not messaging.available(s, who) or t['error'] or s['world']['minute'] < t['muted_until']: continue
            try:
                commit(s, job, job['result'])
            except (OSError, ValueError, KeyError):
                job.pop('result', None)
                job['error'] = 'Generated photo could not be loaded. Use Retry incoming photos.'
            game.persist(); game.render()
        if self.running or codex_images._generation_lock.locked(): return
        camera_jobs = getattr(game, 'camera_jobs', None)
        if camera_jobs and camera_jobs.cancel_event: return
        job = next((p for p in data['pending'] if not p.get('error') and not p.get('result')
                    and not messaging.thread(s,p['author'])['error']), None)
        if job is None: return
        snapshot = copy.deepcopy(s); captured = copy.deepcopy(job)
        cancel = threading.Event(); self.running = (s, job['id'], cancel)
        def work():
            try:
                result = grove_photos.generate(snapshot, captured, cancel)
                self.results.put((s, captured['id'], result, None))
            except Exception as exc:
                self.results.put((s, captured['id'], None, str(exc)))
        threading.Thread(target=work, daemon=True).start()
