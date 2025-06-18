from django.urls import path
from .views import PostListView
from .views import ProfileView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]