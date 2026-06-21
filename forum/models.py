from django.db import models
from django.conf import settings
from courses.models import Course


class ForumThread(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=255, verbose_name='Sujet de discussion')
    content = models.TextField(verbose_name='Question ou message')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False, verbose_name='Résolu')
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='threads',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def reply_count(self):
        return self.replies.count()


class ForumReply(models.Model):
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(verbose_name='Réponse')
    is_official = models.BooleanField(
        default=False,
        verbose_name='Réponse officielle (professeur)',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Réponses forum'

    def __str__(self):
        return f'Réponse de {self.author.username} à {self.thread.title}'

    def save(self, *args, **kwargs):
        if self.author.is_professor():
            self.is_official = True
        super().save(*args, **kwargs)


class ForumAttachment(models.Model):
    reply = models.ForeignKey(ForumReply, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='forum/', blank=True, null=True, verbose_name='Document')
    video_url = models.URLField(blank=True, null=True, verbose_name='Lien vidéo explicative')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pièce jointe - {self.reply.id}'
