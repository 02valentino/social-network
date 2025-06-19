from django.urls import path
from .views import SignupView
from .views import EditProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('edit/', EditProfileView.as_view(), name='edit-profile'),
]