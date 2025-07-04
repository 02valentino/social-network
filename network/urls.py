from django.urls import path
from .views import PostListView
from .views import ProfileView
from .views import PostCreateView
from .views import ModeratorDashboardView
from .views import ToggleBanUserView, DeleteAnyPostView
from .views import ToggleLikeView
from .views import PostDetailView
from .views import PostEditView, PostDeleteView
from .views import CommentDeleteView
from .views import UserSearchView
from .views import NotificationListView
from .views import FriendsListView, UnfriendUserView
from .views import SendFriendRequestView, CancelFriendRequestView, AcceptFriendRequestView, DeclineFriendRequestView
from .views import PostLikesListView
from .views import ExploreView
from .views import FriendSuggestionView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('moderator/', ModeratorDashboardView.as_view(), name='moderator-dashboard'),
    path('moderator/toggle-ban/<int:user_id>/', ToggleBanUserView.as_view(), name='toggle-ban'),
    path('moderator/delete-post/<int:post_id>/', DeleteAnyPostView.as_view(), name='delete-post'),
    path('post/<int:pk>/like/', ToggleLikeView.as_view(), name='toggle-like'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='edit-post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete-post'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('profile/<str:username>/friends/', FriendsListView.as_view(), name='user-friends'),
    path('unfriend/<str:username>/', UnfriendUserView.as_view(), name='unfriend-user'),
    path('friend-request/send/<str:username>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/cancel/<str:username>/', CancelFriendRequestView.as_view(), name='cancel-friend-request'),
    path('friend-request/accept/<str:username>/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('friend-request/decline/<str:username>/', DeclineFriendRequestView.as_view(), name='decline-friend-request'),
    path('post/<int:pk>/likes/', PostLikesListView.as_view(), name='post-likes'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('connect/', FriendSuggestionView.as_view(), name='friend-suggestions'),
]