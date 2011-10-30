from django.conf.urls.defaults import patterns, include, url
from clktc.links import views

urlpatterns = patterns('',
    url(r'^l/links/', views.get_all_links),
    url(r'^l/add/', views.add_link),
    url(r'^l/edit/(?P<link_id>[0-9]+)', views.edit_link),
)
