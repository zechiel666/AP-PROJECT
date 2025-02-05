from django.urls import path
from .views import *

urlpatterns=[
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'),
    path("password-reset/", password_reset, name="password_reset"),
] 