"""Render mission progression and privacy changes in the in-person lab."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
from PIL import ImageGrab
import tkinter as tk
from tkinter import ttk
import game, game_core as core, grove, town
import criminal_dynamics as canon
import laboratory_missions as missions
from careers_ui_smoke import audit


def texts(widget):
    result=[]
    if 'text' in widget.keys(): result.append(str(widget.cget('text')))
    for child in widget.winfo_children():result.extend(texts(child))
    return '\n'.join(result)


with patch.object(game.Game,'check',lambda self:None), patch.object(game.Game,'persist',lambda self:None), patch.object(grove.GrovePump,'tick',lambda self:None), patch.object(game.Game,'begin_incoming',lambda self:None):
    app=game.Game();errors=[];app.report_callback_exception=lambda *args:errors.append(args)
    out=core.ROOT/'.test-tmp';out.mkdir(exist_ok=True)
    try:
        s=core.fresh('ivan');app.state_data=s;town.travel(s,canon.LAB)
        s['world']['minute']=17*60+5
        for who in (*missions.OPERATIVES,'sylvanis'):
            s['world']['cast'][who].update(location=canon.LAB,journey=None,activity='Private laboratory review')
        app.play_screen();app.geometry('1100x850');app.update()
        panel=app.presence_view.site_activities
        assert panel.winfo_toplevel() is app
        panel.viewport.yview_moveto(.35);app.update();audit(panel)
        ImageGrab.grab(window=app.winfo_id()).save(out/'lab-missions-board.png')
        for key in missions.MISSIONS:
            panel.act(missions.begin,key);app.update()
            panel.viewport.yview_moveto(.45);app.update();audit(panel)
            if key=='blue': ImageGrab.grab(window=app.winfo_id()).save(out/'lab-missions-active.png')
            panel.act(missions.choose,0);panel.act(missions.choose,0);app.update()
        assert missions.read(s)['readiness']==10
        panel.viewport.yview_moveto(1);app.update()
        ImageGrab.grab(window=app.winfo_id()).save(out/'lab-missions-result.png')
        # A newly present uncleared listener hides controls, results and stale notices.
        s['world']['cast']['rei'].update(location=canon.LAB,journey=None)
        panel.draw();app.update()
        visible=texts(panel)
        assert 'Private laboratory assignments' not in visible and 'betray' not in visible
        assert 'readiness' not in visible.lower()
        s['player']='rei';__import__('job_apps').ensure(s)['membership']=dict(faction='Syndicate',branch='Spades',rank=6,strikes=0)
        panel.draw();app.update();audit(panel)
        visible=texts(panel)
        assert 'Winterfield strategy' not in visible and 'Set this review aside' not in visible
        assert not errors,errors
        print('PASS: private mission board, all five two-step reviews, results, scrolling and Jack/mixed-audience concealment.')
    finally: app.destroy()
