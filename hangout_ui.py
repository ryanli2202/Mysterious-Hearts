"""In-person conversations staged over the existing location and character artwork.

The scene is a view of the saved hangout, never a second conversation history.
Only the current exchange is on stage; the phone journal retains the full record.
"""
from dataclasses import dataclass, field
import re
import tkinter as tk
from tkinter import font as tkfont, ttk

import game_core as core
import suggestions
import winterfield_ui as ui
from artwork import ArtCanvas, scene_art


@dataclass(eq=True)
class Exchange:
    player: str = ''
    narration: str = ''
    speeches: list = field(default_factory=list)


def current_exchange(state, group, pending=None):
    """Respect session boundaries, speakers, physical actions and phone-only rows."""
    result = Exchange()
    members = group.get('members', [])
    speakers = {}
    for who in members:
        speakers[core.CONTACTS.get(who, (who,))[0]] = who
        speakers[core.contact_name(state, who)] = who
    player = core.PLAYERS[state['player']]
    for line in group.get('history', [])[group.get('journal_offset', 0):]:
        if line.get('channel') == 'text':
            continue
        speaker, text = line.get('speaker', ''), line.get('text', '')
        if speaker == 'Status update':
            result = Exchange()
        elif speaker in (player, player + ' (You)'):
            result = Exchange(narration=text) if line.get('kind') == 'action' else Exchange(player=text)
        elif speaker == 'Narrator':
            # A continuation can have no new player line. Do not repeat old speech.
            if result.speeches:
                result = Exchange()
            result.narration = text
        elif speaker in speakers:
            result.speeches.append((speakers[speaker], text))
    if pending and pending not in (*core.SCENE_DIRECTIONS, core.INCOMING_TEXT):
        result = (Exchange(narration=pending[len(core.ACTION_PREFIX):])
                  if pending.startswith(core.ACTION_PREFIX) else Exchange(player=pending))
    elif pending:
        result = Exchange()
    return result


def text_pages(text, measure, width, lines):
    """Wrap measured text without dropping long words, paragraphs or punctuation."""
    wrapped = []
    for paragraph in text.split('\n'):
        row = ''
        for word in re.findall(r'\S+', paragraph):
            if row and measure(row + ' ' + word) > width:
                wrapped.append(row)
                row = ''
            while measure(word) > width and len(word) > 1:
                cut = 1
                while cut < len(word) and measure(word[:cut + 1]) <= width:
                    cut += 1
                wrapped.append(word[:cut])
                word = word[cut:]
            row = (row + ' ' + word).strip()
        wrapped.append(row)
    return ['\n'.join(wrapped[i:i + lines]) for i in range(0, len(wrapped), lines)] or ['']


class HangoutCanvas(ArtCanvas):
    def __init__(self, parent, game):
        super().__init__(parent, 'ui-header', takefocus=True)
        self.game = game
        self.exchange = Exchange()
        self.members = []
        self.scene_key = None
        self.speech_index = 0
        self.page_indices = {'player': 0, 'speech': 0, 'narration': 0}
        self.pages = {}
        self.portraits = []
        self.portrait_items = {}
        self.bubble_bounds = {}
        self.speech_font = tkfont.Font(self, family='Segoe UI', size=12)
        self.name_font = tkfont.Font(self, family='Segoe UI', size=10, weight='bold')
        self.narration_font = tkfont.Font(self, family='Georgia', size=12, slant='italic')
        self.controls_height = 130
        self.page_controls = {}
        for kind in self.page_indices:
            bar = tk.Frame(self, bg=ui.PANEL)
            previous = ttk.Button(bar, text='‹', width=3,
                                  command=lambda k=kind: self.turn_page(k, -1))
            previous.pack(side='left')
            label = ttk.Label(bar, text='', anchor='center', width=8)
            label.pack(side='left')
            following = ttk.Button(bar, text='›', width=3,
                                   command=lambda k=kind: self.turn_page(k, 1))
            following.pack(side='left')
            item = self.create_window(0, 0, window=bar, state='hidden')
            self.page_controls[kind] = (item, previous, label, following)

    def show(self, group):
        state = self.game.state_data
        exchange = current_exchange(state, group, self.game.pending)
        key = (self.game.group_selected, group.get('journal_started'), group.get('journal_offset'))
        if key != self.scene_key or exchange != self.exchange:
            self.speech_index = 0
            self.page_indices = dict.fromkeys(self.page_indices, 0)
        self.scene_key, self.exchange = key, exchange
        self.members = list(group.get('members', []))
        world = state['world']
        self.artwork = scene_art(world['location'], minute=world['minute'])
        self.redraw()

    def turn_page(self, kind, delta):
        self.page_indices[kind] = max(0, min(len(self.pages.get(kind, [])) - 1,
                                             self.page_indices[kind] + delta))
        self.redraw()

    def turn_speaker(self, delta):
        if not self.exchange.speeches:
            return
        self.speech_index = (self.speech_index + delta) % len(self.exchange.speeches)
        self.page_indices['speech'] = 0
        self.redraw()
        self.master.update_voice_controls()

    def rounded_box(self, x, y, width, height, fill, outline):
        r = 15
        return self.create_polygon(
            x+r, y, x+width-r, y, x+width, y, x+width, y+r,
            x+width, y+height-r, x+width, y+height, x+width-r, y+height,
            x+r, y+height, x, y+height, x, y+height-r, x, y+r, x, y,
            smooth=True, splinesteps=16, fill=fill, outline=outline, width=1,
            tags='scene')

    def page(self, kind, text, width, lines, font):
        self.pages[kind] = text_pages(text, font.measure, max(40, width), lines)
        self.page_indices[kind] = min(self.page_indices[kind], len(self.pages[kind]) - 1)
        return self.pages[kind][self.page_indices[kind]]

    def pager(self, kind, x, y):
        item, previous, label, following = self.page_controls[kind]
        total = len(self.pages[kind])
        if total < 2:
            return
        index = self.page_indices[kind]
        self.coords(item, x, y)
        self.itemconfigure(item, state='normal')
        self.tag_raise(item)
        previous.configure(state='normal' if index else 'disabled')
        following.configure(state='normal' if index < total - 1 else 'disabled')
        label.configure(text=f'{index + 1} / {total}')

    def bubble(self, kind, name, text, x, y, width, anchor_x, anchor_y, lines):
        content = self.page(kind, text, width - 32, lines, self.speech_font)
        heading = text_pages(name, self.name_font.measure, width-32, 10)[0]
        speech_y = 20 + (heading.count('\n')+1)*self.name_font.metrics('linespace')
        height = speech_y + 15 + (content.count('\n') + 1) * self.speech_font.metrics('linespace')
        if len(self.pages[kind]) > 1:
            height += 32
        color, edge = ('#243c52', '#7bb7d9') if kind == 'player' else (ui.PANEL, ui.GOLD)
        self.rounded_box(x, y, width, height, color, edge)
        # A short tail points toward the actual portrait, including group speakers.
        tail_x = max(x + 22, min(x + width - 22, anchor_x))
        tip_x = tail_x + max(-32, min(32, anchor_x - tail_x))
        self.create_polygon(tail_x-9, y+height-1, tail_x+9, y+height-1,
                            tip_x, max(y+height+16, min(y+height+34, anchor_y)),
                            fill=color, outline=edge, tags='scene')
        self.create_line(tail_x-8, y+height-1, tail_x+8, y+height-1, fill=color, width=3, tags='scene')
        self.create_text(x+16, y+13, text=heading, anchor='nw', fill=edge,
                         font=self.name_font, tags='scene')
        self.create_text(x+16, y+speech_y, text=content, anchor='nw', fill=ui.CREAM,
                         font=self.speech_font, tags=('scene', kind+'-speech'))
        self.bubble_bounds[kind] = (x, y, x+width, y+height)
        self.pager(kind, x+width/2, y+height-18)

    def redraw(self, event=None):
        super().redraw(event)
        if not hasattr(self, 'exchange') or not self.game.state_data:
            return
        self.delete('scene')
        for item, *_ in self.page_controls.values():
            self.itemconfigure(item, state='hidden')
        self.bubble_bounds = {}
        w, h = self.winfo_width(), self.winfo_height()
        if w < 200 or h < 200:
            return
        state = self.game.state_data
        world = state['world']
        floor = h - self.controls_height - 112
        portrait_h = max(170, min(620, floor - 125))
        count = len(self.members)
        positions = {state['player']: w * .15}
        for i, who in enumerate(self.members):
            positions[who] = w * (.84 if count == 1 else .48 + .43 * i / max(1, count-1))
        self.portraits = []
        self.portrait_items = {}
        active = self.exchange.speeches[self.speech_index][0] if self.exchange.speeches else None
        for who, x in positions.items():
            cell = w * (.30 if who == state['player'] or count == 1 else min(.27, .52/count))
            x = max(cell/2+4, min(w-cell/2-4, x))
            positions[who] = x
            photo = self.game.portrait(who, (max(48, int(cell)//16*16), int(portrait_h)//16*16),
                                       world['location'], world['minute'])
            self.portraits.append(photo)
            item = self.create_image(x, floor, image=photo, anchor='s', tags='scene')
            self.portrait_items[who] = item
            # Clicking a group portrait selects that character's delivered line.
            self.tag_bind(item, '<Button-1>', lambda e, key=who: self.select_speaker(key))
            self.tag_bind(item, '<Button-3>', lambda e, key=who: self.game.open_profiles(key))
            name = core.contact_name(state, who) + (' · You' if who == state['player'] else '')
            if cell < 100:
                name = ''.join(part[0] for part in core.contact_name(state, who).split())
            width = min(cell + 20, max(95, len(name)*7+18))
            self.rounded_box(x-width/2, floor-1, width, 27, ui.PANEL,
                             ui.GOLD if who == active else ui.EDGE)
            self.create_text(x, floor+12, text=name, fill=ui.GOLD if who == active else ui.CREAM,
                             font=('Segoe UI', 9), width=width-8, tags='scene')
        bubble_y = 86
        bubble_width = min(380, w * .27)
        max_lines = max(2, min(8, int((floor - bubble_y - 135) / self.speech_font.metrics('linespace'))))
        if self.exchange.player:
            self.bubble('player', core.PLAYERS[state['player']] + ' · You', self.exchange.player,
                        w*.24, bubble_y, bubble_width, positions[state['player']], floor-portrait_h*.65, max_lines)
        if self.exchange.speeches:
            who, speech = self.exchange.speeches[self.speech_index]
            self.bubble('speech', core.contact_name(state, who), speech, w*.53, bubble_y,
                        bubble_width, positions[who], floor-portrait_h*.65, max_lines)
        narration = self.exchange.narration
        if not narration:
            narration = ('A response is being written…' if self.game.busy else
                         'You are here together. Say something, or choose an action.')
        content = self.page('narration', narration, w-360, 3, self.narration_font)
        self.create_rectangle(0, floor+32, w, h-self.controls_height, fill=ui.INK,
                              outline='', tags='scene')
        self.create_text(w/2, floor+67, text=content, justify='center', anchor='center',
                         font=self.narration_font, fill=ui.CREAM, tags=('scene', 'narration'))
        self.pager('narration', w-85, floor+70)
        self.master.position_controls()

    def select_speaker(self, who):
        for i, (key, _) in enumerate(self.exchange.speeches):
            if key == who:
                self.speech_index = i
                self.page_indices['speech'] = 0
                self.redraw()
                self.master.update_voice_controls()
                return


class HangoutView(tk.Frame):
    """Full-area art with compact controls; no transcript window in the scene."""
    def __init__(self, parent, game):
        super().__init__(parent, bg=ui.INK)
        self.game = game
        self.canvas = HangoutCanvas(self, game)
        self.canvas.pack(fill='both', expand=True)
        self.header = tk.Frame(self.canvas, bg=ui.PANEL, padx=12, pady=6)
        self.header_item = self.canvas.create_window(12, 12, anchor='nw', window=self.header)
        self.location = ttk.Label(self.header, font=('Segoe UI', 12, 'bold'), foreground=ui.GOLD, wraplength=230)
        self.location.pack(side='left', padx=(0, 18))
        self.voice = ttk.Label(self.header)
        self.voice.pack(side='left')
        self.previous_voice = ttk.Button(self.header, text='‹ Speaker', command=lambda:self.canvas.turn_speaker(-1))
        self.next_voice = ttk.Button(self.header, text='Speaker ›', command=lambda:self.canvas.turn_speaker(1))
        self.fullscreen = ttk.Button(self.header, text='Full screen', command=self.toggle_fullscreen)
        self.fullscreen.pack(side='right')
        ttk.Button(self.header, text='Journal', command=game.journal).pack(side='right', padx=4)
        self.combat_button=ttk.Button(self.header, text='Spar / fight / train', command=lambda:__import__('hangout_combat_ui').open_dialogue(game))
        self.combat_button.pack(side='right', padx=4)
        game.wardrobe_menu(self.header).pack(side='right', padx=4)
        self.controls = tk.Frame(self.canvas, bg=ui.PANEL, padx=14, pady=8)
        self.controls_item = self.canvas.create_window(0, 0, anchor='sw', window=self.controls)
        self.meeting_panel = tk.Frame(self.controls, bg=ui.PANEL)
        bar = tk.Frame(self.controls, bg=ui.PANEL)
        bar.pack(fill='x')
        self.mode = 'reply'
        self.reply_tab = ttk.Button(bar, text='Speak', command=lambda:self.set_mode('reply'))
        self.reply_tab.pack(side='left')
        self.action_tab = ttk.Button(bar, text='Actions', command=lambda:self.set_mode('action'))
        self.action_tab.pack(side='left', padx=4)
        game.panel_switch = ttk.Button(bar, text='Personal talk ›', command=game.toggle_panel)
        game.panel_switch.pack(side='left', padx=4)
        game.suggest_button = ttk.Button(bar, text='Suggest replies', command=lambda:game.request_suggestions('personal' if game.personal_panel else 'main'))
        game.suggest_actions = ttk.Button(bar, text='Suggest actions', command=lambda:game.request_suggestions('actions'))
        game.suggest_button.pack(side='left', padx=4)
        game.goal_button = ttk.Button(bar, command=game.show_date_goals)
        game.end_hangout_button = ttk.Button(bar, text='End hangout', command=game.end_hangout)
        game.end_hangout_button.pack(side='right')
        game.cancel_button = ttk.Button(bar, text='Cancel response', command=game.cancel_generation)
        game.retry = ttk.Button(bar, text='Continue hangout', command=game.retry_or_begin)
        game.retry.pack(side='right', padx=4)
        self.drawer = tk.Canvas(self.controls, height=1, highlightthickness=0, bg=ui.PANEL)
        self.drawer_scroll = ttk.Scrollbar(self.controls, command=self.drawer.yview)
        self.drawer.configure(yscrollcommand=self.drawer_scroll.set)
        self.drawer_body = tk.Frame(self.drawer, bg=ui.PANEL)
        self.drawer_window = self.drawer.create_window(0, 0, anchor='nw', window=self.drawer_body)
        self.drawer.bind('<Configure>', self.resize_drawer)
        self.drawer_body.bind('<Configure>', self.resize_drawer)
        game.reply_controls = tk.Frame(self.drawer_body, bg=ui.PANEL)
        game.action_panel = tk.Frame(self.drawer_body, bg=ui.PANEL)
        game.choices, game.action_choices = [], []
        for container, target, callback in ((game.reply_controls, game.choices, game.choose),
                                             (game.action_panel, game.action_choices, game.choose_action)):
            for i in range(4):
                button = tk.Button(container, command=lambda n=i, cb=callback:cb(n), anchor='w',
                    bg=ui.CARD, fg=ui.CREAM, activebackground=ui.EDGE, activeforeground=ui.CREAM,
                    disabledforeground=ui.MUTED, relief='flat', font=('Segoe UI', 10), padx=10, pady=5)
                button.pack(fill='x', pady=2)
                button.bind('<MouseWheel>', self.scroll_choices)
                target.append(button)
        self.composer = tk.Frame(self.controls, bg=ui.PANEL)
        self.composer.pack(fill='x', pady=(7, 3))
        game.entry = tk.Entry(self.composer, bg=ui.CARD, fg=ui.CREAM, insertbackground=ui.CREAM,
                             disabledbackground=ui.PANEL, disabledforeground=ui.MUTED,
                             font=('Segoe UI', 12), relief='flat')
        game.entry.bind('<Return>', lambda e:game.custom())
        game.send = ttk.Button(self.composer, text='Say', command=game.custom)
        game.action_entry = tk.Entry(self.composer, bg=ui.CARD, fg=ui.CREAM, insertbackground=ui.CREAM,
                                    disabledbackground=ui.PANEL, disabledforeground=ui.MUTED,
                                    font=('Segoe UI', 12), relief='flat')
        game.action_entry.bind('<Return>', lambda e:game.custom_action())
        game.action_send = ttk.Button(self.composer, text='Do action · 20 min', command=game.custom_action)
        game.status = tk.Label(self.controls, text=game.model_status, bg=ui.PANEL, fg=ui.MUTED,
                               font=('Segoe UI', 9), anchor='w')
        game.status.pack(fill='x')
        self.controls.bind('<Configure>', self.resize_controls)
        self.drawer.bind('<MouseWheel>', self.scroll_choices)
        self.drawer_stamp = None
        self.set_mode('reply')
        from hangout_combat_ui import HangoutCombat
        self.combat_actions=HangoutCombat(self)

    def position_controls(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.coords(self.controls_item, 0, h)
        self.canvas.itemconfigure(self.controls_item, width=w)
        self.canvas.itemconfigure(self.header_item, width=max(1, w-24))
        self.game.status.configure(wraplength=max(100, w-32))
        self.canvas.tag_raise(self.header_item)
        self.canvas.tag_raise(self.controls_item)

    def resize_controls(self, event=None):
        height = self.controls.winfo_reqheight()
        if height != self.canvas.controls_height:
            self.canvas.controls_height = height
            self.canvas.redraw()

    def resize_drawer(self, event=None):
        width = max(1, self.drawer.winfo_width())
        self.drawer.itemconfigure(self.drawer_window, width=width)
        for button in self.game.choices + self.game.action_choices:
            button.configure(wraplength=max(100, width-30))
        height = self.drawer_body.winfo_reqheight()
        self.drawer.configure(scrollregion=(0, 0, width, height), height=min(140, height))
        if self.drawer_scroll.winfo_manager():
            self.drawer_scroll.place_configure(height=min(140, height))

    def scroll_choices(self, event):
        self.drawer.yview_scroll(-1 if event.delta > 0 else 1, 'units')
        return 'break'

    def set_mode(self, mode):
        self.mode = mode
        g = self.game
        for widget in (g.entry, g.send, g.action_entry, g.action_send, g.suggest_button, g.suggest_actions):
            widget.pack_forget()
        action = mode == 'action'
        entry, send, suggest = ((g.action_entry, g.action_send, g.suggest_actions) if action else
                                (g.entry, g.send, g.suggest_button))
        send.pack(side='right', padx=(8, 0))
        entry.pack(side='left', fill='x', expand=True, ipady=8)
        suggest.pack(side='left', padx=4)
        self.reply_tab.configure(style='TButton' if action else 'Accent.TButton')
        self.action_tab.configure(style='Accent.TButton' if action else 'TButton')
        self.update_drawer()

    def update_drawer(self):
        g = self.game
        g.reply_controls.pack_forget()
        g.action_panel.pack_forget()
        group = g.state_data['groups'].get(getattr(g, 'group_selected', None), {})
        kind = 'actions' if self.mode == 'action' else 'personal' if g.personal_panel else 'main'
        choices = suggestions.visible(group, kind)
        stamp = (g.group_selected, kind, tuple(choices))
        if choices:
            container = g.action_panel if self.mode == 'action' else g.reply_controls
            container.pack(fill='x')
            self.drawer.pack(fill='x', before=self.composer, pady=(6, 0))
            self.drawer_scroll.place(relx=1, x=-4, y=42, anchor='ne', height=135)
            if stamp != self.drawer_stamp:
                self.drawer.yview_moveto(0)
        else:
            self.drawer.pack_forget()
            self.drawer_scroll.place_forget()
        self.drawer_stamp = stamp

    def toggle_fullscreen(self):
        self.set_fullscreen(not bool(self.game.attributes('-fullscreen')))

    def set_fullscreen(self, enabled):
        self.game.attributes('-fullscreen', enabled)
        self.fullscreen.configure(text='Exit full screen' if enabled else 'Full screen')

    def update_voice_controls(self):
        count = len(self.canvas.exchange.speeches)
        self.voice.configure(text=f'Voice {self.canvas.speech_index+1} / {count}' if count > 1 else 'In person')
        for button in (self.previous_voice, self.next_voice):
            button.pack_forget()
            if count > 1:
                button.pack(side='left', padx=3)

    def refresh(self, group):
        import combat
        offers=combat.pending_offers(self.game.state_data)
        self.combat_button.configure(text='Fight proposal · review' if offers else 'Spar / fight / train')
        import crime_diplomacy as dip
        for child in self.meeting_panel.winfo_children(): child.destroy()
        self.meeting_panel.pack_forget()
        s=self.game.state_data
        m=next((m for m in dip.commitments(s) if m.get('id')==group.get('leadership_meeting') and m['status']=='in_progress'),None)
        if m:
            from careers_ui import stamp
            self.meeting_panel.pack(fill='x',before=self.composer)
            index=m['agenda_index']; topic=m['agenda'][index] if index<len(m['agenda']) else 'Choose final terms'
            ttk.Label(self.meeting_panel,text=f"{stamp(m['start'])} · {m['representative']} · {max(0,m['end']-s['world']['minute'])} minutes left\nAgenda {min(index+1,len(m['agenda']))}/{len(m['agenda'])}: {topic}",wraplength=680).pack(anchor='w')
            if index==len(m['agenda']):
                ttk.Label(self.meeting_panel,text='Measured: $1,500 capital → $2,700 revenue, heat +3. Aggressive: $4,000 → $7,200, heat +12; fails at heat 40+.\nRelationship talks commit no funds. Deals must be completed separately within three days.',wraplength=780).pack(anchor='w')
            row=ttk.Frame(self.meeting_panel); row.pack(fill='x')
            actions=[('Review agenda · 10 min',dip.discuss,())] if index<len(m['agenda']) else [
                ('Relationship talks',dip.conclude,('relations',)),
                ('Measured deal · $1,500',dip.conclude,('measured',)),
                ('Aggressive deal · $4,000',dip.conclude,('aggressive',))]
            for title,fn,args in actions:
                ttk.Button(row,text=title,state='disabled' if self.game.busy else 'normal',
                    command=lambda f=fn,a=args,ident=m['id']:self.meeting_action(f,ident,*a)).pack(side='left',padx=3)
        self.location.configure(text=core.town.loop.place_name(self.game.state_data))
        self.canvas.show(group)
        self.update_voice_controls()
        self.update_drawer()
        if self.game.busy:
            self.game.retry.pack_forget()
            self.game.cancel_button.pack(side='right', padx=4)
        else:
            self.game.cancel_button.pack_forget()
            self.game.retry.pack(side='right', padx=4)
        self.combat_actions.refresh()

    def meeting_action(self,fn,ident,*args):
        if self.game.busy: return
        from phone_dialogs import messagebox
        try: fn(self.game.state_data,ident,*args)
        except ValueError as exc:
            messagebox.showinfo('Leadership meeting',str(exc),parent=self.game); return
        self.game.persist(); self.game.render(); self.game.show_in_person(hide_phone=False)
