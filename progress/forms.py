from django import forms
from .models import Progress


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['current_chapter', 'completed_chapters', 'percentage']
        widgets = {
            'current_chapter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Chapitre 3 - Algorithmes'}),
            'completed_chapters': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Chapitre 1, Chapitre 2'},
            ),
            'percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }
