from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('ISSUE', 'Issue'),
        ('COMMENT', 'Comment'),
        ('MENTION', 'Mention'),
        ('ASSIGNMENT', 'Assignment'),
        ('SPRINT', 'Sprint'),
        ('BOARD', 'Board'),
        ('WARNING', 'Warning'),
        ('SUCCESS', 'Success'),
        ('DEFAULT', 'Default'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='DEFAULT')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message