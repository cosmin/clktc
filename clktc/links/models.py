from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models


class LinkWithShortUrlAlreadyExistsForSite(ValidationError):
    def __init__(self):
        super(LinkWithShortUrlAlreadyExistsForSite, self).__init__({
            'short_url': ["Link with this short URL already exists for this site. Please try another one."]
        })

class Link(models.Model):
    destination_url = models.URLField("Destination", max_length=255, blank=False, verify_exists=False)
    short_url = models.TextField("Short URL", max_length=64, blank=False)
    site = models.ForeignKey(Site)
    user = models.ForeignKey(User, related_name="links", default=1)

    class Meta:
        unique_together = ["short_url", "site"]

    @property
    def url(self):
        return "http://%s/%s" % (self.site.domain, self.short_url)

    def is_unique(self, matching):
        if not len(matching):
            return True
        elif self.pk:
            if len(matching) == 1:
                other = matching.get()
                return other.pk == self.pk

    def save(self, *args, **kw):
        if self.short_url and self.site_id:
            matching = Link.objects.filter(short_url=self.short_url, site=self.site)
            if not self.is_unique(matching):
                raise LinkWithShortUrlAlreadyExistsForSite()
        self.full_clean()
        super(Link, self).save(*args, **kw)

