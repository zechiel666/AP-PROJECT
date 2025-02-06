from django.shortcuts import render , redirect, get_object_or_404
from django.views.generic import ListView, FormView, UpdateView, CreateView
from django.contrib import messages
from courses.models import Course
from user.models import User, SelectedCourse
from .forms import CourseForm, UserEditForm, UserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
 
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


class UserListView(LoginRequiredMixin, ListView):
    """List all students and teachers with search functionality"""
    model = User
    template_name = "user_management.html"
    context_object_name = "users"
    login_url = "/login/"

    def get_queryset(self):
        """Search users by student number"""
        query = self.request.GET.get("q", "")
        users = User.objects.exclude(is_superuser=True)  # Exclude admins
        if query:
            users = users.filter(student_number__icontains=query)
        return users

class UserCreateView(LoginRequiredMixin, CreateView):
    """Add a new user with all necessary fields"""
    model = User
    form_class = UserCreateForm
    template_name = "add_user.html"
    success_url = reverse_lazy("user_list")
    login_url = "/login/"

    def form_valid(self, form):
        """Handle password hashing and save the user"""
        user = form.save(commit=False)
        if form.cleaned_data["password"]:
            user.set_password(form.cleaned_data["password"])  # Hash password
        user.save()
        messages.success(self.request, "User added successfully!")
        return super().form_valid(form)

class UserEditView(LoginRequiredMixin, UpdateView):
    """Edit user details, including password"""
    model = User
    form_class = UserEditForm
    template_name = "edit_user.html"
    success_url = reverse_lazy("user_list")
    login_url = "/login/"

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data["password"]:
            user.set_password(form.cleaned_data["password"])  # Update password if provided
        user.save()
        messages.success(self.request, "User updated successfully!")
        return super().form_valid(form)

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Delete related SelectedCourse entries first
    SelectedCourse.objects.filter(user=user).delete()
    
    # Now delete the user
    user.delete()

    messages.success(request, "User deleted successfully!")
    return redirect("user_list")