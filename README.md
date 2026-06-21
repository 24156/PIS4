# EduPlatform MR — Plateforme Éducative Universitaire

Plateforme web éducative Django (MVT) dédiée aux universités mauritaniennes.

## Fonctionnalités

- **Authentification** : inscription, connexion, profils Professeur / Étudiant
- **Module Cours** : création de cours, ressources (PDF, vidéos, liens), inscriptions
- **Module Devoirs** : assignation, soumission sécurisée, notation par le professeur
- **Module Progression** : suivi du syllabus et tableau de bord étudiant
- **Forum d'entraide** : discussions, réponses étudiants/professeurs, pièces jointes

## Stack technique

- Django 4.2.x
- SQLite (développement) / PostgreSQL (production)
- Bootstrap 5
- Django Forms & Templates

## Installation

```bash
# Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Migrations et données de démo
python manage.py migrate
python manage.py seed_demo

# Lancer le serveur
python manage.py runserver
```

Accédez à : http://127.0.0.1:8000/

## Comptes de démonstration

| Rôle       | Utilisateur         | Mot de passe |
|------------|---------------------|--------------|
| Admin      | admin               | admin123     |
| Professeur | prof.mahmoud        | prof123      |
| Étudiant   | etudiant.fatima     | etud123      |
| Étudiant   | etudiant.mohamed    | etud123      |

Admin Django : http://127.0.0.1:8000/admin/

## Structure du projet

```
PIS4_2026/
├── eduplatform/          # Configuration Django (settings, urls)
├── common/               # Décorateurs, mixins, utilitaires
├── users/                # Authentification et profils
├── courses/              # Cours, ressources, devoirs, inscriptions
├── progress/             # Suivi d'avancement du syllabus
├── forum/                # Forum d'entraide
├── templates/            # Templates globaux et par module
├── static/               # CSS, JS (Bootstrap 5 + custom)
└── media/                # Fichiers uploadés
```

## Modules principaux

### Gestion des utilisateurs
Profils distincts Professeur / Étudiant avec page de profil personnalisable.

### Gestion des cours
Les professeurs créent des cours, déposent des ressources et assignent des devoirs.
Les étudiants s'inscrivent aux cours et accèdent aux contenus.

### Évaluation des avancements
Interface de mise à jour du syllabus par le professeur.
Barre de progression visible par les étudiants sur le tableau de bord.

### Forum d'entraide
Création de fils de discussion, réponses collaboratives (étudiants et professeurs),
réponses officielles des professeurs, pièces jointes document/vidéo.

## Licence

Projet académique — Universités mauritaniennes © 2026
"# PIS4" 
