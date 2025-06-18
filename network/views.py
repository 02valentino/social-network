from django.views.generic import ListView
from .models import Post
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

User = get_user_model()

class PostListView(ListView):
    model = Post
    template_name = 'network/post_list.html'
    context_object_name = 'posts'
    ordering = ['-posted_at']

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
        return context