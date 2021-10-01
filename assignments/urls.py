from django.urls import path, include
import assignments.views

urlpatterns = [
    path('<slug:slug>/', assignments.views.assignment_detail_view, name='view_assignment'),

]
