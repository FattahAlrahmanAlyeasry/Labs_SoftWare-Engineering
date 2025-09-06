"""
Enhanced Django Forms with validation and user experience improvements
Following Django best practices for form handling
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Department, Student, Teacher, Document, UniversityCard, Report

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Enhanced user registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter email address')
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First Name')
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Last Name')
        })
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists.'))
        return email


class StudentForm(forms.ModelForm):
    """Enhanced Student form with validation"""
    
    class Meta:
        model = Student
        fields = ['user', 'department', 'age', 'gender', 'level', 'gpa', 
                 'emergency_contact', 'address']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 16,
                'max': 100
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.00',
                'max': '4.00'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Emergency contact number')
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Full address')
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter users who don't have student profiles
        existing_student_users = Student.objects.values_list('user_id', flat=True)
        self.fields['user'].queryset = User.objects.filter(
            role='student'
        ).exclude(id__in=existing_student_users)
        
        # Filter active departments
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
    
    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0 or gpa > 4):
            raise ValidationError(_('GPA must be between 0.00 and 4.00'))
        return gpa
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 16 or age > 100):
            raise ValidationError(_('Age must be between 16 and 100'))
        return age


class TeacherForm(forms.ModelForm):
    """Enhanced Teacher form with validation"""
    
    class Meta:
        model = Teacher
        fields = ['user', 'department', 'age', 'gender', 'salary', 'qualification',
                 'specialization', 'experience_years']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 22,
                'max': 100
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'qualification': forms.Select(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Area of specialization')
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 50
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter users who don't have teacher profiles
        existing_teacher_users = Teacher.objects.values_list('user_id', flat=True)
        self.fields['user'].queryset = User.objects.filter(
            role='teacher'
        ).exclude(id__in=existing_teacher_users)
        
        # Filter active departments
        self.fields['department'].queryset = Department.objects.filter(is_active=True)
    
    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise ValidationError(_('Salary cannot be negative'))
        return salary
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 22 or age > 100):
            raise ValidationError(_('Age must be between 22 and 100'))
        return age


class DepartmentForm(forms.ModelForm):
    """Department form with validation"""
    
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'location', 'head_of_department']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Department name')
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Department code (e.g., CS, ENG)')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Department description')
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Department location')
            }),
            'head_of_department': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active teachers
        self.fields['head_of_department'].queryset = Teacher.objects.filter(is_active=True)
        self.fields['head_of_department'].empty_label = _('Select Head of Department')
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()
            # Check for uniqueness excluding current instance
            qs = Department.objects.filter(code=code)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(_('A department with this code already exists.'))
        return code


class DocumentForm(forms.ModelForm):
    """Document upload form with validation"""
    
    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'file', 'student', 'teacher']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Document title')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Document description')
            }),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt'
            }),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active students and teachers
        self.fields['student'].queryset = Student.objects.filter(is_active=True)
        self.fields['teacher'].queryset = Teacher.objects.filter(is_active=True)
        self.fields['student'].empty_label = _('Select Student (optional)')
        self.fields['teacher'].empty_label = _('Select Teacher (optional)')
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        teacher = cleaned_data.get('teacher')
        
        # Ensure at least one of student or teacher is selected
        if not student and not teacher:
            raise ValidationError(_('Please select either a student or teacher for this document.'))
        
        # Ensure only one is selected
        if student and teacher:
            raise ValidationError(_('Please select either a student OR a teacher, not both.'))
        
        return cleaned_data
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError(_('File size cannot exceed 10MB.'))
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
            file_extension = file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError(
                    _('Only PDF, DOC, DOCX, and TXT files are allowed.')
                )
        return file


class UniversityCardForm(forms.ModelForm):
    """University Card form"""
    
    class Meta:
        model = UniversityCard
        fields = ['student', 'card_type', 'expiry_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'card_type': forms.Select(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter students who don't have cards
        existing_card_students = UniversityCard.objects.values_list('student_id', flat=True)
        self.fields['student'].queryset = Student.objects.filter(
            is_active=True
        ).exclude(id__in=existing_card_students)
    
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date:
            from datetime import date
            if expiry_date <= date.today():
                raise ValidationError(_('Expiry date must be in the future.'))
        return expiry_date


class ReportForm(forms.ModelForm):
    """Weekly student report form with validation"""

    class Meta:
        model = Report
        fields = ['student', 'title', 'content', 'week_start', 'week_end', 'rating', 'attachment']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Report title')}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Report content')}),
            'week_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'week_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'attachment': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.txt'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # Only active students
        self.fields['student'].queryset = Student.objects.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        week_start = cleaned_data.get('week_start')
        week_end = cleaned_data.get('week_end')
        student = cleaned_data.get('student')

        if week_start and week_end and week_end < week_start:
            raise ValidationError(_('Week end date cannot be before week start date.'))

        # Ensure weekly uniqueness
        if self.instance.pk is None and all([student, week_start, week_end]):
            exists = Report.objects.filter(student=student, week_start=week_start, week_end=week_end).exists()
            if exists:
                raise ValidationError(_('A report for this student and week already exists.'))

        return cleaned_data

    def clean_attachment(self):
        f = self.cleaned_data.get('attachment')
        if f:
            if f.size > 10 * 1024 * 1024:
                raise ValidationError(_('File size cannot exceed 10MB.'))
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']
            ext = f.name.lower().split('.')[-1]
            if f'.{ext}' not in allowed_extensions:
                raise ValidationError(_('Only PDF, DOC, DOCX, and TXT files are allowed.'))
        return f

class SearchForm(forms.Form):
    """Generic search form"""
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search...'),
            'autocomplete': 'off'
        })
    )
    
    def __init__(self, *args, **kwargs):
        self.search_type = kwargs.pop('search_type', 'all')
        super().__init__(*args, **kwargs)
        
        if self.search_type == 'student':
            self.fields['query'].widget.attrs['placeholder'] = _('Search students...')
        elif self.search_type == 'teacher':
            self.fields['query'].widget.attrs['placeholder'] = _('Search teachers...')
        elif self.search_type == 'department':
            self.fields['query'].widget.attrs['placeholder'] = _('Search departments...')
