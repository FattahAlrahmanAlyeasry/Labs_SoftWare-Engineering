from django.db import models

class Student(models.Model):
    # لا تعرّف id بنفسك
    Name = models.CharField(max_length=20)
    Age = models.IntegerField()
    Level = models.CharField(
        max_length=4,
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
    )
    Gender = models.BooleanField(default=True)
    GPA = models.DecimalField(max_digits=4, decimal_places=3)

