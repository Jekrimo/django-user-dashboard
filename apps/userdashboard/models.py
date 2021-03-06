from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{4,8}$')

class Createuser(models.Manager):
    def register(self,first_name, last_name, email_address, create_password, level):
        errors = []
        if PASSWORD_REGEX.match(create_password):
            if EMAIL_REGEX.match(email_address):
                if not Users.objects.filter(email=email_address):
                    hashed_pass = bcrypt.hashpw(create_password.encode(), bcrypt.gensalt())
                    user = Users.objects.create(email = email_address, password = hashed_pass, first_name = first_name, last_name = last_name, user_level= level)
                    return (True, errors, user)
                else:
                    errors.append('Sorry, that email already exsists. Please Login.')
                    return(False, errors)
            else:
                if len(email_address) < 6:
                    errors.append("Email address is too short!")
                if not EMAIL_REGEX.match(email_address):
                    errors.append("Email address is invalid")
                if len(email_address) > 30:
                    errors.append("Email address is too Long!")
                return (False, errors)
        else:
            if len(create_password) < 4:
                errors.append("Password is too short!")
            if not PASSWORD_REGEX.match(create_password):
                errors.append("Password is invalid")
            if len(create_password) > 8:
                errors.append("Password is too Long!")
            return (False, errors)

class Login(models.Manager):
    def userlogin(self, login_email, login_password):
        from bcrypt import hashpw, gensalt
        login_errors = []
        if Users.objects.filter(email=login_email).exists() == False:
            login_errors.append("Sorry, no email found. Please try again.")
            return (False, login_errors)

        else:
            user = Users.objects.get(email=login_email)
            password = user.password.encode()
            loginpass = login_password.encode()
            if hashpw(loginpass, password) == password:
                return (True, login_errors, user)
            else:
                login_errors.append("Sorry, no password match")
                return (False, login_errors)

class Updatepassword(models.Manager):
    def userpassupdate(self, password, id):
        passerrors = []
        if PASSWORD_REGEX.match(password):
            hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            Users.objects.filter(id=id).update(password=hashed_pass)
            return (True, passerrors)
        else:
            passerrors.append('Sorry, rules are not met for entered password.')
            return (False, passerrors)


class Users(models.Model):
    user_level = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    createuser = Createuser()
    login = Login()
    updatepass = Updatepassword()
    objects = models.Manager()


class Messages(models.Model):
  message = models.TextField()
  user = models.ForeignKey(Users)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  m_use_id =  models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Comments(models.Model):
  comment = models.TextField()
  user = models.ForeignKey(Users)
  message = models.ForeignKey(Messages)
  first = models.CharField(max_length=30)
  last = models.CharField(max_length=30)
  mid = models.IntegerField()
  c_use_id =  models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
