from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    def __str__(self):
        return self.email

# Task Model
class Task(models.Model):
    TASK_TYPES = (
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('improvement', 'Improvement'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    completed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ManyToManyField(CustomUser, related_name='tasks', blank=True)

    def __str__(self):
        return self.name
