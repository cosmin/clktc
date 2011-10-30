from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^a/admin/', include(admin.site.urls)),
    url(r'', include('clktc.links.urls')),
)
