from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserCreationForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            if user.user_level == 'admin':
                user.is_staff = True  # Mark admin users
            user.save()  # Now save in DB
            login(request, user)
            if user.user_level == 'admin':
                return redirect('#') #add later
            else:
                return redirect('#') #add later
    else:
        form = UserCreationForm()

    return render(request, 'user/register.html', {'form': form})
