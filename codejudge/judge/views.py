#!/usr/bin/python

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sessions.models import Session
from django.conf import settings
from django.conf.urls.static import static
from judge.models import *
from authentication.models import *
from datetime import *
import json
import socket
import requests
import commands, unicodedata
import random, string, os, subprocess
from django.utils import timezone

# Create your views here.

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def check_submission_validity(contest):
    s_time = contest.startTime
    e_time = contest.endTime

    if timezone.now() < e_time and timezone.now() > s_time:
        return 1
    # Case when opening before
    elif timezone.now() < e_time:
        return 0
    # Case when opening after
    else:
        return 2


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
        
@login_required
def problem(request, contestId, problemId):
    contest = Contest.objects.get(id = contestId)
    var = check_submission_validity(contest)
    # Case when timings are correct
    if var == 1:

        problem = Problem.objects.filter(contest_id=contestId, id=problemId)
        comment = Comments.objects.filter(problem_id=problemId, contest_id=contestId)
        language = Language.objects.all()
        return render(request, 'users/problem.html', {'problem': problem, 'language':language, 'comment':comment})

    elif var == 2:
        return HttpResponseForbidden('The contest has yet not started')

    elif var == 0:
        return HttpResponseForbidden('The contest has already ended')


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
def profile(request):
    hacker = Hacker.objects.get(username = request.session['username'])
    return render(request, 'users/profile.html', {'hacker':hacker})  

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
    h.first_name = request.POST['newFirstName']
    h.last_name = request.POST['newLastName']
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

        var = check_submission_validity(c)
        # Case when timings are correct
        if var == 1:

            payload = {'fmt':'json', 'username':request.session['username'], 'password':request.session['password']}
            auth = requests.get("http://localhost:8000/v1/getAuthID",payload)
            answer = auth.json()
            sol = Solution(hacker=h, contest=c, problem =p , language=l, attempts=0, time=0.0, status=0)

            
            sol.save()

            sol_id = sol.id

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
            print "\n" 
            x = commands.getstatusoutput(arg)
            compile_status = x[1] 

            pos = compile_status.find('error')
            if pos != -1:
                compile_status = compile_status[pos - 6:]
                compile_status.replace("error","")

            # os.system(arg)

            #  checkeing whether the fil got compiled or not.
            file_compiled = False

            print "File address: " + os.getcwd() + '/' + file_name
            file_compiled = os.path.isfile(os.getcwd() + '/' + file_name)


            filepath = os.getcwd() + '/' + file_name
            print filepath


            if file_compiled is True:
                print "\n \n ARG :- ", arg
                os.system(arg)

                print "Output :- ", output
                # print filepath

                print "File Name " + str(sol.id) + "." + str(l.extension)
                sock.connect("127.0.0.1", 6029)
                temp = json.dumps({'id': sol.id, 
                     'filepath': filepath,

                     'input': input,
                     'output': output,

                     'sol_id': sol_id,
                     'time': p.timeLimit})
                sock.send(temp)
                return HttpResponseRedirect('/judge/success')

            else:
                sol.status = 1
                sol.save()
                # return HttpResponseRedirect('/judge/success')
                return render(request, 'users/success_error.html', {'error': compile_status})

        elif var == 2:
            return HttpResponseForbidden('The contest has Yet not started')

        elif var == 0:
            return HttpResponseForbidden('The contest has already ended')


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

def trial(request):
    x = int(request.GET.get('sol_id', ''))
    print request.GET.get('sol_id', '')
    print request.GET.get('result', '')
    x = Solution.objects.get(id = x)
    result = request.GET.get('result', '5')

    # Result = 1 means output matched.
    print "Result is ", result
    x.status = int(result)

    x.save()
    print x
    return HttpResponse()


def handler404(request):
    response = render_to_response('user/login.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response