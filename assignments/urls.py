from django.urls import path, include
import assignments.views

app_name = "assignments"

urlpatterns = [
    path('<slug:course_slug>/newassignment/', assignments.views.assignment_create_view, name='create_assignment'),
    path('<slug:slug>/', assignments.views.assignment_detail_view, name='view_assignment'),
    path('<slug:slug>/deleteassignment/', assignments.views.assignment_delete_view, name='delete_assignment'),
    path('<slug:slug>/publishassignment/', assignments.views.assignment_publish_view, name='publish_assignment'),
    path('<slug:slug>/close_assignment/', assignments.views.assignment_close_view, name='close_assignment'),
    path('<slug:slug>/edit_assignment/', assignments.views.assignment_edit_view, name='edit_assignment'),
    path('<slug:assignment_slug>/newquestion/', assignments.views.question_create_view, name='create_question'),
    path('<slug:assignment_slug>/editquestion/<int:index>', assignments.views.question_edit_view, name='edit_question'),
    path('<slug:assignment_slug>/deletequestion/<int:index>', assignments.views.question_delete_view,
         name='delete_question'),
    path('<slug:assignment_slug>/submission/<int:index>', assignments.views.question_submission_edit_view, name='edit_submission'),
    path('<slug:assignment_slug>/submission/submit', assignments.views.submit_submission_view, name='submit_submission'),
    path('<slug:assignment_slug>/review/<int:index>', assignments.views.edit_graded_assignment_submission_view, name='edit_graded_assignment_submission_view'),
    path('<slug:assignment_slug>/review/<int:index>/<int:q_index>', assignments.views.edit_graded_question_submission_view, name='edit_graded_question_submission_view'),
]
