from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def a_login(request):
    if request.user.is_authenticated:
        return redirect('administrator:logout')
    
    if request.method == 'POST':
        username = request.POST['SRN']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect("administrator:dashboard")
            else:
                messages.error(request, "There was an error logging in")
                return redirect("administrator:login")
        else:
            messages.error(request, "User does not exist")
            return redirect("administrator:login")
        
    return render(request, "alogin.html", {})

def a_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("administrator:login")

def dashboard(request):
    return render(request, )