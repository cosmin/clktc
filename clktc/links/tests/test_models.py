from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db.models.base import Model
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

    @raises_regexp(ValidationError, "destination_url.*This field cannot be null")
    def test_destination_url_cannot_be_null(self):
        link = Link(destination_url = None, short_url="foobarbaz", site=self.site)
        link.save()

    @raises_regexp(ValidationError, "destination_url.*This field cannot be blank")
    def test_destination_url_cannot_be_blank(self):
        link = Link(destination_url = "", short_url="foobarbaz", site=self.site)
        link.save()

    @raises_regexp(ValidationError, "short_url.*This field cannot be null")
    def test_short_url_cannot_be_null(self):
        link = Link(destination_url="http://example.com", short_url=None)
        link.save()

    @raises_regexp(ValidationError, "short_url.*This field cannot be blank")
    def test_short_url_cannot_be_blank(self):
        link = Link(destination_url="http://example.com", short_url="", site=self.site)
        link.save()

    @raises_regexp(ValidationError, 'site.*This field cannot be blank')
    def test_site_cannot_be_empty(self):
        link = Link(destination_url = "http://example.com", short_url="foobarbaz", site_id="")
        link.save()

    @raises_regexp(ValidationError, r'columns short_url, site_id are not unique')
    def test_site_and_short_url_are_unique_together(self):
        l1 = Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site)
        l2 = Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site)
        Model.save(l1)
        Model.save(l2)

    @raises_regexp(ValidationError, 'Link with this short URL already exists for this site. Please try another one.')
    def test_site_and_short_url_are_unique_together(self):
        Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site).save()
        Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site).save()

    def test_returns_correct_full_url(self):
        link = Link(destination_url = "http://example.com", short_url = "foobarbaz", site = self.site)
        link.save()
        self.assertEqual(link.url, "http://%s/%s" % (self.site.domain, link.short_url))
