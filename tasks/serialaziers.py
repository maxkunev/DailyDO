from rest_framework import serializers
from tasks.models import Task

class TaskSerialazier(serializers.ModelSerializer):
    text = serializers.CharField(max_length=300)
    class Meta:
        model = Task
        fields = ['id', 'text', 'date', 'is_done', 'created_at']
        read_only_fields = ['id', 'created_at']