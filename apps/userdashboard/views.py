from django.shortcuts import render, HttpResponse, redirect
from . import models
from models import Users

def index(request):
    return render(request, "userdashboard/index.html")

def signin(request):
    return render(request, "userdashboard/signin.html")

def login(request):
    if request.method == 'POST':
            user = Users.login.userlogin(login_email=request.POST['email'],login_password=request.POST['password'])
            print user[2]
            if user[0] == True:
                if user[2].user_level == 9:
                    request.session['user'] = user[2].id
                    request.session['admin'] = user[2].user_level
                    return redirect('/dashboard/admin')
                else:
                    request.session['user'] = user[2].id
                    return redirect('/dashboard/user')
            else:
                context = {
                    'errors' : user[1]
                }
                return render(request, "userdashboard/signin.html", context)
    else:
        return redirect('/register')


def register(request):
    return render(request, "userdashboard/register.html")

def create(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['passconf']:
            user = Users.createuser.register(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email_address=request.POST['email'],create_password=request.POST['password'], level = 1)
            if user[0] == True:
                print user[2]
                request.session['user'] = user[2].id
                request.session['admin'] = user[2].user_level
                return redirect('/dashboard/admin')
            else:
                context = {
                    'errors' : user[1]
                }
                return render(request, "userdashboard/register.html", context)
        else:
            return redirect('/register')
    else:
        return redirect('/register')

def show(request):
    context= {
        'Users' : Users.objects.all()
    }
    return render(request, "userdashboard/show.html", context)

def showadmin(request):
    context= {
        'Users' : Users.objects.all()
    }
    return render(request, "userdashboard/showadmin.html", context)

def showusers(request, id):
        context = {
            "user" : Users.objects.get(id=id)
        }
        return render(request, "userdashboard/showuser.html", context)

def edit(request, id):
    context = {
        "user" : Users.objects.get(id=id)
    }
    return render(request, "userdashboard/edit.html", context)

def update(request, id):
    if request.method == 'POST':
        l = request.POST['user_level']
        use_level = int(l)
        print use_level
        if request.session['admin'] == 9:
            Users.objects.filter(id=id).update(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],user_level=use_level)
            return redirect('/dashboard/admin')
        else:
            return redirect('/signin')

def updatepass(request, id):
    if request.method == 'POST':
        if request.session['admin'] == 9:
            if request.POST['password'] == request.POST['passconf']:
                updoot = Users.updatepass.userpassupdate(id=id, password=request.POST['password'])
                if updoot[0] == True:
                    return redirect('/dashboard/admin')
                else:
                    context= {
                        'errors' : updoot[1]
                    }
                    return redirect('/users/edit/{id}')
            else:
                return redirect('/users/edit/{id}')
        else:
            return redirect('/signin')

def new(request):
    return render(request, 'userdashboard/new.html')

def createnew(request):
    if request.method == 'POST':
        if request.session['admin'] == 9:
            if request.POST['password'] == request.POST['passconf']:
                user = Users.createuser.register(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email_address=request.POST['email'],create_password=request.POST['password'], level = 1)
                if user[0] == True:
                    print user[2]
                    return redirect('/dashboard/admin')
                else:
                    context = {
                        'errors' : user[1]
                    }
                    return render(request, "userdashboard/new.html", context)
            else:
                return redirect('/signin')
        else:
            return redirect('/users/new')

def delete(request, id):
    Users.objects.filter(id=id).delete()
    return redirect('/dashboard/admin')

def signout(request):
    request.session.clear()
    return redirect('/')
