"""Compile the reviewed MH-005 manuscripts into the game's authored prose library.

Editorial labels are handled explicitly here, never interpreted by the game.
The generated JSON is committed content; playing needs no Markdown or AI service.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sections(filename):
    text = (ROOT / 'roadmap' / filename).read_text(encoding='utf-8')
    result = {}
    chapter = ''
    current = None
    for para in re.split(r'\n\s*\n', text):
        if para.startswith('## '):
            chapter = para[3:].strip()
            current = None
        if para.startswith('### '):
            match = re.match(r'### ((?:[GRF]D|FM)\d+) — (.*)', para)
            current = match[1] if match else None
            if current:
                result[current] = dict(title=match[2].split(' [')[0], chapter=chapter,
                                       source='roadmap/' + filename, blocks=[])
        elif current:
            match = re.match(r'\*\*(.+?)\*\*\s*(.*)', para, re.S)
            if match:
                label, prose = match.groups()
                result[current]['blocks'].append(dict(label=label.rstrip(' :'), inline=bool(prose), paragraphs=[prose] if prose else []))
            else:
                blocks = result[current]['blocks']
                if not blocks:
                    blocks.append(dict(label='', paragraphs=[]))
                blocks[-1]['paragraphs'].append(para.strip())
    return result


def raw_library():
    result = {}
    for name in ('GARRETT', 'REI', 'FOX_GORDON'):
        result.update(sections(name + '_DIALOGUE_MANUSCRIPT.md'))
    return result


# A condition applies only to the labelled paragraph for an inline heading, and
# to the following passage for a stand-alone heading. Unlabelled tails are shared.
CONDITIONS = {
    'GD01': {1: {'support': 'help'}, 2: {'support': 'quiet'}},
    'GD07': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD11': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD12': {1: {'choice': 0}, 2: {'choice': 1}, 3: {'choice': 0}},
    'GD13': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD16': {2: {'choice': 1}, 3: {'choice': 0}},
    'GD18': {1: {'support': 'help'}, 2: {'support': 'quiet'}},
    'GD23': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD24': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD25': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD26': {2: {'disclosure': 'share'}, 3: {'disclosure': 'private'}},
    'GD27': {0: {'disclosure': 'share'}, 1: {'disclosure': 'private'}},
    'GD28': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD29': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD32': {0: {'phase': 'before'}, 3: {'phase': 'after'}},
    'GD34': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD35': {0: {'phase': 'before'}, 2: {'phase': 'after'}},
    'GD38': {0: {'choice': 0}, 1: {'choice': 1}},
    'GD39': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD40': {1: {'choice': 0}, 2: {'choice': 1}},
    'GD42': {0: {'visitor': 'april'}, 1: {'visitor': 'mei'}},
    'RD01': {1: {'choice': 0}, 2: {'choice': 1}},
    'RD02': {1: {'disclosure': 'share'}, 2: {'disclosure': 'private'}},
    'RD06': {0: {'disclosure': 'share'}, 1: {'disclosure': 'private'}},
    'RD15': {1: {'choice': 0}, 2: {'choice': 1}},
    'RD21': {1: {'visitor': 'emily', 'disclosure': 'share'}, 2: {'visitor': 'sophie', 'disclosure': 'share'}, 3: {'disclosure': 'private'}},
    'RD25': {0: {'phase': 'before'}, 2: {'phase': 'after'}},
    'RD26': {0: {'richter': False}, 1: {'richter': True}},
    'RD31': {0: {'phase': 'after'}, 1: {'phase': 'after'}, 2: {'phase': 'failure'}},
    'RD32': {1: {'richter': True, 'disclosure': 'share'}, 2: {'richter': False}},
    'RD33': {1: {'ending': 'lead'}, 2: {'ending': 'leave'}, 3: {'ending': 'destroyed'}},
    'FD05': {0: {'phase': 'before'}, 1: {'phase': 'before','player':'fox'}, 2: {'phase': 'before','player':'gordon'}, 3: {'phase': 'after'}},
    'FD24': {4: {'last_ace': False}, 5: {'last_ace': True}},
    'FD26': {0: {'phase': 'before'}, 2: {'phase': 'before','player':'fox'}, 3: {'phase': 'before','player':'gordon'}, 4: {'phase': 'after'}},
    'FD30': {0: {'phase': 'before'}, 1: {'phase': 'before','player':'fox'}, 2: {'phase': 'before','player':'gordon'}, 4: {'phase': 'after'}},
    'FD38': {1: {'operation':'syndicate_witness'}, 2: {'operation':'syndicate_supply'}, 3: {'operation':'syndicate_coercion'}},
}

# Drop an editorial paragraph (but preserve any unlabelled prose after it).
DIRECTIVES = {
    'GD05':[1], 'GD10':[1], 'GD12':[0], 'GD16':[1], 'GD18':[0],
    'GD20':[0], 'GD22':[1], 'GD23':[0], 'GD24':[3], 'GD26':[1],
    'GD31':[0], 'GD32':[1,2], 'GD35':[1,3], 'GD36':[0], 'GD37':[0],
    'GD38':[2], 'GD41':[0,1,2], 'GD42':[2], 'GD43':[0,1,2],
    'RD05':[1], 'RD10':[1], 'RD11':[0], 'RD16':[1], 'RD19':[1],
    'RD21':[0], 'RD22':[1], 'RD23':[0], 'RD25':[1], 'RD27':[0,1],
    'RD29':[1,2,3], 'RD30':[1], 'RD32':[0,3], 'RD35':[0,1],
    'FD05':[4], 'FD09':[0], 'FD12':[0], 'FD14':[0,3,4,5],
    'FD17':[0,3,4], 'FD20':[0,3,4], 'FD23':[0,3,4], 'FD26':[1,5],
    'FD29':[3,4,5], 'FD30':[3,5], 'FD31':[0], 'FD35':[0],
    'FD37':[0,3,4], 'FD38':[0],
}

# These speeches would require an opponent still present and fit to speak. The
# review happens later at HQ, so it uses the substantial private aftermath only.
DROP_BLOCKS = {'FD15':[0], 'FD18':[0], 'FD21':[0], 'FD24':[0]}


def draft(number):
    t = (ROOT/'roadmap/CAMPAIGN_DIALOGUE_DRAFTS.md').read_text(encoding='utf-8')
    t = re.split(r'## Draft D0' + str(number) + r'[^\n]*\n', t)[1]
    t = t.split('\n## ')[0]
    return [p.strip() for p in re.split(r'\n\s*\n',t) if p.strip() and not p.strip().startswith('**')]


def compiled():
    raw = raw_library()
    result = {}
    for key, scene in raw.items():
        elements = []
        for index, block in enumerate(scene['blocks']):
            if index in DROP_BLOCKS.get(key,[]):
                continue
            label, paras = block['label'], list(block['paragraphs'])
            cond = CONDITIONS.get(key,{}).get(index,{})
            if not cond and (label.startswith(('Fox viewpoint','Fox closing','Fox final','Present return, Fox'))):
                cond = {'player':'fox'}
            if not cond and (label.startswith(('Gordon viewpoint','Gordon closing','Gordon final','Present return, Gordon'))):
                cond = {'player':'gordon'}
            if key in ('FD05','FD26','FD30') and 'phase' in cond:
                scoped = True
            else:
                scoped = not block.get('inline')
            drop = index in DIRECTIVES.get(key,[])
            # A memory marker changes illustration only; no present actor moves.
            if label.startswith('FLASHBACK'):
                caption = label.split('. ')[0].rstrip('.')
                elements.append(dict(text=caption, mode='memory'))
            elif label.lower().startswith(('present return','written present return')):
                elements.append(dict(text='PRESENT DAY', mode='present', when=dict(cond)))
            for n, para in enumerate(paras):
                if drop and (n==0 and block.get('inline') or not block.get('inline')):
                    continue
                when = cond if (scoped or n==0) else {}
                if block.get('inline') and n>0:
                    when={k:v for k,v in cond.items() if k=='phase'}
                elements.append(dict(text=para, when=dict(when)))
        result[key] = {k:v for k,v in scene.items() if k!='blocks'} | dict(elements=elements)

    def replace(key, old, new):
        matches = [e for e in result[key]['elements'] if old in e['text']]
        if len(matches)!=1:
            raise ValueError((key,old,len(matches)))
        matches[0]['text'] = matches[0]['text'].replace(old,new)

    def exact(key, prefix, text):
        matches = [e for e in result[key]['elements'] if e['text'].startswith(prefix)]
        if len(matches)!=1:
            raise ValueError((key,prefix,len(matches)))
        matches[0]['text']=text

    # Final edit of draft instructions embedded within prose paragraphs.
    exact('GD02','He withdrew his hand', 'He withdrew his hand from the phone and selected one page from the present pile. “This one,” he said quietly. He could begin with one thing that was true.')
    exact('GD15','The familiar division', 'The familiar division of washing and drying recalled how it had developed. For Garrett, it began with remembering an order, then noticing when Rei came without one.')
    exact('GD11','Cross-check all three', 'Garrett checked the date, crate count and reference number, then recorded the supported connection. “What work was this account handling?” was a question he could ask without beginning with an accusation.')
    exact('GD11','Treating the name', 'The name alone did not establish the connection. Garrett read the same page after the correction and felt foolish, then angry about feeling foolish. He could wait for tomorrow and ask the narrower question. He could not make a failed enquiry advance by wanting it enough.')
    exact('GD13','The selected accusation', 'He had written a rumour as though it were an answer. The enquiry paused. The accusation produced no confession; the notes still distinguished what he had chosen to claim from what anyone had verified.')
    exact('GD16','The reply cannot', 'The reply could not authenticate him. “No,” Garrett said, too late to make the sent answer different. Certainty said loudly would not repair it. He would have to wait until the next story day to answer again.')
    exact('GD16','The existing reply', 'The reply answered with the unfinished shrimp-shell argument from their last call. A private evening invitation followed: the Glasshouse, between seven and eleven, alone. Garrett unfolded the visitor directions, then returned to the question that had made them possible.')
    exact('GD17','The memory returned', 'The room returned around him. The broth and the argument belonged to his own memory; the reply on the table belonged to the enquiry he had actually made.') if any(e['text'].startswith('The memory returned') for e in result['GD17']['elements']) else None
    exact('GD26','He had come because', 'He had wanted to see April. That was enough reason to be here.') if any(e['text'].startswith('He had come because') for e in result['GD26']['elements']) else None
    exact('GD27','Garrett says,', '“I have an answer I can’t share yet,” Garrett said.\n\n“Then I won’t guess it for you.” Rei moved his cup aside. “Company, or a change of subject?”\n\n“Company. We can find the subject after.”')
    exact('GD27','Garrett asks Rei', 'Garrett asked about Rei’s day and waited for the answer. There was room at the table for something that had happened to someone else.')
    exact('GD29','He ensured the people', 'He made copies for the residents before taking the permitted originals back. The people who had supplied them would not have to ask him to see their own records.')
    exact('GD39','Neither rival had', 'Neither rival had been destroyed. Garrett could feel the unfinished scale of the problem without deciding that every useful thing must therefore be too small. The Dragons would be judged by what happened after the meeting.')
    exact('GD40','He wrote back privately', 'He wrote a private reply, then began preparing the meal. It was personal, with no operational details: an answer to a brother who had finally answered him.')
    exact('GD40','He placed it beside', 'He placed the note beside the recipe. He could answer later. Tonight he could eat without arranging company to prove he was coping.')
    exact('RD06','“I found something.', '“I found something. I’m not ready to show it.”\n\n“Then we can leave it closed,” Yuriko said. “You don’t have to pretend you found nothing.”')
    exact('RD13','Alone again, Rei', 'Alone again, Rei remembered Joseph treating the bullying as something too small to answer for. The storyboard lay on the table in front of him. He let the present settle before following the memory farther.')
    exact('RD21','“I can\'t explain', '“I can’t explain the details,” Rei said.\n\nHis friend accepted the boundary. They could sit together without opening the file. He did not have to turn privacy into an excuse to leave.')
    exact('RD26','The successor outcome', 'The successor outcome was the last outstanding thread. Rei did not have to invent another immediate task because stopping felt unfamiliar. Home could be a place to pause, not the next problem to solve.')
    exact('RD29','Rei checked', 'Rei checked the evidence copy he had retained, then put it away. Carrying proof did not make him immune to what was ahead. He checked the approach before him. This was a mission he would undertake alone.')
    exact('RD31','Omit the entire', '“Not finished,” Rei said, looking at the unresolved objective when he was able. That was all he could accurately call it. He needed recovery and another assessment, not a story in which the confrontation had supplied closure.')
    exact('RD32','“The programme is stopped', '“The programme is stopped,” he said. Sophie nodded once. “All right.” She did not ask him to make that mean everything was finished.')
    exact('FD24','“This one is complete', '“This one is complete,” Gordon said.\n\n“Then we look at the next one as its own problem,” Fox answered. The other enquiries still had their own questions to answer.')
    exact('FD24','Gordon lays the four', 'Gordon laid the four recovered command records together. Fox stood to see them.\n\n“Now we can ask what connects them.”\n\nGordon nodded. “Now. Not before.”')
    exact('FD26','The authenticated summons', 'Gordon compared the recovered summons with the transfer record. Fox watched the check without asking him to skip it because the paper had cost them a fight.')
    exact('FD30','Fox keeps the withdrawal', 'Fox kept the withdrawal route in sight while Gordon covered retreat. The evidence copied before entry remained theirs. They had neither custody nor a new command archive. The Crow remained at headquarters, his birth identity unknown.')
    replace('FM01','while the visible obstruction was dealt with in the limited authored incident. No new named arrest, killing or spectacular victory is supplied.', 'while Fox held the street-facing position. The worker cleared the lane; that was the part Fox could see.')
    # Remove implementation directions that occurred in unlabelled manuscript
    # tails, and turn staging notes into finished, viewpoint-limited prose.
    edits={
      'GD08':{'“Show me the procedure,”':'“Show me how to request it,” Garrett said.'},
      'GD11':{'The retained page was':'The retained page was waiting when the next response arrived. Garrett started with the date, then the crate count, then the reference.'},
      'GD12':{'Garrett heard himself preparing':'Garrett heard himself preparing another accusation and stopped. The clerk would not answer it. He would have to wait until tomorrow and return to the document request.'},
      'GD19':{'When the actual departure':'Garrett was still frightened when the conversation ended. He was also no longer alone with every version of the meeting he had imagined.'},
      'GD21':{'Adult Garrett stood':'Adult Garrett stood at the laboratory approach. Being strong enough to arrive did not make him less in need of an answer. The door in front of him belonged to the present.'},
      'GD28':{'Apply only the chosen':''},
      'GD31':{'A member near the table':'Mina Cho shifted forward.','Another member asked':'Anton Bellamy asked, “What if the collectors say we’re taking over?”','The first member glanced':'Mina glanced toward the door. “Some of us joined because you made it look like we didn’t have to back down.”'},
      'GD32':{'He directed attention':'He checked the exit before looking back at the collection detail.','The weapons were raised.':'The collectors raised their weapons. Garrett would have to face the detail before he could secure the market.','The collectors were defeated':'The collectors were defeated in this incident. Garrett recorded the demands and returned the seized takings to their documented owners. The money had never belonged to him.'},
      'GD34':{'Apply only the existing':'','“You can,” Garrett said, committing':'“You can,” Garrett said. “You don’t owe him a reassuring answer.”','Afterward the crew accepted':'Afterward the crew accepted the written charter. Garrett did not mistake agreement in the room for proof they would never need to test it again.'},
      'GD39':{'He listened to practical objections':'He listened to practical objections about availability and responsibility rather than treating them as disloyalty. The rota would have to be maintained by people who could ask for help themselves.','The existing council choice':'He recorded the commitment to a resident-led council. Agreeing to hear people was the beginning; he could not declare their consent on their behalf.'},
      'GD42':{'“Did you get the bowl back?”':'“Did you get the bowl back?” she asked.','He smiled. The question':'He smiled. The question did not concern a missing man or a new threat. He answered it, then asked which ordinary job she wanted help with.'},
      'RD17':{'He preserved the authorisation':'He kept the authorisation with the complaint and left the unanswered questions visible. The equipment records identified the compound and offices. He copied what he would need before approaching headquarters.'},
      'RD22':{'Rei looked up again. Garrett did':'Rei looked up again. Garrett did not explain the comparison. He simply stayed with the question.'},
      'RD27':{'They made only the arrangement':'They agreed he would let them know when he was able. Neither friend followed him into the operation. Their worry did not become a promise that everything would be all right.'},
      'RD31':{'The powered frame failed':'The powered frame failed. The fight was over. Rei listened to the machinery falling silent.','- “I heard you.':'','The authoritative victory':'Rei secured the research records and disabled the containment controls. The surviving participants could leave.'},
      'FD04':{'The more specific envelope':'The more specific fibres and the observed collection route still mattered. They checked those instead of discarding everything because the first inference had been too large.'},
      'FD05':{'The collector\'s arrival':'The collector had not agreed to stop. The opposition on this route would have to be faced before the witness could be safe from this demand.','A plan looked cleaner':'A plan looked cleaner when nobody had begun to move. Gordon checked the partner beside him. Writing the preparation had not finished his part in it.','Gordon checked what the resolved':'Gordon checked what they had secured before answering. The seized receipt supplied a rail-yard lead. It did not give him a reason to keep a tired witness talking indefinitely.'},
      'FD09':{'They returned to the file':'They returned to the file when the ordinary interruption was finished. The worker’s limited account remained limited; the courier’s materials opened the next lines. A wider investigation did not make the people who had helped into secret experts.'},
      'FM03':{'They divided observation':'They divided observation and protection for the contractor case. Agreeing where to stand did not make either of them invulnerable.'},
      'FD12':{'After the actual successful':'After the successful protection, they checked the contractor’s permitted account once more.','They authorised the enquiries':'They authorised the four enquiries. Before leaving, Gordon checked the contractor’s follow-up arrangement. Fox waited without treating it as an interruption to the important part.'},
      'FD13':{'The actual case reveal':'The original order and independently witnessed deployment identified Martos Cabrera as the Ace of Clubs. The conclusion belonged to the assembled investigation team.'},
      'FD15':{'The record included':'The record included the independently established identity, the victory and the recovered command material. It claimed neither permanent custody nor the destruction of the Suit. Outside the review, both still had the ordinary work of restoring their readiness.'},
      'FD16':{'The correction stayed':'They corrected the attribution with the people they had interviewed. The original instruction and independently observed masked deployment identified Elias Braun as the Ace of Hearts. The finding stayed in the team’s record.'},
      'FD17':{'The refusal leads':'Elias had refused the operation’s request. The conversation had reached its limit; the encounter ahead remained unresolved.'},
      'FD19':{'The actual independent originals':'The independent originals identified Camila Lopez as the Ace of Diamonds. The accounts worker had explained a process, not confessed to a conspiracy. The routine invoice remained genuine.'},
      'FD21':{'Fox nodded. They finished':'Fox nodded. They finished the practical task before returning to the files. Neither pretended a short rest had made the work effortless.'},
      'FD23':{'Mavis was not required':'Mavis waited at the confrontation point and let Gordon state the finding. Her stillness left Fox watching more carefully, not seeing more than was there.'},
      'FD26':{'“Movement ahead,”':'“I want to keep the supported approach in view,” Fox said.'},
      'FD27':{'They continued the existing':'They recorded the authorised operation and its limits. The questions remained part of the plan; a signed approval could not answer them in advance.'},
      'FD28':{'An authorised participant':'Fox asked about the fallback point. Gordon listened before answering.'},
      'FM04':{'Back in the Night Ledger':'Back in the Night Ledger briefing, they confirmed their roles and limits. Protected witnesses would not accompany the raid. The plan was theirs to attempt and theirs to answer for afterward.'},
      'FD29':{'The summons matched':'The summons matched the command entrance and its deployment. Reaching the correct place ended one uncertainty. It did not end the danger.'},
      'FD30':{'No extra escape-wave':''},
      'FD31':{'Fox shifted, then stopped':'Fox shifted, then stopped. There was nothing in the report he could make easier by moving the paper again.'},
      'FD33':{'They made no virtue':'They checked whether they were ready before returning to work. Readiness was not a feeling they could demand from each other.'},
      'FD34':{'They checked only what':'They checked the protected contact route. A future reply would still have to be made; writing down a promise did not keep it.','“No,” Gordon answered,':'“No,” Gordon answered.'},
      'FD36':{'The campaign closes':'The report was complete. The Crow remained at headquarters; the Syndicate remained beyond it. The next piece of work would begin at the public desk, with a specific request and evidence they could check. Neither man mistook that for an ending to every threat.'},
      'FD38':{'After actual success, the protected':'The protected contact received the witness. Fox checked the exit, then returned to Gordon.','The actual encounter resolves':'They recorded the specific shipment interrupted and the records secured. It was one supply run, not a command archive or a promised rematch.','After actual success, the traders':'The traders retained their property and the protected reporting route. Fox asked what practical help remained; Gordon recorded the limited disruption.'},
    }
    for key,mapping in edits.items():
        for prefix,new in mapping.items():exact(key,prefix,new)
    exact('FD37','The quiet after that','The room fell quiet. The record held a completed objective and a contained opponent. Outside, people still needed protection; one line in a file would not supply it.')
    exact('FD05','The promise required','The promise would require follow-through. Gordon wrote the agreed route beside the report, where he would have to see it again.')
    exact('FD05','The shopkeeper asked,','At the headquarters review, the shopkeeper’s last question remained with them. “Can I close?” The answer they had given belonged in the account too.')
    exact('FD30','If both are actually','Later, at the fallback point, they checked the copied evidence together. Their voices were low.')
    exact('FD30','“The route is still there,”','“The route was still there,” Fox said.')
    exact('FD30','“Go. I\'m with you.”','“And we both used it,” Gordon answered.')
    # Failed authentication must not borrow the successful invitation's return.
    e=result['GD17']['elements'][-1];e['when']={'authenticated':True}
    result['GD17']['elements'].append(dict(text='The memory came back with no new reply attached to it. He had answered the enquiry incorrectly. Remembering the cup now would not send another answer or bring tomorrow closer.',when={'authenticated':False}))
    # The two-phase contractor passage avoids claiming frontage corroboration at
    # the earlier interview, and does not relocate the witness to the frontage.
    for i,e in enumerate(result['FD10']['elements']):
        e.setdefault('when',{})['phase']='interview' if i<9 or i in (10,11) else 'after'
    exact('FD10','Later, away from the witness','At the frontage, away from the witness, Fox spoke quietly.')
    exact('FD10','Fox looked toward the closed','Fox looked back toward the verified frontage. “Next question can be smaller.”')
    # Ordinary repeatable-operation outcomes cannot appear in their introduction.
    for index,e in enumerate(result['FD38']['elements']):
        operation=e.get('when',{}).get('operation')
        cutoff={'syndicate_witness':3,'syndicate_supply':12,'syndicate_coercion':16}[operation]
        e['when']['phase']='after' if index>=cutoff else 'before'
    # Shared canonical events use exactly the same spoken exchange in both views.
    canonical = raw['RD04']['blocks'][0]['paragraphs']
    garrett = [
        'Rei had come in alone after a modelling shoot, a sketchbook resting against his leg. Garrett noticed the opened seam before he put the plate down. An imperfect plate was something he could fix.',
        *canonical[1:8],
        'Rei pulled the receipt closer and drew the crooked seam. Garrett returned to clear a little space and stopped beside the table.',
        *canonical[10:17],
        'Rei smiled. Garrett found himself wanting to keep the small joke going.',
        *canonical[18:23],
        'Garrett pinned the receipt up and straightened it. He wanted to remember the customer who had seen something worth keeping in the thing he had meant to replace.',
        '“You don’t have to display it.”', '“I know.”',
        'Rei finished his meal slowly. Garrett returned to work and remembered the order.'
    ]
    # Use a checked shared dialogue list below, rather than fragile prose slices.
    shared_lines = ['“Give me that one. I’ll replace it.”','“It’s all right.”','“It’s opened.”','“I can see that.”',
                    '“Is that a complaint?”','“It has more character than the intact ones.”',
                    '“That sounds suspiciously like a polite complaint.”','“I ate it.”','“A committed critic.”',
                    '“Can I keep that?”','“What for?”','“To remember the standard I’m being held to.”',
                    '“It isn’t a standard.”','“Good. I was worried I’d have to break one on every plate.”',
                    '“You don’t have to display it.”','“I know.”']
    viewpoints = {
        'GD04': [garrett[0], 'Rei pulled the receipt closer and drew the crooked seam. When Garrett returned, he glanced at the paper.',
                 'The answer surprised Garrett into a smile. Here was a customer taking the care he had put into the meal seriously, without asking him to apologise for its seam.',
                 'Rei pushed the receipt toward him. Garrett pinned it up and straightened it. He wanted to keep this small encounter somewhere he could see it.',
                 'Rei finished his meal slowly. Garrett returned to work and remembered the order.'],
        'RD04': [canonical[0], 'Rei pulled the receipt closer and drew the crooked seam. When Garrett returned, he glanced at the paper.',
                 'Rei felt himself smile before he decided whether to encourage him.',
                 'Rei pushed the paper toward him. Garrett pinned it up rather than dropping it beside the till. Rei watched the small care with which he straightened it.',
                 'For once, Rei had no answer ready. He finished his meal more slowly than he needed to.']}
    for key, interiors in viewpoints.items():
        ret = result[key]['elements']
        pos = next(i for i,e in enumerate(ret) if e.get('mode')=='present')
        prose = [interiors[0], *shared_lines[:4], interiors[1], *shared_lines[4:9], interiors[2],
                 *shared_lines[9:14], interiors[3], *shared_lines[14:], interiors[4]]
        result[key]['elements'] = [dict(text='FLASHBACK — Golden Dragon, early months',mode='memory')] + [dict(text=p) for p in prose] + ret[pos:]

    # Install the four substantial passages that the manuscripts reference.
    result['RD11']['elements'] = [dict(text='The folded corner of the storyboard brought back another school morning. Rei sat at his own table and let the memory come.'),dict(text='FLASHBACK — School courtyard',mode='memory')] + [dict(text=p) for p in draft(1)] + result['RD11']['elements']
    result['GD22']['elements'] = [dict(text=p) for p in draft(2)] + [e for e in result['GD22']['elements'] if not e['text'].startswith(('Use the complete','Begin with the complete'))]
    for e in result['GD22']['elements']:
        if e['text'].startswith('For months, Garrett'):break
        e['when']={'direct':False}
    result['GD41']['elements'] = [dict(text=p) for p in draft(3)]
    result['FD32']['elements'] = [dict(text=p,when={'player':'gordon'}) for p in draft(4)]
    # Fox's version preserves the shared spoken dialogue while supplying only his
    # perceptions. The alternative interiors are authored in FD32, not generated.
    fox_blocks = raw['FD32']['blocks'][2:9]
    d4 = draft(4)
    private_prefixes = ('Gordon had read','Fox sat on','Gordon looked at the page.',
                        'For a moment Gordon wanted','Gordon looked toward','A small nod.', 'Gordon changed the first sentence.')
    fox = fox_blocks[0]['paragraphs'][:]
    for p in d4:
        if p.startswith(private_prefixes):continue
        fox.append(p)
        if p.startswith('“So does what'):fox.extend(fox_blocks[1]['paragraphs'])
        elif p.startswith('“What do you want'):fox.append(fox_blocks[2]['paragraphs'][0])
        elif p.startswith('“We failed to contain'):fox.append(fox_blocks[3]['paragraphs'][0])
        elif p.startswith('Fox pushed the paper'):fox.extend(fox_blocks[4]['paragraphs'])
        elif p.startswith('“I know.” Fox looked'):fox.extend(fox_blocks[5]['paragraphs'])
    fox.extend(fox_blocks[6]['paragraphs'])
    result['FD32']['elements'] += [dict(text=p,when={'player':'fox'}) for p in fox]
    # Remove manuscript cross references and compiler-facing instructions.
    for key,scene in result.items():
        for e in scene['elements']:
            e['text'] = e['text'].replace('---','').strip()
            e['text'] = re.sub(r'\*([^*]+)\*',r'\1',e['text'])
        scene['elements'] = [e for e in scene['elements'] if e['text']]
    return result


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    library = compiled()
    output = ROOT/'campaign_prose/catalog.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(dict(version=1,scenes=library),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Compiled {len(library)} authored sections to {output}')
