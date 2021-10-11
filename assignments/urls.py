from django.urls import path, include
import assignments.views

app_name = "assignments"

urlpatterns = [
    path('<slug:course_slug>/newassignment/', assignments.views.assignment_create_view, name='create_assignment'),
    path('<slug:slug>/', assignments.views.assignment_detail_view, name='view_assignment'),
    path('<slug:slug>/delete/', assignments.views.assignment_delete_view, name='delete_assignment'),
    path('<slug:assignment_slug>/newquestion/', assignments.views.question_create_view, name='create_question'),
]
