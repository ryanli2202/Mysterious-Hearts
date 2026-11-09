import json
import unittest
import mixtape_catalog as music
import lifestyle_apps as apps
import game_core as core


class MixtapeTests(unittest.TestCase):
    def test_edit_preserves_legacy_and_shared_snapshot(self):
        state = core.fresh('rei')
        old = apps.save_playlist(state, 'Old', 'Personal song — Friend')
        apps.share_playlist(state, old['id'], 'emily')
        entries = [dict(id=None, label=old['tracks'][0]), dict(id='haneul-01')]
        edited = apps.edit_mixtape_playlist(state, 'New name', entries, 'New memory', old['id'])
        self.assertEqual(edited['song_ids'], [None, 'haneul-01'])
        self.assertEqual(len(apps.ensure(state)['playlists']), 1)
        self.assertEqual(apps.ensure(state)['shares'][0]['content']['title'], 'Old')
        with self.assertRaises(ValueError):
            apps.edit_mixtape_playlist(state, 'Invalid', [dict(id=None, label='Invented')], playlist_id=old['id'])
        self.assertEqual(edited['title'], 'New name')

    def test_complete_catalogue(self):
        self.assertEqual((len(music.ARTISTS), len(music.GENRES), len(music.SONGS)), (44, 11, 1056))
        for artist in music.ARTISTS:
            self.assertTrue(artist['description'])
            self.assertEqual(len(artist['songs']), 24)
            self.assertEqual(len({s['title'] for s in artist['songs']}), 24)
            self.assertTrue(all(s['description'] for s in artist['songs']))
        self.assertEqual(music.SONGS['haneul-01']['title'], '달빛 (Moonlight)')

    def test_save_share_and_legacy_compatibility(self):
        state = core.fresh('rei')
        legacy = apps.save_playlist(state, 'Old', 'Custom song — Old artist')
        ids = ['kai-mercer-23', 'riven-banks-20']  # Same title, different artists.
        item = apps.save_catalog_playlist(state, 'Night Shift', ids, 'A night out')
        apps.share_playlist(state, item['id'], 'emily')
        restored = json.loads(json.dumps(state))
        self.assertEqual(restored['lifestyle_apps']['playlists'][1]['song_ids'], ids)
        self.assertEqual(item['tracks'], ['Night Shift — Kai Mercer', 'Night Shift — Riven Banks'])
        self.assertEqual(legacy['tracks'], ['Custom song — Old artist'])
        self.assertEqual(restored['lifestyle_apps']['shares'][0]['content']['tracks'], item['tracks'])
        for invalid in ([], ['missing'], ids*2, list(music.SONGS)[:31]):
            with self.assertRaises(ValueError): apps.save_catalog_playlist(state, 'Bad', invalid)
        self.assertEqual(len(apps.ensure(state)['playlists']), 2)


if __name__ == '__main__': unittest.main()
