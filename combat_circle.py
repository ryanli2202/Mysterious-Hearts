"""Save-owned Iron Circle championship; competitive position is not strength."""
import copy


def ensure(s, ledger):
    if not ledger: return
    if 'champion' not in ledger:
        ledger['champion']=s['player'] if ledger['rank']==1 else 'rei'
        ledger['titles_earned']=1 if ledger['rank']==1 else 0
    ledger.setdefault('title_history',[])
    if ledger['champion']==s['player']: ledger['rank']=1


def champion_profile(s):
    from combat_profiles import profile
    ledger=s['combat']['ledger']; ensure(s,ledger)
    saved=ledger.get('champion_profile')
    return copy.deepcopy(saved or profile(s,ledger['champion']))


def candidate(s):
    ledger=s['combat']['ledger']; ensure(s,ledger)
    if ledger['rank']==2 and ledger['champion']!=s['player']:
        p=champion_profile(s)
        p['title_bout']=True; p['champion_id']=ledger['champion']
        return p
    return None


def validate_title(s,data):
    ledger=s['combat']['ledger']; ensure(s,ledger)
    if not data.get('title_bout'): return None
    expected=candidate(s)
    if not expected or data.get('champion_id')!=ledger['champion']:
        raise ValueError('The championship changed; prepare the current title bout again.')
    return expected


def finish(s,f,win):
    ledger=s['combat']['ledger']; ensure(s,ledger)
    if f.get('title_bout'):
        if win:
            previous=ledger['champion']; ledger['champion']=s['player']
            ledger.pop('champion_profile',None); ledger['rank']=1
            ledger['titles_earned']=ledger.get('titles_earned',0)+1
            ledger['title_history'].append(dict(minute=s['world']['minute'],previous=previous,champion=s['player'],fight=f['id']))
        else: ledger['rank']=2
    elif f.get('title_defence'):
        if not win:
            previous=ledger['champion']; ledger['champion']=f['opponent']
            ledger['champion_profile']=copy.deepcopy(f['opponent_profile']); ledger['rank']=2
            ledger['title_history'].append(dict(minute=s['world']['minute'],previous=previous,champion=f['opponent'],fight=f['id']))
    else:
        # Legacy active bouts may retain a legitimately earned rank-one title.
        if ledger['rank']==1: return
        ledger['rank']=max(2,ledger['rank']-10) if win else min(450,ledger['rank']+5)
