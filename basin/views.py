from django.shortcuts import render
from rest_framework import viewsets

from basin.models import Task, Label, Assignee
from basin.serializers import TaskSerializer, LabelSerializer, AssigneeSerializer

def index(request):
    context = {}
    return render(request, 'index.html', context)

def display(request):
    context = {
        'active': Task.objects.active().order_by_due()
    }
    return render(request, 'display.html', context)

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
    model = Task
    serializer_class = TaskSerializer

    def get_queryset(self):
        if 'state' in self.request.QUERY_PARAMS:
            state = self.request.QUERY_PARAMS['state']
            if state == 'active':
                return Task.objects.active()
            if state == 'sleeping':
                return Task.objects.sleeping()
            if state == 'blocked':
                return Task.objects.blocked()
            if state == 'delegated':
                return Task.objects.delegated()
            if state == 'completed':
                return Task.objects.completed()
            if state == 'trashed':
                return Task.objects.trashed()
        return Task.objects.all()

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

class AssigneeViewSet(viewsets.ModelViewSet):
    queryset = Assignee.objects.all()
    serializer_class = AssigneeSerializer
