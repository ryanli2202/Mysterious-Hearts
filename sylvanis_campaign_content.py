"""The Crow's Patience: immutable authored scenes and exact historical boundaries."""
from copy import deepcopy

LAB='glasshouse_lab__private_review_reunion_room'
WORK='glasshouse_lab__laboratory_workroom'
HQ='syndicate_hq__executive_meeting_room'
ARENA='sylvanis_arena__ring'
TAKEO='site_01__briefing_room'

def b(who=None,text='',narration='',room=None):
    result=dict(player='',speeches=[[who,text]] if who else [],narration=narration)
    if room:result['room']=room
    return result
def p(text,room=None):return b(narration=text,room=room)

from sylvanis_campaign_manuscript import MEMORY_TEXT, CHAPTER_TEXT, AFTERMATH_TEXT, MEMORY_RETURN_TEXT

# Stable route/era IDs and room contracts are unchanged by the prose revision.
MEMORIES = {'SY-M01': {'title': 'A captured planet, an open world', 'era': 'sylvanis_arrival', 'background': 'arrival'},
 'SY-M02': {'title': 'The most feared man', 'era': 'sylvanis_mastery', 'background': 'arrival'},
 'SY-M03': {'title': 'A useful cause', 'era': 'sylvanis_organisation', 'background': 'compound'},
 'SY-M04': {'title': 'The proposal', 'era': 'sylvanis_proposal', 'background': 'briefing'},
 'SY-M05': {'title': 'The first card', 'era': 'sylvanis_coup', 'background': 'briefing'},
 'SY-M06': {'title': 'The cost of keeping him', 'era': 'sylvanis_expansion', 'background': 'early_office'},
 'SY-M07': {'title': 'Red, blue, and an audience', 'era': 'sylvanis_trials', 'background': 'historic_lab'},
 'SY-M08': {'title': 'The eastern fighters', 'era': 'sylvanis_eastern', 'background': 'eastern'},
 'SY-M09': {'title': 'An amusing applicant', 'era': 'sylvanis_charles', 'background': 'historic_lab'},
 'SY-M10': {'title': 'Business with Mishima', 'era': 'sylvanis_takeo', 'background': 'takeo_meeting'}}
CHAPTERS = {'SY01': {'title': 'A Perfectly Ordinary Order', 'room': 'glasshouse_lab__private_review_reunion_room'},
 'SY02': {'title': 'Everyone Has a Style', 'room': 'glasshouse_lab__private_review_reunion_room'},
 'SY03': {'title': 'A Good Cause', 'room': 'glasshouse_lab__private_review_reunion_room'},
 'SY04': {'title': 'Yes', 'room': 'glasshouse_lab__private_review_reunion_room'},
 'SY05': {'title': 'The Organisation Changes Hands', 'room': 'syndicate_hq__executive_meeting_room'},
 'SY06': {'title': 'Tolerated', 'room': 'syndicate_hq__executive_meeting_room'},
 'SY07': {'title': 'Something New', 'room': 'glasshouse_lab__laboratory_workroom'},
 'SY08': {'title': 'The Eastern Reputation', 'room': 'glasshouse_lab__private_review_reunion_room'},
 'SY09': {'title': 'Let Him In', 'room': 'glasshouse_lab__private_review_reunion_room'},
 'SY10': {'title': 'A Buyer with an Army', 'room': 'site_01__briefing_room'},
 'SY11': {'title': 'Change the Programme', 'room': 'sylvanis_arena__control'},
 'SY12': {'title': 'The Assistant’s Opportunity', 'room': 'glasshouse_lab__private_review_reunion_room'},
 'SY13': {'title': 'One Clear Instruction', 'room': 'syndicate_hq__executive_meeting_room'},
 'SY14': {'title': 'The Exhibition', 'room': 'sylvanis_arena__ring'},
 'SY15': {'title': 'The Crow’s Patience', 'room': 'sylvanis_arena__ring'},
 'SY16': {'title': 'After the Applause', 'room': 'syndicate_hq__executive_meeting_room'}}
for key, spec in MEMORIES.items():
    spec['text'] = deepcopy(MEMORY_TEXT[key])
    spec['after_encounter'] = [p(MEMORY_RETURN_TEXT[key], LAB)]
for key, spec in CHAPTERS.items():
    spec['briefing'] = deepcopy(CHAPTER_TEXT[key])
    spec['aftermath'] = [p(AFTERMATH_TEXT.get(key, 'The account was closed. There were still people waiting for his answer.'), spec['room'])]

# Retained solely for legacy sessions already saved between observation steps.
# New reading completes history on the final page, without journaling prompts.
MEMORY_TASKS = {key: [dict(prompt='Continue the recollection.', options={
    'observe': ('Continue', 'Read the fixed historical sequence.'),
    'context': ('Continue', 'Read the fixed historical sequence.')}),
    dict(prompt='Return to the story.', options={'remember': ('Continue', 'The historical sequence is complete.')})]
    for key in MEMORIES}

ACTION_TEXT={
 'roster':'He inspects the actual supplied roster: a rehearsed pairing with a scheduled finish. No unseen technique or secret appears in it.',
 'provocation':'He chooses whose composure he wants to break first.',
 'reserve':'He commits twenty of eighty campaign operating units to the unsanctioned venue. The ordinary wallet is untouched.',
 'access':'The bounded archive window is granted at the Glasshouse. It is not an admission that Charles’s cover is known.',
 'promise':'He records the authorised delegation and his own additional promise. The two accounts remain distinct.',
 'programme':'Two signed programme copies now give incompatible expectations. The discrepancy is observable evidence, not omniscient deduction.',
 'independent':'Charles’s sealed discrepancy copy and the withheld reserve case receive an independent event receipt. The success cannot be undone by replaying a scene.',
 'cancel':'He acknowledges the direct cancellation and consciously elects to proceed. The Crow withdraws shared support.',
 'exhibition':'The exhibition encounter begins. Actual combat resolves its result; a failed attempt still costs the operation.',
 'finale':'The four-exchange ledger interception begins. Secure the ledger through the combat objective control while the Crow contests each attempt, or seek direct bodily dominance. Shutdown itself is inevitable.',
 'settle':'The shutdown receipt fixes stock, ledger, equipment and campaign account disposition once. The arena remains closed.',
}

def ending_pages(d):
    retained=d.get('settlement',{}).get('ledger')=='sylvanis'
    success=d.get('ending')=='an_expensive_evening'
    return [
      p('The ledger remained with Sylvanis. The Crow secured the remaining consignment and decommissioned the testing equipment. Thirty operating units remained; the expense had bought the serious confrontation he wanted.' if success else ('He had secured the ledger, but the exhibition itself had collapsed. The Crow secured the remaining consignment and decommissioned the equipment. The full eighty-unit operating investment was lost; the paper prize did not turn a spoiled display into the evening he had wanted.' if retained else 'The Crow’s team secured the ledger and remaining consignment. The equipment was decommissioned. The full eighty-unit operating investment was lost. Sylvanis was irritated by a performance that had failed to retain its prize.'),HQ),
      p('Sylvanis turned the last page of the settlement. He had wanted the Crow to abandon the comfort of issuing orders from a distance. The man had come, fought for his own purpose, and left Sylvanis with a cost that could not be laughed out of existence. Even an evening he enjoyed ended by becoming something he already understood.',HQ),
      b('sylvanis','You will find another use for me.',room=HQ),
      b('crow','And you will decide whether it entertains you. We have not mistaken one another for loyal men.',room=HQ),
      p('At Takeo’s headquarters the failed order lay open on the briefing table. Takeo had heard his delegation’s report. He offered no audience for a second version of the performance.',TAKEO),
      b('takeo','The failed demonstration order is closed. Limited supply may resume under revised written terms.' if success else 'The failed demonstration order is closed. That supply line is paused pending a new agreement.',room=TAKEO),
      b('sylvanis','I will try to contain my disappointment.',room=TAKEO),
      b('takeo','Contain it wherever you like. Keep it out of the next agreement.',room=TAKEO),
      p('Sylvanis enjoyed the refusal to turn the exchange into a quarrel. Takeo could not make him dependable by force of wording, but he could refuse to continue paying for a failed promise. No territorial bargain was decided at this meeting. Takeo remained at headquarters when Sylvanis left.',TAKEO),
      p('The Glasshouse was quieter when he returned. Charles had put away the dispatch records and was checking the final exception notice. There was no excitement in his account of the work; the result had not required an audience.',LAB),
      b('charles','The exception report is filed. The supporting copy remains in its separate hold.',room=LAB),
      b('sylvanis','Then we have tomorrow’s work, Charles.',room=LAB),
      b('charles','The copy will remain where it is. It does not depend on what happened at the arena.',room=LAB),
      p('Charles left with his cover intact and his bounded evidence success preserved. Sylvanis watched him go without asking for the storage key. A small piece of the evening had escaped his attention and survived. He found that more promising than the careful respect of the attendants who had spent the night trying not to meet his eyes.',LAB),
      p('Alone, he set the ruined programme beside the Crow’s restriction. He laughed at the price, then stopped. Kaden’s question returned without the man’s voice: whether he would ever truly find the thrill he was looking for. It had not made him remorseful when Kaden was alive. It did not make him remorseful now.',LAB),
      p('He thought of Martos’s knuckle, the thin smear of blood, a result too small to call victory and too unexpected to dismiss. Somewhere between what a body could endure and what a mind could do with the moment available to it, there might still be a question he could not answer before it was asked.',LAB),
      b('sylvanis','Something better, then.',room=LAB),
      p('He opened the research notes. Outside, a member of staff who had been about to knock saw the light still on and walked away. The particular exhibition was over. The Crazed Demon had found another reason to keep looking, and someone else would eventually pay for it.',LAB)]

__import__('sylvanis_campaign_visuals').apply(CHAPTERS,MEMORIES)

def copy_scene(key,field):return deepcopy((MEMORIES if key in MEMORIES else CHAPTERS)[key][field])
