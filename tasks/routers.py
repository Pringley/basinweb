from django.conf.urls import patterns, include, url
from rest_framework import routers

from tasks import views

api_router = routers.DefaultRouter()
api_router.register(r'active', views.ActiveViewSet)
api_router.register(r'sleeping', views.SleepingViewSet)
api_router.register(r'blocked', views.BlockedViewSet)
api_router.register(r'delegated', views.DelegatedViewSet)
api_router.register(r'completed', views.CompletedViewSet)
api_router.register(r'tasks', views.TaskViewSet)
api_router.register(r'labels', views.LabelViewSet)
api_router.register(r'assignees', views.AssigneeViewSet)
