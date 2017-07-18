from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.static import serve
import subprocess, os, time
from .models import Slide, Homework, Accomplish, Upload
from django.contrib.auth.models import User
from .forms import DocumentForm

# Create your views here.
def index(request):
    this_student_id = "10001"
    slides = Slide.objects.all()
    homeworks = Homework.objects.all()
    hw = []
    acc = []
    for homework in homeworks:
        for accomplish in homework.accomplish_set.all():
            if accomplish.user.profile.student_id == this_student_id:
                hw.append(homework)
                acc.append(accomplish)
    hw_acces = zip(hw, acc)
    content = {
            'slides': slides, 
            'hw_acces': hw_acces,
            'student_id': this_student_id,
            }
    return render(request, 'home/index.html', content)

def upload(request, student_id, hw_id, acc_id):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
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
            return HttpResponse('Upload success!')
    else:
        form = DocumentForm()
    return render(request, 'home/upload.html', {'form': form})

def download(request, student_id, hw_id):
    student_name = User.objects.get(userprofile__student_id=student_id).username
    filename_pre = student_name + '_' + hw_id
    filename_real = Upload.objects.filter(std_filename__startswith=filename_pre).order_by('-id')[0].std_filename
    filepath = 'home/upload/' + filename_real
    print(filepath)
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

