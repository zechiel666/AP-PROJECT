from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render , redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class TeacherDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_teacher:  
            return redirect('/select-courses/')  

        return render(request, 'teacher_dashboard.html')
    
