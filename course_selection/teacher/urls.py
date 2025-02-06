from django.urls import path
from .views import course_management, delete_course

urlpatterns = [
    path('manage/', course_management, name='course_management'),
    path('delete/<int:course_id>/', delete_course, name='delete_course'),
]
