import unittest, tempfile, json
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import game_core as core
import camera, messaging
from messages_ui import text_messages

class PhotoMessages(unittest.TestCase):
    def test_send_and_reload(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1] / '.test-tmp') as folder:
            path=Path(folder)/'photo.png'; Image.new('RGB',(30,30)).save(path)
            record=dict(id='test',mode='Selfie',location='Home',path=str(path))
            s=core.fresh('rei'); key=s['active']
            with patch.object(camera,'photos',return_value=[record]), patch.object(camera,'photo_path',return_value=path):
                entry=messaging.send(s,key,'',photo_id='test')
                self.assertEqual(entry['photo']['id'],'test')
                restored=json.loads(json.dumps(s))
                self.assertEqual(text_messages(restored)[-1][6]['id'],'test')
                self.assertIn('[Photo: Selfie',text_messages(restored)[-1][1])
                s['groups']['test']=dict(members=[key],history=[],channel='text')
                messaging.send(s,'test','Look!',True,photo_id='test')
                self.assertEqual(text_messages(s,group=s['groups']['test'])[-1][6]['id'],'test')
                path.unlink()
                before=len(s['routes'][key]['history'])
                with self.assertRaises(ValueError): messaging.send(s,key,'',photo_id='test')
                self.assertEqual(len(s['routes'][key]['history']),before)
    def test_foreign_photo_rejected(self):
        s=core.fresh('rei')
        with patch.object(camera,'photos',return_value=[]), self.assertRaises(ValueError):
            messaging.send(s,s['active'],'',photo_id='foreign')

if __name__=='__main__': unittest.main()

