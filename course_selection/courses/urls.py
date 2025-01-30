from django.urls import path
from .views import *

urlpatterns=[
    path('courses/', CourseListView.as_view(), name='course_list')
]