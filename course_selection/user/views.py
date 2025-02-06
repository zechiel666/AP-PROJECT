from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages 
from .forms import *
from .models import User



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user in DB

            # Log the user in
            login(request, user)

            # Redirect based on user level
            if user.user_level == 'teacher':
                return redirect('#')  # add later
            return redirect('/courses/')  # Redirect students

    else:
        form = UserCreationForm()

    return render(request, 'user/register.html', {'form': form})

def custom_login_view(request):
    template = 'user/registration/login.html'  # Set full path to template
    form = StudentLoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        # Redirect based on user type
        if user.user_level == "student":
            return redirect('/courses/')
        elif user.user_level == "teacher":
            return redirect("#")  #add later

        messages.error(request, "Invalid student number or password.")

    return render(request, template, {"form": form})

def custom_logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout

    
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