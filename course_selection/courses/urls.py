from django.urls import path
from .views import *

urlpatterns=[
    path('courses/', CourseListView.as_view(), name='course_list')
    path('remove-course/', Removeselectedcourse.as_view(), name='remove_selected_course')
]