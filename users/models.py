from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Étudiant'),
        ('professor', 'Professeur'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def is_professor(self):
        return self.role == 'professor'

    def is_student(self):
        return self.role == 'student'

    def __str__(self):
        return self.get_full_name() or self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, verbose_name='Biographie')
    university = models.CharField(max_length=200, blank=True, verbose_name='Université')
    department = models.CharField(max_length=200, blank=True, verbose_name='Département')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Téléphone')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Photo de profil')

    def __str__(self):
        return f'Profil de {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
