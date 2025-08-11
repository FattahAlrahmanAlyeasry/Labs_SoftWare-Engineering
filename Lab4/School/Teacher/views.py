from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.shortcuts import render

def details(request):
    teachers = [
        {
            'name': 'أحمد محمد',
            'subject': 'رياضيات',
            'email': 'ahmed@example.com',
            'phone': '+966 555 123 456',
            'experience': '5 سنوات خبرة',
            'address': 'الرياض، السعودية',
            'notes': 'مدرس متميز وملتزم',
        },
        {
            'name': 'سارة علي',
            'subject': 'فيزياء',
            'email': 'sara@example.com',
            'phone': '+966 555 654 321',
            'experience': '3 سنوات خبرة',
            'address': 'جدة، السعودية',
            'notes': 'متحمسة لتدريس الطلاب',
        },
        # ... مدرسين آخرين
    ]
    context = {
        'teachers': teachers
    }
    return render(request, 'teacher_details.html', context)



def edit_teacher(request):
    # هنا تعالج تعديل بيانات عامة (مثلاً نموذج تعديل عام)
    return render(request, 'edit_teacher.html')

def delete_teacher(request):
    # هنا تعالج حذف بيانات عامة أو تأكيد حذف عام
    return render(request, 'delete_teacher.html')


def home(request):
    # أي بيانات تريد إرسالها
    return render(request, 'teacher_home.html')
