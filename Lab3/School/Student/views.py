from django.shortcuts import render
# Create your views here.
# def index(request):
#     info={'id':"96754664674764543",'name':"Fattah alrhman alyeasery",'Age':"23"}
#     return render(request,'index.html',info)
def home(request):
    variable={'gpa':"95",'id':"90",'name':"fateh alrhman alyeasery",'marks':[99,100,95,93],
             'eachsub':{'programming':"99",'Cient_Server':"100"}}
    return render(request,'home.html',variable)
# def update(request):
#     variable={'gpa':"95",'name':"fateh alrhman alyeasery",'marks':[99,100,95,93],
#              }
#     return render(request,'home.html',variable)
def ShowStudent(request):
   return render(request,'ShowStudent.html')
def Edit(request):
    return render(request,"edit.html")
def delete(request):
    return render(request,'delete.html')