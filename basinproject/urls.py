from django.conf.urls import patterns, include, url
from django.contrib import admin

from basinapp.routers import api_router

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'basinapp.views.index'),
    url(r'^api/', include(api_router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)