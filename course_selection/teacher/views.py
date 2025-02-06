from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib import messages
from courses.models import Course
from .forms import CourseForm

def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'is_teacher') and user.is_teacher
    
@login_required(login_url='/login/')  # Redirects to the correct login page
@user_passes_test(is_teacher, login_url='/login/')
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
