from django.urls import path
from .views import *

urlpatterns = [
    path("manage/", CourseManagementView.as_view(), name="course_management"),
    path('delete/<int:course_id>/', delete_course, name='delete_course'),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/add/", UserCreateView.as_view(), name="add_user"),
    path("users/edit/<int:pk>/", UserEditView.as_view(), name="edit_user"),
    path("users/delete/<int:user_id>/", delete_user, name="delete_user"),
]
 