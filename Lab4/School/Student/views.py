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
    students = [
        {'id': 5, 'name': 'Ahmmed', 'age': 25, 'gpa': 80, 'level': 2},
        {'id': 2, 'name': 'Ali', 'age': 23, 'gpa': 90, 'level': 2},
        {'id': 3, 'name': 'Mohmmed', 'age': 23, 'gpa': 88, 'level': 1},
        {'id': 4, 'name': 'Sali', 'age': 23, 'gpa': 70, 'level': 3},
    ]
    return render(request, 'showStudent.html', {'students': students})

def Edit(request):
    return render(request,"edit.html")
def delete(request):
    return render(request,'delete.html')