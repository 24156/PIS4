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
        fields = ['title', 'description', 'due_date', 'max_score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'comment']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback', 'status']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
