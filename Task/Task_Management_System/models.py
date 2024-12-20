from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from model_utils.models import TimeStampedModel

from .managers import UserManager


class User(AbstractUser, TimeStampedModel):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, default="", blank=True)
    last_name = models.CharField(max_length=100, null=True, default="")

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_set", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name


class Task(TimeStampedModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    PRIORITY_CHOICES = [
        (1, "High"),
        (2, "Medium"),
        (3, "Low"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_receiver"
    )
    assigned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_creater"
    )
    start_date = models.DateField()
    end_date = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    comment = models.CharField(max_length=400)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.first_name} on {self.task.title}"
