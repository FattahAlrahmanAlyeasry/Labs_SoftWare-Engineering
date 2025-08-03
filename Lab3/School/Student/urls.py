from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('ShowStudent/',views.ShowStudent,name="show"),
    path('EditStudent/',views.Edit,name="edit"),
    path("DeleteStudent/",views.delete,name="delete"),
]
