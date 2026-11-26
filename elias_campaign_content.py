"""The Last Applause: authored scenes, never a source of gameplay receipts."""
from copy import deepcopy

def b(speaker=None,text='',narration='',room=None):
    beat=dict(player='',speeches=[[speaker,text]] if speaker else [],narration=narration)
    if room:beat['room']=room
    return beat
def p(text,room=None):return b(narration=text,room=room)

MEMORIES={
 'EL-F03':dict(title='Let them come',age=23,era='elias_defence23',text=[
  p('Germany, the Braun estate outside Hamburg. Elias is twenty-three. Johanna lays the absorption demand beside his rehearsal pages rather than on top of them. He notices the courtesy and straightens the two piles himself.'),
  b('elias-johanna','They want the routes, the accounts and the right to give instructions here.'),
  b('elias','Then they have mistaken an address for an invitation.'),
  b('elias-johanna','This is not a review you can charm into being favourable.'),
  b('elias','No. Reviews require rather more patience.'),
  p('He hands her the script because he wants it kept clean. The first armed formation approaches with a plan for taking the entrance and controlling the family guards. Elias meets it himself. A second formation changes direction toward the loading approach. Johanna marks the two other deployments waiting beyond the courtyard.'),
 ],after_encounter=[
  p('The entrance force withdraws without its intended access. Elias takes the second leader off balance at the loading approach, disarms him and turns the surviving formation back through its own opening. The victories are his; the disciplined attackers were neither an audition nor willing victims. No one has yet defeated him.'),
  b('elias','Competent. They even changed the entrance.'),b('elias-johanna','There are still two formations outside. I have marked both.'),
  p('Present, in the booked receiving office: Johanna points to the promise in Konrad’s pledge. Elias will do again what he did before. He recognises the description because it is true. What follows it is an assumption Konrad has no right to make.'),
 ]),
 'EL-F04':dict(title='The last force falls',age=23,era='elias_defence23',text=[
  p('The third formation takes the courtyard in disciplined pairs. Elias enjoys the problem of its spacing. Heat gathers through his moving body; stopping his movement would limit what he can release. The fourth and final breaching team waits for the courtyard signal, then attacks a different entrance. No reserve deployment remains behind these two.'),
  b('elias-konrad','They think a different door will make a different man of you.'),b('elias','Let us give the door its chance.'),
  p('He studies the courtyard formation’s spacing, then shifts his weight toward its open side. Beyond it the final team is already moving. He will have to answer both.'),
 ],after_encounter=[
  p('The final breaching team loses its leader’s weapon and its line. Elias drives the surviving attackers back through the courtyard exit himself. Johanna checks all four deployments against her report: entry force, loading approach, courtyard reserve, final breaching team. Every incoming formation has lost. The Syndicate’s losses are real; Elias has needed no rescuer.'),
  b('elias-konrad','There. What could they possibly send that changes this?'),b('elias','Someone who has listened, perhaps.'),
  p('There is time afterward for food, sleep and recovery. At the later appointment his body moves without pain or hesitation. He has slept deeply, eaten well and tested the full strength of his hands. He changes into clean clothes and waits in the family meeting room.'),
  p('Present, at the loading office: Elias turns the dispatch carbon toward the light. Konrad has written the victories as if they were an answer to every future question. Elias sets the carbon beside the independent log and checks the next line.'),
 ]),
 'EL-F05':dict(title='Someone above him',age=23,era='elias_duel23',text=[
  p('At twenty-three, Elias waits in his family’s crime headquarters outside Hamburg. Every incoming formation has lost. His body is rested and ready. He expects to set the terms for the next visitor.'),
  p('The clear floor of the family meeting room leaves neither man a convenient excuse. The masked visitor arrives without a captive, threat against a relative or assisting fighter. Family witnesses remain outside the exchange.'),
  b('elias','Every force you sent has lost. I thought you should hear the terms from me.'),
  b('crow','You have made your ability clear. Your family’s independence ends here.'),
  p('Elias hears certainty where irritation should have been. He steps forward to test it, sure of what his body can do. His first movement earns heat. The man across from him watches his planted foot and the shift of weight.'),
 ],after_encounter=[
  p('The Crow takes his balance and fixes his shoulder against the family meeting-room floor. Elias tries to rise. The counter turns that effort into a clear physical impossibility. He cannot continue. No lack of strength excuses it. For the first time, the limit in the room belongs to him.'),
  b('crow','You are capable. That does not place you above me.'),
  p('Fear arrives with the knowledge of what this man could do next. Awe follows so closely that Elias cannot separate them. He has spent his life noticing when an audience understands him. Now he is the one trying to understand. The pressure releases only after the defeat is unmistakable. He watches the gloved hand withdraw and remembers its economy.'),
  p('Present, alone in the dressing room: a stage cue sounds beyond the closed door. Elias removes a sentence from his drafted report describing how impressive the evening will be. The useful facts remain. Lotte knocks and asks whether he is ready. He answers warmly and means it. Loving the work has survived; the thought of one other person’s judgement follows him out.'),
 ]),
}

DUEL_COUNTERS={
 'rhythm':('Elias changes tempo and commits a heated strike. The Crow gives ground just far enough to deny its delivery, then answers inside the recovery. Heat remains Elias’s own; no power has been stolen.','Elias varies his rhythm again. The Crow waits for the committed foot, interrupts that line and leaves the heated hand without a useful path.'),
 'leverage':('Elias closes on a trained throw. The Crow changes his base before the turn closes. Elias recognises the ordinary placement of foot and hip. Recognising it does not make him faster than it.','Elias changes grips and commits a second control entry. The Crow breaks the angle before the leverage becomes a throw and returns him to the open floor.'),
 'distance':('Elias creates distance and combines a feint with a new entry. The Crow answers the actual entry, taking its balance rather than chasing the feint. Excellence has changed the question; the answer is still beyond him.','Elias shortens the combination and steps to a new side. The Crow meets the changed line, controls the shoulder and denies the next step.'),
}

CHAPTERS={
 'EL-01':dict(title='A familiar invitation',room='syndicate_hq__executive_meeting_room',briefing=[
  p('Elias arrives with a rehearsal page folded beneath his operational robe. At the executive desk he leaves it there. The Crow has opened an affiliate report at the Braun family name. Elias recognises the seal before he reads the disputed undertaking.'),
  b('crow','Your relative has pledged reserves and a security team without the administrator’s authority. Establish what he has committed. Preserve the operations I retain.'),
  b('elias','Johanna will have kept the accounts. Konrad has always preferred making the speech.'),
  b('crow','Then bring accounts. End the breach. You are not being sent to inherit the family.'),
  b('elias','Understood, master.'),
  p('His answer comes faster than the graceful remark he had prepared. He waits until the Crow closes the file before reaching for the rehearsal page again.'),
  p('Later, at the Winterfield theatre’s booked receiving office, Johanna arrives for their agreed private meeting. The production is visiting from Germany. Braun hospitality investment has brought Johanna and Konrad to the opening in Winterfield. Johanna keeps the operational folder closed until the door is shut.','elias_theatre__receiving'),
  b('elias-johanna','Konrad promised the reserve before he asked me to release it. He put your name in the pledge.'),
  b('elias','My name has acquired a very busy life without me.'),
  b('elias-johanna','You can laugh after we stop the transfer. There are wages in that reserve.'),
  p('Elias puts away the smile. He asks her to retain the originals and arrange a proper comparison. Johanna waits until he has finished before she draws the case toward her chair.'),
 ],aftermath=[
  p('At the stage, Lotte waits with the marked scene. Her interest is the visiting production and its working company. The private folder has remained behind in the booked office.','elias_theatre__stage'),
  b('elias-lotte','Your entrance is late if you keep greeting the room before you hear the cue.'),b('elias','The room looked lonely.'),b('elias-lotte','The scene is lonelier. Come and give it someone to answer.'),
  p('He takes his mark. Her correction makes him laugh, and the next entrance is exact. He is glad to be here. The assignment and the play will both require more than his pleasure in being wanted.'),
 ]),
 'EL-02':dict(title='Everyone was certain',room='elias_theatre__stage',briefing=[
  p('Elias misses no cue in the next run. He hears a small change in his partner’s breathing and leaves room for the response; the scene ends on the silence Lotte wanted. The company’s attention is specific, earned by what he has done.'),
  b('elias-lotte','Keep that pause. You let her finish the thought without taking the room away.'),b('elias','I do occasionally permit other people a thought.'),b('elias-lotte','A promising new phase.'),
  p('Her dry reply sends him back to another room where a teacher had waited for a difficult phrase and found a ten-year-old ready to offer a variation.'),
 ],aftermath=[
  b('elias-lotte','Good work. Same scene at the next call; keep the lightness in the first entrance.'),b('elias','And the pause.'),b('elias-lotte','You heard it.'),
  p('He did. He could describe exactly why it worked. For a moment the praise is enough on its own. Then he catches himself wondering how the Crow would have phrased the same judgement. This audience has given him something real. He cannot make it answer for a person who was never here.'),
 ]),
 'EL-03':dict(title='A crown too small',room='elias_theatre__receiving',briefing=[
  p('Johanna has three calls to return before she can sit. Elias offers to make the difficult one charming. She gives him the wage schedule instead.'),
  b('elias-johanna','Tell me which promise charm pays on Friday.'),b('elias','The one made to people who enjoy my company.'),b('elias-johanna','They all enjoy it. Two still need paying.'),
  p('He reads the schedule. The work she has carried is familiar enough to make his old refusal precise again.'),
 ],aftermath=[
  b('elias','I left you a rather unglamorous coronation.'),b('elias-johanna','You left an empty chair. I accepted the work. Do not turn it into a gift you gave me.'),
  p('He hands back the schedule without offering to rescue her from it. She has kept the organisation alive under terms he finds less interesting than an audience. Konrad’s offer will not make that work disappear.'),
 ]),
 'EL-04':dict(title='Let them come',room='elias_theatre__receiving',briefing=[p('The original commitment waits in Johanna’s case. Before inspecting it, Elias remembers the first time his family had asked him to answer an outside demand.'),b('elias-johanna','Read what Konrad promises on your behalf. Then decide what the paper proves.')],aftermath=[b('elias','The signature is his. The undertaking is not mine.'),b('elias-johanna','That distinction will need more than your refusal. He has pledged resources I administer.')]),
 'EL-05':dict(title='The last force falls',room='elias_theatre__loading',briefing=[p('A dispatch carbon in the theatre’s service office names the same security allocation as Konrad’s pledge. Elias studies the approach before he compares its stamps. The habit recalls the courtyard outside Hamburg.')],aftermath=[p('The independent duty log corroborates the dispatch carbon. Elias keeps the two sources apart. A familiar family seal is no substitute for an independent record.')]),
 'EL-06':dict(title='Someone above him',room='elias_theatre__dressing',briefing=[p('Alone before the report, Elias holds his phone without sending it. He can still remember the distance between the family table and the clear floor. He puts the phone face down and lets the earlier room return.')],aftermath=[p('He hears the cue again. His drafted report has useful facts, a correct recipient and no promise that the evening will be magnificent. He reads the address twice before leaving the dressing room.')]),
 'EL-07':dict(title='The terms of survival',room='elias_theatre__receiving',briefing=[
  p('Johanna compares the current revenue obligation with the reserve Konrad has promised away. There is a difference between a family surviving and a family remaining independent. She has had to administer that difference every month.'),
  b('elias-johanna','He speaks as though we woke the next morning under a different flag and went on doing the same work. We report the accounts. We do not deploy our own force against the Syndicate.'),b('elias','I remember the terms.'),b('elias-johanna','You remember the person who gave them. Read the terms with me.'),
 ],aftermath=[
  b('elias','The reserve cannot support an independent force. Konrad has pledged exactly that.'),b('elias-johanna','And I need the operations kept running after he loses the right to sign. We still have employees on Monday.'),
  p('He marks the obligations she names. Affection for his family will not make the subordination voluntary for them; fascination with their conqueror will not settle their wages.'),
 ]),
 'EL-08':dict(title='Master',room='elias_theatre__receiving',briefing=[
  p('Johanna agrees to compare the dispatch with the original reserve ledger. Elias asks who entered the allocation, who witnessed the instruction and which signature can cancel it. For once he lets the uninteresting answer finish.'),
  b('elias-johanna','The dispatch clerk can corroborate a route instruction. The clerk cannot tell you what Konrad promised privately.'),b('elias','Then we keep the two statements apart until the records join them.'),
  p('The discipline of a limited report recalls his first assignment in direct service. He had wanted a task large enough to explain why the Crow had kept him.'),
 ],aftermath=[
  b('elias-johanna','Those entries establish the same reserve, same security allocation and same unauthorised pledge. They do not establish that every person on the duty list supported him.'),b('elias','Only the signatures and the instructed deployment go into the report.'),
  p('Johanna returns the ledger to its case. The originals remain hers until an authenticated sealing. Elias has the verified trail needed for the next appointment. His private reason for wanting to succeed has not become evidence for anyone else.'),
 ]),
 'EL-09':dict(title='One person’s judgement',room='elias_theatre__dressing',briefing=[
  p('Lotte leaves the revised call sheet on the dressing table. Elias has written three extra preparations on the back of his own copy. None was requested by the Crow. One occupies the next rehearsal slot.'),
  b('elias-lotte','If you need a changed call, ask me before the company waits. I can move a scene. I cannot move yesterday.'),b('elias','An unforgiving view of time.'),b('elias-lotte','A practical one. Tell me what you can attend.'),
  p('He remembers a short acknowledgement in an earlier room, and the absurd space it had occupied afterward. He can keep this commitment, agree a new time or spend it on unrequested extra preparation. Lotte can judge only what he does about the work she shares.'),
 ],aftermath=[
  p('A later memory: at twenty-five, in a private headquarters appointment, the Crow named him Ace of Hearts. Public influence, psychological operations and spectacle under direct authority. Elias accepted the post. The family chair remained Johanna’s; the Hearts Suit retained its own command.'),
  p('Present, at twenty-seven: Elias folds the call sheet where the agreed time can still be read. A career is made from returning to work other people are trying to finish. His next report to the Crow cannot do that work for them.','elias_theatre__dressing'),
 ]),
 'EL-10':dict(title='Other kinds of service',room='syndicate_hq__cross_branch_operations_room',briefing=[
  p('The private operations room holds three practical questions. Mavis checks where the public route ends. Martos asks who receives the defeated commander. Camila asks for the original source of every line Elias has underlined. The family folder contains no volunteered personal confession.'),
  b('mavis','The audience leaves through the front. Your security argument stays at the service entrance. If you change that, tell me before I start.'),b('elias','A modest stage for such a distinguished company.'),b('mavis','It needs a door. Not a stage.'),
  b('martos','Johanna accepts responsibility. Her receiving team must have a route and an arrival time. Defeating him leaves someone who still needs guarding.'),b('elias','I will not leave your receiving line blank.'),
  b('camila','Which part did he ask for?'),b('elias','All of it would be useful.'),b('camila','That was not my question.'),
  p('He separates the objective from the flourish he imagined would announce its success. Each colleague will still need to accept a defined task and actually arrive when it is done.'),
  p('A separate executive appointment follows. Sylvanis is already there by his own arrangement. No family confession accompanies Elias into the room.','syndicate_hq__executive_meeting_room'),
  b('sylvanis','Must every little assignment come back wrapped so neatly?'),b('crow','The useful ones return with an accurate result.'),
  p('Elias feels the urge to correct Sylvanis’s tone. He has no authority to do it. The Crow has answered for himself. Elias keeps his hands still, gives the limited operational report and leaves the other appointment intact.'),
 ],aftermath=[
  p('Back in the operations room, the roles have to be agreed separately. Elias writes a separate arrival confirmation beside each role, leaving it blank until the colleague can attend.','syndicate_hq__cross_branch_operations_room'),
  b('elias','Civilian cover, records authentication, perimeter and handover. Each has a name, a limit and a stop condition.'),
  p('He can tell a colleague why the work matters to him privately, or keep the personal account to himself. Neither choice replaces the operational information needed for the agreed task.'),
 ]),
 'EL-11':dict(title='The performance he wants',room='elias_theatre__receiving',briefing=[
  p('Konrad attends the private receiving appointment with a proposal he has polished for years. It gives Elias the family chair, the force he once defended and a chance to make the world watch him do it again. There are no spectators in the office to hear the criminal business.'),
  b('elias-konrad','Every force they sent you lost. They have traded on one man walking into our house ever since. Lead us. Let them remember the first part.'),b('elias','You have a gift for ending a story one sentence before its point.'),
  b('elias-konrad','You could be the man who restores us.'),b('elias','I serve the man you want me to oppose. That answer will not change if you offer me a larger chair.'),
  p('The loyalty is settled. The method is not. Quiet coordination can preserve the reserve and the reset. A conspicuous private demonstration can draw the security allocation into a place Elias can defeat it, at a stated reserve and production cost. He checks both routes against Johanna’s timing. The quiet route keeps the reserve free. The demonstration draws the security allocation where he wants it, but the reset will have to wait.'),
 ],aftermath=[
  p('Elias looks at the arrangements he has chosen. Konrad has offered no surrender; the men and money promised in his name will not return merely because he has refused the invitation. Beyond the office, the production is preparing for an evening whose private dangers the company has no reason to know.'),
 ]),
 'EL-12':dict(title='The instruction he was given',room='syndicate_hq__executive_meeting_room',briefing=[
  p('Elias reports the verified commitment, independent dispatch and original reserve ledger. He names Johanna’s actual obligations and the method he has chosen. He does not describe the breakaway pledge as every employee’s intention.'),
  b('crow','Preserve the affiliate’s useful operations. Revoke the commitments through its administrator. Secure the records. Stop the armed attempt at control.'),b('elias','The audience remains outside it. Johanna remains administrator.'),b('crow','And the cost you commit belongs in the result.'),b('elias','Yes, master.'),
  p('He had imagined a more elaborate instruction. This one is clear enough to leave him responsible for what he adds.'),
  p('At the separate private receiving appointment, Johanna checks the limited detention authority and names the affiliate security receiving team. The instruction authorises a supervised handover after disarm and revocation. It does not turn a combat result into custody.','elias_theatre__receiving'),
  b('elias-johanna','I sign the removal of his signing and security authority. My team receives him after the perimeter is secure. They will not take an armed man through the audience.'),b('elias','I will report when the route is ready, then wait for the team to arrive.'),
 ],aftermath=[
  p('Johanna puts her copy beside the receiving instructions. Elias checks the time at which his colleagues are expected. He has promised her an end to the breach. She has asked him to leave her something that can continue afterward.'),
 ]),
 'EL-13':dict(title='The last applause',room='elias_theatre__stage',briefing=[
  p('In the public performance, Elias takes the first entrance without greeting the audience ahead of his character. His partner reaches the difficult pause and finds him listening. The scene opens around the response. For the length of it, the room has the company’s complete attention.'),
  p('After the curtain, Lotte catches him in a quiet dressing-room interval. The audience remains beyond the closed doors.','elias_theatre__dressing'),
  b('elias-lotte','That is the scene. Keep it for the next performance.'),b('elias','I was hoping you would demand the impossible. This is much more exacting.'),
  p('Beyond the closed dressing-room door, the spectators leave with a play to discuss. Elias can still hear the applause. He allows himself a moment to enjoy it before the next appointment.'),
  p('In the private loading court, the selected plan meets Konrad’s armed security allocation. The public route must be separated with Mavis before the confrontation begins. Camila has asked for the original ledger. Johanna has left the revocation line unsigned until the weapon is secured. Martos checks the route the receiving team will use.','elias_theatre__loading'),
  b('elias-konrad','You would put our family under him again.'),b('elias','You committed its money and people without its administrator. That ends here.'),
  p('He could still make a speech large enough for the whole theatre. Instead he checks the service door signal and the actual space in which the team can work. The Crow is not here to rescue him or watch him succeed.'),
 ],aftermath=[
  p('The handover receipt names the defeated, disarmed man, the revoked authority, Johanna as custodian and the receiving team that actually arrived. The sealed ledger retains its original words. The civilian route remained outside the service confrontation.','elias_theatre__loading'),
  b('elias-johanna','I can keep the operations open with this. I still have to do it.'),b('elias','And I still owe you the accurate report, rather than a flattering version of the family.'),
  p('He gives her the copy with every paid cost still visible. The task is complete on its own conditions. The desire for a particular answer from another room has not disappeared with it.'),
 ]),
 'EL-14':dict(title='After the curtain',room='elias_theatre__receiving',briefing=[
  p('Johanna signs the working settlement beside the actual receiving receipt. The affiliate remains under its reporting, revenue and non-independent-force obligations. Konrad no longer controls its signatures or security allocation. She keeps the administrator’s work, not a reward for admiring Elias.'),
  b('elias-johanna','You did the thing I needed. It does not make what we lost four years ago feel chosen.'),b('elias','I know.'),b('elias-johanna','Keep knowing it when he asks for more.'),
  p('She takes her copy. Elias leaves the office with neither the family chair nor a convenient reconciliation in his hands.'),
 ],aftermath=[
  p('In Lotte’s dressing room, the production has a next call. She responds to the commitment Elias actually kept, revised or missed; she receives no operational report.','elias_theatre__dressing'),
  b('elias-lotte','The scene is worth doing again. Your place in the company still requires you at the call.'),b('elias','It will have me. With the entrance after the cue.'),
  p('He means the promise. Art has not become merely an alibi for his other work.'),
  p('At the arranged private headquarters report, Elias puts the intact result and its actual costs on the executive desk.','syndicate_hq__executive_meeting_room'),
  b('elias','The breach is closed, master. Johanna retains the affiliate. The original records are secured, the commitments revoked and Konrad received under her authority.'),
  b('crow','Keep it useful. I expect its reach to increase.'),b('elias','Yes, master.'),
  p('It is a further obligation, not a declaration of affection. Elias remembers the exact wording all the way back to the theatre.'),
  p('The empty stage smells of warmed lamps and dust disturbed by dancers’ shoes. Elias takes his mark and speaks the entrance into the quiet. He loves the line enough to try it twice. Between attempts he checks the message containing his next instruction. He has kept a company’s work and the Crow’s objective. He is still listening for the judgement he cannot supply for himself.','elias_theatre__stage'),
 ]),
}

MEMORIES.update({
 'EL-F01':dict(title='Everyone was certain',age=10,era='elias_childhood10',text=[
  p('Elias is ten. In the Braun estate’s music room, Anja Keller plays a difficult phrase once and asks him to follow its shape. He plays it cleanly, then tries a variation that leaves her hand suspended over the next page. The gift is real. So is the practice that taught his fingers to offer it.'),
  b('elias-anja','Again. The second ending this time. You can hear where it goes; let the others hear it too.'),b('elias','The first one ends before it is finished being interesting.'),b('elias-anja','Then make the second earn its extra time.'),
  p('He does. Later, a short family performance finds him changing his voice and posture so completely that the kitchen staff stop clearing the table to watch. He bows to the person whose chair had been left behind the doorway, inviting her laugh into the room.'),
  b('elias-konrad','You see? Whatever he tries.'),
  p('Supervised physical practice supplies another pleasure: balance, timing, a turn learned with an adult stopping the exercise before it becomes dangerous. Anja calls the exercise finished while he is still eager for another turn. He succeeds at what he is actually taught. Praise gathers around the success until it begins to sound like the natural order of the house.'),
  b('elias','May I do the scene again after supper? I have a better ending.'),
 ],after_encounter=[p('Present, on the stage: Elias hears the pause he learned to leave for another actor. Being praised had not been a fraud. Neither is the pleasure of finding a better ending in front of people who can answer him. He returns to the work before he returns to the report.')]),
 'EL-F02':dict(title='A crown too small',age=21,era='elias_actor21',text=[
  p('At twenty-one, Elias leaves the family estate for the separate German repertory theatre. The rehearsal waits across town, well away from the family table. On stage Lotte Weiss lets him try an entrance that fails, then another that opens the scene. He stays after the run because he wants to find out what the next attempt can do.'),
  b('elias-lotte','The first version showed us you were clever. The second let the scene happen.'),b('elias','I should resent how much more enjoyable the second was.'),b('elias-lotte','You can resent it at tomorrow’s call.'),
  p('Back at the estate’s private meeting room, Konrad offers him the succession. Johanna is present with accounts that someone will need to administer.'),
  b('elias-konrad','They would answer to you. You could make the table your own.'),b('elias','You want me to spend my life waiting for those men to finish telling me how important they are?'),b('elias-konrad','They would be listening to you.'),b('elias','I would still have to listen to them.'),
  b('elias-johanna','Somebody has to answer the creditors as well.'),b('elias','You understand that work. I want the stage.'),
  p('His refusal is contempt for criminal peers he considers beneath him, not a moral rejection of the family’s crime. Acting offers discovery as well as admiration. Johanna accepts administration because the work needs doing, not because his refusal has appointed her to a smaller form of greatness.'),
 ],after_encounter=[p('Present, Johanna returns the wage schedule to its folder. Elias remembers how easily he once left the table. Talent had given him a choice; other people had carried what he chose to leave.')]),
 'EL-F06':dict(title='The terms of survival',age=23,era='elias_settlement23',text=[
  p('A separate quiet interval follows the duel. Elias is twenty-three. In the family meeting room, Johanna has the accounts open for the arranged private settlement appointment. Konrad waits elsewhere. The Crow remains masked. Elias watches him enter and feels his own shoulder tighten at the remembered pressure.'),
  b('crow','The organisation remains useful. Its operations continue under my authority, with reporting, revenue obligations and no independent deployment against me.'),
  p('Johanna accepts internal administration of a retained affiliate. The family keeps operating, but loses independent control of its routes and force. Elias enters the Crow’s direct personal service. He does not take the family chair. The two decisions share a room without becoming the same decision.'),
  b('elias-johanna','The wages continue through the existing operations. I need the reporting interval and the signatory named.'),b('crow','You administer it. The accounts return through the stated channel.'),
  p('After the Crow leaves, Johanna calls Konrad back to review the family obligations. He sits farther from the head of the table than he used to.'),b('elias-konrad','We defended our own house.'),b('elias-johanna','And we still have people living from its work. I am asking what tomorrow requires.'),
  p('Later, alone at a separately arranged service appointment, Elias watches the hand that closes the terms. Fear remains in the attention. So does a need to understand how the man who defeated him can be so economical while changing everyone else’s future.'),
  b('elias','What would you require of me?'),b('crow','Competence under instruction. Your family’s administration is not your post.'),
  p('His answer is direct service, not instant appointment as an Ace. He has not received the Hearts role or command of a Suit. Relatives can be relieved, angry and grateful in different proportions. Their responses cannot turn the loss of independence into his personal triumph.'),
 ],after_encounter=[p('Present: Johanna opens the old settlement beside the current reserve obligation. The terms remain. Konrad’s pledge still contradicts them. Elias draws his chair to the table and reads with her.')]),
 'EL-F07':dict(title='Master',age=24,era='elias_service24',text=[
  p('At twenty-four, before appointment as Hearts, Elias receives a limited private service assignment. Observe a contractor’s genuine commitment, obtain its signed schedule and return the discrepancies. He wants to offer a spectacle that will demonstrate why he was kept.'),
  b('crow','A signed schedule and the discrepancies. Do not manufacture a larger task.'),b('elias','Yes, master.'),
  p('The word still catches behind his teeth. In ordinary rooms he can make people comfortable and turn attention where he wants it. In this room he hears his own breathing and remembers the pressure that would not let his shoulder rise.'),
  p('He interviews the contractor privately, listens past a flattering answer and compares the schedule with the actual loading time. He returns the discrepancy he observed. A successful small assignment is useful on its own terms. It does not purchase an audience’s surrender or the Crow’s approval.'),
  b('elias','The time on the signed schedule is wrong. The loading began twelve minutes earlier. This is the corrected observation, not a confession I could not obtain.'),b('crow','Then record it accurately.'),
  p('He has done the task. The absence of a larger answer stays with him longer than the conversation. He rehearses the report in his head afterward, wondering which version would have made the man look up for another moment.'),
 ],after_encounter=[p('Present, Elias lets Johanna complete the corroboration. He can obtain the useful observation without making the speaker admire him. Remembering that limit does not make him stop wanting a very particular audience.')]),
 'EL-F08':dict(title='One person’s judgement',age=24,era='elias_acknowledgement24',text=[
  p('At twenty-four, still before Hearts, Elias brings a corrected operational report to a private appointment. He has retained the missed opportunity as well as the useful result. The Crow reads the source line, then the correction.'),
  b('crow','That is useful. Keep the distinction in future reports.'),b('elias','I will, master.'),
  p('A few ordinary words of judgement acquire an absurd weight. He knows exactly what was acknowledged: an accurate distinction. By the time he leaves the family-site appointment he has considered whether the wording means a place kept for him. The report contains no such promise.'),
  p('At the separate German theatre, Lotte is waiting for a run. She has not heard the private conversation and knows nothing of the man behind it. Elias warms the room with a ridiculous imitation of a pompous reviewer, then hears her next correction at once.'),
  b('elias-lotte','You are smiling before the character has a reason.'),b('elias','A private triumph. I shall remove it from his face.'),b('elias-lotte','Keep your triumph. Give him his own moment.'),
  p('He finds the moment because he loves the scene. Afterward the acknowledgement returns before he has untied his shoes. Fear and awe have grown into a habit of measuring the day against one person’s response. Neither theatrical success nor private usefulness has put him on equal terms with that person.'),
 ],after_encounter=[p('Present: Lotte’s call sheet remains on the dressing table. Elias can protect or renegotiate the actual commitment, or miss it for an extra task nobody ordered. The call time is still legible beneath his added notes. He turns the sheet toward Lotte before answering.')]),
})

ACTION_TEXT={
 'task':{
  'assignment':'Elias records the bounded assignment and its private audience. Acceptance supplies no evidence, custody or inherited command.',
  'rehearsal':'Elias attends the actual rehearsal call with Lotte. He repeats the scene with the exact pause she marked. The work gives her grounds for professional praise; it discloses none of his private assignment.',
  'commitment':'Johanna opens the original signed pledge. Elias compares the signature, reserve allocation and promised service team. The source is retained intact and distinguished from what Konrad has merely said.',
  'dispatch':'Elias spends three minutes and six stamina checking the loading office’s dispatch carbon against its independent duty log. The matching allocation corroborates a real instruction. The report names its scope rather than treating every employee as a conspirator.',
  'obligation':'Johanna and Elias compare reporting, revenue and force obligations with the reserve promise. She remains administrator. Historical affiliation does not automatically settle current compliance.',
  'corroborate':'The signed pledge and independent dispatch agree with Johanna’s original reserve ledger. Elias records the source chain and its exact original text. Securing and authenticating the original at the final site remain separate tasks.',
  'roles':'All three specialists have individually accepted their bounded roles. They still need actual availability and arrival when those roles are performed.',
  'prepare':'The verified trail, selected method and accepted roles are recorded with Johanna’s limited signed revocation and detention authority. The authorised affiliate receiver must be called after the route is secured, then actually arrive. Readiness is not completed custody.',
 },
 'rehearsal_choice':{'keep':'Elias keeps the rehearsal call he agreed with Lotte. He completes the work before any optional extra preparation. He leaves the extra preparation until after the company’s work.','renegotiate':'Elias asks before the company waits. Lotte agrees a revised call. Five minutes pass while the stage manager adjusts the sheet; the professional commitment is changed explicitly, not silently abandoned.','extra':'Elias misses this call for unrequested extra preparation. Twenty minutes and ten stamina are committed. Lotte records the lost run and requires a reset. The cost is his decision, not an order the Crow gave.'},
 'method':{'quiet':'Elias commits to a coordinated quiet containment plan. It depends on the agreed roles and actual attendance. The reserve remains available for the production reset.','bold':'Elias commits to a viable conspicuous private demonstration drawing the armed security allocation to the loading court. Eighteen stamina and fifteen minutes are spent. The reserve allocation and production reset are consumed by the plan. Civilian separation and the actual encounter remain necessary.'},
 'separate':'Mavis performs the agreed cover task in the actual loading area. The audience and company use the public route; service access is separated before confrontation. Their knowledge remains the public production, without operational titles or family records.',
 'objective':'Elias enters the actual armed confrontation in the private loading court. The Crow is absent. Resolve resistance through combat; a win will not itself seal records, disarm Konrad, revoke his authority or transfer custody.',
 'seal':'Camila checks the original reserve ledger against the recorded hash and source chain. The intact ledger is sealed for Johanna’s secured affiliate archive. The receipt names an actual recipient and authenticator.',
 'disarm':'With the actual armed resistance stopped, Elias secures Konrad’s weapon. Five stamina and one minute are spent. A defeated and disarmed man still requires revoked authority, a perimeter and a receiving handover.',
 'revoke':'Johanna attends and signs removal of Konrad’s signing and security authority. His unauthorised commitments are cancelled through her retained administrative authority. Elias takes no family chair or Suit command.',
 'perimeter':'Martos performs the accepted perimeter task. Eight stamina and two minutes are committed to the receiving route. Johanna’s authorised affiliate security receiving team is called and will arrive five minutes later. Until then, the disarmed man remains held at the secured site.',
 'custody':'The authorised affiliate security receiving team actually arrives and receives disarmed Konrad under Johanna’s limited authority. The handover receipt records the encounter, revoked control, secure route, recipient and minute. This is supervised private detention, not Interpol custody or a global faction capture.',
}

def ending_pages(d):
    lines=deepcopy(CHAPTERS['EL-14']['aftermath'])
    missed=d['choices'].get('missed_rehearsal')
    for beat in lines:
        if beat.get('speeches') and beat['speeches'][0][0]=='elias-lotte':
            beat['speeches'][0][1]='The scene worked. The lost run still belonged to everyone waiting for you. I need the next call kept.' if missed else 'You gave the company the time we agreed. The scene is worth doing again. Keep the next call as well.'
    if d.get('ending')=='expensive_performance':
        index=next(i for i,beat in enumerate(lines) if beat.get('speeches') and beat['speeches'][0][0]=='crow')
        lines[index:index]=[b('crow','The useful result does not erase the additional cost in your report.',room='syndicate_hq__executive_meeting_room'),b('elias','I will not call it necessary simply because it succeeded, master.',room='syndicate_hq__executive_meeting_room')]
    return lines

def initialise():
    __import__('elias_campaign_manuscript').apply(CHAPTERS,MEMORIES)
    __import__('elias_campaign_visuals').apply(CHAPTERS,MEMORIES)

def copy_scene(key,field):return deepcopy((MEMORIES if key.startswith('EL-F') else CHAPTERS)[key][field])

initialise()
