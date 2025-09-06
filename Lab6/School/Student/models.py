from django.db import models
from PIL import Image
from Teacher.models import teacher

# Create your models here.
class student(models.Model):
    name=models.CharField(max_length=20,null=True)
    age=models.IntegerField(default=22)
    gender=models.CharField(choices=[("Male","Male"),("Female","Female")],max_length=6)
    level=models.CharField(choices=[("1","1"),("2","2"),("3","3"),("4","4")],max_length=1)
    gpa=models.DecimalField(max_digits=5,decimal_places=2)
    image=models.ImageField(upload_to='images/%y/%m/%d',null=True)
    uploaded_at=models.DateTimeField(auto_now_add=True,null=True)
    report = models.CharField(max_length=255, null=True, blank=True)
    file_report=models.FileField(upload_to='files/%y/%m/%d/',null=True)
    def __str__(self):
        return self.name
#----------------One Tow One ReleashionShip-------------#
class unv_card (models.Model) :
   expir_date=models.DateField(auto_now=True)
   prod_date=models.DateField(auto_now=True)
   type=models.CharField(choices=[("General","General"),("Finincial","Finincial")],max_length=9)
   student=models.OneToOneField(student,on_delete=models.CASCADE,primary_key=True)
#----------------Many To Many ReleashionShip-----------------#
# تم نقل نموذج المعلم إلى Teacher/models.py لتجنب التكرار
# العلاقة Many-to-Many ستكون في نموذج منفصل إذا لزم الأمر
#-----------One To many ReleaShinShip-----------------#
class Dept(models.Model):
    name=models.CharField(max_length=30) 
    loc=models.TextField()
    add=models.CharField(max_length=70)
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    

  