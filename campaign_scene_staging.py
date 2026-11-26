"""Reviewed source-element visual changes, frozen into new scene snapshots.

Indices refer to the unmodified compiled manuscript. Unnamed adults remain
off screen; a room/cast change changes the shot, ordinary dialogue does not.
"""

def visual(key,index,mode):
    if key=='RD29' and mode=='present':
        return dict(background='locations/blackstone_loading',shot_id='RD29:loading-approach')
    if mode!='memory':return {}
    if key=='RD36':
        if index<5:
            return dict(background='locations/hamayashi-training-hall',portraits={'rei':'rei-child'},shot_id='RD36:training')
        return dict(background='locations/hamayashi-siblings-room',portraits={'rei':'rei-child','yuriko':'yuriko-child'},shot_id='RD36:siblings')
    if key=='RD13':
        if index>=27:
            return dict(background='locations/rei-high-school',portraits={'rei':'rei-high-school'},shot_id='RD13:departure')
        if index>=23:
            return dict(background='locations/campaign-school-office',portraits={'rei':'rei-high-school'},shot_id='RD13:office')
    if key.startswith('FM') and key in ('FM01','FM02','FM03','FM04'):
        room='blackhaven'
        if key=='FM02':room='campaign-annex-table' if index<25 else 'campaign-annex-counter'
        if key=='FM03':room='blackhaven' if index<5 else 'campaign-annex-table'
        if key=='FM04':room='blackhaven' if index<3 else ('campaign-annex-table' if index<22 else 'campaign-annex-kettle')
        return dict(background='locations/'+room,portraits={'fox':'fox-early-partnership','gordon':'gordon-early-partnership'},shot_id=key+':'+room)
    return {}
