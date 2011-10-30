from django.contrib.sites.models import Site
from django.db import models

# Create your models here.

class Link(models.Model):
    destination_url = models.URLField("Destination", blank=False)
    short_url = models.TextField("Short URL", max_length=64, blank=False)
    site = models.ForeignKey(Site)

    class Meta:
        unique_together = ["short_url", "site"]

    @property
    def url(self):
        return "http://%s/%s" % (self.site.domain, self.short_url)

    def save(self, *args, **kw):
        assert self.short_url, "Short URL cannot be empty"
        assert self.destination_url, "Destination URL cannot be empty"
        super(Link, self).save(*args, **kw)

