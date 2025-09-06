from django import forms
from .models import teacher

class TeacherForm(forms.ModelForm):
    name = forms.CharField(
        max_length=20,
        label="الاسم",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم المعلم'})
    )
    age = forms.IntegerField(
        min_value=25,
        max_value=65,
        label="العمر",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'أدخل العمر'})
    )
    salary = forms.IntegerField(
        min_value=1000,
        max_value=50000,
        label="الراتب",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'أدخل الراتب'})
    )
    gender = forms.ChoiceField(
        choices=[("Male", "ذكر"), ("Female", "أنثى")],
        label="الجنس",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        required=False,
        label="الصورة",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    file_report = forms.FileField(
        required=False,
        label="ملف التقرير",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'})
    )

    class Meta:
        model = teacher
        fields = ['name', 'age', 'salary', 'gender', 'image', 'file_report']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) < 2:
            raise forms.ValidationError('يجب أن يكون الاسم أكثر من حرفين')
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError('يجب أن يحتوي الاسم على أحرف فقط')
        return name.strip()

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 25 or age > 65):
            raise forms.ValidationError('يجب أن يكون العمر بين 25 و 65 سنة')
        return age

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary and (salary < 1000 or salary > 50000):
            raise forms.ValidationError('يجب أن يكون الراتب بين 1000 و 50000')
        return salary

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('حجم الصورة يجب أن يكون أقل من 5 ميجابايت')
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('يجب أن يكون الملف صورة')
        return image

    def clean_file_report(self):
        file_report = self.cleaned_data.get('file_report')
        if file_report:
            if file_report.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('حجم الملف يجب أن يكون أقل من 10 ميجابايت')
            allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            if file_report.content_type not in allowed_types:
                raise forms.ValidationError('يجب أن يكون الملف من نوع PDF أو Word')
        return file_report