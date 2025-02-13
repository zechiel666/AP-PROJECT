from django.shortcuts import render , redirect
from django.views.generic import ListView, View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from user.models import SelectedCourse
from django.contrib import messages
import logging
from datetime import time, timedelta, datetime

class CourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    login_url = '/login/'  # Redirect to login page if not authenticated
 
    def test_func(self):
        # Ensure only students can access
        return self.request.user.is_authenticated and self.request.user.user_level == "student" and not self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect to a forbidden page if the user is not authorized
        return redirect("forbidden")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()  # Send department list
        context['user'] = self.request.user  # Pass logged-in user's name
        context['selected_course'] = SelectedCourse.objects.filter(user = self.request.user).values_list('course__code', flat=True)
        return context
    
    def post(self, request,*args, **kwargs):
        course_code_name = request.POST.get('course__code')
        course = Course.objects.get(code=course_code_name)
        user = request.user
        #if both admins and students were logged in
        if user.is_superuser:
            messages.error(request, 'Admins cannot select courses.')
            return redirect('course_list')

        if SelectedCourse.objects.filter(user=user, course=course).exists():
            messages.error(request, 'این درس انتخاب شده است')
            return redirect('course_list')
        
        if course.pishniaz:
            pishniaz_code = course.pishniaz
            if not user.has_passed(pishniaz_code):
                messages.error(request,'پیشنیازی رعایت نشده')
                return redirect('course_list')
        
        if course.hamniaz:
            hamniaz_code = course.ha
            if not user.has_passed(hamniaz_code):
                messages.error(request,'همنیازی رعایت نشده')
                return redirect('course_list')
        
        if course.remainingCapacity <=0:
            messages.error(request, 'ظرفیت پر شده است')
            return redirect('course_list')
        
        if  user.selected_unit + course.credits > user.unit :
            messages.error(request,'واحد انتخاب شده بیش از حداکثر مجاز است')
            return redirect('course_list')
        
        selected_course = SelectedCourse.objects.filter(user = user)
        for sc in selected_course:
            if sc.course.examDate == course.examDate and sc.course.examTime == course.examTime:
                messages.error(request, 'زمان امتحان تداخل دارد')
                return redirect('course_list')
            
        selected_courses = SelectedCourse.objects.filter(user=user)
        for sc in selected_courses:
            days_overlap = set(sc.course.classDays.split('/')) & set(course.classDays.split('/'))
            if days_overlap and (sc.course.startTime < course.endTime and sc.course.endTime > course.startTime):
                messages.error(request, 'زمان کلاس‌ها تداخل دارد')
                return redirect('course_list')


            
        SelectedCourse.objects.create(user=user, course = course)
        course.remainingCapacity -= 1
        user.selected_unit += course.credits
        course.save()
        user.save()

        messages.success (request,f'اخذ شد{course.name} درس ')
        return redirect('course_list')

logger = logging.getLogger(__name__)

class Removeselectedcourse (View):
    def post(self, request, *args, **kwargs):
        course_code = request.POST.get('course__code')
        user = request.user
        try:
            selected_course = SelectedCourse.objects.get(user=user, course__code=course_code)
        except SelectedCourse.DoesNotExist:
            messages.error (request, 'درس در لیست اخذ شده شما قرار ندارد')
            return redirect('course_list')
        
        course = selected_course.course

        course.remainingCapacity += 1
        course.save()

        user.selected_unit -= course.credits
        user.save()

        selected_course.delete()

        messages.success(request, f' حذف شد {course.name} درس ')
        return redirect('course_list')
    

def generate_time_slots(start, end, interval_minutes=30):
    """Generate time slots in HH:MM:SS format with a given interval."""
    slots = []
    current_time = start
    while current_time < end:
        slots.append(current_time.strftime("%H:%M:%S"))
        current_time += timedelta(minutes=interval_minutes)
    return slots

def weekly_table(request):
    selected_courses = SelectedCourse.objects.filter(user=request.user)
    courses = []

    for course in selected_courses:
        courses.append({
            'name': course.course.name,
            'class_days': course.course.classDays,  
            'start_time': str(course.course.startTime),
            'end_time': str(course.course.endTime), 
        })

    days_of_week = ["شنبه/دوشنبه", "یکشنبه/سشنبه"] 
    time_slots = ["08:00:00", "10:00:00", "13:00:00", "15:00:00"]
    time_sheets = {"08:00:00":'08:00-10:00', "10:00:00":'10:00-12:00', "13:00:00":'13:00-15:00', "15:00:00":'15:00-17:00'}
    return render(request, 'weekly_table.html', {
        'courses': courses, 
        'days_of_week': days_of_week, 
        'time_slots': time_slots,
        'time_sheets' : time_sheets,
    })
