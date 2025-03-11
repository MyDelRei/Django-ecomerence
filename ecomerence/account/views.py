from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    success= False
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            success= True
            form = CreateUserForm()
            return redirect('/') 
    else:
        form = CreateUserForm()
    return render(request, 'account/registration/register.html', {'form': form ,'success':success})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')  # Redirect to the store page after login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'account/login/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')