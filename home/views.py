from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.static import serve
import subprocess, os, time, datetime
from .models import Slide, Homework, Accomplish, Upload, UserProfile, Lecture
from django.contrib.auth.models import User
from .forms import DocumentForm

this_student_id = ''

def index(request):
    # prepare student ID
    global this_student_id
    # prepare slides
    slides = Slide.objects.all()
    # prepare homework and accomplish
    homeworks = Homework.objects.all()
    hw = []
    acc = []
    for homework in homeworks:
        for accomplish in homework.accomplish_set.all():
            if accomplish.user.profile.student_id == this_student_id:
                hw.append(homework)
                acc.append(accomplish)
    hw_acces = zip(hw, acc)
    # prepare student name
    student_name = ''
    try:
        student_name = User.objects.get(userprofile__student_id=this_student_id).username
    except User.DoesNotExist:
        pass
    # prepare active_hw
    active_hw = []
    for hw in Homework.objects.order_by('-id'):
        if timezone.localtime(timezone.now()) < hw.ddl:
            active_hw.append(hw.id)
        else:
            break
    # prepare deadline
    deadline = ''
    try:
        student = User.objects.get(userprofile__student_id=this_student_id)
    except User.DoesNotExist:
        pass
    else:
        for acc in student.accomplish_set.order_by('homework__ddl'):
            time_left = acc.homework.ddl - timezone.localtime(timezone.now())
            if acc.submit == False and time_left < datetime.timedelta(hours=8) and time_left > datetime.timedelta(hours=0):
                deadline = '%s in less than %.2f hours.' % (str(acc.homework), time_left.seconds/3600)

    # prepare new_lecture
    new_lecture = ''
    for l in Lecture.objects.order_by('time'):
        if timezone.localtime(timezone.now()) < l.time:
            new_lecture = r'"%s" is on %s.' % (l.title, str(timezone.localtime(l.time)).split('+')[0])

    content = {
            'slides': slides, 
            'hw_acces': hw_acces,
            'student_id': this_student_id,
            'student_name': student_name,
            'deadline': deadline,
            'new_lecture': new_lecture,
            'active_hw': active_hw,
            }
    return render(request, 'home/index.html', content)

@login_required
def upload(request, student_id, hw_id, acc_id):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if timezone.localtime(timezone.now()) < Homework.objects.get(id=hw_id).ddl:
            if form.is_valid():
                SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
                # clean previous version
                student_name = User.objects.get(userprofile__student_id=student_id).username
                std_filename = student_name + '_' + hw_id
                std_path = os.path.join(SITE_ROOT, 'upload', std_filename)
                subprocess.run(['rm '+std_path+'.*'], shell=True)
                # save new version
                form.save()
                # modify submit status
                tmp_acc = Accomplish.objects.get(id=acc_id)
                tmp_acc.submit = True
                tmp_acc.save()
                # get original name
                raw_filename = request.FILES['document'].name
                extension = '.' + raw_filename.split('.')[-1]
                # rename
                std_filename += extension
                newest_doc = Upload.objects.order_by('-id')[0]
                newest_doc.std_filename = std_filename
                newest_doc.save()
                std_path = os.path.join(SITE_ROOT, 'upload', std_filename)
                raw_path = os.path.join(SITE_ROOT, 'upload', raw_filename)
                subprocess.run(['mv '+raw_path+' '+std_path], shell=True)
                return HttpResponse('Upload success!<script>parent.location.reload();</script>')
        else:
            return HttpResponse('Deadline missed. Upload fail.')
    else:
        form = DocumentForm()
    return render(request, 'home/upload.html', {'form': form})

@login_required
def download_hw(request, student_id, hw_id):
    student_name = User.objects.get(userprofile__student_id=student_id).username
    filename_pre = student_name + '_' + hw_id
    filename_real = Upload.objects.filter(std_filename__startswith=filename_pre).order_by('-id')[0].std_filename
    filepath = 'home/upload/' + filename_real
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def download_doc(request, doc_type, doc_id):
    if doc_type == 'slide':
        filepath = 'home/documents/slide/' + Slide.objects.get(id=doc_id).document.name
    elif doc_type == 'homework':
        filepath = 'home/documents/homework/' + Homework.objects.get(id=doc_id).document.name
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        given_username = request.POST.get('username')
        given_password_1 = request.POST.get('password1')
        given_password_2 = request.POST.get('password2')
        if given_username == '' or given_password_1 == '' or given_password_2 == '':
            return HttpResponse('<script>alert("Please complete all blanks!"); parent.location.reload();</script>')
        if given_password_1 != given_password_2:
            return HttpResponse('<script>alert("Password is inconsistent!"); parent.location.reload();</script>')
        try:
            User.objects.get(username=given_username)
        # if this user doesn't exist, accept register request
        except User.DoesNotExist:
            # create user
            new_user = User.objects.create(username=given_username, password=given_password_1)
            new_user.set_password(given_password_1)
            new_user.save()
            # create student_id
            new_student_id = str(int(UserProfile.objects.order_by('-id')[0].student_id) + 1)
            UserProfile.objects.create(user=new_user, student_id=new_student_id)
            # create accomplish
            for hw in Homework.objects.all():
                Accomplish.objects.create(user=new_user, homework=hw)
            register_success = r'<p>Register success.</p><p>Your student ID is %s.</p><p>You can sign in either using your real name or the student ID.</p>' % new_student_id
            return HttpResponse(register_success)
        # if already exist, deny register request
        else:
            return HttpResponse('<script>alert("User already exists. Try another name."); parent.location.reload();</script>')

    return render(request, 'home/signup.html', {})
    
@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            try:
                username = User.objects.get(userprofile__student_id=username).username
            except User.DoesNotExist:
                return HttpResponse('Username or password error. Please try again.<script>parent.location.reload();</script>')
            else:
                user = authenticate(username=username, password=password)
                if user is None:
                    return HttpResponse('Username or password error. Please try again.<script>parent.location.reload();</script>')
        login(request, user)
        global this_student_id
        this_student_id = user.profile.student_id
        return HttpResponse('Sign in success!<script>parent.location.reload();</script>')
    return render(request, 'home/signin.html', {})

def signout(request):
    logout(request)
    global this_student_id
    this_student_id = ''
    return HttpResponseRedirect('/home')
