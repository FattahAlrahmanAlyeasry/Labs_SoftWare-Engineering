from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('showAllStudent/', views.showAllStudent, name="show"),
    path('EditStudent/<int:id>/', views.EditStudent, name="edit"),
    path("DeleteStudent/<int:id>/", views.DeleteStudent, name="delete"),
    path("Read_One_Student/<int:id>/", views.Read_One_Student, name="Read_One_Student"),
    path('AddStudent/', views.AddStudent, name='add_student'),
]
