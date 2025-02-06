from django.urls import path
from .views import TeacherLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path ('login/', TeacherLoginView.as_view(), name = 'teacher_login'),
    path('logout/', LogoutView.as_view(next_page = 'teacher_login'),name = 'teacher_logout')
]