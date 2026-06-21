from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from courses.models import Course, Enrollment
from .forms import RegisterForm, UserProfileForm


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    if request.user.is_professor():
        courses = request.user.courses.all()
        return render(request, 'users/prof_dashboard.html', {'courses': courses})
    enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
    courses = Course.objects.filter(id__in=enrolled_ids)
    all_courses = Course.objects.all()
    return render(
        request,
        'users/student_dashboard.html',
        {'courses': courses, 'all_courses': all_courses},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès. Bienvenue !')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    profile_obj = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile_obj, user=request.user)
    return render(request, 'users/profile.html', {'form': form})
