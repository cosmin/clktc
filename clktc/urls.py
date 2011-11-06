from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^a/admin/', include(admin.site.urls)),
    url(r'^a/login/', 'django.contrib.auth.views.login', name="login"),
    url(r'^a/logout/', 'django.contrib.auth.views.logout', {'next_page':"/"}, name="logout"),
    url(r'', include('clktc.links.urls')),
)
