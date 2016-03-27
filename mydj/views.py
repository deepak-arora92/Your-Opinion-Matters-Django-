#author :Deepak
#date : 25-03-2016 
import json
from hashlib import sha1
from datetime import datetime
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localtime, now,utc
from django.db.models import Q

from .models import *

def getUserId(request):
    """ function to get user_id from Request"""
    user_id = None
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        u = Users.objects.filter(userName=username).first()
        if u is not None:
            user_id = u.user_id
    return user_id

def index(request):
    """ signup page"""
    csrf = RequestContext(request)
    return render_to_response('index.html', csrf)

def detail(request, poll_id):
    """ function to return poll options"""
    already_answered=0
    option_id=0
    user_id = getUserId(request)
    a= Answers.objects.filter(question_id=poll_id,user_id = user_id).first()
    if a is not None:
        already_answered = 1
        option_id = a.option_id
    option_list = Options.objects.filter(question_id=poll_id)
    data = serializers.serialize("json", option_list)
    context = json.dumps({'data': data,"already_answered":already_answered,"option_id":option_id})
    return HttpResponse(context, content_type='application/json')

def login(request):
    context={"msg":"","user":""}
    csrf = RequestContext(request)
    if request.POST:
        userName = request.POST['username']
        pwd = request.POST['password']
        password = sha1(pwd).hexdigest()
        u = Users.objects.filter(Q(userName=userName) | Q(emailId=userName),password=password).first()
        if u is not None:
            response = HttpResponseRedirect('home')
            response.set_cookie("username", u.userName)
            return response
        else:
            context={'msg':"Either user name or password is Incorrect!!"}
            return render_to_response('login.html',context,csrf)
    return render_to_response('login.html',context,csrf)

def vote(request,question_id,username,option_id):
    """ function to save poll answer given by user"""
    user = Users.objects.filter(userName = username)
    user_id = getUserId(request)
    ans = Answers(question_id=question_id, user_id=user_id,option_id=option_id)
    ans.save()
    a = json.dumps({"id":ans.id, "option":ans.option_id})
    return HttpResponse(a, content_type='application/json')

def home(request):
    """ view to render home page after user login/signup""" 
    username=''
    csrf = RequestContext(request)
    if request.POST:
        userName = request.POST['user_login']
        email= request.POST['user_email']
        pwd_str= request.POST['user_password']
        pwd = sha1(pwd_str).hexdigest()
        u = Users.objects.filter(Q(userName=userName) | Q(emailId=email)).first()
        if u is not None:
            msg="User name or Email id  already exists."
            return HttpResponse(msg)
        u = Users(userName=userName, emailId=email,password=pwd)
        u.save()
        username=u.userName
    latest_poll_list = Question.objects.all().order_by('-pub_date')[:20]
    context = {'latest_poll_list': latest_poll_list,"user":username}
    return render_to_response('home.html', context,csrf)

def create(request):
    """ it will save the created question to DB."""
    user_id = getUserId(request)
    csrf = RequestContext(request)
    context={'msg':""}
    if request.POST:
        question_text = request.POST['question']
        q= Question(question_text=question_text,pub_date = now())
        q.save()
        question_id = q.id
        op = [request.POST['option_'+str(i)] for i in xrange(1,5)]
        for option_desc in op:
            opObj = Options(question_id=question_id,option_desc=option_desc)
            opObj.save()
        context={'msg':"Successfully Saved!!"}
    return render_to_response('createPoll.html',context,csrf)

@csrf_exempt
def signup_check(request):
    msg='OK'
    csrf = RequestContext(request)
    if request.POST:
        if 'username' in request.POST:
            userName = request.POST['username']
            u = Users.objects.filter(userName=userName).first()
            if u is not None:
                msg="User name already exists."
        elif 'emailId' in request.POST:
            email= request.POST['emailId']
            u = Users.objects.filter(emailId=email).first()
            if u is not None:
                msg="Email id already exists."
    context={'msg':msg}
    return HttpResponse(json.dumps(context), content_type='application/json')