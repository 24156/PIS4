from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Titre du cours')
    description = models.TextField(verbose_name='Description', blank=True)
    code = models.CharField(max_length=20, blank=True, verbose_name='Code du cours')
    semester = models.CharField(max_length=50, blank=True, verbose_name='Semestre')
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'professor'},
        related_name='courses',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def enrolled_count(self):
        return self.enrollments.count()


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrollments',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.student.username} → {self.course.title}'


class CourseResource(models.Model):
    RESOURCE_TYPES = (
        ('pdf', 'Document PDF'),
        ('doc', 'Document'),
        ('video', 'Vidéo'),
        ('link', 'Lien externe'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200, verbose_name='Titre de la ressource')
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='pdf')
    file = models.FileField(upload_to='courses/', blank=True, null=True, verbose_name='Fichier joint')
    video_url = models.URLField(blank=True, null=True, verbose_name='Lien vidéo')
    external_url = models.URLField(blank=True, null=True, verbose_name='Lien externe')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.title} - {self.course.title}'


# Alias pour compatibilité
Resource = CourseResource


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200, verbose_name='Titre du devoir')
    description = models.TextField(verbose_name='Description')
    due_date = models.DateTimeField(verbose_name='Date limite de rendu')
    max_score = models.PositiveIntegerField(default=20, verbose_name='Note maximale')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        from django.utils import timezone
        return timezone.now() > self.due_date


class Submission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('graded', 'Noté'),
        ('returned', 'Retourné'),
    )
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='submissions',
    )
    file = models.FileField(upload_to='assignments/', verbose_name='Fichier rendu')
    comment = models.TextField(blank=True, verbose_name='Commentaire étudiant')
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name='Note',
    )
    feedback = models.TextField(blank=True, verbose_name='Commentaire du professeur')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f'Rendu de {self.student.username} pour {self.assignment.title}'
