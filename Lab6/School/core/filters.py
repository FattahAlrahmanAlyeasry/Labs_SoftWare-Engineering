"""
Django Filter classes for advanced filtering functionality
"""
import django_filters
from django import forms
from .models import Student, Teacher, Department


class StudentFilter(django_filters.FilterSet):
    """Advanced filtering for students"""
    name = django_filters.CharFilter(
        field_name='user__first_name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name'})
    )
    student_id = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'})
    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    level = django_filters.ChoiceFilter(
        choices=Student.LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gpa_min = django_filters.NumberFilter(
        field_name='gpa',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min GPA'})
    )
    gpa_max = django_filters.NumberFilter(
        field_name='gpa',
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max GPA'})
    )

    class Meta:
        model = Student
        fields = ['name', 'student_id', 'department', 'level', 'gender']


class TeacherFilter(django_filters.FilterSet):
    """Advanced filtering for teachers"""
    name = django_filters.CharFilter(
        field_name='user__first_name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name'})
    )
    employee_id = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'})
    )
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    qualification = django_filters.ChoiceFilter(
        choices=Teacher.QUALIFICATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Teacher
        fields = ['name', 'employee_id', 'department', 'qualification', 'gender']
