from django.conf.urls.defaults import patterns, include, url
from clktc.links import views

urlpatterns = patterns('',
    url(r'^links/', views.get_all_links),
    url(r'^add/', views.add_link),
)
