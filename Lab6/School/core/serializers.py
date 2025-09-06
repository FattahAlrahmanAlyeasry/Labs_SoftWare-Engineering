"""
Django REST Framework Serializers for API endpoints
Following enterprise-level API design patterns
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department, Student, Teacher, UniversityCard, Document

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer for API responses"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'role']
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    """Department serializer with statistics"""
    student_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    head_name = serializers.CharField(source='head_of_department.full_name', read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'location', 'head_name', 
                 'student_count', 'teacher_count', 'is_active']
    
    def get_student_count(self, obj):
        return obj.students.filter(is_active=True).count()
    
    def get_teacher_count(self, obj):
        return obj.teachers.filter(is_active=True).count()


class StudentSerializer(serializers.ModelSerializer):
    """Enhanced Student serializer"""
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(is_active=True),
        source='department',
        write_only=True
    )
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    age_group = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'department', 'department_id', 
                 'full_name', 'age', 'age_group', 'gender', 'level', 'gpa', 
                 'enrollment_date', 'graduation_date', 'emergency_contact', 
                 'address', 'is_active']
        read_only_fields = ['id', 'student_id', 'enrollment_date']
    
    def get_age_group(self, obj):
        if obj.age < 20:
            return 'Young'
        elif obj.age < 25:
            return 'Adult'
        else:
            return 'Mature'


class TeacherSerializer(serializers.ModelSerializer):
    """Enhanced Teacher serializer"""
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(is_active=True),
        source='department',
        write_only=True
    )
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    salary_range = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'employee_id', 'department', 'department_id',
                 'full_name', 'age', 'gender', 'salary', 'salary_range',
                 'qualification', 'specialization', 'hire_date', 
                 'experience_years', 'is_active']
        read_only_fields = ['id', 'employee_id', 'hire_date']
    
    def get_salary_range(self, obj):
        salary = float(obj.salary)
        if salary < 3000:
            return 'Entry Level'
        elif salary < 5000:
            return 'Mid Level'
        elif salary < 8000:
            return 'Senior Level'
        else:
            return 'Executive Level'


class UniversityCardSerializer(serializers.ModelSerializer):
    """University Card serializer"""
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.filter(is_active=True),
        source='student',
        write_only=True
    )
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = UniversityCard
        fields = ['id', 'student', 'student_id', 'card_number', 'card_type',
                 'issue_date', 'expiry_date', 'is_expired', 'is_active']
        read_only_fields = ['id', 'card_number', 'issue_date']
    
    def get_is_expired(self, obj):
        from datetime import date
        return obj.expiry_date < date.today()


class DocumentSerializer(serializers.ModelSerializer):
    """Document serializer with file handling"""
    uploaded_by = UserSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    file_size = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'document_type', 'file',
                 'file_size', 'file_url', 'uploaded_by', 'student', 'teacher',
                 'created_at', 'is_active']
        read_only_fields = ['id', 'uploaded_by', 'created_at']
    
    def get_file_size(self, obj):
        if obj.file:
            size = obj.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024*1024:
                return f"{size/1024:.1f} KB"
            else:
                return f"{size/(1024*1024):.1f} MB"
        return None
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None
