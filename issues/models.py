from django.db import models


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('REVIEW', 'Review'),
        ('DONE', 'Done'),
    ]

    TYPE_CHOICES = [
        ('TASK', 'Task'),
        ('BUG', 'Bug'),
        ('STORY', 'Story'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    issue_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='TASK')

    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.IntegerField(null=True, blank=True)
    actual_hours = models.IntegerField(null=True, blank=True)

    assigned_email = models.EmailField()
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE, null=True, blank=True)
    sprint = models.ForeignKey('sprints.Sprint', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    user_email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.issue.title} by {self.user_email}"