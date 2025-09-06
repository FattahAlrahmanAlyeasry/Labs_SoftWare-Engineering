from django.urls import path
from . import views
urlpatterns = [
    path('',views.Index,name="home"),
      path('show/',views.ShowAll,name="show"),
     path('DeleteTeacher/<int:id>',views.DeleteTeacher,name="DeleteTeacher"),
    path('AddTeacher/',views.AddTeacher,name="AddTeacher"),
    path('EditTeacher/<int:id>',views.EditTeacher,name="EditTeacher"),
    path('Edited/',views.successEditTeacher,name="successEditTeacher"),

]
