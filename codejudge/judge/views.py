#!/usr/bin/python

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sessions.models import Session
from django.conf import settings
from django.conf.urls.static import static
from judge.models import *
from datetime import *
import json
import socket
import requests
import random, string, os, subprocess

# Create your views here.

class Socket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        sent = self.sock.send(msg)


def userLogin(request):
    try:
        if request.session['username']:
            return HttpResponseRedirect("/judge")
    except KeyError:
        context = RequestContext(request)
        error = False
        if request.method == 'POST' and request.is_ajax():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user != None:
                if user.is_authenticated():
                    login(request, user)
                    request.session['username']  = username
                    request.session['password']  = password
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
                else:
                    error = True
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
            else:
                error = True
                return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

        return render(request, 'users/login.html')

def staffLogin(request):
    try:
        if request.session['username']:
            return HttpResponseRedirect("/judge/staffDashboard")
    except KeyError:
        context = RequestContext(request)
        error = False
        if request.method == 'POST' and request.is_ajax():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user != None:
                if user.is_authenticated() and (user.is_staff or user.is_superuser):
                    login(request, user)
                    request.session['username']  = username
                    request.session['password']  = password
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
                else:
                    error = True
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
            else:
                error = True
                return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

    return render(request, 'users/staff_login.html')

def adminLogin(request):
    try:
        if request.session['username']:
            return HttpResponseRedirect("/judge/adminDashboard")
    except KeyError:
        context = RequestContext(request)
        error = False
        if request.method == 'POST' and request.is_ajax():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user != None:
                if user.is_authenticated() and user.is_superuser:
                    login(request, user)
                    request.session['username']  = username
                    request.session['password']  = password
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
                else:
                    error = True
                    return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
            else:
                error = True
            return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

    return render(request, 'users/admin_login.html')

@login_required
def changePassword(request):
    error = 0
    if request.method == "POST":
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']
        user = authenticate(username=request.session['username'], password=old_password)
        if user is not None:
            query = Hacker.objects.get(username=request.session['username'])
            query.set_password(new_password)
            query.save()
            error = 1
            return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
        else:
            error = 2
            return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
            
@user_passes_test(lambda u: u.is_superuser)
def adminDashboard(request):
    return render(request, 'users/admin_dashboard.html')

@user_passes_test(lambda u: u.is_superuser)
def addUser(request):
    return render(request, 'users/add_staff.html')

@user_passes_test(lambda u: u.is_superuser)
def addFaculty(request):
    return render(request, 'users/add_faculty.html')

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def staffDashboard(request):
    return render(request, 'users/staff_dashboard.html')

def home(request):
    link = Link.objects.all()
    notification = Notification.objects.all()
    return render(request, 'users/home.html', {'link':link, 'notif': notification})

def newUser(request):
    return render(request, 'users/register.html')

@login_required
def userLogout(request):
    del request.session['username']
    del request.session['password'] 
    logout(request)
    return HttpResponseRedirect("/judge/home")

@login_required
def problem(request, contestId, problemId):
    problem = Problem.objects.filter(contest_id=contestId, id=problemId)
    language = Language.objects.all()
    return render(request, 'users/problem.html', {'problem': problem, 'language':language})

@login_required
def index(request):
    currentContest = Contest.objects.filter(startTime__lte=datetime.now(), endTime__gt=datetime.now()) 
    futureContest = Contest.objects.filter(startTime__gt=datetime.now())
    pastContest = Contest.objects.filter(endTime__lt=datetime.now())
    return render(request, 'users/index.html', {'futureContest': futureContest, 'pastContest': pastContest, 'currentContest': currentContest })

@login_required
def contest(request, contestId):
    problem = Problem.objects.filter(contest_id=contestId)
    return render(request, 'users/contest.html', {'problem': problem})

@login_required
def course(request, courseId):
    c = Contest.objects.filter(course_id=courseId)
    return render(request, 'users/performance_courses.html', {'contests': c, 'course_id' : courseId})

@login_required
def profile(request):
    hacker = Hacker.objects.filter(username = request.session['username'])
    h = Hacker.objects.get(username=request.session['username'])
    s = 0
    if h.is_staff or h.is_superuser:
        s = 1
    cont = Contest.objects.all()
    l1 = []  
    for c in cont:
        ProSet = Problem.objects.filter(contest_id = c.id)
        l3 = []
        for p in ProSet:
            ProSolSet = Solution.objects.filter(hacker_id = h.id, contest_id = c.id, problem_id = p.id, status = 4)
            if ProSolSet:
                l2 = (str(p.problemTitle),"accepted")
            else:
                l2 = (str(p.problemTitle),"rejected")
            l3.append(l2)
        l1.append((str(c.contestName),tuple(l3)))
    return render(request, 'users/profile.html', {'hacker':hacker, 'data': l1, 'superuser': s})  

@login_required
def changeProfilePic(request):
    if request.method == 'POST':
        m = Hacker.objects.get(username=request.session['username'])
        m.profileImage = request.FILES['image']
        m.save()
        return HttpResponseRedirect('/judge/profile')
    return HttpResponseForbidden('allowed only via POST')

@login_required
def removeProfilePic(request):
    if request.method == 'POST':
        m = Hacker.objects.get(username=request.session['username'])
        m.profileImage = ""
        m.save()
        return HttpResponseRedirect('/judge/profile')
    return HttpResponseForbidden('allowed only via POST')

@login_required
def editProfile(request):
    h = Hacker.objects.get(username=request.session['username'])
    return render(request, 'users/edit_profile.html', {'hacker':h})

@login_required
def editUser(request):
    h = Hacker.objects.get(username=request.session['username'])
    error = 0
    if request.method == "POST" and request.is_ajax():
        newEmail = request.POST['newUserEmail']
        user = Hacker.objects.filter(email=newEmail)
        if len(user) == 1:
            error = 1
            return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
        else:
            h.first_name = request.POST['newFirstName']
            h.last_name = request.POST['newLastName']
            h.email = newEmail
            h.save()
            return HttpResponse(json.dumps({'errors': error}),content_type='application/json')

@login_required
def success(request):
    return render(request, 'users/success.html')

@login_required
def submission(request):
    h = Hacker.objects.get(username=request.session['username'])
    solution = Solution.objects.filter(hacker_id = h.id)
    return render(request, 'users/submission.html', {'solution': solution})


@login_required
def change(request):
    return render(request, 'users/changepass.html')

@login_required
def submitSolution(request):
    if request.method == 'POST':
        h = Hacker.objects.get(username=request.session['username'])
        c = Contest.objects.get(id = request.POST['cid'])
        p = Problem.objects.get(id = request.POST['pid'])
        l = Language.objects.get(id = request.POST['lid'])
        payload = {'fmt':'json', 'username':request.session['username'], 'password':request.session['password']}
        auth = requests.get("http://localhost:8000/v1/getAuthID",payload)
        answer = auth.json()
        sol = Solution(hacker=h, contest=c, problem =p , points=0, language=l, attempts=0, time=0.0, status=0)
        sol.save()
        url = 'http://localhost:8000/v1/file?authid={0}&op=upload&filepath={1}'.format(answer['authid'],str(sol.id) + "." + str(l.extension))
        r = requests.post(url,request.POST['solutionBox'])
        url = 'http://localhost:8000/v1/file?authid={0}&op=download&filepath={1}'.format(answer['authid'],str(sol.id) + "." + str(l.extension))
        req = requests.get(url)
        answer = req.json()
        sol.solution = answer['msg']
        sol.save()
        inputFile = settings.MEDIA_ROOT + str(p.testInput)
        outputFile = settings.MEDIA_ROOT + str(p.testOutput)
        file1 = open(inputFile, 'r')
        input = file1.read()
        file2 = open(outputFile, 'r')
        output = file2.read()
        sock = Socket()

        file_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        text_file = open(file_name + ".cpp", "w")
        text_file.write(request.POST['solutionBox'])
        text_file.close()


        filepath = os.getcwd() + '/' + file_name + '.cpp'
        arg = "g++ " + filepath + ' -o ' + os.getcwd() + '/' + file_name

        print "\n \n ARG :- ", arg
        os.system(arg);



        filepath = os.getcwd() + '/' + file_name

        # print filepath

        print "File Name " + str(sol.id) + "." + str(l.extension)
        sock.connect("127.0.0.1", 6029)
        temp = json.dumps({'id': sol.id, 
             'filepath': filepath,
             # 'filepath': str(sol.id) + "." + str(l.extension),
             # 'code': request.POST['solutionBox'],
             # 'language': l.language,
             'input': input,
             'output': output,
             # 'matchLines': 0,
             # 'partial': 0,
             # 'points':p.points,
             'time': p.timeLimit})
        sock.send(temp)
        return HttpResponseRedirect('/judge/success')
    return HttpResponseForbidden('allowed only via POST')


def register(request): 
    errors = False
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['user_name']
        password = request.POST['pass_word']
        email = request.POST['email']
        roll = str(request.POST['roll'])
        query = Hacker.objects.filter(username=username)
        if query:
            errors = True
        else:
            user = Hacker.objects.create_user(username, email, password)
            user.roll = roll
            user.save()
            payload = {'username':username,'password':password,'email':email}
            requests.get("http://localhost:8000/v1/userRegister",params=payload)
            user = authenticate(username=username, password=password)
            login(request, user)
            
            request.session['username']  = username
            request.session['password']  = password
            
        return HttpResponse(json.dumps({'errors': errors}),content_type='application/json')
    else:
        raise Http404

@user_passes_test(lambda u: u.is_superuser)
def registerStaff(request): 
    errors = False
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['user_name']
        password = request.POST['pass_word']
        email = request.POST['email']
        query = Hacker.objects.filter(username=username)
        if query:
            errors = True
        else:
            user = Hacker.objects.create_staff_user(username, email, password)
            user.save()            
        return HttpResponse(json.dumps({'errors': errors}),content_type='application/json')
    else:
        raise Http404

@user_passes_test(lambda u: u.is_superuser)
def registerFaculty(request):
    errors = False
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['user_name']
        password = request.POST['pass_word']
        email = request.POST['email']
        query = Hacker.objects.filter(username=username)
        if query:
            errors = True
        else:
            user = Hacker.objects.create_user(username, email, password)
            user.is_staff = True
            user.is_superuser = True
            user.save()            
        return HttpResponse(json.dumps({'errors': errors}),content_type='application/json')
    else:
        raise Http404

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def performance(request):
    c = Course.objects.all()
    return render(request, 'users/performance_index.html',{'courses' : c})

def performanceCumulative(request,courseId):
    s = Hacker.objects.filter(course__id = courseId)
    return render(request, 'users/performance_cumulative.html', {'students' : s})

def trial(request):
    return HttpResponse(11111111)
