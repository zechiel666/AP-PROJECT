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
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_level', 'admin')  # تعیین سطح کاربر به صورت پیش‌فرض برای ادمین

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_LEVEL_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    #username = None  # Remove username from AbstractUser
    
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)      
    is_superuser = models.BooleanField(default=False)  
    
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "national_id", "phone_number"]

    def __str__(self):
        return f"{self.email} - {self.user_level}"

    def has_passed(self , code):
        return code in self.passed_courses

class selectedcourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)


    class Meta:
        unique_together = ('user' , 'course')
    
    def __str__(self):
        return f'{self.user.student_number} - {self.course.code}' 
