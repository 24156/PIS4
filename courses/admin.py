from django.contrib import admin
from .models import Course, CourseResource, Enrollment, Assignment, Submission


class CourseResourceInline(admin.TabularInline):
    model = CourseResource
    extra = 1


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'professor', 'semester', 'created_at']
    list_filter = ['semester', 'professor']
    search_fields = ['title', 'code']
    inlines = [CourseResourceInline, EnrollmentInline]


@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'resource_type', 'uploaded_at']
    list_filter = ['resource_type']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']
    list_filter = ['course']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'max_score']
    list_filter = ['course']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'status', 'grade', 'submitted_at']
    list_filter = ['status', 'assignment__course']
