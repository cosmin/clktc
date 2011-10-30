# Create your views here.
from django.contrib.sites.models import get_current_site
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from clktc.links.forms import AddLinkForm, EditLinkForm
from clktc.links.decorators import require_valid_site
from clktc.links.models import Link

@require_valid_site
def get_all_links(request):
    return render_to_response("links/all.html", RequestContext(request, dict(
        links = Link.objects.all(),
    )))

@require_valid_site
def add_link(request):
    if request.method == "POST":
        form = AddLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.site = request.site
            link.save()
            return redirect(get_all_links)
    else:
        form = AddLinkForm()
    return render_to_response("links/add.html", RequestContext(request, {'form': form}))

@require_valid_site
def edit_link(request, link_id):
    link = get_object_or_404(Link, pk=link_id)
    form_cls = EditLinkForm
    if request.method == "POST":
        form = form_cls(request.POST, instance=link)
        if form.is_valid():
            link = form.save()
            return redirect(get_all_links)
    else:
        form = form_cls(instance=link)
    return render_to_response("links/edit.html", RequestContext(request, dict(link=link, form=form)))

@require_valid_site
def try_short_link(request, short_url):
    link = get_object_or_404(Link, short_url=short_url, site=request.site)
    return redirect(link.destination_url)
