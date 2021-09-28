from django.urls import path, include
import courses.views

urlpatterns = [
    path('<slug:slug>/', courses.views.course_detail_view, name='view_course'),

]
