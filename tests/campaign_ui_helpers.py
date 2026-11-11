"""Finish authored beats using the same Continue control as the player."""
from tkinter import ttk
from unittest.mock import patch
import campaign_dialogue

@patch.object(campaign_dialogue, 'request_narration', new=lambda *args: None)
def finish_script(app):
    campaign_dialogue.activate_epilogue(app.state_data)
    if app.state_data.get('campaign_dialogue'):campaign_dialogue.show(app)
    while app.state_data.get('campaign_dialogue'):
        app.update()
        d=app.state_data['campaign_dialogue'];b=d['beats'][d['cursor']]
        if b.get('prose'):
            reader=app.hangout_view.prose_reader
            if b.get('reflection') and b.get('selected') is None:reader.choose(0)
            reader.next.invoke();app.update()
            continue
        buttons=[w for w in app.hangout_view.script_panel.winfo_children() if isinstance(w,ttk.Button)]
        buttons[-1].invoke();app.update()
