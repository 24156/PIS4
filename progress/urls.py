from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_pk>/update/', views.update_progress, name='update_progress'),
]
