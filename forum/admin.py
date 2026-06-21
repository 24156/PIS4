from django.contrib import admin
from .models import ForumThread, ForumReply, ForumAttachment


class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    extra = 0


class ForumAttachmentInline(admin.TabularInline):
    model = ForumAttachment
    extra = 0


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'course', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'course']
    search_fields = ['title', 'content']
    inlines = [ForumReplyInline]


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'is_official', 'created_at']
    list_filter = ['is_official']
    inlines = [ForumAttachmentInline]


@admin.register(ForumAttachment)
class ForumAttachmentAdmin(admin.ModelAdmin):
    list_display = ['reply', 'uploaded_at']
