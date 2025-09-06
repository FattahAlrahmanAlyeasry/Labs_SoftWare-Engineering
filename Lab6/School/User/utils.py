from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_welcome_email(user_email, username):
    """
    Send a welcome email to a newly registered user.
    """
    subject = 'مرحبًا بك في نظام إدارة المدرسة'
    text_content = render_to_string('email/welcome_email.txt', {'username': username})
    html_content = render_to_string('email/welcome_email.html', {'username': username})
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, text_content, from_email, recipient_list, html_message=html_content, fail_silently=False)

def send_update_notification(user_email, username, update_type):
    """
    Send a notification email to a user about an update to their data.
    """
    subject = f'تحديث {update_type} في نظام إدارة المدرسة'
    text_content = render_to_string('email/update_notification.txt', {'username': username, 'update_type': update_type})
    html_content = render_to_string('email/update_notification.html', {'username': username, 'update_type': update_type})
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, text_content, from_email, recipient_list, html_message=html_content, fail_silently=False)
