from django.conf.urls.defaults import patterns, include, url
from clktc.links import views

urlpatterns = patterns('',
    url(r'^l/links/$', views.get_all_links, name="all_links"),
    url(r'^$', views.homepage, name="home"),
    url(r'^l/add/', views.add_link, name="add_link"),
    url(r'^l/edit/(?P<link_id>[0-9]+)', views.edit_link, name="edit_link"),
    url(r'^l/delete/(?P<link_id>[0-9]+)', views.delete_link, name="delete_link"),
    url(r'(?P<short_url>.+)', views.try_short_link, name="short_link")
)
