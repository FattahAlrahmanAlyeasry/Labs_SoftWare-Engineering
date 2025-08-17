from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm   # لازم تعمل forms.py فيه StudentForm

# الصفحة الرئيسية
def home(request):
    variable = {
        'gpa': "95",
        'id': "90",
        'name': "fateh alrhman alyeasery",
        'marks': [99, 100, 95, 93],
        'eachsub': {'programming': "99", 'Cient_Server': "100"}
    }
    return render(request, 'home.html', variable)

def AddStudent(request):
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        level = request.POST.get('level')
        gender = request.POST.get('gender')  # True=Male, False=Female
        gpa = request.POST.get('gpa')

        Student.objects.create(
            Name=name,
            Age=age,
            Level=level,
            Gender=True if gender=='Male' else False,
            GPA=gpa
        )
        return redirect('show')  # بعد الإضافة نرجع لصفحة عرض الطلاب

    return render(request, 'add_student.html')
# عرض جميع الطلاب
def showAllStudent(request):
    students = Student.objects.all()
    return render(request, 'showAllStudent.html', {'students': students})



# تعديل طالب
def EditStudent(request, id):
    student = get_object_or_404(Student, pk=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('show')   # اسم المسار عندك showAllStudent
    else:
        form = StudentForm(instance=student)
    return render(request, "EditStudent.html", {'form': form, 'student': student})


# حذف طالب
def DeleteStudent(request, id):
    student = get_object_or_404(Student, pk=id)
    if request.method == "POST":
        student.delete()
        return redirect('show')
    return render(request, 'DeleteStudentlete.html', {'student': student})


# قراءة بيانات طالب واحد
def Read_One_Student(request, id):
    student = get_object_or_404(Student, pk=id)
    return render(request, 'Read_One_Student.html', {'student': student})
