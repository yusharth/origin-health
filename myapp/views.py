from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import RegisterForm
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request,'myapp/home.html')

def sign_up(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("/home")
    else:
        form = RegisterForm()
    return render(request,'registration/sign_up.html',{"form":form})