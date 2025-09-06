from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('show/',views.ShowAll,name="Show"),
    path('delete/<int:id>',views.Delete,name="delete"),
    path('add/',views.Add,name="add"),
    path('edit/<int:id>',views.Edit,name="edit"),
    path('Edited/',views.successEdit,name="successEdit"),

]
