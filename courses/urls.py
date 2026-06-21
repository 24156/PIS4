from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:pk>/add-resource/', views.add_resource, name='add_resource'),
    path('<int:pk>/add-assignment/', views.add_assignment, name='add_assignment'),
    path('<int:course_pk>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:pk>/grade/', views.grade_submission, name='grade_submission'),
]
