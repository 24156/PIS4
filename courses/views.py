from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from common.decorators import professor_required, student_required
from progress.models import Progress
from .models import Course, Assignment, Submission, Enrollment
from .forms import CourseForm, ResourceForm, AssignmentForm, SubmissionForm, GradeSubmissionForm


@login_required
def course_list(request):
    if request.user.is_professor():
        courses = request.user.courses.all()
    else:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=enrolled_ids)
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
@professor_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.professor = request.user
            course.save()
            Progress.objects.get_or_create(course=course)
            messages.success(request, f'Cours "{course.title}" créé avec succès.')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_create.html', {'form': form})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False
    is_course_professor = request.user.is_professor() and course.professor == request.user
    if request.user.is_student():
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        if not is_enrolled:
            messages.warning(request, 'Vous devez vous inscrire à ce cours pour accéder au contenu.')
    elif request.user.is_professor() and not is_course_professor:
        messages.warning(request, 'Vous ne pouvez consulter que vos propres cours.')
    can_access_content = is_enrolled or is_course_professor
    resources = course.resources.all() if can_access_content else []
    assignments = list(course.assignments.all()) if can_access_content else []
    if request.user.is_student() and can_access_content:
        submissions = Submission.objects.filter(assignment__in=assignments, student=request.user)
        sub_dict = {sub.assignment_id: sub for sub in submissions}
        for assignment in assignments:
            assignment.user_submission = sub_dict.get(assignment.id)
    try:
        progress = course.progress
    except Progress.DoesNotExist:
        progress = None
    context = {
        'course': course,
        'resources': resources,
        'assignments': assignments,
        'progress': progress,
        'is_enrolled': is_enrolled,
        'is_course_professor': is_course_professor,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
@student_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, f'Vous êtes déjà inscrit au cours "{course.title}".')
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f'Inscription au cours "{course.title}" confirmée.')
    return redirect('dashboard')


@login_required
@professor_required
def add_resource(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.professor != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course = course
            resource.save()
            messages.success(request, 'Ressource ajoutée avec succès.')
            return redirect('course_detail', pk=course.pk)
    else:
        form = ResourceForm()
    return render(request, 'courses/course_resources.html', {'form': form, 'course': course, 'action': 'add'})


@login_required
@professor_required
def add_assignment(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.professor != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, 'Devoir créé avec succès.')
            return redirect('course_detail', pk=course.pk)
    else:
        form = AssignmentForm()
    return render(request, 'assignments/assignment_create.html', {'form': form, 'course': course})


@login_required
def assignment_list(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.user.is_professor() and course.professor != request.user:
        raise PermissionDenied
    if request.user.is_student():
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            raise PermissionDenied
    assignments = course.assignments.all()
    return render(request, 'assignments/assignment_list.html', {'course': course, 'assignments': assignments})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    course = assignment.course
    if request.user.is_professor() and course.professor != request.user:
        raise PermissionDenied
    if request.user.is_student():
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            raise PermissionDenied
    submission = None
    if request.user.is_student():
        submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    submissions = assignment.submissions.all() if request.user.is_professor() else None
    return render(
        request,
        'assignments/assignment_detail.html',
        {'assignment': assignment, 'course': course, 'submission': submission, 'submissions': submissions},
    )


@login_required
@student_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not Enrollment.objects.filter(student=request.user, course=assignment.course).exists():
        raise PermissionDenied
    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
    if existing and existing.status == 'graded':
        messages.error(request, 'Ce devoir a déjà été noté. Vous ne pouvez plus le modifier.')
        return redirect('assignment_detail', pk=assignment.pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=existing)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.status = 'pending'
            submission.save()
            if existing:
                Submission.objects.filter(pk=submission.pk).update(submitted_at=timezone.now())
            messages.success(
                request,
                'Devoir modifié avec succès.' if existing else 'Devoir soumis avec succès.',
            )
            return redirect('assignment_detail', pk=assignment.pk)
    else:
        form = SubmissionForm(instance=existing)
    return render(
        request,
        'assignments/submit_assignment.html',
        {'form': form, 'assignment': assignment, 'existing': existing},
    )


@login_required
@professor_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if submission.assignment.course.professor != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.graded_at = timezone.now()
            submission.status = 'graded'
            submission.save()
            messages.success(request, 'Note enregistrée avec succès.')
            return redirect('assignment_detail', pk=submission.assignment.pk)
    else:
        form = GradeSubmissionForm(instance=submission)
    return render(
        request,
        'assignments/grade_submission.html',
        {'form': form, 'submission': submission},
    )
