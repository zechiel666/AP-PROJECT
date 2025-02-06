from django.urls import path
from .views import *

urlpatterns = [
    path("manage/", CourseManagementView.as_view(), name="course_management"),
    path('delete/<int:course_id>/', delete_course, name='delete_course'),
]
 