from django.db import models

BOARD_TYPE_CHOICES = [
    ('SCRUM', 'Scrum'),
    ('KANBAN', 'Kanban'),
]

class Board(models.Model):
    name = models.CharField(max_length=255)
    board_type = models.CharField(max_length=20, choices=BOARD_TYPE_CHOICES)
    project_key = models.CharField(max_length=10, unique=True, blank=True, null=True)
    created_by = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name