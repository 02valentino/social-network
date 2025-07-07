from django.urls import path
from .views import SignupView, EditProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('edit/', EditProfileView.as_view(), name='edit-profile'),
]