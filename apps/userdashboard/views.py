from django.shortcuts import render, HttpResponse, redirect
from . import models
from models import Users

def index(request):
    return render(request, "userdashboard/index.html")

def signin(request):
    return render(request, "userdashboard/signin.html")

def login(request):
    return redirect('/signin')

def register(request):
    return render(request, "userdashboard/register.html")

def create(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passconf']:
            user = Users.createuser.register(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email_address=request.POST['email'],create_password=request.POST['password'], level = 1)
            print user[2]
            request.session['user'] = user[2].id
            request.session['admin'] = user[2].user_le vel
            return redirect('/dashboard/admin')
        else:
            return redirect('/register')
    else:
        return redirect('/register')

def showadmin(request):
    context= {
        'Users' : Users.objects.all()
    }
    return render(request, "userdashboard/showadmin.html", context)
