import unittest
from park_scene import Walker, Renderer, WIDTH, VIEW, STOPS


class ParkTests(unittest.TestCase):
    def test_edges_and_camera(self):
        w=Walker(x=WIDTH-33)
        w.step(1,.05)
        self.assertEqual(w.x,WIDTH-32)
        w.step(1,.05)
        self.assertFalse(w.moving)
        self.assertEqual(w.phase,0)
        self.assertEqual(w.camera,WIDTH-VIEW)
        w.x=33;w.step(-1,.05)
        self.assertEqual(w.x,32)
        self.assertEqual(w.camera,0)

    def test_stride_and_reversal(self):
        w=Walker()
        w.step(1,.05)
        self.assertAlmostEqual(w.phase,2.4/(14/.6))
        w.seated=True;w.step(-1,.05)
        self.assertFalse(w.seated)
        self.assertEqual(w.direction,'left')
        w.step(0,.05);self.assertFalse(w.moving)

    def test_interactions_and_planes(self):
        r=Renderer()
        self.assertEqual(len(r.planes),7)
        self.assertEqual(len(set(f for _,f,_ in r.planes)),7)
        for x,name,_ in STOPS:
            w=Walker(x=x)
            self.assertEqual(w.nearby[1],name)
            self.assertEqual(r.render(w).size,(384,320))
        a=r.render(Walker(x=100));b=r.render(Walker(x=1000))
        self.assertEqual(a.getpixel((20,20)),b.getpixel((20,20)))
        self.assertNotEqual(a.tobytes(),b.tobytes())

if __name__=='__main__':unittest.main()
