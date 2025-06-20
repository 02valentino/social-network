from django.urls import path
from .views import PostListView
from .views import ProfileView
from .views import PostCreateView
from .views import ModeratorDashboardView
from .views import ToggleBanUserView, DeleteAnyPostView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('moderator/', ModeratorDashboardView.as_view(), name='moderator-dashboard'),
    path('moderator/toggle-ban/<int:user_id>/', ToggleBanUserView.as_view(), name='toggle-ban'),
    path('moderator/delete-post/<int:post_id>/', DeleteAnyPostView.as_view(), name='delete-post'),
]