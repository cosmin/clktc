from django.contrib.sites.models import Site
from django.test.client import Client
from django.test import TestCase
from clktc.links.models import Link

EXAMPLE_URL = "http://example.com"


def given_a_link():
    link = Link(destination_url="http://example.com", short_url="example", site=Site.objects.get(pk=1))
    link.save()
    return link

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_all_links_returns_all_links_to_all_template(self):
        link = given_a_link()
        response = self.client.get('/')
        self.assertIn(link, response.context['links'])
        self.assertEqual(response.templates[0].name, "links/all.html")

    def test_add_link_returns_add_link_template(self):
        response = self.client.get('/l/add/')
        self.assertEqual(response.templates[0].name, "links/add.html")

    def test_adding_a_link_creates_link(self):
        self.client.post('/l/add/', {"destination_url" : EXAMPLE_URL, "short_url" : "example"})
        link = Link.objects.get(short_url="example")
        self.assertEqual(link.destination_url, EXAMPLE_URL)

    def test_adding_a_link_redirects_to_all_links_page(self):
        response = self.client.post('/l/add/', {"destination_url" : EXAMPLE_URL, "short_url" : "example"})
        self.assertRedirects(response, "/")

    def test_edit_link_returns_correct_link_to_edit_template(self):
        link = given_a_link()
        response = self.client.get("/l/edit/%s" % link.pk)
        self.assertEqual(response.templates[0].name, "links/edit.html")
        self.assertEqual(response.context['link'], link)


    def test_save_on_edit_link_updates_link_with_new_details(self):
        link = given_a_link()
        self.client.post("/l/edit/%s" % link.pk, {"destination_url" : "http://example.org", "short_url" : "example2"})
        link = Link.objects.get(pk=link.pk)
        self.assertEqual(link.destination_url, "http://example.org")
        self.assertEqual(link.short_url, "example2")

    def test_save_on_edit_link_redirects_to_all_links(self):
        link = given_a_link()
        response = self.client.post("/l/edit/%s" % link.pk, {"destination_url" : "http://example.org", "short_url" : "example2"})
        self.assertRedirects(response, "/")
