from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from courses.models import Course
from django.conf import settings 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_LEVEL_CHOICES = (
        ("admin", "Admin"),
        ("student", "Student"),
    )

    username = None  # Remove username field
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10, unique=True)
    student_number = models.CharField(max_length=15, blank=True, null=True, unique=True)  # Allow NULL values
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    user_level = models.CharField(max_length=10, choices=USER_LEVEL_CHOICES)
    password = models.CharField(max_length=100)
    unit = models.IntegerField(default=20)
    selected_unit = models.IntegerField(default=0)
    passed_courses = models.JSONField(default=list, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "national_id", "phone_number", "user_level"]

    def __str__(self):
        return f"{self.name} - {self.user_level}"

    def has_passed(self, code):
        return code in self.passed_courses

class selectedcourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_for')
    course = models.ForeignKey(Course ,on_delete=models.CASCADE , related_name='student_select')

    class Meta:
        unique_together = ('user' , 'course')
    
    def __str__(self):
        return f'{self.user.student_number} - {self.course.code}' 
