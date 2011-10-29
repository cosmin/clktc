from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.test.client import Client
from django.test import TestCase
from clktc.links.models import Link
from clktc.links.views import get_all_links

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_all_links(self):
        link = Link(destination_url="http://example.com", short_url="example", site=Site.objects.get(pk=1))
        link.save()
        response = self.client.get('/links/')
        self.assertIn(link, response.context['links'])

