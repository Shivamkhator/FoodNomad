from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')
