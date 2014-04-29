from django.conf.urls import patterns, include, url
from rest_framework import routers

from tasks.views import TaskViewSet, LabelViewSet, AssigneeViewSet

api_router = routers.DefaultRouter()
api_router.register(r'tasks', TaskViewSet)
api_router.register(r'labels', LabelViewSet)
api_router.register(r'assignees', AssigneeViewSet)
