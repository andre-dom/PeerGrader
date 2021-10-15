from django.urls import path, include
import assignments.views

app_name = "assignments"

urlpatterns = [
    path('<slug:course_slug>/newassignment/', assignments.views.assignment_create_view, name='create_assignment'),
    path('<slug:slug>/', assignments.views.assignment_detail_view, name='view_assignment'),
    path('<slug:slug>/deleteassignment/', assignments.views.assignment_delete_view, name='delete_assignment'),
    path('<slug:slug>/publishassignment/', assignments.views.assignment_publish_view, name='publish_assignment'),
    path('<slug:assignment_slug>/newquestion/', assignments.views.question_create_view, name='create_question'),
    path('<slug:assignment_slug>/editquestion/<int:index>', assignments.views.question_edit_view, name='edit_question'),
    path('<slug:assignment_slug>/deletequestion/<int:index>', assignments.views.question_delete_view, name='delete_question'),
    path('<slug:assignment_slug>/submission', assignments.views.submission_create_view, name='create_submission'),
]
