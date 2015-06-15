from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from .models import *
from .views import *
# Create your tests here.

def create_users():
    return SCUser.objects.create(username="sam",email="sam@test.com",first_name="sam",last_name="test",
                                birth_date="2015-1-1",address="via mario 23")
class IndexViewTests(TestCase):
    def test_index_view(self):
        client = Client()
        response = client.get(reverse('socialcircle:index'))
        self.assertEqual(response.status_code,200)
    def test_link_reg(self):
        client = Client()
        response = client.get(reverse('socialcircle:reg'),follow=True)
        self.assertEqual(response.status_code,301)
    def test_login(self):
        client = Client()
        response = client.get(reverse('socialcircle:index'))
        self.assertEqual()

