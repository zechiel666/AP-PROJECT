from django.shortcuts import render , redirect
from django.views.generic import ListView, View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import selectedcourse
from django.contrib import messages
import logging
from datetime import datetime , time


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'
    login_url = '/login/'  # Redirect to login page if not authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()  # Send department list
        context['user'] = self.request.user  # Pass logged-in user's name
        context['selected_course'] = selectedcourse.objects.filter(user = self.request.user).values_list('course__code', flat=True)
        return context
    
    def post(self, request,*args, **kwargs):
        course_code_name = request.POST.get('course__code')
        course = Course.objects.get(code=course_code_name)
        user = request.user

        if selectedcourse.objects.filter(user=user, course=course).exists():
            messages.error(request, 'این درس انتخاب شده است')
            return redirect('course_list')
        
        if course.pishniaz:
          pishniaz_code = course.pishniaz
          if not user.has_passed(pishniaz_code):
            messages.error(request,'پیشنیازی رعایت نشده')
            return redirect('course_list')
        
        #if course.hamniaz:
          #  if not selectedcourse.objects.filter(student=student, course__id=course.hamniaz).exists() and not student.hass_passed(course.hamniaz):
           #     messages.error(request, "هم‌نیاز این درس را انتخاب نکرده‌اید یا نگذرانده‌اید.")
           #     return redirect('course_list')
        
        if course.remainingCapacity <=0:
            messages.error(request, 'ظرفیت پر شده است')
            return redirect('course_list')
        
        if  user.selected_unit + course.credits > user.unit :
            messages.error(request,'واحد انتخاب شده بیش از حداکثر مجاز است')
            return redirect('course_list')
        
        selected_course = selectedcourse.objects.filter(user = user)
        for sc in selected_course:
            if sc.course.examDate == course.examDate and sc.course.examTime == course.examTime:
                messages.error(request, 'زمان امتحان تداخل دارد')
                return redirect('course_list')
            
        selected_courses = selectedcourse.objects.filter(user=user)
        for sc in selected_courses:
            days_overlap = set(sc.course.classDays.split('/')) & set(course.classDays.split('/'))
            if days_overlap and (sc.course.startTime < course.endTime and sc.course.endTime > course.startTime):
                messages.error(request, 'زمان کلاس‌ها تداخل دارد')
                return redirect('course_list')


            
        selectedcourse.objects.create(user=user, course = course)
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
            selected_course = selectedcourse.objects.get(user=user, course__code=course_code)
        except selectedcourse.DoesNotExist:
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
    


def weekly_table(request):
    selected_courses = selectedcourse.objects.filter(user=request.user)
    courses = []
    
    for course in selected_courses:
        start_time = course.course.startTime
        end_time = course.course.endTime  

        # تبدیل زمان‌ها به فرمت HH:MM
        start_time_str = start_time.strftime('%H:%M') if isinstance(start_time, time) else ''
        end_time_str = end_time.strftime('%H:%M') if isinstance(end_time, time) else ''

        courses.append({
            'name': course.course.name,
            'class_days': course.course.classDays.split(','),
            'start_time': start_time_str,
            'end_time': end_time_str,
        })
        
    days_of_week = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه"]
    time_slots = ["08:00 - 10:00", "10:00 - 12:00", "12:00 - 14:00", "14:00 - 16:00", "16:00 - 18:00"]

    # تبدیل زمان‌ها به شیء datetime
    time_slot_objects = []
    for slot in time_slots:
        start_str, end_str = slot.split(' - ')  # جدا کردن زمان شروع و پایان
        start_time_obj = datetime.strptime(start_str, "%H:%M")
        end_time_obj = datetime.strptime(end_str, "%H:%M")
        time_slot_objects.append((start_time_obj, end_time_obj))

    # ترکیب time_slots و time_slot_objects
    time_slots_with_objects = zip(time_slots, time_slot_objects)

    return render(request, 'weekly_table.html', {
        'courses': courses, 
        'days_of_week': days_of_week, 
        'time_slots_with_objects': time_slots_with_objects  # ارسال ترکیب‌شده
    })