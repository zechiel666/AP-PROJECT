from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import StudentLoginForm

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
        return reverse_lazy('#')  # Redirect after login *add later