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
        
        current_units = sum([sc.course.credit for sc in selectedcourse.objects.filter(user = user)])
        if current_units + course.credits > user.unit :
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