#!/usr/bin/python

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sessions.models import Session
from django.conf import settings
from django.conf.urls.static import static
from apps.judge.models import *
from apps.authentication.models import *
from datetime import *
import json
import socket
import requests
import commands, unicodedata
import random, string, os, subprocess
from django.utils import timezone

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
        
@login_required
def problem(request, contestId, problemId):
    contest = Contest.objects.get(id = contestId)
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
def allProblems(request):
    problem = Problem.objects.all()
    return render(request, 'users/allProblems.html', {'problemlist' : problem})

@login_required
def success(request):
    return render(request, 'users/success.html')

@login_required
def submission(request):
    h = Hacker.objects.get(username=request.session['username'])
    solution = Solution.objects.filter(hacker_id = h.id)
    return render(request, 'users/submission.html', {'solution': solution})


def saveCode(request):
    if request.method == "POST":
        h = Hacker.objects.get(username=request.session['username'])
        p = Problem.objects.get(id = request.POST['problem_id'])
        l = Language.objects.get(extension = request.POST['language'])
        request.session['code'] = request.POST['code']
        return HttpResponse('Code Saved locally for two hours')

@login_required
def submitSolution(request):
    if request.method == 'POST':
        h = Hacker.objects.get(username=request.session['username'])
        c = Contest.objects.get(id = request.POST['contest_id'])
        p = Problem.objects.get(id = request.POST['problem_id'])
        l = Language.objects.get(extension = request.POST['language'])
        payload = {'fmt':'json', 'username':request.session['username'], 'password':request.session['password']}
        auth = requests.get("http://localhost:8000/v1/getAuthID",payload)
        answer = auth.json()
        sol = Solution(hacker=h, contest=c, problem =p , language=l, attempts=0, time=0.0, status=0)
        sol.save()
        sol_id = sol.id

        url = 'http://localhost:8000/v1/file?authid={0}&op=upload&filepath={1}'.format(answer['authid'],str(sol.id) + "." + str(l.extension))
        r = requests.post(url,request.POST['code'])
        url = 'http://localhost:8000/v1/file?authid={0}&op=download&filepath={1}'.format(answer['authid'],str(sol.id) + "." + str(l.extension))
        req = requests.get(url)
        answer = req.json()
        
        sol.solution = answer['msg']
        sol.save()

        inputFile = settings.MEDIA_ROOT + '/' + str(p.testInput)
        outputFile = settings.MEDIA_ROOT + '/' + str(p.testOutput)
        file1 = open(inputFile, 'r')
        input_file = file1.read()
        file2 = open(outputFile, 'r')
        output = file2.read()

        """
        saving the file from the solution box
        """
        file_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(10))
        # text_file = open(file_name + ".cpp", "w")
        # text_file.write(request.POST['solutionBox'])
        # text_file.close()


        # """
        # compiling the file locally
        # """
        # filepath = os.getcwd() + '/' + file_name + '.cpp'
        # arg = "g++ " + filepath + ' -o ' + os.getcwd() + '/' + file_name
        # x = commands.getstatusoutput(arg)
        # compile_status = x[1] 

        # """
        # check the status of the compiled file
        # """
        # pos = compile_status.find('error')
        # if pos != -1:
        #     compile_status = compile_status[pos - 6:]
        #     compile_status.replace("error","")

        # """
        # checkeing whether the file got compiled or not.
        # """
        # file_compiled = False

        # print "File address: " + os.getcwd() + '/' + file_name
        # file_compiled = os.path.isfile(os.getcwd() + '/' + file_name)


        # filepath = os.getcwd() + '/' + file_name
        # print filepath

def trial(request):
    x = int(request.GET.get('sol_id', ''))
    print request.GET.get('sol_id', '')
    print request.GET.get('result', '')
    x = Solution.objects.get(id = x)
    result = request.GET.get('result', '5')

    # Result = 1 means output matched.
    x.status = int(result)

    x.save()
    print x
    return HttpResponse()


def handler404(request):
    response = render_to_response('user/login.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response