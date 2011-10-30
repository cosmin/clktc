from django.conf.urls.defaults import patterns, include, url
from clktc.links import views

urlpatterns = patterns('',
    url(r'^links/', views.get_all_links),
    url(r'^add/', views.add_link),
    url(r'^edit/(?P<link_id>[0-9]+)', views.edit_link),
)
