from tasks.models import Task, Assignee, Label
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label

class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignee
