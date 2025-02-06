from courses.models import Course
from django import forms
from user.models import User
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "code", "name", "credits", "classDays", "startTime", "endTime",
            "pishniaz", "hamniaz", "examDate", "examTime", "capacity", "remainingCapacity",
            "department", "instructor"
        ]
        widgets = {
            "examDate": forms.DateInput(attrs={"type": "date"}),
            "examTime": forms.TimeInput(attrs={"type": "time"}),
            "startTime": forms.TimeInput(attrs={"type": "time"}),
            "endTime": forms.TimeInput(attrs={"type": "time"}),
        }

class UserCreateForm(forms.ModelForm):
    """Form for adding a new user, including password"""
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "student_number", "user_level", "password"]

class UserEditForm(forms.ModelForm):
    """Form for editing a user, including password update"""
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the same password.")

    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "student_number", "user_level", "password"]
