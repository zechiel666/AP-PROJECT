from django.db import models
from django.contrib.auth.models import AbstractUser
from courses.models import Course
from django.conf import settings 

class User(AbstractUser):
    USER_LEVEL_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    username = None  # Remove username from AbstractUser
    
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10, unique=True)
    student_number = models.CharField(max_length=15, blank=True, null=True)  # Optional for admins
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    user_level = models.CharField(max_length=10, choices=USER_LEVEL_CHOICES)
    password = models.CharField(max_length=100)
    unit = models.IntegerField(default=20)
    selected_unit = models.IntegerField(default=0)
    passed_courses = models.JSONField(default=list , blank=True)

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
    USERNAME_FIELD = "email"  # Use email instead of username
    REQUIRED_FIELDS = ["name", "national_id", 'student_number', "phone_number", "user_level"]

    def __str__(self):
        return f"{self.name} - {self.user_level}"
    
    def has_passed(self , code):
        return code in self.passed_courses

class selectedcourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_for')
    course = models.ForeignKey(Course ,on_delete=models.CASCADE , related_name='student_select')

    class Meta:
        unique_together = ('user' , 'course')
    
    def __str__(self):
        return f'{self.user.student_number} - {self.course.code}' 
