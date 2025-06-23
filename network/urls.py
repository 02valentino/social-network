from django.urls import path
from .views import PostListView
from .views import ProfileView
from .views import PostCreateView
from .views import ModeratorDashboardView
from .views import ToggleBanUserView, DeleteAnyPostView
from .views import FollowUserView, UnfollowUserView
from .views import FollowingFeedView
from .views import ToggleLikeView
from .views import PostDetailView
from .views import PostEditView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('moderator/', ModeratorDashboardView.as_view(), name='moderator-dashboard'),
    path('moderator/toggle-ban/<int:user_id>/', ToggleBanUserView.as_view(), name='toggle-ban'),
    path('moderator/delete-post/<int:post_id>/', DeleteAnyPostView.as_view(), name='delete-post'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/', FollowingFeedView.as_view(), name='following-feed'),
    path('post/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='edit-post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete-post'),
]