from django.test import TestCase

# Create your tests here.
from .models import SportsCard, Tag, TagCard
from PIL import Image
from django.test import Client
import os
from django.core.files.uploadedfile import SimpleUploadedFile

def setup_dataset():
    # read in txt file and card_pictures dir and populate database
    return

class SportsCardModelTests(TestCase):
    def test_simple_add(self):
        c = Client()
        image_path = './test_dataset/img_1.JPG'
        imgFile = SimpleUploadedFile(name='img_1.JPG', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        response = c.post('/store_card/', 
                          {'option': 'no',
                            'sport': 'NBA',
                            'player': 'Aaron Wiggins',
                            'product': 'optic',
                            'variation': 'blue ice',
                            'import-pic': imgFile,
                            'tags': ''
                            }
                        )
        
        # Check img is saved to card_pictures/card_pictures
        self.assertTrue(os.path.isfile('./card_pictures/card_pictures/img_1.JPG'))
        # Check SportsCard table
        self.assertEqual(SportsCard.objects.all().count(), 1)
        saved_entry = SportsCard.objects.get(pk=1)
        self.assertEqual(saved_entry.sport, 'NBA')
        self.assertEqual(saved_entry.player, 'Aaron Wiggins')
        self.assertEqual(saved_entry.product, 'optic')
        self.assertEqual(saved_entry.variation, 'blue ice')
        # Check Tag table
        self.assertEqual(Tag.objects.all().count(), 1)
        saved_tag = Tag.objects.get(pk=1)
        self.assertEqual(saved_tag.name, 'Non-Base Card')
        self.assertEqual(saved_tag.cards.all().count(), 1)
        self.assertEqual(saved_tag.cards.all().get(pk=1), saved_entry)
        # Check TagCard table
        self.assertEqual(TagCard.objects.all().count(), 1)
        saved_tagcard = TagCard.objects.get(pk=1)
        self.assertEqual(str(saved_tagcard), 'optic Aaron Wiggins blue ice - Non-Base Card')

    def test_simple_delete(self):
        c = Client()
        response = c.post('/delete/1')
        self.assertEqual(SportsCard.objects.all().count(), 0)
