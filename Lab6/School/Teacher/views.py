from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import teacher
from .forms import TeacherForm
import os
# Create your views here.
def Index(request):
    return render(request,"home.html")
@login_required
def ShowAll(request):
    t = teacher.objects.values('id', 'name', 'age', 'salary', 'gender', 'image', 'report', 'file_report')
    return render(request,"ShowAllTeachers.html",{"st":t})
@login_required
def EditTeacher(request,id):
    try:
        st_data = teacher.objects.filter(pk=id).values('id', 'name', 'age', 'gender', 'salary', 'image', 'file_report').first()
        if not st_data:
            return render(request,"EditTeacher.html", {'error': 'المعلم غير موجود'})
        st=teacher.objects.get(pk=id)
        if request.method == 'POST':
            form = TeacherForm(request.POST, request.FILES, instance=st)
            if form.is_valid():
                form.save()
                messages.success(request, 'تم تحديث بيانات المعلم بنجاح')
                return render(request,'successEditTeacher.html')
            else:
                messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
                return render(request,"EditTeacher.html",{"form": form, "st": st})
        else:
            form = TeacherForm(instance=st)
            return render(request,"EditTeacher.html",{"form": form, "st": st})
    except teacher.DoesNotExist:
        return render(request,"EditTeacher.html", {'error': 'المعلم غير موجود'})
@login_required
def AddTeacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة المعلم بنجاح')
            return render(request, 'successAddTeacher.html')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
            return render(request, 'AddTeacher.html', {'form': form})
    else:
        form = TeacherForm()
        return render(request, 'AddTeacher.html', {'form': form})
# def succedAdd(request):
 
@login_required
def DeleteTeacher(request,id):
    try:
        st_data=teacher.objects.filter(pk=id).values('id', 'name', 'age', 'gender', 'salary', 'image', 'file_report').first()
        if not st_data:
            return render(request,"DeleteTeacher.html", {'error': 'المعلم غير موجود'})
        st=teacher.objects.get(pk=id)
    except teacher.DoesNotExist:
        return render(request,"DeleteTeacher.html", {'error': 'المعلم غير موجود'})
    # حذف الصورة إذا كانت موجودة
    if st_data['image'] and st.image.path:
        image_path=st.image.path
        if os.path.exists(image_path) :
            os.remove(image_path)
    
    # حذف الملف إذا كان موجود
    if st_data['file_report'] and st.file_report.path :
      file_path=st.file_report.path
      if os.path.exists(file_path):
         os.remove(file_path)
    
    # حذف السجل من قاعدة البيانات
    st.delete()
    return render(request,"DeleteTeacher.html")
def successEditTeacher(request):
    st=teacher.objects.get(pk=request.POST.get("id"))
    if request.method=='POST':
            st.id=request.POST.get("id")
            st. name=request.POST.get("name")
            st.age=request.POST.get("age")
            st.salary=request.POST.get("salary")
            st.gender=request.POST.get("gender")
            st.image=request.FILES.get("image")
            st.file_report=request.FILES.get('file_report')

    st.save()
    return render(request,'successEditTeacher.html')
def show_form(request):
 if request.method=='POST':
   teacher_form=TeacherForm(request.POST,request.FILES)
   if teacher_form.is_valid():
       teacher_form.save()
       return HttpResponse("<h1>the teacher has been created</h1>")
   else:
     return HttpResponse("<h1>the teacher has not been created</h1>") 
