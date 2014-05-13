from basin.models import Task
from rest_framework import serializers

class LabelField(serializers.WritableField):
    def to_native(self, obj):
        if not obj:
            return []
        items = obj.strip().split(',')
        return [item.strip() for item in items]
    def from_native(self, data):
        return ','.join(data)

class TaskSerializer(serializers.ModelSerializer):
    labels = LabelField(blank=True)
    class Meta:
        model = Task
