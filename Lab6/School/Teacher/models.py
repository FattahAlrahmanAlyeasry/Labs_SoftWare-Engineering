from django.db import models

# Create your models here.
class teacher(models.Model):
    name=models.CharField(max_length=20,null=True)
    age=models.IntegerField(default=22)
    salary=models.IntegerField(null=True)
    gender=models.CharField(choices=[("Male","Male"),("Female","Female")],max_length=6)
    image=models.ImageField(upload_to='images/%y/%m/%d',null=True)
    report = models.CharField(max_length=255, null=True, blank=True)
    file_report=models.FileField(upload_to='files/%y/%m/%d/',null=True)
    def __str__(self):
        return self.name