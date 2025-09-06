from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import RegisterForm
from .models import Profile
from .utils import send_welcome_email, send_update_notification
from django.core.mail import send_mail
from datetime import datetime

# Create your views here.
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # توجيه للصفحة الرئيسية
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'تم إنشاء الحساب بنجاح')
            # Send welcome email to the new user
            if user.email:
                send_welcome_email(user.email, user.username)
            return redirect('userlogin')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def UserLogout(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    return redirect('userlogin')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        from .forms import ProfileForm
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            # Send update notification email
            if request.user.email:
                send_update_notification(request.user.email, request.user.username, 'الملف الشخصي')
            return redirect('profile')
    else:
        from .forms import ProfileForm
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'profile': profile, 'form': form})

@login_required
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        send_mail('رسالة من فتح الرحمن الياسري', message, 'fattahalrhmanalyeasry@gmail.com', ['malekalmosanif256@gmail.com'])
        messages.success(request, 'تم إرسال الرسالة بنجاح!')
    return render(request, 'send_message.html')