from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class UserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, label='نام و نام خانوادگی')
    national_id = forms.CharField(max_length=10, label='کدملی')
    student_number = forms.CharField(max_length=15, label='شماره دانشجویی') 
    email = forms.EmailField(label='ایمیل')
    phone_number = forms.CharField(max_length=15, label='شماره تلفن')
    user_level = forms.ChoiceField(choices=User.USER_LEVEL_CHOICES, label='سطح کاربری')
    

    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(),
        help_text="رمز عبور باید حداقل ۸ کاراکتر داشته باشد و شامل اطلاعات شخصی نباشد.",
        error_messages={
            "required": "لطفاً رمز عبور خود را وارد کنید.",
            "password_too_short": "رمز عبور باید حداقل ۸ کاراکتر داشته باشد.",
            "password_too_common": "رمز عبور نمی‌تواند یک رمز عبور رایج باشد.",
            "password_entirely_numeric": "رمز عبور نمی‌تواند فقط عدد باشد.",
        }
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(),
        help_text="رمز عبور را دوباره وارد کنید.",
        error_messages={
            "required": "لطفاً تکرار رمز عبور خود را وارد کنید.",
        }
    )
    class Meta:
        model = User
        fields = ['name', 'national_id', 'student_number', 'email', 'phone_number', 'user_level', 'password1', 'password2']
        widgets = {
            'password': forms.PasswordInput(),  # Render password field as a password input
        }

    def clean(self):
        cleaned_data = super().clean()
        user_level = cleaned_data.get("user_level")
        student_number = cleaned_data.get("student_number")
        
        if user_level == 'student' and not student_number:
            self.add_error('student_number', "Student number is required for students.")
        
        if user_level == 'admin' and not student_number:
            self.add_error('student_number', "Code is required for admins.")

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password1', 'passwords must be same')

        if len(cleaned_data.get('national_id')) != 10:
            self.add_error('national_id', "national_id's length must be 10")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.user_level == 'admin':
            user.is_staff = True  # Make admins staff
        if commit:
            user.save()
        return user


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(label="Student Number")  # Rename to reflect student_number

class PasswordResetForm(forms.Form):
    student_number = forms.CharField(max_length=15, label="شماره دانشجویی", required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="رمز جدید")
    password2 = forms.CharField(widget=forms.PasswordInput, label="تکرار رمز جدید")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        student_number = cleaned_data.get("student_number")

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمزهای عبور مطابقت ندارند.")

        # Ensure student number exists
        if not User.objects.filter(student_number=student_number).exists():
            raise forms.ValidationError("شماره دانشجویی یافت نشد.")

        return cleaned_data
