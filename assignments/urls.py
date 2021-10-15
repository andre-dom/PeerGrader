from django.urls import path, include
import assignments.views

app_name = "assignments"

urlpatterns = [
    path('<slug:course_slug>/new/', assignments.views.assignment_create_view, name='create_assignment'),
    path('<slug:slug>/', assignments.views.assignment_detail_view, name='view_assignment'),
    path('<slug:slug>/delete/', assignments.views.assignment_delete_view, name='delete_assignment'),
    path('<slug:slug>/edit_assignment/', assignments.views.assignment_edit_view, name='edit_assignment'), #1st slug = type, 2nd slug = name
]
