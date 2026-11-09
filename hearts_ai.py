"""Generate anonymous notes off the UI thread through the configured provider."""
import copy
import queue
import threading
import mysterious_hearts as hearts


class NotePump:
    def __init__(self, game):
        self.game = game
        self.results = queue.Queue()
        self.running = False

    def tick(self):
        game = self.game
        s = game.state_data
        try:
            origin, ident, text, error = self.results.get_nowait()
        except queue.Empty:
            pass
        else:
            self.running = False
            if origin is s:
                p = next((p for p in hearts.ensure(s)['pending'] if p['id'] == ident), None)
                if p:
                    if not hearts.request_current(s, p): hearts.ensure(s)['pending'].remove(p)
                    elif error: p['error'] = 'A note could not arrive. Check AI & account, then retry.'
                    else: hearts.commit_note(s, p, text)
                    game.persist()
        if not s or not game.in_game or game.busy or self.running: return
        for p in list(hearts.ensure(s)['pending']):
            if not hearts.request_current(s, p):
                hearts.ensure(s)['pending'].remove(p)
                continue
            if p.get('error'): continue
            snapshot, request = copy.deepcopy(s), copy.deepcopy(p)
            self.running = True
            def work(origin=s, state=snapshot, request=request):
                try: self.results.put((origin, request['id'], hearts.generate(state, request), False))
                except Exception: self.results.put((origin, request['id'], None, True))
            threading.Thread(target=work, daemon=True).start()
            break
