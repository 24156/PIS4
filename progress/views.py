from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from courses.models import Course
from .models import Progress
from .forms import ProgressForm

@login_required
def update_progress(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if not request.user.is_professor() or course.professor != request.user:
        raise PermissionDenied

    progress, created = Progress.objects.get_or_create(course=course)
    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = ProgressForm(instance=progress)
    return render(request, 'progress/update_progress.html', {'form': form, 'course': course})
