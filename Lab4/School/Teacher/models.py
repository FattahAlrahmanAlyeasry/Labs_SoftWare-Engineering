from django.db import models

# Create your models here.
# في ملف models.py داخل تطبيقك

from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المدرس")
    subject = models.CharField(max_length=100, verbose_name="المادة")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    experience = models.IntegerField(verbose_name="سنوات الخبرة")
    address = models.CharField(max_length=255, verbose_name="العنوان")
    notes = models.TextField(blank=True, verbose_name="ملاحظات")

    def __str__(self):
        return self.name
