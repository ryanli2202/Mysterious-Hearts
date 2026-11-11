"""Paged, gesture-operated home screen with a persistent application dock."""
import custom_protagonist
import math
import tkinter as tk
from PIL import Image, ImageOps, ImageTk, ImageEnhance
import phone_personalization as personal
import phone_icons
import winterfield_ui as ui


def page_layout(width, height, count):
    columns = 3 if width < 400 else 4
    rows = max(1, min(3, int((height-240)//108)))
    capacity = columns*rows
    return columns, rows, capacity, max(1, math.ceil(count/capacity))


def home(phone, frame, s):
    d = personal.ensure(s)
    canvas = tk.Canvas(frame, highlightthickness=0, bg='#111925', takefocus=True)
    canvas.pack(fill='both', expand=True)
    phone.home_canvas = canvas
    phone.home_icons = []
    dock = d.setdefault('home_dock', ['Messages', 'Camera', 'Contacts'])
    names = [name for name in dict.fromkeys(d['app_order']+list(phone_icons.COLORS))
             if name in phone_icons.COLORS and name not in dock]
    source = None
    editing, selected = False, None
    slots = []
    hold = edge = None
    dragging = False
    try:
        with Image.open(personal.wallpaper_path(s)) as art: source = art.convert('RGB')
    except OSError: pass

    def change(delta=0, page=None):
        current = d.get('home_page', 0)
        d['home_page'] = max(0, min(phone.home_page_count-1, current+delta if page is None else page))
        if current != d['home_page']:
            draw(); phone.game.persist()
        return 'break'

    def tile(name, x, y, size, label=True):
        icon = phone_icons.AppIcon(canvas, name, lambda: phone.open_app(name), size=size)
        if hasattr(canvas,'background_art'):
            backing=canvas.background_art.crop((int(x-size/2),int(y-size/2),int(x-size/2)+size,int(y-size/2)+size)) if label else Image.new('RGB',(size,size),'#283342')
            icon.backing=ImageTk.PhotoImage(backing,master=icon)
            item=icon.create_image(0,0,image=icon.backing,anchor='nw')
            icon.tag_lower(item)
            icon.configure(highlightthickness=0)
        icon.bind('<ButtonPress-1>', lambda e: press(e, name))
        icon.bind('<ButtonRelease-1>', lambda e: release(e, name))
        icon.bind('<B1-Motion>', motion)
        icon.bind('<Return>', lambda e: choose(name) if editing else phone.open_app(name))
        icon.bind('<space>', lambda e: choose(name) if editing else phone.open_app(name))
        if editing:
            icon.configure(highlightthickness=2, highlightbackground='#80c6ba' if name == selected else '#536171')
        canvas.create_window(x,y,window=icon)
        phone.home_icons.append(icon)
        if label:
            canvas.create_text(x,y+size/2+13,text=name,fill='#dce4ed',font=('Segoe UI',9),width=95)
        if name == 'Messages': phone.messages_icon = icon; icon.set_unread(phone_icons.unread_messages(s))
        elif name == 'Mysterious Hearts': phone.hearts_icon=icon
        elif name == 'Grove': phone.grove_icon=icon
        elif name == 'Meet-Cute':
            import meet_cute
            phone.meet_cute_icon=icon
            icon.set_unread(meet_cute.unread(s))

    def draw(event=None):
        # Do not save a three-slot layout from Tk's initial 1x1 placeholder.
        if canvas.winfo_width() <= 1 or canvas.winfo_height() <= 1: return
        for icon in phone.home_icons: icon.destroy()
        phone.home_icons=[]
        phone.messages_icon=phone.hearts_icon=phone.grove_icon=phone.unread_label=None
        phone.meet_cute_icon=None
        canvas.delete('all')
        width,height=max(200,canvas.winfo_width()),max(290,canvas.winfo_height())
        columns,rows,capacity,pages=page_layout(width,height,len(names))
        capacity = d.setdefault('home_capacity', capacity)
        if 'home_pages' not in d:
            d['home_pages'] = [names[i:i+capacity]+[None]*(capacity-len(names[i:i+capacity]))
                               for i in range(0,len(names),capacity)] or [[None]*capacity]
        layouts = d['home_pages']
        known = set(dock + [n for row in layouts for n in row if n])
        for name in names:
            if name not in known:
                if not any(None in row for row in layouts): layouts.append([None]*capacity)
                row = next(row for row in layouts if None in row)
                row[row.index(None)] = name
        pages = len(layouts) + (1 if editing else 0)
        rows = math.ceil(capacity/columns)
        phone.home_page_count=pages
        page=max(0,min(pages-1,d.get('home_page',0))); d['home_page']=page
        current = layouts[page] if page < len(layouts) else [None]*capacity
        phone.visible_home_apps=[n for n in current+dock if n]
        slots.clear()
        if source:
            art=ImageEnhance.Brightness(ImageOps.fit(source,(width,height),Image.Resampling.LANCZOS)).enhance(.7)
            canvas.background_art=art
            canvas.wallpaper=ImageTk.PhotoImage(art,master=canvas)
            canvas.create_image(0,0,image=canvas.wallpaper,anchor='nw')
        # A textured information panel keeps clock and alerts legible on any wallpaper.
        canvas.header_texture = ImageTk.PhotoImage(ui.surface_texture(width-24, 94, '#192533'), master=canvas)
        canvas.create_image(12, 7, image=canvas.header_texture, anchor='nw')
        canvas.create_rectangle(12, 7, width-12, 101, outline='#3b4a60')
        canvas.create_line(28, 100, width-28, 100, fill='#709e99')
        minute=s['world']['minute']%1440
        canvas.create_text(width/2,32,text=f'{minute//60:02}:{minute%60:02}',fill='#dce4ed',font=('Segoe UI',32,'bold'))
        canvas.create_text(width/2,66,text='Select app, then slot · arrows change page' if editing else f'{custom_protagonist.display_name(s["player"])}’s phone',fill='#dce4ed',font=('Segoe UI',9 if editing else 11))
        control = canvas.create_text(width-24,18,text='Done' if editing else 'Edit',anchor='ne',
                                     fill='#80c6ba',font=('Segoe UI',11,'bold'),tags='edit')
        canvas.tag_bind(control,'<ButtonRelease-1>',lambda e: toggle_edit())
        phone.home_unread_item=canvas.create_text(width/2,87,text='',fill='#dce4ed',font=('Segoe UI',9))
        size=64 if width<400 else 72
        grid_bottom=height-150
        spacing=min(116,max(35,(grid_bottom-100)/rows))
        size=min(size,max(24,int(spacing-28)))
        for i,name in enumerate(current):
            x,y=(i%columns+.5)*width/columns,110+spacing/2+(i//columns)*spacing
            slots.append((x,y,('page',page,i)))
            if editing:
                canvas.create_rectangle(x-size/2-5,y-size/2-5,x+size/2+5,y+size/2+5,
                                        fill='#202c3b',outline='#536171',dash=(3,3))
            if name: tile(name,x,y,size)
        dots_y=height-126
        for n in range(pages):
            x=width/2+(n-(pages-1)/2)*min(20,(width-90)/pages)
            if editing and n == len(layouts):
                item=canvas.create_text(x,dots_y,text='+',fill='#80c6ba',font=('Segoe UI',13),tags=f'page:{n}')
            else:
                item=canvas.create_oval(x-4,dots_y-4,x+4,dots_y+4,fill='#80c6ba' if n==page else '#788593',outline='',tags=f'page:{n}')
            canvas.tag_bind(item,'<ButtonRelease-1>',lambda e,n=n:change(page=n))
        for x,label,delta in [(25,'‹',-1),(width-25,'›',1)]:
            item=canvas.create_text(x,dots_y,text=label,fill='#dce4ed',font=('Segoe UI',24),tags='page-arrow')
            canvas.tag_bind(item,'<ButtonRelease-1>',lambda e,delta=delta:change(delta))
        canvas.create_polygon(28,height-101,width-28,height-101,width-10,height-101,width-10,height-80,
                              width-10,height-12,width-28,height-12,28,height-12,10,height-12,10,height-80,10,height-101,
                              smooth=True,fill='#283342',outline='#536171')
        for i,name in enumerate(dock):
            x,y=(i+.5)*width/3,height-57
            slots.append((x,y,('dock',0,i)))
            if name: tile(name,x,y,size,label=False)
            elif editing:
                canvas.create_rectangle(x-30,y-30,x+30,y+30,outline='#536171',dash=(3,3))

    gesture=[0,0]
    def cancel_timer(kind):
        nonlocal hold, edge
        timer = hold if kind == 'hold' else edge
        if timer: canvas.after_cancel(timer)
        if kind == 'hold': hold = None
        else: edge = None

    def toggle_edit():
        nonlocal editing, selected
        editing = not editing
        selected = None
        cancel_timer('hold'); cancel_timer('edge')
        if not editing:
            while len(d['home_pages']) > 1 and not any(d['home_pages'][-1]):
                d['home_pages'].pop()
            phone.game.persist()
        draw()
        return 'break'

    def choose(name):
        nonlocal selected
        selected = name
        draw()
        return 'break'

    def place(target):
        nonlocal selected
        if not selected: return
        source_row = next(row for row in [dock]+d['home_pages'] if selected in row)
        source_index = source_row.index(selected)
        kind, page, index = target
        if kind == 'dock': row = dock
        else:
            if page == len(d['home_pages']): d['home_pages'].append([None]*d['home_capacity'])
            row = d['home_pages'][page]
        source_row[source_index], row[index] = row[index], selected
        selected = None
        phone.game.persist()
        draw()

    def press(event, name=None):
        nonlocal hold, dragging, selected
        gesture[:]=[event.x_root,event.y_root]
        dragging = False
        canvas.focus_set()
        cancel_timer('hold')
        if name:
            def long_press():
                nonlocal editing, selected, hold
                hold = None
                editing = True; selected = name
                canvas.grab_set()
                draw()
            if editing:
                if not selected:
                    selected = name
                canvas.grab_set()
            else: hold = canvas.after(550,long_press)

    def motion(event):
        nonlocal dragging, edge
        if abs(event.x_root-gesture[0])+abs(event.y_root-gesture[1]) > 10:
            cancel_timer('hold')
            dragging = True
        if not editing or not selected: return
        x,y=event.x_root-canvas.winfo_rootx(),event.y_root-canvas.winfo_rooty()
        canvas.delete('drag')
        canvas.create_text(x,y-30,text=selected,fill='#dce4ed',font=('Segoe UI',10,'bold'),tags='drag')
        direction = -1 if x < 28 else 1 if x > canvas.winfo_width()-28 else 0
        if not direction: cancel_timer('edge')
        elif edge is None:
            def turn():
                nonlocal edge
                edge = None
                change(direction)
            edge = canvas.after(650,turn)

    def release(event,name=None):
        cancel_timer('hold'); cancel_timer('edge')
        if canvas.grab_current() == canvas: canvas.grab_release()
        canvas.delete('drag')
        x,y=event.x_root-canvas.winfo_rootx(),event.y_root-canvas.winfo_rooty()
        if event.widget == canvas and any(
                any(t.startswith('page') or t == 'edit' for t in canvas.gettags(i))
                for i in canvas.find_overlapping(x-1,y-1,x+1,y+1)):
            return 'break'
        if editing:
            if selected:
                for sx,sy,target in sorted(slots, key=lambda slot: (x-slot[0])**2+(y-slot[1])**2):
                    if abs(x-sx)<45 and abs(y-sy)<45:
                        row = dock if target[0] == 'dock' else d['home_pages'][target[1]] if target[1] < len(d['home_pages']) else []
                        if row and row[target[2]] == selected and not dragging:
                            draw(); break
                        place(target); break
            elif name: choose(name)
            return 'break'
        dx,dy=event.x_root-gesture[0],event.y_root-gesture[1]
        if abs(dx)>45 and abs(dx)>abs(dy): return change(1 if dx<0 else -1)
        if name: phone.open_app(name)
    canvas.bind('<ButtonPress-1>',press)
    canvas.bind('<ButtonRelease-1>',release)
    canvas.bind('<B1-Motion>',motion)
    canvas.bind('<Destroy>',lambda e: (cancel_timer('hold'),cancel_timer('edge')) if e.widget == canvas else None)
    phone.edit_home=toggle_edit
    canvas.bind('<Left>',lambda e:change(-1)); canvas.bind('<Right>',lambda e:change(1))
    canvas.bind('<MouseWheel>',lambda e:'break')
    canvas.bind('<Configure>',draw)
    phone.change_home_page=change
    canvas.after_idle(lambda: (draw(),canvas.focus_set()) if canvas.winfo_exists() else None)
