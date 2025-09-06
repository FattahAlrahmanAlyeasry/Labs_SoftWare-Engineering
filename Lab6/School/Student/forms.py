from django import forms
from .models import student

class StudentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=20,
        label="الاسم",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم الطالب'})
    )
    age = forms.IntegerField(
        min_value=16,
        max_value=30,
        label="العمر",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'أدخل العمر'})
    )
    gender = forms.ChoiceField(
        choices=[("Male", "ذكر"), ("Female", "أنثى")],
        label="الجنس",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    level = forms.ChoiceField(
        choices=[("1", "المستوى الأول"), ("2", "المستوى الثاني"), ("3", "المستوى الثالث"), ("4", "المستوى الرابع")],
        label="المستوى",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gpa = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0.00,
        max_value=4.00,
        label="المعدل التراكمي",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00 - 4.00'})
    )
    image = forms.ImageField(
        required=False,
        label="الصورة",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    report = forms.CharField(
        max_length=255,
        required=False,
        label="التقرير",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'أدخل التقرير'})
    )
    file_report = forms.FileField(
        required=False,
        label="ملف التقرير",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'})
    )

    class Meta:
        model = student
        fields = ['name', 'age', 'gender', 'level', 'gpa', 'image', 'report', 'file_report']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) < 2:
            raise forms.ValidationError('يجب أن يكون الاسم أكثر من حرفين')
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError('يجب أن يحتوي الاسم على أحرف فقط')
        return name.strip()

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and (age < 16 or age > 30):
            raise forms.ValidationError('يجب أن يكون العمر بين 16 و 30 سنة')
        return age

    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa and (gpa < 0 or gpa > 4):
            raise forms.ValidationError('يجب أن يكون المعدل بين 0.00 و 4.00')
        return gpa

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
