from django.urls import path, include
import assignments.views

app_name = "assignments"

urlpatterns = [
    path('<slug:course_slug>/new/', assignments.views.assignment_create_view, name='create_assignment'),
    path('<slug:slug>/', assignments.views.assignment_detail_view, name='view_assignment'),
]
