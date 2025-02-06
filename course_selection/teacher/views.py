from django.shortcuts import render , redirect, get_object_or_404
from django.views.generic import ListView, FormView
from django.contrib import messages
from courses.models import Course
from .forms import CourseForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

 
class CourseManagementView(LoginRequiredMixin, UserPassesTestMixin, ListView, FormView):
    model = Course
    template_name = "course_management.html"
    context_object_name = "courses"
    form_class = CourseForm
    login_url = "/login/"  # Redirects unauthorized users to login

    def test_func(self):
        """Ensures that only teachers can access this page"""
        return self.request.user.is_authenticated and self.request.user.user_level == "teacher" and not self.request.user.is_superuser
    
    def handle_no_permission(self):
        # Redirect to a forbidden page if the user is not authorized
        return redirect("forbidden")

    def get_queryset(self):
        """Filters courses based on the search query"""
        query = self.request.GET.get("q", "")
        courses = Course.objects.all()

        if query:
            courses = courses.filter(
                code__icontains=query
            ) | courses.filter(
                name__icontains=query
            ) | courses.filter(
                department__name__icontains=query
            )
        
        return courses

    def form_valid(self, form):
        """Handles course creation when a teacher submits the form"""
        form.save()
        messages.success(self.request, "Course added successfully!")
        return redirect("course_management")

    def get_context_data(self, **kwargs):
        """Adds the form to the context"""
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["query"] = self.request.GET.get("q", "")
        return context


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect("course_management")
