from django.contrib.sites.models import Site
from django.db import models

# Create your models here.

class Link(models.Model):
    destination_url = models.URLField("Destination", max_length=255, blank=False, verify_exists=False)
    short_url = models.TextField("Short URL", max_length=64, blank=False)
    site = models.ForeignKey(Site)

    class Meta:
        unique_together = ["short_url", "site"]

    @property
    def url(self):
        return "http://%s/%s" % (self.site.domain, self.short_url)

    def save(self, *args, **kw):
        self.full_clean()
        super(Link, self).save(*args, **kw)

