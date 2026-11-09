import consequences
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as c
import town
from date_fixtures import finish_date, invite, afternoon_state

def arrive(s, place):
    if s['world']['location'] == place: return
    town.travel(s, place); town.finish_drive(s)

def sleep_home(s):
    arrive(s, town.loop.HOUSES[s['player']][0]); town.rest(s)
    from date_fixtures import next_morning
    next_morning(s)

def visit(s, who):
    # Let a scheduled journey finish before driving to this character.
    if s['world']['cast'][who]['journey']: town.wait(s, 30)
    arrive(s, s['world']['cast'][who]['location'])

class TownTests(unittest.TestCase):
    def test_richter_at_blackstone(self):
        for player in c.playable_cast.ORIGINAL:
            s = c.fresh(player)
            arrive(s, 'blackstone_hq')
            self.assertIn('Robin Vale', s['world']['npcs'])
            self.assertEqual(s['world']['npcs'].count(town.RICHTER), 1)
            scene = town.generate_npc(s, town.RICHTER, None)
            self.assertEqual('Takamura' in scene['lines'][0]['text'], player == 'rei')
            town.commit_npc(s, town.RICHTER, None, scene)
            self.assertFalse(s['npc_chats'][town.RICHTER]['ordered_tones'])
            with patch('groups.generate_exchange') as generate:
                town.generate_npc(s, town.RICHTER, 'What do you mean?')
                self.assertEqual(town.RICHTER_HISTORY in generate.call_args.args[1], player == 'rei')
            arrive(s, 'square')
            with self.assertRaises(ValueError):
                town.npc_details(s, town.RICHTER)

    def test_pizza_counter_and_shared_table(self):
        s = c.fresh('garrett')
        arrive(s, 'marios_pizza')
        dish = 'Cheese corner slice'
        balance = s['world']['money']
        town.order_pizza(s, dish)
        self.assertEqual(s['world']['money'], balance - 5)
        for who in ('rei', 'april'):
            town.summon(s, who)
        before = copy.deepcopy(s)
        with self.assertRaises(ValueError):
            town.order_pizza(s, dish, ['rei'], date=True)
        self.assertEqual(s, before)
        town.order_pizza(s, dish, ['rei', 'april'])
        self.assertEqual(s['shared_events'][-1]['witnesses'], ['rei', 'april'])
        self.assertEqual(s['relationships']['april']['status'], 'childhood friends')
        s['relationships']['april']['status'] = 'official'
        invite(s, 'april')
        town.order_pizza(s, dish, ['april'], date=True)
        self.assertNotIn('date', s['relationships']['april'].get('firsts', {}))
        self.assertEqual(s['world']['money'], balance - 30 - town.dating.PRICE)
        self.assertEqual(s['relationships']['april']['status'], 'official')
        s['world']['money'] = 0
        before = copy.deepcopy(s)
        with self.assertRaises(ValueError):
            town.order_pizza(s, dish)
        self.assertEqual(s, before)

    def test_yuriko_sibling_boundary_and_romance_routes(self):
        for player in c.playable_cast.ORIGINAL:
            state = c.fresh(player)
            state['active'] = 'yuriko'
            self.assertTrue(c.is_texting(state))
            visit(state, 'yuriko')
            town.meet(state, 'yuriko')
            if player == 'rei':
                with self.assertRaises(ValueError):
                    town.relationship(state, 'yuriko', 'date')
                town.social_event(state, 'yuriko', 'returned_flirt')
                bond = town.character_stats(state, 'yuriko')
                self.assertEqual((bond['attraction'], bond['trust'], bond['closeness']), (0, 98, 95))
                self.assertIn('supportive', c.tone_guide(state))
            else:
                finish_date(state, 'yuriko')
                self.assertEqual(state['relationships']['yuriko']['status'], 'dating')

    def test_starting_relationships_depend_on_protagonist(self):
        garrett, rei = c.fresh('garrett'), c.fresh('rei')
        for who in town.GIRLS:
            if who not in c.hidden.CAST:
                self.assertNotEqual(garrett['relationships'][who], rei['relationships'][who])
            for state in (garrett, rei):
                r = state['relationships'][who]
                self.assertTrue(all(0 <= r[key] <= 100 for key in ('attraction', 'trust', 'closeness')))
                self.assertNotIn(r['status'], town.ROMANTIC_STATUSES)
        self.assertGreater(rei['relationships']['emily']['closeness'], garrett['relationships']['emily']['closeness'])
        self.assertGreater(garrett['relationships']['april']['trust'], rei['relationships']['april']['trust'])
        untouched = c.fresh('rei')
        rei['relationships']['emily']['known_betrayals'].append('test')
        self.assertEqual(untouched['relationships']['emily']['known_betrayals'], [])

    def test_starting_types_support_dating_and_block_breakup(self):
        for player in c.playable_cast.ORIGINAL:
            for who in town.GIRLS:
                state = afternoon_state(player)
                with self.assertRaises(ValueError): town.relationship(state, who, 'breakup')
                visit(state, who)
                town.meet(state, who)
                if not town.romanceable(state, who):
                    with self.assertRaises(ValueError):
                        town.relationship(state, who, 'date')
                    continue
                if who in town.hidden.CAST:
                    town.hidden.add_contact(state, who)
                finish_date(state, who)
                self.assertEqual(state['relationships'][who]['status'], 'dating')
                town.relationship(state, who, 'breakup')
                self.assertEqual(state['relationships'][who]['status'], 'friends')

    def test_existing_relationship_progress_is_preserved(self):
        state = c.fresh('rei')
        state['relationships']['emily'].update(attraction=67, trust=81, closeness=73, status='official')
        before = copy.deepcopy(state)
        town.ensure(state)
        self.assertEqual(state, before)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'story.json'
            c.save(state, path)
            loaded=c.load(path)
            for key,value in before.items(): self.assertEqual(loaded[key],value)
            self.assertIn('memory_store',loaded)

    def test_stat_migration_preserves_old_progress(self):
        s=c.fresh()
        r=s['relationships']['emily']
        del r['attraction']; del r['closeness']
        r['affection']=67; r['trust']=83
        town.ensure(s)
        self.assertEqual((r['attraction'],r['trust'],r['closeness']),(67,83,0))
        r['closeness']=24; town.ensure(s)
        self.assertEqual(r['closeness'],24)
        self.assertNotIn('affection',r)

    def test_closeness_growth_limits_and_betrayal(self):
        s=c.fresh(); r=s['relationships']['emily']
        initial = r['closeness']
        friend_initial = s['friendships']['rei']['closeness']
        town.conversation_progress(s,'emily'); town.conversation_progress(s,'emily')
        self.assertEqual(r['closeness'],initial + 2)
        sleep_home(s); town.conversation_progress(s,'emily')
        self.assertEqual(r['closeness'],initial + 4)
        town.conversation_progress(s,'rei')
        self.assertEqual(s['friendships']['rei']['closeness'],friend_initial + 2)
        self.assertNotIn('attraction',s['friendships']['rei'])
        self.official(s)
        before_betrayal = r['closeness']
        self.assertGreater(before_betrayal, initial + 4)
        visit(s,'sophie'); finish_date(s, 'sophie')
        consequences.disclose(s, 0, 'emily')
        self.assertEqual(r['closeness'],before_betrayal - 25)
        sleep_home(s); town.conversation_progress(s,'emily')
        self.assertEqual(r['closeness'],before_betrayal - 25)
        r['closeness']=99
        with self.assertRaises(ValueError): town.relationship(s,'emily','repair')
        self.assertEqual(r['closeness'],99)

    def test_economy_and_inventory(self):
        s=c.fresh(); self.assertEqual(s['world']['money'],100000)
        with self.assertRaises(ValueError): town.buy(s,'plush')
        import phone_apps
        from supafast_fixtures import seed
        seed(s)
        stock = phone_apps.catalog(s)
        item = next(iter(stock)); price = stock[item]['price']
        town.buy(s,item)
        visit(s,'emily'); town.relationship(s,'emily','gift',item)
        self.assertEqual(s['world']['inventory'][item],0)
        self.assertEqual(s['relationships']['emily']['attraction'],town.STARTING_RELATIONSHIPS['garrett']['emily'][0] + 5)
        with self.assertRaises(ValueError): town.relationship(s,'emily','gift',item)
        arrive(s,'flowers'); town.work(s)
        with self.assertRaises(ValueError): town.work(s)
        self.assertEqual(s['world']['money'],100220-price)
        s['world']['money']=0; arrive(s,'boutique')
        with self.assertRaises(ValueError): town.buy(s,'chess')

    def official(self,s):
        visit(s,'emily')
        for _ in range(3): finish_date(s, 'emily')
        invite(s, 'emily', 'official')

    def test_cheating_disclosure_is_persistent(self):
        s=c.fresh(); self.official(s)
        visit(s,'sophie'); finish_date(s, 'sophie')
        consequences.disclose(s, 0, 'emily')
        self.assertEqual(s['relationships']['emily']['status'],'strained')
        self.assertTrue(s['relationships']['sophie']['known_betrayals'])
        self.assertFalse(s['relationships']['amy']['known_betrayals'])
        self.assertIn('tension',s['girl_bonds']['emily:sophie'])
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'story.json'; c.save(s,p); self.assertEqual(c.load(p),s)
        with self.assertRaises(ValueError): town.relationship(s,'emily','repair')
        with self.assertRaises(ValueError): town.relationship(s,'emily','repair')
        self.assertTrue(s['relationships']['emily']['known_betrayals'])

    def test_breakup_before_dating_is_not_cheating(self):
        s=c.fresh(); self.official(s); town.relationship(s,'emily','breakup')
        visit(s,'sophie'); finish_date(s, 'sophie')
        self.assertFalse(s['relationships']['emily']['known_betrayals'])

    def test_npcs_and_travel(self):
        s=c.fresh(); arrive(s,'cafe')
        self.assertTrue(1 <= len(s['world']['npcs']) <=3)
        name = s['world']['npcs'][0]
        result = dict(narration='The crowd thins.', lines=[dict(speaker=name, text='Quiet today.')],
                      choices=['For once.', 'How was yesterday?', 'Busy later?', 'I like it.'])
        result['emotions'] = {'garrett': 'curious', name: 'relieved'}
        result['input_tone'] = 'Friendly'
        result['bond_moments'] = {name: 'none'}
        result['personal_choices'] = c.personal_choices(s, {})
        with patch.object(c, 'request', return_value={'message': {'content': json.dumps(result)}}) as request:
            for reply in (None, result['choices'][1], 'Did the rain keep people away?'):
                exchange = town.generate_npc(s, name, reply)
                context = json.loads(request.call_args.args[1]['messages'][-1]['content'])
                self.assertEqual(context['player_reply'], reply)
                if reply: self.assertEqual(context['recent_exchange'][-1]['text'], 'Quiet today.')
                town.commit_npc(s, name, reply, exchange)
                self.assertEqual(c.emotions.current(s, 'garrett'), 'curious' if reply else 'content')
                self.assertEqual(c.emotions.current(s, name), 'relieved')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'npc.json'
            c.save(s, path)
            self.assertEqual(c.load(path)['npc_chats'], s['npc_chats'])
        with self.assertRaises(ValueError): town.generate_npc(s,'Nobody','Hello')
        s['routes']['emily']['channel']='in_person'; town.travel(s,'track')
        self.assertEqual(s['routes']['emily']['channel'],'text')

    def test_legacy_save_and_male_contacts(self):
        s=c.fresh('rei')
        for k in ('world','relationships','girl_bonds'): del s[k]
        for k in c.PLAYERS: del s['routes'][k]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'story.json'; c.save(s,p); loaded=c.load(p)
        self.assertEqual(loaded['world']['money'],100000)
        for player,other in [('garrett','rei'),('rei','garrett')]:
            s=c.fresh(player); s['active']=other
            with patch.object(c.chatgpt_provider,'settings',return_value={'provider':'ollama','model':''}):
                prompt=c.build_messages(s,'Hello')[0]['content']
            self.assertIn('Keep suggested replies friendly and nonromantic',prompt)
            self.assertIn('rei: straight',prompt)
            scene={'speaker':c.PLAYERS[other],'addressee':c.PLAYERS[player], 'choices_speaker':c.PLAYERS[player], 'narration':'A notification arrives.', 'dialogue':'How have you been?', 'memory':'They texted.', 'choices':['Good. You?','Busy day.','Meet later?','Tell me more.']}
            c.validate_response(scene,s); c.commit(s,'Hello',scene)
            self.assertEqual(c.transcript(s)[1][0],c.PLAYERS[other])

    def test_chat_romance_reports_cheating_only_on_commit(self):
        s=c.fresh(); self.official(s); s['active']='amy'
        scene={'narration':'They share a kiss.', 'dialogue':'That meant something.', 'memory':'They kissed.', 'choices':['Stay?','Talk?','Dinner?','Walk?'], 'romance_event':'romance'}
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError): c.commit(s,'Kiss',dict(scene,choices=[]))
        self.assertEqual(s,before)
        c.commit(s,'Kiss',scene)
        consequences.disclose(s, 0, 'emily')
        self.assertEqual(s['relationships']['emily']['status'],'strained')

if __name__=='__main__': unittest.main()
