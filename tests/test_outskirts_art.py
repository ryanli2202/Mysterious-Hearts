import unittest
from PIL import Image, ImageChops, ImageStat
import artwork
import outskirts


class OutskirtsArtworkTests(unittest.TestCase):
    def test_all_destinations_resolve_to_unique_landscape_art(self):
        contents = set()
        for key in outskirts.VENUES:
            with self.subTest(location=key):
                self.assertEqual(artwork.scene_art(key), 'locations/'+key)
                path = artwork.ASSETS / 'locations' / (key+'.png')
                with Image.open(path) as image:
                    image.load()
                    self.assertGreaterEqual(image.width, 1500)
                    self.assertGreaterEqual(image.height, 900)
                    self.assertGreater(image.width, image.height)
                    contents.add(path.read_bytes())
                self.assertEqual(artwork.source_image(artwork.scene_art(key)).size, image.size)
        self.assertEqual(len(contents), len(outskirts.VENUES))

    def test_lighting_and_weather_render_without_rain_inside(self):
        for key in outskirts.VENUES:
            base = artwork.scene_art(key)
            day = artwork.source_image((base, 'day', 'Clear'))
            night = artwork.source_image((base, 'night', 'Clear'))
            self.assertLess(sum(ImageStat.Stat(night.convert('RGB')).mean),
                            sum(ImageStat.Stat(day.convert('RGB')).mean))
            cloudy = artwork.source_image((base, 'day', 'Cloudy')).convert('RGB')
            for condition in ('Rain', 'Snow'):
                weather = artwork.source_image((base, 'day', condition)).convert('RGB')
                changed = ImageChops.difference(cloudy, weather).getbbox() is not None
                self.assertEqual(changed, key in outskirts.OUTDOORS, (key, condition))


if __name__ == '__main__':
    unittest.main()
