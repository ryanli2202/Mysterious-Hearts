"""Play required memories through the authored state machine in campaign fixtures."""
import campaign_flashbacks as memories
import campaign_dialogue as dialogue


def finish_scene(s):
    while s.get('campaign_dialogue'):
        b=s['campaign_dialogue']['beats'][s['campaign_dialogue']['cursor']]
        if b.get('reflection') and b.get('selected') is None:
            __import__('campaign_prose').choose_reflection(s,0)
        dialogue.next_line(s)


def finish_memories(s):
    import copy
    from test_major_campaigns import arrive
    world=copy.deepcopy(s['world'])
    while memories.pending(s):
        key=memories.pending(s)
        arrive(s,memories.venue(s,key))
        memories.start(s,key)
        finish_scene(s)
    s['world']=world
