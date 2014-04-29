from django.shortcuts import render
from rest_framework import viewsets

from basin.models import Task, Label, Assignee
from basin.serializers import TaskSerializer, LabelSerializer, AssigneeSerializer

def index(request):
    context = {}
    return render(request, 'index.html', context)

class ActiveViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.active()
    serializer_class = TaskSerializer

class SleepingViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.sleeping()
    serializer_class = TaskSerializer

class BlockedViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.blocked()
    serializer_class = TaskSerializer

class DelegatedViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.delegated()
    serializer_class = TaskSerializer

class CompletedViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(completed=True, trashed=False)
    serializer_class = TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

class AssigneeViewSet(viewsets.ModelViewSet):
    queryset = Assignee.objects.all()
    serializer_class = AssigneeSerializer
