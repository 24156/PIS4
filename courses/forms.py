from django import forms
from .models import Course, CourseResource, Assignment, Submission, Enrollment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'semester']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'semester': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: S1 2025-2026'}),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = CourseResource
        fields = ['title', 'resource_type', 'file', 'video_url', 'external_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'external_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_score', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'comment']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.file:
            self.fields['file'].required = False

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            return file
        if self.instance.pk and self.instance.file:
            return self.instance.file
        raise forms.ValidationError('Veuillez joindre un fichier.')


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade is not None and self.instance.assignment_id:
            max_score = self.instance.assignment.max_score
            if grade > max_score:
                raise forms.ValidationError(f'La note ne peut pas dépasser {max_score}.')
        return grade
