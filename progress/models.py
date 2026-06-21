from django.db import models
from courses.models import Course

class Progress(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='progress')
    current_chapter = models.CharField(max_length=200, verbose_name="Chapitre en cours", blank=True)
    completed_chapters = models.TextField(verbose_name="Chapitres terminés", blank=True, help_text="Liste ou description des chapitres terminés.")
    percentage = models.PositiveIntegerField(default=0, verbose_name="Pourcentage d'avancement")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Avancement de {self.course.title} ({self.percentage}%)"
