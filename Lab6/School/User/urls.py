from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',views.UserLogin,name='userlogin'),
    path('register/',views.register,name='register'),
    path('logout/',views.UserLogout,name='UserLogout'),
    path('profile/', views.profile_view, name='profile'),
    path('send-message/', views.send_message, name='send_message'),
]
