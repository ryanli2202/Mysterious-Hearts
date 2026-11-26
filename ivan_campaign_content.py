"""A Life on Loan: eighteen authored chapters with recipient-scoped callbacks."""
from copy import deepcopy

HOME='valentina_home__piano_alcove_view'
HQ='syndicate_hq__executive_meeting_room'
NETWORK='ivan_network__review'
PRACTICE='ivan_network__practice'
RECEIVING='ivan_network__receiving'
CURRENT={who:who+'-selection' for who in ('ivan','valentina','sowon','kouji','paul','somchai','april','garrett','neo','daniel','tyler','sylvanis')}
CURRENT['sylvanis']='sylvanis-syndicate'
CURRENT['crow']='crow-selection'

def b(who,text):return dict(player='',speeches=[[who,text]],narration='')
def p(text):return dict(player='',speeches=[],narration=text)
def c(title,room,cast,briefing,aftermath,choices=None):return dict(title=title,room=room,cast=cast,briefing=briefing,aftermath=aftermath,choices=choices or {})

from ivan_campaign_manuscript import SCENES, RETURNS, CHOICES, SPARING, callbacks
from ivan_campaign_manuscript import MEMORIES as MEMORY_TEXT

MEMORIES = {'IV-M03': {'title': 'Before he had a name', 'era': 'ivan_origin_archive'},
 'IV-M04': {'title': 'Between training counts', 'era': 'ivan_training_unassigned'},
 'IV-M05': {'title': 'The second Joker', 'era': 'ivan_handover18'},
 'IV-M06': {'title': 'Queen of Death', 'era': 'ivan_valentina_unassigned'},
 'IV-M07': {'title': 'Queen of Storms', 'era': 'ivan_sowon_unassigned'},
 'IV-M08': {'title': 'King of Flames', 'era': 'ivan_kouji_unassigned'},
 'IV-M09': {'title': 'King of Ice', 'era': 'ivan_paul_unassigned'},
 'IV-M10': {'title': 'King of Chaos', 'era': 'ivan_somchai_unassigned'}}
for key, row in MEMORIES.items():
    row["text"] = MEMORY_TEXT[key]

CHAPTERS = {'IV01': {'title': 'The hours he is allowed',
          'room': 'valentina_home__piano_alcove_view',
          'cast': ('valentina',),
          'choices': {'music': ('Keep the unfinished phrase',
                                'He marks the unresolved phrase to return to it. Valentina listens once '
                                'more, then lets him close the lid himself.'),
                      'rhythm': ('Tap the old rhythm together',
                                 'Valentina taps a deliberately wrong last beat on the piano lid. Ivan '
                                 'answers with the same mistake, chosen this time.')}},
 'IV02': {'title': 'A branch, not a kingdom',
          'room': 'syndicate_hq__executive_meeting_room',
          'cast': ('sylvanis',),
          'choices': {}},
 'IV03': {'title': 'Before he had a name',
          'room': 'ivan_network__review',
          'cast': (),
          'choices': {'private': ('Keep the file private',
                                  'He keeps the origin record to himself. This is a boundary, not a failure '
                                  'of trust or a demand that friendship be earned by trauma disclosure.'),
                      'excerpt': ('Prepare a bounded excerpt for Valentina',
                                  'He sets aside only the engineering-and-sale excerpt for a private '
                                  'conversation with Valentina. It contains no signed order or other '
                                  'general’s history.')}},
 'IV04': {'title': 'Between training counts',
          'room': 'valentina_home__piano_alcove_view',
          'cast': ('valentina',),
          'choices': {}},
 'IV05': {'title': 'The second Joker', 'room': 'ivan_network__review', 'cast': (), 'choices': {}},
 'IV06': {'title': 'Queen of Death',
          'room': 'ivan_network__review',
          'cast': ('valentina',),
          'choices': {'hear': ('Ask for her reasoning',
                               'Ivan asks her to walk him through the changed route. She does, including the '
                               'part of his original plan she refused.'),
                      'object': ('State the objection plainly',
                                 'Ivan states his objection without withdrawing her authority. Valentina '
                                 'names the consequence she chose to avoid and leaves the disagreement on '
                                 'the table.')}},
 'IV07': {'title': 'Queen of Storms',
          'room': 'ivan_network__review',
          'cast': ('sowon',),
          'choices': {'answer': ('Address the people in the route',
                                 'He asks Sowon to show him who still uses the route and hears the answer '
                                 'before discussing timing.'),
                      'defer': ('Invoke the operational deadline',
                                'He says the deadline cannot move. Sowon records the unanswered concern; '
                                'speed has not made it disappear.')}},
 'IV08': {'title': 'King of Flames',
          'room': 'ivan_network__review',
          'cast': ('kouji',),
          'choices': {'limit': ('Give this assignment a clear limit',
                                'Ivan states where this assignment ends. Kouji asks him to retain that limit '
                                'when the next request comes.'),
                      'review': ('Defer the answer to the review',
                                 'Ivan postpones the discussion. Kouji agrees to attend the review, not to '
                                 'treat the missing answer as assent.')}},
 'IV09': {'title': 'King of Ice',
          'room': 'ivan_network__review',
          'cast': ('paul',),
          'choices': {'discuss': ('Hear the immediate concern',
                                  'They identify the exact instruction Paul is unwilling to accept. His need '
                                  'for shelter does not answer it on his behalf.'),
                      'review': ('Arrange a specific review',
                                 'Ivan puts the concern on the review agenda. Paul asks for a time and '
                                 'receives one, rather than another indefinite reassurance.')}},
 'IV10': {'title': 'King of Chaos',
          'room': 'ivan_network__review',
          'cast': ('somchai',),
          'choices': {'restrict': ('Restrict his assignment',
                                   'Ivan removes Somchai from contact with the intermediary’s workers. The '
                                   'restriction is explicit; the network still bears responsibility for '
                                   'involving him.'),
                      'oversight': ('Require direct oversight',
                                    'Ivan requires direct oversight for the assignment. Supervision is a '
                                    'practical limit, not a claim that the original recruitment was '
                                    'harmless.')}},
 'IV11': {'title': 'An organisation of his own',
          'room': 'ivan_network__review',
          'cast': ('valentina', 'sowon', 'kouji', 'paul', 'somchai'),
          'choices': {'negotiate': ('Negotiate criminal cooperation',
                                    'Ivan negotiates a dispatch agreement with the intermediary. The workers '
                                    'were not party to it; extra availability is treated as something the '
                                    'agreement can demand from them.'),
                      'display': ('Use a coercive display',
                                  'Ivan uses an explicit display of network force to obtain cooperation. No '
                                  'new assault is staged; the threat is enough to make the workers change '
                                  'how they leave the building.')}},
 'IV12': {'title': 'The terms of protection',
          'room': 'ivan_network__receiving',
          'cast': ('garrett',),
          'choices': {'direct': ('Remove the shift-exit restriction now',
                                 'Ivan removes the instruction restricting the shift exit and states that '
                                 'the agreed finishing time stands. This is one fulfilled request, not full '
                                 'restitution.'),
                      'delegate': ('Send the request through command',
                                   'Ivan refers the request through his command. He has not yet fulfilled '
                                   'it. The worker asks when to expect an answer; the outstanding obligation '
                                   'remains recorded.')}},
 'IV13': {'title': 'Orders he once hated',
          'room': 'ivan_network__review',
          'cast': ('valentina', 'sowon', 'kouji', 'paul'),
          'choices': {'private': ('Hear the remaining objections individually',
                                  'Ivan hears the objections in separate bounded conversations. Each person '
                                  'retains only their own exchange; nobody inherits the others’ confidential '
                                  'history.'),
                      'review': ('Keep the objections in the command review',
                                 'Ivan keeps the operational objections in the assembled review. The '
                                 'witnesses can remember what was said there, not private recruitment '
                                 'histories that were never spoken.')}},
 'IV14': {'title': 'One more necessary thing',
          'room': 'ivan_network__review',
          'cast': ('april',),
          'choices': {'admit': ('Name the compulsion directly',
                                'Ivan says he intends to compel the intermediary to continue. April can '
                                'repeat that admission to the five people attending the intervention.'),
                      'temporary': ('Defend it as temporary necessity',
                                    'Ivan defends forcing cooperation as temporary necessity. April can '
                                    'repeat his stated plan and justification to the intervention group, '
                                    'without acquiring unrelated secrets.')}},
 'IV15': {'title': 'The people who came for him',
          'room': 'ivan_network__practice',
          'cast': ('april', 'garrett', 'neo', 'daniel', 'tyler'),
          'choices': {'limited': ('Name the continuing captivity, without the private files',
                                  'Ivan tells the five that he cannot freely leave Syndicate control. He '
                                  'does not disclose his origin file, the signed order, its leverage or the '
                                  'generals’ identities. They recognise the limit without accepting his next '
                                  'coercive order.'),
                      'present': ('Keep the argument on the present order',
                                  'Ivan keeps his history private and answers only for the operation he is '
                                  'trying to impose now. The friends do not make support conditional on '
                                  'disclosure of his trauma.')}},
 'IV16': {'title': 'The victory he wanted',
          'room': 'ivan_network__practice',
          'cast': ('april', 'garrett', 'neo', 'daniel', 'tyler'),
          'choices': {}},
 'IV17': {'title': 'A little blood',
          'room': 'ivan_network__practice',
          'cast': ('sylvanis', 'april', 'garrett', 'neo', 'daniel', 'tyler'),
          'choices': {}},
 'IV18': {'title': 'Still here',
          'room': 'valentina_home__piano_alcove_view',
          'cast': ('valentina', 'april', 'garrett', 'neo', 'daniel', 'tyler'),
          'choices': {}}}
for key, row in CHAPTERS.items():
    row["briefing"], row["aftermath"] = SCENES[key]

BACKGROUNDS={HOME:'locations/interiors/valentina_home/piano_alcove_view',HQ:'locations/interiors/syndicate_hq/executive_meeting_room',NETWORK:'locations/campaign/ivan/review',PRACTICE:'locations/campaign/ivan/practice',RECEIVING:'locations/campaign/ivan/receiving'}
HISTORY_BG={'IV-M03':'archive','IV-M04':'training','IV-M05':'handover','IV-M06':'founding','IV-M07':'athletics','IV-M08':'kickboxing','IV-M09':'refuge','IV-M10':'backroom'}
CORE_SHOTS=__import__('json').loads((__import__('pathlib').Path(__file__).parent/'assets/campaigns/ivan/core/catalog.json').read_text(encoding='utf-8'))['shots']

def stage(lines,key,field,room,memory=False):
    for index,beat in enumerate(lines):
        beat['title']=key+' · '+CHAPTERS[key]['title']
        beat['room']=room;beat['background']=BACKGROUNDS[room]
        cast={'ivan',*CHAPTERS[key].get('cast',()),*[who for who,_ in beat.get('speeches',[])]}
        beat['portraits']={who:portrait for who,portrait in CURRENT.items() if who in cast}
        if room==HQ:beat['portraits']['ivan']='ivan-syndicate'
        if memory:
            mid=__import__('ivan_campaigns').MEMORY_AT[int(key[2:])-1]
            beat['mode']='memory';beat['era']=MEMORIES[mid]['era'];beat['background']='locations/campaign/ivan/'+HISTORY_BG[mid]
            # No modern portrait substitutes for a missing historical identity.
            beat['portraits']={}
            if mid=='IV-M05':beat['portraits']={'ivan':'ivan-handover18'}
        source=f'{key}:{field}:{index:03}';beat['source_id']=source
        segments=[dict(phase='dialogue',speaker=who,text=text) for who,text in beat.get('speeches',[])]
        if beat.get('narration'):segments.append(dict(phase='prose',text=beat['narration']))
        core=next((ident for ident,row in CORE_SHOTS.items() if row['source']==source),None)
        for segment in segments:segment.update(source_id=source,source_element=index,shot_id=source+':stage',background=beat['background'],portraits=deepcopy(beat['portraits']),core_id=core)
        beat['stage_segments']=segments
    return lines
