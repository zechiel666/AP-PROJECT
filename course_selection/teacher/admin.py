from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

class Adminsite(admin.AdminSite):
    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_teacher
    

admin_site = Adminsite (name='admin_site')

urlpatterns = [
    path('admin/', admin_site.urls),
]
