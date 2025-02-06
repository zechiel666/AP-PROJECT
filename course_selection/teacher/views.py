from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class TeacherLoginview(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.is_teacher:
            return '/admin/'
        return super().get_success_url()
    
