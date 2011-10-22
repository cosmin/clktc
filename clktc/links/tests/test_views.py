from django.contrib.sites.models import Site
from django.test.client import Client
from django.test import TestCase
from clktc.links.models import Link

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_all_links(self):
        Link(destination_url="http://example.com", short_url="example", site=Site.objects.get(pk=1)).save()
        response = self.client.get('/links/')
        self.assertContains(response, '<a href="http://example.com">example</a>')
        

