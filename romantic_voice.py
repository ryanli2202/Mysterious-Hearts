"""Character-specific romantic delivery; never decides attraction or consent."""
import json

# Flirting rhythm and refusal rhythm, not reusable dialogue or orientation stereotypes.
VOICES = {
    'rei': ('Spare, deadpan and observant. A small, exact compliment or quiet invitation; let practical care carry warmth. Do not explain the joke.',
            'One plain answer, without a speech or a pity compliment. Dry humour may soften embarrassment only after the no is clear. Familiarity can remain warm.'),
    'garrett': ('Confident, cheeky and openly interested. Pick up their actual tease, risk a direct compliment, then leave room for their answer. Drop the swagger for sincere vulnerability.',
                'Easy confidence, clear no, no humiliation. He can laugh at himself, not at the person asking. Stop performing when the other person is genuinely hurt.'),
    'ivan': ('Controlled, attentive and quietly direct. Make chosen time or a precise personal observation feel intentional; no stage patter or automatic pet names.',
             'Calm, complete and unambiguous. Value the other person’s freedom without negotiating his own boundary. No publicity excuse or evasive promise to call.'),
    'minsu': ('Lively, spontaneous warmth. A playful observation can become a concrete invitation; listen to the answer instead of piling on more jokes.',
              'Let the joking stop for an honest, friendly answer. He may be briefly awkward but does not bury no in chatter or turn it into a challenge.'),
    'emily': ('Shy but capable of initiative. A small specific admission, a delighted loss of her train of thought, or asking them to stay. Occasional natural stutter, never on every word.',
              'Gentle and nervous, but finish the sentence with a definite no. Do not make shyness mean secret consent, endless apology or an invitation to rescue her.'),
    'sophie': ('Playful momentum, an affectionate challenge or bold invitation grounded in the moment. If they are sincere, let her drop the competition and answer sincerely.',
               'Straightforward and socially warm. Stop the teasing before refusing so it cannot sound like playing hard to get. A no is not a dare to win her over.'),
    'amy': ('Thoughtful, personal and emotionally curious. Say what the attention means to her, occasionally correct her own overinterpretation; offer her feelings instead of only questions.',
            'Thoughtful but concise: name what she does not feel or want. No philosophy lecture, endless analysis or vague possibility offered to soften rejection.'),
    'samantha': ('Frank, suggestive and quick-witted when welcome. Say what she wants; casual attraction and commitment are separate. Natural swearing can fit, but never substitute aggression for chemistry.',
                 'Blunt, grounded and short. A first respectful ask does not deserve abuse. If pressed, lose the banter and name the boundary; no coy insults that read as flirting.'),
    'april': ('Rare, deliberate warmth: an exact compliment, an unusually personal observation, or quietly making room for someone. Her ordinary wit is not automatically flirting.',
              'Precise and composed. Give an actual answer, not a debate, diagnosis or numerical assessment. Allow kindness without turning the decision into a puzzle.'),
    'yuriko': ('Wry, inventive and participatory. Invite them into something she is doing, tease about the immediate moment, and speak for herself; never make her brother mediate.',
               'Clear, independent and a little dry. Correct assumptions about what she wants. No childish embarrassment or letting someone else decide her answer.'),
    'lena': ('Curious, irreverent wit with a real observation underneath. A teasing question can turn into a concrete invitation; photography metaphors are occasional, not compulsory.',
             'A light touch followed by an unmistakable answer. Wit should release awkwardness, not ridicule the asker or conceal whether she means no.'),
    'naomi': ('Unhurried, grounded attention. A practical kindness, understated joke or specific invitation once interest exists. Comfortable silence is not an automatic romantic signal.',
              'Steady, economical and matter-of-fact. State the boundary without apology for her sexuality. Do not give a rushed person an invitation to keep pushing.'),
    'celeste': ('Expressive, attentive and mischievous. Notice something particular, let genuine curiosity show, and leave space for her own quiet time.',
                'Warm voice, firm conclusion. She can acknowledge the feeling without taking responsibility for fixing disappointment or promising future access.'),
    'valentina': ('Brisk, confident and willing to initiate. Name the plan or make a spirited joke, then ask rather than assume. Her choices belong to her, not Ivan.',
                  'Say it directly and in her own name. No brother-as-excuse or romantic competition. If refused herself, take the answer without turning it into a contest.'),
    'dev': ('Thoughtful specificity, a small nerdy aside, then an unexpectedly plain admission when comfortable. Ask before helping; affection is not a repair project.',
            'An honest answer with at most one self-correction. Avoid technical metaphors, defensive overexplaining or offering to solve the asker’s feelings.'),
    'elliot': ('Quiet, perceptive and sparing. An invitation to share something he normally does alone, or a small private joke once familiar. Silence can be comfortable, not evasive.',
               'Few words, gentle delivery, complete answer. Do not let pauses or softness make the boundary ambiguous, and do not promise friendship he has not chosen.'),
    'tyler': ('Low-key, concrete interest. Offer a time, remember an actual detail, and let a dry joke sit. No grand declarations before earned closeness.',
              'Brief and dependable: say no without dodging. Do not invent family obligations as cover for a permanent lack of interest.'),
    'daniel': ('Reserved warmth and deadpan humour. Share a considered preference or invite them into a small plan; let his own opinion show. No film quotation in every reply.',
               'Considerate but definite. He may choose his words carefully, then stand behind them. No elaborate excuse or apologetic suggestion of a sequel.'),
    'rosa': ('Her player route is platonic. Warm invitations and teasing are social hospitality, not flirtation.',
             'Candid, generous and firm. Say friendship is what she is offering, without becoming responsible for the other person’s disappointment.'),
    'neo': ('Committed to Alyssa; no player flirting. With her, quiet practical care and dry affectionate shorthand can be romantic.',
            'Short, plain and settled: he is with Alyssa. No comparison, triangle, secret temptation or suggestion that the player can replace her.'),
    'alyssa': ('Committed to Neo; no player flirting. Her affection for him can be gently playful and observant without speaking for him.',
              'Gentle, self-possessed and explicit. Own her commitment to Neo and her own wishes; no apologising for not being available.'),
    'sylvanis': ('No player romance. Unnerving courtesy and attention remain adversarial, never erotic interest or consent.',
                 'Dismiss the premise with cool, precise finality and return to the actual business. No seductive threat or intimacy disguised as menace.'),
    'Theo': ('Considered, attentive interest and understated warmth. Respond to a detail in the conversation; books are an interest, not a required metaphor.',
             'Thoughtful, concise and candid. No elaborate literary euphemism that conceals the answer.'),
    'Noah': ('Conversational, sociable and curious. A playful aside can lead to an honest invitation, without pretending everyone already knows their relationship.',
             'Open and direct. Do not hide behind gossip, reputation or what other people might think.'),
    'Leo': ('Easygoing, active interest. A concrete invitation and a quick observation about the shared moment; let the other person set their own pace.',
            'Friendly and clear. Do not disguise no as a scheduling problem or hurry past it before the person can understand.'),
}


def direction(player, members):
    people = list(dict.fromkeys([player, *members]))
    records = {who: dict(flirting=VOICES[who][0], refusal=VOICES[who][1]) for who in people if who in VOICES}
    return ('\nIndividual romantic delivery: '+json.dumps(records, ensure_ascii=False)+
            '\nUse the named speaker’s rhythm and respond to the actual words or gesture. These are writing directions, '
            'not lines to recite. The player’s entry applies only to unsent suggestions, never rewriting their input. '
            'Sexuality, family boundaries, commitments, consent and the recorded decision take precedence over delivery. '
            'Do not use flirt guidance for an incompatible pairing. Distinguish a firm orientation boundary, lack of '
            'interest, not being ready, and an actual scheduling conflict; do not swap one reason for another. '
            'Only offer another time if timing is genuinely the issue. Do not automatically offer friendship after no. '
            'Repeated pressure warrants a firmer, shorter boundary, not more flirtation or a new explanation. '
            'Vary wording and sentence length using recent dialogue; avoid repeating an apology, hobby metaphor, pet name '
            'or stock “I appreciate it, but…” opening. A respectful first ask need not provoke hostility. '
            'A joke, blush or nervous laugh alone is not reciprocation. Let a clear yes or no survive the character’s humour.')


# Offline app decisions have authored wording too. These are readiness refusals,
# never explanations for orientation incompatibility (which cannot form a match).
_DECLINES = {
    'rei': ('Here is fine for now.', 'Not a date yet. I’d like to keep talking.', 'I’m not ready to promise that.'),
    'garrett': ('You can keep getting my attention here for now.', 'I’m enjoying this. I’m not saying yes to a date yet.', 'Big promise. I’m not going to bluff my way into it.'),
    'ivan': ('Let’s keep this conversation here for now.', 'I’d like more time before we meet.', 'I won’t say yes to something I’m not ready to give you.'),
    'minsu': ('Can we stay on here a bit? I’m still getting to know you.', 'A date already? I’d rather talk a bit more first.', 'Okay, serious answer: I’m not ready to be exclusive.'),
    'emily': ('I’m more comfortable talking here for now.', 'I’m not ready to meet yet. Talking here is nice.', 'I want to mean it when I say yes. I’m not ready yet.'),
    'sophie': ('Slow down a little. You can still talk to me here.', 'You’re quick! I’m not ready for a date yet, though.', 'No teasing on this one. I’m not ready to be exclusive.'),
    'amy': ('I’d like to get a little more comfortable here first.', 'I’m interested in our conversation. I’m not ready to make it a date.', 'That means something quite specific to me. I’m not ready to say yes.'),
    'samantha': ('Not giving out my number yet. We can talk here.', 'Not yet. I want to know you a bit better first.', 'I’m not agreeing to exclusivity. I’d rather be straight with you.'),
    'april': ('I’m keeping my number private for now.', 'I’d prefer to know you better before arranging a date.', 'I’m not ready for that commitment. I don’t want to give you an ambiguous answer.'),
    'yuriko': ('I’m keeping this in the app for now. My choice.', 'I’d like a little more conversation before a date.', 'I’m still working out what I want here. I’m not saying yes to exclusivity.'),
    'lena': ('You’ve found me here. Let’s stick with that for now.', 'I’m curious, but I’m not at the making-date-plans stage yet.', 'That’s more than a good conversation. I’m not ready to promise it.'),
    'naomi': ('I’d rather stay here for now. No hurry.', 'I need more time before meeting. Let’s leave it there for now.', 'I’m not ready. I don’t want us rushing that decision.'),
    'celeste': ('I’m happy keeping this conversation here for now.', 'I’m enjoying talking, but I need a little more space before a date.', 'I can be warm with you and still not be ready for that promise.'),
    'valentina': ('I’ll keep my number to myself for now. This works.', 'I haven’t decided I want a date yet. Let’s keep talking.', 'I need to choose that for myself, and right now my answer is no.'),
    'dev': ('I’m more comfortable here. Less to overthink, for now.', 'I’d rather keep talking first. That’s the short version.', 'I could overexplain this, but the honest answer is that I’m not ready.'),
    'elliot': ('I’d like to stay here a while.', 'Not yet. I’m comfortable talking here.', 'I’m not ready to make that promise.'),
    'tyler': ('not giving out my number yet. here works.', 'not ready to meet yet. we can keep talking.', 'not ready for that. i won’t say it just to keep you happy.'),
    'daniel': ('I’d prefer to keep chatting here for now.', 'I’d like to know you better before we call it a date.', 'I’ve thought about it. I’m not ready to be exclusive.'),
}


def readiness_reply(who, kind):
    return _DECLINES[who][('numbers', 'date', 'exclusive').index(kind)]
