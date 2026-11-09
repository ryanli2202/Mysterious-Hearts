"""Side-scrolling park hosted by the main in-person game screen."""
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import phone_theme
from park_scene import Walker, Renderer, WIDTH, VIEW, HEIGHT


class ParkView(ttk.Frame):
    location_key = 'park'

    def __init__(self, parent, game, on_leave):
        super().__init__(parent)
        self.game=game;self.on_leave=on_leave
        self.walker=Walker();self.held_keys=set();self.timer=None;self.alive=True
        self.last=time.monotonic();self.photo=None
        self.bind('<Destroy>',self._destroyed,add='+')
        body=ttk.Frame(self,padding=8);body.pack(fill='both',expand=True)
        heading=ttk.Frame(body);heading.pack(fill='x')
        self.back_button=ttk.Button(heading,text='‹ Back to location',command=on_leave)
        self.back_button.pack(side='right')
        ttk.Label(heading,text='RIVERSIDE PARK',font=('Segoe UI',18,'bold')).pack(side='left')
        ttk.Label(body,text='Dusk trail · Garrett is the test avatar',foreground='#94afaa').pack(anchor='w',pady=(2,8))
        self.canvas=tk.Canvas(body,bg='#141e2c',highlightthickness=0,height=360,takefocus=True)
        self.canvas.pack(fill='both',expand=True)
        self.canvas.bind('<Configure>',lambda e:self.draw())
        self.canvas.bind('<Button-1>',lambda e:self.canvas.focus_set())
        self.canvas.bind('<KeyPress>',self.press)
        self.canvas.bind('<KeyRelease>',self.release)
        self.canvas.bind('<FocusOut>',lambda e:self.stop())
        self.status=tk.StringVar(master=self,value='Walk along the path to discover the park.')
        ttk.Label(body,textvariable=self.status,wraplength=300).pack(fill='x',pady=6)
        controls=ttk.Frame(body);controls.pack(fill='x')
        for label,key in [('◀ Left','left'),('Right ▶','right')]:
            b=ttk.Button(controls,text=label,takefocus=False)
            b.pack(side='left',fill='x',expand=True,padx=2)
            b.bind('<ButtonPress-1>',lambda e,k=key:self.hold(k))
            b.bind('<ButtonRelease-1>',lambda e:self.stop())
            b.bind('<Leave>',lambda e:self.stop())
        self.interact_button=ttk.Button(controls,text='Look · E',command=self.interact)
        self.interact_button.pack(side='left',padx=2)
        ttk.Label(body,text='← → or A / D to walk · E to interact · Esc to leave',wraplength=300,foreground='#94a4b8').pack(fill='x',pady=(8,0))
        self.renderer=None
        try:self.renderer=Renderer()
        except (OSError,ValueError) as exc:
            self.status.set('Park artwork could not be loaded. Use Back to return to the location.')
            for child in controls.winfo_children():child.configure(state='disabled')
        phone_theme.apply_tree(self)
        self.after_idle(lambda:self.canvas.focus_set() if self.alive else None)
        self.tick()

    def hold(self,key):
        self.canvas.focus_set();self.held_keys={key}

    def stop(self):self.held_keys.clear()

    def press(self,event):
        key=event.keysym.lower()
        if key in ('left','right','a','d'):self.held_keys.add(key)
        elif key=='e':self.interact()
        elif key=='escape':self.on_leave()
        return 'break'

    def release(self,event):self.held_keys.discard(event.keysym.lower());return 'break'

    def interact(self):
        spot=self.walker.nearby
        if spot:
            if spot[1].endswith('gate'):
                self.on_leave();return
            self.stop();self.walker.seated=spot[1]=='Garden bench'
            self.status.set(spot[2]);self.draw()

    def tick(self):
        if not self.alive:return
        now=time.monotonic();dt=now-self.last;self.last=now
        if self.renderer:
            if not self.winfo_viewable():self.stop()
            axis=int(bool(self.held_keys&{'right','d'}))-int(bool(self.held_keys&{'left','a'}))
            self.walker.step(axis,dt)
            spot=self.walker.nearby
            if self.walker.moving:self.status.set((spot[1]+' · press E') if spot else f'Park trail · {int(self.walker.x/WIDTH*100)}%')
            self.draw()
        self.timer=self.after(33,self.tick)

    def draw(self):
        if not getattr(self,'renderer',None) or not self.alive:return
        w,h=self.canvas.winfo_width(),self.canvas.winfo_height()
        if w<2 or h<2:return
        spot=self.walker.nearby
        label='Leave · E' if spot and spot[1].endswith('gate') else 'Rest · E' if spot and spot[1]=='Garden bench' else 'Look · E'
        self.interact_button.configure(state='normal' if spot else 'disabled',text=label)
        im=self.renderer.render(self.walker)
        scale=min(w/VIEW,h/HEIGHT)
        im=im.resize((max(1,int(VIEW*scale)),max(1,int(HEIGHT*scale))),Image.Resampling.NEAREST)
        self.photo=ImageTk.PhotoImage(im,master=self.canvas)
        self.canvas.delete('all');self.canvas.create_image(w//2,h//2,image=self.photo)

    def _destroyed(self,event):
        if event.widget is self:
            self.alive=False;self.stop()
            if self.timer:
                self.after_cancel(self.timer);self.timer=None
