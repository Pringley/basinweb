from django.shortcuts import render
from rest_framework import viewsets

from tasks.models import Task, Label, Assignee
from tasks.serializers import TaskSerializer, LabelSerializer, AssigneeSerializer

def index(request):
    context = {}
    return render(request, 'index.html', context)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

class AssigneeViewSet(viewsets.ModelViewSet):
    queryset = Assignee.objects.all()
    serializer_class = AssigneeSerializer
