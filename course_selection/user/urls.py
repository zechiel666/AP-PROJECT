from django.urls import path
from .views import *

urlpatterns=[
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("password-reset/", password_reset, name="password_reset"),
    path('', CustomLoginView.as_view(), name = 'home' )
]