"""
Enhanced Django Admin configuration for School Management System
Following enterprise-level admin interface best practices
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import User, Department, Student, Teacher, UniversityCard, Document, Report


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced User Admin with custom fields"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Additional Info'), {
            'fields': ('role', 'phone_number', 'date_of_birth', 'profile_image')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Additional Info'), {
            'fields': ('role', 'phone_number', 'date_of_birth', 'profile_image')
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Department Admin with enhanced functionality"""
    list_display = ('name', 'code', 'head_of_department', 'student_count', 'teacher_count', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)
    
    def student_count(self, obj):
        return obj.students.filter(is_active=True).count()
    student_count.short_description = _('Active Students')
    
    def teacher_count(self, obj):
        return obj.teachers.filter(is_active=True).count()
    teacher_count.short_description = _('Active Teachers')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Enhanced Student Admin"""
    list_display = ('student_id', 'full_name', 'department', 'level', 'gpa', 'enrollment_date', 'is_active')
    list_filter = ('department', 'level', 'gender', 'is_active', 'enrollment_date')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    ordering = ('student_id',)
    readonly_fields = ('student_id', 'enrollment_date', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('user', 'student_id', 'department')
        }),
        (_('Personal Details'), {
            'fields': ('age', 'gender', 'emergency_contact', 'address')
        }),
        (_('Academic Information'), {
            'fields': ('level', 'gpa', 'enrollment_date', 'graduation_date')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = _('Full Name')
    full_name.admin_order_field = 'user__first_name'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Enhanced Teacher Admin"""
    list_display = ('employee_id', 'full_name', 'department', 'qualification', 'salary', 'hire_date', 'is_active')
    list_filter = ('department', 'qualification', 'gender', 'is_active', 'hire_date')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email', 'specialization')
    ordering = ('employee_id',)
    readonly_fields = ('employee_id', 'hire_date', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('user', 'employee_id', 'department')
        }),
        (_('Personal Details'), {
            'fields': ('age', 'gender')
        }),
        (_('Professional Information'), {
            'fields': ('qualification', 'specialization', 'experience_years', 'salary', 'hire_date')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = _('Full Name')
    full_name.admin_order_field = 'user__first_name'


@admin.register(UniversityCard)
class UniversityCardAdmin(admin.ModelAdmin):
    """University Card Admin"""
    list_display = ('card_number', 'student', 'card_type', 'issue_date', 'expiry_date', 'is_active')
    list_filter = ('card_type', 'is_active', 'issue_date', 'expiry_date')
    search_fields = ('card_number', 'student__user__first_name', 'student__user__last_name', 'student__student_id')
    ordering = ('-issue_date',)
    readonly_fields = ('card_number', 'issue_date', 'created_at', 'updated_at')
    
    def student(self, obj):
        return obj.student.full_name
    student.short_description = _('Student')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Document Admin with file management"""
    list_display = ('title', 'document_type', 'uploaded_by', 'related_person', 'created_at', 'file_size')
    list_filter = ('document_type', 'created_at', 'is_active')
    search_fields = ('title', 'description', 'uploaded_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'file_size')
    
    def related_person(self, obj):
        if obj.student:
            return format_html('<span style="color: blue;">Student: {}</span>', obj.student.full_name)
        elif obj.teacher:
            return format_html('<span style="color: green;">Teacher: {}</span>', obj.teacher.full_name)
        return '-'
    related_person.short_description = _('Related Person')
    
    def file_size(self, obj):
        if obj.file:
            size = obj.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024*1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        return '-'
    file_size.short_description = _('File Size')


# Admin site customization
admin.site.site_header = _("School Management System")
admin.site.site_title = _("School Admin")
admin.site.index_title = _("Welcome to School Management System")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Report Admin for weekly student reports"""
    list_display = ('title', 'student_name', 'week_start', 'week_end', 'rating', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'week_start', 'week_end', 'rating', 'created_at')
    search_fields = ('title', 'student__user__first_name', 'student__user__last_name', 'student__student_id')
    ordering = ('-week_start', '-created_at')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Report Info'), {
            'fields': ('student', 'title', 'content')
        }),
        (_('Period'), {
            'fields': ('week_start', 'week_end')
        }),
        (_('Evaluation'), {
            'fields': ('rating',)
        }),
        (_('Attachment'), {
            'fields': ('attachment',)
        }),
        (_('Meta'), {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at')
        }),
    )

    def student_name(self, obj):
        return obj.student.full_name
    student_name.short_description = _('Student')
