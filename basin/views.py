from django.shortcuts import render
from rest_framework import viewsets

from basin.models import Task
from basin.serializers import TaskSerializer

def index(request):
    context = {}
    return render(request, 'index.html', context)

def display(request):
    state = 'active'
    if request.method == 'POST':
        state = request.POST['state']
        submit = request.POST['submit']
        tid = request.POST['id']
        if submit == 'check':
            task = Task.objects.get(id=tid)
            task.completed = not task.completed
            task.save()
    elif request.method == 'GET':
        if 'state' in request.GET:
            state = request.GET['state']
    context = {
        'task_list': Task.objects.state(state),
        'state': state,
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
            return Task.objects.state(state)
        return Task.objects.all()
