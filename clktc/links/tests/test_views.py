from django.contrib.sites.models import Site
from django.test.client import Client
from django.test import TestCase
from clktc.links.models import Link

EXAMPLE_URL = "http://example.com/index.html"


def given_a_link(site):
    link = Link(destination_url=EXAMPLE_URL, short_url="example", site=site)
    link.save()
    return link

class ViewBaseTest(TestCase):
    def setUp(self):
        self.site = Site(domain="testserver", name="test")
        self.site.save()
        self.client = Client()

class AllLinksTest(ViewBaseTest):
    def test_get_all_links_returns_all_links_to_all_template(self):
        link = given_a_link(self.site)
        response = self.client.get('/')
        self.assertIn(link, response.context['links'])
        self.assertEqual(response.templates[0].name, "links/all.html")

class AddLinkTest(ViewBaseTest):
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

    def test_adding_a_link_without_destination_url(self):
        response = self.client.post('/l/add/', {"destination_url" : "", "short_url" : "example"})
        self.assertFormError(response, 'form', 'destination_url', u'This field is required.')

    def test_adding_a_link_without_short_url(self):
        response = self.client.post('/l/add/', {"destination_url" : EXAMPLE_URL, "short_url" : ""})
        self.assertFormError(response, 'form', 'short_url', u'This field is required.')

class EditLinkTest(ViewBaseTest):
    def test_edit_link_returns_correct_link_to_edit_template(self):
        link = given_a_link(self.site)
        response = self.client.get("/l/edit/%s" % link.pk)
        self.assertEqual(response.templates[0].name, "links/edit.html")
        self.assertEqual(response.context['link'], link)

    def test_save_on_edit_link_updates_link_with_new_details(self):
        link = given_a_link(self.site)
        self.client.post("/l/edit/%s" % link.pk, {"destination_url" : "http://example.org/"})
        link = Link.objects.get(pk=link.pk)
        self.assertEqual(link.destination_url, "http://example.org/")
    
    def test_save_on_edit_link_redirects_to_all_links(self):
        link = given_a_link(self.site)
        response = self.client.post("/l/edit/%s" % link.pk, {"destination_url" : "http://example.org", "short_url" : "example2"})
        self.assertRedirects(response, "/")

class VisitLinkTest(ViewBaseTest):
    def test_visit_short_url_redirects_to_destination_url(self):
        link = given_a_link(self.site)
        response = self.client.get("/" + link.short_url)
        self.assertEqual(response['Location'], link.destination_url)

    def test_visiting_url_without_proper_site_results_in_404(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.site.delete()
        response = self.client.get('/')
        self.assertEqual(404, response.status_code)
