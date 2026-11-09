"""A native, scrollable Weather app with a large forecast and translucent-style cards."""
import tkinter as tk
from tkinter import ttk
from datetime import date
import weather

def clock(minute):
    return f'{minute//60:02}:{minute%60:02}'

def symbol(w):
    return {'Rain':'☂', 'Snow':'❄', 'Cloudy':'☁', 'Partly cloudy':'☁'}.get(w['condition'], '☾' if w.get('light')=='night' else '☀')

class WeatherView(tk.Frame):
    def __init__(self, parent, state):
        self.forecast=weather.forecast(state['world']['minute'])
        current=self.forecast['current']
        self.bg='#142944' if current['light']=='night' else '#3876a5'
        self.card='#253f5b' if current['light']=='night' else '#4b87b1'
        super().__init__(parent,bg=self.bg)
        self.pack(fill='both',expand=True)
        canvas=tk.Canvas(self,bg=self.bg,highlightthickness=0)
        bar=ttk.Scrollbar(self,orient='vertical',command=canvas.yview)
        bar.pack(side='right',fill='y'); canvas.pack(side='left',fill='both',expand=True)
        canvas.configure(yscrollcommand=bar.set)
        body=tk.Frame(canvas,bg=self.bg,padx=18,pady=16)
        window=canvas.create_window(0,0,window=body,anchor='nw')
        canvas.bind('<Configure>',lambda e:canvas.itemconfigure(window,width=e.width))
        body.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
        def wheel(e): canvas.yview_scroll(-int(e.delta/120),'units')
        def label(parent,text,size=12,**kw):
            widget=tk.Label(parent,text=text,font=('Segoe UI',size),bg=parent['bg'],fg='#dce4ed',**kw)
            widget.pack()
            if 'wraplength' in kw:
                widget.pack_configure(fill='x')
                widget.bind('<Configure>',lambda e:widget.configure(wraplength=max(120,e.width)))
            widget.bind('<MouseWheel>',wheel); return widget
        label(body,'MY LOCATION',10)
        label(body,'Winterfield',30)
        self.temperature=label(body,f"{current['temperature']}°",76)
        label(body,f"{symbol(current)}  {current['condition']}",20)
        label(body,f"H:{current['high']}°  L:{current['low']}°",14)
        label(body,'Story forecast · '+current['date']+' · Celsius',10).pack_configure(pady=(8,22))
        def card(title):
            surface=tk.Canvas(body,bg=self.bg,highlightthickness=0,height=100)
            surface.pack(fill='x',pady=7)
            f=tk.Frame(surface,bg=self.card,padx=4,pady=2)
            item=surface.create_window(16,12,window=f,anchor='nw')
            def shape(event=None):
                width=surface.winfo_width(); height=f.winfo_reqheight()+24
                surface.configure(height=height)
                surface.itemconfigure(item,width=max(1,width-32))
                surface.delete('glass')
                surface.create_polygon(18,0,width-18,0,width,0,width,18,width,height-18,width,height,
                    width-18,height,18,height,0,height,0,height-18,0,18,0,0,
                    fill=self.card,smooth=True,splinesteps=24,tags='glass')
                surface.tag_lower('glass')
            surface.bind('<Configure>',shape); f.bind('<Configure>',shape)
            surface.bind('<MouseWheel>',wheel)
            label(f,title,10).pack_configure(anchor='w',pady=(0,10))
            return f
        f=card('HOURLY FORECAST')
        description='Rain practice moves beneath the boathouse awning.' if weather.shelter(current['minute']) else 'Conditions follow the story clock, even after saving and loading.'
        label(f,description,11,wraplength=440,justify='left').pack_configure(anchor='w',pady=(0,12))
        hours=tk.Canvas(f,height=108,bg=self.card,highlightthickness=0)
        hours.pack(fill='x')
        for i,w in enumerate(self.forecast['hourly']):
            x=35+i*72
            for y,text,size in ((12,'Now' if i==0 else clock(w['minute']%1440),10),(45,symbol(w),22),(82,f"{w['temperature']}°",15)):
                hours.create_text(x,y,text=text,fill='#dce4ed',font=('Segoe UI',size))
        hours.configure(scrollregion=(0,0,24*72,108))
        hbar=ttk.Scrollbar(f,orient='horizontal',command=hours.xview)
        hbar.pack(fill='x'); hours.configure(xscrollcommand=hbar.set)
        f=card('10-DAY FORECAST')
        days=self.forecast['daily']; minimum=min(w['low'] for w in days); maximum=max(w['high'] for w in days)
        chart=tk.Canvas(f,height=350,bg=self.card,highlightthickness=0)
        chart.pack(fill='x')
        def draw(e):
            chart.delete('all'); width=e.width
            for i,w in enumerate(days):
                y=i*35+16; start=width*.48; end=width-45; span=max(1,maximum-minimum)
                chart.create_text(0,y,text='Today' if i==0 else date.fromisoformat(w['date']).strftime('%a'),anchor='w',fill='#dce4ed',font=('Segoe UI',12))
                chart.create_text(width*.22,y,text=symbol(w),fill='#dce4ed',font=('Segoe UI',17))
                chart.create_text(start-20,y,text=f"{w['low']}°",fill='#c4def0',font=('Segoe UI',12))
                chart.create_line(start,y,end,y,fill=self.bg,width=5,capstyle='round')
                chart.create_line(start+(end-start)*(w['low']-minimum)/span,y,start+(end-start)*(w['high']-minimum)/span,y,fill='#e7c47d',width=5,capstyle='round')
                chart.create_text(width-5,y,text=f"{w['high']}°",anchor='e',fill='#dce4ed',font=('Segoe UI',12))
        chart.bind('<Configure>',draw); chart.bind('<MouseWheel>',wheel)
        f=card('CURRENT CONDITIONS')
        values=[('FEELS LIKE',f"{current['feels_like']}°"),('PRECIPITATION',f"{current['precipitation']}%"),('WIND',f"{current['wind']} km/h"),('HUMIDITY',f"{current['humidity']}%"),('SUNRISE',clock(current['sunrise'])),('SUNSET',clock(current['sunset'])),('UV INDEX',str(current['uv'])),('VISIBILITY',f"{current['visibility']} km")]
        grid=tk.Frame(f,bg=self.card); grid.pack(fill='x')
        for i,(title,value) in enumerate(values):
            cell=tk.Frame(grid,bg=self.card,padx=8,pady=12); cell.grid(row=i//2,column=i%2,sticky='ew')
            grid.columnconfigure(i%2,weight=1); label(cell,title,9); label(cell,value,22)
        label(body,'Winterfield simulation · No real-world weather service',10).pack_configure(pady=15)
        canvas.bind('<MouseWheel>',wheel); body.bind('<MouseWheel>',wheel)
