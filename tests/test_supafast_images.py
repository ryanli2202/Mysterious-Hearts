import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import codex_images
import game_core as core
import phone_apps as apps
import supafast
from supafast_fixtures import seed


class ProductImageTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp')
        self.addCleanup(self.folder.cleanup)
        self.path=Path(self.folder.name)
        self.store=patch.object(codex_images,'STORE',self.path)
        self.store.start();self.addCleanup(self.store.stop)
        self.state=core.fresh('rei');seed(self.state)
        self.ident,self.product=next(iter(apps.catalog(self.state).items()))
        self.day=self.state['world']['minute']//1440
        Image.new('RGB',(32,32),'#233545').save(self.path/'item.png')
        self.result={'id':'test-job','path':str(self.path/'item.png')}

    def test_saved_reference_and_duplicate_commit(self):
        original=copy.deepcopy(self.product)
        self.assertTrue(supafast.commit_image(self.state,self.day,self.ident,original,self.result))
        self.assertEqual(supafast.image_path(self.product),self.path/'item.png')
        restored=json.loads(json.dumps(self.state))
        self.assertEqual(supafast.image_path(apps.catalog(restored)[self.ident]),self.path/'item.png')
        self.assertFalse(supafast.commit_image(self.state,self.day,self.ident,original,self.result))
        self.assertEqual(self.product['name'],original['name'])

    def test_stale_day_and_changed_listing_rejected(self):
        old=copy.deepcopy(self.product)
        self.product['description']='Different contents'
        self.assertFalse(supafast.commit_image(self.state,self.day,self.ident,old,self.result))
        self.state['world']['minute']+=1440
        self.assertFalse(supafast.commit_image(self.state,self.day,self.ident,self.product,self.result))
        self.assertNotIn('image',self.product)

    def test_outside_missing_and_invalid_files_rejected(self):
        for path in (core.ROOT/'assets/ui/phone-wallpaper-rei.png', self.path/'missing.png'):
            with self.assertRaises(ValueError):
                supafast.commit_image(self.state,self.day,self.ident,self.product,{'id':'x','path':str(path)})
        (self.path/'bad.png').write_text('not an image')
        with self.assertRaises(OSError):
            supafast.commit_image(self.state,self.day,self.ident,self.product,{'id':'x','path':str(self.path/'bad.png')})
        self.assertNotIn('image',self.product)
        self.product['image']='../outside.png'
        self.assertIsNone(supafast.image_path(self.product))

    def test_prompt_uses_the_listing_and_dark_studio(self):
        prompt=supafast.image_prompt(self.product)
        self.assertIn(self.product['name'],prompt)
        self.assertIn(self.product['description'],prompt)
        self.assertIn('dark slate',prompt)
        self.assertIn('No text',prompt)

if __name__=='__main__':unittest.main()
