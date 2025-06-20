from django.views.generic import ListView
from .models import Post, Follow
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib import messages
from users.models import CustomUser
from django.views import View

User = get_user_model()

class PostListView(ListView):
    model = Post
    template_name = 'network/post_list.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']

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
        context['posts'] = self.object.posts.all().order_by('-posted_at')

        user = self.request.user
        profile_user = self.object

        context['user_follows'] = (
                user.is_authenticated and user != profile_user and
                Follow.objects.filter(follower=user, following=profile_user).exists()
        )
        return context

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

class ModeratorDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'network/mod_dashboard.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Moderator').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['posts'] = Post.objects.all().order_by('-posted_at')
        return context

class ToggleBanUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Moderator').exists()

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_banned = not user.is_banned
        user.save()
        return redirect('moderator-dashboard')

class DeleteAnyPostView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Moderator').exists()

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect('moderator-dashboard')