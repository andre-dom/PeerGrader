from django.urls import path
from .views import SignUpView, EditUsername

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('newusername/', EditUsername.as_view(), name='change_username'),
]