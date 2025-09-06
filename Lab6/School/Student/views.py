from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import student
from .forms import StudentForm
import os
from User.utils import send_update_notification

# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required
def ShowAll(request):
    st = student.objects.all()
    return render(request,"ShowAll.html",{"st":st})

@login_required
def successEdit(request):
    if request.method == 'POST':
        try:
            st = student.objects.get(pk=request.POST.get("id"))
            form = StudentForm(request.POST, request.FILES, instance=st)
            if form.is_valid():
                form.save()
                messages.success(request, 'تم تحديث بيانات الطالب بنجاح')
                if request.user.email:
                    send_update_notification(request.user.email, request.user.username, 'بيانات طالب')
                return render(request, 'SuccessEdit.html')
            else:
                messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
                return render(request, "Edit.html", {"form": form, "st": st})
        except student.DoesNotExist:
            return render(request, 'SuccessEdit.html', {'error': 'الطالب غير موجود'})
    return render(request, 'SuccessEdit.html')

@login_required
def Delete(request,id):
    try:
        st_data = student.objects.filter(pk=id).values('id', 'name', 'age', 'gender', 'level', 'gpa', 'image', 'report', 'file_report').first()
        if not st_data:
            return render(request,"Delete.html", {'error': 'الطالب غير موجود'})
        st_obj = student.objects.filter(pk=id).first()
        if not st_obj:
            return render(request,"Delete.html", {'error': 'الطالب غير موجود'})
    except student.DoesNotExist:
        return render(request,"Delete.html", {'error': 'الطالب غير موجود'})
    
    if request.method == 'POST':
        # حذف الصورة إذا كانت موجودة
        if st_data['image'] and st_obj.image:
            image_path=st_obj.image.path
            if os.path.exists(image_path) :
                os.remove(image_path)
        
        # حذف الملف إذا كان موجود
        if st_data['file_report'] and st_obj.file_report :
          file_path=st_obj.file_report.path
          if os.path.exists(file_path):
             os.remove(file_path)
        
        # حذف السجل من قاعدة البيانات
        st_obj.delete()
        return render(request,"SuccessDelete.html")
    else:
        return render(request,"Delete.html", {"st": st_data})

@login_required
def Edit(request,id):
    try:
        st_data = student.objects.filter(pk=id).values('id', 'name', 'age', 'gender', 'level', 'gpa', 'image', 'report', 'file_report').first()
        if not st_data:
            return render(request,"Edit.html", {'error': 'الطالب غير موجود'})
        st_instance = student.objects.filter(pk=id).first()
        if request.method == 'POST':
            form = StudentForm(request.POST, request.FILES, instance=st_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'تم تحديث بيانات الطالب بنجاح')
                return render(request,'SuccessEdit.html')
            else:
                messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
                return render(request,"Edit.html",{"form": form, "st": st_data})
        else:
            form = StudentForm(instance=st_instance)
            return render(request,"Edit.html",{"form": form, "st": st_data})
    except student.DoesNotExist:
        return render(request,"Edit.html", {'error': 'الطالب غير موجود'})

@login_required
def Add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة الطالب بنجاح')
            if request.user.email:
                send_update_notification(request.user.email, request.user.username, 'إضافة طالب جديد')
            return render(request, 'successAdd.html')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
            return render(request, "AddStudent.html", {'form': form})
    else:
        form = StudentForm()
    return render(request, "AddStudent.html", {'form': form})
