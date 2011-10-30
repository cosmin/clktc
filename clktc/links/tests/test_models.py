from django.contrib.sites.models import Site
from django.db.utils import IntegrityError
from django.test import TestCase
from clktc.links.models import Link
from clktc.test_utils import raises_regexp

class LinkTests(TestCase):
    def setUp(self):
        site = Site(domain="clk.tc", name="clktc")
        site.save()
        self.site = site

    def tearDown(self):
        self.site.delete()

    @raises_regexp(AssertionError, 'Destination URL cannot be empty')
    def test_destination_url_cannot_be_null(self):
        link = Link(destination_url = None, short_url="foobarbaz", site=self.site)
        link.save()

    @raises_regexp(AssertionError, 'Destination URL cannot be empty')
    def test_destination_url_cannot_be_blank(self):
        link = Link(destination_url = "", short_url="foobarbaz", site=self.site)
        link.save()

    @raises_regexp(AssertionError, 'Short URL cannot be empty')
    def test_short_url_cannot_be_null(self):
        link = Link(destination_url="http://example.com", short_url=None)
        link.save()

    @raises_regexp(AssertionError, 'Short URL cannot be empty')
    def test_short_url_cannot_be_blank(self):
        link = Link(destination_url="http://example.com", short_url="", site=self.site)
        link.save()

    @raises_regexp(IntegrityError, 'links_link.site_id may not be NULL')
    def test_site_cannot_be_empty(self):
        link = Link(destination_url = "foo", short_url="foobarbaz", site_id="")
        link.save()

    @raises_regexp(IntegrityError, r'columns short_url, site_id are not unique')
    def test_site_and_short_url_are_unique_together(self):
        Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site).save()
        Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site).save()

    def test_returns_correct_full_url(self):
        link = Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site)
        link.save()
        self.assertEqual(link.url, "http://%s/%s" % (self.site.domain, link.short_url))
