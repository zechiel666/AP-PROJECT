from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_LEVEL_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10, unique=True)
    student_number = models.CharField(max_length=15, blank=True, null=True)  # Optional for admins
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    user_level = models.CharField(max_length=10, choices=USER_LEVEL_CHOICES)
    password = models.CharField(max_length=100)
    unit = models.IntegerField(default=20)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Fix conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Fix conflict
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.user_level})"
