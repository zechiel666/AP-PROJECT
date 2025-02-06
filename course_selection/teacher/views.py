from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render , redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from courses.models import Course, Department
from .forms import CourseForm

class TeacherDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_teacher:  
            return redirect('/select-courses/')  

        return render(request, 'teacher_dashboard.html')
    

def course_management(request):
    query = request.GET.get("q", "")
    courses = Course.objects.all()
    
    if query:
        courses = courses.filter(
            code__icontains=query
        ) | courses.filter(
            name__icontains=query
        ) | courses.filter(
            department__name__icontains=query
        )
    
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect("course_management")
    else:
        form = CourseForm()
    
    return render(request, "course_management.html", {"courses": courses, "form": form, "query": query})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect("course_management")
