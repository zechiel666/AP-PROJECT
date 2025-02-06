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
    """Form for adding a new user with all required fields"""
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = [
            "name", "email", "phone_number", "national_id", "student_number",
            "user_level", "password", "confirm_password"
        ]

    def clean(self):
        """Validate password confirmation"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        
        return cleaned_data

class UserEditForm(forms.ModelForm):
    """Form for editing a user, including password update"""
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep the same password.")

    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "student_number", "user_level", "password"]
