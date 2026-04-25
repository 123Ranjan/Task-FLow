from django.db import models
from boards.models import Board


class Sprint(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    goal = models.TextField(blank=True, null=True)

    # Relationship with Board
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sprints'
    )

    # Statistics (can be calculated or stored)
    issue_count = models.IntegerField(default=0)
    completed_issues = models.IntegerField(default=0)
    completed_points = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name