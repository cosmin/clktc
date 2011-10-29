# Create your views here.
from django.contrib.sites.models import get_current_site
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from clktc.links.models import Link

def get_all_links(request):
    return render_to_response("links/all.html", RequestContext(request, dict(
        links = Link.objects.all(),
    )))


def add_link(request):
    short_url = request.POST['short_url']
    destination_url = request.POST['destination_url']
    link = Link(short_url=short_url, destination_url=destination_url)
    link.site = get_current_site(request)
    link.save()
    return redirect(get_all_links)
