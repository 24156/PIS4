from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from courses.models import Enrollment
from .models import ForumThread, ForumReply
from .forms import ForumThreadForm, ForumReplyForm


def _user_can_access_course(user, course):
    if not course:
        return True
    if user.is_professor():
        return course.professor == user
    if user.is_student():
        return Enrollment.objects.filter(student=user, course=course).exists()
    return False


@login_required
def thread_list(request):
    threads = ForumThread.objects.select_related('author', 'course').prefetch_related('replies')
    if request.user.is_professor():
        threads = threads.filter(Q(course__isnull=True) | Q(course__professor=request.user))
    elif request.user.is_student():
        enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        threads = threads.filter(Q(course__isnull=True) | Q(course_id__in=enrolled_course_ids))
    else:
        threads = threads.none()
    
    course_id = request.GET.get('course')
    if course_id:
        threads = threads.filter(course_id=course_id)
    return render(request, 'forum/thread_list.html', {'threads': threads})


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(ForumThread.objects.select_related('author', 'course'), pk=pk)
    if not _user_can_access_course(request.user, thread.course):
        raise PermissionDenied
    replies = thread.replies.select_related('author').prefetch_related('attachments').all()

    if request.method == 'POST':
        form = ForumReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.save()
            form.save_attachments(reply)
            messages.success(request, 'Réponse publiée avec succès.')
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ForumReplyForm()

    return render(
        request,
        'forum/thread_detail.html',
        {'thread': thread, 'replies': replies, 'form': form},
    )


@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ForumThreadForm(request.POST, user=request.user)
        if form.is_valid():
            course = form.cleaned_data.get('course')
            if not _user_can_access_course(request.user, course):
                raise PermissionDenied
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, 'Discussion créée avec succès.')
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ForumThreadForm(user=request.user)
    return render(request, 'forum/create_thread.html', {'form': form})
