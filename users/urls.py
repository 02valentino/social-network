from django.urls import path
from .views import SignupView, EditProfileView, CustomLoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('edit/', EditProfileView.as_view(), name='edit-profile'),
]