from django.contrib.sites.models import Site
from django.test.client import Client
from django.test import TestCase
from clktc.links.models import Link

EXAMPLE_URL = "http://example.com"

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_all_links(self):
        link = Link(destination_url="http://example.com", short_url="example", site=Site.objects.get(pk=1))
        link.save()
        response = self.client.get('/links/')
        self.assertIn(link, response.context['links'])

    def test_visit_add_link_page(self):
        response = self.client.get('/add/')
        self.assertEquals(response.status_code, 200)

    def test_add_link(self):
        self.client.post('/add/', dict(destination_url=EXAMPLE_URL, short_url="example"))
        link = Link.objects.get(short_url="example")
        self.assertEqual(link.destination_url, EXAMPLE_URL)

