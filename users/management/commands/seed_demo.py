from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User
from courses.models import Course, CourseResource, Assignment, Enrollment
from progress.models import Progress
from forum.models import ForumThread, ForumReply


class Command(BaseCommand):
    help = 'Crée des données de démonstration pour la plateforme éducative'

    def handle(self, *args, **options):
        self.stdout.write('Création des données de démonstration...')

        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@eduplatform.mr',
                'first_name': 'Admin',
                'last_name': 'Système',
                'role': 'professor',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if not admin.check_password('admin123'):
            admin.set_password('admin123')
            admin.save()

        prof, _ = User.objects.get_or_create(
            username='prof.mahmoud',
            defaults={
                'email': 'mahmoud@univ-nkc.mr',
                'first_name': 'Mahmoud',
                'last_name': 'Ould Ahmed',
                'role': 'professor',
            },
        )
        if not prof.check_password('prof123'):
            prof.set_password('prof123')
            prof.save()

        student1, _ = User.objects.get_or_create(
            username='etudiant.fatima',
            defaults={
                'email': 'fatima@student.mr',
                'first_name': 'Fatima',
                'last_name': 'Mint Salem',
                'role': 'student',
            },
        )
        if not student1.check_password('etud123'):
            student1.set_password('etud123')
            student1.save()

        student2, _ = User.objects.get_or_create(
            username='etudiant.mohamed',
            defaults={
                'email': 'mohamed@student.mr',
                'first_name': 'Mohamed',
                'last_name': 'Ould Cheikh',
                'role': 'student',
            },
        )
        if not student2.check_password('etud123'):
            student2.set_password('etud123')
            student2.save()

        course1, _ = Course.objects.get_or_create(
            code='INFO101',
            professor=prof,
            defaults={
                'title': 'Introduction à la Programmation',
                'description': 'Fondamentaux de la programmation en Python pour les étudiants de première année.',
                'semester': 'S1 2025-2026',
            },
        )

        course2, _ = Course.objects.get_or_create(
            code='MATH201',
            professor=prof,
            defaults={
                'title': 'Algèbre Linéaire',
                'description': 'Espaces vectoriels, matrices et applications.',
                'semester': 'S1 2025-2026',
            },
        )

        for course in [course1, course2]:
            Progress.objects.get_or_create(
                course=course,
                defaults={
                    'current_chapter': 'Chapitre 2 - Concepts avancés',
                    'completed_chapters': 'Chapitre 1 - Introduction',
                    'percentage': 35,
                },
            )

        CourseResource.objects.get_or_create(
            course=course1,
            title='Support de cours - Chapitre 1',
            defaults={
                'resource_type': 'pdf',
                'external_url': 'https://docs.python.org/fr/3/tutorial/',
            },
        )

        Assignment.objects.get_or_create(
            course=course1,
            title='TP1 - Variables et boucles',
            defaults={
                'description': 'Réaliser 5 exercices sur les structures de contrôle en Python.',
                'due_date': timezone.now() + timedelta(days=14),
                'max_score': 20,
            },
        )

        Enrollment.objects.get_or_create(student=student1, course=course1)
        Enrollment.objects.get_or_create(student=student1, course=course2)
        Enrollment.objects.get_or_create(student=student2, course=course1)

        thread, _ = ForumThread.objects.get_or_create(
            title='Comment installer Python sur Windows ?',
            defaults={
                'author': student1,
                'content': "Je n'arrive pas à configurer Python sur mon ordinateur. Quelqu'un peut m'aider ?",
                'course': course1,
            },
        )

        if not thread.replies.exists():
            ForumReply.objects.create(
                thread=thread,
                author=student2,
                content="J'ai eu le même problème ! Il faut cocher 'Add Python to PATH' lors de l'installation.",
            )
            ForumReply.objects.create(
                thread=thread,
                author=prof,
                content="Voici la procédure officielle : téléchargez Python depuis python.org, version 3.11 ou supérieure.",
            )

        self.stdout.write(self.style.SUCCESS('Données de démonstration créées avec succès !'))
        self.stdout.write('')
        self.stdout.write('Comptes de test :')
        self.stdout.write('  Admin     : admin / admin123')
        self.stdout.write('  Professeur: prof.mahmoud / prof123')
        self.stdout.write('  Étudiant  : etudiant.fatima / etud123')
        self.stdout.write('  Étudiant  : etudiant.mohamed / etud123')
