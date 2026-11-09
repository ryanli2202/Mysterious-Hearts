import unittest
from PIL import Image
import mixtape_art as art
import mixtape_catalog as music


class ArtworkTests(unittest.TestCase):
    def test_complete_artwork_and_shared_song_covers(self):
        for artist in music.ARTISTS:
            for kind in ('portrait', 'cover'):
                path = art.artist_path(artist['id'], kind)
                self.assertIsNotNone(path, (artist['name'], kind))
                with Image.open(path) as image:
                    self.assertEqual(image.width, image.height)
                    self.assertGreaterEqual(image.width, 512)
                    image.verify()
            covers = {art.song_path(song['id']) for song in artist['songs']}
            self.assertEqual(covers, {art.artist_path(artist['id'], 'cover')})

    def test_safe_lookup_and_thumbnail_cache(self):
        self.assertIsNone(art.artist_path('../portraits/rei'))
        self.assertIsNone(art.song_path(None))
        self.assertIsNone(art.artist_path('voss', 'unknown'))
        path = str(art.artist_path('voss'))
        small = art.thumbnail(path, 64)
        self.assertEqual(small.size, (64, 64))
        self.assertIs(art.thumbnail(path, 64), small)


if __name__ == '__main__': unittest.main()
