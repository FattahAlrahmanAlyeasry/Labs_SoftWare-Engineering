from django.urls import path
from . import views

urlpatterns = [
    path('', views.details, name='teacher_home'),  # هذا يمثّل /Teacher/ بدون أي شيء بعده
    path('details/', views.details, name='teacher_details'),
    path('edit/', views.edit_teacher, name='edit_teacher'),
    path('delete/', views.delete_teacher, name='delete_teacher'),
]
