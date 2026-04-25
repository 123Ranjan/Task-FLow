from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('ADMIN', 'Admin'),
    ('MANAGER', 'Manager'),
    ('TL', 'Team Lead'),
    ('DEV', 'Developer'),
    ('TESTER', 'Tester'),
    ('DESIGNER', 'Designer'),
]

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='DEV')
    bio = models.TextField(blank=True, null=True)  # ✅ ADD THIS

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email