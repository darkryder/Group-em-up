from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from server import urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'groupieserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^really/admin/urlisthis/', include(admin.site.urls)),
    url(r'^stuff/', include(urls)),
)
