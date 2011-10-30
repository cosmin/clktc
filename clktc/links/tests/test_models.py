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

    @raises_regexp(IntegrityError, r'links_link.destination_url may not be NULL')
    def test_destination_url_is_required(self):
        link = Link(destination_url = None)
        link.save()

    @raises_regexp(IntegrityError, r'links_link.short_url may not be NULL')
    def test_short_url_is_required(self):
        link = Link(destination_url="http://example.com", short_url=None)
        link.save()

    @raises_regexp(IntegrityError, r'columns short_url, site_id are not unique')
    def test_site_and_short_url_are_unique_together(self):
        Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site).save()
        Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site).save()

    def test_returns_correct_full_url(self):
        link = Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site)
        link.save()
        self.assertEqual(link.url, "http://%s/%s" % (self.site.domain, link.short_url))
