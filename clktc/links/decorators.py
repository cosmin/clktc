from functools import update_wrapper
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404

def require_valid_site(fn):
    def wrapper(request, *args, **kw):
        host = request.get_host()
        site = get_object_or_404(Site, domain=host)
        request.site = site
        return fn(request, *args, **kw)
    return update_wrapper(wrapper, fn)
