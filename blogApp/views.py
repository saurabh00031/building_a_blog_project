from django.contrib.auth import authenticate,login,logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Postinfo
from .forms import PostReg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpReg,LoginReg
from django.contrib import messages
from django.contrib.auth.models import Group

def home(request):
    posts=Postinfo.objects.all()
    return render(request,'blogApp/home.html',{'posts':posts})

def about(request):
    return render(request,'blogApp/about.html')

def contact(request):
    return render(request,'blogApp/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts=Postinfo.objects.all()
        return render(request,'blogApp/dashboard.html',{'posts':posts})
    else:
        messages.success(request,'Plz login before you proceed!')
        return HttpResponseRedirect('/login/')

def user_login(request):
        if request.method=="POST":
            form=LoginReg(request=request,data=request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,'You have successfully logged in!')
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.success(request,'Sorry! you have not authorised to access the page!')
        else:
            form=LoginReg()
        return render(request,'blogApp/login.html',{'form':form})
  
def user_signup(request):
    if request.method=="POST":
        form=SignUpReg(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulationz,You have successfully created your account')
            user=form.save()
            group=Group.objects.get(name='blogger')
            user.groups.add(group)
    else:
        form=SignUpReg()
    return render(request,'blogApp/signup.html',{'form':form})


#LOGOUT
def user_logout(request):
    logout(request)
    messages.success(request,'Successfully logged out!')
    return HttpResponseRedirect("/")

def add_post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=PostReg(request.POST)
            if form.is_valid():
                form.save()
                form=PostReg()
                return HttpResponseRedirect('/dashboard/')
        else:
            form=PostReg()
            return render(request,'blogApp/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Postinfo.objects.get(pk=id)
            form=PostReg(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi=Postinfo.objects.get(pk=id)
            form=PostReg(instance=pi)
        return render(request,'blogApp/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')       
    
def delete_post(request,id):
    if request.user.is_authenticated:
        pi=Postinfo.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/login/')       
    
