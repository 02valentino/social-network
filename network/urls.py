from django.urls import path
from .views import PostListView
from .views import ProfileView
from .views import PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
]