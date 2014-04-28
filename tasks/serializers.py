from tasks.models import Task, Assignee, Label
from rest_framework import serializers

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('summary', 'completed', 'due', 'project', 'labels',
                'details', 'sleepuntil', 'sleepforever', 'assignee',
                'blockers', 'trashed', 'created', 'modified')

class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Label
        fields = ('name', 'trashed', 'tasks')

class AssigneeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Assignee
        fields = ('name', 'last_request', 'last_response', 'trashed', 'tasks')
