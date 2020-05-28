from rest_framework import serializers

from tasks.models import Label, Task, SubTask

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('uuid', 'name', 'description', 'created_at')

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('uuid', 'name', 'task', 'status')


class TaskSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)
    subtasks = SubTaskSerializer(many=True)
    class Meta:
        model = Task
        fields = "__all__"