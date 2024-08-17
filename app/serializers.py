from rest_framework import serializers
from .models import Task, Label, LabelTask

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'description']

class TaskSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'current_state', 'due_date', 'is_archived', 'labels']

    def get_labels(self, obj):
        labels = obj.labeltask_set.all().select_related('label')
        return LabelSerializer([lt.label for lt in labels], many=True).data
    
class LabelTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelTask
        fields = ['id', 'label', 'task']