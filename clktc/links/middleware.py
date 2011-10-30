from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404

class RequestSiteMiddleware(object):
    def process_request(self, request):
        host = request.get_host()
        site = get_object_or_404(Site, domain=host)
        request.site = site
