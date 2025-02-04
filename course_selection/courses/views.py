from django.shortcuts import render , redirect
from django.views.generic import ListView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import selectedcourse
from django.contrib import messages

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    login_url = '/login/'  # Redirect to login page if not authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()  # Send department list
        context['user'] = self.request.user  # Pass logged-in user's name
        context['selectedcourse'] = selectedcourse.objects.filter(user = self.request.user)
        return context
    
    def post(self, request,*args, **kwargs):
        course_id = request.post.get('code')
        course = Course.objects.get(code=course_id)
        user = request.user

        if selectedcourse.objects.filter(use=user, course=course).exists():
            messages.erorr(request, 'این درس انتخاب شده است')
            return redirect('course_list')
        
        if course.pishniaz and not user.passed_courses:
            messages.eror(request,'پیشنیازی رعایت نشده')
            return redirect('course_list')
        
