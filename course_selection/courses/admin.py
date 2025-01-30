from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter  # Correct import
from django_jalali.admin.widgets import AdminjDateWidget
from django import forms
from persiantools.jdatetime import JalaliDateTime # Import JalaliDateTime for conversion
from .models import *
import jdatetime
class CourseAdminForm(forms.ModelForm):
    """ Custom form to use Jalali DateTime Picker in Django Admin """
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'examDate': AdminjDateWidget(),  # Jalali DateTime Picker
        }


class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ('name', 'examDate_persian')
    list_filter = (('examDate', JDateFieldListFilter),)

    def examDate_persian(self, obj):
        """ Convert examDate from Gregorian to Solar Hijri with Time in admin panel """
        if obj.examDate:
            jalali_datetime = JalaliDateTime(
                obj.examDate.year, obj.examDate.month, obj.examDate.day,
                obj.examDate.hour, obj.examDate.minute
            )
            return jalali_datetime.strftime("%Y-%m-%d %H:%M")  # Show Jalali date & time
        return "No Date"

    examDate_persian.short_description = "Exam Date (Solar Hijri + Time)"


admin.site.register(Course, CourseAdmin)


admin.site.register(Instructor)
admin.site.register(Department)