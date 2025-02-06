from courses.models import Course
from django import forms

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
