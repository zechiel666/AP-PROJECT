from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import StudentLoginForm
from django.contrib import messages
from .models import User

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            if user.user_level == 'admin':
                user.is_staff = True  # Mark admin users
            user.save()  # Now save in DB
            login(request, user)
            return redirect('/login')
    else:
        form = UserCreationForm()

    return render(request, 'user/register.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = StudentLoginForm
    template_name = 'user/registration/login.html'  # Set full path to template

    def get_success_url(self):
        return reverse_lazy('course_list')  # Redirect after login 
    
    
def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            student_number = form.cleaned_data.get("student_number")
            password1 = form.cleaned_data.get("password1")

            try:
                user = User.objects.get(student_number=student_number)
                user.set_password(password1)  # Securely update the password
                user.save()
                messages.success(request, "رمز عبور شما تغییر کرد. لطفاً وارد شوید.")
                return redirect("login")  # Redirect to login page
            except User.DoesNotExist:
                messages.error(request, "شماره دانشجویی یافت نشد. لطفاً دوباره تلاش کنید.")

    else:
        form = PasswordResetForm()

    return render(request, "user/password_reset.html", {"form": form})