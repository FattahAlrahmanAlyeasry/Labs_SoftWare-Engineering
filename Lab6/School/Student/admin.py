from django.contrib import admin
from .models import student
from django.apps import AppConfig
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display=['name','age','gender','gpa','image','file_report','level']
    list_display_links=['level']
    list_editable=['name','age']
    search_fields=['name','age','gpa']
    list_filter=['age']
    fields=['name','age','level','gender','gpa','image','file_report']
admin.site.register(student,StudentAdmin)   
admin.site.site_header="School ManageMent System"
admin.site.site_title=("School ManageMent System")
