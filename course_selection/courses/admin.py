from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter  # Correct import
from django_jalali.admin.widgets import AdminjDateWidget, AdminTimeWidget
from django import forms
from persiantools.jdatetime import JalaliDateTime # Import JalaliDateTime for conversion
from .models import *

class CourseAdminForm(forms.ModelForm):
    """ Custom form to use Jalali Date Picker & Time Picker in Django Admin """
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'examDate': AdminjDateWidget(),  # Jalali Date Picker
            'examTime': AdminTimeWidget(),  # Time Picker
        }

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ('name', 'examDate_persian', 'examTime')  # Show Date & Time
    list_filter = (('examDate', JDateFieldListFilter),)

    def examDate_persian(self, obj):
        """ Convert examDate from Gregorian to Solar Hijri in admin panel """
        if obj.examDate:
            jalali_date = JalaliDateTime(obj.examDate.year, obj.examDate.month, obj.examDate.day)
            return jalali_date.strftime("%Y-%m-%d")  # Show Jalali date (YYYY-MM-DD)
        return "No Date"

    examDate_persian.short_description = "Exam Date (Solar Hijri)"

admin.site.register(Course, CourseAdmin)

admin.site.register(Instructor) 
admin.site.register(Department)