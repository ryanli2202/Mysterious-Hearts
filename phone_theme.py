"""Phone-only dark surface defaults and protection against native light states."""
import tkinter as tk
from tkinter import ttk
import winterfield_ui as ui

BACKGROUND, SURFACE, EDGE, TEXT = '#17171b', '#293447', '#3b4a60', '#c4d1e3'
SURFACE_OPTIONS = ('background', 'activebackground', 'disabledbackground',
                   'readonlybackground', 'selectbackground', 'highlightbackground',
                   'troughcolor', 'selectcolor', 'buttonbackground')
STYLE_OPTIONS = ('background', 'fieldbackground', 'troughcolor', 'selectbackground',
                 'indicatorbackground', 'lightcolor', 'darkcolor', 'bordercolor')
STATES = ((), ('active',), ('pressed',), ('disabled',), ('readonly',),
          ('focus',), ('selected',), ('selected', 'focus'), ('disabled', 'selected'))
_styled = {}


def is_light_surface(widget, color):
    if not color: return False
    try:
        values = [v / 65535 for v in widget.winfo_rgb(str(color))]
    except tk.TclError:
        return False
    # Include pale neutral/blue Windows defaults, without removing coloured accents.
    return min(values) >= .75 and max(values) - min(values) < .18


def install(phone):
    _styled.clear()
    if ttk.Style(phone).theme_use() != 'clam':
        ui.install(phone.winfo_toplevel())
    # Scope classic-widget defaults to this phone, including future child dialogs.
    for key, value in {'background': BACKGROUND, 'foreground': TEXT,
                       'activeBackground': SURFACE, 'activeForeground': TEXT,
                       'disabledBackground': BACKGROUND, 'disabledForeground': '#8191a8',
                       'readonlyBackground': SURFACE, 'selectBackground': EDGE,
                       'selectForeground': TEXT, 'highlightBackground': BACKGROUND,
                       'insertBackground': TEXT, 'troughColor': BACKGROUND}.items():
        phone.option_add(str(phone) + '*' + key, value, 80)
    phone.bind('<Map>', lambda event: apply_widget(event.widget), add='+')


def apply_widget(widget):
    if not widget.winfo_exists(): return
    if isinstance(widget, ttk.Widget):
        style = ttk.Style(widget)
        original = str(widget.cget('style')) or widget.winfo_class()
        if isinstance(widget, (ttk.Scrollbar, ttk.Scale, ttk.Progressbar, ttk.Separator)) and original == widget.winfo_class():
            original = str(widget.cget('orient')).title() + '.' + original
        key = (widget.tk, original)
        if key not in _styled:
            fixes, maps = {}, {}
            for option in STYLE_OPTIONS:
                for state in STATES:
                    color = style.lookup(original, option, state)
                    if is_light_surface(widget, color):
                        if not state: fixes[option] = SURFACE
                        else: maps.setdefault(option, []).append((*state, SURFACE))
            name = original
            if fixes or maps:
                name = original if original.startswith('PhoneDark.') else 'PhoneDark.' + original
                style.configure(name, **fixes)
                for option, entries in maps.items():
                    style.map(name, **{option: entries + style.map(original, option)})
            _styled[key] = name
            _styled[(widget.tk, name)] = name
        if _styled[key] != original:
            widget.configure(style=_styled[key])
        if isinstance(widget, ttk.Combobox):
            popup = widget.tk.call('ttk::combobox::PopdownWindow', str(widget))
            widget.tk.call(str(popup) + '.f.l', 'configure', '-background', SURFACE,
                           '-foreground', TEXT, '-selectbackground', EDGE,
                           '-selectforeground', TEXT, '-highlightbackground', SURFACE)
    else:
        keys = widget.keys()
        for option in SURFACE_OPTIONS:
            if option in keys and is_light_surface(widget, widget.cget(option)):
                widget.configure(**{option: SURFACE})
                if option == 'background' and 'foreground' in keys:
                    widget.configure(foreground=TEXT)


def apply_tree(widget):
    apply_widget(widget)
    for child in widget.winfo_children(): apply_tree(child)
