"""Resolution-independent app icons drawn with native Tk shapes."""
import math
import tkinter as tk
import winterfield_ui as ui

COLORS = {'Mysterious Hearts': '#bb6288', 'Messages': '#43a483', 'Camera': '#596679', 'Gallery': '#a76e9a', 'Grove': '#418c68', 'Contacts': '#658ec7',
          'Weather': '#3985ba', 'Winterfield': '#ab8055', 'Maps': '#459dac', 'Calendar': '#d47785', 'Journal': '#b18b59',
          'Supafast': '#e5a044', 'Doober Eats': '#75a65b', 'Deliveries': '#9377b7',
          'Mini Games': '#7168bd', 'Settings': '#78869f', 'More': '#8e79ab', 'Notes': '#c6a761', 'Pinned messages': '#bc9561'}
COLORS.update({'Mixtape': '#38865e', 'Wardrobe': '#c17e9b', 'Out & About': '#cf8a58',
               'Pocket Wallet': '#4d9479', 'Winterfield Exchange': '#aa935b',
               'Recipe Box': '#bb7454', 'Postcards': '#5f91b5', 'Campus Portal': '#6e7db6'})
COLORS['Meet-Cute'] = '#cf697c'
COLORS.update({'Jobseek': '#326a88', 'Bubblegram': '#375f79'})


def unread_messages(state):
    return sum(r.get('unread', 0) for r in state.get('routes', {}).values()) + sum(
        g.get('unread', 0) for g in state.get('groups', {}).values() if g.get('channel') == 'text')


class AppIcon(tk.Canvas):
    def __init__(self, parent, name, command, size=82):
        super().__init__(parent, width=82, height=82, bg=ui.PANEL,
                         highlightthickness=2, highlightbackground=ui.PANEL,
                         highlightcolor=ui.GOLD, takefocus=True, cursor='hand2')
        color = COLORS[name]
        self.create_polygon(19, 2, 63, 2, 80, 2, 80, 19, 80, 63, 80, 80,
                            63, 80, 19, 80, 2, 80, 2, 63, 2, 19, 2, 2,
                            fill=color, smooth=True, splinesteps=24)
        ink = '#a4b8d0'
        def line(*points, **kw):
            return self.create_line(*points, fill=ink, width=3, capstyle='round', joinstyle='round', **kw)
        def oval(x1, y1, x2, y2, **kw):
            return self.create_oval(x1, y1, x2, y2, outline=ink, width=3, **kw)
        if name == 'Jobseek':
            self.create_rectangle(18, 30, 64, 61, outline=ink, width=3)
            line(31, 30, 31, 21, 51, 21, 51, 30); line(18, 42, 64, 42)
        elif name == 'Bubblegram':
            oval(16, 19, 66, 59); line(26, 55, 21, 68, 40, 59)
            line(28, 39, 53, 39)
        elif name == 'Meet-Cute':
            self.create_text(41, 38, text='♡', fill=ink, font=('Segoe UI', 39))
            line(26, 63, 36, 63); line(46, 63, 56, 63)
        elif name == 'Mixtape':
            line(32, 53, 32, 25, 56, 20, 56, 49)
            oval(20, 48, 32, 59, fill=ink); oval(44, 44, 56, 55, fill=ink)
        elif name == 'Wardrobe':
            self.create_arc(34, 18, 48, 32, start=0, extent=220, outline=ink, width=3, style='arc')
            line(41, 31, 41, 38, 17, 56, 65, 56, 41, 38)
        elif name == 'Out & About':
            self.create_rectangle(17, 25, 65, 58, outline=ink, width=3)
            line(48, 28, 48, 55, dash=(3, 3)); line(25, 37, 39, 37); line(25, 47, 36, 47)
        elif name == 'Pocket Wallet':
            self.create_rectangle(18, 27, 64, 60, outline=ink, width=3)
            line(18, 27, 55, 18, 55, 27)
            self.create_rectangle(47, 37, 67, 51, fill=color, outline=ink, width=3)
            oval(53, 42, 57, 46, fill=ink)
        elif name == 'Winterfield Exchange':
            line(19, 30, 61, 30, 52, 21); line(61, 52, 19, 52, 28, 61)
        elif name == 'Recipe Box':
            self.create_rectangle(21, 39, 61, 64, outline=ink, width=3)
            oval(21, 20, 40, 39); oval(33, 14, 51, 36); oval(45, 20, 63, 39)
            line(31, 50, 51, 50)
        elif name == 'Postcards':
            self.create_rectangle(15, 23, 67, 60, outline=ink, width=3)
            line(43, 28, 43, 55); line(49, 43, 60, 43); line(49, 51, 58, 51)
            line(20, 51, 28, 37, 37, 51); oval(23, 29, 28, 34)
        elif name == 'Campus Portal':
            line(16, 34, 41, 20, 66, 34, 41, 48, 16, 34)
            line(25, 40, 25, 54, 41, 62, 57, 54, 57, 40); line(66, 34, 66, 55)
        elif name == 'Mysterious Hearts':
            self.create_text(41, 40, text='♡', fill=ink, font=('Segoe UI', 40))
        elif name == 'Messages':
            self.create_polygon(19, 24, 63, 24, 63, 54, 37, 54, 24, 64, 26, 54, 19, 54,
                                fill=ink, smooth=True)
            for x in (30, 41, 52): self.create_oval(x-2, 37, x+2, 41, fill=color, outline='')
        elif name == 'Camera':
            self.create_rectangle(16, 28, 66, 61, outline=ink, width=3)
            line(24, 28, 29, 20, 47, 20, 53, 28)
            oval(29, 33, 53, 57)
            self.create_oval(57, 32, 61, 36, fill=ink, outline='')
        elif name == 'Gallery':
            self.create_rectangle(17, 19, 65, 64, outline=ink, width=3)
            self.create_oval(25, 27, 35, 37, fill=ink, outline='')
            line(19, 58, 34, 43, 44, 51, 53, 39, 64, 56)
        elif name == 'Weather':
            self.create_oval(22, 17, 51, 46, fill='#ffdc7a', outline='')
            self.create_oval(28, 34, 62, 61, fill=ink, outline='')
            self.create_oval(16, 40, 45, 61, fill=ink, outline='')
        elif name == 'Winterfield':
            self.create_rectangle(20, 18, 62, 64, outline=ink, width=3)
            line(28, 30, 54, 30); line(28, 41, 54, 41); line(28, 52, 46, 52)
        elif name == 'Grove':
            line(32, 61, 47, 25)
            self.create_polygon(38, 47, 32, 22, 60, 18, 59, 40, 38, 47, fill=ink, smooth=True)
            self.create_line(39, 43, 53, 27, fill=color, width=2)
            self.create_polygon(36, 53, 18, 41, 22, 30, 38, 42, 36, 53, fill='#8fbb9a', smooth=True)
        elif name == 'Contacts':
            oval(31, 20, 51, 40, fill=ink)
            self.create_arc(20, 43, 62, 80, start=0, extent=180, fill=ink, outline='')
            line(23, 62, 59, 62)
        elif name == 'Maps':
            self.create_polygon(15, 30, 32, 24, 50, 31, 67, 25, 67, 62, 50, 68, 32, 61, 15, 67,
                                fill='#84b59c', outline='')
            self.create_line(32, 26, 32, 60, 50, 66, 50, 33, fill=color, width=2)
            self.create_oval(32, 13, 58, 39, fill='#f18577', outline='')
            self.create_polygon(34, 33, 56, 33, 45, 50, fill='#f18577')
            self.create_oval(40, 21, 50, 31, fill=ink, outline='')
        elif name == 'Calendar':
            self.create_rectangle(20, 24, 62, 64, fill=ink, outline='')
            self.create_rectangle(20, 24, 62, 34, fill='#bf8096', outline='')
            line(29, 18, 29, 29); line(53, 18, 53, 29)
            for x in (29, 41, 53):
                for y in (43, 54): self.create_rectangle(x-2, y-2, x+2, y+2, fill=color, outline='')
        elif name in ('Journal', 'Notes'):
            self.create_rectangle(22, 17, 60, 65, outline=ink, width=3)
            line(30, 18, 30, 64)
            line(38, 29, 52, 29); line(38, 38, 52, 38); line(38, 47, 48, 47)
        elif name == 'Pinned messages':
            line(28, 22, 54, 22); line(33, 22, 33, 37, 24, 48, 58, 48, 49, 37, 49, 22)
            line(41, 48, 41, 66)
        elif name == 'Supafast':
            line(29, 27, 59, 27, 63, 62, 25, 62, 29, 27)
            self.create_arc(35, 15, 53, 39, start=0, extent=180, outline=ink, width=3, style='arc')
            self.create_polygon(45, 31, 35, 47, 43, 47, 39, 58, 54, 40, 46, 40, fill=ink)
            line(15, 37, 23, 37); line(12, 47, 20, 47)
        elif name == 'Doober Eats':
            oval(29, 23, 66, 61); oval(36, 30, 59, 54)
            line(18, 21, 18, 62); line(12, 21, 12, 34, 24, 34, 24, 21)
        elif name == 'Deliveries':
            self.create_polygon(18, 28, 41, 17, 64, 28, 64, 55, 41, 67, 18, 55, fill='', outline=ink, width=3)
            line(18, 28, 41, 40, 64, 28); line(41, 40, 41, 66); line(30, 23, 53, 35, 53, 45)
        elif name == 'Mini Games':
            self.create_polygon(23, 27, 59, 27, 69, 59, 56, 61, 49, 51, 33, 51, 26, 61, 13, 59,
                                fill=ink, smooth=True)
            self.create_line(25, 35, 25, 49, fill=color, width=4)
            self.create_line(18, 42, 32, 42, fill=color, width=4)
            for x, y in ((52, 37), (59, 45)):
                self.create_oval(x-3, y-3, x+3, y+3, fill=color, outline='')
        elif name == 'Settings':
            for i in range(8):
                angle = i*math.pi/4
                line(41+22*math.cos(angle), 41+22*math.sin(angle), 41+29*math.cos(angle), 41+29*math.sin(angle))
            oval(20, 20, 62, 62); oval(33, 33, 49, 49)
        else:
            for x in (25, 51):
                for y in (25, 51): self.create_oval(x-7, y-7, x+7, y+7, fill=ink, outline='')
        self.bind('<Button-1>', lambda e: command())
        self.bind('<Return>', lambda e: command())
        self.bind('<space>', lambda e: command())
        self.icon_scale = size/82
        if size != 82:
            self.scale('all',0,0,self.icon_scale,self.icon_scale)
            self.configure(width=size,height=size)

    def set_unread(self, unread):
        self.delete('notification-dot')
        if unread:
            self.create_oval(59, 0, 82, 23, fill='#ff453a', outline=ui.PANEL,
                             width=2, tags='notification-dot')
            self.create_text(70, 11, text=str(unread) if unread < 100 else '99+',
                             fill='#dce4ed', font=('Segoe UI', 9, 'bold'), tags='notification-dot')
            self.scale('notification-dot',0,0,self.icon_scale,self.icon_scale)
