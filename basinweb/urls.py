from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from tasks.views import TaskViewSet, LabelViewSet, AssigneeViewSet

admin.autodiscover()

api_router = routers.DefaultRouter()
api_router.register(r'tasks', TaskViewSet)
api_router.register(r'labels', LabelViewSet)
api_router.register(r'assignees', AssigneeViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'basinweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'tasks.views.index'),
    url(r'^api/', include(api_router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
