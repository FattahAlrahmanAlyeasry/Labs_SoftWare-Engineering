"""
Core models for the School Management System
Following Django best practices and enterprise-level architecture
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from PIL import Image
import os


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    Following Django best practices for user management
    """
    ROLE_CHOICES = [
        ('admin', _('Administrator')),
        ('teacher', _('Teacher')),
        ('student', _('Student')),
        ('staff', _('Staff')),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name=_('Role')
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Phone Number')
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date of Birth')
    )
    profile_image = models.ImageField(
        upload_to='profiles/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name=_('Profile Image')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'core_user'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            self._resize_image()
    
    def _resize_image(self):
        """Resize profile image to optimize storage"""
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)


class BaseModel(models.Model):
    """
    Abstract base model with common fields
    Following DRY principle
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    
    class Meta:
        abstract = True


class Department(BaseModel):
    """
    Department model for organizing students and teachers
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Department Name')
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Department Code')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Location')
    )
    head_of_department = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments',
        verbose_name=_('Head of Department')
    )
    
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(BaseModel):
    """
    Enhanced Student model following Django best practices
    """
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]
    
    LEVEL_CHOICES = [
        ('1', _('First Year')),
        ('2', _('Second Year')),
        ('3', _('Third Year')),
        ('4', _('Fourth Year')),
        ('5', _('Fifth Year')),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name=_('User Account')
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Student ID')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name=_('Department')
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(100)],
        verbose_name=_('Age')
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name=_('Gender')
    )
    level = models.CharField(
        max_length=1,
        choices=LEVEL_CHOICES,
        verbose_name=_('Academic Level')
    )
    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(4.00)],
        verbose_name=_('GPA')
    )
    enrollment_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Enrollment Date')
    )
    graduation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Graduation Date')
    )
    emergency_contact = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_('Emergency Contact')
    )
    address = models.TextField(
        blank=True,
        verbose_name=_('Address')
    )
    
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['student_id']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['department', 'level']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = self._generate_student_id()
        super().save(*args, **kwargs)
    
    def _generate_student_id(self):
        """Generate unique student ID"""
        import datetime
        year = datetime.datetime.now().year
        last_student = Student.objects.filter(
            student_id__startswith=f"{year}"
        ).order_by('student_id').last()
        
        if last_student:
            last_number = int(last_student.student_id[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"{year}{new_number:04d}"


class Teacher(BaseModel):
    """
    Enhanced Teacher model following Django best practices
    """
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]
    
    QUALIFICATION_CHOICES = [
        ('bachelor', _('Bachelor\'s Degree')),
        ('master', _('Master\'s Degree')),
        ('phd', _('PhD')),
        ('other', _('Other')),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name=_('User Account')
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Employee ID')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='teachers',
        verbose_name=_('Department')
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(22), MaxValueValidator(100)],
        verbose_name=_('Age')
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name=_('Gender')
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Salary')
    )
    qualification = models.CharField(
        max_length=20,
        choices=QUALIFICATION_CHOICES,
        verbose_name=_('Highest Qualification')
    )
    specialization = models.CharField(
        max_length=100,
        verbose_name=_('Specialization')
    )
    hire_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Hire Date')
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Years of Experience')
    )
    
    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')
        ordering = ['employee_id']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self._generate_employee_id()
        super().save(*args, **kwargs)
    
    def _generate_employee_id(self):
        """Generate unique employee ID"""
        import datetime
        year = datetime.datetime.now().year
        last_teacher = Teacher.objects.filter(
            employee_id__startswith=f"T{year}"
        ).order_by('employee_id').last()
        
        if last_teacher:
            last_number = int(last_teacher.employee_id[-4:])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"T{year}{new_number:04d}"


class UniversityCard(BaseModel):
    """
    University ID Card model with proper relationship
    """
    CARD_TYPE_CHOICES = [
        ('general', _('General')),
        ('financial', _('Financial Aid')),
        ('international', _('International Student')),
    ]
    
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='university_card',
        verbose_name=_('Student')
    )
    card_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Card Number')
    )
    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPE_CHOICES,
        default='general',
        verbose_name=_('Card Type')
    )
    issue_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Issue Date')
    )
    expiry_date = models.DateField(
        verbose_name=_('Expiry Date')
    )
    
    class Meta:
        verbose_name = _('University Card')
        verbose_name_plural = _('University Cards')
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Card {self.card_number} - {self.student.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = self._generate_card_number()
        if not self.expiry_date:
            import datetime
            self.expiry_date = datetime.date.today() + datetime.timedelta(days=365*4)  # 4 years
        super().save(*args, **kwargs)
    
    def _generate_card_number(self):
        """Generate unique card number"""
        import random
        import string
        while True:
            card_number = ''.join(random.choices(string.digits, k=10))
            if not UniversityCard.objects.filter(card_number=card_number).exists():
                return card_number


class Report(BaseModel):
    """
    Weekly student report model with proper validation
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('Student')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Report Title')
    )
    content = models.TextField(
        verbose_name=_('Report Content')
    )
    week_start = models.DateField(
        verbose_name=_('Week Start')
    )
    week_end = models.DateField(
        verbose_name=_('Week End')
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=50,
        verbose_name=_('Performance Rating')
    )
    attachment = models.FileField(
        upload_to='reports/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])],
        verbose_name=_('Attachment')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_reports',
        verbose_name=_('Created By')
    )

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        ordering = ['-week_start', '-created_at']
        unique_together = ('student', 'week_start', 'week_end')
        indexes = [
            models.Index(fields=['student', 'week_start', 'week_end']),
        ]

    def __str__(self):
        return f"{self.title} - {self.student.full_name} ({self.week_start} → {self.week_end})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.week_end and self.week_start and self.week_end < self.week_start:
            raise ValidationError(_('Week end date cannot be before week start date.'))


class Document(BaseModel):
    """
    Generic document model for storing files and reports
    """
    DOCUMENT_TYPE_CHOICES = [
        ('report', _('Report')),
        ('transcript', _('Transcript')),
        ('certificate', _('Certificate')),
        ('assignment', _('Assignment')),
        ('other', _('Other')),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Document Title')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name=_('Document Type')
    )
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt'])],
        verbose_name=_('File')
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_documents',
        verbose_name=_('Uploaded By')
    )
    # Generic foreign key for flexibility
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='documents',
        verbose_name=_('Related Student')
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='documents',
        verbose_name=_('Related Teacher')
    )
    
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.document_type})"
    
    def delete(self, *args, **kwargs):
        """Delete file when model instance is deleted"""
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
