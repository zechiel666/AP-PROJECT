from django.shortcuts import render
from django.views.generic import ListView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    login_url = '/login/'  # Redirect to login page if not authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()  # Send department list
        context['user'] = self.request.user  # Pass logged-in user's name
        return context