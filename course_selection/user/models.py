from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  BaseUserManager, PermissionsMixin
from courses.models import Course
from django.conf import settings 
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

         # Ensure superusers don't require national_id
        if extra_fields.get('is_superuser', False):
            extra_fields.setdefault('national_id', f'admin-{email}')  # Unique value for superuser
            
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create a Django superuser, not a teacher or student"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure that user_level is **not** required for superusers
        extra_fields.pop('user_level', None)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    STUDENT = 'student'
    TEACHER = 'teacher'
    USER_LEVEL_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]
    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10, unique=True)
    student_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    # Allow user_level to be NULL for superusers
    user_level = models.CharField(
        max_length=10,
        choices=USER_LEVEL_CHOICES,
        blank=True,
        null=True,
        default='student'  # TEMPORARY DEFAULT VALUE
    )

    
    password = models.CharField(max_length=100)
    unit = models.IntegerField(default=20)
    selected_unit = models.IntegerField(default=0)
    passed_courses = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "national_id", "phone_number"]

    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"

    def has_passed(self, code):
        return code in self.passed_courses

    def get_role_display(self):
        if self.is_superuser:
            return "Admin"
        return self.user_level.capitalize() if self.user_level else "Unknown"


class StudentManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_level='student')


class TeacherManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_level='teacher')


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.user_level = 'student'
        super().save(*args, **kwargs)


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.user_level = 'teacher'
        super().save(*args, **kwargs)


class SelectedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.student_number} - {self.course.code}'
