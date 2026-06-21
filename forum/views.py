from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ForumThread, ForumReply
from .forms import ForumThreadForm, ForumReplyForm


@login_required
def thread_list(request):
    threads = ForumThread.objects.select_related('author', 'course').prefetch_related('replies').all()
    course_id = request.GET.get('course')
    if course_id:
        threads = threads.filter(course_id=course_id)
    return render(request, 'forum/thread_list.html', {'threads': threads})


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(ForumThread.objects.select_related('author', 'course'), pk=pk)
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
        form = ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, 'Discussion créée avec succès.')
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = ForumThreadForm()
    return render(request, 'forum/create_thread.html', {'form': form})
