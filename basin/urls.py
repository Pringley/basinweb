from django.conf.urls import patterns, include, url
from django.contrib import admin

from basin.routers import api_router

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'basin.views.index'),
    url(r'^display/$', 'basin.views.display'),
    url(r'^api/', include(api_router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
