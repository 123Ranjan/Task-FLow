from rest_framework import serializers
from .models import Issue

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'priority', 'status',
            'issue_type', 'due_date', 'estimated_hours', 'actual_hours',
            'assigned_email', 'board', 'sprint', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']