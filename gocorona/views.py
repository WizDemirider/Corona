from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape
from .models import Code
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from logics import sendmail

def index(request):
    return HttpResponse("Welcome!")

def signupUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password1'])
        raw_password2 = escape(request.POST['password2'])
        try:
            if raw_password == raw_password2 and len(raw_password) >= 6:
                user = User.objects.create(username=username, password=raw_password)
                user.set_password(raw_password)
                user.save()
                login(request, user) # logs User in
                return redirect('home')
            elif len(raw_password) >= 6:
                return render(request, 'Authentication/signup.html', {'error': "Passwords do not match!"})
            else:
                return render(request, 'Authentication/signup.html', {'error': "Password must be 6 characters or more"})
        except Exception as e:
            return render(request, 'Authentication/signup.html', {'error': str(e)})
    return render(request, 'Authentication/signup.html', {'error': None})

def loginUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password'])
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user) # logs User in
            return redirect('home')
        else:
            return render(request, 'Authentication/signup.html', {'error': "Unable to Log you in!"})
    return render(request, 'Authentication/login.html', {'error': None})

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required
def home(request):
    codes = Code.objects
    return render(request,'Authentication/home.html',{'code':codes,'f':False})
def coding(request):
    return render(request,'code/coding.html')
def testout(request):#just to see if its working, to be altered
    lang = request.POST.get("language",False)
    code = request.POST.get("code",False)
    ip = request.POST.get("input",False)
    is_pub = request.POST.get("is_public",False)
    if is_pub == "False":
        is_pub = ""
    email = request.POST.get("email",False)
    c = Code()
    c.language = lang
    c.input = ip
    c.output = ""
    c.is_public = bool(is_pub)
    c.code = code
    c.save()
    #put your compiler logic here.
    comp = True#stores if compiler worked or not
    if comp:
        sendmail(email,User().username,'Success! Your code compiled','Your code succesfully compiled. Come and see if its the output you wanted!!')
    else:
        sendmail(email,User().username,'Oh no! Your code was compiled succesfully','Something went wrong. Come and check your code!')
    return render(request,'code/test.html',{'lang':lang,'code':code,'ip':ip,'pub':is_pub})
