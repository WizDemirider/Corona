from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape
from .models import Code
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import requests, json
from pygments import highlight, lexers, formatters

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')

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
    codes = Code.objects.all()
    for c in codes:
        lex = lexers.get_lexer_by_name(c.language.split()[0])
        formatter = formatters.HtmlFormatter(noclasses=True)
        c.h_code = highlight(c.code, lex, formatter)

    return render(request,'home.html',{'codes':codes})

@login_required
def coding(request):
    if request.method == 'POST':
        lang = request.POST.get("language","").split(':')
        code = request.POST.get("code","")
        ip = request.POST.get("input","")
        is_pub = request.POST.get("is_public",False)

        r = requests.post('https://api.judge0.com/submissions/', json={"source_code": code, "language_id": int(lang[0]), "stdin": ip})
        data = json.loads(r.text)

        c = Code()
        c.language = lang[1]
        c.language_id = int(lang[0])
        c.stdin = ip
        c.is_public = bool(is_pub)
        c.code = code
        c.owner = request.user
        c.token = data['token']
        c.save()
        return redirect('test', c.pk)

    r  = requests.get('https://api.judge0.com/languages/')
    data = json.loads(r.text)
    return render(request,'code/coding.html', {'languages': data})

@login_required
def testout(request, **kwargs):
    pk = kwargs['pk']
    c = Code.objects.get(pk=pk)
    data = None

    lex = lexers.get_lexer_by_name(c.language.split()[0])
    formatter = formatters.HtmlFormatter(noclasses=True)
    h_code = highlight(c.code, lex, formatter)

    if not c.stdout or bool(request.GET.get('recheck-status', False)):
        r = requests.get('https://api.judge0.com/submissions/'+c.token)
        data = json.loads(r.text)
        if data['stderr']:
            c.stdout = data['stderr']
        else:
            c.stdout = data['stdout']
        c.uptime = data['time']
        c.save()
    return render(request,'code/test.html',{'code_object':c, 'data':data, 'h_code':h_code})
