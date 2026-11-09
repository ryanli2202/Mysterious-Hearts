import unittest
from unittest.mock import Mock, patch
import game_core as core
import job_apps as jobs
from jobseek_workplace_ui import require_workplace, open_workplace
from test_job_apps import place


class WorkplaceTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei'); jobs.apply(self.s,'barista')

    def test_requires_both_locations_and_completed_travel(self):
        place(self.s,'downtown')
        with self.assertRaises(ValueError): require_workplace(self.s)
        self.s['world']['location']='cafe'
        with self.assertRaises(ValueError): require_workplace(self.s)
        place(self.s,'cafe')
        self.s['world']['cast']['rei']['journey']={'destination':'cafe'}
        with self.assertRaises(ValueError): require_workplace(self.s)
        self.s['world']['cast']['rei']['journey']=None
        self.assertEqual(require_workplace(self.s),'barista')

    def test_reviews_and_specialisation_cannot_happen_remotely(self):
        p=jobs.profile(self.s,'barista')
        p.update(rank=2,mentor=20,certificates=['craft'],shifts=15,craft=30,reliability=90)
        place(self.s,'downtown')
        with self.assertRaises(ValueError): jobs.promote(self.s)
        with self.assertRaises(ValueError): jobs.civilian.specialise(self.s,'expert')
        self.assertEqual(p['rank'],2); self.assertIsNone(p['specialty'])

    def test_stale_workplace_and_busy_open_are_rejected(self):
        place(self.s,'cafe')
        jobs.apply(self.s,'model'); place(self.s,'studio')
        with self.assertRaises(ValueError): require_workplace(self.s,'barista')
        game=Mock(state_data=self.s,busy=True)
        with self.assertRaises(ValueError): open_workplace(game)
        game.hide_phone_for_location.assert_not_called()

    def test_phone_physical_action_opens_view_without_performing_work(self):
        from job_apps_ui import JobBoard
        board=object.__new__(JobBoard)
        board.criminal=False; board.in_person=False; board.open_workplace=Mock()
        for fn,args in ((jobs.begin_shift,()),(jobs.resolve,(0,)),(jobs.promote,()),
                        (jobs.civilian.train,('craft',)),(jobs.civilian.network,('mentor',)),
                        (jobs.civilian.specialise,('expert',)),(jobs.civilian.project,()),
                        (jobs.civilian.deliver,()),(jobs.civilian.manage,('team',))):
            board.act(fn,*args)
        self.assertEqual(board.open_workplace.call_count,9)
        self.assertFalse(board.physical_action(jobs.apply,('model',)))
        self.assertFalse(board.physical_action(jobs.civilian.deliver,(True,)))


if __name__=='__main__': unittest.main()
