from django import forms
from courses.models import Course, Enrollment
from .models import ForumThread, ForumReply, ForumAttachment


class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title', 'content', 'course']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['course'].required = False
        self.fields['course'].empty_label = '— Sujet général (hors cours) —'
        if self.user:
            if self.user.is_professor():
                self.fields['course'].queryset = Course.objects.filter(professor=self.user)
            elif self.user.is_student():
                enrolled_ids = Enrollment.objects.filter(student=self.user).values_list('course_id', flat=True)
                self.fields['course'].queryset = Course.objects.filter(id__in=enrolled_ids)
            else:
                self.fields['course'].queryset = Course.objects.none()


class ForumReplyForm(forms.ModelForm):
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    video_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ForumReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Votre réponse...'}),
        }

    def save_attachments(self, reply):
        file = self.cleaned_data.get('file')
        video_url = self.cleaned_data.get('video_url')
        if file or video_url:
            ForumAttachment.objects.create(reply=reply, file=file, video_url=video_url or '')
