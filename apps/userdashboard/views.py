from django.shortcuts import render, HttpResponse, redirect
from . import models
from models import Users
from models import Messages
from models import Comments

def index(request):
    return render(request, "userdashboard/index.html")

def signin(request):
    return render(request, "userdashboard/signin.html")

def login(request):
    if request.method == 'POST':
        user = Users.login.userlogin(login_email=request.POST['email'],login_password=request.POST['password'])
        if user[0] == True:
            if user[2].user_level == 9:
                request.session['user'] = user[2].id
                request.session['admin'] = user[2].user_level
                return redirect('/dashboard/admin')
            else:
                request.session['user'] = user[2].id
                request.session['admin'] = user[2].user_level
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
    if request.session['admin'] == 9:
        return redirect('/dashboard/admin')
    else:
        context= {
            'Users' : Users.objects.all()
        }
        return render(request, "userdashboard/show.html", context)

def showadmin(request):
    if request.session['admin'] == 9:
        context= {
            'Users' : Users.objects.all()
        }
        return render(request, "userdashboard/showadmin.html", context)
    else:
        return redirect('/dashboard/user')

def showusers(request, id):
    mid =Messages.objects.filter(user_id=id)
    midid = mid
    context = {
        "user" : Users.objects.get(id=id),
        "messages" : Messages.objects.filter(user_id=id).order_by('created_at').reverse(),
        "comments" : Comments.objects.all().order_by('created_at').reverse()
    }
    return render(request, "userdashboard/showuser.html", context)

def edit(request, id):
    context = {
        "user" : Users.objects.get(id=id)
    }
    return render(request, "userdashboard/edit.html", context)

def selfedit(request, id):
    context = {
        "user" : Users.objects.get(id=id)
    }
    return render(request, "userdashboard/useredit.html", context)

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

def usersupdate(request, id):
    if request.method == 'POST':
        if int(request.session['user']) == int(id):
            Users.objects.filter(id=id).update(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],description=request.POST['description'])
            return redirect('/users/show/' + id)
        else:
            return redirect('/signin')

def userupdatepass(request, id):
    if request.method == 'POST':
        print id
        print request.session['user']
        if int(request.session['user']) == int(id):
            if request.POST['password'] == request.POST['passconf']:
                updoot = Users.updatepass.userpassupdate(id=id, password=request.POST['password'])
                if updoot[0] == True:
                    return redirect('/dashboard/admin')
                else:
                    context= {
                        'errors' : updoot[1]
                    }
                    return redirect('/user/self/edit/'+ id)
            else:
                return redirect('/user/self/edit/'+ id)
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
                    return redirect('/users/edit/'+ id)
            else:
                return redirect('/users/edit/'+ id)
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

def messages(request, id):
    if request.method == 'POST':
        mid = request.session['user']
        messageleaver = Users.objects.get(id=mid)
        first = messageleaver.first_name
        last = messageleaver.last_name
        user = Users.objects.get(id=id)
        Messages.objects.create(message=request.POST['message'], user=user, first_name=first, last_name=last, m_use_id=mid)
    return redirect('/users/show/'+ id)

def comments(request, id, mid):
    if request.method == 'POST':
        uid = request.session['user']
        commentleaver = Users.objects.get(id=uid)
        mess = Messages.objects.get(id=mid)
        first = commentleaver.first_name
        last = commentleaver.last_name
        user = Users.objects.get(id=id)
        Comments.objects.create(comment=request.POST['comment'],message=mess, user=user, first=first, last=last, c_use_id=uid, mid=mid)
    return redirect('/users/show/'+ id)

def delete(request, id):
    Users.objects.filter(id=id).delete()
    return redirect('/dashboard/admin')

def signout(request):
    request.session.clear()
    return redirect('/')
