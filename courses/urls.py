from django.urls import path, include

import assignments.views
import courses.views

urlpatterns = [
    path('<slug:slug>/', courses.views.course_detail_view, name='view_course'),
    # path('<slug:slug>/assignments/', include('assignments.urls', namespace='assignments')),
]
