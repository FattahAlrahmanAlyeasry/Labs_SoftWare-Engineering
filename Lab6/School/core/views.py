"""
Enhanced Views using Class-Based Views and Django REST Framework
Following enterprise-level architecture patterns
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Department, Student, Teacher, UniversityCard, Document, Report
# from .serializers import (
#     StudentSerializer, TeacherSerializer, DepartmentSerializer, 
#     DocumentSerializer, UniversityCardSerializer
# )
from .forms import StudentForm, TeacherForm, DocumentForm, ReportForm
# from .filters import StudentFilter, TeacherFilter


class DashboardView(LoginRequiredMixin, TemplateView):
    """Enhanced Dashboard with statistics"""
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context.update({
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_teachers': Teacher.objects.filter(is_active=True).count(),
            'total_departments': Department.objects.filter(is_active=True).count(),
            'avg_gpa': Student.objects.filter(is_active=True).aggregate(
                avg_gpa=Avg('gpa')
            )['avg_gpa'] or 0,
            'recent_students': Student.objects.filter(is_active=True).order_by('-created_at')[:5],
            'recent_teachers': Teacher.objects.filter(is_active=True).order_by('-created_at')[:5],
        })
        
        # Department statistics
        dept_stats = Department.objects.annotate(
            student_count=Count('students', filter=Q(students__is_active=True)),
            teacher_count=Count('teachers', filter=Q(teachers__is_active=True))
        ).filter(is_active=True)
        context['department_stats'] = dept_stats
        
        return context


class StudentListView(LoginRequiredMixin, ListView):
    """Enhanced Student List with filtering and pagination"""
    model = Student
    template_name = 'core/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Student.objects.filter(is_active=True).select_related(
            'user', 'department'
        ).order_by('student_id')
        
        # Simple filtering without django-filter
        name = self.request.GET.get('name')
        student_id = self.request.GET.get('student_id')
        department = self.request.GET.get('department')
        level = self.request.GET.get('level')
        
        if name:
            queryset = queryset.filter(user__first_name__icontains=name)
        if student_id:
            queryset = queryset.filter(student_id__icontains=student_id)
        if department:
            queryset = queryset.filter(department_id=department)
        if level:
            queryset = queryset.filter(level=level)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.filter(is_active=True)
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    """Enhanced Student Detail View"""
    model = Student
    template_name = 'core/student_detail.html'
    context_object_name = 'student'
    
    def get_queryset(self):
        return Student.objects.filter(is_active=True).select_related(
            'user', 'department'
        ).prefetch_related('documents', 'university_card')


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Enhanced Student Creation"""
    model = Student
    form_class = StudentForm
    template_name = 'core/student_form.html'
    success_url = reverse_lazy('core:student_list')
    permission_required = 'core.add_student'
    
    def form_valid(self, form):
        messages.success(self.request, _('Student created successfully!'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, _('Please correct the errors below.'))
        return super().form_invalid(form)


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Enhanced Student Update"""
    model = Student
    form_class = StudentForm
    template_name = 'core/student_form.html'
    permission_required = 'core.change_student'
    
    def get_success_url(self):
        return reverse_lazy('core:student_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, _('Student updated successfully!'))
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Enhanced Student Deletion with soft delete"""
    model = Student
    template_name = 'core/student_confirm_delete.html'
    success_url = reverse_lazy('core:student_list')
    permission_required = 'core.delete_student'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Soft delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, _('Student deactivated successfully!'))
        return redirect(self.success_url)


class TeacherListView(LoginRequiredMixin, ListView):
    """Enhanced Teacher List with filtering and pagination"""
    model = Teacher
    template_name = 'core/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Teacher.objects.filter(is_active=True).select_related(
            'user', 'department'
        ).order_by('employee_id')
        
        # Simple filtering without django-filter
        name = self.request.GET.get('name')
        employee_id = self.request.GET.get('employee_id')
        department = self.request.GET.get('department')
        
        if name:
            queryset = queryset.filter(user__first_name__icontains=name)
        if employee_id:
            queryset = queryset.filter(employee_id__icontains=employee_id)
        if department:
            queryset = queryset.filter(department_id=department)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.filter(is_active=True)
        return context


class TeacherDetailView(LoginRequiredMixin, DetailView):
    """Enhanced Teacher Detail View"""
    model = Teacher
    template_name = 'core/teacher_detail.html'
    context_object_name = 'teacher'
    
    def get_queryset(self):
        return Teacher.objects.filter(is_active=True).select_related(
            'user', 'department'
        ).prefetch_related('documents')


class TeacherCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Enhanced Teacher Creation"""
    model = Teacher
    form_class = TeacherForm
    template_name = 'core/teacher_form.html'
    success_url = reverse_lazy('core:teacher_list')
    permission_required = 'core.add_teacher'
    
    def form_valid(self, form):
        messages.success(self.request, _('Teacher created successfully!'))
        return super().form_valid(form)


class TeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Enhanced Teacher Update"""
    model = Teacher
    form_class = TeacherForm
    template_name = 'core/teacher_form.html'
    permission_required = 'core.change_teacher'
    
    def get_success_url(self):
        return reverse_lazy('core:teacher_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, _('Teacher updated successfully!'))
        return super().form_valid(form)


class TeacherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Enhanced Teacher Deletion with soft delete"""
    model = Teacher
    template_name = 'core/teacher_confirm_delete.html'
    success_url = reverse_lazy('core:teacher_list')
    permission_required = 'core.delete_teacher'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Soft delete
        self.object.is_active = False
        self.object.save()
        messages.success(request, _('Teacher deactivated successfully!'))
        return redirect(self.success_url)


# API ViewSets disabled for now
# class StudentViewSet(viewsets.ModelViewSet):
#     """Student API ViewSet"""
#     queryset = Student.objects.filter(is_active=True)
#     serializer_class = StudentSerializer
#     permission_classes = [IsAuthenticated]


# AJAX Views for dynamic content
@login_required
def search_students_ajax(request):
    """AJAX search for students"""
    query = request.GET.get('q', '')
    students = Student.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(student_id__icontains=query),
        is_active=True
    )[:10]
    
    results = [{
        'id': student.id,
        'text': f"{student.full_name} ({student.student_id})",
        'student_id': student.student_id,
        'department': student.department.name
    } for student in students]
    
    return JsonResponse({'results': results})


@login_required
def search_teachers_ajax(request):
    """AJAX search for teachers"""
    query = request.GET.get('q', '')
    teachers = Teacher.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(employee_id__icontains=query),
        is_active=True
    )[:10]
    
    results = [{
        'id': teacher.id,
        'text': f"{teacher.full_name} ({teacher.employee_id})",
        'employee_id': teacher.employee_id,
        'department': teacher.department.name
    } for teacher in teachers]
    
    return JsonResponse({'results': results})


class ReportListView(LoginRequiredMixin, ListView):
    """List reports with simple filtering and pagination"""
    model = Report
    template_name = 'core/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20

    def get_queryset(self):
        qs = Report.objects.filter(is_active=True).select_related('student__user', 'created_by')
        q = self.request.GET.get('q')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(student__user__first_name__icontains=q) |
                Q(student__user__last_name__icontains=q) |
                Q(student__student_id__icontains=q)
            )
        if start:
            qs = qs.filter(week_start__gte=start)
        if end:
            qs = qs.filter(week_end__lte=end)
        return qs.order_by('-week_start', '-created_at')


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'core/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.filter(is_active=True).select_related('student__user', 'created_by')


class ReportCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'core/report_form.html'
    success_url = reverse_lazy('core:report_list')
    permission_required = 'core.add_report'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        messages.success(self.request, _('Report created successfully!'))
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, _('Please correct the errors below.'))
        return super().form_invalid(form)


class ReportUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'core/report_form.html'
    permission_required = 'core.change_report'

    def get_success_url(self):
        return reverse_lazy('core:report_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _('Report updated successfully!'))
        return super().form_valid(form)


class ReportDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Report
    template_name = 'core/report_confirm_delete.html'
    success_url = reverse_lazy('core:report_list')
    permission_required = 'core.delete_report'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(request, _('Report deleted successfully!'))
        return redirect(self.success_url)
