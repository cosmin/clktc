from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test.client import Client
from django.test import TestCase
from clktc.links.models import Link

ALL_LINKS = '/l/links/'

EXAMPLE_URL = "http://example.com/index.html"


def given_a_link(site):
    link = Link(destination_url=EXAMPLE_URL, short_url="example", site=site)
    link.save()
    return link

class ViewBaseTest(TestCase):
    def create_user(self):
        self.user = User(username='test', is_active=True)
        self.user.set_password("test")
        self.user.save()

    def authenticate(self):
        self.client.login(username='test', password='test')

    def create_site(self):
        self.site = Site(domain="testserver", name="test")
        self.site.save()

    def setUp(self):
        self.client = Client()
        self.create_site()
        self.create_user()
        self.authenticate()

class AllLinksTest(ViewBaseTest):
    def test_get_all_links_returns_all_links_to_all_template(self):
        link = given_a_link(self.site)
        link.user = self.user
        link.save()
        response = self.client.get(ALL_LINKS)
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
        self.assertRedirects(response, ALL_LINKS)

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
        self.assertRedirects(response, ALL_LINKS)

class VisitLinkTest(ViewBaseTest):
    def test_visit_short_url_redirects_to_destination_url(self):
        link = given_a_link(self.site)
        response = self.client.get("/" + link.short_url)
        self.assertEqual(response['Location'], link.destination_url)

    def test_visiting_url_without_proper_site_results_in_404(self):
        response = self.client.get(ALL_LINKS)
        self.assertEqual(200, response.status_code)
        self.site.delete()
        response = self.client.get(ALL_LINKS)
        self.assertEqual(404, response.status_code)

class DeleteLinkTest(ViewBaseTest):
    def test_delete_link_returns_405_on_get(self):
        link = given_a_link(self.site)
        response = self.client.get('/l/delete/%s' %  link.pk)
        self.assertEqual(405, response.status_code)

    def test_returns_404_if_called_with_invalid_link_id(self):
        response = self.client.post('/l/delete/%s' % 0)
        self.assertEqual(404, response.status_code)

    def test_deletes_link_when_called_with_post(self):
        link = given_a_link(self.site)
        response = self.client.post('/l/delete/%s' %  link.pk)
        self.assertEqual(0, Link.objects.filter(short_url=link.short_url).count())
