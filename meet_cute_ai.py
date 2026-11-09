"""Nonblocking replies using the game's existing configured dialogue provider."""
import copy
import queue
import threading
import meet_cute as app


class ReplyPump:
    def __init__(self, game):
        self.game = game
        self.results = queue.Queue()
        self.running = None

    def tick(self):
        game = self.game
        s = game.state_data
        try:
            origin, who, ident, result, error = self.results.get_nowait()
        except queue.Empty:
            pass
        else:
            self.running = None
            if origin is s:
                m = app.ensure(s)['matches'].get(who)
                if m and m['status']=='active' and m['pending'] and m['pending']['id']==ident:
                    if error:
                        m['pending']['error'] = 'Reply could not be generated. Check AI & account, then retry.'
                        app.ensure(s)['revision'] += 1
                    else:
                        app.commit_reply(s, who, ident, result)
                    game.persist()
        if not s or not game.in_game or game.busy or self.running or not s.get('meet_cute'): return
        for who,m in app.ensure(s)['matches'].items():
            p = m['pending']
            if m['status']!='active' or not p or p.get('error') or p['due']>app.now(s) or not app.awake(s,who): continue
            ident = p['id']
            snapshot = copy.deepcopy(s)
            self.running = (s, who, ident)
            def work(origin=s, target=who, serial=ident, state=snapshot):
                try: self.results.put((origin,target,serial,app.generate(state,target,serial),None))
                except Exception as exc: self.results.put((origin,target,serial,None,str(exc)))
            threading.Thread(target=work, daemon=True).start()
            break
