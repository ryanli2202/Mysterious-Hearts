"""Check actual Tk surfaces, popup lists and themed widget states for white fill."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock
from PIL import ImageGrab
import game_core as core
import phone_ui
import winterfield_ui as ui


def main():
    root=tk.Tk();root.withdraw();ui.install(root)
    root.state_data=core.fresh('rei');root.busy=False
    for name in ('persist','render','sounds','update_phone_notification','show_in_person','open_calendar',
                 'accounts','sound_button','wardrobe_menu','rename_contact','new_text_group'):
        setattr(root,name,Mock())
    failures=[]
    root.report_callback_exception=lambda *args:failures.append(args)
    def dark(value,label):
        if not value:return
        rgb=root.winfo_rgb(value)
        assert min(rgb)<56000,(label,value)
    styles=ttk.Style(root)
    for name in ('TButton','TCombobox','TEntry','TSpinbox','TCheckbutton','TRadiobutton','TScrollbar','TMenubutton','Treeview'):
        for state in ((),('active',),('pressed',),('disabled',),('readonly',),('selected',),('focus',)):
            for option in ('background','fieldbackground','indicatorbackground','troughcolor'):
                dark(styles.lookup(name,option,state),f'{name} {state} {option}')
    for cls in (tk.Button,tk.Menu,tk.Entry,tk.Listbox,tk.Text,tk.Spinbox,tk.Checkbutton,tk.Radiobutton):
        widget=cls(root)
        for option in ('background','activebackground','disabledbackground','selectbackground','selectcolor'):
            if option in widget.keys():dark(widget.cget(option),f'{cls.__name__} {option}')
        widget.destroy()
    phone=phone_ui.PhoneWindow(root,'Meet-Cute');phone.geometry('430x740');root.update()
    def inspect(widget):
        if 'background' in widget.keys():dark(widget.cget('background'),str(widget))
        for child in widget.winfo_children():inspect(child)
    for name in ('Meet-Cute','Contacts','Settings','Wardrobe','Maps','Messages'):
        phone.open_app(name);root.update();inspect(phone)
    phone.open_app('Meet-Cute');root.update()
    combo=phone.meet_cute_view.fields['Interest 1']
    phone.tk.call('ttk::combobox::Post',str(combo));root.update()
    popup=phone.tk.call('ttk::combobox::PopdownWindow',str(combo))
    listing=str(popup)+'.f.l'
    dark(phone.tk.call(listing,'cget','-background'),'dropdown list')
    dark(phone.tk.call(listing,'cget','-selectbackground'),'dropdown selection')
    phone.tk.call('ttk::combobox::Unpost',str(combo))
    phone.open_app('Maps');root.update()
    folder=core.ROOT/'tests'/'screenshots';folder.mkdir(exist_ok=True)
    ImageGrab.grab(window=phone.winfo_id()).save(folder/'dark-phone-map.png')
    assert not failures,failures
    phone.destroy();root.destroy()
    print('Dark widget states, classic controls, six phone screens and dropdown popup passed.')


if __name__=='__main__':main()
