from django.views.generic import ListView, TemplateView, DetailView, FormView, UpdateView, DeleteView
from .models import Post, Comment, Notification, FriendRequest
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from .forms import PostForm, CommentForm
from django.contrib import messages
from users.models import CustomUser
from django.views import View
from django.db.models import Q
import random

User = get_user_model()

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('post-list')
    return render(request, 'network/welcome.html', {
        'show_auth_links': False
    })

class PostListView(ListView):
    model = Post
    template_name = 'network/post_list.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            friends = user.friends
            return Post.objects.filter(
                Q(author__in=friends) | Q(author=user)
            ).order_by('-posted_at')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_moderator'] = False
        if user.is_authenticated and user.groups.filter(name='Moderator').exists():
            context['is_moderator'] = True
        return context

class ProfileView(DetailView):
    model = User
    template_name = 'network/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        user = self.request.user

        if user.is_authenticated and user != profile_user:
            context['request_sent'] = FriendRequest.objects.filter(sender=user, receiver=profile_user,
                                                                   accepted=False).exists()
            context['request_received'] = FriendRequest.objects.filter(sender=profile_user, receiver=user,
                                                                       accepted=False).exists()
            context['is_friend'] = FriendRequest.objects.filter(
                Q(sender=user, receiver=profile_user) | Q(sender=profile_user, receiver=user),
                accepted=True
            ).exists()
        else:
            context['request_sent'] = False
            context['request_received'] = False
            context['is_friend'] = False

        context['posts_count'] = profile_user.posts.count()
        context['friends_count'] = len(profile_user.friends)
        context['friends'] = profile_user.friends
        context['posts'] = profile_user.posts.order_by('-posted_at')
        return context

class FriendsListView(DetailView):
    model = CustomUser
    template_name = 'network/friends_list.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.get_object().friends
        return context

class UnfriendUserView(LoginRequiredMixin, View):
    def post(self, request, username):
        user = request.user
        other_user = get_object_or_404(CustomUser, username=username)

        friend_request = FriendRequest.objects.filter(
            Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user),
            accepted=True
        ).first()

        if friend_request:
            friend_request.delete()

        return redirect('profile', username=other_user.username)

class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, username):
        to_user = get_object_or_404(CustomUser, username=username)

        if to_user != request.user:
            FriendRequest.objects.filter(
                sender=request.user,
                receiver=to_user,
                accepted=False
            ).delete()

            Notification.objects.filter(
                sender=request.user,
                recipient=to_user,
                message__icontains="sent you a friend request"
            ).delete()

            FriendRequest.objects.create(sender=request.user, receiver=to_user)

        return redirect('profile', username=username)

class CancelFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, username):
        to_user = get_object_or_404(CustomUser, username=username)
        FriendRequest.objects.filter(sender=request.user, receiver=to_user, accepted=False).delete()
        return redirect('profile', username=username)

class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, username):
        from_user = get_object_or_404(CustomUser, username=username)
        fr = FriendRequest.objects.filter(sender=from_user, receiver=request.user, accepted=False).first()
        if fr:
            fr.accepted = True
            fr.save()

            Notification.objects.filter(
                sender=from_user,
                recipient=request.user,
                message__icontains="sent you a friend request"
            ).update(message=f"You and {from_user.username} are now friends.")
        return redirect('profile', username=from_user.username)

class DeclineFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, username):
        from_user = get_object_or_404(CustomUser, username=username)

        Notification.objects.filter(
            sender=from_user,
            recipient=request.user,
            message__icontains="sent you a friend request"
        ).delete()
        FriendRequest.objects.filter(sender=from_user, receiver=request.user, accepted=False).delete()
        return redirect('profile', username=from_user.username)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'network/create_post.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        if self.request.user.is_banned:
            messages.error(self.request, "You are banned from posting.")
            return redirect('post-list')
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content', 'visibility']
    template_name = 'network/edit_post.html'

    def get_success_url(self):
        return reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'network/delete_post.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user == post.author or
            self.request.user.groups.filter(name='Moderator').exists()
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = self.get_context_data()
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context, request)
            from django.http import HttpResponse
            return HttpResponse(html)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object.delete()

            return JsonResponse({
                'success': True,
                'message': 'Post deleted successfully',
                'redirect_url': self.success_url
            })

        return super().post(request, *args, **kwargs)

class PostDetailView(DetailView, FormView):
    model = Post
    template_name = 'network/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = self.get_object()
        comment.save()

        if self.request.user != comment.post.author:
            Notification.objects.create(
                sender=self.request.user,
                recipient=comment.post.author,
                message=f"{self.request.user.username} commented on your post."
            )

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.pk,
                    'content': comment.content,
                    'author': comment.author.username,
                    'author_avatar': comment.author.profile_picture.url if comment.author.profile_picture else None,
                    'created_at': comment.created_at.strftime('%b %d, %Y %H:%M'),
                    'can_edit': True
                },
                'comment_count': self.get_object().comment_count
            })

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.get_form()
        context['comments'] = self.object.comments.select_related('author').all().order_by('-created_at')
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

class ModeratorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'network/mod_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Moderator').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        regular_users = CustomUser.objects.filter(
            is_superuser=False
        ).exclude(groups__name='Moderator')

        context['users'] = regular_users

        context['posts'] = Post.objects.filter(
            author__in=regular_users
        ).order_by('-posted_at')

        return context

class ToggleBanUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Moderator").exists()

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        if user == request.user or user.is_superuser or user.groups.filter(name="Moderator").exists():
            messages.error(request, "You cannot ban this user.")
            return redirect('moderator-dashboard')

        user.is_banned = not user.is_banned
        user.save()
        messages.success(request, f"User {'unbanned' if not user.is_banned else 'banned'}.")
        return redirect('moderator-dashboard')

class DeleteAnyPostView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Moderator').exists()

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect('moderator-dashboard')

class ToggleLikeView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if user.is_authenticated:
            if user in post.liked_by.all():
                post.liked_by.remove(user)
                Notification.objects.filter(
                    sender=user,
                    recipient=post.author,
                    message__icontains="liked your post"
                ).delete()
            else:
                post.liked_by.add(user)
                if user != post.author:
                    Notification.objects.create(
                        sender=user,
                        recipient=post.author,
                        message="liked your post."
                    )
        return redirect(request.META.get('HTTP_REFERER', 'post-list'))

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'network/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        return user == comment.author or user.groups.filter(name='Moderator').exists()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = self.get_context_data()
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context, request)
            from django.http import HttpResponse
            return HttpResponse(html)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post_pk = self.object.post.pk

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object.delete()

            from .models import Post
            post = Post.objects.get(pk=post_pk)
            comment_count = post.comment_count

            return JsonResponse({
                'success': True,
                'message': 'Comment deleted successfully',
                'comment_count': comment_count
            })

        return super().post(request, *args, **kwargs)

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'network/comment_edit.html'

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        return user == comment.author or user.groups.filter(name='Moderator').exists()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            import json
            try:
                data = json.loads(request.body)
                content = data.get('content', '').strip()

                if not content:
                    return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})

                self.object.content = content
                self.object.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Comment updated successfully'
                })
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Invalid data'})

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context

class UserSearchView(ListView):
    model = CustomUser
    template_name = 'network/user_search.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return CustomUser.objects.filter(
                Q(username__icontains=query) |
                Q(location__icontains=query)
            ).exclude(is_superuser=True)
        return CustomUser.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class NotificationListView(ListView):
    model = Notification
    template_name = 'network/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
        qs.update(read=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_friend_requests = FriendRequest.objects.filter(
            receiver=self.request.user,
            accepted=False
        ).values_list('sender__username', flat=True)
        context['active_friend_requests'] = active_friend_requests
        return context

class NotificationDeleteView(DeleteView):
    model = Notification
    success_url = reverse_lazy('notifications')  # or your URL name
    template_name = 'network/confirm_delete.html'

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class DeleteAllNotificationsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request.user.notifications.all().delete()
        return redirect('notifications')

class PostLikesListView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'network/post_likes.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_users'] = self.object.liked_by.all()
        return context

class ExploreView(ListView):
    model = Post
    template_name = 'explore.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            visibility='public'
        ).order_by('-posted_at')

class FriendSuggestionView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'network/friend_suggestions.html'
    context_object_name = 'suggested_users'

    def get_queryset(self):
        user = self.request.user

        sent_requests = FriendRequest.objects.filter(sender=user, accepted=False).values_list('receiver_id', flat=True)
        received_requests = FriendRequest.objects.filter(receiver=user, accepted=False).values_list('sender_id', flat=True)

        friend_ids = [u.id for u in user.friends]

        excluded_ids = friend_ids + [user.id] + list(sent_requests) + list(received_requests)

        candidates = CustomUser.objects.exclude(id__in=excluded_ids).exclude(is_superuser=True)

        return random.sample(list(candidates), min(len(candidates), 10))