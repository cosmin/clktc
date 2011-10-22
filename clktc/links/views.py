# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from clktc.links.models import Link

def get_all_links(request):
    return render_to_response("links/all.html", RequestContext(request, dict(
        links = Link.objects.all(),
    )))
